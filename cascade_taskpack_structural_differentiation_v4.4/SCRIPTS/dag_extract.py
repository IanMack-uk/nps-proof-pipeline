"""Repository Import DAG extraction helper.

Extracts a deterministic import DAG from `src/nps/**/*.py` and writes:

- codebase_dependency_dag.md
- codebase_dependency_edges.json

into the specified output directory.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from nps.audit.import_graph import (
    extract_import_graph,
    render_import_graph_markdown,
    write_edges_json,
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".", help="Repo root path")
    ap.add_argument("--out-dir", required=True, help="Directory to write artefacts")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    graph = extract_import_graph(repo_root)
    (out / "codebase_dependency_dag.md").write_text(
        render_import_graph_markdown(graph, title="Codebase Dependency DAG (Extracted)"),
        encoding="utf-8",
    )
    write_edges_json(out / "codebase_dependency_edges.json", graph)


if __name__ == "__main__":
    main()
