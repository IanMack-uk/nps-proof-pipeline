# Theta Candidate Discovery Report
Date (UTC): 2026-03-05T08:43:59Z
Repo commit SHA: 45f8f5703907f9f98525f24f91c549651644fad5

## Summary
- Candidates found: 6
- Edge-local candidates: 2
- Node-local candidates: 0
- Motif-local candidates: 1
- H_wθ computable today: NO

## Candidate Inventory (table)

| Name (as appears) | Type | Location (path:lines) | How it enters Φ or F | Differentiable in current code | Part of CAS artifacts |
|---|---|---|---|---|---|
| `theta_A` | global scalar | `src/nps/models/real_phi_v0.py:9-16, 120-126, 208-214, 342-345` | Enters Real Φ v0 as coefficient on `log(1 + A_i(w))` in `value/grad/hess` | YES (analytic in model; linear in parameter) | NO (not exported in CAS-A/B/C payloads today; only indirectly via `extension_id`) |
| `theta_M` | global scalar | `src/nps/models/real_phi_v0.py:9-16, 120-126, 209-213, 347-350` | Enters Real Φ v0 as coefficient on `log(1 + M_i(w))` in `value/grad/hess` | YES | NO |
| `theta_R` | global scalar | `src/nps/models/real_phi_v0.py:9-16, 120-126, 210-214, 352-355` | Enters Real Φ v0 as coefficient on `-log(1 + R_i(w))` in `value/grad/hess` | YES | NO |
| `theta` (toy) | global scalar | `src/nps/models/toy/potentials.py:14-26`; used by `src/nps/models/toy/equilibrium.py:27-35` | In toy model, `phi(w,theta)` uses `b = theta * 1`; `grad_phi` depends on `theta` | YES (analytic) | NO (toy harness; not part of Phase B Real Φ CAS chain) |
| `theta` (operator signature) | global scalar / optional | `src/nps/operators/equilibrium_operator.py:17-43` | `F(w,theta)=potential.grad(w,theta)` and `J(w,theta)=potential.hess(w,theta)` define a θ-carrying interface | UNKNOWN (depends on potential implementation; RealPhiV0 ignores theta argument) | INDIRECT (Phase B stores operator definition text, but not θ values) |
| `B_e(G)` / `κ_e(G)` / `R_e(G,w)` | edge-local / motif-local | Spec: `docs/specs/real_phi_v0/REAL_PHI_V0_SPEC.md:11-39`; Code: `src/nps/models/real_phi_v0.py:41-69, 80-100` | Enters Real Φ v0 via brokerage weighting inside `M_i(w)` and via redundancy terms; computed from graph + local triangle structure | YES w.r.t. `w` (for fixed graph); NOT a free parameter in current code (graph fixed) | NO (not separately surfaced in CAS artifacts; only implicit in model spec + `extension_id`) |

## Evidence Snippets

### Real Φ v0 parameters (`theta_A`, `theta_M`, `theta_R`)
```python
@dataclass(frozen=True, slots=True)
class RealPhiV0Spec:
    n: int
    edges: list[tuple[int, int]]
    theta_A: float
    theta_M: float
    theta_R: float
```
(Source: `src/nps/models/real_phi_v0.py:8-15`)

### Φ uses those parameters as linear coefficients
```python
phi += float(self.theta_A * np.log1p(A[i]))
phi += float(self.theta_M * np.log1p(M[i]))
phi -= float(self.theta_R * np.log1p(R[i]))
```
(Source: `src/nps/models/real_phi_v0.py:120-125`)

### Phase A exposure candidates already accept a `theta` argument
```python
class AbsGradientExposure(ExposureDefinition):
    def evaluate(self, e: int, w: NDArray[np.float64], theta: float) -> float:
        g = grad_phi(w, theta)
        return float(np.abs(g[e]))
```
(Source: `src/nps/phases/phase_a/exposure/exposure_candidates.py:17-20`)

### Operator interface is θ-aware (but model may ignore it)
```python
def F(w: np.ndarray, theta: float | None = None) -> np.ndarray:
    return np.asarray(potential.grad(w, theta=theta), dtype=float)
```
(Source: `src/nps/operators/equilibrium_operator.py:26-28`)

### Phase C currently records θ-blocks as placeholders
```python
blocks_payload: dict[str, Any] = {
    "notes": "RealPhiV0 has no explicit theta block in v0; blocks recorded as placeholders.",
    "H_ww": _matrix_to_list(H),
    "H_wtheta": [],
    "H_thetaw": [],
}
```
(Source: `src/nps/phases/phase_c/build_casc.py:121-126`)

## Gaps

### Is `H_ww` computable today?
YES.

- For Real Φ v0, Phase C computes `H_ww = ∇_w^2 Φ_cert(w*)` via `SignedObjective.hess(w_star)`.
- Evidence: `src/nps/phases/phase_c/build_casc.py:107-110` uses `signed.hess(w_star)`.

### Is `H_wθ` computable today?
NO.

Minimal missing ingredients:

- **A θ parameterization contract for Real Φ v0**
  - Today, `RealPhiV0Spec.value/grad/hess` accept `theta: float | None` but explicitly ignore it (`_ = theta`).
  - So there is no differentiable map `θ ↦ Φ(w, θ)` exposed through that API.

- **A defined θ space (dimension + semantics)**
  - Candidates exist as *global scalars* (`theta_A`, `theta_M`, `theta_R`), but they are stored as fields, not a passed-in variable.
  - Phase C needs a coherent choice: e.g. `θ := (theta_A, theta_M, theta_R)`.

- **Cross-derivative implementation**
  - Either:
    - analytic `dtheta_grad(w, θ)` / `cross_hess_w_theta(w, θ)` methods on the model, or
    - a governance-approved finite-difference routine for `∂_θ ∇_w Φ` (likely only for toy/diagnostic unless certified).

- **CAS wiring**
  - CAS-B / CAS-C currently do not record the chosen θ vector or its value at the certified equilibrium; only `certified_objective` and `extension_id` are recorded.

## Candidate mapping to θ families

- `theta_A`, `theta_M`, `theta_R`: NOT_APPLICABLE to EDGE_LOCAL/NODE_LOCAL/MOTIF_LOCAL (they are global scalars).
- `theta` (toy): NOT_APPLICABLE (global scalar).
- `B_e(G)` / `κ_e(G)`: EDGE_LOCAL *structural exposure inputs* but not free parameters in current code.
- `R_e(G,w)`: MOTIF_LOCAL *structural statistic* (triangle motif), depends on `w` not θ.

## Recommended Next Step

The smallest governance-compliant way to introduce θ for Phase C Step 2 is to **reuse existing Real Φ v0 parameters** as the θ-vector by defining `θ := (theta_A, theta_M, theta_R)` and adding a *read-only parameter access layer* (no behavioral change) that exposes these fields as a vector plus an accompanying analytic map for `∂_θ ∇_w Φ`.

A minimal insertion point is to extend `RealPhiV0Spec` with an explicit method such as `grad_w_theta_blocks(w) -> (m,3)` (or equivalent), and then have Phase C compute `H_wθ` using that method. CAS-B/C should record the chosen θ coordinates and the realized θ values used at certification time.
