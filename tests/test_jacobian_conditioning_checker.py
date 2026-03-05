from __future__ import annotations

import numpy as np

from nps.models.quadratic_toy import make_local_quadratic_toy
from nps.validation.phase_b_operator_checks import check_jacobian_conditioning


def test_jacobian_conditioning_checker_reports_hyperbolicity() -> None:
    spec = make_local_quadratic_toy(6, locality_radius=1, seed=0)
    w0 = 0.5 * np.ones(spec.m)

    res = check_jacobian_conditioning(J=lambda w: spec.hess(w), w_star=w0, invertible_eps=1e-9, concavity_eps=1e-9)

    assert res["check_id"] == "CHK.B.JACOBIAN_CONDITIONING"
    assert res["ok"] is True
    wit = res["witness"]
    assert wit["is_hyperbolic"] is True
    assert isinstance(wit["condition_estimate"], float)
    assert isinstance(wit["min_abs_eigenvalue"], float)
