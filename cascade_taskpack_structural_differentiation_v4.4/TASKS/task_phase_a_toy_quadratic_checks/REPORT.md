# Task Report — Phase A Toy Quadratic Φ + Immediate Checkers

## Summary
- **Outcome:** SUCCESS
- Implemented a toy quadratic relational potential Φ with exact gradient and Hessian.
- Implemented Phase-A foundational checkers (finite difference derivative consistency, locality, stationarity) returning audit-grade structured witnesses.
- Wired check results into `CAS-A.json` under a `checks` section when `--toy-quadratic` is enabled.
- Updated Phase A′ closure to block approval if any `CHK.A.*` check fails.

## Files added/changed
- Added: `src/nps/math/__init__.py`
- Added: `src/nps/math/locality.py`
- Added: `src/nps/validation/phase_a_foundations_checks.py`
- Updated: `src/nps/phases/phase_a/build_casa.py` (added `--toy-quadratic`, embeds `checks`, records `extension_id`)
- Updated: `src/nps/phases/phase_a_prime/build_casa_prime.py` (enforces `CHK.A.*` success)
- Tests added:
  - `tests/test_quadratic_toy_derivatives.py`
  - `tests/test_quadratic_toy_locality.py`
  - `tests/test_phase_a_with_toy_checks.py`
  - `tests/test_gates_on_with_toy.py`

## Commands run
- `pytest -q`
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`

## CAS-A checks excerpt
Example check record shape:
```json
{"check_id":"CHK.A.GRAD_FD","ok":true,"margin":0.0,"witness":{...},"notes":null}
```

## Notes
- A′ closure enforces: if CAS-A contains `checks`, all `CHK.A.*` must have `ok==true` or the closure produces blocking issues.
