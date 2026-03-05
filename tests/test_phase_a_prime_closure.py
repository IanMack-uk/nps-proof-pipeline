from __future__ import annotations

import json
from pathlib import Path

from nps.phases.phase_0a.build_cas0a import build_cas0a
from nps.phases.phase_a.build_casa import build_casa
from nps.phases.phase_a_prime.build_casa_prime import build_casa_prime


def test_phase_a_prime_generates_casa_prime(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    cas0a_path = build_cas0a(run_dir)
    casa_path = build_casa(run_dir, input_path=cas0a_path)

    ap_path = build_casa_prime(run_dir, input_path=casa_path)
    ap = json.loads(ap_path.read_text(encoding="utf-8"))

    casa = json.loads(casa_path.read_text(encoding="utf-8"))

    assert ap["cas_id"] == "CAS-Ap"
    assert ap["inputs"] == [casa["cas_id"]]

    assert ap.get("blocking_issues") == []
