"""Equilibrium checks for toy models.

Executable model instance — not general certified theory.
"""

from __future__ import annotations

import numpy as np

from nps.models.toy.domains import box_domain
from nps.models.toy.domains import sample_omega
from nps.models.toy.equilibrium import equilibrium
from nps.models.toy.potentials import grad_phi, phi


def test_equilibrium_within_bounds_and_high_value() -> None:
    rng = np.random.default_rng(0)
    m = 4
    theta = 1.3

    w_star = equilibrium(theta, m, steps=400, lr=0.1)
    lower, upper = box_domain(m)

    assert np.all(w_star >= lower - 1e-12)
    assert np.all(w_star <= upper + 1e-12)

    g = grad_phi(w_star, theta)
    tol = 1e-3
    interior = (w_star > lower + 1e-6) & (w_star < upper - 1e-6)
    if np.any(interior):
        assert float(np.max(np.abs(g[interior]))) < tol

    at_lower = w_star <= lower + 1e-6
    if np.any(at_lower):
        assert float(np.max(g[at_lower])) <= tol

    at_upper = w_star >= upper - 1e-6
    if np.any(at_upper):
        assert float(np.min(g[at_upper])) >= -tol

    phi_star = phi(w_star, theta)
    for _ in range(20):
        w = sample_omega(m, rng)
        assert phi_star >= phi(w, theta) - 1e-6
