# Track 1 · Task 3: Build the Image Viewer & Effect Browser

**Track:** Image Tagger  
**Prerequisite:** Task 1 (your 500 images with provenance) + Task 2 (your 6 latent tag detectors)  
**Points:** 75  
**What you'll have when you're done:** An interactive web page where anyone can search and browse the full image collection by tag category OR by human effect — "show me all restorative environments" or "spaces good for concentration."

---

## Why we need this

Right now, the image-tagger repo has an Explorer app (v3.4.74), but it's a full React/Vite application that requires a running backend, database, and authentication. It's developer infrastructure, not a tool students and researchers can open in a browser and start using.

What we're missing is simple: **a standalone HTML page that lets someone browse images by what they contain (tags) and by what they do to people (effects).**

Here's the gap:

| What exists | What's missing |
|---|---|
| 424 tags in the `Tagging_Contractor` registry, organized by 44 domains | No way to browse images *by tag* without running the full tagger backend |
| 839 outcome terms in the `Outcome_Contractor`, across 7 domains (Cognitive, Affective, Behavioral, Social, Physiological, Neural, Health) | No way to ask "show me spaces that promote creativity" and see matching images |
| 832 constitutive bridges linking effects into a hierarchy | No UI that uses this hierarchy for filtering |
| Your 500 images with provenance (Task 1) | No searchable viewer for your collection |
| Your 6 latent tag detector outputs (Task 2) | No way to see which images have which latent tags |

You're going to build the missing piece.

---

## Two ways to search

Your viewer needs two search modes. Both should feel natural.

### Mode 1: Search by Tag (from Tagging_Contractor)

The user picks environmental features they want to see. The tag categories come from the registry's domain hierarchy:

| Domain | Example tags | What a user might search for |
|---|---|---|
| Lighting | daylight ratio, glare, light warmth | "Show me spaces with strong daylighting" |
| Spatial | ceiling height, openness, enclosure | "Show me high-ceiling spaces" |
| Biophilia | plant count, water view, natural materials | "Show me biophilic interiors" |
| Social-Spatial | sociopetal seating, prospect, privacy | "Show me conversation-friendly layouts" |
| Materials | wood, concrete, glass | "Show me warm material palettes" |
| Color | warmth, saturation, contrast | "Show me cool-toned interiors" |
| Visual Complexity | clutter, symmetry, entropy | "Show me visually calm spaces" |

**Implementation:** Use the registry's 44 domains as high-level categories. Present them as checkboxes or a dropdown. When a user selects a domain, show all images tagged with any tag in that domain.

### Mode 2: Search by Effect (from Outcome_Contractor)

This is the more interesting mode. Instead of asking "what does this space *look like*?", the user asks "what does this space *do to people*?"

The Outcome_Contractor has 839 effect terms organized into 7 domains:

| Domain | # Terms | Example effects |
|---|---|---|
| Cognitive | 100 | Attention, Concentration, Creativity, Memory, Wayfinding |
| Affective | 94 | Stress, Restoration, Mood, Comfort, Awe |
| Behavioral | 147 | Collaboration, Productivity, Creative Output, Exploration |
| Social | 128 | Collaboration, Trust, Communication, Privacy |
| Physiological | 131 | Alertness, Fatigue, Sleep Quality, Cortisol |
| Neural | 107 | Amygdala, Prefrontal, Default Mode Network |
| Health | 132 | Flourishing, Well-being, Recovery |

**Implementation:** Present the 7 domains as top-level checkboxes. Let users drill into sub-effects. Use the constitutive bridges (`constitutive_bridges.json`) to resolve which effects roll up into which — so selecting "Restoration" also pulls in "Stress Recovery" and "Attention Restoration."

**How effects connect to images:** The PNU templates (from Track 2) link environmental features to outcomes. If a PNU says "daylight → circadian entrainment → alertness," then images tagged with high daylight scores should appear when a user searches for "alertness." This is the bridge between tags and effects.

---

## Required features

| Feature | What it does |
|---|---|
| **Free text search** | Search images by keyword (room type, tag name, or effect name) |
| **Tag category filter** | Checkboxes for the high-level tag domains from the registry |
| **Effect filter** | Checkboxes for the 7 Outcome_Contractor domains, with drill-down to sub-effects |
| **Thumbnail grid** | Shows matching images with room type, key tags, and provenance |
| **Image detail view** | Click an image to see: full size, all tags, all linked effects, provenance |
| **Tag overlay** | Shows which tags are active on the selected image, with confidence scores |
| **Effect explanation** | When browsing by effect, show WHY an image matches (which tag → which PNU → which effect) |
| **Scale** | Must handle your full 500-image collection (not just a 100-image sample) |
| **Data source** | Reads from `collection.json` (Task 1) and your detector outputs (Task 2) |

---

## Phase 1: Build the tag browser

> **Contract objective:** "I want a page where I can browse images by selecting tag categories from the Tagging_Contractor registry."
> **Contract is with:** The registry (`registry_v0.2.8.json`) and your `collection.json`.
> **Prompt hint:** *"Build an HTML page that reads the tag registry JSON and shows the 44 domains as checkboxes. When I check a domain, show all images from collection.json that have tags in that domain. Show thumbnails in a grid with room type and key tags."*

Write YOUR OWN contract. Include inputs, processing, outputs, success conditions.

**Success conditions:**
- [ ] All 44 tag domains appear as filterable categories
- [ ] Selecting a domain shows only images with tags in that domain
- [ ] Free text search works across tag names and room types
- [ ] Grid handles 500+ images without freezing (use lazy loading or pagination)
- [ ] Clicking an image shows detail view with all tags and confidence scores

---

## Phase 2: Build the effect browser

> **Contract objective:** "I want to search images by human effect — 'show me restorative environments' or 'spaces good for concentration' — using the Outcome_Contractor vocabulary."
> **Contract is with:** The `outcome_vocab.json` and `constitutive_bridges.json` from the Outcome_Contractor.
> **Prompt hint:** *"Add an effect browser to my viewer. Read the Outcome_Contractor's outcome_vocab.json (7 domains, 839 terms) and constitutive_bridges.json (832 parent-child relationships). Show the 7 domains as top-level checkboxes. When I select 'Cognitive → Concentration', show images whose tags are linked to concentration through the PNU mechanism chains."*

**The hard part:** Connecting effects to images requires the bridge between tags and outcomes. The PNU templates define these links (environmental feature → neural mechanism → human outcome). Your viewer needs to:

1. Read the Outcome_Contractor vocabulary
2. For each effect, find which environmental tags predict it (via PNU templates or a precomputed lookup)
3. Show images that have those tags

If the full PNU bridge is too complex for this task, start with a **simplified mapping** — a JSON file that maps high-level effect domains to tag domains:

```json
{
  "effect_to_tags": {
    "cog.attention": ["lighting.daylight_ratio", "complexity.edge_density", "spatial.openness"],
    "affect.restoration": ["biophilia.plant_count", "biophilia.water_view", "lighting.daylight_ratio"],
    "affect.stress": ["complexity.shannon_entropy", "spatial.enclosure", "lighting.glare"],
    "behav.creativity": ["spatial.ceiling_height", "color.warmth", "complexity.visual_complexity"],
    "social.collaboration": ["social.sociopetal_seating", "social.interactional_visibility"]
  }
}
```

You can generate this mapping by asking your AI to read the PNU templates and extract the tag→outcome links.

**Success conditions:**
- [ ] All 7 Outcome_Contractor domains appear as filterable categories
- [ ] Selecting an effect shows images with tags linked to that effect
- [ ] Effect explanations show the chain: tag → mechanism → effect
- [ ] Hierarchy drill-down works (selecting "Cognitive" shows sub-effects)

---

## Phase 3: Polish and integrate

- [ ] Both search modes (tag and effect) can be combined
- [ ] Image detail view shows BOTH tags and linked effects
- [ ] Provenance is visible (source URL, photographer, license)
- [ ] Data persists — reads from JSON files, no backend required
- [ ] Works as a standalone HTML file that can be opened in any browser

Write YOUR OWN contract and tests for this phase.

---

## What you submit

| Item | Filename |
|---|---|
| Image viewer page | `ka_image_viewer.html` |
| Tag-to-effect mapping | `effect_tag_mapping.json` |
| Contracts + tests | Your written contracts and test checklists |
| Viewer walkthrough | Screenshots or recording showing both search modes |
| File manifest | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 15 | Written BEFORE building. Specific. **(CONTRACT GATE)** |
| **Tag browser** | 20 | Checkboxes for 44 domains, filtering works, grid handles 500 images |
| **Effect browser** | 20 | 7 Outcome domains, drill-down, tag→effect chain shown |
| **Image detail view** | 10 | Tags, effects, provenance, confidence scores all visible |
| **Polish + integration** | 5 | Both modes combine, standalone HTML, no backend needed |
| **Verification** | 5 | Caught problems in AI's implementation, documented fixes |

> ⛔ **Contract gate**: If your contracts and tests are missing or vague, your viewer will be flagged as not ready for integration.

---

## Data sources you should know about

| Repo / File | What it gives you |
|---|---|
| `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json` | 424 tags across 44 domains — your tag filter categories |
| `Outcome_Contractor/contracts/oc_export/outcome_vocab.json` | 839 effect terms across 7 domains — your effect filter categories |
| `Outcome_Contractor/contracts/oc_export/constitutive_bridges.json` | 832 parent→child bridges — the effect hierarchy |
| Your `collection.json` from Task 1 | 500 images with room types and provenance |
| Your detector outputs from Task 2 | Latent tag scores per image |
| `Article_Eater/data/templates/` | 166 PNU templates linking tags to effects (for building `effect_tag_mapping.json`) |
| `image-tagger/docs/CONTRACT.md` | Existing Image Tagger API contract — see `ExplorerSearchResponse` for the data model |
