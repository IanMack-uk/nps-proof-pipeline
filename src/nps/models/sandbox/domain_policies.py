from __future__ import annotations

from typing import Protocol

import numpy as np
from numpy.typing import NDArray

from nps.core.errors import MathematicalInconsistency


class DomainPolicy(Protocol):
    def project(self, w: NDArray[np.float64]) -> NDArray[np.float64]:
        ...

    def sample(self, m: int, rng: np.random.Generator) -> NDArray[np.float64]:
        ...

    def is_admissible(self, w: NDArray[np.float64]) -> bool:
        ...


class NonnegativePolicy:
    upper: float = 1.0

    def __init__(self, upper: float = 1.0) -> None:
        if upper <= 0:
            raise MathematicalInconsistency("NonnegativePolicy upper must be > 0")
        self.upper = float(upper)

    def project(self, w: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.clip(w, 0.0, self.upper).astype(np.float64)

    def sample(self, m: int, rng: np.random.Generator) -> NDArray[np.float64]:
        return rng.uniform(0.0, self.upper, size=m).astype(np.float64)

    def is_admissible(self, w: NDArray[np.float64]) -> bool:
        return bool(np.all((0.0 <= w) & (w <= self.upper)))


class SignedPolicy:
    def project(self, w: NDArray[np.float64]) -> NDArray[np.float64]:
        return w.astype(np.float64, copy=False)

    def sample(self, m: int, rng: np.random.Generator) -> NDArray[np.float64]:
        return rng.uniform(-1.0, 1.0, size=m).astype(np.float64)

    def is_admissible(self, w: NDArray[np.float64]) -> bool:
        _ = w
        return True
