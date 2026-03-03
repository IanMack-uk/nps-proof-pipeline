"""Toy locality / neighbourhood maps.

Executable model instance — not general certified theory.
"""

from __future__ import annotations

from typing import Dict, Set


def ring_neighborhood(m: int, radius: int = 1) -> Dict[int, Set[int]]:
    if m <= 0:
        raise ValueError("m must be positive")
    if radius < 0:
        raise ValueError("radius must be nonnegative")

    neigh: Dict[int, Set[int]] = {}
    for e in range(m):
        s: Set[int] = set()
        for k in range(-radius, radius + 1):
            s.add((e + k) % m)
        neigh[e] = s

    check_neighborhood(neigh, m)
    return neigh


def check_neighborhood(neigh: Dict[int, Set[int]], m: int) -> None:
    if set(neigh.keys()) != set(range(m)):
        raise ValueError("Neighborhood keys must be exactly 0..m-1")
    for e, s in neigh.items():
        if e not in s:
            raise ValueError(f"N({e}) must include {e}")
        for j in s:
            if j < 0 or j >= m:
                raise ValueError(f"N({e}) contains out-of-bounds index {j}")
