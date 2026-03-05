from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ImportGraph:
    nodes: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]


def load_import_graph_from_edges_json(path: Path) -> ImportGraph:
    payload = json.loads(path.read_text(encoding="utf-8"))
    nodes = tuple(payload.get("nodes", []))
    edges = tuple((a, b) for a, b in payload.get("edges", []))
    return ImportGraph(nodes=nodes, edges=edges)


def _phase_of(module: str) -> str | None:
    parts = module.split(".")
    if len(parts) >= 3 and parts[0] == "nps" and parts[1] == "phases":
        return parts[2]
    return None


def validate_phase_order_nonforward_imports(graph: ImportGraph, policy: dict) -> list[str]:
    phase_order = policy.get("phase_order", [])
    rules = policy.get("rules", {})
    forbid_forward = bool(rules.get("forbid_forward_imports", True))
    allow_same = bool(rules.get("allow_same_phase_imports", True))
    allow_backward = bool(rules.get("allow_backward_imports", True))

    if not forbid_forward:
        return []

    rank = {p: i for i, p in enumerate(phase_order)}

    errors: list[str] = []
    for a, b in graph.edges:
        pa = _phase_of(a)
        pb = _phase_of(b)
        if pa is None or pb is None:
            continue
        if pa not in rank or pb not in rank:
            continue

        if pa == pb:
            if not allow_same:
                errors.append(f"Same-phase import forbidden: {a} -> {b}")
            continue

        if rank[pb] < rank[pa]:
            if not allow_backward:
                errors.append(f"Backward import forbidden: {a} -> {b}")
            continue

        if rank[pb] > rank[pa]:
            errors.append(f"Forward-phase import forbidden: {a} -> {b}")

    return errors


def validate_import_policy(graph: ImportGraph, policy: dict) -> list[str]:
    pol = policy.get("policy")
    if pol == "phase_order_nonforward_imports":
        return validate_phase_order_nonforward_imports(graph, policy)
    raise ValueError(f"Unknown import policy: {pol}")
