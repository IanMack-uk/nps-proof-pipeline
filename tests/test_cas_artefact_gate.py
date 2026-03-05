from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from nps.audit.cas_artefact_gate import (
    install_cas_gate,
    is_cas_gate_enabled,
    maybe_install_cas_gate,
    uninstall_cas_gate,
    validate_cas_artefacts,
)


def _write_required_artefacts(tmp_path: Path, *, violations: list | None = None) -> None:
    (tmp_path / "final_dependency_dag.md").write_text("# DAG\n", encoding="utf-8")

    (tmp_path / "final_dependency_edges.json").write_text(
        json.dumps({"nodes": ["a"], "edges": [["a", "b"]]}, indent=2) + "\n",
        encoding="utf-8",
    )

    if violations is None:
        violations = []

    (tmp_path / "phase_import_policy_check.json").write_text(
        json.dumps(
            {
                "policy": "phase_order_nonforward_imports",
                "phase_order": ["phase_0a", "phase_a", "phase_b"],
                "violations": violations,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (tmp_path / "deletion_ledger.md").write_text("# Ledger\n", encoding="utf-8")
    (tmp_path / "REPORT.md").write_text("# Report\n", encoding="utf-8")


@pytest.fixture(autouse=True)
def _clean_gate_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("NPS_CAS_GATE", raising=False)
    uninstall_cas_gate()
    yield
    uninstall_cas_gate()


def test_valid_artefacts_pass(tmp_path: Path) -> None:
    _write_required_artefacts(tmp_path)
    validate_cas_artefacts(tmp_path)


def test_missing_artefact_fails(tmp_path: Path) -> None:
    _write_required_artefacts(tmp_path)
    (tmp_path / "deletion_ledger.md").unlink()
    with pytest.raises(RuntimeError) as exc:
        validate_cas_artefacts(tmp_path)
    assert "missing required artefacts" in str(exc.value)


def test_invalid_schema_fails(tmp_path: Path) -> None:
    _write_required_artefacts(tmp_path)
    (tmp_path / "final_dependency_edges.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(RuntimeError) as exc:
        validate_cas_artefacts(tmp_path)
    assert "invalid schema" in str(exc.value)


def test_gate_disabled_by_default() -> None:
    assert is_cas_gate_enabled() is False


def test_gate_enabled_via_environment_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    assert is_cas_gate_enabled() is False
    monkeypatch.setenv("NPS_CAS_GATE", "1")
    maybe_install_cas_gate()
    assert is_cas_gate_enabled() is True


def test_import_policy_violations_fail(tmp_path: Path) -> None:
    _write_required_artefacts(tmp_path, violations=[{"from": "x", "to": "y"}])
    with pytest.raises(RuntimeError) as exc:
        validate_cas_artefacts(tmp_path)
    assert "violations" in str(exc.value)
