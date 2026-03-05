# CAS-C Taskpack 5 Specification

Schema: C-TASK05.v1

## Purpose

Taskpack 5 certifies the **locality / sparsity structure of the
Hessian** produced in Phase C.

It consumes the structural artefact:

HESSIAN_BLOCKS.json (from Taskpack 4)

and produces a certified sparsity verification artefact.

This task validates that the Hessian support is consistent with the
**locality assumptions imported from CAS-0C / Paper 0**.

------------------------------------------------------------------------

# Inputs

Required run-root artefacts:

-   HESSIAN_BLOCKS.json

------------------------------------------------------------------------

# Outputs

cert_artifacts/`<run_id>`{=html}/

-   HESSIAN_SPARSITY_CERT.json
-   PhaseC_TASK5_SPARSITY_REPORT.md

------------------------------------------------------------------------

# Output JSON Schema

{ "schema_version": "C-TASK05.v1", "run_id": "`<run_id>`{=html}",
"generated_utc": "`<timestamp>`{=html}",

"dimension": `<n>`{=html},

"sparsity_summary": { "nonzero_count": `<int>`{=html}, "density":
`<float>`{=html} },

"checks": \[\] }

------------------------------------------------------------------------

# Check Structure

All checks must follow the canonical structure:

{ "id": "`<CHECK_ID>`{=html}", "ok": true \| false, "status": "PASS" \|
"FAIL", "details": { } }

------------------------------------------------------------------------

# Required Checks

CHK.C5.SPARSITY_PATTERN_PRESENT CHK.C5.NONZERO_POSITIONS_VALID
CHK.C5.DENSITY_COMPUTED

------------------------------------------------------------------------

# Definitions

Nonzero entries are defined by the sparsity pattern generated in
Taskpack 4:

sparsity_pattern.nonzero_positions

Density is defined as:

density = nonzero_count / (dimension \* dimension)

------------------------------------------------------------------------

# Result Rule

Taskpack 5 status is:

DONE

if all checks PASS.

Otherwise:

BLOCKED.
