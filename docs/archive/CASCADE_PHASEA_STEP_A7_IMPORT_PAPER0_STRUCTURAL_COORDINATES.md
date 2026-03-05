# CASCADE PHASE A (STEP A7) --- IMPORT PAPER 0 STRUCTURAL COORDINATES (PROVISIONAL + FALSIFICATION HARNESS)

Project: `nps-proof-pipeline`

Context: - CAS-0A certified and frozen. - Phase A draft closure complete
(A6). - StructuralExposure + StructuralCoordinates framework exists
(controls only). - Phase-B interface contract checker implemented. -
Paper 0 (The Network Potential Series, v13) now available for
extraction. - No Paper 0 definitions have yet been imported into
executable code.

This step introduces **Paper 0 structural coordinate definitions** into
the Phase A validation framework as PROVISIONAL candidates and attempts
systematic falsification.

No theorem promotion. No structural representation claims validated. All
imports remain PROVISIONAL.

------------------------------------------------------------------------

# 🎯 Objective

1.  Extract candidate structural coordinate definitions from Paper 0.
2.  Implement them as CoordinateDefinition plugins.
3.  Encode Paper 0's claimed properties (locality, automorphism
    invariance, monotonicity).
4.  Add validators for those properties.
5.  Seed new CAS-A assumptions (PROVISIONAL).
6.  Attempt falsification using deterministic perturbation tests.
7.  Log evidence and counterexamples.
8.  Register Paper 0 representation theorem as CONJECTURE only.

------------------------------------------------------------------------

# 1️⃣ Extract from Paper 0 (Specification Layer)

Paper 0 defines per-edge coordinates:

Intrinsic coordinate: w_e\
Separation coordinate: S_e(w)\
Redundancy coordinate: R_e(w)

Separation coordinate requirements: - Continuous - Depends only on
bounded neighbourhood N(e) - Automorphism invariant - Monotone under
strengthening alternative paths

Redundancy coordinate requirements: - Continuous - Depends only on
bounded neighbourhood N(e) - Automorphism invariant - Monotone under
closure (alternative short cycles)

Representation claim (Theorem 0.8.1): For each e, ∃ continuous H_e such
that:

F_e(w) = H_e(w_e, S_e(w), R_e(w))

This claim must be registered as CONJECTURE only.

------------------------------------------------------------------------

# 2️⃣ Files to Add

Create:

src/nps/phases/phase_a/coordinates/ coordinate_paper0_candidates.py
coordinate_paper0_validation.py

src/nps/phases/phase_a/ seed_paper0_coordinate_assumptions.py
seed_paper0_conjectures.py

tests/phase_a/ test_paper0_structural_coordinates.py

docs/specs/ cas_a\_paper0_coordinate_import.md

docs/reports/ paper0_coordinate_falsification_log.md

------------------------------------------------------------------------

# 3️⃣ Implement Paper 0 Candidate Coordinates

## 3.1 Separation Candidate (Example)

Implement at least one plausible candidate, e.g.:

S_e(w) := weighted shortest path length between endpoints of e computed
on bounded neighbourhood subgraph N(e) with e removed.

Locality: NEIGHBORHOOD_N(e)

Alternative candidate allowed: effective resistance proxy (bounded
neighbourhood)

Must: - deterministic - finite - no external randomness

## 3.2 Redundancy Candidate

Implement example:

R_e(w) := weighted triangle count involving edge e computed within N(e)

Locality: NEIGHBORHOOD_N(e)

------------------------------------------------------------------------

# 4️⃣ Validators for Paper 0 Properties

In coordinate_paper0_validation.py implement:

## 4.1 check_locality_paper0(...)

Ensure coordinate does not change under perturbations outside N(e).

## 4.2 check_automorphism_invariance(...)

For small test graphs: - Permute node labels - Map edge index
accordingly - Require coordinate value unchanged

Deterministic relabelling.

## 4.3 check_monotonicity_separation(...)

Increase alternative path weights → S_e should not increase.

## 4.4 check_monotonicity_redundancy(...)

Increase alternative short-cycle weights → R_e should not decrease.

All validators must require_assumption_present for relevant CAS-A IDs.

------------------------------------------------------------------------

# 5️⃣ Seed New CAS-A Assumptions (PROVISIONAL)

Register:

CAS-A.COORD.AUTOMORPHISM_INVARIANCE (FOUNDATIONS)
CAS-A.COORD.MONOTONICITY_SEPARATION (FOUNDATIONS)
CAS-A.COORD.MONOTONICITY_REDUNDANCY (FOUNDATIONS)
CAS-A.COORD.PAPER0_LOCALITY (FOUNDATIONS)

All status = PROVISIONAL.

Do not promote.

------------------------------------------------------------------------

# 6️⃣ Register Paper 0 Representation as CONJECTURE

Add StatementRecord:

ID: THM.P0.0_8\_1 Status: CONJECTURE Text: F_e(w) = H_e(w_e, S_e(w),
R_e(w)) with H_e continuous.

No validation attempt.

------------------------------------------------------------------------

# 7️⃣ Tests

test_paper0_structural_coordinates.py must:

-   Verify S and R evaluate finite.
-   Verify locality holds under bounded perturbations.
-   Verify automorphism invariance on small graphs.
-   Verify monotonicity tests.
-   Include negative control (deliberately non-invariant coordinate).
-   Log evidence to ValidationRegistry.
-   If violation found, append deterministic counterexample entry to
    paper0_coordinate_falsification_log.md.

------------------------------------------------------------------------

# 8️⃣ Documentation

docs/specs/cas_a\_paper0_coordinate_import.md

Include: - Status: PROVISIONAL IMPORT - Definitions implemented -
Property validators - Evidence summary - Explicit disclaimer: "No Paper
0 theorem validated."

------------------------------------------------------------------------

# 9️⃣ Verification

Run:

pytest mypy src ruff check .

All must pass.

------------------------------------------------------------------------

# 🚫 Non-Goals

Do NOT: - Promote Paper 0 coordinates to CERTIFIED. - Modify CAS-0A. -
Validate representation theorem. - Introduce nondeterministic testing.

------------------------------------------------------------------------

# ✅ Completion Condition

-   Paper 0 structural coordinates implemented as candidates.
-   Locality, invariance, monotonicity validators implemented.
-   New CAS-A assumptions seeded (PROVISIONAL).
-   Representation theorem registered as CONJECTURE.
-   Tests pass (or controlled failures logged).
-   Falsification log created.

At this point, Phase A becomes a true mathematical stress-testing
environment for Paper 0 definitions.
