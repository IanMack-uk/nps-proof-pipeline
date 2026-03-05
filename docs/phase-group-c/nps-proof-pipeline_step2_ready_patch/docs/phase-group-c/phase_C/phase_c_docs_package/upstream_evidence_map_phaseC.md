
# Upstream Evidence Map — Phase C

Defines what evidence counts as VERIFIED for Phase C claims.

Allowed evidence sources:

- CAS-A.json
- CAS-B.json
- CAS-0C.json
- PhaseC_ENTRY_REPORT.md
- Phase C generated artifacts

Never use experiments/ outputs as VERIFIED evidence.

## Evidence Rules

### HESSIAN_EXISTS

VERIFIED if Hessian successfully computed and stored in HESSIAN_MATRIX.json.

### HESSIAN_SYMMETRIC

VERIFIED if symmetry check passes within tolerance.

### INVERSE_EXISTS

VERIFIED if Phase B regime is strict-concave and Hessian is negative definite.

### BLOCK_DECOMPOSITION

VERIFIED if structural blocks are successfully extracted.

### EXPOSURE_RESPONSE_COMPATIBILITY

VERIFIED if sign pattern of cross-derivative block is compatible with inverse-Hessian sign predictions.
