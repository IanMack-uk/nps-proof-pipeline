"""Toy locality-aware quadratic potentials.

Executable model instance — not general certified theory.

Constructs a symmetric, diagonally-dominant quadratic form so that the gradient
component F_e depends only on weights w[j] for j ∈ N(e).
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from nps.models.toy.locality import check_neighborhood


def build_sparse_Q(
    m: int,
    neigh: dict[int, set[int]],
    *,
    alpha: float = 2.0,
    beta: float = 0.1,
) -> NDArray[np.float64]:
    check_neighborhood(neigh, m)
    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if beta < 0.0:
        raise ValueError("beta must be nonnegative")

    q: NDArray[np.float64] = alpha * np.eye(m, dtype=np.float64)
    for e in range(m):
        for j in neigh[e]:
            if j == e:
                continue
            q[e, j] += beta
            q[j, e] += beta

    return q


def phi_sparse(w: NDArray[np.float64], theta: float, q: NDArray[np.float64]) -> float:
    m = len(w)
    b = theta * np.ones(m, dtype=np.float64)
    return float(b @ w - 0.5 * w @ q @ w)


def grad_phi_sparse(w: NDArray[np.float64], theta: float, q: NDArray[np.float64]) -> NDArray[np.float64]:
    m = len(w)
    b: NDArray[np.float64] = theta * np.ones(m, dtype=np.float64)
    return b - q @ w
