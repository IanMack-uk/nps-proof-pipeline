# CASCADE MODELS STEP 0 --- CREATE MODELS SANDBOX

Project: `nps-proof-pipeline`

This document instructs Cascade to create a **models sandbox layer** for
executable mathematical experimentation, separate from the certified CAS
layers.

This sandbox is for: - Developing and testing explicit formula
instantiations - Verifying gradients numerically - Testing equilibrium
computation - Exploring locality behaviour

This layer MUST NOT modify or weaken the certified Phase 0A / A
infrastructure.

------------------------------------------------------------------------

# 🎯 Objective

Create a new package:

    src/nps/models/

This package contains **toy executable implementations** of:

-   Compact domains Ω
-   Smooth potentials Φ(w, θ)
-   Gradients ∇Φ
-   Basic equilibrium solvers
-   Numerical verification utilities

All implementations must be clearly marked as:

    "Executable model instance — not general certified theory"

------------------------------------------------------------------------

# 1️⃣ Create Folder Structure

Create the following structure:

    src/nps/models/
        __init__.py

        toy/
            __init__.py
            domains.py
            potentials.py
            equilibrium.py
            finite_diff.py

    tests/models/
        __init__.py
        test_gradients.py
        test_equilibrium.py

------------------------------------------------------------------------

# 2️⃣ Implement Basic Toy Domain

File: src/nps/models/toy/domains.py

Implement:

``` python
import numpy as np

def box_domain(m: int):
    """Return bounds for Ω = [0,1]^m."""
    lower = np.zeros(m)
    upper = np.ones(m)
    return lower, upper
```

This encodes a compact admissible set Ω.

------------------------------------------------------------------------

# 3️⃣ Implement Toy Potential Φ

File: src/nps/models/toy/potentials.py

Implement a simple smooth concave quadratic potential:

Φ(w, θ) = b(θ)\^T w − 1/2 w\^T Q w

Use diagonal positive-definite Q for simplicity.

Example:

``` python
import numpy as np

def phi(w: np.ndarray, theta: float) -> float:
    m = len(w)
    b = theta * np.ones(m)
    Q = np.eye(m)
    return float(b @ w - 0.5 * w @ Q @ w)

def grad_phi(w: np.ndarray, theta: float) -> np.ndarray:
    m = len(w)
    b = theta * np.ones(m)
    Q = np.eye(m)
    return b - Q @ w
```

This ensures: - Smoothness - Closed-form gradient - Unique interior
optimum (if unconstrained)

------------------------------------------------------------------------

# 4️⃣ Implement Simple Equilibrium Solver

File: src/nps/models/toy/equilibrium.py

Implement projected gradient ascent for box constraints:

``` python
import numpy as np
from .potentials import grad_phi
from .domains import box_domain

def project_box(w, lower, upper):
    return np.minimum(np.maximum(w, lower), upper)

def equilibrium(theta: float, m: int, steps=200, lr=0.1):
    lower, upper = box_domain(m)
    w = np.zeros(m)

    for _ in range(steps):
        w = w + lr * grad_phi(w, theta)
        w = project_box(w, lower, upper)

    return w
```

This is a numerical approximation of W\*(θ).

------------------------------------------------------------------------

# 5️⃣ Implement Finite-Difference Gradient Check

File: src/nps/models/toy/finite_diff.py

``` python
import numpy as np

def finite_difference_grad(phi, w, theta, h=1e-6):
    m = len(w)
    grad = np.zeros(m)

    for i in range(m):
        e = np.zeros(m)
        e[i] = 1.0
        grad[i] = (phi(w + h*e, theta) - phi(w - h*e, theta)) / (2*h)

    return grad
```

------------------------------------------------------------------------

# 6️⃣ Add Tests

## test_gradients.py

-   Random w inside interior
-   Compare grad_phi vs finite_difference_grad
-   Assert max error \< 1e-5

## test_equilibrium.py

-   Compute w\* = equilibrium(theta, m)
-   Check that:
    -   w\* within bounds
    -   Gradient at w\* small or complementary (projected condition)
    -   Φ(w\*) ≥ Φ(w) for several random w

------------------------------------------------------------------------

# 7️⃣ Verification

All must pass:

    pytest
    mypy src
    ruff check .

------------------------------------------------------------------------

# 🚫 Non-Goals

Do NOT:

-   Modify certification layer
-   Register toy Φ in CAS registry
-   Mix toy implementations with certified objects

Sandbox code must remain clearly separate from proof layer.

------------------------------------------------------------------------

# ✅ Completion Condition

Models sandbox exists. Toy Φ, gradient, solver, and finite difference
check implemented. All tests pass. Certified layer remains untouched.
