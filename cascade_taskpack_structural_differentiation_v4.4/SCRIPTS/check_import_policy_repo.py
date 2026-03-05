"""Repository import policy checker.

Reads a policy JSON (e.g. `docs/specs/import_policy.json`) and validates an
extracted import-edge list (json) against it.

Exit status:
- 0: policy satisfied
- 1: violations detected
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nps.audit.import_policy import load_import_graph_from_edges_json, validate_import_policy


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", required=True, help="Path to import policy json")
    ap.add_argument("--edges", required=True, help="Path to extracted edges json")
    args = ap.parse_args()

    policy_path = Path(args.policy)
    edges_path = Path(args.edges)

    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    graph = load_import_graph_from_edges_json(edges_path)

    errors = validate_import_policy(graph, policy)
    if errors:
        sys.stderr.write("Import policy violations:\n")
        for e in errors:
            sys.stderr.write(f"- {e}\n")
        raise SystemExit(1)

    print("OK: import policy satisfied")


if __name__ == "__main__":
    main()
