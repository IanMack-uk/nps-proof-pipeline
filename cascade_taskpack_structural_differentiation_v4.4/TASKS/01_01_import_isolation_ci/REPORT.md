# Task Report — 01_01_import_isolation_ci: Repo-wide import isolation + CI guardrails

## Summary
- **Outcome:** SUCCESS
- **Primary changes:**
  - Added a repo-wide, CI-enforced phase import isolation policy (`docs/specs/import_policy.json`).
  - Implemented a deterministic AST-based import DAG extractor and policy validator.
  - Wired the taskpack scripts to generate DAG artefacts and validate them against policy.
  - Added a `pytest` guard test that fails on forbidden phase imports or non-whitelisted cycles.
- **Files changed:**
  - `cascade_taskpack_structural_differentiation_v4.3/SCRIPTS/dag_extract.py`
  - `cascade_taskpack_structural_differentiation_v4.3/SCRIPTS/check_import_policy.py`
- **Files added:**
  - `docs/specs/import_policy.json`
  - `docs/specs/import_isolation_enforcement.md`
  - `src/nps/audit/__init__.py`
  - `src/nps/audit/import_graph.py`
  - `tests/test_import_isolation_policy.py`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/01_01_import_isolation_ci/ARTIFACTS/codebase_dependency_dag.md`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/01_01_import_isolation_ci/ARTIFACTS/codebase_dependency_edges.json`
- **Files deleted:**
  - None
- **Tests added/updated:**
  - Added `tests/test_import_isolation_policy.py`
- **Commands run:**
  - `mkdir -p cascade_taskpack_structural_differentiation_v4.3/TASKS/01_01_import_isolation_ci/ARTIFACTS`
  - `PYTHONPATH=src python cascade_taskpack_structural_differentiation_v4.3/SCRIPTS/dag_extract.py --repo-root . --out-dir cascade_taskpack_structural_differentiation_v4.3/TASKS/01_01_import_isolation_ci/ARTIFACTS`
  - `PYTHONPATH=src python cascade_taskpack_structural_differentiation_v4.3/SCRIPTS/check_import_policy.py --policy docs/specs/import_policy.json --edges cascade_taskpack_structural_differentiation_v4.3/TASKS/01_01_import_isolation_ci/ARTIFACTS/codebase_dependency_edges.json`
  - `pytest -q`

## Governance compliance checklist
- [x] No phase merging occurred
- [x] No assumptions weakened silently
- [ ] Assumptions explicitly registered / CAS updated
- [x] Phase import isolation preserved (tests updated)
- [x] Failure modes: loud and witness-producing
- [x] Artefacts written to `ARTIFACTS/`

## Evidence / Artefacts
- DAG markdown:
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/01_01_import_isolation_ci/ARTIFACTS/codebase_dependency_dag.md`
- DAG edges json:
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/01_01_import_isolation_ci/ARTIFACTS/codebase_dependency_edges.json`
- Enforcement documentation:
  - `docs/specs/import_isolation_enforcement.md`

## Risks & Follow-ups
- The existing import cycle `nps.core <-> nps.certification` is temporarily allowlisted in `docs/specs/import_policy.json`.
  - Task `02_02_break_core_cert_cycle` must remove this allowlist and resolve the cycle via `nps.kernel`.

## Minimality & deletion notes
- No deletions performed in this task.

