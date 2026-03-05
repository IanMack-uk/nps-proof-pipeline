# Phase C Taskpack 6 — Diagonal Dominance Certification (FINAL)

Taskpack ID: C-TASK06  
Schema Version: C-TASK06.v2  
Generated: 2026-03-05T13:57:56.233098Z

---

# Objective

Extend

src/nps/phases/phase_c/build_casc.py

so that Phase C runs produce the artefacts:

DIAGONAL_DOMINANCE_CERT.json  
PhaseC_TASK6_DIAGONAL_DOMINANCE_REPORT.md

The step must compute strict diagonal dominance for the coupling matrix.

---

# Required Inputs

Load the following run-root artefacts:

HESSIAN_MATRIX.json  
HESSIAN_BLOCKS.json  
HESSIAN_SPARSITY_CERT.json

Optional:

OPERATOR_LAYER.json

Fail immediately if required files are missing.

---

# Matrix Definitions

Let

H := ∇²_w Φ_cert(w*, θ)

Define coupling matrix

C := -H

---

# Matrix Slice

Use the structural block from Taskpack 4:

blocks["w_w"]

from HESSIAN_BLOCKS.json.

---

# Dominance Computation

For each row i:

row_sum_off(i) = Σ_j≠i |C_ij|

margin_i = C_ii − row_sum_off(i)

Record

min_margin = min_i margin_i  
max_margin = max_i margin_i

Strict diagonal dominance holds if

min_margin > 0

---

# Additional Structural Metrics (Required)

Populate the following fields in DIAGONAL_DOMINANCE_CERT.json:

matrix_definition  
row_metrics  
witnesses  
derived_sign_pattern

These fields must follow the schema defined in

CAS-C_TASK6_SPEC.md

---

# Required Checks

Emit check objects with the structure:

id / ok / status / details

Checks required:

CHK.C6.C_MATRIX.DEFINED  
CHK.C6.DOMINANCE.MARGINS_COMPUTED  
CHK.C6.DOMINANCE.STRICT_PASS

---

# Output Artefact

Write

cert_artifacts/<run_id>/DIAGONAL_DOMINANCE_CERT.json

and

PhaseC_TASK6_DIAGONAL_DOMINANCE_REPORT.md

---

# Commit Policy

Commit code only.  
Do not commit cert_artifacts outputs.

---

# Execution

Run Phase C normally:

PYTHONPATH=src python -m nps.phases.phase_c.build_casc \
  --run-id RUN_ID_TODO \
  --run-root cert_artifacts/RUN_ID_TODO

---

# Result

This taskpack certifies strict diagonal dominance of the coupling matrix
and prepares structural metrics required for

Taskpack 7 — Comparison Inequalities  
Taskpack 8 — Neumann-Series Bounds  
Taskpack 9 — M-Matrix Certification
