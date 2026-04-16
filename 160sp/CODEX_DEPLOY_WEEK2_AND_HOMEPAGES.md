# Codex Deployment Prompt: Week 2 Exercises + Role Homepages

**Created**: 2026-04-08 (final revision)
**For**: Codex to deploy to xrlab.ucsd.edu
**Priority**: URGENT — class is tomorrow (Wed April 9)

---

## Overview

Two groups of files to deploy from the local Knowledge_Atlas repo (`/Users/davidusa/REPOS/Knowledge_Atlas/`) to the live server at `xrlab.ucsd.edu/ka/`:

1. **Week 2 exercises page** — heavily updated with inline step-by-step procedure, data file instructions, submission CTA, pre-submission checklist, and live data explorer links
2. **Role-based homepages** — 6 user-type landing pages committed to GitHub but not yet on the server

---

## GROUP 1: Week 2 Materials

### Files to Upload/Replace

| # | Local Path | Server Path | Action |
|---|-----------|------------|--------|
| 1 | `160sp/week2_exercises.html` | `/ka/160sp/week2_exercises.html` | **REPLACE** — major rewrite |
| 2 | `160sp/context/context_ex0_mechanism_pathway.md` | `/ka/160sp/context/context_ex0_mechanism_pathway.md` | REPLACE — full URLs + data loading |
| 3 | `160sp/context/context_exA_trust_panel.md` | `/ka/160sp/context/context_exA_trust_panel.md` | REPLACE |
| 4 | `160sp/context/context_exB_debate_visualizer.md` | `/ka/160sp/context/context_exB_debate_visualizer.md` | REPLACE |
| 5 | `160sp/context/context_exC_warrant_calculator.md` | `/ka/160sp/context/context_exC_warrant_calculator.md` | REPLACE |
| 6 | `160sp/context/context_exD_search_filter.md` | `/ka/160sp/context/context_exD_search_filter.md` | REPLACE |

### What Changed in week2_exercises.html

The local copy has ALL changes applied. Just replace the server file. Summary of changes:

- **Nav bar**: Simplified — removed quickstart and walkthrough links (just Schedule, Setup, Week 2, Evidence, Ask)
- **Hero pills**: Now read "Choose an Exercise / Follow the Step-by-Step / Submit Your Work"
- **Removed**: Quickstart callout banner (the quickstart page is no longer part of the assignment)
- **New section: "Your Step by Step"** — 11-step inline procedure right after "How Week 2 Works", telling students exactly what to do in order
- **New in Exercise 0: "Step 5 — The Data Files"** — explains evidence.json and argumentation.json, which exercises use which, download links, and instructions to drag files into AI chat
- **New section: "Pre-Submission Checklist"** — 8 checkbox items
- **New section: "Submit Your Work"** — dark CTA block with amber "Submit Here →" button linking to Google Form (URL placeholder `REPLACE_WITH_GOOGLE_FORM_URL` — David will update after creating the form)
- **New section: "Explore the Live Data"** — links to Evidence Explorer, Argumentation Viewer, Warrant Types Reference
- **Grading rubric**: Unchanged (4×25%)

### Files NOT Being Deployed

- `week2_quickstart.html` — **do NOT deploy** (removed from assignment)
- `week2_walkthrough.html` — **do NOT deploy** (content folded into exercises page)

---

## GROUP 2: Role-Based Homepages

| # | Local Path | Server Path | Notes |
|---|-----------|------------|-------|
| 7 | `ka_home_student_new.html` | `/ka/ka_home_student_new.html` | **Use _new version** — do NOT deploy `ka_home_student.html` |
| 8 | `ka_home_instructor.html` | `/ka/ka_home_instructor.html` | Deploy as-is |
| 9 | `ka_home_researcher.html` | `/ka/ka_home_researcher.html` | Deploy as-is |
| 10 | `ka_home_practitioner.html` | `/ka/ka_home_practitioner.html` | Deploy as-is |
| 11 | `ka_home_contributor.html` | `/ka/ka_home_contributor.html` | Deploy as-is |
| 12 | `ka_home_theory.html` | `/ka/ka_home_theory.html` | Deploy as-is |

### Do NOT Overwrite

- `ka_home.html` — already on server
- `ka_user_home.html` — already on server
- `ka_home_student.html` — do NOT deploy this filename
- `160sp/ka_student_setup.html` — existing student setup page

---

## Complete File Inventory (12 files)

| # | Local Path | Server Path | Action |
|---|-----------|------------|--------|
| 1 | `160sp/week2_exercises.html` | `/ka/160sp/week2_exercises.html` | REPLACE |
| 2 | `160sp/context/context_ex0_mechanism_pathway.md` | `/ka/160sp/context/context_ex0_mechanism_pathway.md` | REPLACE |
| 3 | `160sp/context/context_exA_trust_panel.md` | `/ka/160sp/context/context_exA_trust_panel.md` | REPLACE |
| 4 | `160sp/context/context_exB_debate_visualizer.md` | `/ka/160sp/context/context_exB_debate_visualizer.md` | REPLACE |
| 5 | `160sp/context/context_exC_warrant_calculator.md` | `/ka/160sp/context/context_exC_warrant_calculator.md` | REPLACE |
| 6 | `160sp/context/context_exD_search_filter.md` | `/ka/160sp/context/context_exD_search_filter.md` | REPLACE |
| 7 | `ka_home_student_new.html` | `/ka/ka_home_student_new.html` | NEW |
| 8 | `ka_home_instructor.html` | `/ka/ka_home_instructor.html` | NEW |
| 9 | `ka_home_researcher.html` | `/ka/ka_home_researcher.html` | NEW |
| 10 | `ka_home_practitioner.html` | `/ka/ka_home_practitioner.html` | NEW |
| 11 | `ka_home_contributor.html` | `/ka/ka_home_contributor.html` | NEW |
| 12 | `ka_home_theory.html` | `/ka/ka_home_theory.html` | NEW |

---

## Verification Checklist

### Week 2 Exercises
1. `https://xrlab.ucsd.edu/ka/160sp/week2_exercises.html` loads correctly
2. Nav bar has: K-ATLAS | Schedule | Setup | Week 2 | Evidence | Ask
3. Hero pills: "Choose an Exercise" / "Follow the Step-by-Step" / "Submit Your Work"
4. "Your Step by Step" section visible with 11 numbered steps
5. Exercise 0 has "Step 5 — The Data Files" section with download links
6. evidence.json and argumentation.json download links work
7. Pre-Submission Checklist has 8 checkbox items
8. "Submit Here →" button visible (amber, large)
9. "Explore the Live Data" section has 3 links (Evidence Explorer, Argumentation Viewer, Warrant Types)
10. All 5 context files download from their links on the page

### Role Homepages
11. `https://xrlab.ucsd.edu/ka/ka_home_instructor.html` — 200 OK
12. `https://xrlab.ucsd.edu/ka/ka_home_researcher.html` — 200 OK
13. `https://xrlab.ucsd.edu/ka/ka_home_practitioner.html` — 200 OK
14. `https://xrlab.ucsd.edu/ka/ka_home_contributor.html` — 200 OK
15. `https://xrlab.ucsd.edu/ka/ka_home_theory.html` — 200 OK
16. `https://xrlab.ucsd.edu/ka/ka_home_student_new.html` — 200 OK

### Negative checks
17. `week2_quickstart.html` should NOT be on the server (or if already there, leave it — don't deploy the new version)
18. `ka_home_student.html` was NOT overwritten

---

## Do NOT Modify

- Any `.json` data files
- `ka_home.html` or `ka_user_home.html`
- `160sp/ka_student_setup.html`
- Any files not listed in the inventory above
