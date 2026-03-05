# Phase C Taskpack 7 — Comparison Inequalities / Z-Matrix Certification (FINAL)

**Taskpack ID:** C-TASK07  
**Schema Version:** C-TASK07.v2  
**Generated:** {now}

---

## Objective

Extend:

- `src/nps/phases/phase_c/build_casc.py`

so that during a normal Phase C run the pipeline additionally emits **Taskpack 7** run-root artefacts:

- `COMPARISON_INEQUALITIES_CERT.json`
- `PhaseC_TASK7_COMPARISON_INEQUALITIES_REPORT.md`

This step is **artefact-only** and must **not** change CAS-C gating / READY_FOR_PHASE_D semantics.

---

## Required run-root inputs (fail fast)

Load from the run root:

Required:

- `HESSIAN_BLOCKS.json`
- `DIAGONAL_DOMINANCE_CERT.json`

Optional:

- `HESSIAN_SPARSITY_CERT.json`
- `OPERATOR_LAYER.json`
- `HESSIAN_MATRIX.json`

If any required file is missing, write the report as BLOCKED and emit `COMPARISON_INEQUALITIES_CERT.json` with checks showing FAIL at `CHK.C7.INPUTS.PRESENT`.

---

## Matrix and slice definition (no ambiguity)

Use Taskpack-4 blocks to avoid re-slicing:

- Read `H = HESSIAN_BLOCKS.json.blocks["w_w"]`
- Define `C := -H`

Record the convention in `matrix_definition`:

```json
{
  "base_matrix": "H",
  "coupling_matrix": "C := -H",
  "block": "w_w"
}
```

---

## Comparison inequality to certify

Certify the Z-matrix off-diagonal sign condition:

For tolerance `tol = 1e-12` (record it):

- PASS iff for all `i != j`: `C[i,j] <= tol`

Implementation notes:

- Use `numpy` if already imported; otherwise use pure Python loops.
- Compute:
  - `max_offdiag_value = max(C[i,j] for i!=j)`
  - a list of violations where `C[i,j] > tol`
  - keep `top_k_violations` (k=10) sorted by descending value

---

## Integrate with Taskpack 6 (structural reuse)

Read from `DIAGONAL_DOMINANCE_CERT.json`:

- Task-6 check `CHK.C6.DOMINANCE.STRICT_PASS` (or an equivalent strict-DD boolean)
- `matrix_definition` and `derived_sign_pattern`

In Taskpack 7 output:

- include `derived_sign_pattern.from_task6` (subset)
- include `derived_sign_pattern.computed` (Task 7’s computed result)

Define:

- `candidate_Z_matrix = off_diagonal_nonpositive`
- `candidate_m_matrix = candidate_Z_matrix AND (Task6 strict DD PASS)`

---

## Required checks (canonical check objects)

All checks must use the structure:

```json
{"id":"...", "ok": true, "status":"PASS", "details":{}}
```

Emit the following check IDs in order:

### 1) CHK.C7.INPUTS.PRESENT

PASS iff required inputs exist and parse correctly.

Details must include:

- list of inputs found / missing

### 2) CHK.C7.ZMATRIX.OFFDIAG_NONPOSITIVE

PASS iff `max_offdiag_value <= tol`.

Details must include:

- `tolerance`
- `max_offdiag_value`
- `violation_count`
- `top_k_violations`

### 3) CHK.C7.M_MATRIX.CANDIDATE

PASS iff BOTH:

- Task 6 strict diagonal dominance PASS, AND
- `CHK.C7.ZMATRIX.OFFDIAG_NONPOSITIVE` PASS

Details must include:

- `task6_strict_dd_pass`
- `candidate_Z_matrix`
- `candidate_m_matrix`

---

## Output: COMPARISON_INEQUALITIES_CERT.json

Write to run root:

- `cert_artifacts/<run_id>/COMPARISON_INEQUALITIES_CERT.json`

It must follow `CAS-C_TASK7_SPEC.md` v2 and include:

- `sources`
- `matrix_definition`
- `tolerances`
- `derived_sign_pattern`
- `witnesses`
- `checks`

---

## Output: PhaseC_TASK7_COMPARISON_INEQUALITIES_REPORT.md

Write to run root.

Minimum sections:

- Run ID
- Inputs (found/missing)
- Matrix convention (`C := -H`, block `w_w`)
- Tolerance and max off-diagonal value
- Violations summary (top-k table if any)
- Checks table
- Result: DONE/BLOCKED

---

## Commit policy

Commit **code only**.
Do NOT commit any `cert_artifacts/` outputs.

---

## Execution

Run Phase C normally (with governance env vars), e.g.:

```bash
PYTHONPATH=src python -m nps.phases.phase_c.build_casc --run-id 2026-03-04T211059Z --run-root cert_artifacts/2026-03-04T211059Z
```

Expected run-root outputs added by Taskpack 7:

- `COMPARISON_INEQUALITIES_CERT.json`
- `PhaseC_TASK7_COMPARISON_INEQUALITIES_REPORT.md`
