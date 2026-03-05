#!/usr/bin/env python3
"""Copy Real Φ v0 spec docs from the taskpack into the repo.

Usage:
  python taskpack_real_phi_v0_extract_and_integrate/SCRIPTS/copy_real_phi_v0_docs.py
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
PACK = Path(__file__).resolve().parents[1] / "TASKS" / "task_real_phi_v0" / "ARTIFACTS"
DST = ROOT / "docs" / "specs" / "real_phi_v0"
DST.mkdir(parents=True, exist_ok=True)

for name in ["EXTRACTS_VERBATIM.md", "REAL_PHI_V0_SPEC.md"]:
    shutil.copy2(PACK / name, DST / name)

print(f"Copied docs to: {DST}")
