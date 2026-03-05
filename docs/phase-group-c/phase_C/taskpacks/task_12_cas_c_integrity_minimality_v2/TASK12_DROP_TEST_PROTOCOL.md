# Taskpack 12 — Drop Test Protocol (Minimality)

This protocol defines the minimality audit executed by Taskpack 12.

**Goal:** Prevent CAS‑C from silently relying on redundant or accidental dependencies, and ensure every exported claim is supported only by necessary upstream artefacts.

---

## Definitions

- **Exported claim**: a claim listed in `CAS-C.json.claims`.
- **Dependency**: a referenced upstream `check_id` or artefact witness required by a claim.
- **Support**: a claim is supported if every dependency exists and every witness key exists in the referenced artefact.

---

## Strict Minimality Mode (default)

For each exported claim `c`:

1. Let `Deps(c)` be its dependency set.
2. For each dependency `d` in `Deps(c)`:
   - Construct a simulated environment where `d` is removed / unavailable.
   - Re-evaluate whether `c` remains supported.

Outcomes:
- If `c` is still supported without `d`, then `d` is **NOT necessary**.
  - In strict mode: this is a **FAIL** unless the claim is rewritten to remove `d`.
- If `c` becomes unsupported without `d`, then `d` is **necessary** (PASS for that pair).

Overall PASS requires:
- Every dependency listed for every claim is necessary.

---

## Practical simulation mechanics

Because we do not rewrite files, simulation is performed by:
- building an in-memory “availability set” of check_ids and witness keys
- removing the dependency from that availability set
- re-running the “claim supported?” predicate

For witness dependencies, simulate removal by:
- treating the witness `keys` as absent from the referenced JSON object.

---

## Reporting requirements

`PhaseC_DROP_TEST_REPORT.md` must contain:

- Claims enumerated with claim_id and statement
- For each claim:
  - list dependencies
  - drop-test table:
    - dependency
    - result: NECESSARY / REDUNDANT
    - which support condition failed (missing check_id / missing witness key / missing file)
- Final verdict:
  - `DROP_TEST_STATUS: PASS|FAIL`
  - list of redundant dependencies (if any)

---

## Allowed remediation patterns

If redundant dependencies are found:
- Preferred: remove the redundant dependency from the claim’s `depends_on` list.
- Alternatively: strengthen the claim statement so it truly needs the dependency (not recommended during closure).
