# 06_06_nonspectral_inverse_cert_phase_c: Phase C non-spectral inverse-structure certification (dominance margins, Neumann bounds)

## Goal
Implement the non-spectral baseline route for inverse-Hessian structure certification.

## Required actions
1. Extract Hessian block structure under structural coordinates.
2. Implement dominance margin computation (blockwise or elementwise as required).
3. Implement non-spectral inversion certificates:
   - Neumann-series sufficient conditions (norm bounds)
   - explicit inverse norm bound certificates
4. Implement Phase C′ uniformity checks when claimed:
   - dominance margin bounded away from 0 over regime sampler
5. Tests: random structured matrices, adversarial near-fail cases.

## Artefacts
- example C and C′ certificates

## Report requirements
- Precisely state which sufficient conditions are implemented and their limitations.

