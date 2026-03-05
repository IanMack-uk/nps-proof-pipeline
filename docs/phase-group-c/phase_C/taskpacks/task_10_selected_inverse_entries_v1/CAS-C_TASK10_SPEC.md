# CAS-C Task 10 Spec — Selected Inverse Entries and Phase D Interface

This spec defines the **minimum required schema** for the VERIFIED artefact(s) produced by Task 10.

## File location (run root)

All artefacts must be written under:

- `cert_artifacts/<run_id>/`

## Required top-level fields (for each JSON artefact)

Each JSON artefact MUST include:

```json
{
  "schema_version": "C-TASK10.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "sources": {},
  "checks": [
    {"check_id": "CHK.C10.EXAMPLE", "ok": true, "details": "..."}
  ]
}
```

- `sources` must list the authoritative input files used (paths).
- `checks` must include results for every check listed in `phase_C_task10_verification_rules.md`.

## Task 10 artefacts

Expected artefacts:
- `SELECTED_INVERSE_ENTRIES.json`
- `PhaseC_TASK10_SELECTED_INVERSE_ENTRIES_REPORT.md`

Define additional schema fields specific to these artefacts as needed.

