# Task B.3 — Regime‑Respecting Equilibrium Selection + Convention Lock + Phase C Entry Gate — Report

## Files added

- `src/nps/models/signed_objective.py`
- `src/nps/solvers/equilibrium_candidates.py`
- `src/nps/solvers/projected_opt.py`
- `src/nps/audit/phase_c_entry_gate.py`

## Files changed

- `src/nps/phases/phase_b/build_casb.py`

## Tests added

- `tests/test_multistart_candidate_selection.py`
- `tests/test_signed_objective_wrapper.py`
- `tests/test_phase_c_entry_gate.py`
- `tests/test_phase_b_real_phi_regime_fields.py`

## Verification commands run

- `pytest -q` → **105 passed**
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q` → **105 passed**

## Persistent run

- Run dir: `cert_artifacts/2026-03-04T194723Z/`
- Decisive report: `cert_artifacts/2026-03-04T194723Z/RealPhiV0_B3_Decisive_Regime_Report.md`

## CAS artefacts generated (Phase B variants)

- `CAS-B_phi.json`
  - `certified_objective`: `phi`
  - `equilibrium_objective`: `maximize`
  - `equilibrium_regime`: `hyperbolic`
  - `equilibrium_candidate_method`: `stationary_multistart`

- `CAS-B_minus_phi.json`
  - `certified_objective`: `minus_phi`
  - `equilibrium_objective`: `maximize`
  - `equilibrium_regime`: `hyperbolic`
  - `equilibrium_candidate_method`: `stationary_multistart`

## Notes

- The Phase C entry gate is implemented in `src/nps/audit/phase_c_entry_gate.py` and blocks whenever `equilibrium_regime == "hyperbolic"` or when strict-concavity prerequisites are not satisfied.
- The decisive report summarizes whether an interior strict concave maximiser exists under Φ and −Φ for the Real Φ v0 test instance.
