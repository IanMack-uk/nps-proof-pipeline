# Phase C — Task 2 — Candidate Claim Inventory (θ-Family)

These are **idea-level** claims about what θ “should be”.
They must not be treated as VERIFIED without explicit certification.

Use these IDs to track possible θ-definitions and their required checks.

---

## Baseline cert-friendly definition (perturbation basis)
- C.CLAIM.THETA_AS_PERTURBATION_COEFFICIENTS
  - Statement: \(\Phi_{\text{cert}}(w,\theta) = \Phi_{\text{cert}}(w) + \sum_k \theta_k\Psi_k(w)\)
  - Notes: makes \(H_{w\theta}\) computable as gradients of \(\Psi_k\).

---

## Candidate θ families (structural locality variants)

### Edge-local
- C.CLAIM.THETA_EDGE_LOCAL
  - \(\Psi_e(w)=w_e\)

### Node-local
- C.CLAIM.THETA_NODE_LOCAL
  - \(\Psi_v(w)=\sum_{e\sim v} w_e\)

### Motif-local (triangle)
- C.CLAIM.THETA_MOTIF_LOCAL_TRIANGLE
  - \(\Psi_t(w)=\sum_{e\in t} w_e\)

---

## Paper-based idea claims (NOT VERIFIED)

### Paper 0
- P0.CLAIM.LOCALITY_AXIOM_IMPLIES_H_WTHETA_SUPPORT
  - locality claims should be converted into explicit support checks.

### Paper 2
- P2.CLAIM.PERTURBATION_FUNCTIONAL_PSI_EXISTS
  - Paper 2 uses perturbation \(\Phi + t\Psi\); treat as inspiration for θ definition.

### Paper 3
- P3.CLAIM.BUDGET_PERTURBATION_PARAMETER
  - if used, must be explicitly encoded and tested (likely later phase / constrained regime).

