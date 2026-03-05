from __future__ import annotations

import numpy as np

from nps.models.quadratic_toy import make_local_quadratic_toy
from nps.validation.phase_a_foundations_checks import check_grad_finite_difference, check_hess_finite_difference


def test_quadratic_toy_grad_matches_finite_difference() -> None:
    spec = make_local_quadratic_toy(6, locality_radius=1, seed=0)
    w = 0.5 * np.ones(spec.m)
    res = check_grad_finite_difference(spec, w, eps=1e-6, tol=1e-4)
    assert res["ok"] is True


def test_quadratic_toy_hess_matches_finite_difference() -> None:
    spec = make_local_quadratic_toy(6, locality_radius=1, seed=1)
    w = 0.5 * np.ones(spec.m)
    res = check_hess_finite_difference(spec, w, eps=1e-5, tol=1e-3)
    assert res["ok"] is True
