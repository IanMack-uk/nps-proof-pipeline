from __future__ import annotations

from nps.validation.records import AssumptionRecord, ScopeTag
from nps.validation.status import CertificationStatus
from nps.validation.validation_registry import ValidationRegistry


def seed_cas_a_assumptions(registry: ValidationRegistry) -> None:
    """Register Phase A provisional assumptions (CAS-A draft)."""

    registry.register_assumption(
        AssumptionRecord(
            id="CAS-A.EXP.LOCALITY",
            text="Structural exposure E_e(w,θ) depends only on local data (N(e)) when declared local.",
            scope=ScopeTag.FOUNDATIONS,
            status=CertificationStatus.PROVISIONAL,
            sources=[],
            requires=set(),
            evidence=[],
        )
    )

    registry.register_assumption(
        AssumptionRecord(
            id="CAS-A.EXP.WELLPOSED",
            text="Structural exposure is well-defined and finite for all w ∈ Ω.",
            scope=ScopeTag.FOUNDATIONS,
            status=CertificationStatus.PROVISIONAL,
            sources=[],
            requires=set(),
            evidence=[],
        )
    )

    registry.register_assumption(
        AssumptionRecord(
            id="CAS-A.EXP.REGULARITY",
            text="Structural exposure inherits at least C⁰ regularity from its defining objects.",
            scope=ScopeTag.DIFFERENTIABILITY,
            status=CertificationStatus.PROVISIONAL,
            sources=[],
            requires=set(),
            evidence=[],
        )
    )

    registry.register_assumption(
        AssumptionRecord(
            id="CAS-A.NOTATION.STABILITY",
            text="Phase A symbol dictionary remains fixed (versioned freeze) for all subsequent reasoning.",
            scope=ScopeTag.FOUNDATIONS,
            status=CertificationStatus.PROVISIONAL,
            sources=[],
            requires=set(),
            evidence=[],
        )
    )
