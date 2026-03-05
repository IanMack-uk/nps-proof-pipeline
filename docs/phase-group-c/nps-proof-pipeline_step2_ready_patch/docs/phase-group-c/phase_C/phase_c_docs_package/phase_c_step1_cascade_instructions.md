
# Phase C — Step 1 (Hessian Analysis) — Cascade Instructions

## Purpose
This step begins **Phase C — Curvature and Hessian Structure**. The goal is to compute and certify the structural Hessian objects required for downstream comparative-statics analysis.

Outputs must support creation of **CAS-C.json**.

## Target Run
Run ID:
2026-03-04T211059Z

Run root:
cert_artifacts/2026-03-04T211059Z/

## Inputs (must exist in run root)
- CAS-A.json
- CAS-B.json
- CAS-0C.json
- PhaseC_ENTRY_REPORT.md

## Governance Gates (must be enabled)
NPS_IMPORT_FIREWALL=1
NPS_CAS_GATE=1
NPS_CERT_DEP_GATE=1
NPS_RUN_DIR_INTEGRITY=1

## Deliverables
Cascade must produce:

- CAS-C.json
- PhaseC_REPORT.md
- HESSIAN_MATRIX.json
- HESSIAN_BLOCKS.json
- INVERSE_SIGN_STRUCTURE.json
- EXPOSURE_RESPONSE_CHECK.json

All files must be written to the run root.

## Step 1 — Compute Hessian

Compute the Hessian of the certified objective:

H = ∇² Φ_certified(w*, θ)

at the certified equilibrium w* recorded in Phase B.

Store as:
HESSIAN_MATRIX.json

Record:
- dimension
- symmetry check
- numerical tolerance policy

## Step 2 — Structural Block Decomposition

Using the structural-coordinate basis defined in Phase A, compute block partitions:

H_ww
H_wθ
H_θw

Store as:
HESSIAN_BLOCKS.json

## Step 3 — Matrix Hypothesis Certification

Attempt certification using only finite-dimensional tools:

- diagonal dominance margins
- comparison inequalities
- Neumann-series inversion bounds

Spectral methods are forbidden unless explicitly escalated.

Record results.

## Step 4 — Inverse-Hessian Sign Structure

Using certified hypotheses, determine sign predictions for selected entries of:

H^{-1} or C^{-1}, where C = -H.

Store results in:
INVERSE_SIGN_STRUCTURE.json

## Step 5 — Exposure–Response Compatibility

Compute cross-derivative block:

D_θ F(w) = D_θ ∇Φ_certified(w, θ)

Verify compatibility with inverse-Hessian sign predictions.

Store results in:
EXPOSURE_RESPONSE_CHECK.json

## Step 6 — Write Phase C Report

Generate:

PhaseC_REPORT.md

using the provided report template.

## Completion Criteria

Phase C Step 1 is complete when:

- CAS-C.json exists
- PhaseC_REPORT.md exists
- Hessian artifacts exist
- PhaseC_REPORT.md ends with:

Phase C Status: READY_FOR_PHASE_D
