# Taskpack 11 — Artifact Schemas (JSON)

This document specifies the **precise JSON schemas** for Taskpack 11 artefacts.

These schemas are designed to be:
- **Audit-friendly** (explicit fields, no implicit meaning)
- **Backwards compatible** with Phase C style
- **Strict enough** for future verifiers

Unless otherwise stated:
- All numeric tolerances are IEEE floats.
- All integer indices are 0-based.
- All matrices are stored as row-major nested arrays.

---

## 1) EXPOSURE_RESPONSE_CHECK.json

### Filename
`EXPOSURE_RESPONSE_CHECK.json`

### Purpose
Records that the response identity is well-posed for the certified run and ties it to upstream artefacts.

### Schema
```json
{
  "schema_version": "C-EXPOSURE-RESPONSE-CHECK.v1",
  "run_id": "2026-03-04T211059Z",
  "taskpack_id": "C-TASK11.v1",
  "inputs": {
    "h_wtheta_path": "cert_artifacts/<run_id>/H_WTHETA.json",
    "hessian_path": "cert_artifacts/<run_id>/HESSIAN_MATRIX.json",
    "m_matrix_cert_path": "cert_artifacts/<run_id>/M_MATRIX_CERTIFICATE.json",
    "selected_inverse_entries_path": "cert_artifacts/<run_id>/SELECTED_INVERSE_ENTRIES.json",
    "neumann_bound_path": "cert_artifacts/<run_id>/NEUMANN_SERIES_BOUND.json"
  },
  "theta_family": {
    "name": "edge_local_v1",
    "scope": "pointwise_at_w_star",
    "dimension_w": 6,
    "dimension_theta": 6
  },
  "response_identity": {
    "formula": "dw_star_dtheta = - inv(H) @ H_wtheta",
    "sign_convention": {
      "certified_objective": "minus_phi",
      "notes": "H is Hessian of the certified objective. H_wtheta matches Taskpack 2 construction."
    }
  },
  "well_posedness": {
    "h_shape": [6, 6],
    "h_wtheta_shape": [6, 6],
    "shape_compatible": true,
    "invertibility_basis": "M-matrix certificate (Task 9)",
    "response_defined": true
  },
  "checks": [
    {
      "check_id": "CHK.C11.H_WTHETA.EXISTS",
      "status": "PASS",
      "details": {}
    },
    {
      "check_id": "CHK.C11.H_WTHETA.SIGN_STRUCTURE_CERTIFIED",
      "status": "PASS",
      "details": {}
    },
    {
      "check_id": "CHK.C11.RESPONSE.SIGN_UNAMBIGUOUS",
      "status": "PASS",
      "details": {}
    },
    {
      "check_id": "CHK.C11.SCALING.BOUNDS_COMPUTED",
      "status": "PASS",
      "details": {}
    }
  ],
  "created_at_utc": "2026-03-05T00:00:00Z"
}
```

### Field requirements
- `schema_version` MUST equal `C-EXPOSURE-RESPONSE-CHECK.v1`.
- `run_id` MUST match the run directory name.
- `inputs.*_path` MUST be relative to repo root (audit portability).
- `theta_family.dimension_w` MUST equal `well_posedness.h_shape[0]`.
- `response_defined` MUST be `shape_compatible && (invertibility_basis != "")`.

---

## 2) RESPONSE_SIGN_PREDICTIONS.json

### Filename
`RESPONSE_SIGN_PREDICTIONS.json`

### Purpose
Records **sign predictions** for entries of `dw_star_dtheta` implied by:
- `inv(H) >= 0` (Task 9)
- `H_wtheta` sign metadata (Task 2)

This artefact does **not** require numerically forming `inv(H)`.

### Schema
```json
{
  "schema_version": "C-RESPONSE-SIGN-PREDICTIONS.v1",
  "run_id": "2026-03-04T211059Z",
  "taskpack_id": "C-TASK11.v1",
  "inputs": {
    "h_wtheta_path": "cert_artifacts/<run_id>/H_WTHETA.json",
    "m_matrix_cert_path": "cert_artifacts/<run_id>/M_MATRIX_CERTIFICATE.json",
    "selected_inverse_entries_path": "cert_artifacts/<run_id>/SELECTED_INVERSE_ENTRIES.json"
  },
  "assumptions_used": [
    "INV_H_ENTRYWISE_NONNEGATIVE (from Task 9)",
    "H_WTHETA_SIGN_PATTERN (from Task 2)"
  ],
  "tolerance": 1e-12,
  "prediction_rule": {
    "description": "If inv(H) >= 0 entrywise, then sign(dw/dtheta) is the negated sign of H_wtheta aggregated through nonnegative weights. If H_wtheta is entrywise nonnegative, dw/dtheta is entrywise nonpositive.",
    "formula": "dw_star_dtheta = - inv(H) @ H_wtheta"
  },
  "response_sign_matrix": {
    "shape": [6, 6],
    "encoding": "int",
    "legend": {
      "-1": "negative",
      "0": "zero_or_indeterminate",
      "1": "positive"
    },
    "matrix": [[-1,0,0,0,0,0],
               [0,-1,0,0,0,0],
               [0,0,-1,0,0,0],
               [0,0,0,-1,0,0],
               [0,0,0,0,-1,0],
               [0,0,0,0,0,-1]]
  },
  "sign_determinate": true,
  "sign_ambiguities": [],
  "selected_entries_summary": {
    "from_task10_selection": true,
    "entries": [
      {"i": 0, "j": 0, "predicted_sign": -1},
      {"i": 1, "j": 1, "predicted_sign": -1},
      {"i": 2, "j": 2, "predicted_sign": -1},
      {"i": 3, "j": 3, "predicted_sign": -1},
      {"i": 4, "j": 4, "predicted_sign": -1},
      {"i": 5, "j": 5, "predicted_sign": -1}
    ]
  },
  "checks": [
    {
      "check_id": "CHK.C11.RESPONSE.SIGN_UNAMBIGUOUS",
      "status": "PASS",
      "details": {
        "reason": "inv(H) >= 0 and H_wtheta constraint=nonnegative => dw/dtheta <= 0"
      }
    }
  ],
  "created_at_utc": "2026-03-05T00:00:00Z"
}
```

### Field requirements
- `response_sign_matrix.matrix` MUST match declared `shape`.
- `sign_determinate` MUST be false if any selected entry is indeterminate.
- `sign_ambiguities` MUST list all indeterminate selected entries with reasons:
  - missing sign metadata
  - mixed constraint
  - inverse sign certificate absent
  - tolerance ambiguity

---

## 3) SCALING_BOUNDS.json

### Filename
`SCALING_BOUNDS.json`

### Purpose
Provides a certified magnitude bound for the response using the Neumann-series bound from Task 8.

### Schema
```json
{
  "schema_version": "C-SCALING-BOUNDS.v1",
  "run_id": "2026-03-04T211059Z",
  "taskpack_id": "C-TASK11.v1",
  "inputs": {
    "neumann_bound_path": "cert_artifacts/<run_id>/NEUMANN_SERIES_BOUND.json",
    "h_wtheta_path": "cert_artifacts/<run_id>/H_WTHETA.json"
  },
  "rho_bound": 0.1268,
  "inverse_norm_bound": {
    "norm": "inf",
    "bound": 1.1452,
    "derivation": "From Task 8 Neumann series: ||(I - K)^{-1}|| <= 1/(1 - rho_bound) in chosen operator norm"
  },
  "h_wtheta_norm": {
    "norm": "inf",
    "value": 1.0000,
    "notes": "Computed from H_wtheta entries under same tolerance"
  },
  "response_norm_bound": {
    "norm": "inf",
    "bound": 1.1452,
    "formula": "||dw/dtheta|| <= inverse_norm_bound * ||H_wtheta||"
  },
  "finite": true,
  "checks": [
    {
      "check_id": "CHK.C11.SCALING.BOUNDS_COMPUTED",
      "status": "PASS",
      "details": {
        "rho_bound": 0.1268,
        "finite": true
      }
    }
  ],
  "created_at_utc": "2026-03-05T00:00:00Z"
}
```

### Field requirements
- `rho_bound` MUST be < 1 for PASS.
- `finite` MUST be true iff all bounds are finite numbers.
- The `norm` used must match (or be explicitly related to) the norm in Task 8.

---

## 4) PhaseC_TASK11_EXPOSURE_RESPONSE_COMPATIBILITY_REPORT.md

### Filename
`PhaseC_TASK11_EXPOSURE_RESPONSE_COMPATIBILITY_REPORT.md`

### Purpose
Human-readable report that mirrors the `checks` blocks above and provides a Phase D readiness verdict.

### Required report sections
1. Run and inputs summary
2. H_wtheta sign pattern summary (including `constraint`, `tolerance`, `violations`)
3. Inverse sign certificate summary (Task 9)
4. Response sign prediction summary (selected entries + full matrix encoding)
5. Scaling bounds summary (Task 8 → Task 11)
6. Final status (PASS/FAIL) and Phase D gate recommendation
