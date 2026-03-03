from __future__ import annotations

import pytest

from nps.certification.dependency_registry import DependencyRegistry
from nps.core.errors import MathematicalInconsistency
from nps.core.locality import LocalityScope
from nps.core.regularity import RegularityClass
from nps.core.types import MathematicalObject
from nps.phases.phase_0a.build_cas0a import OMEGA_NONEMPTY, build_cas0a_registry
from nps.phases.phase_a.notation_snapshot import render_symbol_dictionary_markdown
from nps.symbols.symbol_dictionary import SymbolDictionary
from nps.certification.citations import source_ref


def test_freeze_prevents_mutation_and_is_versioned() -> None:
    registry = DependencyRegistry()
    build_cas0a_registry(registry)

    symbols = SymbolDictionary(registry=registry)

    omega = MathematicalObject(
        name="Omega",
        domain="TypeSpec:Set",
        codomain="TypeSpec:Subset",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source_ref("CAS-0A-v4", "Assumption A1"),
        requires={OMEGA_NONEMPTY},
    )
    symbols.add(name="Omega", obj=omega)

    symbols.freeze("CAS-A.draft-0")
    assert symbols.is_frozen() is True
    assert symbols.frozen_version == "CAS-A.draft-0"

    with pytest.raises(MathematicalInconsistency, match="frozen"):
        symbols.add(name="Phi", obj=omega)

    with pytest.raises(MathematicalInconsistency, match="frozen"):
        symbols.add(name="Omega", obj=omega)

    with pytest.raises(MathematicalInconsistency, match="already frozen"):
        symbols.freeze("CAS-A.draft-1")


def test_freeze_empty_version_raises() -> None:
    registry = DependencyRegistry()
    build_cas0a_registry(registry)

    symbols = SymbolDictionary(registry=registry)

    with pytest.raises(MathematicalInconsistency):
        symbols.freeze("")


def test_snapshot_renderer_is_deterministic() -> None:
    registry = DependencyRegistry()
    build_cas0a_registry(registry)

    symbols = SymbolDictionary(registry=registry)

    obj = MathematicalObject(
        name="Omega",
        domain="TypeSpec:Set",
        codomain="TypeSpec:Subset",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source_ref("CAS-0A-v4", "Assumption A1"),
        requires={OMEGA_NONEMPTY},
    )

    symbols.add(name="B", obj=obj)
    symbols.add(name="A", obj=obj)

    md1 = render_symbol_dictionary_markdown(symbols)
    md2 = render_symbol_dictionary_markdown(symbols)
    assert md1 == md2
