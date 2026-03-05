# PROV-0C.json — Minimal Specification (v2)

## Purpose
`PROV-0C.json` is the **provisional** dependency set:
- candidate Paper 0 / Paper 1 claims
- additional hypotheses
- any dependency ideas Phase C would like to use but which are not yet certified

Nothing in this file is allowed to be imported by Phase C as a certified dependency.

## File location
- `cert_artifacts/<run_id>/PROV-0C.json`

## Minimal required fields (recommended)

Top-level keys:
- `phase`: string, must be `"0C"`
- `run_id`: string
- `generated_at_utc`: string
- `unverified_candidates`: list of objects

Each object in `unverified_candidates` should include:
- `candidate_id`: string (e.g. `P1.CLAIM.SUSCEPTIBILITY_EXISTS`)
- `description`: string
- `status`: must be `"UNVERIFIED"`
- `why_unverified`: string
- `proposed_test_plan`: string
- `priority`: one of `"high" | "medium" | "low"`
- `blocking_for_phase_c`: boolean

## Notes
This file is meant to be *actionable* for Phase C planning: every entry should have a concrete certification plan.
