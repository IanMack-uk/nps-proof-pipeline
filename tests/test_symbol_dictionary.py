"""Phase A: tests for SymbolDictionary gating rules."""

from __future__ import annotations

import pytest

from nps.certification.citations import source_ref
from nps.certification.dependency_registry import DependencyRegistry, PropertyKey
from nps.core.errors import MathematicalInconsistency
from nps.core.locality import LocalityScope
from nps.core.regularity import RegularityClass
from nps.core.types import MathematicalObject
from nps.symbols.symbol_dictionary import SymbolDictionary


def test_symbol_requires_registered_dependency() -> None:
    reg = DependencyRegistry()
    symbols = SymbolDictionary(registry=reg)
    req = PropertyKey(subject="X", property="definition")

    obj = MathematicalObject(
        name="X",
        domain="A",
        codomain="B",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source_ref("SRC", "Definition of X"),
        requires={req},
    )

    with pytest.raises(MathematicalInconsistency):
        symbols.add(name="X", obj=obj)


def test_symbol_add_and_get() -> None:
    reg = DependencyRegistry()
    req = PropertyKey(subject="X", property="definition")
    reg.register(property_key=req, source=source_ref("SRC", "Axiom x"))

    symbols = SymbolDictionary(registry=reg)
    obj = MathematicalObject(
        name="X",
        domain="A",
        codomain="B",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source_ref("SRC", "Definition of X"),
        requires={req},
    )

    symbols.add(name="X", obj=obj)
    assert "X" in symbols
    assert symbols.get("X").obj.name == "X"
