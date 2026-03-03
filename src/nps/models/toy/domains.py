"""Toy compact domains.

Executable model instance — not general certified theory.
"""

from __future__ import annotations

from typing import cast

import numpy as np
from numpy.typing import NDArray

from nps.models.sandbox.domain_policies import DomainPolicy, NonnegativePolicy


def box_domain(m: int) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Return bounds for Ω = [0,1]^m."""

    lower = cast(NDArray[np.float64], np.zeros(m, dtype=np.float64))
    upper = cast(NDArray[np.float64], np.ones(m, dtype=np.float64))
    return lower, upper


def sample_omega(
    m: int,
    rng: np.random.Generator,
    *,
    policy: DomainPolicy | None = None,
) -> NDArray[np.float64]:
    """Sample w from the sandbox Ω policy (proof-target defaults to nonnegative)."""

    pol = policy if policy is not None else NonnegativePolicy()
    w = pol.sample(m, rng)
    lower, upper = box_domain(m)
    out = np.minimum(np.maximum(w, lower), upper)
    return cast(NDArray[np.float64], out.astype(np.float64))


def project_omega(
    w: NDArray[np.float64],
    *,
    policy: DomainPolicy | None = None,
) -> NDArray[np.float64]:
    """Project onto Ω under the selected sandbox policy (proof-target defaults to nonnegative)."""

    pol = policy if policy is not None else NonnegativePolicy()
    w2 = pol.project(w.astype(np.float64, copy=False))
    lower, upper = box_domain(len(w2))
    out = np.minimum(np.maximum(w2, lower), upper)
    return cast(NDArray[np.float64], out.astype(np.float64))
