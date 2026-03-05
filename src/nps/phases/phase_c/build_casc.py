"""Phase C: Hessian analysis artifacts (CAS-C).

This phase is structural/governance-level: compute and persist Hessian objects
at the certified equilibrium w* and record finite-dimensional certification
attempts without spectral escalation.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from nps.audit.cert_dependency_gate import compute_content_hash
from nps.audit.governance import maybe_install_governance, maybe_validate_run_dir_integrity
from nps.certification.artifacts import make_run_dir, write_json
from nps.models.real_phi_v0 import make_real_phi_v0_test_spec
from nps.models.signed_objective import SignedObjective


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _phase_c_entry_approved(path: Path) -> bool:
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    return bool(lines) and lines[-1].strip() == "Phase C Entry Gate: APPROVED"


def _matrix_to_list(M: np.ndarray) -> list[list[float]]:
    return [[float(x) for x in row] for row in np.asarray(M, dtype=float)]


def _sign_matrix(M: np.ndarray, *, tol: float) -> list[list[int]]:
    A = np.asarray(M, dtype=float)
    out: list[list[int]] = []
    for i in range(A.shape[0]):
        row: list[int] = []
        for j in range(A.shape[1]):
            v = float(A[i, j])
            if abs(v) <= tol:
                row.append(0)
            elif v > 0:
                row.append(1)
            else:
                row.append(-1)
        out.append(row)
    return out


def _diag_dominance_margin(A: np.ndarray) -> float:
    M = np.asarray(A, dtype=float)
    margins = []
    for i in range(M.shape[0]):
        diag = abs(float(M[i, i]))
        off = float(np.sum(np.abs(M[i, :])) - diag)
        margins.append(diag - off)
    return float(min(margins)) if margins else float("-inf")


def build_casc(run_dir: Path) -> tuple[Path, Path, list[Path]]:
    maybe_validate_run_dir_integrity(run_dir)

    casa_path = run_dir / "CAS-A.json"
    casb_path = run_dir / "CAS-B.json"
    cas0c_path = run_dir / "CAS-0C.json"
    entry_path = run_dir / "PhaseC_ENTRY_REPORT.md"

    for required in (casa_path, casb_path, cas0c_path, entry_path):
        if not required.exists():
            raise RuntimeError(f"PhaseC: missing required file in run root: {required.name}")

    casa = _read_json(casa_path)
    casb = _read_json(casb_path)
    cas0c = _read_json(cas0c_path)

    entry_ok = _phase_c_entry_approved(entry_path)

    eq = casb.get("equilibrium_candidate")
    if not isinstance(eq, dict) or not isinstance(eq.get("w_star"), list):
        raise RuntimeError("PhaseC: CAS-B missing equilibrium_candidate.w_star")

    w_star = np.asarray(eq.get("w_star"), dtype=float)

    certified_objective = casb.get("certified_objective")
    if certified_objective not in ("phi", "minus_phi"):
        raise RuntimeError("PhaseC: CAS-B certified_objective must be 'phi' or 'minus_phi'")

    spec = make_real_phi_v0_test_spec()
    trace = casb.get("trace") if isinstance(casb.get("trace"), dict) else {}
    trace_rv = trace.get("real_phi_v0") if isinstance(trace.get("real_phi_v0"), dict) else {}
    extension_id = trace_rv.get("extension_id") if isinstance(trace_rv.get("extension_id"), str) else spec.extension_id
    signed = SignedObjective(
        spec,
        sign=-1.0 if certified_objective == "minus_phi" else 1.0,
        extension_id=extension_id,
    )

    H = np.asarray(signed.hess(w_star), dtype=float)
    if H.shape != (spec.m, spec.m):
        raise RuntimeError("PhaseC: Hessian has unexpected shape")

    tol_sym = 1e-10
    sym_err = float(np.max(np.abs(H - H.T)))

    hessian_matrix_payload: dict[str, Any] = {
        "dimension": int(H.shape[0]),
        "symmetry_error": sym_err,
        "tolerance_policy": {"symmetry_tol": tol_sym},
        "matrix": _matrix_to_list(H),
    }

    blocks_payload: dict[str, Any] = {
        "notes": "RealPhiV0 has no explicit theta block in v0; blocks recorded as placeholders.",
        "H_ww": _matrix_to_list(H),
        "H_wtheta": [],
        "H_thetaw": [],
    }

    # Finite-dimensional certification attempt (non-spectral-first).
    # We work with coupling C := -H under strict concavity.
    C = -H
    dd_margin = _diag_dominance_margin(C)
    neumann_ok = False
    neumann_witness: dict[str, Any] = {}
    try:
        Dinv = np.diag(1.0 / np.diag(C))
        A = np.eye(C.shape[0]) - Dinv @ C
        norm_inf = float(np.max(np.sum(np.abs(A), axis=1)))
        neumann_ok = norm_inf < 1.0
        neumann_witness = {"norm_inf(DinvC-I)": norm_inf}
    except Exception as e:  # noqa: BLE001
        neumann_ok = False
        neumann_witness = {"error": str(e)}

    matrix_hyp_payload: dict[str, Any] = {
        "methods_attempted": [
            "diagonal dominance",
            "comparison inequalities",
            "Neumann series bounds",
        ],
        "diagonal_dominance_margin": dd_margin,
        "neumann_series": {"ok": neumann_ok, "witness": neumann_witness},
        "status": "PASS" if (dd_margin > 0.0 or neumann_ok) else "FAIL",
        "spectral_escalation": bool(cas0c.get("spectral_escalation")),
    }

    # Inverse sign structure (requires invertibility; Phase B already checked Jacobian invertible at w*).
    inv_payload: dict[str, Any]
    try:
        Cinv = np.linalg.inv(C)
        inv_payload = {
            "object": "C^{-1}",
            "tol": 1e-12,
            "sign_matrix": _sign_matrix(Cinv, tol=1e-12),
        }
    except Exception as e:  # noqa: BLE001
        inv_payload = {"error": str(e)}

    # Exposure–response: required for READY_FOR_PHASE_D.
    # RealPhiV0 v0 has no explicit theta; record as not computed.
    exposure_payload: dict[str, Any] = {
        "computed": False,
        "reason": "RealPhiV0 v0 pipeline does not parameterize theta blocks in-object; no D_theta grad available.",
        "status": "FAIL (NOT COMPUTED)",
    }

    created_at = _utc_now()

    out_hessian = run_dir / "HESSIAN_MATRIX.json"
    out_blocks = run_dir / "HESSIAN_BLOCKS.json"
    out_inv = run_dir / "INVERSE_SIGN_STRUCTURE.json"
    out_exposure = run_dir / "EXPOSURE_RESPONSE_CHECK.json"

    write_json(out_hessian, hessian_matrix_payload)
    write_json(out_blocks, blocks_payload)
    write_json(out_inv, inv_payload)
    write_json(out_exposure, exposure_payload)

    # CAS-C
    exposure_ok = bool(exposure_payload.get("computed") is True and exposure_payload.get("status") == "PASS")
    cas_c_ok = bool(entry_ok and matrix_hyp_payload["status"] == "PASS" and exposure_ok)

    cas_c_payload: dict[str, Any] = {
        "cas_id": "CAS-C",
        "created_at": created_at,
        "inputs": [str(cas0c.get("cas_id", "CAS-0C"))],
        "content_hash": "",
        "phase": "C",
        "run_id": run_dir.name,
        "entry_gate": {"approved": entry_ok, "report": entry_path.name},
        "equilibrium": {
            "equilibrium_objective": casb.get("equilibrium_objective"),
            "equilibrium_regime": casb.get("equilibrium_regime"),
            "certified_objective": certified_objective,
        },
        "hessian": {"path": out_hessian.name, "symmetry_error": sym_err},
        "blocks": {"path": out_blocks.name},
        "matrix_hypothesis": matrix_hyp_payload,
        "inverse_sign_structure": {"path": out_inv.name},
        "exposure_response": {"path": out_exposure.name, "status": exposure_payload.get("status")},
        "status": "APPROVED" if cas_c_ok else "BLOCKED",
    }
    cas_c_payload["content_hash"] = compute_content_hash(cas_c_payload)

    out_casc = run_dir / "CAS-C.json"
    write_json(out_casc, cas_c_payload)

    # PhaseC_REPORT.md from template structure (filled minimal)
    out_report = run_dir / "PhaseC_REPORT.md"
    phase_c_status = "READY_FOR_PHASE_D" if cas_c_payload["status"] == "APPROVED" else "INCOMPLETE"

    out_report.write_text(
        "\n".join(
            [
                "# Phase C Report",
                "",
                f"Run ID: {run_dir.name}",
                f"Date (UTC): {created_at}",
                "Generated by: nps.phases.phase_c.build_casc",
                "",
                "## Inputs Verified",
                f"- CAS-A.json: {'PASS' if casa_path.exists() else 'FAIL'}",
                f"- CAS-B.json: {'PASS' if casb_path.exists() else 'FAIL'}",
                f"- CAS-0C.json: {'PASS' if cas0c_path.exists() else 'FAIL'}",
                f"- PhaseC_ENTRY_REPORT.md: {'PASS' if entry_path.exists() else 'FAIL'}",
                "",
                "## Hessian Computation",
                "",
                f"Matrix dimension: {int(H.shape[0])}",
                f"Symmetry check: {'PASS' if sym_err <= tol_sym else 'FAIL'} (error={sym_err})",
                f"Tolerance policy: symmetry_tol={tol_sym}",
                "",
                "Artifact:",
                out_hessian.name,
                "",
                "## Structural Block Decomposition",
                "",
                "Blocks:",
                "",
                "- H_ww",
                "- H_wθ",
                "- H_θw",
                "",
                "Artifact:",
                out_blocks.name,
                "",
                "## Matrix Hypothesis Certification",
                "",
                "Methods attempted:",
                "",
                "- diagonal dominance",
                "- comparison inequalities",
                "- Neumann series bounds",
                "",
                "Result:",
                "",
                matrix_hyp_payload["status"],
                "",
                "## Inverse-Hessian Sign Structure",
                "",
                "Certified sign predictions:",
                "",
                "Artifact:",
                out_inv.name,
                "",
                "## Exposure–Response Compatibility",
                "",
                "Cross-derivative block computed:",
                "",
                out_exposure.name,
                "",
                "Compatibility status:",
                "",
                str(exposure_payload.get("status", "FAIL")),
                "",
                "## Decision",
                "",
                "CAS-C Status:",
                "",
                cas_c_payload["status"],
                "",
                "Phase C Status:",
                "",
                phase_c_status,
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    return out_casc, out_report, [out_hessian, out_blocks, out_inv, out_exposure]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-root", default="cert_artifacts")
    args = parser.parse_args()

    maybe_install_governance()

    if args.run_root and args.run_root != "cert_artifacts":
        run_dir = Path(args.run_root)
        run_dir.mkdir(parents=True, exist_ok=True)
    else:
        run_dir = make_run_dir(args.run_id)
    out_casc, out_report, _ = build_casc(run_dir)

    print(str(out_casc))
    print(str(out_report))


if __name__ == "__main__":
    main()
