from __future__ import annotations

from pathlib import Path

CANONICAL_CAS = {
    "CAS-0A.json",
    "CAS-A.json",
    "CAS-Ap.json",
    "CAS-0B.json",
    "CAS-B.json",
    "CAS-Bp.json",
    "CAS-0C.json",
    "CAS-C.json",
}


def validate_run_directory_integrity(run_dir: Path) -> None:
    """Raise RuntimeError if run root contains ambiguous CAS artefact variants."""

    if not run_dir.exists() or not run_dir.is_dir():
        raise RuntimeError(f"validate_run_directory_integrity: run_dir does not exist: {run_dir}")

    cas_like = sorted(p.name for p in run_dir.iterdir() if p.is_file() and p.name.startswith("CAS-") and p.name.endswith(".json"))

    offenders = [n for n in cas_like if n not in CANONICAL_CAS]
    if offenders:
        raise RuntimeError(
            "Run directory contains non-canonical CAS artefact variants in root: "
            + ", ".join(offenders)
            + ". Move variants to experiments/"
        )

    # Also fail on common "duplicate" patterns that can confuse consumers.
    duplicates = [n for n in cas_like if "(" in n or ")" in n]
    if duplicates:
        raise RuntimeError(
            "Run directory contains suspicious duplicate-named canonical files in root: "
            + ", ".join(duplicates)
        )
