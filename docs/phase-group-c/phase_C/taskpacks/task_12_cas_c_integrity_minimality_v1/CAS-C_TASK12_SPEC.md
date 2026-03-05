# CAS-C Task 12 Spec — CAS-C Integrity and Minimality (Drop-Test)

This spec defines the **minimum required schema** for the VERIFIED artefact(s) produced by Task 12.

## File location (run root)

All artefacts must be written under:

- `cert_artifacts/<run_id>/`

## Required top-level fields (for each JSON artefact)

Each JSON artefact MUST include:

```json
{
  "schema_version": "C-TASK12.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "sources": {},
  "checks": [
    {"check_id": "CHK.C12.EXAMPLE", "ok": true, "details": "..."}
  ]
}
```

- `sources` must list the authoritative input files used (paths).
- `checks` must include results for every check listed in `phase_C_task12_verification_rules.md`.

## Task 12 artefacts

Expected artefacts:
- `CAS-C.json`
- `PhaseC_REPORT.md`
- `PhaseC_DROP_TEST_REPORT.md`

Define additional schema fields specific to these artefacts as needed.

