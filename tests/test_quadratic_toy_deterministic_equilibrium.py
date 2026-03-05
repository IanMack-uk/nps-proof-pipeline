from __future__ import annotations

import numpy as np

from nps.models.quadratic_toy import make_local_quadratic_toy
from nps.validation.phase_a_foundations_checks import check_negative_definite_hessian


def test_quadratic_toy_deterministic_equilibrium_is_interior_and_stationary() -> None:
    spec = make_local_quadratic_toy(8, locality_radius=1, seed=0)
    w0 = 0.5 * np.ones(spec.m)

    assert float(np.min(w0)) > spec.domain_lower
    assert float(np.max(w0)) < spec.domain_upper

    g = spec.grad(w0)
    assert float(np.linalg.norm(g, ord=np.inf)) <= 1e-12

    res = check_negative_definite_hessian(spec.A)
    assert res["ok"] is True
