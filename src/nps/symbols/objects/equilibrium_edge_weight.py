"""EquilibriumEdgeWeight symbol object stub (Phase A).

Defines a typed placeholder object with explicit domain/codomain and sourcing.
"""

from __future__ import annotations

from nps.certification.dependency_registry import PropertyKey
from nps.core.locality import LocalityScope
from nps.core.regularity import RegularityClass
from nps.core.types import MathematicalObject, SourceRef


def make_equilibrium_edge_weight(*, source: SourceRef) -> MathematicalObject:
    requires = {PropertyKey(subject="EquilibriumEdgeWeight", property="definition")}
    return MathematicalObject(
        name="EquilibriumEdgeWeight",
        domain="Edge",
        codomain="Real",
        regularity=RegularityClass.C0,
        locality=LocalityScope.LOCAL,
        source=source,
        requires=requires,
    )
