from __future__ import annotations

import numpy as np

from nps.models.graph.automorphisms import apply_node_permutation, image_edge_index, transport_edge_weights
from nps.models.graph.simple_graph import SimpleGraph


def test_relabelling_transports_weights() -> None:
    g = SimpleGraph(n=4, edges=[(0, 1), (1, 2), (2, 3), (0, 3)])

    perm = [1, 0, 2, 3]  # swap 0 and 1
    g2 = apply_node_permutation(g, perm)

    w = np.array([10.0, 11.0, 12.0, 13.0], dtype=np.float64)
    w2 = transport_edge_weights(g, g2, perm, w)

    for e_idx in range(len(g.edges)):
        e2 = image_edge_index(g, g2, perm, e_idx)
        assert float(w2[e2]) == float(w[e_idx])
