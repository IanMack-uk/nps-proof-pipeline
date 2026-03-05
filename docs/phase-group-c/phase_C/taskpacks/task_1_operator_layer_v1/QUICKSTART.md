# Taskpack 1 — Operator Layer (Quickstart)

This taskpack certifies the **objects + conventions layer** needed for Phase C Hessian analysis:
- what is the operator / objective being differentiated,
- what is the equilibrium point being evaluated,
- what is the structural-coordinate basis (Phase A),
- what are the sign conventions (maximize/minimize; Φ vs −Φ; coupling matrix definition).

> **Important**: This taskpack is governance-sensitive. Do not infer “proof” from Papers 0–3. Use upstream CAS artefacts and explicit checks only.

---

## Preconditions (must hold)

### Run root exists and is canonical
Run root (example):
- `cert_artifacts/RUN_ID_TODO/`

Must contain the canonical chain in the run root:
- `CAS-0A.json`
- `CAS-A.json`
- `CAS-Ap.json`
- `CAS-0B.json`
- `CAS-B.json`
- `CAS-Bp.json`

And Phase C entry report:
- `PhaseC_ENTRY_REPORT.md` ending with `Phase C Entry Gate: APPROVED`

### Governance gates (recommended)
```bash
export NPS_IMPORT_FIREWALL=1
export NPS_CAS_GATE=1
export NPS_CERT_DEP_GATE=1
export NPS_RUN_DIR_INTEGRITY=1
```

---

## Execution options

### Option A (preferred): implement checks in code + run CLI
If your repo already has `nps.phases.phase_c.build_casc`, run it after adding the operator-layer checks:

```bash
RUN=RUN_ID_TODO
PYTHONPATH=src python -m nps.phases.phase_c.build_casc   --run-id "$RUN"   --run-root "cert_artifacts/$RUN"
```

### Option B (docs-only): produce operator-layer report
If you are not patching code yet, you can still complete a governance-clean deliverable:
- Write `PhaseC_TASK1_OPERATOR_LAYER_REPORT.md` to the run root
- Populate it using:
  - `phaseC_TASK1_REPORT_TEMPLATE.md`
  - `phase_C_task1_verification_rules.md`
  - `phase_C_task1_upstream_evidence_map.md`

---

## Deliverables (minimum)

Write to run root:
- `OPERATOR_LAYER.json` (new; formal operator/basis/convention object)
- `PhaseC_TASK1_OPERATOR_LAYER_REPORT.md` (new; uses the template)

Optionally (if your Phase C CLI supports it already):
- `CAS-C.json` updated with an `operator_layer` section referencing `OPERATOR_LAYER.json`

---

## Recommended commit policy

- Commit and push:
  - code changes (if any)
  - docs under `docs/phase-group-c/phase_C/`
- Do **not** commit `cert_artifacts/` outputs unless you have an explicit exception policy.

If you want proof-of-execution evidence without committing generated artefacts, add:
- `docs/phase-group-c/phase_C/RUNS/RUN_ID_TODO.md`

containing the exact command + env vars + commit SHA.

