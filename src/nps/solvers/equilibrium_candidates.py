from __future__ import annotations

from typing import Callable

import numpy as np

from nps.solvers.interior_stationary import find_interior_stationary_point


def generate_deterministic_starts(m: int) -> list[np.ndarray]:
    if m <= 0:
        raise ValueError("generate_deterministic_starts: m must be positive")

    starts: list[np.ndarray] = []
    base = np.linspace(0.2, 0.8, num=5)
    for a in base:
        starts.append(np.full(m, a, dtype=float))

    w = np.full(m, 0.5, dtype=float)
    for i in range(min(m, 4)):
        ww = w.copy()
        ww[i] = 0.65
        starts.append(ww)

    uniq: list[np.ndarray] = []
    seen: set[tuple[float, ...]] = set()
    for s in starts:
        key = tuple(np.round(s, 12))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(s)
    return uniq


def classify_hessian_spectrum(eigs: np.ndarray, eps: float = 1e-8) -> dict:
    eigs = np.asarray(eigs, dtype=float)
    if eigs.ndim != 1:
        raise ValueError("classify_hessian_spectrum: eigs must be 1d")

    is_hyperbolic = bool(np.min(np.abs(eigs)) > eps)
    is_neg_def = bool(np.max(eigs) < -eps)
    is_pos_def = bool(np.min(eigs) > eps)
    is_indef = bool((np.min(eigs) < -eps) and (np.max(eigs) > eps))

    neg_count = int(np.sum(eigs < -eps))
    pos_count = int(np.sum(eigs > eps))
    zero_like_count = int(len(eigs) - neg_count - pos_count)

    return {
        "eps": float(eps),
        "min_eigenvalue": float(np.min(eigs)),
        "max_eigenvalue": float(np.max(eigs)),
        "min_abs_eigenvalue": float(np.min(np.abs(eigs))),
        "max_abs_eigenvalue": float(np.max(np.abs(eigs))),
        "neg_count": neg_count,
        "pos_count": pos_count,
        "zero_like_count": zero_like_count,
        "is_hyperbolic": is_hyperbolic,
        "is_neg_def": is_neg_def,
        "is_pos_def": is_pos_def,
        "is_indef": is_indef,
    }


def find_stationary_candidates_multistart(
    grad_fn: Callable[[np.ndarray], np.ndarray],
    hess_fn: Callable[[np.ndarray], np.ndarray],
    *,
    starts: list[np.ndarray],
    lower,
    upper,
    tol_grad: float = 1e-8,
) -> list[dict]:
    candidates: list[dict] = []
    for idx, w_init in enumerate(starts):
        w_star, info = find_interior_stationary_point(
            grad_fn=grad_fn,
            hess_fn=hess_fn,
            w_init=np.asarray(w_init, dtype=float),
            lower=lower,
            upper=upper,
            eps_interior=1e-6,
            tol_grad=tol_grad,
            max_iter=200,
            damping=0.5,
        )

        g = grad_fn(w_star)
        g2 = float(np.linalg.norm(g, ord=2))
        ginf = float(np.linalg.norm(g, ord=np.inf))

        H = hess_fn(w_star)
        Hsym = 0.5 * (H + H.T)
        eigs = np.linalg.eigvalsh(Hsym)
        cls = classify_hessian_spectrum(eigs)

        candidates.append(
            {
                "start_index": idx,
                "w": w_star.tolist(),
                "solver_info": info,
                "grad_norm_2": g2,
                "grad_norm_inf": ginf,
                "hessian_spectrum": cls,
            }
        )

    return candidates


def select_candidate_for_regime(
    candidates: list[dict],
    *,
    objective: str,
    regime: str,
) -> dict | None:
    if objective not in {"maximize", "minimize"}:
        raise ValueError(f"select_candidate_for_regime: invalid objective={objective}")
    if regime not in {"strict_concave", "hyperbolic"}:
        raise ValueError(f"select_candidate_for_regime: invalid regime={regime}")

    feasible: list[dict] = []
    for c in candidates:
        hs = c.get("hessian_spectrum")
        if not isinstance(hs, dict):
            continue

        ok = False
        if regime == "hyperbolic":
            ok = hs.get("is_hyperbolic") is True
        else:
            if objective == "maximize":
                ok = hs.get("is_neg_def") is True
            else:
                ok = hs.get("is_pos_def") is True

        if ok:
            feasible.append(c)

    if not feasible:
        return None

    def key(c: dict) -> tuple[float, float]:
        hs = c["hessian_spectrum"]
        g = float(c.get("grad_norm_2", float("inf")))
        if regime == "hyperbolic":
            margin = float(hs.get("min_abs_eigenvalue", 0.0))
        elif objective == "maximize":
            margin = float(-hs.get("max_eigenvalue", 0.0))
        else:
            margin = float(hs.get("min_eigenvalue", 0.0))
        return (g, -margin)

    return sorted(feasible, key=key)[0]
