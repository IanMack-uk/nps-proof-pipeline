# CAS-A Assumption Ledger (Phase A)

## Purpose

This document is the living ledger for **CAS-A**: provisional assumptions and statements that bridge from frozen CAS-0A into Phase A development.

Items begin **PROVISIONAL** and may be promoted to **CERTIFIED** only when supported by explicit evidence (tests, counterexamples resolved, review notes).

## Status definitions

- `PROVISIONAL`: admissible for exploration; not trusted for downstream phase gates
- `CERTIFIED`: evidence-backed and approved for dependency requirements
- `REJECTED`: disallowed; any use must be removed or isolated

For statements:

- `CONJECTURE`: proposed but not yet supported
- `VALIDATED`: supported by evidence
- `DISPROVEN`: falsified by counterexample or failed validation

## Scope tags

- `FOUNDATIONS`
- `PHASE_B_INTERFACE`
- `DIFFERENTIABILITY`
- `UNIQUENESS`

## Assumption table template

| ID | Text | Scope | Status | Sources | Requires (CAS-0A) | Evidence |
|---|---|---|---|---|---|---|
| CAS-A.EXP.LOCALITY | Structural exposure E_e(w,θ) depends only on local data (N(e)) when declared local. | FOUNDATIONS | PROVISIONAL |  |  |  |
| CAS-A.EXP.WELLPOSED | Structural exposure is well-defined and finite for all w ∈ Ω. | FOUNDATIONS | PROVISIONAL |  |  |  |
| CAS-A.EXP.REGULARITY | Structural exposure inherits at least C⁰ regularity from its defining objects. | DIFFERENTIABILITY | PROVISIONAL |  |  |  |
| CAS-A.NOTATION.STABILITY | Phase A symbol dictionary remains fixed (versioned freeze) for all subsequent reasoning. | FOUNDATIONS | PROVISIONAL |  |  |  |
| CAS-A.OMEGA.NONNEGATIVE | For the proof-target model class, Ω ⊂ R^m_{≥0} (weights are componentwise nonnegative). | FOUNDATIONS | PROVISIONAL |  |  |  |

CAS-A draft: no assumption certified yet; minimality and closure pending Phase Aʹ.

## Statement table template

| ID | Statement | Status | Sources | Requires (CAS-0A) | Depends on assumptions | Evidence |
|---|---|---|---|---|---|---|

## Promotion protocol

An item may be promoted only when:

- Evidence links point to deterministic, passing tests (or reviewed proof notes)
- Any required CAS-0A prerequisites are explicit
- The status transition is recorded (PROVISIONAL -> CERTIFIED for assumptions; CONJECTURE -> VALIDATED for statements)
