# Phase 0C — Step 2 (v4) — Cascade Instructions

This v4 adds the missing determinism listed in the v3 checklist:
- run id pinned
- deliverables pinned
- claim inventory pinned
- upstream evidence acceptance pinned
- optional automation entrypoint supplied (build_cas0c)

## Target run
- `2026-03-04T211059Z`
- `cert_artifacts/2026-03-04T211059Z/`

## Inputs required (run root)
- `PhaseC_ENTRY_REPORT.md` ending with `Phase C Entry Gate: APPROVED`
- Canonical CAS chain:
  - `CAS-0A.json`, `CAS-A.json`, `CAS-Ap.json`, `CAS-0B.json`, `CAS-B.json`, `CAS-Bp.json`

## Outputs required (write to run root)
- `CAS-0C.json` (VERIFIED-only; conforms to v3 CAS-0C_SPEC)
- `PROV-0C.json` (UNVERIFIED; conforms to v3 PROV-0C_SPEC)
- `Phase0C_REPORT.md` (use v4 template)

## Procedure
1) Confirm Step 1 approval exists.
2) Use the authoritative deliverables list in the report template.
3) Audit each claim in `candidate_claim_inventory_v4.md` using `upstream_evidence_map_v4.md`.
4) Populate `CAS-0C.json` with VERIFIED imports only (include tools you intend to use).
5) Populate `PROV-0C.json` with UNVERIFIED candidates + test plan + priority.
6) Perform the minimality drop-test for CAS-0C (conceptual is acceptable, but must cite which deliverable breaks).
7) Write the report to the run root.

## Preferred (automated) path
Run the CLI:
```bash
PYTHONPATH=src python -m nps.phases.phase_0c.build_cas0c \
  --run-id 2026-03-04T211059Z \
  --run-root cert_artifacts/2026-03-04T211059Z \
  --phase-c-entry-report cert_artifacts/2026-03-04T211059Z/PhaseC_ENTRY_REPORT.md
```

Then paste `cert_artifacts/2026-03-04T211059Z/Phase0C_REPORT.md` into ChatGPT for review.
