# Phase C Taskpack 5 --- Locality & Sparsity Certification (Final Cascade Instructions)

Taskpack ID: C-TASK05\
Schema Version: C-TASK05.v1\
Generated: 2026-03-05T13:18:28.301020Z

------------------------------------------------------------------------

# Goal

Produce **deterministic, auditable artefacts** verifying the **locality
/ sparsity support bounds** of the Phase C Hessian.

Outputs:

-   `HESSIAN_SPARSITY.json`
-   `PhaseC_TASK5_LOCALITY_SPARSITY_REPORT.md`

These artefacts certify the **support structure of the Hessian** used
later in Phase C tasks (diagonal dominance, comparison inequalities,
Neumann bounds, and M‑matrix certification).

------------------------------------------------------------------------

# Governance Rules

This taskpack is **governance-sensitive**.

Rules:

• Do **not** verify mathematics by reading Paper 0/1/2/3 or the thesis.\
• Papers may be quoted only as **PROV hypotheses**.\
• **VERIFIED results must come only from:**

    CAS artefacts
    computed numerical checks
    deterministic analysis of run artefacts

------------------------------------------------------------------------

# Target Run

Run ID:

    RUN_ID_TODO

Run root:

    cert_artifacts/RUN_ID_TODO/

------------------------------------------------------------------------

# Required Repo Search (Cascade must perform)

Before writing new code, search the repository for existing
implementations.

Search terms:

    locality sparsity
    hessian
    HESSIAN_
    block partition
    dominance
    comparison
    Z-matrix
    M-matrix
    Neumann
    inverse sign
    H_wtheta
    dw_dtheta

Search locations:

    src/nps/phases/phase_c/
    src/nps/models/
    src/nps/audit/
    src/nps/certification/

If code exists, **reuse it and add checks/reporting** instead of
duplicating logic.

------------------------------------------------------------------------

# Required Inputs

Load from run root:

    HESSIAN_BLOCKS.json

This artefact was produced by **Taskpack 4**.

Required fields inside it:

    dimension
    block_structure
    sparsity_pattern.nonzero_positions
    blocks

If `HESSIAN_BLOCKS.json` is missing → **FAIL immediately**.

------------------------------------------------------------------------

# Computations

## Extract Structure

Example:

``` python
data = load_json("HESSIAN_BLOCKS.json")

n = data["dimension"]
nonzero_positions = data["sparsity_pattern"]["nonzero_positions"]
```

------------------------------------------------------------------------

## Compute Sparsity Metrics

``` python
nonzero_count = len(nonzero_positions)
density = nonzero_count / (n * n)
```

------------------------------------------------------------------------

# Locality Radius Test

Define a **support radius** based on structural distance between
indices.

Example placeholder implementation:

``` python
max_radius = max(abs(i - j) for i,j in nonzero_positions)
```

This produces a **measured locality radius** for the Hessian support.

------------------------------------------------------------------------

# Required Checks

All checks must follow the canonical structure:

``` json
{
"id": "...",
"ok": true,
"status": "PASS",
"details": {}
}
```

------------------------------------------------------------------------

## CHK.C5.SPARSITY.METRICS_RECORDED

PASS if:

    nonzero_count > 0
    density > 0

------------------------------------------------------------------------

## CHK.C5.LOCALITY.RADIUS_TESTED

PASS if a locality radius value was computed.

Example details:

    locality_radius: <int>

------------------------------------------------------------------------

## CHK.C5.LOCALITY.SUPPORT_BOUND_HOLDS

PASS if Hessian support is finite and bounded.

Example rule:

    locality_radius < n

------------------------------------------------------------------------

# Output Artefact

Write:

    cert_artifacts/<run_id>/HESSIAN_SPARSITY.json

Schema:

``` json
{
"schema_version": "C-TASK05.v1",
"run_id": "<run_id>",
"generated_utc": "<timestamp>",

"dimension": n,

"sparsity_summary": {
"nonzero_count": nonzero_count,
"density": density,
"locality_radius": locality_radius
},

"checks": [...]
}
```

------------------------------------------------------------------------

# Report

Write:

    PhaseC_TASK5_LOCALITY_SPARSITY_REPORT.md

Example structure:

    # Phase C Task 5 — Locality & Sparsity Certification

    Run ID: <run_id>

    Dimension: <n>

    Nonzero entries: <nonzero_count>

    Density: <density>

    Locality radius: <radius>

    ## Checks

    CHK.C5.SPARSITY.METRICS_RECORDED
    CHK.C5.LOCALITY.RADIUS_TESTED
    CHK.C5.LOCALITY.SUPPORT_BOUND_HOLDS

    ## Result

    DONE if all PASS  
    BLOCKED otherwise

------------------------------------------------------------------------

# Commit Policy

Recommended:

• Commit **code + docs only**\
• Do **not commit `cert_artifacts/` outputs**

Optional run transcript:

    docs/phase-group-c/phase_C/RUNS/RUN_ID_TODO.md

------------------------------------------------------------------------

# Execution

Run Phase C normally:

``` bash
export NPS_IMPORT_FIREWALL=1
export NPS_CAS_GATE=1
export NPS_CERT_DEP_GATE=1
export NPS_RUN_DIR_INTEGRITY=1

PYTHONPATH=src python -m nps.phases.phase_c.build_casc   --run-id RUN_ID_TODO   --run-root cert_artifacts/RUN_ID_TODO
```

------------------------------------------------------------------------

# Result

This taskpack certifies the **finite support structure of the Hessian**.

These results feed directly into:

    Taskpack 6 — Diagonal Dominance
    Taskpack 7 — Comparison Inequalities
    Taskpack 8 — Neumann-Series Bounds
    Taskpack 9 — M-Matrix Certification
