from __future__ import annotations

import numpy as np

from nps.solvers.equilibrium_candidates import (
    classify_hessian_spectrum,
    generate_deterministic_starts,
    select_candidate_for_regime,
)


def test_generate_deterministic_starts_is_deterministic_and_interior() -> None:
    s1 = generate_deterministic_starts(5)
    s2 = generate_deterministic_starts(5)
    assert len(s1) == len(s2)
    for a, b in zip(s1, s2, strict=True):
        assert np.allclose(a, b)
        assert np.all(a > 0.0)
        assert np.all(a < 1.0)


def test_classify_hessian_spectrum_flags() -> None:
    cls_neg = classify_hessian_spectrum(np.array([-2.0, -1.0, -0.5]), eps=1e-8)
    assert cls_neg["is_neg_def"] is True
    assert cls_neg["is_pos_def"] is False
    assert cls_neg["is_hyperbolic"] is True

    cls_pos = classify_hessian_spectrum(np.array([0.5, 1.0, 2.0]), eps=1e-8)
    assert cls_pos["is_pos_def"] is True
    assert cls_pos["is_neg_def"] is False
    assert cls_pos["is_hyperbolic"] is True

    cls_indef = classify_hessian_spectrum(np.array([-1.0, 0.5, 2.0]), eps=1e-8)
    assert cls_indef["is_indef"] is True


def test_select_candidate_for_regime_prefers_small_grad_then_margin() -> None:
    c1 = {
        "w": [0.1],
        "grad_norm_2": 1e-3,
        "hessian_spectrum": {
            "is_neg_def": True,
            "is_pos_def": False,
            "is_hyperbolic": True,
            "max_eigenvalue": -1.0,
            "min_eigenvalue": -2.0,
            "min_abs_eigenvalue": 1.0,
        },
    }
    c2 = {
        "w": [0.2],
        "grad_norm_2": 1e-6,
        "hessian_spectrum": {
            "is_neg_def": True,
            "is_pos_def": False,
            "is_hyperbolic": True,
            "max_eigenvalue": -0.1,
            "min_eigenvalue": -10.0,
            "min_abs_eigenvalue": 0.1,
        },
    }

    chosen = select_candidate_for_regime([c1, c2], objective="maximize", regime="strict_concave")
    assert chosen is c2
