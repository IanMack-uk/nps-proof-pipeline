# Task Report — 05_05_instance_verification_harness_phase_b: Phase B instance-level verification harness (equilibrium + Hessian diagnostics)

## Summary
- **Outcome:** SUCCESS
- **Primary changes:**
  - Implemented a Phase B instance-level verification harness with an explicit `Instance` protocol:
    - basepoint `w*`
    - gradient `∇φ(w*)`
    - Hessian `D²φ(w*)`
  - Implemented certificate generation:
    - `EquilibriumCertificate` (stationarity residual norms, nonnegativity feasibility witness)
    - `HessianCertificate` (symmetry defect, eigenvalues, negative-definiteness decision, conditioning estimate, degeneracy witness)
  - Implemented robust diagnostics and fail-loud behavior using `MathematicalInconsistency`.
  - Added unit tests including:
    - acceptance for a minimal analytic concave quadratic instance
    - rejection tests for stationarity violations, nonnegativity violations, and Hessian degeneracy
    - perturbation-style robustness test under small symmetric Hessian perturbations
  - Generated an example certificate JSON artefact.

- **Thresholds / logic (defaults):**
  - stationarity: `||∇φ(w*)||_∞ <= 1e-8`
  - symmetry: `||H - Hᵀ||_∞ <= 1e-10`
  - negative definiteness: `max eig(H) < -1e-10`
  - conditioning (abs eigenvalue ratio): `cond <= 1e12`
  - degeneracy detection: non-negative-definite Hessian emits a witness (max eigenpair)

- **Files changed:**
  - `src/nps/phases/phase_b/instance_harness.py`

- **Files added:**
  - `src/nps/phases/phase_b/instance_harness.py`
  - `tests/test_phase_b_instance_harness.py`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/05_05_instance_verification_harness_phase_b/ARTIFACTS/phase_b_example_certificates.json`

- **Files deleted:**
  - None

- **Tests added/updated:**
  - Added `tests/test_phase_b_instance_harness.py`

- **Commands run:**
  - `mkdir -p cascade_taskpack_structural_differentiation_v4.3/TASKS/05_05_instance_verification_harness_phase_b/ARTIFACTS`
  - `PYTHONPATH=src python -c "... certify_phase_b_instance(...) ..."` (wrote example artefact)
  - `pytest -q`

## Governance compliance checklist
- [x] No phase merging occurred
- [x] No assumptions weakened silently
- [ ] Assumptions explicitly registered / CAS updated
- [x] Phase import isolation preserved (tests updated)
- [x] Failure modes: loud and witness-producing
- [x] Artefacts written to `ARTIFACTS/`

## Evidence / Artefacts
- Example instance certificates:
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/05_05_instance_verification_harness_phase_b/ARTIFACTS/phase_b_example_certificates.json`

## Risks & Follow-ups
- This harness currently uses a direct Hessian eigenvalue check for negative definiteness; later tasks may need matrix-analysis alternatives (e.g. Gershgorin / dominance margins) to align with non-spectral-first policies.
- Property-based testing is implemented as deterministic perturbation loops (no external Hypothesis dependency); if Hypothesis is desired, it should be introduced explicitly with governance.

## Minimality & deletion notes
- No deletions performed in this task.

