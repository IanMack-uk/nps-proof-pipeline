# Canonical “Real Φ v0” specification (certification-ready)

This file turns the verbatim extracts into **Phase-A/B certification-ready objects** to implement in Python.

## Objects

### Configuration space
Let a fixed finite graph be **G = (V, E)** with |E| = m edges.
Define the configuration vector **w ∈ W = [0,1]^m**, with interior **W° = (0,1)^m**.

### Structural exposure (edge-level)
For an undirected edge **e = (i,j)**:

- Neighbour overlap: κ_e(G) = |N(i) ∩ N(j)|
- Fix a strictly decreasing function f: N → R_+.
- Brokerage index: B_e(G) := f(κ_e(G))
- Redundancy index: R_e(G,w) := Σ_{k ∈ N(i) ∩ N(j)} w_{ik} w_{jk}

We treat the structural exposure map as:
> Exp_e(G,w) := (B_e(G), R_e(G,w))

### Relational / Network Potential Φ
We adopt the thesis definitions (global Φ with node-level NPF_i):

#### Node-level components (for node i)
Let Γ(i) denote the neighbour set of i, and p ≥ 1.

- Cohesion:
  - A_i(w) := Σ_{j ∈ Γ(i)} w_{ij}^p
- Brokerage-weighted weak-tie mass:
  - M_i(w) := Σ_{j ∈ Γ(i)} (1 - w_{ij})^p · B_{ij}(G)
- Redundancy / closure:
  - R_i(w) := Σ_{ {j,k} ⊆ Γ(i) } w_{ij}^p w_{ik}^p · 1_E(j,k)

#### Node potential (parameters θ_A, θ_M, θ_R ≥ 0)
NPF_i(w) := θ_A log(1 + A_i(w)) + θ_M log(1 + M_i(w)) - θ_R log(1 + R_i(w))

#### Global potential
Φ(w) := Σ_{i ∈ V} NPF_i(w)

## Equilibrium (Phase B regime)
We use Paper 2’s interior regime:

- Stationary point: w ∈ W° satisfies ∇Φ(w) = 0
- Strict local maximiser: w* ∈ W° stationary and Φ(w) < Φ(w*) for all feasible w near w*

## Operator formulation (Phase B)
Define:
- F(w) := ∇Φ(w)
- J(w) := ∂F/∂w = ∇²Φ(w)

Incident Hessian operator at node i (Paper 2):
- H_i(w) := P_i H(w) ι_i : R^{E(i)} → R^{E(i)}
where H(w) is the full Hessian and E(i) is the incident edge set.

## Implementation contract (for the codebase)
The Python model must expose:

- value(w) -> float
- grad(w) -> (m,) array  (analytic, not FD)
- hess(w) -> (m,m) array (analytic, not FD)
- exposure_edge(e, w) -> (B_e, R_e)

And must record:
- derivative_definition.extension_id = "real_phi_v0"

## Known “v0” limitations (explicitly allowed)
- The papers are drafts; if a symbol is under-specified, choose a canonical interpretation and record it in the Phase reports as a SPEC_V0_CHOICE note.
- Start with a small graph (m ≤ 12) so Hessians are cheap and FD checks are stable.
