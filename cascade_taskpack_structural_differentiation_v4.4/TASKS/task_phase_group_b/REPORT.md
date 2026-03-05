# Task Report — Phase Group B (0B → B → B′)

## Summary
- **Outcome:** SUCCESS
- Implemented Phase Group B artefacts and checkers for the toy quadratic harness.
- Added an operator formulation `F(w)=∇Φ(w)` and Jacobian `J(w)=∂F/∂w` (toy: constant Hessian).
- Added witness-based Phase B checkers (`CHK.B.*`) and wired them into CAS-B generation under `--toy-quadratic`.
- Implemented Phase 0B / Phase B / Phase B′ generators producing `CAS-0B.json`, `CAS-B.json`, `CAS-Bp.json` under `cert_artifacts/<run_id>/`.
- Implemented Phase B′ closure rule: blocks approval if any `CHK.B.*` check fails when checks are present.

## Files added/changed
- Added: `src/nps/operators/__init__.py`
- Added: `src/nps/operators/equilibrium_operator.py`
- Added: `src/nps/validation/phase_b_operator_checks.py`
- Added: `src/nps/phases/phase_0b/__init__.py`
- Added: `src/nps/phases/phase_0b/build_cas0b.py`
- Added: `src/nps/phases/phase_b/__init__.py`
- Added: `src/nps/phases/phase_b/build_casb.py`
- Added: `src/nps/phases/phase_b_prime/__init__.py`
- Added: `src/nps/phases/phase_b_prime/build_casb_prime.py`
- Added tests:
  - `tests/test_phase_0b_cas0b_generation.py`
  - `tests/test_phase_b_operator_checks_toy.py`
  - `tests/test_phase_group_b_end_to_end.py`
  - `tests/test_gates_on_phase_group_b.py`

## Commands run (taskpack convention)
- `PYTHONPATH=src python -m nps.phases.phase_0b.build_cas0b --input <path-to-CAS-A.json>`
- `PYTHONPATH=src python -m nps.phases.phase_b.build_casb --toy-quadratic --input <path-to-CAS-0B.json>`
- `PYTHONPATH=src python -m nps.phases.phase_b_prime.build_casb_prime --input <path-to-CAS-B.json>`
- `pytest -q`
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`

## CAS-B checks excerpt
Example check records (shape + key witness fields):
```json
{"check_id":"CHK.B.OPERATOR_MATCHES_GRAD","ok":true,
 "witness":{"max_abs_diff":0.0,"sample_point":[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]}}
```
```json
{"check_id":"CHK.B.JACOBIAN_INVERTIBLE_AT_WSTAR","ok":true,
 "witness":{"min_singular_value":1.0,"cond_estimate":3.2}}
```

## Notes: checked vs assumed
- **Checked (toy):** operator/gradient agreement, Jacobian/Hessian agreement, Jacobian symmetry, Jacobian sparsity-locality, invertibility at `w*`.
- **Assumed for later phases:** any non-toy structural claims beyond the interior-regime toy harness; Phase B is scoped to certify the operator objects and computational prerequisites.
