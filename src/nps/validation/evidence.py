from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Evidence:
    kind: str
    ref: str
    summary: str
    link: Optional[str] = None
