# Task Report — Phase Group A (Option 2) — Phase 0A → Phase A → Phase A′

## Summary
- **Outcome:** SUCCESS
- Implemented Phase Group A generators that write CAS artefacts to `cert_artifacts/<run_id>/`.
- Artefacts include audit metadata (`cas_id`, `created_at`, `inputs`, `content_hash`) compatible with the existing certification integrity gate.

## Files added/changed
- Added: `src/nps/phases/phase_a_prime/build_casa_prime.py`
- Updated: `src/nps/phases/phase_0a/build_cas0a.py`
- Updated: `src/nps/phases/phase_a/build_casa.py`
- Added tests:
  - `tests/test_phase_0a_cas0a_generation.py`
  - `tests/test_phase_a_casa_generation.py`
  - `tests/test_phase_a_prime_closure.py`
  - `tests/test_gates_on_phase_group_a.py`
- Added: `cascade_taskpack_structural_differentiation_v4.3/TASKS/task_phase_group_a/REPORT.md`

## Commands run
- `pytest -q`
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`

## Test results
- **Default mode:** PASS
- **CI-mode (gates enabled):** PASS

## Evidence excerpt (CAS-0A)
Example extracted item (from programme doc):
- Target: `A.T1`..`A.T4` (Phase A Foundations numbered items)
- Dependency: `DEP.PROG.PhaseA.Foundations` with locator `Phase A --- Foundations`
