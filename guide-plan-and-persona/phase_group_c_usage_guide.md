# Phase Group C — Repo Usage Guide (for ChatGPT / Cascade taskpack conversations)

This repository is a **formal certification pipeline** for mathematical artefacts in the NPS programme.

The practical workflow is:
- Run Phase Group A/B builders to produce a single canonical CAS chain under `cert_artifacts/<run_id>/`.
- Use the **Phase C entry gate** to decide whether Phase Group C work is permitted (strict concavity certified) or quarantined (hyperbolic-only regime).

This document is written to be **copy/paste friendly** for coordinating work in ChatGPT while building new Cascade taskpacks for Phase Group C.

---

## 1) Quick start

### Prerequisites
- Python available locally.
- Run commands from the repository root.

Most examples below use:

```bash
PYTHONPATH=src python -m <module> [args...]
```

### Choose a run id
A run writes to `cert_artifacts/<run_id>/`.

```bash
RUN=2026-03-04T235900Z
```

If you omit `--run-id`, the code will generate a UTC timestamp run id automatically.

---

## 2) Repo structure (what matters for Phase Group C)

- `src/nps/phases/`
  - Phase modules that build CAS artefacts (0A, A, A′, 0B, B, B′, etc.).
- `src/nps/audit/`
  - Governance gates and entry gates.
  - Phase C entry gate lives at `nps.audit.phase_c_entry_gate`.
- `src/nps/models/`
  - Mathematical model specs (e.g. Real Φ v0).
  - `SignedObjective` wrapper used to lock conventions for Φ vs −Φ.
- `cert_artifacts/`
  - Run outputs; each run is isolated by run id.

---

## 3) CAS artefacts and run directory hygiene

### Canonical chain invariant
For a **certifying run**, there should be exactly one canonical chain in the run root:

- `CAS-0A.json`
- `CAS-A.json`
- `CAS-Ap.json`
- `CAS-0B.json`
- `CAS-B.json`
- `CAS-Bp.json`

Plus reports like `PhaseA_REPORT.md`, `PhaseB_REPORT.md`, etc.

### Experiments / variants
If you need multiple Phase B outputs (different objectives, regimes, diagnostics), **do not** write variants into the run root.

Variants should go under:

- `cert_artifacts/<run_id>/experiments/`

Phase B supports this via:
- `--output-suffix <name>`
- `--write-to-experiments`

This avoids ambiguous states like `CAS-B.json` and `CAS-B_phi.json` co-existing in the run root.

### Optional integrity enforcement (recommended for Phase Group C)
There is an env-gated integrity checker that blocks Phase B′ approval if the run root contains ambiguous CAS variants.

Enable it with:

```bash
export NPS_RUN_DIR_INTEGRITY=1
```

---

## 4) Governance gates (recommended settings)

The repo supports opt-in governance gates via environment variables.

A common “cert-like” configuration is:

```bash
export NPS_IMPORT_FIREWALL=1
export NPS_CAS_GATE=1
export NPS_CERT_DEP_GATE=1
export NPS_RUN_DIR_INTEGRITY=1
```

These gates are designed to:
- enforce import discipline
- enforce CAS schema / artefact requirements
- enforce dependency integrity
- enforce run directory hygiene

---

## 5) Phase Group B run (0A → A → A′ → 0B → B → B′)

### 5.1 Phase 0A

```bash
PYTHONPATH=src python -m nps.phases.phase_0a.build_cas0a --run-id "$RUN"
```

Writes `cert_artifacts/$RUN/CAS-0A.json`.

### 5.2 Phase A (CAS-A)

There are multiple Phase A modes. Two common ones:

#### Toy quadratic (sanity)

```bash
PYTHONPATH=src python -m nps.phases.phase_a.build_casa \
  --toy-quadratic \
  --run-id "$RUN" \
  --input "cert_artifacts/$RUN/CAS-0A.json"
```

#### Real Φ v0 (math development)

`--certified-objective` is the convention lock:
- `phi` means certify Φ
- `minus-phi` means certify −Φ (sign-flipped objective with sign-consistent grad/Hess)

```bash
PYTHONPATH=src python -m nps.phases.phase_a.build_casa \
  --real-phi-v0 \
  --certified-objective minus-phi \
  --run-id "$RUN" \
  --input "cert_artifacts/$RUN/CAS-0A.json"
```

Writes `cert_artifacts/$RUN/CAS-A.json`.

### 5.3 Phase A′ (CAS-Ap approval)

```bash
PYTHONPATH=src python -m nps.phases.phase_a_prime.build_casa_prime \
  --run-id "$RUN" \
  --input "cert_artifacts/$RUN/CAS-A.json"
```

Writes `cert_artifacts/$RUN/CAS-Ap.json`.

### 5.4 Phase 0B

```bash
PYTHONPATH=src python -m nps.phases.phase_0b.build_cas0b \
  --run-id "$RUN" \
  --input "cert_artifacts/$RUN/CAS-A.json"
```

Writes `cert_artifacts/$RUN/CAS-0B.json`.

### 5.5 Phase B (CAS-B equilibrium selection)

Two key concepts for Phase Group C readiness:
- `--regime` selects which stationary points are admissible.
  - `strict-concave` corresponds to negative definite Hessian (interior strict concave maximiser regime).
  - `hyperbolic` corresponds to saddle/hyperbolic stationary points.
- `--certified-objective` locks whether you are solving for Φ vs −Φ.

Example (Real Φ v0, strict concave, −Φ convention):

```bash
PYTHONPATH=src python -m nps.phases.phase_b.build_casb \
  --real-phi-v0 \
  --objective maximize \
  --certified-objective minus-phi \
  --candidate-method stationary-multistart \
  --regime strict-concave \
  --run-id "$RUN" \
  --input "cert_artifacts/$RUN/CAS-0B.json"
```

Writes canonical `cert_artifacts/$RUN/CAS-B.json`.

#### Writing diagnostic variants safely

```bash
PYTHONPATH=src python -m nps.phases.phase_b.build_casb \
  --real-phi-v0 \
  --objective maximize \
  --certified-objective phi \
  --candidate-method stationary-multistart \
  --regime hyperbolic \
  --output-suffix phi_hyperbolic \
  --write-to-experiments \
  --run-id "$RUN" \
  --input "cert_artifacts/$RUN/CAS-0B.json"
```

This writes into `cert_artifacts/$RUN/experiments/` and keeps the run root unambiguous.

### 5.6 Phase B′ (CAS-Bp approval)

```bash
PYTHONPATH=src python -m nps.phases.phase_b_prime.build_casb_prime \
  --run-id "$RUN" \
  --input "cert_artifacts/$RUN/CAS-B.json"
```

Writes `cert_artifacts/$RUN/CAS-Bp.json`.

If `NPS_RUN_DIR_INTEGRITY=1` is set, Phase B′ will block approval when the run root contains ambiguous CAS variants.

---

## 6) Phase C entry gate (the Phase Group C blocker)

The Phase C entry gate enforces:
- `CAS-B.json` exists
- `CAS-Bp.json` exists
- equilibrium regime is **not** hyperbolic-only
- equilibrium is `maximize` under `strict_concave`
- Phase A checks certify strict concavity prerequisites:
  - `CHK.A.STATIONARITY` ok
  - `CHK.A.NEG_DEF_HESSIAN` ok

You can run it directly:

```bash
PYTHONPATH=src python -c "from pathlib import Path; from nps.audit.phase_c_entry_gate import validate_phase_c_entry; validate_phase_c_entry(Path('cert_artifacts')/'$RUN')"
```

If it raises, Phase Group C should be treated as **blocked/quarantined** for that run.

---

## 7) “Decisive experiment” pattern (Φ vs −Φ)

For Real Φ v0, the standard investigation pattern is:
- Run Phase A/B under `--certified-objective phi`.
- Run Phase A/B under `--certified-objective minus-phi`.
- Compare whether either configuration yields an **interior strict concave maximiser** that satisfies the Phase C gate.

Practical note:
- If Φ does not admit a strict concave maximiser but −Φ does, Phase Group C work should proceed only under the certified −Φ convention.

---

## 8) Testing / verification

Local unit tests:

```bash
pytest -q
```

With governance gates:

```bash
NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 NPS_RUN_DIR_INTEGRITY=1 pytest -q
```

---

## 9) What to include when pasting into ChatGPT (recommended checklist)

When starting a Phase Group C taskpack conversation, include:
- The exact `RUN=<run_id>` you’re targeting.
- Whether you are certifying `phi` or `minus-phi`.
- The Phase B settings you used:
  - `objective` (maximize/minimize)
  - `candidate_method`
  - `regime` (strict-concave/hyperbolic)
- Whether governance env gates were enabled.
- Whether Phase C entry gate passed.

---

## 10) Common failure modes (and what to do)

- Phase C gate fails due to regime/objective mismatch:
  - Re-run Phase B with `--objective maximize --regime strict-concave`.
- Phase C gate fails due to missing strict concavity prerequisites:
  - Re-run Phase A under the correct `--certified-objective` and confirm `CHK.A.NEG_DEF_HESSIAN` is ok.
- Phase B′ blocks due to run directory integrity:
  - Move variants into `cert_artifacts/<run_id>/experiments/` and keep only canonical artefacts in the run root.
