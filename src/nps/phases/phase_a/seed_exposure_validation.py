from __future__ import annotations

from nps.phases.phase_a.seed_cas_a_assumptions import seed_cas_a_assumptions
from nps.validation.validation_registry import ValidationRegistry


def seed_structural_exposure_ledger(registry: ValidationRegistry) -> None:
    """Register provisional CAS-A ledger entries for Structural Exposure tests."""

    seed_cas_a_assumptions(registry)
