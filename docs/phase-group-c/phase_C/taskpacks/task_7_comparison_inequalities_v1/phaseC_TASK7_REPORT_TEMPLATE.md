# Phase C Taskpack 7 Report — Comparison Inequalities

**Taskpack:** C-TASK07  
**Schema Version:** C-TASK07.v2  
**Generated:** 2026-03-05T14:42:33Z

---

# Run Information

Run ID:

```
<run_id>
```

Run root:

```
cert_artifacts/<run_id>/
```

---

# Inputs

| Artefact | Status |
|--------|--------|
| HESSIAN_BLOCKS.json | |
| DIAGONAL_DOMINANCE_CERT.json | |
| HESSIAN_SPARSITY_CERT.json | |
| OPERATOR_LAYER.json | |
| HESSIAN_MATRIX.json | |

---

# Matrix Definition

Base matrix:

```
H = blocks["w_w"]
```

Coupling matrix:

```
C := -H
```

Dimension:

```
<n>
```

---

# Z-Matrix Sign Condition

Tolerance:

```
1e-12
```

Maximum off-diagonal value:

```
<max_offdiag_value>
```

Violation count:

```
<violation_count>
```

---

# Largest Violations (if any)

| i | j | value |
|---|---|---|
| | | |

---

# Derived Sign Pattern

| Property | Value |
|--------|--------|
| off_diagonal_nonpositive | |
| candidate_Z_matrix | |
| candidate_m_matrix | |

---

# Checks

| Check ID | Status |
|--------|--------|
| CHK.C7.INPUTS.PRESENT | |
| CHK.C7.ZMATRIX.OFFDIAG_NONPOSITIVE | |
| CHK.C7.M_MATRIX.CANDIDATE | |

---

# Result

```
DONE / BLOCKED
```

---

# Interpretation

If **candidate_m_matrix = TRUE**, the coupling matrix

```
C = -H
```

is a **valid M-matrix candidate**.

This result enables:

- Taskpack 8 — Neumann-series bounds
- Taskpack 9 — inverse positivity certification
