# CASCADE MODELS STEP 1 --- LOCALITY-AWARE POTENTIALS + TESTS

Project: `nps-proof-pipeline`

This document instructs Cascade to extend the **models sandbox** with a
locality-aware toy potential Φ and explicit tests that verify **local
dependence** of the marginal field F = ∇₍w₎Φ.

This is executable experimentation only. Do NOT modify the certified CAS
layers.

------------------------------------------------------------------------

## 🎯 Objective

Add a toy model where:

-   Variables `w[0], …, w[m-1]` represent edge weights (index set E).
-   A neighbourhood map `N(e)` defines which weights influence edge e.
-   The potential Φ is built so that the gradient component **F_e(w,θ)**
    depends only on `w[j]` for `j ∈ N(e)`.
-   Unit tests verify locality invariance: perturbing weights outside
    `N(e)` does not change `F_e`.

------------------------------------------------------------------------

## 1️⃣ Add Files / Structure

Create the following files:

    src/nps/models/toy/
      locality.py
      potentials_sparse.py

    tests/models/
      test_locality.py

------------------------------------------------------------------------

## 2️⃣ Implement Neighbourhood Maps

File: `src/nps/models/toy/locality.py`

Implement:

-   `ring_neighborhood(m: int, radius: int = 1) -> dict[int, set[int]]`
    -   Indices are modulo m.
    -   For radius=1: N(e) = {e-1, e, e+1} mod m
    -   N(e) MUST include e itself.
-   `check_neighborhood(neigh: dict[int, set[int]], m: int) -> None`
    -   Raise ValueError if:
        -   keys are not exactly 0..m-1
        -   any N(e) missing e
        -   any index out of bounds

Example skeleton:

``` python
from __future__ import annotations
from typing import Dict, Set

def ring_neighborhood(m: int, radius: int = 1) -> Dict[int, Set[int]]:
    if m <= 0:
        raise ValueError("m must be positive")
    if radius < 0:
        raise ValueError("radius must be nonnegative")

    neigh: Dict[int, Set[int]] = {}
    for e in range(m):
        s: Set[int] = set()
        for k in range(-radius, radius + 1):
            s.add((e + k) % m)
        neigh[e] = s
    check_neighborhood(neigh, m)
    return neigh

def check_neighborhood(neigh: Dict[int, Set[int]], m: int) -> None:
    if set(neigh.keys()) != set(range(m)):
        raise ValueError("Neighborhood keys must be exactly 0..m-1")
    for e, s in neigh.items():
        if e not in s:
            raise ValueError(f"N({e}) must include {e}")
        for j in s:
            if j < 0 or j >= m:
                raise ValueError(f"N({e}) contains out-of-bounds index {j}")
```

------------------------------------------------------------------------

## 3️⃣ Implement Sparse Quadratic Potential

File: `src/nps/models/toy/potentials_sparse.py`

Implement a locality-coupled quadratic:

Φ(w, θ) = b(θ)\^T w − 1/2 w\^T Q w

Where Q is constructed so that:

-   `Q[e, j] = 0` whenever `j ∉ N(e)`
-   Q is symmetric positive definite (SPD) for stability

Simplest SPD construction:

-   Start with `Q = alpha * I`
-   For each neighbourhood coupling (e, j) with j in N(e), add small
    symmetric weights: `Q[e, j] += beta` and `Q[j, e] += beta`, but keep
    diagonal dominance by choosing alpha large.

Implement:

-   `build_sparse_Q(m: int, neigh: dict[int, set[int]], alpha: float = 2.0, beta: float = 0.1) -> np.ndarray`
-   `phi_sparse(w: np.ndarray, theta: float, Q: np.ndarray) -> float`
-   `grad_phi_sparse(w: np.ndarray, theta: float, Q: np.ndarray) -> np.ndarray`

Use:

-   `b(θ) = θ * ones(m)`

Example:

``` python
import numpy as np

def build_sparse_Q(m: int, neigh: dict[int, set[int]], alpha: float = 2.0, beta: float = 0.1) -> np.ndarray:
    Q = alpha * np.eye(m)
    for e in range(m):
        for j in neigh[e]:
            if j == e:
                continue
            Q[e, j] += beta
            Q[j, e] += beta
    # Ensure SPD by diagonal dominance (alpha should exceed degree*beta).
    return Q

def phi_sparse(w: np.ndarray, theta: float, Q: np.ndarray) -> float:
    m = len(w)
    b = theta * np.ones(m)
    return float(b @ w - 0.5 * w @ Q @ w)

def grad_phi_sparse(w: np.ndarray, theta: float, Q: np.ndarray) -> np.ndarray:
    m = len(w)
    b = theta * np.ones(m)
    return b - Q @ w
```

------------------------------------------------------------------------

## 4️⃣ Add Locality Verification Test

File: `tests/models/test_locality.py`

Create a test that verifies:

For random `w` and chosen index `e`, if we perturb components `w[j]`
with `j ∉ N(e)`, then:

    grad_phi_sparse(w,θ,Q)[e]  == grad_phi_sparse(w_perturbed,θ,Q)[e]

to within a tight tolerance, e.g. `1e-10`.

Implementation details:

-   Choose parameters: m=10, radius=1, theta=0.5
-   Build `neigh = ring_neighborhood(m, radius)`
-   Build `Q = build_sparse_Q(m, neigh, alpha=?, beta=?)` (ensure alpha
    \> 2*radius*beta\*2 roughly)
-   Sample w uniformly in \[0,1\]\^m
-   Choose a few e values (e.g., loop e in \[0, 3, 7\])
-   Perturb outside indices with random noise of order 1e-2
-   Confirm invariance of the e-th gradient component

Also add a negative control test:

-   If we perturb an index j IN N(e), gradient component should
    generally change (assert difference \> small threshold for at least
    one case).

------------------------------------------------------------------------

## 5️⃣ Optional: Finite Difference Check for Sparse Gradient

Add one test verifying:

`grad_phi_sparse ≈ finite_difference_grad(phi_sparse)`

Reuse `finite_difference_grad` from Step 0.

------------------------------------------------------------------------

## 6️⃣ Verification

All must pass:

    pytest
    mypy src
    ruff check .

------------------------------------------------------------------------

## 🚫 Non-Goals

Do NOT:

-   Modify certified CAS layers
-   Register toy properties in DependencyRegistry
-   Add Paper 0 / Paper 1 theorem content
-   Add heavy graph libraries

This is a sandbox-only locality experiment.

------------------------------------------------------------------------

## ✅ Completion Condition

-   New modules exist: `locality.py`, `potentials_sparse.py`
-   Locality invariance test passes
-   Negative control test passes
-   All checks pass
