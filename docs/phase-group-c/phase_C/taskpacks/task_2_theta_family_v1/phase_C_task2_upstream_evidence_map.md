# Phase C — Task 2 — Upstream Evidence Map (θ-Family)

This file defines what counts as VERIFIED evidence for θ-family claims.

Run: `RUN_ID_TODO`

Allowed VERIFIED sources:
- `cert_artifacts/RUN_ID_TODO/CAS-A.json`
- `cert_artifacts/RUN_ID_TODO/CAS-B.json`
- `cert_artifacts/RUN_ID_TODO/CAS-0C.json` (tool whitelist, if present)
- `cert_artifacts/RUN_ID_TODO/PhaseC_ENTRY_REPORT.md`

Never use:
- Papers / thesis as VERIFIED evidence.
- `experiments/` outputs as VERIFIED evidence.

---

## Evidence rules

### C.CLAIM.THETA_AS_PERTURBATION_COEFFICIENTS
VERIFIED if:
- `THETA_FAMILY.json` defines θ via an explicit perturbation basis and the implementation computes `H_WTHETA.json` accordingly.

### C.CLAIM.THETA_EDGE_LOCAL / NODE_LOCAL / MOTIF_LOCAL_TRIANGLE
VERIFIED if:
- the θ-family implementation exists in code,
- it defines deterministic labels,
- and `H_WTHETA.json` passes the declared support locality check.

### Any sign-structure claims about H_WTHETA
VERIFIED only if:
- a sign check is computed (e.g., all entries nonnegative), and
- numeric tolerance / sparsity rule is declared in the report.

### New mathematical tools
VERIFIED only if:
- already present as verified imports in `CAS-0C.json` referencing `PHASE_C_MATHEMATICAL_TOOL_WHITELIST`.

Otherwise:
- treat as UNVERIFIED and BLOCK.

