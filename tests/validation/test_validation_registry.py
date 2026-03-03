from __future__ import annotations

import pytest

from nps.core.errors import MathematicalInconsistency
from nps.validation.evidence import Evidence
from nps.validation.records import AssumptionRecord, ScopeTag, StatementRecord
from nps.validation.status import CertificationStatus, StatementStatus
from nps.validation.validation_registry import ValidationRegistry


def test_register_assumption_and_duplicate_fails() -> None:
    registry = ValidationRegistry()
    record = AssumptionRecord(
        id="CAS-A.P1",
        text="Provisional assumption.",
        scope=ScopeTag.FOUNDATIONS,
        status=CertificationStatus.PROVISIONAL,
    )
    registry.register_assumption(record)

    with pytest.raises(MathematicalInconsistency, match="Duplicate assumption id"):
        registry.register_assumption(record)


def test_register_statement_and_duplicate_fails() -> None:
    registry = ValidationRegistry()
    record = StatementRecord(
        id="THM.SDOT.v4",
        statement="Conjectured statement.",
        status=StatementStatus.CONJECTURE,
    )
    registry.register_statement(record)

    with pytest.raises(MathematicalInconsistency, match="Duplicate statement id"):
        registry.register_statement(record)


def test_add_evidence_works_and_missing_id_fails() -> None:
    registry = ValidationRegistry()
    a = AssumptionRecord(
        id="CAS-A.P1",
        text="Provisional assumption.",
        scope=ScopeTag.FOUNDATIONS,
        status=CertificationStatus.PROVISIONAL,
    )
    registry.register_assumption(a)

    ev = Evidence(kind="test", ref="tests/validation/test_validation_registry.py::x", summary="smoke")
    registry.add_evidence_to_assumption("CAS-A.P1", ev)

    with pytest.raises(MathematicalInconsistency, match="Unknown assumption id"):
        registry.add_evidence_to_assumption("MISSING", ev)

    s = StatementRecord(
        id="THM.SDOT.v4",
        statement="Conjectured statement.",
        status=StatementStatus.CONJECTURE,
    )
    registry.register_statement(s)
    registry.add_evidence_to_statement("THM.SDOT.v4", ev)

    with pytest.raises(MathematicalInconsistency, match="Unknown statement id"):
        registry.add_evidence_to_statement("MISSING", ev)


def test_require_assumption_certified_transition() -> None:
    registry = ValidationRegistry()
    a = AssumptionRecord(
        id="CAS-A.P1",
        text="Provisional assumption.",
        scope=ScopeTag.FOUNDATIONS,
        status=CertificationStatus.PROVISIONAL,
    )
    registry.register_assumption(a)

    with pytest.raises(MathematicalInconsistency, match="Assumption not certified"):
        registry.require_assumption_certified("CAS-A.P1")

    registry.promote_assumption("CAS-A.P1")
    registry.require_assumption_certified("CAS-A.P1")


def test_promotion_transition_rules_enforced() -> None:
    registry = ValidationRegistry()
    a = AssumptionRecord(
        id="CAS-A.P1",
        text="Provisional assumption.",
        scope=ScopeTag.FOUNDATIONS,
        status=CertificationStatus.PROVISIONAL,
    )
    registry.register_assumption(a)
    registry.promote_assumption("CAS-A.P1")

    with pytest.raises(MathematicalInconsistency, match="Cannot promote assumption"):
        registry.promote_assumption("CAS-A.P1")


def test_require_statement_validated_transition() -> None:
    registry = ValidationRegistry()
    s = StatementRecord(
        id="THM.SDOT.v4",
        statement="Conjectured statement.",
        status=StatementStatus.CONJECTURE,
    )
    registry.register_statement(s)

    with pytest.raises(MathematicalInconsistency, match="Statement not validated"):
        registry.require_statement_validated("THM.SDOT.v4")

    registry.validate_statement("THM.SDOT.v4")
    registry.require_statement_validated("THM.SDOT.v4")
