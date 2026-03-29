# K-ATLAS Agent Directory

**Last updated**: 2026-03-29
**Canonical location**: `/Users/davidusa/REPOS/Knowledge_Atlas/agents/`
**Mirror/origin**: `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/agents/`

This directory contains the active agent specifications for the K-ATLAS project. Each agent is a purpose-built AI worker with a defined role, input contract, output format, and runnable prompt.

---

## Active Agents

| Agent | File | Role | Runs at step |
|-------|------|------|--------------|
| Science-Writing Agent | `SCIENCE_WRITER_AGENT.md` | Page copy, microcopy, example questions, warnings, state text | 1 |
| GUI Agent v3 | `GUI_AGENT_V3.md` | 32-item interaction spec per page; dual-framework (Streamlit + HTML/JS) | 2 |
| GUI Presentation Agent | `GUI_PRESENTATION_AGENT.md` | Runnable mockup from spec + copy pack | 3 |
| Usability Critic Agent | `USABILITY_CRITIC_AGENT.md` | 35-dimension heuristic evaluation (Nielsen + Shneiderman + Viz V1–V17) | 4a |
| Experimental Evaluate Agent | `EXPERIMENTAL_EVALUATE_AGENT.md` | Evaluates candidate experimental designs against 5 criteria | Research |

---

## Run sequence for any new or redesigned page

```
1. Science-Writing Agent  →  13-item copy pack
                              docs/ATLAS_SCIENCE_COPY_PACK_[PAGE]_[DATE].md

2. GUI Agent v3           →  32-item interaction spec
                              docs/GUI_AGENT_V3_OUTPUT_[PAGE]_[DATE].md

3. GUI Presentation Agent →  runnable mockup
                              pages/[page]_mockup.py  (Streamlit)
                           OR pages/[page]_mockup.html  (HTML/JS)

4. [RUN IN PARALLEL]
   4a. Usability Critic Agent  →  35-dimension critique report
                                   docs/USABILITY_CRITIQUE_[PAGE]_[DATE].md
   4b. Expert panel / D3 critique → structured panel feedback

5. GUI Agent v3 (re-run)  →  revised 32-item spec based on both critiques

6. GUI Presentation Agent →  revised mockup

7. Developer              →  production page (Streamlit .py or HTML/JS .html)
```

---

## Agent capabilities comparison (v3 vs. KA stub / v2)

| Capability | KA stub (2026-03-24) | AE GUI v2 (2026-03-22) | **GUI v3 (2026-03-29)** |
|-----------|----------------------|------------------------|-------------------------|
| Output items | Unspecified | 26 | **32** |
| Framework | Streamlit preferred | Streamlit only | **Streamlit + HTML/JS** |
| User roles | Generic personas | Generic personas | **6 KA roles from ka_workflows.js** |
| Panel scholars | 0 embedded | 5 | **13 + 4 viz scholars** |
| Viz heuristics | None | None | **V1–V17 (Tufte/Cleveland/Cairo/Knaflic/Shneiderman)** |
| Eval checklist | None | 13-item | **20-item** |
| Panel judgment | None | 8 questions | **12 questions** |
| KA doc references | GUI_DESIGN_* docs | AE docs only | **Both KA + AE docs** |
| Usability critic integration | None | None | **ka_usability_critic.js targets in item 31** |

---

## Framework selection guide

The GUI Agent v3 supports two implementation frameworks. It selects based on page type:

| Framework | When | Primary roles |
|-----------|------|---------------|
| **Streamlit** | Research analysis, evidence explorer, hypothesis builder, admin dashboard | researcher, contributor, instructor |
| **HTML/JS** | Student-facing, onboarding, workflow steps, schedule, user home | student_explorer, practitioner, theory_mechanism_explorer |

Every design output from GUI Agent v3 declares `FRAMEWORK: [Streamlit | HTML/JS]` at the top with a one-sentence rationale.

---

## The 6 K-ATLAS user roles (from ka_workflows.js)

| Role ID | Display name | Recommended workflows |
|---------|-------------|----------------------|
| `student_explorer` | Student Explorer | first-questions, deep-dive, evidence-pipeline |
| `contributor` | Contributor | evidence-pipeline, first-questions, deep-dive |
| `researcher` | Researcher / PI | hypothesis-test, lit-synthesis, evidence-pipeline, deep-dive |
| `practitioner` | Practitioner | design-decision, client-brief, deep-dive |
| `instructor` | Instructor | student-onboarding |
| `theory_mechanism_explorer` | Theory / Mechanism Explorer | mechanism-trace, hypothesis-test, deep-dive |

---

## Visualization heuristics (V1–V17) — quick reference

These 17 heuristics are embedded in `GUI_AGENT_V3.md` (item 28), `USABILITY_CRITIC_AGENT.md` (Tab 3), and `ka_usability_critic.js` (in-browser Viz tab). They apply to any K-ATLAS page with data displays.

| Group | Codes | Scholar |
|-------|-------|---------|
| Data-Ink & Integrity | V1–V4 | Tufte (1983, 2001) |
| Graphical Perception | V5–V7 | Cleveland (1985, 1993) |
| Truthfulness & Purpose | V8–V11 | Cairo (2012, 2016) |
| Cognitive Design | V12–V15 | Knaflic (2015) |
| Info-Seeking Mantra | V16–V17 | Shneiderman (1996) |

Full principle text: see `gui_visualization_guide.html` and `ka_usability_critic.js`.

---

## In-browser critique tool

`ka_usability_critic.js` is the browser-side implementation of the Usability Critic Agent. It adds a floating purple 🔎 button (bottom-left) to any ATLAS page where it is included. It implements the same 35 dimensions in an interactive rating panel.

Currently wired into: `ka_dashboard.html`, `ka_home.html`, `ka_demo_v04.html`, `ka_user_home.html`, `ka_workflow_hub.html`.

To add to any page: `<script src="ka_usability_critic.js"></script>`

---

## Reference documents

### KA-specific (most current design decisions)
```
Knowledge_Atlas/docs/GUI_DESIGN_AGENT_SPEC_2026-03-24.md
Knowledge_Atlas/docs/GUI_DESIGN_PANEL_REVIEW_2026-03-24.md
Knowledge_Atlas/docs/GUI_DESIGN_PROCESS_AND_REPAIRS_2026-03-24.md
Knowledge_Atlas/docs/GUI_RUTHLESS_AUDIT_2026-03-24.md
Knowledge_Atlas/docs/GUI_DATA_CONTRACTS_2026-03-24.md
Knowledge_Atlas/ka_workflows.js
```

### AE foundation docs (personas, journeys, page map)
```
Article_Eater_PostQuinean_v1_recovery/docs/K_ATLAS_GUI_PAGE_MAP_AND_AGENT_HANDOFF_2026-03-18.md
Article_Eater_PostQuinean_v1_recovery/docs/KA_USER_PERSONAS_AND_USE_CASES_2026-03-16.md
Article_Eater_PostQuinean_v1_recovery/docs/UI_JOURNEY_BENCHMARKS_2026-03-16.md
Article_Eater_PostQuinean_v1_recovery/docs/ATLAS_UI_INTERACTION_PACK_2026-03-18.md
```

### Visualization and expert reference
```
Designing_Experiments/docs/student_tracks/gui_visualization_guide.html
Designing_Experiments/docs/student_tracks/gui_design_experts_reference.html
```

---

## Pages to build (priority order, from GUI Presentation Agent)

| Priority | Page | Framework | Primary roles | Why now |
|----------|------|-----------|---------------|---------|
| 1 | Ask (core query) | Streamlit | researcher, student_explorer | Primary entry point for all roles |
| 2 | Research Gaps + Experiment Maker | Streamlit | researcher, theory_mechanism_explorer | Fall course critical path |
| 3 | Evidence explorer | Streamlit | researcher, contributor | Dense analytic; hardest to get right |
| 4 | Home | HTML/JS | all | Orientation and routing; first impression |
| 5 | Neuroscience Perspective | Streamlit | theory_mechanism_explorer | Epistemic-transparency challenge |
| 6 | Author Mode | Streamlit | contributor | Expert workspace |
| 7 | Practitioner Workspace | HTML/JS | practitioner | Actionability surface |
| 8 | COGS 160 Student Mode | HTML/JS | student_explorer | Scaffolded learning mode |

---

## Version history

| Date | Change |
|------|--------|
| 2026-03-22 | AE: GUI Agent v2, Science-Writing Agent, GUI Presentation Agent created |
| 2026-03-24 | KA: stub `gui_design_agent_prompt.md` created; KA GUI design docs written |
| 2026-03-26 | AE: Experimental Evaluate Agent added |
| 2026-03-29 | KA: Full unification — GUI Agent v3 (32-item, dual-framework, 13-scholar panel, V1–V17 viz, 6-role model); Usability Critic Agent (new); all AE agents mirrored with path updates; this README |
