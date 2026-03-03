from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from nps.core.errors import MathematicalInconsistency
from nps.models.toy.locality import ring_neighborhood
from nps.phases.phase_a.coordinates.coordinate_paper0_candidates import (
    paper0_redundancy_candidate,
    paper0_separation_candidate,
)
from nps.phases.phase_a.coordinates.coordinate_paper0_validation import (
    check_automorphism_invariance,
    check_locality_paper0,
    check_monotonicity_redundancy,
    check_monotonicity_separation,
)
from nps.phases.phase_a.coordinates.coordinate_types import CoordinateDefinition, StructuralCoordinate
from nps.phases.phase_a.seed_paper0_conjectures import seed_paper0_conjectures
from nps.phases.phase_a.seed_paper0_coordinate_assumptions import seed_paper0_coordinate_assumptions
from nps.validation.evidence import Evidence
from nps.validation.status import StatementStatus
from nps.validation.validation_registry import ValidationRegistry


def _append_counterexample_if_missing(path: Path, marker: str, entry: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    path.write_text(text + "\n" + entry + "\n", encoding="utf-8")


def test_paper0_candidates_finite_and_local() -> None:
    m = 9
    rng = np.random.default_rng(0)
    w = rng.normal(size=m).astype(np.float64)

    neigh = ring_neighborhood(m, radius=1)

    registry = ValidationRegistry()
    seed_paper0_coordinate_assumptions(registry)

    S = paper0_separation_candidate(neigh)
    R = paper0_redundancy_candidate(neigh)

    s_val = float(S.definition.evaluate(e=3, w=w))
    r_val = float(R.definition.evaluate(e=3, w=w))

    assert np.isfinite(s_val)
    assert np.isfinite(r_val)

    check_locality_paper0(S, w, e=3, neighborhood=neigh[3], registry=registry)
    check_locality_paper0(R, w, e=3, neighborhood=neigh[3], registry=registry)


def test_paper0_automorphism_invariance_controls() -> None:
    m = 8
    rng = np.random.default_rng(1)
    w = rng.normal(size=m).astype(np.float64)
    neigh = ring_neighborhood(m, radius=1)

    registry = ValidationRegistry()
    seed_paper0_coordinate_assumptions(registry)

    check_automorphism_invariance(paper0_separation_candidate, w, e=2, neighborhoods=neigh, registry=registry)
    check_automorphism_invariance(paper0_redundancy_candidate, w, e=2, neighborhoods=neigh, registry=registry)


def test_paper0_monotonicity_controls() -> None:
    m = 8
    rng = np.random.default_rng(2)
    w = rng.normal(size=m).astype(np.float64)
    neigh = ring_neighborhood(m, radius=1)

    registry = ValidationRegistry()
    seed_paper0_coordinate_assumptions(registry)

    S = paper0_separation_candidate(neigh)
    R = paper0_redundancy_candidate(neigh)

    check_monotonicity_separation(S, w, e=4, neighborhood=neigh[4], registry=registry)
    check_monotonicity_redundancy(R, w, e=4, neighborhood=neigh[4], registry=registry)


def test_negative_control_noninvariant_detected() -> None:
    class NonInvariantGlobal(CoordinateDefinition):
        def evaluate(self, e: int, w: np.ndarray) -> float:
            _ = e
            idx = 0
            return float(w[idx])

    def factory(_neigh: dict[int, set[int]]) -> StructuralCoordinate:
        return StructuralCoordinate(
            name="P0.NEG.non_invariant",
            definition=NonInvariantGlobal(),
            domain="Omega",
            codomain="R",
            locality="GLOBAL",
            notes="Deliberate negative control",
        )

    m = 7
    rng = np.random.default_rng(3)
    w = rng.normal(size=m).astype(np.float64)
    neigh = ring_neighborhood(m, radius=1)

    registry = ValidationRegistry()
    seed_paper0_coordinate_assumptions(registry)

    with pytest.raises(MathematicalInconsistency, match="automorphism"):
        check_automorphism_invariance(factory, w, e=1, neighborhoods=neigh, registry=registry)

    log_path = Path("docs/reports/paper0_coordinate_falsification_log.md")
    marker = "P0-NEG-AUTOMORPHISM"
    entry = "- ID: P0-NEG-AUTOMORPHISM\n  Summary: Deliberate non-invariant negative control coordinate violates automorphism invariance.\n  Test: tests/phase_a/test_paper0_structural_coordinates.py::test_negative_control_noninvariant_detected"
    _append_counterexample_if_missing(log_path, marker=marker, entry=entry)


def test_evidence_logging_and_conjecture_registration() -> None:
    registry = ValidationRegistry()
    seed_paper0_coordinate_assumptions(registry)
    seed_paper0_conjectures(registry)

    # evidence for locality check (passing control)
    ev = Evidence(
        kind="test",
        ref="tests/phase_a/test_paper0_structural_coordinates.py::test_paper0_candidates_finite_and_local",
        summary="Paper0 candidate coordinates: finite and pass locality control",
    )
    registry.add_evidence_to_assumption("CAS-A.COORD.PAPER0_LOCALITY", ev)

    st = registry.list_statements()
    matches = [s for s in st if s.id == "THM.P0.0_8_1"]
    assert len(matches) == 1
    assert matches[0].status is StatementStatus.CONJECTURE
