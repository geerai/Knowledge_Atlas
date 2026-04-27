# Track 1 · Task 1: Image Collection Pipeline

**Track:** Image Tagger  
**What you build:** Explore the Tagging Contractor's 424-tag registry to understand what we need to detect in architectural images, curate your own list of open-source image databases, build an automated image search pipeline, and deliver 500 images with full provenance into a collection dashboard.  
**Core lesson:** Before you can tag or train anything, you need images — and every image needs to say where it came from and what license it carries. This is infrastructure.

---

## What You're Working With

### The three repos

| Repo | What it provides | What you need from it |
|---|---|---|
| `Tagging_Contractor` | **424 tags** organized by domain (Lighting, Spatial, Materials, Color, Biophilia, etc.) with definitions, aliases, extractability flags, and extraction methods | The tag hierarchy — which tags can be detected from 2D images |
| `Outcome_Contractor` | **Human-side vocabulary** — cognitive, affective, behavioral effects (attention, stress, mood, productivity) | Context for WHY we need certain images (what effect are we testing?) |
| `image-tagger` | The Image Tagger app itself — Explorer, Workbench, Admin upload API | Where your images will eventually go |

### The tag registry

The canonical registry lives at:
```
Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json
```

Each of the 424 tags has these fields:
```json
{
  "affect.cozy": {
    "canonical_name": "Cozy",
    "domain": "Affect",
    "definition": "...",
    "aliases": ["Cozy", "feels Cozy", "sense of Cozy"],
    "extractability": {
      "from_2d": "yes",       // ← CAN we detect this from a photo?
      "from_3d_vr": "partial",
      "region_support": false
    },
    "extraction": {
      "method_family": "VLM/CLIP semantic classifier",
      "compute_from": "2D_semantic"
    }
  }
}
```

**The key field is `extractability.from_2d`.** Tags where this is `"yes"` or `"partial"` are the ones we can detect from photographs. Tags where this is `"no"` need sensors, 3D models, or metadata — we can't detect them from images alone.

### Tag domains (what you'll search for)

| Domain | Tags | Examples |
|---|---|---|
| Luminous Environment | 41 | daylight ratio, glare, light warmth, contrast |
| Spatial Configuration | 39 | ceiling height, room volume, openness, enclosure |
| Visual Complexity & Order | 22 | clutter, symmetry, edge density, entropy |
| Biophilic Elements | 20 | plant count, water view, natural materials, fractals |
| Social-Spatial | 18 | seating arrangement, privacy, prospect-refuge |
| Control & Personalization | 16 | adjustable lighting, furniture movability |
| CNfA (Cognitive Neuroarchitecture) | 48 | fractal dimension, coherence, mystery, legibility |
| Architecture / Components | 39 | ceiling type, wall material, kitchen layout, bathroom |
| Color | 14 | warmth, saturation, lightness contrast |
| Materials & Texture | 23 | wood, concrete, glass, roughness |

---

## Phase 1: Explore the Tag Hierarchy

### 1A. Read the registry

Ask your AI:

> *"Read the Tagging Contractor registry at `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json`. How many tags are there? Group them by domain. Which domains have the most tags? For each domain, list 3 example tags."*

### 1B. Filter to searchable tags

> *"Filter the registry to tags where `extractability.from_2d` is `'yes'` or `'partial'`. How many remain? These are the tags we can detect from photographs."*

### 1C. Build a simplified space-type taxonomy

> **Contract objective:** "I want a simplified taxonomy of 20-30 architectural interior space types that maps to the tag registry domains."
> **Contract is with:** The `Tagging_Contractor` registry and the image databases you'll search.
> **Prompt hint:** *"Based on the tag registry domains, create a taxonomy of interior space types that would give us good coverage. For example: living_room, bedroom, office, classroom, hospital_corridor, restaurant, lobby, etc. For each space type, list which tag domains are most likely present."*

Write YOUR OWN contract for this. Your contract must include:

1. **Inputs** — the registry JSON
2. **Processing** — how you group tags into searchable space types
3. **Outputs** — a JSON taxonomy file: `{ "living_room": { "expected_tags": [...], "search_terms": [...] }, ... }`
4. **Success conditions** — at least 20 space types, each maps to ≥ 3 registry tags, covers all major domains

**Deliverable:** `space_type_taxonomy.json` — your simplified taxonomy mapping space types to tag domains and search terms.

---

## Phase 2: Curate Open-Source Image Databases

### 2A. Research available sources

> **Contract objective:** "I want a curated, tested list of image databases where I can find CC-licensed architectural interior photographs."
> **Contract is with:** Free public image APIs and open datasets.
> **Prompt hint:** *"Find at least 5 sources of open-source/CC-licensed architectural interior images. For each source: what API does it offer (if any)? What license types? How many architectural images does it have? Can I filter by room type? Give me the API documentation URL."*

Start with these leads (but don't stop here):
- **Unsplash** — free API, requires attribution, good architectural content
- **Pexels** — free API, no attribution required, interior photos
- **Flickr** — API with CC license filtering, large architecture community
- **Wikimedia Commons** — CC/public domain, building interiors
- **Google Custom Search** — 100 free queries/day, license-filterable
- **Open Images Dataset (Google)** — labeled images, some indoor scenes
- **SUN Database** — scene recognition dataset with room types
- **Places365** — MIT scene dataset with interior categories

### 2B. Write YOUR OWN database curation contract

Your contract must include:
1. **Inputs** — your space type taxonomy
2. **Processing** — for each database: test the API, verify license, estimate image count
3. **Outputs** — a curated database list as JSON:
```json
{
  "databases": [
    {
      "name": "Unsplash",
      "api_url": "https://api.unsplash.com/",
      "api_type": "REST",
      "license": "Unsplash License (free, attribution requested)",
      "auth_required": true,
      "rate_limit": "50 req/hour (free)",
      "architectural_coverage": "good",
      "room_type_filter": false,
      "tested": true,
      "test_query": "modern living room interior",
      "test_result_count": 1247,
      "notes": "High quality but no room-type faceting"
    }
  ]
}
```
4. **Success conditions** — at least 5 databases tested, at least 3 with working APIs, combined coverage ≥ 10k images

### 2C. Validate

- [ ] Each database entry has a `tested: true` flag
- [ ] Each tested database has a `test_query` and `test_result_count`
- [ ] At least 3 databases have working API access
- [ ] Licenses are documented and allow non-commercial research use

**Deliverable:** `image_databases.json`

---

## Phase 3: Build the Image Search Pipeline

### 3A. Write YOUR OWN search pipeline contract

> **Contract objective:** "I want a Python script that takes my space-type taxonomy and searches my curated databases for images matching each space type."
> **Contract is with:** The image database APIs from Phase 2 and your taxonomy from Phase 1.
> **Prompt hint:** *"I need a search pipeline that loops through my space types, queries each database API, downloads image metadata (URL, title, license, source), and stores results as JSON. It must only collect openly licensed images and must track provenance."*

**Minimum bar** your contract must cover:
- Reads `space_type_taxonomy.json` for search terms
- Reads `image_databases.json` for API endpoints
- For each space type × database: runs the search query
- Collects per image: `url`, `thumbnail_url`, `title`, `photographer`, `license`, `source_database`, `source_page_url`
- De-duplicates by URL
- Respects rate limits
- Stores results as structured JSON

**Success conditions you must define:**
- How many images per space type?
- What's the minimum total across all space types?
- What fields are required vs. optional per image?

### 3B. Write your tests BEFORE building

- [ ] API calls use the correct authentication (API keys in env vars, not hardcoded)
- [ ] Rate limits respected (check for `time.sleep` or rate limiting)
- [ ] Only CC-licensed or public domain images collected (check license field)
- [ ] Every image has a `source_page_url` (the web page where the image was found)
- [ ] Every image has a `source_database` (which database it came from)
- [ ] Output JSON is valid and parseable
- [ ] De-duplication works (no duplicate URLs in output)

### 3C. Build and validate

> *"Show me the API call for one database. What parameters does it use? What does the response look like?"*

> *"How do you filter for license type? Show me the logic that rejects non-open images."*

> *"Run a test search for 'modern living room'. How many results? Do they look relevant?"*

**Deliverable:** `search_pipeline.py` + `search_results.json`

---

## Phase 4: Build the Collection Dashboard

### 4A. Write YOUR OWN collection page contract

> **Contract objective:** "I want an interactive web page where I can search for images, browse results, accept/reject them into my collection, and upload images from local files or folders — all with provenance tracking."
> **Contract is with:** The Image Tagger's upload API (`POST /v1/admin/upload`) and your search pipeline.
> **Prompt hint:** *"I need an HTML page with: (1) a search interface that queries my image databases, (2) a grid viewer showing results with thumbnails, (3) accept/reject buttons per image, (4) a file/folder upload zone, (5) provenance fields for each image (source URL, source name), (6) a collection counter showing progress toward 500."*

**Required features:**

| Feature | What it does |
|---|---|
| **Search bar** | Queries image databases by keyword or space type |
| **Results grid** | Shows thumbnails with title, source, license badge |
| **Accept / Reject** | Adds image to collection or marks as rejected |
| **File upload** | Drag-and-drop for single images, multiple files, or folders |
| **Provenance fields** | Per image: (1) source URL (auto-filled from search, manual for uploads), (2) source name (e.g., "Unsplash", "Architectural Digest", "House") |
| **License indicator** | Shows CC-BY, CC0, Public Domain, etc. |
| **Collection counter** | Shows `N / 500` progress |
| **Export** | Exports collection as JSON with full provenance |

### 4B. Provenance requirements (non-negotiable)

Every image in your collection MUST have:

```json
{
  "image_id": "img_001",
  "url": "https://unsplash.com/photos/abc123",
  "thumbnail_url": "...",
  "source_database": "Unsplash",
  "source_page_url": "https://unsplash.com/photos/abc123",
  "source_name": "Unsplash",
  "photographer": "Jane Doe",
  "license": "Unsplash License",
  "license_url": "https://unsplash.com/license",
  "space_type": "living_room",
  "collected_at": "2026-05-01T12:00:00Z",
  "collected_by": "student_name"
}
```

For images uploaded from local files (not from search), the student must manually fill in:
- `source_page_url` — where did you find this image?
- `source_name` — what publication/site was it from?
- `license` — what license applies?

**If you cannot determine the source or license of an image, do not add it to the collection.**

### 4C. Write your tests

- [ ] Search returns results from at least 2 databases
- [ ] Accept button adds image to collection JSON
- [ ] Reject button marks image as rejected (not in collection)
- [ ] File upload accepts .jpg, .png, .webp
- [ ] Provenance fields are required (form won't submit without them)
- [ ] Collection counter updates in real time
- [ ] Export produces valid JSON with all required provenance fields
- [ ] Data persists after page refresh (localStorage or JSON file)

**Deliverable:** `ka_image_collection.html` (or equivalent)

---

## Phase 5: Collect 500 Images

### 5A. Collection strategy

Your 500 images should cover your taxonomy. Aim for:
- At least 15 of your 20+ space types represented
- At least 10 images per space type (for the top 10 types)
- A mix of databases (not all from one source)
- Full provenance on every image

### 5B. Collection report

| Metric | Your Count |
|---|---|
| Total images collected | /500 |
| Space types represented | /20+ |
| Databases used | |
| Images with full provenance | /500 |
| Images from search pipeline | |
| Images from manual upload | |

### 5C. Spot-check provenance

Pick 10 random images from your collection. For each:
1. Open the `source_page_url` — does the page exist?
2. Does the license match what you recorded?
3. Is the photographer name correct?

Report any discrepancies.

---

## What You Submit

| Item | What it is |
|---|---|
| **Space-type taxonomy** | `space_type_taxonomy.json` — 20+ types mapped to registry tags |
| **Database list** | `image_databases.json` — curated, tested database entries |
| **Search pipeline** | `search_pipeline.py` — automated image search script |
| **Search results** | `search_results.json` — raw results from all searches |
| **Collection dashboard** | `ka_image_collection.html` — working interactive page |
| **Image collection** | `collection.json` — 500 images with full provenance |
| **Collection report** | Summary table with counts per space type + database |
| **Provenance spot-check** | 10 images verified against their source URLs |
| **Contracts** | Your written contracts for each phase (in markdown or docstrings) |
| **Test checklists** | Your test checklists with pass/fail results |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + success conditions + tests** | 20 | Written BEFORE building; specific, not vague (CONTRACT GATE) |
| **Taxonomy** | 10 | ≥ 20 space types, maps to registry tags, covers domains |
| **Database curation** | 10 | ≥ 5 tested, APIs verified, licenses documented |
| **Search pipeline** | 10 | Automated, respects licenses, tracks provenance |
| **Collection dashboard** | 10 | Search + browse + upload + provenance fields + export |
| **500 images with provenance** | 10 | Full provenance, ≥ 15 space types, source diversity |
| **Verification questions** | 5 | Caught problems in AI's implementation |

> ⛔ **Contract gate**: If your contracts, success conditions, and tests are insufficient, your submission will be flagged as *not ready for integration* regardless of other scores. See Track 2 for examples of adequate contracts.

---

## A Note About Reuse

The space-type taxonomy, database list, and search pipeline you build here become infrastructure for the rest of Track 1. In Task 2 (tagging), you'll tag images from this collection. In Task 3 (inter-rater), you'll run agreement tests on these images. In Task 4 (classifier), you'll train on them. **Build it right now so you don't have to rebuild it later.**

---

## Existing Code You Should Know About

| File | What it provides |
|---|---|
| `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json` | The 424-tag registry with domains, definitions, and extractability |
| `Tagging_Contractor/Tagging_Contractor_What_it_is_and_How_to_use_it.md` | How the tagging system works |
| `Tagging_Contractor/contracts/localized_image_tags.schema.json` | JSON schema for tagged image output |
| `Outcome_Contractor/README.md` | Human-side outcome vocabulary |
| `image-tagger/docs/CONTRACT.md` | Image Tagger API contract (upload, explore, workbench) |
| `./bin/tc audit-tags` | Audit tool for tag completeness |
| `./bin/tc audit-semantics` | Semantics completeness gate |
