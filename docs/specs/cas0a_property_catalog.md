# CAS-0A Property Catalog (Phase 2)

This file is the human-readable audit view of the CAS-0A property catalog that is registered in code.

Source of truth:

- `src/nps/phases/phase_0a/build_cas0a.py`

## Properties

Each property is registered as a `PropertyKey(subject, property)` with a `SourceRef(key="CAS-0A-v4", detail=...)` locator.

- `("Omega", "nonempty")` — CAS-0A-v4: Assumption A1
- `("Omega", "compact")` — CAS-0A-v4: Assumption A1

- `("Phi", "continuous")` — CAS-0A-v4: Assumption A2
- `("Phi", "C3_extension")` — CAS-0A-v4: Assumption A3

- `("Locality", "defined_neighborhood_N(e)")` — CAS-0A-v4: Assumption A5
- `("Locality", "uniform_radius_r")` — CAS-0A-v4: Assumption A7

- `("F", "defined_as_grad_w_Phi")` — CAS-0A-v4: Definition 4.1

- `("W_star", "defined_as_argmax_over_Omega")` — CAS-0A-v4: Definition 7.1
