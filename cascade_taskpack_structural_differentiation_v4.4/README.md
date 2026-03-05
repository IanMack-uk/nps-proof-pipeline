# Cascade Task Pack — Structural Differentiation / Ordering Theorem Programme (v4.3)

Date generated: 2026-03-04

This pack is designed to be **dropped into the repo root** and used as a **work-plan input** for Cascade.
It contains:

- `TASKS/` — one folder per task
  - `TASK.md` — instruction file for Cascade
  - `REPORT.md` — report template; Cascade must fill and commit alongside implementation
  - (optional) `ARTIFACTS/` — where Cascade should write generated outputs (CAS tables, DAG exports, etc.)
- `POLICIES/` — governance rules Cascade must follow
- `SCRIPTS/` — small utilities to support audits (DAG, lint hooks placeholders)

## How to use

1. Copy this folder into your repo root (e.g. `./cascade_taskpack_structural_differentiation_v4.3`).
2. Point Cascade at the folder and instruct it to execute tasks in order: `TASKS/01_*` → `TASKS/02_*` → …
3. For **each task**, Cascade must:
   - Implement changes in the codebase
   - Run tests (or add tests if missing)
   - Produce a filled `REPORT.md` in that same task folder
   - Add any generated artefacts under that task folder’s `ARTIFACTS/`

## Nonnegativity policy (proof-target pipeline)

The proof-target pipeline must assume **nonnegative weights (w ≥ 0)**.
Signed weights may exist **only** in an adversarial test suite.

