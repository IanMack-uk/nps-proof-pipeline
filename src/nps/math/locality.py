from __future__ import annotations

from collections import deque

import numpy as np


def line_graph_neighbors_from_edge_incidence(edges: list[tuple[int, int]]) -> list[list[int]]:
    """Compute line-graph adjacency of edges.

    Two edges are neighbors if they share an endpoint.
    """

    m = len(edges)
    neighbors: list[list[int]] = [[] for _ in range(m)]

    endpoint_to_edges: dict[int, list[int]] = {}
    for ei, (u, v) in enumerate(edges):
        endpoint_to_edges.setdefault(u, []).append(ei)
        endpoint_to_edges.setdefault(v, []).append(ei)

    for ei, (u, v) in enumerate(edges):
        adj = set(endpoint_to_edges.get(u, [])) | set(endpoint_to_edges.get(v, []))
        adj.discard(ei)
        neighbors[ei] = sorted(adj)

    return neighbors


def k_hop_neighborhood(neighbors: list[list[int]], k: int) -> list[set[int]]:
    if k < 0:
        raise ValueError("k must be nonnegative")

    out: list[set[int]] = []
    for i in range(len(neighbors)):
        seen: set[int] = {i}
        q: deque[tuple[int, int]] = deque([(i, 0)])
        while q:
            node, dist = q.popleft()
            if dist == k:
                continue
            for nxt in neighbors[node]:
                if nxt in seen:
                    continue
                seen.add(nxt)
                q.append((nxt, dist + 1))
        out.append(seen)

    return out


def sparsity_support(A: np.ndarray, tol: float = 0.0) -> list[set[int]]:
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A must be square")

    m = int(A.shape[0])
    support: list[set[int]] = []
    for i in range(m):
        row = A[i, :]
        idx = set(int(j) for j in np.where(np.abs(row) > tol)[0].tolist())
        support.append(idx)

    return support
