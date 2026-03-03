from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from nps.core.errors import MathematicalInconsistency
from nps.models.graph.simple_graph import SimpleGraph


def apply_node_permutation(g: SimpleGraph, perm: list[int]) -> SimpleGraph:
    if len(perm) != g.n:
        raise MathematicalInconsistency("Permutation length must equal number of nodes")
    if sorted(perm) != list(range(g.n)):
        raise MathematicalInconsistency("Permutation must be a bijection of nodes")

    permuted_edges: list[tuple[int, int]] = []
    for u, v in g.edges:
        u2 = perm[u]
        v2 = perm[v]
        a, b = (u2, v2) if u2 < v2 else (v2, u2)
        permuted_edges.append((a, b))

    return SimpleGraph(n=g.n, edges=permuted_edges)


def _expected_permuted_edges(g: SimpleGraph, perm: list[int]) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for u, v in g.edges:
        u2 = perm[u]
        v2 = perm[v]
        a, b = (u2, v2) if u2 < v2 else (v2, u2)
        edges.append((a, b))
    return sorted(edges)


def transport_edge_weights(
    g: SimpleGraph,
    g2: SimpleGraph,
    perm: list[int],
    w: NDArray[np.float64],
) -> NDArray[np.float64]:
    if w.shape != (len(g.edges),):
        raise MathematicalInconsistency("Weight vector shape mismatch")

    expected_edges = _expected_permuted_edges(g, perm)
    if g2.n != g.n or g2.edges != expected_edges:
        raise MathematicalInconsistency("Permuted graph edges do not match expected image")

    out = np.zeros(len(g2.edges), dtype=np.float64)
    for e_idx, (u, v) in enumerate(g.edges):
        u2 = perm[u]
        v2 = perm[v]
        a, b = (u2, v2) if u2 < v2 else (v2, u2)
        idx2 = g2.edge_index.get((a, b))
        if idx2 is None:
            raise MathematicalInconsistency("Missing image edge in permuted graph")
        out[idx2] = float(w[e_idx])

    return out


def image_edge_index(
    g: SimpleGraph,
    g2: SimpleGraph,
    perm: list[int],
    e_idx: int,
) -> int:
    u, v = g.endpoints(e_idx)
    u2 = perm[u]
    v2 = perm[v]
    a, b = (u2, v2) if u2 < v2 else (v2, u2)
    idx2 = g2.edge_index.get((a, b))
    if idx2 is None:
        raise MathematicalInconsistency("Missing image edge in permuted graph")
    return idx2