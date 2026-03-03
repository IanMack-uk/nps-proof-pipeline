"""Phase 0A: approval path for CAS-0A.

Calling this module freezes the CAS-0A registry used for Phase A gating.
"""

from __future__ import annotations

from nps.certification.dependency_registry import DependencyRegistry
from nps.phases.phase_0a.build_cas0a import build_cas0a_registry


def approve_and_freeze_cas0a() -> None:
    registry = DependencyRegistry()
    build_cas0a_registry(registry)
    registry.freeze()
    print("CAS-0A frozen")
