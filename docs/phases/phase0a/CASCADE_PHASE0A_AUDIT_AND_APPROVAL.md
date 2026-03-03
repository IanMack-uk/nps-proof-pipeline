# CASCADE PHASE 0A --- AUDIT AND APPROVAL

Project: `nps-proof-pipeline`

This document instructs Cascade to formally complete **Phase 0A ---
Prior Results Certification for Phase A** as defined in
Structural_Differentiation_Programme_v4.

The infrastructure for CAS-0A exists (property-level registry, SourceRef
enforcement, drop tests, audit export).

This phase performs the **mathematical audit and formal approval** step
required by the programme.

------------------------------------------------------------------------

# 🎯 Objective

Produce a formally audited and approved **Certified Dependency Set
CAS-0A**.

This requires:

1.  Hypothesis verification for all imported properties
2.  Differentiability sufficiency audit
3.  Locality consistency audit
4.  Minimality confirmation (post-audit)
5.  Formal approval + freeze of CAS-0A

No new mathematics should be introduced.

------------------------------------------------------------------------

# 1️⃣ Generate CAS-0A Property Audit Table

Create or update:

    docs/specs/cas0a_audit_report.md

For each registered CAS-0A PropertyKey:

Record the following fields:

-   Subject
-   Property
-   SourceRef (document + locator)
-   Imported Definition/Lemma Summary (1--3 lines)
-   Required Hypotheses
-   Verified Hypotheses Present? (Yes/No + explanation)
-   Regularity Level Stated
-   Locality Scope Stated
-   Used By (Phase A targets)
-   Stronger Assumptions Implicitly Used? (Yes/No)
-   Audit Status (PASS / REQUIRES CLARIFICATION)

This table must be complete for every property currently registered.

------------------------------------------------------------------------

# 2️⃣ Hypothesis Verification Step

For each property:

-   Confirm that the SourceRef location explicitly states the property.
-   Confirm all hypotheses required by that statement are recorded in
    CAS-0A.
-   Confirm no hidden assumptions are relied upon.

If any property relies on: - stronger differentiability - additional
compactness conditions - unrecorded structural assumptions

Mark as REQUIRES CLARIFICATION and stop approval.

------------------------------------------------------------------------

# 3️⃣ Differentiability Sufficiency Audit

Specifically verify:

-   Is C³ extension sufficient for all Phase A differentiation
    requirements?
-   Are gradients defined globally or only locally?
-   Are Hessians implicitly assumed anywhere?
-   Does equilibrium definition require more smoothness?

Record findings in a dedicated section:

    "Differentiability Sufficiency Review"

Outcome must be one of: - SUFFICIENT - INSUFFICIENT (specify required
strengthening)

------------------------------------------------------------------------

# 4️⃣ Locality Consistency Audit

Verify:

-   Locality definition in CAS-0A matches that used in Paper 0.
-   Neighborhood definition N(e) is consistent.
-   No ambiguity in interior vs boundary conventions.
-   Structural dependence assumptions do not exceed registered
    properties.

Record findings in:

    "Locality Consistency Review"

Outcome must be one of: - CONSISTENT - INCONSISTENT (specify mismatch)

------------------------------------------------------------------------

# 5️⃣ Post-Audit Minimality Re-Run

After completing audit table:

-   Re-run drop test for each property (automated or documented).
-   Confirm removal of any property breaks at least one Phase A seed
    symbol.

Record confirmation in:

    "Minimality Confirmation"

------------------------------------------------------------------------

# 6️⃣ Formal Approval Record

If and only if:

-   All properties PASS
-   Differentiability audit = SUFFICIENT
-   Locality audit = CONSISTENT
-   Minimality confirmed

Then:

1.  Add section to audit report:

    \## CAS-0A APPROVAL

    Status: APPROVED Date: Reviewer: Registry Frozen: YES

2.  Freeze CAS-0A in code (registry.freeze() if available).

3.  Tag repository state (optional, recommended): v0.1-cas0a-approved

------------------------------------------------------------------------

# 7️⃣ Verification

After documentation and freeze:

-   pytest
-   mypy src
-   ruff check .

All must pass.

------------------------------------------------------------------------

# 🚫 Non-Goals

Do NOT:

-   Add new properties
-   Modify Phase A objects
-   Introduce structural exposure yet
-   Expand to Paper 1 operator theory

This is strictly closure of Phase 0A.

------------------------------------------------------------------------

# ✅ Completion Condition

Phase 0A is complete when:

-   Full audit table exists
-   All properties verified
-   Differentiability audit marked SUFFICIENT
-   Locality audit marked CONSISTENT
-   Minimality reconfirmed
-   Registry frozen
-   Approval recorded in documentation
-   All checks pass
