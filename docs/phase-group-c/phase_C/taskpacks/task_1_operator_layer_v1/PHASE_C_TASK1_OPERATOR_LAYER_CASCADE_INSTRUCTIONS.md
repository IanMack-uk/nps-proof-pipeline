# Taskpack 1 — Operator Layer — Cascade Instructions

## Goal

Create an auditable, deterministic “operator layer” artefact for Phase C:

- Define the certified objective \(\Phi_{\text{cert}}\) and its sign convention (Φ vs −Φ).
- Define the equilibrium operator used in Phase C:
  - baseline: \(F(w,\theta) := \nabla_w \Phi_{\text{cert}}(w,\theta)\)
- Pin the equilibrium point \(w^*\) from `CAS-B.json`.
- Pin the structural-coordinate basis from Phase A (index map / permutation).
- Define the Phase C coupling matrix convention:
  - usually \(C := -H\) where \(H := \nabla^2_w\Phi_{\text{cert}}(w^*,\theta)\)
- Verify basic well-posedness invariants (dimension, symmetry, regime tags).
- Write a report + JSON artefact so later Phase C lemmas can reference it without ambiguity.

This taskpack is intended to support Phase C steps:
1) compute Hessian in structural basis,
2) block decomposition,
3) dominance/comparison hypotheses,
4) inverse sign structure,
5) exposure–response compatibility.

---

## Inputs (authoritative, run root only)

Target run:
- `RUN_ID_TODO`
- Run root: `cert_artifacts/RUN_ID_TODO/`

Required files:
- `cert_artifacts/RUN_ID_TODO/PhaseC_ENTRY_REPORT.md`
- `cert_artifacts/RUN_ID_TODO/CAS-A.json`
- `cert_artifacts/RUN_ID_TODO/CAS-B.json`
- `cert_artifacts/RUN_ID_TODO/CAS-0C.json` (if present; tool whitelist + dependency context)

**Do not** use `experiments/` outputs as VERIFIED evidence.

---

## Outputs (write to run root)

1) `OPERATOR_LAYER.json`

A deterministic object capturing:
- run id, creation timestamp
- objective convention (`phi` or `minus_phi`)
- equilibrium operator definition (string + metadata)
- equilibrium point reference:
  - `w_star_ref`: (path into CAS-B fields)
  - `dim_w`
- structural-coordinate basis:
  - `basis_id`
  - `edge_order` (list of edge ids if available)
  - `permutation_P` (optional; list[int] mapping raw → structural)
- hessian convention:
  - `H_definition`: `"H = d2/dw2 Phi_cert (w_star, theta)"` (string)
  - `C_definition`: `"C = -H"` (string)
- verification checks:
  - list of `{check_id, ok, details}`

2) `PhaseC_TASK1_OPERATOR_LAYER_REPORT.md`

Use `phaseC_TASK1_REPORT_TEMPLATE.md`.

---

## What to change in code (preferred path)

### A) Add / reuse a Phase C helper module

Create (or extend) a module near Phase C, for example:
- `src/nps/phases/phase_c/operator_layer.py`

It should expose:

- `build_operator_layer(run_root: Path) -> dict`
- `validate_operator_layer(operator_layer: dict) -> list[dict]` (check results)
- `write_operator_layer(run_root: Path, operator_layer: dict) -> Path`

### B) Integrate into Phase C CLI (if applicable)

If Phase C already has:
- `src/nps/phases/phase_c/build_casc.py`

then:
- call `build_operator_layer(...)`
- write `OPERATOR_LAYER.json`
- append a summary block to `PhaseC_REPORT.md`

### C) Add minimal unit tests

Add tests that:
- load fixture CAS-A/CAS-B JSONs (can use small toy fixtures)
- ensure operator_layer validation catches:
  - dimension mismatch
  - missing objective convention
  - inconsistent maximize/minus_phi sign conventions

---

## Verification rules (must follow)

Implement the checks defined in:
- `phase_C_task1_verification_rules.md`

Use upstream evidence rules from:
- `phase_C_task1_upstream_evidence_map.md`

Any statement not supported by an upstream artefact or an explicit computational check must be classified as **UNVERIFIED** and moved to a PROV-style record (do not silently “assume”).

---

## Required repo search (Cascade must do this)

Search for how Phase A encodes “structural coordinates” / basis ordering.

Look for any of:
- fields in `CAS-A.json` like:
  - `structural_coordinates`
  - `edge_index_map`
  - `structural_basis`
  - `indexing`
- code keywords:
  - `structural`
  - `edge_order`
  - `coordinate`
  - `permutation`
  - `basis`
- likely locations:
  - `src/nps/phases/phase_a/`
  - `src/nps/models/`

If **no basis map exists** upstream, then Task 1 must produce:
- a deterministic definition of the basis ordering used in Phase C,
- and record it explicitly in `OPERATOR_LAYER.json`.

---

## Completion criteria (definition of “done”)

Task 1 is complete when:

- `OPERATOR_LAYER.json` exists in the run root
- `PhaseC_TASK1_OPERATOR_LAYER_REPORT.md` exists in the run root
- All checks in `phase_C_task1_verification_rules.md` are implemented and PASS **or** are explicitly FAIL with explanation
- Any FAIL that would affect Phase C downstream lemmas is clearly marked as **BLOCKER**

---

## Paste-back summary (for ChatGPT)

After running, paste back:

- the full contents of `PhaseC_TASK1_OPERATOR_LAYER_REPORT.md`
- the list of check IDs with PASS/FAIL
- the git commit SHA and the exact command used (if applicable)

