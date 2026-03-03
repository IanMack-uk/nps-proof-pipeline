from __future__ import annotations

from nps.validation.validation_registry import ValidationRegistry


def seed_phase_a_validation_registry() -> ValidationRegistry:
    """Create an empty Phase A validation registry (draft layer)."""
    return ValidationRegistry()
