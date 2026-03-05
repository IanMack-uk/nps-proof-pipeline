# CASCADE PHASE A (STEP A5) --- STRUCTURAL COORDINATES + PHASE B INTERFACE CONTRACT (PROVISIONAL)

Project: `nps-proof-pipeline`

Context: - CAS-0A certified and frozen. - Phase A theorem registered as
CONJECTURE. - StructuralExposure provisional + validated controls. -
CAS-A draft assumptions explicitly extracted (PROVISIONAL). - Notation
frozen and versioned. - No Paper 0 structural coordinates imported yet.

This step completes **Phase A task (4)**:

> Extract structural coordinates and neighbourhood conventions (from
> Paper 0) and record the interface contract to Phase B.

Because Paper 0 is not trusted, coordinates and contract are introduced
as **provisional testable objects**, starting with control
implementations.

------------------------------------------------------------------------

## 🎯 Objective

1.  Define strictly typed StructuralCoordinate objects.
2.  Add plugin interface for candidate coordinate definitions.
3.  Implement control coordinate candidates.
4.  Define and implement a Phase-B interface contract checker.
5.  Add positive and negative contract controls.
6.  Seed provisional CAS-A assumptions for coordinates + contract.
7.  Add validation tests and evidence logging.

No theorem promotion. No structural differentiation proof yet.

------------------------------------------------------------------------

## 0️⃣ Files / Folders to Add

Create:

    src/nps/phases/phase_a/coordinates/
      __init__.py
      coordinate_types.py
      coordinate_candidates.py
      coordinate_validation.py

    src/nps/phases/phase_a/
      seed_coordinate_validation.py

    tests/phase_a/
      test_structural_coordinates_validation.py

    docs/specs/
      cas_a_structural_coordinates.md

Do NOT modify CAS-0A.

------------------------------------------------------------------------

## 1️⃣ Coordinate Types (Strict Typing + Plugin Interface)

File: `coordinate_types.py`

### 1.1 CoordinateDefinition Protocol

``` python
class CoordinateDefinition(Protocol):
    def evaluate(self, e: int, w: np.ndarray) -> float:
        ...
```

### 1.2 StructuralCoordinate Dataclass

Fields:

-   name: str
-   definition: CoordinateDefinition
-   domain: str ("Omega")
-   codomain: str ("R")
-   locality: str ("EDGE_ONLY", "NEIGHBORHOOD_N(e)", etc.)
-   notes: str

Include:

``` python
def evaluate_vector(self, w: np.ndarray, m: int) -> np.ndarray:
```

Must: - return shape (m,) - raise MathematicalInconsistency on
non-finite output

------------------------------------------------------------------------

## 2️⃣ Control Coordinate Candidates

File: `coordinate_candidates.py`

Implement:

### 2.1 S_e control: S_e(w) := w_e

Locality: EDGE_ONLY

### 2.2 R_e control: R_e(w) := 0

Locality: EDGE_ONLY

### 2.3 Negative control coordinate (for testing only):

R_e(w) := sum(w) (global dependence)

------------------------------------------------------------------------

## 3️⃣ Phase B Interface Contract Checker

File: `coordinate_validation.py`

Define contract:

> F_e(w,θ) depends only on (w_e, S_e(w), R_e(w), θ)

Implement function:

``` python
def check_phase_b_contract(
    grad_phi_fn: Callable[[np.ndarray, float], np.ndarray],
    S: StructuralCoordinate,
    R: StructuralCoordinate,
    w: np.ndarray,
    theta: float,
    e: int,
    neighborhood: set[int],
) -> None:
```

Logic:

1.  Compute baseline values:

    -   w_e
    -   S_e(w)
    -   R_e(w)
    -   F_e(w,θ)

2.  Perturb coordinates outside declared locality (and optionally
    outside neighborhood).

3.  If perturbation preserves:

    -   w_e
    -   S_e
    -   R_e

    but changes F_e, then contract violated → raise
    MathematicalInconsistency.

Include deterministic perturbation (fixed RNG seed).

------------------------------------------------------------------------

## 4️⃣ Seed CAS-A Coordinate Assumptions

File: `seed_coordinate_validation.py`

Register provisional assumptions:

### A. CAS-A.COORD.LOCALITY

"Structural coordinates depend only on declared local data."

Scope: FOUNDATIONS Status: PROVISIONAL

### B. CAS-A.CONTRACT.F_DEPENDENCE

"Marginal field component F_e depends only on (w_e, S_e(w), R_e(w), θ)."

Scope: PHASE_B\_INTERFACE Status: PROVISIONAL

Do not promote.

------------------------------------------------------------------------

## 5️⃣ Documentation

Create `docs/specs/cas_a_structural_coordinates.md`

Include:

-   Status: PROVISIONAL
-   Definition interface for coordinates
-   Current control candidates
-   Statement of Phase B interface contract
-   Note: No Paper 0 coordinate definitions imported yet
-   Validation checks performed
-   Link to CAS-A assumptions IDs

Keep deterministic formatting.

------------------------------------------------------------------------

## 6️⃣ Tests

File: `test_structural_coordinates_validation.py`

### 6.1 Well-posedness

-   S and R vector evaluation shape + finiteness

### 6.2 Positive contract control

Use toy grad_phi and control S_e = w_e, R_e = 0 For typical quadratic
potential toy model, contract should hold

### 6.3 Negative contract control

Use R_e = sum(w) Check that contract violation is detected

### 6.4 Evidence logging

-   Create ValidationRegistry
-   Seed coordinate assumptions
-   Log Evidence for passing positive control under
    CAS-A.CONTRACT.F_DEPENDENCE
-   Assert stored

------------------------------------------------------------------------

## 7️⃣ Verification

Run:

    pytest
    mypy src
    ruff check .

All must pass.

------------------------------------------------------------------------

## 🚫 Non-Goals

Do NOT:

-   Import Paper 0 coordinate formulas
-   Promote assumptions to CERTIFIED
-   Modify theorem status
-   Modify CAS-0A
-   Introduce nondeterministic tests

------------------------------------------------------------------------

## ✅ Completion Condition

-   StructuralCoordinate interface exists
-   Control S and R coordinates implemented
-   Phase-B contract checker implemented
-   Positive + negative controls pass/fail correctly
-   CAS-A coordinate assumptions seeded (PROVISIONAL)
-   Documentation updated
-   All tests pass

At this point Phase A tasks (1)-(5) are structurally complete (draft
state).

Phase Aʹ (closure + stronger minimality + consistency audit) becomes the
next step.
