
# Phase 0C Step 2 — Schema Compatibility Patch Instructions for Cascade

## Purpose

This document instructs **Cascade/Windsurf** to apply a small robustness patch to the Phase 0C Step 2 builder so that it correctly handles both the **new** and **legacy** CAS‑A schema for the `certified_objective` field.

The change ensures that Phase 0C Step 2 remains stable across historical runs and older CAS‑A builders.

The patch must be **minimal, governance‑compliant, and deterministic**.

---

# Target File

src/nps/phases/phase_0c/build_cas0c.py

---

# Constraints

Cascade must follow these rules:

• Minimal surgical modification only  
• Do NOT change mathematical logic  
• Do NOT introduce new modelling assumptions  
• Preserve current behaviour when the new schema exists  
• Maintain compatibility with NPS governance gates  
• Maintain compatibility with `NPS_IMPORT_FIREWALL`  

---

# Step 1 — Implement Schema‑Fallback Helper

Add the following helper function to:

```
src/nps/phases/phase_0c/build_cas0c.py
```

```python
def _get_casa_certified_objective(casa: dict) -> str | None:
    """
    Resolve CAS‑A certified objective convention across schema variants.
    """
    derivative_def = casa.get("derivative_definition", {})
    if isinstance(derivative_def, dict):
        value = derivative_def.get("certified_objective")
        if value:
            return value

    # legacy fallback
    value = casa.get("certified_objective")
    if value:
        return value

    return None
```

---

# Step 2 — Replace Direct Access

Replace any direct access pattern such as:

```
casa.get("derivative_definition", {}).get("certified_objective")
```

with:

```
_get_casa_certified_objective(casa)
```

---

# Step 3 — Add Auditable Logging

Add a small diagnostic note describing which schema path was used.

Example messages:

```
CAS-A convention source: derivative_definition.certified_objective
```

or

```
CAS-A convention source: certified_objective (legacy)
```

---

# Step 4 — Add Lightweight Self‑Check

Create:

```
src/nps/phases/phase_0c/self_check.py
```

This module must test both schema variants.

Example structure:

```python
def run_self_check():
    from .build_cas0c import _get_casa_certified_objective

    casa_new = {
        "derivative_definition": {"certified_objective": "minus_phi"}
    }

    casa_old = {
        "certified_objective": "minus_phi"
    }

    assert _get_casa_certified_objective(casa_new) == "minus_phi"
    assert _get_casa_certified_objective(casa_old) == "minus_phi"

    print("Phase 0C schema compatibility self-check PASSED")


if __name__ == "__main__":
    run_self_check()
```

---

# Step 5 — Create Patch Summary Document

Create:

```
docs/phase-group-c/phase_0C_step2_cascade_package/v4/STEP2_SCHEMA_COMPAT_PATCH_SUMMARY.md
```

The document must contain:

## Changes

• Added schema‑fallback helper  
• Updated build_cas0c access logic  
• Added deterministic self‑check  

## Purpose

Ensure compatibility between legacy CAS‑A schema and current schema.

## Files Modified

```
src/nps/phases/phase_0c/build_cas0c.py
src/nps/phases/phase_0c/self_check.py
```

## How to Run the Self‑Check

```
PYTHONPATH=src python -m nps.phases.phase_0c.self_check
```

---

# Step 6 — Run the Self‑Check

Cascade must execute:

```
PYTHONPATH=src python -m nps.phases.phase_0c.self_check
```

If the self‑check fails, **abort the patch and do not commit**.

---

# Step 7 — Commit the Changes

If the self‑check passes:

```
git add src/nps/phases/phase_0c/build_cas0c.py
git add src/nps/phases/phase_0c/self_check.py
git add docs/phase-group-c/phase_0C_step2_cascade_package/v4/STEP2_SCHEMA_COMPAT_PATCH_SUMMARY.md
```

Commit using:

```
git commit -m "Phase 0C Step 2 robustness patch — CAS-A certified_objective schema fallback"
```

Push to the current branch:

```
git push
```

---

# Step 8 — Output Completion Summary

After the push, Cascade must output:

• List of modified files  
• Confirmation self‑check passed  
• Raw GitHub URLs of changed files  

Example:

```
https://raw.githubusercontent.com/IanMack-uk/nps-proof-pipeline/main/src/nps/phases/phase_0c/build_cas0c.py
```

---

# Completion

After completing these steps, paste the generated summary back into the ChatGPT conversation for verification.
