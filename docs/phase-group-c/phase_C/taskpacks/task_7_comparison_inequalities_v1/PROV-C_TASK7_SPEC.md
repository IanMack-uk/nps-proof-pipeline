# PROV-C Task 7 Spec — Comparison Inequalities and Z-Matrix Sign Pattern

This spec defines the minimum schema for unverified candidate claims associated with Task 7.

## File location (run root)

- `cert_artifacts/<run_id>/PROV-C-TASK07.json` (recommended)

## Minimum schema

```json
{
  "schema_version": "PROV-C-TASK07.v1",
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

This file is optional, but recommended whenever Task 7 depends on Paper/thesis ideas.

