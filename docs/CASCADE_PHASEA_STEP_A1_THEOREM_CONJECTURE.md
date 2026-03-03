# CASCADE PHASE A (STEP A1) --- STRUCTURAL DIFFERENTIATION THEOREM AS CONJECTURE

Project: `nps-proof-pipeline`

Context: - CAS-0A is certified and frozen. - Phase A0 validation layer
exists. - Paper 0/1/2 mathematics is NOT trusted. - Therefore, the
Structural Differentiation / Ordering Theorem must enter the system as a
**CONJECTURE**, not as a certified theorem.

This step creates a precise, fully quantified theorem statement object
and registers it in the Phase A ValidationRegistry with status =
CONJECTURE.

------------------------------------------------------------------------

## 🎯 Objective

1.  Create a precise statement of the Structural Differentiation /
    Ordering Theorem (as a conjecture).
2.  Encode it as a `StatementRecord`.
3.  Register it in a Phase A validation seed function.
4.  Add tests ensuring:
    -   It is well-formed.
    -   Dependencies exist.
    -   It cannot be required as VALIDATED yet.

No mathematics is assumed correct in this step.

------------------------------------------------------------------------

## 0️⃣ Files to Add

Create:

    docs/specs/
      phase_a_structural_differentiation_conjecture.md

    src/nps/phases/phase_a/
      seed_conjectures.py

    tests/phase_a/
      __init__.py
      test_structural_differentiation_conjecture.py

------------------------------------------------------------------------

## 1️⃣ Write the Theorem Conjecture Document

File: `docs/specs/phase_a_structural_differentiation_conjecture.md`

Requirements:

-   Use precise quantifiers.

-   Explicitly reference objects: Ω, Φ, F, W\*(θ).

-   State equilibrium notion exactly as defined in CAS-0A.

-   Leave structural exposure and coordinates as named but not yet
    defined symbols (e.g., E_e(w), S_e(w), R_e(w)).

-   Mark clearly at top:

    Status: CONJECTURE (Phase A)

Example skeleton (do not claim proof):

  ------------------------------------------------------------
  \# Structural Differentiation / Ordering Theorem
  (Conjecture)

  Status: CONJECTURE (Phase A)

  Let: - G be a finite graph with edge set E. - Ω ⊂ ℝ\^\|E\|
  be admissible and compact (CAS-0A). - Φ: Ω × Θ → ℝ satisfy
  CAS-0A assumptions. - F(w,θ) = ∇\_w Φ(w,θ) (Definition
  4.1). - W\*(θ) = argmax\_{w∈Ω} Φ(w,θ).

  Conjecture: For each θ ∈ Θ and each equilibrium w\* ∈ W*(θ),
  there exist structural quantities (to be defined): -
  Structural exposure E_e(w*) - Separation coordinate
  S_e(w*) - Redundancy coordinate R_e(w*) such that the
  marginal field component F_e(w\*,θ) admits a representation
  of the form:

  F_e(w*,θ) = H_e(w*\_e, S_e(w*), R_e(w*), θ)

  for some function H_e depending only on local data.

  No claim of proof is made at this stage.
  ------------------------------------------------------------

Do not embellish beyond that.

------------------------------------------------------------------------

## 2️⃣ Seed Conjecture Registration

File: `src/nps/phases/phase_a/seed_conjectures.py`

Implement:

``` python
from nps.validation.validation_registry import ValidationRegistry
from nps.validation.records import StatementRecord
from nps.validation.status import StatementStatus
from nps.core.citations import cas0a  # if available
from nps.certification.dependency_registry import PropertyKey

def seed_phase_a_conjectures(registry: ValidationRegistry) -> None:
    """Register Phase A conjectures (draft layer)."""

    stmt = StatementRecord(
        id="THM.SDOT.v4",
        statement="See docs/specs/phase_a_structural_differentiation_conjecture.md",
        status=StatementStatus.CONJECTURE,
        sources=[],
        requires={
            PropertyKey(subject="Omega", property="compact"),
            PropertyKey(subject="Phi", property="continuous"),
            PropertyKey(subject="F", property="defined_as_grad_w_Phi"),
            PropertyKey(subject="W_star", property="defined_as_argmax_over_Omega"),
        },
        depends_on_assumptions=set(),
        evidence=[],
    )

    registry.register_statement(stmt)
```

No promotion here. No validation yet.

------------------------------------------------------------------------

## 3️⃣ Tests

File: `tests/phase_a/test_structural_differentiation_conjecture.py`

Tests must:

1.  Create a ValidationRegistry.
2.  Call `seed_phase_a_conjectures(registry)`.
3.  Confirm:
    -   Statement id "THM.SDOT.v4" exists.
    -   Status is CONJECTURE.
4.  Confirm that:

``` python
registry.require_statement_validated("THM.SDOT.v4")
```

raises `MathematicalInconsistency`.

This ensures the theorem cannot be used as validated yet.

------------------------------------------------------------------------

## 4️⃣ Verification

All must pass:

    pytest
    mypy src
    ruff check .

------------------------------------------------------------------------

## 🚫 Non-Goals

Do NOT:

-   Define structural exposure yet.
-   Define S_e or R_e yet.
-   Add assumptions to CAS-A ledger.
-   Mark theorem as VALIDATED.
-   Modify CAS-0A registry.

------------------------------------------------------------------------

## ✅ Completion Condition

-   Conjecture doc exists and is precise.
-   StatementRecord registered with status CONJECTURE.
-   Tests confirm it cannot be required as VALIDATED.
-   All checks pass.

This completes Phase A Step A1.
