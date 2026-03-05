# Task A.1 — Curvature + Interior Equilibrium Determinism (Phase A)

## Objective
Upgrade the Phase‑A toy‑quadratic verification scaffold so that Phase A can be considered **mathematically complete** (for the toy harness) with respect to:

1) **Curvature consistency with maximisation** (stationary point is actually a local maximiser)  
2) **Interior‑regime determinism** (the toy equilibrium candidate is guaranteed to lie in Ω° by construction)

This task adds two small but critical checks and ensures the toy construction is deterministic in CI.

---

## Context
Current implementation (already merged) provides:
- Toy quadratic Φ with exact grad/hess
- Phase‑A checks:
  - `CHK.A.DOMAIN_BOX`
  - `CHK.A.GRAD_FD`
  - `CHK.A.HESS_FD`
  - `CHK.A.LOCALITY_SPARSITY`
  - `CHK.A.LOCALITY_PERTURB` (optional)
  - `CHK.A.STATIONARITY`
- Phase A wiring (`--toy-quadratic`) embeds checks into `CAS-A.json`
- Phase A′ enforces `CHK.A.*` checks when present

What is missing:
- A curvature check to validate maximisation semantics
- A deterministic guarantee that w* lies in Ω° (or else treat interior regime as not discharged)

---

## Required changes

### 1) Add curvature check: `CHK.A.NEG_DEF_HESSIAN`
File to update:
- `src/nps/validation/phase_a_foundations_checks.py`

Add a new checker:

#### `check_negative_definite_hessian(A: np.ndarray, *, eps: float = 1e-9) -> dict`
- `check_id`: `CHK.A.NEG_DEF_HESSIAN`
- `ok`: true iff A is symmetric (within tolerance) and strictly negative definite with a margin.
- Implementation requirements:
  - Compute symmetry error: `||A - A.T||_max`
  - Enforce symmetry within tolerance (e.g. `1e-10`)
  - Then certify negative definiteness by **one** of:
    - eigenvalue check: `min_eig < -eps` (preferred for small m)
    - or Cholesky on `-A` (if `-A` is SPD)
  - Provide a **margin** value (positive when ok), e.g. `-(min_eig)` or cholesky min diagonal margin.
- Witness must include:
  - `symmetry_error`
  - `min_eigenvalue` (or equivalent)
  - `eps`

Notes:
- For m≤32 eigenvalue check is fine and deterministic.

### 2) Add interior feasibility check: `CHK.A.INTERIOR_FEASIBILITY`
File to update:
- `src/nps/validation/phase_a_foundations_checks.py`

Add a new checker:

#### `check_interior_feasibility(w_star: np.ndarray, lower: float, upper: float, *, eps: float = 1e-12) -> dict`
- `check_id`: `CHK.A.INTERIOR_FEASIBILITY`
- For box Ω=[lower,upper]^m, check:
  - `lower + eps < w_star_i < upper - eps` for all i
- Margin:
  - `min(w_star - (lower+eps), (upper-eps) - w_star)` (minimum componentwise interior slack)
- Witness includes:
  - `min_component`, `max_component`
  - `min_slack`
  - `eps`, `lower`, `upper`
  - indices of violations if any

### 3) Make toy equilibrium deterministic and interior by construction
File to update:
- `src/nps/models/quadratic_toy.py`

Update `make_local_quadratic_toy(...)` so that it guarantees an interior equilibrium for the default Phase‑A run.

Required behaviour:
1. Construct A as before (symmetric, strictly diagonally dominant, negative definite, locality-compatible sparsity).
2. Choose a canonical interior point:
   - `w0 = 0.5 * np.ones(m)`
3. Set `b = -A @ w0` (and choose c=0 unless needed)

Then the stationary point satisfies:
- `grad(w0) = A @ w0 + b = 0`
and, since A is negative definite, `w0` is the unique local (and global) maximiser for the concave quadratic and is interior to Ω.

This eliminates the “maybe w* lies on boundary” branch for the toy scaffold.

**IMPORTANT:** preserve any existing helper functions and public exports in this module. Do not delete `__all__` if present. Make minimal edits.

### 4) Wire new checks into Phase‑A CAS generation (`--toy-quadratic`)
File to update:
- `src/nps/phases/phase_a/build_casa.py`

When `--toy-quadratic` is enabled:
- Use `w0` from the toy spec (if available) or reconstruct it as `0.5*ones(m)`.
- Add the new checks to the embedded check list:
  - `CHK.A.NEG_DEF_HESSIAN` on `A`
  - `CHK.A.INTERIOR_FEASIBILITY` on `w_star` with lower/upper from spec

Suggested ordering of checks:
1. DOMAIN_BOX
2. INTERIOR_FEASIBILITY
3. STATIONARITY
4. NEG_DEF_HESSIAN
5. GRAD_FD
6. HESS_FD
7. LOCALITY_*

### 5) Enforce in Phase A′ (already present)
Phase A′ currently enforces all `CHK.A.*` are `ok==true` when checks exist.
No change needed unless it filters check ids; ensure the two new check ids are included.

---

## Tests (required)

1) **New:** `tests/test_quadratic_toy_deterministic_equilibrium.py`
- Build toy spec with defaults
- Assert `w0` is interior (0<0.5<1)
- Assert `grad(w0)` is (near) zero
- Assert negative definiteness check passes

2) Update `tests/test_phase_a_with_toy_checks.py`
- Ensure CAS‑A `checks` includes:
  - `CHK.A.NEG_DEF_HESSIAN`
  - `CHK.A.INTERIOR_FEASIBILITY`
- Ensure both are `ok==true`

3) Update `tests/test_gates_on_with_toy.py`
- Same assertions under env‑vars-on mode

All tests must remain fast.

---

## Reporting
Write:

- `cascade_taskpack_structural_differentiation_v4.3/TASKS/task_A_1_curvature_interior_determinism/REPORT.md`

Must include:
- files changed
- commands run
- excerpt showing the two new checks in CAS‑A
- note that toy equilibrium is now deterministic and interior by construction

---

## Verification commands (must run)
- `pytest -q`
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`

Both must pass.

---

## Definition of Done
- `CHK.A.NEG_DEF_HESSIAN` implemented and recorded in CAS‑A under `--toy-quadratic`
- `CHK.A.INTERIOR_FEASIBILITY` implemented and recorded
- `make_local_quadratic_toy` guarantees an interior stationary point by construction (w0=0.5 ones)
- tests added/updated and passing in default and CI‑mode
- report written
