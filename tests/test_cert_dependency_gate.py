from __future__ import annotations

import json
from pathlib import Path

import pytest

from nps.audit.cert_dependency_gate import (
    install_cert_dependency_gate,
    is_cert_dependency_gate_enabled,
    maybe_install_cert_dependency_gate,
    uninstall_cert_dependency_gate,
    validate_cert_dependency_integrity,
)


def _write_cas(path: Path, *, cas_id: str, inputs: list[str]) -> None:
    payload = {
        "cas_id": cas_id,
        "created_at": "2026-03-04T00:00:00Z",
        "inputs": inputs,
        "content_hash": "",  # filled below
        "data": {"value": cas_id},
    }

    # compute hash of payload excluding metadata fields (matches implementation)
    stripped = {"data": payload["data"]}
    canonical = json.dumps(stripped, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    import hashlib

    payload["content_hash"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


@pytest.fixture(autouse=True)
def _clean_gate(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("NPS_CERT_DEP_GATE", raising=False)
    uninstall_cert_dependency_gate()
    yield
    uninstall_cert_dependency_gate()


def test_valid_chain_passes(tmp_path: Path) -> None:
    _write_cas(tmp_path / "CAS-0A.json", cas_id="CAS-0A", inputs=[])
    _write_cas(tmp_path / "CAS-A.json", cas_id="CAS-A", inputs=["CAS-0A"])
    _write_cas(tmp_path / "CAS-0B.json", cas_id="CAS-0B", inputs=["CAS-A"])
    _write_cas(tmp_path / "CAS-B.json", cas_id="CAS-B", inputs=["CAS-0B"])
    _write_cas(tmp_path / "CAS-0C.json", cas_id="CAS-0C", inputs=["CAS-B"])
    _write_cas(tmp_path / "CAS-C.json", cas_id="CAS-C", inputs=["CAS-0C"])
    _write_cas(tmp_path / "CAS-0D.json", cas_id="CAS-0D", inputs=["CAS-C"])
    _write_cas(tmp_path / "CAS-D.json", cas_id="CAS-D", inputs=["CAS-0D"])

    validate_cert_dependency_integrity(tmp_path)


def test_missing_prerequisite_fails(tmp_path: Path) -> None:
    _write_cas(tmp_path / "CAS-0A.json", cas_id="CAS-0A", inputs=[])
    _write_cas(tmp_path / "CAS-A.json", cas_id="CAS-A", inputs=["CAS-0A"])
    _write_cas(tmp_path / "CAS-0B.json", cas_id="CAS-0B", inputs=["CAS-A"])
    _write_cas(tmp_path / "CAS-B.json", cas_id="CAS-B", inputs=["CAS-0B"])
    _write_cas(tmp_path / "CAS-C.json", cas_id="CAS-C", inputs=["CAS-0C"])

    with pytest.raises(RuntimeError) as exc:
        validate_cert_dependency_integrity(tmp_path)
    assert "missing prerequisite" in str(exc.value)


def test_wrong_upstream_cas_id_fails(tmp_path: Path) -> None:
    _write_cas(tmp_path / "CAS-0A.json", cas_id="CAS-0A", inputs=[])
    _write_cas(tmp_path / "CAS-A.json", cas_id="CAS-A", inputs=["CAS-0A"])
    _write_cas(tmp_path / "CAS-0B.json", cas_id="CAS-0B", inputs=["CAS-A"])
    _write_cas(tmp_path / "CAS-B.json", cas_id="CAS-B", inputs=["CAS-0B"])
    _write_cas(tmp_path / "CAS-0C.json", cas_id="CAS-0C", inputs=["CAS-B"])
    _write_cas(tmp_path / "CAS-C.json", cas_id="CAS-C", inputs=["NOT-CAS-0C"])

    with pytest.raises(RuntimeError) as exc:
        validate_cert_dependency_integrity(tmp_path)
    assert "missing required upstream" in str(exc.value)


def test_missing_metadata_fails(tmp_path: Path) -> None:
    (tmp_path / "CAS-0A.json").write_text("{}\n", encoding="utf-8")
    _write_cas(tmp_path / "CAS-A.json", cas_id="CAS-A", inputs=["CAS-0A"])

    with pytest.raises(RuntimeError) as exc:
        validate_cert_dependency_integrity(tmp_path)
    assert "missing required metadata fields" in str(exc.value)


def test_gate_disabled_by_default() -> None:
    assert is_cert_dependency_gate_enabled() is False


def test_gate_enabled_via_env(monkeypatch: pytest.MonkeyPatch) -> None:
    assert is_cert_dependency_gate_enabled() is False
    monkeypatch.setenv("NPS_CERT_DEP_GATE", "1")
    maybe_install_cert_dependency_gate()
    assert is_cert_dependency_gate_enabled() is True
