# Pre-Math Prep Report

## Summary
Implemented minimal certification-run scaffolding to avoid churn when starting Phase 0A.

- Added a governance bootstrap helper to compose existing optional gates.
- Added a repository-level certification artefacts convention (`cert_artifacts/<run_id>/`).
- Ensured certification artefacts are gitignored.

## Files added/changed
- Added: `src/nps/audit/governance.py`
- Added: `src/nps/certification/artifacts.py`
- Added: `docs/specs/cert_artifacts_convention.md`
- Added: `tests/test_cert_artifacts_convention.py`
- Added: `docs/specs/pre_math_prep_report.md`
- Changed: `.gitignore` (added `cert_artifacts/`)

## Commands run
- `pytest -q`
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`

## Behavioural impact
- When env vars are unset, no governance gates are enabled automatically.
- `cert_artifacts/` is a new output convention only; it does not affect existing programme logic.
