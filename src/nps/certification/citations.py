"""Citation stubs for the Programme (Phase 0A).

This module centralises human-readable citations used by SourceRef.
"""

from __future__ import annotations

from nps.core.types import SourceRef


def source_ref(key: str, detail: str) -> SourceRef:
    return SourceRef(key=key, detail=detail)
