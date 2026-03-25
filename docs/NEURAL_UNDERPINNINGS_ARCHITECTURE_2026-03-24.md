# Neural Underpinnings Architecture

Date: 2026-03-24
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`
Purpose: define the explicit neural-underpinnings layer for the Atlas and connect it to article-finding work

## Why this needs its own lane

Neural underpinnings should not be hidden:
- under generic theory
- inside methods
- or inside mechanism notes that only experts will find

This material is central because the Atlas is trying to explain:
- what systems and pathways are implicated
- what the evidence really bears on
- where explanation is direct versus inferential

So the site should have a large explicit layer for neural underpinnings.
This may begin as a top-level nav item.

## Starting point

The initial substrate should come from:
1. pathways proposed by the panels when they created the mechanisms
2. classic articles those panels pointed to
3. the existing theory and mechanism architecture

The starting point is not “all neural literature.”
It is:
- the pathway families the Atlas already thinks matter
- then deeper literature collection around each one

## Progressive disclosure model

Each neural-underpinnings page should support at least three levels:

### Level 1 — Quick orientation
- one-paragraph plain-language explanation
- what this pathway is about
- where it matters in architecture/environment research
- confidence band

### Level 2 — Structured mechanism view
- component systems
- ordered or branching pathway steps
- directly measured versus inferred steps
- linked theories
- linked topics
- classic papers

### Level 3 — Research depth
- detailed evidence table
- historical development
- disputes and limitations
- missing evidence
- candidate next-study directions

## Neural object types

### 1. Pathway Guide

Required fields:
- `pathway_id`
- `pathway_name`
- `plain_language_summary`
- `linked_theories[]`
- `linked_topics[]`
- `systems_involved[]`
- `key_steps[]`
- `directly_measured_steps[]`
- `inferred_steps[]`
- `classic_papers[]`
- `current_limitations[]`
- `why_it_matters`
- `guide_confidence`

### 2. Neural System Guide

Required fields:
- `system_id`
- `system_name`
- `system_role`
- `linked_pathways[]`
- `linked_theories[]`
- `measurement_options[]`
- `classic_papers[]`
- `known_limits[]`
- `guide_confidence`

### 3. Pathway Reading List

Required fields:
- `pathway_id`
- `classic_anchor_papers[]`
- `follow_on_papers[]`
- `recent_review_papers[]`
- `why_each_matters[]`
- `collection_status`

## What counts as a good page

A strong neural-underpinnings page should answer:
1. what pathway is being claimed?
2. what parts are directly supported?
3. what parts are inferred?
4. what classic papers anchor this claim family?
5. what would we need to read next to deepen the literature?

## Relationship to theory guides

Theory guides and neural-underpinnings pages should cross-link, but they are not the same thing.

Theory guide:
- explanatory framework
- conceptual scope
- historical and current status

Neural-underpinnings page:
- systems
- pathways
- evidence surfaces
- measurement possibilities

## Relationship to mechanisms

Mechanism pages and neural-underpinnings pages overlap, but the emphasis differs.

Mechanism page:
- pathway or productive chain in the context of findings

Neural-underpinnings page:
- broader neural system/pathway family
- classic literature
- system-level grounding

## Integration with COGS 160 article finding

This layer should directly shape article-finding work.

The article-finding students should not search randomly.
They should be assigned pathway families.

### Workflow

1. choose a pathway family from the panel-proposed list
2. identify the classic anchor articles already proposed by panels
3. retrieve those first
4. then expand outward:
- cited-by
- recent review papers
- direct measurement papers
- mediation/pathway tests
- related system papers
5. record what the pathway page still lacks

### Student deliverables

For each assigned pathway family:
- `classic paper set`
- `follow-on paper set`
- `one-paragraph pathway explanation`
- `what is directly measured vs inferred`
- `what remains unclear`

## Near-term implementation rule

We do not need a full polished neural explorer immediately.
But the architecture should reserve it now.

Minimum near-term requirement:
1. add `Neural Underpinnings` to the nav architecture
2. define pathway guide and reading-list objects
3. assign article-finding work by pathway family
4. start with classic articles the panels already proposed

## Recommended next move

1. compile the initial panel-proposed pathway list
2. create a first pathway inventory sheet
3. connect that inventory to article-finder assignments
4. later build the visible Neural Underpinnings Explorer from that substrate
