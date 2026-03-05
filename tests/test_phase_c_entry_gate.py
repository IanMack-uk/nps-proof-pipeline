from __future__ import annotations

import json
from pathlib import Path

import pytest

from nps.audit.phase_c_entry_gate import validate_phase_c_entry


def _write(p: Path, obj: dict) -> None:
    p.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def test_phase_c_entry_gate_allows_strict_concave_maximiser(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    _write(
        run_dir / "CAS-A.json",
        {
            "cas_id": "CAS-A",
            "checks": [
                {"check_id": "CHK.A.STATIONARITY", "ok": True},
                {"check_id": "CHK.A.NEG_DEF_HESSIAN", "ok": True},
            ],
        },
    )
    _write(
        run_dir / "CAS-B.json",
        {
            "cas_id": "CAS-B",
            "equilibrium_objective": "maximize",
            "equilibrium_regime": "strict_concave",
        },
    )
    _write(run_dir / "CAS-Bp.json", {"cas_id": "CAS-Bp"})

    validate_phase_c_entry(run_dir)


def test_phase_c_entry_gate_blocks_hyperbolic(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    _write(
        run_dir / "CAS-A.json",
        {
            "cas_id": "CAS-A",
            "checks": [
                {"check_id": "CHK.A.STATIONARITY", "ok": True},
                {"check_id": "CHK.A.NEG_DEF_HESSIAN", "ok": True},
            ],
        },
    )
    _write(
        run_dir / "CAS-B.json",
        {
            "cas_id": "CAS-B",
            "equilibrium_objective": "maximize",
            "equilibrium_regime": "hyperbolic",
        },
    )
    _write(run_dir / "CAS-Bp.json", {"cas_id": "CAS-Bp"})

    with pytest.raises(RuntimeError, match="quarantined"):
        validate_phase_c_entry(run_dir)
