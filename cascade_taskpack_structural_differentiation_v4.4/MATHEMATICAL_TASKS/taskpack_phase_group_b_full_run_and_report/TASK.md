# Phase Group B — Full Maths Run + Consolidated Reporting (0B → B → B′)

## Purpose
Run the repo’s **Phase Group B mathematics** end-to-end (including required Phase Group A prerequisites) and produce:
- a **fresh certification run** under `cert_artifacts/<run_id>/`
- all **per-phase reports** and **CAS artefacts**
- a single **consolidated run report** summarising what was achieved and the results

This task pack is **execution + reporting only**:
- **Do not modify code** unless the run fails and you are instructed to create a separate fix task.
- Treat failures as audit findings: capture them, do not patch silently.

## Command convention (authoritative)
All module invocations must be executed from repo root using:
- `PYTHONPATH=src python -m ...`

## What this task executes
This run performs:
- **Phase 0A → A → A′** (inputs needed for B-chain integrity)
- **Phase 0B → B → B′** (Phase Group B)

Phase B is executed in **toy quadratic mode** (deterministic checks).

---

## Outputs expected (per run directory)
A new run directory under `cert_artifacts/<run_id>/` containing:

### Phase Group A artefacts (inputs to B-chain)
- `CAS-0A.json`
- `Phase0A_REPORT.md`
- `CAS-A.json`
- `PhaseA_REPORT.md`
- `assumption_registry.json` (if produced by Phase A)
- `CAS-Ap.json`
- `PhaseA_prime_REPORT.md`

### Phase Group B artefacts
- `CAS-0B.json`
- `Phase0B_REPORT.md`
- `CAS-B.json`
- `PhaseB_REPORT.md`
- `CAS-Bp.json`
- `PhaseB_prime_REPORT.md`

### Consolidated report (this task pack)
- `PhaseGroupB_RUN_REPORT.md`

---

## Execution method
You may run the commands manually OR use the provided script:
- `SCRIPTS/run_phase_group_b_full.py`

Prefer the script because it:
- creates a single `run_id`
- runs phases in order
- captures stdout/stderr
- writes `PhaseGroupB_RUN_REPORT.md` automatically

---

## Step 1 — Run the pipeline (preferred: script)

From repo root:

```bash
PYTHONPATH=src python SCRIPTS/run_phase_group_b_full.py
```

The script prints the run directory and writes the consolidated report.

If you cannot use the script, run the phases manually (fallback in Step 1b).

### Step 1b — Manual commands (fallback)
Use a single run id, e.g. `RUN=2026-03-04T145711Z`.

```bash
PYTHONPATH=src python -m nps.phases.phase_0a.build_cas0a --run-id "$RUN"
PYTHONPATH=src python -m nps.phases.phase_a.build_casa --toy-quadratic --run-id "$RUN" --input "cert_artifacts/$RUN/CAS-0A.json"
PYTHONPATH=src python -m nps.phases.phase_a_prime.build_casa_prime --run-id "$RUN" --input "cert_artifacts/$RUN/CAS-A.json"

PYTHONPATH=src python -m nps.phases.phase_0b.build_cas0b --run-id "$RUN" --input "cert_artifacts/$RUN/CAS-A.json"
PYTHONPATH=src python -m nps.phases.phase_b.build_casb --toy-quadratic --run-id "$RUN" --input "cert_artifacts/$RUN/CAS-0B.json"
PYTHONPATH=src python -m nps.phases.phase_b_prime.build_casb_prime --run-id "$RUN" --input "cert_artifacts/$RUN/CAS-B.json"
```

Then manually create `cert_artifacts/$RUN/PhaseGroupB_RUN_REPORT.md` using the report requirements below.

---

## Step 2 — Verification commands (must run)
Run both and record results in the consolidated report.

### Default
```bash
pytest -q
```

### Gates-on (cert posture)
```bash
NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q
```

---

## Step 3 — Consolidated report requirements (must satisfy)
Ensure `cert_artifacts/<run_id>/PhaseGroupB_RUN_REPORT.md` contains:

### A) Run metadata
- run_id
- timestamp
- git status (clean/dirty)
- command convention used (`PYTHONPATH=src ...`)

### B) Artefacts produced (with paths)
- list each CAS artefact file and each Phase report file
- confirm the CAS chain exists:
  - CAS-0A → CAS-A → CAS-0B → CAS-B → CAS-Bp

### C) Phase B results (math checks)
From `CAS-B.json`:
- list each `CHK.B.*` with `ok`, `margin`, and 1–2 key witness fields
- explicitly mention:
  - `CHK.B.OPERATOR_MATCHES_GRAD`
  - `CHK.B.JACOBIAN_MATCHES_HESS`
  - `CHK.B.JACOBIAN_SYMMETRY`
  - `CHK.B.JACOBIAN_LOCALITY_SPARSITY`
  - `CHK.B.JACOBIAN_INVERTIBLE_AT_WSTAR`

### D) Phase B′ closure outcome
From `CAS-Bp.json` / `PhaseB_prime_REPORT.md`:
- whether approval succeeded
- if blocked, list blocking issues verbatim

### E) Test outcomes
- `pytest -q` summary
- gates-on pytest summary

### F) If anything fails
- do NOT patch
- capture the full failure message and the relevant witness excerpt
- recommend a follow-on “fix task” with minimal scope

---

## Repo-level report (static, checked in)
Write/update a short run report at:

`cascade_taskpack_structural_differentiation_v4.3/TASKS/task_phase_group_b_run/REPORT.md`

This report must include:
- run_id used
- pointer to `cert_artifacts/<run_id>/PhaseGroupB_RUN_REPORT.md`
- verification commands run and results

---

## Definition of Done
This task is complete when:
- a fresh run directory exists under `cert_artifacts/<run_id>/`
- all Phase 0A/A/A′ and 0B/B/B′ artefacts and reports exist
- `PhaseGroupB_RUN_REPORT.md` exists and satisfies all requirements above
- `pytest -q` and gates-on pytest both ran and results are recorded
- repo-level run report is written/updated
