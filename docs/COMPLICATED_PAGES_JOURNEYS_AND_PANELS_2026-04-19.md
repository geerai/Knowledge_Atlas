# Complicated pages, user journeys, and a panel-based discovery plan

*Date*: 2026-04-19
*Author*: CW (for DK deliberation)
*Commissioned in response to*: "what main complicated pages such as single article, topics... EN viewing... BN viewing... interpretation layer... argumentation layer... the question answering layer; the neuro, mechanisms, theory layers. Any others?... My concerns are: design elegance, functionality for user types, hook, and how well it plays on mobile... What else should we be surfacing and what are the journeys - how can we discover those? Would it be plausible to use panels?"

This document answers the four questions in order. It is scoped to the *complicated* surfaces — the layer-specific inspectors where a first visit either teaches the visitor what the Knowledge Atlas is or loses them. Pages already designed (the home, the topics family, the article view, the theory explainer pages) are referenced but not re-analysed here.

---

## 1. The complicated-page inventory

DK enumerated ten surfaces. Organising them by what they expose, and adding the ones that belong in the same class, the inventory is:

**Layer A — Article-centred views** (one paper, deepened).
- `ka_article_view.html` — the per-paper record (landed 2026-04-19; shows title, abstract, main conclusion, Atlas classification, related papers).
- *Argumentation-around-an-article view* — "what are the obvious arguments against this paper?" A page that takes a paper id and produces its critics: contradicting papers, methodological caveats from the instrument registry, and the argument graph edges that attack this paper's claims. **New.**
- *Neuroscientific interpretation view* — given a paper with an outcome measure, what neural mechanisms does it plausibly engage? **New, shares fate with the neuro layer (see C).**

**Layer B — Topic-centred views** (one topic bundle, deepened).
- The six topic-page variants now in place (`ka_topics.html` Classic View + five purpose-built variants).
- `ka_topics_public_view.html` (public variant landed today) and `ka_topics_student_view.html` (student variant landed today).
- *Topic-inside-the-hierarchy inspector* — given a topic bundle, show its position in the modality × outcome grid, the parent and sibling bundles, and the empty adjacent cells as explicit gaps. **New.**

**Layer C — Network-centred views** (Web of Belief, Bayesian Network, epistemic state).
- *EN viewing* — the Epistemic Network / Web of Belief. DK's question: *what is it good for?* The honest answer is that the EN is load-bearing for the system's author persona (DK inspecting his own theory) and for graduate students doing theory work. It is *not* load-bearing for practitioners or for the general public — most end users will never have a task that reaches into the graph directly. The design implication is that the EN view should be a *power-user inspector*, not a front-door artefact. **New.**
- *BN viewing* — the Bayesian Network layer that carries conditional probabilities and directed edges for causal projection. *What is it good for?* Causal-query answering; projection-calculus runs; sensitivity analysis when a study's effect size updates. Again a power-user inspector; most end users will consume its output (a recommendation with a confidence) without needing to see the graph. **New.**
- *Argumentation graph viewer* — the Pollock/Dung-style defeasible argument graph that underpins the contested-claim machinery. Visualises support and attack edges at the claim level. Overlaps with Layer A's "arguments against this paper". **New.**

**Layer D — Interpretation and answer generation.**
- *Interpretation layer explorer* — what does the Atlas think this corpus means? Given a query or a region of the graph, show the synthesised interpretation, its provenance (which papers, which theories), and the uncertainty envelope. Closest in spirit to a science-writer summary with provenance footnotes. **New.**
- *Question-answering layer* — natural-language Q&A over the Atlas, with a structured answer (claim, confidence, sources, caveats). **New; prototype worthy of panel review before build.**

**Layer E — Mechanism-and-theory views.**
- `ka_theories.html` — already exists; lists T1 and T1.5.
- `ka_framework_*.html` (11 pages) — already exist.
- `ka_theory_*.html` (13 T1.5 pages) — already exist; twelve are panel-review stubs.
- *Mechanisms page* — exists at `ka_mechanisms.html` but thin. **Revisit.**
- *Neuro page* — exists at `ka_neural.html` showing PNU profiles. **Revisit.**
- *PNU detail page* — one plausible-neuroscience-underpinning, deepened. **New.**
- *Theory-to-topic-to-paper lattice viewer* — a navigable tree that starts at a T1 framework, descends to its T1.5 children, descends to the topic bundles that instantiate each T1.5, descends to the papers. **New.**

**Layer F — Meta-surfaces (gaps, research fronts, evidence).**
- `ka_evidence.html` — currently a redirect to topics. **Revisit; needs its own surface.**
- `ka_gaps.html` — currently a redirect. **Revisit.**
- *Research fronts inspector* — fronts are an Atlas-specific object (a research community clustering papers that cite each other in close proximity and use similar instruments); the fronts view would show the front's maturity, VOI, replication count, and recent arrivals. **New.**
- *Contradictions dashboard* — paper pairs that contradict each other, ranked by effect-size magnitude of the disagreement. Load-bearing for the author persona; narrative-worthy for the public ("where is the science still arguing?"). **New.**
- *Replication dashboard* — what replicates, what doesn't, and who funded what. Public-facing accountability. **New.**

**Layer G — Inspectors (maintainer-side).**
- *Ontology inspector* — every T1 framework, every T1.5 theory, every topic bundle, every outcome term, every architectural root, viewable as a browsable tree with counts. Maintainer tool; not user-facing. **New.**
- *Topics inspector* — the crosswalk payload in inspectable form (adjacent-cell gaps, unresolved outcomes, evidence-status distribution). Overlaps with Layer B's inspector. **New; half-built already via Codex's crosswalk tooling.**
- *Classifier inspector* — every paper's classifier output with confidences and disagreements between layers. Audit tool; admin-only. **New.**

**Layer H — Workflow and provenance.**
- *Pipeline dashboard* — papers × stages matrix showing where each paper currently sits in the extraction pipeline. Admin + Track 2 student. **Partially exists.**
- *Warrant-chain viewer* — for a claim, the chain of warrants that support it (theory-derived / constitutive / rebutting / undercutting). Load-bearing for the author and for the graduate-student persona. **New.**

**What else?** Two I would add on top of DK's list:

- *VOI dashboard* — Value Of Information per research front, per topic bundle, per question. A ranked surface for "where should the next study go?" — directly useful for Persona 1 (Author), Persona 3 (Senior Researchers), and pedagogically useful for 160 students learning how to pick a thesis topic. **New.**
- *Panel deliberation viewer* — the panels we dispatch (see §5 below) produce artefacts; those artefacts themselves deserve a browsable home so future readers can re-read why a decision was made. Meta-system. **New.**

That gives us roughly **27 distinct surface candidates**, of which about eight exist, three are in mid-flight, and sixteen are new.

---

## 2. What each layer surfaces, and why the layer is useful

The right way to answer "what is EN viewing good for?" is to name a concrete user task that only that layer makes answerable.

| Layer | Load-bearing task | Persona fit | Production-ready effort |
|---|---|---|---|
| Article view | "Is this paper's finding what I think it is?" | Public, student, practitioner | Done |
| Topics | "What does the evidence say about X?" | All personas | In flight |
| Topic-in-hierarchy inspector | "Where does this topic sit in the map of knowledge?" | Student, researcher | Small (day) |
| EN viewing | "What does the system believe about X right now, and what is that belief resting on?" | Author, senior researcher, graduate student | **Large (week+)** |
| BN viewing | "If we set up condition X, what does the system predict for outcome Y?" | Author, practitioner (indirectly), graduate student | **Large** |
| Argumentation graph | "What are the strongest attacks on this claim?" | Author, graduate student, 160 student doing T4 | Medium (2–3 days) |
| Interpretation layer | "Give me the 400-word synthesis the system would tell a public reader." | Public, practitioner | Medium |
| Question-answering layer | "Plain-language Q&A with honest uncertainty." | Public, practitioner | **Large (genuinely hard; panel first)** |
| Neuro / mechanisms | "What neural systems do we think mediate this effect?" | Graduate student, researcher | Medium (pages exist; revisit) |
| Theory lattice | "How does framework F1 connect to the papers I just read?" | Student, researcher | Small |
| Research fronts | "Where is the evidence actively accumulating?" | Senior researcher, journalist | Medium |
| Contradictions | "Where is the field arguing with itself?" | Journalist, author | Small |
| Replications | "Did this finding hold up?" | All personas; public-facing accountability | Medium |
| VOI | "Where is the next study most needed?" | Author, researcher, 160 student thesis-picking | Medium |
| Ontology inspector | "Show me the taxonomy the whole site is built on." | Maintainer | Small (admin-side) |
| Classifier inspector | "Which papers is our classifier uncertain about?" | Maintainer, Codex, CW | Small (admin-side) |
| Pipeline dashboard | "Where is paper X stuck?" | Admin, Track 2 student | Small (partially exists) |
| Warrant-chain viewer | "Why does the system believe this?" | Author, graduate student | Medium |
| Panel deliberation viewer | "Why was this decision made, and by whom?" | Everyone reading the audit trail | Small |

This table is the first-cut prioritisation you'd want for a build sprint, but the honest answer to "which layer is worth building first" runs through the panel method described in §5.

---

## 3. Per-user-type functionality matrix

The question DK raised on 2026-04-19 was: **are we being well served** at each surface? For the end-user personas, the matrix below scopes what each persona needs (not what's built). Rows = surfaces; columns = our three primary end-user personas. A cell marked **(need)** is load-bearing for that persona; **(helpful)** is a secondary use; **(—)** is irrelevant.

| Surface | 160 student | Public visitor | Admin / instructor |
|---|:---:|:---:|:---:|
| Article view | need | need | helpful |
| Topics (facet or classic) | need | need | helpful |
| Topic-in-hierarchy inspector | helpful | helpful | need |
| EN viewing | — | — | need |
| BN viewing | — | helpful (as "predicted output") | need |
| Argumentation graph | helpful (Track 4 rubric) | — | need |
| Interpretation layer | need (synthesised version of their sub-topic) | need | helpful |
| Question-answering | helpful | **need** (first-contact discovery) | helpful |
| Neuro / mechanisms | need (Track 3) | helpful | helpful |
| Theory lattice | need (Track 1, Track 3) | helpful | need |
| Research fronts | helpful | need | need |
| Contradictions | helpful | need ("where is science arguing?") | need |
| Replications | helpful | need | need |
| VOI | helpful (thesis-pick, Track 2) | — | need |
| Ontology inspector | — | — | need |
| Classifier inspector | — | — | need |
| Pipeline dashboard | need (Track 2) | — | need |
| Warrant-chain viewer | helpful | — | need |
| Panel deliberation viewer | helpful (learning artefact) | helpful | need |

The matrix tells us four practical things. First, the **public visitor** has a relatively narrow column — only ~ 6 surfaces are genuinely load-bearing for them. Second, the **admin** column is broad — an admin needs almost every surface at some point. Third, the **160 student** column is medium-width but deeply conditioned on which track the student is on (which is why the persona-specific `ka_topics_student_view.html` reads the student's track from localStorage and tailors the page). Fourth, some surfaces (EN, BN, ontology, classifier) should arguably not be publicly reachable at all — they belong in an admin-gated sub-site.

---

## 4. Design elegance — as a rubric, not a preference

DK's four stated concerns (design elegance, functionality for user types, hook, mobile) are best treated as a rubric a panel can grade, not as a preference list. Translating each into a scorable question:

**Elegance** is Tufte's (1983) data-ink ratio plus Tognazzini's (1992) Apple HIG principle of *decorum over decoration*. The practical test: can the page be reduced by half with no loss of function? If yes, it is not yet elegant. On our current surfaces, `ka_topics.html` (Classic View), `ka_home.html`, and `ka_contribute.html` (the full version) all fail this test; the five new variant pages and the `ka_article_view.html` pass it.

**Functionality for user types** is the matrix in §3. The test: for each surface, who is it *for*, and does the copy, the default view, and the visual hierarchy reflect that? A surface that tries to serve every persona equally usually serves none of them well (Cooper et al., 2014). This is why the split-variant pattern matters.

**The hook** is about the first 30 seconds. The Nielsen–Loranger (2006) usability studies, and more recently Krug (2014), find that first-time visitors form their judgement of a site before they scroll. The test: within the first viewport, does the page answer "what is this and why should I stay?" For the public visitor, our current `ka_home.html` answers imperfectly; `ka_topics_public_view.html` (as of today) answers well via its welcome strip and glossary callout. `ka_contribute_public.html` answers well via the "Why it's useful" card. `ka_article_view.html` answers via its type-pill and title; its hook is acceptable.

**Mobile** is a secondary concern for our current users (DK primarily reviews on desktop; the 160 students use university machines), but ignoring it carries a future cost. The test: does the page render usably at 390 × 844 (iPhone 15) without horizontal scroll, text at legible size, and touch targets ≥ 44 px? Most of our pages are responsive because they use `max-width` and `grid-template-columns: 1fr` fallbacks at narrow viewports. The pages that break are the Dashboard topic variant (three-column layout cramps below 820 px but falls back to stacked), the heatmap topic variant (wide matrix overflows; we allow horizontal scroll), and `ka_admin.html` (the Grading tab's multi-column table cramps). Overall the mobile story is *adequate but not considered*; a deliberate pass when we have time would improve it, but it is not blocking.

---

## 5. Discovering journeys: the panel method, and Codex has already proved it works

DK asked: "what are the journeys — how can we discover those? Would it be plausible to use panels?" The answer is **yes, panels are plausible and already working**. Proof: on 2026-04-19 Codex landed `docs/KNOWLEDGE_REPRESENTATION_PANEL_BRIEF_2026-04-19.md` — a full panel-ready brief for a Knowledge Representation panel focused specifically on the topic-representation stack. It names the distinctions that must stay clear, the eight decision questions, the seven recommended panel members (ontologist, computational librarian, outcome-vocabulary specialist, architectural-taxonomy owner, classifier engineer, KA product/UX owner, optional domain scholar), the evidence packet to pre-read, and the seven desired outputs. This is the template.

The panel method for journey discovery works because each panel assembles expertise that crosses the production team's blind spots. A page-level UX pass by one engineer will not surface the questions a domain scholar would ask. A domain scholar acting alone will not surface the UI affordance questions a computational librarian would flag. The panel turns the journey-discovery problem from a one-person audit into a small collective deliberation.

**Proposed panel roster for the layers in §1.** Each panel follows the Codex brief's shape: current state, distinctions to preserve, decision questions, recommended members, evidence packet, desired outputs. Panels are dispatched as sub-agent Task invocations (general-purpose agent with a careful brief per panel); the sub-agent produces an artefact saved under `docs/panels/` and the main session synthesises across panels.

| Panel | Focus | Recommended chair | Members (4–6) |
|---|---|---|---|
| Knowledge Representation (Codex, already briefed) | Topic object, crosswalk, outcome vocabulary | Ontologist | Computational librarian, outcome specialist, architectural taxonomist, classifier engineer, product owner |
| Epistemic-Network & Belief | EN view: what to show, what to hide, how to render graph inspection | Belief-revision theorist (Quine / Haack line) | Graph-visualisation researcher, scientific-communication writer, Track 4 student rep, an Article Finder student |
| Bayesian-Network & Projection | BN surface: causal queries, projection calculus, population transfer | Bayesian-network theorist (Pearl line) | Graphical-model implementer, medical-decision-aid designer, epidemiologist, public-communicator |
| Argumentation | Argument graphs, attack/support edges, "arguments against this paper" | Defeasible-reasoning theorist (Pollock / Dung) | Legal-reasoning theorist, dialectics-in-science scholar, science journalist, UX researcher |
| Interpretation | Synthesised summaries with honest uncertainty | Science-communication scholar (Sagan / Yong) | Philosopher of science, statistics communicator, public-health communicator, end-user (journalist) |
| Question-answering | Natural-language Q&A over the Atlas | Information-retrieval + IR-with-uncertainty specialist | Human-AI interaction researcher, science journalist, a graduate student, a practitioner |
| Mechanism & neuro | PNU architecture, mechanism-level pages | Systems neuroscientist | Cognitive neuroscientist, science writer, graduate student, environmental psychologist |
| Meta / research fronts / VOI | Fronts inspector, VOI dashboard, contradictions | Philosopher of science | Sociologist of science, research-funding officer, working researcher, statistics communicator |
| UX / journey synthesis | Cross-panel integration; defines the *journeys* visitors take across surfaces | UX research lead | Information architect, cognitive scientist, a student on the UX track (Track 4), a mobile-first designer |

Nine panels. Each runs one sub-agent pass (~ 30–60 min of sub-agent work), produces a 4–6 KB markdown artefact, and feeds into the main session's synthesis. Total elapsed wall-clock if panels run sequentially: ~ 6–9 hours of sub-agent time. If run in parallel (three-at-a-time, per the Agent tool's parallel-dispatch capacity), ~ 2–3 hours elapsed.

**What the panel synthesis gives us** that the page-by-page audit cannot: *journeys*. A journey is not a single page — it is a sequence across pages. The UX panel's output is specifically the synthesis: given a public visitor lands at `ka_home.html` with the question "does daylight help me sleep?", what is the 4-step journey through the site that answers them, and which pages need to exist (or need revision) to support that journey? That is what §5 of the brief would ask each panel to sketch for their layer, and what the UX panel would stitch together.

**When to dispatch.** My recommendation: approve the roster above (add or remove members as needed), then dispatch the first four panels (KR, EN, BN, Argumentation) in this session because their findings are prerequisites for designing the related views. Interpretation, QA, Mechanism, Meta, and UX follow after we've digested the first four.

---

## 6. Mobile, briefly

Per DK's note ("less important"), mobile is a secondary concern but worth stating the policy so we don't accidentally regress. The policy: every global page must render usably at 390 × 844 px without horizontal scroll. "Usably" means the primary task can be completed; the dense inspector views (EN, BN, argumentation graph) are explicitly exempt because their visual density is the feature. Admin-only surfaces are exempt. The mobile story is verified by the visual-regression scaffold at `scripts/visual_check.py` (currently at three viewports, one of which is mobile).

---

## 7. Priority, and what to do this sprint

Respecting DK's stated sprint (Spring 2026) plus the Codex-topic-panel already teed up, the order that delivers most persona-benefit per unit of effort is:

1. **Dispatch the four first-wave panels** (KR, EN, BN, Argumentation) — this turn or next. Codex's KR brief is ready; CW drafts EN, BN, Argumentation briefs in the shape of the KR template, then dispatches four sub-agents in parallel. Artefacts land in `docs/panels/`. Total ~ 2 hours CW time + 2 hours sub-agent wall clock.
2. **Act on the KR panel's output** — the canonical topic object decision settles what ka_topics.html defaults to, which variant becomes production, and whether the iv_root/outcome/tag hierarchy needs revision. This unblocks the remaining topic work.
3. **Build one EN inspector page** as a proof of concept — CW scaffolds a read-only Web-of-Belief view using the existing graph payloads, at admin-only access. No public exposure until the EN panel has weighed in.
4. **Build the argumentation-against-a-paper view** — this is the most publicly evocative of the layer inspectors (it answers "what are the best objections?" which is a press-release-able question) and the best hook test for the public visitor persona.
5. **Dispatch Interpretation and QA panels** only after the first-wave panels have landed; these are the hardest to get right, and the first-wave decisions constrain their design.

What I will *not* do without DK's explicit sign-off: start building the BN inspector, the EN inspector, or the QA layer. Each is load-bearing for the system's conceptual integrity and should not be built without a panel having signed off on the object-level decisions.

---

## 8. References

Bertin, J. (1967). *Sémiologie graphique: les diagrammes, les réseaux, les cartes*. Gauthier-Villars. (English translation: *Semiology of Graphics*, W. J. Berg, 1983, University of Wisconsin Press.) Google Scholar: 7,900+.

Card, S. K., Mackinlay, J. D., & Shneiderman, B. (Eds.). (1999). *Readings in information visualization: using vision to think*. Morgan Kaufmann. Google Scholar: 6,400+.

Cooper, A., Reimann, R., Cronin, D., & Noessel, C. (2014). *About face: the essentials of interaction design* (4th ed.). Wiley. Google Scholar: 5,800+.

Dung, P. M. (1995). On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games. *Artificial Intelligence*, 77(2), 321–357. https://doi.org/10.1016/0004-3702(94)00041-X Google Scholar: 6,200+.

Gould, J. D., & Lewis, C. (1985). Designing for usability: key principles and what designers think. *Communications of the ACM*, 28(3), 300–311. https://doi.org/10.1145/3166.3170 Google Scholar: 2,700+.

Haack, S. (1993). *Evidence and inquiry: towards reconstruction in epistemology*. Blackwell. Google Scholar: 2,400+. [For the foundherentism / warrant-type lineage behind the Web of Belief.]

Hearst, M. A. (2009). *Search user interfaces*. Cambridge University Press. https://doi.org/10.1017/CBO9781139644082 Google Scholar: 2,800+.

Krug, S. (2014). *Don't make me think, revisited: a common sense approach to web usability* (3rd ed.). New Riders. Google Scholar: 5,700+.

Nielsen, J., & Loranger, H. (2006). *Prioritizing web usability*. New Riders. Google Scholar: 1,900+.

Norman, D. A. (2013). *The design of everyday things* (Revised & expanded ed.). Basic Books. (Original 1988.) Google Scholar: 48,000+.

Pearl, J. (2009). *Causality: models, reasoning, and inference* (2nd ed.). Cambridge University Press. https://doi.org/10.1017/CBO9780511803161 Google Scholar: 38,000+.

Pollock, J. L. (1995). *Cognitive carpentry: a blueprint for how to build a person*. MIT Press. Google Scholar: 1,500+. [For defeasible argumentation.]

Rosenfeld, L., Morville, P., & Arango, J. (2015). *Information architecture: for the web and beyond* (4th ed.). O'Reilly. Google Scholar: 4,600+.

Rosson, M. B., & Carroll, J. M. (2002). *Usability engineering: scenario-based development of human-computer interaction*. Morgan Kaufmann. Google Scholar: 2,600+.

Shneiderman, B. (1996). The eyes have it: a task by data type taxonomy for information visualizations. *Proceedings of the IEEE Symposium on Visual Languages*, 336–343. https://doi.org/10.1109/VL.1996.545307 Google Scholar: 8,400+. [Source of the "overview first, zoom and filter, then details on demand" mantra — directly relevant to the BN and EN inspector design.]

Suchman, L. A. (2007). *Human-machine reconfigurations: plans and situated actions* (2nd ed.). Cambridge University Press. https://doi.org/10.1017/CBO9780511808418 Google Scholar: 9,500+. [Source of the situated-action framing for journey discovery.]

Tognazzini, B. (1992). *Tog on interface*. Addison-Wesley. Google Scholar: 940+. [Apple HIG "decorum over decoration" lineage.]

Tufte, E. R. (1983). *The visual display of quantitative information*. Graphics Press. Google Scholar: 17,000+.

Quine, W. V. O., & Ullian, J. S. (1978). *The web of belief* (2nd ed.). Random House. Google Scholar: 1,700+. [Source text for the Web-of-Belief concept the EN layer operationalises.]

Sagan, C. (1995). *The demon-haunted world: science as a candle in the dark*. Random House. Google Scholar: 5,400+. [Science-communication lineage for the Interpretation layer.]

Yong, E. (2022). *An immense world: how animal senses reveal the hidden realms around us*. Random House. Google Scholar: 200+. [Exemplar of honest-uncertainty science writing.]

Codex (GPT-5.x). (2026-04-19). *Knowledge Representation Panel Brief*. `docs/KNOWLEDGE_REPRESENTATION_PANEL_BRIEF_2026-04-19.md`. [Proof that the panel pattern is already in production use by a collaborating AI worker on this project.]

---

*Deliverable end.*
