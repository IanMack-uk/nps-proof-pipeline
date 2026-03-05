from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

import numpy as np


@dataclass(frozen=True, slots=True)
class OperatorSpec:
    name: str
    definition: str
    derivative_definition: dict
    locality: dict | None


def equilibrium_operator_from_potential(potential: Any) -> Callable[[np.ndarray, float | None], np.ndarray]:
    """Return F(w, theta=None) representing the equilibrium operator.

    For Phase B toy harness, we take F(w) := ∇Φ(w).
    """

    if not hasattr(potential, "grad"):
        raise TypeError("potential must provide grad(w, theta=None)")

    def F(w: np.ndarray, theta: float | None = None) -> np.ndarray:
        return np.asarray(potential.grad(w, theta=theta), dtype=float)

    return F


def jacobian_from_potential(potential: Any) -> Callable[[np.ndarray, float | None], np.ndarray]:
    """Return J(w, theta=None) representing the Jacobian of F.

    For Phase B toy harness, J(w) equals the Hessian of Φ.
    """

    if not hasattr(potential, "hess"):
        raise TypeError("potential must provide hess(w, theta=None)")

    def J(w: np.ndarray, theta: float | None = None) -> np.ndarray:
        return np.asarray(potential.hess(w, theta=theta), dtype=float)

    return J
