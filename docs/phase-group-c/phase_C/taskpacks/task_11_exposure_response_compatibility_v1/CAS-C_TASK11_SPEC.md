# CAS-C Task 11 Spec — Exposure–Response Compatibility and Scaling

This spec defines the **minimum required schema** for the VERIFIED artefact(s) produced by Task 11.

## File location (run root)

All artefacts must be written under:

- `cert_artifacts/<run_id>/`

## Required top-level fields (for each JSON artefact)

Each JSON artefact MUST include:

```json
{
  "schema_version": "C-TASK11.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "sources": {},
  "checks": [
    {"check_id": "CHK.C11.EXAMPLE", "ok": true, "details": "..."}
  ]
}
```

- `sources` must list the authoritative input files used (paths).
- `checks` must include results for every check listed in `phase_C_task11_verification_rules.md`.

## Task 11 artefacts

Expected artefacts:
- `EXPOSURE_RESPONSE_CHECK.json`
- `RESPONSE_SIGN_PREDICTIONS.json`
- `SCALING_BOUNDS.json`
- `PhaseC_TASK11_EXPOSURE_RESPONSE_COMPATIBILITY_REPORT.md`

Define additional schema fields specific to these artefacts as needed.

