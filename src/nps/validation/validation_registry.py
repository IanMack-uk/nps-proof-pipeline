from __future__ import annotations

from dataclasses import replace

from nps.core.errors import MathematicalInconsistency
from nps.validation.evidence import Evidence
from nps.validation.records import AssumptionRecord, ScopeTag, StatementRecord
from nps.validation.status import CertificationStatus, StatementStatus


class ValidationRegistry:
    def __init__(self) -> None:
        self._assumptions: dict[str, AssumptionRecord] = {}
        self._statements: dict[str, StatementRecord] = {}

    def require_assumption_present(self, assumption_id: str) -> None:
        if assumption_id not in self._assumptions:
            raise MathematicalInconsistency(f"Unknown assumption id: {assumption_id}")

    def register_assumption(self, record: AssumptionRecord) -> None:
        if record.id in self._assumptions:
            raise MathematicalInconsistency(f"Duplicate assumption id: {record.id}")
        self._assumptions[record.id] = record

    def register_statement(self, record: StatementRecord) -> None:
        if record.id in self._statements:
            raise MathematicalInconsistency(f"Duplicate statement id: {record.id}")
        self._statements[record.id] = record

    def add_evidence_to_assumption(self, assumption_id: str, evidence: Evidence) -> None:
        record = self._assumptions.get(assumption_id)
        if record is None:
            raise MathematicalInconsistency(f"Unknown assumption id: {assumption_id}")
        record.evidence.append(evidence)

    def add_evidence_to_statement(self, statement_id: str, evidence: Evidence) -> None:
        record = self._statements.get(statement_id)
        if record is None:
            raise MathematicalInconsistency(f"Unknown statement id: {statement_id}")
        record.evidence.append(evidence)

    def promote_assumption(self, assumption_id: str) -> None:
        record = self._assumptions.get(assumption_id)
        if record is None:
            raise MathematicalInconsistency(f"Unknown assumption id: {assumption_id}")
        if record.status is not CertificationStatus.PROVISIONAL:
            raise MathematicalInconsistency(
                f"Cannot promote assumption {assumption_id} from status {record.status}"
            )
        self._assumptions[assumption_id] = replace(record, status=CertificationStatus.CERTIFIED)

    def reject_assumption(self, assumption_id: str) -> None:
        record = self._assumptions.get(assumption_id)
        if record is None:
            raise MathematicalInconsistency(f"Unknown assumption id: {assumption_id}")
        if record.status is CertificationStatus.REJECTED:
            return
        self._assumptions[assumption_id] = replace(record, status=CertificationStatus.REJECTED)

    def validate_statement(self, statement_id: str) -> None:
        record = self._statements.get(statement_id)
        if record is None:
            raise MathematicalInconsistency(f"Unknown statement id: {statement_id}")
        if record.status is not StatementStatus.CONJECTURE:
            raise MathematicalInconsistency(
                f"Cannot validate statement {statement_id} from status {record.status}"
            )
        self._statements[statement_id] = replace(record, status=StatementStatus.VALIDATED)

    def disprove_statement(self, statement_id: str) -> None:
        record = self._statements.get(statement_id)
        if record is None:
            raise MathematicalInconsistency(f"Unknown statement id: {statement_id}")
        if record.status is StatementStatus.DISPROVEN:
            return
        self._statements[statement_id] = replace(record, status=StatementStatus.DISPROVEN)

    def require_assumption_certified(self, assumption_id: str) -> None:
        record = self._assumptions.get(assumption_id)
        if record is None:
            raise MathematicalInconsistency(f"Unknown assumption id: {assumption_id}")
        if record.status is not CertificationStatus.CERTIFIED:
            raise MathematicalInconsistency(f"Assumption not certified: {assumption_id}")

    def require_statement_validated(self, statement_id: str) -> None:
        record = self._statements.get(statement_id)
        if record is None:
            raise MathematicalInconsistency(f"Unknown statement id: {statement_id}")
        if record.status is not StatementStatus.VALIDATED:
            raise MathematicalInconsistency(f"Statement not validated: {statement_id}")

    def list_assumptions(self, scope: ScopeTag | None = None) -> list[AssumptionRecord]:
        items = list(self._assumptions.values())
        if scope is not None:
            items = [r for r in items if r.scope is scope]
        return sorted(items, key=lambda r: r.id)

    def list_statements(self) -> list[StatementRecord]:
        return sorted(self._statements.values(), key=lambda r: r.id)
