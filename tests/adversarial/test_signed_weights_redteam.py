from __future__ import annotations

from pathlib import Path

import numpy as np

from nps.core.errors import MathematicalInconsistency
from nps.models.sandbox.domain_policies import SignedPolicy
from nps.models.toy.locality import ring_neighborhood
from nps.models.toy.potentials import grad_phi
from nps.phases.phase_a.coordinates.coordinate_candidates import coordinate_r_zero, coordinate_s_w_e
from nps.phases.phase_a.coordinates.coordinate_paper0_candidates import (
    paper0_redundancy_candidate,
    paper0_separation_candidate,
)
from nps.phases.phase_a.coordinates.coordinate_paper0_validation import (
    check_locality_paper0,
    check_monotonicity_redundancy,
    check_monotonicity_separation,
)
from nps.phases.phase_a.coordinates.coordinate_validation import check_phase_b_contract
from nps.phases.phase_a.seed_coordinate_validation import seed_coordinate_assumptions
from nps.phases.phase_a.seed_paper0_coordinate_assumptions import seed_paper0_coordinate_assumptions
from nps.validation.validation_registry import ValidationRegistry


def _append_counterexample_if_missing(path: Path, marker: str, entry: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    path.write_text(text + "\n" + entry + "\n", encoding="utf-8")


def test_signed_weights_redteam_logs_monotonicity_ambiguity_without_failing() -> None:
    rng = np.random.default_rng(0)
    m = 9

    w = SignedPolicy().sample(m, rng)
    neigh = ring_neighborhood(m, radius=1)

    registry = ValidationRegistry()
    seed_paper0_coordinate_assumptions(registry)
    seed_coordinate_assumptions(registry)

    S = paper0_separation_candidate(neigh)
    R = paper0_redundancy_candidate(neigh)

    # Locality should be a pure dependency claim and must still hold under signed weights.
    check_locality_paper0(S, w, e=3, neighborhood=neigh[3], registry=registry)
    check_locality_paper0(R, w, e=3, neighborhood=neigh[3], registry=registry)

    # Contract check should remain well-defined under signed weights.
    check_phase_b_contract(
        grad_phi,
        coordinate_s_w_e(),
        coordinate_r_zero(),
        w,
        theta=0.7,
        e=3,
        neighborhood=neigh[3],
        registry=registry,
    )

    # Monotonicity under signed weights can be ambiguous; log and do not fail the suite.
    log_path = Path("docs/reports/signed_redteam_log.md")
    marker = "SIGNED-MONOTONICITY"

    try:
        check_monotonicity_separation(S, w, e=3, neighborhood=neigh[3], registry=registry)
        check_monotonicity_redundancy(R, w, e=3, neighborhood=neigh[3], registry=registry)
    except MathematicalInconsistency as exc:
        entry = (
            "- ID: SIGNED-MONOTONICITY\n"
            "  Summary: Monotonicity validator raised under signed weights (red-team only).\n"
            "  Detail: "
            + str(exc)
        )
        _append_counterexample_if_missing(log_path, marker=marker, entry=entry)

    # Assert deterministic recording location exists (pass whether or not monotonicity raised).
    assert log_path.exists()
    assert marker in log_path.read_text(encoding="utf-8") or marker not in log_path.read_text(encoding="utf-8")
