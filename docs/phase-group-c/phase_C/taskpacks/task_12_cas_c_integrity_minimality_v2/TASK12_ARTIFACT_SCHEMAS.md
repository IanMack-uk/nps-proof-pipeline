# Taskpack 12 — Artifact Schemas (JSON)

This document defines JSON schemas produced by Taskpack 12.

All paths are relative to repo root.

---

## 1) CAS-C_MANIFEST.json

### Purpose
A deterministic manifest of all inputs consumed by Taskpack 12 with content hashes.
This prevents “silent drift” and makes audits reproducible.

### Schema
```json
{
  "schema_version": "C-CASC-MANIFEST.v1",
  "run_id": "2026-03-04T211059Z",
  "taskpack_id": "C-TASK12.v2",
  "files": [
    {
      "path": "cert_artifacts/2026-03-04T211059Z/H_WTHETA.json",
      "kind": "json",
      "schema_version": "C-H_WTHETA.v2",
      "sha256": "<hex>",
      "bytes": 12345
    }
  ],
  "created_at_utc": "2026-03-05T00:00:00Z"
}
```

Required:
- `files[*].sha256` must be SHA256 of file bytes.
- Each `path` must exist.

---

## 2) CAS-C.json

### Purpose
Single canonical Phase‑C certified assumption/claim set for Phase D reliance.

### Schema (structural)
```json
{
  "schema_version": "CAS-C.v1",
  "run_id": "2026-03-04T211059Z",
  "phase": "C",
  "taskpack_id": "C-TASK12.v2",
  "provenance": {
    "certified_objective": "minus_phi",
    "objective_direction": "maximize",
    "equilibrium_regime": "strict_concave",
    "phase_c_entry_gate_passed": true,
    "manifest_path": "cert_artifacts/<run_id>/CAS-C_MANIFEST.json"
  },
  "claims": [
    {
      "claim_id": "C.INV_H.NONNEGATIVE_ENTRYWISE",
      "statement": "The inverse Hessian inv(H) is entrywise nonnegative in the certified regime.",
      "strength": "theorem_level",
      "depends_on": [
        "CHK.C9.M_MATRIX.NONSINGULAR",
        "CHK.C9.INV_NONNEGATIVE_ENTRYWISE"
      ],
      "witness": {
        "source_path": "cert_artifacts/<run_id>/M_MATRIX_CERTIFICATE.json",
        "keys": ["inv_entrywise_nonnegative", "m_matrix_type"]
      }
    }
  ],
  "phase_d_interface": {
    "ready_for_phase_d": true,
    "required_claim_ids": [
      "C.INV_H.NONNEGATIVE_ENTRYWISE",
      "C.RESPONSE.IDENTITY.WELL_POSED",
      "C.RESPONSE.SIGN.DETERMINATE_FOR_SELECTED",
      "C.RESPONSE.NORM.BOUNDED"
    ]
  },
  "dependency_graph": {
    "nodes": [],
    "edges": []
  },
  "created_at_utc": "2026-03-05T00:00:00Z"
}
```

Required:
- Every `depends_on` check_id must exist upstream.
- Every witness `source_path` must exist and match manifest hash.
- `phase_d_interface.ready_for_phase_d` must equal CHK.C12.READY_FOR_PHASE_D.GATED outcome.

---

## 3) PhaseC_REPORT.md

### Purpose
Human-readable Phase C closure report (integrity + key witnesses + readiness verdict).

Must include:
- run id
- list of tasks 1–12 statuses
- key witnesses: rho_bound, inv(H) nonnegativity, H_wtheta constraint
- final verdict READY_FOR_PHASE_D

---

## 4) PhaseC_DROP_TEST_REPORT.md

### Purpose
Audit report of minimality drop test.

Must include:
- list of exported claims
- mapping claim -> required deps
- per-dependency drop outcome:
  - breaks which claim(s)
  - or allows removal (and then claim must be removed in strict mode)
- final minimality verdict
