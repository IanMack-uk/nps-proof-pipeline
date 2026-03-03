# CASCADE BOOTSTRAP INSTRUCTIONS

Project: `nps-proof-pipeline`

This document instructs Cascade (or any AI coding agent) to initialise
the `nps-proof-pipeline` project with the correct folder structure, base
files, and required packages for Phase 0A → Aʹ certification.

------------------------------------------------------------------------

# 1️⃣ Objective

Create a reproducible Python project for the **NPS Proof Pipeline**,
implementing:

-   Phase 0A --- Dependency certification
-   Phase A --- Symbol dictionary & typed mathematical objects
-   Phase Aʹ --- Minimality / drop test enforcement

The project must enforce:

-   Strict typing
-   Explicit dependency registration
-   No hidden mathematical assumptions
-   Test-driven certification gates

------------------------------------------------------------------------

# 2️⃣ Create Project Structure

Create the following directory structure:

    nps-proof-pipeline/
    │
    ├── pyproject.toml
    ├── README.md
    ├── .gitignore
    │
    ├── docs/
    │   ├── programme/
    │   └── specs/
    │
    ├── src/
    │   └── nps/
    │       ├── __init__.py
    │       │
    │       ├── core/
    │       │   ├── __init__.py
    │       │   ├── errors.py
    │       │   ├── regularity.py
    │       │   ├── locality.py
    │       │   └── types.py
    │       │
    │       ├── certification/
    │       │   ├── __init__.py
    │       │   ├── dependency_registry.py
    │       │   ├── citations.py
    │       │   └── drop_test.py
    │       │
    │       ├── symbols/
    │       │   ├── __init__.py
    │       │   ├── symbol_dictionary.py
    │       │   └── objects/
    │       │       ├── __init__.py
    │       │       ├── structural_exposure.py
    │       │       ├── relational_potential.py
    │       │       └── equilibrium_edge_weight.py
    │       │
    │       └── phases/
    │           ├── __init__.py
    │           ├── phase_0a/
    │           │   ├── __init__.py
    │           │   └── build_cas0a.py
    │           │
    │           ├── phase_a/
    │           │   ├── __init__.py
    │           │   └── build_casa.py
    │           │
    │           └── phase_a_prime/
    │               ├── __init__.py
    │               └── closure.py
    │
    └── tests/
        ├── __init__.py
        ├── test_dependency_registry.py
        ├── test_symbol_dictionary.py
        └── test_drop_test_phaseA.py

All modules must include module-level docstrings referencing the
Programme phase they implement.

------------------------------------------------------------------------

# 3️⃣ Create `.gitignore`

Add:

    .venv/
    __pycache__/
    *.pyc
    .mypy_cache/
    .pytest_cache/

------------------------------------------------------------------------

# 4️⃣ Create `pyproject.toml`

Use modern Python packaging (not requirements.txt unless explicitly
needed).

Create the following:

``` toml
[project]
name = "nps-proof-pipeline"
version = "0.1.0"
description = "Formal certification pipeline for the Network Potential Structural Differentiation Programme"
requires-python = ">=3.11"

dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "mypy>=1.0",
    "ruff>=0.1.0"
]

[tool.pytest.ini_options]
pythonpath = ["src"]

[tool.mypy]
strict = true
python_version = "3.11"
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
no_implicit_optional = true
```

------------------------------------------------------------------------

# 5️⃣ Required Packages

After creating the project:

### Create virtual environment

    python -m venv .venv
    source .venv/bin/activate

### Install in editable mode

    pip install -e .[dev]

This installs:

-   pytest (testing)
-   mypy (strict typing enforcement)
-   ruff (linting)

------------------------------------------------------------------------

# 6️⃣ Certification Enforcement Rules

Cascade must ensure:

1.  Every mathematical object:
    -   Has a domain
    -   Has a codomain
    -   Has a regularity class
    -   Has a locality scope
    -   Has a SourceRef
2.  No symbol is added to the SymbolDictionary unless:
    -   It is registered in DependencyRegistry
    -   All required properties are declared
3.  Phase Aʹ must include:
    -   A drop test
    -   A failure if a required dependency is removed
4.  No mathematical property may be assumed implicitly.

------------------------------------------------------------------------

# 7️⃣ Initial Implementation Targets

Cascade should first implement:

-   `MathematicalInconsistency` in `core/errors.py`
-   `DependencyRegistry` in `certification/dependency_registry.py`
-   `SymbolDictionary` in `symbols/symbol_dictionary.py`
-   A minimal drop test in `tests/test_drop_test_phaseA.py`

Do not implement higher-phase operator theory yet.

------------------------------------------------------------------------

# 8️⃣ Verification Checklist

After bootstrap, the following must succeed:

    pytest
    mypy src
    ruff check .

All must pass with no errors.

------------------------------------------------------------------------

# 9️⃣ Explicit Non-Goals (At This Stage)

Do NOT:

-   Implement full operator theory (Phase B+)
-   Add numerical solvers
-   Add graph libraries
-   Add network simulation code
-   Introduce external ML libraries

This repository is a **proof pipeline**, not a modelling environment.

------------------------------------------------------------------------

# 10️⃣ Completion Condition

Bootstrap is complete when:

-   Folder structure matches Section 2
-   pyproject.toml is valid
-   Tests execute
-   Strict typing passes
-   Registry + drop test operate correctly
