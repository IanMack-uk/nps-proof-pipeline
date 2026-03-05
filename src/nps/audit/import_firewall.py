from __future__ import annotations

import importlib.machinery
import importlib.util
import inspect
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Optional

_ENV_FLAG = "NPS_IMPORT_FIREWALL"


@dataclass(frozen=True, slots=True)
class _FirewallConfig:
    policy_name: str
    rank: dict[str, int]


class _RuntimeImportFirewall(importlib.machinery.PathFinder):
    def __init__(self, config: _FirewallConfig) -> None:
        self._config = config

    def find_spec(self, fullname: str, path: object | None = None, target: ModuleType | None = None):  # type: ignore[override]
        importer = _detect_importer_module_name()
        if importer:
            self._maybe_block(importer_module=importer, target_module=fullname)

        # Delegate resolution to the remaining meta_path finders so that we do not
        # bypass custom loaders.
        removed = False
        try:
            try:
                sys.meta_path.remove(self)
                removed = True
            except ValueError:
                removed = False
            return importlib.util.find_spec(fullname)
        finally:
            if removed:
                sys.meta_path.insert(0, self)

    def _maybe_block(self, *, importer_module: str, target_module: str) -> None:
        importer_phase = get_phase_id(importer_module)
        target_phase = get_phase_id(target_module)

        if importer_phase is None or target_phase is None:
            return

        if not is_forward_phase_import(importer_phase, target_phase, self._config.rank):
            return

        msg = (
            "RuntimeImportFirewall: forward phase import blocked\n"
            f"Importer: {importer_module}\n"
            f"Target: {target_module}\n"
            f"Importer phase: {importer_phase}\n"
            f"Imported phase: {target_phase}\n"
            f"Policy: {self._config.policy_name}\n\n"
            "Suggested fix:\n"
            "Move shared logic to a lower layer (core/models) or invert dependency."
        )
        raise ImportError(msg)


_firewall: _RuntimeImportFirewall | None = None


def load_import_policy(path: str | Path) -> dict:
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))


def get_phase_id(module_name: str) -> str | None:
    # `nps.phases.phase_<id>.*` -> `phase_<id>`
    parts = module_name.split(".")
    if len(parts) >= 3 and parts[0] == "nps" and parts[1] == "phases":
        ph = parts[2]
        if ph.startswith("phase_"):
            return ph
    return None


def is_forward_phase_import(importer_phase: str, imported_phase: str, rank: dict[str, int]) -> bool:
    if importer_phase not in rank or imported_phase not in rank:
        return False
    return rank[imported_phase] > rank[importer_phase]


def is_firewall_enabled() -> bool:
    return _firewall is not None


def install_import_firewall(policy_path: str | Path = "docs/specs/import_policy.json") -> None:
    global _firewall

    if _firewall is not None:
        return

    policy = load_import_policy(policy_path)

    phase_order = tuple(policy.get("phase_order", []))
    rank = {p: i for i, p in enumerate(phase_order)}

    config = _FirewallConfig(
        policy_name=str(policy.get("policy", "(unknown)")),
        rank=rank,
    )

    _firewall = _RuntimeImportFirewall(config)
    sys.meta_path.insert(0, _firewall)


def uninstall_import_firewall() -> None:
    global _firewall
    if _firewall is None:
        return

    try:
        sys.meta_path.remove(_firewall)
    except ValueError:
        pass
    _firewall = None


def maybe_install_import_firewall() -> None:
    if os.environ.get(_ENV_FLAG) == "1":
        install_import_firewall()


def _detect_importer_module_name() -> Optional[str]:
    # Walk up the stack and find the first frame that looks like user/module code.
    # This is best-effort; if we cannot find an importer, we skip enforcement.
    for frame_info in inspect.stack()[2:]:
        frame = frame_info.frame
        name = frame.f_globals.get("__name__")
        if not isinstance(name, str) or not name:
            continue
        if name.startswith("importlib"):
            continue
        if name == __name__:
            continue
        return name
    return None
