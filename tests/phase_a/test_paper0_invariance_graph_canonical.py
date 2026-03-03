from __future__ import annotations

import numpy as np
import pytest

from nps.core.errors import MathematicalInconsistency
from nps.models.graph.simple_graph import SimpleGraph
from nps.models.sandbox.domain_policies import NonnegativePolicy
from nps.phases.phase_a.coordinates.coordinate_paper0_candidates import (
    paper0_redundancy_candidate,
    paper0_separation_candidate,
)
from nps.phases.phase_a.coordinates.coordinate_paper0_validation import check_automorphism_invariance_graph
from nps.phases.phase_a.coordinates.coordinate_types import CoordinateDefinition, StructuralCoordinate
from nps.phases.phase_a.seed_paper0_coordinate_assumptions import seed_paper0_coordinate_assumptions
from nps.validation.validation_registry import ValidationRegistry


def test_paper0_graph_canonical_invariance() -> None:
    # Triangle + tail on n=4
    g = SimpleGraph(n=4, edges=[(0, 1), (1, 2), (0, 2), (2, 3)])
    m = len(g.edges)

    rng = np.random.default_rng(0)
    w = NonnegativePolicy().sample(m, rng)

    perms = [
        [1, 0, 2, 3],
        [2, 1, 0, 3],
    ]

    registry = ValidationRegistry()
    seed_paper0_coordinate_assumptions(registry)

    check_automorphism_invariance_graph(
        paper0_separation_candidate,
        g,
        w,
        radius=1,
        perms=perms,
        registry=registry,
    )
    check_automorphism_invariance_graph(
        paper0_redundancy_candidate,
        g,
        w,
        radius=1,
        perms=perms,
        registry=registry,
    )


def test_negative_control_raw_edge_index_breaks_invariance() -> None:
    class EdgeIndexCoordinate(CoordinateDefinition):
        def evaluate(self, e: int, w: np.ndarray) -> float:
            _ = w
            return float(e)

    def factory(_neigh: dict[int, set[int]]) -> StructuralCoordinate:
        return StructuralCoordinate(
            name="P0.NEG.edge_index",
            definition=EdgeIndexCoordinate(),
            domain="Omega",
            codomain="R",
            locality="GLOBAL",
            notes="Deliberate negative control",
        )

    g = SimpleGraph(n=4, edges=[(0, 1), (1, 2), (0, 2), (2, 3)])
    m = len(g.edges)

    rng = np.random.default_rng(0)
    w = NonnegativePolicy().sample(m, rng)

    perms = [
        [1, 0, 2, 3],
    ]

    registry = ValidationRegistry()
    seed_paper0_coordinate_assumptions(registry)

    with pytest.raises(MathematicalInconsistency, match="automorphism"):
        check_automorphism_invariance_graph(
            factory,
            g,
            w,
            radius=1,
            perms=perms,
            registry=registry,
        )
