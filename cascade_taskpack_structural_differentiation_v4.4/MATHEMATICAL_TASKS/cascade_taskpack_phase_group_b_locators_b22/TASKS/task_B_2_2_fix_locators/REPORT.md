# Task B.2.2 — Fix CAS‑0B Paper‑1 Definition Locators — Report

## Files changed

- `docs/specs/phase_group_b_defs/CAS0B_Dependencies_And_Obligations.md`
- `src/nps/phases/phase_0b/build_cas0b.py`

## Locator mappings applied (authoritative)

Paper: `NetworkPotential_Paper1_OperatorTheory_v0.6`

- `DEP.P1.DEF.MARGINAL_STRUCTURAL_FIELD`
  - `section`: `2.1`
  - `definition`: `2.1.1`
- `DEP.P1.DEF.HESSIAN_OPERATOR`
  - `section`: `2.2`
  - `definition`: `2.2.1`
- `DEP.P1.DEF.HYPERBOLIC_EQUILIBRIUM`
  - `section`: `2.4`
  - `definition`: `2.4.2`
- `DEP.P1.IDENTITY.SUSCEPTIBILITY_RESPONSE`
  - `section`: `2.4-2.5`
  - `note`: `discussion`

## Commands run

- `pytest -q`
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`
- `PYTHONPATH=src python -m nps.phases.phase_0b.build_cas0b --input cert_artifacts/2026-03-04T172947Z/CAS-A.json`

## Pytest summary

- Default: `98 passed`
- Gates-on: `98 passed`

## Persistent run

- Run dir: `cert_artifacts/2026-03-04T182514Z/`
- Artefact: `cert_artifacts/2026-03-04T182514Z/CAS-0B.json`

## CAS‑0B excerpt (Paper‑1 deps)

From `CAS-0B.json` → `dependency_table`:

- `DEP.P1.DEF.MARGINAL_STRUCTURAL_FIELD`
  - `source`: `NetworkPotential_Paper1_OperatorTheory_v0.6`
  - `locator`: `{ "section": "2.1", "definition": "2.1.1" }`
- `DEP.P1.DEF.HESSIAN_OPERATOR`
  - `source`: `NetworkPotential_Paper1_OperatorTheory_v0.6`
  - `locator`: `{ "section": "2.2", "definition": "2.2.1" }`
- `DEP.P1.DEF.HYPERBOLIC_EQUILIBRIUM`
  - `source`: `NetworkPotential_Paper1_OperatorTheory_v0.6`
  - `locator`: `{ "section": "2.4", "definition": "2.4.2" }`
- `DEP.P1.IDENTITY.SUSCEPTIBILITY_RESPONSE`
  - `source`: `NetworkPotential_Paper1_OperatorTheory_v0.6`
  - `locator`: `{ "section": "2.4-2.5", "note": "discussion" }`

## Acceptance criteria check

- pytest passes (both modes): ✓
- CAS‑0B.json contains locator fields: ✓
- No empty locator arrays: ✓
- Persistent run generated: ✓
