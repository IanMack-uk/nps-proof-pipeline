"""Symbol dictionary and gating rules for the Programme (Phase A).

No symbol may be registered unless:
- Every required property is registered in DependencyRegistry (Phase 0A)
- Its object declares domain/codomain/regularity/locality/source explicitly
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from nps.certification.dependency_registry import DependencyRegistry
from nps.core.errors import MathematicalInconsistency
from nps.core.types import MathematicalObject


@dataclass(frozen=True, slots=True)
class SymbolEntry:
    name: str
    obj: MathematicalObject


class SymbolDictionary:
    def __init__(self, *, registry: DependencyRegistry) -> None:
        self._registry = registry
        self._symbols: dict[str, SymbolEntry] = {}
        self._frozen_version: Optional[str] = None

    @property
    def frozen_version(self) -> Optional[str]:
        return self._frozen_version

    def is_frozen(self) -> bool:
        return self._frozen_version is not None

    def freeze(self, version: str) -> None:
        if version == "":
            raise MathematicalInconsistency("SymbolDictionary freeze version must be non-empty")
        if self._frozen_version is not None:
            raise MathematicalInconsistency("SymbolDictionary already frozen")
        self._frozen_version = version

    def add(self, *, name: str, obj: MathematicalObject) -> None:
        if self._frozen_version is not None:
            raise MathematicalInconsistency("SymbolDictionary is frozen")
        if name in self._symbols:
            raise MathematicalInconsistency(f"Symbol already registered: {name}")
        self._validate_object(obj=obj)
        for required in obj.requires:
            self._registry.require(required)
        self._symbols[name] = SymbolEntry(name=name, obj=obj)

    def get(self, name: str) -> SymbolEntry:
        try:
            return self._symbols[name]
        except KeyError as exc:
            raise MathematicalInconsistency(f"Unknown symbol: {name}") from exc

    def __contains__(self, name: str) -> bool:
        return name in self._symbols

    def entries(self) -> list[SymbolEntry]:
        return list(self._symbols.values())

    @staticmethod
    def _validate_object(*, obj: MathematicalObject) -> None:
        if obj.domain == "" or obj.codomain == "":
            raise MathematicalInconsistency("MathematicalObject must declare domain and codomain")
        if obj.name == "":
            raise MathematicalInconsistency("MathematicalObject must declare a name")
        if obj.source.key == "" or obj.source.detail == "":
            raise MathematicalInconsistency("MathematicalObject must declare a SourceRef")
        if len(obj.requires) == 0:
            raise MathematicalInconsistency("MathematicalObject must declare non-empty required properties")
