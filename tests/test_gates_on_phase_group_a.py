from __future__ import annotations

import os
from pathlib import Path

from nps.audit.cert_dependency_gate import validate_cert_dependency_integrity
from nps.phases.phase_0a.build_cas0a import build_cas0a
from nps.phases.phase_a.build_casa import build_casa
from nps.phases.phase_a_prime.build_casa_prime import build_casa_prime


def test_phase_group_a_with_gates_on(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("NPS_IMPORT_FIREWALL", "1")
    monkeypatch.setenv("NPS_CAS_GATE", "1")
    monkeypatch.setenv("NPS_CERT_DEP_GATE", "1")

    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    cas0a_path = build_cas0a(run_dir)
    casa_path = build_casa(run_dir, input_path=cas0a_path)
    _ = build_casa_prime(run_dir, input_path=casa_path)

    # Validate chain integrity for present CAS artefacts.
    validate_cert_dependency_integrity(run_dir)
