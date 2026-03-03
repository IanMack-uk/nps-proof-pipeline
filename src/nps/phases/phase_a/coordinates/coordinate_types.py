from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np
from numpy.typing import NDArray

from nps.core.errors import MathematicalInconsistency


class CoordinateDefinition(Protocol):
    def evaluate(self, e: int, w: NDArray[np.float64]) -> float:  # pragma: no cover
        ...


@dataclass(frozen=True)
class StructuralCoordinate:
    name: str
    definition: CoordinateDefinition
    domain: str
    codomain: str
    locality: str
    notes: str

    def evaluate_vector(self, w: NDArray[np.float64], m: int) -> NDArray[np.float64]:
        if w.shape != (m,):
            raise MathematicalInconsistency(f"Coordinate input w must have shape ({m},)")

        x = np.empty(m, dtype=np.float64)
        for e in range(m):
            val = float(self.definition.evaluate(e, w))
            if not np.isfinite(val):
                raise MathematicalInconsistency("Coordinate produced non-finite value")
            x[e] = val

        return x
