
# Task B.2.2 — Fix CAS‑0B Paper‑1 Definition Locators

## Objective
Correct the missing locator metadata for Paper‑1 definitions in `CAS-0B.json`.

Dependencies affected:

- DEP.P1.DEF.MARGINAL_STRUCTURAL_FIELD
- DEP.P1.DEF.HESSIAN_OPERATOR

## Authoritative Source

Paper: NetworkPotential_Paper1_OperatorTheory_v0.6

| Dependency | Paper Location |
|---|---|
| DEP.P1.DEF.MARGINAL_STRUCTURAL_FIELD | Section 2.1 — Definition 2.1.1 |
| DEP.P1.DEF.HESSIAN_OPERATOR | Section 2.2 — Definition 2.2.1 |
| DEP.P1.DEF.HYPERBOLIC_EQUILIBRIUM | Section 2.4 — Definition 2.4.2 |
| DEP.P1.IDENTITY.SUSCEPTIBILITY_RESPONSE | Section 2.4–2.5 discussion |

## Required Changes

Update locator fields inside:

docs/specs/phase_group_b_defs/CAS0B_Dependencies_And_Obligations.md

Ensure `build_cas0b.py` writes these locators into `CAS-0B.json`.

### Expected JSON Format

{
  "dep_id": "DEP.P1.DEF.MARGINAL_STRUCTURAL_FIELD",
  "source": "NetworkPotential_Paper1_OperatorTheory_v0.6",
  "locator": {
    "section": "2.1",
    "definition": "2.1.1"
  }
}

Repeat for other Paper‑1 dependencies.

## Verification

Run:

pytest -q

NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q

Then regenerate CAS‑0B:

PYTHONPATH=src python -m nps.phases.phase_0b.build_cas0b

Confirm:

cert_artifacts/<run_id>/CAS-0B.json

contains non‑empty locators for all DEP.P1.* entries.

## Acceptance Criteria

✓ pytest passes (both modes)

✓ CAS‑0B.json contains locator fields

✓ No empty locator arrays

✓ Persistent run generated

## Reporting

Write report to:

cascade_taskpack_structural_differentiation_v4.3/
MATHEMATICAL_TASKS/
cascade_taskpack_phase_group_b_locators_b22/
TASKS/task_B_2_2_fix_locators/REPORT.md

Include:

• files changed
• locator mappings
• pytest output summary
• CAS‑0B excerpt
