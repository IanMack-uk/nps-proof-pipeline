# Phase C Taskpack 4 --- Verification Rules

Taskpack ID: C-TASK04\
Schema Version: C-TASK04.v2

These rules define the **certifiable checks** that must be executed when
generating `HESSIAN_BLOCKS.json`.

The checks must be emitted using the canonical structure:

{ "id": "`<CHECK_ID>`{=html}", "ok": true \| false, "status": "PASS" \|
"FAIL" \| "SKIP", "details": { ... } }

All checks must appear in the `checks` array in `HESSIAN_BLOCKS.json`.

------------------------------------------------------------------------

# Inputs

Required run-root artefacts:

-   `HESSIAN_MATRIX.json`
-   `OPERATOR_LAYER.json`

If either artefact is missing the task must **FAIL immediately**.

------------------------------------------------------------------------

# Check Rules

## CHK.C4.HESSIAN_AVAILABLE

**Goal**\
Verify that the Hessian matrix exists and can be loaded.

**PASS if**

-   `HESSIAN_MATRIX.json` exists
-   matrix field present
-   matrix dimension \> 0

**FAIL if**

-   file missing
-   matrix missing
-   dimension == 0

Example details:

{ "dimension": 12 }

------------------------------------------------------------------------

## CHK.C4.BLOCK_DIMENSION_MATCH

**Goal**\
Verify that the block decomposition covers the full Hessian dimension.

**PASS if**

block_size == Hessian dimension

**FAIL if**

block_size != dimension

Example details:

{ "hessian_dimension": 12, "block_dimension": 12 }

------------------------------------------------------------------------

## CHK.C4.BLOCK_SYMMETRIC

**Goal**\
Confirm that the Hessian block remains symmetric.

Compute:

symmetry_error = max(abs(H - H.T))

Tolerance:

1e-10

**PASS if**

symmetry_error ≤ tolerance

Example details:

{ "symmetry_error": 2.3e-15, "tolerance": 1e-10 }

------------------------------------------------------------------------

## CHK.C4.SPARSITY_PATTERN_COMPUTED

**Goal**\
Confirm that the sparsity pattern metadata was generated.

**PASS if**

-   `nonzero_positions` list exists
-   list length \> 0

Example details:

{ "nonzero_count": 44 }

------------------------------------------------------------------------

# Determinism Requirement

The generated artefact must be deterministic.

Running Phase C twice with the same run root inputs must produce:

-   identical `dimension`
-   identical `block_structure`
-   identical `sparsity_pattern`
-   identical `checks` results

If determinism fails the task is considered **BLOCKED**.

------------------------------------------------------------------------

# Artefact Validation

`HESSIAN_BLOCKS.json` must contain:

dimension\
block_structure\
sparsity_pattern\
blocks\
checks

Missing any field → FAIL.

------------------------------------------------------------------------

# Result Rule

Taskpack 4 status is:

DONE

if all checks PASS.

Otherwise:

BLOCKED.
