# Task B.2.1 — Phase Group B Definition Blocks → CAS-0B Dependencies + Obligations

## Goal
Lock Phase B conventions **unambiguously** by extracting the exact definition blocks from:
- `NetworkPotential_Paper1_OperatorTheory_v0.6.docx` (Paper 1)
- `Network-Potential-and-Relational-Optimisation-mathematics-thesis.docx` (Core thesis)

and converting them into:
1) a verbatim “definition blocks” artefact
2) a CAS-0B “dependencies + obligations” artefact ready to be embedded into `CAS-0B.json`.

## Deliverables
Add (repo):
- `docs/specs/phase_group_b_defs/Paper1_Thesis_Definition_Blocks.md`
- `docs/specs/phase_group_b_defs/CAS0B_Dependencies_And_Obligations.md`

Copy them from this taskpack’s `ARTIFACTS/` folder.

## Wiring requirement (minimal change)
Update `src/nps/phases/phase_0b/build_cas0b.py` so that:
- `CAS-0B.json` includes a `dependency_table` entries corresponding to the DEP.* IDs in `CAS0B_Dependencies_And_Obligations.md`
- `CAS-0B.json` includes an `obligations` section listing the OBL.* items

Locators must point to paragraph indices in `Paper1_Thesis_Definition_Blocks.md`.

## Verification
- Run:
  - `pytest -q`
  - `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`
- Create a persistent run and confirm `CAS-0B.json` now contains:
  - `DEP.P1.DEF.MARGINAL_STRUCTURAL_FIELD`
  - `DEP.P1.DEF.HESSIAN_OPERATOR`
  - `DEP.P1.DEF.HYPERBOLIC_EQUILIBRIUM`
  - `DEP.P1.IDENTITY.SUSCEPTIBILITY_RESPONSE`
  - `DEP.THESIS.PROB.MAXIMISATION_STATEMENT`
  - and obligations OBL.B.* as specified.

## Reporting
Write:
- `cascade_taskpack_structural_differentiation_v4.3/TASKS/task_B_2_1_phase_group_b_defs_to_cas0b/REPORT.md`

Include:
- files added/changed
- commands run
- excerpt of CAS-0B dependency_table IDs and obligation IDs
