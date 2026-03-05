# Task Pack — Phase A Mathematical Objects + Toy Quadratic Φ + Immediate Checkers (Mode B)

## Objective
Implement a **toy quadratic relational potential** Φ with **exact gradient/Hessian**, plus Phase‑A checkers that immediately verify:

- **Derivative consistency** (exact grad/hess vs finite differences in Ω°)
- **Locality** of the marginal field **F = ∇Φ** (by sparsity inspection and optional perturbation witness)
- **Stationarity** for an interior equilibrium candidate **w\***

All outputs must be recorded as **audit‑grade witnesses** inside `CAS-A.json` under a `checks` section, so that Phase **A′** can approve Phase A as mathematically usable.

This task is a **verification scaffold**; it does not commit the project to a quadratic model long-term.

---

## Inputs (authoritative)
Cascade must read and align with:

- `docs/Structural_Differentiation_Programme_v4.3.md`
- `CAS-0A-v4-FROZEN.docx` (or the repo equivalent) for:
  - Ω as edge-weight domain (canonical box)
  - extension-based derivative definitions (fixed extension choice)
  - locality definition in terms of F components depending on neighbourhoods N(e)

---

## New Code to Add

### 1) Toy quadratic potential implementation
Create:

- `src/nps/models/quadratic_toy.py`

Provide:

#### Dataclasses / types
- `QuadraticToySpec`
  - `m: int` (dimension = |E|)
  - `A: np.ndarray` (m×m)
  - `b: np.ndarray` (m,)
  - `c: float`
  - `domain_lower: float = 0.0`
  - `domain_upper: float = 1.0`
  - `extension_id: str = "toy_quadratic_v1"`

#### Functions / methods
- `value(w: np.ndarray, theta: float | None = None) -> float`
- `grad(w: np.ndarray, theta: float | None = None) -> np.ndarray`
- `hess(w: np.ndarray, theta: float | None = None) -> np.ndarray`

Rules:
- Treat θ as optional (toy default: ignore θ unless you later parameterise A,b).
- **Maximisation convention**: the toy should be concave on Ω° when we want an interior maximiser.
  - Achieve this by ensuring `A` is **negative definite** (e.g. `A = -Q` with Q SPD).
- Grad and Hess must be **exact**:
  - `grad = A @ w + b`
  - `hess = A`

Include helper constructor:
- `make_local_quadratic_toy(m: int, *, locality_radius: int, line_graph_neighbors: list[list[int]] | None = None, seed: int = 0) -> QuadraticToySpec`
  - Builds a sparse, symmetric, strictly diagonally dominant negative definite A consistent with a supplied neighbourhood structure, or a simple banded neighbourhood if none supplied.

---

### 2) Locality / neighbourhood utilities (Phase‑A compatible)
Create:

- `src/nps/math/locality.py`

Provide:
- `line_graph_neighbors_from_edge_incidence(edges: list[tuple[int,int]]) -> list[list[int]]`
- `k_hop_neighborhood(neighbors: list[list[int]], k: int) -> list[set[int]]`
- `sparsity_support(A: np.ndarray, tol: float = 0.0) -> list[set[int]]`

These are used for locality checks:
- locality by **sparsity inspection**: row support subset of N(e)
- optionally: locality by **perturbation witness**

---

### 3) Phase‑A checkers with witnesses
Create:

- `src/nps/validation/phase_a_foundations_checks.py`

Expose check functions that return **structured evidence**:

#### Common return shape
Each checker returns a dict:
- `check_id: str`
- `ok: bool`
- `margin: float | None`
- `witness: dict`
- `notes: str | None`

#### Required checkers
1. `check_domain_box(m: int, lower: float, upper: float) -> dict`
2. `check_grad_finite_difference(spec: QuadraticToySpec, w: np.ndarray, eps: float = 1e-6, tol: float = 1e-4) -> dict`
3. `check_hess_finite_difference(spec: QuadraticToySpec, w: np.ndarray, eps: float = 1e-5, tol: float = 1e-3) -> dict`
4. `check_locality_by_sparsity(A: np.ndarray, neighborhoods: list[set[int]], *, tol: float = 0.0) -> dict`
5. `check_stationarity(spec: QuadraticToySpec, w_star: np.ndarray, tol: float = 1e-8) -> dict`

#### Optional (nice-to-have) checker
6. `check_locality_by_perturbation(spec: QuadraticToySpec, neighborhoods: list[set[int]], rng_seed: int = 0, tol: float = 1e-8) -> dict`

**Check IDs:** prefix all check IDs with `CHK.A.` (e.g. `CHK.A.GRAD_FD`).

---

### 4) Wire checkers into Phase A CAS‑A generation
Update:

- `src/nps/phases/phase_a/build_casa.py`

Add CLI flag:
- `--toy-quadratic`

When enabled, Phase A must:
1. Build a toy spec with default `m=8` and `locality_radius=1`
2. Choose an interior test point `w_test = 0.5 * ones(m)`
3. Compute interior equilibrium candidate `w_star = -A^{-1} b`
   - If `w_star` is not in Ω° (0,1)^m, record `notes` and still run derivative/locality checks at `w_test`.
4. Build neighbourhood sets `N(i)` (from the toy’s own neighbours) and run the checkers.
5. Embed results into CAS‑A under:

```json
"checks": [
  { "check_id": "CHK.A....", "ok": true, "margin": 0.0, "witness": {...}, "notes": "..." }
]
```

Also record `extension_id` in CAS‑A (e.g. `derivative_definition.extension_id`) and in `trace`.

Do not change existing CAS‑A metadata / content hashing logic.

---

### 5) Phase A′ closure enforcement (light)
Update:

- `src/nps/phases/phase_a_prime/build_casa_prime.py`

Rule:
- If CAS‑A contains `checks`, require **all** `check_id` starting with `CHK.A.` to have `ok==true`, otherwise add a blocking issue and do not approve.

---

## Tests (required)
Add:

1. `tests/test_quadratic_toy_derivatives.py`
2. `tests/test_quadratic_toy_locality.py`
3. `tests/test_phase_a_with_toy_checks.py`
4. `tests/test_gates_on_with_toy.py`

Keep dimensions small so tests remain fast.

---

## Reporting
Write:

- `cascade_taskpack_structural_differentiation_v4.3/TASKS/task_phase_a_toy_quadratic_checks/REPORT.md`

Must include:
- files added/changed
- commands run
- brief excerpt of CAS‑A `checks`
- note that A′ blocks if checks fail

---

## Verification commands (must run)
- `pytest -q`
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`

Both must pass.

---

## Definition of Done
- Toy quadratic Φ exists with exact grad/hess and explicit `extension_id`
- Phase‑A checkers run and write audit‑grade witnesses into CAS‑A when `--toy-quadratic` is used
- Phase A′ enforces success of `CHK.A.*` checks when present
- Tests pass in default and CI-mode (gates on)
- Report written
