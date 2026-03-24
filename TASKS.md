# TASKS.md — Knowledge_Atlas

*Last updated: 2026-03-24*
*Owner repo: `/Users/davidusa/REPOS/Knowledge_Atlas/`*
*This file is the canonical task log for all GUI / frontend work.*

---

## Repo Assignment Rules (MANDATORY — all AI workers)

| Repo | Purpose | GUI work goes here? |
|------|---------|-------------------|
| `Knowledge_Atlas` | Live GUI · site · frontend | **YES — all new GUI work here** |
| `Article_Eater_PostQuinean_v1_recovery` | Extraction · JSON · EN/BN · summaries · rebuild logic | No |
| `Designing_Experiments` | Course docs · planning · legacy frontend (retiring) | No — migrate to KA |

**Rules:**
1. All new HTML, JS, CSS files go in `Knowledge_Atlas/`. Never in REPOS root or AE recovery.
2. `Designing_Experiments/frontend/` is legacy. Files there are superseded by KA equivalents. Do not add new UI files there.
3. When moving UI assets, record: old path · new path · whether old copy deleted/deprecated.
4. Commit by workstream — GUI commit separate from backend/docs commits.
5. Knowledge_Atlas has no GitHub remote yet. Do NOT attempt `git push` until David creates the remote.

---

## Pending

| ID | Task | Added | Context |
|----|------|-------|---------|
| KA-T1 | **Create GitHub remote for Knowledge_Atlas and push** | 2026-03-24 | David must create `github.com/dkirsh/Knowledge_Atlas` first, then: `git remote add origin …` + `git push -u origin master`. CW cannot do this without the remote URL. |
| KA-T2 | **Build GUI evaluation / design agent (Track 4 tool)** | 2026-03-24 | An autonomous agent that inspects KA pages, identifies usability issues against the user-type specs in `ka_gui_assignment.html`, and proposes design changes. Not just a student workbook — an actual AI agent that runs through the site on a scenario, records what it finds, and outputs a structured UX report. Proposed by David 2026-03-24. |
| KA-T3 | **Update `ka_article_finder_assignment.html` week numbers** | 2026-03-24 | Current page spans "Weeks 1–10". Students start Week 3. Adjust all week labels to Weeks 3–8, add explicit milestone table at top of hero, sharpen per-phase quantity targets (15 queries, 20 questions, 50 papers, 150 citation records). See session notes 2026-03-24 for full milestone table. |
| KA-T4 | **Add `howItWorks` paragraphs to all 27 measures in `ka_sensors.html`** | 2026-03-24 | Mechanistic explanations + expanded construct lists for every signal. Identified in prior session, not yet executed. |
| KA-T5 | **Add query templates for remaining DYK topics** | 2026-03-24 | DONE for 12 topics in this session. Verify all 15 QUERY_BANK entries render correctly when clicked from `ka_home.html`. |
| KA-T6 | **Wire `ka_topics.html` into standalone page navs** | 2026-03-24 | Pages like `ka_article_search.html`, `ka_sensors.html`, `ka_gaps.html` use simple inline navs (not the delegated nav system). Add Topics link to those navbars. |
| KA-T7 | **Create GitHub remote and push AE recovery pending changes** | 2026-03-24 | 30 tracked modified files in AE recovery await push to `origin/codex/recovery-cc-migration-artifacts`. Awaiting David's go-ahead. |
| KA-T8 | **Track 2 milestone table — update page** | 2026-03-24 | David approved the Weeks 3–8 milestone table proposed 2026-03-24. Implement in `ka_article_finder_assignment.html`: milestone table in hero, adjusted week numbers, per-phase quantity callouts. |

---

## In Progress

| ID | Task | Started | Notes |
|----|------|---------|-------|

---

## Completed

| ID | Task | Completed | Outcome |
|----|------|-----------|---------|
| KA-C1 | Move KA HTML files from REPOS root to `Knowledge_Atlas/` | 2026-03-24 | 22 HTML + 3 JS files moved. Zero broken links (verified by link checker script). |
| KA-C2 | Move DE frontend files to `Knowledge_Atlas/Designing_Experiments/` | 2026-03-24 | 12 HTML + `data/en_navigator_data.json` moved. DE repo move recorded with git commit 8f90267. |
| KA-C3 | Initialize git in Knowledge_Atlas, first commit | 2026-03-24 | 39 files, commit 8b48ffb. No remote yet — see KA-T1. |
| KA-C4 | Wire new pages into contributor nav + NAV_MAP | 2026-03-24 | Tag Bundles, Question Maker, Propose Article, Article Finder, GUI Assignment, Topic Browser all wired. |
| KA-C5 | Build `ka_topics.html` — 20-cluster topic browser | 2026-03-24 | VOI-sorted grid, priority banner, category filter tabs, 4 action buttons per card. |
| KA-C6 | Complete QUERY_BANK — 12 missing DYK topics | 2026-03-24 | All 15 topics now have full answer entries in `ka_demo_v04.html`. |
| KA-C7 | Build `ka_article_finder_assignment.html` (Track 2) | 2026-03-23 | 5-phase workflow, Query Diary, tool orientation, pipeline steps. |
| KA-C8 | Build `ka_question_maker.html` | 2026-03-23 | 20 clusters, 4 tools, quality-gate queue, VOI panel. |
| KA-C9 | Build `ka_article_propose.html` | 2026-03-23 | DOI lookup, 4-step intake, PDF upload, queue sidebar. |
| KA-C10 | Fix two bugs in `ka_hypothesis_builder.html` | 2026-03-23 | Bug 1: sum-signals replace chain (all 8 IDs). Bug 2: Stage 6 gauge not updated by credence slider. |
| KA-C11 | Build `ka_tag_assignment.html` (Track 1) | 2026-03-23 | 5 algorithm bundles (A–E), claim modal, Phase 0 reference table. |
| KA-C12 | Build `ka_gui_assignment.html` (Track 4) | 2026-03-23 | 4-phase workbook: User Types · Scenarios · Walkthrough · Spec Wall. |

---

## Session Notes — 2026-03-24

### Repo consolidation completed
All KA UI files now in `Knowledge_Atlas/`. REPOS root is clean. DE legacy frontend moved to `Knowledge_Atlas/Designing_Experiments/` as subdirectory.

### Knowledge_Atlas awaits GitHub remote
Until David creates `github.com/dkirsh/Knowledge_Atlas` and CW runs `git remote add` + `git push`, all work is local-only. Files exist on Mac disk at `/Users/davidusa/REPOS/Knowledge_Atlas/`.

### GUI agent (KA-T2) — design note
The planned GUI agent is distinct from `ka_gui_assignment.html` (a student workbook). The agent would: (1) autonomously navigate KA pages using browser tools; (2) run through defined user scenarios; (3) compare its path against the AI-suggested optimal path; (4) output a structured UX report flagging friction points, missing affordances, and copy issues. This is Track 4's analytical deliverable automated.
