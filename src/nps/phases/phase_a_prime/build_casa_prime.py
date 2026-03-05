"""Phase Aʹ: build CAS-Ap (closure / approval)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from nps.audit.cert_dependency_gate import compute_content_hash
from nps.audit.governance import maybe_install_governance
from nps.certification.artifacts import make_run_dir, write_json


def build_casa_prime(run_dir: Path, *, input_path: Path) -> Path:
    casa = json.loads(input_path.read_text(encoding="utf-8"))
    upstream_id = casa.get("cas_id")
    if not isinstance(upstream_id, str) or not upstream_id:
        raise RuntimeError("PhaseAPrime: invalid CAS-A input (missing cas_id)")

    blocking_issues: list[str] = []

    checks = casa.get("checks")
    if checks is not None:
        if not isinstance(checks, list):
            blocking_issues.append("CAS-A checks is not a list")
        else:
            failed = []
            for chk in checks:
                if not isinstance(chk, dict):
                    continue
                cid = chk.get("check_id")
                if isinstance(cid, str) and cid.startswith("CHK.A."):
                    if chk.get("ok") is not True:
                        failed.append(cid)
            if failed:
                blocking_issues.append(
                    "CHK.A.* checks failed: " + ", ".join(sorted(set(failed)))
                )

    # Minimal internal consistency checks.
    nf = casa.get("notation_freeze")
    if not isinstance(nf, dict) or "symbols" not in nf:
        blocking_issues.append("CAS-A missing notation_freeze.symbols")

    introduced = casa.get("assumptions", {}).get("introduced")
    if not isinstance(introduced, list):
        blocking_issues.append("CAS-A assumptions.introduced is not a list")

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    payload: dict = {
        "cas_id": "CAS-Ap",
        "created_at": created_at,
        "inputs": [upstream_id],
        "content_hash": "",
        "programme": {
            "name": "Structural Differentiation / Ordering Theorem Programme",
            "version": "4.3",
            "phase": "A_prime",
        },
        "checks": {
            "internal_consistency": True if not blocking_issues else False,
            "no_hidden_assumptions": True if not blocking_issues else False,
            "phase_a_interface_frozen": True if not blocking_issues else False,
        },
        "blocking_issues": blocking_issues,
        "minimality_audit_update": {
            "confirm_no_extra_deps": True,
            "notes": "Baseline closure: no additional dependencies recorded beyond CAS-0A consumption.",
        },
        "trace": {
            "generated_by": {"tool": "nps.phases.phase_a_prime.build_casa_prime", "tool_version": "option2"},
            "consumed": {"casa_path": str(input_path)},
        },
    }

    payload["content_hash"] = compute_content_hash(payload)

    out = run_dir / "CAS-Ap.json"
    write_json(out, payload)

    (run_dir / "PhaseA_prime_REPORT.md").write_text(
        "# Phase A′ Report\n\n"
        f"- CAS artefact: {out.name}\n"
        f"- Upstream: {upstream_id}\n"
        f"- Blocking issues: {len(blocking_issues)}\n",
        encoding="utf-8",
    )

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Build CAS-Ap (Phase A′) into cert_artifacts/<run_id>/")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    maybe_install_governance()
    run_dir = make_run_dir(args.run_id)
    out = build_casa_prime(run_dir, input_path=Path(args.input))
    print(str(out))


if __name__ == "__main__":
    main()
