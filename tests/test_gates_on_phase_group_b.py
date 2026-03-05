from __future__ import annotations

import json
from pathlib import Path

from nps.audit.cert_dependency_gate import validate_cert_dependency_integrity
from nps.phases.phase_0a.build_cas0a import build_cas0a
from nps.phases.phase_0b.build_cas0b import build_cas0b
from nps.phases.phase_a.build_casa import build_casa
from nps.phases.phase_a_prime.build_casa_prime import build_casa_prime
from nps.phases.phase_b.build_casb import build_casb
from nps.phases.phase_b_prime.build_casb_prime import build_casb_prime


def test_gates_on_phase_group_b(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("NPS_IMPORT_FIREWALL", "1")
    monkeypatch.setenv("NPS_CAS_GATE", "1")
    monkeypatch.setenv("NPS_CERT_DEP_GATE", "1")

    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    cas0a_path = build_cas0a(run_dir)

    setattr(build_casa, "_toy_quadratic_enabled", True)
    casa_path = build_casa(run_dir, input_path=cas0a_path)

    casa_prime_path = build_casa_prime(run_dir, input_path=casa_path)
    casa_prime = json.loads(casa_prime_path.read_text(encoding="utf-8"))
    assert casa_prime.get("blocking_issues") == []

    cas0b_path = build_cas0b(run_dir, input_path=casa_path)

    setattr(build_casb, "_toy_quadratic_enabled", True)
    casb_path = build_casb(run_dir, input_path=cas0b_path)

    casbp_path = build_casb_prime(run_dir, input_path=casb_path)
    casbp = json.loads(casbp_path.read_text(encoding="utf-8"))
    assert casbp.get("approved") is True

    validate_cert_dependency_integrity(run_dir)
