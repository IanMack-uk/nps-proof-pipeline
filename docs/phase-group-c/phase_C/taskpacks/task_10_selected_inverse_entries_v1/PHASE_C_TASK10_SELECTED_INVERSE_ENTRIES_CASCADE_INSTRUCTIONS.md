
---

### 2) `PHASE_C_TASK10_SELECTED_INVERSE_ENTRIES_CASCADE_INSTRUCTIONS_FINAL.md`
```md
# Phase C Taskpack 10 — Selected Inverse Entries (FINAL) — Cascade Instructions

**Taskpack ID:** C-TASK10  
**Schema Version:** C-TASK10.v2  
**Depends on:** Taskpack 4 + (Taskpack 9 OR Taskpack 8)  
**Outputs:**  
- `SELECTED_INVERSE_ENTRIES.json`  
- `PhaseC_TASK10_SELECTED_INVERSE_ENTRIES_REPORT.md`

---

## Objective

Extend `src/nps/phases/phase_c/build_casc.py` so that a normal Phase C run also produces Taskpack 10 artefacts in the run root.

This step must be:
- deterministic
- auditable (explicit selection + witnesses)
- governance-clean (no paper/thesis “verification”)

Do NOT change:
- CAS-C gating
- READY_FOR_PHASE_D semantics

---

## Concrete inputs (run root only)

Read:
- `HESSIAN_BLOCKS.json` → `dimension` and `blocks["w_w"]` size
- inverse-sign source (prefer Task 9):
  - `INVERSE_POSITIVITY_CERT.json`
  - else `NEUMANN_SERIES_BOUND.json`

Optional:
- `THETA_FAMILY.json` only if the selection rule uses θ labels.

FAIL loudly if required inputs are missing.

---

## Definitions (must be explicit)

Let `H := HESSIAN_BLOCKS.json.blocks["w_w"]`.  
Define coupling matrix: `C := -H`.

Task 9 provides the certified sign conclusion for `C^{-1}` (preferred).  
Task 10 must record whether it certifies signs for `C^{-1}` or `H^{-1}` and remain consistent.

Recommended: certify `sign(C^{-1})`.

---

## Selection rule (minimal + deterministic)

Default rule (recommended):
- `pairs = [(i,i) for i in range(dimension)]`
- `indices = [0,1,...,dimension-1]`

This is deterministic, nonempty, and certified if Task 9 says `C^{-1} ≥ 0` entrywise.

Keep `pairs` explicit even if you later refine the rule.

---

## Required checks (canonical structure)

Use `{id, ok, status, details}`.

### CHK.C10.SELECTION.RULE_DEFINED
PASS iff:
- rule_id + rule_text present
- selected pairs nonempty
- indices/pairs in range

### CHK.C10.SELECTION.DETERMINISTIC
PASS iff:
- pairs lexicographically sorted; indices sorted unique
- selection_hash matches sha256(canonical(selection.selected))

### CHK.C10.SELECTED_SIGNS.CERTIFIED
PASS iff:
- inverse-sign source is Task 9 and indicates entrywise nonnegative, AND
- every selected pair has sign="+" and source="INVERSE_POSITIVITY_CERT"

Else FAIL.

---

## Outputs

Write to run root:
- `SELECTED_INVERSE_ENTRIES.json` (schema C-TASK10.v2)
- `PhaseC_TASK10_SELECTED_INVERSE_ENTRIES_REPORT.md` (use the template)

Do not commit cert_artifacts outputs.

---

## Execution (example)

```bash
export NPS_IMPORT_FIREWALL=1
export NPS_CAS_GATE=1
export NPS_CERT_DEP_GATE=1
export NPS_RUN_DIR_INTEGRITY=1

RUN=2026-03-04T211059Z
PYTHONPATH=src python -m nps.phases.phase_c.build_casc \
  --run-id "$RUN" \
  --run-root "cert_artifacts/$RUN"