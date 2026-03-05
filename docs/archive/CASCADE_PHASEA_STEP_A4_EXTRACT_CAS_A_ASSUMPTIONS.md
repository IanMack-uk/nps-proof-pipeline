# CASCADE PHASE A (STEP A4) --- EXTRACT AND FORMALISE CAS-A ASSUMPTIONS

Project: `nps-proof-pipeline`

Context: - CAS-0A is certified and frozen. - Phase A theorem is
registered as CONJECTURE. - StructuralExposure exists as a provisional
object with validation harness. - Notation is frozen (SymbolDictionary
versioned). - CAS-A assumption ledger scaffold exists but is not yet
populated.

This step completes **Phase A task (3)** from the programme document:

> Extract and label assumptions (scope-tagged for later phases).

The goal is to build a formally explicit, minimal, auditable **Certified
Assumption Set CAS-A (draft)**.

------------------------------------------------------------------------

## 🎯 Objective

1.  Enumerate all Phase A deliverables currently in the system.
2.  Identify every assumption implicitly required for them to be
    well-posed.
3.  Convert those assumptions into explicit `AssumptionRecord`s in the
    ValidationRegistry.
4.  Scope-tag each assumption.
5.  Implement a CAS-A drop test to confirm minimality.
6.  Update `docs/specs/cas_a_assumption_ledger.md` to reflect the
    extracted assumptions.

No structural coordinates are introduced in this step.

------------------------------------------------------------------------

## 0️⃣ Files to Modify / Add

### Modify:

-   `src/nps/phases/phase_a/seed_exposure_validation.py`
-   `docs/specs/cas_a_assumption_ledger.md`

### Add:

    src/nps/phases/phase_a/
      seed_cas_a_assumptions.py

    tests/phase_a/
      test_cas_a_minimality.py

Do NOT modify CAS-0A. Do NOT promote any assumption to CERTIFIED yet.
All CAS-A assumptions remain PROVISIONAL.

------------------------------------------------------------------------

## 1️⃣ Enumerate Phase A Deliverables

Deliverables currently active:

1.  THM.SDOT.v4 (CONJECTURE)
2.  StructuralExposure object
3.  EXP.w_e control candidate
4.  EXP.absF control candidate
5.  Exposure locality validation harness
6.  SymbolDictionary freeze invariants

For each deliverable, determine required properties.

------------------------------------------------------------------------

## 2️⃣ Extract Required Assumptions

Create `seed_cas_a_assumptions.py`.

Implement:

``` python
from nps.validation.validation_registry import ValidationRegistry
from nps.validation.records import AssumptionRecord, ScopeTag
from nps.validation.status import CertificationStatus

def seed_cas_a_assumptions(registry: ValidationRegistry) -> None:
    """Register Phase A provisional assumptions (CAS-A draft)."""
```

Register the following assumptions (all PROVISIONAL):

------------------------------------------------------------------------

### A. CAS-A.EXP.LOCALITY

Text: "Structural exposure E_e(w,θ) depends only on local data (N(e))
when declared local."

Scope: FOUNDATIONS

Required for: - Exposure validation harness - Later Phase B locality
arguments

------------------------------------------------------------------------

### B. CAS-A.EXP.WELLPOSED

Text: "Structural exposure is well-defined and finite for all w ∈ Ω."

Scope: FOUNDATIONS

Required for: - Theorem well-posedness - Exposure vector evaluation

------------------------------------------------------------------------

### C. CAS-A.EXP.REGULARITY

Text: "Structural exposure inherits at least C⁰ regularity from its
defining objects."

Scope: DIFFERENTIABILITY

Required for: - Later equilibrium response arguments

------------------------------------------------------------------------

### D. CAS-A.NOTATION.STABILITY

Text: "Phase A symbol dictionary remains fixed (versioned freeze) for
all subsequent reasoning."

Scope: FOUNDATIONS

Required for: - Logical coherence of CAS-A

------------------------------------------------------------------------

No structural-coordinate assumptions yet.

------------------------------------------------------------------------

## 3️⃣ Update CAS-A Ledger Documentation

Update `docs/specs/cas_a_assumption_ledger.md`:

Populate assumption table with:

  ID   Text   Scope   Status   Evidence
  ---- ------ ------- -------- ----------

All entries status = PROVISIONAL.

Include note:

"CAS-A draft: no assumption certified yet; minimality and closure
pending Phase Aʹ."

Keep deterministic formatting.

------------------------------------------------------------------------

## 4️⃣ CAS-A Minimality Drop Test

Create:

`tests/phase_a/test_cas_a_minimality.py`

Test logic:

1.  Create ValidationRegistry.
2.  Seed CAS-A assumptions.
3.  Remove one assumption at a time (or simulate removal by not
    seeding).
4.  Assert that at least one Phase A deliverable fails:
    -   Exposure locality check fails without CAS-A.EXP.LOCALITY.
    -   Exposure vector evaluation fails without CAS-A.EXP.WELLPOSED.
    -   etc.

If removal does not cause failure, assumption is unnecessary → test must
fail.

Keep logic minimal but meaningful.

------------------------------------------------------------------------

## 5️⃣ Verification

Run:

    pytest
    mypy src
    ruff check .

All must pass.

------------------------------------------------------------------------

## 🚫 Non-Goals

Do NOT:

-   Introduce structural coordinates
-   Modify theorem status
-   Promote any assumption to CERTIFIED
-   Change CAS-0A
-   Add non-deterministic behaviour

------------------------------------------------------------------------

## ✅ Completion Condition

-   CAS-A assumptions explicitly seeded
-   CAS-A ledger populated
-   Drop test enforces minimality
-   All tests pass
-   System now has explicit CAS-A draft layer

At this point Phase A task (3) is complete.
