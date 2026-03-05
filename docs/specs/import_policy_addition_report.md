# Import Policy Addition Report

## Summary
A repository-native import policy file was added so that phase import isolation checks are reproducible and version-controlled.

## Files added
- `docs/specs/import_policy.json`
- `src/nps/audit/__init__.py`
- `src/nps/audit/import_policy.py`
- `cascade_taskpack_structural_differentiation_v4.3/SCRIPTS/check_import_policy_repo.py`

## Verification
- `pytest -q`: PASS
- Dependency edges regenerated: `cascade_taskpack_structural_differentiation_v4.3/TASKS/10_10_pristine_cleanup_pass/ARTIFACTS/final_dependency_edges.json`
- Import policy check:
  - Command:
    - `PYTHONPATH=src python cascade_taskpack_structural_differentiation_v4.3/SCRIPTS/check_import_policy_repo.py --policy docs/specs/import_policy.json --edges cascade_taskpack_structural_differentiation_v4.3/TASKS/10_10_pristine_cleanup_pass/ARTIFACTS/final_dependency_edges.json`
  - Result: OK (0 forward-phase import violations)

## Artefacts
- `cascade_taskpack_structural_differentiation_v4.3/TASKS/10_10_pristine_cleanup_pass/ARTIFACTS/phase_import_policy_check.json`

## Notes
- The checker enforces the `phase_order_nonforward_imports` policy against extracted edge lists.
- Type-only imports are expected to be excluded upstream when generating edges (the DAG regeneration step used for Task 10 excludes imports under `if TYPE_CHECKING:`).
