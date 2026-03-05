#!/usr/bin/env python3
"""
Optional helper to generate a strict-concave minus-phi persistent run after implementation.

Usage (repo root):
  PYTHONPATH=src python taskpack_task_B_3_1_phase_a_certified_objective_minus_phi/SCRIPTS/run_b3_1_strict_concave_minus_phi.py

This will:
- create a run_id
- run 0A/A/A′ and 0B/B/B′ with certified-objective=minus-phi
- validate phase C entry gate
- write cert_artifacts/<run_id>/B3_1_StrictConcave_MinusPhi_RUN_REPORT.md
"""
from __future__ import annotations
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CERT = REPO / "cert_artifacts"

def rid() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

def run(cmd: list[str]) -> None:
    env = {**os.environ, "PYTHONPATH": str(REPO / "src")}
    p = subprocess.run(cmd, cwd=str(REPO), env=env, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stdout)
        print(p.stderr)
        raise SystemExit(p.returncode)

def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))

def main() -> int:
    run_id = rid()
    run_dir = CERT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    run(["python","-m","nps.phases.phase_0a.build_cas0a","--run-id",run_id])

    run(["python","-m","nps.phases.phase_a.build_casa",
         "--real-phi-v0","--certified-objective","minus-phi",
         "--run-id",run_id,"--input",str(run_dir/"CAS-0A.json")])

    run(["python","-m","nps.phases.phase_a_prime.build_casa_prime",
         "--run-id",run_id,"--input",str(run_dir/"CAS-A.json")])

    run(["python","-m","nps.phases.phase_0b.build_cas0b",
         "--run-id",run_id,"--input",str(run_dir/"CAS-A.json")])

    run(["python","-m","nps.phases.phase_b.build_casb",
         "--real-phi-v0","--certified-objective","minus-phi",
         "--objective","maximize","--regime","strict-concave",
         "--candidate-method","stationary-multistart",
         "--run-id",run_id,"--input",str(run_dir/"CAS-0B.json")])

    run(["python","-m","nps.phases.phase_b_prime.build_casb_prime",
         "--run-id",run_id,"--input",str(run_dir/"CAS-B.json")])

    # Phase C gate
    env = {**os.environ, "PYTHONPATH": str(REPO / "src")}
    gate_cmd = ["python","-c",
        "from pathlib import Path; from nps.audit.phase_c_entry_gate import validate_phase_c_entry; "
        f"validate_phase_c_entry(Path('cert_artifacts/{run_id}'))"
    ]
    p = subprocess.run(gate_cmd, cwd=str(REPO), env=env, capture_output=True, text=True)
    gate_ok = (p.returncode == 0)
    gate_msg = (p.stdout + p.stderr).strip()

    casa = load_json(run_dir/"CAS-A.json")
    casap = load_json(run_dir/"CAS-Ap.json")
    casb = load_json(run_dir/"CAS-B.json")
    casbp = load_json(run_dir/"CAS-Bp.json")

    # Extract key witnesses
    def find_check(cas, check_id):
        for c in cas.get("checks", []):
            if c.get("check_id") == check_id:
                return c
        return None

    chk_stat = find_check(casa, "CHK.A.STATIONARITY")
    chk_negdef = find_check(casa, "CHK.A.NEG_DEF_HESSIAN")

    report_lines = []
    report_lines.append("# B3.1 Strict-Concave Minus-Phi Run Report")
    report_lines.append("")
    report_lines.append(f"run_id: {run_id}")
    report_lines.append(f"run_dir: cert_artifacts/{run_id}/")
    report_lines.append("")
    report_lines.append("## Certified objective")
    report_lines.append(f"- CAS-A derivative_definition.certified_objective: {casa.get('derivative_definition',{}).get('certified_objective')}")
    report_lines.append(f"- CAS-B certified_objective: {casb.get('certified_objective')}")
    report_lines.append("")
    report_lines.append("## Approvals")
    report_lines.append(f"- CAS-Ap approved: {casap.get('approved')}")
    report_lines.append(f"- CAS-Bp approved: {casbp.get('approved')}")
    report_lines.append("")
    report_lines.append("## Phase C entry gate")
    report_lines.append(f"- PASS: {gate_ok}")
    if gate_msg:
        report_lines.append("```")
        report_lines.append(gate_msg[:2000])
        report_lines.append("```")
    report_lines.append("")
    report_lines.append("## Key witnesses")
    if chk_stat:
        report_lines.append(f"- CHK.A.STATIONARITY ok: {chk_stat.get('ok')}, witness: {chk_stat.get('witness')}")
    if chk_negdef:
        report_lines.append(f"- CHK.A.NEG_DEF_HESSIAN ok: {chk_negdef.get('ok')}, witness: {chk_negdef.get('witness')}")
    report_path = run_dir/"B3_1_StrictConcave_MinusPhi_RUN_REPORT.md"
    report_path.write_text("\\n".join(report_lines)+\"\\n\", encoding=\"utf-8\")
    print(f\"Wrote run report: {report_path}\")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
