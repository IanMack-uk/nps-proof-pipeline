# Project Setup Report — `nps-proof-pipeline`

Date: 2026-03-03

This report summarises the Phase **0A → Aʹ** bootstrap performed according to:

- `docs/CASCADE_BOOTSTRAP_INSTRUCTIONS.md`

## 1. Objective

The repository was bootstrapped into a reproducible Python project that enforces:

- Strict typing (`mypy` strict)
- Explicit dependency registration (`DependencyRegistry`)
- No implicit mathematical assumptions (typed objects require explicit fields)
- Test-driven certification gates (`pytest`)
- Drop-test enforcement for Phase **Aʹ** minimality

## 2. Packaging / Tooling

### Python version

- Requires Python `>=3.11`

### Project metadata

- Managed via `pyproject.toml`
- Editable install supported (`pip install -e .[dev]`)

### Development dependencies

Installed via optional extras group `dev`:

- `pytest`
- `mypy`
- `ruff`

### Typing configuration

`pyproject.toml` includes:

- `strict = true`
- `python_version = "3.11"`
- `warn_unused_ignores = true`
- `disallow_untyped_defs = true`
- `disallow_incomplete_defs = true`
- `no_implicit_optional = true`

### Git ignore rules

`.gitignore` includes:

- `.venv/`
- `__pycache__/`
- `*.pyc`
- `.mypy_cache/`
- `.pytest_cache/`

## 3. Repository Structure (created / aligned)

The following structure was created to match the bootstrap specification:

- `docs/programme/`
- `docs/specs/`
- `src/nps/`
  - `core/`
    - `errors.py`
    - `regularity.py`
    - `locality.py`
    - `types.py`
  - `certification/`
    - `dependency_registry.py`
    - `citations.py`
    - `drop_test.py`
  - `symbols/`
    - `symbol_dictionary.py`
    - `objects/`
      - `structural_exposure.py`
      - `relational_potential.py`
      - `equilibrium_edge_weight.py`
  - `phases/`
    - `phase_0a/build_cas0a.py`
    - `phase_a/build_casa.py`
    - `phase_a_prime/closure.py`
- `tests/`
  - `test_dependency_registry.py`
  - `test_symbol_dictionary.py`
  - `test_drop_test_phaseA.py`

## 4. Implemented Components

### 4.1 Phase 0A — Dependency certification

- `nps.core.errors.MathematicalInconsistency`
  - Canonical exception type for explicit certification/mathematical violations.

- `nps.certification.dependency_registry.DependencyRegistry`
  - `register(name, source)` registers a dependency exactly once
  - `require(name)` raises `MathematicalInconsistency` if missing
  - `drop(name)` removes a dependency and raises if unknown

### 4.2 Phase A — Symbol dictionary + typed objects

- `nps.core.types.MathematicalObject`
  - Requires explicit:
    - `domain`
    - `codomain`
    - `regularity` (`RegularityClass`)
    - `locality` (`LocalityScope`)
    - `source` (`SourceRef`)

- `nps.symbols.symbol_dictionary.SymbolDictionary`
  - Enforces:
    - a symbol cannot be added unless its dependency exists in the registry
    - object fields are explicitly declared (no empty domain/codomain/name/source)

### 4.3 Phase Aʹ — Minimality / drop test

- `nps.phases.phase_a_prime.closure.certify_minimality(registry, symbols)`
  - Fails with `MathematicalInconsistency` if any registered symbol depends on a missing dependency.

- `tests/test_drop_test_phaseA.py`
  - Registers a dependency, adds a symbol, asserts minimality passes
  - Drops the dependency, asserts minimality fails

## 5. Verification Commands and Results

The following commands were executed in the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

pytest
mypy src
ruff check .
```

Results:

- `pytest`: **PASS** (6 tests)
- `mypy src`: **PASS** (`Success: no issues found in 23 source files`)
- `ruff check .`: **PASS** (`All checks passed!`)

## 6. Explicit Non-Goals Confirmed

No Phase B+ operator theory, numerical solvers, graph libraries, simulations, or ML libraries were added.

## 7. Notes for Next Steps

The project is ready to proceed beyond bootstrap into additional Phase A/Aʹ specification work (e.g., expanding the symbol dictionary with formally sourced entries, strengthening minimality gates, adding richer type-level invariants), while maintaining:

- Explicit dependencies
- Explicit typed object declarations
- Test-first certification gates
