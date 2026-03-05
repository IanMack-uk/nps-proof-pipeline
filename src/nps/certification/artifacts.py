from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def get_cert_artifacts_root() -> Path:
    """Return the repository-level certification artefacts root directory."""

    # repo root assumed to be 3 levels above: src/nps/certification
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "cert_artifacts"


def make_run_dir(run_id: str | None = None) -> Path:
    root = get_cert_artifacts_root()
    if run_id is None:
        run_id = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

    run_dir = root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    path.write_text(payload, encoding="utf-8")


def get_experiments_dir(run_dir: Path) -> Path:
    d = run_dir / "experiments"
    d.mkdir(parents=True, exist_ok=True)
    return d
