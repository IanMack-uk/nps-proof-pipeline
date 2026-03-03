"""Explicit dependency registration for the Programme (Phase 0A).

A symbol cannot be added to the SymbolDictionary unless its dependency is
registered here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from nps.core.errors import MathematicalInconsistency

if TYPE_CHECKING:
    from nps.core.types import SourceRef


@dataclass(frozen=True, slots=True)
class PropertyKey:
    subject: str
    property: str


@dataclass(frozen=True, slots=True)
class PropertyCertification:
    property_key: PropertyKey
    source: SourceRef


class DependencyRegistry:
    def __init__(self) -> None:
        self._properties: dict[PropertyKey, PropertyCertification] = {}
        self._frozen = False

    def freeze(self) -> None:
        self._frozen = True

    def is_frozen(self) -> bool:
        return self._frozen

    def register(self, *, property_key: PropertyKey, source: SourceRef) -> None:
        if self._frozen:
            raise MathematicalInconsistency("Registry is frozen")
        if property_key in self._properties:
            raise MathematicalInconsistency(f"Property already registered: {property_key}")
        self._properties[property_key] = PropertyCertification(
            property_key=property_key,
            source=source,
        )

    def is_registered(self, property_key: PropertyKey) -> bool:
        return property_key in self._properties

    def require(self, property_key: PropertyKey) -> PropertyCertification:
        try:
            return self._properties[property_key]
        except KeyError as exc:
            raise MathematicalInconsistency(f"Missing required property: {property_key}") from exc

    def drop(self, property_key: PropertyKey) -> None:
        if self._frozen:
            raise MathematicalInconsistency("Registry is frozen")
        if property_key not in self._properties:
            raise MathematicalInconsistency(f"Cannot drop unknown property: {property_key}")
        del self._properties[property_key]

    def rows(self) -> list[tuple[PropertyKey, SourceRef]]:
        items = [(cert.property_key, cert.source) for cert in self._properties.values()]
        return sorted(items, key=lambda x: (x[0].subject, x[0].property))
