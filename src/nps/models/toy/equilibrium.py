"""Toy equilibrium solver.

Executable model instance — not general certified theory.

Implements projected gradient ascent for box constraints.
"""

from __future__ import annotations

from typing import cast

import numpy as np
from numpy.typing import NDArray

from nps.models.toy.domains import box_domain
from nps.models.toy.potentials import grad_phi


def project_box(
    w: NDArray[np.float64],
    lower: NDArray[np.float64],
    upper: NDArray[np.float64],
) -> NDArray[np.float64]:
    return cast(NDArray[np.float64], np.minimum(np.maximum(w, lower), upper))


def equilibrium(theta: float, m: int, *, steps: int = 200, lr: float = 0.1) -> NDArray[np.float64]:
    lower, upper = box_domain(m)
    lower_f = cast(NDArray[np.float64], lower.astype(np.float64, copy=False))
    upper_f = cast(NDArray[np.float64], upper.astype(np.float64, copy=False))
    w = cast(NDArray[np.float64], np.zeros(m, dtype=np.float64))

    for _ in range(steps):
        w = w + lr * grad_phi(w, theta)
        w = project_box(w, lower_f, upper_f)

    return w
