"""Projected optimality checks for box constraints.

Executable model instance — not general certified theory.

Implements a projected-gradient residual for Ω = [0,1]^m.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def project_box(
    w: NDArray[np.float64],
    lower: NDArray[np.float64],
    upper: NDArray[np.float64],
) -> NDArray[np.float64]:
    return np.minimum(np.maximum(w, lower), upper)


def projected_residual(
    w: NDArray[np.float64],
    grad: NDArray[np.float64],
    lower: NDArray[np.float64],
    upper: NDArray[np.float64],
    *,
    eta: float = 1e-2,
) -> float:
    w_step = w + eta * grad
    w_proj = project_box(w_step, lower, upper)
    return float(np.linalg.norm(w - w_proj))
