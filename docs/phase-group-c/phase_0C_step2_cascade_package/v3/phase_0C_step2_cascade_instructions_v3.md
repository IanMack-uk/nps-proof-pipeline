# Phase 0C — Step 2 (v3)
## CAS-0C Construction with VERIFIED/PROVISIONAL Split

This guide is an *operational* version of Step 2.

It preserves the v2 policy intent:
- Paper 0 / Paper 1 are **idea documents**, not certified dependencies.
- Step 2 produces **two artefacts**:
  - `CAS-0C.json` = VERIFIED only
  - `PROV-0C.json` = UNVERIFIED candidates + Phase C test plan

---

# Outputs (required)

Write to the run root:

- `cert_artifacts/<run_id>/CAS-0C.json`
- `cert_artifacts/<run_id>/PROV-0C.json`
- `cert_artifacts/<run_id>/Phase0C_REPORT.md`

---

# Preconditions

- Phase 0C Step 1 must have passed.
- Required file:
  - `cert_artifacts/<run_id>/PhaseC_ENTRY_REPORT.md`
  - must end with `Phase C Entry Gate: APPROVED`
- Canonical chain must exist in the run root (do not read from `experiments/`):

```
CAS-0A.json
CAS-A.json
CAS-Ap.json
CAS-0B.json
CAS-B.json
CAS-Bp.json
```

---

# Governance Gates (must be enabled)

```bash
export NPS_IMPORT_FIREWALL=1
export NPS_CAS_GATE=1
export NPS_CERT_DEP_GATE=1
export NPS_RUN_DIR_INTEGRITY=1
```

---

# Reference specs (use these shapes)

Use these files as the minimal spec for the JSON outputs:
- `CAS-0C_SPEC.md`
- `PROV-0C_SPEC.md`

Use these rules for VERIFIED vs UNVERIFIED:
- `phase_0C_step2_verification_rules.md`

Use this report template:
- `phase0C_REPORT_TEMPLATE_v3.md`

---

# Required Procedure

## A) Confirm Step 1 approval
1. Open `PhaseC_ENTRY_REPORT.md`.
2. Confirm it ends with `Phase C Entry Gate: APPROVED`.
3. Record the result + reference path in `Phase0C_REPORT.md`.

## B) Backward extract dependencies
1. Enumerate Phase C deliverables.
2. For each deliverable, list required properties.
3. Map each property to one of:
   - Upstream certified artefact evidence (preferred)
   - Finite-dimensional tool import (allowed tools)
   - Paper 0/1 candidate claim (must remain provisional unless VERIFIED)

Record this in the report table.

## C) Verify candidate claims (promote or park)
For each candidate Paper 0/1 claim:
- If VERIFIED under `phase_0C_step2_verification_rules.md`, add it to `CAS-0C.json`.
- Otherwise add it to `PROV-0C.json` with a concrete Phase C test plan.

## D) Minimality drop-test for CAS-0C
For each item in `CAS-0C.json`:
- Attempt removal (conceptually).
- Record whether Phase C becomes ill-posed.
- Keep only necessary VERIFIED items.

## E) Write outputs
1. Write `CAS-0C.json` following `CAS-0C_SPEC.md`.
2. Write `PROV-0C.json` following `PROV-0C_SPEC.md`.
3. Write `Phase0C_REPORT.md` using `phase0C_REPORT_TEMPLATE_v3.md`.

---

# Deliverable for ChatGPT Review

Paste the full contents of:

`cert_artifacts/<run_id>/Phase0C_REPORT.md`

into the ChatGPT conversation to approve Phase 0C and unlock Phase C.
