# Taskpack 12 — Implementation Checklist (for Cascade)

Use this checklist to ensure Taskpack 12 is airtight.

## Inputs discovery
- [ ] Identify all required artefacts for Tasks 1–11 in run root (or via known filenames).
- [ ] Build `CAS-C_MANIFEST.json` with SHA256 hashes.

## Integrity checks
- [ ] Verify all required artefacts exist.
- [ ] Verify upstream PASS statuses using JSON `checks[]` when present.
- [ ] Validate minimal JSON schema requirements per artefact.

## Cross-consistency
- [ ] run_id matches across all JSON artefacts.
- [ ] dimensions consistent (H, H_wtheta, theta dims, selected indices).
- [ ] convention lock consistent (certified_objective, maximize, strict_concave).
- [ ] sign metadata clarity: sign_pattern.constraint present, violations semantics satisfied.

## CAS-C assembly
- [ ] Construct claims list with stable claim_id and precise statement.
- [ ] For each claim, include `depends_on` + `witness` pointers.
- [ ] Ensure every witness points to a key that exists in the source JSON.
- [ ] Write `CAS-C.json` and validate against Task 12 schema.

## Drop test
- [ ] Execute strict minimality drop test for every dependency of every claim.
- [ ] Write `PhaseC_DROP_TEST_REPORT.md` with full table.
- [ ] Fail if any dependency is redundant (strict mode), unless claim rewritten to remove it.

## Final gating
- [ ] Verify required claim ids for Phase D interface are present.
- [ ] Write `PhaseC_REPORT.md` with summary and READY_FOR_PHASE_D verdict.

## Repo hygiene
- [ ] Do not commit `cert_artifacts/`.
- [ ] Commit only code/spec docs updates.
