from __future__ import annotations

from nps.validation.records import AssumptionRecord, ScopeTag
from nps.validation.status import CertificationStatus
from nps.validation.validation_registry import ValidationRegistry


def seed_coordinate_assumptions(registry: ValidationRegistry) -> None:
    """Register provisional CAS-A ledger entries for Structural Coordinate + contract tests."""

    registry.register_assumption(
        AssumptionRecord(
            id="CAS-A.COORD.LOCALITY",
            text="Structural coordinates depend only on declared local data.",
            scope=ScopeTag.FOUNDATIONS,
            status=CertificationStatus.PROVISIONAL,
            sources=[],
            requires=set(),
            evidence=[],
        )
    )

    registry.register_assumption(
        AssumptionRecord(
            id="CAS-A.CONTRACT.F_DEPENDENCE",
            text="Marginal field component F_e depends only on (w_e, S_e(w), R_e(w), θ).",
            scope=ScopeTag.PHASE_B_INTERFACE,
            status=CertificationStatus.PROVISIONAL,
            sources=[],
            requires=set(),
            evidence=[],
        )
    )
