from __future__ import annotations


def run_self_check() -> None:
    from .build_cas0c import _get_casa_certified_objective

    casa_new = {"derivative_definition": {"certified_objective": "minus_phi"}}

    casa_old = {"certified_objective": "minus_phi"}

    assert _get_casa_certified_objective(casa_new) == "minus_phi"
    assert _get_casa_certified_objective(casa_old) == "minus_phi"

    print("Phase 0C schema compatibility self-check PASSED")


if __name__ == "__main__":
    run_self_check()
