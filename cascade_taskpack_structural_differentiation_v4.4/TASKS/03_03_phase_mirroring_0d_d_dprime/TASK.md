# 03_03_phase_mirroring_0d_d_dprime: Restore canonical phase mirroring for 0D/D/D′ under nps.phases

## Goal
Ensure all phases live under `nps.phases.*` and match the programme’s canonical structure.

## Required actions
1. Create modules:
   - `src/nps/phases/phase_0d/`
   - `src/nps/phases/phase_d/`
   - `src/nps/phases/phase_d_prime/`
2. Move or wrap any existing Phase D code (e.g. `src/nps/phase_d/`) into the canonical location.
3. Add temporary re-exports if needed; document deprecation.
4. Update import policy and tests to include these modules.

## Artefacts
- updated DAG

## Report requirements
- Explicitly list old paths and new canonical paths.
- Confirm no phase leakage introduced.

