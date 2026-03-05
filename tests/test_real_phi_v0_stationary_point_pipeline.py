from __future__ import annotations

import json
from pathlib import Path

from nps.phases.phase_0a.build_cas0a import build_cas0a
from nps.phases.phase_0b.build_cas0b import build_cas0b
from nps.phases.phase_a.build_casa import build_casa
from nps.phases.phase_b.build_casb import build_casb


def test_real_phi_v0_uses_solver_w_star_and_adds_conditioning(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    cas0a_path = build_cas0a(run_dir)

    setattr(build_casa, "_real_phi_v0_enabled", True)
    casa_path = build_casa(run_dir, input_path=cas0a_path)
    casa = json.loads(casa_path.read_text(encoding="utf-8"))

    eq = casa.get("equilibrium_candidate")
    assert isinstance(eq, dict)
    assert isinstance(eq.get("w_star"), list)
    assert isinstance(eq.get("solver_info"), dict)

    cas0b_path = build_cas0b(run_dir, input_path=casa_path)

    setattr(build_casb, "_real_phi_v0_enabled", True)
    casb_path = build_casb(run_dir, input_path=cas0b_path)
    casb = json.loads(casb_path.read_text(encoding="utf-8"))

    assert isinstance(casb.get("equilibrium_candidate"), dict)

    check_ids = [c.get("check_id") for c in casb.get("checks", []) if isinstance(c, dict)]
    assert "CHK.B.JACOBIAN_CONDITIONING" in check_ids
