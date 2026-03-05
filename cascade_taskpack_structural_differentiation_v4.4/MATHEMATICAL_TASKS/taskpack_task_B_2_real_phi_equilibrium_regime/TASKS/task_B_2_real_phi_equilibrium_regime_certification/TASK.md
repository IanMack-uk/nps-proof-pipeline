# Task B.2 — Real Φ Equilibrium Finder + Regime Certification (Phase Group B)

## Purpose
Your Real Φ v0 run showed:
- `CHK.A.STATIONARITY` fails at the fixed probe point `w0 = 0.5·1`
- `CHK.A.NEG_DEF_HESSIAN` fails at that same probe point

That is expected for a non-quadratic Φ. This task upgrades the pipeline so that **Real Φ is evaluated at an actual interior stationary point** `w*` found by a solver, and the pipeline reports whether Real Φ supports:

- **Strict concavity** at `w*` (negative definite Hessian), or
- **Only hyperbolicity** at `w*` (invertible Jacobian but not negative definite), or
- **Neither** (singular / ill-conditioned Jacobian, or solver cannot find interior stationary point).

It also adds a governance rule:
> **Phase B′ must not approve if Phase A′ blocked**, unless explicitly running in diagnostic mode.

This keeps the certification chain honest.

---

## Command convention (authoritative)
All commands are executed from repo root using:

```bash
PYTHONPATH=src python -m ...
```

---

## High-level deliverables
### A) Solver for interior stationary point
Add a solver that finds `w* ∈ W°` such that `||∇Φ(w*)||` is small.

### B) Evaluate checks at `w*`, not at fixed `w0`
For Real Φ v0 mode, Phase A and Phase B checks must use the **solver-produced `w*`**.

### C) Add condition-number + invertibility diagnostics
Add witnesses that record:
- smallest eigenvalue magnitude / singular value
- condition number estimate
- whether strict concavity holds (max eigenvalue < -eps)
- whether hyperbolicity holds (min |eigenvalue| > eps)

### D) Enforce “no Phase B′ approval if Phase A′ blocked” unless diagnostic
Implement a robust rule in B′ closure.

### E) Increase report detail
Phase reports and a new consolidated run report must include more evidence to understand Real Φ (component breakdown, solver traces, curvature spectrum, locality stats).

---

## Required code changes

### 1) Solver module (new)
Add:

- `src/nps/solvers/__init__.py`
- `src/nps/solvers/interior_stationary.py`

Provide API:

```python
def find_interior_stationary_point(
    grad_fn,
    hess_fn,
    *,
    w_init,
    lower,
    upper,
    eps_interior=1e-6,
    tol_grad=1e-8,
    max_iter=200,
    damping=0.5,
    method="damped_newton",
) -> tuple[w_star, info]
```

**Requirements**
- Must be deterministic.
- Must keep iterates in the interior by projection/clipping to `[lower+eps, upper-eps]`.
- Provide `info` dict including:
  - iterations, converged bool, final_grad_norm_inf, final_grad_norm_2
  - step norms, damping schedule
  - reasons for termination
  - any line-search / backtracking stats
- Use **damped Newton** with fallback to gradient descent if Hessian is singular/ill-conditioned.
- For symmetric Hessian, prefer `np.linalg.solve`; if it fails, fall back to `np.linalg.lstsq` with warning in `info`.

### 2) Phase A Real Φ wiring: compute w* and run checks at w*
Update `src/nps/phases/phase_a/build_casa.py`:

- When `--real-phi-v0` is enabled:
  - Build `RealPhiV0Spec` via existing `make_real_phi_v0_test_spec()`.
  - Compute `w_star` using `find_interior_stationary_point` starting from `w_init = 0.5·1`.
  - Record `w_star` and the solver `info` under:
    - `equilibrium_candidate: { w_star: [...], solver_info: {...} }`
  - Run Phase A checks using `w_star` (not w0):
    - `CHK.A.INTERIOR_FEASIBILITY` evaluated at `w_star`
    - `CHK.A.STATIONARITY` evaluated at `w_star`
    - `CHK.A.NEG_DEF_HESSIAN` evaluated at `w_star` (Hessian at w*)
- If solver fails to converge, `CHK.A.STATIONARITY` must fail with witness including solver info.

### 3) Phase B Real Φ wiring: reuse w* and compute operator/J at w*
Update `src/nps/phases/phase_b/build_casb.py`:

- When `--real-phi-v0` is enabled:
  - Load `w_star` from `cert_artifacts/<run_id>/CAS-A.json` (same run-id).
  - If absent, recompute using the solver and record it.
  - Run `CHK.B.*` checks at `w_star`.
  - Add new check:
    - `CHK.B.JACOBIAN_CONDITIONING` with witness:
      - `min_abs_eigenvalue`
      - `max_abs_eigenvalue`
      - `condition_estimate`
      - `invertible_eps`
      - `is_hyperbolic`
      - `is_strictly_concave`

### 4) Checker additions/updates
Update `src/nps/validation/phase_a_foundations_checks.py` and the Phase B operator-check module:

#### A-side
- Ensure `check_stationarity(w, grad)` returns witness with norms.
- Ensure `check_negative_definite_hessian(A)` records:
  - `min_eigenvalue`, `max_eigenvalue`, `spectrum_summary` (min/median/max)

#### B-side
Add `check_jacobian_conditioning(J, eps=...)` returning `CHK.B.JACOBIAN_CONDITIONING`.

### 5) Governance: B′ approval depends on A′ approval
Update `src/nps/phases/phase_b_prime/build_casb_prime.py`:

- Load **CAS-Ap.json** from the same run directory.
- If `approved != true` then:
  - If diagnostic mode is NOT enabled: block approval with issue:
    - `UPSTREAM_BLOCK: Phase A′ not approved; Phase B′ cannot approve under certification mode.`
  - If diagnostic mode IS enabled: allow approval but add a non-blocking note.

**Diagnostic enablement**
- Add CLI flag: `--diagnostic-allow-upstream-block`
- And environment variable: `NPS_DIAGNOSTIC=1`
- Default: **off**.

### 6) Reporting upgrades (more evidence)
Upgrade reports for Real Φ v0 runs:

**Must include**
- Solver trace summary: iterations, convergence, termination reason, grad norms.
- `w_star` summary: min/max component, min_slack.
- Curvature summary at w*:
  - min_eig, max_eig, count_pos, count_neg, count_near_zero
  - strict concavity yes/no
  - hyperbolicity yes/no
- Component breakdown (Real Φ):
  - For a few nodes i: A_i, M_i, R_i and each log-term contribution
  - Total Φ and per-term totals.
- Locality stats:
  - Hessian nonzeros, sparsity ratio.
- If anything fails: include witness JSON snippet and interpretation.

### 7) New consolidated regime report (required)
Write into the run dir:

- `cert_artifacts/<run_id>/RealPhiV0_B2_Regime_CERT_REPORT.md`

Must answer:
- Found interior stationary point?
- Strictly concave at w*?
- If not, still hyperbolic/invertible?
- Conditioning summary
- Any approval blocks due to upstream A′
- Implications for Phase C readiness

### 8) Tests (required)
Add:
- `tests/test_interior_stationary_solver.py`
- `tests/test_real_phi_v0_stationary_point_pipeline.py`
- `tests/test_b_prime_upstream_blocking.py`
- `tests/test_jacobian_conditioning_checker.py`

### 9) Verification commands (must run)
```bash
pytest -q
NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q
```

---

## Required persistent run (must do)
Create a new run and capture artefacts/reports:

```bash
PYTHONPATH=src python -m nps.phases.phase_0a.build_cas0a
PYTHONPATH=src python -m nps.phases.phase_a.build_casa --real-phi-v0 --input cert_artifacts/<run_id>/CAS-0A.json
PYTHONPATH=src python -m nps.phases.phase_a_prime.build_casa_prime --input cert_artifacts/<run_id>/CAS-A.json

PYTHONPATH=src python -m nps.phases.phase_0b.build_cas0b --input cert_artifacts/<run_id>/CAS-A.json
PYTHONPATH=src python -m nps.phases.phase_b.build_casb --real-phi-v0 --input cert_artifacts/<run_id>/CAS-0B.json
PYTHONPATH=src python -m nps.phases.phase_b_prime.build_casb_prime --input cert_artifacts/<run_id>/CAS-B.json
```

Then write:
- `cert_artifacts/<run_id>/RealPhiV0_B2_Regime_CERT_REPORT.md`

---

## Acceptance criteria
DONE when:
- Checks for Real Φ v0 evaluate at solver-found `w*`.
- Reports clearly state strict concavity vs hyperbolicity (or failure).
- `CHK.B.JACOBIAN_CONDITIONING` exists with meaningful witness.
- B′ blocks if A′ blocked unless diagnostic mode is enabled.
- Tests pass in both default and gates-on modes.
- A persistent run exists with all reports + consolidated regime report.
