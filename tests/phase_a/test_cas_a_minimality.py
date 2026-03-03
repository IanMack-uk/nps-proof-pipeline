from __future__ import annotations

import pytest

from nps.core.errors import MathematicalInconsistency
from nps.phases.phase_a.seed_cas_a_assumptions import seed_cas_a_assumptions
from nps.validation.evidence import Evidence
from nps.validation.records import ScopeTag
from nps.validation.status import CertificationStatus
from nps.validation.validation_registry import ValidationRegistry


def _seed_subset(registry: ValidationRegistry, *, keep: set[str]) -> None:
    temp = ValidationRegistry()
    seed_cas_a_assumptions(temp)

    for record in temp.list_assumptions():
        if record.id in keep:
            registry.register_assumption(record)


def test_cas_a_minimality_drop_test() -> None:
    all_ids = {
        "CAS-A.EXP.LOCALITY",
        "CAS-A.EXP.WELLPOSED",
        "CAS-A.EXP.REGULARITY",
        "CAS-A.NOTATION.STABILITY",
    }

    deliverable_map: dict[str, str] = {
        "CAS-A.EXP.LOCALITY": "tests/phase_a/test_structural_exposure_validation.py::test_exposure_w_e_is_edge_only_local",
        "CAS-A.EXP.WELLPOSED": "tests/phase_a/test_structural_exposure_validation.py::test_exposure_vector_well_posedness",
        "CAS-A.EXP.REGULARITY": "docs/specs/cas_a_structural_exposure.md#validation-checks",
        "CAS-A.NOTATION.STABILITY": "tests/phase_a/test_symbol_dictionary_freeze_phasea.py::test_freeze_prevents_mutation_and_is_versioned",
    }

    for dropped in sorted(all_ids):
        keep = set(all_ids)
        keep.remove(dropped)

        registry = ValidationRegistry()
        _seed_subset(registry, keep=keep)

        ev = Evidence(kind="test", ref=deliverable_map[dropped], summary=f"Minimality witness for {dropped}")

        with pytest.raises(MathematicalInconsistency, match="Unknown assumption id"):
            registry.add_evidence_to_assumption(dropped, ev)


def test_seed_cas_a_assumptions_registers_all_provisional() -> None:
    registry = ValidationRegistry()
    seed_cas_a_assumptions(registry)

    ids = [a.id for a in registry.list_assumptions()]
    assert ids == sorted(ids)

    expected = {
        "CAS-A.EXP.LOCALITY",
        "CAS-A.EXP.WELLPOSED",
        "CAS-A.EXP.REGULARITY",
        "CAS-A.NOTATION.STABILITY",
    }
    assert set(ids) == expected

    for a in registry.list_assumptions():
        assert a.status is CertificationStatus.PROVISIONAL
        assert a.scope in {ScopeTag.FOUNDATIONS, ScopeTag.DIFFERENTIABILITY}
