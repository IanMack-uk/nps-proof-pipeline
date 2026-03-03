from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from nps.core.errors import MathematicalInconsistency
from nps.phases.phase_a.coordinates.coordinate_types import CoordinateDefinition, StructuralCoordinate


@dataclass(frozen=True)
class Paper0NeighborhoodSeparation(CoordinateDefinition):
    neighborhoods: dict[int, set[int]]

    def evaluate(self, e: int, w: NDArray[np.float64]) -> float:
        n = self.neighborhoods.get(e)
        if n is None:
            raise MathematicalInconsistency("Missing neighborhood for edge")
        alt = [j for j in n if j != e]
        s = float(np.sum(w[np.array(alt, dtype=int)])) if len(alt) else 0.0
        # Proxy for "separation": decreases when alternative paths strengthen.
        return 1.0 / (1.0 + max(0.0, s))


@dataclass(frozen=True)
class Paper0NeighborhoodRedundancy(CoordinateDefinition):
    neighborhoods: dict[int, set[int]]

    def evaluate(self, e: int, w: NDArray[np.float64]) -> float:
        n = self.neighborhoods.get(e)
        if n is None:
            raise MathematicalInconsistency("Missing neighborhood for edge")
        alt = [j for j in n if j != e]
        if not alt:
            return 0.0
        v = w[np.array(alt, dtype=int)]
        # Proxy for "redundancy": increases with strengthened short-cycle alternatives.
        vp = np.maximum(v, 0.0)
        return float(np.sum(np.square(vp)))


def paper0_separation_candidate(neighborhoods: dict[int, set[int]]) -> StructuralCoordinate:
    return StructuralCoordinate(
        name="P0.S.neighborhood_proxy",
        definition=Paper0NeighborhoodSeparation(neighborhoods=neighborhoods),
        domain="Omega",
        codomain="R",
        locality="NEIGHBORHOOD_N(e)",
        notes="Paper 0 provisional separation proxy computed from bounded neighborhood N(e).",
    )


def paper0_redundancy_candidate(neighborhoods: dict[int, set[int]]) -> StructuralCoordinate:
    return StructuralCoordinate(
        name="P0.R.neighborhood_proxy",
        definition=Paper0NeighborhoodRedundancy(neighborhoods=neighborhoods),
        domain="Omega",
        codomain="R",
        locality="NEIGHBORHOOD_N(e)",
        notes="Paper 0 provisional redundancy proxy computed from bounded neighborhood N(e).",
    )
