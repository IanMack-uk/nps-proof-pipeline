# Taskpack 12 — CAS-C Integrity and Minimality (Drop-Test) (Quickstart)

## Purpose

Assemble `CAS-C.json` from the verified artefacts and perform a minimality/drop-test audit so Phase C assumptions are sufficient and (as far as possible) minimal.

## Preconditions

- Run root exists: `cert_artifacts/RUN_ID_TODO/`
- Phase C entry gate approved:
  - `cert_artifacts/RUN_ID_TODO/PhaseC_ENTRY_REPORT.md` ends with `Phase C Entry Gate: APPROVED`
- Canonical chain present in run root:
  - `CAS-0A.json`, `CAS-A.json`, `CAS-Ap.json`, `CAS-0B.json`, `CAS-B.json`, `CAS-Bp.json`

### Governance gates (recommended)

```bash
export NPS_IMPORT_FIREWALL=1
export NPS_CAS_GATE=1
export NPS_CERT_DEP_GATE=1
export NPS_RUN_DIR_INTEGRITY=1
```

## Inputs

Authoritative (run root only):
- `All prior Taskpack artefacts referenced by CAS-C.json`
- `docs/phase-group-c/phase_C/phaseC_REPORT_TEMPLATE.md (repo canonical)`
- `docs/phase-group-c/PHASE_C_MATHEMATICAL_TOOL_WHITELIST.md`

## Outputs (write to run root)

- `CAS-C.json`
- `PhaseC_REPORT.md`
- `PhaseC_DROP_TEST_REPORT.md`

## Execution

### Option A (preferred): implement in Phase C CLI and re-run
```bash
RUN=RUN_ID_TODO
PYTHONPATH=src python -m nps.phases.phase_c.build_casc \
  --run-id "$RUN" \
  --run-root "cert_artifacts/$RUN"
```

### Option B: docs-only execution
If you are not patching code yet, you can still complete a governance-clean deliverable by writing the report in the run root using:
- `phaseC_TASK12_REPORT_TEMPLATE.md`
- `phase_C_task12_verification_rules.md`
- `phase_C_task12_upstream_evidence_map.md`

## Deliverable definition

- **VERIFIED** facts must come from upstream CAS artefacts or explicit computed checks.
- Papers 0–3 and the thesis are **idea documents only** and must be tracked as **PROV** unless independently verified.

## Notes

- READY_FOR_PHASE_D must remain governance-honest: it requires Task 11 computed + PASS.

