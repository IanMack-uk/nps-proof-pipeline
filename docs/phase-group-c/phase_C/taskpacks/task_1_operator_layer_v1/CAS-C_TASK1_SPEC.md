# CAS-C Task 1 Spec — Operator Layer Artefact (`OPERATOR_LAYER.json`)

This spec defines the **minimum required schema** for the Task 1 operator-layer artefact.

This artefact is intended to be referenced by `CAS-C.json` (eventually), but it can stand alone as a run-root deliverable.

---

## File location (run root)

`cert_artifacts/<run_id>/OPERATOR_LAYER.json`

---

## Required top-level fields

```json
{
  "schema_version": "C-OPERATOR-LAYER.v1",
  "run_id": "2026-03-04T211059Z",
  "generated_utc": "2026-03-05T12:34:56Z",
  "sources": {
    "cas_a": "cert_artifacts/<run_id>/CAS-A.json",
    "cas_b": "cert_artifacts/<run_id>/CAS-B.json",
    "phase_c_entry_report": "cert_artifacts/<run_id>/PhaseC_ENTRY_REPORT.md"
  },
  "objective_convention": {
    "certified_objective": "minus_phi",
    "equilibrium_objective": "maximize",
    "notes": "If minus_phi + maximize, then curvature negativity corresponds to strict concavity of -Phi."
  },
  "equilibrium": {
    "w_star_ref": "CAS-B.equilibrium.w_star",
    "dim_w": 0
  },
  "operator": {
    "F_definition": "F(w,theta) := grad_w Phi_cert(w,theta)",
    "H_definition": "H(w,theta) := d2/dw2 Phi_cert(w,theta)",
    "C_definition": "C := -H"
  },
  "structural_basis": {
    "basis_id": "STRUCTURAL_COORDS_PHASE_A",
    "ordering_rule": "describe deterministic ordering here",
    "permutation_P": []
  },
  "checks": [
    {"check_id": "CHK.C1.HESSIAN.SYMMETRIC", "ok": true, "details": "..." }
  ]
}
```

Notes:
- `dim_w` must be the dimension of the equilibrium weight vector.
- `permutation_P` may be empty only if an explicit `ordering_rule` is provided and deterministic.

---

## Check ID requirements

`checks` must include results for every rule in:
- `phase_C_task1_verification_rules.md`

---

## Relationship to CAS-C

When Phase C is fully implemented, `CAS-C.json` should include:
- a reference to `OPERATOR_LAYER.json` (path)
- a summary of PASS/FAIL status of the operator-layer checks

