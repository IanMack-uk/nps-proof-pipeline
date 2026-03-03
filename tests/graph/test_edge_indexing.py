from __future__ import annotations

from nps.models.graph.simple_graph import SimpleGraph


def test_edge_indexing_deterministic() -> None:
    g = SimpleGraph(n=4, edges=[(2, 0), (3, 1), (1, 2)])

    assert g.edges == [(0, 2), (1, 2), (1, 3)]
    assert g.edge_index[(0, 2)] == 0
    assert g.edge_index[(1, 2)] == 1
    assert g.edge_index[(1, 3)] == 2

    assert g.endpoints(0) == (0, 2)
    assert g.endpoints(2) == (1, 3)
