from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path


_ENV_FLAG = "NPS_CERT_DEP_GATE"


@dataclass(frozen=True, slots=True)
class CasMeta:
    cas_id: str
    created_at: str
    inputs: list[str]
    content_hash: str


_gate_enabled = False


def is_cert_dependency_gate_enabled() -> bool:
    return _gate_enabled


def install_cert_dependency_gate() -> None:
    global _gate_enabled
    _gate_enabled = True


def uninstall_cert_dependency_gate() -> None:
    global _gate_enabled
    _gate_enabled = False


def maybe_install_cert_dependency_gate() -> None:
    if os.environ.get(_ENV_FLAG) == "1":
        install_cert_dependency_gate()


def validate_cert_dependency_integrity(
    artefact_dir: str | Path,
    *,
    policy_path: str | Path = "docs/specs/import_policy.json",
) -> None:
    """Validate CAS chain ordering + minimal cross-artefact consistency.

    The `policy_path` parameter exists to match the required API, but this gate
    validates CAS artefact integrity and does not currently use the import policy.

    Raises RuntimeError with audit-grade messages.
    """

    _ = policy_path

    d = Path(artefact_dir)
    if not d.exists() or not d.is_dir():
        raise RuntimeError(
            "CertDependencyGate: artefact_dir is not a directory\n"
            f"Artefact dir: {d}"
        )

    chain = [
        "CAS-0A",
        "CAS-A",
        "CAS-0B",
        "CAS-B",
        "CAS-0C",
        "CAS-C",
        "CAS-0D",
        "CAS-D",
    ]

    prereq: dict[str, str] = {
        "CAS-A": "CAS-0A",
        "CAS-0B": "CAS-A",
        "CAS-B": "CAS-0B",
        "CAS-0C": "CAS-B",
        "CAS-C": "CAS-0C",
        "CAS-0D": "CAS-C",
        "CAS-D": "CAS-0D",
    }

    present: dict[str, Path] = {}
    for cas in chain:
        p = _find_cas_file(d, cas)
        if p is not None:
            present[cas] = p

    # Ordering constraints: if downstream exists, prereq must exist.
    for cas, pth in present.items():
        need = prereq.get(cas)
        if need is None:
            continue
        if need not in present:
            raise RuntimeError(
                "CertDependencyGate: missing prerequisite CAS artefact\n"
                f"Artefact dir: {d}\n"
                f"CAS present: {cas} ({pth.name})\n"
                f"Missing prerequisite: {need}"
            )

    # Minimal metadata and cross-artefact cas_id consistency.
    metas: dict[str, CasMeta] = {}
    for cas, pth in present.items():
        payload = _load_json(pth)
        meta = _extract_meta(payload, cas_label=cas, path=pth)
        metas[cas] = meta

        computed = compute_content_hash(payload)
        if meta.content_hash != computed:
            raise RuntimeError(
                "CertDependencyGate: content_hash mismatch\n"
                f"Artefact: {cas} ({pth.name})\n"
                f"Declared: {meta.content_hash}\n"
                f"Computed: {computed}\n"
                "Suggested fix: regenerate CAS artefacts with correct hashing."
            )

    # inputs must match upstream cas_id
    for cas, need in prereq.items():
        if cas not in metas:
            continue
        if need not in metas:
            continue
        downstream = metas[cas]
        upstream = metas[need]

        if upstream.cas_id not in downstream.inputs:
            raise RuntimeError(
                "CertDependencyGate: downstream CAS missing required upstream cas_id\n"
                f"Downstream: {cas} cas_id={downstream.cas_id}\n"
                f"Upstream: {need} cas_id={upstream.cas_id}\n"
                f"Downstream inputs: {downstream.inputs}"
            )


def compute_content_hash(payload: dict) -> str:
    """Compute stable content hash for a CAS artefact.

    Uses JSON canonicalization (sorted keys) and excludes volatile metadata fields.
    """

    if not isinstance(payload, dict):
        raise ValueError("CAS payload must be a JSON object")

    stripped = dict(payload)
    # exclude metadata fields
    for k in ("cas_id", "created_at", "inputs", "content_hash"):
        stripped.pop(k, None)

    canonical = json.dumps(stripped, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _find_cas_file(dir_path: Path, cas_label: str) -> Path | None:
    # tolerant match: hyphen/underscore variants and optional lowercase.
    candidates = {
        f"{cas_label}.json",
        f"{cas_label.replace('-', '_')}.json",
        f"{cas_label.lower()}.json",
        f"{cas_label.replace('-', '_').lower()}.json",
    }
    for name in candidates:
        p = dir_path / name
        if p.exists():
            return p
    return None


def _load_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(
            "CertDependencyGate: failed to parse CAS artefact JSON\n"
            f"Path: {path}\n"
            f"Error: {exc}"
        ) from exc

    if not isinstance(payload, dict):
        raise RuntimeError(
            "CertDependencyGate: CAS artefact is not a JSON object\n" f"Path: {path}"
        )

    return payload


def _extract_meta(payload: dict, *, cas_label: str, path: Path) -> CasMeta:
    required = ("cas_id", "created_at", "inputs", "content_hash")
    missing = [k for k in required if k not in payload]
    if missing:
        raise RuntimeError(
            "CertDependencyGate: missing required metadata fields\n"
            f"Artefact: {cas_label} ({path.name})\n"
            f"Missing: {missing}\n"
            "Suggested fix: regenerate artefacts with required metadata."
        )

    cas_id = payload.get("cas_id")
    created_at = payload.get("created_at")
    inputs = payload.get("inputs")
    content_hash = payload.get("content_hash")

    if not isinstance(cas_id, str) or not cas_id:
        raise RuntimeError(
            "CertDependencyGate: invalid cas_id\n" f"Artefact: {cas_label} ({path.name})"
        )
    if not isinstance(created_at, str) or not created_at:
        raise RuntimeError(
            "CertDependencyGate: invalid created_at\n" f"Artefact: {cas_label} ({path.name})"
        )
    if not isinstance(inputs, list) or not all(isinstance(x, str) for x in inputs):
        raise RuntimeError(
            "CertDependencyGate: invalid inputs\n" f"Artefact: {cas_label} ({path.name})"
        )
    if not isinstance(content_hash, str) or not content_hash:
        raise RuntimeError(
            "CertDependencyGate: invalid content_hash\n" f"Artefact: {cas_label} ({path.name})"
        )

    return CasMeta(cas_id=cas_id, created_at=created_at, inputs=list(inputs), content_hash=content_hash)
