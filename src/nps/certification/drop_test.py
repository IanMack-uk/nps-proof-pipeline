"""Drop test enforcement for the Programme (Phase Aʹ).

A drop test asserts that removing a required dependency breaks certification.
"""

from __future__ import annotations

from collections.abc import Callable

from nps.core.errors import MathematicalInconsistency


def expect_failure_on_drop(*, drop: Callable[[], None], action: Callable[[], None]) -> None:
    """Run a drop action and assert that subsequent action fails."""

    drop()
    try:
        action()
    except MathematicalInconsistency:
        return
    raise AssertionError("Expected MathematicalInconsistency after drop")
