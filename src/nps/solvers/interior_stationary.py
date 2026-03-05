from __future__ import annotations

from typing import Any, Callable

import numpy as np


def _clip_interior(w: np.ndarray, *, lower: float, upper: float, eps_interior: float) -> np.ndarray:
    lo = lower + eps_interior
    hi = upper - eps_interior
    if not (lo < hi):
        raise ValueError("Invalid interior bounds")
    return np.clip(np.asarray(w, dtype=float), lo, hi)


def find_interior_stationary_point(
    grad_fn: Callable[[np.ndarray], np.ndarray],
    hess_fn: Callable[[np.ndarray], np.ndarray],
    *,
    w_init: np.ndarray,
    lower: float,
    upper: float,
    eps_interior: float = 1e-6,
    tol_grad: float = 1e-8,
    max_iter: int = 200,
    damping: float = 0.5,
    method: str = "damped_newton",
) -> tuple[np.ndarray, dict[str, Any]]:
    """Deterministic interior stationary point finder.

    Uses damped Newton with interior projection. If the Newton system is singular/ill-conditioned,
    falls back to a gradient-descent step for that iteration.

    Returns (w_star, info).
    """

    if method != "damped_newton":
        raise ValueError("Only method='damped_newton' is supported in v0")

    w = _clip_interior(np.asarray(w_init, dtype=float), lower=lower, upper=upper, eps_interior=eps_interior)

    info: dict[str, Any] = {
        "method": method,
        "lower": float(lower),
        "upper": float(upper),
        "eps_interior": float(eps_interior),
        "tol_grad": float(tol_grad),
        "max_iter": int(max_iter),
        "iterations": 0,
        "converged": False,
        "termination_reason": None,
        "final_grad_norm_inf": None,
        "final_grad_norm_2": None,
        "step_norms_2": [],
        "damping_schedule": [],
        "linear_solve": [],
        "backtracking_steps": [],
    }

    def grad_norms(gv: np.ndarray) -> tuple[float, float]:
        return (float(np.linalg.norm(gv, ord=np.inf)), float(np.linalg.norm(gv, ord=2)))

    for it in range(int(max_iter)):
        g = np.asarray(grad_fn(w), dtype=float)
        g_inf, g_2 = grad_norms(g)
        info["iterations"] = it
        info["final_grad_norm_inf"] = g_inf
        info["final_grad_norm_2"] = g_2

        if g_inf <= tol_grad:
            info["converged"] = True
            info["termination_reason"] = "grad_tol"
            break

        H = np.asarray(hess_fn(w), dtype=float)
        symmetric_error = float(np.max(np.abs(H - H.T)))
        if symmetric_error > 1e-8:
            # Use symmetrized Hessian deterministically.
            H = 0.5 * (H + H.T)

        step_type = "newton"
        p: np.ndarray
        try:
            p = np.linalg.solve(H, -g)
            info["linear_solve"].append({"iter": it, "kind": "solve"})
        except Exception as e:  # noqa: BLE001
            step_type = "grad_descent"
            p = -g
            info["linear_solve"].append({"iter": it, "kind": "fallback_grad", "error": str(e)})

        # Backtracking on the gradient infinity norm (deterministic schedule).
        alpha = float(damping)
        bt = 0
        w_next = _clip_interior(w + alpha * p, lower=lower, upper=upper, eps_interior=eps_interior)
        g_next = np.asarray(grad_fn(w_next), dtype=float)
        g_next_inf, _ = grad_norms(g_next)
        while g_next_inf > g_inf and bt < 25:
            alpha *= 0.5
            bt += 1
            w_next = _clip_interior(w + alpha * p, lower=lower, upper=upper, eps_interior=eps_interior)
            g_next = np.asarray(grad_fn(w_next), dtype=float)
            g_next_inf, _ = grad_norms(g_next)

        info["damping_schedule"].append({"iter": it, "alpha": alpha, "step_type": step_type})
        info["backtracking_steps"].append({"iter": it, "steps": bt})

        step_norm = float(np.linalg.norm(w_next - w, ord=2))
        info["step_norms_2"].append(step_norm)

        w = w_next

        if step_norm == 0.0:
            # Projection can cause zero motion; terminate to avoid infinite loop.
            info["termination_reason"] = "no_progress"
            break

    else:
        info["termination_reason"] = "max_iter"

    return (np.asarray(w, dtype=float), info)
