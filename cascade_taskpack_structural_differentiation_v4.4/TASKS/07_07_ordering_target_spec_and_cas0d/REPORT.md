# Task Report — 07_07_ordering_target_spec_and_cas0d: OrderingTargetSpec + CAS-0D backward dependency extractor

## Summary
- **Outcome:** SUCCESS
- **Primary changes:**
  - Implemented `OrderingTargetSpec` with explicit target modes:
    - `AGGREGATE_DIRECTIONAL` (default; non-spectral baseline)
    - `PAIRWISE_ENTRYWISE` (escalation; spectral/M-matrix opt-in only)
  - Implemented a CAS-0D selector that is *target-driven* and enforces **no silent escalation**.
  - Implemented CAS-0D artefact emission integrated with the unified schema/emitter from Task 04.
  - Added unit tests ensuring:
    - default target never includes spectral tool IDs
    - pairwise/entrywise target requires explicit `allow_spectral_escalation=True`
    - escalated target includes spectral IDs deterministically
  - Regenerated and stored CAS-0D artefacts for both target modes in this task’s `ARTIFACTS/`.

- **Dependency differences between target modes:**
  - Default (`AGGREGATE_DIRECTIONAL`) emits `CAS-00D.json` containing only `CAS0D_BASE_IDS`.
  - Escalated (`PAIRWISE_ENTRYWISE` with `allow_spectral_escalation=True`) emits `CAS-00D_ESCALATED.json` containing:
    - `CAS0D_BASE_IDS`
    - `CAS0D_SPECTRAL_OPT_IN_IDS`

- **Files changed:**
  - `docs/specs/import_policy.json` (allow `nps.certificates` for phase artefact emission)
  - `src/nps/phases/phase_0d/cas0d_artifact_emission.py` (fix CAS-0 vs CAS-X filename separation)

- **Files added:**
  - `src/nps/phases/phase_0d/ordering_target_spec.py`
  - `src/nps/phases/phase_0d/cas0d_generator.py`
  - `src/nps/phases/phase_0d/cas0d_artifact_emission.py`
  - `tests/test_ordering_target_spec_cas0d_selection.py`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/07_07_ordering_target_spec_and_cas0d/ARTIFACTS/CAS-00D.json`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/07_07_ordering_target_spec_and_cas0d/ARTIFACTS/CAS-00D_ESCALATED.json`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/07_07_ordering_target_spec_and_cas0d/ARTIFACTS/CAS-0D.json`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/07_07_ordering_target_spec_and_cas0d/ARTIFACTS/CAS-0D_ESCALATED.json`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/07_07_ordering_target_spec_and_cas0d/ARTIFACTS/Phase0DReport.md`

- **Files deleted:**
  - None

- **Tests added/updated:**
  - Added `tests/test_ordering_target_spec_cas0d_selection.py`

- **Commands run:**
  - `mkdir -p cascade_taskpack_structural_differentiation_v4.3/TASKS/07_07_ordering_target_spec_and_cas0d/ARTIFACTS`
  - `PYTHONPATH=src python -c "... emit_cas0d_for_target(...)"` (generated both target-mode outputs)
  - `pytest -q`

## Governance compliance checklist
- [x] No phase merging occurred
- [x] No assumptions weakened silently
- [ ] Assumptions explicitly registered / CAS updated
- [x] Phase import isolation preserved (tests updated)
- [x] Failure modes: loud and witness-producing
- [x] Artefacts written to `ARTIFACTS/`

## Evidence / Artefacts
- CAS-0D outputs (CAS-0) for both target modes:
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/07_07_ordering_target_spec_and_cas0d/ARTIFACTS/CAS-00D.json`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/07_07_ordering_target_spec_and_cas0d/ARTIFACTS/CAS-00D_ESCALATED.json`

- CAS-0D outputs (CAS-X placeholders) for both target modes:
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/07_07_ordering_target_spec_and_cas0d/ARTIFACTS/CAS-0D.json`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/07_07_ordering_target_spec_and_cas0d/ARTIFACTS/CAS-0D_ESCALATED.json`

## Risks & Follow-ups
- CAS-0D artefact emission currently certifies assumption IDs as present/certified to support governance; later tasks must connect these IDs to actual checkable/non-checkable certificates and evidence.

## Minimality & deletion notes
- No deletions performed in this task.

