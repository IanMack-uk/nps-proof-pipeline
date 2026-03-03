from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from nps.core.errors import MathematicalInconsistency
from nps.phases.phase_a.exposure.exposure_types import StructuralExposure
from nps.validation.validation_registry import ValidationRegistry

_TOL = 1e-8


def assert_finite_vector(x: NDArray[np.float64]) -> None:
    if x.ndim != 1:
        raise MathematicalInconsistency("Exposure vector must be 1D")
    if not np.all(np.isfinite(x)):
        raise MathematicalInconsistency("Exposure vector must be finite")


def check_edge_only_locality(
    exposure: StructuralExposure,
    w: NDArray[np.float64],
    theta: float,
    e: int,
    *,
    registry: ValidationRegistry,
) -> None:
    registry.require_assumption_present("CAS-A.EXP.LOCALITY")
    m = len(w)
    base = float(exposure.definition.evaluate(e, w, theta))

    rng = np.random.default_rng(0)
    w2 = w.copy()
    for j in range(m):
        if j == e:
            continue
        w2[j] = w2[j] + float(rng.normal(scale=0.1))

    val2 = float(exposure.definition.evaluate(e, w2, theta))
    if abs(val2 - base) > _TOL:
        raise MathematicalInconsistency("Exposure violates EDGE_ONLY locality")


def check_neighborhood_locality(
    exposure: StructuralExposure,
    w: NDArray[np.float64],
    theta: float,
    e: int,
    neighborhood: set[int],
    *,
    registry: ValidationRegistry,
) -> None:
    registry.require_assumption_present("CAS-A.EXP.LOCALITY")
    m = len(w)
    base = float(exposure.definition.evaluate(e, w, theta))

    rng = np.random.default_rng(0)
    w2 = w.copy()
    for j in range(m):
        if j in neighborhood:
            continue
        w2[j] = w2[j] + float(rng.normal(scale=0.1))

    val2 = float(exposure.definition.evaluate(e, w2, theta))
    if abs(val2 - base) > _TOL:
        raise MathematicalInconsistency("Exposure violates neighborhood locality")
