# CAS-A Structural Coordinates (Provisional)

Status: PROVISIONAL

## Coordinate interface

Structural coordinates are represented as:

- `CoordinateDefinition` (plugin interface)
- `StructuralCoordinate` (typed wrapper with domain/codomain/locality metadata)

## Control candidates

- `COORD.S.w_e` (control): S_e(w) := w_e
- `COORD.R.zero` (control): R_e(w) := 0

Negative control used in tests:

- `COORD.R.sumw`: R_e(w) := sum(w)

## Phase B interface contract

Contract (provisional):

- F_e(w,θ) depends only on (w_e, S_e(w), R_e(w), θ)

## Validation checks performed

- Coordinate well-posedness (shape and finiteness)
- Contract positive control (toy grad_phi with controls)
- Contract negative control (detects violation)
- Evidence logging under CAS-A assumptions

## Linked CAS-A assumptions

- CAS-A.COORD.LOCALITY
- CAS-A.CONTRACT.F_DEPENDENCE

No Paper 0 coordinate definitions are imported yet.
