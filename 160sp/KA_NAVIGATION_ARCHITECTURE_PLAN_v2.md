# K-ATLAS Navigation Architecture Plan v2

**Date**: 2026-04-12  
**Author**: Claude (with David Kirsh)  
**Status**: DETAILED DRAFT — for review by David, AG, and Codex  
**Supersedes**: KA_NAVIGATION_ARCHITECTURE_PLAN.md (v1)

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Design Principles (Grounded)](#2-design-principles)
3. [Architecture Overview](#3-architecture-overview)
4. [Global Site Navigation](#4-global-site-navigation)
5. [Course Site Navigation](#5-course-site-navigation)
6. [Topic Pages Redesign](#6-topic-pages-redesign)
7. [Track Portal Pages](#7-track-portal-pages)
8. [Fall 160 Subsite](#8-fall-160-subsite)
9. [Auth Widget & Profile Dropdown](#9-auth-widget--profile-dropdown)
10. [Shared Infrastructure Files](#10-shared-infrastructure-files)
11. [Design Agent Pipeline Integration](#11-design-agent-pipeline-integration)
12. [Contracts](#12-contracts)
13. [Self-Testing & Validation](#13-self-testing--validation)
14. [Migration Strategy (Pipeline-Integrated)](#14-migration-strategy)
15. [Navigation Skill Specification](#15-navigation-skill-specification)
16. [Open Questions](#16-open-questions)

---

## 1. Problem Statement

### Current State (Empirical)

An audit of 25 representative pages across the site reveals:

| Dimension | Observed Variance |
|-----------|-------------------|
| Navbar implementations | 7+ distinct patterns |
| Wordmark styles | 3 (icon+two-line, icon+single, "K-ATLAS" shorthand) |
| Nav height | 52px vs. 56px (inconsistent even within the same section) |
| Positioning | Mixed `fixed` and `sticky` with no rule |
| Top-bar link count | 0 (ka_home) to 6+ (ka_schedule) — no stable set |
| Breadcrumbs | Present on ~5 of 80+ pages |
| Left sidebar | Present on 4 pages (evidence, articles, tagger, warrants) |
| Auth widget loaded | 0 pages in local repo (exists only on server) |
| Mobile/responsive nav | None (no hamburger, no breakpoints on any page) |
| Shared CSS files | 0 (every page has inline `<style>` blocks for nav) |

### Consequences

1. **Cognitive load violation**: Students encounter a different interface on nearly every click. Per Sweller's cognitive load theory, extraneous load from inconsistent UI competes with germane load from the actual content (Sweller, 1988; cited ~15,400 times).

2. **Information scent failure**: Per Shneiderman's information-seeking mantra — "overview first, zoom and filter, details on demand" — users cannot form a stable mental model of the site's structure when the structure itself keeps changing (Shneiderman, 1996; cited ~4,200 times).

3. **No progressive disclosure**: Without a persistent left-hand nav, users must hold the site's hierarchy in working memory. Miller's 7±2 constraint (Miller, 1956; cited ~25,000 times) and more recent estimates of 3–5 chunks (Cowan, 2001; cited ~5,600 times) mean students literally cannot maintain a map of 80+ pages.

4. **Maintenance burden**: Each new page requires reinventing navigation markup. No skill or contract exists to guide AI workers or human developers.

---

## 2. Design Principles (Grounded in Project Norms)

These principles are drawn from the project's own `SCIENCE_COMMUNICATION_NORMS.md`, `WRITING_STYLE_GUIDE.md`, the Academic Presentation Service, and the ATLAS Visualization Design Service. They are not generic UI advice — they are the project's commitments applied to navigation.

### P1. Structure Is Communication (Doumont)

> "A well-organized page with mediocre prose communicates better than a brilliantly designed page with poor organization."

The navigation IS the structure. If the nav is inconsistent, the site's intellectual organization is invisible. Every page must declare its position in the hierarchy through breadcrumbs, left-nav highlighting, and top-bar regime.

### P2. Data-Ink Maximization (Tufte)

Every visual element in the nav must earn its place by conveying unique information. Remove: decorative icons, redundant emoji, gradient fills that don't encode data. The nav should have a "lard factor" below 20% — meaning fewer than 1 in 5 pixels carries no information.

**Specific application**: No decorative separators between nav links. No icons next to text labels that repeat the label's meaning. Track colors encode category — don't also use track icons AND track labels AND track numbers for the same distinction.

### P3. Cognitive Load Management (Sweller / Mayer)

Working memory holds 3–5 novel chunks. The top bar should have ≤6 links. The left nav should show ≤7 top-level sections, with subsections collapsed by default. Progressive disclosure is mandatory: expand on demand, never dump everything.

**The Shneiderman sequence**: Overview (top bar + left nav sections) → Zoom (expand a section) → Filter (track personalization) → Details (the page content itself).

### P4. The Billboard Test (3-Second Comprehension)

Every page must communicate its core purpose in 3 seconds to a first-time visitor. The nav contributes by answering: Where am I? What section is this? How do I get back? These answers must be available pre-attentively — through position, color, and typography — not by reading small text.

### P5. Honest Uncertainty (Carson / Sagan)

Where the nav displays dynamic data (grades, deadlines, progress), it must be honest about currency: "Updated 2h ago" rather than implying real-time accuracy when the data is cached. Status indicators use the project's confidence spectrum: saturated color for confirmed, lighter for tentative.

### P6. Scaffolded Complexity (Feynman Staircase)

New students see a simplified left nav (Course, Assignments, Your Track, Resources). As they progress through weeks, additional sections become visible (Sprint work, Integration, Final Presentations). The nav grows with the student's familiarity — it does not present the entire semester's complexity on day one.

### P7. Functional Color Only (Ware / Tufte)

Every color in the nav must distinguish categories or encode quantity. The four track colors (gold, green, blue, pink) are functional — they map 1:1 to tracks. The amber accent marks the active/current item. Navy is the background. No additional decorative colors.

| Color | Function |
|-------|----------|
| `#1C3D3A` (navy) | Nav background — constant, stable |
| `#E8872A` (amber) | Active item / current page / accent |
| `#F7F4EF` (cream) | Breadcrumb bar / left nav background |
| `#FFF0CC` (gold) | Track 1: Image Tagging |
| `#E3F4EC` (green) | Track 2: Article Finder |
| `#E8F0FD` (blue) | Track 3: VR Production |
| `#FDE8F4` (pink) | Track 4: GUI Evaluation |
| `#2A7868` (teal) | Hover state / secondary accent |
| `#A8C8BF` (muted teal) | Inactive nav text |

---

## 3. Architecture Overview

### Three-Layer Navigation Model

```
LAYER 1: TOP BAR (fixed, 52px)
─────────────────────────────────────────────────────────
  Identity    |    Stable Links (regime-specific)    |  Auth
  (Wordmark)  |    (never change within regime)      | (Widget)

LAYER 2: BREADCRUMB BAR (sticky below top bar, 36px)
─────────────────────────────────────────────────────────
  Home > Section > Subsection > Current Page

LAYER 3: LEFT JOURNEY NAV (240px sidebar, collapsible)
─────────────────────────────────────────────────────────
  ▾ Expanded Section (current context)
    · Sub-page (linked)
    · Sub-page (active — highlighted)
    · Sub-page (linked)
  ▸ Collapsed Section
  ▸ Collapsed Section
```

### Two Nav Regimes

| Regime | Scope | Top Bar Links | Left Nav Content |
|--------|-------|---------------|------------------|
| **Global** | All non-course pages (~45 files) | Explore, Evidence, Articles, Contribute, Course | User-type journey (student, researcher, instructor, contributor, practitioner, theory) |
| **Course** | All 160sp/ pages (~34 files) | Syllabus, A0, A1, Sprints, Tracks | Course journey (assignments, tracks, weeks, resources) |
| **Fall 160** | Designing_Experiments/ + fall160_schedule.html | Syllabus, Assignments, Tracks, Tools | Fall course journey (phases, experiments, tracks) |

### What Each Layer Answers

| Layer | Question Answered | Changes When? |
|-------|-------------------|---------------|
| Top bar | "What site am I on? What are the main areas?" | Never within a regime |
| Breadcrumb | "Where exactly am I? How do I go up?" | Every page |
| Left nav | "What's in this section? Where am I in the journey?" | Per section; auto-expands current context |

---

## 4. Global Site Navigation

### 4A. Top Bar (Global Regime)

```
┌─────────────────────────────────────────────────────────────┐
│  K-ATLAS          Explore  Evidence  Articles  Contribute   │
│  (wordmark,       (stable link set — never changes)         │
│   links home)                                    [Avatar ▾] │
└─────────────────────────────────────────────────────────────┘
```

| Position | Element | Target | Always Visible? |
|----------|---------|--------|-----------------|
| Left | "K-ATLAS" wordmark (amber on navy, Georgia serif, 1.1rem) | ka_home.html | Yes |
| Center-1 | Explore | ka_topics.html | Yes |
| Center-2 | Evidence | ka_evidence.html | Yes |
| Center-3 | Articles | ka_article_search.html | Yes |
| Center-4 | Contribute | ka_contribute.html | Yes |
| Right | Auth Widget | — | Yes (changes state based on login) |

**When logged out**: Auth widget shows "Log in" link only. No "Register" button in the top bar. Registration is accessed from the login page or from portal page CTAs. This keeps the nav clean and avoids a call-to-action competing with content links.

**When logged in**: Auth widget shows avatar (initials, user-type color background) with dropdown. No "Log in" or "Register" visible anywhere. "Log out" lives exclusively in the profile dropdown.

**Note**: "Course" is NOT in the global top bar. It's accessed from the left nav's journey sections. This keeps the top bar to 4 content links + auth, within the 5±2 cognitive limit.

### 4B. Breadcrumb Bar (Global Regime)

```
┌─────────────────────────────────────────────────────────────┐
│  K-ATLAS  ›  Evidence  ›  Warrant Types                     │
└─────────────────────────────────────────────────────────────┘
```

- Cream background (`#F7F4EF`), 36px height, 1px bottom border
- Each segment is a link except the last (current page, bold, no link)
- Separator: `›` (right-pointing, muted color)
- On the home page: breadcrumb bar is hidden (home IS the root)

### 4C. Left Journey Nav (Global Regime)

The left nav adapts to the user's role. Role is read from `ka_current_user.role` in localStorage. If no user is logged in, default to "Explorer" (a generic superset).

**Rendering rule**: The section containing the current page is auto-expanded. All other sections are collapsed. The current page is highlighted with an amber left-border.

#### Student Journey (left nav)

```
▾ Getting Started
  · Register & Login        → ka_login.html
  · Student Setup            → 160sp/ka_student_setup.html
  · Choose Your Track        → 160sp/ka_tracks.html

▾ Explore the Atlas           (expanded if currently in this section)
  · Topics                   → ka_topics.html
  · Questions                → ka_question_maker.html  ← NEW entry point
  · Evidence Table           → ka_evidence.html
  · Warrant Types            → ka_warrants.html
  · Knowledge Gaps           → ka_gaps.html

▸ Contribute
  · Propose an Article       → ka_article_propose.html
  · Submit Evidence          → ka_contribute.html
  · My Work                  → ka_my_work.html

▸ Course (COGS 160)
  · Spring 2026              → 160sp/ka_schedule.html
  · Fall 2026                → fall160_schedule.html
```

#### Researcher Journey

```
▾ Evidence System
  · Evidence Table           → ka_evidence.html
  · Warrant Types            → ka_warrants.html
  · Knowledge Gaps           → ka_gaps.html

▾ Article Pipeline
  · Search Articles          → ka_article_search.html
  · Propose Articles         → ka_article_propose.html
  · Argumentation            → ka_argumentation.html

▸ Analysis Tools
  · Hypothesis Builder       → ka_hypothesis_builder.html
  · Question Maker           → ka_question_maker.html
  · Interpretation           → ka_interpretation.html

▸ System
  · How It Works             → ka_explain_system.html
  · AI Methodology           → ka_ai_methodology.html
```

#### Instructor Journey

The instructor left nav has **two accordion views**, defaulting to Student View open:

```
▾ Student View                (default OPEN)
  · Schedule                 → 160sp/ka_schedule.html
  · Student Setup            → 160sp/ka_student_setup.html
  · Tracks Overview          → 160sp/ka_tracks.html
  · Week-by-Week Agendas     → (expandable sub-list)

▸ Instructor View             (collapsed by default)
  · Instructor Prep          → 160sp/instructor_prep.html
  · Approve Submissions      → 160sp/ka_approve.html
  · Grading Dashboard        → 160sp/ka_grades.html (NEW)
  · Student Roster           → 160sp/ka_roster.html (NEW)
  · Track Health             → (inline metrics)

▸ Content Management
  · Topics                   → ka_topics.html
  · Evidence                 → ka_evidence.html
  · Articles                 → ka_article_search.html
  · Workflow Hub             → ka_workflow_hub.html
```

If the nav is long, the accordion pattern keeps it manageable: only one view is expanded at a time, and the default (Student View) is what the instructor most often needs — seeing what students see.

#### Contributor / Practitioner / Theory Journeys

Similar patterns adapted to their existing portal page structures:

- **Contributor**: Step-based (Step 1: Learn Standards → Step 2: Find Topics → Step 3: Submit → Step 4: Track Progress)
- **Practitioner**: Space-type filtered (Select Space → View Evidence → Evaluate Decision → Build Brief)
- **Theory**: Framework-based (Pick Frameworks → Explore Mechanisms → Compare Theories → Critical Tests)

Each mirrors the step/journey framing already present in their respective portal pages (`ka_home_contributor.html`, `ka_home_practitioner.html`, `ka_home_theory.html`).

---

## 5. Course Site Navigation

### 5A. Top Bar (Course Regime)

```
┌─────────────────────────────────────────────────────────────┐
│  K-ATLAS   COGS 160    Syllabus  A0  A1  Sprints  Tracks   │
│  (home)    (amber,     (assignment-oriented links)          │
│            course ID)                            [Avatar ▾] │
└─────────────────────────────────────────────────────────────┘
```

| Position | Element | Target | Notes |
|----------|---------|--------|-------|
| Left-1 | "K-ATLAS" wordmark | ka_home.html | Returns to global site |
| Left-2 | "COGS 160" | 160sp/ka_schedule.html | Course identity marker, amber text, acts as course home |
| Center-1 | Syllabus | 160sp/ka_schedule.html | Master schedule |
| Center-2 | A0 | 160sp/ka_collect_articles.html | Assignment 0 |
| Center-3 | A1 | 160sp/week2_exercises.html | Assignment 1 |
| Center-4 | Sprints | 160sp/ka_tracks.html#sprints | Track-specific sprint work (A2+) |
| Center-5 | Tracks | 160sp/ka_tracks.html | Track overview / selection |
| Right | Auth Widget | — | Personalized dropdown |

**Why "Sprints" instead of "A2, A3, A4..."**: After A1, assignments are track-specific and sprint-numbered. Different tracks may have different sprint deliverables on different weeks. A single "Sprints" link leads to the tracks page where the student's own track is auto-expanded, showing their current sprint. This avoids a top bar that grows with each new assignment.

### 5B. Breadcrumb Bar (Course Regime)

```
┌─────────────────────────────────────────────────────────────┐
│  COGS 160  ›  Tracks  ›  Image Tagging  ›  Sprint 1        │
└─────────────────────────────────────────────────────────────┘
```

Note: breadcrumbs in the course regime start from "COGS 160" (not "K-ATLAS"), because that's the relevant root for students. Clicking "K-ATLAS" in the top bar takes them to the global site; the breadcrumbs keep them in course context.

### 5C. Left Journey Nav (Course Regime)

```
▾ Course                                    ← always visible
  · Syllabus / Schedule
  · Student Setup
  · Technical Setup

▾ Assignments                               ← always visible
  · A0: Collect Articles
  · A1: Programming Exercises

▾ Your Track: Image Tagging                 ← PERSONALIZED, auto-expanded
  · Track Portal                            ← NEW page (ka_track1_portal.html)
  · Sprint 1 Workbook                       ← ka_tag_assignment.html
  · Sprint 2 Workbook                       ← (when available)
  · Your Team                               ← team members, within-track
  · GitHub Branch                           ← link to track/1-staging
  · Submit Work                             ← submission form

▸ Track AF: Article Finder                  ← collapsed (not your track)
▸ Track IT: Image Tagging                   ← hidden (IS your track, shown above)
▸ Track AI+VR: VR Production                ← collapsed
▸ Track GUI: GUI Evaluation                 ← collapsed

▾ Weekly Agendas                            ← current week highlighted
  · Week 1: Orientation
  · Week 2: First Assignment
  · ● Week 3: Track Selection               ← amber dot = current week
  · Week 4–7: Sprint Work
  · Week 8: Integration
  · Weeks 9–10: Presentations

▸ Resources
  · Google Scholar Guide
  · Evidence Explorer
  · Argumentation Viewer
  · Ask / Office Hours

▸ Fall 160                                  ← link to fall subsite
```

**Personalization logic**:
1. Read `ka_current_user.track` from localStorage
2. The user's track section title changes to "Your Track: [Track Name]" and auto-expands
3. The corresponding track in the collapsed track list is hidden (no duplication)
4. If no track is assigned yet, show "Choose Your Track" with a link to ka_tracks.html
5. Current week is detected by date (Week 1 starts March 30, 2026) and marked

**Teams within tracks**: Team membership is displayed within the track section, not at the course level. When a student clicks "Your Team," they see their team members, each member's role/progress, and any shared resources. This is contained within the track portal.

### 5D. Profile Dropdown (Course-Specific)

When logged in on a course page, the auth widget dropdown includes course-personalized items:

```
┌──────────────────────────────┐
│  Jane Student                 │
│  jstudent@ucsd.edu            │
│  Track: Article Finder        │
│  Team: Pipeline Alpha         │
├──────────────────────────────┤
│  What's Due                   │  → computed from schedule data
│    A1 due Sun Apr 13          │  → next upcoming deadline
│    Track selection by Apr 18  │
├──────────────────────────────┤
│  My Grades                    │  → 160sp/ka_grades.html
│  My Profile                   │  → ka_account_settings.html
│  My Submissions               │  → 160sp/ka_submissions.html (NEW)
├──────────────────────────────┤
│  Log out                      │
└──────────────────────────────┘
```

**"What's Due" computation**: `ka_nav.js` reads the `schedule.deadlines` array from `ka_nav_config.json`, filters for deadlines after today, and displays the next 2. If the student's track has track-specific deadlines, those are included. This is a read-only display — no API call needed, just date comparison against config data.

---

## 6. Topic Pages Redesign

### Current State (Good Foundations)

The topic pages already use cluster-level cards in a 3-column grid, with VOI scoring, category badges, construct tags, and 4 action buttons (Ask, Articles, Questions, Study Design). This is well-designed and should be preserved.

### Changes Required

#### 6A. Card-Level Changes

**Keep**: Card grid layout, VOI indicator, category badge, construct tags, maturity label, paper count.

**Add small links at bottom of each card**:

```
┌─────────────────────────────────┐
│  [Category Badge]    [VOI dot]  │
│                                 │
│  Topic Name (Georgia, bold)     │
│  Short description (2-3 lines)  │
│                                 │
│  [Construct tag] [Construct]    │
│                                 │
│  ──────────────────────────     │
│  📄 PDFs  ·  📝 Summary  ·  🔗 Related  │
└─────────────────────────────────┘
```

- **PDFs**: Links to the source articles in the cluster (opens a filtered article search showing PDFs in this cluster)
- **Summary**: Opens a one-paragraph AI-generated summary of the cluster's key findings (can be a tooltip or expandable inline)
- **Related**: Links to other clusters that share constructs or mechanisms (filtered topic view)

These replace the current 4 action buttons (Ask, Articles, Questions, Study Design) which are tool-oriented. The new links are content-oriented — they answer "what's here?" before "what can I do with it?"

The tool actions (Ask, Questions, Study Design) move to the **detail panel** that opens when a card is clicked. This follows Shneiderman's overview→detail sequence: cards provide the overview, the detail panel provides the tools.

#### 6B. Questions Page as Alternate Entry Point

**New page**: `ka_questions.html` — A "Did You Know?" questions page that provides a curiosity-driven route into topics.

**Structure**:

```
[Top bar — global regime]
[Breadcrumb: K-ATLAS > Questions]

┌──────────────┬──────────────────────────────────────────────┐
│  LEFT NAV    │  Did You Know?                               │
│  (Explorer   │                                              │
│   journey)   │  [Filter tabs: All | Surprising | Debated |  │
│              │   Unsolved | Most Cited]                     │
│              │                                              │
│              │  ┌─────────────────────────────────────┐     │
│              │  │ "Open offices were supposed to help │     │
│              │  │  collaboration — but actually reduce│     │
│              │  │  face-to-face interaction by 70%."  │     │
│              │  │                                     │     │
│              │  │  Topic: Workspace Layout             │     │
│              │  │  Evidence: Strong (5 studies, d=0.6) │     │
│              │  │  [Explore Topic →]                   │     │
│              │  └─────────────────────────────────────┘     │
│              │                                              │
│              │  ┌─────────────────────────────────────┐     │
│              │  │ "Hospital patients in rooms with a  │     │
│              │  │  view of trees recover faster and   │     │
│              │  │  need fewer painkillers."            │     │
│              │  │                                     │     │
│              │  │  Topic: Nature Views & Recovery      │     │
│              │  │  Evidence: Established (meta-analysis│     │
│              │  │  [Explore Topic →]                   │     │
│              │  └─────────────────────────────────────┘     │
│              │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

**Content generation**: Each question/factoid is derived from the topic cluster data — specifically from the highest-VOI or most-replicated findings. The "Surprising" tab prioritizes counter-intuitive findings. The "Debated" tab shows claims with contradictions. The "Unsolved" tab shows high-VOI gaps.

**Each card links to the parent topic**: The "Explore Topic →" link takes the user to the topic card's detail panel, providing a seamless transition from curiosity to systematic exploration.

#### 6C. Granularity Rule

**Topic cards MUST display high-level research clusters only** — not subtopics, not individual papers, not fine-grained constructs. The current 20 primary "research fronts" are the right granularity. If the topic database grows, group new topics into existing clusters or create new high-level clusters — never add subtopic cards to the main grid.

Subtopics appear only inside the detail panel when a topic card is clicked. This follows P6 (Scaffolded Complexity): overview first, detail on demand.

---

## 7. Track Portal Pages

### Template Structure

Each track gets a dedicated portal page serving as the student's home base within that track. These are **new pages** (ka_track1_portal.html through ka_track4_portal.html).

```
[Top bar — course regime]
[Breadcrumb: COGS 160 > Tracks > Image Tagging]

┌──────────────┬──────────────────────────────────────────────┐
│  LEFT NAV    │  TRACK PORTAL: Image Tagging                 │
│  (course     │                                              │
│   journey,   │  ┌──────────────────────────────────────┐    │
│   this track │  │ [Track color hero banner]             │    │
│   expanded)  │  │ Status: Week 3 — Sprint begins W4    │    │
│              │  │ Team: Pixel Scouts (3 members)        │    │
│              │  └──────────────────────────────────────┘    │
│              │                                              │
│              │  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│              │  │ Sprint   │ │ GitHub   │ │ Submit   │     │
│              │  │ Workbook │ │ Branch   │ │ Work     │     │
│              │  └──────────┘ └──────────┘ └──────────┘     │
│              │                                              │
│              │  ─── This Week's Tasks ───                   │
│              │  □ Read sprint 1 requirements                │
│              │  □ Set up development environment             │
│              │  □ Complete checkpoint 1                      │
│              │                                              │
│              │  ─── Your Team ───                           │
│              │  · Alice Chen (Lead) — checkpoint 1 ✓        │
│              │  · Bob Park — checkpoint 1 pending           │
│              │  · You — checkpoint 1 pending                │
│              │                                              │
│              │  ─── Resources ───                           │
│              │  · K-ATLAS Tagger Tool                       │
│              │  · JSON Schema Reference                     │
│              │  · Track-Specific Slack Channel               │
│              │                                              │
│              │  ─── Progress ───                            │
│              │  ✓ Track assigned (Week 3)                   │
│              │  ✓ Team formed                                │
│              │  □ Sprint 1 submitted                        │
│              │  ○ Sprint 2 (not yet available)              │
│              │  ○ Integration (Week 8)                      │
│              │  ○ Final presentation (Week 9-10)            │
│              │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

### Four Track Portals

| Track | Portal URL | Color | Sprint Workbook | GitHub |
|-------|-----------|-------|-----------------|--------|
| **Image Tagging** | 160sp/ka_track1_portal.html | Gold (#FFF0CC / #7A4F00) | ka_tag_assignment.html | track/1-staging |
| **Article Finder** | 160sp/ka_track2_portal.html | Green (#E3F4EC / #1A5C30) | ka_article_finder_assignment.html | track/2-staging |
| **VR Production** | 160sp/ka_track3_portal.html | Blue (#E8F0FD / #1A3A7A) | ka_vr_assignment.html | track/3-staging |
| **GUI Evaluation** | 160sp/ka_track4_portal.html | Pink (#FDE8F4 / #7A1A5C) | ka_gui_assignment.html | track/4-staging |

### Team Management (Within Track)

Teams are formed within tracks after A1. Team management appears in the track portal:
- Team name, team members (from ka_workflow.db registrations table)
- Each member's progress on the current sprint
- Team-level submission status
- Instructor can view all teams across all tracks from the Instructor View accordion

---

## 8. Fall 160 Subsite

### Identification

**Fall 160 = "Experiment Making"**. The main schedule page is `fall160_schedule.html` (64KB). The `Designing_Experiments/` directory contains supplementary tools and student track documentation that supports both courses.

**This is a separate subsite** with its own nav regime, but sharing the K-ATLAS visual language.

### Top Bar (Fall 160 Regime)

```
┌─────────────────────────────────────────────────────────────┐
│  K-ATLAS   COGS 160F   Syllabus  Phases  Tracks  Tools     │
│  (home)    (amber)                                [Avatar ▾]│
└─────────────────────────────────────────────────────────────┘
```

### Left Nav (Fall 160 Regime)

```
▾ Course
  · Fall Schedule
  · Pre-Requisites

▾ Phases
  · Phase 1: Design & Build (Wk 1–5)
  · Phase 2: Pre-Registration (Wk 6–7)
  · Phase 3: Sensor Setup (Wk 8)
  · Phase 4: Pilot & Write-Up (Wk 9–10)

▸ Tracks
  · VR Stimulus Design
  · Image Annotation
  · GUI/Acoustics/Adaptive

▸ Tools
  · Experiment Wizard
  · Hypothesis Builder
  · Measurement Instruments
  · Sensor Catalogue

▸ Spring 160                         ← cross-link to spring
```

### File Organization

The `Designing_Experiments/` directory stays where it is but is treated as the Fall subsite's content area. Pages within it use the Fall 160 nav regime. The tools (experiment wizard, hypothesis builder, etc.) are shared infrastructure accessible from both Spring and Fall left navs.

---

## 9. Auth Widget & Profile Dropdown

### Unified Widget Behavior

The auth widget (currently in `ka_auth_widget.js`, 472 lines) is refactored into `ka_nav.js`. Its behavior:

**Logged out**:
- Shows "Log in" text link in the top bar's right section
- No "Register" button in the nav (registration is accessed from the login page or portal CTAs)
- Left nav shows a generic "Explorer" journey

**Logged in**:
- Shows avatar (initials on user-type–colored circle)
- Click opens dropdown
- No "Log in" or "Register" visible anywhere
- Left nav adapts to user's role

### Dropdown Contents

| Item | Source | Behavior |
|------|--------|----------|
| Name + email | `ka_current_user` (localStorage) | Display only |
| Track + Team | `ka_current_user.track` + team lookup | Display; links to track portal |
| What's Due | `ka_nav_config.json` schedule data | Computed client-side; shows next 2 deadlines |
| My Grades | — | Links to 160sp/ka_grades.html (course) or hidden (global) |
| My Profile | — | Links to ka_account_settings.html |
| My Submissions | — | Links to 160sp/ka_submissions.html (course) or ka_my_work.html (global) |
| Log out | — | Clears localStorage, reloads page |

### What "What's Due" Displays

```javascript
// Pseudocode for deadline computation
const now = new Date();
const deadlines = config.schedule.deadlines
  .filter(d => new Date(d.due) > now)
  .sort((a, b) => new Date(a.due) - new Date(b.due))
  .slice(0, 2);

// Track-specific deadlines included if user has a track
if (user.track) {
  const trackDeadlines = config.schedule.track_deadlines[user.track]
    .filter(d => new Date(d.due) > now);
  deadlines.push(...trackDeadlines);
  deadlines.sort((a, b) => new Date(a.due) - new Date(b.due));
  deadlines = deadlines.slice(0, 3);
}
```

---

## 10. Shared Infrastructure Files

### 10A. `ka_nav.css` (~400 lines estimated)

All navigation styling in one file. Organized by component:

```css
/* === TOP BAR === */
/* Shared across all regimes */

/* === BREADCRUMB BAR === */

/* === LEFT NAV === */
/* Sections, items, expand/collapse, active state, track colors */

/* === AUTH WIDGET === */
/* Avatar, dropdown, dropdown items */

/* === MOBILE RESPONSIVE === */
/* Hamburger, slide-out, breakpoints */

/* === TRACK COLOR TOKENS === */
/* .track-1, .track-2, .track-3, .track-4 */

/* === UTILITY === */
/* Current-week highlight, active-page indicator */
```

**Every page includes**: `<link rel="stylesheet" href="/ka/ka_nav.css">`
(For 160sp/ pages: `href="../ka_nav.css"`)

### 10B. `ka_nav.js` (~600 lines estimated)

Single script handling all nav behavior. Modules:

```javascript
// 1. AUTH STATE
//    - Read localStorage (token, user, refresh_token)
//    - Token refresh on 401 (absorbed from ka_auth_widget.js)
//    - Login/logout helpers

// 2. PAGE CONTEXT
//    - Read window.__KA_PAGE__ metadata
//    - Determine regime (global/course/fall160)
//    - Determine current section and page

// 3. TOP BAR INJECTION
//    - Build top bar HTML from config
//    - Set active link based on current page
//    - Inject auth widget (logged-in or logged-out state)

// 4. BREADCRUMB INJECTION
//    - Build breadcrumb from __KA_PAGE__.breadcrumb array
//    - Inject below top bar

// 5. LEFT NAV INJECTION
//    - Read nav structure from config (regime + user role)
//    - Build collapsible section HTML
//    - Auto-expand section containing current page
//    - Personalize track section (if course regime + user has track)
//    - Highlight current page with amber left-border
//    - Attach expand/collapse click handlers

// 6. PROFILE DROPDOWN
//    - Build dropdown HTML
//    - Compute "What's Due" from schedule config
//    - Attach toggle handler
//    - Close on outside click

// 7. MOBILE
//    - Hamburger toggle for top bar
//    - Slide-out for left nav
//    - Breakpoint: 768px

// 8. WEEK DETECTION
//    - Compute current course week from date
//    - Apply current-week highlight in left nav
//    - Expose window.__KA_CURRENT_WEEK__ for page use

// 9. SELF-TEST (development mode)
//    - Validate __KA_PAGE__ metadata completeness
//    - Check all nav links resolve to existing pages
//    - Warn on missing breadcrumb segments
//    - Log validation results to console
```

**Every page includes**: `<script src="/ka/ka_nav.js"></script>`

### 10C. `ka_nav_config.json` (~200 lines)

Declarative nav structure. Excerpt:

```json
{
  "regimes": {
    "global": {
      "topbar": [
        {"label": "Explore", "href": "/ka/ka_topics.html", "id": "explore"},
        {"label": "Evidence", "href": "/ka/ka_evidence.html", "id": "evidence"},
        {"label": "Articles", "href": "/ka/ka_article_search.html", "id": "articles"},
        {"label": "Contribute", "href": "/ka/ka_contribute.html", "id": "contribute"}
      ],
      "journeys": {
        "student": {
          "sections": [
            {
              "title": "Getting Started",
              "id": "getting-started",
              "items": [
                {"label": "Register & Login", "href": "/ka/ka_login.html", "id": "login"},
                {"label": "Student Setup", "href": "/ka/160sp/ka_student_setup.html", "id": "setup"},
                {"label": "Choose Your Track", "href": "/ka/160sp/ka_tracks.html", "id": "tracks"}
              ]
            },
            {
              "title": "Explore the Atlas",
              "id": "explore-atlas",
              "items": [
                {"label": "Topics", "href": "/ka/ka_topics.html", "id": "topics"},
                {"label": "Questions", "href": "/ka/ka_questions.html", "id": "questions"},
                {"label": "Evidence Table", "href": "/ka/ka_evidence.html", "id": "evidence"},
                {"label": "Warrant Types", "href": "/ka/ka_warrants.html", "id": "warrants"},
                {"label": "Knowledge Gaps", "href": "/ka/ka_gaps.html", "id": "gaps"}
              ]
            }
          ]
        },
        "researcher": { "sections": ["..."] },
        "instructor": { "sections": ["..."] },
        "contributor": { "sections": ["..."] },
        "practitioner": { "sections": ["..."] },
        "theory": { "sections": ["..."] }
      }
    },
    "course": {
      "topbar": [
        {"label": "Syllabus", "href": "/ka/160sp/ka_schedule.html", "id": "syllabus"},
        {"label": "A0", "href": "/ka/160sp/ka_collect_articles.html", "id": "a0"},
        {"label": "A1", "href": "/ka/160sp/week2_exercises.html", "id": "a1"},
        {"label": "Sprints", "href": "/ka/160sp/ka_tracks.html#sprints", "id": "sprints"},
        {"label": "Tracks", "href": "/ka/160sp/ka_tracks.html", "id": "tracks"}
      ],
      "left_nav": {
        "sections": [
          {
            "title": "Course",
            "id": "course-info",
            "items": [
              {"label": "Syllabus / Schedule", "href": "/ka/160sp/ka_schedule.html", "id": "schedule"},
              {"label": "Student Setup", "href": "/ka/160sp/ka_student_setup.html", "id": "student-setup"},
              {"label": "Technical Setup", "href": "/ka/160sp/ka_technical_setup.html", "id": "tech-setup"}
            ]
          },
          {
            "title": "Assignments",
            "id": "assignments",
            "items": [
              {"label": "A0: Collect Articles", "href": "/ka/160sp/ka_collect_articles.html", "id": "a0"},
              {"label": "A1: Programming Exercises", "href": "/ka/160sp/week2_exercises.html", "id": "a1"}
            ]
          },
          {
            "title": "Your Track: {TRACK_NAME}",
            "id": "your-track",
            "personalized": true,
            "track_dependent": true,
            "items": [
              {"label": "Track Portal", "href": "/ka/160sp/ka_track{N}_portal.html", "id": "portal"},
              {"label": "Sprint Workbook", "href": "/ka/160sp/ka_track{N}_assignment.html", "id": "workbook"},
              {"label": "Your Team", "href": "/ka/160sp/ka_track{N}_portal.html#team", "id": "team"},
              {"label": "GitHub Branch", "href": "https://github.com/dkirsh/Knowledge_Atlas/tree/track/{N}-staging", "id": "github", "external": true},
              {"label": "Submit Work", "href": "/ka/160sp/ka_track{N}_portal.html#submit", "id": "submit"}
            ]
          }
        ]
      }
    },
    "fall160": {
      "topbar": [
        {"label": "Syllabus", "href": "/ka/fall160_schedule.html", "id": "f-syllabus"},
        {"label": "Phases", "href": "/ka/fall160_schedule.html#phases", "id": "f-phases"},
        {"label": "Tracks", "href": "/ka/Designing_Experiments/docs/student_tracks/", "id": "f-tracks"},
        {"label": "Tools", "href": "/ka/Designing_Experiments/experiment_wizard.html", "id": "f-tools"}
      ],
      "left_nav": { "sections": ["..."] }
    }
  },
  "schedule": {
    "week1_start": "2026-03-30",
    "deadlines": [
      {"id": "a0", "label": "A0: Collect Articles", "due": "2026-04-06", "type": "assignment"},
      {"id": "a1", "label": "A1: Programming Exercises", "due": "2026-04-13", "type": "assignment"},
      {"id": "track-selection", "label": "Track Selection", "due": "2026-04-18", "type": "milestone"}
    ],
    "track_deadlines": {
      "1": [
        {"id": "t1-s1", "label": "Sprint 1: Initial Annotations", "due": "2026-04-27", "type": "sprint"}
      ],
      "2": [
        {"id": "t2-s1", "label": "Sprint 1: Query Engine", "due": "2026-04-27", "type": "sprint"}
      ],
      "3": [
        {"id": "t3-s1", "label": "Sprint 1: Scene Prototype", "due": "2026-04-27", "type": "sprint"}
      ],
      "4": [
        {"id": "t4-s1", "label": "Sprint 1: Interface Spec", "due": "2026-04-27", "type": "sprint"}
      ]
    }
  },
  "tracks": {
    "1": {"name": "Image Tagging", "short": "IT", "color": "#FFF0CC", "textColor": "#7A4F00"},
    "2": {"name": "Article Finder", "short": "AF", "color": "#E3F4EC", "textColor": "#1A5C30"},
    "3": {"name": "VR Production", "short": "VR", "color": "#E8F0FD", "textColor": "#1A3A7A"},
    "4": {"name": "GUI Evaluation", "short": "GUI", "color": "#FDE8F4", "textColor": "#7A1A5C"}
  }
}
```

### 10D. Page Metadata Convention

Each page includes a small data block in `<head>` before the nav script:

```html
<head>
  <!-- ... existing head content ... -->
  <link rel="stylesheet" href="../ka_nav.css">
  <script>
    window.__KA_PAGE__ = {
      regime: 'course',
      section: 'assignments',
      page: 'a1',
      breadcrumb: [
        {label: 'COGS 160', href: 'ka_schedule.html'},
        {label: 'Assignments'},
        {label: 'A1: Programming Exercises'}
      ],
      title: 'A1: Programming Exercises'
    };
  </script>
  <script src="../ka_nav.js"></script>
</head>
```

**Required fields**:
- `regime`: 'global' | 'course' | 'fall160'
- `section`: ID of the left-nav section this page belongs to
- `page`: ID matching a left-nav item (for active-state highlighting)
- `breadcrumb`: Array of {label, href?} objects

**Optional fields**:
- `title`: Page title (used in mobile nav header)
- `week`: Force a specific week number (overrides date-based detection)

---

## 11. Design Agent Pipeline Integration

### 11A. The Pipeline

The K-ATLAS project has a four-agent design pipeline (`agents/` directory) that MUST be used for all new pages and all major redesigns. The navigation system — comprising 5 distinct component types (top bar, breadcrumbs, left nav, auth widget/profile dropdown, mobile responsive nav) plus 8 new pages — is a major redesign. Skipping this pipeline would violate the project's own design methodology and produce components that haven't been evaluated against the 35-dimension usability framework.

**The agents, in execution order:**

```
STEP 1: Science-Writing Agent
  Input:  Page function, persona guidance, journey benchmarks
  Output: 13-item copy pack per component/page
  Spec:   agents/SCIENCE_WRITER_AGENT.md

STEP 2: GUI Agent v3
  Input:  Copy pack + this navigation plan
  Output: 32-item interaction spec per component/page
  Spec:   agents/GUI_AGENT_V3.md

STEP 3: GUI Presentation Agent
  Input:  32-item spec + copy pack
  Output: Runnable mockup (HTML/JS for nav components)
  Spec:   agents/GUI_PRESENTATION_AGENT.md

STEP 4: [PARALLEL]
  4a. Usability Critic Agent → 35-dimension critique report
      Spec: agents/USABILITY_CRITIC_AGENT.md
  4b. ka_usability_critic.js in-browser session → student ratings

STEP 5: GUI Agent v3 (re-run) → revised spec addressing critique
STEP 6: GUI Presentation Agent (re-run) → revised mockup
STEP 7: Developer → production implementation
```

### 11B. What Gets Run Through the Pipeline

Not every file needs the full pipeline. The components fall into three tiers:

**Tier 1 — Full Pipeline (all 7 steps)**: Components that users interact with on every page and that define the site's identity.

| Component | Primary Role(s) | Rationale |
|-----------|----------------|-----------|
| Top bar (global regime) | All 6 roles | Seen on every page; orientation anchor; 3-second billboard test |
| Top bar (course regime) | student_explorer, instructor | Students see this 50+ times per week |
| Left nav (global, per-journey) | Role-dependent | Journey structure IS the intellectual architecture |
| Left nav (course) | student_explorer | Assignment/sprint navigation is the primary student workflow |
| Profile dropdown | All authenticated | Personalized; "What's Due" must be accurate; grades access |
| Auth widget (logged-in / logged-out) | All | Login state is the primary mode switch |

**Tier 2 — Abbreviated Pipeline (steps 1–2 + 4a, skip mockup)**: New pages where the layout follows established patterns but the copy and interaction spec need design attention.

| Page | Primary Role(s) | Rationale |
|------|----------------|-----------|
| ka_track1_portal.html | student_explorer | Template-based; once one portal is designed, others follow |
| ka_track2_portal.html | student_explorer | Clone of track 1 with different content |
| ka_track3_portal.html | student_explorer | Clone |
| ka_track4_portal.html | student_explorer | Clone |
| ka_questions.html ("Did You Know?") | student_explorer, researcher | Novel page type; needs copy pack for question content |
| ka_grades.html | student_explorer, instructor | Sensitive data display; needs role adaptation |
| ka_submissions.html | student_explorer | Straightforward list; abbreviated OK |
| ka_roster.html | instructor | Admin view; abbreviated OK |

**Tier 3 — Migration Only (no pipeline, just mechanical nav swap)**: Existing pages where the content is unchanged and only the nav markup is being replaced with the shared system.

| Scope | Count | Work |
|-------|-------|------|
| Existing course pages | ~34 | Strip inline nav, add shared includes + `__KA_PAGE__` metadata |
| Existing global pages | ~45 | Same |
| Fall 160 pages | ~18 | Same |

### 11C. Science-Writing Agent Outputs for Nav Components

The Science-Writing Agent produces a 13-item copy pack. For navigation components, some items are adapted:

**For the top bar:**
1. `One-sentence purpose line`: "The top bar tells you what site you're on, gives you the 4–5 main areas, and shows who you are."
2. `Short intro`: N/A (nav components don't have intros)
3. `Expanded explainer`: N/A
4. `Section labels`: The link labels themselves — "Explore", "Evidence", "Articles", "Contribute" (global); "Syllabus", "A0", "A1", "Sprints", "Tracks" (course)
5. `Primary CTA wording`: N/A (top bar has no primary CTA)
6. `Example questions`: N/A
7. `Warnings / caveats`: N/A
8. `Empty-state text`: N/A (top bar is never empty)
9. `Loading-state text`: "Loading navigation..." (for JS-injected nav)
10. `Error-state text`: Fallback static nav links if ka_nav.js fails to load
11. `Tooltip / helper text candidates`: Tooltips for each nav link explaining what the section contains
12. `Beginner variant`: Same links, but with expanded tooltip text explaining each section
13. `Expert variant`: Same links — experts don't need a different top bar

**For the profile dropdown:**
1. `One-sentence purpose line`: "Your profile, your deadlines, your grades — one click."
5. `Primary CTA wording`: "What's Due" (most actionable item in dropdown)
7. `Warnings / caveats`: If deadline data is stale: "Schedule last updated [date]"
8. `Empty-state text`: "No upcoming deadlines" / "No grades yet" / "No track assigned — choose one"
10. `Error-state text`: "Could not load your profile. Try refreshing."
11. `Tooltip / helper text candidates`: "What's Due" → "Your next 2–3 deadlines, computed from the course schedule"

**For the left nav:**
4. `Section labels`: All section titles from ka_nav_config.json (e.g., "Getting Started", "Explore the Atlas", "Assignments", "Your Track: Image Tagging", "Weekly Agendas", "Resources")
8. `Empty-state text`: "Choose Your Track" (when no track assigned), "No agendas yet" (pre-course)
11. `Tooltip / helper text candidates`: Each section title gets a one-line description
12. `Beginner variant`: Fewer sections visible initially (scaffolded complexity — see P6 in §2)
13. `Expert variant`: All sections visible, including collapsed research tools

### 11D. GUI Agent v3 Outputs for Nav Components

The GUI Agent v3 produces 32 items per page/component. For each Tier 1 component, we need the full 32. Key items specific to navigation:

**Item 1 (Purpose)**: "The [component] provides persistent [orientation / journey context / identity / auth state] across all [regime] pages."

**Item 6 (Visible immediately)**: Critical for nav — everything in the nav is visible immediately (above the fold, persistent). The left nav's collapsed sections are "one click away" (item 7).

**Item 9 (First misconception)**: For the left nav: "Students may think clicking a collapsed section navigates away from the current page. It doesn't — it expands in place." For the profile dropdown: "Students may not realize 'What's Due' is personalized to their track."

**Item 12 (Task → Data → View → Interaction):**

| Task | Data Source | View | Interaction |
|------|------------|------|-------------|
| Find my current assignment | ka_nav_config.json deadlines | Left nav: current week highlighted | Click to navigate |
| Check what's due | ka_nav_config.json schedule | Profile dropdown: "What's Due" section | Click avatar → read |
| Navigate to my track | ka_current_user.track (localStorage) | Left nav: "Your Track: [name]" expanded | Auto-expanded; click item to navigate |
| Switch between sections | ka_nav_config.json sections | Left nav: expand/collapse | Click section header |
| Return to course home | Top bar: "COGS 160" link | Top bar | Click |
| Return to global home | Top bar: "K-ATLAS" wordmark | Top bar | Click |
| Log out | Profile dropdown: "Log out" | Dropdown | Click → clear localStorage → reload |

**Item 27 (Framework choice)**: `FRAMEWORK: HTML/JS` — Navigation is static HTML/JS served from the KA repo, not Streamlit. All nav components use `ka_nav.js` + `ka_nav.css`. This is mandatory because nav appears on every page including non-Streamlit pages.

**Item 28 (Viz critique)**: N/A for nav components (no data visualizations in the nav itself). However, the "What's Due" deadline display in the profile dropdown should be evaluated for V15 (contextual text: does it state the deadline clearly?) and V8 (uncertainty: is the schedule data current?).

**Item 29 (Role adaptation table):**

| Role | Top Bar Change | Left Nav Change | Profile Dropdown Change |
|------|---------------|-----------------|------------------------|
| student_explorer | Course regime top bar | Course journey, track expanded | Track, team, "What's Due", grades |
| researcher | Global regime top bar | Researcher journey | No track/team; "My Work" instead |
| instructor | Course regime top bar (same as student) | Student View accordion (open) + Instructor View accordion | Admin items: roster, grading dashboard |
| contributor | Global regime top bar | Contributor journey (step-based) | Submission tracking instead of grades |
| practitioner | Global regime top bar | Practitioner journey (space-type filtered) | No course items |
| theory_mechanism_explorer | Global regime top bar | Theory journey (framework-based) | No course items |

**Item 30 (Workflow CTA spec)**: N/A for nav components (nav is not a workflow step). However, the left nav contains workflow CTAs for pages that ARE workflow steps — these are defined in the page's own GUI Agent v3 spec, not the nav's.

**Item 31 (Usability critic targets):**

| Component | At-Risk Heuristics | Why |
|-----------|-------------------|-----|
| Top bar | H4 (Consistency), R1 (Consistency), H8 (Minimalist) | Two regimes must feel consistent despite different link sets |
| Left nav | H6 (Recognition not recall), R8 (Reduce memory), V17 (Persistent context) | Collapse/expand must not hide current location |
| Profile dropdown | H1 (System status), R3 (Informative feedback), R4 (Closure) | "What's Due" must be current; grades must show clear status |
| Auth widget | H4 (Consistency), H5 (Error prevention) | Login/logout state must be unambiguous; no Register when logged in |
| Breadcrumbs | H6 (Recognition), R8 (Memory load) | Must accurately reflect page hierarchy at all times |
| Mobile nav | H3 (User control), R7 (Locus of control) | Hamburger must be discoverable; slide-out must not trap user |

### 11E. Usability Critic Agent Application

After the nav components are built (Phase 1 in §14), the Usability Critic Agent runs against each component. The evaluation uses the full 35-dimension framework with these ATLAS-specific calibrations:

**Nav-specific heuristic guidance:**

- **H1 (System status)**: Does the nav show which page/section is active? Is the current week highlighted? Is the user's login state unambiguous?
- **H2 (Real-world match)**: Are nav labels in student language, not developer language? ("Syllabus" not "ka_schedule"; "Your Track" not "track_portal")
- **H4 (Consistency)**: Is the same label always in the same position? Does the wordmark always link to the same place? Does the amber accent always mean "active/current"?
- **H6 (Recognition)**: Can the user find their track without remembering its number? Can they find the current week without counting?
- **H8 (Minimalist)**: Are all nav elements earning their place? Is the top bar within the ≤6 link limit? Are collapsed sections truly secondary?
- **R1 (Consistency)**: Do the global and course regimes feel like the same design system, despite different link sets?
- **R8 (Memory load)**: Can the user navigate without remembering information from a previous page?
- **V12 (Preattentive focal signal)**: Is there exactly one accent color (amber) guiding the eye to the active item?

**Minimum passing criteria for nav components:**

- 0 Major Fails on H1, H4, H6, H8, R1, R8
- 0 Major Fails on any V-code (if applicable — mostly N/A for nav)
- ≤3 Minor Issues total across all 35 dimensions
- All 7 success conditions (SC-UC-1 through SC-UC-7) met

If the critique produces Major Fails, the nav design returns to GUI Agent v3 (Step 5) for revision before proceeding to migration.

### 11F. In-Browser Usability Critic Integration

The `ka_usability_critic.js` floating panel (purple 🔎 button) must be loaded on every page post-migration. Currently it's only on 5 pages. After migration:

```html
<!-- Every page includes this alongside ka_nav.js -->
<script src="ka_usability_critic.js"></script>
```

This enables COGS 160 Track 4 (GUI Evaluation) students to run structured heuristic critiques on any page, including the nav components themselves. The in-browser tool produces the same 35-dimension ratings that the Usability Critic Agent processes — creating a feedback loop between student evaluations and agent-driven design revisions.

### 11G. GUI Design Success Conditions Contract

Every page post-migration must pass the automated checks in `config/gui_design_success_conditions.json`:

**Required (must pass — failure blocks deployment):**

| Check | What It Validates |
|-------|-------------------|
| `has_title` | `<title>` tag present |
| `has_viewport` | Responsive viewport meta tag |
| `has_primary_heading_signal` | H1 or equivalent heading |
| `has_nav_or_header_nav` | Nav landmark present (satisfied by ka_nav.js injection) |
| `has_responsive_layout_signal` | Media queries or flex/grid responsive patterns |

**Warning (should pass — logged but not blocking):**

| Check | What It Validates |
|-------|-------------------|
| `has_cta` | At least one action affordance |
| `has_page_purpose_marker` | Explicit purpose or workflow cue |
| `has_evidence_or_source_marker` | Source/evidence language (for evidence-heavy pages) |

The existing `scripts/check_gui_design_contract.py` and `tests/test_gui_design_contract.py` run these checks. Post-migration, `validate_nav.py` (§13) runs alongside these existing tests.

### 11H. Full Pipeline Timeline for Nav Components

```
Day 1 (3 hours):
  Science-Writing Agent → copy packs for:
    - Top bar (global + course)
    - Left nav (6 journey variants + course)
    - Profile dropdown
    - Auth widget states
    - Breadcrumb patterns
    - Mobile nav
  [6 copy packs total, run in parallel]

Day 1–2 (4 hours):
  GUI Agent v3 → 32-item specs for:
    - Top bar (global + course as one spec with regime variants)
    - Left nav (one spec with journey variants)
    - Profile dropdown + auth widget (one spec)
    - Breadcrumbs (one spec)
    - Mobile responsive (one spec)
  [5 specs total, can run in parallel after copy packs]

Day 2 (3 hours):
  Implementation → Build ka_nav.css, ka_nav.js, ka_nav_config.json
  [Informed by the 5 specs and 6 copy packs]

Day 2–3 (2 hours):
  Usability Critic Agent → critique report for each Tier 1 component
  [5 critique reports, run in parallel]
  ka_usability_critic.js → in-browser session on test pages

Day 3 (1–2 hours):
  Revise if needed → Address any Major Fails from critique
  GUI Agent v3 re-run (only for components with Major Fails)

Day 3–4:
  Migration begins (Phase 3 in §14) — only after nav components pass critique
```

---

## 12. Contracts

### Why Contracts

The navigation system has three shared files (`ka_nav.css`, `ka_nav.js`, `ka_nav_config.json`) that must stay synchronized with ~80 web pages. Each page declares a `__KA_PAGE__` metadata block that references IDs defined in the config. If an ID in the config is renamed but pages aren't updated, nav breaks silently — no error, just a missing highlight or broken breadcrumb.

Contracts formalize the interfaces between these components so that violations are caught at build/test time rather than discovered by students in production.

### Contract 1: Page ↔ Config (Metadata Validity)

**Parties**: Every HTML page's `__KA_PAGE__` block ↔ `ka_nav_config.json`

**Terms**:
```
INVARIANT: For every page P with __KA_PAGE__.regime = R:
  1. R must be a key in config.regimes
  2. P.section must match a section.id in config.regimes[R].left_nav.sections
     OR in config.regimes[R].journeys[user_role].sections (for global regime)
  3. P.page must match an item.id in the matched section's items array
  4. Every href in P.breadcrumb must resolve to an existing HTML file
     (relative to the page's directory)
```

**Enforcement**: `ka_nav.js` includes a development-mode validator (see §12) that checks these invariants on every page load when `?nav_debug=1` is in the URL. In production, the validator is silent. A CI script (`scripts/validate_nav.py`) also checks all pages against the config.

### Contract 2: Config ↔ Nav JS (Rendering Completeness)

**Parties**: `ka_nav_config.json` ↔ `ka_nav.js`

**Terms**:
```
INVARIANT: For every item I in config:
  1. I.href must be a valid relative or absolute path
  2. I.id must be a non-empty string matching [a-z0-9-]+
  3. I.label must be a non-empty string ≤ 40 characters
  4. If I.personalized = true, ka_nav.js must substitute {TRACK_NAME}
     and {N} with user data before rendering
  5. If I.external = true, ka_nav.js must add target="_blank" rel="noopener"

INVARIANT: For every section S in config:
  1. S.id must be unique within its regime
  2. S.title must be ≤ 50 characters
  3. S.items must contain ≥ 1 item
```

**Enforcement**: `ka_nav.js` validates the config on load (development mode). If a section has 0 items, it's hidden. If an ID is duplicated, a console warning fires.

### Contract 3: Auth State ↔ Nav Display (Login State Consistency)

**Parties**: localStorage auth data ↔ nav rendering

**Terms**:
```
INVARIANT: Auth display states
  IF localStorage has ka_access_token AND ka_current_user:
    - Avatar with initials is visible in top bar
    - Dropdown contains: name, email, track, What's Due, Grades, Profile, Log out
    - "Log in" link is NOT visible
    - "Register" link/button is NOT visible anywhere in nav

  IF localStorage does NOT have ka_access_token:
    - "Log in" link is visible in top bar right section
    - Avatar and dropdown are NOT visible
    - Left nav shows "Explorer" journey (generic)
    - No personalized track section

  NEVER: Both "Log in" AND avatar visible simultaneously
  NEVER: "Register" visible in the nav bar (access via login page only)
```

**Enforcement**: `ka_nav.js` has a single `renderAuthWidget()` function with two branches (logged-in, logged-out). There is no third state. The function is the sole authority on what auth UI appears.

### Contract 4: Schedule Data ↔ "What's Due" Display

**Parties**: `ka_nav_config.json` schedule data ↔ dropdown "What's Due" section

**Terms**:
```
INVARIANT: Deadline display
  1. Only deadlines with due > now() are shown
  2. Maximum 3 deadlines displayed
  3. Deadlines are sorted by due date ascending
  4. If user has a track, track-specific deadlines are included
  5. Each deadline shows: label + human-readable due date
  6. If no upcoming deadlines exist, section shows "No upcoming deadlines"
  7. Dates display as "Mon Apr 13" (abbreviated, no year)
```

**Enforcement**: Unit test in `tests/test_nav_deadlines.js` with mock dates.

### Contract 5: Week Detection ↔ Left Nav Highlighting

**Parties**: Date-based week computation ↔ left nav "current week" indicator

**Terms**:
```
INVARIANT: Week detection
  1. Week 1 starts on config.schedule.week1_start (Monday)
  2. Current week = floor((today - week1_start) / 7) + 1
  3. If today < week1_start, current week = 0 (pre-course)
  4. If current week > 10, current week = 10 (post-course)
  5. Page can override with __KA_PAGE__.week (integer)
  6. Current week's left-nav item gets .nav-current-week class
     (amber left-border + bold text)
```

---

## 13. Self-Testing & Validation

### 13A. Development-Mode Validator (Client-Side)

When any page is loaded with `?nav_debug=1` in the URL, `ka_nav.js` runs a validation suite and outputs results to the browser console:

```javascript
function validateNavState() {
  const results = [];
  const page = window.__KA_PAGE__;

  // 1. Metadata completeness
  if (!page) results.push({level: 'ERROR', msg: 'No __KA_PAGE__ metadata found'});
  if (!page.regime) results.push({level: 'ERROR', msg: 'Missing regime in __KA_PAGE__'});
  if (!page.section) results.push({level: 'WARN', msg: 'Missing section — left nav will not highlight'});
  if (!page.page) results.push({level: 'WARN', msg: 'Missing page — no active item in left nav'});
  if (!page.breadcrumb || page.breadcrumb.length === 0)
    results.push({level: 'WARN', msg: 'Missing breadcrumb — breadcrumb bar will be empty'});

  // 2. Config consistency
  const regime = config.regimes[page.regime];
  if (!regime) results.push({level: 'ERROR', msg: `Unknown regime: ${page.regime}`});

  // 3. Section exists in config
  const sections = regime.left_nav?.sections || [];
  const matchedSection = sections.find(s => s.id === page.section);
  if (!matchedSection && page.section)
    results.push({level: 'ERROR', msg: `Section "${page.section}" not found in ${page.regime} config`});

  // 4. Page ID exists in section
  if (matchedSection) {
    const matchedItem = matchedSection.items.find(i => i.id === page.page);
    if (!matchedItem && page.page)
      results.push({level: 'ERROR', msg: `Page "${page.page}" not in section "${page.section}"`});
  }

  // 5. Breadcrumb link resolution
  for (const crumb of (page.breadcrumb || [])) {
    if (crumb.href) {
      // Attempt fetch HEAD to check link exists
      fetch(crumb.href, {method: 'HEAD'}).then(r => {
        if (!r.ok) results.push({level: 'WARN', msg: `Breadcrumb link 404: ${crumb.href}`});
      }).catch(() => {
        results.push({level: 'WARN', msg: `Breadcrumb link unreachable: ${crumb.href}`});
      });
    }
  }

  // 6. Auth state consistency
  const hasToken = !!localStorage.getItem('ka_access_token');
  const hasUser = !!localStorage.getItem('ka_current_user');
  if (hasToken !== hasUser)
    results.push({level: 'WARN', msg: 'Auth state inconsistent: token and user out of sync'});

  // 7. DOM validation
  const topbar = document.querySelector('.ka-topbar');
  const breadcrumb = document.querySelector('.ka-breadcrumb');
  const leftNav = document.querySelector('.ka-left-nav');
  if (!topbar) results.push({level: 'ERROR', msg: 'Top bar not rendered'});
  if (!breadcrumb && page.breadcrumb?.length > 0)
    results.push({level: 'ERROR', msg: 'Breadcrumb bar missing despite breadcrumb data'});
  if (!leftNav) results.push({level: 'ERROR', msg: 'Left nav not rendered'});

  // Output
  console.group('🧭 KA Nav Validation');
  for (const r of results) {
    if (r.level === 'ERROR') console.error(r.msg);
    else if (r.level === 'WARN') console.warn(r.msg);
    else console.log(r.msg);
  }
  if (results.length === 0) console.log('✅ All nav checks passed');
  console.groupEnd();

  return results;
}
```

### 13B. CI/Build-Time Validator (`scripts/validate_nav.py`)

A Python script that runs against all HTML files and the config. Checks:

```python
# 1. Every HTML file in the site has ka_nav.css and ka_nav.js includes
# 2. Every HTML file has a __KA_PAGE__ metadata block (except index.html redirects)
# 3. Every page.section and page.page ID exists in ka_nav_config.json
# 4. Every href in ka_nav_config.json resolves to an existing HTML file
# 5. No duplicate section IDs within a regime
# 6. No duplicate page IDs within a section
# 7. All breadcrumb hrefs resolve to existing files (relative path resolution)
# 8. Schedule deadlines are in chronological order
# 9. Track numbers in config match track portal files that exist
# 10. Character length limits on labels and titles
```

Output: PASS/FAIL with specific file:line references for each violation.

### 13C. Visual Regression Testing

After migration, capture screenshots of representative pages and compare:

| Test | Pages | What to Check |
|------|-------|---------------|
| Global logged-out | ka_home, ka_topics, ka_evidence | No avatar, "Log in" visible, Explorer left nav |
| Global logged-in (student) | ka_topics, ka_evidence | Avatar, student journey left nav, no Register |
| Course logged-in | 160sp/ka_schedule, week2_exercises | Course top bar, personalized track in left nav |
| Course logged-out | 160sp/ka_schedule | Course top bar, "Log in", no track personalization |
| Mobile (360px) | ka_home, ka_schedule, ka_tracks | Hamburger, slide-out left nav, no overflow |
| Track portal | ka_track1_portal | Track color, team section, sprint checklist |
| Instructor view | ka_home_instructor | Accordion with Student View open by default |

### 13D. Runtime Assertions (Contracts in Code)

Key functions in `ka_nav.js` include assertion checks that throw in development mode:

```javascript
function renderTopBar(regime, config) {
  assert(config.regimes[regime], `Unknown regime: ${regime}`);
  assert(config.regimes[regime].topbar.length <= 7,
    `Top bar has ${config.regimes[regime].topbar.length} links — exceeds cognitive limit`);
  // ... render
}

function renderLeftNav(sections, currentSection, currentPage) {
  assert(sections.length <= 12,
    `Left nav has ${sections.length} sections — exceeds scan limit`);
  for (const s of sections) {
    assert(s.items.length > 0, `Section "${s.title}" has 0 items`);
    assert(s.title.length <= 50, `Section title too long: "${s.title}"`);
  }
  // ... render
}

function renderAuthWidget(isLoggedIn, user) {
  // Auth state contract: exactly one of two states
  const loginVisible = document.querySelector('.ka-auth-login');
  const avatarVisible = document.querySelector('.ka-auth-avatar');
  // After render, assert mutual exclusion
  setTimeout(() => {
    assert(!(loginVisible && avatarVisible),
      'CONTRACT VIOLATION: Both login and avatar visible');
    assert(loginVisible || avatarVisible,
      'CONTRACT VIOLATION: Neither login nor avatar visible');
  }, 100);
}
```

### 13E. Automated Smoke Test (`scripts/smoke_test_nav.js`)

A Node.js script using Puppeteer that:

1. Opens every HTML file in the site
2. Checks that `.ka-topbar`, `.ka-breadcrumb`, `.ka-left-nav` are present
3. Checks that no console errors related to nav occurred
4. Checks that the nav debug validator passes (appends `?nav_debug=1`)
5. Takes a screenshot of each page's nav area for manual review
6. Outputs a summary: X pages tested, Y passed, Z failed with reasons

---

## 14. Migration Strategy (Pipeline-Integrated)

### Phase 0: Prerequisite — Git Reconciliation (1 hour)

Before touching navigation:
1. Get the live site copy from `/var/www/xrlab/ka`
2. Merge server branding/auth changes into local
3. Commit to GitHub as the single source of truth
4. This is tracked separately but is a hard prerequisite

### Phase 1: Design Pipeline for Nav Components (Day 1 — 6 hours)

Before any code is written, the nav components go through the design pipeline.

**Step 1A: Science-Writing Agent (2 hours, parallelizable)**

Run the Science-Writing Agent to produce 13-item copy packs for:

| Copy Pack | Key Items | Parallel Group |
|-----------|-----------|----------------|
| Top bar (both regimes) | Section labels, tooltips, beginner/expert variants | A |
| Left nav (all journeys) | Section labels, empty states, beginner/expert variants | A |
| Profile dropdown | CTA wording ("What's Due"), empty/error states, tooltips | B |
| Auth widget (both states) | Loading/error states, logged-out CTA text | B |
| Breadcrumb patterns | Label conventions, separator choice | B |
| Mobile nav | Hamburger label, slide-out header text | B |

Output: `docs/ATLAS_SCIENCE_COPY_PACK_NAV_COMPONENTS_2026-04-12.md`

**Step 1B: GUI Agent v3 (3 hours, after 1A completes)**

Run GUI Agent v3 to produce 32-item interaction specs for the 5 Tier 1 components. Each spec must include:

- Item 27: `FRAMEWORK: HTML/JS` (mandatory — nav is static HTML/JS)
- Item 29: Role adaptation table for all 6 roles
- Item 31: Usability critic targets (the at-risk heuristics listed in §11D)
- Item 12: Task → Data → View → Interaction mapping (the table from §11D)

Output: `docs/GUI_AGENT_V3_OUTPUT_NAV_COMPONENTS_2026-04-12.md`

The spec must declare:
```
FRAMEWORK: HTML/JS
RATIONALE: Navigation appears on every page including non-Streamlit static HTML pages
PRIMARY ROLE(S): all — nav is universal
```

**Step 1C: Review gate**

David reviews the copy packs and interaction specs before implementation begins. Key questions the review must answer:
- Are the nav labels right? (students will see these hundreds of times)
- Is the role adaptation table complete? (missing a role = broken nav for that user)
- Are the usability critic targets realistic? (these guide student evaluations)

### Phase 2: Build Shared Infrastructure (Day 1–2 — 5 hours)

Implementation guided by the specs from Phase 1.

| Task | File | Estimated Lines | Dependencies | Spec Reference |
|------|------|-----------------|--------------|----------------|
| 2.1 | `ka_nav.css` | ~400 | None | Copy pack labels + GUI spec item 13 (layout) |
| 2.2 | `ka_nav.js` (core: top bar, breadcrumb, left nav) | ~350 | 2.1 | GUI spec items 6, 7, 14, 16 |
| 2.3 | `ka_nav.js` (auth widget, profile dropdown) | ~150 | 2.2 | GUI spec items 19, 20, 23; copy pack items 5, 7, 8, 10 |
| 2.4 | `ka_nav.js` (week detection, What's Due) | ~80 | 2.2 | GUI spec item 12 (Task→Data→View) |
| 2.5 | `ka_nav.js` (mobile responsive) | ~80 | 2.2 | GUI spec item 25 |
| 2.6 | `ka_nav.js` (dev-mode validator) | ~80 | 2.2 | Contracts §12 |
| 2.7 | `ka_nav_config.json` | ~200 | 2.2 | Copy pack section labels; schedule data |
| 2.8 | `scripts/validate_nav.py` | ~150 | 2.7 | Contracts §12 |
| 2.9 | Contract documentation | ~100 | All above | §12 |

**Deliverable**: Three shared files + validator. Every implementation decision traces back to a spec item.

### Phase 3: Usability Critique of Nav Components (Day 2–3 — 2 hours)

**Step 3A: Usability Critic Agent (automated)**

Run the Usability Critic Agent against each Tier 1 component, producing the full 8-item critique report:
1. Page summary
2. Nielsen assessment (H1–H10)
3. Shneiderman assessment (R1–R8)
4. Visualization assessment (V1–V17, mostly N/A for nav)
5. 35-row verdict table
6. Severity counts
7. Prioritized repair list
8. Recommended GUI Agent v3 re-run brief

Output: `docs/USABILITY_CRITIQUE_NAV_COMPONENTS_2026-04-12.md`

**Minimum pass criteria** (from §11E):
- 0 Major Fails on H1, H4, H6, H8, R1, R8
- ≤3 Minor Issues total
- All SC-UC-1 through SC-UC-7 success conditions met

**Step 3B: In-browser critique session**

Load the nav components on a test page. Run `ka_usability_critic.js` manually. Compare browser-session ratings with agent critique. Resolve discrepancies.

**Step 3C: Revision (if needed)**

If Major Fails are found:
1. GUI Agent v3 re-runs with the critique report as input
2. Revised spec produced
3. Implementation updated
4. Critic re-runs to confirm resolution

**Gate**: Migration (Phase 4) does NOT begin until nav components pass critique.

### Phase 4: New Pages (Day 3 — 4 hours)

Build 8 new pages, all using the shared nav. Each gets an abbreviated pipeline (Science-Writing Agent copy pack + Usability Critic post-build check).

| Task | File | Pipeline Level | Dependencies |
|------|------|----------------|--------------|
| 4.1 | `ka_track1_portal.html` | Tier 2 (full copy pack + abbreviated spec) | Phase 2 |
| 4.2 | `ka_track2_portal.html` | Tier 3 (clone of 4.1 with content swap) | 4.1 |
| 4.3 | `ka_track3_portal.html` | Tier 3 (clone) | 4.1 |
| 4.4 | `ka_track4_portal.html` | Tier 3 (clone) | 4.1 |
| 4.5 | `ka_questions.html` (Did You Know) | Tier 2 (needs copy pack for question content) | Phase 2 |
| 4.6 | `ka_grades.html` | Tier 2 (sensitive data display) | Phase 2 |
| 4.7 | `ka_submissions.html` | Tier 3 (straightforward list) | Phase 2 |
| 4.8 | `ka_roster.html` | Tier 3 (admin view) | Phase 2 |

Track portal 1 gets the full Tier 2 treatment (Science-Writing Agent copy pack + GUI Agent v3 abbreviated spec covering items 1–12, 27, 29, 31). Portals 2–4 clone the template with track-specific content.

### Phase 5: Migrate Existing Pages (Day 3–4 — 6 hours)

Mechanical migration: Tier 3 — no pipeline, just nav swap.

**Batch A — Course pages (34 files)**:
- Highest priority. Students use these daily.
- All use `regime: 'course'`
- Parallelize: 4 agents, ~8 pages each

**Batch B — Global pages (45 files)**:
- Second priority. Various user types.
- All use `regime: 'global'`
- Parallelize: 4 agents, ~11 pages each

**Batch C — Fall 160 / Designing_Experiments (~18 files)**:
- Third priority. Placeholder subsite.
- All use `regime: 'fall160'`

**Migration checklist per page**:
1. ☐ Remove all inline `<style>` blocks for nav components
2. ☐ Remove all inline nav `<nav>` / `<header>` HTML
3. ☐ Add `<link rel="stylesheet" href="[path]/ka_nav.css">`
4. ☐ Add `<script>window.__KA_PAGE__ = {...}</script>`
5. ☐ Add `<script src="[path]/ka_nav.js"></script>`
6. ☐ Add `<script src="[path]/ka_usability_critic.js"></script>` (on all pages)
7. ☐ Verify page renders with shared nav (dev mode validator: `?nav_debug=1`)
8. ☐ Verify breadcrumbs correct
9. ☐ Verify left nav highlights correct section and page
10. ☐ Verify mobile responsive (resize to 360px)
11. ☐ Run `gui_design_success_conditions.json` checks (has_title, has_viewport, has_nav, has_responsive)

### Phase 6: Topic Page Updates (2 hours)

1. Add PDF/Summary/Related links to topic card bottoms
2. Move tool actions (Ask, Questions, Study Design) to detail panel
3. Wire "Related" links to filtered topic view
4. Science-Writing Agent copy pack for "Did You Know" question content

### Phase 7: Full QA & Testing (Day 4 — 3 hours)

**Automated:**
1. Run `validate_nav.py` — all pages must pass (nav metadata + config consistency)
2. Run `check_gui_design_contract.py` — all pages must pass required checks
3. Run `smoke_test_nav.js` (Puppeteer) — all pages render nav without console errors

**Usability Critic:**
4. Run Usability Critic Agent on 5 representative pages (one per regime/type):
   - `ka_home.html` (global, logged-out)
   - `ka_topics.html` (global, logged-in researcher)
   - `160sp/ka_schedule.html` (course, student)
   - `160sp/ka_track1_portal.html` (course, track portal)
   - `160sp/instructor_prep.html` (course, instructor)

**Manual:**
5. Test logged-in vs. logged-out on both regimes
6. Test mobile on 3 pages (360px, 768px, 1024px)
7. Visual regression comparison against pre-migration screenshots
8. David walkthrough: navigate the full student journey from home → register → setup → track selection → sprint workbook → submit

### Total Estimated Effort (Pipeline-Integrated)

| Phase | Hours | Day | Parallelizable? |
|-------|-------|-----|-----------------|
| 0: Git reconciliation | 1 | 0 | No |
| 1: Design pipeline (copy + specs) | 6 | 1 | Yes (copy packs parallel; specs after) |
| 2: Build infrastructure | 5 | 1–2 | Partially (CSS + JS in parallel) |
| 3: Usability critique + revision | 2 | 2–3 | Yes (5 component critiques in parallel) |
| 4: New pages | 4 | 3 | Yes (4 track portals in parallel) |
| 5: Migrate existing pages | 6 | 3–4 | Yes (batch by regime, 4 agents) |
| 6: Topic page updates | 2 | 4 | Yes |
| 7: Full QA | 3 | 4 | Partially |
| **Total** | **29** | **4 days** | |

The pipeline adds ~8 hours compared to the non-pipeline estimate (21 hours), but produces design artifacts that are evaluated against a 35-dimension heuristic framework, have role adaptation tables for all 6 user types, and include concrete copy for every state (loading, empty, error). The marginal cost buys significantly higher quality and maintainability.

---

## 15. Navigation Skill Specification

After the nav system is built and validated, it becomes a **skill** — a reusable specification that any AI worker can follow when creating or modifying K-ATLAS pages.

### Skill Location

```
.claude/skills/ka-navigation/SKILL.md
```

### Skill Contents

The skill will contain:

1. **The nav HTML template** — the exact `<head>` includes and `__KA_PAGE__` metadata format
2. **Regime selection rules** — when to use `global` vs. `course` vs. `fall160`
3. **Section and page ID conventions** — naming rules for left-nav section and item IDs
4. **Breadcrumb generation rules** — how to construct the breadcrumb array
5. **Color tokens** — the 9 functional colors from §2 P7
6. **GUI Agent v3 checklist excerpt** — the 20-item evaluation checklist (items relevant to nav)
7. **Usability Critic targets** — the at-risk heuristics for nav components (from §11D item 31)
8. **V1–V17 visualization checklist** — for pages with data displays (embedded from GUI Agent v3)
9. **Science-Writing Agent copy norms** — the 12 communication norms and 3-pass revision protocol (from `contracts/SCIENCE_COMMUNICATION_NORMS.md`)
10. **Contract validation** — how to run `validate_nav.py` and `check_gui_design_contract.py`
11. **QA checklist** — the per-page migration checklist from Phase 5
12. **Design pipeline reference** — when to run which agent for new pages vs. modified pages

### When the Skill Triggers

Any AI worker creating or modifying a K-ATLAS page MUST read this skill first. Triggers:
- Creating a new `.html` file in the Knowledge_Atlas repo
- Modifying the nav structure of any existing page
- Adding a new section or page to `ka_nav_config.json`
- Changing auth widget behavior
- Adding a new user role or journey

### Relationship to Other Agents

The navigation skill is NOT a replacement for the design pipeline. It is a quick-reference that tells the implementer:
- What shared files to include
- What metadata to set
- What validation to run
- When to escalate to the full pipeline (new component types, new roles, Major Fails in critique)

For routine page creation (adding a new weekly agenda, a new track assignment page), the skill is sufficient. For novel page types (a new visualization tool, a new admin dashboard), the full pipeline (Science-Writing Agent → GUI Agent v3 → Usability Critic) should be run.

---

## 16. Open Questions (Updated)

1. **Sprint numbering**: Are sprints numbered globally (Sprint 1 = first sprint regardless of track) or per-track (each track has its own Sprint 1, 2, 3)? This affects both the config data and the left-nav display.

2. **Designing_Experiments tools**: The experiment wizard, hypothesis builder, measurement instruments, and sensor catalogue are powerful tools. Should they be accessible from the Spring 2026 left nav under "Resources," or kept exclusively in the Fall 160 subsite?

3. **Grade visibility**: Can students see only their own grades, or also aggregate statistics (class average, track average)? This affects the grades page design.

4. **Instructor portal merge**: The existing `ka_home_instructor.html` has metric cards (Students, Submissions, Pending Reviews, Track Health). Should these be preserved and integrated into the Instructor View accordion, or replaced by the new grading/roster pages?

5. **Did-You-Know content source**: The questions page needs actual "did you know" factoids derived from topic clusters. Are these hand-curated, AI-generated from cluster summaries, or pulled from a database? If AI-generated, we need a generation step in the build pipeline.

6. **Team formation mechanism**: How are teams formed? Instructor assignment? Student self-selection? Random? This affects whether the track portal needs a "Join Team" UI or just displays the assigned team.

7. **Scaffolded nav visibility (P6)**: I proposed that early weeks show fewer left-nav sections, with more appearing as the course progresses. Do you want this time-gated behavior, or prefer showing the full nav from day one (with future items grayed out)?

---

## References

- Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*, 24(1), 87–114. (Cited ~5,600 times)
- Doumont, J.-L. (2009). *Trees, Maps, and Theorems: Effective Communication for Rational Minds*. Principiae.
- Mayer, R. E. (2009). *Multimedia Learning* (2nd ed.). Cambridge University Press. (Cited ~12,000 times)
- Miller, G. A. (1956). The magical number seven, plus or minus two: Some limits on our capacity for processing information. *Psychological Review*, 63(2), 81–97. (Cited ~25,000 times)
- Shneiderman, B. (1996). The eyes have it: A task by data type taxonomy for information visualizations. *Proceedings of the IEEE Symposium on Visual Languages*, 336–343. (Cited ~4,200 times)
- Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science*, 12(2), 257–285. (Cited ~15,400 times)
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.). Graphics Press.
- Ware, C. (2012). *Information Visualization: Perception for Design* (3rd ed.). Morgan Kaufmann.

---

*This plan is ready for critique by AG, Codex, and David. Implementation begins after approval.*
