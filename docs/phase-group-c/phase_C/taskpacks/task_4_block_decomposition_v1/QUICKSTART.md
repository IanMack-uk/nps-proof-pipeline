# Phase C Taskpack 4 --- Block Decomposition (QUICKSTART)

Taskpack ID: C-TASK04\
Schema: C-TASK04.v1

## Purpose

Taskpack 4 introduces the **structural block decomposition of the
Hessian** produced in Taskpack 3.\
It creates a canonical block representation of the Hessian matrix so
later Phase C tasks can reason about:

-   locality / sparsity structure
-   diagonal dominance
-   comparison inequalities
-   Neumann-series bounds
-   M-matrix criteria
-   selected inverse entries

This taskpack **does not change Phase C semantics or gating**.\
It only emits structural artefacts derived from the already-certified
Hessian.

------------------------------------------------------------------------

# Dependencies

Taskpack 4 assumes the following tasks have already been implemented and
executed:

1.  **Taskpack 1 --- Operator Layer**
    -   `OPERATOR_LAYER.json`
2.  **Taskpack 3 --- Hessian Artefact**
    -   `HESSIAN_MATRIX.json`

Both artefacts must exist in the run root.

------------------------------------------------------------------------

# Artefacts Produced

Running this taskpack will create:

    HESSIAN_BLOCKS.json
    PhaseC_TASK4_BLOCK_DECOMP_REPORT.md

Both are written into the run root:

    cert_artifacts/<run_id>/

------------------------------------------------------------------------

# What the Task Does

1.  Reads the Hessian matrix already computed by Phase C.
2.  Constructs a deterministic structural block representation.
3.  Verifies basic structural invariants.
4.  Writes a machine-readable JSON artefact and a human-readable report.

The initial block partition is intentionally minimal:

    w_w  → full Hessian block for edge variables

Later taskpacks refine this structure.

------------------------------------------------------------------------

# Execution (Cascade)

Run this taskpack using Cascade with the instruction file:

    PHASE_C_TASK4_CASCADE_INSTRUCTIONS.md

Cascade will extend:

    src/nps/phases/phase_c/build_casc.py

to generate the required artefacts automatically during a Phase C run.

------------------------------------------------------------------------

# Running Phase C After Implementation

After Cascade applies the Taskpack 4 patch, run Phase C normally:

``` bash
export NPS_IMPORT_FIREWALL=1
export NPS_CAS_GATE=1
export NPS_CERT_DEP_GATE=1
export NPS_RUN_DIR_INTEGRITY=1

PYTHONPATH=src python -m nps.phases.phase_c.build_casc   --run-id 2026-03-04T211059Z   --run-root cert_artifacts/2026-03-04T211059Z
```

------------------------------------------------------------------------

# Expected Run Root

After the run you should see:

    cert_artifacts/2026-03-04T211059Z/

    OPERATOR_LAYER.json
    HESSIAN_MATRIX.json
    HESSIAN_BLOCKS.json

    PhaseC_TASK1_OPERATOR_LAYER_REPORT.md
    PhaseC_TASK3_HESSIAN_ARTIFACTS_REPORT.md
    PhaseC_TASK4_BLOCK_DECOMP_REPORT.md

------------------------------------------------------------------------

# Verification

Open:

    cert_artifacts/<run_id>/HESSIAN_BLOCKS.json

Confirm:

-   `schema_version: "C-TASK04.v1"`
-   block structure is present
-   checks use `{id, ok, status, details}` structure

Expected checks:

    CHK.C4.HESSIAN_AVAILABLE
    CHK.C4.BLOCK_DIMENSION_MATCH
    CHK.C4.BLOCK_SYMMETRIC

------------------------------------------------------------------------

# Result Criteria

Taskpack 4 is **DONE** if:

-   `HESSIAN_BLOCKS.json` is generated
-   all `CHK.C4.*` checks PASS
-   the report `PhaseC_TASK4_BLOCK_DECOMP_REPORT.md` is written

Otherwise the task is **BLOCKED**.

------------------------------------------------------------------------

# Next Taskpacks

Once Taskpack 4 is complete, the following become implementable:

-   Taskpack 5 --- Locality / sparsity verification
-   Taskpack 6 --- Diagonal dominance
-   Taskpack 8 --- Neumann-series bounds

All of these operate directly on `HESSIAN_BLOCKS.json`.
