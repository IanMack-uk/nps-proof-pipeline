# CAS-C Task 7 Spec — Comparison Inequalities / Z-Matrix Certification (FINAL)

**Taskpack ID:** C-TASK07  
**Schema Version:** C-TASK07.v2  
**Generated:** {now}

This spec defines the run-root VERIFIED artefact produced by **Phase C Taskpack 7**.
Taskpack 7 certifies the **comparison-inequality sign pattern** needed to treat the
coupling matrix as a **Z-matrix / M-matrix candidate**, enabling Tasks 8–9.

---

## Run-root location

All outputs are written under:

- `cert_artifacts/<run_id>/`

---

## Outputs

Taskpack 7 must produce:

- `COMPARISON_INEQUALITIES_CERT.json`
- `PhaseC_TASK7_COMPARISON_INEQUALITIES_REPORT.md`

---

## Required inputs (run root)

Taskpack 7 consumes outputs from earlier tasks:

Required:

- `HESSIAN_BLOCKS.json` (Task 4) — provides `blocks["w_w"]` as the w-block Hessian `H`
- `DIAGONAL_DOMINANCE_CERT.json` (Task 6) — provides dominance summary and `matrix_definition` / `derived_sign_pattern`

Optional (record if present):

- `HESSIAN_SPARSITY_CERT.json` (Task 5)
- `OPERATOR_LAYER.json` (Task 1)
- `HESSIAN_MATRIX.json` (Task 3)

If a required input is missing, Taskpack 7 must FAIL.

---

## Matrix conventions

Taskpack 7 must record and use the same conventions as Taskpack 6:

- `H := blocks["w_w"]` from `HESSIAN_BLOCKS.json`
- `C := -H`

Taskpack 7 must include a `matrix_definition` object, and it MUST match Task 6’s convention.

---

## Tolerance

Because computed matrices can have tiny numerical noise, Taskpack 7 must use and record:

- `tolerance_offdiag <= 0` test tolerance (default: `1e-12`)

Off-diagonal nonpositivity condition is interpreted as:

- PASS iff for all `i != j`, `C[i,j] <= tolerance_offdiag`

---

## Required JSON schema

`COMPARISON_INEQUALITIES_CERT.json` MUST contain:

### Top-level required fields

- `schema_version` (must be `"C-TASK07.v2"`)
- `run_id`
- `generated_utc`
- `sources` (paths to run-root inputs used)
- `matrix_definition`
- `tolerances`
- `derived_sign_pattern`
- `witnesses`
- `checks`

### sources

Example:

```json
{
  "HESSIAN_BLOCKS": "HESSIAN_BLOCKS.json",
  "DIAGONAL_DOMINANCE": "DIAGONAL_DOMINANCE_CERT.json"
}
```

### matrix_definition

Example (must be consistent with Task 6):

```json
{
  "base_matrix": "H",
  "coupling_matrix": "C := -H",
  "block": "w_w"
}
```

### tolerances

```json
{
  "offdiag_nonpositive": 1e-12
}
```

### derived_sign_pattern

Must include BOTH:

- `computed` values from Task 7’s own scan, and
- `from_task6` values read from `DIAGONAL_DOMINANCE_CERT.json` (if present)

Example:

```json
{
  "computed": {
    "off_diagonal_nonpositive": true,
    "candidate_Z_matrix": true
  },
  "from_task6": {
    "off_diagonal_nonpositive": true,
    "offdiagonal_nonpositive": true,
    "candidate_Z_matrix": true,
    "candidate_m_matrix": true
  }
}
```

### witnesses

If FAIL, include concrete counterexamples. Minimum:

```json
{
  "max_offdiag_value": 0.0,
  "top_k_violations": [
    {"i": 0, "j": 1, "value": 1.2e-6}
  ]
}
```

If PASS, `top_k_violations` may be empty.

### checks

Checks MUST be objects with the canonical structure:

```json
{"id": "...", "ok": true, "status": "PASS", "details": {}}
```

Required check IDs (must appear in this order):

1. `CHK.C7.INPUTS.PRESENT`
2. `CHK.C7.ZMATRIX.OFFDIAG_NONPOSITIVE`
3. `CHK.C7.M_MATRIX.CANDIDATE`

Interpretation:

- `CHK.C7.ZMATRIX.OFFDIAG_NONPOSITIVE` certifies the Z-matrix sign condition (`C_ij <= tol` for `i≠j`).
- `CHK.C7.M_MATRIX.CANDIDATE` is PASS iff:
  - Task 6 strict DD PASS (read from `DIAGONAL_DOMINANCE_CERT.json`), AND
  - `CHK.C7.ZMATRIX.OFFDIAG_NONPOSITIVE` PASS.

---

## Purpose

This artefact is the formal “comparison inequality” gate needed for:

- Task 8 (Neumann-series / invertibility bounds)
- Task 9 (M-matrix criteria / inverse-positivity certification)
