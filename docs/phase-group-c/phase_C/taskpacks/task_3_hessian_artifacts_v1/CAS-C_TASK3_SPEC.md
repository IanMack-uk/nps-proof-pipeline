# CAS-C Task 3 Spec — Hessian Computation Artefacts

This spec defines the **minimum required schema** for the VERIFIED artefact(s) produced by Task 3.

## File location (run root)

All artefacts must be written under:

- `cert_artifacts/<run_id>/`

## Required top-level fields (for each JSON artefact)

Each JSON artefact MUST include:

```json
{
  "schema_version": "C-TASK03.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "sources": {},
  "checks": [
    {"check_id": "CHK.C3.EXAMPLE", "ok": true, "details": "..."}
  ]
}
```

- `sources` must list the authoritative input files used (paths).
- `checks` must include results for every check listed in `phase_C_task3_verification_rules.md`.

## Task 3 artefacts

Expected artefacts:
- `HESSIAN_MATRIX.json`
- `PhaseC_TASK3_HESSIAN_ARTIFACTS_REPORT.md`

Define additional schema fields specific to these artefacts as needed.

