# Cleanup Plan (Stage 2)

This plan is conservative and does not authorize any large or ambiguous deletions.

## Scope / invariants

- Repository documentation under `docs/specs/*`, `docs/research/*`, programme documents, CAS documentation, and phase descriptions must be retained.
- Certification infrastructure under `src/nps/certificates/*`, `src/nps/kernel/*`, `src/nps/phases/*`, `src/nps/audit/*` must be retained.
- Test suite under `tests/*` must be retained (unless the tested code is removed).
- `cascade_taskpack_structural_differentiation_v4.3/*` must not be deleted.

## Candidate deletions

### 1) Python bytecode and cache directories (`__pycache__`, `*.pyc`)

- `file_path`: any tracked `__pycache__/` directories and `*.pyc` files
- `reason`: build artefacts; should not be committed; already excluded by `.gitignore`
- `dependency_check`: NONE (not imported)
- `test_impact`: NONE
- `approval_status`: CONDITIONAL

Notes:
- Current working tree contains `__pycache__/` and `*.pyc` on disk (see `repo_file_inventory.md`), but `git ls-files` did not list any such files as tracked at the time of plan generation.
- Therefore **no deletion action is authorized** unless we confirm these files are actually tracked (or the user explicitly wants them removed from the working tree as a housekeeping step).

### 2) macOS metadata files (`.DS_Store`)

- `file_path`: any tracked `.DS_Store`
- `reason`: OS metadata; should not be committed; already excluded by `.gitignore`
- `dependency_check`: NONE
- `test_impact`: NONE
- `approval_status`: CONDITIONAL

Notes:
- `find` did not locate `.DS_Store` files under the repo at the time of plan generation.

## Non-deletion cleanup candidates (REVIEW ONLY)

### 3) "Unused" modules detected by heuristic scan

See `unused_modules_report.md` for a conservative list of modules with no detected importers in `src/`.

- `approval_status`: NEEDS_REVIEW
- Rationale: many phase entrypoints and scripts are expected to be invoked externally (CLI/workflow) rather than imported; automatic removal would be unsafe.

## Blocking issue (must be resolved before Stage 3)

The git working tree is currently not clean (many modified/deleted/untracked files are present). Stage 3 requires running tests and producing final DAG artefacts after controlled deletions; to keep this auditable we should first restore to a clean baseline (or confirm that the current changes are intentional and in-scope for Task 10).
