# PROV-C Task 1 Spec — Operator Layer Unverified Record

If Task 1 encounters statements that are **useful but not certifiable yet**, record them in a PROV-style artefact instead of silently assuming.

This keeps `OPERATOR_LAYER.json` clean (VERIFIED-only) while preserving a test plan.

---

## File location (run root)

`cert_artifacts/<run_id>/PROV-C_TASK1_OPERATOR_LAYER.json`

---

## Minimum schema

```json
{
  "schema_version": "PROV-C-TASK1.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "unverified_claims": [
    {
      "claim_id": "P1.CLAIM.HESSIAN_SELF_ADJOINT",
      "statement": "Hessian is self-adjoint in the structural-coordinate basis.",
      "why_unverified": "No explicit symmetry check implemented / tolerance not defined.",
      "proposed_test": "Implement CHK.C1.HESSIAN.SYMMETRIC and record numeric tolerance + max asymmetry.",
      "priority": "HIGH",
      "blocks": ["Phase C inverse sign structure lemmas"]
    }
  ]
}
```

---

## Rule

- Anything that is not backed by upstream CAS artefacts or explicit checks must go here.
- Do not “upgrade” a claim to VERIFIED without adding a check or an upstream artefact reference.

