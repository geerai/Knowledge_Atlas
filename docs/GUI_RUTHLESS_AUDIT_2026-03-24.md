# Knowledge Atlas Ruthless GUI Audit

Date: 2026-03-24
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`
Scope: root Knowledge Atlas pages, embedded `Designing_Experiments` pages, course site, and GUI integration implications for the next rebuild

## What "ruthless" means here

Ruthless does not mean hostile.
It means:
- prioritize the failures that would mislead users, fragment the product, or waste the remaining class-prep time
- distinguish cosmetic issues from structural ones
- judge the site as a system, not as isolated pages
- prefer a working unified surface over a larger pile of disconnected good-looking pages

## Current page inventory

### Root Knowledge Atlas pages
Count: `22`

Main families visible now:
- authentication / home
- contributor/admin surfaces
- research discovery surfaces
- student assignment surfaces
- demo/meta pages

### Embedded Designing Experiments pages
Count: `12`

These remain valuable, but they now live inside the KA repo as a legacy/parallel surface.

## Highest-level finding

The repo now contains **three overlapping site families**:

1. `Knowledge Atlas main site`
- `ka_home`, `ka_topics`, `ka_evidence`, `ka_gaps`, `ka_dashboard`, etc.

2. `Contributor / management / assignment surfaces`
- `ka_articles`, `ka_article_propose`, `ka_tag_assignment`, `ka_tagger`, `ka_approve`, `ka_datacapture`

3. `Embedded course / legacy experiment design site`
- `Designing_Experiments/*.html`
- especially `cogs160_spring_2026_site.html`, `experiment_wizard.html`, `knowledge_navigator.html`, `en_navigator.html`, `bn_navigator.html`

This is not yet one coherent product.
It is a promising but fragmented federation.

## Strongest current assets

1. The visual language is already stronger than average.
- warm palette
- serious tone
- strong page identity
- not generic SaaS styling

2. The page repertoire is broad enough to support the class.
- topics
- evidence
- gaps
- sensors
- assignment pages
- experiment-design pages

3. The contributor/admin side exists.
- this matters because the class is partly about building and curating the system, not only consuming it

4. The image tagger already exists as a real page.
- this is good, because it means integration is an IA problem, not a greenfield build

## Structural failures

### 1. The sitemap is obsolete
The current sitemap still describes the system as if it were a 14-page prototype.
That is no longer true.

Implication:
- navigation and planning documents are lagging the actual repo
- the system risks confusing both builders and students

Severity: high

### 2. There is no single authoritative public/workflow story yet
Right now a user could reasonably ask:
- where do I start?
- am I in the main atlas, the contributor surface, or the course tool?
- which pages are canonical and which are legacy?

Implication:
- strong pages still do not add up to a coherent site

Severity: high

### 3. The class site and the main site are not yet integrated conceptually
The class site is still its own strong narrative object.
The main site is its own strong interface family.
They are related, but not yet made to feel like one environment.

Implication:
- students may learn the course as one thing and the Atlas as another
- contributor work may remain detached from the live Atlas workflows

Severity: high

### 4. Evidence-heavy pages are still mostly static prototypes
Pages like:
- `ka_topics.html`
- `ka_evidence.html`
- `ka_gaps.html`

show the intended product shape, but they are not yet meaningfully connected to the current rebuild outputs.

Implication:
- these pages are useful for design review, not yet for real system use

Severity: high

### 5. The image tagger is stranded in contributor/course logic
The image tagger exists, but it is not yet clearly part of the main Atlas mental model.

Implication:
- a genuinely important part of the annotation pipeline still feels peripheral

Severity: medium-high

### 6. Root and embedded DE pages overlap in function
Examples:
- root `ka_hypothesis_builder.html`
- embedded `Designing_Experiments/hypothesis_builder.html`

Implication:
- duplicate concepts will confuse builders and users unless one surface becomes clearly canonical and the other clearly legacy or course-specific

Severity: high

## What should not be done

1. Do not rewrite everything before integration.
2. Do not hook every page to live data before we define which pages are canonical first.
3. Do not let CW and Codex both edit the same site family at the same time without a clean split.
4. Do not wait for gold extraction before wiring any real data into the UI.

## Database hookup judgment

### Can the database be hooked up before everything has content?
Yes.
That is the correct move.

But the hookup should happen in **layers**:

#### Hook up now
Pages where real data matters immediately:
- `ka_topics.html`
- `ka_evidence.html`
- article detail / abstract / results display surfaces
- `ka_gaps.html`

#### Stub or partial for now
Pages where layout/IA is more important than full corpus wiring:
- class-facing assignment pages
- management/contributor assignment orchestration pages
- some admin surfaces

### Should the hookup wait for the next rebuild?
For evidence-heavy pages, mostly yes.

Best approach:
- define adapters now
- use a stable mock contract during GUI integration
- switch the adapters to the new rebuild outputs as soon as the next rebuild is ready

So the answer is:
- do not wait to define the integration shape
- do wait to treat the current content layer as authoritative for the major evidence pages

## Recommended division of labor

### CW
Best use of CW now:
- revise the class site
- tighten course narrative
- bring the course-facing pages into alignment with the new unified IA
- help rationalize what remains course-specific versus what should become shared Atlas UI

### Codex
Best use of Codex now:
- review the whole current site architecture
- define the unified IA
- integrate the main KA pages
- connect the evidence-heavy pages to the rebuilt data contracts
- pull the image tagger into the main site map and navigation
- define and enforce the rebuild/data/UI contract

This is the right split because:
- CW has already done extensive page work and course shaping
- Codex is already deep in the extraction/rebuild/data semantics and can bridge those into the UI

## Immediate conclusions

1. Yes, the class site should be revised in parallel while the main site is unified.
2. Yes, the DB/data layer can begin to be integrated before every page is content-complete.
3. The next rebuild should become the first real evidence-content source for the live research pages.
4. The image tagger should be brought into the main KA information architecture now, not later.
5. The next planning artifact should be a sprint plan that separates:
- IA unification
- class-site revision
- data/rebuild integration
- extraction/rebuild hardening
