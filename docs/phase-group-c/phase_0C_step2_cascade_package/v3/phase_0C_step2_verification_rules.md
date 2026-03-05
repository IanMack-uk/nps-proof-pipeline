# Phase 0C Step 2 — Verification Rules (operational)

This file defines what counts as **VERIFIED** vs **UNVERIFIED** when constructing `CAS-0C.json` and `PROV-0C.json`.

## Core rule
- **Never** place a Paper 0 / Paper 1 claim into `CAS-0C.json` unless it is **VERIFIED** under the rules below.
- Any non-VERIFIED claim must be placed into `PROV-0C.json` with a concrete Phase C test plan.

## Allowed evidence for VERIFIED (preferred order)

### A) Upstream certified artefact evidence (preferred)
A claim is VERIFIED if it is directly supported by a **specific upstream CAS artefact field** or **explicit check result** that is already part of the canonical chain:
- `CAS-A.json` checks (e.g. `CHK.A.*` with `ok: true`)
- `CAS-B.json` equilibrium regime fields (e.g. `equilibrium_objective`, `equilibrium_regime`, `equilibrium_certified_objective`)
- Anything already locked by A′ / B′ approvals (presence of `CAS-Ap.json`, `CAS-Bp.json`) provided the evidence is explicit.

### B) Step 2 explicit verification
If Step 2 performs an explicit, auditable verification action, it may mark a claim VERIFIED **only if**:
- the action is described in `Phase0C_REPORT.md` with inputs/outputs, and
- the action writes an artefact (or cites an existing artefact) that a reviewer can re-run or inspect.

Practical examples of acceptable Step 2 verifications:
- Reading a specific upstream check result and asserting it matches the claim.
- Verifying a simple algebraic convention lock by comparing fields in CAS-A vs CAS-B.

## Not allowed as VERIFIED evidence (must remain UNVERIFIED)
- “Paper says so.”
- Informal reasoning without an auditable upstream artefact reference.
- Diagnostics from `experiments/`.
- Numeric experiments that are not written as structured artefacts (at minimum: report + reproducible command).

## What to record in the report for each claim
For every candidate claim you consider, record:
- Claim ID
- Short description
- Evidence (file + field path, or explicit Step 2 verification action)
- Status: VERIFIED or UNVERIFIED
- If UNVERIFIED: a Phase C test plan (what check/module will certify it)
