# Phase 0C Step 2 Package (v2) — Quickstart

This folder provides copy/paste instructions for running **Phase 0C — Step 2** and producing three artefacts in the run root:

- `CAS-0C.json` (VERIFIED ONLY)
- `PROV-0C.json` (UNVERIFIED candidates + test plan)
- `Phase0C_REPORT.md` (review report)

## Inputs
- A target run directory: `cert_artifacts/<run_id>/`
- Step 1 must be complete:
  - `cert_artifacts/<run_id>/PhaseC_ENTRY_REPORT.md` ends with `Phase C Entry Gate: APPROVED`
- Canonical chain exists in run root:
  - `CAS-0A.json`, `CAS-A.json`, `CAS-Ap.json`, `CAS-0B.json`, `CAS-B.json`, `CAS-Bp.json`

## Governance gates (required)

```bash
export NPS_IMPORT_FIREWALL=1
export NPS_CAS_GATE=1
export NPS_CERT_DEP_GATE=1
export NPS_RUN_DIR_INTEGRITY=1
```

## What to paste into Cascade
- Primary instructions: `phase_0C_step2_cascade_instructions_v3.md`
- Report template: `phase0C_REPORT_TEMPLATE_v3.md`

## What to paste back into ChatGPT
- `cert_artifacts/<run_id>/Phase0C_REPORT.md`
