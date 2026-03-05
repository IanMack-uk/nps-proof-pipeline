# CASCADE PHASE A (STEP A8) --- NONNEGATIVE Ω POLICY (CERTIFIED PIPELINE) + SIGNED ADVERSARIAL SUITE

Project: `nps-proof-pipeline`

Decision (locked): - **Certified / proof-target pipeline:** enforce **w
≥ 0** on Ω (nonnegative weights). - **Adversarial suite:** allow signed
weights only for falsification/stress tests (not for promotion).

This step operationalizes that decision in code, docs, and tests without
weakening frozen CAS-0A.

------------------------------------------------------------------------

## 🎯 Objectives

1.  Introduce an explicit **CAS-A domain policy assumption** for
    nonnegativity (PROVISIONAL).
2.  Enforce nonnegativity in the **sandbox model class** used by
    proof-target tests.
3.  Add a parallel **signed adversarial model class** used only by
    red-team tests.
4.  Ensure validators and candidates behave predictably under both
    regimes.
5.  Keep everything deterministic and strictly typed.

------------------------------------------------------------------------

## 0️⃣ Files to Modify / Add

### Modify

-   `docs/specs/cas_a_assumption_ledger.md`
-   `src/nps/models/sandbox/domain.py` *(or the current module that
    defines Ω / projection / sampling --- adjust to actual path)*
-   `tests/models/*` where Ω is sampled/constructed (minimal surgical
    edits)

### Add

    src/nps/models/sandbox/
      domain_policies.py

    tests/adversarial/
      __init__.py
      test_signed_weights_redteam.py

    docs/specs/
      cas_a_domain_policy.md

Do **NOT** modify CAS-0A, registry.freeze behavior, or any certified
property keys.

------------------------------------------------------------------------

## 1️⃣ Add CAS-A Assumption: Nonnegative Weights Policy

### 1.1 Seed assumption

Create: `src/nps/phases/phase_a/seed_domain_policy_assumptions.py`

Register PROVISIONAL assumption:

-   ID: `CAS-A.OMEGA.NONNEGATIVE`
-   Scope: `FOUNDATIONS`
-   Text: "For the proof-target model class, Ω ⊂ R\^m\_{≥0} (weights are
    componentwise nonnegative)."
-   Rationale: aligns monotonicity + ordering semantics with programme
    goal.

Add minimal evidence hook usage (do not promote).

### 1.2 Update ledger

Append row in `docs/specs/cas_a_assumption_ledger.md` deterministically.

Also create `docs/specs/cas_a_domain_policy.md` describing: -
proof-target Ω policy (nonnegative) - adversarial Ω policy (signed) -
what each is allowed to influence (promotion rules)

------------------------------------------------------------------------

## 2️⃣ Implement DomainPolicy Abstraction (Sandbox)

Create `src/nps/models/sandbox/domain_policies.py`:

-   `DomainPolicy` protocol:
    -   `project(w: np.ndarray) -> np.ndarray`
    -   `sample(m: int, rng: np.random.Generator) -> np.ndarray`
    -   `is_admissible(w: np.ndarray) -> bool`

Implement two policies:

### 2.1 NonnegativePolicy (proof-target)

-   `project`: clip below at 0 (and any existing Ω bounds you already
    enforce)
-   `sample`: samples in \[0, 1\] (or existing bounds) deterministically
    via rng
-   `is_admissible`: all components ≥ 0 (plus existing bounds)

### 2.2 SignedPolicy (adversarial)

-   `project`: identity (or existing bounds, symmetric)
-   `sample`: samples in \[-1, 1\]
-   `is_admissible`: always true (or symmetric bounds)

Do not change existing math; just route Ω behavior through a policy.

------------------------------------------------------------------------

## 3️⃣ Wire Proof-Target Sandbox to NonnegativePolicy

Update the sandbox Ω construction so that **all existing models tests**
continue to use: - `NonnegativePolicy` by default.

This is a minimal surgical change: - one default policy injection
point - no change to existing test expectations beyond sampling ranges.

------------------------------------------------------------------------

## 4️⃣ Add Signed "Red Team" Tests (No Promotion)

Create `tests/adversarial/test_signed_weights_redteam.py`:

### 4.1 Purpose

These tests are allowed to fail assumptions; they should never be used
to promote CAS-A.

### 4.2 Contents

-   Construct a signed Ω sample using `SignedPolicy`.
-   Run the Paper 0 coordinate validators and contract checks on signed
    samples.
-   Expected outcomes:
    -   locality should still hold (pure dependency claim)
    -   monotonicity may fail or become ambiguous → if it fails, log
        evidence/counterexample but **do not fail the test suite**
        unless you want strict red-team gating.

Recommendation: - Make these tests **pass by asserting behavior is
recorded**, not that monotonicity holds.

Example assertions: - If monotonicity validator raises, catch it and
append a deterministic entry to `docs/reports/signed_redteam_log.md`. -
Assert the log entry count increases deterministically.

------------------------------------------------------------------------

## 5️⃣ Update Exposure/Coordinate Candidates (Minimal)

No changes required to existing candidates unless they explicitly rely
on negative handling. However: - Ensure Paper 0 redundancy/separation
candidates document that they are intended for **nonnegative Ω**. - If
they include positive-part transforms, keep them but note: "harmless
under w≥0; relevant only for signed red-team."

Add a short note to: `docs/specs/cas_a_paper0_coordinate_import.md`
(doc-only): "Validated under NonnegativePolicy; signed regime is
red-team."

------------------------------------------------------------------------

## 6️⃣ Verification

Run: - `pytest` - `mypy src` - `ruff check .`

All must pass.

------------------------------------------------------------------------

## ✅ Completion Condition

-   Proof-target sandbox enforces w ≥ 0 by default.
-   CAS-A includes a PROVISIONAL domain-policy assumption
    `CAS-A.OMEGA.NONNEGATIVE`.
-   Signed weights exist only in `tests/adversarial/` and/or explicitly
    marked red-team.
-   Docs clearly separate certified vs adversarial regimes.
-   All checks pass.
