from __future__ import annotations

from nps.validation.records import AssumptionRecord, ScopeTag
from nps.validation.status import CertificationStatus
from nps.validation.validation_registry import ValidationRegistry


def seed_paper0_coordinate_assumptions(registry: ValidationRegistry) -> None:
    registry.register_assumption(
        AssumptionRecord(
            id="CAS-A.COORD.AUTOMORPHISM_INVARIANCE",
            text="Paper0 structural coordinates are invariant under automorphisms (relabeling).",
            scope=ScopeTag.FOUNDATIONS,
            status=CertificationStatus.PROVISIONAL,
            sources=[],
            requires=set(),
            evidence=[],
        )
    )

    registry.register_assumption(
        AssumptionRecord(
            id="CAS-A.COORD.MONOTONICITY_SEPARATION",
            text="Paper0 separation coordinate is monotone under strengthening alternative paths.",
            scope=ScopeTag.FOUNDATIONS,
            status=CertificationStatus.PROVISIONAL,
            sources=[],
            requires=set(),
            evidence=[],
        )
    )

    registry.register_assumption(
        AssumptionRecord(
            id="CAS-A.COORD.MONOTONICITY_REDUNDANCY",
            text="Paper0 redundancy coordinate is monotone under closure (strengthening short cycles).",
            scope=ScopeTag.FOUNDATIONS,
            status=CertificationStatus.PROVISIONAL,
            sources=[],
            requires=set(),
            evidence=[],
        )
    )

    registry.register_assumption(
        AssumptionRecord(
            id="CAS-A.COORD.PAPER0_LOCALITY",
            text="Paper0 structural coordinates depend only on bounded neighborhood N(e).",
            scope=ScopeTag.FOUNDATIONS,
            status=CertificationStatus.PROVISIONAL,
            sources=[],
            requires=set(),
            evidence=[],
        )
    )
