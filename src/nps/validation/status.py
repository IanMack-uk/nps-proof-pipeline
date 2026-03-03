from __future__ import annotations

from enum import Enum


class CertificationStatus(str, Enum):
    PROVISIONAL = "PROVISIONAL"
    CERTIFIED = "CERTIFIED"
    REJECTED = "REJECTED"


class StatementStatus(str, Enum):
    CONJECTURE = "CONJECTURE"
    VALIDATED = "VALIDATED"
    DISPROVEN = "DISPROVEN"
