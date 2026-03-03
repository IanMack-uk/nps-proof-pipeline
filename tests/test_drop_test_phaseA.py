"""Phase Aʹ: minimal drop-test enforcement."""

from __future__ import annotations

import pytest

from nps.certification.citations import source_ref
from nps.certification.dependency_registry import DependencyRegistry, PropertyKey
from nps.core.errors import MathematicalInconsistency
from nps.core.locality import LocalityScope
from nps.core.regularity import RegularityClass
from nps.core.types import MathematicalObject
from nps.phases.phase_a_prime.closure import certify_minimality
from nps.symbols.symbol_dictionary import SymbolDictionary


def test_drop_test_fails_when_required_dependency_removed() -> None:
    reg = DependencyRegistry()
    required = PropertyKey(subject="Phi", property="C3_extension")
    reg.register(property_key=required, source=source_ref("SRC", "C3 extension for Phi"))

    symbols = SymbolDictionary(registry=reg)
    obj = MathematicalObject(
        name="Phi",
        domain="A",
        codomain="B",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source_ref("SRC", "Definition of Phi"),
        requires={required},
    )
    symbols.add(name="Phi", obj=obj)

    certify_minimality(registry=reg, symbols=symbols)

    reg.drop(required)
    with pytest.raises(MathematicalInconsistency):
        certify_minimality(registry=reg, symbols=symbols)
