# K-ATLAS Visual Style Guide

**Date**: 2026-04-15
**Status**: Canonical — all AI workers (CW, AG, Codex) and human contributors must follow this guide
**Location**: `docs/KA_STYLE_GUIDE.md`
**Supersedes**: `docs/KA_BRAND_STYLE_GUIDE.md` (which covered brand identity only; this guide adds the full token set, component patterns, and the three-regime distinction)

---

## 1. Three Visual Regimes

K-ATLAS serves three audiences with three visual regimes that share a common design language but differ in palette emphasis, navigation, and information density.

### 1a. Global K-ATLAS (the research tool)

For pages serving all user types — researchers, practitioners, contributors, and students browsing the knowledge network.

| Property | Value |
|----------|-------|
| Nav background | `#1C3D3A` (dark teal) |
| Nav accent | `#F5A623` (amber) |
| Hero gradient | `#1C3D3A → #163230` |
| Body background | `#F7F4EF` (cream) |
| Card border | `#E0D8CC` |
| Primary accent | `#2A7868` (teal) |
| CTA accent | `#E8872A` (warm amber) |
| Typography | System sans + Georgia serif headings |
| Nav items | Articles · Topics · Theories · Mechanisms · Neural Underpinnings |
| Logo links to | `ka_home.html` |

### 1b. COGS 160 Spring (160sp — the Spring 2026 course)

For all pages primarily serving enrolled Spring students: everything in `160sp/`, the schedule, login, track hubs, setup guides.

| Property | Value |
|----------|-------|
| Palette | **Same** as Global K-ATLAS |
| Nav items | Syllabus · A0 · A1 · Track 1 · Track 2 · Track 3 · Track 4 · [Student Profile] |
| Logo links to | `160sp/ka_schedule.html` |
| Wordmark third line | `COGS 160` in `#7a9bbf` |
| Phase colours | Design=teal-bg, Build=blue-lt, Run=green-lt, Present=amber-lt |
| Week card accent | Left border matches phase colour |

### 1c. COGS 160 Fall (the original Designing_Experiments course site)

The original course site lived in `Designing_Experiments/docs/student_tracks/` and used a **different palette** based on the official UCSD blue. When the Fall schedule was ported to K-ATLAS as `fall160_schedule.html`, it was restyled to match the K-ATLAS palette. However, the legacy Designing_Experiments pages remain on the old palette and should not be mixed with K-ATLAS pages.

| Property | Legacy Fall (Designing_Experiments) | Ported Fall (fall160_schedule.html) |
|----------|-------------------------------------|-------------------------------------|
| Primary colour | `#002d5b` (UCSD blue) | `#1C3D3A` (K-ATLAS teal) |
| Gradient | `#002d5b → #00508f` | `#1C3D3A → #163230` |
| Accent/highlight | `#00a699` (bright teal) | `#E8872A` (amber) |
| Track colours | Orange `#d4620f`, Green `#1a7a5e`, Gold `#b8860b`, Purple `#6b3fa0` | Same track phase colours as Spring |
| Body background | `#f5f5f5` (neutral grey) | `#F7F4EF` (cream) |
| Border accent | `#002d5b` (blue) | `#D8D0C5` (warm grey) |
| Typography | System sans, no serif headings | System sans + Georgia serif headings |

**Rule**: All new pages use the K-ATLAS palette (regime 1a or 1b). The legacy UCSD-blue palette is frozen in Designing_Experiments and must not be extended. If a Fall page needs to be created or updated, use the K-ATLAS palette with Fall-specific content.

---

## 2. Colour Tokens

### 2a. Primary Palette

| Token | Hex | CSS var | Usage |
|-------|-----|---------|-------|
| Dark Teal | `#1C3D3A` | `--navy` | Nav background, hero background, headings |
| Teal | `#2A7868` | `--teal` | Links, active tab borders, primary brand |
| Light Teal | `#5AC8AA` | `--teal-lt` | Hero eyebrows, progress indicators |
| Teal Background | `#E6F5F0` | `--teal-bg` | Design-phase banners, pill backgrounds |
| Amber | `#E8872A` | `--amber` | CTA buttons, progress bars, active nav, "las" in wordmark |
| Light Amber | `#FFF3E0` | `--amber-lt` | Present-phase banners, warning backgrounds |
| Dark Amber | `#9a5010` | `--amber-dk` | Badge text on light amber |
| Gold | `#F5A623` | — | Wordmark accent, active nav highlight, SVG hub node |
| Cream | `#F7F4EF` | `--cream` | Body background |

### 2b. Neutrals

| Token | Hex | Usage |
|-------|-----|-------|
| Ink | `#2D2D2D` or `#2C2C2C` | Primary body text |
| Muted | `#6B6B6B` | Secondary text, taglines |
| Label Grey | `#8A9A96` | Section numbers, small-caps labels, twisty icons |
| Light Grey | `#7A7060` | Venue text, meta information |
| Border | `#E0D8CC` or `#D8D0C5` | Card borders, dividers |
| Light Background | `#F9F5EE` | Panel heads, hover states, card sections |
| Breadcrumb Background | `#E8E0D4` | Breadcrumb strip |
| Breadcrumb Text | `#6A5A4A` | Breadcrumb separator, muted text |

### 2c. Semantic Colours

| State | Background | Text/Border | Usage |
|-------|------------|-------------|-------|
| Success | `#d4edda` | `#155724` | Completed, well-established |
| Supported | `#E8F8F2` | `#1A7050` | Supported claims, green pills |
| Info/Cool | `#E8F0FE` | `#1A56A0` | Informational pills, blue badges |
| Warning | `#FEF3E2` | `#985E0A` | Speculative banners, amber pills |
| Error | `#FEE4E4` | `#A02020` | Local-only badges, speculative status |
| Neuro | `#F3E8FE` | `#6B2FA0` | Neural-underpinning pills |

### 2d. Phase Colours (Schedule Pages)

| Phase | Background | Border | CSS class |
|-------|------------|--------|-----------|
| Design | `#E6F5F0` | `#b8dfd8` | `.phase-design` |
| Build | `#EBF2F8` (`--blue-lt`) | `#b8cce8` | `.phase-build` |
| Run | `#E3F4EC` (`--green-lt`) | `#a0d8b8` | `.phase-run` |
| Present | `#FFF3E0` (`--amber-lt`) | `#f0c888` | `.phase-present` |

### 2e. VOI (Value of Investigation) Dots

| Level | Colour | Class |
|-------|--------|-------|
| Critical | `#D63B3B` | `.voi-critical` |
| High | `#E8872A` | `.voi-high` |
| Medium | `#D4A820` | `.voi-medium` |
| Low | `#A0B8B0` | `.voi-low` |

### 2f. On-Dark Text (for use on `#1C3D3A` or darker backgrounds)

| Element | Colour | Notes |
|---------|--------|-------|
| Nav text (default) | `#B8D4CE` | Links, muted text |
| Nav text (hover) | `#FFFFFF` | |
| Nav text (active) | `#F5A623` | With 2px bottom border |
| Wordmark "KNOWLEDGE" | `#A8C8BF` | Small-caps, lightweight |
| Wordmark "Atlas" | `#FFFFFF` | Bold |
| Wordmark "las" | `#F5A623` | Amber accent |
| Hero eyebrow | `#7AACA0` | Small-caps |
| Hero body text | `#9ABFB8` | Paragraph text on hero |
| Hero h1 | `#FFFFFF` | |

---

## 3. Typography

### 3a. Font Stack

| Role | Stack |
|------|-------|
| Body / UI | `-apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif` |
| Headings (Georgia) | `Georgia, serif` — used for h1, h2, section titles, card titles, week titles |
| Code | System monospace via `<code>` and `<pre>` elements |

### 3b. Scale

| Element | Size | Weight | Other |
|---------|------|--------|-------|
| Body text | 15px (implicit via browser default) | 400 | line-height: 1.5 |
| Nav links | 0.88rem | 500 | |
| Small-caps labels | 0.66–0.72rem | 700 | letter-spacing: 0.08–0.24em, text-transform: uppercase |
| Card titles | 1.05rem | 700 | Georgia serif |
| Section titles (h2) | 1.3–1.35rem | 700 | Georgia serif, border-bottom: 2px solid `#E0D8CC` |
| Page title (h1) | 1.9–2.1rem | 600–700 | Georgia serif, on hero |
| Meta text | 0.78rem | 400 | colour: `#7A7060` |
| Pills / badges | 0.66–0.68rem | 600–700 | letter-spacing: 0.04em |
| Breadcrumb | 0.78rem | — | |
| Footer | 0.8rem | — | |

### 3c. Line Heights

| Context | Value |
|---------|-------|
| Body text | 1.5 (shell default) |
| Prose blocks | 1.6–1.7 (summary-prose, hub-region-body) |
| Cards / compact UI | 1.35 |
| Wordmark | 1.1 |

---

## 4. Spacing

### 4a. Core Spacing Scale

| Size | Value | Usage |
|------|-------|-------|
| xs | 4px | Pill internal padding, very tight gaps |
| sm | 8px | Breadcrumb padding, pill gaps, small margins |
| md | 12px | Card internal padding between elements, form field spacing |
| lg | 16px | Card grid gap, panel body padding |
| xl | 18px | Hub region body padding, main card padding |
| 2xl | 24px | Shell grid gap, nav horizontal padding, page padding |
| 3xl | 32px | Hero padding, article-shell column gap |
| 4xl | 44–48px | Hero vertical padding, major section spacing |

### 4b. Border Radius

| Element | Value |
|---------|-------|
| Cards, panels, regions | 10–12px |
| Buttons, inputs, code blocks | 6–8px |
| Pills, badges | 10–12px (circular) |
| User pill in nav | 20px (capsule) |

### 4c. Shadows

| Context | Value |
|---------|-------|
| Navbar | `0 2px 8px rgba(0,0,0,0.15)` |
| Card hover | `0 6px 20px rgba(0,0,0,0.08)` |
| Week card rest | `0 1px 3px rgba(0,0,0,0.05)` |
| Search focus | `0 0 0 3px rgba(42,120,104,0.15)` |

---

## 5. Component Patterns

### 5a. Navbar (`ka_canonical_navbar.js` + `ka_atlas_shell.css`)

The canonical navbar is injected by JavaScript. Every page must include:

```html
<body data-ka-active="articles"
      data-ka-crumbs='[["Home","ka_home.html"],["Articles",""]]'>
<div id="ka-navbar-slot"></div>
<div id="ka-breadcrumb-slot"></div>
...
<script src="ka_canonical_navbar.js" defer></script>
```

Valid `data-ka-active` values: `articles`, `topics`, `theories`, `mechanisms`, `neural`, `home`, or empty string.

Pages in `160sp/` automatically get `../` prefixed to all nav links via `basePrefix()`.

**Do not** build custom inline navbars. If a page has one, migrate it to the canonical pattern.

### 5b. Cards (`.ka-card`)

White background, 1.5px `#E0D8CC` border, 12px radius. On hover: subtle lift (`translateY(-2px)`) + shadow. Expanded state spans full grid width with teal border. Card children: `.ka-card-title` (Georgia, 1.05rem), `.ka-card-meta` (0.78rem, muted), `.ka-card-pills`, `.ka-card-body` (hidden until expanded).

### 5c. Pills (`.ka-pill`)

Small rounded labels: 0.68rem, 600 weight, 3px/9px padding, 12px radius. Four variants: default (teal-on-green), `.ka-pill-warn` (amber-on-cream), `.ka-pill-cool` (blue), `.ka-pill-neuro` (purple).

### 5d. Tabs (`.ka-tabs`)

Horizontal tab bar with 2px bottom border `#E0D8CC`. Active tab: teal text + teal bottom border. Panels use `.ka-tabpanel` / `.ka-tabpanel.active`.

### 5e. Hub Regions (`.hub-region`)

For track hub pages. White card with `#F9F5EE` header background. Region number in small-caps label grey. Region title in Georgia serif. Body padding 16px 18px.

### 5f. Task Manifests (`.task-manifest`)

Collapsible task cards within hub regions. Status pills: `.status-supported` (green), `.status-partial` (amber), `.status-speculative` (red). Definition-list layout: 130px label column + 1fr value column.

### 5g. Expandable Panels (`.panel`)

White card, dashed border-top separator when open. Twisty indicator (▸) rotates 90° on open. Used for related-articles lists, challenge details, etc.

### 5h. Buttons

Two variants: `.ka-btn-primary` (amber `#E8872A` background, white text) and `.ka-btn-secondary` (cream background, dark text, subtle border). 8px/14px padding, 8px radius, 0.85rem font.

---

## 6. Layout Patterns

### 6a. Two-Column Article Layout

```css
.article-shell {
  max-width: 1180px; margin: 0 auto; padding: 24px;
  display: grid; grid-template-columns: 1fr 280px; gap: 32px;
}
```

Main content on left, sticky right rail (TOC) at 280px. Collapses to single column below 900px.

### 6b. Shell with Journey Nav

```css
.ka-shell {
  display: grid;
  grid-template-columns: 240px 1fr;
  max-width: 1400px;
  gap: 24px;
}
```

Left subnav (sticky at top: 76px) + main content area. Collapses to single column below 900px.

### 6c. Card Grid

```css
.ka-card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}
```

### 6d. Miller Columns

Three-column hierarchy selector with 12px gap, 10px border-radius wrapper. Each column scrolls independently (max-height 540px). Selected items turn dark-teal background.

---

## 7. Accessibility (MANDATORY)

1. **WCAG 2.1 AA minimum** for all text/background pairs (4.5:1 normal text, 3:1 large text).
2. **Never use dark blue text on dark backgrounds.** See root CLAUDE.md for terminal-colour specifics.
3. **Skip link** (`.ka-skip`) must appear on every page with the canonical navbar (the JS injects it automatically).
4. **Focus indicators**: search inputs get a teal ring (`box-shadow: 0 0 0 3px rgba(42,120,104,0.15)`). Tab focus must be visible on all interactive elements.
5. **Alt text** required on all images (the figure gallery uses `onerror` fallbacks for missing images).
6. **Colour is never the sole channel** — use text labels, patterns, or icons alongside colour-coded status.

---

## 8. Do / Don't Quick Reference

### Do

- Use the canonical navbar on every page via `ka_canonical_navbar.js`.
- Use Georgia serif for headings, system sans for body.
- Use cream `#F7F4EF` as page background, white `#FFFFFF` for cards and panels.
- Use the K-ATLAS teal/amber palette for all new pages.
- Use pills (`.ka-pill`) for status labels, not bold coloured text.
- Use `ka_atlas_shell.css` as the shared stylesheet.
- Use proper list markup (`LevelFormat.BULLET`) in docx, not unicode bullets.

### Don't

- Don't invent new colour palettes. If a new semantic state is needed, propose it here.
- Don't use the UCSD-blue palette (`#002d5b`, `#00508f`) on K-ATLAS pages — that's the legacy Designing_Experiments scheme.
- Don't use the Article_Eater `GUI_STYLE_GUIDE.md` palette (`#182B49`, `#00C6D7`) for K-ATLAS — that's the Streamlit dashboard.
- Don't build inline navbars. Always use the canonical `ka-navbar-slot` pattern.
- Don't put page titles in the brand/logo area (the wordmark is "Knowledge Atlas" only).
- Don't use dark blue text on dark backgrounds.
- Don't use `ShadingType.SOLID` in docx tables (causes black backgrounds).

---

## 9. Three Palettes at a Glance (Quick Disambiguation)

| Property | K-ATLAS (canonical) | Article_Eater Dashboard | Designing_Experiments (legacy) |
|----------|--------------------|-----------------------|-------------------------------|
| Primary | `#1C3D3A` dark teal | `#182B49` UCSD navy | `#002d5b` UCSD blue |
| Accent | `#F5A623` amber | `#C69214` UCSD gold | `#00a699` bright teal |
| CTA | `#E8872A` warm amber | `#00C6D7` UCSD teal | `#d4620f` orange |
| Background | `#F7F4EF` cream | White | `#f5f5f5` neutral grey |
| Headings font | Georgia serif | Inter sans | System sans (no serif) |
| CSS location | `ka_atlas_shell.css` | Inline in Streamlit | Inline in each HTML file |
| Authority file | **This guide** | `AE/docs/GUI_STYLE_GUIDE.md` | None (legacy, frozen) |

**If you are building or modifying any K-ATLAS page, use only the K-ATLAS column.**
