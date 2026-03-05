# Taskpack 11 — Exposure–Response Compatibility and Scaling (Quickstart)

## Purpose

Compute and certify the cross-derivative block `H_{wθ}`, verify its sign structure, and combine it with inverse-sign results to produce unambiguous response sign predictions and scaling bounds.

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
- `THETA_FAMILY.json (Taskpack 2)`
- `H_WTHETA.json (Taskpack 2)`
- `HESSIAN_MATRIX.json (Taskpack 3)`
- `SELECTED_INVERSE_ENTRIES.json (Taskpack 10)`

## Outputs (write to run root)

- `EXPOSURE_RESPONSE_CHECK.json`
- `RESPONSE_SIGN_PREDICTIONS.json`
- `SCALING_BOUNDS.json`
- `PhaseC_TASK11_EXPOSURE_RESPONSE_COMPATIBILITY_REPORT.md`

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
- `phaseC_TASK11_REPORT_TEMPLATE.md`
- `phase_C_task11_verification_rules.md`
- `phase_C_task11_upstream_evidence_map.md`

## Deliverable definition

- **VERIFIED** facts must come from upstream CAS artefacts or explicit computed checks.
- Papers 0–3 and the thesis are **idea documents only** and must be tracked as **PROV** unless independently verified.

## Notes

- This task is the honest gate for: `Phase C Status: READY_FOR_PHASE_D`.

