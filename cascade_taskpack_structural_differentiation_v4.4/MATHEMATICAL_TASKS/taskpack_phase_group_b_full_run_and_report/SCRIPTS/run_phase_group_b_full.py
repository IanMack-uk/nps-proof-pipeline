#!/usr/bin/env python3
"""
Run Phase Group B end-to-end (including prerequisite Phase Group A)
and write a consolidated report into cert_artifacts/<run_id>/PhaseGroupB_RUN_REPORT.md

Usage (from repo root):
  PYTHONPATH=src python SCRIPTS/run_phase_group_b_full.py
"""
from __future__ import annotations

import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import json

REPO_ROOT = Path(__file__).resolve().parents[1]
CERT_ARTIFACTS = REPO_ROOT / "cert_artifacts"

def _run(cmd: list[str], extra_env: dict | None = None) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": str(REPO_ROOT / "src")}
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

def _utc_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

def main() -> int:
    run_id = _utc_run_id()
    run_dir = CERT_ARTIFACTS / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    commands = [
        ["python", "-m", "nps.phases.phase_0a.build_cas0a", "--run-id", run_id],
        ["python", "-m", "nps.phases.phase_a.build_casa", "--toy-quadratic", "--run-id", run_id, "--input", str(run_dir / "CAS-0A.json")],
        ["python", "-m", "nps.phases.phase_a_prime.build_casa_prime", "--run-id", run_id, "--input", str(run_dir / "CAS-A.json")],
        ["python", "-m", "nps.phases.phase_0b.build_cas0b", "--run-id", run_id, "--input", str(run_dir / "CAS-A.json")],
        ["python", "-m", "nps.phases.phase_b.build_casb", "--toy-quadratic", "--run-id", run_id, "--input", str(run_dir / "CAS-0B.json")],
        ["python", "-m", "nps.phases.phase_b_prime.build_casb_prime", "--run-id", run_id, "--input", str(run_dir / "CAS-B.json")],
    ]

    outputs: list[dict] = []
    ok = True
    for cmd in commands:
        proc = _run(cmd)
        outputs.append({"cmd": cmd, "returncode": proc.returncode, "output": proc.stdout})
        if proc.returncode != 0:
            ok = False
            break

    test_default = _run(["pytest", "-q"])
    test_gates = _run(["pytest", "-q"], extra_env={"NPS_IMPORT_FIREWALL":"1","NPS_CAS_GATE":"1","NPS_CERT_DEP_GATE":"1"})

    cas_b_path = run_dir / "CAS-B.json"
    cas_b = None
    if cas_b_path.exists():
        try:
            cas_b = json.loads(cas_b_path.read_text(encoding="utf-8"))
        except Exception:
            cas_b = None

    report_lines: list[str] = []
    report_lines.append("# Phase Group B — Consolidated Run Report")
    report_lines.append("")
    report_lines.append(f"- **run_id:** `{run_id}`")
    report_lines.append(f"- **timestamp (UTC):** `{datetime.now(timezone.utc).isoformat()}`")
    report_lines.append(f"- **run_dir:** `{run_dir}`")
    report_lines.append("- **command convention:** `PYTHONPATH=src python -m ...`")
    report_lines.append("")
    report_lines.append("## Commands executed")
    report_lines.append("")
    for item in outputs:
        cmd_str = " ".join(item["cmd"])
        report_lines.append(f"### `{cmd_str}`")
        report_lines.append(f"- returncode: `{item['returncode']}`")
        report_lines.append("```")
        report_lines.append(item["output"][:20000])
        report_lines.append("```")
        report_lines.append("")

    report_lines.append("## Artefacts present")
    report_lines.append("")
    expected = [
        "CAS-0A.json","Phase0A_REPORT.md",
        "CAS-A.json","PhaseA_REPORT.md",
        "CAS-Ap.json","PhaseA_prime_REPORT.md",
        "CAS-0B.json","Phase0B_REPORT.md",
        "CAS-B.json","PhaseB_REPORT.md",
        "CAS-Bp.json","PhaseB_prime_REPORT.md",
    ]
    for name in expected:
        report_lines.append(f"- `{name}`: {'✅' if (run_dir / name).exists() else '❌'}")
    report_lines.append("")

    report_lines.append("## Phase B check summary (from CAS-B.json)")
    report_lines.append("")
    if cas_b and isinstance(cas_b, dict) and isinstance(cas_b.get("checks"), list):
        for chk in cas_b.get("checks", []):
            cid = chk.get("check_id")
            okv = chk.get("ok")
            margin = chk.get("margin")
            witness = chk.get("witness") if isinstance(chk.get("witness"), dict) else {}
            witness_keys = list(witness.keys())[:3]
            witness_snip = {k: witness.get(k) for k in witness_keys}
            report_lines.append(f"- `{cid}` ok={okv} margin={margin} witness={witness_snip}")
    else:
        report_lines.append("- CAS-B checks not available (CAS-B.json missing or unreadable).")
    report_lines.append("")

    report_lines.append("## Test results")
    report_lines.append("")
    report_lines.append("### Default: `pytest -q`")
    report_lines.append("```")
    report_lines.append(test_default.stdout[:20000])
    report_lines.append("```")
    report_lines.append("")
    report_lines.append("### Gates-on: `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`")
    report_lines.append("```")
    report_lines.append(test_gates.stdout[:20000])
    report_lines.append("```")
    report_lines.append("")

    report_lines.append("## Outcome")
    report_lines.append("")
    report_lines.append("✅ Pipeline execution succeeded." if ok else "❌ Pipeline execution failed (see command output above).")
    report_lines.append("")

    out_path = run_dir / "PhaseGroupB_RUN_REPORT.md"
    out_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Wrote consolidated report: {out_path}")
    print(f"Run directory: {run_dir}")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
