"""Gradient checks for toy models.

Executable model instance — not general certified theory.
"""

from __future__ import annotations

import numpy as np

from nps.models.toy.finite_diff import finite_difference_grad
from nps.models.toy.domains import sample_omega
from nps.models.toy.potentials import grad_phi, phi


def test_grad_phi_matches_finite_difference() -> None:
    rng = np.random.default_rng(0)
    m = 5
    theta = 1.7

    w = 0.2 + 0.6 * sample_omega(m, rng)
    g_true = grad_phi(w, theta)
    g_fd = finite_difference_grad(phi, w, theta)

    err = np.max(np.abs(g_true - g_fd))
    assert err < 1e-5
