"""Locality scopes for Programme objects (Phase A).

Locality indicates where a definition or property is valid.
"""

from __future__ import annotations

from enum import Enum


class LocalityScope(str, Enum):
    LOCAL = "local"
    GLOBAL = "global"
