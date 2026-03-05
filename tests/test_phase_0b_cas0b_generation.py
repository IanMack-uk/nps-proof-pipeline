from __future__ import annotations

import json
from pathlib import Path

from nps.phases.phase_0a.build_cas0a import build_cas0a
from nps.phases.phase_0b.build_cas0b import build_cas0b
from nps.phases.phase_a.build_casa import build_casa


def test_phase_0b_cas0b_generation(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    cas0a_path = build_cas0a(run_dir)
    setattr(build_casa, "_toy_quadratic_enabled", True)
    casa_path = build_casa(run_dir, input_path=cas0a_path)

    cas0b_path = build_cas0b(run_dir, input_path=casa_path)

    cas0b = json.loads(cas0b_path.read_text(encoding="utf-8"))
    assert cas0b.get("cas_id") == "CAS-0B"
    assert "created_at" in cas0b
    assert cas0b.get("inputs") == ["CAS-A"]
    assert isinstance(cas0b.get("phase_targets"), list)
    assert isinstance(cas0b.get("dependency_table"), list)
