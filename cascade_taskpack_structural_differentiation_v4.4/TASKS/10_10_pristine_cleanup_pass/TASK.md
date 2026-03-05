
# 10_10_pristine_cleanup_pass
## Pristine Codebase Cleanup (Controlled & Auditable)

## Objective

Transform the repository into a **pristine, minimal, auditable codebase** without removing any material required for:

- mathematical certification
- governance compliance
- documentation of the research programme
- reproducibility

This task must be performed **conservatively and incrementally**.

Large destructive deletions are **not permitted without prior inventory and justification**.

---

# Cleanup Philosophy

The goal is **not simply to delete files**.

The goal is to ensure the repository is:

- structurally coherent
- dependency-clean
- free of dead code
- free of obsolete compatibility layers
- aligned with the canonical phase architecture

while **retaining all documentation and research artefacts required to understand the programme.**

---

# Cleanup Workflow

The cleanup must occur in **three stages**.

Cascade must execute them sequentially.

---

# Stage 1 — Repository Inventory (NON-DESTRUCTIVE)

Generate a full inventory of the repository.

**Do not delete anything yet.**

Produce the following artefacts in:

```
TASKS/10_10_pristine_cleanup_pass/ARTIFACTS/
```

---

## 1. File Inventory

Create:

```
repo_file_inventory.md
```

List all files grouped by:

- `src/`
- `tests/`
- `docs/`
- `tools/`
- `scripts/`
- `configs/`
- `other`

For each file include:

- `path`
- `purpose`
- `imported_by`
- `status_candidate` (KEEP / REVIEW / REMOVE)

---

## 2. Import Usage Analysis

Generate:

```
unused_modules_report.md
```

Identify:

- modules never imported
- functions never referenced
- deprecated compatibility shims

Mark them as:

- `safe_remove`
- `needs_review`
- `keep`

---

## 3. Documentation Inventory

Create:

```
docs_inventory.md
```

Classify documentation as:

- `programme_spec`
- `governance_spec`
- `implementation_docs`
- `historical_notes`
- `generated_outputs`

Only **generated outputs** are candidates for removal.

Programme specs and governance docs must be retained.

---

# Stage 2 — Candidate Cleanup Plan

Create a structured cleanup plan:

```
cleanup_plan.md
```

For each proposed deletion include:

- `file_path`
- `reason`
- `dependency_check`
- `test_impact`
- `approval_status`

Only files with:

- `dependency_check = NONE`
- `test_impact = NONE`

may be automatically removed.

All others must remain.

---

# Stage 3 — Controlled Cleanup Execution

Only after **Stage 1 + Stage 2 artefacts** are produced may deletion occur.

Perform deletions in **small atomic commits**.

For each deletion group:

1. Remove files
2. Run full test suite
3. Regenerate dependency DAG
4. Verify import policy

If any step fails → **restore the files**.

---

# Prohibited Deletions

Cascade **must not delete** the following categories.

## Research Documentation

```
docs/specs/*
docs/research/*
programme documents
CAS documentation
phase descriptions
```

## Certification Infrastructure

```
nps/certificates/*
nps/kernel/*
nps/phases/*
nps/audit/*
```

## Test Suite

```
tests/*
```

Tests may only be removed if the code they test has been removed.

## Cascade Task Pack

```
cascade_taskpack_structural_differentiation_v4.3/*
```

---

# Compatibility Layer Cleanup

Temporary compatibility modules introduced earlier (e.g. facades or re-exports) must be evaluated.

If they exist solely for migration and no longer have call sites:

```
mark safe_remove
```

Otherwise mark:

```
keep_for_now
```

---

# Dependency Graph Verification

After cleanup, regenerate the DAG.

Write to:

```
final_dependency_dag.md
final_dependency_edges.json
```

Verify:

- no forbidden phase imports
- no cycles in core/kernel modules
- phase mirroring intact

---

# Repository Consistency Checks

Before declaring success verify:

- pytest passes
- import policy check passes
- no orphan modules remain
- phase directories match programme phases
- certificate emission still works

---

# Required Artefacts

The following must exist when the task completes:

```
ARTIFACTS/
    repo_file_inventory.md
    unused_modules_report.md
    docs_inventory.md
    cleanup_plan.md
    final_dependency_dag.md
    final_dependency_edges.json
    deletion_ledger.md
```

---

# Deletion Ledger Format

Create:

```
deletion_ledger.md
```

Each entry must include:

- deleted_file
- reason
- verification_steps
- tests_run

---

# Definition of Success

The repository is considered **pristine** when:

- no dead code remains
- no obsolete compatibility modules remain
- dependency graph is clean
- phase architecture is canonical
- documentation is intact
- all tests pass

---

# Execution Start

Begin with **Stage 1 inventory generation**.

No files may be deleted until **Stage 2 cleanup plan** is produced.
