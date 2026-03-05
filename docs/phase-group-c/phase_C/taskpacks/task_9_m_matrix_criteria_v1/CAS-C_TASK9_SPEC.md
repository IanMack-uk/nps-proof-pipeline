# CAS-C Task 9 Spec — M-Matrix Criteria and Inverse Positivity

This spec defines the **minimum required schema** for the VERIFIED artefact(s) produced by Task 9.

## File location (run root)

All artefacts must be written under:

- `cert_artifacts/<run_id>/`

## Required top-level fields (for each JSON artefact)

Each JSON artefact MUST include:

```json
{
  "schema_version": "C-TASK09.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "sources": {},
  "checks": [
    {"check_id": "CHK.C9.EXAMPLE", "ok": true, "details": "..."}
  ]
}
```

- `sources` must list the authoritative input files used (paths).
- `checks` must include results for every check listed in `phase_C_task9_verification_rules.md`.

## Task 9 artefacts

Expected artefacts:
- `M_MATRIX_CERT.json`
- `INVERSE_POSITIVITY_CERT.json`
- `PhaseC_TASK9_M_MATRIX_REPORT.md`

Define additional schema fields specific to these artefacts as needed.

