# Task B.3.1 — Phase A `--certified-objective` propagation + first strict‑concave run (minus_phi)

## Context
Task B.3 produced a decisive result: Real Φ v0 admits a strict concave maximiser under **−Φ** but not under Φ (for the Real Φ v0 test instance). fileciteturn40file0

However, Phase A Real Φ mode did not yet support selecting the certified objective (Φ vs −Φ). This task:

1) propagates `--certified-objective` into **Phase A** Real Φ v0 mode so Phase A checks are evaluated consistently, and
2) produces the first **strict‑concave maximiser** certified run under `minus_phi`, suitable for Phase C entry.

---

## Command convention (authoritative)
All commands are executed from repo root using:

```bash
PYTHONPATH=src python -m ...
```

---

## Deliverables

### A) Phase A supports `--certified-objective`
Update:

- `src/nps/phases/phase_a/build_casa.py`

Add CLI flag:

- `--certified-objective` with allowed values:
  - `phi`
  - `minus-phi`
- Default: `phi`

**Behaviour (only when `--real-phi-v0` is enabled)**
- Build the base Real Φ v0 spec using the existing helper (do not change the Real Φ definition here).
- Wrap the base spec with the existing sign-consistent wrapper:

  - `nps.models.signed_objective.SignedObjective`

so that **value/grad/hess are sign-consistent**.

- `certified-objective="phi"` → sign = +1
- `certified-objective="minus-phi"` → sign = −1

Then:
- compute `w*` (interior stationary point) exactly as Phase A already does
- run **all Phase A checks at `w*`** using the signed objective (so curvature sign matches the certified objective)

**CAS-A recording**
In the generated `CAS-A.json`, record:

- `derivative_definition.extension_id == "real_phi_v0"` (unchanged)
- add: `derivative_definition.certified_objective` with value `"phi"` or `"minus_phi"` (use underscore in JSON even if CLI uses hyphen)
- add: `equilibrium_candidate.method` (existing if present) and keep `solver_info`

**PhaseA_REPORT.md recording**
Add an explicit section:

- Certified objective: `phi` or `minus_phi`
- Expected curvature regime note (e.g. “Under minus_phi we expect concavity at maximiser if one exists.”)

### B) Tests
Add:

- `tests/test_phase_a_real_phi_certified_objective.py`

Required assertions:
- Under `--real-phi-v0 --certified-objective minus-phi`:
  - `CHK.A.STATIONARITY.ok == true`
  - `CHK.A.NEG_DEF_HESSIAN.ok == true`
  - `derivative_definition.certified_objective == "minus_phi"`
- Under `--real-phi-v0 --certified-objective phi`:
  - `CHK.A.STATIONARITY.ok == true` (stationary points invariant)
  - `CHK.A.NEG_DEF_HESSIAN.ok == false` for the Real Φ v0 test instance
  - `derivative_definition.certified_objective == "phi"`

Notes:
- Use the same test harness pattern already used in the repo’s phase generation tests (tmp_path run_dir).
- Keep tests deterministic.

### C) Produce the first strict‑concave certified run under minus_phi (required)
Create a new persistent run in `cert_artifacts/<run_id>/` that achieves:

- Phase A′ approves (all CHK.A.* ok in Real Φ mode)
- Phase B uses the same `minus_phi` certified objective and is run in:
  - `equilibrium_objective = maximize`
  - `equilibrium_regime = strict_concave`
  - `candidate-method = stationary-multistart` (or maximize-projected if you prefer)
- Phase B′ approves
- Phase C entry gate **passes** on that run_dir

Required commands (example; use consistent `--run-id`):

```bash
PYTHONPATH=src python -m nps.phases.phase_0a.build_cas0a --run-id <run_id>

PYTHONPATH=src python -m nps.phases.phase_a.build_casa   --real-phi-v0 --certified-objective minus-phi   --run-id <run_id> --input cert_artifacts/<run_id>/CAS-0A.json

PYTHONPATH=src python -m nps.phases.phase_a_prime.build_casa_prime   --run-id <run_id> --input cert_artifacts/<run_id>/CAS-A.json

PYTHONPATH=src python -m nps.phases.phase_0b.build_cas0b   --run-id <run_id> --input cert_artifacts/<run_id>/CAS-A.json

PYTHONPATH=src python -m nps.phases.phase_b.build_casb   --real-phi-v0 --certified-objective minus-phi   --objective maximize --regime strict-concave   --candidate-method stationary-multistart   --run-id <run_id> --input cert_artifacts/<run_id>/CAS-0B.json

PYTHONPATH=src python -m nps.phases.phase_b_prime.build_casb_prime   --run-id <run_id> --input cert_artifacts/<run_id>/CAS-B.json
```

Then validate Phase C entry:

```bash
PYTHONPATH=src python -c "from pathlib import Path; from nps.audit.phase_c_entry_gate import validate_phase_c_entry; validate_phase_c_entry(Path('cert_artifacts/<run_id>'))"
```

Write a run note:

- `cert_artifacts/<run_id>/B3_1_StrictConcave_MinusPhi_RUN_REPORT.md`

The note must include:
- certified objective used in Phase A and Phase B
- A′ approved? (true/false)
- B′ approved? (true/false)
- Phase C entry gate: pass/fail (include message if fail)
- key curvature witness values (min/max eigenvalue at w*)

### D) Task report (required)
Write:

- `cascade_taskpack_structural_differentiation_v4.3/MATHEMATICAL_TASKS/taskpack_task_B_3_1_phase_a_certified_objective_minus_phi/TASKS/task_B_3_1_phase_a_certified_objective_minus_phi/REPORT.md`

Include:
- files changed/added
- verification commands and results
- run_id and links to run artefacts
- evidence that `CAS-A.json` and `CAS-B.json` both record `certified_objective == "minus_phi"` for the strict-concave run

---

## Verification (must run)
```bash
pytest -q
NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q
```

---

## Acceptance criteria
DONE when:
- Phase A supports `--certified-objective` and uses `SignedObjective` when `--real-phi-v0` is enabled.
- New tests pass and demonstrate φ vs −φ curvature flip at stationary point.
- A persistent run exists where:
  - certified_objective is `minus_phi` in Phase A and Phase B
  - Phase A′ approved
  - Phase B′ approved under strict-concave regime
  - Phase C entry gate passes
- Task report and run report are written.
