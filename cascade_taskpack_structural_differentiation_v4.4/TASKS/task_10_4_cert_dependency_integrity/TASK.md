# Task 10.4 — Certification Dependency Integrity Gate (CAS Chain Consistency)

## Objective
Add a **Certification Dependency Integrity Gate** that enforces that certification artefacts are produced in a **valid dependency order** and are **mutually consistent**.

This prevents invalid states like:
- CAS-C existing without CAS-B
- CAS-D produced while CAS-C is stale or missing
- A phase report claiming success without required upstream CAS inputs

This gate complements Task 10.3 (artefact completeness) by validating **cross-artefact dependency integrity**.

The gate must be:
- **disabled by default**
- enabled only during CI and certification runs via an environment variable

---

# Scope and Constraints

## In scope
- Validate that required upstream CAS artefacts exist before downstream phases are considered valid.
- Validate that downstream artefacts include explicit references to upstream artefact IDs/hashes (minimal, pragmatic).
- Provide audit-grade failure messages.

## Out of scope
- Rewriting the whole pipeline
- Introducing new modelling assumptions
- Forcing a specific artefact directory layout beyond what already exists in the task pack / repo conventions

---

# Required Files to Implement

## 1) New module: `src/nps/audit/cert_dependency_gate.py`

Must expose exactly:

- `validate_cert_dependency_integrity(artefact_dir: str | Path, *, policy_path: str | Path = "docs/specs/import_policy.json") -> None`
- `install_cert_dependency_gate() -> None`
- `uninstall_cert_dependency_gate() -> None`
- `is_cert_dependency_gate_enabled() -> bool`
- `maybe_install_cert_dependency_gate() -> None`

Enablement:
- Disabled by default
- Enabled only when `NPS_CERT_DEP_GATE=1` (via `maybe_install_cert_dependency_gate()`)

---

# Dependency Rules (Minimal Contract)

The gate validates a **CAS chain** within an artefact directory.

### Required phase artefacts (by filename)
The gate must validate the presence/consistency of these files when downstream ones exist:

- `CAS-0A.json` (or `CAS_0A.json` if your repo uses that)
- `CAS-A.json`
- `CAS-0B.json`
- `CAS-B.json`
- `CAS-0C.json`
- `CAS-C.json`
- `CAS-0D.json`
- `CAS-D.json`

**Important:** Use a tolerant matching strategy:
- accept hyphen/underscore variants (e.g. `CAS-0A.json`, `CAS_0A.json`)
- accept lower-case `cas-0a.json` if present (optional)

### Required ordering constraints
If a file exists, its prerequisites must exist:

- CAS-A requires CAS-0A
- CAS-0B requires CAS-A
- CAS-B requires CAS-0B
- CAS-0C requires CAS-B
- CAS-C requires CAS-0C
- CAS-0D requires CAS-C
- CAS-D requires CAS-0D

### Minimal consistency check (required)
Each CAS artefact JSON must include a minimal metadata block:

- `cas_id` (string)
- `created_at` (string or ISO timestamp)
- `inputs` (list of upstream cas_ids, may be empty for CAS-0A)
- `content_hash` (string; hash of the artefact content excluding metadata is acceptable)

If an artefact lacks required fields, validation fails.

If an artefact claims an upstream input cas_id that does not match the actual upstream artefact’s cas_id, validation fails.

---

# Implementation Notes

## Metadata enforcement without disrupting the repo
If your CAS artefacts already exist but do not include the required metadata fields, implement the gate so it:
- detects missing fields,
- fails with a clear message telling the user to regenerate artefacts with metadata.

Do NOT silently patch artefacts.

## Hashing requirement
Implement a simple hashing utility:
- stable JSON canonicalization (sorted keys) for hashing
- exclude volatile fields (created_at) if needed
- SHA256 recommended

---

# Acceptance Tests

Create: `tests/test_cert_dependency_gate.py`

### Test A — Valid chain passes
Create a temp directory with CAS files for a valid chain and minimal metadata; validation must pass.

### Test B — Missing prerequisite fails
Example: CAS-C exists but CAS-0C missing → must raise RuntimeError with audit-grade message.

### Test C — Wrong upstream cas_id fails
Example: CAS-C inputs claim CAS-0C id "X" but actual CAS-0C cas_id is "Y" → fail.

### Test D — Missing metadata fails
Example: CAS-B missing `inputs` or `content_hash` → fail.

### Test E — Gate disabled by default
Without `NPS_CERT_DEP_GATE`, nothing is auto-enforced.

### Test F — Gate enabled via env var
With `NPS_CERT_DEP_GATE=1`, calling `maybe_install_cert_dependency_gate()` enables the gate; validation runs.

---

# Enablement (CI / Certification Runs)

Enable only when:

- `NPS_CERT_DEP_GATE=1`

Recommended CI command:

```bash
NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q
```

Developer ergonomics:
- default runs do not enable the gate
- certification runners may enable it explicitly

---

# Reporting

Write a task report at:

- `cascade_taskpack_structural_differentiation_v4.3/TASKS/task_10_4_cert_dependency_integrity/REPORT.md`

Report must include:
- files added/changed
- commands run
- test results in both default and CI-mode
- a short example of a failure message (brief excerpt)

---

# Definition of Done

Task is complete when:
- `src/nps/audit/cert_dependency_gate.py` implemented with required API
- `tests/test_cert_dependency_gate.py` added
- Gate is off by default and enabled with `NPS_CERT_DEP_GATE=1`
- `pytest -q` passes with:
  - default mode
  - `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1`
- Report written
