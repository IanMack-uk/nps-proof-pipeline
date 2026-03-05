# CAS-C Task 8 Spec --- Neumann Series / Invertibility Bounds (FINAL)

**Taskpack ID:** C-TASK08\
**Schema Version:** C-TASK08.v1\
**Generated:** 2026-03-05T14:59:23Z

Taskpack 8 certifies **invertibility bounds for the coupling matrix**

C := -H

using Neumann-series--style criteria derived from the decomposition

C = D - B

where

D = diag(C)\
B = diag(C) - C

The goal is to produce a **governance‑auditable certification artefact**
establishing that the matrix is safely invertible and structurally
compatible with M‑matrix theory used in later taskpacks.

------------------------------------------------------------------------

## Inputs (run root)

Required:

-   HESSIAN_BLOCKS.json
-   DIAGONAL_DOMINANCE_CERT.json
-   COMPARISON_INEQUALITIES_CERT.json

------------------------------------------------------------------------

## Matrix Definition

    H = blocks["w_w"]
    C := -H

Diagonal:

    D = diag(C)

Off‑diagonal magnitude matrix:

    B = D - C

------------------------------------------------------------------------

## Certification Metric

Compute

    ρ_bound = max_i ( row_sum(|B_i|) / D_ii )

Strict dominance implies

    ρ_bound < 1

This provides a **Neumann‑series invertibility bound**.

------------------------------------------------------------------------

## Output Artefacts

Taskpack 8 must emit

    NEUMANN_SERIES_CERT.json
    PhaseC_TASK8_NEUMANN_SERIES_REPORT.md

in

    cert_artifacts/<run_id>/

------------------------------------------------------------------------

## Required Checks

Checks must appear in this order:

1.  CHK.C8.INPUTS.PRESENT
2.  CHK.C8.NEUMANN.RHO_BOUND_COMPUTED
3.  CHK.C8.NEUMANN.RHO_LT_ONE

------------------------------------------------------------------------

## Purpose

This artefact prepares the final **inverse‑positivity certification** in
Taskpack 9.
