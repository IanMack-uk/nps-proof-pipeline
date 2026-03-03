"""StructuralExposure symbol object stub (Phase A).

Defines a typed placeholder object with explicit domain/codomain and sourcing.
"""

from __future__ import annotations

from nps.certification.dependency_registry import PropertyKey
from nps.core.locality import LocalityScope
from nps.core.regularity import RegularityClass
from nps.core.types import MathematicalObject, SourceRef


def make_structural_exposure(*, source: SourceRef) -> MathematicalObject:
    requires = {PropertyKey(subject="StructuralExposure", property="definition")}
    return MathematicalObject(
        name="StructuralExposure",
        domain="Network",
        codomain="Real",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source,
        requires=requires,
    )
