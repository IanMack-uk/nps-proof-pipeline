from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SignedObjective:
    base: Any
    sign: float
    extension_id: str

    def __getattr__(self, name: str):
        return getattr(self.base, name)

    @property
    def certified_objective(self) -> str:
        if self.sign == 1.0:
            return "phi"
        if self.sign == -1.0:
            return "minus_phi"
        raise ValueError(f"SignedObjective: unsupported sign={self.sign}")

    def value(self, w, *, theta: float | None = None):
        try:
            v = self.base.value(w, theta=theta)
        except TypeError:
            v = self.base.value(w)
        return float(self.sign) * float(v)

    def grad(self, w, *, theta: float | None = None):
        try:
            g = self.base.grad(w, theta=theta)
        except TypeError:
            g = self.base.grad(w)
        return float(self.sign) * g

    def hess(self, w, *, theta: float | None = None):
        try:
            h = self.base.hess(w, theta=theta)
        except TypeError:
            h = self.base.hess(w)
        return float(self.sign) * h
