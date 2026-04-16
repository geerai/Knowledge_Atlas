# Theory Guides Integration Plan

Date: 2026-03-24
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`
External source currently in use: `/Users/davidusa/REPOS/theory_guides`

## Current reality

There is already an existing theory-guide set at:
- `/Users/davidusa/REPOS/theory_guides`

Current files:
- `index.html`
- `chronobiology_guide.html`
- `cognitive_map_guide.html`
- `cpted_guide.html`
- `episodic_memory_guide.html`
- `flow_theory_guide.html`
- `goldilocks_principle_guide.html`
- `kaplan_preference_guide.html`
- `pad_model_guide.html`
- `place_attachment_guide.html`
- `privacy_regulation_guide.html`
- `proxemics_guide.html`

These are already written as progressive-disclosure guides with multiple reading levels.
That is important.
The core idea was right.

## Architectural implication

We should not reinvent theory guides as if none exist.
Instead:
1. preserve the current guide set
2. classify the guides within the new architecture
3. link them into the main KA information architecture
4. later migrate or wrap them into the canonical KA repo when appropriate

## Current classification judgment

The existing guide set appears to contain a mix of:
- current or still-useful theories
- older theories that remain influential
- theories that ATLAS currently marks as rejected or deferred

This is exactly why the new architecture needs:
- T1 current guides
- T1.5 bridge guides
- T1.5 `Older Theories`

## Most important immediate reclassification

Based on the current theory-guide index and statuses, several existing guides are best understood not as main current T1 guides, but as `Older Theories` candidates.

Examples likely in that category:
- Chronobiology
- Cognitive Map Theory
- CPTED / Defensible Space
- Proxemics
- Kaplan Preference Matrix
- PAD Model
- Privacy Regulation Theory

The right treatment is not deletion.
It is:
- preserve
- explain what they got right
- explain where they are limited
- explain what replaced or absorbed them

## Why this matches the new architecture

Your point is correct:
- many older theories still have real sway in the field
- some still contain useful ideas
- later theories often absorb their strengths

So the UI should not say only:
- `rejected`

It should also say:
- what survives
- why the field moved on
- where the theory still influences practice or interpretation

## Near-term integration rule

### Step 1
Treat `/Users/davidusa/REPOS/theory_guides/index.html` as the current external theory-guide index.

### Step 2
Add a `Theory Guides` route in the KA architecture and nav model.

### Step 3
Classify each existing guide as one of:
- `current`
- `bridge`
- `older`
- `deferred`

### Step 4
For guides in the `older` class, ensure the UI framing includes:
- strengths
- weaknesses
- supersession
- surviving contributions

## Migration guidance

Right now the guides live outside the canonical KA repo.
That is acceptable temporarily, but not ideal.

Longer term, one of these should happen:
1. migrate them into `Knowledge_Atlas` as canonical content
2. or keep them external but maintain a tracked registry and link layer

The first is cleaner.
The second is acceptable only if the content is stable and intentionally maintained.

## Recommended next move

Create a small `Theory Guides` bridge in KA that:
- points to the existing guide index
- introduces the distinction between current theories and older theories
- prepares the ground for eventual full integration

## AG docs worth using

The following AG documents are useful inputs and should be treated as support material for the KA theory/mechanism architecture:

Strong inputs:
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/ATLAS_THEORY_TO_LAYER_TEST_MATRIX_2026-03-17.md`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/ATLAS_THEORY_LAYER_REPAIR_PLAN_2026-03-17.md`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/ATLAS_ACTIVE_PROGRAM_THEORY_MAP_2026-03-17.md`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/ATLAS_THEORY_SENSITIVE_VOI_SPEC_2026-03-14.md`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/CHEAT_SHEET_MECHANISM_MEDIATION_2026-03-21.md`

Use with caution:
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/THEORY_HIERARCHY_IMPLEMENTATION.md`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/THEORY_HIERARCHY_QUICKSTART.md`

Why caution is needed:
- the hierarchy documents are useful as a provisional lookup and navigation scaffold
- but they are too assertive to be treated as final ontology truth
- several T1/T1.5 mappings are plausible but not yet stable enough for automatic explanatory presentation in the public-facing UI

## Incorporation rule

1. Use the theory-hierarchy docs for:
- alias resolution
- browse scaffolding
- provisional theory-family grouping

2. Use the repair-plan and test-matrix docs for:
- success conditions
- ruthless audits
- rebuild-layer verification

3. Use the mechanism cheat sheet for:
- mechanism-claim extraction discipline
- mechanism-page writing rules
- wording discipline around mediation versus inference

4. Use the theory-sensitive VOI spec for:
- gap cards
- theory guides
- study recommendation surfaces

5. Do not use any current AG theory map as if it were already a finished theory guide corpus.
