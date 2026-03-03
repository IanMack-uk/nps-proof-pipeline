"""Regularity classes for Programme objects (Phase A).

Regularity is always explicit; no implicit smoothness assumptions are allowed.
"""

from __future__ import annotations

from enum import Enum


class RegularityClass(str, Enum):
    C0 = "C0"
    C1 = "C1"
    C2 = "C2"
    SMOOTH = "smooth"
