# Taskpack 11 — Execution Guide (for Cascade implementation)

This guide describes **exactly what Cascade should implement** for Taskpack 11 inside:

`src/nps/phases/phase_c/build_casc.py`

The taskpack is **purely compositional**: it reads Phase C artefacts produced by Tasks 2, 8, 9, and 10, performs lightweight verification and derivations, and writes Task 11 artefacts + report.

It must not alter earlier artefacts or re-run earlier computations.

---

## A) Inputs (run directory)

Given a run id `RUN`, Taskpack 11 reads from:

- `cert_artifacts/RUN/H_WTHETA.json` (Task 2)
- `cert_artifacts/RUN/NEUMANN_SERIES_BOUND.json` (Task 8)
- `cert_artifacts/RUN/M_MATRIX_CERTIFICATE.json` (Task 9)
- `cert_artifacts/RUN/SELECTED_INVERSE_ENTRIES.json` (Task 10)

Optional (only for shape cross-check, if present):
- `cert_artifacts/RUN/HESSIAN_MATRIX.json` (Task 3)

If any required file is missing, Taskpack 11 must FAIL loudly.

---

## B) Checks to implement (CHK.C11.*)

### CHK.C11.H_WTHETA.EXISTS
1. Confirm `H_WTHETA.json` exists.
2. Confirm it parses.
3. Confirm matrix `H_wtheta` is present and has numeric entries.
4. Record shape.

PASS if all above true.

### CHK.C11.H_WTHETA.SIGN_STRUCTURE_CERTIFIED
1. Read `H_WTHETA.json.sign_pattern`.
2. Require fields:
   - `constraint`  (new clarity field)
   - `tolerance`
   - `violations`
3. If `constraint` is `"nonnegative"` or `"nonpositive"`:
   - require `violations == 0` for PASS.
4. If `constraint` is `"mixed"`:
   - PASS but record that sign inference may be indeterminate downstream.

PASS conditions:
- required fields present
- violations consistent with constraint semantics

### CHK.C11.RESPONSE.SIGN_UNAMBIGUOUS
This check produces `RESPONSE_SIGN_PREDICTIONS.json`.

Inputs needed:
- From Task 9: evidence that `inv(H) >= 0` entrywise (M-matrix certificate)
- From Task 2: `H_wtheta.sign_pattern.constraint`
- From Task 10: selected entries list

Implementation rule (sign-only, no inversion):
1. If Task 9 indicates `inv(H) >= 0` entrywise, set `invH_sign = NONNEGATIVE`.
2. Infer sign of `dw/dtheta = - inv(H) @ H_wtheta`.

Sufficient cases:
- If `inv(H) >= 0` and `H_wtheta.constraint == "nonnegative"` then `dw/dtheta` is entrywise **nonpositive**.
- If `inv(H) >= 0` and `H_wtheta.constraint == "nonpositive"` then `dw/dtheta` is entrywise **nonnegative**.

Otherwise:
- mark indeterminate for any entry that cannot be concluded from available sign constraints.

Encoding:
- predicted negative -> -1
- predicted positive -> +1
- indeterminate or zero -> 0

Selected entries:
- For each selected (i,j) from Task 10, store predicted sign and note indeterminate reasons if 0.

PASS conditions:
- All selected entries have nonzero predicted sign (±1), OR
- If the governance allows weak readiness, then PASS may allow 0 with a recorded warning.
  (Default: require determinate for all selected entries.)

### CHK.C11.SCALING.BOUNDS_COMPUTED
This check produces `SCALING_BOUNDS.json`.

1. Read `rho_bound` and any derived bound from Task 8.
2. Require `rho_bound < 1`.
3. Compute `inverse_norm_bound`:
   - If Task 8 provides an explicit bound, reuse it.
   - Else compute `1/(1-rho_bound)` in the stated norm (record derivation).
4. Compute `||H_wtheta||_inf` from Task 2 matrix.
5. Set `response_norm_bound = inverse_norm_bound * ||H_wtheta||`.
6. Require finiteness.

PASS if `rho_bound < 1` and all computed bounds are finite.

---

## C) Artefact writing

Write the following files into `cert_artifacts/RUN/`:

- `EXPOSURE_RESPONSE_CHECK.json`
- `RESPONSE_SIGN_PREDICTIONS.json`
- `SCALING_BOUNDS.json`
- `PhaseC_TASK11_EXPOSURE_RESPONSE_COMPATIBILITY_REPORT.md`

All JSON files must include:
- `schema_version`
- `run_id`
- `taskpack_id`
- `inputs` paths
- `checks` array with CHK.C11.* statuses

The report must:
- list all checks + PASS/FAIL
- include sign_pattern details (constraint/tolerance/violations)
- state the derived response sign conclusion for selected entries
- state the scaling bound values
- end with `TASK11_STATUS: PASS|FAIL` and `READY_FOR_PHASE_D: YES|NO`

---

## D) Failure modes (must be explicit)

Taskpack 11 must FAIL if:
- missing required artefacts
- malformed JSON or schema mismatch
- `sign_pattern.constraint` missing
- `sign_pattern.violations != 0` under a declared global constraint
- Task 9 does not certify inverse nonnegativity
- selected entries have indeterminate sign (default strict mode)
- `rho_bound >= 1`

---

## E) Minimality / non-invasiveness

- Do not change any earlier artefacts.
- Do not recompute Hessians or inverses.
- Only compute sign-inference and simple norms.
- All derived numbers must cite upstream artefacts in `inputs`.

---

## F) Suggested CLI integration

If the repo uses a single `build_casc.py` entry, implement Task 11 under the existing Phase C build switch and ensure it runs after Task 10.

Return / report outcome consistent with other Taskpack reports.
