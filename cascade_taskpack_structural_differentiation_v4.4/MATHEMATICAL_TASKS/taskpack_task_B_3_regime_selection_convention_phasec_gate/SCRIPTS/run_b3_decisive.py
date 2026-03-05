#!/usr/bin/env python3
"""
Optional helper to run a B.3 decisive regime experiment after implementation.

It runs Phase A (real-phi-v0) and Phase B twice:
- once with certified_objective=phi
- once with certified_objective=minus-phi

Usage (repo root):
  PYTHONPATH=src python taskpack_task_B_3_regime_selection_convention_phasec_gate/SCRIPTS/run_b3_decisive.py
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

    # Phase 0A / A / A′ (real phi)
    run(["python","-m","nps.phases.phase_0a.build_cas0a","--run-id",run_id])
    run(["python","-m","nps.phases.phase_a.build_casa","--real-phi-v0","--run-id",run_id,"--input",str(run_dir/"CAS-0A.json")])
    run(["python","-m","nps.phases.phase_a_prime.build_casa_prime","--run-id",run_id,"--input",str(run_dir/"CAS-A.json")])

    # Phase 0B
    run(["python","-m","nps.phases.phase_0b.build_cas0b","--run-id",run_id,"--input",str(run_dir/"CAS-A.json")])

    # Phase B: phi
    run(["python","-m","nps.phases.phase_b.build_casb",
         "--real-phi-v0","--run-id",run_id,"--input",str(run_dir/"CAS-0B.json"),
         "--objective","maximize","--certified-objective","phi",
         "--candidate-method","stationary-multistart","--regime","hyperbolic"])

    # Phase B: minus-phi (write into same run with suffix? implementation decides; likely separate CAS-B variants)
    # This script assumes implementation supports output suffix flags or separate run; adapt as needed.
    run(["python","-m","nps.phases.phase_b.build_casb",
         "--real-phi-v0","--run-id",run_id,"--input",str(run_dir/"CAS-0B.json"),
         "--objective","maximize","--certified-objective","minus-phi",
         "--candidate-method","stationary-multistart","--regime","hyperbolic"])

    print(f"B.3 decisive experiment run directory: {run_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
