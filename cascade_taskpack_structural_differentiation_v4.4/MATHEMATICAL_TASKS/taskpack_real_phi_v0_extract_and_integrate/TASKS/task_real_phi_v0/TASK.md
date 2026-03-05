# Task Pack — Real Φ v0: Extract → Encode → Run Phase Group B (0B → B → B′)

This task pack turns your uploaded draft papers into a canonical **Real Φ v0** and integrates it into the existing Phase A/B pipeline **without weakening governance**.

## Goal
1) **Extract** the exact definitions of Φ / exposure / equilibrium (provided in `ARTIFACTS/EXTRACTS_VERBATIM.md`).
2) **Encode** them as a Python model with **analytic** derivatives.
3) **Run** Phase Group B (0B → B → B′) using Real Φ v0 and write a consolidated run report stating what passes/fails and why.

## Non-negotiable rules
- Do not change phase-order import rules.
- Do not weaken any audit gate.
- Any failed mathematical obligation must be recorded as a blocking issue in the run’s phase reports and CAS artefacts (fail-loudly, no silent patching).
- Use the command convention: `PYTHONPATH=src python -m ...`

## Deliverables

### 1) Spec + extracts (documentation)
Add:
- `docs/specs/real_phi_v0/EXTRACTS_VERBATIM.md`
- `docs/specs/real_phi_v0/REAL_PHI_V0_SPEC.md`

Copy them from this task pack’s `ARTIFACTS/` directory.

### 2) Model implementation
Add:
- `src/nps/models/real_phi_v0.py`

It must implement:
- `RealPhiV0Spec` dataclass (graph, parameters θ_A, θ_M, θ_R, exponent p, etc.)
- `value(w)`, `grad(w)`, `hess(w)` with **analytic** derivatives
- helper functions implementing:
  - A_i(w), M_i(w), R_i(w)
  - B_e(G) brokerage index via f(kappa)
  - R_e(G,w) edge-level redundancy index (triangle participation)

Canonical v0 choice:
- f(kappa) := 1 / (1 + kappa)  (strictly decreasing N→R_+)

Record in the model:
- `extension_id = "real_phi_v0"`

### 3) Wire into Phase A / Phase B generators
Update:
- `src/nps/phases/phase_a/build_casa.py`
- `src/nps/phases/phase_b/build_casb.py`

Add CLI flag:
- `--real-phi-v0`

When enabled:
- construct a small test graph (m ≤ 12) deterministically
- run the same checks used for the toy quadratic harness
- embed check results into CAS artefacts under `checks: [...]`
- set `derivative_definition.extension_id = "real_phi_v0"`

### 4) Closure behaviour (no weakening)
Confirm A′ and B′:
- block approval if any CHK.A.* or CHK.B.* check fails (when checks are present)
- include blocking issues in the phase reports and CAS-*p artefacts

### 5) Tests
Add tests that verify:
- model shapes + finiteness
- `--real-phi-v0` produces CAS artefacts with extension_id
- checks are recorded (pass/fail is acceptable for v0, but failures must include witnesses and create blocking issues)

## Required run + reporting
Create one persistent run in `cert_artifacts/<run_id>/` and write:

- `RealPhiV0_PhaseGroupB_RUN_REPORT.md`

It must include:
- run_id and file paths
- pass/fail status for each check
- witness payloads for failures
- any SPEC_V0_CHOICE notes

## Acceptance criteria
- Real Φ v0 model exists and is wired via `--real-phi-v0`.
- CAS artefacts include `extension_id="real_phi_v0"`.
- No governance weakening.
- `pytest -q` passes.
- Gates-on mode passes:
  - `NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q`
