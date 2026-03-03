"""Comparative statics harness for toy equilibrium correspondence.

Executable model instance — not general certified theory.

Computes w*(θ) over grids, step differences, sensitivity, and kink flags based
on box-constraint active sets.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Dict, List, Set, Tuple

import numpy as np
from numpy.typing import NDArray


def active_set(w: NDArray[np.float64], tol: float = 1e-6) -> Set[int]:
    """Return indices i where w_i is within tol of 0 or 1."""

    a: Set[int] = set()
    for i, wi in enumerate(w):
        if float(wi) <= tol or float(wi) >= 1.0 - tol:
            a.add(i)
    return a


def equilibria_over_grid(
    theta_grid: NDArray[np.float64],
    solve_equilibrium: Callable[[float], NDArray[np.float64]],
) -> List[Tuple[float, NDArray[np.float64]]]:
    """Compute (theta, w*(theta)) over a grid."""

    out: List[Tuple[float, NDArray[np.float64]]] = []
    for th in theta_grid:
        out.append((float(th), solve_equilibrium(float(th))))
    return out


def step_differences(path: List[Tuple[float, NDArray[np.float64]]]) -> NDArray[np.float64]:
    """Return array of ||w*(θ_{k+1}) - w*(θ_k)|| for successive grid points."""

    diffs: list[float] = []
    for k in range(len(path) - 1):
        diffs.append(float(np.linalg.norm(path[k + 1][1] - path[k][1])))
    return np.asarray(diffs, dtype=np.float64)


def sensitivity_central(
    theta: float,
    delta: float,
    solve_equilibrium: Callable[[float], NDArray[np.float64]],
) -> NDArray[np.float64]:
    """Estimate dw*/dθ via central difference."""

    w_plus = solve_equilibrium(theta + delta)
    w_minus = solve_equilibrium(theta - delta)
    return (w_plus - w_minus) / (2.0 * delta)


def kink_flags(
    path: List[Tuple[float, NDArray[np.float64]]],
    tol: float = 1e-6,
) -> Dict[float, bool]:
    """Return {theta_k: True/False} for whether active set changes after theta_k."""

    flags: Dict[float, bool] = {}
    for k in range(len(path) - 1):
        th = path[k][0]
        a0 = active_set(path[k][1], tol=tol)
        a1 = active_set(path[k + 1][1], tol=tol)
        flags[th] = a0 != a1
    if path:
        flags[path[-1][0]] = False
    return flags
