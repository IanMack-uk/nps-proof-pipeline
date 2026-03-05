"""Phase B′: closure/approval for operator objects."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from nps.audit.cert_dependency_gate import compute_content_hash
from nps.audit.governance import maybe_install_governance, maybe_validate_run_dir_integrity
from nps.certification.artifacts import make_run_dir, write_json


def build_casb_prime(run_dir: Path, *, input_path: Path) -> Path:
    casb = json.loads(input_path.read_text(encoding="utf-8"))
    upstream_id = casb.get("cas_id")
    if not isinstance(upstream_id, str) or not upstream_id:
        raise RuntimeError("PhaseBPrime: invalid CAS-B input (missing cas_id)")

    blocking_issues: list[str] = []

    diagnostic = bool(getattr(build_casb_prime, "_diagnostic_allow_upstream_block", False)) or os.getenv(
        "NPS_DIAGNOSTIC", "0"
    ) == "1"

    # Upstream approval dependency: Phase A′ must be unblocked unless diagnostic mode.
    casa_prime_path = run_dir / "CAS-Ap.json"
    if casa_prime_path.exists():
        try:
            casa_p = json.loads(casa_prime_path.read_text(encoding="utf-8"))
            upstream_blocking = casa_p.get("blocking_issues")
            upstream_ok = isinstance(upstream_blocking, list) and len(upstream_blocking) == 0
            if not upstream_ok:
                msg = "UPSTREAM_BLOCK: Phase A′ not approved; Phase B′ cannot approve under certification mode."
                if diagnostic:
                    # Non-blocking note: record but do not block approval.
                    blocking_issues.append("DIAGNOSTIC_NOTE: " + msg)
                else:
                    blocking_issues.append(msg)
        except Exception:
            if not diagnostic:
                blocking_issues.append("UPSTREAM_BLOCK: unable to parse CAS-Ap.json; Phase B′ cannot approve.")

    checks = casb.get("checks")
    if checks is not None:
        if not isinstance(checks, list):
            blocking_issues.append("CAS-B checks is not a list")
        else:
            failed = []
            for chk in checks:
                if not isinstance(chk, dict):
                    continue
                cid = chk.get("check_id")
                if isinstance(cid, str) and cid.startswith("CHK.B."):
                    if chk.get("ok") is not True:
                        failed.append(cid)
            if failed:
                blocking_issues.append("CHK.B.* checks failed: " + ", ".join(sorted(set(failed))))

    # Optional CI/cert-run hygiene gate: fail if run root contains ambiguous CAS variants.
    try:
        maybe_validate_run_dir_integrity(run_dir)
    except Exception as e:
        blocking_issues.append("RUN_DIR_INTEGRITY: " + str(e))

    def _is_blocking_issue(msg: str) -> bool:
        return not msg.startswith("DIAGNOSTIC_NOTE:")

    approved = not any(_is_blocking_issue(m) for m in blocking_issues)

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    payload: dict = {
        "cas_id": "CAS-Bp",
        "created_at": created_at,
        "inputs": [upstream_id],
        "content_hash": "",
        "programme": {
            "name": "Structural Differentiation / Ordering Theorem Programme",
            "version": "4.3",
            "phase": "B_prime",
        },
        "approved": bool(approved),
        "blocking_issues": blocking_issues,
        "trace": {
            "generated_by": {"tool": "nps.phases.phase_b_prime.build_casb_prime", "tool_version": "option2"},
            "consumed": {"casb_path": str(input_path)},
            "diagnostic": {"enabled": diagnostic},
        },
    }

    payload["content_hash"] = compute_content_hash(payload)

    out = run_dir / "CAS-Bp.json"
    write_json(out, payload)

    (run_dir / "PhaseB_prime_REPORT.md").write_text(
        "# Phase B′ Report\n\n" f"- CAS artefact: {out.name}\n" f"- Upstream: {upstream_id}\n" f"- Blocking issues: {len(blocking_issues)}\n",
        encoding="utf-8",
    )

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Build CAS-Bp (Phase B′) into cert_artifacts/<run_id>/")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--input", required=True)
    parser.add_argument("--diagnostic-allow-upstream-block", action="store_true")
    args = parser.parse_args()

    maybe_install_governance()
    run_dir = make_run_dir(args.run_id)
    setattr(build_casb_prime, "_diagnostic_allow_upstream_block", bool(args.diagnostic_allow_upstream_block))
    out = build_casb_prime(run_dir, input_path=Path(args.input))
    print(str(out))


if __name__ == "__main__":
    main()
