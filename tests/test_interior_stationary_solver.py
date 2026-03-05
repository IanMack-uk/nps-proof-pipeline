from __future__ import annotations

import numpy as np

from nps.models.quadratic_toy import make_local_quadratic_toy
from nps.solvers.interior_stationary import find_interior_stationary_point


def test_interior_stationary_solver_converges_on_quadratic() -> None:
    spec = make_local_quadratic_toy(6, locality_radius=1, seed=0)
    w0 = 0.5 * np.ones(spec.m)

    w_star, info = find_interior_stationary_point(
        grad_fn=lambda w: spec.grad(w),
        hess_fn=lambda w: spec.hess(w),
        w_init=w0,
        lower=spec.domain_lower,
        upper=spec.domain_upper,
        eps_interior=1e-6,
        tol_grad=1e-8,
        max_iter=200,
        damping=0.5,
    )

    assert isinstance(info, dict)
    assert info.get("converged") is True
    assert float(info.get("final_grad_norm_inf")) <= 1e-8
    assert np.all(w_star > spec.domain_lower)
    assert np.all(w_star < spec.domain_upper)
