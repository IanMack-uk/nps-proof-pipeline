# Task B.3.H — Run Directory Hygiene (Canonical CAS Chain) Before Phase Group C — Report

## Purpose

Enforce a single canonical CAS chain in each `cert_artifacts/<run_id>/` run root, moving all variant CAS artefacts under `experiments/` and adding an env-gated integrity check to prevent ambiguity.

## Findings (Step 1)

- Phase B previously supported writing variants directly into run root via an output suffix (e.g. `CAS-B_phi.json`, `CAS-B_minus_phi.json`).
- This creates ambiguity about which artefact is canonical for Phase C consumption.

## Convention chosen (Step 2)

- **Canonical mode (default):**
  - Writes `cert_artifacts/<run_id>/CAS-B.json`
  - Writes `cert_artifacts/<run_id>/PhaseB_REPORT.md`
- **Variant/experiment mode:**
  - Triggered when either:
    - `--output-suffix` is non-empty, or
    - `--write-to-experiments` is set
  - Writes artefacts into:
    - `cert_artifacts/<run_id>/experiments/`
  - Example filenames:
    - `CAS-B_phi.json`
    - `CAS-B_minus_phi.json`
    - `PhaseB_REPORT_phi.md`
    - `PhaseB_REPORT_minus_phi.md`

## Changes made

### Files changed

- `src/nps/phases/phase_b/build_casb.py`
  - Default output is now strictly canonical (`CAS-B.json` + `PhaseB_REPORT.md`) in run root.
  - Variant output goes to `experiments/`.

- `src/nps/certification/artifacts.py`
  - Added helper `get_experiments_dir(run_dir: Path) -> Path`.

- `src/nps/audit/governance.py`
  - Added `maybe_validate_run_dir_integrity(run_dir)` gated by `NPS_RUN_DIR_INTEGRITY=1`.

- `src/nps/phases/phase_b_prime/build_casb_prime.py`
  - Calls `maybe_validate_run_dir_integrity(run_dir)` and records failures as blocking issues.

### Files added

- `src/nps/audit/run_directory_integrity.py`
  - `validate_run_directory_integrity(run_dir)`

## Integrity check behavior (Step 3/4)

- In run root (not `experiments/`), any `CAS-*.json` file not in the canonical set:

  - `CAS-0A.json`, `CAS-A.json`, `CAS-Ap.json`, `CAS-0B.json`, `CAS-B.json`, `CAS-Bp.json`

  causes a **RuntimeError**.

Example error excerpt:

- `Run directory contains non-canonical CAS artefact variants in root: CAS-B_phi.json. Move variants to experiments/`

## Tests added (Step 5)

- `tests/test_run_directory_integrity.py`
  - Pass with canonical chain only.
  - Fail with `CAS-B_phi.json` in run root.
  - Pass with `CAS-B_phi.json` under `experiments/`.
  - Env-gated helper behaves as expected.

## Verification commands run (Step 6)

- `pytest -q` → **110 passed**
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 NPS_RUN_DIR_INTEGRITY=1 pytest -q` → **110 passed**

## Sanity strict-concave minus_phi run (Step 7)

- Run id: `2026-03-04T211059Z`
- Phase C entry gate: **PASS**

### Run root listing (filenames)

- `CAS-0A.json`
- `CAS-A.json`
- `CAS-Ap.json`
- `CAS-0B.json`
- `CAS-B.json`
- `CAS-Bp.json`
- `Phase0A_REPORT.md`
- `Phase0B_REPORT.md`
- `PhaseA_REPORT.md`
- `PhaseA_prime_REPORT.md`
- `PhaseB_REPORT.md`
- `PhaseB_prime_REPORT.md`
- `assumption_registry.json`
