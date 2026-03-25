# Theory Guides Architecture

Date: 2026-03-24
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`
Purpose: define how theory guides should appear in the Knowledge Atlas as a progressive-disclosure layer

## Why this matters

The Atlas should not treat theory as:
- a hidden metadata tag
- a list of names
- or a final unquestioned answer

Theory guides are valuable because they help users:
- understand the historical and conceptual landscape
- see what each theory got right
- see where it is weak or superseded
- understand how later theories absorbed earlier strengths

This is especially important in a field where older theories continue to influence design and interpretation even when they are no longer the best available frameworks.

## Core design principle

Theory guides are a progressive-disclosure layer.
They are not just classification labels.

The goal is not only to say:
- `this paper cites theory X`

The goal is to explain:
- what the theory claims
- what it was good at
- where it breaks down
- what later theories replaced or absorbed it
- what still survives from it

## Existing guide corpus

There is already a live theory-guide set at:
- `/Users/davidusa/REPOS/theory_guides`

This existing corpus should be treated as the starting point for the theory-guide layer, not ignored.

## Main architectural distinction

### T1 section
This is the main current theory layer.

For each T1 theory, the Atlas should eventually provide a guide with:
1. plain-language explanation
2. core commitments
3. what phenomena it explains well
4. key supporting evidence patterns
5. key limitations
6. relation to nearby theories
7. current status in the field
8. why it still matters for design/research

### T1.5 section
This is the intermediate / theory-development layer.

It should include:
- active bridge theories
- candidate reductions or integrations
- newer domain-level explanatory structures
- and a dedicated subsection:
  - `Older Theories`

## Older Theories subsection

This should not be a dumping ground.
It should be a disciplined explanatory archive.

For each older theory, explain:
1. what the theory was trying to explain
2. what it got right
3. what it got wrong or left underspecified
4. why the field moved on
5. which later theories absorbed its strengths
6. whether it still has practical or historical value
7. whether it still holds sway in parts of the field despite theoretical decline

This is important because a user often needs to know not only:
- what the current preferred theory is
but also:
- why earlier theories remain influential

## Theory-guide object types

### 1. Current Theory Guide
Used for active T1 theories.

Required fields:
- `theory_id`
- `theory_name`
- `tier` = `T1`
- `plain_language_summary`
- `core_commitments[]`
- `best_explained_domains[]`
- `key_support_patterns[]`
- `main_limitations[]`
- `related_theories[]`
- `current_status`
- `design_implications[]`
- `guide_confidence`

### 2. Older Theory Guide
Used for older but still relevant theories.

Required fields:
- `theory_id`
- `theory_name`
- `tier` = `T1.5_older`
- `historical_role`
- `what_it_got_right[]`
- `what_it_got_wrong[]`
- `why_the_field_moved_on`
- `what_replaced_it[]`
- `what_survives[]`
- `where_it_still_has_influence`
- `guide_confidence`

### 3. Bridge Theory Guide
Used for live T1.5 theories that connect areas rather than serving only as historical residue.

Required fields:
- `theory_id`
- `theory_name`
- `tier` = `T1.5`
- `bridge_role`
- `connected_theories[]`
- `main_mechanism_or_principle`
- `evidence_status`
- `limitations[]`
- `promotion_status`
- `guide_confidence`

## UI behavior

### Main Theory Explorer
Should expose at least three tabs or filters:
1. `Current Theories`
2. `Bridge / Intermediate Theories`
3. `Older Theories`

### Per-theory page behavior
Every theory guide should answer quickly:
- what is this theory about?
- why did people use it?
- what is still good about it?
- what are its weaknesses?
- what should replace it conceptually?

### Tone rule
Do not mock older theories.
Do not preserve them uncritically.

The correct tone is:
- fair
- historically informed
- conceptually sharp
- explicit about supersession

## Relationship to topics

Some theory guides may also appear as visible Atlas topics.
That is acceptable if:
- the system has enough content to say something useful
- the theory topic is clearly labelled as a theory topic

Not every theory name should become a topic.
But major theories should be explorable.

## Relationship to mechanisms

Theory guides and mechanism guides should not be conflated.

Theory guides answer questions like:
- what explanatory framework is being used?
- what does that framework claim?
- what remains valuable in it?

Mechanism guides answer different questions:
- what pathway is being proposed or tested?
- which step is directly measured versus inferred?
- what is the maturity of the mechanism claim?

The Atlas should therefore treat mechanisms as a companion layer, not as a subheading inside every theory guide.

Near-term rule:
- theory guides may link to mechanism families
- mechanism pages may link back to relevant theories
- but the UI should not imply that a cited theory automatically establishes a mechanism

This matters because many papers:
- cite a theory but do not test a mechanism
- propose a mechanism in discussion without directly measuring it
- inherit older theory language that no longer gives the best mechanistic account

## Relationship to current site architecture

This architecture implies:
1. the unified nav should eventually include a visible theory route
2. article detail pages should link to theory guides where available
3. topic pages should be able to surface theory-guided topics
4. older theories should not be erased from the system simply because they are no longer top-tier

## Status language

The theory-guide layer should not use a raw status like `rejected` without interpretation.
Where a guide is no longer top-tier, the UI should explain:
- what was retained
- what was superseded
- what practical influence remains

## Near-term implementation rule

We do not need full polished theory guides immediately.
But the architecture should reserve space for them now.

Minimum near-term requirement:
- include `Theory Guides` in the architecture and nav model
- reserve a T1 area and a T1.5 `Older Theories` area
- include the required fields in future data-contract planning
- reserve a companion `Mechanism Guides` or `Mechanism Explorer` layer that can distinguish:
  - directly tested mechanisms
  - mediation/moderation claims
  - discussion-level inferred pathways
