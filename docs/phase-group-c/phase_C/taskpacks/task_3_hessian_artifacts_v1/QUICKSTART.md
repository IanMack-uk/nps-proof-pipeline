# Taskpack 3 — Hessian Computation Artefacts (Quickstart)

## Purpose

Compute the Hessian of the **certified objective** at the certified equilibrium point and store it as an auditable run-root artefact (in the structural-coordinate basis).

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
- `OPERATOR_LAYER.json (from Taskpack 1, recommended)`
- `CAS-A.json`
- `CAS-B.json`
- `PhaseC_ENTRY_REPORT.md`

## Outputs (write to run root)

- `HESSIAN_MATRIX.json`
- `PhaseC_TASK3_HESSIAN_ARTIFACTS_REPORT.md`

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
- `phaseC_TASK3_REPORT_TEMPLATE.md`
- `phase_C_task3_verification_rules.md`
- `phase_C_task3_upstream_evidence_map.md`

## Deliverable definition

- **VERIFIED** facts must come from upstream CAS artefacts or explicit computed checks.
- Papers 0–3 and the thesis are **idea documents only** and must be tracked as **PROV** unless independently verified.

## Notes

- If `build_casc.py` already writes `HESSIAN_MATRIX.json`, Task 3 focuses on making it **audit-grade**: basis-locked, schema-stable, and verified by explicit checks.

