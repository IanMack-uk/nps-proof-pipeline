# Phase Group A Task Pack (Option 2) — Phase 0A → Phase A → Phase A′

## Objective
Implement **Phase Group A** of the Structural Differentiation / Ordering Theorem Programme:

- **Phase 0A**: Prior Results Certification for Phase A → generate **CAS-0A.json** by **extracting targets + dependencies from the programme spec** (not placeholders).
- **Phase A**: Foundations → generate **CAS-A.json** with precise definitions, notation freeze, assumption registry, and obligations discharge.
- **Phase A′**: Closure → generate **CAS-Ap.json** (A-prime) approving internal consistency + minimality and freezing the Phase-A interface.

All artefacts must be written into a run directory:

- `cert_artifacts/<run_id>/`

and must satisfy existing gates (content hash, inputs chain, completeness, etc.) when gates are enabled.

---

## Inputs (documents to read)
Cascade must read and use the following documents already in the repo (or provided in this project):

1. `docs/Computational_Certification_Architect_Role_Prompt.md`
2. `docs/Structural_Differentiation_Programme_v4.3.md` (or the equivalent location in the repo)

These documents are authoritative for:
- phase goals and deliverables
- governance requirements (explicit assumptions, no silent strengthening, minimality, auditability)

---

## High-level deliverables

### Phase 0A deliverables
- `cert_artifacts/<run_id>/CAS-0A.json`
- `cert_artifacts/<run_id>/Phase0A_REPORT.md`

### Phase A deliverables
- `cert_artifacts/<run_id>/CAS-A.json` (must include `inputs: ["CAS-0A"]` by cas_id)
- `cert_artifacts/<run_id>/PhaseA_REPORT.md`
- `cert_artifacts/<run_id>/assumption_registry.json` (recommended; can also be embedded in CAS-A)

### Phase A′ deliverables
- `cert_artifacts/<run_id>/CAS-Ap.json` (A-prime closure artefact; must include `inputs: ["CAS-A"]`)
- `cert_artifacts/<run_id>/PhaseA_prime_REPORT.md`

---

## Architecture constraints (must respect)
- Use existing repo governance tooling:
  - `src/nps/certification/artifacts.py` for run directories + stable JSON writing
  - `src/nps/audit/governance.py` to enable optional gates (env-controlled)
- Respect phase isolation:
  - no forward imports across phases (import policy + firewall)
- CAS chain integrity:
  - include metadata fields required by `cert_dependency_gate`
  - compute `content_hash` according to the repo’s canonical hashing (exclude metadata fields as implemented)

---

# Part 1 — Implement Phase 0A (CAS-0A generator)

## Goal of Phase 0A
Produce a **certified dependency set** for Phase A by **backward-extracting** from the programme spec:

- Phase A targets (deliverables)
- dependencies (programme references, Paper references if present, standard theorems)
- imported assumptions needed to justify Phase A deliverables
- obligations that Phase A must discharge/verify
- minimality audit structure (drop-test plan; can be “manual/partial” but must reference real dep IDs)

## Required code
Create:

- `src/nps/phases/phase_0a/build_cas0a.py`

Expose:

- `def build_cas0a(run_dir: Path) -> Path:`
- `def main():` CLI entrypoint

CLI:
- `python -m nps.phases.phase_0a.build_cas0a --run-id <optional>`

The CLI must:
1. call `maybe_install_governance()`
2. create run directory via `make_run_dir()`
3. parse the programme document
4. extract Phase A targets + dependencies (real locators)
5. write `CAS-0A.json` using `write_json()`
6. write `Phase0A_REPORT.md` summarizing what was extracted

## Extraction rules (Option 2)
- Targets MUST be extracted from the Phase A section(s) of the programme doc.
- Dependencies MUST be extracted from:
  - explicit “imports”, “prior results”, “dependencies”, “requires”, “lemmas used” statements in the programme doc
  - any explicitly named “Paper 0 / Paper 2 / Paper 3” prerequisites referenced in Phase A planning
  - standard theory references explicitly indicated (e.g., chain rule, IFT, variational analysis) if the programme calls them out as required for Phase A deliverables

### Dependency IDs
Use stable IDs that include source + locator:
- `DEP.PROG.<section>.<item>` for programme-extracted requirements
- `DEP.PAPER0.<section>.<def/lem/theorem>` when a paper is explicitly referenced
- `DEP.STD.<domain>.<topic>` for standard results

Each dependency record must include:
- `dep_id`
- `type` (definition | lemma | theorem | assumption | standard_result)
- `source.document`
- `source.locator` (section/heading text from the programme doc; if a paper is referenced, include that)
- `provides` (what it gives)
- `used_in` (target_ids)

### Obligations
Each target must list obligations Phase A must discharge. Obligations must be checkable and scoped, e.g.:
- “Define object X formally”
- “Prove well-posedness of definition under assumptions Y”
- “Freeze notation and symbol dictionary”

Obligation fields:
- `obligation_id`
- `statement`
- `method` (definition | proof | check | assumption)
- `status` (unverified_in_0A)
- `to_be_discharged_in` (CAS-A)

### Minimality audit
Include a `minimality_audit` section with:
- method: `drop_test`
- status: `planned` or `partial_manual`
- at least one concrete entry referencing a real `dep_id` extracted from the programme doc

## CAS-0A schema requirements (must satisfy gates)
Top-level metadata:
- `cas_id`: "CAS-0A"
- `created_at`: ISO timestamp
- `inputs`: []
- `content_hash`: computed

Body fields required:
- `programme` (name, version, phase)
- `phase_targets` (extracted targets)
- `dependency_table`
- `assumptions.imported` and `assumptions.introduced` (introduced must be empty in 0A)
- `obligations`
- `minimality_audit`
- `trace` (tool, version, source docs list)

---

# Part 2 — Implement Phase A (CAS-A generator)

## Goal of Phase A
Produce the **foundational specification layer** for later mathematics:

- precise theorem statement (quantifiers, regime)
- core objects (structural exposure, equilibrium correspondence, coordinates/locality)
- explicit assumptions introduced in Phase A
- discharge obligations imported from CAS-0A
- freeze notation / symbol dictionary

## Required code
Create:

- `src/nps/phases/phase_a/build_casa.py`

Expose:
- `def build_casa(run_dir: Path) -> Path:`
- `def main():` CLI

CLI:
- `python -m nps.phases.phase_a.build_casa --run-id <optional> --input <path-to-CAS-0A.json>`

Rules:
1. Must read CAS-0A.json and treat it as authoritative input
2. Must set CAS-A `inputs` to include the upstream `cas_id` value from CAS-0A (not hard-coded)
3. Must reference dependency IDs from CAS-0A when citing foundations
4. Must produce:
   - `CAS-A.json`
   - `PhaseA_REPORT.md`
   - (optional) `assumption_registry.json`

## CAS-A content requirements (minimum)
- `theorem_statement`: structured fields
  - regime (interior baseline)
  - quantifiers (agents/indices)
  - conclusion (ordering statement)
- `objects` section defining:
  - structural exposure (type signature)
  - equilibrium correspondence (maximisation convention explicit)
  - structural coordinates / locality graph (how locality is encoded)
  - derivative objects needed later (∇Φ, Hessian, mapping F)
- `assumptions` section:
  - `imported` (from CAS-0A)
  - `introduced` (new Phase-A assumptions; must be explicit)
- `obligations_discharge` section:
  - list each obligation from CAS-0A and mark `discharged: true/false`
  - for discharged obligations, include a short “how discharged” note and references to dependency IDs
- `notation_freeze`:
  - symbol dictionary list
  - disambiguations (indices vs enumeration etc.)

Top-level metadata:
- `cas_id`: "CAS-A"
- `inputs`: ["CAS-0A"] (actual upstream id)
- `content_hash`: computed

---

# Part 3 — Implement Phase A′ (Closure / Approval)

## Goal of Phase A′
Freeze and approve CAS-A as a governed artefact.

A′ checks:
- internal consistency (no undefined symbols)
- no hidden assumptions beyond those explicit in CAS-A
- Phase-A interface is sufficient for Phase 0B/B to proceed later

## Required code
Create:

- `src/nps/phases/phase_a_prime/build_casa_prime.py`

CLI:
- `python -m nps.phases.phase_a_prime.build_casa_prime --run-id <optional> --input <path-to-CAS-A.json>`

Outputs:
- `CAS-Ap.json`
- `PhaseA_prime_REPORT.md`

CAS-Ap should contain:
- summary of checks performed
- list of blocking issues (must be empty to approve)
- minimality audit update (confirm no extra deps beyond CAS-0A unless recorded)
- `inputs`: ["CAS-A"] (actual cas_id read from CAS-A)

---

# Tests (must be added)

Create tests:

1. `tests/test_phase_0a_cas0a_generation.py`
   - runs build_cas0a into tmp run dir
   - asserts CAS-0A.json exists
   - asserts required top-level keys
   - asserts `inputs == []`
   - asserts `content_hash` matches recomputation (using same hashing utility as gate)
   - asserts at least one target and one dependency extracted from programme doc

2. `tests/test_phase_a_casa_generation.py`
   - generates CAS-0A then CAS-A
   - asserts CAS-A inputs include CAS-0A cas_id
   - asserts obligations_discharge exists and references obligations from CAS-0A

3. `tests/test_phase_a_prime_closure.py`
   - generates CAS-0A, CAS-A, then CAS-Ap
   - asserts CAS-Ap inputs include CAS-A cas_id
   - asserts blocking issues list is empty (or absent) for baseline

4. `tests/test_gates_on_phase_group_a.py`
   - runs generation with env vars set:
     - `NPS_IMPORT_FIREWALL=1`
     - `NPS_CAS_GATE=1`
     - `NPS_CERT_DEP_GATE=1`
   - asserts no failures and artefacts satisfy gates

---

# Reporting
Add phase reports under the task folder:

- `cascade_taskpack_structural_differentiation_v4.3/TASKS/task_phase_group_a/REPORT.md`

Must include:
- files added/changed
- commands run
- test results:
  - `pytest -q`
  - `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`
- example excerpt from CAS-0A showing at least one extracted target + dependency with locator

---

# Verification commands (must run)
- `pytest -q`
- `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`

Both must pass.

---

# Definition of Done
Phase Group A is complete when:
- Phase 0A generates CAS-0A with **targets + dependencies extracted from programme doc** (not placeholders)
- Phase A generates CAS-A consuming CAS-0A and discharging obligations
- Phase A′ generates CAS-Ap approving Phase A
- Artefacts are written under `cert_artifacts/<run_id>/`
- Tests pass in default and CI-mode (gates on)
- Report written under task folder
