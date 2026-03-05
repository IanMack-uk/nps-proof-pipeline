from __future__ import annotations

import json
from pathlib import Path

from nps.certification.artifacts import get_cert_artifacts_root, make_run_dir, write_json


def test_get_cert_artifacts_root_points_to_repo_dir() -> None:
    root = get_cert_artifacts_root()
    assert root.name == "cert_artifacts"


def test_make_run_dir_creates_under_cert_artifacts(tmp_path: Path, monkeypatch) -> None:
    # Ensure we don't write into the real repo during tests.
    from nps import certification as _cert_pkg

    # Patch artifacts module to treat tmp_path as repo root by patching __file__ resolution.
    # We do this by monkeypatching the function itself to a tmp-rooted variant.
    import nps.certification.artifacts as artifacts

    def _tmp_root() -> Path:
        return tmp_path / "cert_artifacts"

    monkeypatch.setattr(artifacts, "get_cert_artifacts_root", _tmp_root)

    run_dir = make_run_dir("unit-test")
    assert run_dir.exists()
    assert run_dir.is_dir()
    assert run_dir.parent == _tmp_root()


def test_write_json_writes_parseable_json(tmp_path: Path) -> None:
    p = tmp_path / "out.json"
    write_json(p, {"b": 2, "a": 1})

    loaded = json.loads(p.read_text(encoding="utf-8"))
    assert loaded == {"a": 1, "b": 2}
