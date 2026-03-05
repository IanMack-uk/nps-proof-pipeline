# Taskpack 12 — Execution Guide (Cascade / build_casc.py)

This guide specifies the step-by-step implementation for Taskpack 12 in:

`src/nps/phases/phase_c/build_casc.py`

Taskpack 12 should run after Task 11.

---

## 1) Locate inputs and build manifest

### 1.1 Required artefact map
Define a REQUIRED map of logical artefacts to candidate filenames, e.g.:

- TASK2_H_WTHETA: ["H_WTHETA.json"]
- TASK8_NEUMANN: ["NEUMANN_SERIES_BOUND.json"]
- TASK9_M_MATRIX: ["M_MATRIX_CERTIFICATE.json"]
- TASK10_SELECTED: ["SELECTED_INVERSE_ENTRIES.json"]
- TASK11_EXPOSURE_CHECK: ["EXPOSURE_RESPONSE_CHECK.json"]
- TASK11_SIGN_PRED: ["RESPONSE_SIGN_PREDICTIONS.json"]
- TASK11_SCALING: ["SCALING_BOUNDS.json"]

…and similarly for Tasks 1–7 artefacts.

Resolve each by checking existence in run root.

### 1.2 Hashing
Compute SHA256 for every consumed artefact file.
Write `CAS-C_MANIFEST.json` with schema `C-CASC-MANIFEST.v1`.

Implement CHK.C12.MANIFEST.BUILT.

---

## 2) Evaluate upstream PASS status

Prefer JSON `checks[]` arrays.
If missing, fall back to parsing the corresponding PhaseC_TASK*_REPORT.md and require explicit PASS markers.

Implement:
- CHK.C12.UPSTREAM.ALL_REQUIRED_TASKS_PRESENT
- CHK.C12.UPSTREAM.ALL_REQUIRED_TASKS_PASS

---

## 3) Schema validation (minimal but strict)

For each required JSON artefact:
- schema_version present and string
- run_id present and matches run directory
- required fields exist for that artefact type
- matrices have consistent nested list structure and declared shapes (when declared)

Implement CHK.C12.SCHEMA.ALL_REQUIRED_JSON_VALID.

---

## 4) Cross-consistency

### 4.1 RUN_ID match
Implement CHK.C12.CONSISTENCY.RUN_ID_MATCH.

### 4.2 Dimension match
Extract:
- dim_w, dim_theta from THETA_FAMILY / H_WTHETA
- H shape from Hessian artefact (if available)
- selected indices bounds from SELECTED_INVERSE_ENTRIES
- response_sign_matrix shape from Task 11

Implement CHK.C12.CONSISTENCY.DIMENSIONS_MATCH.

### 4.3 Convention lock
Verify consistent:
- certified_objective
- objective_direction = maximize
- equilibrium_regime = strict_concave
- entry gate pass indicators if recorded

Implement CHK.C12.CONSISTENCY.CONVENTION_LOCK.

### 4.4 Sign metadata clarity
Require in H_WTHETA.json:
- sign_pattern.constraint exists
- if constraint in {nonnegative, nonpositive}: violations == 0

Implement CHK.C12.CONSISTENCY.SIGN_METADATA_CLARITY.

---

## 5) Assemble CAS‑C

Create a deterministic list of claims with:
- stable claim_id
- statement
- strength
- depends_on: upstream check_ids
- witness: {source_path, keys}

Recommended minimum Phase‑D interface claim ids:
- C.INV_H.NONNEGATIVE_ENTRYWISE  (Task 9)
- C.RESPONSE.IDENTITY.WELL_POSED  (Task 11)
- C.RESPONSE.SIGN.DETERMINATE_FOR_SELECTED (Task 11 + Task 10)
- C.RESPONSE.NORM.BOUNDED (Task 11 + Task 8)

Write `CAS-C.json` with schema_version `CAS-C.v1`.

Implement:
- CHK.C12.CASC.SCHEMA_VALID
- CHK.C12.CASC.CLAIMS_SUPPORTED

---

## 6) Execute drop test (strict mode)

Implement the predicate `claim_supported(claim, availability)` where availability includes:
- available check_ids
- available witness keys per source artefact
- available files (by manifest)

For each claim and each dependency:
- remove dependency from availability
- re-evaluate support
- record outcome NECESSARY/REDUNDANT

Write `PhaseC_DROP_TEST_REPORT.md`.

Implement:
- CHK.C12.MINIMALITY.DROP_TEST_EXECUTED
- CHK.C12.MINIMALITY.DROP_TEST_PASS

Strict mode: any REDUNDANT dependency => FAIL unless the claim is rewritten to remove it.

---

## 7) Final gate and reporting

Compute `READY_FOR_PHASE_D`:

YES iff all REQUIRED checks PASS and required claim ids exist.

Write:
- `PhaseC_REPORT.md`
- include all CHK.C12.* statuses + key witnesses
- include final verdict

Implement CHK.C12.READY_FOR_PHASE_D.GATED.

---

## 8) Repo hygiene

- Never write variants of CAS‑C into run root.
- Never commit `cert_artifacts/`.
- Commit only code and docs changes.
