# Review Prompt: K-ATLAS Navigation Architecture Plan v2

**Date**: 2026-04-12
**From**: David Kirsh (via CW)
**To**: AG and Codex
**Action requested**: Structured critique and improvement suggestions

---

## Context

CW has produced a comprehensive navigation architecture plan for the K-ATLAS website. The plan redesigns the entire navigation system — currently 7+ divergent navbar implementations across ~80 pages — into a unified system with two nav regimes (global site and COGS 160 course site), a persistent left-hand journey nav, breadcrumbs on every page, a personalized profile dropdown, and 8 new pages (4 track portals, a "Did You Know?" questions page, grades, submissions, and roster).

The plan integrates the project's existing design agent pipeline: Science-Writing Agent → GUI Agent v3 → GUI Presentation Agent → Usability Critic Agent. It specifies 5 formal contracts between the shared nav files and the web pages, a 4-level self-testing framework, and a 7-phase migration strategy.

**The plan is at**: `/Users/davidusa/REPOS/Knowledge_Atlas/160sp/KA_NAVIGATION_ARCHITECTURE_PLAN_v2.md` (if not there yet, check `Workspace_Docs/` or ask David)

It is 1,715 lines and has 16 sections:

1. Problem Statement
2. Design Principles (grounded in project norms: Tufte, Shneiderman, Sweller, Doumont, Ware)
3. Architecture Overview (three-layer model: top bar, breadcrumbs, left nav)
4. Global Site Navigation (top bar, breadcrumb, left journey nav per user type)
5. Course Site Navigation (assignment-oriented top bar, personalized track left nav)
6. Topic Pages Redesign (cluster-level cards, PDF/Summary/Related links, "Did You Know?" questions page)
7. Track Portal Pages (4 new pages, team management within track)
8. Fall 160 Subsite (own nav regime, Designing_Experiments/ as content area)
9. Auth Widget & Profile Dropdown (unified widget, "What's Due" computation, grade access)
10. Shared Infrastructure Files (ka_nav.css, ka_nav.js, ka_nav_config.json, page metadata convention)
11. Design Agent Pipeline Integration (Science-Writer → GUI Agent v3 → Usability Critic, tiered by component)
12. Contracts (5 formal contracts: Page↔Config, Config↔JS, Auth↔Display, Schedule↔Deadlines, Week↔Highlight)
13. Self-Testing & Validation (dev-mode validator, CI script, Puppeteer smoke test, runtime assertions)
14. Migration Strategy (7 phases across 4 days, ~29 hours, pipeline-integrated)
15. Navigation Skill Specification (reusable .claude/skills/ka-navigation/SKILL.md)
16. Open Questions (7 items needing David's decision)

---

## What I need from you

### 1. Architecture Critique

Read the full plan and answer these questions:

- **Is the three-layer model (top bar / breadcrumbs / left nav) the right decomposition?** Are there cases where it breaks down — pages that don't fit neatly into either the global or course regime? What about the Designing_Experiments tools (experiment wizard, hypothesis builder) that serve both courses?

- **Is the left-nav journey model scalable?** There are 6 user-type journeys for the global site plus the course journey. That's 7 distinct nav structures maintained in `ka_nav_config.json`. Is this maintainable? Would a simpler model (e.g., 3 journeys: student, researcher, admin) work better?

- **Does the course top bar work?** The plan puts Syllabus, A0, A1, Sprints, Tracks in the course top bar. After A1, all assignments are track-specific sprints. Does "Sprints" as a top-bar link make sense to a student who doesn't yet know what a sprint is (Week 1–2)?

- **Is the "What's Due" computation robust?** It reads deadlines from a static JSON config file. But deadlines change (extensions, schedule shifts). Should this instead query the server's database? What's the right trade-off between client-side simplicity and data freshness?

### 2. Design Agent Pipeline Critique

- **Is the tiering right?** Tier 1 (full pipeline) covers 6 nav components. Tier 2 (abbreviated) covers 8 new pages. Tier 3 (mechanical migration) covers ~97 existing pages. Is there anything in Tier 3 that should be Tier 2? Any Tier 2 items that actually need full Tier 1 treatment?

- **Are the Usability Critic pass criteria realistic?** The plan requires 0 Major Fails on H1, H4, H6, H8, R1, R8 and ≤3 Minor Issues total. Is this achievable for a first implementation, or does it set up a revision loop that delays migration indefinitely?

- **Is the Science-Writing Agent adaptation for nav components useful?** The 13-item copy pack was designed for page content, not navigation components. Some items (example questions, expanded explainer) don't apply. Is the adaptation in §11C natural, or should the Science-Writing Agent spec be formally extended for nav components?

### 3. Contract Critique

- **Are the 5 contracts sufficient?** Are there interfaces between components that aren't covered? For example: the left nav's personalization (reading user track from localStorage) isn't formally contracted — what happens if the user object schema changes?

- **Is the contract enforcement strategy practical?** The plan uses dev-mode validators (`?nav_debug=1`), a CI Python script, and runtime assertions. Is this the right set of enforcement points? Should there also be a pre-commit hook?

### 4. Feasibility and Priorities

- **Is the 29-hour, 4-day estimate realistic?** Given the current state of the codebase (7+ nav patterns, no shared CSS, auth widget not loaded locally), is this achievable? What's most likely to take longer than estimated?

- **What should be cut if we only have 2 days?** Students need track selection working by Week 3 (next week). If we had to ship in 2 days instead of 4, what would you cut from the plan while preserving the ability to enable track signup?

- **What's missing?** Is there anything the plan doesn't address that it should? Consider: accessibility (screen readers, keyboard navigation), internationalization, performance (loading 3 shared files on every page), SEO, analytics.

### 5. Improvements

- **Propose specific changes.** Don't just identify problems — suggest fixes. If you think the left nav should have fewer journeys, specify which ones to merge. If you think a contract is missing, write it. If you think a phase should be reordered, give the new order.

- **Identify the 3 highest-risk decisions in the plan.** For each, explain why it's risky and what the mitigation should be.

- **If you were building this, what would you do differently?** Not hypothetically — concretely. What files would you create first? What would you test first? What would you skip entirely?

---

## Reference Files You Should Read

Before or while reviewing the plan, read these for context:

### The plan itself
```
/Users/davidusa/REPOS/Knowledge_Atlas/160sp/KA_NAVIGATION_ARCHITECTURE_PLAN_v2.md
```

### Current site state (to understand the problem)
```
/Users/davidusa/REPOS/Knowledge_Atlas/ka_home.html                    (global home — 7+ nav patterns start here)
/Users/davidusa/REPOS/Knowledge_Atlas/160sp/ka_schedule.html           (course schedule — different nav)
/Users/davidusa/REPOS/Knowledge_Atlas/160sp/ka_tracks.html             (track selection — yet another nav)
/Users/davidusa/REPOS/Knowledge_Atlas/160sp/week2_exercises.html       (A1 exercises — another nav variant)
/Users/davidusa/REPOS/Knowledge_Atlas/ka_evidence.html                 (evidence table — has left sidebar, unique)
```

### Design agents (to evaluate pipeline integration)
```
/Users/davidusa/REPOS/Knowledge_Atlas/agents/GUI_AGENT_V3.md           (32-item interaction spec)
/Users/davidusa/REPOS/Knowledge_Atlas/agents/USABILITY_CRITIC_AGENT.md (35-dimension critique framework)
/Users/davidusa/REPOS/Knowledge_Atlas/agents/SCIENCE_WRITER_AGENT.md   (13-item copy pack)
```

### Existing infrastructure
```
/Users/davidusa/REPOS/Knowledge_Atlas/ka_auth_widget.js                (server copy — 472 lines, 5-strategy injection)
   NOTE: This file may only be on the server copy at Knowledge_Atlas_xrlab_20260411/
/Users/davidusa/REPOS/Knowledge_Atlas/ka_workflows.js                  (6 roles, 9 workflows)
/Users/davidusa/REPOS/Knowledge_Atlas/config/gui_design_success_conditions.json
```

### Database state (to evaluate data-driven nav features like "What's Due")
```
/Users/davidusa/REPOS/Knowledge_Atlas/data/ka_auth.server_2026-04-12.db
   48 users, 251 articles, 30 research questions
   View: assignment0_submission_roster_with_questions_v (241 rows)
```

### Project norms (to evaluate whether the plan follows them)
```
/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/contracts/SCIENCE_COMMUNICATION_NORMS.md
/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/contracts/WRITING_STYLE_GUIDE.md
```

---

## Output Format

Please structure your review as:

```markdown
# Navigation Architecture Plan v2 — Review by [AG/Codex]

**Date**: 2026-04-XX
**Reviewer**: [AG/Codex]

## 1. Architecture Assessment
[Your analysis of §1–10]

## 2. Pipeline Assessment
[Your analysis of §11]

## 3. Contract Assessment
[Your analysis of §12]

## 4. Feasibility Assessment
[Your analysis of §14, with 2-day cut recommendations]

## 5. What's Missing
[Gaps not addressed in the plan]

## 6. Top 3 Risks
[Highest-risk decisions, with mitigations]

## 7. Specific Proposed Changes
[Concrete diffs — not "consider doing X" but "change X to Y because Z"]

## 8. If I Were Building This
[Your implementation approach, first files, first tests, what to skip]
```

Save your review to:
```
/Users/davidusa/REPOS/Knowledge_Atlas/docs/NAV_PLAN_REVIEW_[AG|CODEX]_2026-04-12.md
```

---

## Timeline

Please complete your review before implementation begins. The plan estimates Day 1 starts with the Science-Writing Agent copy packs. Your review should arrive before that, so any architectural objections can be addressed first.

If you have blocking concerns (something that would make the plan fail), surface those immediately rather than waiting for the full review.
