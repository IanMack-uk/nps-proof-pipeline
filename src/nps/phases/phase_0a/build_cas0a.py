"""Phase 0A: build utilities (dependency certification)."""

from __future__ import annotations

from nps.certification.citations import source_ref
from nps.certification.dependency_registry import DependencyRegistry, PropertyKey
from nps.core.types import SourceRef


OMEGA_NONEMPTY = PropertyKey(subject="Omega", property="nonempty")
OMEGA_COMPACT = PropertyKey(subject="Omega", property="compact")

PHI_CONTINUOUS = PropertyKey(subject="Phi", property="continuous")
PHI_C3_EXTENSION = PropertyKey(subject="Phi", property="C3_extension")

LOCALITY_DEFINED_NEIGHBORHOOD = PropertyKey(subject="Locality", property="defined_neighborhood_N(e)")
LOCALITY_UNIFORM_RADIUS = PropertyKey(subject="Locality", property="uniform_radius_r")

F_DEFINED_AS_GRAD_W_PHI = PropertyKey(subject="F", property="defined_as_grad_w_Phi")

W_STAR_DEFINED_AS_ARGMAX = PropertyKey(subject="W_star", property="defined_as_argmax_over_Omega")


def build_cas0a_registry(registry: DependencyRegistry) -> None:
    """Register CAS-0A certified properties with exact SourceRef locators."""

    def cas0a(locator: str) -> SourceRef:
        return source_ref("CAS-0A-v4", locator)

    registry.register(property_key=OMEGA_NONEMPTY, source=cas0a("Assumption A1"))
    registry.register(property_key=OMEGA_COMPACT, source=cas0a("Assumption A1"))

    registry.register(property_key=PHI_CONTINUOUS, source=cas0a("Assumption A2"))
    registry.register(property_key=PHI_C3_EXTENSION, source=cas0a("Assumption A3"))

    registry.register(property_key=LOCALITY_DEFINED_NEIGHBORHOOD, source=cas0a("Assumption A5"))
    registry.register(property_key=LOCALITY_UNIFORM_RADIUS, source=cas0a("Assumption A7"))

    registry.register(property_key=F_DEFINED_AS_GRAD_W_PHI, source=cas0a("Definition 4.1"))
    registry.register(property_key=W_STAR_DEFINED_AS_ARGMAX, source=cas0a("Definition 7.1"))


def cas0a_dependency_rows(registry: DependencyRegistry) -> list[tuple[PropertyKey, SourceRef]]:
    """Return a stable, sortable list for audit reporting."""

    return registry.rows()


def build_registry() -> DependencyRegistry:
    return DependencyRegistry()
