# AG Theory and Mechanism Review

Date: 2026-03-24
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`
Purpose: identify which AG theory/mechanism docs are strong enough to reuse and decide how they should enter the KA architecture

## Bottom line

AG has produced useful material in three different categories:

1. layer test and repair material
2. theory grouping and lookup material
3. mechanism extraction guidance

These categories should not be treated equally.

The strongest AG contributions are:
- test matrices
- repair plans
- active-program mismatch maps
- mechanism extraction discipline

The weakest AG contributions are:
- hard-coded theory hierarchy mappings when treated as finished ontology truth

So the right approach is:
- reuse AG heavily for verification and extraction discipline
- reuse AG cautiously for theory browse scaffolding
- do not treat AG’s current hierarchy tables as final public-facing theoretical authority

## Files reviewed

Primary files:
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/THEORY_HIERARCHY_IMPLEMENTATION.md`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/THEORY_HIERARCHY_QUICKSTART.md`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/ATLAS_ACTIVE_PROGRAM_THEORY_MAP_2026-03-17.md`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/ATLAS_THEORY_LAYER_REPAIR_PLAN_2026-03-17.md`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/ATLAS_THEORY_TO_LAYER_TEST_MATRIX_2026-03-17.md`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/CHEAT_SHEET_MECHANISM_MEDIATION_2026-03-21.md`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/ATLAS_THEORY_SENSITIVE_VOI_SPEC_2026-03-14.md`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/THEORY_IMPLEMENTATION_GAP_TODO_2026-03-22.md`

## What is clearly usable

### 1. Theory-to-layer test matrix

Usable because it does something the UI/program architecture needs:
- translates theory commitments into executable checks
- names failure modes rather than only naming concepts
- keeps theory tied to concrete products

Best use:
- rebuild SCs
- ruthless audits
- acceptance criteria for theory-heavy surfaces

Not for:
- student-facing theory prose

### 2. Theory layer repair plan

Usable because it is operational and prioritised.

Best use:
- sprint planning
- backend repair sequencing
- deciding which theoretical claims are actually production-ready

Not for:
- direct public explanation

### 3. Active program theory map

Usable because it is honest about mismatch between theory docs and live code.

Best use:
- architecture review
- deciding what the current system can truly claim
- identifying where the UI should show provisional or partial status

Not for:
- public-facing triumphant “ATLAS already does X” language

### 4. Mechanism and mediation cheat sheet

Usable because it is disciplined and modest.

Its strongest contribution is a very good central question:
- is the paper showing a mechanism, or merely proposing one?

Best use:
- mechanism extraction prompts
- mechanism page writing rules
- science summary guardrails
- reviewer/operator checks

This is the best AG mechanism document for immediate reuse.

### 5. Theory-sensitive VOI spec

Usable because it broadens VOI beyond predictive change.

Best use:
- gap cards
- research-prioritisation surfaces
- theory-guide and study-recommendation UIs

Important implication:
- mechanism clarification and theory discrimination can be high-value even when predictive change is small

## What is usable but only with caution

### Theory hierarchy implementation / quickstart

These docs are useful as:
- lookup scaffolding
- alias resolution
- preliminary browse structure
- provisional theory-family grouping

But they are risky if treated as:
- final ontology truth
- final parentage of theories
- a basis for public-facing certainty about what explains what

Main concerns:
1. several T1/T1.5 mappings are plausible but contestable
2. the current hierarchy is stronger as an engineering convenience than as settled theory
3. automatic upward annotation can make the UI look more certain than the papers justify
4. the existing theory-guide corpus already shows that many influential theories are historically layered, superseded, or mixed in status

So:
- keep the hierarchy as internal scaffolding
- expose it publicly only with explicit tentativeness and commentary

## What should not drive the architecture directly

### Gap TODOs as user-facing structure

`THEORY_IMPLEMENTATION_GAP_TODO_2026-03-22.md` is useful for backend planning.
It should not directly shape theory-guide prose or student-facing architecture.

Reason:
- it is about mathematical implementation gaps
- not about explanatory presentation

## Architectural decisions from this review

### 1. Theory guides stay separate from mechanism guides

Reason:
- AG’s mechanism cheat sheet reinforces the difference between:
  - theory cited
  - mechanism tested
  - mechanism inferred in discussion

This supports the KA rule:
- do not collapse theory pages and mechanism pages into one object

### 2. Theory hierarchy becomes a provisional navigation aid

Reason:
- it is useful for grouping and linking
- it is not yet reliable enough to be the final explanatory authority

This means:
- okay for browse filters
- okay for related-theory suggestions
- not okay as silent explanatory truth

### 3. Theory-layer SCs should come from AG’s test matrix and repair plan

Reason:
- these are the strongest AG documents
- they are much better than relying on vague “theory integration” claims

### 4. Mechanism pages should use AG’s mechanism discipline explicitly

Mechanism pages should always state:
1. what pathway is proposed
2. what evidence surface supports it
3. whether the mechanism is directly tested or only inferred

That rule should be canonical.

## Incorporation into Knowledge Atlas

### Immediate

1. patch theory-guide architecture to mention companion mechanism guides
2. add mechanism-guide data contract
3. treat AG test/repair docs as SC sources for rebuild and theory-heavy UI layers
4. keep theory hierarchy marked as provisional

### Near-term

1. build a Theory Explorer bridge page
2. build a Mechanism Explorer bridge page
3. classify existing `/Users/davidusa/REPOS/theory_guides` guides into:
- current
- bridge
- older
- deferred

### Later

1. review contested T1/T1.5 mappings with a focused theory panel
2. only then promote more of the hierarchy into public-facing explanatory text

## Best current reuse judgment

If I had to rank AG’s theory/mechanism contributions by immediate value:

1. `ATLAS_THEORY_TO_LAYER_TEST_MATRIX_2026-03-17.md`
2. `ATLAS_THEORY_LAYER_REPAIR_PLAN_2026-03-17.md`
3. `CHEAT_SHEET_MECHANISM_MEDIATION_2026-03-21.md`
4. `ATLAS_ACTIVE_PROGRAM_THEORY_MAP_2026-03-17.md`
5. `ATLAS_THEORY_SENSITIVE_VOI_SPEC_2026-03-14.md`
6. `THEORY_HIERARCHY_IMPLEMENTATION.md`
7. `THEORY_HIERARCHY_QUICKSTART.md`
8. `THEORY_IMPLEMENTATION_GAP_TODO_2026-03-22.md`

That is the order I would use for incorporation.
