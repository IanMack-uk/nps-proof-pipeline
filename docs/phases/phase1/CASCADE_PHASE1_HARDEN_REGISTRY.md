# CASCADE PHASE 1 --- PROPERTY-LEVEL CERTIFICATION HARDENING

Project: `nps-proof-pipeline`

This document instructs Cascade to upgrade the current Phase 0A
certification system from object-level registration to **property-level
certification**.

This is a structural hardening step. No new mathematics should be added.

------------------------------------------------------------------------

# 🎯 Objective

Refactor the certification layer so that:

-   Dependencies are registered at the level of **(subject, property)**
-   Every property must include a `SourceRef`
-   Mathematical objects declare explicit required properties
-   Drop tests remove individual properties, not whole objects
-   Certification gates fail precisely when a required property is
    missing

This enables true CAS-0A minimality auditing.

------------------------------------------------------------------------

# 1️⃣ Required Refactor

## 1.1 Define PropertyKey

Create in:

`src/nps/certification/dependency_registry.py`

``` python
from dataclasses import dataclass

@dataclass(frozen=True)
class PropertyKey:
    subject: str        # e.g. "Phi"
    property: str       # e.g. "C3_extension"
```

------------------------------------------------------------------------

## 1.2 Upgrade DependencyRegistry

Replace object-level registration with:

``` python
register(property_key: PropertyKey, source: SourceRef)
require(property_key: PropertyKey)
drop(property_key: PropertyKey)
is_registered(property_key: PropertyKey) -> bool
```

Rules:

-   A property cannot be registered without a SourceRef
-   Duplicate registration must raise an error
-   Dropping a non-existent property must raise
    MathematicalInconsistency

------------------------------------------------------------------------

# 2️⃣ Upgrade MathematicalObject

In:

`src/nps/core/types.py`

Add:

``` python
from typing import Set
from nps.certification.dependency_registry import PropertyKey

class MathematicalObject:
    ...
    requires: Set[PropertyKey]
```

Rules:

-   `requires` must be non-empty
-   Every required property must be present in the registry before
    symbol addition

------------------------------------------------------------------------

# 3️⃣ Upgrade SymbolDictionary

In:

`src/nps/symbols/symbol_dictionary.py`

When adding a symbol:

-   For each property in `symbol.requires`
    -   call `registry.require(property_key)`
-   Raise MathematicalInconsistency if any missing

------------------------------------------------------------------------

# 4️⃣ Upgrade Drop Test

Modify:

`tests/test_drop_test_phaseA.py`

New behaviour:

1.  Register property: ("Phi", "C3_extension")
2.  Create object requiring that property
3.  Assert certification passes
4.  Drop only ("Phi", "C3_extension")
5.  Assert certification fails

The test must confirm the system detects property-level inconsistency.

------------------------------------------------------------------------

# 5️⃣ Verification Requirements

After refactor, the following must pass:

    pytest
    mypy src
    ruff check .

No new warnings permitted.

------------------------------------------------------------------------

# 6️⃣ Non-Goals

Do NOT:

-   Add Phase B logic
-   Add operator theory
-   Add numerical solvers
-   Expand mathematical content

This step strictly strengthens certification granularity.

------------------------------------------------------------------------

# ✅ Completion Condition

Phase 1 is complete when:

-   Registry operates at property-level
-   MathematicalObject declares required properties
-   SymbolDictionary enforces property certification
-   Drop test fails when a single property is removed
-   All checks pass

Do not proceed to mathematical expansion until this phase is stable.
