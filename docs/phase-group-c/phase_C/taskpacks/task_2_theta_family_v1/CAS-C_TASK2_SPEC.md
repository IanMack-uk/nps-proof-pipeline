# CAS-C Task 2 Spec — θ-Family Artefacts

This spec defines the minimum required schema for:

- `THETA_FAMILY.json`
- `H_WTHETA.json`

These artefacts are intended to be referenced by `CAS-C.json` once Phase C is fully certified.

---

## 1) THETA_FAMILY.json

### Location
`cert_artifacts/<run_id>/THETA_FAMILY.json`

### Minimum schema
```json
{
  "schema_version": "C-THETA-FAMILY.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "theta_family_id": "edge_local_v1",
  "definition": {
    "pattern": "perturbation_basis",
    "phi_theta_form": "Phi_cert(w,theta) = Phi_cert(w) + sum_k theta_k Psi_k(w)",
    "psi_family_description": "Edge-local linear basis Psi_e(w)=w_e"
  },
  "theta_dim": 0,
  "labels": ["theta:e=...", "..."],
  "references": {
    "cas_a": "cert_artifacts/<run_id>/CAS-A.json",
    "cas_b": "cert_artifacts/<run_id>/CAS-B.json"
  }
}
```

---

## 2) H_WTHETA.json

### Location
`cert_artifacts/<run_id>/H_WTHETA.json`

### Representation options

#### Dense
```json
{
  "schema_version": "C-H_WTHETA.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "shape": [0, 0],
  "format": "dense",
  "data": [[0.0, 1.0], [0.0, 0.0]]
}
```

#### Sparse (recommended when theta_dim is large)
```json
{
  "schema_version": "C-H_WTHETA.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "shape": [0, 0],
  "format": "coo",
  "rows": [0, 3, 10],
  "cols": [0, 1, 1],
  "vals": [1.0, 1.0, 1.0],
  "tolerance": 0.0,
  "notes": "All omitted entries are treated as exactly zero."
}
```

---

## Required linkage

- `THETA_FAMILY.json.theta_dim` must equal `H_WTHETA.json.shape[1]`.
- `H_WTHETA.json.shape[0]` must equal `dim_w` from equilibrium.

---

## Required checks

These artefacts must include (either inline metadata or in the report) the outcomes of:
- `phase_C_task2_verification_rules.md`

