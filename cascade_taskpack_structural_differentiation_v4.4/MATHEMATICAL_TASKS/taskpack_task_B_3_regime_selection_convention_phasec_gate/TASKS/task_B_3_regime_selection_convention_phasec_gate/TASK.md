# Task B.3 — Regime‑Respecting Equilibrium Selection + Convention Lock + Phase C Entry Gate

## Why this task exists
Real Φ v0 currently produces an interior stationary point `w*` with **positive definite Hessian** in at least one run.
That means the solver may converge to a **local minimum** even though the programme’s equilibrium meaning is anchored to **local maximisers**.

Before Phase C is allowed to assume curvature sign structure, we must:

1) Make equilibrium candidate selection regime-respecting (seek maxima if claiming maximiser regime).
2) Split and lock conventions in CAS artefacts so they cannot drift.
3) Add a Phase C entry gate that blocks strict-concavity assumptions unless certified.
4) Run a decisive experiment on Real Φ v0 under both Φ and −Φ, and report whether an interior strict concave maximiser exists.

---

## Command convention (authoritative)
All commands executed from repo root using:

```bash
PYTHONPATH=src python -m ...
```

---

## Deliverables summary
### A) Multi-start stationary solver with Hessian screening
Add a deterministic “multi-start” equilibrium candidate selector that:
- runs the existing interior stationary solver from multiple initial points
- classifies each stationary point by Hessian spectrum
- selects a candidate consistent with the declared regime (maximiser vs diagnostic)

### B) Optional projected maximiser mode
Add an option to directly maximise Φ over the box `[0,1]^m` using a projected ascent method.
This is not a proof, but is a regime-aligned candidate finder.

### C) Split CAS-B fields cleanly (no overloaded meaning)
CAS-B must record:
- `equilibrium_objective`: `"maximize"` or `"minimize"`
- `equilibrium_regime`: `"strict_concave"` or `"hyperbolic"`
- `certified_objective`: `"phi"` or `"minus_phi"`
- `equilibrium_candidate_method`: `"stationary_multistart"` | `"maximize_projected"` | `"diagnostic_only"`

### D) Phase C preflight gate (hard block)
Phase C must refuse to proceed unless strict concavity is certified under the maximiser objective.
Hyperbolic-only regime is quarantined and cannot run Phase C (unless you add an explicitly separate Phase C-hyperbolic track later).

### E) One decisive Real Φ v0 report (Φ and −Φ)
Write a report that answers:

- Does an interior strict concave maximiser exist for Real Φ v0 under Φ?
- Does an interior strict concave maximiser exist for Real Φ v0 under −Φ?
- If neither: Phase C strict concavity path is blocked for Real Φ v0.

---

## Required code changes

### 1) Signed objective wrapper (new)
Add:

- `src/nps/models/signed_objective.py`

Provide:

```python
@dataclass(frozen=True)
class SignedObjective:
    base: Any
    sign: float  # +1.0 for phi, -1.0 for minus_phi
    extension_id: str  # e.g. "real_phi_v0" + suffix

    def value(self, w): ...
    def grad(self, w): ...
    def hess(self, w): ...
```

Requirements:
- value/grad/hess must be sign-consistent (no drift).
- Expose `certified_objective` string: `"phi"` if sign=+1, `"minus_phi"` if sign=-1.

### 2) Multi-start stationary candidate selection (new)
Add:

- `src/nps/solvers/equilibrium_candidates.py`

Provide:

```python
def generate_deterministic_starts(m: int) -> list[np.ndarray]:
    """Return a small deterministic set of interior start points in (0,1)^m."""

def find_stationary_candidates_multistart(
    grad_fn,
    hess_fn,
    *,
    starts: list[np.ndarray],
    lower,
    upper,
    tol_grad=1e-8,
) -> list[dict]:
    """Return candidates with w, solver_info, grad norms, Hessian spectrum summary."""

def classify_hessian_spectrum(eigs: np.ndarray, eps=1e-8) -> dict:
    """Return is_neg_def, is_pos_def, is_indef, is_hyperbolic, min/max eig, counts."""

def select_candidate_for_regime(
    candidates: list[dict],
    *,
    objective: str,  # "maximize"|"minimize"
    regime: str,     # "strict_concave"|"hyperbolic"
) -> dict | None:
    """Select best candidate consistent with regime; return None if no match."""
```

Selection logic:
- If objective="maximize" and regime="strict_concave": require negative definite Hessian.
- If objective="minimize" and regime="strict_concave": require positive definite Hessian.
- If regime="hyperbolic": require invertible/hyperbolic (min|eig| > eps).
- Prefer smallest grad norm; tie-break by stronger definiteness margin.

### 3) Optional projected maximiser mode (new)
Add:

- `src/nps/solvers/projected_opt.py`

Provide:

```python
def projected_gradient_ascent(
    value_fn,
    grad_fn,
    *,
    w_init,
    lower,
    upper,
    step=0.1,
    max_iter=500,
    tol=1e-8,
) -> tuple[w, info]
```

Requirements:
- deterministic
- always keeps w in box
- info includes objective trace and termination reason

### 4) Wire into Phase B generation
Update:

- `src/nps/phases/phase_b/build_casb.py`

Add CLI flags (Real Φ v0 mode only):
- `--objective maximize|minimize` (default: maximize)
- `--certified-objective phi|minus-phi` (default: phi)
- `--candidate-method stationary-multistart|maximize-projected|diagnostic-only` (default: stationary-multistart)
- `--regime strict-concave|hyperbolic` (default: hyperbolic for Real Φ until proven)

Behaviour:
- Wrap Real Φ spec in `SignedObjective` according to certified-objective.
- Generate candidates via requested method.
- Select candidate matching objective+regime; if none exists:
  - record a blocking issue in PhaseB_REPORT.md and in CAS-B fields:
    - `equilibrium_candidate_found: false`
    - include candidate table summary
- Evaluate CHK.B checks at the selected candidate w* (if present).
- Record CAS-B fields exactly as specified above.

### 5) Phase C preflight gate (new)
Add:

- `src/nps/audit/phase_c_entry_gate.py`

Provide:

```python
def validate_phase_c_entry(run_dir: Path) -> None:
    """Raise RuntimeError if Phase C is not allowed to proceed."""
```

Rules:
- Load CAS-B and CAS-Bp (same run_dir).
- Require `equilibrium_objective == "maximize"` and `equilibrium_regime == "strict_concave"`.
- Require checks:
  - CHK.A.STATIONARITY ok
  - CHK.A.NEG_DEF_HESSIAN ok
- Otherwise raise audit-grade RuntimeError explaining which prerequisite failed.
- If equilibrium_regime == "hyperbolic": always raise with message “Phase C quarantined under hyperbolic-only regime.”

Add optional env override:
- `NPS_DIAGNOSTIC=1` allows *printing* status but still must not silently run Phase C. (Gate may return a warning object in diagnostic mode, but must still block any actual Phase C generator if present.)

### 6) Decisive experiment report (required)
For a persistent run, write:

- `cert_artifacts/<run_id>/RealPhiV0_B3_Decisive_Regime_Report.md`

This report must include:

- Run metadata (run_id, commit hash if available)
- Two experiment blocks:
  1) Real Φ v0 with certified_objective="phi"
  2) Real Φ v0 with certified_objective="minus_phi"

For each block:
- Candidate method used (multistart and/or projected)
- Number of stationary points found and their classification counts:
  - neg-def / pos-def / indefinite / hyperbolic
- Whether an **interior strict concave maximiser** exists:
  - YES/NO
- If YES: record selected w*, min/max eig, grad norm, slack
- If NO: show best available hyperbolic candidate and explain why strict concavity failed

Conclusion section must state plainly:
- “strict concave maximiser exists” or “does not exist” under Φ and −Φ

---

## Tests (required)
Add:
- `tests/test_multistart_candidate_selection.py`
- `tests/test_signed_objective_wrapper.py`
- `tests/test_phase_c_entry_gate.py`
- `tests/test_phase_b_real_phi_regime_fields.py`

---

## Verification commands (must run)
```bash
pytest -q
NPS_IMPORT_FIREWALL=1 NPS_CAS_GATE=1 NPS_CERT_DEP_GATE=1 pytest -q
```

---

## Required persistent run (must do)
Create a new run directory and generate artefacts.

At minimum:
- Phase A artefacts for Real Φ (so CHK.A.* exist)
- Phase B artefacts with regime fields

Then write:
- `RealPhiV0_B3_Decisive_Regime_Report.md`

---

## Acceptance criteria
DONE when:
- Multi-start candidate selector exists and is used in Phase B.
- SignedObjective wrapper exists and is used to run Φ vs −Φ without drift.
- CAS-B contains split fields (objective, regime, certified objective, candidate method).
- Phase C entry gate exists and blocks unless strict concave maximiser regime is certified.
- Decisive report exists showing whether strict concave maximiser exists for Φ and −Φ.
- Tests pass in both default and gates-on modes.
