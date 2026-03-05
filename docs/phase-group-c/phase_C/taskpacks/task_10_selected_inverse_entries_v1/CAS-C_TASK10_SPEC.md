# CAS-C Task 10 Spec — Selected Inverse Entries and Phase D Interface (FINAL)

**Taskpack ID:** C-TASK10  
**Schema version:** C-TASK10.v2  
**Purpose:** Define a **deterministic, minimal selection rule** for the inverse-Hessian information that Phase D will actually consume, and certify sign conclusions for that selected subset.

> Governance note: Only **upstream CAS artefacts + computed checks** may be marked VERIFIED. Papers/thesis content must be tracked as **PROV** unless separately certified.

---

## Authoritative inputs (run root only)

Required (at least one inverse-sign source must be present):
- `HESSIAN_BLOCKS.json` (Taskpack 4)
- `INVERSE_POSITIVITY_CERT.json` (Taskpack 9) **OR** `NEUMANN_SERIES_BOUND.json` (Taskpack 8)

Optional:
- `THETA_FAMILY.json` (Taskpack 2) — only if your selection depends on θ labels/indexing

---

## Outputs (write to run root)

- `SELECTED_INVERSE_ENTRIES.json`
- `PhaseC_TASK10_SELECTED_INVERSE_ENTRIES_REPORT.md`

Optional (ideas only):
- `PROV-C-TASK10.json`

---

## SELECTED_INVERSE_ENTRIES.json — required schema (VERIFIED)

```json
{
  "schema_version": "C-TASK10.v2",
  "run_id": "RUN_ID",
  "generated_utc": "YYYY-MM-DDThh:mm:ssZ",
  "sources": {
    "HESSIAN_BLOCKS": "HESSIAN_BLOCKS.json",
    "INVERSE_SIGN_SOURCE": "INVERSE_POSITIVITY_CERT.json"
  },
  "dimension": 0,
  "inverse_sign_source": {
    "kind": "INVERSE_POSITIVITY_CERT|NEUMANN_SERIES_BOUND",
    "entrywise_nonnegative": true,
    "notes": "If kind=NEUMANN_SERIES_BOUND, entrywise_nonnegative may be false/unknown."
  },
  "selection": {
    "rule_id": "C10.RULE.MINIMAL_PHASED_INTERFACE.v1",
    "rule_text": "Human-readable rule; deterministic and auditable.",
    "basis": {
      "type": "index_set|block|pairs",
      "description": "What object the rule selects (indices, blocks, (i,j) pairs)."
    },
    "selected": {
      "indices": [0],
      "pairs": [[0, 0]]
    }
  },
  "selected_signs": {
    "convention": "sign(C^{-1}) or sign(H^{-1}) — must match rule_text",
    "entries": [
      {
        "i": 0,
        "j": 0,
        "sign": "+",
        "source": "INVERSE_POSITIVITY_CERT"
      }
    ]
  },
  "witnesses": {
    "selection_hash": "sha256-of-canonical-selection-json",
    "ordering": "sorted_lexicographic"
  },
  "checks": [
    {"id": "CHK.C10.SELECTION.RULE_DEFINED", "ok": true, "status": "PASS", "details": {}},
    {"id": "CHK.C10.SELECTION.DETERMINISTIC", "ok": true, "status": "PASS", "details": {}},
    {"id": "CHK.C10.SELECTED_SIGNS.CERTIFIED", "ok": true, "status": "PASS", "details": {}}
  ]
}