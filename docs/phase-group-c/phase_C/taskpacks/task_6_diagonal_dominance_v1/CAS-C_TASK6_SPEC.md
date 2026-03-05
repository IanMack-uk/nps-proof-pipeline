# CAS‑C Task 6 Spec — Diagonal Dominance Certification (FINAL)

Schema Version: C-TASK06.v2  
Generated: 2026-03-05T13:57:56.233060Z

This specification defines the **minimum required schema** for the VERIFIED artefacts produced by **Phase C Taskpack 6 (Diagonal Dominance Certification)**.

---

# File Location (Run Root)

All artefacts must be written under:

cert_artifacts/<run_id>/

---

# Expected Artefacts

Taskpack 6 must produce:

DIAGONAL_DOMINANCE_CERT.json  
PhaseC_TASK6_DIAGONAL_DOMINANCE_REPORT.md

---

# Required Top-Level JSON Fields

Each JSON artefact MUST include:

```
schema_version
run_id
generated_utc
sources
checks
```

Example:

```
{
  "schema_version": "C-TASK06.v2",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "sources": {
      "HESSIAN_MATRIX": "HESSIAN_MATRIX.json",
      "HESSIAN_BLOCKS": "HESSIAN_BLOCKS.json",
      "HESSIAN_SPARSITY": "HESSIAN_SPARSITY_CERT.json"
  },
  "checks": []
}
```

The `checks` array must contain the results defined in
`phase_C_task6_verification_rules.md`.

---

# Matrix Convention

Taskpack 6 must explicitly record the matrix definitions used.

```
H := ∇²_w Φ_cert(w*, θ)
C := -H
```

The diagonal dominance test is always applied to **C**.

---

# Matrix Slice

Dominance must be evaluated on the **w-variable block** from

HESSIAN_BLOCKS.json

Specifically

blocks["w_w"]

---

# Dominance Metrics

For each row i compute:

```
row_sum_off(i) = Σ_j≠i |C_ij|
margin_i = C_ii − row_sum_off(i)
```

Define:

```
min_margin = min_i margin_i
max_margin = max_i margin_i
```

Strict diagonal dominance holds if

```
min_margin > 0
```

---

# Required Additional Artefact Fields

To support downstream taskpacks (7–9), the certification artefact must include:

```
matrix_definition
row_metrics
witnesses
derived_sign_pattern
```

## matrix_definition

Records the matrix conventions used.

```
"matrix_definition": {
  "base_matrix": "H",
  "coupling_matrix": "C := -H",
  "block": "w_w"
}
```

## row_metrics

Metrics computed per matrix row.

```
"row_metrics": [
  {
    "row": i,
    "diag": "...",
    "row_sum_off": "...",
    "margin": "...",
    "strict": true
  }
]
```

## witnesses

Store rows with smallest margins.

```
"witnesses": {
  "min_margin_row": "...",
  "min_margin": "..."
}
```

## derived_sign_pattern

Information used for Tasks 7–9.

```
"derived_sign_pattern": {
  "off_diagonal_nonpositive": true,
  "candidate_Z_matrix": true
}
```

---

# Required Checks

The following checks must appear in the `checks` list:

CHK.C6.C_MATRIX.DEFINED  
CHK.C6.DOMINANCE.MARGINS_COMPUTED  
CHK.C6.DOMINANCE.STRICT_PASS

Each check must follow the structure:

```
{"id": "...", "ok": true, "status": "PASS", "details": {}}
```

---

# Purpose

This artefact provides all dominance metrics required for:

Taskpack 7 — Comparison Inequalities  
Taskpack 8 — Neumann-Series Bounds  
Taskpack 9 — M-Matrix Certification
