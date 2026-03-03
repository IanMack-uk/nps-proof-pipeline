"""Core error types for the Programme (Phase 0A).

Errors here represent violations of explicit mathematical or certification
constraints.
"""

from __future__ import annotations


class MathematicalInconsistency(Exception):
    """Raised when an explicit mathematical requirement is violated."""
