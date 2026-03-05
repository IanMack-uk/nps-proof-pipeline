# Taskpack 8 Verification Rules (FINAL)

**Taskpack ID:** C-TASK08\
**Schema Version:** C-TASK08.v1\
**Generated:** 2026-03-05T14:59:23Z

------------------------------------------------------------------------

## Artefact Verified

    NEUMANN_SERIES_CERT.json

------------------------------------------------------------------------

## Required Checks

### CHK.C8.INPUTS.PRESENT

Required files:

-   HESSIAN_BLOCKS.json
-   DIAGONAL_DOMINANCE_CERT.json
-   COMPARISON_INEQUALITIES_CERT.json

PASS if all present and parse correctly.

------------------------------------------------------------------------

### CHK.C8.NEUMANN.RHO_BOUND_COMPUTED

Ensure

    rho_bound

exists and is numeric.

------------------------------------------------------------------------

### CHK.C8.NEUMANN.RHO_LT_ONE

PASS if

    rho_bound < 1

FAIL otherwise.
