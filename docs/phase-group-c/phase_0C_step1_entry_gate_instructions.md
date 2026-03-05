
# Phase 0C – Step 1 Execution Guide
## Validate Phase C Entry Gate and Produce Certification Report

This document instructs **Cascade / Windsurf** to execute **Step 1 of Phase 0C** in the Structural Differentiation / Ordering Theorem certification pipeline.

The goal of this step is to **validate that a given run satisfies the Phase C entry conditions** and to produce a **formal report** summarising the result.

---

# Objective

Confirm that the target run satisfies the **Phase C entry gate**.

Phase C is only permitted if the following conditions hold:

1. **Strict‑concave maximiser regime**
2. **Stationarity of the equilibrium**
3. **Negative‑definite Hessian at the equilibrium**
4. The run directory contains a **valid canonical CAS chain** through Phase B′.

If these conditions are not satisfied, **Phase Group C must not proceed**.

---

# Preconditions

The run directory must contain the canonical certification chain:

```
CAS-0A.json
CAS-A.json
CAS-Ap.json
CAS-0B.json
CAS-B.json
CAS-Bp.json
```

Location:

```
cert_artifacts/<run_id>/
```

No files should be read from `experiments/` during this validation.

---

# Required Environment Gates

Before executing validation, ensure the governance gates are enabled:

```bash
export NPS_IMPORT_FIREWALL=1
export NPS_CAS_GATE=1
export NPS_CERT_DEP_GATE=1
export NPS_RUN_DIR_INTEGRITY=1
```

These gates enforce certification integrity and dependency isolation.

---

# Execution Command

Run the Phase C entry validator using the repository module.

```
PYTHONPATH=src python -c "
from pathlib import Path
from nps.audit.phase_c_entry_gate import validate_phase_c_entry

validate_phase_c_entry(Path('cert_artifacts')/'<run_id>')
"
```

Replace `<run_id>` with the run identifier.

Example:

```
PYTHONPATH=src python -c "
from pathlib import Path
from nps.audit.phase_c_entry_gate import validate_phase_c_entry

validate_phase_c_entry(Path('cert_artifacts')/'RUN_2026_03_04')
"
```

---

# Expected Behaviour

The validator must perform the following checks:

### 1. CAS Chain Integrity
Verify that all Phase B certification artefacts exist and are readable.

### 2. Certified Objective Consistency
Confirm that the certified objective recorded in CAS-A and CAS-B is consistent.

### 3. Stationarity Condition
Verify that the equilibrium satisfies:

```
F(w*, θ) = 0
```

where

```
F(w, θ) = ∇Φ_certified(w, θ)
```

### 4. Strict‑Concave Maximiser Regime
Confirm that the certified regime in CAS-B is:

```
strict-concave maximiser
```

### 5. Hessian Negative Definiteness
Confirm that the Hessian at the equilibrium is certified as negative definite.

---

# Output Requirements

Cascade/Windsurf must generate a **Phase C Entry Report**.

Save the report in the run directory:

```
cert_artifacts/<run_id>/PhaseC_ENTRY_REPORT.md
```

---

# Required Report Structure

```
# Phase C Entry Gate Report

Run ID:
Date:
Validator Module:

## CAS Chain Verification
Status:
Files inspected:

## Certified Objective Convention
Detected convention:
Consistency status:

## Stationarity Verification
Result:

## Hessian Curvature Verification
Result:

## Certified Equilibrium Regime
Detected regime:

## Phase C Eligibility Decision
PASS / FAIL

## Blocking Issues (if any)

## Notes for Phase 0C
Recommended next actions.
```

---

# PASS Criteria

Phase C entry is approved if:

- All CAS artefacts exist
- Stationarity holds
- Regime is **strict‑concave maximiser**
- Hessian negative definiteness is certified

The report must end with:

```
Phase C Entry Gate: APPROVED
```

---

# FAIL Behaviour

If any condition fails:

- Phase C must be **blocked**
- The report must clearly describe the failing condition
- The run must be marked:

```
Phase C Entry Gate: BLOCKED
```

---

# Deliverable for ChatGPT Review

After running this step, paste the full contents of:

```
cert_artifacts/<run_id>/PhaseC_ENTRY_REPORT.md
```

into the ChatGPT conversation so Phase **0C dependency extraction** can begin.

---

# End of Instruction
