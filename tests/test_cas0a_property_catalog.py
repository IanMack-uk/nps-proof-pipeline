"""Phase 0A/Phase A: CAS-0A property catalog and seed symbol tests (Phase 2)."""

from __future__ import annotations

from nps.certification.dependency_registry import DependencyRegistry
from nps.phases.phase_0a.build_cas0a import (
    F_DEFINED_AS_GRAD_W_PHI,
    LOCALITY_DEFINED_NEIGHBORHOOD,
    LOCALITY_UNIFORM_RADIUS,
    OMEGA_COMPACT,
    OMEGA_NONEMPTY,
    PHI_C3_EXTENSION,
    PHI_CONTINUOUS,
    W_STAR_DEFINED_AS_ARGMAX,
    build_cas0a_registry,
)
from nps.phases.phase_a.build_casa import build_phase_a_symbols


def test_build_registers_minimum_cas0a_keys() -> None:
    registry = DependencyRegistry()
    build_cas0a_registry(registry)

    for key in [
        OMEGA_NONEMPTY,
        OMEGA_COMPACT,
        PHI_CONTINUOUS,
        PHI_C3_EXTENSION,
        LOCALITY_DEFINED_NEIGHBORHOOD,
        LOCALITY_UNIFORM_RADIUS,
        F_DEFINED_AS_GRAD_W_PHI,
        W_STAR_DEFINED_AS_ARGMAX,
    ]:
        assert registry.is_registered(key)


def test_phase_a_seed_symbols_validate() -> None:
    registry = DependencyRegistry()
    build_cas0a_registry(registry)

    symbols = build_phase_a_symbols(registry)
    for name in ["Omega", "Phi", "F", "W_star"]:
        assert name in symbols
