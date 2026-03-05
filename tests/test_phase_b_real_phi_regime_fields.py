from __future__ import annotations

import json
from pathlib import Path

from nps.phases.phase_0a.build_cas0a import build_cas0a
from nps.phases.phase_0b.build_cas0b import build_cas0b
from nps.phases.phase_a.build_casa import build_casa
from nps.phases.phase_b.build_casb import build_casb


def test_phase_b_records_regime_fields_for_real_phi(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    try:
        cas0a_path = build_cas0a(run_dir)
        setattr(build_casa, "_real_phi_v0_enabled", True)
        casa_path = build_casa(run_dir, input_path=cas0a_path)
        cas0b_path = build_cas0b(run_dir, input_path=casa_path)

        setattr(build_casb, "_real_phi_v0_enabled", True)
        setattr(
            build_casb,
            "_real_phi_v0_settings",
            {
                "objective": "maximize",
                "regime": "hyperbolic",
                "certified_objective": "phi",
                "candidate_method": "stationary_multistart",
            },
        )

        casb_path = build_casb(run_dir, input_path=cas0b_path)
        casb = json.loads(casb_path.read_text(encoding="utf-8"))

        assert casb.get("equilibrium_objective") == "maximize"
        assert casb.get("equilibrium_regime") == "hyperbolic"
        assert casb.get("certified_objective") in {"phi", "minus_phi"}
        assert casb.get("equilibrium_candidate_method") == "stationary_multistart"
        assert isinstance(casb.get("equilibrium_candidate_found"), bool)
        assert isinstance(casb.get("equilibrium_candidates"), list)
    finally:
        setattr(build_casa, "_real_phi_v0_enabled", False)
        setattr(build_casa, "_toy_quadratic_enabled", False)
        setattr(build_casb, "_real_phi_v0_enabled", False)
        setattr(build_casb, "_toy_quadratic_enabled", False)
        setattr(build_casb, "_output_suffix", "")
