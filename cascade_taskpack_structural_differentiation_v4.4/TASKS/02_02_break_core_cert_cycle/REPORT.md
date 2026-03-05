# Task Report — 02_02_break_core_cert_cycle: Break the nps.core <-> nps.certification cycle

## Summary
- **Outcome:** SUCCESS
- **Primary changes:**
  - Introduced `nps.kernel` as a shared base layer for foundational types and errors.
  - Moved shared types (`SourceRef`, `PropertyKey`) to `nps.kernel.types` and refactored imports.
  - Moved foundational exception (`MathematicalInconsistency`) to `nps.kernel.errors` and refactored imports.
  - Converted `nps.core.errors` into a compatibility shim re-exporting from `nps.kernel.errors`.
  - Regenerated DAG artefacts to prove `nps.core <-> nps.certification` cycle is eliminated.
  - Tightened `docs/specs/import_policy.json` to remove the cycle allowlist and allow `nps.kernel` imports.
- **Files changed:**
  - `docs/specs/import_policy.json`
  - `src/nps/core/errors.py`
  - `src/nps/core/types.py`
  - `src/nps/certification/citations.py`
  - `src/nps/certification/dependency_registry.py`
  - `src/nps/certification/drop_test.py`
  - `src/nps/validation/records.py`
  - `src/nps/phases/phase_0a/build_cas0a.py`
  - `src/nps/phases/phase_a/seed_conjectures.py`
  - `src/nps/phases/phase_a/exposure/exposure_candidates.py`
  - `src/nps/phases/phase_a/exposure/exposure_types.py`
  - `src/nps/symbols/objects/equilibrium_edge_weight.py`
  - `src/nps/symbols/objects/relational_potential.py`
  - `src/nps/symbols/objects/structural_exposure.py`
- **Files added:**
  - `src/nps/kernel/__init__.py`
  - `src/nps/kernel/types.py`
  - `src/nps/kernel/errors.py`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/02_02_break_core_cert_cycle/ARTIFACTS/codebase_dependency_dag.md`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/02_02_break_core_cert_cycle/ARTIFACTS/codebase_dependency_edges.json`
- **Files deleted:**
  - None
- **Tests added/updated:**
  - No new tests required beyond the existing repo-wide import policy test from Task 01.
- **Commands run:**
  - `mkdir -p cascade_taskpack_structural_differentiation_v4.3/TASKS/02_02_break_core_cert_cycle/ARTIFACTS`
  - `PYTHONPATH=src python cascade_taskpack_structural_differentiation_v4.3/SCRIPTS/dag_extract.py --repo-root . --out-dir cascade_taskpack_structural_differentiation_v4.3/TASKS/02_02_break_core_cert_cycle/ARTIFACTS`
  - `PYTHONPATH=src python cascade_taskpack_structural_differentiation_v4.3/SCRIPTS/check_import_policy.py --policy docs/specs/import_policy.json --edges cascade_taskpack_structural_differentiation_v4.3/TASKS/02_02_break_core_cert_cycle/ARTIFACTS/codebase_dependency_edges.json`
  - `pytest -q`

## Governance compliance checklist
- [x] No phase merging occurred
- [x] No assumptions weakened silently
- [ ] Assumptions explicitly registered / CAS updated
- [x] Phase import isolation preserved (tests updated)
- [x] Failure modes: loud and witness-producing
- [x] Artefacts written to `ARTIFACTS/`

## Evidence / Artefacts
- Updated DAG markdown:
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/02_02_break_core_cert_cycle/ARTIFACTS/codebase_dependency_dag.md`
- Updated DAG edges json:
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/02_02_break_core_cert_cycle/ARTIFACTS/codebase_dependency_edges.json`

### Before/after edge evidence

- **Before (Task 01 edges):**
  - `nps.core -> nps.certification`
  - `nps.certification -> nps.core`
- **After (Task 02 edges):**
  - `nps.core -> nps.kernel`
  - `nps.certification -> nps.kernel`
  - (no `nps.core -> nps.certification`)
  - (no `nps.certification -> nps.core`)

## Risks & Follow-ups
- `nps.core.errors` remains as a compatibility re-export shim; a later cleanup task may remove it once all call sites migrate to `nps.kernel.errors`.

## Minimality & deletion notes
- No deletions performed in this task.

