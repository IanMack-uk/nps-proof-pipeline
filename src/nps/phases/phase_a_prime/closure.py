"""Phase Aʹ: closure rules and minimality enforcement."""

from __future__ import annotations

from nps.certification.dependency_registry import DependencyRegistry
from nps.core.errors import MathematicalInconsistency
from nps.symbols.symbol_dictionary import SymbolDictionary


def certify_minimality(*, registry: DependencyRegistry, symbols: SymbolDictionary) -> None:
    for symbol in symbols.entries():
        for required in symbol.obj.requires:
            if not registry.is_registered(required):
                raise MathematicalInconsistency(
                    f"Symbol '{symbol.name}' requires missing property '{required}'"
                )
