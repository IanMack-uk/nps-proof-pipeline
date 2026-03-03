# CASCADE MODELS STEP 2 --- PROJECTED OPTIMALITY (BOX-KKT CHECKS)

Project: `nps-proof-pipeline`

This document instructs Cascade to extend the models sandbox with
numerical optimality verification for box-constrained problems.

We implement and test a projected gradient optimality residual for Ω =
\[0,1\]\^m.

This step strengthens the executable interpretation of:

    W*(θ) = argmax_{w ∈ Ω} Φ(w, θ)

WITHOUT modifying the certified CAS layers.

------------------------------------------------------------------------

# 🎯 Objective

Add numerical verification that computed equilibria satisfy a
projected-gradient (box KKT-style) condition.

For Ω = \[0,1\]\^m, define residual:

    r_eta(w) = || w - Π_Ω(w + η F(w,θ)) ||

At equilibrium w\*, this residual should be small.

------------------------------------------------------------------------

# 1️⃣ Add Files

Create:

src/nps/models/toy/optimality.py
tests/models/test_projected_optimality.py

------------------------------------------------------------------------

# 2️⃣ Implement Projected Residual

File: src/nps/models/toy/optimality.py

Implement:

``` python
import numpy as np

def project_box(w: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> np.ndarray:
    return np.minimum(np.maximum(w, lower), upper)

def projected_residual(
    w: np.ndarray,
    grad: np.ndarray,
    lower: np.ndarray,
    upper: np.ndarray,
    eta: float = 1e-2,
) -> float:
    # Compute || w - Π_Ω(w + eta * grad) ||
    w_step = w + eta * grad
    w_proj = project_box(w_step, lower, upper)
    return float(np.linalg.norm(w - w_proj))
```

------------------------------------------------------------------------

# 3️⃣ Test: Residual Small at Equilibrium

File: tests/models/test_projected_optimality.py

Test 1:

-   m = 8
-   radius = 1
-   theta = 0.7
-   Build neighborhood + sparse Q
-   Compute w\* using existing equilibrium solver
-   Compute grad = grad_phi_sparse(w\*, theta, Q)
-   Compute residual
-   Assert residual \< 1e-4

------------------------------------------------------------------------

# 4️⃣ Test: Residual Decreases During Iteration

Test 2:

-   Run projected gradient ascent manually
-   Track residual each step
-   Assert residual_final \< residual_initial

Example logic:

``` python
residuals = []
for _ in range(steps):
    grad = grad_phi_sparse(w, theta, Q)
    r = projected_residual(w, grad, lower, upper)
    residuals.append(r)
    w = project_box(w + lr * grad, lower, upper)

assert residuals[-1] < residuals[0]
```

------------------------------------------------------------------------

# 5️⃣ Optional Interior Check

If equilibrium is interior (all coordinates strictly between 0 and 1),
assert \|\|grad\|\| \< tolerance.

------------------------------------------------------------------------

# 6️⃣ Verification

All must pass:

pytest mypy src ruff check .

------------------------------------------------------------------------

# 🚫 Non-Goals

Do NOT:

-   Modify certified CAS layers
-   Add scipy.optimize
-   Add operator-theoretic content

------------------------------------------------------------------------

# ✅ Completion Condition

-   projected_residual implemented
-   Residual small at equilibrium
-   Residual decreases during iteration
-   All checks pass
