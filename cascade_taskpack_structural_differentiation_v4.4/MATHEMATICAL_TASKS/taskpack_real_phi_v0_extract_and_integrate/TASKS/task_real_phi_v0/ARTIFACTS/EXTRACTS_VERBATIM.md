# Verbatim extracts for canonical Real Φ v0

These are **verbatim text+math extracts** pulled from the uploaded draft documents.
Math is extracted from Word OMML where available (shown inline as `MATH: ...`).


## Relational / Network potential functional Φ

**Source:** `Network-Potential-and-Relational-Optimisation-mathematics-thesis.docx`

- [365] 3.3 Global Network Potential
- [367] Definition 3.2 (Network Potential Functional)
- [368] Define the Network Potential Functional
- [369] `MATH: Φ(w)=i∈VNPFi(w).`
- [370] For fixed and , the functional `MATH: VE`
- [371] `MATH: Φ:[0,1]∣E∣→R`
- [372] maps tie-strength configurations to scalar potential values.
- [373] The functional measures global structural quality. `MATH: Φ(w)`
- [374] Relational optimisation is formulated as:
- [375] `MATH: max⁡w∈[0,1]∣E∣Φ(w).`
- [376] 3.4 Well-Definedness and Bounds

## Node-level potential NPFᵢ

**Source:** `Network-Potential-and-Relational-Optimisation-mathematics-thesis.docx`

- [350] 3.2 Node-Level Network Potential
- [352] Definition 3.1 (Network Potential Function)
- [353] Let
- [354] `MATH: θA,θM,θR≥0`
- [355] be fixed parameters.
- [356] For node , define the Network Potential Function `MATH: i∈V`
- [357] `MATH: NPFi(w)=θAlog⁡(1+Ai(w))+θMlog⁡(1+Mi(w))-θRlog⁡(1+Ri(w)).`
- [358] The Network Potential Function measures the structural quality of node 's relational configuration. `MATH: i`
- [359] The three terms represent:
- [360] cohesion through strong ties,
- [361] nonredundant reach through brokerage-weighted weak ties,
- [362] redundancy penalties through closure.
- [363] The logarithmic form ensures diminishing marginal returns in each component.

## Cohesion component Aᵢ(w)

**Source:** `Network-Potential-and-Relational-Optimisation-mathematics-thesis.docx`

- [255] 2.6 Stability Functional
- [256] Define the stability functional:
- [257] `MATH: Ai(w)=j∈Γ(i)Sij.`
- [258] Explicitly:
- [259] `MATH: Ai(w)=j∈Γ(i)wijp.`
- [260] The stability functional measures cohesive capacity around node . `MATH: i`
- [262] Proposition 2.1 (Bounds on Stability)
- [263] For all nodes : `MATH: i`
- [264] `MATH: 0≤Ai(w)≤di.`

## Brokerage component Mᵢ(w)

**Source:** `Network-Potential-and-Relational-Optimisation-mathematics-thesis.docx`

- [269] 2.7 Mobility Functional
- [270] Define the mobility functional:
- [271] `MATH: Mi(w)=j∈Γ(i)WijBij.`
- [272] Explicitly:
- [273] `MATH: Mi(w)=j∈Γ(i)(1-wij)pBij.`
- [274] This functional measures brokerage-weighted weak-tie mass.
- [276] Proposition 2.2 (Bounds on Mobility)
- [277] For all nodes : `MATH: i`
- [278] `MATH: 0≤Mi(w)≤di.`

## Redundancy component Rᵢ(w)

**Source:** `Network-Potential-and-Relational-Optimisation-mathematics-thesis.docx`

- [288] `MATH: 1E(j,k)=1if {j,k}∈E0otherwise.`
- [289] Define redundancy:
- [290] `MATH: Ri(w)={j,k}⊆Γ(i)SijSik1E(j,k).`
- [291] Explicitly:
- [292] `MATH: Ri(w)={j,k}⊆Γ(i)wijpwikp1E(j,k).`
- [293] This functional measures weighted triadic closure around node . `MATH: i`
- [295] Proposition 2.3 (Bounds on Redundancy)
- [296] For all nodes : `MATH: i`
- [297] `MATH: 0≤Ri(w)≤di2.`
- [298] Proof
- [299] Each summand satisfies:

## Configuration space W and interior W°

**Source:** `The-Network-Potential-Series-Paper2-v25.docx`

- [138] 1.0 Foundational Theorem Schema
- [140] 1.0.1 Configuration Space
- [142] Let be a fixed finite graph with edge set . A weighted network on is specified by a vector of edge weights `MATH: G=(V,E)EG`
- [144] `MATH: w=(we)e∈E∈[0,1]∣E∣.`
- [145] The configuration space of admissible weight assignments is therefore the compact hypercube
- [147] `MATH: W=[0,1]∣E∣,`
- [148] with interior
- [150] `MATH: W∘=(0,1)∣E∣.`
- [151] Points represent relational configurations on the fixed topology . Throughout this paper the topology is assumed fixed unless explicitly stated otherwise. `MATH: w∈WGG`
- [152] Relational optimisation is formulated through scalar functionals

## Equilibrium as interior stationarity / strict local maximiser

**Source:** `The-Network-Potential-Series-Paper2-v25.docx`

- [479] 1.2.3 Equilibrium and Stability
- [481] Definition 2.1 (Stationary Point)
- [482] A weight vector is stationary if `MATH: w∈Ω∘`
- [483] `MATH: ∇Φw=0,`
- [484] equivalently,
- [485] `MATH: ∂eΦw=0for all e∈E.`
- [486] Definition 2.2 (Strict Local Maximiser)
- [487] A stationary point is a strict local maximiser if there exists  such that `MATH: w\*∈Ω∘ε>0`
- [489] `MATH: Φw<Φw\*for all w∈Ω with 0<∥w-w\*∥<ε.`
- [490] Although the feasible weight space
- [491] `MATH: Ω=[0,1]∣E∣`
- [492] is compact, the structural analysis developed in this paper relies on differential properties that hold on the open domain
- [494] `MATH: Ω∘=(0,1)∣E∣.`
- [495] The following lemma establishes that strict local maximisers necessarily lie in the interior of the feasible region under the marginal structure of the Network Potential Functional.

## Structural exposure component: Brokerage index Bₑ

**Source:** `The-Network-Potential-Series-Paper2-v25.docx`

- [570] For , `MATH: e=i,j`
- [571] `MATH: κeG≔∣Ni∩Nj∣.`
- [572] Definition 2.4 (Brokerage Index)
- [573] Let be strictly decreasing. Define `MATH: f:N→R+`
- [574] `MATH: BeG≔fκeG.`
- [575] Higher indicates greater structural separation. `MATH: Be`
- [577] Definition 2.5 (Redundancy Index)
- [578] For , `MATH: e=i,j`
- [579] `MATH: ReG,w≔k∈Ni∩Njwikwjk,`
- [580] the weighted triangle participation of . `MATH: e`

## Structural exposure component: Redundancy index Rₑ

**Source:** `The-Network-Potential-Series-Paper2-v25.docx`

- [575] Higher indicates greater structural separation. `MATH: Be`
- [577] Definition 2.5 (Redundancy Index)
- [578] For , `MATH: e=i,j`
- [579] `MATH: ReG,w≔k∈Ni∩Njwikwjk,`
- [580] the weighted triangle participation of . `MATH: e`
- [582] 1.2.5 Symmetry
- [584] Definition 2.6 (Local Structural Symmetry)
- [585] Two incident edges  are structurally symmetric if `MATH: e,f∈Ei`

## Incident Hessian operator Hᵢ(w)

**Source:** `The-Network-Potential-Series-Paper2-v25.docx`

- [642] denote the natural inclusion map.
- [644] Definition 1.5 (Incident Hessian Operator)
- [645] The incident Hessian operator at node is defined by `MATH: i`
- [647] `MATH: Hi(w)=Pi H(w) ιi:RE(i)→RE(i).`
- [648] Equivalently,  is represented in edge coordinates by the principal Hessian block  introduced in §1.2.8.1. The operator formulation makes explicit that the incident Hessian acts intrinsically on the incident perturbation space and is independent of the ordering of edges. `MATH: Hi(w)Hi(w)`
- [650] Structural Interpretation
- [651] The operator represents the local curvature of the Network Potential Functional with respect to perturbations of tie strengths incident to node . In particular: `MATH: Hi(w)i`
- [652] diagonal entries describe marginal curvature of individual ties,
- [653] off-diagonal entries describe cross-partial coupling between incident ties,
- [654] the operator spectrum determines local curvature behaviour on the incident subspace and therefore governs local structural stability and comparative statics.
- [655] Thus  governs the local structural response of equilibrium tie strengths to perturbations of incident marginal incentives. `MATH: Hi(w)`

## Structural dominance partial order

**Source:** `The-Network-Potential-Series-Paper2-v25.docx`

- [832] 1.3.3 Structural Dominance and Partial Ordering
- [834] Definition 3.1 (Structural Dominance)
- [835] For incident edges  , we say structurally dominates if `MATH: e,f∈Eief`
- [837] `MATH: Be≥Bf,Re≥Rf,`
- [838] with at least one strict inequality.
- [840] Theorem 3.1 (Equilibrium Structural Ordering)
- [841] Let  be a strict local maximiser. Under Assumption 2.6, if structurally dominates , then `MATH: w⋆ef`
- [842] `MATH: we⋆<wf⋆`
- [843] generically (i.e., outside the structural symmetry locus).
- [845] Remark 3.1 (M-matrix Sign Control)
