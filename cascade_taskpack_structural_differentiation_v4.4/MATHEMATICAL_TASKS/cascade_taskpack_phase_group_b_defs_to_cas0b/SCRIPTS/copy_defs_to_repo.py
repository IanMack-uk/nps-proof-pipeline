#!/usr/bin/env python3
"""
Copy the Phase Group B definition artefacts into the repo.

Usage (repo root):
  python cascade_taskpack_phase_group_b_defs_to_cas0b/SCRIPTS/copy_defs_to_repo.py
"""
from pathlib import Path
import shutil

REPO = Path(__file__).resolve().parents[1]
PACK = Path(__file__).resolve().parents[1] / "TASKS" / "task_B_2_1_phase_group_b_defs_to_cas0b" / "ARTIFACTS"
DST = REPO / "docs" / "specs" / "phase_group_b_defs"
DST.mkdir(parents=True, exist_ok=True)

for name in ["Paper1_Thesis_Definition_Blocks.md", "CAS0B_Dependencies_And_Obligations.md"]:
    shutil.copy2(PACK / name, DST / name)

print(f"Copied artefacts to: {DST}")
