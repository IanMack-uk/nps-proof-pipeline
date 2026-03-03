from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from nps.phases.phase_a.coordinates.coordinate_types import CoordinateDefinition, StructuralCoordinate


class EdgeCoordinate(CoordinateDefinition):
    def evaluate(self, e: int, w: NDArray[np.float64]) -> float:
        return float(w[e])


class ZeroCoordinate(CoordinateDefinition):
    def evaluate(self, e: int, w: NDArray[np.float64]) -> float:
        _ = e
        _ = w
        return 0.0


class GlobalSumCoordinate(CoordinateDefinition):
    def evaluate(self, e: int, w: NDArray[np.float64]) -> float:
        _ = e
        return float(np.sum(w))


def coordinate_s_w_e() -> StructuralCoordinate:
    return StructuralCoordinate(
        name="COORD.S.w_e",
        definition=EdgeCoordinate(),
        domain="Omega",
        codomain="R",
        locality="EDGE_ONLY",
        notes="Control S_e coordinate: S_e(w) := w_e.",
    )


def coordinate_r_zero() -> StructuralCoordinate:
    return StructuralCoordinate(
        name="COORD.R.zero",
        definition=ZeroCoordinate(),
        domain="Omega",
        codomain="R",
        locality="EDGE_ONLY",
        notes="Control R_e coordinate: R_e(w) := 0.",
    )


def coordinate_r_sumw_negative_control() -> StructuralCoordinate:
    return StructuralCoordinate(
        name="COORD.R.sumw",
        definition=GlobalSumCoordinate(),
        domain="Omega",
        codomain="R",
        locality="GLOBAL",
        notes="Negative control R_e coordinate: R_e(w) := sum(w).",
    )
