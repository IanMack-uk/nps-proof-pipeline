from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from numpy.typing import NDArray

from nps.core.errors import MathematicalInconsistency
from nps.models.graph.automorphisms import apply_node_permutation, image_edge_index, transport_edge_weights
from nps.models.graph.simple_graph import SimpleGraph
from nps.models.sandbox.neighborhoods import compute_edge_neighborhoods
from nps.phases.phase_a.coordinates.coordinate_types import StructuralCoordinate
from nps.validation.validation_registry import ValidationRegistry

_TOL = 1e-8


def check_locality_paper0(
    coord: StructuralCoordinate,
    w: NDArray[np.float64],
    e: int,
    neighborhood: set[int],
    *,
    registry: ValidationRegistry,
) -> None:
    registry.require_assumption_present("CAS-A.COORD.PAPER0_LOCALITY")

    base = float(coord.definition.evaluate(e, w))
    rng = np.random.default_rng(0)
    w2 = w.copy()
    for j in range(len(w)):
        if j in neighborhood:
            continue
        w2[j] = w2[j] + float(rng.normal(scale=0.1))

    v2 = float(coord.definition.evaluate(e, w2))
    if abs(v2 - base) > _TOL:
        raise MathematicalInconsistency("Paper0 coordinate locality violated")


@dataclass(frozen=True)
class EdgePermutation:
    perm: list[int]

    def inv(self) -> list[int]:
        inv = [0] * len(self.perm)
        for i, j in enumerate(self.perm):
            inv[j] = i
        return inv

    def apply_vector(self, w: NDArray[np.float64]) -> NDArray[np.float64]:
        idx: NDArray[np.int64] = np.array(self.perm, dtype=np.int64)
        out = np.take(w, idx)
        return out.astype(np.float64)

    def apply_edge(self, e: int) -> int:
        return self.inv()[e]

    def apply_neighborhoods(self, neighborhoods: dict[int, set[int]]) -> dict[int, set[int]]:
        inv = self.inv()
        out: dict[int, set[int]] = {}
        for e_old, n_old in neighborhoods.items():
            e_new = inv[e_old]
            out[e_new] = {inv[j] for j in n_old}
        return out


def check_automorphism_invariance(
    coord_factory: Callable[[dict[int, set[int]]], StructuralCoordinate],
    w: NDArray[np.float64],
    e: int,
    neighborhoods: dict[int, set[int]],
    *,
    registry: ValidationRegistry,
) -> None:
    registry.require_assumption_present("CAS-A.COORD.AUTOMORPHISM_INVARIANCE")

    m = len(w)
    perms = [
        EdgePermutation(perm=list(range(m))[::-1]),
        EdgePermutation(perm=list(range(1, m)) + [0]),
    ]

    base_coord = coord_factory(neighborhoods)
    base = float(base_coord.definition.evaluate(e, w))

    for p in perms:
        w_p = p.apply_vector(w)
        neigh_p = p.apply_neighborhoods(neighborhoods)
        coord_p = coord_factory(neigh_p)
        e_p = p.apply_edge(e)
        v_p = float(coord_p.definition.evaluate(e_p, w_p))
        if abs(v_p - base) > _TOL:
            raise MathematicalInconsistency("Paper0 coordinate automorphism invariance violated")


def check_automorphism_invariance_graph(
    coord_factory: Callable[[dict[int, set[int]]], StructuralCoordinate],
    g: SimpleGraph,
    w: NDArray[np.float64],
    *,
    radius: int,
    perms: list[list[int]],
    registry: ValidationRegistry,
) -> None:
    registry.require_assumption_present("CAS-A.COORD.AUTOMORPHISM_INVARIANCE")

    if w.shape != (len(g.edges),):
        raise MathematicalInconsistency("Weight vector shape mismatch")

    neighborhoods = compute_edge_neighborhoods(g, radius=radius)
    base_coord = coord_factory(neighborhoods)

    for perm in perms:
        g2 = apply_node_permutation(g, perm)
        w2 = transport_edge_weights(g, g2, perm, w)
        neighborhoods2 = compute_edge_neighborhoods(g2, radius=radius)
        coord2 = coord_factory(neighborhoods2)

        for e_idx in range(len(g.edges)):
            e2 = image_edge_index(g, g2, perm, e_idx)
            v1 = float(base_coord.definition.evaluate(e_idx, w))
            v2 = float(coord2.definition.evaluate(e2, w2))
            if abs(v2 - v1) > _TOL:
                raise MathematicalInconsistency("Paper0 coordinate automorphism invariance violated")


def check_monotonicity_separation(
    S: StructuralCoordinate,
    w: NDArray[np.float64],
    e: int,
    neighborhood: set[int],
    *,
    registry: ValidationRegistry,
) -> None:
    registry.require_assumption_present("CAS-A.COORD.MONOTONICITY_SEPARATION")

    base = float(S.definition.evaluate(e, w))
    w2 = w.copy()
    for j in neighborhood:
        if j == e:
            continue
        w2[j] = w2[j] + 0.2

    v2 = float(S.definition.evaluate(e, w2))
    if v2 - base > _TOL:
        raise MathematicalInconsistency("Paper0 separation monotonicity violated")


def check_monotonicity_redundancy(
    R: StructuralCoordinate,
    w: NDArray[np.float64],
    e: int,
    neighborhood: set[int],
    *,
    registry: ValidationRegistry,
) -> None:
    registry.require_assumption_present("CAS-A.COORD.MONOTONICITY_REDUNDANCY")

    base = float(R.definition.evaluate(e, w))
    w2 = w.copy()
    for j in neighborhood:
        if j == e:
            continue
        w2[j] = w2[j] + 0.2

    v2 = float(R.definition.evaluate(e, w2))
    if base - v2 > _TOL:
        raise MathematicalInconsistency("Paper0 redundancy monotonicity violated")
