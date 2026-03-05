# Taskpack 10 — Selected Inverse Entries and Phase D Interface (Quickstart)

## Purpose

Define the **selection rule** for which inverse-Hessian entries (or blocks) matter for Phase D, and certify sign conclusions for just that selected subset.

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
- `INVERSE_POSITIVITY_CERT.json (Taskpack 9) OR NEUMANN_SERIES_BOUND.json (Taskpack 8)`
- `HESSIAN_BLOCKS.json (Taskpack 4)`
- `THETA_FAMILY.json (Taskpack 2, if selection depends on θ labels)`

## Outputs (write to run root)

- `SELECTED_INVERSE_ENTRIES.json`
- `PhaseC_TASK10_SELECTED_INVERSE_ENTRIES_REPORT.md`

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
- `phaseC_TASK10_REPORT_TEMPLATE.md`
- `phase_C_task10_verification_rules.md`
- `phase_C_task10_upstream_evidence_map.md`

## Deliverable definition

- **VERIFIED** facts must come from upstream CAS artefacts or explicit computed checks.
- Papers 0–3 and the thesis are **idea documents only** and must be tracked as **PROV** unless independently verified.

## Notes

- Keep selection **minimal**: only include the rows/cols Phase D truly uses.

