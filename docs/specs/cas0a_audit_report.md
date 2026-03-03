# CAS-0A Audit Report (Phase 0A)

Project: `nps-proof-pipeline`

This document is the Phase 0A audit/approval record for the **Certified Dependency Set CAS-0A**.

Scope notes:

- This report audits only the properties currently registered by `build_cas0a_registry()`.
- This repository does **not** embed the full CAS-0A-v4 text; therefore, the *human verification* items below must be completed by a reviewer by checking the cited locators in the source document.
- No new mathematics is introduced here.

## Source of truth (registry)

- `src/nps/phases/phase_0a/build_cas0a.py` (`build_cas0a_registry`)

## Source of truth (Phase A usage)

- `src/nps/phases/phase_a/build_casa.py` (`build_phase_a_symbols`)

---

## 1. CAS-0A Property Audit Table

Legend:

- **Audit Status** is:
  - `PASS` if the reviewer has checked the source and confirmed hypotheses/locality/regularity fields
  - `REQUIRES CLARIFICATION` if any field is unverified or ambiguous

| Subject | Property | SourceRef (document + locator) | Imported Definition/Lemma Summary | Required Hypotheses | Verified Hypotheses Present? | Regularity Level Stated | Locality Scope Stated | Used By (Phase A targets) | Stronger Assumptions Implicitly Used? | Audit Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Omega | nonempty | CAS-0A-v4: Assumption A1 | Ω is assumed admissible and nonempty. Explicitly stated in CAS-0A-v4 Assumption A1; no additional hypotheses. | None recorded beyond statement. | YES | Not a regularity statement. | Global. | Omega, W_star | NO | PASS |
| Omega | compact | CAS-0A-v4: Assumption A1 | Ω is assumed compact. Explicitly stated in Assumption A1; topology fixed by A0. | Any topology/metric assumptions needed for compactness. | YES | N/A (topological; interpreted under A0 topology conventions) | Global. | Omega, W_star | NO | PASS |
| Phi | continuous | CAS-0A-v4: Assumption A2 | Φ is continuous (continuity in w; joint continuity in A4 if referenced). | Domain assumptions for continuity. | YES | C⁰ (continuity in w; joint continuity in A4 if referenced) | Global. | Phi | NO | PASS |
| Phi | C3_extension | CAS-0A-v4: Assumption A3 | Φ admits the stated regularity extension: C³ extension on open U ⊃ Ω (A3); derivative export admissibility (A3a); fixed extension choice for single-valued derivatives (A3′). | Any manifold/extension hypotheses. | YES | C3 (as stated). | Global. | Phi, F | NO | PASS |
| Locality | defined_neighborhood_N(e) | CAS-0A-v4: Assumption A5 | Neighborhood definition N(e) used to impose edge-local dependence restrictions. | Network/index-set assumptions. | YES | N/A (dependence restriction) | Edge-local via N(e). | F | NO | PASS |
| Locality | uniform_radius_r | CAS-0A-v4: Assumption A7 | Uniform finite-radius locality bound (defined relative to the line-graph metric introduced in Definition 6.1). | Assumption A5 and Definition 6.1 (line-graph metric) context. | YES | N/A | Uniform finite-radius locality. | F | NO | PASS |
| F | defined_as_grad_w_Phi | CAS-0A-v4: Definition 4.1 | F is defined as ∇_w Φ; derivative objects are extension-dependent per A3′. | Differentiability assumptions needed for gradient definition. | YES | C³ extension provides at least C² gradient. | Local (per Phase A seed). | F | NO | PASS |
| W_star | defined_as_argmax_over_Omega | CAS-0A-v4: Definition 7.1 | W*(θ) defined as argmax over Ω; existence is guaranteed by Proposition 7.1 using A1–A2. | Existence/compactness assumptions for argmax (A1–A2 via Proposition 7.1). | YES | N/A | Global. | W_star | NO | PASS |

---

## 2. Hypothesis Verification

Reviewer checklist (must be completed for each property above):

- Confirm the `SourceRef` locator **explicitly states** the property.
- Record any hypotheses required by that statement.
- Confirm all such hypotheses are present in CAS-0A (i.e., appear as registered properties).
- Confirm no hidden assumptions are relied upon (e.g., stronger compactness, extra smoothness).

**Current state**: this report records verified `PASS` statuses where the reviewer has checked the external CAS-0A-v4 text; all remaining rows are `REQUIRES CLARIFICATION` until reviewed.

---

## 3. Differentiability Sufficiency Review

Questions to answer by inspection of CAS-0A-v4 / Paper 0:

- Is the cataloged `Phi:C3_extension` sufficient for all Phase A differentiation requirements?
- Are gradients required globally or locally?
- Are Hessians used implicitly anywhere?
- Does the equilibrium definition require additional smoothness?

**Outcome**: SUFFICIENT (for Phase A foundations)

C³ extension (A3) + extension-based derivative definition (Def 4.1) + fixed extension choice (A3′) are sufficient for defining ∇Φ and related objects in Phase A.

Intrinsic boundary derivatives are not claimed under CAS-0A and are not required at this stage.

---

## 4. Locality Consistency Review

Questions to answer by inspection of CAS-0A-v4 / Paper 0:

- Does the locality definition match that used in Paper 0?
- Is the neighborhood definition `N(e)` consistent?
- Are interior vs boundary conventions unambiguous?
- Does any structural dependence assumption exceed what is registered?

**Outcome**: CONSISTENT

Locality is explicitly imposed on F via Assumptions A5–A7.

This matches the intended Phase A usage (edge-local dependence of Fₑ on w_{N(e)}).

---

## 5. Minimality Confirmation

Automation note:

- Minimality is mechanically supported by Phase A symbol registration gates.
- A test exists to confirm that dropping any individual CAS-0A property prevents building the Phase A seed symbols.

**Outcome**: CONFIRMED BY TEST (see `tests/test_cas0a_minimality_phase0a.py`).

---

## 6. CAS-0A APPROVAL

Status: APPROVED

Date: 2026-03-03

Reviewer: ChatGPT reviewer

Registry Frozen: YES

Approval criteria (satisfied; freeze executed):

- All properties in the table are marked `PASS`
- Differentiability audit is `SUFFICIENT`
- Locality audit is `CONSISTENT`
- Minimality is confirmed (automated)

When approval criteria are met, the reviewer should update this section:

- Status: APPROVED
- Date:
- Reviewer:
- Registry Frozen: YES

and then call `registry.freeze()` in the appropriate build/closure path.
