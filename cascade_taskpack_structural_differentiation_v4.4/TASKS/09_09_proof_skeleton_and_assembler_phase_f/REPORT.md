# Task Report — 09_09_proof_skeleton_and_assembler_phase_f: Proof skeleton artefact + proof assembler (Phase F)

## Summary
- **Outcome:** SUCCESS
- **Primary changes:**
  - Added a machine-readable proof skeleton format for the Ordering Theorem proof as an explicit lemma chain.
  - Implemented a proof assembler that checks all lemma prerequisites are certified in a `ValidationRegistry`.
  - Implemented loud failure witnesses when proof assembly cannot proceed.
  - Added unit tests for success/failure cases.
  - Generated a proof skeleton artefact and an example failure witness output in the task `ARTIFACTS/`.

- **Files changed:**
  - None

- **Files added:**
  - `src/nps/phases/phase_f/__init__.py`
  - `src/nps/phases/phase_f/proof_skeleton.py`
  - `src/nps/phases/phase_f/proof_assembler.py`
  - `tests/test_phase_f_proof_assembler.py`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/09_09_proof_skeleton_and_assembler_phase_f/ARTIFACTS/proof_skeleton_THM_SDOT_v4.json`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/09_09_proof_skeleton_and_assembler_phase_f/ARTIFACTS/proof_assembly_failure_example.txt`

- **Files deleted:**
  - None

- **Tests added/updated:**
  - Added `tests/test_phase_f_proof_assembler.py`

- **Commands run:**
  - `mkdir -p cascade_taskpack_structural_differentiation_v4.3/TASKS/09_09_proof_skeleton_and_assembler_phase_f/ARTIFACTS`
  - `pytest -q`
  - `PYTHONPATH=src python -c "... assemble_proof(...) ..."` (wrote failure witness example)

## Governance compliance checklist
- [x] No phase merging occurred
- [x] No assumptions weakened silently
- [ ] Assumptions explicitly registered / CAS updated
- [x] Phase import isolation preserved (tests updated)
- [x] Failure modes: loud and witness-producing
- [x] Artefacts written to `ARTIFACTS/`

## Evidence / Artefacts
- Proof skeleton artefact:
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/09_09_proof_skeleton_and_assembler_phase_f/ARTIFACTS/proof_skeleton_THM_SDOT_v4.json`
- Failure-case demonstration (missing lemma prerequisites):
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/09_09_proof_skeleton_and_assembler_phase_f/ARTIFACTS/proof_assembly_failure_example.txt`

## Risks & Follow-ups
- The proof skeleton is a governed *dependency/lemma chain*; it is not yet a full formal proof. Subsequent tasks must populate lemma evidence and connect lemma outputs to Phase D certificates.

## Minimality & deletion notes
- No deletions performed in this task.

