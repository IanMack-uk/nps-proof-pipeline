"""Projected optimality residual tests.

Executable model instance — not general certified theory.
"""

from __future__ import annotations

import numpy as np

from nps.models.toy.domains import box_domain
from nps.models.toy.locality import ring_neighborhood
from nps.models.toy.optimality import project_box, projected_residual
from nps.models.toy.potentials_sparse import build_sparse_Q, grad_phi_sparse


def _solve_projected_gradient(
    *,
    theta: float,
    q: np.ndarray,
    m: int,
    steps: int,
    lr: float,
) -> np.ndarray:
    lower, upper = box_domain(m)
    w = np.zeros(m, dtype=np.float64)

    for _ in range(steps):
        grad = grad_phi_sparse(w, theta, q)
        w = project_box(w + lr * grad, lower, upper)

    return w


def test_residual_small_at_equilibrium() -> None:
    m = 8
    radius = 1
    theta = 0.7

    neigh = ring_neighborhood(m, radius)
    q = build_sparse_Q(m, neigh, alpha=4.0, beta=0.1)

    w_star = _solve_projected_gradient(theta=theta, q=q, m=m, steps=800, lr=0.1)
    lower, upper = box_domain(m)
    grad = grad_phi_sparse(w_star, theta, q)

    r = projected_residual(w_star, grad, lower, upper, eta=1e-2)
    assert r < 1e-4


def test_residual_decreases_during_iteration() -> None:
    m = 8
    radius = 1
    theta = 0.7

    neigh = ring_neighborhood(m, radius)
    q = build_sparse_Q(m, neigh, alpha=4.0, beta=0.1)

    lower, upper = box_domain(m)
    w = np.zeros(m, dtype=np.float64)

    residuals: list[float] = []
    steps = 80
    lr = 0.1
    for _ in range(steps):
        grad = grad_phi_sparse(w, theta, q)
        residuals.append(projected_residual(w, grad, lower, upper, eta=1e-2))
        w = project_box(w + lr * grad, lower, upper)

    assert residuals[-1] < residuals[0]
