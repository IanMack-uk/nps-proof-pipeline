# Governance Policies for Cascade

## Non-negotiables
- Do **not** merge phases.
- Do **not** silently weaken assumptions.
- All assumptions must be explicit and registered (no implicit maths).
- Phase import isolation must be enforced and tested.
- Every phase must produce auditable outputs (CAS tables + dependency traces + minimality logs).
- Must fail loudly on violated hypotheses (exceptions + failure witnesses).

## Artefact rules
- Every task must produce a `REPORT.md` stored **next to the task instruction**.
- If a task generates or updates documents (DAG, CAS tables, proof skeleton), write them into the task’s `ARTIFACTS/` folder.
- If a task introduces deprecations or file deletions, report them explicitly and justify.

## Clean-up rule (pristine repo target)
- Prefer small, verifiable deletions.
- Remove dead code only after:
  1) call sites are removed,
  2) tests confirm behavior unchanged,
  3) DAG check confirms no hidden imports remain.

