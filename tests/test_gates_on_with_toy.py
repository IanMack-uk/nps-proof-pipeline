from __future__ import annotations

import json
from pathlib import Path

from nps.audit.cert_dependency_gate import validate_cert_dependency_integrity
from nps.phases.phase_0a.build_cas0a import build_cas0a
from nps.phases.phase_a.build_casa import build_casa
from nps.phases.phase_a_prime.build_casa_prime import build_casa_prime


def test_gates_on_with_toy_checks(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("NPS_IMPORT_FIREWALL", "1")
    monkeypatch.setenv("NPS_CAS_GATE", "1")
    monkeypatch.setenv("NPS_CERT_DEP_GATE", "1")

    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    cas0a_path = build_cas0a(run_dir)

    setattr(build_casa, "_toy_quadratic_enabled", True)
    casa_path = build_casa(run_dir, input_path=cas0a_path)

    casa = json.loads(casa_path.read_text(encoding="utf-8"))
    assert "checks" in casa

    by_id = {c.get("check_id"): c for c in casa.get("checks", []) if isinstance(c, dict)}
    assert by_id["CHK.A.NEG_DEF_HESSIAN"]["ok"] is True
    assert by_id["CHK.A.INTERIOR_FEASIBILITY"]["ok"] is True

    ap_path = build_casa_prime(run_dir, input_path=casa_path)
    ap = json.loads(ap_path.read_text(encoding="utf-8"))
    assert ap.get("blocking_issues") == []

    validate_cert_dependency_integrity(run_dir)
