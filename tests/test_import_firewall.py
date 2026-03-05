from __future__ import annotations

import importlib
import importlib.abc
import importlib.machinery
import os
import sys
from dataclasses import dataclass
from types import ModuleType

import pytest

from nps.audit.import_firewall import (
    install_import_firewall,
    is_firewall_enabled,
    maybe_install_import_firewall,
    uninstall_import_firewall,
)


@dataclass(frozen=True, slots=True)
class _MemMod:
    name: str
    source: str


class _MemImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, modules: dict[str, _MemMod]) -> None:
        self._modules = modules

    def find_spec(self, fullname: str, path=None, target=None):  # type: ignore[override]
        if fullname not in self._modules:
            return None
        return importlib.machinery.ModuleSpec(fullname, self)

    def create_module(self, spec):  # type: ignore[override]
        return None

    def exec_module(self, module: ModuleType) -> None:  # type: ignore[override]
        mod = self._modules[module.__name__]
        code = compile(mod.source, f"<{mod.name}>", "exec")
        exec(code, module.__dict__)


@pytest.fixture(autouse=True)
def _clean_firewall_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("NPS_IMPORT_FIREWALL", raising=False)
    uninstall_import_firewall()
    yield
    uninstall_import_firewall()


def _install_mem_importer(mods: dict[str, str]) -> _MemImporter:
    modules = {k: _MemMod(name=k, source=v) for k, v in mods.items()}
    imp = _MemImporter(modules)
    sys.meta_path.insert(0, imp)
    return imp


def _uninstall_mem_importer(imp: _MemImporter) -> None:
    try:
        sys.meta_path.remove(imp)
    except ValueError:
        pass


def _purge(mod_names: list[str]) -> None:
    for n in mod_names:
        sys.modules.pop(n, None)


def test_firewall_disabled_by_default() -> None:
    assert is_firewall_enabled() is False


def test_blocks_forward_import() -> None:
    mods = {
        "nps.phases.phase_d.target": "VALUE = 1\n",
        "nps.phases.phase_b.example": "import importlib\nimportlib.import_module('nps.phases.phase_d.target')\n",
    }
    imp = _install_mem_importer(mods)
    try:
        install_import_firewall()
        _purge(list(mods.keys()))
        with pytest.raises(ImportError) as exc:
            importlib.import_module("nps.phases.phase_b.example")
        msg = str(exc.value)
        assert "RuntimeImportFirewall" in msg
        assert "Importer:" in msg
        assert "Target:" in msg
        assert "Importer phase:" in msg
        assert "Imported phase:" in msg
        assert "Policy:" in msg
    finally:
        _purge(list(mods.keys()))
        _uninstall_mem_importer(imp)


def test_allows_backward_import() -> None:
    mods = {
        "nps.phases.phase_b.ok": "VALUE = 1\n",
        "nps.phases.phase_d.example": "import importlib\nimportlib.import_module('nps.phases.phase_b.ok')\n",
    }
    imp = _install_mem_importer(mods)
    try:
        install_import_firewall()
        _purge(list(mods.keys()))
        importlib.import_module("nps.phases.phase_d.example")
    finally:
        _purge(list(mods.keys()))
        _uninstall_mem_importer(imp)


def test_firewall_reversible() -> None:
    mods = {
        "nps.phases.phase_d.target": "VALUE = 1\n",
        "nps.phases.phase_b.example": "import importlib\nimportlib.import_module('nps.phases.phase_d.target')\n",
    }
    imp = _install_mem_importer(mods)
    try:
        install_import_firewall()
        _purge(list(mods.keys()))
        with pytest.raises(ImportError):
            importlib.import_module("nps.phases.phase_b.example")

        uninstall_import_firewall()
        assert is_firewall_enabled() is False
        _purge(list(mods.keys()))
        importlib.import_module("nps.phases.phase_b.example")
    finally:
        _purge(list(mods.keys()))
        _uninstall_mem_importer(imp)


def test_maybe_install_import_firewall_uses_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    assert is_firewall_enabled() is False

    monkeypatch.setenv("NPS_IMPORT_FIREWALL", "1")
    maybe_install_import_firewall()
    assert is_firewall_enabled() is True
