"""Locality invariance tests for toy sparse potential.

Executable model instance — not general certified theory.
"""

from __future__ import annotations

import numpy as np

from nps.models.toy.locality import ring_neighborhood
from nps.models.toy.domains import sample_omega
from nps.models.toy.potentials_sparse import build_sparse_Q, grad_phi_sparse


def test_locality_invariance_outside_neighborhood() -> None:
    rng = np.random.default_rng(0)
    m = 10
    radius = 1
    theta = 0.5

    neigh = ring_neighborhood(m, radius)
    q = build_sparse_Q(m, neigh, alpha=4.0, beta=0.1)

    w = sample_omega(m, rng)

    for e in [0, 3, 7]:
        g = grad_phi_sparse(w, theta, q)[e]
        w2 = w.copy()

        outside = [j for j in range(m) if j not in neigh[e]]
        noise = rng.normal(scale=1e-2, size=len(outside)).astype(np.float64)
        for idx, j in enumerate(outside):
            w2[j] += noise[idx]

        g2 = grad_phi_sparse(w2, theta, q)[e]
        assert abs(float(g - g2)) < 1e-10


def test_locality_negative_control_inside_neighborhood_changes() -> None:
    rng = np.random.default_rng(1)
    m = 10
    radius = 1
    theta = 0.5

    neigh = ring_neighborhood(m, radius)
    q = build_sparse_Q(m, neigh, alpha=4.0, beta=0.1)

    w = sample_omega(m, rng)

    e = 3
    g = grad_phi_sparse(w, theta, q)[e]

    candidates = [j for j in neigh[e] if j != e]
    assert len(candidates) > 0
    j = candidates[0]

    w2 = w.copy()
    w2[j] += 1e-2

    g2 = grad_phi_sparse(w2, theta, q)[e]
    assert abs(float(g - g2)) > 1e-8
