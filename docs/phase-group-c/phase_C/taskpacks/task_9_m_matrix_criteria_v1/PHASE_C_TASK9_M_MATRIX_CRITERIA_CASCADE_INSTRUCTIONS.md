# Taskpack 9 — M-Matrix Criteria and Inverse Positivity — Cascade Instructions

## Goal

Produce **deterministic, auditable artefacts** for:

- `M_MATRIX_CERT.json`
- `INVERSE_POSITIVITY_CERT.json`
- `PhaseC_TASK9_M_MATRIX_REPORT.md`

…and a run-root report:

- `PhaseC_TASK9_M_MATRIX_CRITERIA_REPORT.md`

This taskpack is **governance-sensitive**:
- Do not “verify” mathematics by reading Paper 0/1/2/3 or the thesis.
- You may *quote them as PROV ideas* in `PROV-*` artefacts only.
- VERIFIED = upstream CAS + computed checks.

---

## Target run

- Run ID: `RUN_ID_TODO`
- Run root: `cert_artifacts/RUN_ID_TODO/`

---

## Required repo search (Cascade must do this)

Search for existing implementations before adding new code.

Suggested search terms:
- `m matrix criteria`
- `hessian` / `HESSIAN_`
- `block` / `partition`
- `dominance` / `diagonal dominance`
- `comparison` / `Z-matrix` / `M-matrix`
- `Neumann` / `||A|| < 1`
- `inverse sign` / `susceptibility`
- `H_wtheta` / `cross-derivative`
- `dw_dtheta`

Suggested locations:
- `src/nps/phases/phase_c/`
- `src/nps/models/`
- `src/nps/audit/`
- `src/nps/certification/`

If an implementation already exists, **reuse it** and add checks/reporting instead of forking.

---

## Procedure (high-level)

1. **Load authoritative inputs** from the run root only.
2. If this task depends on earlier taskpack artefacts, verify they exist (fail loudly if not).
3. Compute the required quantities deterministically.
4. Run the verification rules in `phase_C_task9_verification_rules.md`.
5. Write artefacts to the run root.
6. Write the report using `phaseC_TASK9_REPORT_TEMPLATE.md`.

---

## Required check IDs

Your output JSON must contain results for these check IDs:

- `CHK.C9.MMATRIX.PRECONDITIONS_PASS`
- `CHK.C9.MMATRIX.NONSINGULAR_CONCLUDED`
- `CHK.C9.INVERSE.NONNEGATIVE_CONCLUDED`

---

## Output schema

Conform to:
- `CAS-C_TASK9_SPEC.md` for VERIFIED artefacts
- `PROV-C_TASK9_SPEC.md` for any unverified candidates

---

## Commit policy (recommended)

- Commit code + docs.
- Prefer a run transcript doc under:
  - `docs/phase-group-c/phase_C/RUNS/RUN_ID_TODO.md`
- Do **not** commit `cert_artifacts/` outputs unless you have an explicit exception policy.

