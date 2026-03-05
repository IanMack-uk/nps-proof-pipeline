# 02_02_break_core_cert_cycle: Break the nps.core <-> nps.certification cycle

## Goal
Eliminate the foundational cycle so strict isolation enforcement is feasible.

## Required actions
1. Identify the symbols causing mutual imports.
2. Create `nps.kernel` (or `nps.base`) containing only:
   - shared types
   - exceptions
   - minimal utilities
3. Refactor imports so:
   - `nps.core` imports `nps.kernel`
   - `nps.certification` imports `nps.kernel`
   - neither imports the other
4. Update DAG + isolation tests.

## Artefacts
- updated DAG

## Report requirements
- Before/after edge list proving the cycle is removed.
- Note any public API changes and whether re-exports were used.

