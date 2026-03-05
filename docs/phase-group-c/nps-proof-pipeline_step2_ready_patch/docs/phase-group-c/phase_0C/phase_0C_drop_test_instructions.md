# Phase 0C — Step 3: Minimality Drop-Test (CAS-0C) — Cascade Instructions

## Purpose

Phase 0C is only complete once we have verified that **CAS-0C is sufficient and minimal**.

This instruction file tells **Cascade/Windsurf** to perform a minimality “drop test” on the dependency set recorded in:

- `cert_artifacts/<run_id>/CAS-0C.json`

The drop test must attempt to remove each `verified_import` entry, rebuild/validate CAS-0C consistency, and record whether Phase C readiness is preserved.

This produces a run-root report:

- `cert_artifacts/<run_id>/Phase0C_DROP_TEST_REPORT.md`

If minimality is not satisfied, Cascade must propose the smallest correction (remove unused imports) and regenerate `CAS-0C.json` plus the report.

---

## Target Run

Run ID:

```
2026-03-04T211059Z
```

Run root:

```
cert_artifacts/2026-03-04T211059Z/
```

---

## Inputs (must exist)

Cascade must confirm these exist **in the run root** (not `experiments/`):

- `CAS-0C.json`
- `CAS-A.json`
- `CAS-B.json`
- `PhaseC_ENTRY_REPORT.md`
- `docs/phase-group-c/PHASE_C_MATHEMATICAL_TOOL_WHITELIST.md`

If any are missing: stop and report `PHASE_0C_DROP_TEST_FAIL: Missing required input`.

---

## Governance Gates (must be enabled)

Cascade must run with:

```
NPS_IMPORT_FIREWALL=1
NPS_CAS_GATE=1
NPS_CERT_DEP_GATE=1
NPS_RUN_DIR_INTEGRITY=1
```

If any gate cannot be enabled, stop and report `PHASE_0C_DROP_TEST_FAIL: Governance gates not enabled`.

---

## Drop Test Definition (what counts as “still sufficient”)

A dependency set is considered **still sufficient** after dropping a candidate import if:

1. The Phase C Entry Gate remains valid for this run (strict-concave maximiser regime):
   - `equilibrium_objective = maximize`
   - `equilibrium_regime = strict_concave`
   - Phase C entry report ends with `Phase C Entry Gate: APPROVED`
2. CAS-0C still contains the minimum **finite-dimensional tool whitelist** entries needed for Phase C (unless the dropped item is non-essential).
3. The CAS-0C file remains schema-valid (content hash updates; JSON well-formed).
4. The CAS-0C status remains `APPROVED`.

Important:
- This drop test is **structural / governance-level**.
- It does not require computing Hessians (that begins in Phase C).

---

## Step 1 — Load CAS-0C and Enumerate Verified Imports

Open:

```
cert_artifacts/2026-03-04T211059Z/CAS-0C.json
```

Extract:

- `verified_imports` list
- each entry’s `import_id`

Record the baseline count.

---

## Step 2 — For Each Import, Attempt a Drop

For each `import_id` in `verified_imports`:

1. Create a temporary candidate CAS-0C payload that removes that single entry.
2. Recompute/update `content_hash` deterministically (use the same helper used elsewhere in the repo).
3. Validate the candidate CAS-0C against the drop-test sufficiency conditions above.

### Notes
- Do not edit upstream artefacts (CAS-A / CAS-B).
- Do not change the run directory structure.
- Only test removal of a single import at a time.

---

## Step 3 — Classification Output

For each import, record one of:

- **ESSENTIAL**: dropping it violates sufficiency (explain why, referencing the sufficiency condition number).
- **REMOVABLE**: dropping it preserves sufficiency (so it should be removed from CAS-0C).
- **INCONCLUSIVE**: only if there is a tooling limitation; must include a remediation step.

---

## Step 4 — Apply Minimality Fix (if needed)

If any imports are classified **REMOVABLE**:

1. Generate a new `CAS-0C.json` in the run root with those imports removed.
2. Recompute `content_hash`.
3. Ensure the new CAS-0C remains `APPROVED` and satisfies the sufficiency conditions.

If no imports are removable, do not modify CAS-0C.

---

## Step 5 — Write the Drop-Test Report

Write:

```
cert_artifacts/2026-03-04T211059Z/Phase0C_DROP_TEST_REPORT.md
```

The report must follow this structure exactly:

```markdown
# Phase 0C Drop-Test Report

Run ID: 2026-03-04T211059Z
Generated at (UTC):

## Inputs Verified
- CAS-0C.json: PASS/FAIL
- CAS-A.json: PASS/FAIL
- CAS-B.json: PASS/FAIL
- PhaseC_ENTRY_REPORT.md: PASS/FAIL
- PHASE_C_MATHEMATICAL_TOOL_WHITELIST.md: PASS/FAIL

## Governance Gates
- NPS_IMPORT_FIREWALL=1: PASS/FAIL
- NPS_CAS_GATE=1: PASS/FAIL
- NPS_CERT_DEP_GATE=1: PASS/FAIL
- NPS_RUN_DIR_INTEGRITY=1: PASS/FAIL

## Baseline
- verified_imports count:

## Drop-Test Results
| import_id | classification | reason (sufficiency condition #) | action |
|---|---|---|---|
| ... | ESSENTIAL/REMOVABLE/INCONCLUSIVE | ... | kept/removed |

## Post-Fix CAS-0C Status
- CAS-0C modified?: YES/NO
- verified_imports count after fix:
- CAS-0C status: APPROVED/BLOCKED

## Final Status
CAS-0C Minimality: PASS/FAIL
```

---

## Step 6 — Output Completion Summary (pasteable)

At the end of execution, print:

- list of modified files (if any)
- final `verified_imports` count
- final minimality status `PASS/FAIL`
- the absolute path to the drop-test report

---

## Reference Files

- Tool whitelist:
  - `docs/phase-group-c/PHASE_C_MATHEMATICAL_TOOL_WHITELIST.md`
- Phase C entry gate logic:
  - `src/nps/audit/phase_c_entry_gate.py`
- CAS-0C builder:
  - `src/nps/phases/phase_0c/build_cas0c.py`
- Drop-test helper (if used):
  - `src/nps/certification/drop_test.py`

---

## Completion Criteria

Phase 0C is considered fully complete for this run if:

- `Phase0C_DROP_TEST_REPORT.md` exists in the run root, and
- it ends with:

```
CAS-0C Minimality: PASS
```

After that, Phase C work may begin.
