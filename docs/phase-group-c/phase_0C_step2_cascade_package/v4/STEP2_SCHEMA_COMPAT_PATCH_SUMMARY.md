## Changes

• Added schema-fallback helper  
• Updated build_cas0c access logic  
• Added deterministic self-check

## Purpose

Ensure compatibility between legacy CAS-A schema and current schema.

## Files Modified

```
src/nps/phases/phase_0c/build_cas0c.py
src/nps/phases/phase_0c/self_check.py
```

## How to Run the Self-Check

```
PYTHONPATH=src python -m nps.phases.phase_0c.self_check
```
