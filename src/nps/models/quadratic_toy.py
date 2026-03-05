from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class QuadraticToySpec:
    m: int
    A: np.ndarray
    b: np.ndarray
    c: float
    domain_lower: float = 0.0
    domain_upper: float = 1.0
    extension_id: str = "toy_quadratic_v1"

    def value(self, w: np.ndarray, theta: float | None = None) -> float:
        _ = theta
        wv = np.asarray(w, dtype=float)
        return float(0.5 * wv.T @ self.A @ wv + self.b.T @ wv + self.c)

    def grad(self, w: np.ndarray, theta: float | None = None) -> np.ndarray:
        _ = theta
        wv = np.asarray(w, dtype=float)
        return self.A @ wv + self.b

    def hess(self, w: np.ndarray, theta: float | None = None) -> np.ndarray:
        _ = w
        _ = theta
        return self.A


def make_local_quadratic_toy(
    m: int,
    *,
    locality_radius: int,
    line_graph_neighbors: list[list[int]] | None = None,
    seed: int = 0,
) -> QuadraticToySpec:
    """Construct a sparse, symmetric, strictly diagonally dominant negative definite A.

    If `line_graph_neighbors` is not provided, a simple banded neighborhood is used.
    """

    if m <= 0:
        raise ValueError("m must be positive")
    if locality_radius < 0:
        raise ValueError("locality_radius must be nonnegative")

    if line_graph_neighbors is None:
        neighbors: list[list[int]] = []
        for i in range(m):
            lo = max(0, i - locality_radius)
            hi = min(m - 1, i + locality_radius)
            nb = [j for j in range(lo, hi + 1) if j != i]
            neighbors.append(nb)
    else:
        if len(line_graph_neighbors) != m:
            raise ValueError("line_graph_neighbors length must equal m")
        neighbors = [list(nbs) for nbs in line_graph_neighbors]

    rng = np.random.default_rng(seed)

    A = np.zeros((m, m), dtype=float)

    # Symmetric sparse off-diagonals.
    for i in range(m):
        for j in neighbors[i]:
            if j < 0 or j >= m or j == i:
                continue
            if A[i, j] != 0.0:
                continue
            weight = float(rng.uniform(0.01, 0.05))
            # Use a small negative coupling; keep symmetry.
            A[i, j] = -weight
            A[j, i] = -weight

    # Strict diagonal dominance with negative diagonal ensures negative definiteness for symmetric matrices.
    for i in range(m):
        row_sum = float(np.sum(np.abs(A[i, :])))
        A[i, i] = -(row_sum + 1.0)

    # Deterministic interior equilibrium by construction.
    w0 = 0.5 * np.ones(m)
    b = (-A @ w0).astype(float)
    c = 0.0

    return QuadraticToySpec(m=m, A=A, b=b, c=c)
