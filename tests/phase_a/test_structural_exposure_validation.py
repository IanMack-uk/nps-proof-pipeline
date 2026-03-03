from __future__ import annotations

import numpy as np
import pytest

from nps.core.errors import MathematicalInconsistency
from nps.phases.phase_a.exposure.exposure_candidates import exposure_abs_f, exposure_w_e
from nps.phases.phase_a.exposure.exposure_types import ExposureDefinition, StructuralExposure
from nps.phases.phase_a.exposure.exposure_validation import check_edge_only_locality
from nps.phases.phase_a.seed_exposure_validation import seed_structural_exposure_ledger
from nps.validation.evidence import Evidence
from nps.validation.records import ScopeTag
from nps.validation.status import CertificationStatus
from nps.validation.validation_registry import ValidationRegistry


def test_exposure_vector_well_posedness() -> None:
    m = 5
    rng = np.random.default_rng(0)
    w = rng.normal(size=m).astype(np.float64)
    theta = 0.5

    registry = ValidationRegistry()
    seed_structural_exposure_ledger(registry)

    exp = exposure_w_e()
    x = exp.evaluate_vector(w, theta, m, registry=registry)
    assert x.shape == (m,)
    assert np.all(np.isfinite(x))

    exp2 = exposure_abs_f()
    x2 = exp2.evaluate_vector(w, theta, m, registry=registry)
    assert x2.shape == (m,)
    assert np.all(np.isfinite(x2))


def test_exposure_w_e_is_edge_only_local() -> None:
    m = 5
    rng = np.random.default_rng(1)
    w = rng.normal(size=m).astype(np.float64)
    theta = 1.0
    e = 2

    registry = ValidationRegistry()
    seed_structural_exposure_ledger(registry)

    exp = exposure_w_e()
    check_edge_only_locality(exp, w, theta, e, registry=registry)


def test_negative_control_global_exposure_fails_edge_only_check() -> None:
    class GlobalSumExposure(ExposureDefinition):
        def evaluate(self, e: int, w: np.ndarray, theta: float) -> float:
            _ = e
            _ = theta
            return float(np.sum(w))

    exp = StructuralExposure(
        name="EXP.sumw",
        definition=GlobalSumExposure(),
        domain="Omega",
        codomain="R",
        regularity="UNKNOWN",
        locality="GLOBAL",
        requires_properties=set(),
        notes="Deliberately non-local negative control.",
    )

    rng = np.random.default_rng(2)
    w = rng.normal(size=5).astype(np.float64)

    registry = ValidationRegistry()
    seed_structural_exposure_ledger(registry)

    with pytest.raises(MathematicalInconsistency):
        check_edge_only_locality(exp, w, theta=0.0, e=0, registry=registry)


def test_evidence_logging_into_validation_registry() -> None:
    registry = ValidationRegistry()
    seed_structural_exposure_ledger(registry)

    items = registry.list_assumptions(scope=ScopeTag.FOUNDATIONS)
    matches = [a for a in items if a.id == "CAS-A.EXP.LOCALITY"]
    assert len(matches) == 1
    assert matches[0].status is CertificationStatus.PROVISIONAL

    ev = Evidence(
        kind="test",
        ref="tests/phase_a/test_structural_exposure_validation.py::test_exposure_w_e_is_edge_only_local",
        summary="Edge-only locality positive control for EXP.w_e",
    )
    registry.add_evidence_to_assumption("CAS-A.EXP.LOCALITY", ev)

    matches2 = [a for a in registry.list_assumptions(scope=ScopeTag.FOUNDATIONS) if a.id == "CAS-A.EXP.LOCALITY"]
    assert len(matches2) == 1
    assert len(matches2[0].evidence) == 1
    assert matches2[0].evidence[0].ref == ev.ref
