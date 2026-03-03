# CAS-A Domain Policy (Phase A)

Status: PROVISIONAL

## Proof-target policy (certified pipeline)

- Ω is treated as a nonnegative domain: w ≥ 0 componentwise.
- Sampling and projection in the sandbox model utilities default to nonnegative weights.
- This policy supports monotonicity and ordering semantics used in Phase A and beyond.

## Adversarial policy (red-team)

- Signed weights are permitted only for falsification and stress testing.
- Signed tests must not be used to promote CAS-A assumptions.

## Promotion rules

- Evidence from proof-target (nonnegative) tests may be attached to Phase A assumptions.
- Promotion means updating an AssumptionRecord’s CertificationStatus (e.g., PROVISIONAL → CERTIFIED) in the ValidationRegistry.
- Evidence/counterexamples from signed red-team tests are recorded separately and are not admissible for promotion.
