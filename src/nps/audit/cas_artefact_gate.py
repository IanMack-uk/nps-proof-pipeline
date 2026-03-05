from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


_ENV_FLAG = "NPS_CAS_GATE"


@dataclass(frozen=True, slots=True)
class CasArtefactRequirements:
    required_files: tuple[str, ...] = (
        "final_dependency_dag.md",
        "final_dependency_edges.json",
        "phase_import_policy_check.json",
        "deletion_ledger.md",
        "REPORT.md",
    )


_gate_enabled = False


def is_cas_gate_enabled() -> bool:
    return _gate_enabled


def install_cas_gate() -> None:
    global _gate_enabled
    _gate_enabled = True


def uninstall_cas_gate() -> None:
    global _gate_enabled
    _gate_enabled = False


def maybe_install_cas_gate() -> None:
    if os.environ.get(_ENV_FLAG) == "1":
        install_cas_gate()


def validate_cas_artefacts(artefact_dir: str | Path) -> None:
    """Validate required CAS artefacts exist and satisfy minimal schema rules.

    Raises RuntimeError with audit-grade details on failure.
    """

    p = Path(artefact_dir)

    req = CasArtefactRequirements()

    missing = [name for name in req.required_files if not (p / name).exists()]
    if missing:
        raise RuntimeError(
            "CASArtefactGate: missing required artefacts\n"
            f"Artefact dir: {p}\n"
            f"Missing: {missing}"
        )

    # final_dependency_edges.json schema
    edges_path = p / "final_dependency_edges.json"
    edges_payload = json.loads(edges_path.read_text(encoding="utf-8"))
    if not isinstance(edges_payload, dict) or "nodes" not in edges_payload or "edges" not in edges_payload:
        raise RuntimeError(
            "CASArtefactGate: invalid schema in final_dependency_edges.json\n"
            f"Path: {edges_path}\n"
            "Required keys: nodes, edges"
        )

    policy_check_path = p / "phase_import_policy_check.json"
    policy_payload = json.loads(policy_check_path.read_text(encoding="utf-8"))
    required_keys = ("policy", "phase_order", "violations")
    if not isinstance(policy_payload, dict) or any(k not in policy_payload for k in required_keys):
        raise RuntimeError(
            "CASArtefactGate: invalid schema in phase_import_policy_check.json\n"
            f"Path: {policy_check_path}\n"
            f"Required keys: {list(required_keys)}"
        )

    violations = policy_payload.get("violations")
    if violations != []:
        raise RuntimeError(
            "CASArtefactGate: import policy violations present\n"
            f"Path: {policy_check_path}\n"
            f"Violations: {violations}"
        )
