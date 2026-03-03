"""RelationalPotential symbol object stub (Phase A).

Defines a typed placeholder object with explicit domain/codomain and sourcing.
"""

from __future__ import annotations

from nps.certification.dependency_registry import PropertyKey
from nps.core.locality import LocalityScope
from nps.core.regularity import RegularityClass
from nps.core.types import MathematicalObject, SourceRef


def make_relational_potential(*, source: SourceRef) -> MathematicalObject:
    requires = {PropertyKey(subject="RelationalPotential", property="definition")}
    return MathematicalObject(
        name="RelationalPotential",
        domain="Network",
        codomain="Real",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source,
        requires=requires,
    )
