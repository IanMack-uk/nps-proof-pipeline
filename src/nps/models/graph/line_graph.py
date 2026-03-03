from __future__ import annotations

from collections import deque

from nps.core.errors import MathematicalInconsistency
from nps.models.graph.simple_graph import SimpleGraph


def line_neighbors(g: SimpleGraph, e_idx: int) -> set[int]:
    if e_idx < 0 or e_idx >= len(g.edges):
        raise MathematicalInconsistency("Edge index out of range")

    u, v = g.endpoints(e_idx)
    out: set[int] = set()
    for j, (a, b) in enumerate(g.edges):
        if j == e_idx:
            continue
        if a == u or b == u or a == v or b == v:
            out.add(j)
    return out


def line_ball(g: SimpleGraph, e_idx: int, radius: int) -> set[int]:
    if radius < 0:
        raise MathematicalInconsistency("Radius must be nonnegative")
    if e_idx < 0 or e_idx >= len(g.edges):
        raise MathematicalInconsistency("Edge index out of range")

    visited: set[int] = {e_idx}
    q: deque[tuple[int, int]] = deque([(e_idx, 0)])

    while q:
        cur, dist = q.popleft()
        if dist == radius:
            continue
        for nb in sorted(line_neighbors(g, cur)):
            if nb in visited:
                continue
            visited.add(nb)
            q.append((nb, dist + 1))

    return visited
