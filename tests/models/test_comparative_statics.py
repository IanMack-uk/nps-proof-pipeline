"""Comparative statics tests for toy equilibrium correspondence.

Executable model instance — not general certified theory.
"""

from __future__ import annotations

import numpy as np

from nps.models.toy.comparative_statics import (
    active_set,
    equilibria_over_grid,
    kink_flags,
    sensitivity_central,
    step_differences,
)
from nps.models.toy.domains import box_domain
from nps.models.toy.locality import ring_neighborhood
from nps.models.toy.optimality import project_box
from nps.models.toy.potentials_sparse import build_sparse_Q, grad_phi_sparse


def _solve_equilibrium_factory(*, q: np.ndarray, m: int, steps: int = 800, lr: float = 0.1):
    lower, upper = box_domain(m)

    def solve(theta: float) -> np.ndarray:
        w = np.zeros(m, dtype=np.float64)
        for _ in range(steps):
            grad = grad_phi_sparse(w, theta, q)
            w = project_box(w + lr * grad, lower, upper)
        return w

    return solve


def test_continuity_surrogate_in_interior_regime() -> None:
    m = 8
    radius = 1
    neigh = ring_neighborhood(m, radius)
    q = build_sparse_Q(m, neigh, alpha=4.0, beta=0.1)

    solve = _solve_equilibrium_factory(q=q, m=m, steps=800, lr=0.1)

    theta_grid = np.linspace(0.05, 0.2, 6, dtype=np.float64)
    path = equilibria_over_grid(theta_grid, solve)
    diffs = step_differences(path)

    assert float(np.max(diffs)) < 0.2

    for _, w in path:
        assert len(active_set(w)) == 0


def test_kink_detection_or_active_set_nonempty_in_boundary_regime() -> None:
    m = 8
    radius = 1
    neigh = ring_neighborhood(m, radius)
    q = build_sparse_Q(m, neigh, alpha=2.0, beta=0.1)

    solve = _solve_equilibrium_factory(q=q, m=m, steps=800, lr=0.1)

    theta_grid = np.linspace(3.0, 5.0, 6, dtype=np.float64)
    path = equilibria_over_grid(theta_grid, solve)

    tol = 1e-3
    flags = kink_flags(path, tol=tol)
    any_kink = any(flags.values())
    any_active = any(len(active_set(w, tol=tol)) > 0 for _, w in path)

    assert any_kink or any_active


def test_sensitivity_central_shape_and_finite() -> None:
    m = 8
    radius = 1
    neigh = ring_neighborhood(m, radius)
    q = build_sparse_Q(m, neigh, alpha=4.0, beta=0.1)

    solve = _solve_equilibrium_factory(q=q, m=m, steps=800, lr=0.1)

    theta = 0.12
    delta = 1e-2
    sens = sensitivity_central(theta, delta, solve)

    assert sens.shape == (m,)
    assert np.isfinite(sens).all()
