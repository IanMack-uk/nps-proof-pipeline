# CASCADE PHASE A (STEP A3) --- STRUCTURAL EXPOSURE (PROVISIONAL OBJECT + VALIDATION HARNESS)

Project: `nps-proof-pipeline`

Context: - CAS-0A is certified and frozen. - Phase A0 validation layer
exists (ValidationRegistry, evidence, promotion). - Phase A1 theorem is
registered as CONJECTURE. - Phase A2 notation is frozen
(SymbolDictionary freeze + deterministic snapshot). - Paper 0/1/2
mathematics is NOT trusted; structural exposure must be introduced as
**provisional** and validated via tests.

This step builds the *framework* to define and test candidate structural
exposure formulas, starting with a baseline exposure to validate the
harness.

------------------------------------------------------------------------

## 🎯 Objective

1.  Define `StructuralExposure` as a strictly typed Phase A object
    (domain/codomain/regularity/locality required).
2.  Add a plugin interface so multiple candidate exposure definitions
    can be tested without rewriting infrastructure.
3.  Implement **two** candidate exposures:
    -   A trivial baseline (control): `E_e(w) := w_e` (should satisfy
        strict locality)
    -   A gradient-based baseline (control): `E_e(w,θ) := |F_e(w,θ)|`
        (locality depends on F locality)
4.  Add a validation harness with tests:
    -   well-posedness (shape, finiteness)
    -   locality invariance (positive control for `w_e` baseline)
    -   a negative control that fails when exposure depends on non-local
        coordinates
5.  Record evidence into ValidationRegistry for exposure properties (as
    PROVISIONAL evidence links).

No attempt to import Paper 0 exposure formula yet.

------------------------------------------------------------------------

## 0️⃣ Files / Folders to Add

Create:

    src/nps/phases/phase_a/
      exposure/
        __init__.py
        exposure_types.py
        exposure_candidates.py
        exposure_validation.py
      seed_exposure_validation.py

    tests/phase_a/
      test_structural_exposure_validation.py

    docs/specs/
      cas_a_structural_exposure.md

Do NOT modify CAS-0A registry or any frozen CAS-0A artifacts.

------------------------------------------------------------------------

## 1️⃣ Exposure Types (Strict typing + plugin interface)

File: `src/nps/phases/phase_a/exposure/exposure_types.py`

Implement:

### 1.1 Regularity / Locality metadata (string enums are OK)

Provide small enums or literal types for:

-   RegularityClass: e.g., "C0", "C1", "C2", "UNKNOWN"
-   LocalityScope: e.g., "EDGE_ONLY", "NEIGHBORHOOD_N(e)", "UNKNOWN"

### 1.2 ExposureDefinition protocol

Define a Protocol:

``` python
from __future__ import annotations
from typing import Protocol
import numpy as np

class ExposureDefinition(Protocol):
    def evaluate(self, e: int, w: np.ndarray, theta: float) -> float:
        ...
```

(Use e as int index for sandbox models; later can become Edge id
object.)

### 1.3 StructuralExposure dataclass

Fields:

-   `name: str`
-   `definition: ExposureDefinition`
-   `domain: str` (e.g., "Omega")
-   `codomain: str` (e.g., "R")
-   `regularity: str`
-   `locality: str`
-   `requires_properties: set[PropertyKey]` (CAS-0A prerequisites; may
    be empty for w_e baseline)
-   `notes: str`

Also include:

``` python
def evaluate_vector(self, w: np.ndarray, theta: float, m: int) -> np.ndarray:
    """Return exposure vector in R^m for edges 0..m-1."""
```

This must raise MathematicalInconsistency on shape mismatch / non-finite
outputs.

Use `nps.core.exceptions.MathematicalInconsistency`.

------------------------------------------------------------------------

## 2️⃣ Candidate Exposures

File: `src/nps/phases/phase_a/exposure/exposure_candidates.py`

Implement two candidates:

### 2.1 Coordinate baseline: E_e(w) = w_e

-   Requires no CAS-0A properties.
-   Locality: EDGE_ONLY.
-   Regularity: C∞ (or "SMOOTH" if you use a fixed set; otherwise
    "UNKNOWN" is fine but prefer "C1+" to make tests meaningful).

### 2.2 Gradient magnitude baseline: E_e(w,θ) = abs(F_e(w,θ))

This requires access to a sandbox model that can compute F(w,θ). Use the
existing toy model API (whatever exists under `src/nps/models/...`).

If your model API differs, adapt accordingly, but keep the candidate
simple.

Requires properties: - F defined as grad w Phi
(PropertyKey("F","defined_as_grad_w\_Phi")) - Locality assumptions
(PropertyKey("Locality","defined_neighborhood_N(e)") and
("Locality","uniform_radius_r"))

Locality: NEIGHBORHOOD_N(e)

------------------------------------------------------------------------

## 3️⃣ Exposure Validation Utilities

File: `src/nps/phases/phase_a/exposure/exposure_validation.py`

Implement helpers:

-   `assert_finite_vector(x: np.ndarray) -> None`
-   `check_edge_only_locality(exposure: StructuralExposure, w: np.ndarray, theta: float, e: int) -> None`
    -   Perturb only non-e coordinates and ensure exposure for edge e
        unchanged (within tolerance).
-   `check_neighborhood_locality(exposure, w, theta, e, neighborhood: set[int])`
    -   Perturb outside neighborhood, assert unchanged.

Include tolerance constants (e.g., 1e-8) and make deterministic using
fixed RNG seed.

------------------------------------------------------------------------

## 4️⃣ Seed Exposure Validation Evidence

File: `src/nps/phases/phase_a/seed_exposure_validation.py`

Implement:

``` python
from nps.validation.validation_registry import ValidationRegistry
from nps.validation.records import AssumptionRecord, ScopeTag
from nps.validation.status import CertificationStatus
from nps.validation.evidence import Evidence

def seed_structural_exposure_ledger(registry: ValidationRegistry) -> None:
    """Register provisional CAS-A ledger entries for Structural Exposure tests."""
```

Register at least one assumption record representing the *property you
intend to certify later*, e.g.:

-   id: "CAS-A.EXP.LOCALITY"
-   text: "Structural exposure E_e depends only on local data (N(e))."
-   scope: FOUNDATIONS
-   status: PROVISIONAL
-   sources: \[\] (or Paper0 placeholder SourceRef is allowed but not
    authoritative)
-   requires: set() or include locality properties if you want
-   evidence: \[\]

Then tests can add evidence to this assumption by calling
`add_evidence_to_assumption`.

------------------------------------------------------------------------

## 5️⃣ Documentation: Structural Exposure Spec (Draft)

Create `docs/specs/cas_a_structural_exposure.md` with:

-   Status: DRAFT / PROVISIONAL
-   Definition interface: ExposureDefinition + StructuralExposure
    wrapper
-   List current candidates:
    -   EXP.w_e (control)
    -   EXP.absF (control)
-   List validation checks performed (edge-locality,
    neighborhood-locality, well-posedness)
-   State explicitly: "No Paper 0 exposure formula imported yet."

Keep it short and auditable.

------------------------------------------------------------------------

## 6️⃣ Tests

File: `tests/phase_a/test_structural_exposure_validation.py`

Tests required:

### 6.1 Well-posedness: vector evaluation returns finite values

-   Construct small w (e.g., m=5 random vector).
-   Evaluate vector for EXP.w_e and confirm shape (m,) and finite.

### 6.2 Positive locality control: EXP.w_e is EDGE_ONLY local

-   For random w, theta, choose edge e
-   Perturb all coordinates except e
-   Assert exposure value for e unchanged (exact or within tolerance)

### 6.3 Negative control: a deliberately non-local exposure fails EDGE_ONLY check

Implement a small local-only test exposure inside the test file: -
E_e(w) = sum(w) (clearly global) Run `check_edge_only_locality` and
assert it raises MathematicalInconsistency.

### 6.4 Evidence logging into ValidationRegistry

-   Create registry
-   call `seed_structural_exposure_ledger(registry)`
-   Add Evidence pointing to passing test for EXP.w_e locality
-   Assert registry stores the evidence under "CAS-A.EXP.LOCALITY"

Do not promote anything to CERTIFIED yet.

------------------------------------------------------------------------

## 7️⃣ Verification

Run:

    pytest
    mypy src
    ruff check .

All must pass.

------------------------------------------------------------------------

## 🚫 Non-Goals

Do NOT: - implement Paper 0 structural exposure formula - mark any
exposure assumptions CERTIFIED - modify theorem conjecture status -
change CAS-0A registry - introduce nondeterministic tests (no
timestamps, no network)

------------------------------------------------------------------------

## ✅ Completion Condition

-   StructuralExposure types + plugin interface exists
-   Two control candidates exist (w_e and abs(F_e))
-   Validation utilities exist with locality checks
-   Provisional ledger entries seeded in ValidationRegistry
-   Tests pass including positive and negative controls + evidence
    logging
-   Docs spec exists and clearly states provisional status
