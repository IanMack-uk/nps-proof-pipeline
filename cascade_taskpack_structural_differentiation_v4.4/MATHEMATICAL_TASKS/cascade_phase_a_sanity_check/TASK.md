# Phase A Sanity Verification (Read-Only Check)

Before moving on to Phase Group B, perform a quick verification that the Phase A toy-quadratic harness produced the expected certification artefacts.

## Rules
- Do **not modify any code**.
- Do **not create or edit files**.
- This is a **read-only verification step**.

## Step 1 — Run Phase A generator
Run the Phase A generator with the toy quadratic enabled.

Command:

python -m nps.phases.phase_a.build_casa --toy-quadratic

Allow the system to generate a new certification run directory under:

cert_artifacts/<run_id>/

## Step 2 — Locate CAS-A artefact

Open:

cert_artifacts/<run_id>/CAS-A.json

## Step 3 — Verify checks are present

Inspect the "checks" section of CAS-A.json.

Confirm that the following checks exist:

CHK.A.INTERIOR_FEASIBILITY
CHK.A.NEG_DEF_HESSIAN

## Step 4 — Verify witness fields

Confirm the witness payloads include the expected diagnostic fields.

For CHK.A.NEG_DEF_HESSIAN confirm:

witness.min_eigenvalue
witness.symmetry_error

For CHK.A.INTERIOR_FEASIBILITY confirm:

witness.min_slack
witness.min_component
witness.max_component

These fields confirm the curvature and interior-regime evidence is being recorded.

## Step 5 — Verify extension identifier

Confirm that the CAS-A artefact records the derivative extension identifier:

derivative_definition.extension_id

Expected value (or equivalent):

toy_quadratic_v1

## Step 6 — Produce a short verification note

Create a short summary stating:
- the run directory used
- whether both checks were present
- whether witness fields were populated
- whether extension_id was recorded

Do **not change any source files**.

## Completion Criteria

The verification is successful if:

- CAS-A.json contains both new checks
- witness fields (min_eigenvalue, min_slack, etc.) are present
- extension_id is recorded

If all conditions are satisfied, Phase Group A verification is confirmed and the project can proceed to Phase Group B.
