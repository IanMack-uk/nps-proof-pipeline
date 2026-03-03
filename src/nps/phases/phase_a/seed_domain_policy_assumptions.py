from __future__ import annotations

from nps.validation.records import AssumptionRecord, ScopeTag
from nps.validation.status import CertificationStatus
from nps.validation.validation_registry import ValidationRegistry


def seed_domain_policy_assumptions(registry: ValidationRegistry) -> None:
    registry.register_assumption(
        AssumptionRecord(
            id="CAS-A.OMEGA.NONNEGATIVE",
            text="For the proof-target model class, Ω ⊂ R^m_{≥0} (weights are componentwise nonnegative).",
            scope=ScopeTag.FOUNDATIONS,
            status=CertificationStatus.PROVISIONAL,
            sources=[],
            requires=set(),
            evidence=[],
        )
    )
