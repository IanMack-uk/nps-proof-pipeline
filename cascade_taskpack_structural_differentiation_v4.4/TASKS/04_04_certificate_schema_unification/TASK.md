# 04_04_certificate_schema_unification: Unify certificate schemas and phase artefact outputs

## Goal
Standardize certificate objects and ensure every phase can emit auditable artefacts.

## Required actions
1. Implement schema types (dataclasses / pydantic OK):
   - AssumptionCertificate
   - PropertyCertificate (checkable)
   - NumericCertificate (approx + diagnostics)
   - NonCheckableAssumption (explicitly flagged)
2. Standardize per-phase outputs:
   - CAS-0X.json (dependency table + drop-test evidence)
   - CAS-X.json (constructed objects + certified properties)
   - PhaseReport.md
3. Add a report generator utility and unit tests.

## Artefacts
- example outputs generated on a toy instance (stored here)

## Report requirements
- Show schemas and an example emission.
- Explain how “fails loudly” is implemented (exceptions + witnesses).

