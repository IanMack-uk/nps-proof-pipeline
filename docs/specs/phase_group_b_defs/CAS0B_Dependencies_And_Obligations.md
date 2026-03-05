# CAS-0B Dependencies + Obligations (Phase B conventions locked)

This file converts the verbatim extracts into a **machine-trackable** set of dependencies and obligations for **Phase 0B**.
It is designed to be pasted into (or generated as) `CAS-0B.json` under `dependency_table` and `obligations`.

## Conventions (non-negotiable)
- **Equilibrium is defined under a maximisation convention** (local maximiser of Φ on the feasible set; interior regime uses stationarity).
- **Operator formulation for Phase B** is finite-dimensional:
  - `F(w) := ∇Φ(w)` (marginal structural field)
  - `J(w) := ∇F(w) = ∇²Φ(w)` (Hessian operator / linearisation)
- **Nondegeneracy regime split**:
  - *Strict concavity regime*: `J(w*) ≺ 0` (negative definite) ⇒ strict local maximiser.
  - *Hyperbolic regime*: `det J(w*) ≠ 0` (invertible) ⇒ IFT-style local branch regularity, but not necessarily a maximiser.

## Dependency table entries

### DEP.P1.DEF.MARGINAL_STRUCTURAL_FIELD
- **Type:** definition
- **Source:** Paper 1 (Operator Theory) — “Definition (Marginal Structural Field)”
- **Locator:** Paper 1 `NetworkPotential_Paper1_OperatorTheory_v0.6` — Section 2.1, Definition 2.1.1
- **Provides:** the operator `F(w)` as the first derivative / marginal field associated with Φ
- **Used in:** Phase B.1 (equilibrium condition as `F(w)=0`), Phase B.2 (regularity / linearisation), Phase B.4 (response identity)

### DEP.P1.DEF.HESSIAN_OPERATOR
- **Type:** definition
- **Source:** Paper 1 (Operator Theory) — “Definition (Hessian Operator)”
- **Locator:** Paper 1 `NetworkPotential_Paper1_OperatorTheory_v0.6` — Section 2.2, Definition 2.2.1
- **Provides:** the linear operator / Jacobian `J(w)` as second derivative / Hessian operator
- **Used in:** Phase B.2–B.4; Phase B′ algebraic closure

### DEP.P1.DEF.HYPERBOLIC_EQUILIBRIUM
- **Type:** definition
- **Source:** Paper 1 (Operator Theory) — “hyperbolic equilibrium” definition text
- **Locator:** Paper 1 `NetworkPotential_Paper1_OperatorTheory_v0.6` — Section 2.4, Definition 2.4.2
- **Provides:** the nondegeneracy criterion `det J(w*) ≠ 0`
- **Used in:** Phase B.2–B.3 (IFT applicability; response identity well-defined)

### DEP.P1.IDENTITY.SUSCEPTIBILITY_RESPONSE
- **Type:** identity / theorem statement (draft)
- **Source:** Paper 1 (Operator Theory) — susceptibility / response identity section
- **Locator:** Paper 1 `NetworkPotential_Paper1_OperatorTheory_v0.6` — Section 2.4–2.5 discussion
- **Provides:** response identity of the form `dw*/dθ = - J(w*)^{-1} (∂F/∂θ)` (exact sign must match maximisation convention)
- **Used in:** Phase B.4 and Phase B′ re-derivation

### DEP.THESIS.PROB.MAXIMISATION_STATEMENT
- **Type:** problem statement / modelling convention
- **Source:** Core thesis — maximisation problem statement section
- **Locator:** see definition blocks doc
- **Provides:** global convention “equilibrium = (local) maximiser of Φ”, establishing sign conventions for first/second order conditions
- **Used in:** Phase B regime choice (stationarity + negative definiteness for strict local maxima)

## Obligations (to discharge in Phase B/B′)

Each obligation is an auditable claim that must be either:
- **discharged** by checkers on the chosen Φ instance, or
- **explicitly assumed** in CAS-B (with scope tags) if not mechanically discharged.

### OBL.B.REGIME.INTERIOR
- **Statement:** The equilibrium candidate is interior: `w* ∈ W°`.
- **Discharge:** `CHK.A.INTERIOR_FEASIBILITY` at `w*`.

### OBL.B.EQ.STATIONARITY
- **Statement:** Interior equilibrium satisfies `F(w*) = ∇Φ(w*) = 0`.
- **Discharge:** `CHK.A.STATIONARITY` at `w*`.

### OBL.B.NONDEGEN.HYPERBOLIC
- **Statement:** Hyperbolicity holds: `det J(w*) ≠ 0` (equivalently min |eig(J)| > eps).
- **Discharge:** `CHK.B.JACOBIAN_CONDITIONING` witness `is_hyperbolic=true`.

### OBL.B.NONDEGEN.STRICT_CONCAVITY (optional regime)
- **Statement:** Strict concavity holds: `J(w*) ≺ 0`.
- **Discharge:** `CHK.A.NEG_DEF_HESSIAN` at `w*` or Phase-B equivalent; witness `is_strictly_concave=true`.
- **If fails:** CAS-B must explicitly choose hyperbolic regime and must not claim “strict local maximiser” consequences.

### OBL.B.RESPONSE.IDENTITY.SIGN
- **Statement:** The response identity sign matches the maximisation convention.
- **Discharge:** Phase B′ independent derivation + automated algebra check on toy harness; on Real Φ, confirm via finite-difference parameter perturbation sanity check.

---

## What to do with this file
- Commit the verbatim blocks doc and this dependency/obligation doc.
- Update `phase_0b.build_cas0b` so `CAS-0B.json` includes these deps + obligations with locators pointing to paragraph indices.
