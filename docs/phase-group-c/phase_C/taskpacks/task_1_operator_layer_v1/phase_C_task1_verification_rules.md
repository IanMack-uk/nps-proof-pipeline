# Phase C — Task 1 — Verification Rules (Operator Layer)

These rules define certifiable checks (candidate CAS-C lemma checks) for the **operator layer**.

Each rule should become either:
- a concrete computational check in code, or
- an upstream-evidence check that reads an earlier CAS artefact / gate report.

If a rule cannot be checked, it must be explicitly marked UNVERIFIED (do not silently pass).

---

## CHK.C1.ENTRY_GATE_APPROVED
**Definition**: Phase C is only entered if Step 1 entry gate report ends with `Phase C Entry Gate: APPROVED`.

**Evidence**: `PhaseC_ENTRY_REPORT.md` in run root.

---

## CHK.C1.CONVENTION.CERTIFIED_OBJECTIVE_PRESENT
**Definition**: `CAS-A.json` declares a certified objective convention (`phi` or `minus_phi`).

**Evidence**: `CAS-A.json` field(s).

---

## CHK.C1.CONVENTION.CERTIFIED_OBJECTIVE_MATCHES_CASB
**Definition**: `CAS-A` and `CAS-B` agree on certified objective convention.

**Evidence**: `CAS-A.json`, `CAS-B.json`.

---

## CHK.C1.REGIME.STRICT_CONCAVE_MAXIMIZE
**Definition**: `CAS-B` declares the interior strict-concave maximiser regime:
- `equilibrium_objective == "maximize"`
- `equilibrium_regime == "strict_concave"`

**Evidence**: `CAS-B.json`.

---

## CHK.C1.EQUILIBRIUM_POINT.W_STAR_PRESENT
**Definition**: `CAS-B` provides an equilibrium point `w_star` (or an equivalent field) and its dimension is consistent across artefacts.

**Evidence**: `CAS-B.json`.

---

## CHK.C1.BASIS.STRUCTURAL_COORDINATE_MAP_DETERMINISTIC
**Definition**: There exists a deterministic structural-coordinate basis definition used for Phase C Hessian representation.

**PASS criteria**:
- either `CAS-A.json` provides an explicit basis mapping (ordering / permutation), or
- Phase C defines and records an explicit deterministic ordering rule in `OPERATOR_LAYER.json`.

---

## CHK.C1.HESSIAN.SHAPE_MATCHES_DIM_W
**Definition**: Hessian dimension is \(\dim(w) \times \dim(w)\).

**Evidence**: computed (from Hessian artefact or direct computation).

---

## CHK.C1.HESSIAN.SYMMETRIC
**Definition**: Hessian is symmetric within numeric tolerance (if computed numerically) or exactly (if analytic).

**Evidence**: computed.

---

## CHK.C1.SIGN_CONVENTION.COUPLING_MATRIX_DEFINED
**Definition**: The sign convention for coupling matrix is pinned:
- `H := ∇²_w Φ_cert`
- `C := -H` (if used later for M-matrix / diagonal dominance)

**Evidence**: `OPERATOR_LAYER.json` must contain both strings + a check that they are consistent with maximize/minus_phi.

---

## CHK.C1.DEPENDENCY_WHITELIST.COMPLETE
**Definition**: If Task 1 introduces matrix-analysis tools or relies on them, they must be listed in `CAS-0C.json` `verified_imports` with `source_ref: PHASE_C_MATHEMATICAL_TOOL_WHITELIST`.

**Evidence**: `CAS-0C.json` (if present). Otherwise mark as UNVERIFIED and BLOCK Phase C checks that depend on it.

