# Task B.2.1 — Phase Group B Definition Blocks → CAS-0B Dependencies + Obligations — Report

## Files added/changed

- `docs/specs/phase_group_b_defs/Paper1_Thesis_Definition_Blocks.md`
- `docs/specs/phase_group_b_defs/CAS0B_Dependencies_And_Obligations.md`
- `src/nps/phases/phase_0b/build_cas0b.py`

## Commands run

- `pytest -q`
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`
- `PYTHONPATH=src python -m nps.phases.phase_0b.build_cas0b --input cert_artifacts/2026-03-04T172947Z/CAS-A.json`

## Persistent run

- Run dir: `cert_artifacts/2026-03-04T180551Z/`
- Artefact: `cert_artifacts/2026-03-04T180551Z/CAS-0B.json`

## CAS-0B excerpt (dependency_table IDs)

The following `dependency_table[*].dep_id` entries are now present in `CAS-0B.json`:

- `DEP.P1.DEF.MARGINAL_STRUCTURAL_FIELD`
- `DEP.P1.DEF.HESSIAN_OPERATOR`
- `DEP.P1.DEF.HYPERBOLIC_EQUILIBRIUM`
- `DEP.P1.IDENTITY.SUSCEPTIBILITY_RESPONSE`
- `DEP.THESIS.PROB.MAXIMISATION_STATEMENT`

## CAS-0B excerpt (obligation IDs)

The following Phase-B convention obligations are now present in `CAS-0B.json` under `obligations`:

- `OBL.B.REGIME.INTERIOR`
- `OBL.B.EQ.STATIONARITY`
- `OBL.B.NONDEGEN.HYPERBOLIC`
- `OBL.B.NONDEGEN.STRICT_CONCAVITY`
- `OBL.B.RESPONSE.IDENTITY.SIGN`
