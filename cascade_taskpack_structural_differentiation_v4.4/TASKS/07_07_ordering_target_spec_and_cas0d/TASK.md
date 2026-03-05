# 07_07_ordering_target_spec_and_cas0d: OrderingTargetSpec + CAS-0D backward dependency extractor

## Goal
Make the ordering target explicit and ensure dependency extraction is target-driven and minimal.

## Required actions
1. Implement `OrderingTargetSpec`:
   - aggregate_directional (default)
   - pairwise_entrywise (escalation)
2. Implement CAS-0D generator that reads the spec and selects required imports:
   - default: no spectral tools
   - escalation: explicitly import spectral/M-matrix tools (opt-in only)
3. Add “no silent escalation” tests.
4. Integrate with phase artefact emission.

## Artefacts
- CAS-0D outputs for both target modes

## Report requirements
- Show dependency differences between target modes.

