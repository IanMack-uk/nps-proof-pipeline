"""Typed mathematical object model for the Programme (Phase A).

All mathematical objects must declare domain, codomain, regularity, locality,
and a source reference.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from nps.core.locality import LocalityScope
from nps.core.regularity import RegularityClass

if TYPE_CHECKING:
    from collections.abc import Set

    from nps.certification.dependency_registry import PropertyKey


@dataclass(frozen=True, slots=True)
class SourceRef:
    """An explicit citation/source pointer for a definition."""

    key: str
    detail: str


@dataclass(frozen=True, slots=True)
class MathematicalObject:
    """A minimal typed mathematical object record."""

    name: str
    domain: str
    codomain: str
    regularity: RegularityClass
    locality: LocalityScope
    source: SourceRef
    requires: "Set[PropertyKey]"
