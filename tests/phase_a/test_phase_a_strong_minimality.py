from __future__ import annotations

import numpy as np
import pytest

from nps.certification.dependency_registry import DependencyRegistry
from nps.core.errors import MathematicalInconsistency
from nps.models.toy.locality import ring_neighborhood
from nps.models.toy.potentials import grad_phi
from nps.phases.phase_0a.build_cas0a import build_cas0a_registry
from nps.phases.phase_a.build_casa import build_phase_a_symbols
from nps.phases.phase_a.closure_audit import run_phase_a_coherence_audit
from nps.phases.phase_a.coordinates.coordinate_candidates import coordinate_r_zero, coordinate_s_w_e
from nps.phases.phase_a.coordinates.coordinate_validation import check_phase_b_contract
from nps.phases.phase_a.exposure.exposure_candidates import exposure_w_e
from nps.phases.phase_a.exposure.exposure_validation import check_edge_only_locality
from nps.phases.phase_a.seed_cas_a_assumptions import seed_cas_a_assumptions
from nps.phases.phase_a.seed_coordinate_validation import seed_coordinate_assumptions
from nps.validation.validation_registry import ValidationRegistry


def test_strong_minimality_missing_exp_locality_blocks_locality_check() -> None:
    registry = ValidationRegistry()
    seed_cas_a_assumptions(registry)

    # remove EXP.LOCALITY by rebuilding without it
    registry2 = ValidationRegistry()
    for a in registry.list_assumptions():
        if a.id != "CAS-A.EXP.LOCALITY":
            registry2.register_assumption(a)

    w = np.array([0.1, -0.2, 0.3], dtype=np.float64)
    with pytest.raises(MathematicalInconsistency, match="Unknown assumption id: CAS-A.EXP.LOCALITY"):
        check_edge_only_locality(exposure_w_e(), w, theta=0.0, e=0, registry=registry2)


def test_strong_minimality_missing_exp_wellposed_blocks_exposure_eval() -> None:
    registry = ValidationRegistry()
    seed_cas_a_assumptions(registry)

    registry2 = ValidationRegistry()
    for a in registry.list_assumptions():
        if a.id != "CAS-A.EXP.WELLPOSED":
            registry2.register_assumption(a)

    w = np.array([0.1, -0.2, 0.3], dtype=np.float64)
    with pytest.raises(MathematicalInconsistency, match="Unknown assumption id: CAS-A.EXP.WELLPOSED"):
        exposure_w_e().evaluate_vector(w, theta=0.0, m=3, registry=registry2)


def test_strong_minimality_missing_contract_blocks_phase_b_contract_check() -> None:
    registry = ValidationRegistry()
    seed_coordinate_assumptions(registry)

    registry2 = ValidationRegistry()
    for a in registry.list_assumptions():
        if a.id != "CAS-A.CONTRACT.F_DEPENDENCE":
            registry2.register_assumption(a)

    m = 5
    w = np.zeros(m, dtype=np.float64)
    neigh = ring_neighborhood(m, radius=1)

    with pytest.raises(MathematicalInconsistency, match="Unknown assumption id: CAS-A.CONTRACT.F_DEPENDENCE"):
        check_phase_b_contract(
            grad_phi,
            coordinate_s_w_e(),
            coordinate_r_zero(),
            w,
            theta=0.0,
            e=0,
            neighborhood=neigh[0],
            registry=registry2,
        )


def test_phase_a_coherence_audit_passes_under_full_seed() -> None:
    cas0a = DependencyRegistry()
    build_cas0a_registry(cas0a)

    symbols = build_phase_a_symbols(cas0a)
    symbols.freeze("CAS-A.draft-closure")

    validation = ValidationRegistry()
    seed_cas_a_assumptions(validation)
    seed_coordinate_assumptions(validation)

    run_phase_a_coherence_audit(symbols, validation)
