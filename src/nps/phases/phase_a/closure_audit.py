from __future__ import annotations

import inspect

from nps.core.errors import MathematicalInconsistency
from nps.symbols.symbol_dictionary import SymbolDictionary
from nps.validation.validation_registry import ValidationRegistry


def run_phase_a_coherence_audit(symbols: SymbolDictionary, registry: ValidationRegistry) -> None:
    if not symbols.is_frozen():
        raise MathematicalInconsistency("SymbolDictionary must be frozen for coherence audit")

    for required_symbol in ("Omega", "Phi", "F", "W_star"):
        if required_symbol not in symbols:
            raise MathematicalInconsistency(f"Missing required symbol: {required_symbol}")

    for entry in symbols.entries():
        obj = entry.obj
        if obj.domain == "" or obj.codomain == "":
            raise MathematicalInconsistency("Phase A object missing domain/codomain")
        if obj.regularity.value == "" or obj.locality.value == "":
            raise MathematicalInconsistency("Phase A object missing regularity/locality")
        if obj.source.key == "" or obj.source.detail == "":
            raise MathematicalInconsistency("Phase A object missing source")

    for assumption_id in (
        "CAS-A.EXP.LOCALITY",
        "CAS-A.EXP.WELLPOSED",
        "CAS-A.CONTRACT.F_DEPENDENCE",
    ):
        registry.require_assumption_present(assumption_id)

    from nps.phases.phase_a.coordinates.coordinate_validation import check_phase_b_contract

    sig = inspect.signature(check_phase_b_contract)
    if "registry" not in sig.parameters:
        raise MathematicalInconsistency("Phase-B contract checker must require CAS-A.CONTRACT.F_DEPENDENCE")
