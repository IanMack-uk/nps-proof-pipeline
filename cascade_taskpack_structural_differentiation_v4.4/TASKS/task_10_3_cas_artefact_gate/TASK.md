
# Task 10.3 — CAS Artefact Completeness Gate

## Objective
Add a **CAS Artefact Completeness Gate** that ensures every certification stage produces the required artefacts with the required structure before the phase can be considered valid.

The gate must:
- validate artefact presence
- validate minimal schema structure
- fail with an audit-grade error message if requirements are not met

The gate must be **disabled by default** and enabled only during CI and certification runs.

---

# Required Files to Implement

## 1. src/nps/audit/cas_artefact_gate.py

Must expose:

validate_cas_artefacts(artefact_dir)
install_cas_gate()
uninstall_cas_gate()
is_cas_gate_enabled()
maybe_install_cas_gate()

Responsibilities:
- Validate required artefacts exist
- Validate minimal JSON structure
- Raise RuntimeError with audit-grade messages when validation fails

---

# Artefact Validation Rules

Default artefact directory pattern:

cascade_taskpack_structural_differentiation_v4.3/TASKS/*/ARTIFACTS/

Required artefacts:

final_dependency_dag.md
final_dependency_edges.json
phase_import_policy_check.json
deletion_ledger.md
REPORT.md

Checks:

final_dependency_edges.json must contain keys:
- nodes
- edges

phase_import_policy_check.json must contain keys:
- policy
- phase_order
- violations

violations must equal []

---

# Acceptance Tests

Create:

tests/test_cas_artefact_gate.py

Required tests:

Test A — Valid artefacts pass
Test B — Missing artefact fails
Test C — Invalid schema fails
Test D — Gate disabled by default
Test E — Gate enabled via environment variable

---

# Enablement

Gate enabled only when:

NPS_CAS_GATE=1

Example CI command:

NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 pytest -q

---

# Reporting

Create:

cascade_taskpack_structural_differentiation_v4.3/TASKS/task_10_3_cas_artefact_gate/REPORT.md

Include:
- files added
- commands run
- test results
- confirmation gate is off by default

---

# Definition of Done

- cas_artefact_gate implemented
- artefact validation logic working
- tests implemented
- pytest passes
- gate disabled by default
- gate enabled via env variable
- clear error messages
- report written
