# Unified Navigation Model

Date: 2026-03-24
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`

## Purpose

Define the top-level navigation model that unifies the current site families without pretending they are all the same kind of page.

## Audience reality

The likely early users are not mostly:
- neuroscientists
- theory specialists

They are more likely to begin with:
- literature exploration
- topics
- findings
- article browsing
- assignment-driven task entry

So the information architecture and the visible primary navigation should not force theory or neural entry too early.

## Top-level model

The unified top level should be:

1. `Atlas`
- the main research/discovery surface

2. `Contribute`
- contributor and operational workflows

3. `Theory Guides`
- theory, explanatory-guide, and older-theory surfaces

4. `Neural Underpinnings`
- pathways, systems, mechanism families, and neural evidence surfaces

5. `Course / Studio`
- class-facing and experiment-design surfaces

6. `About / Docs`
- sitemap, meta pages, orientation

## Primary public-facing nav recommendation

The internal site architecture can keep the six lanes above.
But the visible primary nav for most users should lead with:

1. `Explore the Literature`
2. `Contribute`
3. `Course / Studio`
4. `About`

Then `Explore the Literature` should open structured subnav for:
- Topics
- Evidence
- Gaps
- Article Search
- Theory Guides
- Neural Underpinnings

Reason:
- this better matches non-expert starting behavior
- it keeps theory and neural depth available
- it avoids over-weighting specialist language at first contact

Architectural rule:
- `Theory Guides` and `Neural Underpinnings` remain top-level lanes in the IA
- but they may be exposed to most users through the `Explore the Literature` umbrella

## Adaptive nav after login

The nav may change after signup/login based on:
- user role
- declared preference
- current task lane

This is a good fit for the expected user population.

Recommended signup preference options:
1. `Explore the literature`
2. `Build or test experiments`
3. `Contribute to the Atlas`
4. `Theory and mechanisms`

Recommended rule:
- before login: broad public nav led by `Explore the Literature`
- after login: preserve the same IA, but promote the user's preferred lane in the primary nav order

Example:
- a student choosing `Explore the literature` sees Topics, Evidence, Gaps, and Article Search first
- a contributor choosing `Contribute to the Atlas` sees Dashboard, Articles, Tagging, and Approval first
- a theory-oriented user choosing `Theory and mechanisms` sees Theory Guides and Neural Underpinnings promoted

Important constraint:
- adaptive nav should reorder emphasis, not create a different ontology for different users
- cross-lane handoffs should remain visible

## Anonymous user-type selection

Adaptive nav should not require login.

If a visitor chooses a user type before logging in, the system should:
- store that choice locally
- adapt the navbar and featured entry points immediately
- allow the choice to be changed easily

Recommended anonymous user-type choices:
1. `Student explorer`
2. `Researcher`
3. `Contributor`
4. `Instructor`
5. `Practitioner`
6. `Theory / mechanism explorer`

Recommended behavior:
- before any choice: broad default nav led by `Explore the Literature`
- after anonymous choice: reorder nav, landing cards, and calls to action for that user type
- after login: keep the same preference unless the account profile already stores a stronger preference

Preference precedence:
1. explicit in-session choice made this visit
2. saved account preference for logged-in user
3. saved anonymous local preference
4. broad default public nav

Important rule:
- anonymous personalization should feel like orientation, not lock-in
- the system should always provide a visible `Switch mode` control

## Atlas section

Primary pages:
- `ka_home.html`
- `ka_topics.html`
- `ka_demo_v04.html`
- `ka_evidence.html`
- `ka_gaps.html`
- `ka_article_search.html`
- `ka_sensors.html`
- `ka_question_maker.html`
- `ka_hypothesis_builder.html`

This section answers:
- what does the literature say?
- where are the gaps?
- what topic should I explore?
- what evidence supports this?
- how might I move toward a study?

## Contribute section

Primary pages:
- `ka_dashboard.html`
- `ka_articles.html`
- `ka_article_propose.html`
- `ka_datacapture.html`
- `ka_tagger.html`
- `ka_tag_assignment.html`
- `ka_approve.html`

This section answers:
- what work is assigned?
- how do I contribute?
- how do I propose articles?
- how do I tag images?
- how do instructors approve contributors?

Important rule:
- image tagging belongs here visibly, not as a hidden course-side function

## Theory Guides section

Planned primary surfaces:
- current external guide index at `/Users/davidusa/REPOS/theory_guides/index.html`
- future Theory Explorer / theory-guide pages
- topic-linked theory topics where content is sufficient
- older-theories subsection under T1.5

This section answers:
- what does this theory claim?
- what is still good about it?
- what are its weaknesses?
- what replaced or absorbed it?

Important rule:
- theory guides should distinguish current T1 theories from T1.5 bridge theories and older theories

## Neural Underpinnings section

Planned primary surfaces:
- future Neural Underpinnings Explorer
- pathway pages seeded from panel-proposed mechanisms
- classic-paper reading lists for each pathway
- links from theories, topics, and article pages into relevant neural pathways

This section answers:
- what neural systems are plausibly involved?
- what pathway is proposed?
- which steps are directly measured versus inferred?
- what classic papers anchor this mechanism family?
- where is the literature still thin?

Important rules:
- this lane should be large and explicit, not buried
- it should use progressive disclosure
- it should begin from panel-proposed pathways, then deepen through targeted literature finding
- it should not imply that every cited theory already has strong neural evidence

## Course / Studio section

Primary pages:
- `Designing_Experiments/cogs160_spring_2026_site.html`
- `Designing_Experiments/course_pilot.html`
- `Designing_Experiments/knowledge_navigator.html`
- `Designing_Experiments/experiment_wizard.html`
- `Designing_Experiments/en_navigator.html`
- `Designing_Experiments/bn_navigator.html`
- `Designing_Experiments/theory_and_experiment_design.html`
- `Designing_Experiments/methods_taxonomy.html`
- `Designing_Experiments/measurement_instruments.html`
- `Designing_Experiments/sensor_catalogue.html`

This section answers:
- how do students learn the space?
- how do they compare methods and theories?
- how do they design experiments?

## About / Docs section

Primary pages:
- `ka_sitemap.html`
- `ka_gui_assignment.html`
- `ka_article_finder_assignment.html`
- supporting docs where linked

## Routing rules

### Public default entry
`ka_home.html`

### Research default entry after orientation
`ka_topics.html`

### Contributor default entry after login
`ka_dashboard.html`

### Course default entry
`Designing_Experiments/cogs160_spring_2026_site.html`

## Rules for nav design

1. Atlas, Contribute, Theory Guides, Neural Underpinnings, and Course / Studio should be visible as distinct lanes.
2. The current lane should always be obvious.
3. A page should not pretend to belong to two lanes at once.
4. Cross-links between lanes should be explicit handoffs, not silent context switches.
5. The nav should preserve the current KA aesthetic and page seriousness.
