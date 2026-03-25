# Topic Selection Policy

Date: 2026-03-24
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`
Purpose: define how topics should be selected, typed, and promoted for the Knowledge Atlas and for course-facing use

## Problem

The current KA topic page uses a hand-curated list of 20 topics.
That list is intellectually promising, but it currently mixes several different topic types without naming them.

Examples in the current list:
- environmental effect topics
- physiological topics
- neuroscience / mechanism topics
- broad theory topics
- methodology / replication topics

This is not wrong.
But without a selection policy, the page will drift.

## Core principle

A topic should not be included only because:
- it is experimentable for students
- it has a cluster in the data
- it is theoretically interesting
- it has high VOI

Instead, topics should be selected from a **hybrid policy**:
1. data substrate
2. editorial judgment
3. product purpose

## Topic types

### 1. Atlas topic
Definition:
- a visible topic appropriate for the whole Knowledge Atlas

Selection criteria:
- scientifically important
- enough corpus support or structured uncertainty to say something meaningful
- useful for browsing or orientation
- not only a course exercise prompt

### 2. Course starter topic
Definition:
- a topic shown to students to help them choose an area for a bounded project

Selection criteria:
- tractable
- experimentable
- pedagogically useful
- likely to lead to a manageable question and method choice

### 3. Mechanism / neuroscience topic
Definition:
- a topic organized around a pathway, subsystem, or mechanistic explanation rather than only a surface environmental factor

Selection criteria:
- enough grounded literature or structured theory context to say something nontrivial
- not merely speculative
- clearly caveated if evidence is sparse

### 4. Theory topic
Definition:
- a topic organized around a theory or explanatory framework

Selection criteria:
- the system has enough theory-linked content to make the page useful
- theory fidelity is acceptable or visibly caveated
- theory terms and canonical theory assignments can be distinguished

### 5. Methodology topic
Definition:
- a topic organized around replication, methods, measurement, or study design quality

Selection criteria:
- cross-paper methodological relevance
- useful for both Atlas understanding and course work

## Selection substrate

### Data substrate
Topics should begin from one or more of:
- finding clusters
- paper theory frames
- structured result rows
- method-claim distributions
- gap/VOI outputs

### Editorial layer
Then apply editorial judgment to:
- merge noisy clusters
- split over-broad clusters
- create theory/mechanism topics where the system genuinely has something to say
- suppress topics that are merely artifacts of extraction noise

## Promotion rule

Promotion to a visible topic should require at least one of:
1. strong evidence density
2. high strategic uncertainty / VOI
3. strong theoretical relevance
4. strong mechanistic relevance
5. clear pedagogical value

Prefer topics that satisfy more than one criterion.

## What should not automatically become a visible topic

1. every finding cluster
2. every theory name
3. every mechanism phrase
4. every narrow antecedent/consequent pairing

Those may remain:
- internal clusters
- filters
- secondary browse options
- article-detail annotations

## Current KA list: reclassification

The current 20 static KA topics break down roughly like this.

### Mechanism / neuroscience topics
- LC-NE System & Sustained Attention
- Default Mode Network & Fatigue
- PFC Function & Environmental Load
- Neuroscience of Attention Pathways

### Environmental / physiological Atlas topics
- Temperature & Thermal Comfort
- Indoor Plants & Air Quality
- Color & Spatial Design
- Crowding & Social Density
- Lighting & Circadian Rhythms
- Physical Activity & Cognition
- VDT Fatigue & Visual Ergonomics
- Open Office & Noise Distraction
- Nature Views & Stress Recovery
- Biophilic Design
- Wayfinding & Spatial Cognition

### Cognitive / mixed topics
- Multitasking & Task Switching
- Executive Function & Environment
- Cognitive Load & Workspace Design

### Theory / methodology topics
- Attention Restoration Theory
- Replication & Effect Sizes

## Judgment on the current KA list

It is better than a purely student-experiment topic list because it already includes:
- theory
- mechanism
- neuroscience
- methodology

That is a strength and should be preserved.

But it currently lacks explicit typing.
That means the page risks pretending all topics are the same kind of object.
They are not.

## Recommended page behavior

### Atlas Topics page
Show a mixed set of topic types, but label them.
Example visible badges:
- `environment`
- `mechanism`
- `theory`
- `methodology`
- `course-friendly`

### Course Starter view
Provide a filter or companion view that emphasizes:
- tractable topics
- good student project candidates
- topics with clearer operational pathways

### Mechanism / theory visibility
These should stay on the Atlas topic surface if:
- the system has something meaningful to say
- caveats are visible where needed

## Working rule for implementation

Right now:
- the KA page is a hand-curated editorial seed
- the recovery topic catalog is more cluster-driven

Next step:
- combine them

The policy should be:
1. start from cluster-derived substrate
2. apply editorial topic typing and promotion
3. expose different filtered views for Atlas browsing and course browsing

## Immediate implementation implications

1. Add topic-type metadata to the KA topic list.
2. Distinguish `Atlas topics` from `Course starter topics`.
3. Allow theory and mechanism topics to remain first-class.
4. Do not force every visible topic to be a student experiment candidate.
5. Use finding clusters as substrate, not as the final visible ontology.
