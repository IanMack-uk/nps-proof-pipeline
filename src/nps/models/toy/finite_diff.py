"""Finite-difference utilities.

Executable model instance — not general certified theory.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np


def finite_difference_grad(
    phi: Callable[[np.ndarray, float], float],
    w: np.ndarray,
    theta: float,
    *,
    h: float = 1e-6,
) -> np.ndarray:
    m = len(w)
    grad = np.zeros(m)

    for i in range(m):
        e = np.zeros(m)
        e[i] = 1.0
        grad[i] = (phi(w + h * e, theta) - phi(w - h * e, theta)) / (2 * h)

    return grad
