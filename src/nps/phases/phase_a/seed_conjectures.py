from __future__ import annotations

from nps.certification.dependency_registry import PropertyKey
from nps.validation.records import StatementRecord
from nps.validation.status import StatementStatus
from nps.validation.validation_registry import ValidationRegistry


def seed_phase_a_conjectures(registry: ValidationRegistry) -> None:
    """Register Phase A conjectures (draft layer)."""

    stmt = StatementRecord(
        id="THM.SDOT.v4",
        statement="See docs/specs/phase_a_structural_differentiation_conjecture.md",
        status=StatementStatus.CONJECTURE,
        sources=[],
        requires={
            PropertyKey(subject="Omega", property="compact"),
            PropertyKey(subject="Phi", property="continuous"),
            PropertyKey(subject="F", property="defined_as_grad_w_Phi"),
            PropertyKey(subject="W_star", property="defined_as_argmax_over_Omega"),
        },
        depends_on_assumptions=set(),
        evidence=[],
    )

    registry.register_statement(stmt)
