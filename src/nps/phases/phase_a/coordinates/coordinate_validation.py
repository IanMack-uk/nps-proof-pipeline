from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

from nps.core.errors import MathematicalInconsistency
from nps.phases.phase_a.coordinates.coordinate_types import StructuralCoordinate
from nps.validation.validation_registry import ValidationRegistry

_TOL = 1e-8


def check_phase_b_contract(
    grad_phi_fn: Callable[[NDArray[np.float64], float], NDArray[np.float64]],
    S: StructuralCoordinate,
    R: StructuralCoordinate,
    w: NDArray[np.float64],
    theta: float,
    e: int,
    neighborhood: set[int],
    *,
    registry: ValidationRegistry,
) -> None:
    """Check the Phase B interface contract for a single edge index.

    Contract: F_e(w,θ) depends only on (w_e, S_e(w), R_e(w), θ).

    We search for a deterministic perturbation of w outside `neighborhood` that preserves
    w_e, S_e(w), and R_e(w). If such a perturbation changes F_e, the contract is violated.
    """

    registry.require_assumption_present("CAS-A.CONTRACT.F_DEPENDENCE")

    m = len(w)
    if e < 0 or e >= m:
        raise MathematicalInconsistency("Edge index out of bounds")

    base_w_e = float(w[e])
    base_S = float(S.definition.evaluate(e, w))
    base_R = float(R.definition.evaluate(e, w))
    base_F = float(grad_phi_fn(w, theta)[e])

    outside = [j for j in range(m) if j not in neighborhood]
    outside = [j for j in outside if j != e]
    if len(outside) == 0:
        return

    rng = np.random.default_rng(0)

    def invariants_preserved(w2: NDArray[np.float64]) -> bool:
        if abs(float(w2[e]) - base_w_e) > _TOL:
            return False
        if abs(float(S.definition.evaluate(e, w2)) - base_S) > _TOL:
            return False
        if abs(float(R.definition.evaluate(e, w2)) - base_R) > _TOL:
            return False
        return True

    # First try a structured pair-perturbation which preserves sum(w) if needed.
    if len(outside) >= 2:
        j, k = outside[0], outside[1]
        w2 = w.copy()
        delta = 0.123
        w2[j] = w2[j] + delta
        w2[k] = w2[k] - delta
        if invariants_preserved(w2):
            f2 = float(grad_phi_fn(w2, theta)[e])
            if abs(f2 - base_F) > _TOL:
                raise MathematicalInconsistency("Phase B contract violated")
            return

    # Fallback: search random perturbations until invariants are preserved.
    for _ in range(200):
        w2 = w.copy()
        for j in outside:
            w2[j] = w2[j] + float(rng.normal(scale=0.1))
        if not invariants_preserved(w2):
            continue
        f2 = float(grad_phi_fn(w2, theta)[e])
        if abs(f2 - base_F) > _TOL:
            raise MathematicalInconsistency("Phase B contract violated")
        return

    # If we cannot construct a perturbation that preserves the invariants, treat as inconclusive.
    # (Controls used in tests are constructed so that this search succeeds deterministically.)
    raise MathematicalInconsistency("Unable to construct invariant-preserving perturbation")
