"""Phase C: Hessian analysis artifacts (CAS-C).

This phase is structural/governance-level: compute and persist Hessian objects
at the certified equilibrium w* and record finite-dimensional certification
attempts without spectral escalation.
"""

from __future__ import annotations

import argparse
import hashlib
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


def _extract_certified_objective(cas: dict[str, Any]) -> str | None:
    """Best-effort extraction of certified objective convention.

    This is schema-tolerant by design because upstream artefact schemas may evolve.
    """

    derivative_def = cas.get("derivative_definition")
    if isinstance(derivative_def, dict):
        v0 = derivative_def.get("certified_objective")
        if isinstance(v0, str):
            return v0
        if isinstance(v0, dict) and isinstance(v0.get("id"), str):
            return v0.get("id")

    v = cas.get("certified_objective")
    if isinstance(v, str):
        return v
    if isinstance(v, dict) and isinstance(v.get("id"), str):
        return v.get("id")

    obj = cas.get("objective")
    if isinstance(obj, dict):
        v2 = obj.get("certified_objective")
        if isinstance(v2, str):
            return v2
        if isinstance(v2, dict) and isinstance(v2.get("id"), str):
            return v2.get("id")

    return None


def _operator_layer_all_required_pass(checks: list[dict[str, Any]]) -> bool:
    """Task 1 PASS semantics: any explicit FAIL blocks; SKIP does not."""

    for chk in checks:
        ok = chk.get("ok")
        if ok is False:
            return False
    return True


def _task3_all_required_pass(checks: list[dict[str, Any]]) -> bool:
    for chk in checks:
        if chk.get("ok") is not True:
            return False
    return True


def _task2_all_required_pass(checks: list[dict[str, Any]]) -> bool:
    for chk in checks:
        if chk.get("ok") is not True:
            return False
    return True


def _mk_check(*, id: str, ok: bool, details: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": id,
        "ok": bool(ok),
        "status": "PASS" if ok else "FAIL",
        "details": details,
    }


def _task4_all_required_pass(checks: list[dict[str, Any]]) -> bool:
    for chk in checks:
        if chk.get("ok") is not True:
            return False
    return True


def _task5_all_required_pass(checks: list[dict[str, Any]]) -> bool:
    for chk in checks:
        if chk.get("ok") is not True:
            return False
    return True


def _task9_all_required_pass(checks: list[dict[str, Any]]) -> bool:
    for chk in checks:
        if chk.get("ok") is not True:
            return False
    return True


def _task10_all_required_pass(checks: list[dict[str, Any]]) -> bool:
    for chk in checks:
        if chk.get("ok") is not True:
            return False
    return True


def _task6_all_required_pass(checks: list[dict[str, Any]]) -> bool:
    for chk in checks:
        if chk.get("ok") is not True:
            return False
    return True


def _task7_all_required_pass(checks: list[dict[str, Any]]) -> bool:
    for chk in checks:
        if chk.get("ok") is not True:
            return False
    return True


def _task8_all_required_pass(checks: list[dict[str, Any]]) -> bool:
    for chk in checks:
        if chk.get("ok") is not True:
            return False
    return True


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

    created_at = _utc_now()

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

    # === TASKPACK 1: OPERATOR LAYER ===
    # ---------------------------------------------------------------------
    # Taskpack 1 (Operator Layer): emit OPERATOR_LAYER.json + report.
    # This is an additional artefact-only step; it must not modify Phase C
    # gating semantics.
    # ---------------------------------------------------------------------
    casa_cert_obj = _extract_certified_objective(casa)

    operator_layer_checks: list[dict[str, Any]] = []

    operator_layer_checks.append(
        {
            "check_id": "CHK.C1.ENTRY_GATE_APPROVED",
            "ok": bool(entry_ok),
            "details": "PhaseC_ENTRY_REPORT.md last line must be 'Phase C Entry Gate: APPROVED'.",
        }
    )
    operator_layer_checks.append(
        {
            "check_id": "CHK.C1.CONVENTION.CERTIFIED_OBJECTIVE_PRESENT",
            "ok": casa_cert_obj in ("phi", "minus_phi"),
            "details": "CAS-A must declare certified objective convention as 'phi' or 'minus_phi'.",
        }
    )
    operator_layer_checks.append(
        {
            "check_id": "CHK.C1.CONVENTION.CERTIFIED_OBJECTIVE_MATCHES_CASB",
            "ok": bool(casa_cert_obj in ("phi", "minus_phi") and casa_cert_obj == certified_objective),
            "details": f"CAS-A certified_objective={casa_cert_obj!r}, CAS-B certified_objective={certified_objective!r}.",
        }
    )
    operator_layer_checks.append(
        {
            "check_id": "CHK.C1.EQUILIBRIUM_POINT.W_STAR_PRESENT",
            "ok": bool(w_star.shape == (spec.m,)),
            "details": f"w_star dim={int(w_star.shape[0])} expected={int(spec.m)}.",
        }
    )

    # Task 1 is the operator layer. Hessian checks are *informational* here and should
    # not make Task 1 brittle if H is not yet available.
    h_available = isinstance(H, np.ndarray) and H.ndim == 2 and H.shape[0] == H.shape[1]
    if h_available:
        operator_layer_checks.append(
            {
                "check_id": "CHK.C1.HESSIAN.SHAPE_MATCHES_DIM_W",
                "ok": bool(H.shape == (w_star.shape[0], w_star.shape[0])),
                "details": f"H shape={tuple(int(x) for x in H.shape)}.",
            }
        )
        operator_layer_checks.append(
            {
                "check_id": "CHK.C1.HESSIAN.SYMMETRIC",
                "ok": bool(sym_err <= tol_sym),
                "details": f"symmetry_error={sym_err} tol={tol_sym}.",
            }
        )
    else:
        operator_layer_checks.append(
            {
                "check_id": "CHK.C1.HESSIAN.SHAPE_MATCHES_DIM_W",
                "ok": None,
                "details": "SKIP (NOT AVAILABLE): Hessian not available at Task 1 time.",
            }
        )
        operator_layer_checks.append(
            {
                "check_id": "CHK.C1.HESSIAN.SYMMETRIC",
                "ok": None,
                "details": "SKIP (NOT AVAILABLE): Hessian not available at Task 1 time.",
            }
        )
    operator_layer_checks.append(
        {
            "check_id": "CHK.C1.SIGN_CONVENTION.COUPLING_MATRIX_DEFINED",
            "ok": True,
            "details": "Operator layer records H := ∇²_w Φ_cert and coupling matrix convention C := -H.",
        }
    )
    operator_layer_checks.append(
        {
            "check_id": "CHK.C1.DEPENDENCY_WHITELIST.COMPLETE",
            "ok": isinstance(cas0c.get("verified_imports"), list),
            "details": "CAS-0C should provide verified_imports for Phase C tool whitelist posture.",
        }
    )

    operator_layer_ok = _operator_layer_all_required_pass(operator_layer_checks)

    operator_layer_payload: dict[str, Any] = {
        "schema_version": "C-OPERATOR-LAYER.v1",
        "run_id": run_dir.name,
        "generated_utc": created_at,
        "scope": "pointwise_at_w_star",
        "sources": {
            "cas_a": str(casa_path),
            "cas_b": str(casb_path),
            "cas_0c": str(cas0c_path),
            "phase_c_entry_report": str(entry_path),
        },
        "objective_convention": {
            "certified_objective": certified_objective,
            "equilibrium_objective": casb.get("equilibrium_objective"),
            "equilibrium_regime": casb.get("equilibrium_regime"),
            "notes": "H := ∇²_w Φ_cert. For strict concave maximize, coupling matrix C := -H is the positive-stability object.",
        },
        "operator": {
            "F_definition": "F(w,θ) := ∇_w Φ_cert(w,θ)",
            "derivative_map": {
                "D_w F": "H_ww",
                "D_θ F": "H_wθ",
            },
            "H_definition": "H(w,θ) := ∇²_w Φ_cert(w,θ)",
            "C_definition": "C := -H",
        },
        "equilibrium": {
            "w_star_ref": "CAS-B.equilibrium_candidate.w_star",
            "dim_w": int(w_star.shape[0]),
        },
        "structural_basis": {
            "basis_id": "REAL_PHI_V0_SPEC_EDGE_ORDER",
            "ordering_rule": "Implicit ordering used by RealPhiV0Spec / SignedObjective implementation (edge order internal to spec).",
            "permutation_P": [],
        },
        "hessian": {
            "dim": int(H.shape[0]),
            "symmetry_error": sym_err,
            "tolerance_policy": {"symmetry_tol": tol_sym},
        },
        "checks": operator_layer_checks,
        "status": "PASS" if operator_layer_ok else "FAIL",
    }

    out_operator_layer = run_dir / "OPERATOR_LAYER.json"
    write_json(out_operator_layer, operator_layer_payload)

    out_operator_report = run_dir / "PhaseC_TASK1_OPERATOR_LAYER_REPORT.md"
    out_operator_report.write_text(
        "\n".join(
            [
                "# Phase C Task 1 Report — Operator Layer",
                "",
                f"Run ID: {run_dir.name}",
                f"Date (UTC): {created_at}",
                "Generated by: nps.phases.phase_c.build_casc (Taskpack 1 step)",
                "",
                "## Operator definition (certified)",
                "",
                "- F(w,θ) = ∇_w Φ_cert(w,θ)",
                "- D_w F = H_ww",
                "- D_θ F = H_wθ",
                "",
                "## Sign conventions",
                "",
                f"- certified_objective: `{certified_objective}`",
                f"- equilibrium_objective (CAS-B): `{casb.get('equilibrium_objective')}`",
                f"- equilibrium_regime (CAS-B): `{casb.get('equilibrium_regime')}`",
                "- Hessian convention: H = ∇²_w Φ_cert",
                "- Coupling convention (if used): C = −H",
                "",
                "## Structural basis",
                "",
                "- basis_id: `REAL_PHI_V0_SPEC_EDGE_ORDER`",
                "- ordering: implicit RealPhiV0Spec edge ordering",
                "",
                "## Scope",
                "",
                "- scope: `pointwise_at_w_star`",
                "",
                "## Verification checks",
                "",
                *[
                    (
                        f"- {chk['check_id']}: PASS"
                        if chk.get("ok") is True
                        else (
                            f"- {chk['check_id']}: FAIL"
                            if chk.get("ok") is False
                            else f"- {chk['check_id']}: SKIP"
                        )
                    )
                    for chk in operator_layer_checks
                ],
                "",
                "## Decision",
                "",
                f"Task 1 status: {'PASS' if operator_layer_ok else 'FAIL'}",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # === TASKPACK 2: THETA FAMILY ===
    # ---------------------------------------------------------------------
    # Taskpack 2 (θ-family + H_wθ): emit THETA_FAMILY.json + H_WTHETA.json + report.
    # Artefact-only; must not modify Phase C gating semantics.
    # ---------------------------------------------------------------------
    out_theta_family = run_dir / "THETA_FAMILY.json"
    out_hwtheta = run_dir / "H_WTHETA.json"

    task2_inputs_ok = bool(casa_path.exists() and casb_path.exists() and cas0c_path.exists() and entry_path.exists())

    theta_family_id = "edge_local_v1"
    dim_w2 = int(w_star.shape[0])
    theta_dim2 = int(dim_w2)
    labels2 = [f"theta:k={k}" for k in range(theta_dim2)]
    labels_hash2 = hashlib.sha256(
        json.dumps(labels2, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    H_wtheta = np.eye(dim_w2, dtype=float)
    H_wtheta_list = _matrix_to_list(H_wtheta)

    tol_sign2 = 1e-12
    H_wtheta_sign = _sign_matrix(H_wtheta, tol=tol_sign2)
    violations_nonneg2 = int(np.sum(np.asarray(H_wtheta) < -tol_sign2))
    violations_nonpos2 = int(np.sum(np.asarray(H_wtheta) > tol_sign2))
    nonnegative2 = bool(violations_nonneg2 == 0)
    nonpositive2 = bool(violations_nonpos2 == 0)
    mixed_sign2 = bool((not nonnegative2) and (not nonpositive2))

    if mixed_sign2:
        violations2 = 0
    elif nonnegative2:
        violations2 = violations_nonneg2
    elif nonpositive2:
        violations2 = violations_nonpos2
    else:
        violations2 = 0

    nnz2 = int(np.sum(np.abs(H_wtheta) > 0.0))
    nnz_by_col2 = [int(np.sum(np.abs(H_wtheta[:, j]) > 0.0)) for j in range(theta_dim2)]
    max_support_radius2 = 0

    selected_inverse_path2 = run_dir / "SELECTED_INVERSE_ENTRIES.json"
    readiness_slice_skipped2 = not selected_inverse_path2.exists()
    readiness_slice_details2: dict[str, Any] = {}
    if readiness_slice_skipped2:
        readiness_slice_details2 = {
            "skipped": True,
            "reason": "SELECTED_INVERSE_ENTRIES.json not present; readiness slice is optional.",
        }
    else:
        try:
            sel_inv2 = _read_json(selected_inverse_path2)
            sel_obj2 = sel_inv2.get("selection", {}).get("selected", {}) if isinstance(sel_inv2.get("selection"), dict) else {}
            sel_indices2 = sel_obj2.get("indices") if isinstance(sel_obj2, dict) else None
            if isinstance(sel_indices2, list) and all(isinstance(i, int) for i in sel_indices2):
                rows = [int(i) for i in sel_indices2 if 0 <= int(i) < dim_w2]
                slice_mat = H_wtheta[rows, :] if rows else np.zeros((0, theta_dim2), dtype=float)
                slice_viol_nonneg = int(np.sum(np.asarray(slice_mat) < -tol_sign2))
                slice_viol_nonpos = int(np.sum(np.asarray(slice_mat) > tol_sign2))
                slice_nonneg = bool(slice_viol_nonneg == 0)
                slice_nonpos = bool(slice_viol_nonpos == 0)
                slice_mixed = bool((not slice_nonneg) and (not slice_nonpos))
                if slice_mixed:
                    slice_violations = 0
                elif slice_nonneg:
                    slice_violations = slice_viol_nonneg
                elif slice_nonpos:
                    slice_violations = slice_viol_nonpos
                else:
                    slice_violations = 0
                readiness_slice_details2 = {
                    "skipped": False,
                    "selected_indices": rows,
                    "row_count": int(len(rows)),
                    "sign_pattern": {
                        "tolerance": tol_sign2,
                        "nonnegative": slice_nonneg,
                        "nonpositive": slice_nonpos,
                        "mixed_sign": slice_mixed,
                        "violations": int(slice_violations),
                    },
                }
            else:
                readiness_slice_details2 = {
                    "skipped": True,
                    "reason": "SELECTED_INVERSE_ENTRIES.json present but selection.selected.indices not readable.",
                }
        except Exception:  # noqa: BLE001
            readiness_slice_details2 = {
                "skipped": True,
                "reason": "Failed to parse SELECTED_INVERSE_ENTRIES.json; readiness slice skipped.",
            }

    task2_checks: list[dict[str, Any]] = []
    task2_checks.append(
        _mk_check(
            id="CHK.C2.INPUTS.PRESENT",
            ok=task2_inputs_ok,
            details={
                "CAS-A.json": casa_path.exists(),
                "CAS-B.json": casb_path.exists(),
                "CAS-0C.json": cas0c_path.exists(),
                "PhaseC_ENTRY_REPORT.md": entry_path.exists(),
                "SELECTED_INVERSE_ENTRIES.json": selected_inverse_path2.exists(),
            },
        )
    )
    task2_checks.append(
        _mk_check(
            id="CHK.C2.THETA_FAMILY.DEFINED",
            ok=bool(theta_family_id and theta_dim2 == len(labels2)),
            details={"theta_family_id": theta_family_id, "theta_dim": theta_dim2, "labels_len": int(len(labels2))},
        )
    )
    task2_checks.append(
        _mk_check(
            id="CHK.C2.LABELS.DETERMINISTIC",
            ok=bool(isinstance(labels_hash2, str) and len(labels_hash2) == 64),
            details={"labels_hash": labels_hash2},
        )
    )
    task2_checks.append(
        _mk_check(
            id="CHK.C2.H_WTHETA.COMPUTED",
            ok=bool(H_wtheta.shape[0] == dim_w2 and H_wtheta.shape[1] == theta_dim2),
            details={"computed": True, "format": "dense"},
        )
    )
    task2_checks.append(
        _mk_check(
            id="CHK.C2.H_WTHETA.SHAPE_MATCH",
            ok=bool(tuple(H_wtheta.shape) == (dim_w2, theta_dim2)),
            details={"shape": [int(H_wtheta.shape[0]), int(H_wtheta.shape[1])], "expected": [dim_w2, theta_dim2]},
        )
    )
    task2_checks.append(
        _mk_check(
            id="CHK.C2.H_WTHETA.FINITE_VALUES",
            ok=bool(np.isfinite(H_wtheta).all()),
            details={"all_finite": bool(np.isfinite(H_wtheta).all())},
        )
    )
    task2_checks.append(
        _mk_check(
            id="CHK.C2.H_WTHETA.SIGN_PATTERN_RECORDED",
            ok=True,
            details={
                "tolerance": tol_sign2,
                "nonnegative": nonnegative2,
                "nonpositive": nonpositive2,
                "mixed_sign": mixed_sign2,
                "violations": int(violations2),
            },
        )
    )
    task2_checks.append(
        _mk_check(
            id="CHK.C2.READINESS_SLICE.RECORDED",
            ok=True,
            details=readiness_slice_details2,
        )
    )

    task2_ok = _task2_all_required_pass(task2_checks)

    theta_family_payload: dict[str, Any] = {
        "schema_version": "C-THETA-FAMILY.v2",
        "run_id": run_dir.name,
        "generated_utc": created_at,
        "theta_family_id": theta_family_id,
        "scope": "pointwise_at_w_star",
        "definition": {
            "pattern": "perturbation_basis",
            "phi_theta_form": "Phi_cert(w,theta) = Phi_cert(w) + sum_k theta_k Psi_k(w)",
            "psi_family_description": "edge-local basis: Psi_e(w) = w_e",
            "psi_basis_type": "edge_local",
            "requires_graph_incidence": True,
        },
        "theta_dim": theta_dim2,
        "labels": labels2,
        "w_coordinate_system": {
            "dim_w": dim_w2,
            "edge_ordering_ref": "OPERATOR_LAYER.json",
            "notes": "w indices follow the implicit RealPhiV0Spec edge ordering recorded in OPERATOR_LAYER.json.",
        },
        "references": {
            "cas_a": "CAS-A.json",
            "cas_b": "CAS-B.json",
            "selected_inverse_entries": "SELECTED_INVERSE_ENTRIES.json" if selected_inverse_path2.exists() else "",
        },
    }

    hwtheta_payload: dict[str, Any] = {
        "schema_version": "C-H_WTHETA.v2",
        "run_id": run_dir.name,
        "generated_utc": created_at,
        "shape": [dim_w2, theta_dim2],
        "format": "dense",
        "data": H_wtheta_list,
        "tolerance": 0.0,
        "sparsity_summary": {
            "nnz": nnz2,
            "nnz_by_col": nnz_by_col2,
            "support_metric": "index_distance (order-dependent)",
            "max_support_radius": max_support_radius2,
        },
        "sign_pattern": {
            "tolerance": tol_sign2,
            "nonnegative": nonnegative2,
            "nonpositive": nonpositive2,
            "mixed_sign": mixed_sign2,
            "violations": int(violations2),
        },
        "sources": {
            "theta_family": "THETA_FAMILY.json",
            "cas_a": "CAS-A.json",
            "cas_b": "CAS-B.json",
        },
    }

    write_json(out_theta_family, theta_family_payload)
    write_json(out_hwtheta, hwtheta_payload)

    out_task2_report = run_dir / "PhaseC_TASK2_THETA_FAMILY_REPORT.md"
    out_task2_report.write_text(
        "\n".join(
            [
                "# Phase C Task 2 — θ-Family Definition + H_wθ Report (Template)",
                "",
                f"Run ID: **{run_dir.name}**",
                f"Generated (UTC): `{created_at}`",
                "",
                "## Summary",
                "",
                f"- Selected θ-family: `{theta_family_id}`",
                "- Scope: `pointwise_at_w_star`",
                f"- dim_w: `{dim_w2}`",
                f"- theta_dim: `{theta_dim2}`",
                "- H_wθ format: `dense`",
                f"- Status: **{'DONE' if task2_ok else 'BLOCKED'}**",
                "",
                "## Inputs (run root)",
                "",
                f"- CAS-A.json: {'✅' if casa_path.exists() else '❌'}",
                f"- CAS-B.json: {'✅' if casb_path.exists() else '❌'}",
                f"- CAS-0C.json: {'✅' if cas0c_path.exists() else '❌'}",
                f"- PhaseC_ENTRY_REPORT.md: {'✅' if entry_path.exists() else '❌'}",
                f"- SELECTED_INVERSE_ENTRIES.json (optional): {'✅' if selected_inverse_path2.exists() else '❌'}",
                "",
                "## Definition adopted",
                "",
                "State:",
                "\\[",
                "\\Phi_{\\mathrm{cert}}(w,\\theta) = \\Phi_{\\mathrm{cert}}(w) + \\sum_k \\theta_k\\,\\Psi_k(w)",
                "\\]",
                "and describe \\Psi_k for the chosen family.",
                "",
                "## Deterministic coordinate mapping",
                "",
                "Explain how w-indices correspond to edges (and nodes/motifs if used), and where the ordering comes from.",
                "",
                "## H_wθ artefact summary",
                "",
                f"- Shape: `({dim_w2}, {theta_dim2})`",
                f"- Sparsity: nnz=`{nnz2}`, nnz_by_col=`{nnz_by_col2}`, max_support_radius=`{max_support_radius2}` (state metric)",
                f"- Sign pattern (tol `{tol_sign2}`): nonnegative={nonnegative2} / nonpositive={nonpositive2} / mixed={mixed_sign2} / violations={int(violations2)}",
                "",
                "## Task-11 readiness slice (if Task 10 exists)",
                "",
                "If `SELECTED_INVERSE_ENTRIES.json` exists:",
                "- list selected indices/pairs",
                "- summarize the sign pattern of `H_wθ` restricted to those rows",
                "",
                "## Checks",
                "",
                "| Check ID | Status | Notes |",
                "|---|---|---|",
                *[
                    f"| {chk['id']} | {chk.get('status','FAIL')} | {json.dumps(chk.get('details', {}), sort_keys=True)} |"
                    for chk in task2_checks
                ],
                "",
                "## Result",
                "",
                f"**{'DONE' if task2_ok else 'BLOCKED'}**",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # === TASKPACK 3: HESSIAN ARTEFACTS ===
    # ---------------------------------------------------------------------
    # Taskpack 3 (Hessian artefacts): make HESSIAN_MATRIX.json audit-grade
    # with required checks and a run-root report.
    # ---------------------------------------------------------------------
    operator_layer_available = out_operator_layer.exists()
    structural_basis_rule = (
        "From OPERATOR_LAYER.json" if operator_layer_available else "Implicit RealPhiV0Spec edge ordering"
    )

    task3_checks: list[dict[str, Any]] = []
    dim_w = int(w_star.shape[0])
    is_square = bool(H.ndim == 2 and H.shape[0] == H.shape[1])
    dim_match = bool(is_square and int(H.shape[0]) == dim_w)
    finite_values = bool(np.isfinite(H).all())
    tol_policy_ok = bool(tol_sym == 1e-10)

    task3_checks.append(
        _mk_check(
            id="CHK.C3.HESSIAN_DIMENSION_MATCH",
            ok=dim_match,
            details={"dim_w": dim_w, "h_shape": [int(H.shape[0]), int(H.shape[1])]},
        )
    )
    task3_checks.append(
        _mk_check(
            id="CHK.C3.HESSIAN_SQUARE",
            ok=is_square,
            details={"h_shape": [int(H.shape[0]), int(H.shape[1])]},
        )
    )
    task3_checks.append(
        _mk_check(
            id="CHK.C3.HESSIAN_SYMMETRIC",
            ok=bool(sym_err <= tol_sym),
            details={"symmetry_error": sym_err, "symmetry_tol": tol_sym},
        )
    )
    task3_checks.append(
        _mk_check(
            id="CHK.C3.HESSIAN_FINITE_VALUES",
            ok=finite_values,
            details={"all_finite": finite_values},
        )
    )
    task3_checks.append(
        _mk_check(
            id="CHK.C3.HESSIAN_NUMERIC_TOLERANCE",
            ok=tol_policy_ok,
            details={"symmetry_tol": tol_sym, "expected": 1e-10},
        )
    )

    task3_ok = _task3_all_required_pass(task3_checks)

    hessian_matrix_payload: dict[str, Any] = {
        "schema_version": "C-TASK03.v1",
        "run_id": run_dir.name,
        "generated_utc": created_at,
        "sources": {
            "cas_a": str(casa_path),
            "cas_b": str(casb_path),
            "phase_c_entry_report": str(entry_path),
            "operator_layer": str(out_operator_layer) if operator_layer_available else None,
        },
        "structural_basis": {
            "basis_id": operator_layer_payload.get("structural_basis", {}).get("basis_id")
            if isinstance(operator_layer_payload.get("structural_basis"), dict)
            else "REAL_PHI_V0_SPEC_EDGE_ORDER",
            "ordering_rule": structural_basis_rule,
        },
        "dimension": int(H.shape[0]),
        "symmetry_error": sym_err,
        "tolerance_policy": {"symmetry_tol": tol_sym},
        "matrix": _matrix_to_list(H),
        "checks": task3_checks,
        "status": "PASS" if task3_ok else "FAIL",
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

    out_hessian = run_dir / "HESSIAN_MATRIX.json"
    out_blocks = run_dir / "HESSIAN_BLOCKS.json"
    out_inv = run_dir / "INVERSE_SIGN_STRUCTURE.json"
    out_exposure = run_dir / "EXPOSURE_RESPONSE_CHECK.json"

    write_json(out_hessian, hessian_matrix_payload)

    # === TASKPACK 4: BLOCK DECOMPOSITION ===
    # ---------------------------------------------------------------------
    # Taskpack 4 (Block decomposition): emit HESSIAN_BLOCKS.json + report.
    # Must not modify Phase C gating semantics.
    # ---------------------------------------------------------------------
    if not out_hessian.exists():
        raise RuntimeError("Task 4: missing required input HESSIAN_MATRIX.json")
    if not out_operator_layer.exists():
        raise RuntimeError("Task 4: missing required input OPERATOR_LAYER.json")

    n = int(H.shape[0])
    block_structure: dict[str, Any] = {
        "blocks": [
            {
                "name": "w",
                "index_start": 0,
                "index_end": n - 1,
                "size": n,
            }
        ]
    }

    tol_struct = 1e-12
    nz_i, nz_j = np.nonzero(np.abs(H) > tol_struct)
    nonzero_positions = [[int(i), int(j)] for i, j in zip(nz_i.tolist(), nz_j.tolist())]

    blocks = {
        "w_w": _matrix_to_list(H),
    }

    task4_checks: list[dict[str, Any]] = []
    hessian_available = bool(n > 0 and isinstance(hessian_matrix_payload.get("matrix"), list))
    task4_checks.append(_mk_check(id="CHK.C4.HESSIAN_AVAILABLE", ok=hessian_available, details={"dimension": n}))

    block_dim = sum(int(b.get("size", 0)) for b in block_structure.get("blocks", []) if isinstance(b, dict))
    task4_checks.append(
        _mk_check(
            id="CHK.C4.BLOCK_DIMENSION_MATCH",
            ok=bool(block_dim == n),
            details={"hessian_dimension": n, "block_dimension": int(block_dim)},
        )
    )

    task4_sym_err = float(np.max(np.abs(H - H.T)))
    task4_checks.append(
        _mk_check(
            id="CHK.C4.BLOCK_SYMMETRIC",
            ok=bool(task4_sym_err <= 1e-10),
            details={"symmetry_error": task4_sym_err, "tolerance": 1e-10},
        )
    )

    task4_checks.append(
        _mk_check(
            id="CHK.C4.SPARSITY_PATTERN_COMPUTED",
            ok=bool(len(nonzero_positions) > 0),
            details={"nonzero_count": int(len(nonzero_positions)), "tolerance": tol_struct},
        )
    )

    task4_ok = _task4_all_required_pass(task4_checks)

    blocks_payload: dict[str, Any] = {
        "schema_version": "C-TASK04.v2",
        "run_id": run_dir.name,
        "generated_utc": created_at,
        "dimension": n,
        "block_structure": block_structure,
        "sparsity_pattern": {"nonzero_positions": nonzero_positions},
        "blocks": blocks,
        "checks": task4_checks,
        "status": "PASS" if task4_ok else "FAIL",
    }

    write_json(out_blocks, blocks_payload)

    out_task4_report = run_dir / "PhaseC_TASK4_BLOCK_DECOMP_REPORT.md"
    out_task4_report.write_text(
        "\n".join(
            [
                "# Phase C Task 4 — Hessian Block Decomposition",
                "",
                f"Run ID: {run_dir.name}",
                f"Date (UTC): {created_at}",
                "Generated by: nps.phases.phase_c.build_casc (Taskpack 4 step)",
                "",
                "## Dimension",
                "",
                str(n),
                "",
                "## Block Structure",
                "",
                "w block → indices 0..n-1",
                "",
                "## Sparsity Pattern",
                "",
                f"Total non-zero entries (|H_ij| > {tol_struct}): {len(nonzero_positions)}",
                "",
                "## Checks",
                "",
                "| Check | Status |",
                "|---|---|",
                *[f"| {chk['id']} | {chk.get('status','FAIL')} |" for chk in task4_checks],
                "",
                "## Result",
                "",
                "DONE" if task4_ok else "BLOCKED",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    write_json(out_inv, inv_payload)
    write_json(out_exposure, exposure_payload)

    # === TASKPACK 5: LOCALITY/SPARSITY ===
    # ---------------------------------------------------------------------
    # Taskpack 5 (Locality/Sparsity certification): emit HESSIAN_SPARSITY_CERT.json
    # + report. Must not modify Phase C gating semantics.
    # ---------------------------------------------------------------------
    out_sparsity = run_dir / "HESSIAN_SPARSITY_CERT.json"

    if not out_blocks.exists():
        raise RuntimeError("Task 5: missing required input HESSIAN_BLOCKS.json")
    if not out_hessian.exists():
        raise RuntimeError("Task 5: missing required input HESSIAN_MATRIX.json")

    blocks_json = _read_json(out_blocks)
    n = int(blocks_json.get("dimension"))
    sp = blocks_json.get("sparsity_pattern") if isinstance(blocks_json.get("sparsity_pattern"), dict) else {}
    nonzero_positions_raw = sp.get("nonzero_positions")

    tol_struct = 1e-12
    sparsity_pattern_present = isinstance(sp, dict) and isinstance(nonzero_positions_raw, list)

    nonzero_positions: list[tuple[int, int]] = []
    if isinstance(nonzero_positions_raw, list):
        for p in nonzero_positions_raw:
            if not (isinstance(p, list) and len(p) == 2):
                continue
            i, j = p
            if not (isinstance(i, int) and isinstance(j, int)):
                continue
            if i < 0 or j < 0 or i >= n or j >= n:
                continue
            nonzero_positions.append((i, j))

    nonzero_positions_valid = sparsity_pattern_present and (len(nonzero_positions) == len(nonzero_positions_raw))
    nonzero_count = int(len(nonzero_positions))
    density = float(nonzero_count) / float(n * n) if n > 0 else 0.0
    locality_radius = int(max((abs(i - j) for (i, j) in nonzero_positions), default=0))

    task5_checks: list[dict[str, Any]] = []

    metrics_recorded_ok = bool(
        sparsity_pattern_present
        and nonzero_positions_valid
        and nonzero_count > 0
        and density > 0.0
    )
    task5_checks.append(
        _mk_check(
            id="CHK.C5.SPARSITY.METRICS_RECORDED",
            ok=metrics_recorded_ok,
            details={
                "dimension": n,
                "tolerance": tol_struct,
                "nonzero_count": nonzero_count,
                "density": density,
                "sparsity_pattern_present": sparsity_pattern_present,
                "nonzero_positions_valid": nonzero_positions_valid,
            },
        )
    )

    radius_tested_ok = bool(sparsity_pattern_present and nonzero_positions_valid)
    task5_checks.append(
        _mk_check(
            id="CHK.C5.LOCALITY.RADIUS_TESTED",
            ok=radius_tested_ok,
            details={
                "locality_radius": locality_radius,
                "definition": "max(abs(i-j)) over nonzero_positions (from HESSIAN_BLOCKS.json)",
            },
        )
    )

    support_bound_ok = bool(radius_tested_ok and locality_radius < n)
    task5_checks.append(
        _mk_check(
            id="CHK.C5.LOCALITY.SUPPORT_BOUND_HOLDS",
            ok=support_bound_ok,
            details={
                "locality_radius": locality_radius,
                "dimension": n,
                "rule": "locality_radius < dimension",
            },
        )
    )

    task5_ok = _task5_all_required_pass(task5_checks)

    sparsity_payload: dict[str, Any] = {
        "schema_version": "C-TASK05.v1",
        "run_id": run_dir.name,
        "generated_utc": created_at,
        "locality_metric": "index_distance",
        "interpretation": "order-dependent (coordinate-order bandedness), not graph-distance locality",
        "dimension": n,
        "sparsity_summary": {
            "nonzero_count": nonzero_count,
            "density": density,
            "locality_radius": locality_radius,
        },
        "checks": task5_checks,
    }

    write_json(out_sparsity, sparsity_payload)

    out_task5_report = run_dir / "PhaseC_TASK5_SPARSITY_REPORT.md"
    out_task5_report.write_text(
        "\n".join(
            [
                "# Phase C — Task 5 Report — Locality and Sparsity Support Bounds",
                "",
                f"Run ID: {run_dir.name}",
                f"Date (UTC): {created_at}",
                "Generated by: nps.phases.phase_c.build_casc (Taskpack 5 step)",
                "",
                "Artifacts written (run root):",
                f"- HESSIAN_SPARSITY_CERT.json: {out_sparsity.name}",
                f"- PhaseC_TASK5_SPARSITY_REPORT.md: {out_task5_report.name}",
                "",
                "---",
                "",
                "## Metrics",
                "",
                f"- dimension: {n}",
                f"- structural_zero_tol: {tol_struct}",
                f"- nonzero_count: {nonzero_count}",
                f"- density: {density}",
                f"- locality_radius: {locality_radius}",
                "",
                "## Checks",
                "",
                "| Check | Status |",
                "|---|---|",
                *[f"| {chk['id']} | {chk.get('status','FAIL')} |" for chk in task5_checks],
                "",
                "## Result",
                "",
                "DONE" if task5_ok else "BLOCKED",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # === TASKPACK 6: DIAGONAL DOMINANCE ===
    # ---------------------------------------------------------------------
    # Taskpack 6 (Diagonal Dominance certification): emit DIAGONAL_DOMINANCE_CERT.json
    # + report. Must not modify Phase C gating semantics.
    # ---------------------------------------------------------------------
    out_ddom = run_dir / "DIAGONAL_DOMINANCE_CERT.json"

    if not out_blocks.exists():
        raise RuntimeError("Task 6: missing required input HESSIAN_BLOCKS.json")
    if not out_hessian.exists():
        raise RuntimeError("Task 6: missing required input HESSIAN_MATRIX.json")
    if not out_sparsity.exists():
        raise RuntimeError("Task 6: missing required input HESSIAN_SPARSITY_CERT.json")

    blocks_json_6 = _read_json(out_blocks)
    blocks_6 = blocks_json_6.get("blocks") if isinstance(blocks_json_6.get("blocks"), dict) else {}
    Hww_raw = blocks_6.get("w_w")
    if not isinstance(Hww_raw, list):
        raise RuntimeError("Task 6: missing required blocks['w_w'] in HESSIAN_BLOCKS.json")

    Hww = np.asarray(Hww_raw, dtype=float)
    if Hww.ndim != 2 or Hww.shape[0] != Hww.shape[1]:
        raise RuntimeError("Task 6: blocks['w_w'] must be a square matrix")

    n6 = int(Hww.shape[0])
    C = -Hww

    diag6 = np.diag(C)
    absC6 = np.abs(C)
    row_sum_abs6 = np.sum(absC6, axis=1)
    row_sum_off6 = row_sum_abs6 - np.abs(diag6)
    margins6 = diag6 - row_sum_off6

    row_metrics6: list[dict[str, Any]] = []
    for i in range(n6):
        margin_i = float(margins6[i])
        row_metrics6.append(
            {
                "row": int(i),
                "diag": float(diag6[i]),
                "row_sum_off": float(row_sum_off6[i]),
                "margin": margin_i,
                "strict": bool(margin_i > 0.0),
            }
        )

    min_margin6 = float(np.min(margins6)) if n6 > 0 else float("nan")
    min_margin_row6 = int(np.argmin(margins6)) if n6 > 0 else -1

    # Derived sign pattern metrics for downstream tasks.
    tol_sign6 = 1e-12
    offdiag6 = C.copy()
    np.fill_diagonal(offdiag6, 0.0)
    offdiag_max6 = float(np.max(offdiag6)) if n6 > 1 else 0.0
    off_diagonal_nonpositive6 = bool(offdiag_max6 <= tol_sign6)
    candidate_z_matrix6 = off_diagonal_nonpositive6
    candidate_m_matrix6 = bool(off_diagonal_nonpositive6 and np.isfinite(min_margin6) and min_margin6 > 0.0)

    task6_checks: list[dict[str, Any]] = []
    task6_checks.append(
        _mk_check(
            id="CHK.C6.C_MATRIX.DEFINED",
            ok=bool(np.all(np.isfinite(C))),
            details={
                "dimension": n6,
                "definition": "C := -H where H is blocks['w_w'] from HESSIAN_BLOCKS.json",
            },
        )
    )
    task6_checks.append(
        _mk_check(
            id="CHK.C6.DOMINANCE.MARGINS_COMPUTED",
            ok=bool(len(row_metrics6) == n6 and np.all(np.isfinite(margins6))),
            details={
                "dimension": n6,
                "min_margin": min_margin6,
            },
        )
    )
    task6_checks.append(
        _mk_check(
            id="CHK.C6.DOMINANCE.STRICT_PASS",
            ok=bool(np.isfinite(min_margin6) and min_margin6 > 0.0),
            details={
                "min_margin": min_margin6,
                "min_margin_row": min_margin_row6,
            },
        )
    )

    task6_ok = _task6_all_required_pass(task6_checks)

    ddom_payload: dict[str, Any] = {
        "schema_version": "C-TASK06.v2",
        "run_id": run_dir.name,
        "generated_utc": created_at,
        "sources": {
            "HESSIAN_MATRIX": str(out_hessian),
            "HESSIAN_BLOCKS": str(out_blocks),
            "HESSIAN_SPARSITY": str(out_sparsity),
        },
        "matrix_definition": {
            "base_matrix": "H",
            "coupling_matrix": "C := -H",
            "block": "w_w",
        },
        "row_metrics": row_metrics6,
        "witnesses": {
            "min_margin_row": min_margin_row6,
            "min_margin": min_margin6,
        },
        "derived_sign_pattern": {
            "off_diagonal_nonpositive": off_diagonal_nonpositive6,
            "offdiagonal_nonpositive": off_diagonal_nonpositive6,
            "candidate_Z_matrix": candidate_z_matrix6,
            "candidate_m_matrix": candidate_m_matrix6,
            "tolerance": tol_sign6,
        },
        "checks": task6_checks,
        "status": "PASS" if task6_ok else "FAIL",
    }

    write_json(out_ddom, ddom_payload)

    out_task6_report = run_dir / "PhaseC_TASK6_DIAGONAL_DOMINANCE_REPORT.md"
    out_task6_report.write_text(
        "\n".join(
            [
                "# Phase C — Task 6 Report — Diagonal Dominance Certification",
                "",
                f"Run ID: {run_dir.name}",
                f"Date (UTC): {created_at}",
                "Generated by: nps.phases.phase_c.build_casc (Taskpack 6 step)",
                "",
                "Artifacts written (run root):",
                f"- DIAGONAL_DOMINANCE_CERT.json: {out_ddom.name}",
                f"- PhaseC_TASK6_DIAGONAL_DOMINANCE_REPORT.md: {out_task6_report.name}",
                "",
                "---",
                "",
                "## Matrix definition",
                "",
                "C := -H, where H is blocks['w_w'] from HESSIAN_BLOCKS.json",
                "",
                "## Summary",
                "",
                f"- dimension: {n6}",
                f"- min_margin: {min_margin6}",
                f"- min_margin_row: {min_margin_row6}",
                f"- strict_diagonal_dominance: {bool(np.isfinite(min_margin6) and min_margin6 > 0.0)}",
                "",
                "## Derived sign pattern",
                "",
                f"- off_diagonal_nonpositive: {off_diagonal_nonpositive6}",
                f"- candidate_Z_matrix: {candidate_z_matrix6}",
                f"- tolerance: {tol_sign6}",
                "",
                "## Checks",
                "",
                "| Check | Status |",
                "|---|---|",
                *[f"| {chk['id']} | {chk.get('status','FAIL')} |" for chk in task6_checks],
                "",
                "## Result",
                "",
                "DONE" if task6_ok else "BLOCKED",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # === TASKPACK 7: COMPARISON INEQUALITIES ===
    # ---------------------------------------------------------------------
    # Taskpack 7 (Comparison inequalities / Z-matrix certification)
    # Artefact-only; must not modify Phase C gating semantics.
    # ---------------------------------------------------------------------
    out_cmp = run_dir / "COMPARISON_INEQUALITIES_CERT.json"

    required_paths = {
        "HESSIAN_BLOCKS": out_blocks,
        "DIAGONAL_DOMINANCE": out_ddom,
    }
    optional_paths = {
        "HESSIAN_SPARSITY": out_sparsity,
        "OPERATOR_LAYER": out_operator_layer,
        "HESSIAN_MATRIX": out_hessian,
    }

    inputs_found: list[str] = []
    inputs_missing: list[str] = []
    for k, p in required_paths.items():
        if p.exists():
            inputs_found.append(k)
        else:
            inputs_missing.append(k)
    for k, p in optional_paths.items():
        if p.exists():
            inputs_found.append(k)

    tol_offdiag = 1e-12

    matrix_definition7: dict[str, Any] = {
        "base_matrix": "H",
        "coupling_matrix": "C := -H",
        "block": "w_w",
    }

    derived_from_task6: dict[str, Any] = {}
    task6_strict_dd_pass = False

    z_ok = False
    max_offdiag_value = float("nan")
    violations: list[dict[str, Any]] = []

    # Try to parse inputs. If missing, emit FAIL artefacts without raising.
    inputs_parse_ok = True
    Hww7: np.ndarray | None = None
    if inputs_missing:
        inputs_parse_ok = False
    else:
        try:
            blocks_json7 = _read_json(out_blocks)
            blocks7 = blocks_json7.get("blocks") if isinstance(blocks_json7.get("blocks"), dict) else {}
            Hww_raw7 = blocks7.get("w_w")
            Hww7 = np.asarray(Hww_raw7, dtype=float)
            if Hww7.ndim != 2 or Hww7.shape[0] != Hww7.shape[1]:
                inputs_parse_ok = False
        except Exception:  # noqa: BLE001
            inputs_parse_ok = False

        try:
            ddom_json7 = _read_json(out_ddom)
            if isinstance(ddom_json7.get("matrix_definition"), dict):
                matrix_definition7 = dict(ddom_json7.get("matrix_definition"))
            if isinstance(ddom_json7.get("derived_sign_pattern"), dict):
                derived_from_task6 = dict(ddom_json7.get("derived_sign_pattern"))
            checks6 = ddom_json7.get("checks") if isinstance(ddom_json7.get("checks"), list) else []
            for chk in checks6:
                if not isinstance(chk, dict):
                    continue
                if chk.get("id") == "CHK.C6.DOMINANCE.STRICT_PASS":
                    task6_strict_dd_pass = bool(chk.get("ok") is True)
                    break
        except Exception:  # noqa: BLE001
            inputs_parse_ok = False

    if inputs_parse_ok and Hww7 is not None:
        C7 = -Hww7
        n7 = int(C7.shape[0])
        max_val = -float("inf")
        for i in range(n7):
            for j in range(n7):
                if i == j:
                    continue
                v = float(C7[i, j])
                if v > max_val:
                    max_val = v
                if v > tol_offdiag:
                    violations.append({"i": int(i), "j": int(j), "value": v})
        max_offdiag_value = float(max_val) if n7 > 0 else 0.0
        violations_sorted = sorted(violations, key=lambda x: float(x["value"]), reverse=True)
        top_k_violations = violations_sorted[:10]
        z_ok = bool(max_offdiag_value <= tol_offdiag)
    else:
        top_k_violations = []

    candidate_z_matrix = bool(z_ok)
    candidate_m_matrix = bool(candidate_z_matrix and task6_strict_dd_pass)

    task7_checks: list[dict[str, Any]] = []
    task7_checks.append(
        _mk_check(
            id="CHK.C7.INPUTS.PRESENT",
            ok=bool(inputs_parse_ok),
            details={
                "inputs_found": sorted(inputs_found),
                "inputs_missing": sorted(inputs_missing),
            },
        )
    )
    task7_checks.append(
        _mk_check(
            id="CHK.C7.ZMATRIX.OFFDIAG_NONPOSITIVE",
            ok=bool(inputs_parse_ok and z_ok),
            details={
                "tolerance": tol_offdiag,
                "max_offdiag_value": max_offdiag_value,
                "violation_count": int(len(violations)),
                "top_k_violations": top_k_violations,
            },
        )
    )
    task7_checks.append(
        _mk_check(
            id="CHK.C7.M_MATRIX.CANDIDATE",
            ok=bool(inputs_parse_ok and candidate_m_matrix),
            details={
                "task6_strict_dd_pass": task6_strict_dd_pass,
                "candidate_Z_matrix": candidate_z_matrix,
                "candidate_m_matrix": candidate_m_matrix,
            },
        )
    )

    task7_ok = _task7_all_required_pass(task7_checks)
    cmp_payload: dict[str, Any] = {
        "schema_version": "C-TASK07.v2",
        "run_id": run_dir.name,
        "generated_utc": created_at,
        "sources": {
            **{k: str(p) for k, p in required_paths.items() if p.exists()},
            **{k: str(p) for k, p in optional_paths.items() if p.exists()},
        },
        "matrix_definition": matrix_definition7,
        "tolerances": {"offdiag_nonpositive": tol_offdiag},
        "derived_sign_pattern": {
            "computed": {
                "off_diagonal_nonpositive": bool(z_ok),
                "candidate_Z_matrix": bool(candidate_z_matrix),
                "candidate_m_matrix": bool(candidate_m_matrix),
            },
            "from_task6": derived_from_task6,
        },
        "witnesses": {
            "max_offdiag_value": max_offdiag_value,
            "top_k_violations": top_k_violations,
        },
        "checks": task7_checks,
        "status": "PASS" if task7_ok else "FAIL",
    }

    write_json(out_cmp, cmp_payload)

    out_task7_report = run_dir / "PhaseC_TASK7_COMPARISON_INEQUALITIES_REPORT.md"
    out_task7_report.write_text(
        "\n".join(
            [
                "# Phase C — Task 7 Report — Comparison Inequalities",
                "",
                f"Run ID: {run_dir.name}",
                f"Date (UTC): {created_at}",
                "Generated by: nps.phases.phase_c.build_casc (Taskpack 7 step)",
                "",
                "Artifacts written (run root):",
                f"- COMPARISON_INEQUALITIES_CERT.json: {out_cmp.name}",
                f"- PhaseC_TASK7_COMPARISON_INEQUALITIES_REPORT.md: {out_task7_report.name}",
                "",
                "---",
                "",
                "## Inputs",
                "",
                f"- inputs_found: {', '.join(sorted(inputs_found))}",
                f"- inputs_missing: {', '.join(sorted(inputs_missing))}",
                "",
                "## Matrix definition",
                "",
                json.dumps(matrix_definition7, sort_keys=True),
                "",
                "## Z-matrix sign condition",
                "",
                f"- tolerance: {tol_offdiag}",
                f"- max_offdiag_value: {max_offdiag_value}",
                f"- violation_count: {len(violations)}",
                "",
                "## Derived sign pattern",
                "",
                f"- off_diagonal_nonpositive: {bool(z_ok)}",
                f"- candidate_Z_matrix: {candidate_z_matrix}",
                f"- candidate_m_matrix: {candidate_m_matrix}",
                f"- task6_strict_dd_pass: {task6_strict_dd_pass}",
                "",
                "## Checks",
                "",
                "| Check | Status |",
                "|---|---|",
                *[f"| {chk['id']} | {chk.get('status','FAIL')} |" for chk in task7_checks],
                "",
                "## Result",
                "",
                "DONE" if task7_ok else "BLOCKED",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # === TASKPACK 8: NEUMANN-SERIES BOUNDS ===
    # ---------------------------------------------------------------------
    # Taskpack 8 (Neumann-series inversion bounds)
    # Artefact-only; must not modify Phase C gating semantics.
    # ---------------------------------------------------------------------
    out_neumann = run_dir / "NEUMANN_SERIES_CERT.json"

    required_paths8 = {
        "HESSIAN_BLOCKS": out_blocks,
        "DIAGONAL_DOMINANCE": out_ddom,
        "COMPARISON_INEQUALITIES": out_cmp,
    }
    optional_paths8 = {
        "HESSIAN_SPARSITY": out_sparsity,
        "OPERATOR_LAYER": out_operator_layer,
        "HESSIAN_MATRIX": out_hessian,
    }

    inputs_found8: list[str] = []
    inputs_missing8: list[str] = []
    for k, p in required_paths8.items():
        if p.exists():
            inputs_found8.append(k)
        else:
            inputs_missing8.append(k)
    for k, p in optional_paths8.items():
        if p.exists():
            inputs_found8.append(k)

    matrix_definition8: dict[str, Any] = {
        "base_matrix": "H",
        "coupling_matrix": "C := -H",
        "block": "w_w",
        "splitting": "C = D - B with D = diag(C) and B = D - C",
    }

    inputs_parse_ok8 = True
    Hww8: np.ndarray | None = None
    if inputs_missing8:
        inputs_parse_ok8 = False
    else:
        try:
            blocks_json8 = _read_json(out_blocks)
            blocks8 = blocks_json8.get("blocks") if isinstance(blocks_json8.get("blocks"), dict) else {}
            Hww_raw8 = blocks8.get("w_w")
            Hww8 = np.asarray(Hww_raw8, dtype=float)
            if Hww8.ndim != 2 or Hww8.shape[0] != Hww8.shape[1]:
                inputs_parse_ok8 = False
        except Exception:  # noqa: BLE001
            inputs_parse_ok8 = False

        try:
            ddom_json8 = _read_json(out_ddom)
            if isinstance(ddom_json8.get("matrix_definition"), dict):
                matrix_definition8.update({"task6_matrix_definition": ddom_json8.get("matrix_definition")})
        except Exception:  # noqa: BLE001
            inputs_parse_ok8 = False

        try:
            cmp_json8 = _read_json(out_cmp)
            checks7 = cmp_json8.get("checks") if isinstance(cmp_json8.get("checks"), list) else []
            # best-effort: ensure prior step passed its required checks
            for chk in checks7:
                if isinstance(chk, dict) and chk.get("id") == "CHK.C7.M_MATRIX.CANDIDATE":
                    matrix_definition8.update({"task7_candidate_m_matrix": bool(chk.get("ok") is True)})
                    break
        except Exception:  # noqa: BLE001
            inputs_parse_ok8 = False

    rho_bound = float("nan")
    rho_per_row: list[float] = []
    min_diag = float("nan")
    bad_diag_rows: list[int] = []

    if inputs_parse_ok8 and Hww8 is not None:
        C8 = -Hww8
        diag8 = np.diag(C8)
        if diag8.size:
            min_diag = float(np.min(diag8))
        rho_vals: list[float] = []
        for i in range(int(C8.shape[0])):
            d_ii = float(C8[i, i])
            off_sum = float(np.sum(np.abs(C8[i, :])) - abs(float(C8[i, i])))
            if not np.isfinite(d_ii) or d_ii <= 0.0:
                bad_diag_rows.append(int(i))
                rho_i = float("inf")
            else:
                rho_i = off_sum / d_ii
            rho_vals.append(float(rho_i))
        rho_per_row = rho_vals
        rho_bound = float(np.max(rho_vals)) if rho_vals else 0.0

    task8_checks: list[dict[str, Any]] = []
    task8_checks.append(
        _mk_check(
            id="CHK.C8.INPUTS.PRESENT",
            ok=bool(inputs_parse_ok8),
            details={
                "inputs_found": sorted(inputs_found8),
                "inputs_missing": sorted(inputs_missing8),
            },
        )
    )
    task8_checks.append(
        _mk_check(
            id="CHK.C8.NEUMANN.RHO_BOUND_COMPUTED",
            ok=bool(inputs_parse_ok8 and np.isfinite(rho_bound)),
            details={
                "rho_bound": rho_bound,
                "min_diag": min_diag,
                "bad_diag_rows": bad_diag_rows,
            },
        )
    )
    task8_checks.append(
        _mk_check(
            id="CHK.C8.NEUMANN.RHO_LT_ONE",
            ok=bool(inputs_parse_ok8 and np.isfinite(rho_bound) and rho_bound < 1.0),
            details={
                "rho_bound": rho_bound,
                "threshold": 1.0,
            },
        )
    )

    task8_ok = _task8_all_required_pass(task8_checks)
    neumann_payload: dict[str, Any] = {
        "schema_version": "C-TASK08.v1",
        "run_id": run_dir.name,
        "generated_utc": created_at,
        "sources": {
            **{k: str(p) for k, p in required_paths8.items() if p.exists()},
            **{k: str(p) for k, p in optional_paths8.items() if p.exists()},
        },
        "matrix_definition": matrix_definition8,
        "neumann_bound": {
            "rho_bound": rho_bound,
            "rho_per_row": rho_per_row,
        },
        "witnesses": {
            "min_diag": min_diag,
            "bad_diag_rows": bad_diag_rows,
        },
        "checks": task8_checks,
        "status": "PASS" if task8_ok else "FAIL",
    }

    write_json(out_neumann, neumann_payload)

    out_task8_report = run_dir / "PhaseC_TASK8_NEUMANN_SERIES_REPORT.md"
    out_task8_report.write_text(
        "\n".join(
            [
                "# Phase C — Task 8 Report — Neumann-Series Inversion Bounds",
                "",
                f"Run ID: {run_dir.name}",
                f"Date (UTC): {created_at}",
                "Generated by: nps.phases.phase_c.build_casc (Taskpack 8 step)",
                "",
                "Artifacts written (run root):",
                f"- NEUMANN_SERIES_CERT.json: {out_neumann.name}",
                f"- PhaseC_TASK8_NEUMANN_SERIES_REPORT.md: {out_task8_report.name}",
                "",
                "------------------------------------------------------------------------",
                "",
                "## Run",
                "",
                f"    {run_dir.name}",
                "",
                "------------------------------------------------------------------------",
                "",
                "## Matrix Definition",
                "",
                "    C := -H",
                "",
                "------------------------------------------------------------------------",
                "",
                "## Neumann Bound",
                "",
                "  Metric      Value",
                "  ----------- -------",
                f"  rho_bound   {rho_bound}",
                "",
                "------------------------------------------------------------------------",
                "",
                "## Checks",
                "",
                "  Check                               Status",
                "  ----------------------------------- --------",
                *[f"  {chk['id']:<35} {chk.get('status','FAIL')}" for chk in task8_checks],
                "",
                "------------------------------------------------------------------------",
                "",
                "## Result",
                "",
                f"    {'DONE' if task8_ok else 'BLOCKED'}",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # === TASKPACK 9: M-MATRIX CRITERIA ===
    # ---------------------------------------------------------------------
    # Taskpack 9 (M-matrix criteria and inverse positivity)
    # Must fail loudly if required upstream artefacts are missing.
    # ---------------------------------------------------------------------
    out_m_matrix = run_dir / "M_MATRIX_CERT.json"
    out_inv_pos = run_dir / "INVERSE_POSITIVITY_CERT.json"

    required_paths9 = {
        "DIAGONAL_DOMINANCE": out_ddom,
        "COMPARISON_INEQUALITIES": out_cmp,
        "NEUMANN_SERIES": out_neumann,
        "HESSIAN_BLOCKS": out_blocks,
    }
    missing9 = [k for k, p in required_paths9.items() if not p.exists()]
    if missing9:
        raise RuntimeError(f"Task 9: missing required inputs: {', '.join(sorted(missing9))}")

    ddom_json9 = _read_json(out_ddom)
    cmp_json9 = _read_json(out_cmp)
    neumann_json9 = _read_json(out_neumann)
    blocks_json9 = _read_json(out_blocks)

    # Preconditions (authoritative via upstream tasks)
    strict_dd_ok9 = False
    checks6_9 = ddom_json9.get("checks") if isinstance(ddom_json9.get("checks"), list) else []
    for chk in checks6_9:
        if isinstance(chk, dict) and chk.get("id") == "CHK.C6.DOMINANCE.STRICT_PASS":
            strict_dd_ok9 = bool(chk.get("ok") is True)
            break

    offdiag_nonpos_ok9 = False
    checks7_9 = cmp_json9.get("checks") if isinstance(cmp_json9.get("checks"), list) else []
    for chk in checks7_9:
        if isinstance(chk, dict) and chk.get("id") == "CHK.C7.ZMATRIX.OFFDIAG_NONPOSITIVE":
            offdiag_nonpos_ok9 = bool(chk.get("ok") is True)
            break

    preconditions_ok9 = bool(strict_dd_ok9 and offdiag_nonpos_ok9)
    theorem_used9 = "Z_MATRIX_PLUS_STRICT_DD_IMPLIES_NONSINGULAR_M_MATRIX"

    inverse_sign_conclusion9: dict[str, Any] = {
        "matrix": "C := -H",
        "is_nonsingular_m_matrix": bool(preconditions_ok9),
        "inverse_entrywise_nonnegative": bool(preconditions_ok9),
        "theorem_used": theorem_used9,
    }

    task9_checks: list[dict[str, Any]] = []
    task9_checks.append(
        _mk_check(
            id="CHK.C9.MMATRIX.PRECONDITIONS_PASS",
            ok=bool(preconditions_ok9),
            details={
                "task6": {
                    "strict_diagonal_dominance": strict_dd_ok9,
                    "check_id": "CHK.C6.DOMINANCE.STRICT_PASS",
                    "artifact": out_ddom.name,
                },
                "task7": {
                    "off_diagonal_nonpositive": offdiag_nonpos_ok9,
                    "check_id": "CHK.C7.ZMATRIX.OFFDIAG_NONPOSITIVE",
                    "artifact": out_cmp.name,
                },
            },
        )
    )
    task9_checks.append(
        _mk_check(
            id="CHK.C9.MMATRIX.NONSINGULAR_CONCLUDED",
            ok=bool(preconditions_ok9),
            details={
                "theorem_used": theorem_used9,
                "logic": "Z-matrix + strict diagonal dominance => nonsingular M-matrix",
            },
        )
    )
    task9_checks.append(
        _mk_check(
            id="CHK.C9.INVERSE.NONNEGATIVE_CONCLUDED",
            ok=bool(preconditions_ok9),
            details={
                "conclusion": "C^{-1} >= 0 (entrywise)",
                "basis": theorem_used9,
            },
        )
    )

    task9_ok = _task9_all_required_pass(task9_checks)

    matrix_definition9: dict[str, Any] = {
        "base_matrix": "H",
        "coupling_matrix": "C := -H",
        "block": "w_w",
    }

    m_matrix_payload: dict[str, Any] = {
        "schema_version": "C-TASK09.v1",
        "run_id": run_dir.name,
        "generated_utc": created_at,
        "sources": {
            "DIAGONAL_DOMINANCE_CERT": str(out_ddom),
            "COMPARISON_INEQUALITIES_CERT": str(out_cmp),
            "NEUMANN_SERIES_CERT": str(out_neumann),
            "HESSIAN_BLOCKS": str(out_blocks),
        },
        "matrix_definition": matrix_definition9,
        "upstream_summary": {
            "task6": {
                "strict_diagonal_dominance": strict_dd_ok9,
            },
            "task7": {
                "off_diagonal_nonpositive": offdiag_nonpos_ok9,
            },
            "task8": {
                "status": neumann_json9.get("status"),
            },
            "task4": {
                "blocks_present": isinstance(blocks_json9.get("blocks"), dict),
            },
        },
        "inverse_sign_conclusion": inverse_sign_conclusion9,
        "checks": task9_checks,
        "status": "PASS" if task9_ok else "FAIL",
    }

    inv_pos_payload: dict[str, Any] = {
        "schema_version": "C-TASK09.v1",
        "run_id": run_dir.name,
        "generated_utc": created_at,
        "sources": {
            "M_MATRIX_CERT": str(out_m_matrix),
            "DIAGONAL_DOMINANCE_CERT": str(out_ddom),
            "COMPARISON_INEQUALITIES_CERT": str(out_cmp),
            "NEUMANN_SERIES_CERT": str(out_neumann),
        },
        "matrix": "C := -H",
        "inverse_sign_conclusion": inverse_sign_conclusion9,
        "checks": task9_checks,
        "status": "PASS" if task9_ok else "FAIL",
    }

    write_json(out_m_matrix, m_matrix_payload)
    write_json(out_inv_pos, inv_pos_payload)

    out_task9_report = run_dir / "PhaseC_TASK9_M_MATRIX_REPORT.md"
    out_task9_report.write_text(
        "\n".join(
            [
                "# Phase C Taskpack 9 Report",
                "",
                f"Run ID: {run_dir.name}",
                f"Date (UTC): {created_at}",
                "Generated by: nps.phases.phase_c.build_casc (Taskpack 9 step)",
                "",
                "------------------------------------------------------------------------",
                "",
                "## Run",
                "",
                f"    {run_dir.name}",
                "",
                "------------------------------------------------------------------------",
                "",
                "## Matrix Definition",
                "",
                "C := -H",
                "",
                "------------------------------------------------------------------------",
                "",
                "## Preconditions",
                "",
                "  Property                     Status",
                "  ---------------------------- --------",
                f"  Strict diagonal dominance     {'PASS' if strict_dd_ok9 else 'FAIL'}",
                f"  Off-diagonal nonpositivity    {'PASS' if offdiag_nonpos_ok9 else 'FAIL'}",
                "",
                "------------------------------------------------------------------------",
                "",
                "## Theorem Used",
                "",
                "Z-matrix + strict diagonal dominance ⇒ nonsingular M-matrix",
                "",
                "------------------------------------------------------------------------",
                "",
                "## Certification Result",
                "",
                "  Property                        Value",
                "  ------------------------------- -------",
                f"  is_nonsingular_m_matrix          {inverse_sign_conclusion9['is_nonsingular_m_matrix']}",
                f"  inverse_entrywise_nonnegative    {inverse_sign_conclusion9['inverse_entrywise_nonnegative']}",
                "",
                "------------------------------------------------------------------------",
                "",
                "## Checks",
                "",
                "  Check                                  Status",
                "  -------------------------------------- --------",
                *[f"  {chk['id']:<38} {chk.get('status','FAIL')}" for chk in task9_checks],
                "",
                "------------------------------------------------------------------------",
                "",
                "## Result",
                "",
                f"    {'DONE' if task9_ok else 'BLOCKED'}",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # === TASKPACK 10: SELECTED INVERSE ENTRIES ===
    # ---------------------------------------------------------------------
    # Taskpack 10 (Selected inverse entries and Phase D interface)
    # Deterministic selection + witnesses; must not modify Phase C gating.
    # ---------------------------------------------------------------------
    out_sel_inv = run_dir / "SELECTED_INVERSE_ENTRIES.json"

    task10_missing_deps = False
    task10_missing_details: dict[str, Any] = {}

    if not out_blocks.exists():
        task10_missing_deps = True
        task10_missing_details["missing"] = ["HESSIAN_BLOCKS.json"]

    inv_sign_path = run_dir / "INVERSE_POSITIVITY_CERT.json"
    neumann_bound_path = run_dir / "NEUMANN_SERIES_BOUND.json"
    neumann_cert_path = run_dir / "NEUMANN_SERIES_CERT.json"

    inv_kind = ""
    inv_source_path: Path | None = None
    inv_entrywise_nonnegative: bool | None = None
    inv_notes = ""

    if inv_sign_path.exists():
        inv_kind = "INVERSE_POSITIVITY_CERT"
        inv_source_path = inv_sign_path
        try:
            inv_json = _read_json(inv_sign_path)
            concl = (
                inv_json.get("inverse_sign_conclusion")
                if isinstance(inv_json.get("inverse_sign_conclusion"), dict)
                else {}
            )
            inv_entrywise_nonnegative = (
                bool(concl.get("inverse_entrywise_nonnegative"))
                if isinstance(concl.get("inverse_entrywise_nonnegative"), bool)
                else None
            )
        except Exception:  # noqa: BLE001
            inv_entrywise_nonnegative = None
    elif neumann_bound_path.exists():
        inv_kind = "NEUMANN_SERIES_BOUND"
        inv_source_path = neumann_bound_path
        inv_entrywise_nonnegative = False
        inv_notes = "Neumann-series bound does not by itself certify entrywise sign; treated as unknown."
    elif neumann_cert_path.exists():
        inv_kind = "NEUMANN_SERIES_BOUND"
        inv_source_path = neumann_cert_path
        inv_entrywise_nonnegative = False
        inv_notes = "Using NEUMANN_SERIES_CERT.json as fallback; does not certify entrywise sign."
    else:
        task10_missing_deps = True
        inv_kind = "MISSING"
        inv_source_path = None
        inv_entrywise_nonnegative = None
        inv_notes = "Missing inverse-sign source (expected INVERSE_POSITIVITY_CERT.json or NEUMANN_SERIES_BOUND.json / NEUMANN_SERIES_CERT.json)."

    dim10 = 0
    if not task10_missing_deps:
        blocks_json10 = _read_json(out_blocks)
        blocks10 = blocks_json10.get("blocks") if isinstance(blocks_json10.get("blocks"), dict) else {}
        Hww_raw10 = blocks10.get("w_w")
        if not isinstance(Hww_raw10, list):
            task10_missing_deps = True
            task10_missing_details["missing"] = (task10_missing_details.get("missing") or []) + ["HESSIAN_BLOCKS.blocks.w_w"]
        else:
            Hww10 = np.asarray(Hww_raw10, dtype=float)
            if Hww10.ndim != 2 or Hww10.shape[0] != Hww10.shape[1]:
                task10_missing_deps = True
                task10_missing_details["invalid"] = {"w_w_shape": [int(x) for x in Hww10.shape]}
            else:
                dim10 = int(Hww10.shape[0])

    rule_id10 = "C10.RULE.MINIMAL_PHASED_INTERFACE.v1"
    rule_text10 = (
        "Select diagonal entries (i,i) for all i in [0, dimension-1] to provide a minimal deterministic Phase D interface."
    )
    indices10 = list(range(dim10))
    pairs10 = [(i, i) for i in range(dim10)]

    selected_obj10: dict[str, Any] = {
        "indices": indices10,
        "pairs": [[int(i), int(j)] for i, j in pairs10],
    }
    canonical_selected10 = json.dumps(selected_obj10, sort_keys=True, separators=(",", ":"))
    selection_hash10 = hashlib.sha256(canonical_selected10.encode("utf-8")).hexdigest()

    selected_entries10: list[dict[str, Any]] = []
    if (not task10_missing_deps) and inv_kind == "INVERSE_POSITIVITY_CERT" and inv_entrywise_nonnegative is True:
        for i, j in pairs10:
            selected_entries10.append(
                {"i": int(i), "j": int(j), "sign": "+", "source": "INVERSE_POSITIVITY_CERT"}
            )
    else:
        for i, j in pairs10:
            selected_entries10.append({"i": int(i), "j": int(j), "sign": "?", "source": inv_kind})

    in_bounds_indices10 = all(isinstance(i, int) and 0 <= i < dim10 for i in indices10)
    in_bounds_pairs10 = all(0 <= int(i) < dim10 and 0 <= int(j) < dim10 for i, j in pairs10)
    sorted_unique_indices10 = indices10 == sorted(set(indices10))
    sorted_pairs10 = pairs10 == sorted(pairs10)

    chk_rule_defined_ok10 = bool(rule_id10 and rule_text10 and len(pairs10) > 0 and in_bounds_indices10 and in_bounds_pairs10)
    chk_deterministic_ok10 = bool(
        sorted_unique_indices10
        and sorted_pairs10
        and isinstance(selection_hash10, str)
        and selection_hash10 == hashlib.sha256(canonical_selected10.encode("utf-8")).hexdigest()
    )
    chk_signs_ok10 = bool(
        (not task10_missing_deps)
        and inv_kind == "INVERSE_POSITIVITY_CERT"
        and inv_entrywise_nonnegative is True
        and all(e.get("sign") == "+" and e.get("source") == "INVERSE_POSITIVITY_CERT" for e in selected_entries10)
    )

    task10_checks: list[dict[str, Any]] = []
    task10_checks.append(
        _mk_check(
            id="CHK.C10.SELECTION.RULE_DEFINED",
            ok=chk_rule_defined_ok10,
            details={
                "rule_id": rule_id10,
                "dimension": dim10,
                "selected_indices_count": int(len(indices10)),
                "selected_pairs_count": int(len(pairs10)),
                "in_bounds": {"indices": in_bounds_indices10, "pairs": in_bounds_pairs10},
            },
        )
    )
    task10_checks.append(
        _mk_check(
            id="CHK.C10.SELECTION.DETERMINISTIC",
            ok=chk_deterministic_ok10,
            details={
                "ordering": "sorted_lexicographic",
                "selection_hash": selection_hash10,
                "sorted_unique_indices": sorted_unique_indices10,
                "sorted_pairs": sorted_pairs10,
            },
        )
    )
    task10_checks.append(
        _mk_check(
            id="CHK.C10.SELECTED_SIGNS.CERTIFIED",
            ok=chk_signs_ok10,
            details={
                "inverse_sign_source_kind": inv_kind,
                "entrywise_nonnegative": inv_entrywise_nonnegative,
                "notes": inv_notes,
                "dependency_guard": {"missing_deps": task10_missing_deps, **task10_missing_details},
            },
        )
    )

    task10_ok = _task10_all_required_pass(task10_checks)

    selected_payload10: dict[str, Any] = {
        "schema_version": "C-TASK10.v2",
        "run_id": run_dir.name,
        "generated_utc": created_at,
        "sources": {
            "HESSIAN_BLOCKS": out_blocks.name,
            "INVERSE_SIGN_SOURCE": inv_source_path.name if inv_source_path is not None else "",
        },
        "dimension": dim10,
        "inverse_sign_source": {
            "kind": inv_kind,
            "entrywise_nonnegative": inv_entrywise_nonnegative,
            "notes": inv_notes,
        },
        "selection": {
            "rule_id": rule_id10,
            "rule_text": rule_text10,
            "basis": {"type": "pairs", "description": "Diagonal (i,i) pairs for all i in [0,dimension-1]."},
            "selected": selected_obj10,
        },
        "selected_signs": {
            "convention": "sign(C^{-1})",
            "entries": selected_entries10,
        },
        "witnesses": {
            "selection_hash": selection_hash10,
            "ordering": "sorted_lexicographic",
        },
        "checks": task10_checks,
        "status": "PASS" if task10_ok else "FAIL",
    }

    write_json(out_sel_inv, selected_payload10)

    out_task10_report = run_dir / "PhaseC_TASK10_SELECTED_INVERSE_ENTRIES_REPORT.md"
    out_task10_report.write_text(
        "\n".join(
            [
                "# Phase C — Task 10 Report — Selected Inverse Entries and Phase D Interface (FINAL)",
                "",
                f"Run ID: {run_dir.name}",
                f"Date (UTC): {created_at}",
                "Generated by: `nps.phases.phase_c.build_casc` (Taskpack 10)",
                "",
                "---",
                "",
                "## 1) Inputs (authoritative)",
                "",
                f"Run root: `cert_artifacts/{run_dir.name}/`",
                "",
                "Inputs used:",
                "- `HESSIAN_BLOCKS.json`",
                "- inverse-sign source:",
                f"  - `{inv_source_path.name if inv_source_path is not None else ''}`",
                "",
                "---",
                "",
                "## 2) Outputs produced",
                "",
                "- `SELECTED_INVERSE_ENTRIES.json` (schema_version: C-TASK10.v2)",
                "- `PhaseC_TASK10_SELECTED_INVERSE_ENTRIES_REPORT.md` (this file)",
                "",
                "---",
                "",
                "## 3) Selection rule",
                "",
                f"- rule_id: {rule_id10}",
                f"- rule_text: {rule_text10}",
                f"- selected indices count: {len(indices10)}",
                f"- selected pairs count: {len(pairs10)}",
                "",
                "---",
                "",
                "## 5) Verification checklist",
                "",
                "| check_id | result |",
                "|---|---|",
                *[f"| {chk['id']} | {chk.get('status','FAIL')} |" for chk in task10_checks],
                "",
                "---",
                "",
                f"Task 10 status: **{'DONE' if task10_ok else 'BLOCKED'}**",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    out_task3_report = run_dir / "PhaseC_TASK3_HESSIAN_ARTIFACTS_REPORT.md"
    out_task3_report.write_text(
        "\n".join(
            [
                "# Phase C — Task 3 Report — Hessian Computation Artefacts",
                "",
                f"Run ID: {run_dir.name}",
                f"Date (UTC): {created_at}",
                "Generated by: nps.phases.phase_c.build_casc (Taskpack 3 step)",
                "",
                "Artifacts written (run root):",
                f"- HESSIAN_MATRIX.json: {out_hessian.name}",
                f"- PhaseC_TASK3_HESSIAN_ARTIFACTS_REPORT.md: {out_task3_report.name}",
                "",
                "---",
                "",
                "## 1) Inputs (authoritative)",
                "",
                f"Run root: `cert_artifacts/{run_dir.name}/`",
                "",
                "Inputs used:",
                f"- OPERATOR_LAYER.json: {'present' if operator_layer_available else 'not present (not required, but recommended)'}",
                "- CAS-A.json",
                "- CAS-B.json",
                "- PhaseC_ENTRY_REPORT.md",
                "",
                "---",
                "",
                "## 2) Outputs produced",
                "",
                "- HESSIAN_MATRIX.json includes: schema_version, sources, structural_basis, checks, and the matrix.",
                "",
                "---",
                "",
                "## 3) Verification checklist (Task 3)",
                "",
                "| check_id | result | notes |",
                "|---|---|---|",
                *[
                    f"| {chk['id']} | {chk.get('status','FAIL')} | {json.dumps(chk.get('details', {}), sort_keys=True)} |"
                    for chk in task3_checks
                ],
                "",
                "---",
                "",
                "## 5) Decision",
                "",
                f"Task 3 status: {'DONE' if task3_ok else 'BLOCKED'}",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

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

    return out_casc, out_report, [
        out_operator_layer,
        out_operator_report,
        out_theta_family,
        out_hwtheta,
        out_task2_report,
        out_hessian,
        out_task3_report,
        out_blocks,
        out_task4_report,
        out_sparsity,
        out_task5_report,
        out_ddom,
        out_task6_report,
        out_cmp,
        out_task7_report,
        out_neumann,
        out_task8_report,
        out_m_matrix,
        out_inv_pos,
        out_task9_report,
        out_sel_inv,
        out_task10_report,
        out_inv,
        out_exposure,
    ]


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
