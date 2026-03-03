"""Phase 0A: freeze enforcement.

After CAS-0A approval, the registry must reject any further mutation.
"""

from __future__ import annotations

import pytest

from nps.certification.citations import source_ref
from nps.certification.dependency_registry import DependencyRegistry, PropertyKey
from nps.core.errors import MathematicalInconsistency
from nps.phases.phase_0a.build_cas0a import build_cas0a_registry


def test_registry_rejects_register_after_freeze() -> None:
    registry = DependencyRegistry()
    build_cas0a_registry(registry)
    registry.freeze()

    with pytest.raises(MathematicalInconsistency, match="Registry is frozen"):
        registry.register(
            property_key=PropertyKey(subject="X", property="y"),
            source=source_ref("CAS-0A-v4", "Assumption A0"),
        )


def test_registry_rejects_drop_after_freeze() -> None:
    registry = DependencyRegistry()
    build_cas0a_registry(registry)
    registry.freeze()

    with pytest.raises(MathematicalInconsistency, match="Registry is frozen"):
        registry.drop(PropertyKey(subject="Omega", property="nonempty"))
