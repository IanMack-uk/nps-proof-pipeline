# Phase 0C — Step 2 (v3): What is still missing to *run/complete* this step

This package provides:
- a procedure (`phase_0C_step2_cascade_instructions_v3.md`)
- minimal output specs (`CAS-0C_SPEC.md`, `PROV-0C_SPEC.md`)
- verification rules (`phase_0C_step2_verification_rules.md`)
- a report template (`phase0C_REPORT_TEMPLATE_v3.md`)

However, Step 2 is **not yet a fully automated pipeline step** in the same way Step 1 is, because several required inputs/decisions are outside the package.

---

## 1) Required concrete inputs (not provided by this package)

### A) Target run id
You must specify the run directory:

- `cert_artifacts/<run_id>/`

This run must already contain the canonical chain:
- `CAS-0A.json`
- `CAS-A.json`
- `CAS-Ap.json`
- `CAS-0B.json`
- `CAS-B.json`
- `CAS-Bp.json`

And Step 1 must have produced:
- `PhaseC_ENTRY_REPORT.md` ending with `Phase C Entry Gate: APPROVED`

### B) Concrete Phase C deliverables list
Step 2 requires an explicit list of what Phase C is trying to build/prove.

The v2/v3 instructions include example targets (Hessian facts, locality decomposition, susceptibility bounds, etc.), but **you must choose the authoritative deliverables list** for this run so the backward-extraction table is meaningful.

### C) Candidate claim inventory (Paper 0 / Paper 1)
Step 2 needs a concrete list of candidate claims to audit.

This package provides **examples** (e.g. `P1.CLAIM.*` identifiers), but does not provide a canonical enumeration of Paper 0/1 claims.

You must supply one of:
- a curated list of claim IDs you care about in Phase C, or
- a copy/paste excerpt from Paper 0/1 that Step 2 will translate into claim IDs.

---

## 2) Required policy decisions (not fully determined by this package)

Even with the verification rules, Step 2 requires judgment calls.

### A) What counts as “VERIFIED by upstream artefacts”
The rules prefer upstream CAS evidence (checks/fields), but you still must decide:
- which upstream fields/checks are accepted as evidence for each candidate claim
- how strict the match must be (exact check id vs “implied by several facts”)

### B) Spectral escalation boundary
The instructions allow an explicit escalation path:

- `spectral_escalation = true`

But you must decide:
- whether Phase C is allowed to use spectral facts in your current certification posture
- which spectral facts are acceptable, if any

### C) Minimality criteria for CAS-0C
The “drop-test” step is conceptual unless you define:
- what it means for Phase C to become “ill-posed”
- whether minimality is strict (smallest set) or practical (small set)

---

## 3) Missing automation (if you want Step 2 to be executable like Step 1)

Step 1 has a concrete command that runs a validator module.

Step 2 currently does **not** have a code entrypoint that will:
- parse the run directory
- read Step 1 approval report
- construct `CAS-0C.json` and `PROV-0C.json`
- write `Phase0C_REPORT.md` from a structured internal representation

If you want this, the repo needs a module such as:

- `src/nps/phases/phase_0c/build_cas0c.py`

with a CLI like:

```bash
PYTHONPATH=src python -m nps.phases.phase_0c.build_cas0c \
  --run-id <run_id> \
  --input "cert_artifacts/<run_id>/PhaseC_ENTRY_REPORT.md"
```

and a schema gate (optional) for `CAS-0C.json` / `PROV-0C.json`.

---

## 4) Minimal checklist to complete Step 2 manually (using this package)

- Confirm Step 1 approval exists in `PhaseC_ENTRY_REPORT.md`.
- Define the Phase C deliverables list for this run.
- Create a candidate claim inventory (Paper 0/1 targets).
- Fill the backward dependency extraction table in `Phase0C_REPORT.md`.
- For each claim:
  - mark VERIFIED only with explicit upstream CAS evidence, otherwise UNVERIFIED
  - write UNVERIFIED items into `PROV-0C.json` with test plan + priority
- Write VERIFIED-only items into `CAS-0C.json`.
- Perform the minimality drop-test section in the report.
- Decide `CAS-0C Status: APPROVED / BLOCKED`.

---

## 5) What to provide to Cascade/ChatGPT to remove ambiguity

To make Step 2 deterministic, provide:
- `<run_id>`
- a list of Phase C deliverables
- a list of candidate Paper 0/1 claims (IDs + brief text)
- a rule for what upstream evidence is acceptable for each claim
