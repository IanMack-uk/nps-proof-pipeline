
# Task 10.2 — Runtime Phase Import Firewall

## Objective
Implement a runtime import firewall that enforces the repository phase import policy (`docs/specs/import_policy.json`) during execution.  
This prevents forward‑phase imports (e.g., `phase_b` importing `phase_d`) even if attempted via dynamic imports.

The firewall must be **disabled by default** and enabled only for CI / certification runs via an environment variable.

---

# Files to Implement

## 1. src/nps/audit/import_firewall.py

Must expose:

install_import_firewall(policy_path="docs/specs/import_policy.json")
uninstall_import_firewall()
is_firewall_enabled()
maybe_install_import_firewall()

Responsibilities:

• Load `docs/specs/import_policy.json`  
• Determine module phases from module names:
  `nps.phases.phase_<id>.*` → phase id `phase_<id>`  
• Install a `sys.meta_path` import hook  
• Detect forward imports using `phase_order`  
• Raise ImportError if violated  

Error message must contain:

• importer module
• imported module
• importer phase
• imported phase
• policy name

Example message:

RuntimeImportFirewall: forward phase import blocked
Importer: nps.phases.phase_b.example
Target: nps.phases.phase_d.target
Policy: phase_order_nonforward_imports

Suggested fix:
Move shared logic to a lower layer (core/models) or invert dependency.

---

## 2. Update (if needed)

src/nps/audit/import_policy.py

Reuse existing policy parsing utilities.

Expose helpers if necessary:

load_import_policy(path)
get_phase_id(module_name)
is_forward_phase_import(importer_phase, imported_phase, policy)

---

## 3. tests/test_import_firewall.py

Tests required:

### Test A — Blocks forward import

Simulate module in:

nps.phases.phase_b

Attempt import:

nps.phases.phase_d

Expect ImportError with policy message.

---

### Test B — Allows backward import

phase_d importing phase_b must succeed.

---

### Test C — Firewall disabled by default

Without environment variable:

NPS_IMPORT_FIREWALL

imports must behave normally.

---

### Test D — Firewall reversible

install_import_firewall()
→ forward import blocked

uninstall_import_firewall()
→ import allowed again

---

# CI Enablement

Firewall must activate only when:

NPS_IMPORT_FIREWALL=1

Recommended CI command:

NPS_IMPORT_FIREWALL=1 pytest -q

Developers should run normally without firewall.

---

# Acceptance Criteria

✔ Firewall implemented in `src/nps/audit/import_firewall.py`  
✔ Forward imports blocked when firewall enabled  
✔ Firewall disabled by default  
✔ Tests validate behavior  
✔ `pytest -q` passes with firewall off and on  
✔ Clear audit‑grade error messages  

---

# Deliverables

• src/nps/audit/import_firewall.py
• tests/test_import_firewall.py
• updated audit utilities if required
• documentation update

