from __future__ import annotations

import numpy as np

from nps.math.locality import sparsity_support
from nps.models.quadratic_toy import make_local_quadratic_toy
from nps.validation.phase_a_foundations_checks import check_locality_by_sparsity


def test_quadratic_toy_locality_by_sparsity() -> None:
    spec = make_local_quadratic_toy(8, locality_radius=1, seed=0)
    neighborhoods = [set(s) for s in sparsity_support(spec.A, tol=0.0)]
    res = check_locality_by_sparsity(spec.A, neighborhoods, tol=0.0)
    assert res["ok"] is True
