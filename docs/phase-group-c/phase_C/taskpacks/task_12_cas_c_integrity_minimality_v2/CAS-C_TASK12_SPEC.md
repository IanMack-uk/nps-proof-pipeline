# Phase C — Taskpack 12
# CAS‑C Integrity, Minimality, and Phase‑D Readiness (v2)

## Purpose

Taskpack 12 is the **closure gate** for Phase Group C.

It produces the canonical Phase‑C certified artefact:

- `CAS-C.json`

and verifies, with audit‑grade rigor, that:

1. **Integrity** — all Phase C taskpacks required for Phase‑D reliance are present, PASS, schema‑valid, and cross‑consistent.
2. **Minimality** — every exported CAS‑C claim is supported by a *necessary* upstream artefact and check; run a systematic drop test to prevent hidden imports and accidental reliance on redundant conditions.
3. **Readiness** — emits a single authoritative verdict:
   - `READY_FOR_PHASE_D = YES|NO`
   - with explicit reasons and blocking failures.

This taskpack is designed so Phase D can cite **CAS‑C** as a single object containing:
- the certified regime (strict‑concave, maximize, convention lock),
- the certified inverse‑sign structure and response interface properties,
- and the dependency graph linking every exported claim to a concrete upstream witness.

---

## Inputs (run directory)

Taskpack 12 operates on a **single run directory**:

`cert_artifacts/<RUN>/`

It reads the Phase C taskpack artefacts (Tasks 1–11) and their reports/check metadata.

Required upstream artefacts (minimum for Phase‑D reliance):

- Task 1: `OPERATOR_LAYER.json` (or equivalent Task‑1 output)
- Task 2: `THETA_FAMILY.json`, `H_WTHETA.json`
- Task 3: `HESSIAN_MATRIX.json` (or `HESSIAN_ARTIFACTS.json`)
- Task 4: `BLOCK_DECOMP.json`
- Task 5: `SPARSITY_STRUCTURE.json`
- Task 6: `DIAGONAL_DOMINANCE.json`
- Task 7: `COMPARISON_INEQUALITIES.json`
- Task 8: `NEUMANN_SERIES_BOUND.json`
- Task 9: `M_MATRIX_CERTIFICATE.json`
- Task 10: `SELECTED_INVERSE_ENTRIES.json`
- Task 11: `EXPOSURE_RESPONSE_CHECK.json`, `RESPONSE_SIGN_PREDICTIONS.json`, `SCALING_BOUNDS.json`

Plus the Phase C task reports `PhaseC_TASK*_REPORT.md` where present.

> Note: Exact filenames may vary by repo evolution. Taskpack 12 must locate artefacts via a *declared manifest* (see Execution Guide).

---

## Outputs

Taskpack 12 writes into the **run root**:

1. `CAS-C.json`  
2. `PhaseC_REPORT.md`  
3. `PhaseC_DROP_TEST_REPORT.md`  
4. `CAS-C_MANIFEST.json` (new) — explicit list of all consumed artefacts with hashes

All outputs must be deterministic for a given run directory.

---

## CAS‑C Contents (what Phase D is allowed to rely on)

`CAS-C.json` must contain:

### A) Provenance & regime lock
- `run_id`
- `certified_objective` (phi / minus-phi)
- `objective_direction` (maximize)
- `equilibrium_regime` (strict_concave)
- `phase_c_entry_gate_passed` (true)

### B) Exported claims (Phase‑D interface)
Export a finite list of claims, each with:
- a stable `claim_id`
- a precise statement
- `strength`: {theorem_level, lemma_level, metadata}
- `depends_on`: list of upstream `check_id`s and artefact paths
- `witness`: pointers to concrete numeric witnesses (e.g. rho_bound, violations counts)

Minimum exported claims recommended for Phase D:
- `C.CURVATURE.NEG_DEF_AT_WSTAR` (or equivalent strict concavity witness)
- `C.MATRIX.Z_MATRIX` (off-diagonal nonpositive of C := -H, as certified)
- `C.MATRIX.M_MATRIX_NONSINGULAR` (Task 9)
- `C.INV_H.NONNEGATIVE_ENTRYWISE` (Task 9 conclusion)
- `C.RESPONSE.IDENTITY.WELL_POSED` (Task 11)
- `C.RESPONSE.SIGN.DETERMINATE_FOR_SELECTED` (Task 11 + Task 10)
- `C.RESPONSE.NORM.BOUNDED` (Task 11 + Task 8)

### C) Dependency graph snapshot
- a compact representation of claim → checks → artefacts
- a declared “no hidden dependencies” statement supported by the drop test

---

## Pass Criteria

Taskpack 12 is PASS iff:

1. All required upstream taskpacks (1–11) are present and PASS.
2. All schemas validate for the consumed artefacts (by schema_version and required fields).
3. Cross‑consistency checks succeed (dimensions, run_id, convention lock, regime).
4. Drop test passes: removing any **declared required dependency** breaks at least one exported claim (or the claim set is reduced accordingly).
5. The produced `CAS-C.json` is schema‑valid and internally consistent.
6. `READY_FOR_PHASE_D == YES`.

Any failure yields:
- `READY_FOR_PHASE_D == NO`
- and explicit blocking reasons.

---

## Governance constraints

- Do not recompute Phase C mathematics.
- Do not relax assumptions silently.
- Do not infer claims not supported by a recorded witness.
- Do not rely on file timestamps; rely on content hashes + schema_version.
- Keep run root canonical: only one CAS‑C per run directory.
