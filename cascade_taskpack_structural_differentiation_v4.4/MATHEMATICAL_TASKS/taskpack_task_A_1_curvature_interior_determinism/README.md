# Task A.1 — Curvature + Interior Equilibrium Determinism

Point Cascade to `TASK.md`.

This is a small upgrade to the Phase‑A toy quadratic harness:
- adds curvature (negative definiteness) check
- adds interior feasibility check
- makes toy equilibrium deterministic and interior by construction

This prevents two subtle inconsistencies:
1) stationarity alone does not certify a maximiser;
2) boundary equilibria violate the interior‑regime contract.
