from __future__ import annotations

from dataclasses import dataclass, field

from nps.core.errors import MathematicalInconsistency


@dataclass(frozen=True)
class SimpleGraph:
    n: int
    edges: list[tuple[int, int]]
    edge_index: dict[tuple[int, int], int] = field(init=False)

    def __post_init__(self) -> None:
        if self.n <= 0:
            raise MathematicalInconsistency("Graph must have positive number of nodes")

        canonical: list[tuple[int, int]] = []
        seen: set[tuple[int, int]] = set()
        for u, v in self.edges:
            if u == v:
                raise MathematicalInconsistency("Self-loops are not allowed")
            if u < 0 or v < 0 or u >= self.n or v >= self.n:
                raise MathematicalInconsistency("Edge endpoint out of range")
            a, b = (u, v) if u < v else (v, u)
            if (a, b) in seen:
                raise MathematicalInconsistency("Duplicate edges are not allowed")
            seen.add((a, b))
            canonical.append((a, b))

        canonical_sorted = sorted(canonical)
        object.__setattr__(self, "edges", canonical_sorted)

        edge_index = {e: i for i, e in enumerate(canonical_sorted)}
        object.__setattr__(self, "edge_index", edge_index)

    def neighbors(self, v: int) -> set[int]:
        if v < 0 or v >= self.n:
            raise MathematicalInconsistency("Node out of range")
        out: set[int] = set()
        for a, b in self.edges:
            if a == v:
                out.add(b)
            elif b == v:
                out.add(a)
        return out

    def endpoints(self, e_idx: int) -> tuple[int, int]:
        if e_idx < 0 or e_idx >= len(self.edges):
            raise MathematicalInconsistency("Edge index out of range")
        return self.edges[e_idx]
