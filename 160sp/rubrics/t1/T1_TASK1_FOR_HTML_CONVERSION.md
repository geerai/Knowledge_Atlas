# Prompt for Claude: Convert this assignment to a polished HTML page

Convert the assignment below into a single, self-contained HTML file. Design requirements:

1. **Style**: Dark theme, professional academic look. Use CSS variables for colors. Sans-serif font (Inter or system-ui). Subtle gradients on headers. Good spacing and readability.
2. **Layout**: Max-width 900px centered container. Sticky table of contents sidebar on desktop, collapsible on mobile. Responsive.
3. **Tables**: Styled with alternating row colors, rounded corners, hover effects.
4. **Code blocks**: Syntax-highlighted JSON examples with dark background and monospace font. Copy-to-clipboard button on each code block.
5. **Checklists**: Render `- [ ]` as interactive checkboxes that persist in localStorage.
6. **Callouts**: Render blockquotes starting with "Contract objective" as styled callout cards with a left accent border. Render ⛔ warnings as red-bordered alert boxes.
7. **Progress tracker**: Add a visual progress bar at the top that updates based on checked checkboxes.
8. **Collapsible sections**: Make each Phase collapsible (click to expand/collapse) with smooth animation. All expanded by default.
9. **Print-friendly**: Include a print stylesheet that removes the sidebar and expands all sections.
10. **No external dependencies**: Everything inline — CSS, JS, fonts (use system fonts if needed).

---

# Track 1 · Task 1: Build an Image Collection

**Track:** Image Tagger  
**Points:** 75  
**What you'll have when you're done:** 500 openly-licensed photographs of architectural interiors, organized by room type, with every image traceable to the web page you found it on.

---

## The big picture

The Knowledge Atlas studies how buildings affect people — how ceiling height changes your thinking, how daylight shifts your mood, how clutter raises your stress. To study these things computationally, we need thousands of photographs of real interior spaces. Your job is to collect 500 of them.

But "collect" doesn't mean "drag images off Google." Every image must:

1. **Be openly licensed** — Creative Commons, public domain, or equivalent. No copyright violations.
2. **Have provenance** — For every image you know: where you found it, who took it, and what license it carries.
3. **Be categorized** — You know what kind of room it shows.

You'll build the tools to do this efficiently, then use those tools to collect your 500.

---

## The 15 room types

We need images across a range of interior spaces. Use these 15 categories:

| # | Room Type | What to search for | Why we need it |
|---|---|---|---|
| 1 | `living_room` | living room, lounge, sitting room | Furniture layout, daylight, biophilia, color warmth |
| 2 | `bedroom` | bedroom, sleeping quarters | Lighting warmth, enclosure, materials, tranquility |
| 3 | `kitchen` | kitchen, cooking area | Component detection (cabinets, counters), materials, layout |
| 4 | `bathroom` | bathroom, restroom, washroom | Materials (tile, glass), fixtures, spatial geometry |
| 5 | `office` | office interior, workspace, workstation | Task lighting, spatial openness, visual complexity |
| 6 | `classroom` | classroom, lecture hall, seminar room | Social-spatial layout, lighting, legibility |
| 7 | `hospital` | hospital room, clinic interior, patient room | Safety, materials, lighting, wayfinding |
| 8 | `restaurant` | restaurant interior, café, dining room | Social density, lighting ambiance, material warmth |
| 9 | `lobby` | hotel lobby, building lobby, atrium | Spatial volume, ceiling height, prospect-refuge |
| 10 | `corridor` | hallway, corridor, passage | Spatial geometry, wayfinding, enclosure ratio |
| 11 | `library` | library interior, reading room | Cognitive restoration, natural light, visual order |
| 12 | `retail` | retail store, shop interior, showroom | Color, lighting, visual complexity, layout |
| 13 | `museum` | museum gallery, exhibition space | Spatial volume, lighting, visual complexity |
| 14 | `worship` | church interior, temple, mosque | Ceiling height, geometry, fractal patterns, affect |
| 15 | `gym` | gym, fitness center, sports hall | Spatial openness, materials, lighting intensity |

You may add up to 5 more categories if you find important gaps. But these 15 are your minimum.

Save this as `space_types.json` in your repo. Format:

```json
{
  "living_room": {
    "search_terms": ["living room interior", "lounge interior", "sitting room"],
    "why": "Furniture layout, daylight, biophilia, color warmth"
  },
  "bedroom": {
    "search_terms": ["bedroom interior", "sleeping quarters"],
    "why": "Lighting warmth, enclosure, materials, tranquility"
  }
}
```

---

## Phase 1: Find your image sources

You need to find at least **5 websites or databases** where you can get openly-licensed architectural photographs. Some have free APIs. Some you'll browse manually. All must have clear licensing.

### What "openly licensed" means

| License | OK to use? | Attribution needed? |
|---|---|---|
| CC0 (Public Domain) | ✅ Yes | No |
| CC-BY | ✅ Yes | Yes — credit the photographer |
| CC-BY-SA | ✅ Yes | Yes — credit and share alike |
| Unsplash License | ✅ Yes | Attribution appreciated, not required |
| Pexels License | ✅ Yes | No attribution required |
| CC-NC (Non-Commercial) | ⚠️ Check | OK for academic research, not commercial |
| All Rights Reserved / © | ❌ No | Cannot use |

### Starting points (you must find more)

- **Unsplash** (unsplash.com) — High-quality, free API, good architectural content
- **Pexels** (pexels.com) — Free API, no attribution needed
- **Flickr** (flickr.com) — API with CC license filtering, large architecture groups
- **Wikimedia Commons** (commons.wikimedia.org) — CC/public domain, building interiors
- **Pixabay** (pixabay.com) — Free, CC0-equivalent license

### Your deliverable: `image_sources.json`

> **Contract objective:** "I want a tested, documented list of image sources I can use to collect 500 interior photos."
> **Contract is with:** Public image APIs and websites.
> **Prompt hint:** *"I need to find 5+ sources of openly-licensed architectural interior photos. For each: does it have an API? What license? How do I search it? Test one query and tell me how many results."*

Write YOUR OWN contract for this phase. Include Inputs, Processing, Outputs, and Success Conditions.

**Success conditions (minimum):**

- [ ] At least 5 sources documented
- [ ] Each source has: name, URL, license type, API availability (yes/no)
- [ ] At least 3 sources tested with a sample query
- [ ] Each tested source shows how many results the sample query returned

```json
{
  "sources": [
    {
      "name": "Unsplash",
      "url": "https://unsplash.com",
      "api_url": "https://api.unsplash.com/",
      "has_api": true,
      "license": "Unsplash License (free, attribution appreciated)",
      "rate_limit": "50 requests/hour (free tier)",
      "tested": true,
      "test_query": "modern living room interior",
      "test_results": 1247
    }
  ]
}
```

---

## Phase 2: Build the search pipeline

Now automate it. Write a Python script that takes a room type and a source, runs the search, and saves the results.

> **Contract objective:** "I want a script that searches my image sources for photos of each room type and saves the results as JSON."
> **Contract is with:** Your image source APIs and `space_types.json`.
> **Prompt hint:** *"Build a Python script that reads space_types.json, loops through each room type, queries the Unsplash/Pexels/Flickr API for that room type's search terms, and saves results as JSON. Each result must include: image URL, thumbnail URL, photographer name, source name, source page URL, and license."*

Write YOUR OWN contract. Then write your tests BEFORE building:

- [ ] API keys are in environment variables, not hardcoded
- [ ] Rate limits are respected (check for `time.sleep`)
- [ ] Every image result has: `url`, `source_name`, `source_page_url`, `license`
- [ ] Output JSON is valid
- [ ] Zero-result searches are logged, not silently skipped

### What each image record must look like

```json
{
  "url": "https://images.unsplash.com/photo-abc123",
  "thumbnail_url": "https://images.unsplash.com/photo-abc123?w=400",
  "title": "Modern minimalist living room",
  "photographer": "Jane Doe",
  "source_name": "Unsplash",
  "source_page_url": "https://unsplash.com/photos/abc123",
  "license": "Unsplash License",
  "space_type": "living_room",
  "search_query": "modern living room interior",
  "collected_at": "2026-05-01T12:00:00Z"
}
```

**Deliverable:** `search_pipeline.py` + `search_results.json`

---

## Phase 3: Build the collection page

Build a web page where you can browse search results, accept or reject images, upload local files, and track your progress toward 500.

> **Contract objective:** "I want an interactive page where I can manage my image collection — search, browse, accept/reject, upload, and export."
> **Contract is with:** Your search results and the Image Tagger upload API.
> **Prompt hint:** *"Build an HTML page with these features: (1) a search bar that loads results from search_results.json, (2) a thumbnail grid with accept/reject buttons, (3) a file upload zone for drag-and-drop, (4) provenance fields that are required before accepting, (5) a progress counter showing N/500, (6) an export button that downloads the collection as JSON."*

### Required features

| Feature | What it does |
|---|---|
| **Search / filter** | Filter images by room type or keyword |
| **Thumbnail grid** | Shows images with title, source, license |
| **Accept / Reject** | Accept into collection or reject |
| **Upload** | Drag-and-drop for local files or folders |
| **Provenance fields** | Source URL and source name — required before accepting |
| **Progress counter** | Shows how many images you've collected out of 500 |
| **Export** | Downloads `collection.json` with all provenance |

### Provenance is non-negotiable

Every image in your collection must have these fields filled in:

| Field | Required? | Auto-filled from search? |
|---|---|---|
| `source_page_url` | ✅ Yes | Yes (from API) |
| `source_name` | ✅ Yes | Yes (from API) |
| `photographer` | Best effort | Usually (from API) |
| `license` | ✅ Yes | Yes (from API) |
| `space_type` | ✅ Yes | Yes (from search) |

For **manually uploaded** images (not from search), the student must type in the source URL and source name. If you don't know where an image came from, **don't add it**.

Write YOUR OWN contract and tests for this phase.

**Deliverable:** `ka_image_collection.html`

---

## Phase 4: Collect 500 images

Use your pipeline and collection page to gather 500 images.

### Distribution targets

| Requirement | Target |
|---|---|
| Total images | 500 |
| Room types covered | ≥ 12 of the 15 |
| Images per top-10 room type | ≥ 15 each |
| Sources used | ≥ 3 different databases |
| Images with full provenance | 500 / 500 |

### Spot-check your provenance

Pick **10 random images** from your collection. For each one:

1. Open the `source_page_url` in a browser. Does the page exist?
2. Does the license on the page match what you recorded?
3. Is the photographer credit correct?

Record what you find. Discrepancies happen — the point is that you checked.

### Collection report

Fill in this table:

| Metric | Your count |
|---|---|
| Total images | /500 |
| Room types represented | /15 |
| Images from search pipeline | |
| Images from manual upload | |
| Sources used | |
| Provenance spot-check: pages exist | /10 |
| Provenance spot-check: license matches | /10 |

**Deliverables:** `collection.json` + collection report (in your submission)

---

## What you submit

| Item | Filename |
|---|---|
| Space types | `space_types.json` |
| Image sources | `image_sources.json` |
| Search pipeline | `search_pipeline.py` |
| Search results | `search_results.json` |
| Collection page | `ka_image_collection.html` |
| Image collection | `collection.json` (500 images with provenance) |
| Collection report | Table above, filled in |
| Contracts + tests | Your written contracts and test checklists |
| File manifest | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 20 | Written BEFORE building. Specific, not vague. **(CONTRACT GATE)** |
| **Image sources** | 10 | ≥ 5 sources, ≥ 3 tested, licenses documented |
| **Search pipeline** | 10 | Automated, respects rate limits, tracks provenance |
| **Collection page** | 15 | Search + browse + upload + provenance + export |
| **500 images** | 15 | Full provenance, ≥ 12 room types, ≥ 3 sources |
| **Verification** | 5 | Spot-checked provenance, caught AI implementation issues |

> ⛔ **Contract gate**: If your contracts and tests are missing or vague ("it works"), your submission will be flagged and your images will not be integrated into the Atlas. Write real contracts with real success conditions.

---

## Reuse

Your image sources, search pipeline, and collection page are infrastructure. In Task 2, you'll tag these images. In Task 3, you'll run inter-rater agreement on them. In Task 4, you'll train a classifier on them. Build it right the first time.

---

## Existing code you should know about

| Repo / File | What it gives you |
|---|---|
| `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json` | 424 tags organized by domain — tells you what features matter in each room type |
| `Tagging_Contractor/Tagging_Contractor_What_it_is_and_How_to_use_it.md` | How the tagging system works |
| `image-tagger/docs/CONTRACT.md` | Image Tagger API — the upload endpoint your images will eventually go into |
| `Outcome_Contractor/README.md` | The human-side vocabulary (cognitive, affective effects) — context for why we need these images |
