# Certification Artefacts Convention

## Purpose
`cert_artifacts/` is the repository-level output location for certification runs.

It is intentionally separate from taskpack artefacts so that Phase 0A → D can be executed end-to-end without depending on the taskpack directory layout.

## Directory layout
- Artefacts root: `cert_artifacts/`
- Per-run directory: `cert_artifacts/<run_id>/`

## Run ID convention
- Default `run_id` is an ISO-like UTC timestamp: `YYYY-MM-DDTHHMMSSZ`
- A caller may also provide an explicit `run_id` (e.g. a CI build ID).

## Expected files (examples)
A certification run directory may contain:
- `CAS-0A.json`, `CAS-A.json`, `CAS-0B.json`, ...
- `PhaseReport.md`
- dependency DAG artefacts (`final_dependency_dag.md`, `final_dependency_edges.json`)
- policy validation outputs (`phase_import_policy_check.json`)

## CI / certification mode
Enable governance gates explicitly via environment variables:

```bash
NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q
```
