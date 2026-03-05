# Phase C Run Transcript (Template)

Run ID: RUN_ID_TODO  
Date (UTC):  
Machine:  
Operator:  

---

## Git state

- repo: `IanMack-uk/nps-proof-pipeline`
- branch: `main`
- commit SHA: `SHA_TODO`

---

## Governance gates enabled

```bash
export NPS_IMPORT_FIREWALL=1
export NPS_CAS_GATE=1
export NPS_CERT_DEP_GATE=1
export NPS_RUN_DIR_INTEGRITY=1
```

---

## Commands executed

### Phase C entry gate
```bash
PYTHONPATH=src python -c "from pathlib import Path; from nps.audit.phase_c_entry_gate import validate_phase_c_entry; validate_phase_c_entry(Path('cert_artifacts')/'RUN_ID_TODO')"
```

Result:
- PASS / FAIL

### Phase C build
```bash
PYTHONPATH=src python -m nps.phases.phase_c.build_casc   --run-id RUN_ID_TODO   --run-root cert_artifacts/RUN_ID_TODO
```

Result:
- PASS / FAIL

---

## Key outputs observed (run root)

List the files written, and paste any decision lines from the report(s):
- `PhaseC_REPORT.md` decision lines:
  - ...
- `CAS-C.json` status:
  - ...

---

## Notes / anomalies

- ...

