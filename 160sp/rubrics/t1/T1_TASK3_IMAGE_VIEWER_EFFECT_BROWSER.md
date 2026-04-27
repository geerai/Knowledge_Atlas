# Track 1 · Task 3: Annotate the Collection & Build the Image Viewer

**Track:** Image Tagger  
**Prerequisite:** Task 1 (your 500 images with provenance) + Task 2 (your 6 latent tag detectors)  
**Points:** 75  
**What you'll have when you're done:** Every image in your 500-image collection annotated with latent tag scores, plus an interactive web page where anyone can search and browse images by tag category OR by human effect.

---

## Why we need this

Your team built 6 latent tag detectors in Task 2. But you only tested them on a small gold-set. Now it's time to run them on the **entire 500-image collection** and then build a viewer so humans can actually browse, search, and verify the results.

Right now, the image-tagger repo has an Explorer app (v3.4.74), but it's a full React/Vite application that requires a running backend, database, and authentication. It's developer infrastructure, not something students and researchers can open in a browser and start using.

Here's the gap:

| What exists | What's missing |
|---|---|
| 424 tags in the `Tagging_Contractor` registry, organized by 44 domains | No way to browse images *by tag* without running the full tagger backend |
| 839 outcome terms in the `Outcome_Contractor`, across 7 domains (Cognitive, Affective, Behavioral, Social, Physiological, Neural, Health) | No way to ask "show me spaces that promote creativity" and see matching images |
| 832 constitutive bridges linking effects into a hierarchy | No UI that uses this hierarchy for filtering |
| Your 500 images with provenance (Task 1) | No searchable viewer for your collection |
| Your 6 latent tag detectors (Task 2) | **They've only run on a small gold-set — not the full collection** |

You're going to close both gaps: first annotate everything, then build the viewer.

---

## Phase 1: Run your detectors on the full image collection

Before you can browse annotations, you need to produce them. This is the moment of truth for your Task 2 detectors: do they actually work at scale?

### What we learned from prototyping this task

We prototyped the full pipeline for one latent tag (L42 Interactional Visibility) to verify everything works. Here's what you need to know:

**Dependencies are minimal.** You only need `Pillow` (PIL) and `numpy`. No deep learning frameworks are required — your detectors compute geometric predicates over image statistics, not neural network features.

**Proxy features work.** The registry says L42 requires "floor-plan-augmented isovist computation." You don't have floor plans. That's fine. The registry acknowledges this: the 2D proxy approach uses edge density, brightness variance, and partition coverage as stand-ins for the full isovist. Your detectors should document what they're proxying and why.

**Directional accuracy is what matters.** Our prototype scored an open office at 2.4/4.0 and a cubicle farm at 1.9/4.0 — correct direction, modest separation. That's expected for a proxy approach without real depth maps. If your detector separates high-visibility from low-visibility spaces in the right direction, it's working.

**Use the registry's output format.** Each tag in the registry has a `value_type` (binary, ordinal, continuous) and a `value_range`. The social interaction tags use `ordinal` with range `[0, 4]` (Likert scale). Your annotations must use the registry's `tag_id` as the key, not an invented name.

**Set confidence honestly.** Without real depth maps or segmentation, your confidence should be low (0.2-0.4). If you add a real depth model like MiDaS, confidence goes up. Document what confidence means in your detector's docstring.

### 1A. Write the batch runner contract

> **Contract objective:** "I want a script that runs all 6 of my latent tag detectors on every image in `collection.json` and produces a single `annotations.json` file with scores per image."
> **Contract is with:** Your 6 detector functions (from Task 2) and your `collection.json` (from Task 1).
> **Prompt hint:** *"I have 6 detector functions and 500 images. Write a batch runner that loads each image, runs all 6 detectors using PIL and numpy, and writes the results to annotations.json. It must handle failures gracefully — if one detector crashes on one image, log the error and continue. I only need Pillow and numpy, no ML frameworks."*

**Your contract must cover:**
- Reads image paths from `collection.json`
- For each image, loads the image with PIL and computes proxy features (edge density, brightness stats, color statistics)
- Runs all 6 detectors, collecting results per detector per image
- Writes a single `annotations.json` following the `image_tagger_observation` schema:

```json
{
  "version": "1.0",
  "generated_at": "2026-04-27T...",
  "detectors": ["social.interactional_visibility", "social.sociopetal_seating",
                "social.dyadic_intimacy", "social.small_group_conversation",
                "social.shared_attention_anchor", "social.boundary_permeability"],
  "images": {
    "img_001.jpg": {
      "room_type": "living_room",
      "tags": {
        "social.sociopetal_seating": {
          "value": 2.8,
          "value_type": "ordinal",
          "confidence": 0.35,
          "evidence": {
            "facing_pairs": 3,
            "cluster_size": 4,
            "depth_source": "proxy"
          }
        },
        "social.interactional_visibility": {
          "value": 3.2,
          "value_type": "ordinal",
          "confidence": 0.30,
          "evidence": {
            "partition_score": 0.15,
            "openness_score": 0.82,
            "partition_coverage": 0.08
          }
        }
      }
    }
  },
  "errors": {
    "img_099.jpg": {"detector": "social.shared_attention_anchor", "error": "image too dark for edge detection"}
  },
  "stats": {
    "total_images": 500,
    "images_annotated": 497,
    "images_with_errors": 3,
    "mean_scores": {"social.sociopetal_seating": 1.85, "social.interactional_visibility": 2.10}
  }
}
```

**Key:** Use the registry's `tag_id` (e.g., `social.interactional_visibility`), NOT an invented name. Use `value` (not `score`) with the tag's `value_type` and `value_range` from the registry.

### 1B. Write your tests BEFORE running

- [ ] Script runs on 10 images without crashing
- [ ] Each image gets scores for all 6 detectors (or a logged error)
- [ ] `annotations.json` is valid JSON and matches the schema above
- [ ] Failed images appear in the `errors` section (not silently dropped)
- [ ] Stats section has correct counts
- [ ] Score distributions are plausible (not all 0.0 or all 1.0)

### 1C. Run the batch and verify

```bash
python3 batch_annotate.py --collection collection.json --output annotations.json
```

After it finishes, check:

> *"How many images were annotated? How many had errors? Show me the score distribution for each detector — are they plausible?"*

**Reality check:** These are 0-4 Likert scores. If a detector scores > 2.5 on more than 80% of images, something is wrong — not every space has sociopetal seating. If a detector scores < 0.5 on everything, it might not be working. Our prototype found means around 1.9-2.4 across room types, which is plausible.

```python
# Quick sanity check
import json
ann = json.load(open("annotations.json"))
for det in ann["detectors"]:
    scores = [img["tags"][det]["value"]
              for img in ann["images"].values() if det in img.get("tags", {})]
    print(f"{det}: mean={sum(scores)/len(scores):.2f}, "
          f">2.5: {sum(1 for s in scores if s > 2.5)}/{len(scores)}")
```

### 1D. Fix detector issues discovered at scale

Running on 500 images will surface problems that 10 gold-set images didn't catch:
- Depth maps missing for certain room types
- Segmentation failing on unusual furniture
- Edge cases in your geometric predicates

Document what broke, fix it, re-run. This is the most valuable engineering learning in the task.

**Your deliverable:** `annotations.json` with scores for 500 images, plus a "batch run report" documenting errors found and fixes applied.

---

## Phase 2: Build the image viewer

Now that you have `annotations.json`, build a standalone HTML viewer. We've prototyped this and confirmed it's feasible as a single HTML file with inline CSS and JavaScript — no framework, no backend, no build step.

> **Contract objective:** "I want a standalone HTML page that loads `annotations.json` and the tag registry, and lets users browse images by tag domain or by human effect."

### Architecture: one HTML file, three data files

```
ka_image_viewer.html      ← your viewer (HTML + CSS + JS, all inline)
annotations.json          ← your Phase 1 output (500 images × 6 tag scores)
effect_tag_mapping.json   ← maps Outcome_Contractor effects to tag IDs
collection.json           ← your Task 1 image manifest (paths + provenance)
```

The viewer loads these JSON files at startup with `fetch()`. Everything runs client-side.

### Component 1: Mode selector (tag mode vs. effect mode)

Two tab buttons at the top. When the user clicks a tab, the filter bar switches.

```
┌─────────────────────────────────────────────────────┐
│  🏷️ [Search by Tag]   🧠 [Search by Effect]        │
└─────────────────────────────────────────────────────┘
```

- **Tag mode:** Shows domain checkboxes from the Tagging_Contractor registry
- **Effect mode:** Shows domain checkboxes from the Outcome_Contractor vocab

### Component 2: Filter bar

**In tag mode:** One checkbox per tag domain, generated dynamically from the registry. Group the 44 domains into manageable categories:

```
┌─────────────────────────────────────────────────────┐
│ 🔍 [Search images, tags, effects...              ]  │
│                                                     │
│ ☐ Social-Spatial (18)  ☐ Lighting (41)             │
│ ☐ Spatial Config (39)  ☐ Biophilia (20)            │
│ ☐ Materials (14)       ☐ Complexity (22)           │
│ ☐ Color (14)           ☐ ...more                   │
└─────────────────────────────────────────────────────┘
```

**In effect mode:** One checkbox per Outcome_Contractor domain:

```
┌─────────────────────────────────────────────────────┐
│ ☐ Cognitive (100)    ☐ Affective (94)              │
│ ☐ Behavioral (147)  ☐ Social (128)                 │
│ ☐ Physiological (131)  ☐ Neural (107)              │
│ ☐ Health (132)                                      │
└─────────────────────────────────────────────────────┘
```

**How to build the domain checkboxes:**

```javascript
// Load registry, extract unique domains, count tags per domain
const registry = await fetch('registry_v0.2.8.json').then(r => r.json());
const domains = {};
for (const [tid, tag] of Object.entries(registry.tags)) {
  const d = tag.domain || 'unknown';
  domains[d] = (domains[d] || 0) + 1;
}
// Render as checkbox inputs
filterBar.innerHTML = Object.entries(domains)
  .sort((a,b) => b[1] - a[1])
  .map(([name, count]) => 
    `<input type="checkbox" id="d-${name}" onchange="render()">` +
    `<label for="d-${name}">${name} (${count})</label>`
  ).join('');
```

### Component 3: Image grid

A CSS Grid of image cards. Each card shows:
- **Thumbnail** (the actual image from `collection.json` paths)
- **Image name** (from filename)
- **Room type** (from collection metadata)
- **Tag count** ("6 tags")
- **Top tag score** as a colored bar (green > 0.6, yellow 0.3-0.6, red < 0.3)
- **Score label** ("interactional visibility: 3.2/4.0")

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}
```

**Filtering logic:** When checkboxes are selected, filter `annotations.json` to show only images that have tags in the selected domains with scores above a threshold (e.g., > 0.5).

**Pagination:** For 500 images, implement lazy loading or "Load more" to avoid DOM overload. Show 50 images per page.

### Component 4: Image detail modal

When the user clicks a card, show a modal with:

```
┌─────────────────────────────────────────────────────┐
│                                              [×]    │
│  test open office                                   │
│  Room: office · Source: Unsplash · License: CC0     │
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │                                             │    │
│  │          [Full-size image]                   │    │
│  │                                             │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  Tags & Scores                                      │
│  ┌─────────────────────────────────────────────┐    │
│  │ interactional visibility    3.2/4.0  ████░  │    │
│  │   partition_score: 0.150                    │    │
│  │   openness: 0.820                           │    │
│  │   partition_coverage: 0.080                 │    │
│  ├─────────────────────────────────────────────┤    │
│  │ sociopetal seating          1.8/4.0  ██░░░  │    │
│  │   facing_pairs: 2                           │    │
│  │   cluster_size: 3                           │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  Linked Effects                                     │
│  [Social] ← interactional visibility, sociopetal    │
│  [Cognitive] ← interactional visibility             │
└─────────────────────────────────────────────────────┘
```

Key elements:
- **Score bars:** Colored bars proportional to the 0-4 Likert value
- **Evidence table:** Show every key-value pair from the `evidence` dict in the annotation
- **Linked effects:** For each Outcome_Contractor domain that maps to tags present on this image, show the domain name and which tags triggered it. Use `effect_tag_mapping.json` for this.
- **Provenance:** Source URL, photographer, license from `collection.json`

### Component 5: Effect explanations (effect mode only)

When browsing by effect, each card should show WHY it matched:

```
tag → mechanism → effect

Example: "interactional visibility (3.2/4.0) → mutual awareness → Social outcomes"
```

Build this from the `ae_outcome_lookup.json` and PNU templates.

### How to build `effect_tag_mapping.json`

This is the bridge between the Outcome_Contractor's 7 domains and the Tagging_Contractor's tag IDs. You need it for effect-mode filtering.

**Option A (recommended — use existing data):**

```python
# Start from ae_outcome_lookup.json (2,114 pre-built term→outcome mappings)
import json
lookup = json.load(open('Outcome_Contractor/contracts/oc_export/ae_outcome_lookup.json'))
# This maps text terms → outcome IDs
# Cross-reference with your tag IDs to build domain-level mapping
```

**Option B (manual, for your 6 tags):**

Since you only have 6 detectors, you can manually map them to effects:

```json
{
  "effect_to_tags": {
    "social": ["social.interactional_visibility", "social.sociopetal_seating",
               "social.dyadic_intimacy", "social.shared_attention_anchor"],
    "cog": ["social.interactional_visibility"],
    "affect": ["social.sociopetal_seating", "social.dyadic_intimacy"],
    "behav": ["social.sociopetal_seating", "social.interactional_visibility"]
  }
}
```

Ask your AI: *"Given these 6 latent tags and their registry definitions, which Outcome_Contractor domains (Cognitive, Affective, Behavioral, Social, Physiological, Neural, Health) does each tag relate to? Use the PNU templates in Article_Eater/data/templates/ for evidence."*

### Success conditions

- [ ] Viewer loads `annotations.json`, `collection.json`, and `effect_tag_mapping.json` at startup
- [ ] Tag mode: domain checkboxes generated from registry, filtering shows only matching images
- [ ] Effect mode: 7 domain checkboxes from Outcome_Contractor, filtering uses the effect→tag mapping
- [ ] Free text search works across image names, room types, tag names, and effect names
- [ ] Image grid handles 500 images (lazy loading or pagination — 50 per page)
- [ ] Clicking a card opens detail modal with all tags, scores, evidence, effects, and provenance
- [ ] Score bars are color-coded (green/yellow/red) and proportional to value
- [ ] No backend needed — works as a standalone HTML file opened directly in a browser
- [ ] Both modes can be combined (e.g., "Social-Spatial" tag domain + "Cognitive" effect domain)

---

## Phase 3: Polish and integrate

- [ ] Score distributions look correct (not all 0.0, not all 4.0)
- [ ] Provenance is visible on every image (source URL, photographer, license)
- [ ] Annotation scores shown as visual bars with value labels
- [ ] Modal close on Escape key and overlay click
- [ ] Responsive layout (works on mobile and desktop)
- [ ] Page title and subtitle describe what the tool does
- [ ] Empty state ("No images match your filters") when nothing matches

Write YOUR OWN contract and tests for this phase.

---

## What you submit

| Item | What it is |
|---|---|
| **`annotations.json`** (Phase 1) | All 500 images annotated with all 6 detector scores |
| **Batch run report** (Phase 1) | Errors found at scale, fixes applied, score distributions |
| **`ka_image_viewer.html`** (Phase 2) | Standalone viewer with tag + effect search |
| **`effect_tag_mapping.json`** (Phase 2) | Mapping from effects to tags |
| **Contracts + tests** | Your written contracts and test checklists for each phase |
| **Viewer walkthrough** | Screenshots or recording showing both search modes |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 10 | Written BEFORE building. Specific. **(CONTRACT GATE)** |
| **Batch annotation** | 15 | 500 images annotated, errors logged, score distributions plausible |
| **Scale fixes** | 10 | Documented what broke at scale and how you fixed it |
| **Tag browser** | 15 | Checkboxes for domains, filtering works, grid handles 500 images |
| **Effect browser** | 15 | 7 Outcome domains, drill-down, tag→effect chain shown |
| **Image detail + polish** | 10 | Tags, effects, provenance, confidence all visible, standalone HTML |

> ⛔ **Contract gate**: If your contracts and tests are missing or vague, your work will be flagged as not ready for integration.

---

## Data sources you should know about

### Tag and annotation data

| Repo / File | What it gives you |
|---|---|
| `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json` | 424 tags across 44 domains — your tag filter categories |
| `Tagging_Contractor/.../observations/image_tagger_observation.schema.json` | **Official annotation schema** — your `annotations.json` should conform to this. Each tag entry has `tag_id`, `value_type` (binary/ordinal/continuous), `value`, `confidence`, and `evidence` |
| `Tagging_Contractor/contracts/localized_image_tags.schema.json` | Spatial annotation schema with `semantic_regions`, `dense_maps`, and `pipeline_provenance` — use this if your detectors produce region-level output |
| Your `collection.json` from Task 1 | 500 images with room types and provenance |
| Your 6 detector functions from Task 2 | Detectors that produce `TagResult` per image |

### Effect and outcome data

| Repo / File | What it gives you |
|---|---|
| `Outcome_Contractor/contracts/oc_export/outcome_vocab.json` | 839 effect terms across 7 domains — your effect filter categories |
| `Outcome_Contractor/contracts/oc_export/constitutive_bridges.json` | 832 parent→child bridges — the effect hierarchy for drill-down |
| `Outcome_Contractor/contracts/oc_export/ae_outcome_lookup.json` | **Pre-built tag→outcome lookup** — 2,114 entries mapping text terms to outcome IDs. This is your shortcut for the effect browser. Instead of building `effect_tag_mapping.json` from scratch, start here |
| `Outcome_Contractor/contracts/oc_export/bn_outcome_nodes.json` | Bayesian network node definitions — shows causal structure between outcomes |
| `Outcome_Contractor/contracts/oc_export/VERSION_MANIFEST.json` | Tells you the schema versions and file checksums for all OC exports |

### Existing viewer code (reference, not required)

| Repo / File | What it gives you |
|---|---|
| `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/frontend/apps/explorer/` | Existing React explorer — study `ImageDetailModal.jsx` to see what APIs it calls (depth, segmentation, materials, affordance). You don't need to use this code, but it shows the data model |
| `image-tagger/docs/CONTRACT.md` | Image Tagger API contract — `ExplorerSearchResponse` shows the response shape |
| `image-tagger/docs/ENGINEERING_BRIEF.md` | Architecture overview — four user journeys: Explorer, Workbench, Monitor, Admin |
| `Article_Eater/data/templates/` | 166 PNU templates linking tags to effects — use these to enrich your `effect_tag_mapping.json` beyond what `ae_outcome_lookup.json` provides |

---

## Reuse

Your `annotations.json` becomes the canonical annotation layer for the image collection. Your viewer becomes the public-facing tool for the Image Tagger track. Both will be reused by future cohorts — build them as infrastructure, not throwaway assignments.
