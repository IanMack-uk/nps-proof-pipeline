from __future__ import annotations

from nps.models.graph.line_graph import line_ball
from nps.models.graph.simple_graph import SimpleGraph


def compute_edge_neighborhoods(g: SimpleGraph, radius: int) -> dict[int, set[int]]:
    return {e_idx: line_ball(g, e_idx, radius=radius) for e_idx in range(len(g.edges))}
