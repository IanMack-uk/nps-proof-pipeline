"""Phase 0A: minimality confirmation over the CAS-0A property catalog.

This test confirms that dropping any single CAS-0A property key breaks
construction of at least one Phase A seed symbol.
"""

from __future__ import annotations

import pytest

from nps.certification.dependency_registry import DependencyRegistry
from nps.core.errors import MathematicalInconsistency
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


def test_each_property_is_individually_required_by_phase_a_seed() -> None:
    keys = [
        OMEGA_NONEMPTY,
        OMEGA_COMPACT,
        PHI_CONTINUOUS,
        PHI_C3_EXTENSION,
        LOCALITY_DEFINED_NEIGHBORHOOD,
        LOCALITY_UNIFORM_RADIUS,
        F_DEFINED_AS_GRAD_W_PHI,
        W_STAR_DEFINED_AS_ARGMAX,
    ]

    for key in keys:
        registry = DependencyRegistry()
        build_cas0a_registry(registry)
        registry.drop(key)

        with pytest.raises(MathematicalInconsistency):
            build_phase_a_symbols(registry)
