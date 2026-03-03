from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from nps.certification.dependency_registry import PropertyKey
from nps.models.toy.potentials import grad_phi
from nps.phases.phase_a.exposure.exposure_types import ExposureDefinition, ExposureLocality, ExposureRegularity, StructuralExposure


class EdgeCoordinateExposure(ExposureDefinition):
    def evaluate(self, e: int, w: NDArray[np.float64], theta: float) -> float:
        _ = theta
        return float(w[e])


class AbsGradientExposure(ExposureDefinition):
    def evaluate(self, e: int, w: NDArray[np.float64], theta: float) -> float:
        g = grad_phi(w, theta)
        return float(np.abs(g[e]))


def exposure_w_e() -> StructuralExposure:
    return StructuralExposure(
        name="EXP.w_e",
        definition=EdgeCoordinateExposure(),
        domain="Omega",
        codomain="R",
        regularity=ExposureRegularity.SMOOTH.value,
        locality=ExposureLocality.EDGE_ONLY.value,
        requires_properties=set(),
        notes="Control exposure: E_e(w) := w_e.",
    )


def exposure_abs_f() -> StructuralExposure:
    return StructuralExposure(
        name="EXP.absF",
        definition=AbsGradientExposure(),
        domain="Omega×Theta",
        codomain="R_+",
        regularity=ExposureRegularity.C1.value,
        locality=ExposureLocality.NEIGHBORHOOD_N_E.value,
        requires_properties={
            PropertyKey(subject="F", property="defined_as_grad_w_Phi"),
            PropertyKey(subject="Locality", property="defined_neighborhood_N(e)"),
            PropertyKey(subject="Locality", property="uniform_radius_r"),
        },
        notes="Control exposure: E_e(w,θ) := |F_e(w,θ)| with F computed from toy grad_phi.",
    )
