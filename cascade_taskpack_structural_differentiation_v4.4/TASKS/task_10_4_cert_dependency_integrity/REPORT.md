# Task Report — 10.4 Certification Dependency Integrity Gate

## Summary
- **Outcome:** SUCCESS
- **Primary changes:**
  - Implemented certification dependency integrity gate to validate CAS chain prerequisites and cross-artefact consistency.
  - Gate is disabled by default; enabled via `NPS_CERT_DEP_GATE=1`.
  - Added comprehensive tests for valid chain, missing prerequisite, wrong upstream cas_id, missing metadata, and enablement behavior.
- **Files added:**
  - `src/nps/audit/cert_dependency_gate.py`
  - `tests/test_cert_dependency_gate.py`
  - `cascade_taskpack_structural_differentiation_v4.3/TASKS/task_10_4_cert_dependency_integrity/REPORT.md`

## Commands run
- `pytest -q`
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`

## Test results
- **Default mode (gate off):** PASS (74 passed)
- **CI mode (gate on):** PASS (74 passed)

## Example failure message (excerpt)
```
CertDependencyGate: missing prerequisite CAS artefact
CAS present: CAS-C (CAS-C.json)
Missing prerequisite: CAS-0C
```

## Notes
- Chain prerequisites enforced (minimal contract):
  - CAS-A requires CAS-0A
  - CAS-0B requires CAS-A
  - CAS-B requires CAS-0B
  - CAS-0C requires CAS-B
  - CAS-C requires CAS-0C
  - CAS-0D requires CAS-C
  - CAS-D requires CAS-0D
- Minimal metadata required on each CAS JSON:
  - `cas_id`, `created_at`, `inputs`, `content_hash`
- Consistency checks:
  - `content_hash` must match stable hash of content excluding metadata fields
  - downstream `inputs` must include the upstream artefact’s `cas_id`
