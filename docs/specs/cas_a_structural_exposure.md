# CAS-A Structural Exposure (Draft)

Status: DRAFT / PROVISIONAL

## Interface

Structural exposure is represented as:

- `ExposureDefinition` (plugin interface)
- `StructuralExposure` (typed wrapper with domain/codomain/regularity/locality metadata)

## Candidates (controls)

- `EXP.w_e` (control): E_e(w) := w_e
- `EXP.absF` (control): E_e(w,θ) := |F_e(w,θ)|

## Validation checks

- Well-posedness (shape and finiteness)
- Edge-locality check (EDGE_ONLY)
- Neighborhood-locality check (N(e))

## Non-claim

No Paper 0 structural exposure formula is imported yet.
