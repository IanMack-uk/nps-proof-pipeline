from __future__ import annotations

import json
from pathlib import Path

from nps.phases.phase_0a.build_cas0a import build_cas0a
from nps.phases.phase_a.build_casa import build_casa


def test_phase_a_writes_checks_when_toy_enabled(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    cas0a_path = build_cas0a(run_dir)

    setattr(build_casa, "_toy_quadratic_enabled", True)
    casa_path = build_casa(run_dir, input_path=cas0a_path)

    casa = json.loads(casa_path.read_text(encoding="utf-8"))
    assert "checks" in casa
    checks = casa["checks"]
    assert isinstance(checks, list)
    assert any(isinstance(c, dict) and str(c.get("check_id", "")).startswith("CHK.A.") for c in checks)

    by_id = {c.get("check_id"): c for c in checks if isinstance(c, dict)}
    assert by_id["CHK.A.NEG_DEF_HESSIAN"]["ok"] is True
    assert by_id["CHK.A.INTERIOR_FEASIBILITY"]["ok"] is True

    dd = casa.get("derivative_definition")
    assert isinstance(dd, dict)
    assert isinstance(dd.get("extension_id"), str)
