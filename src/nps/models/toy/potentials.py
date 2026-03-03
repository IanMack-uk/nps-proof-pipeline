"""Toy smooth potentials.

Executable model instance — not general certified theory.

Implements a simple concave quadratic potential with closed-form gradient.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def phi(w: np.ndarray, theta: float) -> float:
    m = len(w)
    b = theta * np.ones(m)
    q = np.eye(m)
    return float(b @ w - 0.5 * w @ q @ w)


def grad_phi(w: NDArray[np.float64], theta: float) -> NDArray[np.float64]:
    m = len(w)
    b: NDArray[np.float64] = theta * np.ones(m, dtype=np.float64)
    q: NDArray[np.float64] = np.eye(m, dtype=np.float64)
    return b - q @ w
