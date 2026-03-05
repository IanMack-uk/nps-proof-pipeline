# Phase 0C --- Pre‑Execution Verification Tasks for Cascade

## Purpose

Before executing **Phase 0C Step 2**, Cascade must verify that the
upstream artefacts and governance gates are correctly configured.\
These checks ensure that CAS‑0C generation is deterministic and
compliant with the NPS certification pipeline rules.

This document instructs Cascade to:

1.  Locate required artefacts in the run directory.
2.  Validate that required fields exist in CAS‑A and CAS‑B artefacts.
3.  Confirm that the Phase C entry gate report is valid.
4.  Confirm governance gates are active.
5.  Confirm the project structure matches expected Phase 0C locations.

If any check fails, Cascade must stop and report the failure.

------------------------------------------------------------------------

# Target Run

Run ID:

    2026-03-04T211059Z

Run directory:

    cert_artifacts/2026-03-04T211059Z/

------------------------------------------------------------------------

# Step 1 --- Locate Required Files

Cascade must locate the following files:

    cert_artifacts/2026-03-04T211059Z/CAS-A.json
    cert_artifacts/2026-03-04T211059Z/CAS-B.json
    cert_artifacts/2026-03-04T211059Z/PhaseC_ENTRY_REPORT.md

If any file is missing, report:

    PHASE_0C_PRECHECK_FAIL: Missing required artifact

------------------------------------------------------------------------

# Step 2 --- Validate CAS-A Structure

Open:

    CAS-A.json

Confirm that the following checks exist:

    CHK.A.STATIONARITY
    CHK.A.NEG_DEF_HESSIAN

Expected structure:

    "checks": [
      {
        "check_id": "CHK.A.STATIONARITY",
        "ok": true
      },
      {
        "check_id": "CHK.A.NEG_DEF_HESSIAN",
        "ok": true
      }
    ]

If either check is missing or `ok` is not `true`, report:

    PHASE_0C_PRECHECK_FAIL: CAS-A required checks missing

------------------------------------------------------------------------

# Step 3 --- Validate CAS-B Fields

Open:

    CAS-B.json

Confirm the following fields exist:

    equilibrium_objective
    equilibrium_regime
    certified_objective

Expected values for this run:

    equilibrium_objective = maximize
    equilibrium_regime = strict_concave
    certified_objective = minus_phi

If fields are missing or values differ, report:

    PHASE_0C_PRECHECK_FAIL: CAS-B equilibrium regime mismatch

------------------------------------------------------------------------

# Step 4 --- Validate Phase C Entry Gate

Open:

    PhaseC_ENTRY_REPORT.md

Confirm the **final line** is exactly:

    Phase C Entry Gate: APPROVED

If not, report:

    PHASE_0C_PRECHECK_FAIL: Phase C entry gate not approved

------------------------------------------------------------------------

# Step 5 --- Confirm Governance Gates

Cascade must confirm the following environment variables are enabled:

    NPS_IMPORT_FIREWALL=1
    NPS_CAS_GATE=1
    NPS_CERT_DEP_GATE=1
    NPS_RUN_DIR_INTEGRITY=1

If any variable is missing or disabled, report:

    PHASE_0C_PRECHECK_FAIL: Governance gates not enabled

------------------------------------------------------------------------

# Step 6 --- Confirm Phase 0C Code Location

Cascade must confirm that the Phase 0C module exists:

    src/nps/phases/phase_0c/build_cas0c.py

And that the documentation folder exists:

    docs/phase-group-c/phase_0C_step2_cascade_package/

If either path is missing, report:

    PHASE_0C_PRECHECK_FAIL: Phase 0C module not found

------------------------------------------------------------------------

# Step 7 --- Produce Verification Report

Cascade must generate:

    cert_artifacts/2026-03-04T211059Z/Phase0C_PRECHECK_REPORT.md

Report structure:

    # Phase 0C Pre‑Execution Verification Report

    Run ID: 2026-03-04T211059Z

    ## Artifact Presence
    PASS / FAIL

    ## CAS-A Checks
    PASS / FAIL

    ## CAS-B Regime
    PASS / FAIL

    ## Entry Gate
    PASS / FAIL

    ## Governance Gates
    PASS / FAIL

    ## Phase 0C Module Presence
    PASS / FAIL

    ## Final Status
    READY_FOR_PHASE_0C / BLOCKED

------------------------------------------------------------------------

# Final Action

If all checks pass:

Cascade may proceed to execute:

    PYTHONPATH=src python -m nps.phases.phase_0c.build_cas0c   --run-id 2026-03-04T211059Z   --run-root cert_artifacts/2026-03-04T211059Z   --phase-c-entry-report cert_artifacts/2026-03-04T211059Z/PhaseC_ENTRY_REPORT.md

Otherwise, Phase 0C execution must be blocked.
