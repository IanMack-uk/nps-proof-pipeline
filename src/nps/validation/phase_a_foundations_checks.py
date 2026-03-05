from __future__ import annotations

import numpy as np

from nps.math.locality import sparsity_support
from nps.models.quadratic_toy import QuadraticToySpec


def _result(*, check_id: str, ok: bool, margin: float | None, witness: dict, notes: str | None = None) -> dict:
    return {
        "check_id": check_id,
        "ok": ok,
        "margin": margin,
        "witness": witness,
        "notes": notes,
    }


def check_domain_box(m: int, lower: float, upper: float) -> dict:
    ok = m > 0 and lower < upper
    return _result(
        check_id="CHK.A.DOMAIN_BOX",
        ok=ok,
        margin=None,
        witness={"m": m, "lower": lower, "upper": upper},
        notes=None if ok else "Invalid box domain parameters",
    )


def check_grad_finite_difference(
    spec: QuadraticToySpec,
    w: np.ndarray,
    eps: float = 1e-6,
    tol: float = 1e-4,
) -> dict:
    wv = np.asarray(w, dtype=float)
    g_exact = spec.grad(wv)

    g_fd = np.zeros_like(g_exact)
    for i in range(spec.m):
        e = np.zeros(spec.m)
        e[i] = 1.0
        f_plus = spec.value(wv + eps * e)
        f_minus = spec.value(wv - eps * e)
        g_fd[i] = (f_plus - f_minus) / (2.0 * eps)

    err = float(np.linalg.norm(g_exact - g_fd, ord=np.inf))
    ok = err <= tol
    return _result(
        check_id="CHK.A.GRAD_FD",
        ok=ok,
        margin=tol - err,
        witness={"eps": eps, "tol": tol, "err_inf": err, "g_exact": g_exact.tolist(), "g_fd": g_fd.tolist()},
        notes=None,
    )


def check_hess_finite_difference(
    spec: QuadraticToySpec,
    w: np.ndarray,
    eps: float = 1e-5,
    tol: float = 1e-3,
) -> dict:
    wv = np.asarray(w, dtype=float)
    H_exact = spec.hess(wv)

    H_fd = np.zeros_like(H_exact)
    for j in range(spec.m):
        e = np.zeros(spec.m)
        e[j] = 1.0
        g_plus = spec.grad(wv + eps * e)
        g_minus = spec.grad(wv - eps * e)
        H_fd[:, j] = (g_plus - g_minus) / (2.0 * eps)

    err = float(np.linalg.norm(H_exact - H_fd, ord=np.inf))
    ok = err <= tol
    return _result(
        check_id="CHK.A.HESS_FD",
        ok=ok,
        margin=tol - err,
        witness={"eps": eps, "tol": tol, "err_inf": err},
        notes=None,
    )


def check_negative_definite_hessian(A: np.ndarray, *, eps: float = 1e-9) -> dict:
    Av = np.asarray(A, dtype=float)
    symmetry_error = float(np.max(np.abs(Av - Av.T)))
    symmetric_ok = symmetry_error <= 1e-10

    min_eig: float | None
    margin: float | None
    ok: bool
    notes: str | None

    if not symmetric_ok:
        min_eig = None
        margin = None
        ok = False
        notes = "Hessian is not symmetric within tolerance"
    else:
        # Deterministic for small m and matches taskpack guidance.
        eigvals = np.linalg.eigvalsh(Av)
        min_eig = float(np.min(eigvals))
        max_eig = float(np.max(eigvals))
        median_eig = float(np.median(eigvals))
        ok = min_eig < -eps
        margin = (-eps) - min_eig
        notes = None

    return _result(
        check_id="CHK.A.NEG_DEF_HESSIAN",
        ok=ok,
        margin=margin,
        witness={
            "symmetry_error": symmetry_error,
            "min_eigenvalue": min_eig,
            "max_eigenvalue": None if not symmetric_ok else max_eig,
            "eps": eps,
            "spectrum_summary": None
            if not symmetric_ok
            else {"min": min_eig, "median": median_eig, "max": max_eig},
        },
        notes=notes,
    )


def check_interior_feasibility(
    w_star: np.ndarray,
    lower: float,
    upper: float,
    *,
    eps: float = 1e-12,
) -> dict:
    wv = np.asarray(w_star, dtype=float)
    lower_eps = lower + eps
    upper_eps = upper - eps

    violations: list[int] = []
    for i, wi in enumerate(wv.tolist()):
        if not (lower_eps < wi < upper_eps):
            violations.append(int(i))

    slack_low = wv - lower_eps
    slack_high = upper_eps - wv
    min_slack = float(np.min(np.minimum(slack_low, slack_high)))
    ok = len(violations) == 0

    return _result(
        check_id="CHK.A.INTERIOR_FEASIBILITY",
        ok=ok,
        margin=min_slack,
        witness={
            "min_component": float(np.min(wv)),
            "max_component": float(np.max(wv)),
            "min_slack": min_slack,
            "eps": eps,
            "lower": lower,
            "upper": upper,
            "violations": violations,
        },
        notes=None,
    )


def check_locality_by_sparsity(A: np.ndarray, neighborhoods: list[set[int]], *, tol: float = 0.0) -> dict:
    support = sparsity_support(A, tol=tol)
    bad_rows: list[dict] = []
    for i, supp in enumerate(support):
        # Allow self-dependence always.
        allowed = set(neighborhoods[i]) | {i}
        extra = sorted(supp - allowed)
        if extra:
            bad_rows.append({"row": i, "extra_support": extra, "support": sorted(supp), "allowed": sorted(allowed)})

    ok = len(bad_rows) == 0
    return _result(
        check_id="CHK.A.LOCALITY_SPARSITY",
        ok=ok,
        margin=None,
        witness={"tol": tol, "bad_rows": bad_rows},
        notes=None,
    )


def check_stationarity(spec: QuadraticToySpec, w_star: np.ndarray, tol: float = 1e-8) -> dict:
    wv = np.asarray(w_star, dtype=float)
    g = spec.grad(wv)
    err = float(np.linalg.norm(g, ord=np.inf))
    err_2 = float(np.linalg.norm(g, ord=2))
    ok = err <= tol

    interior = bool(np.all(wv > spec.domain_lower) and np.all(wv < spec.domain_upper))

    return _result(
        check_id="CHK.A.STATIONARITY",
        ok=ok,
        margin=tol - err,
        witness={
            "tol": tol,
            "grad_inf": err,
            "grad_2": err_2,
            "interior": interior,
            "w_star_min": float(np.min(wv)),
            "w_star_max": float(np.max(wv)),
        },
        notes=None if interior else "w_star not in open box; stationarity still evaluated at provided w_star",
    )


def check_locality_by_perturbation(
    spec: QuadraticToySpec,
    neighborhoods: list[set[int]],
    w_base: np.ndarray | None = None,
    rng_seed: int = 0,
    tol: float = 1e-8,
) -> dict:
    rng = np.random.default_rng(rng_seed)
    w0 = 0.5 * np.ones(spec.m) if w_base is None else np.asarray(w_base, dtype=float)
    g0 = spec.grad(w0)

    witnesses: list[dict] = []
    ok = True
    for i in range(spec.m):
        allowed = set(neighborhoods[i]) | {i}
        outside = [j for j in range(spec.m) if j not in allowed]
        if not outside:
            continue
        j = int(rng.choice(outside))
        delta = np.zeros(spec.m)
        delta[j] = 1e-3
        g1 = spec.grad(w0 + delta)
        change_i = float(abs(g1[i] - g0[i]))
        if change_i > tol:
            ok = False
            witnesses.append({"row": i, "perturbed_index": j, "change": change_i, "tol": tol})

    return _result(
        check_id="CHK.A.LOCALITY_PERTURB",
        ok=ok,
        margin=None,
        witness={"tol": tol, "counterexamples": witnesses},
        notes=None,
    )
