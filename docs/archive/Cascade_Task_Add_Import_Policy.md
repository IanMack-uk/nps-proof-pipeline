# Task 10.1 — Add Repository Import Policy (Required Before Proceeding)

## Objective
Add a repository-native import policy file so phase import isolation checks are **reproducible** and do not rely on ad-hoc artefacts.

This must be completed **before moving on** to any new tasks.

---

## Context
Stage 3 completed using a substitute policy check artifact because the baseline did not include:

- `docs/specs/import_policy.json`

We will now add this file as the authoritative, version-controlled policy.

---

## Required Actions (Cascade)

### 1) Create the policy file
Create the directory if it does not exist:

- `docs/specs/`

Then add:

- `docs/specs/import_policy.json`

Use the following exact content:

```json
{
  "policy": "phase_order_nonforward_imports",
  "phase_order": [
    "phase_0a",
    "phase_0b",
    "phase_0c",
    "phase_0d",
    "phase_a",
    "phase_a_prime",
    "phase_b",
    "phase_b_prime",
    "phase_c",
    "phase_c_prime",
    "phase_d",
    "phase_d_prime",
    "phase_f"
  ],
  "rules": {
    "allow_same_phase_imports": true,
    "allow_backward_imports": true,
    "forbid_forward_imports": true
  },
  "notes": [
    "Earlier phases must never import later phases.",
    "Core modules may be imported by any phase.",
    "Certification and symbol layers are globally accessible.",
    "Type-only imports under TYPE_CHECKING are ignored by policy checks."
  ]
}
```

---

### 2) Wire the policy checker to use the policy file (minimal)
Update whichever script/test currently performs the phase import policy check so that it:

- reads `docs/specs/import_policy.json` if present
- fails if forward-phase imports are detected

If the repository already has a policy checker entrypoint (recommended), ensure it accepts:

- `--policy docs/specs/import_policy.json`
- and consumes the current DAG edges json.

If the checker does not exist yet, implement a minimal one that:
- parses `final_dependency_edges.json`-style edge lists or the repo’s current edge format
- applies the phase ordering rule
- ignores type-only imports when explicitly marked/identified

**Important:** Do not introduce new modelling assumptions or change phase boundaries. This is governance metadata + enforcement only.

---

### 3) Verification steps (must run)
Run:

1. `pytest -q`
2. regenerate DAG artefacts (if your standard workflow does so)
3. run the import policy check using the policy file

---

### 4) Artefacts to produce
Write or update (choose the appropriate task folder for where you are tracking governance artefacts; if continuing under Task 10, use its ARTIFACTS folder):

- `ARTIFACTS/final_dependency_dag.md` (if regenerated)
- `ARTIFACTS/final_dependency_edges.json` (if regenerated)
- `ARTIFACTS/phase_import_policy_check.json` (optional, but if present should be generated using the policy file)

---

### 5) Reporting requirements
Create a short report file (or update the most recent task report) including:

- files added/changed
- commands run
- confirmation the policy file is now authoritative
- policy-check result (0 violations expected)

Suggested report filename:

- `docs/specs/import_policy_addition_report.md`

---

## Definition of Done
This task is complete when:

- `docs/specs/import_policy.json` exists and is committed
- a policy checker reads it and detects forward imports
- `pytest -q` passes
- policy check reports **0 violations**
- a short report is written documenting the change
