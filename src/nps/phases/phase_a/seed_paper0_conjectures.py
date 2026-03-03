from __future__ import annotations

from nps.validation.records import StatementRecord
from nps.validation.status import StatementStatus
from nps.validation.validation_registry import ValidationRegistry


def seed_paper0_conjectures(registry: ValidationRegistry) -> None:
    registry.register_statement(
        StatementRecord(
            id="THM.P0.0_8_1",
            statement="For each edge e, there exists a continuous H_e such that F_e(w) = H_e(w_e, S_e(w), R_e(w)).",
            status=StatementStatus.CONJECTURE,
            sources=[],
            requires=set(),
            depends_on_assumptions={
                "CAS-A.COORD.PAPER0_LOCALITY",
                "CAS-A.COORD.AUTOMORPHISM_INVARIANCE",
                "CAS-A.COORD.MONOTONICITY_SEPARATION",
                "CAS-A.COORD.MONOTONICITY_REDUNDANCY",
            },
            evidence=[],
        )
    )
