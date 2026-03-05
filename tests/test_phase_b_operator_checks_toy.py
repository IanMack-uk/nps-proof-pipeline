from __future__ import annotations

import numpy as np

from nps.math.locality import sparsity_support
from nps.models.quadratic_toy import make_local_quadratic_toy
from nps.operators.equilibrium_operator import equilibrium_operator_from_potential, jacobian_from_potential
from nps.validation.phase_b_operator_checks import (
    check_jacobian_invertible_at_wstar,
    check_jacobian_locality_sparsity,
    check_jacobian_matches_hess,
    check_jacobian_symmetry,
    check_operator_matches_grad,
)


def test_phase_b_operator_checks_toy() -> None:
    spec = make_local_quadratic_toy(8, locality_radius=1, seed=0)
    w0 = 0.5 * np.ones(spec.m)

    F = equilibrium_operator_from_potential(spec)
    J = jacobian_from_potential(spec)

    neighborhoods = [set(s) for s in sparsity_support(spec.A, tol=0.0)]

    checks = [
        check_operator_matches_grad(
            grad=lambda w: spec.grad(w),
            F=lambda w: F(w),
            m=spec.m,
            lower=spec.domain_lower,
            upper=spec.domain_upper,
        ),
        check_jacobian_matches_hess(
            hess=lambda w: spec.hess(w),
            J=lambda w: J(w),
            m=spec.m,
            lower=spec.domain_lower,
            upper=spec.domain_upper,
        ),
        check_jacobian_symmetry(J=lambda w: J(w), w=w0),
        check_jacobian_locality_sparsity(J=lambda w: J(w), w=w0, neighborhoods=neighborhoods, tol=0.0),
        check_jacobian_invertible_at_wstar(J=lambda w: J(w), w_star=w0, eps=1e-9),
    ]

    assert all(c["ok"] is True for c in checks)
