# 01_01_import_isolation_ci: Repo-wide import isolation + CI guardrails

## Goal
Turn the existing DAG-based audit into **enforceable invariants**:
- CI fails on forbidden phase imports or new cycles.
- A single source-of-truth import policy exists (json/yaml).

## Required actions
1. Create `docs/specs/import_policy.json` (or yaml) declaring allowed imports:
   - `nps.phases.phase_a` may import only `nps.kernel`/`nps.core` + `nps.phases.phase_a.*` + explicitly imported prior-phase artefacts
   - prohibit later-phase imports earlier (A cannot import B/C/D/E)
2. Add a test (or CI script) that:
   - regenerates the import DAG from `src/nps/**/*.py`
   - validates it against the policy
   - detects cycles and fails unless explicitly whitelisted
3. Update documentation describing the enforcement.

## Artefacts to write into ARTIFACTS/
- latest DAG markdown
- edges json (node/edge list)

## Report requirements
- Provide the exact policy rules implemented.
- Show failing example(s) and how they’re prevented.

