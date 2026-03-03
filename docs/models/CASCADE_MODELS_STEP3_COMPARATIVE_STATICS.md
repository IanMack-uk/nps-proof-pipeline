# CASCADE MODELS STEP 3 --- COMPARATIVE STATICS IN θ (CONTINUITY + SENSITIVITY + KINKS)

Project: `nps-proof-pipeline`

This document instructs Cascade to extend the **models sandbox** with a
comparative statics harness for the equilibrium correspondence θ ↦
W\*(θ).

We will: - compute equilibria over a θ-grid - verify an empirical
continuity surrogate - estimate sensitivity via finite differences -
detect "kinks" where box constraints activate (loss of smoothness)

This remains sandbox-only. Do NOT modify certified CAS layers.

------------------------------------------------------------------------

## 🎯 Objective

Given: - Ω = \[0,1\]\^m - Φ(w,θ) and F(w,θ)=∇Φ(w,θ) (dense or sparse
quadratic toy)

Implement utilities to compute: - w*(θ) for θ in a grid - stepwise
differences \|\|w*(θ\_{k+1}) − w*(θ_k)\|\| - finite-difference
sensitivity (w*(θ+δ) − w*(θ−δ)) / (2δ) - "active set" A(θ) = {i :
w_i*(θ) near 0 or 1} - kink flags where A(θ) changes across θ

------------------------------------------------------------------------

## 1️⃣ Add Files

Create:

    src/nps/models/toy/comparative_statics.py
    tests/models/test_comparative_statics.py

------------------------------------------------------------------------

## 2️⃣ Implement Comparative Statics Utilities

File: `src/nps/models/toy/comparative_statics.py`

Implement the following functions (type-hinted, mypy-clean):

### 2.1 Active set detection

``` python
from __future__ import annotations
import numpy as np
from typing import Set

def active_set(w: np.ndarray, tol: float = 1e-6) -> Set[int]:
    """Return indices i where w_i is within tol of 0 or 1."""
    A: Set[int] = set()
    for i, wi in enumerate(w):
        if wi <= tol or wi >= 1.0 - tol:
            A.add(i)
    return A
```

### 2.2 Compute equilibria over a θ-grid

``` python
from typing import Callable, List, Tuple

def equilibria_over_grid(
    theta_grid: np.ndarray,
    solve_equilibrium: Callable[[float], np.ndarray],
) -> List[Tuple[float, np.ndarray]]:
    """Compute (theta, w*(theta)) over a grid."""
    out: List[Tuple[float, np.ndarray]] = []
    for th in theta_grid:
        out.append((float(th), solve_equilibrium(float(th))))
    return out
```

### 2.3 Step differences

``` python
def step_differences(path: List[Tuple[float, np.ndarray]]) -> np.ndarray:
    """Return array of ||w*(θ_{k+1}) - w*(θ_k)|| for successive grid points."""
    diffs = []
    for k in range(len(path) - 1):
        diffs.append(np.linalg.norm(path[k+1][1] - path[k][1]))
    return np.asarray(diffs, dtype=float)
```

### 2.4 Sensitivity estimate (central difference)

``` python
def sensitivity_central(
    theta: float,
    delta: float,
    solve_equilibrium: Callable[[float], np.ndarray],
) -> np.ndarray:
    """Estimate dw*/dθ via central difference."""
    w_plus = solve_equilibrium(theta + delta)
    w_minus = solve_equilibrium(theta - delta)
    return (w_plus - w_minus) / (2.0 * delta)
```

### 2.5 Kink detection

Define "kink points" where the active set changes between adjacent grid
points.

``` python
from typing import Dict

def kink_flags(
    path: List[Tuple[float, np.ndarray]],
    tol: float = 1e-6,
) -> Dict[float, bool]:
    """Return {theta_k: True/False} for whether active set changes after theta_k."""
    flags: Dict[float, bool] = {}
    for k in range(len(path) - 1):
        th = path[k][0]
        A0 = active_set(path[k][1], tol=tol)
        A1 = active_set(path[k+1][1], tol=tol)
        flags[th] = (A0 != A1)
    if path:
        flags[path[-1][0]] = False
    return flags
```

------------------------------------------------------------------------

## 3️⃣ Add Tests

File: `tests/models/test_comparative_statics.py`

Use the sparse quadratic model (locality-aware) as default.

### Test A --- continuity surrogate in interior regime

Pick a parameter band where the solution is likely interior (e.g., small
theta).

Procedure: - m = 8, radius=1 - Build neighborhood + Q - Define
solve_equilibrium(theta) using existing `equilibrium(...)` with fixed m
and Q. (If your current solver builds Q internally, wrap it or add a
helper that closes over Q.) - Choose theta_grid = np.linspace(0.05, 0.2,
6) - Compute path - Compute diffs - Assert max(diffs) \< 0.2 (tunable;
should be comfortably small for this toy model)

Also assert that active sets are empty (or mostly empty) in this
regime: - For each w\* in path, assert len(active_set(w\*)) == 0

### Test B --- kink detection triggers in boundary regime

Pick larger theta so that projection hits upper bounds.

-   theta_grid = np.linspace(0.8, 1.2, 6)
-   Compute path
-   Compute kink_flags
-   Assert at least one kink flag is True OR at least one active set is
    non-empty (kinks often coincide with constraints activating)

### Test C --- sensitivity finite difference shape

Pick a theta in interior regime, delta=1e-2: - compute sens =
sensitivity_central(theta, delta, solve_equilibrium) - assert sens.shape
== (m,) - assert np.isfinite(sens).all()

------------------------------------------------------------------------

## 4️⃣ Verification

All must pass:

    pytest
    mypy src
    ruff check .

------------------------------------------------------------------------

## 🚫 Non-Goals

Do NOT: - modify certified CAS layers - add plotting libraries - add
scipy.optimize - assume smoothness beyond what toy model exhibits

This step is purely numerical comparative statics exploration.

------------------------------------------------------------------------

## ✅ Completion Condition

-   comparative_statics.py added with required functions
-   tests pass for continuity surrogate, kink detection, and sensitivity
    shape
-   all checks pass
-   certified CAS layers remain untouched
