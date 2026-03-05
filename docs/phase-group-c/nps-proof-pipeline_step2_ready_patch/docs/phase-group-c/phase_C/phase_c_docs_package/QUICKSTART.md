
# Phase C Quickstart

## Target Run

Run ID:
2026-03-04T211059Z

Run root:
cert_artifacts/2026-03-04T211059Z/

## Required Inputs

- CAS-A.json
- CAS-B.json
- CAS-0C.json
- PhaseC_ENTRY_REPORT.md

## Outputs

- CAS-C.json
- PhaseC_REPORT.md
- HESSIAN_MATRIX.json
- HESSIAN_BLOCKS.json
- INVERSE_SIGN_STRUCTURE.json
- EXPOSURE_RESPONSE_CHECK.json

## Recommended Execution

If CLI module exists:

PYTHONPATH=src python -m nps.phases.phase_c.build_casc   --run-id 2026-03-04T211059Z   --run-root cert_artifacts/2026-03-04T211059Z

Otherwise use the cascade instructions document.

## Completion

Phase C Step 1 is complete once PhaseC_REPORT.md confirms:

Phase C Status: READY_FOR_PHASE_D
