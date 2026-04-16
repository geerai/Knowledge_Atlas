# Codex Pre-Deploy Audit Prompt — 2026-04-13

**Date created:** 2026-04-13
**Owner:** Prof. David Kirsh (UCSD Cognitive Science)
**Author:** Cowork (CW)
**Purpose:** Audit the batch of HTML/JS changes about to be pushed to
`github.com/dkirsh/Knowledge_Atlas` and deployed to the production server.
Paste this prompt into Codex *before* the push so problems are caught in
the working tree, not on the live site.

> **Frozen snapshot of the audit contract as of 2026-04-13.** File paths,
> navbar strings, and link targets listed below reflect the working tree on
> that date. Later sessions (e.g. post-Codex-2 fixes on the same day and
> beyond) may have added files, renamed targets, or supplemented the intake
> contract. When rerunning the audit, do not grep the file-list sections of
> this document for current strings — consult the live repo. This document is
> historical reference, not truth.

---

## Prompt for Codex — Pre-Deploy Audit of COGS 160 K-ATLAS Session Changes

**Your role.** You are auditing a batch of HTML/JS changes that will shortly
be pushed to `github.com/dkirsh/Knowledge_Atlas` and deployed to the
production server. Treat every issue as potentially user-facing. Be severe,
specific, and line-numbered. Do not be polite. If something is broken, say
so. If something is ambiguous, flag it. Do not make edits — produce a
structured issue report only.

**Repo location and branch.**
`/Users/davidusa/REPOS/Knowledge_Atlas/` on branch `master`. The relevant
commit is not yet made — the changes are in the working tree. Use
`git diff --stat HEAD` and `git diff HEAD -- <path>` to see the full change
set.

**Files modified or added in this session (primary audit targets).**

New files:

- `160sp/ka_track1_setup.html`
- `160sp/ka_track2_setup.html`
- `160sp/ka_track3_setup.html`
- `160sp/ka_track4_setup.html`
- `ka_critique_endpoints.py` *(KA-T22 back-end)*

Modified files:

- `160sp/ka_track1_tagging.html`
- `160sp/ka_track2_pipeline.html`
- `160sp/ka_track3_vr.html`
- `160sp/ka_track4_ux.html`
- `160sp/ka_student_setup.html`
- `ka_login.html`
- `ka_home_student.html`
- `ka_home_contributor.html`
- `ka_home_instructor.html`
- `ka_home_researcher.html`
- `ka_home_practitioner.html`
- `ka_home_theory.html`
- `ka_auth_server.py`  *(registers the critique router)*
- `ka_usability_critic.js`  *(KA-T22 front-end)*
- `.gitignore`

**What was added this session (so you know what to look for).**

1. Four new track setup pages with prerequisites, numbered install steps,
   and "Common Snags" sections.
2. A left-hand sticky `<aside class="track-subnav">` on each of the four
   track pages, with in-page anchor links plus an orange "How to Set Up →"
   CTA.
3. A bottom dual-CTA on each of the four track pages: "Set Up Your
   Environment →" (navy) + "Join this Track →" (amber). The Join button
   calls `openJoinModal(trackName)`, which opens `.jt-modal-backdrop` and
   on confirm writes `localStorage.ka_current_track`.
4. On `ka_student_setup.html`: replaced the shell navbar with the
   canonical class navbar, converted §1 and §2 into `.accordion` blocks
   default-closed, left §3 ("Choose Your Track") expanded and
   front-and-centre.
5. On `ka_login.html`: post-auth routing now unconditionally redirects to
   `160sp/ka_student_setup.html` (removed the older A0-progress-check
   branch).
6. On all six user-type portal pages: injected a fixed
   `<aside class="portal-subnav">` with section anchor links plus a
   "Journeys" sub-group; injected `<span id="j-…">` anchor spans
   immediately before each journey card; injected `id="…"` attributes on
   the relevant h2 section headings.
7. Added a global `:target { scroll-margin-top: 96px; }` rule plus an
   `h1[id], h2[id], h3[id], h4[id], section[id], div[id], a[id] { scroll-margin-top: 96px; }`
   rule inside each affected page's `<style>` block, so anchor jumps clear
   the fixed top navbar.
8. **KA-T22 — AI Suggestions endpoint.** New module
   `ka_critique_endpoints.py` exposes `POST /api/critique/suggest` that
   accepts the usability-critic payload, calls Claude when
   `ANTHROPIC_API_KEY` is set, and returns rule-based fallback suggestions
   otherwise. `ka_usability_critic.js` gains a `✨ Get AI suggestions`
   button in the Summary tab that POSTs the ratings and renders
   priority-coded suggestion cards inline. Wire-up happens in
   `ka_auth_server.py` just below the article-submission block.

**Robustness checks — do ALL of these.**

**A. Anchor integrity (critical).**

1. For every page in the list, parse the HTML and enumerate every
   `<a href="#…">`. For each one, confirm the target `id="…"` exists
   *somewhere in the same document*. Report every dead anchor with file,
   line, href, and the likely intended target.
2. Confirm that every id is unique within its document (no duplicate ids
   — this breaks `getElementById` and anchor scrolling).

**B. CSS class and variable collisions.**

1. The class names added this session include `track-subnav`,
   `track-subnav-title`, `track-subnav-cta`, `track-bottom-ctas`, `big-cta`,
   `big-cta-setup`, `big-cta-join`, `jt-modal-backdrop`, `jt-modal`,
   `jt-btn`, `jt-btn-primary`, `jt-btn-secondary`, `portal-subnav`,
   `portal-subnav-title`, `portal-subnav-group`, `journey-anchor`. Grep the
   full repo — do any of these names collide with pre-existing classes
   that carry a different meaning? Report collisions.
2. Confirm CSS custom properties (`--navy`, `--amber`, `--cream`,
   `--green`) are defined on each modified page (either locally or via a
   linked stylesheet). If any page uses these variables without declaring
   them, the sub-nav will render as black-on-white and look broken.

**C. JavaScript integrity.**

1. `openJoinModal`, `closeJoinModal`, `confirmJoin` must each be defined
   exactly once per page and be invocable without ReferenceError. Check
   for stray duplicates or missing definitions.
2. `localStorage.ka_current_track` is the declared source of truth. Grep
   the entire repo for any other code path writing to a *different* key
   with similar intent (e.g., `ka_track`, `current_track`, `studentTrack`,
   `my_track`) and report collisions.
3. On `ka_student_setup.html`, confirm the accordion toggle function
   (`toggleAccordion` or equivalent) exists and actually binds to the
   `.accordion-header` elements. Confirm §3 is not inside an accordion
   wrapper.
4. On `ka_login.html`, trace the post-auth path. Confirm there is no
   surviving branch that still routes students to `ka_schedule.html` or
   anywhere other than `160sp/ka_student_setup.html`.
5. On `ka_usability_critic.js`, confirm the new `requestAiSuggestions`,
   `buildCritiquePayload`, and `renderSuggestionsInto` helpers are within
   the IIFE (i.e., not leaking to `window`), and that the
   `#ka-ai-btn` / `#ka-ai-suggestions` IDs are unique.

**D. Navbar canonical consistency.**
Each page should have the canonical class navbar: logo SVG + brand
"At**las** · COGS 160" + nav-center with links to 160 Syllabus, A0, A1,
Track 1, Track 2, Track 3, Track 4 + nav-right "160 Student Profile".
Diff each modified 160sp page's navbar against the canonical. Report
every deviation — wrong label, wrong href, missing link, extra link,
wrong active-state, wrong order.

**E. Cross-link integrity.**

1. Every `<a href="FILE.html">` in the modified files must resolve to an
   existing file (relative to the page). Report every dead cross-link.
2. Each track page must link to its corresponding `ka_trackN_setup.html`.
   Each setup page must link back to its track page. Verify both
   directions.

**F. HTML validity.**
Run a validator (tidy, html5validator, or equivalent) on each modified
file. Report errors (not warnings). Particular things to watch: unclosed
`<div>` from injections, duplicate ids, invalid nesting (e.g., block
elements inside `<a>`), orphan `</aside>` or `</section>`, stray
`<style>` blocks outside `<head>`, and any case where injection
corrupted existing markup.

**G. Responsive behavior.**
Both sub-navs (`.track-subnav` and `.portal-subnav`) are hidden below
1280 px. Confirm no page has important content *only* in the sub-nav —
every sub-nav link must also be reachable via normal page scroll or the
top navbar.

**H. Accessibility.**

1. The join-track modal must trap focus, be dismissible with Escape, and
   have appropriate ARIA (`role="dialog"`, `aria-modal="true"`,
   `aria-labelledby`). Report missing attributes.
2. The amber gradient on the "Join this Track" CTA must meet WCAG AA
   contrast against its text colour. Report if not. (Per root
   `CLAUDE.md`: "NEVER use dark blue on dark backgrounds. All color
   combinations must meet WCAG 2.1 AA: 4.5:1 normal text, 3:1 large
   text.")
3. Every accordion header on `ka_student_setup.html` must have
   `role="button"`, `aria-expanded`, and keyboard (Enter/Space)
   activation. Report gaps.

**I. Security / XSS.**
The modal reads `localStorage.ka_current_track` and writes it into the
DOM via `textContent` (per my injection). Confirm nothing in the
injected JS uses `innerHTML` with user-derived content. Report any case
where it does. Also confirm the new critique fetch body is sanitised
before render (`escHtml` is applied).

**J. Breaking changes for other pages.**

1. On `ka_student_setup.html`, §1 and §2 being accordion-collapsed by
   default means returning students who had bookmarked `#section-1` or
   similar will no longer see their target. Check for any inbound link
   across the repo that uses such anchors. If present, flag as needing
   an `onHashChange` handler that auto-opens the accordion.
2. On `ka_login.html`, the removed A0-progress branch means even
   students who previously completed A0 are routed to
   `ka_student_setup.html`. Confirm this is acceptable (the accordions
   handle it gracefully, but verify no other code relied on the old
   branch).

**K. Sitewide sweep.**
Ripgrep the whole repo for the literal strings `TODO`, `FIXME`, `XXX`,
`Lorem`, `coming soon`, `placeholder`, `REPLACE ME`, and un-rendered
markdown (`**bold**`, `__italic__`, `[link](url)`) appearing in HTML
`<body>` content. Report every occurrence, with file and line.

**L. Portal journey sub-nav coverage.**
For each of the six portal pages, confirm the journeys listed in the
left aside match the actual journey cards rendered in the page body
(same count, same order, same labels). Report mismatches.

**M. CSS injection sanity.**
The session injected a `scroll-margin-top: 96px;` rule globally on
anchored headings. Confirm this does not visually break any page that
relies on heading margin layouts (e.g., pages with decorative hero
sections where the first h1 sits flush against the top).

**N. Duplicate CSS / duplicate injection.**
The injection script guarded against double-insertion by checking for
the marker string. Confirm no page has the injected CSS block twice,
and no page has the `.portal-subnav` or `.track-subnav` HTML twice.

**O. Encoding.**
Report any un-escaped `&` in attribute values, any `&amp;amp;`
double-encoding, any stray BOM, any non-UTF-8 characters.

**P. KA-T22 endpoint wiring.**

1. Confirm `ka_auth_server.py` imports `ka_critique_endpoints` inside a
   `try` block so a missing `anthropic` package does not crash startup.
2. Confirm the router prefix is `/api/critique` and the POST path is
   `/suggest` (full URL `/api/critique/suggest`).
3. Confirm the fallback path is used when `ANTHROPIC_API_KEY` is unset
   and that it returns HTTP 200 with `source: "fallback"`.
4. Confirm the front-end sends `Content-Type: application/json`, handles
   non-2xx responses gracefully (visible error state, button re-enabled),
   and does not send on pages where `currentSession` is null.

**Deliverable format.**

Produce a single markdown report with four sections:

1. **BLOCKERS (fix before deploy).** Anything that breaks a user-facing
   feature — dead anchors, broken JS, missing navbar links, broken login
   routing, XSS. File + line + one-sentence fix.
2. **HIGH (fix this session).** Inconsistencies that will be noticed —
   navbar deviations, contrast failures, missing ARIA, duplicate ids,
   broken responsive behavior.
3. **MEDIUM (fix soon).** Copy/polish — terminology inconsistency,
   sparse sections, minor HTML-validity warnings.
4. **LOW (tracked for later).** Suggestions and nice-to-haves.

For each item include: file path, line number (or id anchor name if no
line), one-sentence description, one-sentence proposed fix. If a
category is empty, say "None found." Do not summarise or editorialise.
Do not produce patches — just the report.

**Hard rules.**

- Do not modify any file. Read-only.
- Do not run the production server.
- Do not invent issues to look thorough. If a file is clean, say so.
- Cover every file in the "Files modified or added" list above — do not
  sample.
- Run at least one HTML validator and one link checker programmatically.
  Do not rely on visual inspection.
