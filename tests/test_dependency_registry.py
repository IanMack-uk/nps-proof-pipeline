"""Phase 0A: tests for DependencyRegistry."""

from __future__ import annotations

import pytest

from nps.certification.citations import source_ref
from nps.certification.dependency_registry import DependencyRegistry, PropertyKey
from nps.core.errors import MathematicalInconsistency


def test_register_and_require_roundtrip() -> None:
    reg = DependencyRegistry()
    key = PropertyKey(subject="Phi", property="C3_extension")
    reg.register(property_key=key, source=source_ref("SRC", "Foo axiom"))

    cert = reg.require(key)
    assert cert.property_key == key


def test_duplicate_register_fails() -> None:
    reg = DependencyRegistry()
    key = PropertyKey(subject="Phi", property="C3_extension")
    reg.register(property_key=key, source=source_ref("SRC", "Foo axiom"))

    with pytest.raises(MathematicalInconsistency):
        reg.register(property_key=key, source=source_ref("SRC", "Foo axiom"))


def test_drop_unknown_fails() -> None:
    reg = DependencyRegistry()

    with pytest.raises(MathematicalInconsistency):
        reg.drop(PropertyKey(subject="Phi", property="missing"))
