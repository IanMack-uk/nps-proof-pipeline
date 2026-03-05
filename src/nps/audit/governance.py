from __future__ import annotations

import os
from pathlib import Path

from nps.audit.cas_artefact_gate import maybe_install_cas_gate
from nps.audit.cert_dependency_gate import maybe_install_cert_dependency_gate
from nps.audit.import_firewall import maybe_install_import_firewall
from nps.audit.run_directory_integrity import validate_run_directory_integrity


def maybe_install_governance() -> None:
    """Idempotent glue to install optional governance gates.

    Gates remain disabled unless their corresponding env vars are set.
    """

    maybe_install_import_firewall()
    maybe_install_cas_gate()
    maybe_install_cert_dependency_gate()


def maybe_validate_run_dir_integrity(run_dir: Path) -> None:
    if os.getenv("NPS_RUN_DIR_INTEGRITY") == "1":
        validate_run_directory_integrity(run_dir)
