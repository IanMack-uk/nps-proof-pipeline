# Phase C Taskpack 4 --- Hessian Block Decomposition (Consolidated Instructions)

Taskpack ID: C-TASK04\
Schema Version: C-TASK04.v2\
Dependencies: - Taskpack 1 --- Operator Layer - Taskpack 3 --- Hessian
Artefact

Outputs: - HESSIAN_BLOCKS.json - PhaseC_TASK4_BLOCK_DECOMP_REPORT.md

Generated: 2026-03-05T12:58:47.933472Z

------------------------------------------------------------------------

# Objective

Extend:

src/nps/phases/phase_c/build_casc.py

so that during a normal **Phase C run** the pipeline performs **Taskpack
4: Hessian Block Decomposition**.

This step must:

1.  Read the Hessian already computed in Phase C.
2.  Construct a **structural block representation** of the Hessian.
3.  Emit run‑root artefacts.
4.  Use the canonical check structure introduced in Taskpack 3:

```{=html}
<!-- -->
```
    {id, ok, status, details}

5.  Emit structural metadata required for Tasks **5--9**:
    -   dimension
    -   block_structure
    -   sparsity_pattern
    -   blocks
    -   checks
6.  **Do NOT change CAS‑C gating or READY_FOR_PHASE_D semantics.**

------------------------------------------------------------------------

# Target File

Only modify:

    src/nps/phases/phase_c/build_casc.py

Do **not** modify other modules.

------------------------------------------------------------------------

# Implementation Steps

## 1. Locate the Hessian

The Hessian matrix `H` already exists from Taskpack 3.

Example:

``` python
n = H.shape[0]
```

------------------------------------------------------------------------

## 2. Compute Structural Metadata

### Dimension

``` python
dimension = n
```

------------------------------------------------------------------------

### Block Structure

Define a deterministic block partition.

Initial minimal partition:

    w block → indices 0..n-1

Implementation:

``` python
block_structure = {
  "blocks": [
    {
      "name": "w",
      "index_start": 0,
      "index_end": n-1,
      "size": n
    }
  ]
}
```

------------------------------------------------------------------------

### Sparsity Pattern

Compute non‑zero positions.

``` python
import numpy as np

nonzero_positions = [
    [int(i), int(j)]
    for i, j in zip(*np.nonzero(H))
]
```

------------------------------------------------------------------------

## 3. Create Block Matrices

``` python
blocks = {
  "w_w": H.tolist()
}
```

Future taskpacks may add additional blocks.

------------------------------------------------------------------------

## 4. Build Verification Checks

Checks must follow the canonical schema:

    {
    "id": "...",
    "ok": true,
    "status": "PASS",
    "details": { }
    }

### Required Checks

#### CHK.C4.HESSIAN_AVAILABLE

Verify Hessian exists.

    ok = H is not None

------------------------------------------------------------------------

#### CHK.C4.BLOCK_DIMENSION_MATCH

Verify block dimension equals Hessian dimension.

    block_dimension == n

------------------------------------------------------------------------

#### CHK.C4.BLOCK_SYMMETRIC

Compute:

``` python
symmetry_error = float(np.max(np.abs(H - H.T)))
```

PASS if:

    symmetry_error <= 1e-10

------------------------------------------------------------------------

#### CHK.C4.SPARSITY_PATTERN_COMPUTED

PASS if:

    len(nonzero_positions) > 0

------------------------------------------------------------------------

## 5. Emit HESSIAN_BLOCKS.json

Structure must be:

``` json
{
"schema_version": "C-TASK04.v2",
"run_id": "<run_id>",
"generated_utc": "<timestamp>",

"dimension": n,

"block_structure": {
  "blocks": [...]
},

"sparsity_pattern": {
  "nonzero_positions": [...]
},

"blocks": {
  "w_w": [...]
},

"checks": [...]
}
```

Write to:

    cert_artifacts/<run_id>/HESSIAN_BLOCKS.json

Example write:

``` python
json.dump(data, f, indent=2)
```

------------------------------------------------------------------------

## 6. Generate Markdown Report

Create:

    PhaseC_TASK4_BLOCK_DECOMP_REPORT.md

Location:

    cert_artifacts/<run_id>/

Example report structure:

    # Phase C Task 4 — Hessian Block Decomposition

    Run ID: <run_id>

    ## Dimension

    <n>

    ## Block Structure

    w block → indices 0..n-1

    ## Sparsity Pattern

    Total non‑zero entries: <count>

    ## Checks

    | Check | Status |
    |------|-------|
    CHK.C4.HESSIAN_AVAILABLE | PASS |
    CHK.C4.BLOCK_DIMENSION_MATCH | PASS |
    CHK.C4.BLOCK_SYMMETRIC | PASS |
    CHK.C4.SPARSITY_PATTERN_COMPUTED | PASS |

    ## Result

    DONE if all checks PASS
    BLOCKED otherwise

------------------------------------------------------------------------

# Governance Requirements

Do NOT modify:

    CAS-C Status
    Phase C Status
    READY_FOR_PHASE_D

Do NOT commit run artefacts.

All generated artefacts remain in:

    cert_artifacts/<run_id>/

------------------------------------------------------------------------

# Execution

Run Phase C normally:

``` bash
export NPS_IMPORT_FIREWALL=1
export NPS_CAS_GATE=1
export NPS_CERT_DEP_GATE=1
export NPS_RUN_DIR_INTEGRITY=1

PYTHONPATH=src python -m nps.phases.phase_c.build_casc   --run-id 2026-03-04T211059Z   --run-root cert_artifacts/2026-03-04T211059Z
```

------------------------------------------------------------------------

# Expected Run Root

    cert_artifacts/2026-03-04T211059Z/

    OPERATOR_LAYER.json
    HESSIAN_MATRIX.json
    HESSIAN_BLOCKS.json

    PhaseC_TASK1_OPERATOR_LAYER_REPORT.md
    PhaseC_TASK3_HESSIAN_ARTIFACTS_REPORT.md
    PhaseC_TASK4_BLOCK_DECOMP_REPORT.md

------------------------------------------------------------------------

# Result

Taskpack 4 now produces a **canonical structural Hessian artefact**.

Downstream tasks (5--9) will use:

    dimension
    block_structure
    sparsity_pattern

to perform:

-   locality verification
-   diagonal dominance checks
-   comparison inequalities
-   Neumann bounds
-   M‑matrix certification

without rescanning the full matrix each time.
