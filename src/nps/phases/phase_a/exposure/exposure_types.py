from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

from nps.certification.dependency_registry import PropertyKey
from nps.core.errors import MathematicalInconsistency

if TYPE_CHECKING:
    from nps.validation.validation_registry import ValidationRegistry


class ExposureRegularity(str, Enum):
    C0 = "C0"
    C1 = "C1"
    C2 = "C2"
    SMOOTH = "SMOOTH"
    UNKNOWN = "UNKNOWN"


class ExposureLocality(str, Enum):
    EDGE_ONLY = "EDGE_ONLY"
    NEIGHBORHOOD_N_E = "NEIGHBORHOOD_N(e)"
    UNKNOWN = "UNKNOWN"


class ExposureDefinition(Protocol):
    def evaluate(self, e: int, w: NDArray[np.float64], theta: float) -> float:  # pragma: no cover
        ...


@dataclass(frozen=True)
class StructuralExposure:
    name: str
    definition: ExposureDefinition
    domain: str
    codomain: str
    regularity: str
    locality: str
    requires_properties: set[PropertyKey]
    notes: str

    def evaluate_vector(
        self,
        w: NDArray[np.float64],
        theta: float,
        m: int,
        *,
        registry: "ValidationRegistry",
    ) -> NDArray[np.float64]:
        registry.require_assumption_present("CAS-A.EXP.WELLPOSED")
        if w.shape != (m,):
            raise MathematicalInconsistency(f"Exposure input w must have shape ({m},)")

        x = np.empty(m, dtype=np.float64)
        for e in range(m):
            val = float(self.definition.evaluate(e, w, theta))
            if not np.isfinite(val):
                raise MathematicalInconsistency("Exposure produced non-finite value")
            x[e] = val

        return x
