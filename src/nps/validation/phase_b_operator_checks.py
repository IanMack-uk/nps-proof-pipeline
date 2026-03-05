from __future__ import annotations

from typing import Callable

import numpy as np

from nps.math.locality import sparsity_support


def _result(*, check_id: str, ok: bool, margin: float | None, witness: dict, notes: str | None = None) -> dict:
    return {
        "check_id": check_id,
        "ok": ok,
        "margin": margin,
        "witness": witness,
        "notes": notes,
    }


def _sample_interior_points(
    *,
    m: int,
    lower: float,
    upper: float,
    n: int,
    rng_seed: int,
    eps: float,
) -> list[np.ndarray]:
    rng = np.random.default_rng(rng_seed)
    lo = lower + eps
    hi = upper - eps
    if not (lo < hi):
        raise ValueError("Invalid interior sampling bounds")
    pts = [0.5 * np.ones(m)]
    for _ in range(max(0, n - 1)):
        pts.append(rng.uniform(lo, hi, size=(m,)).astype(float))
    return pts


def check_operator_matches_grad(
    *,
    grad: Callable[[np.ndarray], np.ndarray],
    F: Callable[[np.ndarray], np.ndarray],
    m: int,
    lower: float,
    upper: float,
    n: int = 4,
    tol: float = 1e-10,
    rng_seed: int = 0,
    interior_eps: float = 1e-12,
) -> dict:
    pts = _sample_interior_points(m=m, lower=lower, upper=upper, n=n, rng_seed=rng_seed, eps=interior_eps)

    worst = -1.0
    worst_w: list[float] | None = None
    for w in pts:
        diff = np.asarray(F(w), dtype=float) - np.asarray(grad(w), dtype=float)
        worst = max(worst, float(np.max(np.abs(diff))))
        if worst_w is None or float(np.max(np.abs(diff))) >= worst:
            worst_w = w.tolist()

    ok = worst <= tol
    return _result(
        check_id="CHK.B.OPERATOR_MATCHES_GRAD",
        ok=ok,
        margin=tol - worst,
        witness={"n": n, "tol": tol, "max_abs_diff": worst, "sample_point": worst_w},
        notes=None,
    )


def check_jacobian_matches_hess(
    *,
    hess: Callable[[np.ndarray], np.ndarray],
    J: Callable[[np.ndarray], np.ndarray],
    m: int,
    lower: float,
    upper: float,
    n: int = 2,
    tol: float = 1e-10,
    rng_seed: int = 0,
    interior_eps: float = 1e-12,
) -> dict:
    pts = _sample_interior_points(m=m, lower=lower, upper=upper, n=n, rng_seed=rng_seed, eps=interior_eps)

    worst = -1.0
    sym_err = -1.0
    for w in pts:
        Hw = np.asarray(hess(w), dtype=float)
        Jw = np.asarray(J(w), dtype=float)
        worst = max(worst, float(np.max(np.abs(Jw - Hw))))
        sym_err = max(sym_err, float(np.max(np.abs(Jw - Jw.T))))

    ok = worst <= tol
    return _result(
        check_id="CHK.B.JACOBIAN_MATCHES_HESS",
        ok=ok,
        margin=tol - worst,
        witness={"n": n, "tol": tol, "max_abs_diff": worst, "symmetry_error": sym_err},
        notes=None,
    )


def check_jacobian_symmetry(*, J: Callable[[np.ndarray], np.ndarray], w: np.ndarray, tol: float = 1e-10) -> dict:
    Jw = np.asarray(J(w), dtype=float)
    symmetry_error = float(np.max(np.abs(Jw - Jw.T)))
    ok = symmetry_error <= tol
    return _result(
        check_id="CHK.B.JACOBIAN_SYMMETRY",
        ok=ok,
        margin=tol - symmetry_error,
        witness={"tol": tol, "symmetry_error": symmetry_error},
        notes=None,
    )


def check_jacobian_locality_sparsity(
    *,
    J: Callable[[np.ndarray], np.ndarray],
    w: np.ndarray,
    neighborhoods: list[set[int]],
    tol: float = 0.0,
) -> dict:
    Jw = np.asarray(J(w), dtype=float)
    support = sparsity_support(Jw, tol=tol)

    violations: list[dict] = []
    max_outside = 0.0
    for i, supp in enumerate(support):
        allowed = set(neighborhoods[i]) | {i}
        extra = sorted(supp - allowed)
        if extra:
            for j in extra:
                max_outside = max(max_outside, float(abs(Jw[i, j])))
            violations.append({"row": i, "extra_support": extra, "allowed": sorted(allowed), "support": sorted(supp)})

    ok = len(violations) == 0
    return _result(
        check_id="CHK.B.JACOBIAN_LOCALITY_SPARSITY",
        ok=ok,
        margin=None,
        witness={"tol": tol, "violations": violations, "max_out_of_neighborhood": max_outside},
        notes=None,
    )


def check_jacobian_invertible_at_wstar(
    *,
    J: Callable[[np.ndarray], np.ndarray],
    w_star: np.ndarray,
    eps: float = 1e-9,
) -> dict:
    Jw = np.asarray(J(w_star), dtype=float)
    svals = np.linalg.svd(Jw, compute_uv=False)
    min_sv = float(np.min(svals))
    max_sv = float(np.max(svals))
    cond_est = float(max_sv / min_sv) if min_sv > 0 else float("inf")

    ok = min_sv >= eps
    return _result(
        check_id="CHK.B.JACOBIAN_INVERTIBLE_AT_WSTAR",
        ok=ok,
        margin=min_sv - eps,
        witness={"eps": eps, "min_singular_value": min_sv, "cond_estimate": cond_est},
        notes=None,
    )


def check_jacobian_conditioning(
    *,
    J: Callable[[np.ndarray], np.ndarray],
    w_star: np.ndarray,
    invertible_eps: float = 1e-9,
    concavity_eps: float = 1e-9,
) -> dict:
    Jw = np.asarray(J(w_star), dtype=float)
    symmetry_error = float(np.max(np.abs(Jw - Jw.T)))
    if symmetry_error <= 1e-8:
        Jw = 0.5 * (Jw + Jw.T)

    try:
        eigvals = np.linalg.eigvals(Jw)
    except Exception as e:  # noqa: BLE001
        return _result(
            check_id="CHK.B.JACOBIAN_CONDITIONING",
            ok=False,
            margin=None,
            witness={
                "error": str(e),
                "symmetry_error": symmetry_error,
                "invertible_eps": invertible_eps,
                "concavity_eps": concavity_eps,
            },
            notes="Failed to compute Jacobian eigenvalues",
        )

    abs_eigs = np.abs(eigvals)
    min_abs = float(np.min(abs_eigs))
    max_abs = float(np.max(abs_eigs))
    cond_est = float(max_abs / min_abs) if min_abs > 0 else float("inf")

    is_hyperbolic = bool(min_abs > invertible_eps)

    # Strict concavity for potential corresponds to negative definite Hessian.
    # Here we check whether all eigenvalues are strictly negative by concavity_eps.
    if symmetry_error <= 1e-8:
        eigvals_real = np.real(eigvals)
        max_eig_real = float(np.max(eigvals_real))
        min_eig_real = float(np.min(eigvals_real))
        is_strictly_concave = bool(max_eig_real < -concavity_eps)
    else:
        max_eig_real = None
        min_eig_real = None
        is_strictly_concave = False

    ok = is_hyperbolic
    return _result(
        check_id="CHK.B.JACOBIAN_CONDITIONING",
        ok=ok,
        margin=min_abs - invertible_eps,
        witness={
            "symmetry_error": symmetry_error,
            "invertible_eps": invertible_eps,
            "concavity_eps": concavity_eps,
            "min_abs_eigenvalue": min_abs,
            "max_abs_eigenvalue": max_abs,
            "condition_estimate": cond_est,
            "min_eigenvalue": min_eig_real,
            "max_eigenvalue": max_eig_real,
            "is_hyperbolic": is_hyperbolic,
            "is_strictly_concave": is_strictly_concave,
        },
        notes=None,
    )
