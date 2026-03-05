# CASCADE PHASE A (STEP A9) --- GRAPH-CANONICAL NEIGHBOURHOODS + TRUE AUTOMORPHISM ACTION (SANDBOX)

Project: `nps-proof-pipeline`

Context: - CAS-0A frozen (certified base). - Phase A + Phase Aʹ draft
closure complete through A8. - Paper 0 coordinate candidates imported
(A7), validated against locality/invariance using a `neighborhoods`
oracle. - Domain policy fixed: proof-target uses nonnegative Ω; signed
is red-team.

Problem: Current "automorphism invariance" and "locality" checks depend
on a precomputed `neighborhoods` mapping. This can hide failures because
invariance/locality may be an artifact of the mapping rather than a true
graph-level property.

This step introduces a minimal, deterministic **Graph sandbox** and
canonical **N(e)** generation (line-graph radius), plus a true
**automorphism / relabelling action** that transports weights and edge
indices correctly. This strengthens Phase A validators so they test
structural properties, not oracle consistency.

------------------------------------------------------------------------

## 🎯 Objectives

1.  Add a minimal graph object (undirected, no multi-edges) with
    deterministic edge indexing.
2.  Implement canonical neighbourhoods `N_r(e)` using **line-graph
    distance** (radius r).
3.  Implement node relabellings (permutations) and induced edge-index
    transport.
4.  Upgrade Paper 0 invariance tests to use real relabellings and
    transported weights.
5.  Keep everything sandbox-only, deterministic, and strictly typed.

------------------------------------------------------------------------

## 0️⃣ Files / Folders to Add

Create:

    src/nps/models/graph/
      __init__.py
      simple_graph.py
      line_graph.py
      automorphisms.py

    src/nps/models/sandbox/
      neighborhoods.py

    tests/graph/
      __init__.py
      test_edge_indexing.py
      test_line_graph_neighborhoods.py
      test_relabelling_transport.py

    tests/phase_a/
      test_paper0_invariance_graph_canonical.py

Do NOT modify CAS-0A. Do NOT change existing Phase A assumption IDs.
Keep existing oracle-based validators; add graph-canonical variants and
migrate Paper 0 tests to the stronger version.

------------------------------------------------------------------------

## 1️⃣ Minimal Graph Representation

### 1.1 `SimpleGraph`

File: `src/nps/models/graph/simple_graph.py`

Requirements: - Undirected simple graph on n nodes labeled 0..n-1 -
Store edges as sorted pairs (u \< v) - Deterministic edge index mapping:
edges sorted lexicographically

API: - `n: int` - `edges: list[tuple[int,int]]` -
`edge_index: dict[tuple[int,int], int]` - `neighbors(v) -> set[int]` -
`endpoints(e_idx) -> tuple[int,int]`

Validation: - no self-loops - no duplicate edges - nodes within range

------------------------------------------------------------------------

## 2️⃣ Line-Graph Neighbourhoods

### 2.1 Line graph adjacency

File: `src/nps/models/graph/line_graph.py`

Define edges adjacent if they share an endpoint in original graph.

API: - `line_neighbors(g: SimpleGraph, e_idx: int) -> set[int]` -
`line_ball(g: SimpleGraph, e_idx: int, radius: int) -> set[int]`

`line_ball` should BFS in the line graph and return all edge indices
within distance ≤ radius, including e itself.

Deterministic (BFS over sorted neighbors).

### 2.2 Sandbox wrapper

File: `src/nps/models/sandbox/neighborhoods.py`

API: -
`compute_edge_neighborhoods(g: SimpleGraph, radius: int) -> dict[int, set[int]]`

------------------------------------------------------------------------

## 3️⃣ Relabelling / Automorphism Transport

File: `src/nps/models/graph/automorphisms.py`

Implement:

### 3.1 Node permutation action

-   Input: permutation `perm: list[int]` representing mapping old_node
    -\> new_node
-   Apply to edges: (u,v) -\> (perm\[u\], perm\[v\]) then sort endpoints
-   Build new `SimpleGraph` with permuted edges

### 3.2 Edge-weight transport

Given: - original graph g - permuted graph g' - weights w indexed by
g.edge_index

Return transported weights w' indexed by g'.edge_index such that:
w'\_{e'} = w_e where e' is image of e under perm.

API: -
`transport_edge_weights(g: SimpleGraph, g2: SimpleGraph, perm: list[int], w: np.ndarray) -> np.ndarray`

Validate shape and that g2 edges equal permuted edges.

------------------------------------------------------------------------

## 4️⃣ Upgrade Paper 0 Invariance Validator to Graph-Canonical

Add a new validator function in:
`src/nps/phases/phase_a/coordinates/coordinate_paper0_validation.py`

Function: `check_automorphism_invariance_graph(...)`

Inputs: - graph g - radius r (to compute N_r(e)) - coordinate candidate
callable that accepts (e_idx, w, neighborhoods) - a small fixed list of
permutations (deterministic) - policy: NonnegativePolicy for
proof-target weights

Procedure: 1. Compute neighborhoods from g, radius r. 2. For each
perm: - build g' - transport w -\> w' - compute neighborhoods' from g',
radius r - for each e_idx in g: compare coord(e, w, N) vs coord(e', w',
N') where e' is image edge index 3. Require equality within small
tolerance.

This is true invariance.

Keep old oracle-based check in place for backward compatibility; migrate
Paper 0 tests to the stronger check.

------------------------------------------------------------------------

## 5️⃣ Tests

### 5.1 Graph core tests

-   edge indexing deterministic
-   line_ball correct on small graphs (triangle, path, square)
-   relabelling transport correct (weights match mapped edges)

### 5.2 Phase A invariance test

`tests/phase_a/test_paper0_invariance_graph_canonical.py`

-   Build a small graph (triangle + tail) with n=4, edges deterministic.
-   Sample w with NonnegativePolicy.
-   Compute Paper 0 S/R on canonical neighborhoods.
-   Verify graph-canonical invariance under at least 2 nontrivial
    permutations.
-   Include negative control coordinate that uses raw edge index (breaks
    invariance) and ensure it fails.

Evidence logging optional here; keep tests purely correctness-focused.

------------------------------------------------------------------------

## 6️⃣ Verification

Run: - `pytest` - `mypy src` - `ruff check .`

All must pass.

------------------------------------------------------------------------

## ✅ Completion Condition

-   Canonical `N_r(e)` implemented via line-graph radius.
-   True relabelling transport implemented.
-   Paper 0 invariance checks upgraded to graph-canonical.
-   Tests cover indexing, neighborhoods, transport, invariance.
-   All checks pass.

After A9, Paper 0 coordinate validation is meaningfully structural
rather than oracle-dependent.
