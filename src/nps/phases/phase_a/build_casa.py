"""Phase A: build utilities (symbol dictionary)."""

from __future__ import annotations

from nps.certification.citations import source_ref
from nps.certification.dependency_registry import DependencyRegistry
from nps.core.locality import LocalityScope
from nps.core.regularity import RegularityClass
from nps.core.types import MathematicalObject
from nps.phases.phase_0a.build_cas0a import (
    F_DEFINED_AS_GRAD_W_PHI,
    LOCALITY_DEFINED_NEIGHBORHOOD,
    LOCALITY_UNIFORM_RADIUS,
    OMEGA_COMPACT,
    OMEGA_NONEMPTY,
    PHI_C3_EXTENSION,
    PHI_CONTINUOUS,
    W_STAR_DEFINED_AS_ARGMAX,
)
from nps.symbols.symbol_dictionary import SymbolDictionary


def build_symbol_dictionary(*, registry: DependencyRegistry) -> SymbolDictionary:
    return SymbolDictionary(registry=registry)


def build_phase_a_symbols(registry: DependencyRegistry) -> SymbolDictionary:
    """Create minimal Phase A symbols that only require CAS-0A properties."""

    symbols = SymbolDictionary(registry=registry)

    omega = MathematicalObject(
        name="Omega",
        domain="TypeSpec:Set",
        codomain="TypeSpec:Subset",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source_ref("CAS-0A-v4", "Assumption A1"),
        requires={OMEGA_NONEMPTY, OMEGA_COMPACT},
    )
    symbols.add(name="Omega", obj=omega)

    phi = MathematicalObject(
        name="Phi",
        domain="TypeSpec:Omega×Omega",
        codomain="TypeSpec:Real",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source_ref("CAS-0A-v4", "Assumption A3"),
        requires={PHI_CONTINUOUS, PHI_C3_EXTENSION},
    )
    symbols.add(name="Phi", obj=phi)

    f = MathematicalObject(
        name="F",
        domain="TypeSpec:Omega",
        codomain="TypeSpec:Covector",
        regularity=RegularityClass.C0,
        locality=LocalityScope.LOCAL,
        source=source_ref("CAS-0A-v4", "Definition (Gradient / marginal field)"),
        requires={F_DEFINED_AS_GRAD_W_PHI, LOCALITY_DEFINED_NEIGHBORHOOD, LOCALITY_UNIFORM_RADIUS},
    )
    symbols.add(name="F", obj=f)

    w_star = MathematicalObject(
        name="W_star",
        domain="TypeSpec:Omega",
        codomain="TypeSpec:P(Omega)",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source_ref("CAS-0A-v4", "Definition (Equilibrium correspondence)"),
        requires={W_STAR_DEFINED_AS_ARGMAX, OMEGA_NONEMPTY, OMEGA_COMPACT},
    )
    symbols.add(name="W_star", obj=w_star)

    return symbols
