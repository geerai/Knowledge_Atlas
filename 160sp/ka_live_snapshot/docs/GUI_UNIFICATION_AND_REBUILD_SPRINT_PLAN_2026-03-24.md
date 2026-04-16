# GUI Unification And Rebuild Sprint Plan

Date: 2026-03-24
Primary repos:
- GUI: `/Users/davidusa/REPOS/Knowledge_Atlas`
- Extraction / rebuild: `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery`

## Planning principle

The class timeline changes the strategy.

We should aim for:
- a coherent working site soon
- with transparent imperfections in content
- while rebuild and extraction continue to improve underneath it

The wrong strategy now would be:
- wait for gold everywhere before site integration

## Operating assumptions

1. Streamlit is the default framework for new internal analytic tools.
2. Existing static HTML pages in `Knowledge_Atlas` remain valid implementation surfaces during the unification phase.
3. The next rebuild should supply the first real content layer for the evidence-heavy GUI pages.
4. Content perfection is not required before UI integration, but provenance and uncertainty must remain visible.

## Success conditions for the whole plan

The program succeeds when:
1. there is one coherent site map and navigation story
2. students can move through the class site without falling into dead-end legacy paths
3. at least the key evidence-heavy pages use real rebuilt data
4. image tagging is part of the main site, not stranded in a course side lane
5. theory guides are architecturally accounted for, including an `Older Theories` area under T1.5
6. neural underpinnings are a visible first-class layer rather than buried theory metadata
7. the rebuild pipeline is auditable and checked against current theory commitments
8. SCs fail loudly when data or rebuild behavior is broken

## Sprint 0 — Severe audit and canon definition

Goal:
- define what is canonical, what is legacy, and what is shared

Deliverables:
- ruthless GUI audit
- canonical site-family map
- page ownership table
- legacy/deprecated page list
- unified sitemap spec

Success conditions:
- every page belongs to one of:
  - canonical main site
  - course-specific site
  - contributor/admin workflow
  - legacy / to-be-retired
- there are no ambiguous duplicate owners for major page families

Notes:
- this sprint is effectively started by the current audit

## Sprint 1 — Information architecture unification

Goal:
- make the site one system instead of three overlapping ones

Key work:
1. update `ka_sitemap.html` to reflect the real repo surface
2. define a top-level navigation model for:
- Atlas / Research
- Contribute / Manage
- Course / Studio
3. integrate `ka_tagger.html` and `ka_tag_assignment.html` into the main site map
4. explicitly mark embedded `Designing_Experiments` pages as:
- canonical shared tool
- course-only
- or legacy

Success conditions:
- a user can understand where to start
- the sitemap matches reality
- major duplicate page families are resolved conceptually

Ownership:
- Codex leads
- CW reviews for course coherence

## Sprint 2 — Class site revision

Goal:
- make the class site fit the unified product and the near-term teaching needs

Key work:
1. revise `cogs160_spring_2026_site.html`
2. decide which course pages remain separate and which become shared Atlas pages
3. ensure assignments point students into the main Atlas where appropriate
4. tighten milestones, roles, and pathways for the actual class timeline

Success conditions:
- course narrative is coherent
- students know which pages are class tools and which are Atlas tools
- assignment tracks reflect the current system, not an older one

Ownership:
- CW leads
- Codex sets integration constraints and shared IA rules

## Sprint 3 — Data contract and adapter layer

Goal:
- define how the GUI will consume rebuilt outputs before full content hookup

Key work:
1. define page-level data contracts for:
- topics
- evidence/results
- article detail
- gaps
- theory frame
- theory guides
 - neural underpinnings
2. create adapter layer against mock or partial data first
3. specify status flags for imperfect content:
- provisional
- rebuilt from current corpus
- theory tentative
- constructed result table
- subject count missing

Success conditions:
- the GUI can be wired to stable interfaces even while rebuild content evolves
- imperfect data is visible as imperfect

Ownership:
- Codex leads

## Sprint 4 — Rebuild hardening and theoretical alignment

Goal:
- produce a rebuild that is robust enough to power the first live evidence pages

Key work:
1. freeze a Mathpix / extraction corpus for the next visible site iteration
2. rerun extraction and summaries with the latest method/result/theory improvements
3. run rebuild with explicit inspection of every stage
4. verify SCs against current theory commitments, especially:
- warrant / omega behavior
- grounding discipline
- theory handling
- subject-count handling
- result-structure preservation
5. update SC set where it is stale or underpowered

### Required checks in this sprint

Preflight checks:
- corpus manifest correctness
- article type distribution sanity
- abstract coverage report
- subject-count coverage report
- direction-of-effect normalization report
- theory-frame sanity report

Rebuild checks:
- hard-gate pass/fail visibility
- BN edge creation
- annotation volume and diversity
- IV/DV mapping coverage
- warrant distribution sanity
- grounding-cluster audit
- CCI structural readiness

Post-rebuild UI checks:
- adapters can read the outputs
- article pages can render abstract, results, and figures
- topic pages can render real paper/topic counts

Success conditions:
- the rebuild is not merely successful, but trustworthy enough to drive the first live GUI layer

Ownership:
- Codex leads
- panel review recommended at sprint end

## Sprint 5 — First live data hookup

Goal:
- connect the first truly important GUI pages to rebuilt data

Pages to wire first:
1. `ka_topics.html`
2. `ka_evidence.html`
3. article detail / abstract / results surface
4. `ka_gaps.html`
5. image tagger / tag assignment status surfaces if data is ready

Guidance:
- not every page needs full live data in this sprint
- prioritize the pages that prove the site works as a research system

Success conditions:
- the site shows real papers, real summaries, real result structures, and real provenance on key pages
- data caveats are visible where needed

Ownership:
- Codex leads

## Sprint 6 — Theory guides and neural-underpinnings architecture

Goal:
- make theory guides and neural-underpinnings guides first-class progressive-disclosure layers

Key work:
1. define T1 guide template
2. define T1.5 bridge guide template
3. define `Older Theories` template and placement under T1.5
4. define pathway and neural-system guide templates
5. identify first candidate theory guides and pathway guides
6. wire theory-guide and pathway placeholders into the IA and article/topic linking model
7. create article-finder pathway assignments seeded by panel-proposed classic papers

Success conditions:
- theory is not only a tag layer
- older theories are preserved critically rather than erased or flattened
- neural underpinnings are visible as their own explanatory layer
- the system can later explain what was good, bad, superseded, directly measured, and still inferred

Ownership:
- Codex leads
- panel review recommended for theoretical fairness and clarity

## Sprint 7 — Image tagger integration

Goal:
- bring image tagging into the main product story

Key work:
1. put image tagging on the main site map
2. connect image-tag tasks to contributor workflows
3. expose why image tagging matters to the Atlas as a whole
4. if possible, expose tagged-image outputs or review states in a visible way

Success conditions:
- image tagging no longer feels like a side quest
- contributors understand how it fits into annotation and analysis

Ownership:
- Codex leads on integration
- CW can help with contributor-facing framing if needed

## Sprint 8 — Iteration loop to gold

Goal:
- tighten extraction and summaries by using the live site as feedback pressure

Loop:
1. inspect weak outputs in the site
2. patch extraction / summary logic
3. rebuild
4. re-render
5. compare

This sprint is ongoing.

Success conditions:
- the visible site gets steadily more correct
- regressions are caught by SCs and UI-level spot checks

## Recommended panel use

### Panel 1: after Sprint 1
Use a product/IA panel to challenge the unified navigation and the separation between:
- main Atlas
- course
- contributor/admin

### Panel 2: after Sprint 4
Use a theory/rebuild quality panel to challenge whether the rebuilt outputs are actually good enough to drive live pages.

This second panel matters because the biggest remaining risk is epistemic, not visual.

### Panel 3: after Sprint 6
Use a theory-guide panel to review fairness, supersession logic, and whether older theories are being presented critically but constructively.

## Immediate next actions

1. Codex
- produce canonical site-family map
- update sitemap spec
- define first data contracts

2. CW
- revise class site in parallel against the new IA
- identify which course pages remain distinct versus shared

3. Codex + CW
- agree on duplicate-page dispositions
- especially around hypothesis builder / navigators / experiment-design tools

4. Codex
- define rebuild preflight and SC audit checklist for the next content run

## Bottom line

Yes, parallel work is the right move.

The correct near-term structure is:
- CW revises the class-facing surface
- Codex unifies the main site and connects it to rebuilt data
- the rebuild is hardened in parallel with visible SCs and theory-aware checks
- the image tagger is pulled into the main site now rather than deferred
