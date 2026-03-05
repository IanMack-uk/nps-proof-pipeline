from __future__ import annotations

import numpy as np

from nps.models.signed_objective import SignedObjective


class _Base:
    extension_id = "base"

    def value(self, w, *, theta=None):
        return float(np.sum(w) + (0.0 if theta is None else float(theta)))

    def grad(self, w, *, theta=None):
        _ = theta
        return np.ones_like(w, dtype=float)

    def hess(self, w, *, theta=None):
        _ = w
        _ = theta
        return np.eye(3, dtype=float)


def test_signed_objective_sign_and_certified_objective() -> None:
    base = _Base()
    w = np.array([1.0, 2.0, 3.0])

    so = SignedObjective(base=base, sign=1.0, extension_id="x")
    assert so.certified_objective == "phi"
    assert so.value(w, theta=2.0) == 8.0
    assert np.allclose(so.grad(w, theta=2.0), np.ones(3))
    assert np.allclose(so.hess(w, theta=2.0), np.eye(3))

    so2 = SignedObjective(base=base, sign=-1.0, extension_id="x")
    assert so2.certified_objective == "minus_phi"
    assert so2.value(w, theta=2.0) == -8.0
    assert np.allclose(so2.grad(w, theta=2.0), -np.ones(3))
    assert np.allclose(so2.hess(w, theta=2.0), -np.eye(3))
