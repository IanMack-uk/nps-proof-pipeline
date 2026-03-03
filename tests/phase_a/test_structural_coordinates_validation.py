from __future__ import annotations

import numpy as np
import pytest

from nps.core.errors import MathematicalInconsistency
from nps.models.toy.locality import ring_neighborhood
from nps.models.toy.potentials import grad_phi
from nps.phases.phase_a.coordinates.coordinate_candidates import (
    coordinate_r_sumw_negative_control,
    coordinate_r_zero,
    coordinate_s_w_e,
)
from nps.phases.phase_a.coordinates.coordinate_validation import check_phase_b_contract
from nps.phases.phase_a.seed_coordinate_validation import seed_coordinate_assumptions
from nps.validation.evidence import Evidence
from nps.validation.status import CertificationStatus
from nps.validation.validation_registry import ValidationRegistry


def test_coordinates_well_posedness() -> None:
    m = 5
    rng = np.random.default_rng(0)
    w = rng.normal(size=m).astype(np.float64)

    s = coordinate_s_w_e()
    r = coordinate_r_zero()

    xs = s.evaluate_vector(w, m)
    xr = r.evaluate_vector(w, m)

    assert xs.shape == (m,)
    assert xr.shape == (m,)
    assert np.all(np.isfinite(xs))
    assert np.all(np.isfinite(xr))


def test_phase_b_contract_positive_control() -> None:
    m = 7
    rng = np.random.default_rng(1)
    w = rng.normal(size=m).astype(np.float64)
    theta = 0.7
    e = 3

    neigh = ring_neighborhood(m, radius=1)
    registry = ValidationRegistry()
    seed_coordinate_assumptions(registry)
    check_phase_b_contract(
        grad_phi,
        coordinate_s_w_e(),
        coordinate_r_zero(),
        w,
        theta,
        e,
        neigh[e],
        registry=registry,
    )


def test_phase_b_contract_negative_control_detected() -> None:
    m = 7
    rng = np.random.default_rng(2)
    w = rng.normal(size=m).astype(np.float64)
    theta = 0.7
    e = 3

    neigh = ring_neighborhood(m, radius=1)

    def grad_phi_nonlocal(x: np.ndarray, t: float) -> np.ndarray:
        g = grad_phi(x.astype(np.float64), t)
        # Inject a deterministic non-local dependence into component e.
        # Choose an index outside N(e) for ring radius=1.
        j = 0
        g2 = g.copy()
        g2[e] = g2[e] + 0.25 * x[j]
        return g2

    with pytest.raises(MathematicalInconsistency, match="contract violated"):
        registry = ValidationRegistry()
        seed_coordinate_assumptions(registry)
        check_phase_b_contract(
            grad_phi_nonlocal,
            coordinate_s_w_e(),
            coordinate_r_sumw_negative_control(),
            w,
            theta,
            e,
            neigh[e],
            registry=registry,
        )


def test_coordinate_contract_evidence_logging() -> None:
    registry = ValidationRegistry()
    seed_coordinate_assumptions(registry)

    assert any(a.id == "CAS-A.CONTRACT.F_DEPENDENCE" for a in registry.list_assumptions())

    ev = Evidence(
        kind="test",
        ref="tests/phase_a/test_structural_coordinates_validation.py::test_phase_b_contract_positive_control",
        summary="Positive control contract check using toy grad_phi with S=w_e and R=0",
    )
    registry.add_evidence_to_assumption("CAS-A.CONTRACT.F_DEPENDENCE", ev)

    matches = [a for a in registry.list_assumptions() if a.id == "CAS-A.CONTRACT.F_DEPENDENCE"]
    assert len(matches) == 1
    assert matches[0].status is CertificationStatus.PROVISIONAL
    assert len(matches[0].evidence) == 1
    assert matches[0].evidence[0].ref == ev.ref
