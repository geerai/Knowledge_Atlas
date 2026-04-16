# GOOD_IDEAS.md
*Knowledge Atlas Project — Emerging Design and Pedagogical Innovations*
*Maintained by David Kirsh and the KA development team*
*Last updated: 2026-03-23*

---

## Purpose of this file

A running log of ideas that arise during KA development that appear genuinely novel, or that apply established principles in an unusually apt way. Not every idea belongs here — only those worth preserving as intellectual property, sharing with other design teams, or developing into publishable contributions. Each entry includes a brief statement of the idea, its intellectual lineage (what it borrows from and how it differs), and current implementation status.

---

## Idea Log

---

### IDEA-001 · Page Function Specification Link
**Date**: 2026-03-23
**Origin**: Emerged from discussion about whether pages were communicating their purpose clearly enough to GUI evaluation teams.

**The idea**: Every page in the deployed GUI carries an embedded, evaluator-visible button (labeled "⊙ Page function spec") that opens a structured side-panel specifying:
- **Audience**: who is supposed to use this page and when
- **Purpose**: what the page is for in one clear paragraph
- **Workflow position**: where in the user's task sequence this page sits
- **Not for**: explicit statement of what the page is *not* for (deliberately out of scope)
- **Critical path phase**: which backend phase is required to make this page live
- **Evaluation questions**: 4–6 specific questions for the GUI track to use when assessing the page

The button is gated to logged-in users only (invisible to casual visitors), so it does not clutter the user-facing interface. A keyboard shortcut (Shift+F) allows rapid access during evaluation sessions.

**Why this is interesting**: It makes the design intent a persistent, version-controlled artifact that travels with the page rather than living in a separate Figma file, Jira ticket, or Word document. It transforms the evaluation task from open-ended critique to structured assessment against explicit criteria. The evaluation questions are page-specific rather than generic heuristics, which forces the design team to commit — before evaluation — to what they believe each page should accomplish.

**Intellectual lineage and what's different**:
The idea borrows from several established traditions but combines them in a way that has not, to our knowledge, been formalized as a distinct practice:

- *Heuristic evaluation* (Nielsen & Molich, 1990) embeds evaluation criteria in the evaluator's mind or a separate checklist. We embed them in the live UI itself.
- *Design annotation / redlines* document intent in design tools (Figma, Sketch). We move annotations into the deployed product.
- *Contextual help systems* explain how to use a page. We specify what the page is for — a different and arguably prior question.
- *Acceptance criteria* in Agile development specify when a feature is "done." We adapt that concept to an ongoing evaluation instrument rather than a one-time gate.
- *The Schön (1983) reflective practitioner model* in architecture education uses critique structured around design intent. We operationalize design intent as machine-readable structured data rather than verbal articulation.

The closest analogy in practice may be the "usage guidelines" sections in design systems (e.g., Shopify Polaris, IBM Carbon), but those describe reusable components, not complete pages in their workflow context. Our version is page-level, in-situ, and evaluation-question-driven.

**Current implementation**:
- `ka_page_function.js` — shared utility, injects button and panel on all pages
- `window.KA_PAGE_FUNCTION` object defined per page with all fields above
- Implemented on all 14 KA pages as of 2026-03-23
- Gated to `localStorage.ka_logged_in === '1'`; also accessible via `?fnspec=1` URL parameter for demos

**Potential to publish**: Yes. This could be written up as a short paper for a venue like CHI [ACM Conference on Human Factors in Computing Systems] or DIS [ACM Designing Interactive Systems] — "In-Situ Design Rationale: Embedding Function Specifications in Deployed Research Prototypes." The contribution would be the conceptual framework (purpose, audience, not-for, workflow position, eval questions as a five-part specification structure) and evidence from applying it in a real multi-team student project.

---

### IDEA-002 · Critical Path as Student Team Task Driver
**Date**: 2026-03-23
**Origin**: David's observation that the critical path document (generated for KA this session) could structure student team assignments rather than remaining a planning artifact for the development team alone.

**The idea**: The five-phase critical path (Infrastructure → Data Seeding → User Management → Core Tool Backends → Course Integration) maps naturally to different student team competencies and assignment types:
- Data contribution tracks (Tracks 1–4) execute Phase 2 tasks (seeding the corpus)
- A GUI evaluation track executes page-level evaluation using the function spec system (IDEA-001)
- A future software development track would execute Phases 1, 3, 4, and 5

In this framing the critical path is not just a project management document — it is a curriculum structure. Each phase becomes a module, each task within a phase becomes an assignable deliverable, and the dependency graph of the critical path becomes the prerequisite structure of the course.

**What's interesting**: Most courses assign tasks that are pedagogically motivated but disconnected from real production systems. Here the student output (tagged images, evaluated articles, evaluated pages) is the actual input to the system. The critical path makes the dependency structure of that real system explicit, so students understand why their work is sequenced as it is and where it lands.

**Current status**: Nascent — discussed, not yet formalized as an assignment structure. Requires: (a) deciding which student populations cover which phases, (b) packaging each phase into bounded assignments with rubrics, (c) building the Phase 1 infrastructure (probably by faculty or staff, not students) to unblock Phase 2 student work.

---

*[Further entries to be added as ideas emerge]*

---

## Ideas Under Consideration (not yet logged)

| Tentative idea | Origin | Next step |
|---|---|---|
| Auto-generating evaluation rubrics from PAGE_FUNCTION.evalQuestions | 2026-03-23 discussion | Prototype as a simple export from ka_page_function.js |
| VOI-ranked gap assignment: assign hypothesis topics to students by VOI score | 2026-03-23 | Formalize as assignment design pattern |
| Warrant chain visualization as a teaching tool for scientific reasoning | Prior sessions | Needs a dedicated mockup |

