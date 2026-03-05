from __future__ import annotations

import os
from pathlib import Path

import pytest

from nps.audit.governance import maybe_validate_run_dir_integrity
from nps.audit.run_directory_integrity import validate_run_directory_integrity


def _touch(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{}\n", encoding="utf-8")


def test_integrity_passes_with_only_canonical_files(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    for name in [
        "CAS-0A.json",
        "CAS-A.json",
        "CAS-Ap.json",
        "CAS-0B.json",
        "CAS-B.json",
        "CAS-Bp.json",
    ]:
        _touch(run_dir / name)

    validate_run_directory_integrity(run_dir)


def test_integrity_fails_on_variant_in_root(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)
    _touch(run_dir / "CAS-B.json")
    _touch(run_dir / "CAS-B_phi.json")

    with pytest.raises(RuntimeError, match="Move variants to experiments"):
        validate_run_directory_integrity(run_dir)


def test_integrity_passes_on_variant_in_experiments(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)
    _touch(run_dir / "CAS-B.json")
    _touch(run_dir / "experiments" / "CAS-B_phi.json")

    validate_run_directory_integrity(run_dir)


def test_env_gated_maybe_validate(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)
    _touch(run_dir / "CAS-B.json")
    _touch(run_dir / "CAS-B_phi.json")

    monkeypatch.delenv("NPS_RUN_DIR_INTEGRITY", raising=False)
    maybe_validate_run_dir_integrity(run_dir)

    monkeypatch.setenv("NPS_RUN_DIR_INTEGRITY", "1")
    with pytest.raises(RuntimeError):
        maybe_validate_run_dir_integrity(run_dir)
