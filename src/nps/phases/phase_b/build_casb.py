"""Phase B: operator formulation and checkers."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from nps.audit.cert_dependency_gate import compute_content_hash
from nps.audit.governance import maybe_install_governance
from nps.certification.artifacts import get_experiments_dir, make_run_dir, write_json
from nps.math.locality import sparsity_support
from nps.models.signed_objective import SignedObjective
from nps.models.quadratic_toy import make_local_quadratic_toy
from nps.models.real_phi_v0 import make_real_phi_v0_test_spec
from nps.operators.equilibrium_operator import OperatorSpec, equilibrium_operator_from_potential, jacobian_from_potential
from nps.solvers.equilibrium_candidates import (
    find_stationary_candidates_multistart,
    generate_deterministic_starts,
    select_candidate_for_regime,
)
from nps.solvers.interior_stationary import find_interior_stationary_point
from nps.solvers.projected_opt import projected_gradient_ascent
from nps.validation.phase_b_operator_checks import (
    check_jacobian_conditioning,
    check_jacobian_invertible_at_wstar,
    check_jacobian_locality_sparsity,
    check_jacobian_matches_hess,
    check_jacobian_symmetry,
    check_operator_matches_grad,
)


def build_casb(run_dir: Path, *, input_path: Path) -> Path:
    cas0b = json.loads(input_path.read_text(encoding="utf-8"))
    upstream_id = cas0b.get("cas_id")
    if not isinstance(upstream_id, str) or not upstream_id:
        raise RuntimeError("PhaseB: invalid CAS-0B input (missing cas_id)")

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    output_suffix = str(getattr(build_casb, "_output_suffix", ""))
    write_to_experiments = bool(getattr(build_casb, "_write_to_experiments", False))

    is_variant = bool(output_suffix) or bool(write_to_experiments)
    suffix = output_suffix.strip("_") if output_suffix else ""
    if is_variant and not suffix:
        suffix = "variant"

    cas_id = "CAS-B" + ("_" + suffix if is_variant else "")

    payload: dict = {
        "cas_id": cas_id,
        "created_at": created_at,
        "inputs": [upstream_id],
        "content_hash": "",
        "programme": {
            "name": "Structural Differentiation / Ordering Theorem Programme",
            "version": "4.3",
            "phase": "B",
        },
        "operator_spec": None,
        "checks": [],
        "trace": {
            "generated_by": {"tool": "nps.phases.phase_b.build_casb", "tool_version": "option2"},
            "consumed": {"cas0b_path": str(input_path)},
        },
    }

    if getattr(build_casb, "_toy_quadratic_enabled", False):
        spec = make_local_quadratic_toy(8, locality_radius=1, seed=0)
        w0 = 0.5 * np.ones(spec.m)

        F = equilibrium_operator_from_potential(spec)
        J = jacobian_from_potential(spec)

        support = sparsity_support(spec.A, tol=0.0)
        neighborhoods = [set(s) for s in support]
        locality = {
            "neighborhoods": [sorted(list(s)) for s in neighborhoods],
            "radius": None,
        }

        op_spec = OperatorSpec(
            name="equilibrium_operator",
            definition="F(w,theta)=∇Φ(w,theta) in interior regime",
            derivative_definition={"extension_id": spec.extension_id},
            locality=locality,
        )

        checks = [
            check_operator_matches_grad(
                grad=lambda w: spec.grad(w),
                F=lambda w: F(w),
                m=spec.m,
                lower=spec.domain_lower,
                upper=spec.domain_upper,
            ),
            check_jacobian_matches_hess(
                hess=lambda w: spec.hess(w),
                J=lambda w: J(w),
                m=spec.m,
                lower=spec.domain_lower,
                upper=spec.domain_upper,
            ),
            check_jacobian_symmetry(J=lambda w: J(w), w=w0),
            check_jacobian_locality_sparsity(J=lambda w: J(w), w=w0, neighborhoods=neighborhoods, tol=0.0),
            check_jacobian_invertible_at_wstar(J=lambda w: J(w), w_star=w0, eps=1e-9),
        ]

        payload["operator_spec"] = {
            "name": op_spec.name,
            "definition": op_spec.definition,
            "derivative_definition": op_spec.derivative_definition,
            "locality": op_spec.locality,
        }
        payload["checks"] = checks
        payload["trace"]["toy_quadratic"] = {"m": spec.m, "extension_id": spec.extension_id}

    if getattr(build_casb, "_real_phi_v0_enabled", False):
        spec = make_real_phi_v0_test_spec()
        w0 = 0.5 * np.ones(spec.m)

        settings = getattr(build_casb, "_real_phi_v0_settings", {})
        objective = settings.get("objective", "maximize")
        regime = settings.get("regime", "hyperbolic")
        certified_objective = settings.get("certified_objective", "phi")
        candidate_method = settings.get("candidate_method", "stationary_multistart")

        sign = 1.0 if certified_objective == "phi" else -1.0
        signed = SignedObjective(
            base=spec,
            sign=sign,
            extension_id=spec.extension_id + ("_minus_phi" if sign < 0.0 else ""),
        )

        candidates: list[dict] = []
        selected: dict | None = None

        if candidate_method == "stationary_multistart":
            starts = generate_deterministic_starts(spec.m)
            candidates = find_stationary_candidates_multistart(
                grad_fn=lambda w: signed.grad(w),
                hess_fn=lambda w: signed.hess(w),
                starts=starts,
                lower=spec.domain_lower,
                upper=spec.domain_upper,
                tol_grad=1e-8,
            )
            selected = select_candidate_for_regime(candidates, objective=objective, regime=regime)
        elif candidate_method == "maximize_projected":
            w_proj, info = projected_gradient_ascent(
                value_fn=lambda w: signed.value(w),
                grad_fn=lambda w: signed.grad(w),
                w_init=w0,
                lower=spec.domain_lower,
                upper=spec.domain_upper,
                step=0.1,
                max_iter=500,
                tol=1e-8,
            )
            g = signed.grad(w_proj)
            g2 = float(np.linalg.norm(g, ord=2))
            ginf = float(np.linalg.norm(g, ord=np.inf))
            H = signed.hess(w_proj)
            Hsym = 0.5 * (H + H.T)
            eigs = np.linalg.eigvalsh(Hsym)
            from nps.solvers.equilibrium_candidates import classify_hessian_spectrum

            candidates = [
                {
                    "start_index": 0,
                    "w": np.asarray(w_proj, dtype=float).tolist(),
                    "solver_info": info,
                    "grad_norm_2": g2,
                    "grad_norm_inf": ginf,
                    "hessian_spectrum": classify_hessian_spectrum(eigs),
                }
            ]
            selected = select_candidate_for_regime(candidates, objective=objective, regime=regime)
        elif candidate_method == "diagnostic_only":
            candidates = []
            selected = None
        else:
            raise RuntimeError(f"PhaseB: unknown candidate method: {candidate_method}")

        w_star = None
        solver_info = None
        if selected is not None and isinstance(selected.get("w"), list):
            w_star = np.asarray(selected.get("w"), dtype=float)
            solver_info = selected.get("solver_info")

        payload["equilibrium_objective"] = str(objective)
        payload["equilibrium_regime"] = str(regime)
        payload["certified_objective"] = signed.certified_objective
        payload["equilibrium_candidate_method"] = (
            "stationary_multistart"
            if candidate_method == "stationary_multistart"
            else "maximize_projected"
            if candidate_method == "maximize_projected"
            else "diagnostic_only"
        )
        payload["equilibrium_candidate_found"] = bool(w_star is not None)
        payload["equilibrium_candidates"] = candidates

        payload["trace"]["real_phi_v0"] = {
            "n": spec.n,
            "m": spec.m,
            "extension_id": signed.extension_id,
            "selection": {
                "objective": objective,
                "regime": regime,
                "certified_objective": signed.certified_objective,
                "candidate_method": candidate_method,
            },
        }

        if w_star is None:
            payload["equilibrium_candidate"] = None
            payload["operator_spec"] = None
            payload["checks"] = []
        else:
            F = equilibrium_operator_from_potential(signed)
            J = jacobian_from_potential(signed)

            H_star = signed.hess(w_star)
            support = sparsity_support(H_star, tol=0.0)
            neighborhoods = [set(s) for s in support]
            locality = {
                "neighborhoods": [sorted(list(s)) for s in neighborhoods],
                "radius": None,
            }

            op_spec = OperatorSpec(
                name="equilibrium_operator",
                definition="F(w,theta)=∇Φ(w,theta) in interior regime",
                derivative_definition={"extension_id": signed.extension_id},
                locality=locality,
            )

            checks = [
                check_operator_matches_grad(
                    grad=lambda w: signed.grad(w),
                    F=lambda w: F(w),
                    m=spec.m,
                    lower=spec.domain_lower,
                    upper=spec.domain_upper,
                ),
                check_jacobian_matches_hess(
                    hess=lambda w: signed.hess(w),
                    J=lambda w: J(w),
                    m=spec.m,
                    lower=spec.domain_lower,
                    upper=spec.domain_upper,
                ),
                check_jacobian_symmetry(J=lambda w: J(w), w=w_star),
                check_jacobian_locality_sparsity(
                    J=lambda w: J(w), w=w_star, neighborhoods=neighborhoods, tol=0.0
                ),
                check_jacobian_invertible_at_wstar(J=lambda w: J(w), w_star=w_star, eps=1e-9),
                check_jacobian_conditioning(
                    J=lambda w: J(w), w_star=w_star, invertible_eps=1e-9, concavity_eps=1e-9
                ),
            ]

            payload["operator_spec"] = {
                "name": op_spec.name,
                "definition": op_spec.definition,
                "derivative_definition": op_spec.derivative_definition,
                "locality": op_spec.locality,
            }
            payload["equilibrium_candidate"] = {"w_star": w_star.tolist(), "solver_info": solver_info}
            payload["checks"] = checks

    payload["content_hash"] = compute_content_hash(payload)

    out_dir = get_experiments_dir(run_dir) if is_variant else run_dir
    out_name = f"{cas_id}.json" if is_variant else "CAS-B.json"
    out = out_dir / out_name
    write_json(out, payload)

    # minimal report
    ok_count = 0
    checks = payload.get("checks")
    if isinstance(checks, list):
        ok_count = sum(1 for c in checks if isinstance(c, dict) and c.get("ok") is True)

    report_dir = out_dir
    report_name = f"PhaseB_REPORT_{suffix}.md" if is_variant else "PhaseB_REPORT.md"
    (report_dir / report_name).write_text(
        "# Phase B Report\n\n"
        f"- CAS artefact: {out.name}\n"
        f"- Upstream: {upstream_id}\n"
        f"- Checks ok: {ok_count}\n"
        + _real_phi_v0_report_block(payload),
        encoding="utf-8",
    )

    return out


def _real_phi_v0_report_block(payload: dict) -> str:
    trace = payload.get("trace")
    if not isinstance(trace, dict) or "real_phi_v0" not in trace:
        return ""

    objective = payload.get("equilibrium_objective")
    regime = payload.get("equilibrium_regime")
    certified_objective = payload.get("certified_objective")
    method = payload.get("equilibrium_candidate_method")
    found = payload.get("equilibrium_candidate_found")

    eq = payload.get("equilibrium_candidate")
    if not isinstance(eq, dict) or not isinstance(eq.get("w_star"), list):
        candidates = payload.get("equilibrium_candidates")
        cand_count = len(candidates) if isinstance(candidates, list) else None
        return (
            "\n## Real Φ v0 — equilibrium regime selection\n"
            f"- equilibrium_objective: {objective}\n"
            f"- equilibrium_regime: {regime}\n"
            f"- certified_objective: {certified_objective}\n"
            f"- equilibrium_candidate_method: {method}\n"
            f"- equilibrium_candidate_found: {found}\n"
            f"- candidates_generated: {cand_count}\n"
        )

    wv = np.asarray(eq.get("w_star"), dtype=float)
    solver_info = eq.get("solver_info") if isinstance(eq.get("solver_info"), dict) else {}

    conditioning = None
    checks = payload.get("checks")
    if isinstance(checks, list):
        for c in checks:
            if isinstance(c, dict) and c.get("check_id") == "CHK.B.JACOBIAN_CONDITIONING":
                conditioning = c.get("witness")

    return (
        "\n## Real Φ v0 — equilibrium candidate evidence\n"
        f"- solver.converged: {solver_info.get('converged')}\n"
        f"- solver.iterations: {solver_info.get('iterations')}\n"
        f"- solver.termination_reason: {solver_info.get('termination_reason')}\n"
        "\n### w* summary\n"
        f"- min_component: {float(np.min(wv))}\n"
        f"- max_component: {float(np.max(wv))}\n"
        "\n### Jacobian conditioning @ w* (CHK.B.JACOBIAN_CONDITIONING witness)\n"
        f"- witness: {conditioning}\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build CAS-B (Phase B) into cert_artifacts/<run_id>/")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--input", required=True)
    parser.add_argument("--toy-quadratic", action="store_true")
    parser.add_argument("--real-phi-v0", action="store_true")
    parser.add_argument("--output-suffix", default="")
    parser.add_argument("--write-to-experiments", action="store_true")
    parser.add_argument("--objective", choices=["maximize", "minimize"], default="maximize")
    parser.add_argument("--certified-objective", choices=["phi", "minus-phi"], default="phi")
    parser.add_argument(
        "--candidate-method",
        choices=["stationary-multistart", "maximize-projected", "diagnostic-only"],
        default="stationary-multistart",
    )
    parser.add_argument("--regime", choices=["strict-concave", "hyperbolic"], default=None)
    args = parser.parse_args()

    maybe_install_governance()
    run_dir = make_run_dir(args.run_id)

    setattr(build_casb, "_toy_quadratic_enabled", bool(args.toy_quadratic))
    setattr(build_casb, "_real_phi_v0_enabled", bool(args.real_phi_v0))
    setattr(build_casb, "_output_suffix", str(args.output_suffix))
    setattr(build_casb, "_write_to_experiments", bool(args.write_to_experiments))

    if bool(args.real_phi_v0):
        regime = args.regime or "hyperbolic"
        settings = {
            "objective": str(args.objective),
            "certified_objective": "phi" if args.certified_objective == "phi" else "minus_phi",
            "candidate_method": (
                "stationary_multistart"
                if args.candidate_method == "stationary-multistart"
                else "maximize_projected"
                if args.candidate_method == "maximize-projected"
                else "diagnostic_only"
            ),
            "regime": "strict_concave" if regime == "strict-concave" else "hyperbolic",
        }
        setattr(build_casb, "_real_phi_v0_settings", settings)
    out = build_casb(run_dir, input_path=Path(args.input))
    print(str(out))


if __name__ == "__main__":
    main()
