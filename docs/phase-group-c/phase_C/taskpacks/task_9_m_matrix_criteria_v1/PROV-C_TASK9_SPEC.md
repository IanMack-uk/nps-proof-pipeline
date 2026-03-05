# PROV-C Task 9 Spec — M-Matrix Criteria and Inverse Positivity

This spec defines the minimum schema for unverified candidate claims associated with Task 9.

## File location (run root)

- `cert_artifacts/<run_id>/PROV-C-TASK09.json` (recommended)

## Minimum schema

```json
{
  "schema_version": "PROV-C-TASK09.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "candidates": [
    {
      "claim_id": "P0.CLAIM.EXAMPLE",
      "status": "UNVERIFIED",
      "source_refs": ["Paper0", "Thesis"],
      "why_unverified": "Not certified upstream; requires proof/check.",
      "proposed_check": "Describe computational test or lemma needed.",
      "priority": "high/med/low"
    }
  ]
}
```

This file is optional, but recommended whenever Task 9 depends on Paper/thesis ideas.

