# K-ATLAS Navigation Architecture Plan

**Date**: 2026-04-11  
**Author**: Claude (with David Kirsh)  
**Status**: DRAFT — for David's review before implementation

---

## 1. The Problem

The current site has **at least 7 distinct navbar implementations** across ~80 pages. Wordmarks appear in three styles (icon+two-line, icon+single-line, "K-ATLAS" shorthand). Heights vary (52px vs. 56px). Positioning alternates between `fixed` and `sticky`. Link sets range from zero links (ka_home.html) to six or more (ka_schedule.html). Breadcrumbs exist on ~5 pages. Left sidebars exist on 4 pages (evidence, articles, tagger, warrants) but nowhere else. The auth widget (`ka_auth_widget.js`) exists on the server but is not loaded in the local repo at all.

Every page reinvents its own `<style>` block for navigation. There is no shared CSS file, no shared HTML template, and no convention that a new page author could follow.

**Result**: Students encounter a different interface on nearly every click. The site feels like a collection of prototypes rather than a single product.

---

## 2. Design Principles

1. **Two regimes, one system.** The global site and the course site are different products for different audiences, but they share a visual language (colors, typography, component patterns).

2. **The top bar is stable.** It doesn't change link order or structure as you navigate. It provides identity (wordmark), context (where am I?), and auth (who am I?). The left-hand nav carries the journey.

3. **Left-hand nav is the journey.** Every page gets a collapsible left sidebar showing where the user is in a multi-step flow. This replaces the current practice of cramming context into the top bar.

4. **Breadcrumbs everywhere.** Every page below the root gets a breadcrumb trail. This is non-negotiable for orientation.

5. **One CSS file, one JS file.** `ka_nav.css` and `ka_nav.js` are included on every page. No more per-page nav styling.

6. **Progressive disclosure.** Left-nav sections expand on demand. A student in Track 2 sees their track expanded; the other tracks are collapsed.

7. **Personalized where it matters.** The profile dropdown knows your name, track, and what's due. The left nav highlights your current position. The top bar doesn't change.

---

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  TOP BAR (fixed, 52px, navy)                                    │
│  ┌──────────┐  ┌──────────────────────────┐  ┌───────────────┐ │
│  │ Wordmark  │  │   Global Links            │  │  Auth Widget  │ │
│  │ K-ATLAS   │  │   (stable across pages)   │  │  [Avatar ▾]   │ │
│  └──────────┘  └──────────────────────────┘  └───────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  BREADCRUMB BAR (cream, 36px)                                   │
│  Home > Course > Week 3 > Track Selection                       │
├──────────────┬──────────────────────────────────────────────────┤
│  LEFT NAV    │  MAIN CONTENT                                    │
│  (240px,     │                                                  │
│   collapsible│  (full-width when left nav collapsed)            │
│   sticky)    │                                                  │
│              │                                                  │
│  ▸ Section   │                                                  │
│  ▾ Section   │                                                  │
│    · Page    │                                                  │
│    · Page    │                                                  │
│  ▸ Section   │                                                  │
│              │                                                  │
└──────────────┴──────────────────────────────────────────────────┘
```

---

## 4. The Two Nav Regimes

### 4A. Global Site (non-course pages)

**Top bar links** (stable, always the same order):

| Position | Label | Target | Notes |
|----------|-------|--------|-------|
| Left | **K-ATLAS** (wordmark) | ka_home.html | Always links home |
| Center-1 | Explore | ka_topics.html | Topic hierarchy |
| Center-2 | Evidence | ka_evidence.html | Evidence table |
| Center-3 | Articles | ka_article_search.html | Article search |
| Center-4 | Contribute | ka_contribute.html | Submission flow |
| Center-5 | Course | 160sp/ka_schedule.html | Bridge to course site |
| Right | [Auth Widget] | — | Login/Register or Avatar+dropdown |

**Left-hand nav** varies by user type. When a user clicks their user-type on the homepage, they land on a **portal page** for that type. The left nav on every subsequent page shows their journey:

**Student Journey (left nav):**
```
▾ Getting Started
  · Register & Login
  · Student Setup
  · Choose Your Track
▸ Explore the Atlas
  · Topics
  · Evidence Table
  · Article Search
  · Warrant Types
  · Knowledge Gaps
▸ Contribute
  · Propose an Article
  · Submit Evidence
  · My Work
```

**Researcher Journey:**
```
▾ Getting Started
  · Register & Login
  · Research Overview
▸ Evidence System
  · Evidence Table
  · Warrant Types
  · Knowledge Gaps
▸ Article Pipeline
  · Search Articles
  · Propose Articles
▸ Analysis Tools
  · Hypothesis Builder
  · Question Maker
  · Interpretation
```

**Instructor Journey:**
```
▾ Course Management
  · Instructor Prep
  · Schedule
  · Approve Submissions
  · Student Dashboard
  · Grading
▸ Content
  · Topics
  · Evidence
  · Articles
▸ System
  · Workflow Hub
  · Account Settings
```

**Contributor / Practitioner / Theory**: Similar patterns, emphasizing their respective workflows.

The key insight: **the top bar never changes**. The left nav adapts to the user type (read from `ka_current_user` in localStorage, or defaulting to a generic "Explorer" journey for unauthenticated visitors).

---

### 4B. Course Site (160sp/ pages)

**Top bar links** (different from global, course-specific):

| Position | Label | Target | Notes |
|----------|-------|--------|-------|
| Left | **K-ATLAS** | ka_home.html | Returns to global home |
| Left-2 | **COGS 160** | 160sp/ka_schedule.html | Course identity marker (amber) |
| Center-1 | Syllabus | 160sp/ka_schedule.html | Master schedule |
| Center-2 | A0 | 160sp/ka_collect_articles.html | Assignment 0 |
| Center-3 | A1 | 160sp/week2_exercises.html | Assignment 1 |
| Center-4 | Tracks | 160sp/ka_tracks.html | Track overview |
| Right | [Auth Widget] | — | Avatar+dropdown (personalized) |

**Why this works**: The top bar gives direct access to every assignment and the syllabus. Students always know where they are in the course sequence. The "Tracks" link is the gateway to all four track portals.

**Profile dropdown** (inside auth widget, course-personalized):

```
┌──────────────────────────┐
│  David Kirsh              │
│  dkirsh@ucsd.edu          │
│  Track: GUI Evaluation    │
├──────────────────────────┤
│  📋 What's Due            │  ← computed from schedule + current week
│  📊 My Grades             │  ← links to grade view
│  👤 My Profile            │  ← profile info, track, team
│  ⚙️ Account Settings      │
├──────────────────────────┤
│  Log out                  │
└──────────────────────────┘
```

**Left-hand nav** (course journey, collapsible sections):

```
▾ Course
  · Syllabus / Schedule
  · Student Setup
  · Technical Setup

▾ Assignments
  · A0: Collect Articles
  · A1: Programming Exercises

▾ Your Track: [Track Name]         ← personalized, auto-expanded
  · Track Overview
  · Sprint Workbook
  · GitHub Branch
  · Submit Work

▸ Track AF: Article Finder         ← collapsed if not your track
▸ Track IT: Image Tagging
▸ Track AI+VR: VR Production
▸ Track GUI: GUI Evaluation

▾ Weekly Agendas
  · Week 1: Orientation
  · Week 2: First Assignment
  · Week 3: Track Selection         ← highlighted if current week
  · Week 4–7: Sprint Work
  · Week 8: Integration
  · Week 9–10: Final Presentations

▸ Resources
  · Google Scholar Guide
  · Evidence Explorer
  · Ask / Office Hours

▸ Fall 160                          ← link to fall quarter materials
```

**Critical behaviors:**
- The student's own track section is **auto-expanded** and marked with their track color pill.
- Other tracks are collapsed but visible (students can browse).
- Current week is **highlighted** (amber left-border or bold).
- "What's Due" in the dropdown pulls from the schedule data and shows the next upcoming deadline.

---

## 5. Track Portal Pages

Each track needs a dedicated portal page that serves as the home base for students in that track. These don't fully exist yet. Structure:

### Track Portal Template

```
[Top bar — course regime]
[Breadcrumb: COGS 160 > Tracks > Image Tagging]

┌──────────────┬──────────────────────────────────────────────┐
│  LEFT NAV    │  TRACK PORTAL: Image Tagging                 │
│  (course     │                                              │
│   journey,   │  [Track color hero banner]                   │
│   this track │  Status: Week 3 — Sprint begins next week    │
│   expanded)  │                                              │
│              │  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│              │  │ Workbook │ │ GitHub   │ │ Submit   │     │
│              │  │ (sprint) │ │ Branch   │ │ Work     │     │
│              │  └──────────┘ └──────────┘ └──────────┘     │
│              │                                              │
│              │  ## This Week's Tasks                        │
│              │  [Computed from week number + track]          │
│              │                                              │
│              │  ## Your Team                                │
│              │  [Team members, if assigned]                  │
│              │                                              │
│              │  ## Resources                                │
│              │  [Track-specific links, docs, tools]          │
│              │                                              │
│              │  ## Progress                                 │
│              │  [Checklist of milestones, checked off as     │
│              │   submissions are recorded]                   │
│              │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

Each of the four tracks gets this template:

| Track | Portal URL | Color | Key Tools |
|-------|-----------|-------|-----------|
| **Image Tagging** | 160sp/ka_track1_portal.html | Gold (#FFF0CC / #7A4F00) | Tagger, JSON schemas, K-ATLAS API |
| **Article Finder** | 160sp/ka_track2_portal.html | Green (#E3F4EC / #1A5C30) | Python, Google Scholar, SQL |
| **VR Production** | 160sp/ka_track3_portal.html | Blue (#E8F0FD / #1A3A7A) | Unreal/A-Frame, 3D modeling |
| **GUI Evaluation** | 160sp/ka_track4_portal.html | Pink (#FDE8F4 / #7A1A5C) | HTML/CSS/JS, usability testing |

---

## 6. Shared Infrastructure Files

### 6A. `ka_nav.css` — Single shared stylesheet

Contains ALL navigation styling:
- Top bar (fixed, 52px, navy background, amber accent)
- Breadcrumb bar (cream background, 36px)
- Left sidebar (240px, white/cream, collapsible)
- Auth widget dropdown
- Profile dropdown
- Active states, hover states
- Mobile responsive (hamburger for top bar, slide-out for left nav)
- Track color tokens (gold, green, blue, pink)
- Current-week highlight style

Every page includes: `<link rel="stylesheet" href="/ka/ka_nav.css">`

### 6B. `ka_nav.js` — Single shared behavior script

Handles:
- Reading auth state from localStorage
- Injecting the auth widget (avatar, dropdown)
- Computing "What's Due" from schedule data
- Building the left nav from a JSON structure (global vs. course)
- Expanding/collapsing left nav sections
- Highlighting current page in left nav and breadcrumbs
- Auto-expanding the user's track section
- Week detection (current course week)
- Mobile hamburger toggle
- Breadcrumb generation from page metadata

Every page includes: `<script src="/ka/ka_nav.js"></script>`

### 6C. `ka_nav_config.json` — Navigation structure data

```json
{
  "global": {
    "topbar": [
      {"label": "Explore", "href": "/ka/ka_topics.html"},
      {"label": "Evidence", "href": "/ka/ka_evidence.html"},
      {"label": "Articles", "href": "/ka/ka_article_search.html"},
      {"label": "Contribute", "href": "/ka/ka_contribute.html"},
      {"label": "Course", "href": "/ka/160sp/ka_schedule.html"}
    ],
    "journeys": {
      "student": { "sections": ["..."] },
      "researcher": { "sections": ["..."] },
      "instructor": { "sections": ["..."] },
      "contributor": { "sections": ["..."] },
      "practitioner": { "sections": ["..."] },
      "theory": { "sections": ["..."] }
    }
  },
  "course": {
    "topbar": [
      {"label": "Syllabus", "href": "/ka/160sp/ka_schedule.html"},
      {"label": "A0", "href": "/ka/160sp/ka_collect_articles.html"},
      {"label": "A1", "href": "/ka/160sp/week2_exercises.html"},
      {"label": "Tracks", "href": "/ka/160sp/ka_tracks.html"}
    ],
    "left_nav": {
      "sections": ["Course", "Assignments", "Your Track", "Track AF", "Track IT", "Track AI+VR", "Track GUI", "Weekly Agendas", "Resources", "Fall 160"]
    }
  },
  "schedule": {
    "week1_start": "2026-03-30",
    "deadlines": [
      {"week": 2, "label": "A1: Programming Exercises", "due": "2026-04-13"},
      {"week": 3, "label": "Track Selection", "due": "2026-04-18"}
    ]
  }
}
```

---

## 7. Page Metadata Convention

Each page declares its nav context with a small data block in the `<head>`:

```html
<script>
  window.__KA_PAGE__ = {
    regime: 'course',          // 'global' or 'course'
    section: 'assignments',    // left-nav section to expand
    page: 'a1-exercises',      // left-nav item to highlight
    breadcrumb: [
      {label: 'COGS 160', href: 'ka_schedule.html'},
      {label: 'Assignments', href: '#'},
      {label: 'A1: Programming Exercises'}
    ]
  };
</script>
```

`ka_nav.js` reads this to configure the left nav, breadcrumbs, and active states. Pages that don't set `__KA_PAGE__` get sensible defaults (global regime, no section expanded).

---

## 8. Migration Strategy

### Phase 1: Build the shared files (do first)
- Create `ka_nav.css` with all nav component styles
- Create `ka_nav.js` with nav injection, auth widget, left nav, breadcrumbs
- Create `ka_nav_config.json` with full nav structure
- Refactor `ka_auth_widget.js` capabilities INTO `ka_nav.js` (single script)

### Phase 2: Create course nav infrastructure
- Build the 4 track portal pages (ka_track1_portal.html through ka_track4_portal.html)
- Create "My Grades" page (stub, wired to submissions table)
- Create "What's Due" computation in ka_nav.js

### Phase 3: Migrate existing pages (batch by type)
- **Batch A — Course pages** (34 files in 160sp/): Strip inline nav CSS and HTML, add `<link>` to ka_nav.css, add `<script>` for ka_nav.js, add `__KA_PAGE__` metadata block.
- **Batch B — Global pages** (45 root files): Same process, using global regime.
- **Batch C — Designing_Experiments pages**: Decide whether these join the course regime or get their own. (Recommend: fold into course regime as a "Research Methods" section in left nav.)

### Phase 4: QA and refinement
- Test every page for correct breadcrumbs, left nav state, auth widget
- Test logged-in vs. logged-out states
- Test track-personalized left nav
- Test mobile responsive behavior
- Visual regression check on representative pages

### Estimated effort:
- Phase 1: ~4 hours (building ka_nav.css + ka_nav.js + config)
- Phase 2: ~3 hours (portal pages + grade stub + what's due)
- Phase 3: ~6 hours (mechanical migration across ~80 pages, parallelizable)
- Phase 4: ~2 hours (testing)
- **Total: ~15 hours of implementation work**

---

## 9. What This Replaces

| Current State | New State |
|--------------|-----------|
| 7+ navbar implementations | 1 shared top bar (2 regimes: global, course) |
| 3 wordmark styles | 1 wordmark: "K-ATLAS" (amber, consistent everywhere) |
| Mixed fixed/sticky positioning | Sticky everywhere (52px) |
| Nav links vary 0–6+ per page | Fixed link sets (5 global, 4 course) |
| Breadcrumbs on ~5 pages | Breadcrumbs on every non-root page |
| Left sidebar on 4 pages | Left journey nav on every page |
| Auth widget not loaded locally | Auth widget built into ka_nav.js, loaded everywhere |
| No mobile nav | Hamburger + slide-out left nav |
| Per-page `<style>` blocks for nav | Single `ka_nav.css` |
| No "What's Due" | Personalized deadline widget in profile dropdown |
| No track portals | 4 dedicated portal pages |
| No grades view | Grade page linked from profile dropdown |

---

## 10. Open Questions for David

1. **Assignment naming**: I used A0, A1 in the top bar. Will there be an A2, A3, etc.? Or do track sprints replace further numbered assignments? This affects whether we keep individual assignment links in the top bar or switch to "Assignments" as a dropdown.

2. **Fall 160 link**: You mentioned this in your list. Is this a link to archival materials from a previous quarter, or a placeholder for a future fall offering?

3. **Designing_Experiments pages**: These contain detailed per-track weekly materials (46+ pages). Should they be integrated into the course left nav, or kept separate?

4. **Team management**: You mentioned teams. Are teams within tracks (e.g., 3 students form a team within Image Tagging), or cross-track? This affects whether the "Your Team" section lives inside the track portal or at the course level.

5. **Instructor view**: Should the instructor see a different left nav entirely (focused on grading, approvals, student management), or the same course nav with additional items?

6. **Global user-type portals**: Do you want me to build portal pages for all 6 user types (student, researcher, contributor, instructor, practitioner, theory), or focus on student + instructor first?

---

## 11. Implementation as a Skill

You mentioned wanting this as a **skill** — a reusable specification that any AI worker can follow when creating or modifying K-ATLAS pages. After you approve this plan, I'll create:

```
.claude/skills/ka-navigation/SKILL.md
```

This skill will contain:
- The nav HTML template to include on every page
- The `__KA_PAGE__` metadata format
- Color tokens and CSS variable reference
- Left nav section structure
- Rules for when to use global vs. course regime
- Breadcrumb generation rules
- QA checklist for nav compliance

Any future page creation — by you, me, AG, or Codex — will follow this skill to produce consistent navigation automatically.

---

*This plan is ready for your review. Tell me what to change, what to cut, and what to expand, and I'll revise before implementation.*
