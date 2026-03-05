# Taskpack 9 — M-Matrix Criteria and Inverse Positivity (Quickstart)

## Purpose

If allowed by the whitelist posture, certify that the coupling matrix is a **nonsingular M-matrix** (e.g., strict diagonal dominance + Z-matrix) and conclude inverse nonnegativity/sign structure.

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
- `DIAGONAL_DOMINANCE_CERT.json (Taskpack 6)`
- `COMPARISON_INEQUALITIES_CERT.json (Taskpack 7)`
- `OPERATOR_LAYER.json (Taskpack 1)`

## Outputs (write to run root)

- `M_MATRIX_CERT.json`
- `INVERSE_POSITIVITY_CERT.json`
- `PhaseC_TASK9_M_MATRIX_REPORT.md`

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
- `phaseC_TASK9_REPORT_TEMPLATE.md`
- `phase_C_task9_verification_rules.md`
- `phase_C_task9_upstream_evidence_map.md`

## Deliverable definition

- **VERIFIED** facts must come from upstream CAS artefacts or explicit computed checks.
- Papers 0–3 and the thesis are **idea documents only** and must be tracked as **PROV** unless independently verified.

## Notes

- If `CAS-0C.spectral_escalation == false`, you must avoid spectral proofs.
- Typical route: Z-matrix + strict diagonal dominance ⇒ nonsingular M-matrix ⇒ inverse ≥ 0.

