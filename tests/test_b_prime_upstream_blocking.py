from __future__ import annotations

import json
from pathlib import Path

from nps.phases.phase_b_prime.build_casb_prime import build_casb_prime


def test_b_prime_blocks_if_a_prime_blocked_by_default(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    # Minimal CAS-B to allow builder to run.
    (run_dir / "CAS-B.json").write_text(
        json.dumps({"cas_id": "CAS-B", "checks": []}, indent=2) + "\n",
        encoding="utf-8",
    )

    # Upstream A′ blocked.
    (run_dir / "CAS-Ap.json").write_text(
        json.dumps({"cas_id": "CAS-Ap", "blocking_issues": ["x"]}, indent=2) + "\n",
        encoding="utf-8",
    )

    out = build_casb_prime(run_dir, input_path=run_dir / "CAS-B.json")
    bp = json.loads(out.read_text(encoding="utf-8"))

    assert bp["approved"] is False
    assert any("UPSTREAM_BLOCK" in s for s in bp.get("blocking_issues", []))


def test_b_prime_allows_diagnostic_override(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "CAS-B.json").write_text(
        json.dumps({"cas_id": "CAS-B", "checks": []}, indent=2) + "\n",
        encoding="utf-8",
    )
    (run_dir / "CAS-Ap.json").write_text(
        json.dumps({"cas_id": "CAS-Ap", "blocking_issues": ["x"]}, indent=2) + "\n",
        encoding="utf-8",
    )

    setattr(build_casb_prime, "_diagnostic_allow_upstream_block", True)
    out = build_casb_prime(run_dir, input_path=run_dir / "CAS-B.json")
    bp = json.loads(out.read_text(encoding="utf-8"))

    assert bp["approved"] is True
    assert isinstance(bp.get("blocking_issues"), list)
    assert any("DIAGNOSTIC_NOTE" in s for s in bp.get("blocking_issues", []))
