# Phase C — Taskpack 12 Verification Rules (v2)

This document defines the checks required for Taskpack 12 certification.

Each check has a stable `check_id` and produces:
- `status`: PASS|FAIL|WARN
- `details`: structured dict for audit

Taskpack 12 PASS requires all REQUIRED checks PASS and no BLOCKING WARN.

---

## Integrity checks (REQUIRED)

### CHK.C12.MANIFEST.BUILT
Build `CAS-C_MANIFEST.json` listing every consumed artefact with:
- relative path
- schema_version (if JSON)
- SHA256 hash
- size bytes

PASS if manifest built and all listed files exist.

### CHK.C12.UPSTREAM.ALL_REQUIRED_TASKS_PRESENT
Verify all required task outputs exist (Tasks 1–11 minimum set).

PASS if all present; FAIL lists missing.

### CHK.C12.UPSTREAM.ALL_REQUIRED_TASKS_PASS
Verify upstream checks indicate PASS.
Source of truth:
- JSON artefacts that carry `checks[]` (preferred)
- otherwise parse Task reports and require explicit “PASS/FAIL” lines.

PASS if each required taskpack has PASS status.

### CHK.C12.SCHEMA.ALL_REQUIRED_JSON_VALID
Validate each required JSON artefact minimally:
- schema_version present
- required fields present
- numeric arrays shape-consistent

PASS if all valid; FAIL lists offending artefacts and missing fields.

---

## Cross-consistency checks (REQUIRED)

### CHK.C12.CONSISTENCY.RUN_ID_MATCH
All consumed JSON artefacts must declare the same `run_id` as the run directory.

PASS if all match.

### CHK.C12.CONSISTENCY.DIMENSIONS_MATCH
Verify consistent dimensions across:
- Hessian H shape
- H_wtheta shape
- theta_family dimensions
- selected inverse entries indices within bounds
- response_sign_matrix shape

PASS if all consistent.

### CHK.C12.CONSISTENCY.CONVENTION_LOCK
Verify convention lock is consistent across Phase C:
- `certified_objective` (phi or minus-phi)
- objective direction (maximize)
- regime (strict_concave)
- Phase C entry gate prerequisites satisfied (or recorded pass)

PASS if consistent.

### CHK.C12.CONSISTENCY.SIGN_METADATA_CLARITY
Require `H_WTHETA.json.sign_pattern.constraint` exists and violations semantics consistent.
PASS if constraint present and (constraint in {nonnegative, nonpositive} => violations==0).

---

## CAS‑C assembly checks (REQUIRED)

### CHK.C12.CASC.SCHEMA_VALID
The produced `CAS-C.json` must satisfy the Task 12 CAS‑C schema:
- required top-level fields present
- claim list present with stable claim_id
- each claim has depends_on + witness pointers

PASS if valid.

### CHK.C12.CASC.CLAIMS_SUPPORTED
For each exported claim in `CAS-C.json`, verify:
- every referenced check_id exists upstream
- every referenced artefact path exists and matches manifest hash
- witness keys exist in the referenced artefact

PASS if all supported.

---

## Minimality checks (REQUIRED)

### CHK.C12.MINIMALITY.DROP_TEST_EXECUTED
Run the drop-test protocol (see `TASK12_DROP_TEST_PROTOCOL.md`) on the exported claim set.

PASS if executed and report written.

### CHK.C12.MINIMALITY.DROP_TEST_PASS
For each dependency marked REQUIRED by a claim:
- simulate dropping it (by removing it from the dependency graph / manifest)
- verify at least one exported claim becomes unsupported
- OR the claim set is reduced and CAS‑C is re-assembled without that claim (strict mode default: dropping breaks readiness)

PASS if all REQUIRED deps are necessary.

---

## Final readiness check (REQUIRED)

### CHK.C12.READY_FOR_PHASE_D.GATED
PASS iff:
- all REQUIRED checks PASS
- CAS‑C claims include Phase‑D interface minimum set:
  - INV_H nonnegative entrywise
  - response identity well-posed
  - response sign determinate for selected entries
  - response norm bounded (rho_bound < 1 witness)

Outputs:
- `READY_FOR_PHASE_D: YES|NO`
- blocking reasons list if NO

---

## Optional checks (WARN)

### CHK.C12.HYGIENE.RUN_ROOT_CANONICAL
WARN if run root contains ambiguous variants of CAS artefacts (e.g. multiple CAS-C*).
This should align with `NPS_RUN_DIR_INTEGRITY=1` behaviour.

### CHK.C12.TRACEABILITY.REPORT_LINKS
WARN if reports are missing or do not mention the same run_id.
