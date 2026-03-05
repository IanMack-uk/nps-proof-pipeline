# CAS-C Task 8 Spec — Neumann-Series Inversion Bounds

This spec defines the **minimum required schema** for the VERIFIED artefact(s) produced by Task 8.

## File location (run root)

All artefacts must be written under:

- `cert_artifacts/<run_id>/`

## Required top-level fields (for each JSON artefact)

Each JSON artefact MUST include:

```json
{
  "schema_version": "C-TASK08.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "sources": {},
  "checks": [
    {"check_id": "CHK.C8.EXAMPLE", "ok": true, "details": "..."}
  ]
}
```

- `sources` must list the authoritative input files used (paths).
- `checks` must include results for every check listed in `phase_C_task8_verification_rules.md`.

## Task 8 artefacts

Expected artefacts:
- `NEUMANN_SERIES_BOUND.json`
- `PhaseC_TASK8_NEUMANN_SERIES_REPORT.md`

Define additional schema fields specific to these artefacts as needed.

