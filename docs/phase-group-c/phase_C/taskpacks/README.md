# Phase C Taskpacks (Templates)

This folder contains **Cascade-ready taskpack templates** for Phase C.

Each taskpack is designed to be copied into:

- `docs/phase-group-c/phase_C/taskpacks/<taskpack>/`

…and then pinned to a specific `RUN=<run_id>` before execution.

These templates align with:

- **Computational Certification Architect role constraints** (phase isolation, explicit assumptions, auditable artefacts, loud failures).
- **Phase Group C repo usage guide** (governance gates, canonical run-root chain, `PYTHONPATH=src python -m ...` workflow).

---

## What’s in here (Taskpacks 1–12)

### Taskpack 1 — Operator layer
`task_1_operator_layer_v1/`

Certifies the **objects + conventions layer**:
- What is the equilibrium operator?
- What is the certified objective convention (Φ vs −Φ)?
- What is the structural-coordinate basis / index map?
- What is the Hessian object in that basis (shape, symmetry, sign convention)?

### Taskpack 2 — θ-family definition
`task_2_theta_family_v1/`

Defines and certifies the **test-parameter family θ** (edge-local / node-local / motif-local / other) and makes the cross-derivative block

\[
H_{w\theta}(w^*,\theta) = D_\theta\,\nabla_w \Phi_{\text{cert}}(w^*,\theta)
\]

exist as a computed artefact (so exposure–response compatibility can be certified).

### Taskpack 3 — Hessian computation artefacts
`task_3_hessian_artifacts_v1/`

Makes Hessian computation **audit-grade**:
- computed at the certified equilibrium
- expressed in the structural basis
- schema-stable artefact + explicit verification checks

### Taskpack 4 — Structural block decomposition
`task_4_block_decomposition_v1/`

Defines a deterministic **block partition** of the Hessian induced by Phase A structural coordinates (and later exposure groupings).

### Taskpack 5 — Locality and sparsity support bounds
`task_5_locality_sparsity_v1/`

Certifies (run-specific) sparsity/locality support statements:
- sparsity metrics
- neighbourhood-radius support tests

> Note: global locality axioms remain PROV unless separately proven/certified.

### Taskpack 6 — Diagonal dominance certification
`task_6_diagonal_dominance_v1/`

Computes and certifies strict (or block) diagonal-dominance margins for the coupling matrix or relevant blocks.

### Taskpack 7 — Comparison inequalities and Z-matrix sign pattern
`task_7_comparison_inequalities_v1/`

Certifies sign-pattern prerequisites (e.g., off-diagonals ≤ 0) and other comparison preconditions needed for inverse-sign conclusions.

### Taskpack 8 — Neumann-series inversion bounds
`task_8_neumann_series_bounds_v1/`

Certifies invertibility and inverse bounds via Neumann-series criteria using whitelist-compliant finite-dimensional norms.

### Taskpack 9 — M-matrix criteria and inverse positivity
`task_9_m_matrix_criteria_v1/`

If whitelist posture allows, combines Task 6 + 7 results to certify M-matrix conditions and infer inverse sign structure.

### Taskpack 10 — Selected inverse entries and Phase D interface
`task_10_selected_inverse_entries_v1/`

Defines *which inverse entries/blocks actually matter* for Phase D, and certifies sign conclusions for that selected subset.

### Taskpack 11 — Exposure–response compatibility and scaling
`task_11_exposure_response_compatibility_v1/`

Computes/validates:
- sign structure of `H_{w\theta}`
- compatibility with inverse-sign conclusions
- response sign predictions + scaling bounds

This is the **honest gate** for `READY_FOR_PHASE_D`.

### Taskpack 12 — CAS-C integrity and minimality (drop-test)
`task_12_cas_c_integrity_minimality_v1/`

Assembles `CAS-C.json` and performs:
- schema + completeness checks
- minimality/drop-test audit (similar to CAS-0C)

---

## How to use (generic)

1. Copy one taskpack folder (or keep them all).
2. Pin a target run id:
   - replace every `RUN_ID_TODO` placeholder with your actual run id (e.g. `2026-03-04T211059Z`)
3. Run under governance gates:
   - `NPS_IMPORT_FIREWALL=1`
   - `NPS_CAS_GATE=1`
   - `NPS_CERT_DEP_GATE=1`
   - `NPS_RUN_DIR_INTEGRITY=1`
4. Commit **code + docs only** (preferably not `cert_artifacts/` outputs unless you have an explicit repo policy for them).
5. For run outputs, commit a **run transcript doc**:
   - `docs/phase-group-c/phase_C/RUNS/<run_id>.md`

---

## Governance reminder

- Do **not** mark Paper 0/1/2/3 statements as VERIFIED by “reading the paper”.
- Papers are **idea documents**; verification must come from:
  - upstream CAS artefacts,
  - explicit computational checks,
  - or separately certified mathematical imports (Phase 0C whitelist).

