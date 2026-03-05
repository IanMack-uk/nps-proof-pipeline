# CAS-0C.json — Minimal Specification (v2)

This spec is intentionally minimal: it describes the **shape** of `CAS-0C.json` so Phase 0C Step 2 can produce a consistent artefact for review.

## Purpose
`CAS-0C.json` is the **approved / VERIFIED-only** dependency set that Phase C is allowed to import.

It must contain **no unverified Paper 0 / Paper 1 claims**.

## File location
- `cert_artifacts/<run_id>/CAS-0C.json`

## Minimal required fields (recommended)

Top-level keys:
- `phase`: string, must be `"0C"`
- `run_id`: string
- `generated_at_utc`: string (ISO-like UTC timestamp)
- `inputs`:
  - `phase_c_entry_report`: relative path string
  - `cas_chain`: list of relative path strings (canonical chain inspected)
- `spectral_escalation`: boolean
- `verified_imports`: list of objects

Each object in `verified_imports` should include:
- `import_id`: string (stable identifier, e.g. `P1.CLAIM.HESSIAN_SELF_ADJOINT` or `TOOL.NEUMANN_SERIES_BOUND`)
- `kind`: one of:
  - `"upstream_cas_fact"`
  - `"finite_dim_tool"`
- `source_ref`: string (where it came from)
  - if upstream: `CAS-A.json:<path>` / `CAS-B.json:<path>`
  - if tool: a short label or citation key
- `status`: must be `"VERIFIED"`
- `notes`: optional string

## Non-goals
- This file does not attempt to fully model Paper 0 / Paper 1.
- This file is not a proof; it is a **dependency declaration** backed by evidence.
