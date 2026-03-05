# Taskpack 2 — θ-Family Definition — Cascade Instructions

## Goal

Define a **certifiable** test-parameter family \(\theta\) and compute the cross-derivative block:

\[
H_{w\theta}(w^*,\theta) = D_\theta\,\nabla_w \Phi_{\text{cert}}(w^*,\theta)
\]

so Phase C can certify exposure–response compatibility and (when all other Phase C checks pass) honestly emit:

- `Phase C Status: READY_FOR_PHASE_D`

---

## Inputs (authoritative, run root only)

Target run:
- `RUN_ID_TODO`
- Run root: `cert_artifacts/RUN_ID_TODO/`

Required:
- `CAS-A.json` (objective convention; structural basis hints)
- `CAS-B.json` (equilibrium point \(w^*\))
- `CAS-0C.json` (tool whitelist; matrix-analysis imports)
- `PhaseC_ENTRY_REPORT.md` (entry gate PASS)

Optional (ideas only; **not** verified evidence):
- Thesis and Papers 0–3 (treat as PROV sources)

---

## Outputs (write to run root)

1) `THETA_FAMILY.json` (VERIFIED definition object; schema v1)
2) `H_WTHETA.json` (computed \(H_{w\theta}\) as matrix or sparse structure)
3) `PhaseC_TASK2_THETA_FAMILY_REPORT.md`

Optionally:
- Update `EXPOSURE_RESPONSE_CHECK.json` and `CAS-C.json` (via Phase C CLI)

---

## Required repo search (Cascade must do this)

Before defining anything, search the repo for existing parameterization signals:

Keywords:
- `theta`
- `parameter`
- `exposure`
- `perturbation`
- `psi`
- `shock`
- `comparative statics`
- `dw_dtheta`
- `H_wtheta`
- `cross-derivative`
- `Dtheta`
- `budget perturbation` (Paper 3 language)

Likely locations:
- `src/nps/models/`
- `src/nps/phases/phase_a/` (structural coords)
- `src/nps/phases/phase_b/` (equilibrium objects)
- `src/nps/phases/phase_c/` (current Phase C scaffold)

If an existing θ-definition exists, reuse it and certify it (do not fork silently).

---

## Recommended mathematical definition (cert-friendly)

### Perturbation-basis θ (recommended default)

Define \(\theta\) as coefficients of a finite set of perturbation functionals \(\{\Psi_k\}\):

\[
\Phi_{\text{cert}}(w,\theta) := \Phi_{\text{cert}}(w) + \sum_{k=1}^m \theta_k\,\Psi_k(w)
\]

Then the Phase C cross-derivative block is:

\[
H_{w\theta}(w^*) = \left[\nabla_w \Psi_1(w^*)\;\cdots\;\nabla_w \Psi_m(w^*)\right]
\]

This makes \(H_{w\theta}\) computable without changing the underlying certified objective \(\Phi_{\text{cert}}(w)\).

### Candidate θ-families to support

Implement **at least** these three families:

1) **Edge-local**
- parameters: one per edge
- \(\Psi_e(w) := w_e\)
- \(\nabla_w \Psi_e = e_e\) (basis vector)
- expected \(H_{w\theta}\): identity (or a column subset)

2) **Node-local**
- parameters: one per node
- \(\Psi_v(w) := \sum_{e\sim v} w_e\)
- \(\nabla_w \Psi_v\) is the edge–node incidence indicator vector

3) **Motif-local** (triangle-local is a good first motif)
- parameters: one per triangle \(t\)
- \(\Psi_t(w) := \sum_{e\in t} w_e\) (start simple)
- \(\nabla_w \Psi_t\) is a triangle–edge incidence indicator vector

> These definitions are deliberately simple and allow you to test edge/node/motif locality with minimal risk.

If later you want “true” exposure parameters (brokerage/redundancy coefficients), add them as a separate θ-family version and keep the above as a baseline test family.

---

## What to change in code (required)

### A) Add a Θ-family module

Create:
- `src/nps/phases/phase_c/theta_family.py`

It should define:

- `class ThetaFamily(Protocol)` with:
  - `theta_family_id: str`
  - `theta_dim: int`
  - `labels: list[str]` (stable order)
  - `grad_psi_matrix(w_star, cas_a, cas_b) -> np.ndarray`  # returns H_wθ

And implement:
- `EdgeLocalThetaFamily`
- `NodeLocalThetaFamily`
- `MotifLocalThetaFamily`

### B) Determine graph / incidence data

Source of truth should come from CAS artefacts if available (preferred), otherwise from the Real Φ model spec used in Phase A/B.

You must produce a deterministic edge ordering and refer to it (Task 1 operator-layer artefact helps here).

### C) Integrate into Phase C CLI

Update `src/nps/phases/phase_c/build_casc.py`:

- load `w_star`
- choose a θ-family (default `edge_local_v1` unless overridden by CLI flag)
- compute `H_wtheta`
- write:
  - `THETA_FAMILY.json`
  - `H_WTHETA.json`
- compute exposure–response compatibility object and mark:
  - `computed: true`
  - `status: PASS/FAIL`
- only mark `READY_FOR_PHASE_D` when computed + PASS.

### D) Add tests

- test each θ-family has deterministic labels and stable dimension
- test `H_wtheta` shape is `(dim_w, theta_dim)`
- test edge-local produces an identity-like structure (or expected submatrix)
- test node-local produces expected incidence columns on a toy graph fixture

---

## Verification rules

Implement the checks in:
- `phase_C_task2_verification_rules.md`

Use the evidence rules in:
- `phase_C_task2_upstream_evidence_map.md`

If you cannot certify a θ-family choice, record it as UNVERIFIED in:
- `PROV-C_TASK2_THETA_FAMILY.json`

---

## Completion criteria (definition of “done”)

Task 2 is complete when:

- `THETA_FAMILY.json` exists in run root and is deterministic
- `H_WTHETA.json` exists in run root and matches required shape
- Exposure–response check is computed (not “NOT COMPUTED”)
- `PhaseC_TASK2_THETA_FAMILY_REPORT.md` exists and lists:
  - which θ-family was chosen
  - why it was chosen
  - which alternates remain as PROV candidates
- Phase C CLI semantics are honest (READY_FOR_PHASE_D gated on computed+PASS)

---

## Paste-back summary (for ChatGPT)

After completing, paste back:

- full contents of `PhaseC_TASK2_THETA_FAMILY_REPORT.md`
- the chosen `theta_family_id`
- the dimension `(dim_w, theta_dim)`
- git commit SHA + exact command used

