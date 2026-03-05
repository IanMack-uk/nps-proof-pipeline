#!/usr/bin/env python3
"""
Optional helper to run a fresh persistent Real Φ v0 regime run after implementation.

Usage (repo root):
  PYTHONPATH=src python taskpack_task_B_2_real_phi_equilibrium_regime/SCRIPTS/run_real_phi_b2.py
"""
from __future__ import annotations
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CERT = REPO / "cert_artifacts"

def rid() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

def run(cmd: list[str], env_extra: dict | None = None) -> None:
    env = {**os.environ, "PYTHONPATH": str(REPO / "src")}
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(cmd, cwd=str(REPO), env=env)
    if p.returncode != 0:
        raise SystemExit(p.returncode)

def main() -> int:
    run_id = rid()
    run_dir = CERT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    run(["python", "-m", "nps.phases.phase_0a.build_cas0a", "--run-id", run_id])
    run(["python", "-m", "nps.phases.phase_a.build_casa", "--real-phi-v0", "--run-id", run_id, "--input", str(run_dir/"CAS-0A.json")])
    run(["python", "-m", "nps.phases.phase_a_prime.build_casa_prime", "--run-id", run_id, "--input", str(run_dir/"CAS-A.json")])

    run(["python", "-m", "nps.phases.phase_0b.build_cas0b", "--run-id", run_id, "--input", str(run_dir/"CAS-A.json")])
    run(["python", "-m", "nps.phases.phase_b.build_casb", "--real-phi-v0", "--run-id", run_id, "--input", str(run_dir/"CAS-0B.json")])
    run(["python", "-m", "nps.phases.phase_b_prime.build_casb_prime", "--run-id", run_id, "--input", str(run_dir/"CAS-B.json")])

    print(f"Run complete: {run_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
