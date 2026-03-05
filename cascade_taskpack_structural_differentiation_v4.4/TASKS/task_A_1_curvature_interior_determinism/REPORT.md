# Task Report — A.1 Curvature + Interior Equilibrium Determinism

## Summary
- **Outcome:** SUCCESS
- Added two missing Phase‑A checks for the toy harness:
  - `CHK.A.NEG_DEF_HESSIAN` (curvature consistency with maximisation)
  - `CHK.A.INTERIOR_FEASIBILITY` (interior‑regime feasibility)
- Updated the toy quadratic construction so the equilibrium is deterministic and interior by construction (`w0 = 0.5·1`, `b = -A @ w0`).
- Wired the new checks into `CAS-A.json` under `--toy-quadratic` in the taskpack’s required ordering.

## Files changed
- Updated: `src/nps/validation/phase_a_foundations_checks.py`
  - Added `check_negative_definite_hessian` (`CHK.A.NEG_DEF_HESSIAN`)
  - Added `check_interior_feasibility` (`CHK.A.INTERIOR_FEASIBILITY`)
- Updated: `src/nps/models/quadratic_toy.py`
  - Deterministic interior equilibrium by construction (`w0 = 0.5*ones`, `b = -A@w0`, `c=0`)
- Updated: `src/nps/phases/phase_a/build_casa.py`
  - Embedded the two new checks into the toy check list
- Added: `tests/test_quadratic_toy_deterministic_equilibrium.py`
- Updated: `tests/test_phase_a_with_toy_checks.py`
- Updated: `tests/test_gates_on_with_toy.py`

## Commands run
- `pytest -q`
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`

## CAS‑A excerpt
Example of the two new check records in `CAS-A.json` (shape only):
```json
{"check_id":"CHK.A.INTERIOR_FEASIBILITY","ok":true,"margin":0.499999999999,"witness":{...}}
{"check_id":"CHK.A.NEG_DEF_HESSIAN","ok":true,"margin":1.000000001,"witness":{...}}
```

## Notes
- With `b = -A @ w0`, the toy has `grad(w0)=0` exactly (up to floating arithmetic), and since `A` is negative definite, `w0` is the unique global maximiser of Φ over Ω.
