from __future__ import annotations

import json
from pathlib import Path

from nps.phases.phase_0a.build_cas0a import build_cas0a
from nps.phases.phase_a.build_casa import build_casa


def test_phase_a_generates_casa_consuming_cas0a(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    cas0a_path = build_cas0a(run_dir)
    cas0a = json.loads(cas0a_path.read_text(encoding="utf-8"))

    casa_path = build_casa(run_dir, input_path=cas0a_path)
    casa = json.loads(casa_path.read_text(encoding="utf-8"))

    assert casa["cas_id"] == "CAS-A"
    assert casa["inputs"] == [cas0a["cas_id"]]

    discharge = casa.get("obligations_discharge")
    assert isinstance(discharge, list)

    cas0a_obligations = cas0a.get("obligations", [])
    if cas0a_obligations:
        cas0a_ob_ids = {o.get("obligation_id") for o in cas0a_obligations}
        casa_ob_ids = {o.get("obligation_id") for o in discharge}
        assert cas0a_ob_ids.issubset(casa_ob_ids)
