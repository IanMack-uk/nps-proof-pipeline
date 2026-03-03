from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from nps.certification.dependency_registry import PropertyKey
from nps.core.types import SourceRef
from nps.validation.evidence import Evidence
from nps.validation.status import CertificationStatus, StatementStatus


class ScopeTag(str, Enum):
    FOUNDATIONS = "FOUNDATIONS"
    PHASE_B_INTERFACE = "PHASE_B_INTERFACE"
    DIFFERENTIABILITY = "DIFFERENTIABILITY"
    UNIQUENESS = "UNIQUENESS"


@dataclass
class AssumptionRecord:
    id: str
    text: str
    scope: ScopeTag
    status: CertificationStatus
    sources: list[SourceRef] = field(default_factory=list)
    requires: set[PropertyKey] = field(default_factory=set)
    evidence: list[Evidence] = field(default_factory=list)


@dataclass
class StatementRecord:
    id: str
    statement: str
    status: StatementStatus
    sources: list[SourceRef] = field(default_factory=list)
    requires: set[PropertyKey] = field(default_factory=set)
    depends_on_assumptions: set[str] = field(default_factory=set)
    evidence: list[Evidence] = field(default_factory=list)
