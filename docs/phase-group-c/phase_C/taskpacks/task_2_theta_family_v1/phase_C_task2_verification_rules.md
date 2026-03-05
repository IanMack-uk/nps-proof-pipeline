# Phase C — Task 2 — Verification Rules (θ-Family)

These rules define certifiable checks (candidate CAS-C lemma checks) for θ-family definition and cross-derivative computation.

---

## CHK.C2.ENTRY_GATE_APPROVED
**Definition**: Phase C entry gate must be approved for the run.

**Evidence**: `PhaseC_ENTRY_REPORT.md`.

---

## CHK.C2.THETA.DEFINITION_PRESENT
**Definition**: `THETA_FAMILY.json` exists and conforms to the Task 2 spec.

**Evidence**: run-root artefact.

---

## CHK.C2.THETA.DETERMINISTIC_LABEL_ORDER
**Definition**: θ components have stable labels and stable ordering.

**PASS criteria**:
- `labels` list is deterministic (same run inputs → same labels and order).

---

## CHK.C2.H_WTHETA.SHAPE_MATCH
**Definition**: \(H_{w\theta}\) has shape `(dim_w, theta_dim)`.

**Evidence**: `H_WTHETA.json` + metadata.

---

## CHK.C2.H_WTHETA.COMPUTED
**Definition**: `H_WTHETA.json` is computed (not missing, not placeholder).

---

## CHK.C2.H_WTHETA.SUPPORT_LOCALITY_IF_DECLARED
**Definition**: If the θ-family declares locality/sparsity, then a support statement is checked.

Example PASS criteria:
- edge-local: each column has exactly one nonzero at the corresponding edge index.
- node-local: each column nonzeros only on incident edges.
- motif-local: each column nonzeros only on edges in the motif.

---

## CHK.C2.EXPOSURE_RESPONSE.COMPATIBILITY_COMPUTED
**Definition**: Phase C exposure–response compatibility artefact is computed (not “NOT COMPUTED”).

**Evidence**: `EXPOSURE_RESPONSE_CHECK.json` in run root (if Phase C CLI writes it).

---

## CHK.C2.EXPOSURE_RESPONSE.SIGN_COMPATIBLE_WITH_INVERSE_SIGN_TOOLS
**Definition**: The sign structure of \(H_{w\theta}\) is compatible with the inverse sign structure / comparison inequalities used in Phase C.

This check depends on whatever inverse sign structure lemmas you certify (M-matrix, diagonal dominance, Neumann bounds, etc.).

PASS criteria must be explicit and declared in the Phase C report.

---

## CHK.C2.DEPENDENCY_WHITELIST.NO_NEW_MATH_IMPORTS
**Definition**: Task 2 introduces **no new mathematical imports** beyond what is already verified in `CAS-0C.json`.

If you need new tools (e.g. a new matrix inequality lemma), you must update:
- `PHASE_C_MATHEMATICAL_TOOL_WHITELIST.md`
- and re-run Phase 0C to certify them.

