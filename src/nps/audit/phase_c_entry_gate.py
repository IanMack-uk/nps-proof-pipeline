from __future__ import annotations

import json
import os
from pathlib import Path


def _has_ok_check(cas: dict, check_id: str) -> bool:
    checks = cas.get("checks")
    if not isinstance(checks, list):
        return False
    for chk in checks:
        if not isinstance(chk, dict):
            continue
        if chk.get("check_id") == check_id:
            return chk.get("ok") is True
    return False


def validate_phase_c_entry(run_dir: Path) -> None:
    casb_path = run_dir / "CAS-B.json"
    casbp_path = run_dir / "CAS-Bp.json"

    if not casb_path.exists():
        raise RuntimeError("Phase C entry gate: missing CAS-B.json")
    if not casbp_path.exists():
        raise RuntimeError("Phase C entry gate: missing CAS-Bp.json")

    casb = json.loads(casb_path.read_text(encoding="utf-8"))
    _ = json.loads(casbp_path.read_text(encoding="utf-8"))

    diagnostic = os.getenv("NPS_DIAGNOSTIC", "0") == "1"

    eq_obj = casb.get("equilibrium_objective")
    eq_regime = casb.get("equilibrium_regime")

    if eq_regime == "hyperbolic":
        raise RuntimeError("Phase C quarantined under hyperbolic-only regime.")

    if eq_obj != "maximize" or eq_regime != "strict_concave":
        raise RuntimeError(
            "Phase C entry gate: requires equilibrium_objective='maximize' and equilibrium_regime='strict_concave'"
        )

    casa_path = run_dir / "CAS-A.json"
    if not casa_path.exists():
        raise RuntimeError("Phase C entry gate: missing CAS-A.json (required for CHK.A.* prerequisites)")

    casa = json.loads(casa_path.read_text(encoding="utf-8"))

    stationarity_ok = _has_ok_check(casa, "CHK.A.STATIONARITY")
    neg_def_ok = _has_ok_check(casa, "CHK.A.NEG_DEF_HESSIAN")

    if not stationarity_ok or not neg_def_ok:
        msg = (
            "Phase C entry gate: strict concavity prerequisites not satisfied: "
            f"CHK.A.STATIONARITY ok={stationarity_ok}, CHK.A.NEG_DEF_HESSIAN ok={neg_def_ok}"
        )
        if diagnostic:
            raise RuntimeError(msg)
        raise RuntimeError(msg)
