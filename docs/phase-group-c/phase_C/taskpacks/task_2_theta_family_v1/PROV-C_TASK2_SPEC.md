# PROV-C Task 2 Spec — θ-Family Unverified Record

If you are unsure which θ-family is “the correct one” for the thesis/Papers, do NOT guess.
Certify one minimal, explicitly-defined θ-family (recommended: perturbation basis, edge-local),
and record alternative candidate θ-families here as UNVERIFIED.

---

## Location (run root)

`cert_artifacts/<run_id>/PROV-C_TASK2_THETA_FAMILY.json`

---

## Minimum schema

```json
{
  "schema_version": "PROV-C-TASK2.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "unverified_theta_candidates": [
    {
      "theta_family_id": "brokerage_exposure_v0",
      "statement": "θ is a vector of structural exposure parameters that enter Φ_cert multiplicatively.",
      "why_unverified": "No canonical definition exists in code; paper-only idea.",
      "proposed_test": "Define Ψ_k exposure perturbations and compare response predictions vs edge-local baseline.",
      "priority": "HIGH",
      "blocks": ["Phase D monotone comparative statics"]
    }
  ]
}
```

---

## Rule

- A θ-family is VERIFIED only if:
  - it is defined explicitly as an object,
  - it has deterministic labels and ordering,
  - and `H_WTHETA.json` is computed and passes declared support/sign checks.

