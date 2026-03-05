from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class RealPhiV0Spec:
    # Graph encoded by undirected edges (u,v) with u < v.
    n: int
    edges: list[tuple[int, int]]
    theta_A: float
    theta_M: float
    theta_R: float
    p: float = 2.0
    domain_lower: float = 0.0
    domain_upper: float = 1.0
    extension_id: str = "real_phi_v0"

    @property
    def m(self) -> int:
        return len(self.edges)

    def _edge_index(self) -> dict[tuple[int, int], int]:
        idx: dict[tuple[int, int], int] = {}
        for k, (u, v) in enumerate(self.edges):
            if u == v:
                raise ValueError("self-loops not supported")
            a, b = (u, v) if u < v else (v, u)
            idx[(a, b)] = k
        return idx

    def _adjacency(self) -> list[set[int]]:
        adj = [set() for _ in range(self.n)]
        for u, v in self.edges:
            adj[u].add(v)
            adj[v].add(u)
        return adj

    def _kappa(self, adj: list[set[int]], u: int, v: int) -> int:
        return int(len(adj[u].intersection(adj[v])))

    def _brokerage(self, kappa: int) -> float:
        # Canonical v0 choice.
        return float(1.0 / (1.0 + float(kappa)))

    def exposure_edge(self, e: tuple[int, int], w: np.ndarray) -> tuple[float, float]:
        wv = np.asarray(w, dtype=float)
        idx = self._edge_index()
        adj = self._adjacency()

        u, v = e
        a, b = (u, v) if u < v else (v, u)
        if (a, b) not in idx:
            raise ValueError("edge not in graph")

        kappa = self._kappa(adj, a, b)
        B = self._brokerage(kappa)

        common = adj[a].intersection(adj[b])
        R = 0.0
        for k in common:
            ea = (a, k) if a < k else (k, a)
            eb = (b, k) if b < k else (k, b)
            if ea in idx and eb in idx:
                R += float(wv[idx[ea]] * wv[idx[eb]])

        return (B, float(R))

    def value(self, w: np.ndarray, theta: float | None = None) -> float:
        _ = theta
        wv = np.asarray(w, dtype=float)
        if wv.shape != (self.m,):
            raise ValueError("w has wrong shape")

        idx = self._edge_index()
        adj = self._adjacency()

        # Precompute brokerage for each edge.
        B_edge = np.zeros(self.m, dtype=float)
        for e_i, (u, v) in enumerate(self.edges):
            kappa = self._kappa(adj, u, v)
            B_edge[e_i] = self._brokerage(kappa)

        # Node-level components.
        A = np.zeros(self.n, dtype=float)
        M = np.zeros(self.n, dtype=float)
        R = np.zeros(self.n, dtype=float)

        for e_i, (u, v) in enumerate(self.edges):
            w_e_p = float(wv[e_i] ** self.p)
            A[u] += w_e_p
            A[v] += w_e_p

            weak_u = float((1.0 - wv[e_i]) ** self.p) * float(B_edge[e_i])
            weak_v = weak_u
            M[u] += weak_u
            M[v] += weak_v

        # Redundancy: for each node i, sum over neighbor pairs {j,k} with edge(j,k).
        for i in range(self.n):
            neigh = sorted(adj[i])
            for a_pos in range(len(neigh)):
                j = neigh[a_pos]
                e_ij = (i, j) if i < j else (j, i)
                if e_ij not in idx:
                    continue
                w_ij_p = float(wv[idx[e_ij]] ** self.p)
                for b_pos in range(a_pos + 1, len(neigh)):
                    k = neigh[b_pos]
                    if k not in adj[j]:
                        continue
                    e_ik = (i, k) if i < k else (k, i)
                    if e_ik not in idx:
                        continue
                    w_ik_p = float(wv[idx[e_ik]] ** self.p)
                    R[i] += w_ij_p * w_ik_p

        phi = 0.0
        for i in range(self.n):
            phi += float(self.theta_A * np.log1p(A[i]))
            phi += float(self.theta_M * np.log1p(M[i]))
            phi -= float(self.theta_R * np.log1p(R[i]))

        return float(phi)

    def grad(self, w: np.ndarray, theta: float | None = None) -> np.ndarray:
        _ = theta
        wv = np.asarray(w, dtype=float)
        if wv.shape != (self.m,):
            raise ValueError("w has wrong shape")

        idx = self._edge_index()
        adj = self._adjacency()

        # brokerage per edge
        B_edge = np.zeros(self.m, dtype=float)
        for e_i, (u, v) in enumerate(self.edges):
            B_edge[e_i] = self._brokerage(self._kappa(adj, u, v))

        # Node-level A,M,R and their first derivatives wrt incident edges.
        A = np.zeros(self.n, dtype=float)
        M = np.zeros(self.n, dtype=float)
        R = np.zeros(self.n, dtype=float)

        # First, accumulate A,M.
        for e_i, (u, v) in enumerate(self.edges):
            w_e_p = float(wv[e_i] ** self.p)
            A[u] += w_e_p
            A[v] += w_e_p

            weak = float((1.0 - wv[e_i]) ** self.p) * float(B_edge[e_i])
            M[u] += weak
            M[v] += weak

        # Redundancy scalar R_i.
        for i in range(self.n):
            neigh = sorted(adj[i])
            for a_pos in range(len(neigh)):
                j = neigh[a_pos]
                e_ij = (i, j) if i < j else (j, i)
                if e_ij not in idx:
                    continue
                w_ij_p = float(wv[idx[e_ij]] ** self.p)
                for b_pos in range(a_pos + 1, len(neigh)):
                    k = neigh[b_pos]
                    if k not in adj[j]:
                        continue
                    e_ik = (i, k) if i < k else (k, i)
                    if e_ik not in idx:
                        continue
                    w_ik_p = float(wv[idx[e_ik]] ** self.p)
                    R[i] += w_ij_p * w_ik_p

        g = np.zeros(self.m, dtype=float)

        for e_i, (u, v) in enumerate(self.edges):
            w_e = float(wv[e_i])
            if w_e <= 0.0 and self.p < 1.0:
                raise ValueError("p must be >= 1")

            # dA_u/dw_e and dA_v/dw_e
            dA = float(self.p * (w_e ** (self.p - 1.0)))

            # dM_u/dw_e and dM_v/dw_e
            dM = float(-self.p * ((1.0 - w_e) ** (self.p - 1.0)) * float(B_edge[e_i]))

            # dR_u/dw_e and dR_v/dw_e
            def dR_at(node: int, other: int) -> float:
                # Sum over k common neighbors of node and other with triangle (node, other, k): w_{node,k}^p
                common = adj[node].intersection(adj[other])
                s = 0.0
                for k in common:
                    if k not in adj[other]:
                        continue
                    e_nk = (node, k) if node < k else (k, node)
                    if e_nk not in idx:
                        continue
                    s += float(wv[idx[e_nk]] ** self.p)
                return float(self.p * (w_e ** (self.p - 1.0)) * s)

            dR_u = dR_at(u, v)
            dR_v = dR_at(v, u)

            # node contributions
            for node, dR_node in ((u, dR_u), (v, dR_v)):
                coeff_A = float(self.theta_A / (1.0 + A[node])) if self.theta_A != 0.0 else 0.0
                coeff_M = float(self.theta_M / (1.0 + M[node])) if self.theta_M != 0.0 else 0.0
                coeff_R = float(self.theta_R / (1.0 + R[node])) if self.theta_R != 0.0 else 0.0
                g[e_i] += coeff_A * dA
                g[e_i] += coeff_M * dM
                g[e_i] -= coeff_R * dR_node

        return g

    def hess(self, w: np.ndarray, theta: float | None = None) -> np.ndarray:
        _ = theta
        wv = np.asarray(w, dtype=float)
        if wv.shape != (self.m,):
            raise ValueError("w has wrong shape")

        idx = self._edge_index()
        adj = self._adjacency()

        B_edge = np.zeros(self.m, dtype=float)
        for e_i, (u, v) in enumerate(self.edges):
            B_edge[e_i] = self._brokerage(self._kappa(adj, u, v))

        # Node-level scalars A_i, M_i, R_i
        A = np.zeros(self.n, dtype=float)
        M = np.zeros(self.n, dtype=float)
        R = np.zeros(self.n, dtype=float)

        for e_i, (u, v) in enumerate(self.edges):
            w_e = float(wv[e_i])
            w_e_p = float(w_e**self.p)
            A[u] += w_e_p
            A[v] += w_e_p

            weak = float((1.0 - w_e) ** self.p) * float(B_edge[e_i])
            M[u] += weak
            M[v] += weak

        for i in range(self.n):
            neigh = sorted(adj[i])
            for a_pos in range(len(neigh)):
                j = neigh[a_pos]
                e_ij = (i, j) if i < j else (j, i)
                if e_ij not in idx:
                    continue
                w_ij_p = float(wv[idx[e_ij]] ** self.p)
                for b_pos in range(a_pos + 1, len(neigh)):
                    k = neigh[b_pos]
                    if k not in adj[j]:
                        continue
                    e_ik = (i, k) if i < k else (k, i)
                    if e_ik not in idx:
                        continue
                    w_ik_p = float(wv[idx[e_ik]] ** self.p)
                    R[i] += w_ij_p * w_ik_p

        H = np.zeros((self.m, self.m), dtype=float)

        # Helper for redundancy second derivatives at a node.
        def redundancy_second(node: int, nb1: int, nb2: int, w_n_nb1: float, w_n_nb2: float) -> float:
            if nb1 == nb2:
                # diag: p(p-1) w^{p-2} * sum_{k triangle} w_{node,k}^p
                common = adj[node].intersection(adj[nb1])
                s = 0.0
                for k in common:
                    e_nk = (node, k) if node < k else (k, node)
                    if e_nk in idx:
                        s += float(wv[idx[e_nk]] ** self.p)
                return float(self.p * (self.p - 1.0) * (w_n_nb1 ** (self.p - 2.0)) * s)

            # off-diagonal: triangle indicator * p^2 w1^{p-1} w2^{p-1}
            if nb2 in adj[nb1]:
                return float((self.p**2) * (w_n_nb1 ** (self.p - 1.0)) * (w_n_nb2 ** (self.p - 1.0)))
            return 0.0

        for node in range(self.n):
            # incident edges at node
            incident: list[tuple[int, int]] = []  # (edge_index, neighbor)
            for nb in adj[node]:
                e = (node, nb) if node < nb else (nb, node)
                if e in idx:
                    incident.append((idx[e], nb))

            if not incident:
                continue

            # first derivatives for A/M/R at this node
            dA = {}
            dM = {}
            dR = {}
            d2A = {}
            d2M = {}
            d2R = {}

            for e_i, nb in incident:
                w_e = float(wv[e_i])
                dA[e_i] = float(self.p * (w_e ** (self.p - 1.0)))
                d2A[e_i] = float(self.p * (self.p - 1.0) * (w_e ** (self.p - 2.0)))

                dM[e_i] = float(-self.p * ((1.0 - w_e) ** (self.p - 1.0)) * float(B_edge[e_i]))
                d2M[e_i] = float(self.p * (self.p - 1.0) * ((1.0 - w_e) ** (self.p - 2.0)) * float(B_edge[e_i]))

            # redundancy derivatives
            for e_i, nb in incident:
                w_e = float(wv[e_i])
                common = adj[node].intersection(adj[nb])
                s = 0.0
                for k in common:
                    e_nk = (node, k) if node < k else (k, node)
                    if e_nk in idx:
                        s += float(wv[idx[e_nk]] ** self.p)
                dR[e_i] = float(self.p * (w_e ** (self.p - 1.0)) * s)

            # second derivatives for redundancy
            for e_i, nb_i in incident:
                w_i = float(wv[e_i])
                # diag
                d2R[(e_i, e_i)] = redundancy_second(node, nb_i, nb_i, w_i, w_i)
                for e_j, nb_j in incident:
                    if e_j <= e_i:
                        continue
                    w_j = float(wv[e_j])
                    v = redundancy_second(node, nb_i, nb_j, w_i, w_j)
                    if v != 0.0:
                        d2R[(e_i, e_j)] = v
                        d2R[(e_j, e_i)] = v

            # coefficients for chain rule
            invA = float(1.0 / (1.0 + A[node]))
            invM = float(1.0 / (1.0 + M[node]))
            invR = float(1.0 / (1.0 + R[node])) if (1.0 + R[node]) != 0 else 0.0

            for e_i, _ in incident:
                for e_j, _ in incident:
                    # A contribution
                    if self.theta_A != 0.0:
                        d2 = d2A[e_i] if e_i == e_j else 0.0
                        H[e_i, e_j] += float(self.theta_A * (invA * d2 - (invA**2) * dA[e_i] * dA[e_j]))

                    # M contribution
                    if self.theta_M != 0.0:
                        d2 = d2M[e_i] if e_i == e_j else 0.0
                        H[e_i, e_j] += float(self.theta_M * (invM * d2 - (invM**2) * dM[e_i] * dM[e_j]))

                    # R contribution (negative)
                    if self.theta_R != 0.0:
                        d2 = float(d2R.get((e_i, e_j), 0.0))
                        H[e_i, e_j] -= float(self.theta_R * (invR * d2 - (invR**2) * dR[e_i] * dR[e_j]))

        return H


def make_real_phi_v0_test_spec() -> RealPhiV0Spec:
    """Deterministic small graph with triangles; m <= 12."""

    # Two triangles sharing a node: (0,1,2) and (2,3,4)
    edges = [(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (2, 4)]
    return RealPhiV0Spec(
        n=5,
        edges=edges,
        theta_A=1.0,
        theta_M=0.5,
        theta_R=0.25,
        p=2.0,
    )
