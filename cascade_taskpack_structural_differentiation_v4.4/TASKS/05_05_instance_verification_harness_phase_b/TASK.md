# 05_05_instance_verification_harness_phase_b: Phase B instance-level verification harness (equilibrium + Hessian diagnostics)

## Goal
Create the missing programme-blocker: an instance-level harness that produces Phase B certificates.

## Required actions
1. Implement an `Instance` interface describing required model hooks:
   - objective extension choice (fixed)
   - gradient, Hessian access
   - basepoint specification
   - regime (interior)
2. Implement certificate generation:
   - EquilibriumCertificate (stationarity residuals; feasibility; w>=0 enforced in proof-target)
   - HessianCertificate (symmetry; negative definiteness at basepoint; conditioning; degeneracy witness)
3. Add robust numerical diagnostics with clear failure modes.
4. Add unit tests, property-based perturbation tests, and degeneracy tests.

## Artefacts
- example certificates for a minimal analytic instance

## Report requirements
- Include thresholds, conditioning logic, and how degeneracy is detected.

