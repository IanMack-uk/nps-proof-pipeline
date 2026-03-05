from __future__ import annotations

import json
from pathlib import Path

from nps.audit.cert_dependency_gate import compute_content_hash
from nps.phases.phase_0a.build_cas0a import build_cas0a


def test_phase_0a_generates_cas0a(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    out = build_cas0a(run_dir)
    assert out.exists()

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["cas_id"] == "CAS-0A"
    assert payload["inputs"] == []

    for k in ("cas_id", "created_at", "inputs", "content_hash"):
        assert k in payload

    assert payload["content_hash"] == compute_content_hash(payload)

    assert isinstance(payload.get("phase_targets"), list)
    assert len(payload["phase_targets"]) >= 1

    assert isinstance(payload.get("dependency_table"), list)
    assert len(payload["dependency_table"]) >= 1
