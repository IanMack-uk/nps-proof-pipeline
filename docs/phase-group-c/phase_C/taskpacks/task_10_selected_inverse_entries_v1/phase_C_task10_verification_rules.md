
---

### 3) `phase_C_task10_verification_rules_FINAL.md`
```md
# Phase C — Task 10 Verification Rules (FINAL)
**Taskpack:** C-TASK10

## Required checks

### CHK.C10.SELECTION.RULE_DEFINED
PASS if:
- `selection.rule_id` and `selection.rule_text` are non-empty
- `selection.selected.pairs` exists, non-empty, and in bounds
- `selection.selected.indices` exists, sorted unique, and in bounds

FAIL otherwise.

### CHK.C10.SELECTION.DETERMINISTIC
PASS if:
- `pairs` sorted lexicographically; `indices` sorted unique
- `witnesses.selection_hash` exists and matches sha256(canonical(selection.selected))
- `witnesses.ordering` declares the canonical ordering used

FAIL otherwise.

### CHK.C10.SELECTED_SIGNS.CERTIFIED
PASS if:
- `inverse_sign_source.kind == "INVERSE_POSITIVITY_CERT"`
- Task 9 cert indicates entrywise nonnegative, AND
- every selected entry is labeled `sign="+"` with `source="INVERSE_POSITIVITY_CERT"`

FAIL otherwise.