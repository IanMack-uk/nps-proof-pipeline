# Task 10 Upstream Evidence Map — Selected Inverse Entries and Phase D Interface

This file specifies what counts as **VERIFIED** evidence for Task 10.

Evidence sources allowed:
- `cert_artifacts/<run_id>/CAS-A.json`
- `cert_artifacts/<run_id>/CAS-B.json`
- `cert_artifacts/<run_id>/CAS-0C.json` (tool whitelist + dependency posture)
- `cert_artifacts/<run_id>/PhaseC_ENTRY_REPORT.md`
- **Computed artefacts written to the run root by this taskpack** (deterministic)

Never use:
- `experiments/` outputs as VERIFIED evidence.

## Required upstream anchors

- Entry gate approval:
  - `CAS-0C.phase_c_entry_gate.approved == true` (if CAS-0C exists)
  - and/or `PhaseC_ENTRY_REPORT.md` ends with `APPROVED`

- Regime:
  - `CAS-0C.equilibrium.equilibrium_regime == "strict_concave"` (if CAS-0C exists)
  - otherwise: import from `CAS-B`

- Tool posture:
  - `CAS-0C.spectral_escalation == false` unless explicitly escalated
  - `docs/phase-group-c/PHASE_C_MATHEMATICAL_TOOL_WHITELIST.md` vocabulary

## Task-specific evidence rules

For each check id in Task 10, record:
- evidence source (upstream vs computed)
- exact CAS field path(s) used
- exact computed artefact path(s) used

