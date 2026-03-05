# Phase C Taskpack 7 — Verification Rules (FINAL)

**Taskpack ID:** C-TASK07  
**Schema Version:** C-TASK07.v2  
**Generated:** 2026-03-05T14:42:33Z

This document defines the **formal verification rules** for Taskpack 7 outputs.

The artefact verified is:

`COMPARISON_INEQUALITIES_CERT.json`

located in:

`cert_artifacts/<run_id>/`

---

# Required checks

The following checks **must appear** in the `checks` array in the specified order.

Each check must follow the canonical structure:

```json
{"id": "...", "ok": true, "status": "PASS", "details": {}}
```

---

## CHK.C7.INPUTS.PRESENT

### Purpose
Verify that the required upstream artefacts exist and can be parsed.

### Required inputs
- `HESSIAN_BLOCKS.json`
- `DIAGONAL_DOMINANCE_CERT.json`

### PASS condition

Both files:

- exist in the run root
- load as valid JSON
- contain the required fields used by Taskpack 7

### FAIL condition

Any required input:

- missing
- unreadable
- malformed JSON

### Required details fields

```json
{
  "inputs_found": [],
  "inputs_missing": []
}
```

---

## CHK.C7.ZMATRIX.OFFDIAG_NONPOSITIVE

### Purpose

Certify the **Z-matrix sign condition**:

For matrix `C := -H`,

```
C_ij ≤ tolerance  for all i ≠ j
```

### Matrix source

```
H = HESSIAN_BLOCKS.json.blocks["w_w"]
C = -H
```

### Tolerance

Default:

```
tolerance = 1e-12
```

### PASS condition

```
max_offdiag_value ≤ tolerance
```

### FAIL condition

Any off-diagonal element satisfies:

```
C[i,j] > tolerance
```

### Required details fields

```json
{
  "tolerance": 1e-12,
  "max_offdiag_value": 0.0,
  "violation_count": 0,
  "top_k_violations": []
}
```

`top_k_violations` must contain at most **10 largest violations**.

---

## CHK.C7.M_MATRIX.CANDIDATE

### Purpose

Confirm the matrix is an **M-matrix candidate**.

Condition:

```
candidate_Z_matrix AND strict_diagonal_dominance
```

Where:

- `candidate_Z_matrix` comes from the Task 7 check above
- `strict_diagonal_dominance` is read from Task 6 output

### Required Task 6 input

From `DIAGONAL_DOMINANCE_CERT.json`:

```
CHK.C6.DOMINANCE.STRICT_PASS
```

### PASS condition

Both:

```
Z-matrix condition PASS
Task 6 strict diagonal dominance PASS
```

### FAIL condition

Either condition fails.

### Required details fields

```json
{
  "task6_strict_dd_pass": true,
  "candidate_Z_matrix": true,
  "candidate_m_matrix": true
}
```

---

# Artefact completeness rules

`COMPARISON_INEQUALITIES_CERT.json` must contain:

Top-level fields:

```
schema_version
run_id
generated_utc
sources
matrix_definition
tolerances
derived_sign_pattern
witnesses
checks
```

Failure to include any required field results in **verification failure**.

---

# Governance

Taskpack 7 is **artefact-only**.

It does **NOT** change:

- CAS-C gating
- READY_FOR_PHASE_D logic
- pipeline control flow

It only certifies structural comparison inequalities used by:

- Taskpack 8
- Taskpack 9
