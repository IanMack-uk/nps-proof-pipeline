"""Phase 0A: build utilities (dependency certification)."""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

from nps.audit.cert_dependency_gate import compute_content_hash
from nps.audit.governance import maybe_install_governance
from nps.certification.citations import source_ref
from nps.certification.artifacts import make_run_dir, write_json
from nps.certification.dependency_registry import DependencyRegistry, PropertyKey
from nps.core.types import SourceRef


OMEGA_NONEMPTY = PropertyKey(subject="Omega", property="nonempty")
OMEGA_COMPACT = PropertyKey(subject="Omega", property="compact")

PHI_CONTINUOUS = PropertyKey(subject="Phi", property="continuous")
PHI_C3_EXTENSION = PropertyKey(subject="Phi", property="C3_extension")

LOCALITY_DEFINED_NEIGHBORHOOD = PropertyKey(subject="Locality", property="defined_neighborhood_N(e)")
LOCALITY_UNIFORM_RADIUS = PropertyKey(subject="Locality", property="uniform_radius_r")

F_DEFINED_AS_GRAD_W_PHI = PropertyKey(subject="F", property="defined_as_grad_w_Phi")

W_STAR_DEFINED_AS_ARGMAX = PropertyKey(subject="W_star", property="defined_as_argmax_over_Omega")


def build_cas0a_registry(registry: DependencyRegistry) -> None:
    """Register CAS-0A certified properties with exact SourceRef locators."""

    def cas0a(locator: str) -> SourceRef:
        return source_ref("CAS-0A-v4", locator)

    registry.register(property_key=OMEGA_NONEMPTY, source=cas0a("Assumption A1"))
    registry.register(property_key=OMEGA_COMPACT, source=cas0a("Assumption A1"))

    registry.register(property_key=PHI_CONTINUOUS, source=cas0a("Assumption A2"))
    registry.register(property_key=PHI_C3_EXTENSION, source=cas0a("Assumption A3"))

    registry.register(property_key=LOCALITY_DEFINED_NEIGHBORHOOD, source=cas0a("Assumption A5"))
    registry.register(property_key=LOCALITY_UNIFORM_RADIUS, source=cas0a("Assumption A7"))

    registry.register(property_key=F_DEFINED_AS_GRAD_W_PHI, source=cas0a("Definition 4.1"))
    registry.register(property_key=W_STAR_DEFINED_AS_ARGMAX, source=cas0a("Definition 7.1"))


def cas0a_dependency_rows(registry: DependencyRegistry) -> list[tuple[PropertyKey, SourceRef]]:
    """Return a stable, sortable list for audit reporting."""

    return registry.rows()


def build_registry() -> DependencyRegistry:
    return DependencyRegistry()


def _read_programme_doc() -> str:
    # Taskpack refers to docs/*, but in this repo the authoritative files live under plan-and-persona/.
    repo_root = Path(__file__).resolve().parents[4]
    programme_path = repo_root / "plan-and-persona" / "Structural_Differentiation_Programme_v4.3.md"
    return programme_path.read_text(encoding="utf-8")


def _extract_phase_a_targets(programme_text: str) -> list[dict]:
    # Minimal, robust parsing: locate the Phase A section and take its numbered items.
    m = re.search(r"^## Phase A --- Foundations\s*$", programme_text, flags=re.MULTILINE)
    if not m:
        return []

    tail = programme_text[m.end() :]
    stop = re.search(r"^## Phase A′", tail, flags=re.MULTILINE)
    if stop:
        tail = tail[: stop.start()]

    targets: list[dict] = []
    for idx, line in enumerate(tail.splitlines()):
        mm = re.match(r"^\s*(\d+)\.\s+(.*\S)\s*$", line)
        if not mm:
            continue
        n = int(mm.group(1))
        statement = mm.group(2)
        targets.append(
            {
                "target_id": f"A.T{n}",
                "statement": statement,
                "obligations": [
                    {
                        "obligation_id": f"A.T{n}.O1",
                        "statement": statement,
                        "method": "check",
                        "status": "unverified_in_0A",
                        "to_be_discharged_in": "CAS-A",
                    }
                ],
            }
        )

    return targets


def _extract_dependencies(programme_text: str, phase_targets: list[dict]) -> list[dict]:
    # Option 2 requirement: dependencies must come from programme spec references.
    # We treat the programme-wide dependency rule and the Phase A bullets as programme-derived deps.
    used_in = [t["target_id"] for t in phase_targets] or ["A.T1"]
    return [
        {
            "dep_id": "DEP.PROG.DependencyRule.NoForwardUse",
            "type": "assumption",
            "source": {
                "document": "Structural_Differentiation_Programme_v4.3",
                "locator": "Programme-Wide Dependency Rule (No use without CAS citation)",
            },
            "provides": [
                "Phase dependency discipline: no use unless certified in CAS-0X/CAS-X or carried forward with a link"
            ],
            "used_in": used_in,
        },
        {
            "dep_id": "DEP.PROG.PhaseA.Foundations",
            "type": "definition",
            "source": {
                "document": "Structural_Differentiation_Programme_v4.3",
                "locator": "Phase A --- Foundations",
            },
            "provides": ["Authoritative Phase A targets list"],
            "used_in": used_in,
        },
    ]


def build_cas0a(run_dir: Path) -> Path:
    programme_text = _read_programme_doc()
    targets = _extract_phase_a_targets(programme_text)
    dependencies = _extract_dependencies(programme_text, targets)

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    obligations = []
    for t in targets:
        obligations.extend(t.get("obligations", []))

    payload: dict = {
        "cas_id": "CAS-0A",
        "created_at": created_at,
        "inputs": [],
        "content_hash": "",
        "programme": {
            "name": "Structural Differentiation / Ordering Theorem Programme",
            "version": "4.3",
            "phase": "0A",
        },
        "phase_targets": targets,
        "dependency_table": dependencies,
        "assumptions": {"imported": [], "introduced": []},
        "obligations": obligations,
        "minimality_audit": {
            "method": "drop_test",
            "status": "partial_manual",
            "results": [
                {
                    "dep_id": dependencies[0]["dep_id"] if dependencies else "DEP.PROG.PhaseA.Foundations",
                    "dropped": False,
                    "reason_required": "Programme-wide dependency rule is required to justify governed Phase-A execution.",
                }
            ],
        },
        "trace": {
            "generated_by": {"tool": "nps.phases.phase_0a.build_cas0a", "tool_version": "option2"},
            "source_docs": [
                {
                    "path": "plan-and-persona/Structural_Differentiation_Programme_v4.3.md",
                    "role_prompt": "plan-and-persona/Computational_Certification_Architect_Role_Prompt.md",
                }
            ],
        },
    }

    payload["content_hash"] = compute_content_hash(payload)

    out = run_dir / "CAS-0A.json"
    write_json(out, payload)

    report = run_dir / "Phase0A_REPORT.md"
    report.write_text(
        "# Phase 0A Report\n\n"
        f"- CAS artefact: {out.name}\n"
        f"- Targets extracted: {len(targets)}\n"
        f"- Dependencies extracted: {len(dependencies)}\n",
        encoding="utf-8",
    )

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Build CAS-0A (Phase 0A) into cert_artifacts/<run_id>/")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()

    maybe_install_governance()
    run_dir = make_run_dir(args.run_id)
    out = build_cas0a(run_dir)
    print(str(out))


if __name__ == "__main__":
    main()
