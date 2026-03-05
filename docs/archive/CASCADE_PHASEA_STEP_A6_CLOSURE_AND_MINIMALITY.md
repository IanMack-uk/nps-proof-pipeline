# CASCADE PHASE Aʹ (STEP A6) --- CLOSURE, COHERENCE, AND STRONG MINIMALITY

Project: `nps-proof-pipeline`

Context: - CAS-0A certified and frozen. - Phase A tasks (1)--(5)
structurally complete (draft). - CAS-A assumptions extracted and
PROVISIONAL. - StructuralExposure + StructuralCoordinates + Phase-B
contract exist. - Validation harnesses + evidence logging in place. -
All tests currently passing.

This step executes **Phase Aʹ --- Assumption Closure** from the
programme document:

> Verify definition consistency and notation coherence. Prove auxiliary
> lemmas required for Phase B. Re-run minimality (strong form).

The goal is to complete Phase A rigorously before any promotion or Phase
B work.

------------------------------------------------------------------------

## 🎯 Objectives

1.  Run a coherence audit across all Phase A objects.
2.  Upgrade minimality testing from structural-ID tests to semantic
    blocking tests.
3.  Ensure all validators explicitly depend on CAS-A assumptions.
4.  Produce a deterministic Phase A closure report.
5.  Optionally promote strictly non-mathematical governance assumptions.

No theorem validation. No Paper 0 imports.

------------------------------------------------------------------------

# 1️⃣ Coherence Audit (Definitions + Notation)

## 1.1 Add closure audit module

Create:

src/nps/phases/phase_a/closure_audit.py

Implement a function:

def run_phase_a\_coherence_audit(symbols, registry) -\> None:

It must verify:

-   All theorem symbols exist in frozen dictionary.
-   All Phase A objects declare domain, codomain, locality, and
    regularity metadata.
-   All referenced CAS-A assumptions exist in the registry.
-   Phase-B contract checker references CAS-A.CONTRACT.F_DEPENDENCE.

Raise MathematicalInconsistency on failure.

Deterministic. No file writes.

------------------------------------------------------------------------

# 2️⃣ Strong Minimality Enforcement

Current drop tests only confirm ID presence.

We now require semantic blocking.

## 2.1 Modify validators to require assumptions

In:

-   exposure_validation.py
-   coordinate_validation.py

Before performing checks, call:

registry.require_assumption_present("CAS-A.EXP.LOCALITY")

Similarly:

-   Exposure evaluation requires CAS-A.EXP.WELLPOSED
-   Contract checker requires CAS-A.CONTRACT.F_DEPENDENCE

If assumption absent → MathematicalInconsistency.

------------------------------------------------------------------------

## 2.2 Upgrade Minimality Test

Create:

tests/phase_a/test_phase_a\_strong_minimality.py

Test logic:

1.  Seed full CAS-A assumption set.
2.  Remove one assumption.
3.  Attempt to run its dependent validation check.
4.  Assert MathematicalInconsistency is raised.

Examples:

-   Remove CAS-A.EXP.LOCALITY → check_edge_only_locality must fail.
-   Remove CAS-A.CONTRACT.F_DEPENDENCE → check_phase_b\_contract must
    fail.

If removal does not block → assumption unnecessary → test fails.

------------------------------------------------------------------------

# 3️⃣ Phase A Closure Report

Create deterministic document:

docs/specs/phase_a\_closure_report.md

Include:

-   CAS-0A status: FROZEN
-   CAS-A status: DRAFT (PROVISIONAL)
-   List of CAS-A assumptions
-   Strong minimality test result: PASS
-   Coherence audit result: PASS
-   Explicit statement:

"Phase A complete (draft closure). No mathematical claims promoted."

No timestamps. Deterministic formatting.

------------------------------------------------------------------------

# 4️⃣ Optional Promotion (Governance Only)

If desired, promote:

CAS-A.NOTATION.STABILITY → CERTIFIED

Rationale: - Purely governance property. - Already enforced by
SymbolDictionary.freeze().

Do NOT promote mathematical assumptions.

Promotion must require explicit evidence entry in ledger.

------------------------------------------------------------------------

# 5️⃣ Verification

Run:

pytest mypy src ruff check .

All must pass.

------------------------------------------------------------------------

# 🚫 Non-Goals

Do NOT:

-   Validate the theorem.
-   Promote exposure locality to certified (unless mathematically
    proven).
-   Import Paper 0 coordinates.
-   Modify CAS-0A.
-   Introduce nondeterminism.

------------------------------------------------------------------------

# ✅ Completion Condition

-   Coherence audit implemented and passing.
-   Strong minimality enforced (semantic blocking).
-   Closure report written.
-   All tests pass.
-   Phase A declared COMPLETE (draft-closed).

At this point, the project is ready to either:

A)  Import first real Paper-derived definitions for stress testing, or
B)  Move into Phase B (operator-theoretic equilibrium analysis).
