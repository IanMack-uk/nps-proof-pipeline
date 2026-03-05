# Taskpack 8 — Neumann-Series Inversion Bounds (Quickstart)

## Purpose

Certify an explicit Neumann-series invertibility bound for the matrix used in inverse-sign reasoning, using a declared matrix norm and splitting.

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
- `HESSIAN_MATRIX.json (Taskpack 3)`
- `OPERATOR_LAYER.json (Taskpack 1)`
- `DIAGONAL_DOMINANCE_CERT.json (Taskpack 6, recommended)`

## Outputs (write to run root)

- `NEUMANN_SERIES_BOUND.json`
- `PhaseC_TASK8_NEUMANN_SERIES_REPORT.md`

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
- `phaseC_TASK8_REPORT_TEMPLATE.md`
- `phase_C_task8_verification_rules.md`
- `phase_C_task8_upstream_evidence_map.md`

## Deliverable definition

- **VERIFIED** facts must come from upstream CAS artefacts or explicit computed checks.
- Papers 0–3 and the thesis are **idea documents only** and must be tracked as **PROV** unless independently verified.

## Notes

- Keep this whitelist-compliant: finite-dimensional norms only; no spectral-radius arguments unless separately certified.

