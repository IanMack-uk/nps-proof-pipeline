# Task B.3.1 — Phase A `--certified-objective` propagation + first strict‑concave run (minus_phi) — Report

## Files changed

- `src/nps/phases/phase_a/build_casa.py`
  - Added Phase A CLI flag `--certified-objective {phi,minus-phi}` (default `phi`).
  - When `--real-phi-v0` is enabled, wraps the Real Φ v0 base spec with `nps.models.signed_objective.SignedObjective` using sign `+1` for `phi` and `-1` for `minus_phi`.
  - Records `derivative_definition.certified_objective` in `CAS-A.json`.
  - Adds a `PhaseA_REPORT.md` section reporting `certified_objective`.

- `src/nps/models/signed_objective.py`
  - Added attribute proxying via `__getattr__` so it can serve as a drop-in spec (for `m`, `n`, bounds, etc.).

## Tests added

- `tests/test_phase_a_real_phi_certified_objective.py`
  - Confirms curvature flip at the same stationary point:
    - `minus_phi` → `CHK.A.NEG_DEF_HESSIAN.ok == true`
    - `phi` → `CHK.A.NEG_DEF_HESSIAN.ok == false`
  - Confirms `CHK.A.STATIONARITY.ok == true` under both.
  - Confirms `CAS-A.derivative_definition.certified_objective` is recorded as expected.

## Verification commands run

- `pytest -q` → **106 passed**
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q` → **106 passed**

## Required strict‑concave certified run (minus_phi)

- Run id: `2026-03-04T203129Z`
- Run dir: `cert_artifacts/2026-03-04T203129Z/`

### Commands executed (repo root)

```bash
PYTHONPATH=src python -m nps.phases.phase_0a.build_cas0a --run-id 2026-03-04T203129Z

PYTHONPATH=src python -m nps.phases.phase_a.build_casa --real-phi-v0 --certified-objective minus-phi --run-id 2026-03-04T203129Z --input cert_artifacts/2026-03-04T203129Z/CAS-0A.json

PYTHONPATH=src python -m nps.phases.phase_a_prime.build_casa_prime --run-id 2026-03-04T203129Z --input cert_artifacts/2026-03-04T203129Z/CAS-A.json

PYTHONPATH=src python -m nps.phases.phase_0b.build_cas0b --run-id 2026-03-04T203129Z --input cert_artifacts/2026-03-04T203129Z/CAS-A.json

PYTHONPATH=src python -m nps.phases.phase_b.build_casb --real-phi-v0 --certified-objective minus-phi --objective maximize --regime strict-concave --candidate-method stationary-multistart --run-id 2026-03-04T203129Z --input cert_artifacts/2026-03-04T203129Z/CAS-0B.json

PYTHONPATH=src python -m nps.phases.phase_b_prime.build_casb_prime --run-id 2026-03-04T203129Z --input cert_artifacts/2026-03-04T203129Z/CAS-B.json

PYTHONPATH=src python -c "from pathlib import Path; from nps.audit.phase_c_entry_gate import validate_phase_c_entry; validate_phase_c_entry(Path('cert_artifacts/2026-03-04T203129Z'))"
```

### Evidence

- **Phase A**:
  - `CAS-A.derivative_definition.certified_objective == "minus_phi"`
- **Phase A′**:
  - `CAS-Ap.blocking_issues == []` → approved
- **Phase B**:
  - `CAS-B.certified_objective == "minus_phi"`
  - `CAS-B.equilibrium_regime == "strict_concave"`
- **Phase B′**:
  - `CAS-Bp.approved == true` and `CAS-Bp.blocking_issues == []`
- **Phase C entry gate**:
  - **PASS**

## Run report

- `cert_artifacts/2026-03-04T203129Z/B3_1_StrictConcave_MinusPhi_RUN_REPORT.md`
