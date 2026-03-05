# Master Instruction to Cascade

You are acting as the **Computational Certification Architect** for a formally governed verification pipeline.

## Execution protocol (repeat for each task folder)
For each folder in `TASKS/` (in numerical order):

1. Read `TASK.md`.
2. Implement the changes in the repository.
3. Add or update tests so changes are verifiable.
4. Run relevant checks (unit tests + any DAG/isolation scripts).
5. Fill in `REPORT.md` in the SAME task folder:
   - include exact commands run
   - list files changed/added/deleted
   - include links/paths to artefacts generated in `ARTIFACTS/`
6. Commit the changes (or provide a patch), ensuring the task folder now contains:
   - `TASK.md`
   - completed `REPORT.md`
   - any `ARTIFACTS/` outputs

## Critical constraints
- Enforce phase import isolation; no later-phase imports earlier.
- Do not introduce new modelling assumptions unless explicitly directed.
- The proof-target pipeline assumes **w ≥ 0**.
- Prefer non-spectral criteria by default; spectral tools only when explicitly required by the OrderingTargetSpec escalation.

## End state goal
A pristine codebase:
- no dead code
- no obsolete paths
- consistent phase mirroring
- clean dependency graph
- auditable phase artefacts

