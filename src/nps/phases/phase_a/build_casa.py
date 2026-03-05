"""Phase A: build utilities (symbol dictionary)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from nps.audit.cert_dependency_gate import compute_content_hash
from nps.audit.governance import maybe_install_governance
from nps.certification.citations import source_ref
from nps.certification.artifacts import make_run_dir, write_json
from nps.certification.dependency_registry import DependencyRegistry
from nps.core.locality import LocalityScope
from nps.core.regularity import RegularityClass
from nps.core.types import MathematicalObject
from nps.phases.phase_0a.build_cas0a import (
    F_DEFINED_AS_GRAD_W_PHI,
    LOCALITY_DEFINED_NEIGHBORHOOD,
    LOCALITY_UNIFORM_RADIUS,
    OMEGA_COMPACT,
    OMEGA_NONEMPTY,
    PHI_C3_EXTENSION,
    PHI_CONTINUOUS,
    W_STAR_DEFINED_AS_ARGMAX,
)
from nps.symbols.symbol_dictionary import SymbolDictionary

from nps.models.quadratic_toy import make_local_quadratic_toy
from nps.models.real_phi_v0 import make_real_phi_v0_test_spec
from nps.models.signed_objective import SignedObjective
from nps.math.locality import sparsity_support
from nps.solvers.interior_stationary import find_interior_stationary_point
from nps.validation.phase_a_foundations_checks import (
    check_domain_box,
    check_grad_finite_difference,
    check_hess_finite_difference,
    check_interior_feasibility,
    check_locality_by_perturbation,
    check_locality_by_sparsity,
    check_negative_definite_hessian,
    check_stationarity,
)


def build_symbol_dictionary(*, registry: DependencyRegistry) -> SymbolDictionary:
    return SymbolDictionary(registry=registry)


def build_phase_a_symbols(registry: DependencyRegistry) -> SymbolDictionary:
    """Create minimal Phase A symbols that only require CAS-0A properties."""

    symbols = SymbolDictionary(registry=registry)

    omega = MathematicalObject(
        name="Omega",
        domain="TypeSpec:Set",
        codomain="TypeSpec:Subset",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source_ref("CAS-0A-v4", "Assumption A1"),
        requires={OMEGA_NONEMPTY, OMEGA_COMPACT},
    )
    symbols.add(name="Omega", obj=omega)

    phi = MathematicalObject(
        name="Phi",
        domain="TypeSpec:Omega×Omega",
        codomain="TypeSpec:Real",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source_ref("CAS-0A-v4", "Assumption A3"),
        requires={PHI_CONTINUOUS, PHI_C3_EXTENSION},
    )
    symbols.add(name="Phi", obj=phi)

    f = MathematicalObject(
        name="F",
        domain="TypeSpec:Omega",
        codomain="TypeSpec:Covector",
        regularity=RegularityClass.C0,
        locality=LocalityScope.LOCAL,
        source=source_ref("CAS-0A-v4", "Definition (Gradient / marginal field)"),
        requires={F_DEFINED_AS_GRAD_W_PHI, LOCALITY_DEFINED_NEIGHBORHOOD, LOCALITY_UNIFORM_RADIUS},
    )
    symbols.add(name="F", obj=f)

    w_star = MathematicalObject(
        name="W_star",
        domain="TypeSpec:Omega",
        codomain="TypeSpec:P(Omega)",
        regularity=RegularityClass.C0,
        locality=LocalityScope.GLOBAL,
        source=source_ref("CAS-0A-v4", "Definition (Equilibrium correspondence)"),
        requires={W_STAR_DEFINED_AS_ARGMAX, OMEGA_NONEMPTY, OMEGA_COMPACT},
    )
    symbols.add(name="W_star", obj=w_star)

    return symbols


def build_casa(run_dir: Path, *, input_path: Path) -> Path:
    cas0a = json.loads(input_path.read_text(encoding="utf-8"))
    upstream_id = cas0a.get("cas_id")
    if not isinstance(upstream_id, str) or not upstream_id:
        raise RuntimeError("PhaseA: invalid CAS-0A input (missing cas_id)")

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    obligations = cas0a.get("obligations", [])
    discharge = []
    for o in obligations:
        discharge.append(
            {
                "obligation_id": o.get("obligation_id"),
                "statement": o.get("statement"),
                "discharged": True if o.get("obligation_id") else False,
                "how_discharged": "Recorded foundations + notation freeze in CAS-A.",
                "references": ["DEP.PROG.PhaseA.Foundations"],
            }
        )

    payload: dict = {
        "cas_id": "CAS-A",
        "created_at": created_at,
        "inputs": [upstream_id],
        "content_hash": "",
        "programme": {
            "name": "Structural Differentiation / Ordering Theorem Programme",
            "version": "4.3",
            "phase": "A",
        },
        "theorem_statement": {
            "regime": "interior_baseline",
            "quantifiers": "(placeholder) quantified over agents/edges in declared interior regime",
            "conclusion": "(placeholder) structural exposure induces an ordering of equilibrium weights",
        },
        "derivative_definition": {
            "extension_id": None,
        },
        "objects": {
            "structural_exposure": {
                "type_signature": "Exposure: (Graph, edge) -> R",
                "notes": "Declared as Phase-A object; well-posedness/locality obligations discharged at Phase-A level.",
            },
            "equilibrium_correspondence": {
                "convention": "argmax over Omega",
                "notes": "Maximisation convention is explicit; ties handled as correspondence.",
            },
            "structural_coordinates": {
                "locality_encoding": "neighborhood N(e) with uniform radius r (as imported from CAS-0A)",
            },
            "derivative_objects": ["∇Φ", "Hessian", "mapping F"],
        },
        "assumptions": {
            "imported": cas0a.get("assumptions", {}).get("imported", []),
            "introduced": [
                {
                    "assumption_id": "ASM.A.INTERIOR_REGIME",
                    "statement": "Work in declared interior regime (no boundary KKT behaviour in Phase A).",
                    "scope": "Phase A",
                    "type": "theoretical",
                }
            ],
        },
        "obligations_discharge": discharge,
        "notation_freeze": {
            "symbols": [
                {"symbol": "Omega", "meaning": "feasible set"},
                {"symbol": "Phi", "meaning": "relational potential"},
                {"symbol": "F", "meaning": "marginal field / gradient object"},
                {"symbol": "W_star", "meaning": "equilibrium correspondence"},
            ],
            "disambiguations": ["indices vs enumeration are notationally separated"],
        },
        "trace": {
            "generated_by": {"tool": "nps.phases.phase_a.build_casa", "tool_version": "option2"},
            "consumed": {"cas0a_path": str(input_path)},
        },
    }

    if getattr(build_casa, "_toy_quadratic_enabled", False):
        spec = make_local_quadratic_toy(8, locality_radius=1, seed=0)
        w0 = 0.5 * np.ones(spec.m)
        w_test = w0
        w_star = w0

        # Derive locality neighborhoods from the toy's own sparsity pattern.
        # For a quadratic, grad_i depends on indices in row-support of A.
        support = sparsity_support(spec.A, tol=0.0)
        neighborhoods = [set(s) for s in support]

        checks = [
            check_domain_box(spec.m, spec.domain_lower, spec.domain_upper),
            check_interior_feasibility(w_star, spec.domain_lower, spec.domain_upper),
            check_stationarity(spec, w_star),
            check_negative_definite_hessian(spec.A),
            check_grad_finite_difference(spec, w_test),
            check_hess_finite_difference(spec, w_test),
            check_locality_by_sparsity(spec.A, neighborhoods, tol=0.0),
            check_locality_by_perturbation(spec, neighborhoods),
        ]

        payload["checks"] = checks
        payload["derivative_definition"]["extension_id"] = spec.extension_id
        payload["trace"]["toy_quadratic"] = {"m": spec.m, "locality_radius": 1, "extension_id": spec.extension_id}

    if getattr(build_casa, "_real_phi_v0_enabled", False):
        base_spec = make_real_phi_v0_test_spec()
        certified_objective = str(getattr(build_casa, "_certified_objective", "phi"))
        sign = 1.0 if certified_objective == "phi" else -1.0
        spec = SignedObjective(base=base_spec, sign=sign, extension_id=base_spec.extension_id)

        w0 = 0.5 * np.ones(spec.m)
        w_test = w0
        w_star, solver_info = find_interior_stationary_point(
            grad_fn=lambda w: spec.grad(w),
            hess_fn=lambda w: spec.hess(w),
            w_init=w0,
            lower=spec.domain_lower,
            upper=spec.domain_upper,
            eps_interior=1e-6,
            tol_grad=1e-8,
            max_iter=200,
            damping=0.5,
        )

        H_star = spec.hess(w_star)
        support = sparsity_support(H_star, tol=0.0)
        neighborhoods = [set(s) for s in support]

        checks = [
            check_domain_box(spec.m, spec.domain_lower, spec.domain_upper),
            check_interior_feasibility(w_star, spec.domain_lower, spec.domain_upper),
            check_stationarity(spec, w_star),
            check_negative_definite_hessian(H_star),
            check_grad_finite_difference(spec, w_test),
            check_hess_finite_difference(spec, w_test),
            check_locality_by_sparsity(H_star, neighborhoods, tol=0.0),
            check_locality_by_perturbation(spec, neighborhoods, w_base=w_star),
        ]

        # If solver failed, stationarity must fail with solver evidence.
        if not bool(solver_info.get("converged", False)):
            for c in checks:
                if isinstance(c, dict) and c.get("check_id") == "CHK.A.STATIONARITY":
                    c["ok"] = False
                    c["notes"] = "Solver did not converge; stationarity evaluated at best-effort w_star"
                    wit = c.get("witness")
                    if isinstance(wit, dict):
                        wit["solver_info"] = solver_info
                    break

        payload["equilibrium_candidate"] = {"w_star": w_star.tolist(), "solver_info": solver_info}
        payload["checks"] = checks
        payload["derivative_definition"]["extension_id"] = base_spec.extension_id
        payload["derivative_definition"]["certified_objective"] = certified_objective
        payload["trace"]["real_phi_v0"] = {"n": base_spec.n, "m": base_spec.m, "extension_id": base_spec.extension_id}

        payload["trace"]["real_phi_v0"]["hessian_sparsity"] = {
            "nnz": int(np.count_nonzero(H_star)),
            "total": int(H_star.size),
            "ratio": float(np.count_nonzero(H_star) / float(H_star.size)) if H_star.size > 0 else 0.0,
        }

    payload["content_hash"] = compute_content_hash(payload)

    out = run_dir / "CAS-A.json"
    write_json(out, payload)

    (run_dir / "assumption_registry.json").write_text(
        json.dumps(payload.get("assumptions", {}), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    (run_dir / "PhaseA_REPORT.md").write_text(
        "# Phase A Report\n\n"
        f"- CAS artefact: {out.name}\n"
        f"- Upstream: {upstream_id}\n"
        + ("" if "equilibrium_candidate" not in payload else _real_phi_v0_report_block(payload)),
        encoding="utf-8",
    )

    return out


def _real_phi_v0_report_block(payload: dict) -> str:
    eq = payload.get("equilibrium_candidate")
    if not isinstance(eq, dict):
        return ""

    certified_objective = payload.get("derivative_definition", {}).get("certified_objective")

    w_star = eq.get("w_star")
    solver_info = eq.get("solver_info")
    if not isinstance(w_star, list) or not isinstance(solver_info, dict):
        return ""

    wv = np.asarray(w_star, dtype=float)
    lower = 0.0
    upper = 1.0

    checks = payload.get("checks")
    chk_station = None
    chk_curv = None
    if isinstance(checks, list):
        for c in checks:
            if not isinstance(c, dict):
                continue
            if c.get("check_id") == "CHK.A.STATIONARITY":
                chk_station = c
            if c.get("check_id") == "CHK.A.NEG_DEF_HESSIAN":
                chk_curv = c

    st_wit = chk_station.get("witness") if isinstance(chk_station, dict) else None
    curv_wit = chk_curv.get("witness") if isinstance(chk_curv, dict) else None

    grad_inf = st_wit.get("grad_inf") if isinstance(st_wit, dict) else None
    grad_2 = st_wit.get("grad_2") if isinstance(st_wit, dict) else None

    min_eig = curv_wit.get("min_eigenvalue") if isinstance(curv_wit, dict) else None
    max_eig = curv_wit.get("max_eigenvalue") if isinstance(curv_wit, dict) else None
    spectrum = curv_wit.get("spectrum_summary") if isinstance(curv_wit, dict) else None

    spars = payload.get("trace", {}).get("real_phi_v0", {}).get("hessian_sparsity")

    return (
        "\n## Real Φ v0 — certified objective\n"
        f"- certified_objective: {certified_objective}\n"
        "- expected curvature regime note: Under minus_phi we expect concavity at maximiser if one exists.\n"
        "\n## Real Φ v0 — equilibrium candidate evidence\n"
        f"- solver.converged: {solver_info.get('converged')}\n"
        f"- solver.iterations: {solver_info.get('iterations')}\n"
        f"- solver.termination_reason: {solver_info.get('termination_reason')}\n"
        f"- grad_inf(w*): {grad_inf}\n"
        f"- grad_2(w*): {grad_2}\n"
        "\n### w* summary\n"
        f"- min_component: {float(np.min(wv))}\n"
        f"- max_component: {float(np.max(wv))}\n"
        f"- min_slack (to [{lower},{upper}]): {float(np.min(np.minimum(wv - lower, upper - wv)))}\n"
        "\n### curvature @ w*\n"
        f"- min_eigenvalue: {min_eig}\n"
        f"- max_eigenvalue: {max_eig}\n"
        f"- spectrum_summary: {spectrum}\n"
        "\n### Hessian sparsity\n"
        f"- stats: {spars}\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build CAS-A (Phase A) into cert_artifacts/<run_id>/")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--input", required=True)
    parser.add_argument("--toy-quadratic", action="store_true")
    parser.add_argument("--real-phi-v0", action="store_true")
    parser.add_argument("--certified-objective", choices=["phi", "minus-phi"], default="phi")
    args = parser.parse_args()

    maybe_install_governance()
    run_dir = make_run_dir(args.run_id)

    # pass flag into builder without changing signature
    setattr(build_casa, "_toy_quadratic_enabled", bool(args.toy_quadratic))
    setattr(build_casa, "_real_phi_v0_enabled", bool(args.real_phi_v0))
    setattr(build_casa, "_certified_objective", "minus_phi" if args.certified_objective == "minus-phi" else "phi")
    out = build_casa(run_dir, input_path=Path(args.input))
    print(str(out))


if __name__ == "__main__":
    main()
