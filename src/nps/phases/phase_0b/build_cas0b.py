"""Phase 0B: certify Phase B targets and dependencies."""

from __future__ import annotations

import argparse
import re
import json
from datetime import datetime, timezone
from pathlib import Path

from nps.audit.cert_dependency_gate import compute_content_hash
from nps.audit.governance import maybe_install_governance
from nps.certification.artifacts import make_run_dir, write_json


def _read_programme_doc() -> str:
    repo_root = Path(__file__).resolve().parents[4]
    programme_path = repo_root / "plan-and-persona" / "Structural_Differentiation_Programme_v4.3.md"
    return programme_path.read_text(encoding="utf-8")


def _extract_phase_b_targets(programme_text: str) -> list[dict]:
    m = re.search(r"^## Phase B --- Local Equilibrium Analysis\s*$", programme_text, flags=re.MULTILINE)
    if not m:
        return []

    tail = programme_text[m.end() :]
    stop = re.search(r"^## Phase B′", tail, flags=re.MULTILINE)
    if stop:
        tail = tail[: stop.start()]

    targets: list[dict] = []
    for line in tail.splitlines():
        mm = re.match(r"^\s*(\d+)\.\s+(.*\S)\s*$", line)
        if not mm:
            continue
        n = int(mm.group(1))
        statement = mm.group(2)
        targets.append(
            {
                "target_id": f"B.T{n}",
                "statement": statement,
                "obligations": [
                    {
                        "obligation_id": f"B.T{n}.O1",
                        "statement": statement,
                        "method": "check",
                        "status": "unverified_in_0B",
                        "to_be_discharged_in": "CAS-B",
                    }
                ],
            }
        )

    return targets


def _extract_dependencies(programme_text: str, phase_targets: list[dict]) -> list[dict]:
    used_in = [t["target_id"] for t in phase_targets] or ["B.T1"]
    return [
        {
            "dep_id": "DEP.PROG.PhaseB.OperatorObjects",
            "type": "definition",
            "source": {
                "document": "Structural_Differentiation_Programme_v4.3",
                "locator": "Phase B --- Local Equilibrium Analysis",
            },
            "provides": ["Authoritative Phase B targets list and operator prerequisites"],
            "used_in": used_in,
        }
    ]


def _phase_group_b_defs_dependencies_and_obligations(*, used_in: list[str]) -> tuple[list[dict], list[dict]]:
    deps: list[dict] = [
        {
            "dep_id": "DEP.P1.DEF.MARGINAL_STRUCTURAL_FIELD",
            "type": "definition",
            "source": "NetworkPotential_Paper1_OperatorTheory_v0.6",
            "locator": {"section": "2.1", "definition": "2.1.1"},
            "provides": ["Definition of marginal structural field F(w) := ∇Φ(w)"],
            "used_in": used_in,
        },
        {
            "dep_id": "DEP.P1.DEF.HESSIAN_OPERATOR",
            "type": "definition",
            "source": "NetworkPotential_Paper1_OperatorTheory_v0.6",
            "locator": {"section": "2.2", "definition": "2.2.1"},
            "provides": ["Definition of Hessian / Jacobian operator J(w) := ∇F(w) = ∇²Φ(w)"],
            "used_in": used_in,
        },
        {
            "dep_id": "DEP.P1.DEF.HYPERBOLIC_EQUILIBRIUM",
            "type": "definition",
            "source": "NetworkPotential_Paper1_OperatorTheory_v0.6",
            "locator": {"section": "2.4", "definition": "2.4.2"},
            "provides": ["Definition of hyperbolic equilibrium via nonsingularity of equilibrium Hessian"],
            "used_in": used_in,
        },
        {
            "dep_id": "DEP.P1.IDENTITY.SUSCEPTIBILITY_RESPONSE",
            "type": "identity",
            "source": "NetworkPotential_Paper1_OperatorTheory_v0.6",
            "locator": {"section": "2.4-2.5", "note": "discussion"},
            "provides": ["Susceptibility / response identity context for equilibrium perturbations"],
            "used_in": used_in,
        },
        {
            "dep_id": "DEP.THESIS.PROB.MAXIMISATION_STATEMENT",
            "type": "problem_statement",
            "source": {
                "document": "Network-Potential-and-Relational-Optimisation-mathematics-thesis",
                "locator": {
                    "spec": "docs/specs/phase_group_b_defs/Paper1_Thesis_Definition_Blocks.md",
                    "section": "Thesis — Maximisation problem statement (most explicit match found)",
                    "paragraph_indices": [138],
                },
            },
            "provides": ["Convention: equilibrium as maximisation of network potential over admissible weights"],
            "used_in": used_in,
        },
    ]

    obls: list[dict] = [
        {
            "obligation_id": "OBL.B.REGIME.INTERIOR",
            "statement": "The equilibrium candidate is interior: w* ∈ W°.",
            "method": "check",
            "status": "to_be_discharged_in_B",
        },
        {
            "obligation_id": "OBL.B.EQ.STATIONARITY",
            "statement": "Interior equilibrium satisfies F(w*) = ∇Φ(w*) = 0.",
            "method": "check",
            "status": "to_be_discharged_in_B",
        },
        {
            "obligation_id": "OBL.B.NONDEGEN.HYPERBOLIC",
            "statement": "Hyperbolicity holds: det J(w*) ≠ 0 (equivalently min |eig(J)| > eps).",
            "method": "check",
            "status": "to_be_discharged_in_B",
        },
        {
            "obligation_id": "OBL.B.NONDEGEN.STRICT_CONCAVITY",
            "statement": "Strict concavity holds: J(w*) ≺ 0.",
            "method": "check",
            "status": "optional_regime",
        },
        {
            "obligation_id": "OBL.B.RESPONSE.IDENTITY.SIGN",
            "statement": "The response identity sign matches the maximisation convention.",
            "method": "derivation_and_check",
            "status": "to_be_discharged_in_B_prime",
        },
    ]

    return deps, obls


def build_cas0b(run_dir: Path, *, input_path: Path) -> Path:
    casa = json.loads(input_path.read_text(encoding="utf-8"))
    upstream_id = casa.get("cas_id")
    if not isinstance(upstream_id, str) or not upstream_id:
        raise RuntimeError("Phase0B: invalid CAS-A input (missing cas_id)")

    programme_text = _read_programme_doc()
    targets = _extract_phase_b_targets(programme_text)
    used_in = [t["target_id"] for t in targets] or ["B.T1"]
    dependencies = _extract_dependencies(programme_text, targets)
    defs_deps, defs_obls = _phase_group_b_defs_dependencies_and_obligations(used_in=used_in)
    dependencies.extend(defs_deps)

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    obligations = []
    for t in targets:
        obligations.extend(t.get("obligations", []))
    obligations.extend(defs_obls)

    payload: dict = {
        "cas_id": "CAS-0B",
        "created_at": created_at,
        "inputs": [upstream_id],
        "content_hash": "",
        "programme": {
            "name": "Structural Differentiation / Ordering Theorem Programme",
            "version": "4.3",
            "phase": "0B",
        },
        "phase_targets": targets,
        "dependency_table": dependencies,
        "assumptions": {
            "imported": casa.get("assumptions", {}).get("imported", []),
            "introduced": [],
        },
        "obligations": obligations,
        "minimality_audit": {
            "method": "drop_test",
            "status": "placeholder",
            "results": [],
        },
        "trace": {
            "generated_by": {"tool": "nps.phases.phase_0b.build_cas0b", "tool_version": "option2"},
            "consumed": {"casa_path": str(input_path)},
        },
    }

    payload["content_hash"] = compute_content_hash(payload)

    out = run_dir / "CAS-0B.json"
    write_json(out, payload)

    (run_dir / "Phase0B_REPORT.md").write_text(
        "# Phase 0B Report\n\n"
        f"- CAS artefact: {out.name}\n"
        f"- Upstream: {upstream_id}\n"
        f"- Targets extracted: {len(targets)}\n",
        encoding="utf-8",
    )

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Build CAS-0B (Phase 0B) into cert_artifacts/<run_id>/")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    maybe_install_governance()
    run_dir = make_run_dir(args.run_id)
    out = build_cas0b(run_dir, input_path=Path(args.input))
    print(str(out))


if __name__ == "__main__":
    main()
