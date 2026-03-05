"""Phase 0C: CAS-0C (VERIFIED) + PROV-0C (UNVERIFIED) + Phase0C report.

Paper 0 / Paper 1 are idea documents: never trust their claims by default.
VERIFIED status must be backed by explicit upstream artefact evidence (checks/fields),
consistent with docs/phase-group-c/.../v3/phase_0C_step2_verification_rules.md.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nps.audit.governance import maybe_install_governance, maybe_validate_run_dir_integrity
from nps.audit.cert_dependency_gate import compute_content_hash
from nps.certification.artifacts import make_run_dir, write_json


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _phase_c_entry_approved(phase_c_entry_report: Path) -> bool:
    lines = phase_c_entry_report.read_text(encoding="utf-8").strip().splitlines()
    return bool(lines) and lines[-1].strip() == "Phase C Entry Gate: APPROVED"


def _has_ok_check(cas: dict[str, Any], check_id: str) -> bool:
    checks = cas.get("checks")
    if not isinstance(checks, list):
        return False
    for chk in checks:
        if not isinstance(chk, dict):
            continue
        if chk.get("check_id") == check_id:
            return chk.get("ok") is True
    return False


def build_cas0c(run_dir: Path, *, phase_c_entry_report: Path) -> tuple[Path, Path, Path]:
    # Optional hygiene gate
    integrity_note = ""
    try:
        maybe_validate_run_dir_integrity(run_dir)
    except Exception as e:
        integrity_note = str(e)

    casa_path = run_dir / "CAS-A.json"
    casb_path = run_dir / "CAS-B.json"
    if not casa_path.exists():
        raise RuntimeError("Phase0C: missing CAS-A.json in run root")
    if not casb_path.exists():
        raise RuntimeError("Phase0C: missing CAS-B.json in run root")
    if not phase_c_entry_report.exists():
        raise RuntimeError("Phase0C: missing PhaseC_ENTRY_REPORT.md")

    casa = _read_json(casa_path)
    casb = _read_json(casb_path)
    entry_ok = _phase_c_entry_approved(phase_c_entry_report)

    created_at = _utc_now()

    verified_imports: list[dict[str, Any]] = []

    # VERIFIED: convention lock (objective convention + strict-concave maximiser regime)
    eq_obj = casb.get("equilibrium_objective")
    eq_regime = casb.get("equilibrium_regime")
    casa_obj = casa.get("certified_objective")
    casb_obj = casb.get("equilibrium_certified_objective", casb.get("certified_objective"))

    if (
        isinstance(casa_obj, str)
        and isinstance(casb_obj, str)
        and casa_obj == casb_obj
        and eq_obj == "maximize"
        and eq_regime == "strict_concave"
    ):
        verified_imports.append(
            {
                "import_id": "P1.CLAIM.COUPLING_OPERATOR_CONVENTION",
                "kind": "upstream_cas_fact",
                "source_ref": f"{casa_path.name}:certified_objective + {casb_path.name}:equilibrium_*",
                "status": "VERIFIED",
                "notes": f"CAS-A/CAS-B objective convention aligned: {casa_obj}.",
            }
        )

    # VERIFIED: Hessian neg-def (supports coupling positive definite under sign convention)
    if _has_ok_check(casa, "CHK.A.NEG_DEF_HESSIAN"):
        verified_imports.append(
            {
                "import_id": "P1.CLAIM.POSITIVE_DEFINITE_COUPLING",
                "kind": "upstream_cas_fact",
                "source_ref": f"{casa_path.name}:checks[CHK.A.NEG_DEF_HESSIAN].ok",
                "status": "VERIFIED",
                "notes": "At strict maxima, H≺0 implies C=-H ≻0.",
            }
        )
        verified_imports.append(
            {
                "import_id": "P1.CLAIM.HESSIAN_SELF_ADJOINT",
                "kind": "upstream_cas_fact",
                "source_ref": f"{casa_path.name}:checks[CHK.A.NEG_DEF_HESSIAN].ok",
                "status": "VERIFIED",
                "notes": "Hessian object computed in pipeline; treated as symmetric/self-adjoint object.",
            }
        )

    # VERIFIED: stationarity (critical point)
    if _has_ok_check(casa, "CHK.A.STATIONARITY"):
        verified_imports.append(
            {
                "import_id": "P1.CLAIM.EQUILIBRIUM_HESSIAN_WELL_DEFINED",
                "kind": "upstream_cas_fact",
                "source_ref": f"{casa_path.name}:checks[CHK.A.STATIONARITY].ok",
                "status": "VERIFIED",
                "notes": "Stationarity certified; equilibrium evaluation point is well-defined.",
            }
        )

    # VERIFIED (conservative): susceptibility exists if Phase C entry approved under strict concavity
    if entry_ok and eq_obj == "maximize" and eq_regime == "strict_concave":
        verified_imports.append(
            {
                "import_id": "P1.CLAIM.SUSCEPTIBILITY_EXISTS",
                "kind": "upstream_cas_fact",
                "source_ref": f"{phase_c_entry_report.name}:APPROVED + {casb_path.name}:equilibrium_regime",
                "status": "VERIFIED",
                "notes": "Allowed as an existence precondition for response identities (bounds remain Phase C work).",
            }
        )

    # VERIFIED tool imports (non-spectral-first baseline)
    verified_imports.extend(
        [
            {
                "import_id": "TOOL.NEUMANN_SERIES_INVERSION",
                "kind": "finite_dim_tool",
                "source_ref": "finite_dim_tool",
                "status": "VERIFIED",
                "notes": "Norm-based inverse control (non-spectral-first).",
            },
            {
                "import_id": "TOOL.BLOCK_NORM_INVERSION_BOUND",
                "kind": "finite_dim_tool",
                "source_ref": "finite_dim_tool",
                "status": "VERIFIED",
                "notes": "Blockwise bounds for inverse structure.",
            },
        ]
    )

    # UNVERIFIED candidates (must go to PROV-0C)
    unverified_candidates: list[dict[str, Any]] = [
        {
            "candidate_id": "P0.CLAIM.STRUCTURAL_LOCALITY_AXIOM",
            "description": "Locality induces Hessian sparsity outside neighbourhoods.",
            "status": "UNVERIFIED",
            "why_unverified": "No explicit upstream artefact evidence recorded yet.",
            "proposed_test_plan": "Phase C: add explicit sparsity/locality checks and write structured artefacts.",
            "priority": "high",
            "blocking_for_phase_c": False,
        },
        {
            "candidate_id": "P1.CLAIM.INVERSE_NORM_BOUND",
            "description": "||C^{-1}|| ≤ 1/lambda_min(C) (spectral).",
            "status": "UNVERIFIED",
            "why_unverified": "Spectral escalation not enabled in CAS-0C by default.",
            "proposed_test_plan": "Phase C: either certify non-spectral bound or explicitly escalate spectral facts.",
            "priority": "medium",
            "blocking_for_phase_c": False,
        },
        {
            "candidate_id": "TOOL.DIAGONAL_DOMINANCE_MARGIN",
            "description": "Diagonal-dominance margin conditions for inverse control.",
            "status": "UNVERIFIED",
            "why_unverified": "Not chosen as a required tool for this run's baseline.",
            "proposed_test_plan": "Phase C: include only if needed; otherwise treat as diagnostic.",
            "priority": "low",
            "blocking_for_phase_c": False,
        },
    ]

    cas0c_payload: dict[str, Any] = {
        "phase": "0C",
        "run_id": run_dir.name,
        "generated_at_utc": created_at,
        "inputs": {
            "phase_c_entry_report": str(phase_c_entry_report.relative_to(run_dir.parent)),
            "cas_chain": [
                str((run_dir / "CAS-0A.json").relative_to(run_dir.parent)),
                str((run_dir / "CAS-A.json").relative_to(run_dir.parent)),
                str((run_dir / "CAS-Ap.json").relative_to(run_dir.parent)),
                str((run_dir / "CAS-0B.json").relative_to(run_dir.parent)),
                str((run_dir / "CAS-B.json").relative_to(run_dir.parent)),
                str((run_dir / "CAS-Bp.json").relative_to(run_dir.parent)),
            ],
        },
        "spectral_escalation": False,
        "verified_imports": verified_imports,
        "status": "APPROVED" if entry_ok else "BLOCKED",
        "notes": {"run_dir_integrity_note": integrity_note},
    }
    cas0c_payload["content_hash"] = compute_content_hash(cas0c_payload)

    prov0c_payload: dict[str, Any] = {
        "phase": "0C",
        "run_id": run_dir.name,
        "generated_at_utc": created_at,
        "unverified_candidates": unverified_candidates,
    }
    prov0c_payload["content_hash"] = compute_content_hash(prov0c_payload)

    out_cas0c = run_dir / "CAS-0C.json"
    out_prov0c = run_dir / "PROV-0C.json"
    out_report = run_dir / "Phase0C_REPORT.md"

    write_json(out_cas0c, cas0c_payload)
    write_json(out_prov0c, prov0c_payload)

    out_report.write_text(
        "\n".join(
            [
                "# Phase 0C Report",
                "",
                f"- Run ID: {run_dir.name}",
                f"- Generated at (UTC): {created_at}",
                "",
                "## Phase C Entry Gate Status",
                f"- Approved line present: {entry_ok}",
                f"- Reference: {phase_c_entry_report.name}",
                "",
                "## CAS-0C Summary",
                f"- status: {cas0c_payload['status']}",
                f"- spectral_escalation: {cas0c_payload['spectral_escalation']}",
                f"- verified_imports: {len(verified_imports)}",
                "",
                "## PROV-0C Summary",
                f"- unverified_candidates: {len(unverified_candidates)}",
                "",
                "## Notes",
                f"- run_dir_integrity_note: {integrity_note or 'none'}",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    return out_cas0c, out_prov0c, out_report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build CAS-0C / PROV-0C (Phase 0C Step 2) into cert_artifacts//"
    )
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--run-root", default=None)
    parser.add_argument("--phase-c-entry-report", required=True)
    args = parser.parse_args()

    maybe_install_governance()

    if args.run_root:
        run_dir = Path(args.run_root)
        run_dir.mkdir(parents=True, exist_ok=True)
    else:
        run_dir = make_run_dir(args.run_id)

    out_cas0c, out_prov0c, out_report = build_cas0c(
        run_dir, phase_c_entry_report=Path(args.phase_c_entry_report)
    )
    print(str(out_cas0c))
    print(str(out_prov0c))
    print(str(out_report))


if __name__ == "__main__":
    main()
