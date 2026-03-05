# CASCADE PHASE A (STEP A0) --- PROVISIONAL / VALIDATION LAYER BRIDGE

Project: `nps-proof-pipeline`

Context: - CAS-0A is certified and frozen. - Paper 0/1/2 mathematics is
not yet trusted. - Phase A must therefore treat all Paper-derived
objects/lemmas as **provisional** and earn certification via tests.

This document instructs Cascade to create a **validation layer** that
bridges: - the certified DependencyRegistry (CAS-0A) - the sandbox
experimentation code (toy Ω/Φ/F/W\* etc.) - the Phase A draft
objects/lemmas (exposure, coordinates, interface contracts)

------------------------------------------------------------------------

## 🎯 Objective

Create a new package:

    src/nps/validation/

that provides:

1.  Status enums for provisional → certified promotion
2.  A ValidationRegistry that records:
    -   assumptions (CAS-A ledger entries)
    -   statements (conjectures/lemmas/theorems)
    -   evidence links (tests, counterexamples, notes)
3.  Minimal enforcement hooks so Phase A builders can:
    -   register provisional assumptions/statements
    -   require that certain items are CERTIFIED before Phase B use
4.  Documentation scaffolding for a living CAS-A assumption ledger.

All changes must preserve mypy strictness and ruff compliance.

------------------------------------------------------------------------

## 0️⃣ Files / Folders to Add

Create:

    src/nps/validation/
      __init__.py
      status.py
      evidence.py
      records.py
      validation_registry.py

    docs/specs/
      cas_a_assumption_ledger.md

    tests/validation/
      __init__.py
      test_validation_registry.py

Do NOT modify certified CAS-0A objects except where explicitly listed
below.

------------------------------------------------------------------------

## 1️⃣ Status Enums

File: `src/nps/validation/status.py`

Implement enums:

-   `CertificationStatus`: PROVISIONAL, CERTIFIED, REJECTED
-   `StatementStatus`: CONJECTURE, VALIDATED, DISPROVEN

Example:

``` python
from __future__ import annotations
from enum import Enum

class CertificationStatus(str, Enum):
    PROVISIONAL = "PROVISIONAL"
    CERTIFIED = "CERTIFIED"
    REJECTED = "REJECTED"

class StatementStatus(str, Enum):
    CONJECTURE = "CONJECTURE"
    VALIDATED = "VALIDATED"
    DISPROVEN = "DISPROVEN"
```

------------------------------------------------------------------------

## 2️⃣ Evidence Model

File: `src/nps/validation/evidence.py`

Create a minimal evidence record to link registry items to tests and
notes.

``` python
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Evidence:
    kind: str                 # e.g., "test", "counterexample", "note"
    ref: str                  # e.g., "tests/models/test_locality.py::test_invariance"
    summary: str              # 1-2 line explanation
    link: Optional[str] = None  # optional URL or file path
```

No external dependencies.

------------------------------------------------------------------------

## 3️⃣ Records: AssumptionRecord and StatementRecord

File: `src/nps/validation/records.py`

Implement:

### 3.1 Scope tags (CAS-A scoping)

``` python
from enum import Enum

class ScopeTag(str, Enum):
    FOUNDATIONS = "FOUNDATIONS"
    PHASE_B_INTERFACE = "PHASE_B_INTERFACE"
    DIFFERENTIABILITY = "DIFFERENTIABILITY"
    UNIQUENESS = "UNIQUENESS"
```

### 3.2 AssumptionRecord

Fields:

-   id: str (e.g., "CAS-A.P1")
-   text: str (normative content)
-   scope: ScopeTag
-   status: CertificationStatus
-   sources: list\[SourceRef\] (can include Paper 0 refs; not trusted by
    default)
-   requires: set\[PropertyKey\] (CAS-0A properties required to even
    state/use it)
-   evidence: list\[Evidence\]

### 3.3 StatementRecord

Fields:

-   id: str (e.g., "THM.SDOT.v4")
-   statement: str (precise mathematical statement; markdown allowed)
-   status: StatementStatus
-   sources: list\[SourceRef\]
-   requires: set\[PropertyKey\] (CAS-0A prerequisites)
-   depends_on_assumptions: set\[str\] (AssumptionRecord ids)
-   evidence: list\[Evidence\]

Use dataclasses. Ensure mypy strict compatible typing (use `list[...]`,
`set[...]`).

------------------------------------------------------------------------

## 4️⃣ ValidationRegistry

File: `src/nps/validation/validation_registry.py`

Implement a class:

-   internal dicts for assumptions/statements by id
-   methods:

``` python
register_assumption(record: AssumptionRecord) -> None
register_statement(record: StatementRecord) -> None

add_evidence_to_assumption(assumption_id: str, evidence: Evidence) -> None
add_evidence_to_statement(statement_id: str, evidence: Evidence) -> None

promote_assumption(assumption_id: str) -> None       # PROVISIONAL -> CERTIFIED
reject_assumption(assumption_id: str) -> None        # -> REJECTED
validate_statement(statement_id: str) -> None        # CONJECTURE -> VALIDATED
disprove_statement(statement_id: str) -> None        # -> DISPROVEN

require_assumption_certified(assumption_id: str) -> None
require_statement_validated(statement_id: str) -> None

list_assumptions(scope: ScopeTag | None = None) -> list[AssumptionRecord]
list_statements() -> list[StatementRecord]
```

Rules: - Duplicate ids must raise MathematicalInconsistency. - Requiring
non-existent ids must raise MathematicalInconsistency. -
Promotion/validation must enforce allowed transitions only. - Adding
evidence to non-existent ids must raise MathematicalInconsistency.

Use `nps.core.exceptions.MathematicalInconsistency`.

------------------------------------------------------------------------

## 5️⃣ Minimal Integration Hook (Phase A builder placeholder)

Add a placeholder file (no math yet):

`src/nps/phases/phase_a/validation_seed.py`

Implement:

``` python
from nps.validation.validation_registry import ValidationRegistry

def seed_phase_a_validation_registry() -> ValidationRegistry:
    """Create an empty Phase A validation registry (draft layer)."""
    return ValidationRegistry()
```

No new assumptions or statements yet --- just seed wiring.

------------------------------------------------------------------------

## 6️⃣ Documentation Scaffold

Create:

`docs/specs/cas_a_assumption_ledger.md`

Include headings:

-   Purpose (provisional → certified workflow)
-   Status definitions (PROVISIONAL/CERTIFIED/REJECTED)
-   Scope tags
-   Assumption table template (empty for now)
-   Statement table template (empty for now)
-   Promotion protocol (what evidence is needed to certify)

Keep it short and explicit. This doc will become the living CAS-A
ledger.

------------------------------------------------------------------------

## 7️⃣ Tests

Create `tests/validation/test_validation_registry.py` covering:

1.  register_assumption success; duplicate id fails
2.  register_statement success; duplicate id fails
3.  add_evidence works; missing id fails
4.  require_assumption_certified fails when PROVISIONAL and passes when
    CERTIFIED
5.  promotion transition rules enforced
6.  require_statement_validated fails when CONJECTURE and passes when
    VALIDATED

Keep tests minimal and deterministic.

------------------------------------------------------------------------

## 8️⃣ Verification

All must pass:

    pytest
    mypy src
    ruff check .

------------------------------------------------------------------------

## 🚫 Non-Goals

Do NOT: - import Paper 0/1/2 mathematics as certified truth - modify
CAS-0A registry or properties - add structural exposure or coordinates
yet - add numeric solvers or plotting - change existing sandbox model
behaviour

------------------------------------------------------------------------

## ✅ Completion Condition

Phase A0 validation layer is complete when: - validation package exists
with status enums, records, registry -
docs/specs/cas_a\_assumption_ledger.md scaffold exists - tests validate
registry behaviour and promotion/require logic - all checks pass
