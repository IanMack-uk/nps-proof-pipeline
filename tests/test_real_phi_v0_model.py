from __future__ import annotations

import numpy as np

from nps.models.real_phi_v0 import make_real_phi_v0_test_spec


def test_real_phi_v0_shapes_and_finiteness() -> None:
    spec = make_real_phi_v0_test_spec()
    w = 0.5 * np.ones(spec.m)

    v = spec.value(w)
    g = spec.grad(w)
    H = spec.hess(w)

    assert np.isfinite(v)
    assert g.shape == (spec.m,)
    assert H.shape == (spec.m, spec.m)
    assert np.all(np.isfinite(g))
    assert np.all(np.isfinite(H))

    # Should be symmetric (up to numerical roundoff).
    assert float(np.max(np.abs(H - H.T))) <= 1e-8
