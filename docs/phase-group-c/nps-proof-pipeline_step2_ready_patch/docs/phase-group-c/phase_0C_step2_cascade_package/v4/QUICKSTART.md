# Phase 0C — Step 2 (v4) Quickstart

This folder makes Step 2 **deterministic** by providing the missing inputs noted in v3's checklist.

## Target run (current default)
- Run ID: `2026-03-04T211059Z`
- Run root: `cert_artifacts/2026-03-04T211059Z/`

## Outputs (written to run root)
- `CAS-0C.json` (VERIFIED-only; Phase C may import)
- `PROV-0C.json` (UNVERIFIED candidates + Phase C test plan)
- `Phase0C_REPORT.md`

## Option A — Manual (docs-only)
Use:
- `phase_0C_step2_cascade_instructions_v4.md`
- `phase0C_REPORT_TEMPLATE_v4.md`
- `candidate_claim_inventory_v4.md`
- `upstream_evidence_map_v4.md`
- Specs/rules from v3 folder (still apply)

## Option B — Automated (recommended)
Run:
```bash
PYTHONPATH=src python -m nps.phases.phase_0c.build_cas0c \
  --run-id 2026-03-04T211059Z \
  --run-root cert_artifacts/2026-03-04T211059Z \
  --phase-c-entry-report cert_artifacts/2026-03-04T211059Z/PhaseC_ENTRY_REPORT.md
```

This writes the three required artefacts into the run root.
