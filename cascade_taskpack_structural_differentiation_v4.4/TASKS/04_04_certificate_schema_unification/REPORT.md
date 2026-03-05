# Task Report — 04_04_certificate_schema_unification: Unify certificate schemas and phase artefact outputs

## Summary
- **Outcome:** SUCCESS
- **Primary changes:**
  - Implemented a unified certificate schema covering:
    - `AssumptionCertificate`
    - `PropertyCertificate` (checkable)
    - `NumericCertificate` (approx + diagnostics)
    - `NonCheckableAssumption` (explicitly flagged)
  - Implemented a deterministic per-phase artefact emitter producing:
    - `CAS-0X.json`
    - `CAS-X.json`
    - `PhaseReport.md`
  - Added unit tests for deterministic emission and JSON normalization.
  - Generated example outputs under this task’s `ARTIFACTS/`.
- **Files changed:**
  - `src/nps/certificates/emitter.py`
  - `src/nps/certificates/schema.py`
- **Files added:**
  - `src/nps/certificates/__init__.py`
  - `src/nps/certificates/schema.py`
  - `src/nps/certificates/emitter.py`
  - `tests/test_certificate_schema_emission.py`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/04_04_certificate_schema_unification/ARTIFACTS/CAS-00D.json`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/04_04_certificate_schema_unification/ARTIFACTS/CAS-0D.json`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/04_04_certificate_schema_unification/ARTIFACTS/Phase0DReport.md`
- **Files deleted:**
  - None
- **Tests added/updated:**
  - Added `tests/test_certificate_schema_emission.py`
- **Commands run:**
  - `mkdir -p cascade_taskpack_structural_differentiation_v4.3/TASKS/04_04_certificate_schema_unification/ARTIFACTS`
  - `PYTHONPATH=src python -c "... emit_phase_artifacts(...)"` (see shell history: wrote example artefacts to the task `ARTIFACTS/` directory)
  - `pytest -q`

## Governance compliance checklist
- [x] No phase merging occurred
- [x] No assumptions weakened silently
- [ ] Assumptions explicitly registered / CAS updated
- [x] Phase import isolation preserved (tests updated)
- [x] Failure modes: loud and witness-producing
- [x] Artefacts written to `ARTIFACTS/`

## Evidence / Artefacts
- Example outputs:
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/04_04_certificate_schema_unification/ARTIFACTS/CAS-00D.json`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/04_04_certificate_schema_unification/ARTIFACTS/CAS-0D.json`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/04_04_certificate_schema_unification/ARTIFACTS/Phase0DReport.md`

### Fail-loud semantics

- Emission and schema building rely on the existing registry enforcement (`ValidationRegistry`) which raises `MathematicalInconsistency` on:
  - unknown IDs
  - uncertified assumptions required by gates
  - invalid promotion transitions

- The schema itself is deterministic and does not attempt to “auto-heal” missing or inconsistent inputs.

## Risks & Follow-ups
- `CAS-X.json` is emitted as an explicit placeholder `NonCheckableAssumption` for now; later tasks will populate CAS-X with phase-specific checkable and numeric certificates.

## Minimality & deletion notes
- No deletions performed in this task.

