# Phase C Mathematical Tool Whitelist

## Purpose

Phase C of the NPS proof pipeline studies the **curvature structure of
equilibrium systems**, in particular:

-   Hessian structure of the certified objective
-   coupling operator structure
-   inverse-Hessian / susceptibility structure
-   sign structure of comparative statics responses

To maintain **governance control and proof minimality**, Phase C is
restricted to a **certified whitelist of finite-dimensional
matrix-analysis tools**.

Global operator-theoretic machinery and spectral methods are **excluded
by default** unless separately certified.

This document defines the **allowed mathematical tool layer** for Phase
C.

------------------------------------------------------------------------

# Scope of Phase C

Phase C operates on:

H = ∇²Φ(w\*, θ)

where Φ is the certified objective and w\* is the certified equilibrium.

Phase C studies the coupling operator

C = -H

under the maximisation convention.

The goal is to establish:

-   sign structure of H
-   sign structure of C⁻¹
-   comparative statics response structure

------------------------------------------------------------------------

# Governance Principle

Phase C must satisfy the following constraint:

> Only **finite-dimensional matrix-analysis tools** may be used unless a
> separate certification layer authorises spectral or operator-theoretic
> methods.

This ensures:

-   proofs remain **structural and local**
-   the pipeline remains **auditable**
-   dependency chains remain **minimal**

------------------------------------------------------------------------

# Allowed Mathematical Tool Classes

The following tools are **certified for use in Phase C**.

------------------------------------------------------------------------

# 1. Neumann-Series Inversion Bounds

## Statement

If

‖I − A‖ \< 1

then

(I − A)⁻¹ = Σ Aᵏ

## Role in Phase C

Used to establish:

-   inverse existence
-   bounds on inverse operators
-   perturbation stability

## Status

TOOL.NEUMANN_SERIES_INVERSION

Certified for Phase C.

------------------------------------------------------------------------

# 2. Matrix Comparison Inequalities

## Examples

Comparison arguments of the form:

A ≤ B ⇒ A⁻¹ ≥ B⁻¹

under appropriate monotonicity conditions.

## Role in Phase C

Used for:

-   sign propagation
-   bounding inverse entries
-   monotone comparative statics

## Status

TOOL.MATRIX_COMPARISON_INEQUALITIES

Certified for Phase C.

------------------------------------------------------------------------

# 3. Block Matrix Inversion Bounds

## Structure

For block matrices

\[ A B \] \[ C D \]

use Schur complement arguments and block norm inequalities.

## Role in Phase C

Used to study:

-   locality structure
-   subsystem coupling
-   structural neighbourhood interactions

## Status

TOOL.BLOCK_NORM_INVERSION_BOUND

Certified for Phase C.

------------------------------------------------------------------------

# 4. Diagonal Dominance Criteria

## Example

Strict diagonal dominance:

\|a_ii\| \> Σ \|a_ij\|

## Role in Phase C

Provides sufficient conditions for:

-   invertibility
-   sign structure
-   stability of inverse matrices

## Status

TOOL.DIAGONAL_DOMINANCE_MARGIN

Certified as a **sufficient-condition diagnostic tool**.

------------------------------------------------------------------------

# 5. Finite-Dimensional M-Matrix Criteria

## Description

Conditions guaranteeing:

-   positive inverse
-   monotone systems

Typical characterisation:

A = sI − B

with

B ≥ 0

and

s \> ρ(B)

## Role in Phase C

Useful for:

-   sign structure of inverse coupling matrices
-   monotone systems

## Status

TOOL.M_MATRIX_CRITERIA

Allowed **only where applicable**.

If used, the dependency must be recorded in CAS-0C.json.

------------------------------------------------------------------------

# Excluded Methods (Default)

The following methods are **not permitted in Phase C by default**.

------------------------------------------------------------------------

## Spectral Theory

Examples:

-   eigenvalue decompositions
-   spectral radius arguments
-   Perron--Frobenius theorems

Reason:

These introduce **global operator dependencies**.

Allowed only if:

CAS-0C.spectral_escalation = true

------------------------------------------------------------------------

## Functional Analysis

Examples:

-   compact operators
-   Banach space arguments
-   infinite-dimensional operator theory

Reason:

Phase C operates strictly in **finite-dimensional matrix settings**.

------------------------------------------------------------------------

## Global Operator-Theoretic Machinery

Examples:

-   resolvent operators
-   spectral measures
-   semigroup theory

Reason:

These exceed the structural requirements of the NPS pipeline.

------------------------------------------------------------------------

# Required Usage Rules

Whenever a tool is used in Phase C:

1.  The tool must appear in CAS-0C.json as a verified_import.

Example:

{ "import_id": "TOOL.NEUMANN_SERIES_INVERSION", "kind":
"finite_dim_tool", "status": "VERIFIED" }

2.  If a tool is **not on this whitelist**, it must be placed in
    PROV-0C.json with a certification plan.

------------------------------------------------------------------------

# Relationship to CAS-0C

CAS-0C defines the **mathematical dependency layer** for Phase C.

This whitelist specifies the **allowed tool vocabulary**.

CAS-0C therefore contains entries such as:

TOOL.NEUMANN_SERIES_INVERSION\
TOOL.BLOCK_NORM_INVERSION_BOUND\
TOOL.MATRIX_COMPARISON_INEQUALITIES

These become **certified dependencies** for the Phase C proof layer.

------------------------------------------------------------------------

# Future Extensions

Additional tools may be added through **separate certification**.

Possible candidates:

-   graph Laplacian sign structure
-   structured sparsity theorems
-   monotone system theory

Any addition must:

1.  be explicitly justified\
2.  be added to this whitelist\
3.  appear in CAS-0C.json.

------------------------------------------------------------------------

# Summary

Phase C operates under the following rule:

> The curvature and inverse-curvature analysis must rely only on
> certified finite-dimensional matrix-analysis tools unless a
> higher-level certification authorises spectral or operator-theoretic
> methods.

This ensures the NPS proof pipeline remains:

-   mathematically controlled\
-   dependency-minimal\
-   computationally auditable.
