# K-ATLAS Brand Style Guide

**Date**: 2026-04-12
**Status**: Active — all design agents must follow this guide
**Canonical location**: `docs/KA_BRAND_STYLE_GUIDE.md`

---

## Brand Identity

Knowledge Atlas has **two brand regimes**: the global KA site brand and the COGS 160 course brand. Both use the same visual language but differ in wordmark text, logo link target, and navigation structure.

---

## The Canonical Logo

The KA logo is a **network-graph node icon** (inline SVG, no image file) paired with a **two-line wordmark**. The icon represents the knowledge-network metaphor: three outer nodes connected to a central hub.

### SVG Icon (canonical version — from ka_home.html)

```svg
<svg class="wordmark-icon" viewBox="0 0 32 32" fill="none">
  <circle cx="16" cy="16" r="3.5" fill="#F5A623"/>
  <circle cx="16" cy="5"  r="2.5" fill="#A8C8BF"/>
  <circle cx="27" cy="22" r="2.5" fill="#A8C8BF"/>
  <circle cx="5"  cy="22" r="2.5" fill="#A8C8BF"/>
  <line x1="16" y1="7.5"  x2="16"   y2="12.5" stroke="#F5A623" stroke-width="1.5" stroke-opacity="0.9"/>
  <line x1="24.8" y1="20.2" x2="19.0" y2="17.3" stroke="#F5A623" stroke-width="1.5" stroke-opacity="0.9"/>
  <line x1="7.2"  y1="20.2" x2="13.0" y2="17.3" stroke="#F5A623" stroke-width="1.5" stroke-opacity="0.9"/>
  <line x1="16" y1="7.5"  x2="25.5" y2="20" stroke="#fff" stroke-width="0.8" stroke-opacity="0.18"/>
  <line x1="25.5" y1="20" x2="6.5"  y2="20" stroke="#fff" stroke-width="0.8" stroke-opacity="0.18"/>
  <line x1="6.5"  y1="20" x2="16"   y2="7.5" stroke="#fff" stroke-width="0.8" stroke-opacity="0.18"/>
</svg>
```

**Icon anatomy**:
- Central hub node: amber (#F5A623), r=3.5
- Three outer nodes: teal (#A8C8BF), r=2.5, positioned at top, bottom-left, bottom-right
- Hub-to-node edges: amber (#F5A623), stroke-width 1.5, high opacity
- Outer triangle edges: white (#fff), stroke-width 0.8, very low opacity (0.18) — subtle structure

**Size**: 30px x 30px in the nav bar. Scale up to 48px for decorative use (e.g., login card header).

### Do NOT use:
- The old 100x100 viewBox SVG with crude circles-and-lines (gradient fills, large translucent background circle)
- Any rasterized image file — the logo is always inline SVG
- Page titles as part of the logo/brand area (e.g., "Topic Hierarchy" below "Knowledge Atlas" — this makes the page title invisible)

---

## Wordmark

### Global KA site wordmark

```html
<div class="wordmark-text">
  <span class="wm-top">Knowledge</span>
  <span class="wm-bottom">At<span>las</span></span>
</div>
```

**CSS**:
```css
.wordmark-text { display: flex; flex-direction: column; line-height: 1.1; }
.wm-top { font-size: 0.66rem; font-weight: 400; letter-spacing: 0.24em; text-transform: uppercase; color: #A8C8BF; }
.wm-bottom { font-size: 1.05rem; font-weight: 700; letter-spacing: 0.03em; color: #fff; }
.wm-bottom span { color: #F5A623; }
```

- "KNOWLEDGE" in small caps, teal, lightweight
- "Atlas" in bold white, with "las" in amber (#F5A623)
- Logo links to: `ka_home.html`

### COGS 160 course wordmark

Same as above, plus a third line:

```html
<span class="wm-sub">COGS 160</span>
```

```css
.wm-sub { font-size: 0.6rem; font-weight: 600; color: #7a9bbf; letter-spacing: 0.08em; }
```

- Logo links to: `160sp/ka_schedule.html` (the syllabus)

### Alternate text-only brand (for simpler navs)

Some pages use a text-only brand without the SVG icon:

```html
<a href="ka_home.html" class="nav-brand">K-ATLAS</a>
```

or for the search guide style:

```html
<div class="header-logo">K-<span>ATLAS</span></div>
<div class="header-tag">UC San Diego · Cognitive Science</div>
```

These are acceptable but the icon+wordmark version is preferred for all new pages.

---

## Color Palette

### Primary colors

| Name | Hex | Usage |
|------|-----|-------|
| KA Teal | `#2A7868` / `#1C3D3A` | Primary brand color, nav backgrounds, buttons |
| Deep Navy | `#182B49` | Page headers, hero sections, strong emphasis |
| Amber / Gold | `#F5A623` / `#E8872A` / `#C69214` | Accent, CTAs, "las" in wordmark, active states |
| Light Teal | `#A8C8BF` | Secondary text on dark backgrounds, outer nodes |

### Semantic colors

| State | Hex | Usage |
|-------|-----|-------|
| Success | `#d4edda` / `#27ae60` | Completed, approved, strong evidence |
| Warning | `#fff3cd` / `#C69214` | Pending, uncertain, attention needed |
| Error | `#f8d7da` / `#c0392b` | Failed, rejected, errors |
| Info | `#e0ffff` | Tooltips, informational strips |

### Accessibility (MANDATORY)

- NEVER use dark blue text on dark backgrounds
- All color pairs must meet WCAG 2.1 AA (4.5:1 normal text, 3:1 large text)
- On dark nav backgrounds (#1C3D3A), use: teal (#A8C8BF), amber (#F5A623), white (#fff)
- On dark navy hero backgrounds (#182B49), use: white, amber, light teal

---

## Typography

- System font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
- Base size: 15px, line-height: 1.6
- Nav links: 0.8-0.82rem, font-weight 500-600
- Headings: font-weight 700-800
- Small caps labels: letter-spacing 0.08-0.24em, text-transform uppercase

---

## Two Navigation Regimes

### Global KA site nav

For pages serving all user types (researchers, contributors, practitioners, etc.):

```
[Logo: Knowledge Atlas] | Explore | Evidence | Gaps | Articles | Contribute | Course | [Profile/Login]
```

- Background: `#1C3D3A` (dark teal)
- Border bottom: 2px solid `#E8872A`
- Logo links to: `ka_home.html`

### COGS 160 course nav

For all pages within the 160sp/ directory and all pages that primarily serve enrolled students:

```
[Logo: Knowledge Atlas / COGS 160] | Syllabus | A0 | A1 | Track 1 | Track 2 | Track 3 | Track 4 | [Student Profile]
```

- Same visual styling as global nav
- Logo links to: `160sp/ka_schedule.html`
- Student Profile: shows initials from JWT, clickable dropdown with name, email, role, logout, account settings

### Which pages use which nav

- **Course nav**: Everything in `160sp/`, `ka_login.html`, `ka_register.html`, `ka_account_settings.html`, `ka_google_search_guide.html`, `ka_ai_methodology.html` (course content even though at root level)
- **Global nav**: `ka_home.html`, `ka_topics.html`, `ka_evidence.html`, `ka_gaps.html`, `ka_article_search.html`, `ka_contribute.html`, `ka_explain_system.html`, and all non-course content pages

---

## Rules for Design Agents

1. **Always use the canonical SVG icon** from this guide. Never create new logo variants.
2. **Never put page titles in the brand area.** The wordmark is "Knowledge Atlas" (+ "COGS 160" for course pages). Page identity goes in breadcrumbs or page headers, not the logo.
3. **Use the correct nav regime** based on page audience. When in doubt, use the course nav for student-facing pages.
4. **The nav bar must include a functional profile element** on auth-gated pages — showing the logged-in user's initials from the JWT, with a clickable dropdown for logout and settings.
5. **No System State panels, demo mode modals, or developer scaffolding** on any student-facing page.
6. **Refer to the instructor as "Prof Kirsh"** in all user-facing text. "David" is not acceptable in student-facing contexts.
7. **Color accessibility is mandatory.** Run WCAG contrast checks on all text/background combinations.
