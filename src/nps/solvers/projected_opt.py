from __future__ import annotations

from typing import Callable

import numpy as np


def _project_box(w: np.ndarray, lower, upper) -> np.ndarray:
    return np.clip(w, float(lower), float(upper))


def projected_gradient_ascent(
    value_fn: Callable[[np.ndarray], float],
    grad_fn: Callable[[np.ndarray], np.ndarray],
    *,
    w_init,
    lower,
    upper,
    step: float = 0.1,
    max_iter: int = 500,
    tol: float = 1e-8,
) -> tuple[np.ndarray, dict]:
    w = _project_box(np.asarray(w_init, dtype=float), lower, upper)

    values: list[float] = []
    termination_reason = "max_iter"

    for it in range(int(max_iter)):
        v = float(value_fn(w))
        values.append(v)

        g = np.asarray(grad_fn(w), dtype=float)
        ginf = float(np.linalg.norm(g, ord=np.inf))
        if ginf <= float(tol):
            termination_reason = "grad_tol"
            break

        w_next = _project_box(w + float(step) * g, lower, upper)

        if float(np.linalg.norm(w_next - w, ord=np.inf)) <= float(tol):
            w = w_next
            termination_reason = "step_tol"
            break

        w = w_next

    info = {
        "method": "projected_gradient_ascent",
        "step": float(step),
        "max_iter": int(max_iter),
        "tol": float(tol),
        "iterations": int(len(values) - 1),
        "termination_reason": termination_reason,
        "values": values,
    }
    return w, info
