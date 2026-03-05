# Task B.3.H — Run Directory Hygiene (Canonical CAS Chain) Before Phase Group C

## Purpose
Before Phase Group C, eliminate any ambiguity in certification runs by enforcing a **single canonical CAS chain** per `cert_artifacts/<run_id>/`.

This task:
1) separates *diagnostic/experimental* CAS outputs from *certifying* CAS outputs, and  
2) adds a small integrity check so future runs cannot silently drift into an ambiguous state.

This is a **small, high-leverage** hygiene fix that prevents Phase C from accidentally consuming the wrong artefact variant.

---

## Rules
- Prefer **minimal changes**.
- Do **not** alter mathematics or solver logic.
- Do **not** change Phase A or Phase B correctness criteria.
- Only adjust **output locations**, **naming**, and **auditable checks**.
- Keep developer ergonomics: default behavior should remain simple.

---

## Target invariant (must hold after this task)
For any run directory:

```
cert_artifacts/<run_id>/
```

There must be **exactly one** canonical artefact for each CAS stage at the root:

```
CAS-0A.json
CAS-A.json
CAS-Ap.json
CAS-0B.json
CAS-B.json
CAS-Bp.json
```

Any additional variants (e.g., `CAS-B_phi.json`, `CAS-B_minus_phi.json`) must be stored under:

```
cert_artifacts/<run_id>/experiments/
```

No `CAS-*.json` variants are allowed in the run root except the canonical chain above.

---

## Step 1 — Identify current behavior and sources of ambiguity
Search for any code that writes variant CAS artefacts into the run root, especially Phase B where multiple certified objectives may be run.

Focus on:
- `src/nps/phases/phase_b/build_casb.py`
- any “decisive experiment” / multi-run helper scripts under taskpacks
- any logic that writes `CAS-B_*.json` to `cert_artifacts/<run_id>/`

Document what you find in the task report.

---

## Step 2 — Implement the experiments/ output convention

### 2.1 Create a helper for run subdirectories (if helpful)
Add a small utility (optional but recommended):

- `src/nps/certification/artifacts.py` (already exists)

Add function:

```python
def get_experiments_dir(run_dir: Path) -> Path:
    d = run_dir / "experiments"
    d.mkdir(parents=True, exist_ok=True)
    return d
```

If you prefer not to touch this file, implement locally in Phase B generator—keep it minimal.

### 2.2 Modify Phase B generator to keep canonical outputs single-valued
Update:

- `src/nps/phases/phase_b/build_casb.py`

Required behavior:

**Canonical mode (default)**
- Writes:
  - `cert_artifacts/<run_id>/CAS-B.json`
  - `cert_artifacts/<run_id>/PhaseB_REPORT.md`
- Writes no variant CAS artefacts to the run root.

**Diagnostic/experiment mode**
If the command indicates it’s producing a *non-canonical variant* (examples):
- explicit `--certified-objective phi` while the canonical run is `minus-phi`, OR
- a new explicit flag `--write-to-experiments`, OR
- the run script is performing “both φ and −φ in one run_id”

Then:
- write variant artefacts to:
  - `cert_artifacts/<run_id>/experiments/`
- allowed variant filenames inside experiments:
  - `CAS-B_phi.json`
  - `CAS-B_minus_phi.json`
  - `PhaseB_REPORT_phi.md`
  - `PhaseB_REPORT_minus_phi.md`
  - additional diagnostic markdown/json as needed

**Important**
- Do not change the internal JSON schema.
- Do not change hash computation logic.
- This is strictly “where files go” and “what is canonical”.

### 2.3 Decide and encode what counts as canonical
Add a deterministic rule in Phase B generator:

- If `--certified-objective` is passed:
  - treat it as canonical **unless** `--write-to-experiments` is also passed.
- If you want a safer policy:
  - default canonical objective for `--real-phi-v0` is `minus-phi`
  - `phi` defaults to experiments unless explicitly forced canonical.

Pick one policy and state it clearly in the report.

Recommended minimal policy (low disruption):
- Canonical is whatever the CLI invocation is, but any “two-objective experiment in one run_id” must write the second into `experiments/`.

---

## Step 3 — Add a run directory integrity check (fail loudly)

Add:

- `src/nps/audit/run_directory_integrity.py`

Expose:

```python
from pathlib import Path

CANONICAL_CAS = {
    "CAS-0A.json", "CAS-A.json", "CAS-Ap.json",
    "CAS-0B.json", "CAS-B.json", "CAS-Bp.json",
}

def validate_run_directory_integrity(run_dir: Path) -> None:
    """Raise RuntimeError if run root contains ambiguous CAS artefact variants."""
```

Rules:
- Look in `run_dir` (root only).
- If any file matches pattern `CAS-*.json` but is not in `CANONICAL_CAS`, raise RuntimeError:
  - include offending filenames in message
  - instruct: “Move variants to experiments/”
- Also, if multiple canonical files exist with confusing names (e.g. `CAS-B (1).json`), fail.
- Do not inspect `experiments/` for this check.

---

## Step 4 — Wire integrity check into certification gating (CI/cert runs only)
Do not affect developer ergonomics. Enable only in CI/cert runs:

- Add env var: `NPS_RUN_DIR_INTEGRITY=1`

Implement in `src/nps/audit/governance.py` (already exists):
- add optional `maybe_install_run_dir_integrity_gate()` that checks env var.
- OR keep it explicit in scripts: call it when running cert runs.

Minimal approach:
- Add a helper function:

```python
def maybe_validate_run_dir_integrity(run_dir: Path) -> None:
    if os.getenv("NPS_RUN_DIR_INTEGRITY") == "1":
        validate_run_directory_integrity(run_dir)
```

Call this at the end of:
- Phase B generator (after writing outputs), and/or
- Phase B′ generator before approval

Recommended:
- Call it in **Phase B′** right before setting `approved=true`, because B′ is “approval/closure”.

---

## Step 5 — Tests (required)
Add:

- `tests/test_run_directory_integrity.py`

Cases:
1) **Pass** when only canonical CAS files exist in run root.
2) **Fail** when `CAS-B_phi.json` exists in run root.
3) **Pass** when `CAS-B_phi.json` exists under `experiments/`.
4) **Env-gated call** (if you added `maybe_validate...`):
   - ensure it does nothing when env var is unset
   - ensure it raises when env var is set and invalid state exists

Use `tmp_path` to simulate run dirs.

---

## Step 6 — Verification commands (must run)
From repo root:

```bash
pytest -q
NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 NPS_RUN_DIR_INTEGRITY=1 pytest -q
```

---

## Step 7 — Produce a fresh strict-concave minus_phi run (sanity check)
Create a new run (or reuse your B.3.1 strict run logic) and confirm:
- root contains only canonical CAS artefacts
- any diagnostic variants (if produced) are under `experiments/`
- Phase C entry gate continues to pass

Record run_id in report.

---

## Reporting (required)
Write a task report at:

```
cascade_taskpack_structural_differentiation_v4.3/MATHEMATICAL_TASKS/task_B_3_hygiene_before_phase_c/REPORT.md
```

Include:
- files changed
- the “canonical vs experiments” convention chosen
- pytest outputs for both modes
- example error message from integrity check (short excerpt)
- run_id used for the sanity run and directory listing of run root (just filenames)

---

## Completion criteria
This task is DONE when:
- Variant CAS artefacts are never written into run root (they go to `experiments/`).
- `validate_run_directory_integrity()` exists and catches ambiguity.
- Integrity check is **CI/cert-run gated** via env var.
- Tests cover pass/fail cases.
- Both pytest modes pass.
- A strict-concave minus_phi run exists with a clean run root, and Phase C entry gate passes.
