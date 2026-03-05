# CAS-C Taskpack 4 Specification

Schema: C-TASK04.v2

## Purpose

Taskpack 4 defines the **canonical structural representation of the
Hessian** used by subsequent Phase C tasks (5--9).

The goal is to compute a **structural decomposition artefact** that
exposes:

-   dimension
-   block structure
-   sparsity pattern
-   block matrices
-   verification checks

This artefact becomes the **single structural source of truth** for all
downstream matrix‑analysis tasks.

------------------------------------------------------------------------

# Output Artefact

File:

HESSIAN_BLOCKS.json

Location:

cert_artifacts/`<run_id>`{=html}/

------------------------------------------------------------------------

# Required Top-Level Fields

The JSON must contain the following fields.

{ "schema_version": "C-TASK04.v2", "run_id": "`<run_id>`{=html}",
"generated_utc": "`<timestamp>`{=html}",

"dimension": `<n>`{=html},

"block_structure": { "blocks": \[\] },

"sparsity_pattern": { "nonzero_positions": \[\] },

"blocks": {},

"checks": \[\] }

------------------------------------------------------------------------

# Field Definitions

## dimension

Integer size of the Hessian.

Example:

"dimension": 12

------------------------------------------------------------------------

## block_structure

Defines the deterministic structural partition of the variable space.

Example:

"block_structure": { "blocks": \[ { "name": "w", "index_start": 0,
"index_end": 11, "size": 12 } \] }

------------------------------------------------------------------------

## sparsity_pattern

Defines the support of the Hessian.

Example:

"sparsity_pattern": { "nonzero_positions": \[ \[0,0\], \[0,1\], \[1,0\],
\[1,1\] \] }

Positions correspond to non‑zero entries of H.

------------------------------------------------------------------------

## blocks

Contains the block matrices.

Example:

"blocks": { "w_w": \[\[...\]\] }

Future taskpacks may add additional blocks.

------------------------------------------------------------------------

## checks

Verification checks must use the canonical structure:

{ "id": "`<CHECK_ID>`{=html}", "ok": true, "status": "PASS", "details":
{} }

------------------------------------------------------------------------

# Required Checks

Taskpack 4 must produce at least:

CHK.C4.HESSIAN_AVAILABLE CHK.C4.BLOCK_DIMENSION_MATCH
CHK.C4.BLOCK_SYMMETRIC CHK.C4.SPARSITY_PATTERN_COMPUTED

------------------------------------------------------------------------

# Why This Schema Exists

Tasks 5--9 rely heavily on the **structural support of the Hessian**.

Instead of recomputing sparsity and block metadata in each task, this
artefact centralizes that information.

Downstream tasks then operate on:

-   block_structure
-   sparsity_pattern

rather than scanning the full matrix repeatedly.
