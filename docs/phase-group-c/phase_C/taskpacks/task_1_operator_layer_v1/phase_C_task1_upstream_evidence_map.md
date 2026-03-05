# Phase C — Task 1 — Upstream Evidence Map (Operator Layer)

This file defines what counts as **VERIFIED** evidence for Task 1 claims.

Run: `RUN_ID_TODO`

Allowed VERIFIED sources (run root only):
- `cert_artifacts/RUN_ID_TODO/CAS-A.json`
- `cert_artifacts/RUN_ID_TODO/CAS-B.json`
- `cert_artifacts/RUN_ID_TODO/PhaseC_ENTRY_REPORT.md`
- `cert_artifacts/RUN_ID_TODO/CAS-0C.json` (tool whitelist, if present)

Never use:
- `cert_artifacts/RUN_ID_TODO/experiments/` as VERIFIED evidence.

---

## Evidence rules

### P2.CLAIM.STRICT_CONCAVE_MAXIMIZER_REGIME
VERIFIED if:
- `PhaseC_ENTRY_REPORT.md` indicates PASS, and
- `CAS-B.json` declares `equilibrium_objective=maximize` and `equilibrium_regime=strict_concave`.

### P2.CLAIM.NEG_DEF_HESSIAN_AT_WSTAR
VERIFIED if:
- Phase C entry report recorded a passing negative-definite Hessian prerequisite (e.g. `CHK.A.NEG_DEF_HESSIAN: ok: true`), OR
- `CAS-A.json` includes a passing strict concavity / Hessian check in its checks list.

### P1.CLAIM.HESSIAN_SELF_ADJOINT
VERIFIED only if:
- a computational symmetry check is performed in Phase C and recorded in `OPERATOR_LAYER.json`.
(Do not accept “Hessians are symmetric” as a paper-only statement.)

### P0.CLAIM.STRUCTURAL_COORDINATES_EXIST / P0.CLAIM.STRUCTURAL_BASIS_ORDERING_DETERMINISTIC
VERIFIED if:
- `CAS-A.json` contains an explicit structural coordinate / basis map, OR
- Phase C defines and records a deterministic basis ordering rule in `OPERATOR_LAYER.json`.

### Tools / matrix analysis imports
VERIFIED if:
- `CAS-0C.json` lists them as verified imports with `source_ref: PHASE_C_MATHEMATICAL_TOOL_WHITELIST`.

Otherwise:
- treat as UNVERIFIED and BLOCK any downstream use.

