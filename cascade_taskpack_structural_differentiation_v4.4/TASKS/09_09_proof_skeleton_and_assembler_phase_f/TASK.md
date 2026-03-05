# 09_09_proof_skeleton_and_assembler_phase_f: Proof skeleton artefact + proof assembler (Phase F)

## Goal
Represent the ordering theorem proof as an explicit lemma chain and bind each step to CAS certificates.

## Required actions
1. Create a machine-readable proof skeleton file (json/yaml/md) with:
   - lemma IDs
   - required CAS IDs per lemma
   - inputs/outputs per lemma
2. Implement a proof assembler that:
   - checks all lemmas have backing certificates/imports
   - fails loudly with missing-proof witnesses
3. Add tests for missing-lemma and wrong-CAS cases.

## Artefacts
- proof skeleton file
- proof bundle directory example

## Report requirements
- Demonstrate a failure case when a lemma is missing.

