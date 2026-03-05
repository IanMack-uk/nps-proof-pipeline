# Phase Group B Task Pack (Option 2 style): Phase 0B → Phase B → Phase B′
**Command convention:** use `PYTHONPATH=src python -m ...` in all commands and reports.

---

## Objective
Implement the **operator formulation of equilibrium** and certify the **structural differentiation prerequisites** needed for later Ordering Theorem phases, while staying faithful to the governance rules already in place.

Phase Group B must:
1) Generate governed artefacts **CAS-0B**, **CAS-B**, and **CAS-Bp** into `cert_artifacts/<run_id>/`
2) Introduce a concrete, machine-checkable definition of the **equilibrium operator** (and its linearisation objects) that later phases will use.
3) Provide **auditable checkers** (witness-based) for the toy quadratic model so we can immediately validate:
   - operator correctness (matches ∇Φ)
   - Jacobian/Hessian structure (symmetry, sparsity/locality)
   - nondegeneracy/invertibility conditions (when asserted)
4) Ensure Phase B′ approval blocks if required checks fail (when present).

This task pack follows the same philosophy as Phase Group A:
- encode objects and obligations,
- run checkers,
- write artefacts with witnesses,
- gate closure on failures,
- remain phase-isolated.

---

## Inputs (authoritative)
Cascade must read and align with:
- `docs/Structural_Differentiation_Programme_v4.3.md` (Phase 0B/B/B′ sections)
- `CAS-0A-v4-FROZEN.docx` (for derivative conventions, locality framing, equilibrium maximisation convention)
- Repo policy + gates:
  - `docs/specs/import_policy.json`
  - runtime firewall / CAS gates / dependency gate (already implemented)
- Existing Phase A artefacts + code:
  - `src/nps/models/quadratic_toy.py`
  - `src/nps/validation/phase_a_foundations_checks.py`
  - `src/nps/phases/phase_0a/build_cas0a.py`
  - `src/nps/phases/phase_a/build_casa.py`
  - `src/nps/phases/phase_a_prime/build_casa_prime.py`

---

## Deliverables (must be produced)
In `cert_artifacts/<run_id>/`:
- `CAS-0B.json`
- `Phase0B_REPORT.md`
- `CAS-B.json`
- `PhaseB_REPORT.md`
- `CAS-Bp.json`
- `PhaseB_prime_REPORT.md`

Each CAS artefact must include the integrity metadata required by Task 10.4:
- `cas_id`, `created_at`, `inputs`, `content_hash`

And CAS chain ordering must satisfy the dependency gate:
- `CAS-0A → CAS-A → CAS-0B → CAS-B → CAS-Bp`

---

## What Phase Group B means in code (pragmatic, certification-ready)
Phase B introduces the **equilibrium operator** and its first linearisation objects in a way later phases can reference without ambiguity.

### Core objects to encode
1) **Equilibrium operator** (maximisation convention, interior regime):
- Define an operator `F(w, theta)` intended to represent the marginal field driving equilibrium.
- For Phase B (toy), take:
  - `F(w) := ∇Φ(w)`
  - (Optional later) add constraints / normal-cone KKT objects; for now focus on interior regime.

2) **Jacobian of operator**
- `J(w) := ∂F/∂w` (for toy, equals Hessian of Φ)
- For toy quadratic: `J(w) = A` constant.

3) **Locality structure**
- For each coordinate i, certify a neighbourhood `N(i)` such that `F_i` depends only on `w|_{N(i)}`.
- For toy quadratic, locality is equivalent to sparsity of A’s rows.

4) **Nondegeneracy / invertibility (conditional)**
- Later phases will need invertibility of `J(w*)` (implicit function style).
- For toy harness, we can check:
  - `det(J)` not near 0 or `min_singular_value` bounded away from 0
- But in B we must treat this as:
  - either an explicit **assumption** or a **checked** condition (for toy).

---

## Required new code

### 1) Operator module
Create:
- `src/nps/operators/equilibrium_operator.py`
and ensure package init exists:
- `src/nps/operators/__init__.py`

Expose:
- `def equilibrium_operator_from_potential(potential) -> callable`
  - Returns `F(w, theta=None)` callable consistent with the provided potential.
- `def jacobian_from_potential(potential) -> callable`
  - Returns `J(w, theta=None)` callable (for toy: constant A).
- `@dataclass OperatorSpec`
  - `name: str`
  - `definition: str` (short text)
  - `derivative_definition: dict` (must include `extension_id` when applicable)
  - `locality: dict | None` (neighbourhoods, radius if defined)

Notes:
- Keep the API minimal and dependency-free.
- Do not introduce forward-phase imports.

### 2) Phase B checkers (witness-based)
Create:
- `src/nps/validation/phase_b_operator_checks.py`

All checkers return dicts with fields:
- `check_id`, `ok`, `margin`, `witness`, `notes`

Required checkers (toy quadratic must pass):

#### B.1 Operator matches gradient
`CHK.B.OPERATOR_MATCHES_GRAD`
- Given potential Φ and operator F built from it:
  - sample interior points w in Ω°
  - verify `F(w) == grad(w)` within tolerance (should be exact for toy)

Witness:
- max abs diff, sample point

#### B.2 Jacobian matches Hessian
`CHK.B.JACOBIAN_MATCHES_HESS`
- verify `J(w)` matches `hess(w)` within tolerance
- for toy, constant equality

Witness:
- max abs diff, symmetry error

#### B.3 Symmetry of Jacobian (if required)
`CHK.B.JACOBIAN_SYMMETRY`
- verify `||J - J.T||_max ≤ tol`

Witness:
- symmetry_error

#### B.4 Locality / sparsity of Jacobian
`CHK.B.JACOBIAN_LOCALITY_SPARSITY`
- given neighbourhoods `N(i)` (from toy construction or from `sparsity_support`),
  verify support(J[i,:]) ⊆ N(i)

Witness:
- violating indices, max out-of-neighbour magnitude

#### B.5 Invertibility / conditioning at equilibrium (toy)
`CHK.B.JACOBIAN_INVERTIBLE_AT_WSTAR`
- at w* used in toy Phase A run (w0),
  verify `min_singular_value(J(w*)) ≥ eps`
  and record condition number estimate if feasible.

Witness:
- min_singular_value, cond_estimate

This is the computational counterpart to “nondegeneracy” prerequisites for IFT-style steps later.

### 3) Phase 0B/ B / B′ generators
Create modules with CLIs similar to Phase Group A:

#### Phase 0B
Create:
- `src/nps/phases/phase_0b/build_cas0b.py`
CLI:
- `PYTHONPATH=src python -m nps.phases.phase_0b.build_cas0b --run-id <optional> --input <path-to-CAS-A.json>`

Behaviour:
- Creates `CAS-0B.json` and `Phase0B_REPORT.md` in run_dir.
- `CAS-0B.inputs` must include upstream `cas_id` from CAS-A.
- Content should:
  - backward-extract Phase B targets from programme spec (as done in 0A)
  - enumerate dependencies required for Phase B operator formulation
  - declare obligations to be checked in Phase B (operator correctness, Jacobian structure, locality)

#### Phase B
Create:
- `src/nps/phases/phase_b/build_casb.py`
CLI:
- `PYTHONPATH=src python -m nps.phases.phase_b.build_casb --run-id <optional> --input <path-to-CAS-0B.json> --toy-quadratic`

Behaviour:
- Builds operator objects for the toy quadratic potential.
- Runs Phase B checkers and writes them into `CAS-B.json` under `checks`.
- Writes `PhaseB_REPORT.md` summarising results and key witness margins.
- Must record:
  - operator definition text
  - derivative extension_id
  - locality neighbourhood summary

#### Phase B′
Create:
- `src/nps/phases/phase_b_prime/build_casb_prime.py`
CLI:
- `PYTHONPATH=src python -m nps.phases.phase_b_prime.build_casb_prime --run-id <optional> --input <path-to-CAS-B.json>`

Behaviour:
- Produces `CAS-Bp.json` and `PhaseB_prime_REPORT.md`
- Approval rule:
  - If CAS-B has `checks`, then all `CHK.B.*` must be `ok==true` or B′ blocks (add blocking issues).

### 4) Ensure phase package init files exist
If missing, add `__init__.py` for new phase directories:
- `src/nps/phases/phase_0b/__init__.py`
- `src/nps/phases/phase_b/__init__.py`
- `src/nps/phases/phase_b_prime/__init__.py`

---

## CAS schema expectations (minimal)
For **CAS-0B**:
- `phase_targets`: list extracted from programme Phase B section (deliverables)
- `dependency_table`: list with `dep_id`, `type`, `source`, `provides`, `used_in`
- `assumptions.imported` vs `assumptions.introduced`
- `minimality_audit.drop_test` placeholder ok (recorded, not necessarily automated yet)

For **CAS-B**:
- Must include `checks` list with `CHK.B.*` results
- Must include `operator_spec` (or similar) describing F and J
- Must include `trace.generated_by` tool metadata

For **CAS-Bp**:
- Must record approval decision and any blocking issues
- Must include required metadata fields and correct `inputs` upstream

---

## Tests (required)
Add tests ensuring end-to-end behaviour and gate compatibility.

1) `tests/test_phase_0b_cas0b_generation.py`
- Run Phase A to produce CAS-A
- Run Phase 0B and assert CAS-0B exists and includes required keys + upstream input id

2) `tests/test_phase_b_operator_checks_toy.py`
- Construct toy quadratic potential
- Build operator + Jacobian and run checkers
- Assert all `CHK.B.*` pass

3) `tests/test_phase_group_b_end_to_end.py`
- Run Phase A (0A → A → A′) with toy checks
- Run Phase 0B → B (toy) → B′
- Assert all CAS artefacts created and B′ approves

4) `tests/test_gates_on_phase_group_b.py`
- Same as above but with:
  - `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1`
- Assert full success.

Keep m small (8) so tests remain fast.

---

## Reporting (required)
Write a task report:
- `cascade_taskpack_structural_differentiation_v4.3/TASKS/task_phase_group_b/REPORT.md`

Include:
- files added/changed
- commands run (with PYTHONPATH=src)
- sample excerpts from CAS-B checks (at least 2)
- note about what is *checked* vs what remains an assumption for later phases

---

## Verification commands (must run)
1) Default:
```bash
pytest -q
```

2) Gates on:
```bash
NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q
```

Both must pass.

---

## Definition of Done
Phase Group B is complete when:
- CAS-0B / CAS-B / CAS-Bp are generated into `cert_artifacts/<run_id>/`
- `CAS-B.json` contains passing `CHK.B.*` checks for toy quadratic mode
- B′ blocks if any `CHK.B.*` fails (when checks present)
- end-to-end tests pass in default and gates-on modes
- report written and reproducible (PYTHONPATH=src commands)
