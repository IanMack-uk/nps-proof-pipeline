# Upstream Evidence Map (v4)

This file makes Step 2 deterministic by specifying what counts as VERIFIED evidence for each claim.

Run: `2026-03-04T211059Z`
Evidence sources allowed:
- `cert_artifacts/2026-03-04T211059Z/CAS-A.json` (checks list)
- `cert_artifacts/2026-03-04T211059Z/CAS-B.json` (objective/regime fields)
- `cert_artifacts/2026-03-04T211059Z/PhaseC_ENTRY_REPORT.md` (Step 1 record)
Never use `experiments/` outputs as VERIFIED evidence.

## Evidence rules (minimal, strict)

### P1.CLAIM.COUPLING_OPERATOR_CONVENTION
VERIFIED if:
- CAS-A and CAS-B agree on certified objective convention (e.g. both `minus_phi`), and
- CAS-B has `equilibrium_objective=maximize` and `equilibrium_regime=strict_concave`.

### P1.CLAIM.POSITIVE_DEFINITE_COUPLING
VERIFIED if Step 1 recorded:
- `CHK.A.NEG_DEF_HESSIAN: ok: true`.

### P1.CLAIM.SUSCEPTIBILITY_EXISTS
VERIFIED if CAS-B regime is strict-concave and Step 1 approved (Phase C entry PASS).

### P1.CLAIM.HESSIAN_SELF_ADJOINT / P0.CLAIM.C2_REGULARITY_ON_INTERIOR
VERIFIED if Step 1 recorded Hessian computation success via `CHK.A.NEG_DEF_HESSIAN: ok: true`.

### P1.CLAIM.INVERSE_NORM_BOUND
UNVERIFIED unless spectral escalation is explicitly enabled in CAS-0C.

Tools (TOOL.*) do not require upstream evidence.
