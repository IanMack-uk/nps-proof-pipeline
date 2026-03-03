from __future__ import annotations

import pytest

from nps.core.errors import MathematicalInconsistency
from nps.phases.phase_a.seed_conjectures import seed_phase_a_conjectures
from nps.validation.status import StatementStatus
from nps.validation.validation_registry import ValidationRegistry


def test_structural_differentiation_conjecture_registered_and_not_validated() -> None:
    registry = ValidationRegistry()
    seed_phase_a_conjectures(registry)

    matches = [s for s in registry.list_statements() if s.id == "THM.SDOT.v4"]
    assert len(matches) == 1
    assert matches[0].status is StatementStatus.CONJECTURE

    with pytest.raises(MathematicalInconsistency):
        registry.require_statement_validated("THM.SDOT.v4")
