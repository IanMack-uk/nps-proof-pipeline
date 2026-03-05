from __future__ import annotations

import json
from pathlib import Path

from nps.phases.phase_0a.build_cas0a import build_cas0a
from nps.phases.phase_a.build_casa import build_casa


def _get_chk(casa: dict, check_id: str) -> dict:
    for c in casa.get("checks", []):
        if isinstance(c, dict) and c.get("check_id") == check_id:
            return c
    raise AssertionError(f"missing check_id={check_id}")


def test_phase_a_real_phi_certified_objective_phi_vs_minus_phi(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    cas0a_path = build_cas0a(run_dir)

    # minus_phi
    try:
        setattr(build_casa, "_real_phi_v0_enabled", True)
        setattr(build_casa, "_certified_objective", "minus_phi")
        casa_path = build_casa(run_dir, input_path=cas0a_path)
        casa = json.loads(casa_path.read_text(encoding="utf-8"))

        assert casa.get("derivative_definition", {}).get("certified_objective") == "minus_phi"

        st = _get_chk(casa, "CHK.A.STATIONARITY")
        assert st.get("ok") is True

        curv = _get_chk(casa, "CHK.A.NEG_DEF_HESSIAN")
        assert curv.get("ok") is True
    finally:
        setattr(build_casa, "_real_phi_v0_enabled", False)
        setattr(build_casa, "_toy_quadratic_enabled", False)

    # phi
    try:
        setattr(build_casa, "_real_phi_v0_enabled", True)
        setattr(build_casa, "_certified_objective", "phi")
        casa_path = build_casa(run_dir, input_path=cas0a_path)
        casa = json.loads(casa_path.read_text(encoding="utf-8"))

        assert casa.get("derivative_definition", {}).get("certified_objective") == "phi"

        st = _get_chk(casa, "CHK.A.STATIONARITY")
        assert st.get("ok") is True

        curv = _get_chk(casa, "CHK.A.NEG_DEF_HESSIAN")
        assert curv.get("ok") is False
    finally:
        setattr(build_casa, "_real_phi_v0_enabled", False)
        setattr(build_casa, "_toy_quadratic_enabled", False)
