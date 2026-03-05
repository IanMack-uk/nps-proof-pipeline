# CAS-C Task 6 Spec — Diagonal Dominance Certification

This spec defines the **minimum required schema** for the VERIFIED artefact(s) produced by Task 6.

## File location (run root)

All artefacts must be written under:

- `cert_artifacts/<run_id>/`

## Required top-level fields (for each JSON artefact)

Each JSON artefact MUST include:

```json
{
  "schema_version": "C-TASK06.v1",
  "run_id": "RUN_ID_TODO",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "sources": {},
  "checks": [
    {"check_id": "CHK.C6.EXAMPLE", "ok": true, "details": "..."}
  ]
}
```

- `sources` must list the authoritative input files used (paths).
- `checks` must include results for every check listed in `phase_C_task6_verification_rules.md`.

## Task 6 artefacts

Expected artefacts:
- `DIAGONAL_DOMINANCE_CERT.json`
- `PhaseC_TASK6_DIAGONAL_DOMINANCE_REPORT.md`

Define additional schema fields specific to these artefacts as needed.

