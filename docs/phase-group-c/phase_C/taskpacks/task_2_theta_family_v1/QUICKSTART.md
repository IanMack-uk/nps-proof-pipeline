# Taskpack 2 — θ-Family Definition (Quickstart)

This taskpack defines the **test-parameter family** \(\theta\) for Phase C and makes the cross-derivative block

\[
H_{w\theta}(w^*,\theta) = D_\theta\,\nabla_w \Phi_{\text{cert}}(w^*,\theta)
\]

exist as a computed artefact.

This is required to complete Phase C step “exposure–response compatibility” and to honestly gate:

- `Phase C Status: READY_FOR_PHASE_D`

---

## Why this exists

Phase C can compute Hessian \(H_{ww}\) at \(w^*\) without knowing \(\theta\).
But Phase C cannot compute **equilibrium response signs** or exposure–response compatibility without:
- a precise definition of \(\theta\),
- and a computable \(H_{w\theta}\).

---

## Preconditions (must hold)

### Phase C entry gate is approved
Run root:
- `cert_artifacts/RUN_ID_TODO/`

Must contain:
- `PhaseC_ENTRY_REPORT.md` ending with `Phase C Entry Gate: APPROVED`
- canonical CAS chain in run root

### Governance gates (recommended)
```bash
export NPS_IMPORT_FIREWALL=1
export NPS_CAS_GATE=1
export NPS_CERT_DEP_GATE=1
export NPS_RUN_DIR_INTEGRITY=1
```

---

## Recommended definition pattern (cert-friendly)

Treat \(\theta\) as coefficients of a **perturbation functional basis**:

\[
\Phi_{\text{cert}}(w,\theta) := \Phi_{\text{cert}}(w) + \sum_{k=1}^m \theta_k\,\Psi_k(w)
\]

Then:

\[
H_{w\theta}(w^*,\theta) = \left[\nabla_w \Psi_1(w^*)\;\cdots\;\nabla_w \Psi_m(w^*)\right]
\]

This avoids having to “guess” how \(\theta\) enters the base NPF model.

---

## Execution option

### Preferred: implement in Phase C CLI and re-run

After implementing the θ-family and cross-derivative computation, re-run Phase C:

```bash
RUN=RUN_ID_TODO
PYTHONPATH=src python -m nps.phases.phase_c.build_casc   --run-id "$RUN"   --run-root "cert_artifacts/$RUN"
```

Expected updated run-root artefacts include:
- `EXPOSURE_RESPONSE_CHECK.json` with `computed: true` and `status: PASS` (or a clear FAIL)
- `CAS-C.json` status updated from BLOCKED/INCOMPLETE → APPROVED/READY (only if criteria met)

---

## Deliverables (minimum)

Write to run root:
- `THETA_FAMILY.json` (new; formal θ definition + basis labels)
- `H_WTHETA.json` (new; the computed cross-derivative block, or sparse representation)
- `PhaseC_TASK2_THETA_FAMILY_REPORT.md` (new; uses the template)

---

## Recommended commit policy

- Commit code + docs.
- Prefer a run transcript doc rather than committing generated `cert_artifacts/` outputs.

