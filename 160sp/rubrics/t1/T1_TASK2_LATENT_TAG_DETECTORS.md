# Track 1 · Task 2: Build Latent Tag Detectors

**Track:** Image Tagger  
**Prerequisite:** Task 1 (you need your 500 images with provenance)  
**Points:** 75  
**What you'll have when you're done:** Working Python detectors for 6 latent environmental tags, each backed by a design note, a typed contract, and a test suite that runs against a gold-set of labeled images.

---

## The big picture

In Task 1, you collected 500 architectural interior photographs with provenance. Now you need to *tag* them — not with simple labels like "living room" or "bedroom," but with latent environmental features that affect human cognition and behavior.

### What the instructor already did (Sprint 1)

Before this course began, the instructor completed Sprint 1: integrating 58 latent variables (L01–L58) from the Environment–Cognition Taxonomy V2.6 into the Tagging Contractor registry. This means:

- Every latent tag (like L44 Sociopetal Seating, L17 Prospect, L42 Interactional Visibility) **already exists in the registry** with a full semantic contract
- Each entry has a `definition_long` explaining what the tag means in human terms
- Each entry has a `method_family` specifying *how* to detect it from an image
- Each entry has `extractability` flags telling you whether it can be detected from 2D photos

You can read these entries yourself:
```bash
python3 -c "
import json
r = json.load(open('Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json'))
tags = r['tags']
# Look at one latent tag
for tid, t in tags.items():
    if 'sociopetal' in t.get('canonical_name','').lower() or 'L44' in tid:
        print(json.dumps(t, indent=2))
        break
"
```

**The registry is your source of truth.** Your detectors must match the registry's vocabulary. If your detector drifts from the `definition_long`, the semantic audit gate will catch it.

### What you bring from Task 1

- Your **500 images** organized by room type, with provenance
- Your **`space_types.json`** taxonomy
- Your **collection page** for browsing and managing images

### What the tagger provides (intermediate representations)

For a gold-set of images, the tagger has already computed:
- **COCO-133 segmentation masks** (people, furniture, objects)
- **Monocular depth maps** (estimated distance per pixel)
- **Skeletonized floor masks** (circulation paths extracted from floor regions)
- **Basic VLM/CLIP tag predictions** (simple visual features already detected)

Your job is to write detectors that compute *on top of* these intermediate representations. You are NOT training neural networks. You are writing geometric and logical predicates — computational geometry, not deep learning.

---

## The 18 latent tags, grouped by detection method

Each tag belongs to one of three families based on what geometric computation it requires:

### Family A: Furniture Geometry (object detection + spatial arrangement)

These tags are recoverable from pairwise angles, distances, and cluster counts over the COCO-133 segment masks already produced by the tagger. The classical F-formation geometry (Kendon, 1990; Marquardt et al., 2012) gives the predicate set.

| Tag ID | Tag Name | What it measures |
|---|---|---|
| L44 | Sociopetal Seating | Are seats arranged facing each other (conversation-promoting)? |
| L48 | Dyadic Intimacy | Is there a pair of seats at intimate distance (< 1.2m)? |
| L49 | Small-Group Support | Does the seating arrangement support 3-5 person groups? |
| L53 | Shared Attention Anchor | Is there a focal point (screen, fireplace, window) that the seating faces? |

### Family B: Sightlines & Isovists (depth map + spatial analysis)

These tags are recoverable from isovist area, maximum viewshed depth, and partition-height ratios computed over the monocular depth map (Benedikt, 1979; Wiener et al., 2007).

| Tag ID | Tag Name | What it measures |
|---|---|---|
| L42 | Interactional Visibility | Can occupants see each other across the space? |
| L54 | Boundary Permeability | How open vs. enclosed are the spatial boundaries? |
| L17 | Prospect | Does the space offer long views (high prospect)? |

### Family C: Circulation & Apertures (floor plan skeleton + graph analysis)

These tags reduce to path counts, aperture widths, and dead-end detection over a skeletonized floor mask (Hillier & Hanson, 1984).

| Tag ID | Tag Name | What it measures |
|---|---|---|
| L41 | Chance-Encounter Potential | Does the layout create intersections where people meet by accident? |
| L47 | Turn-Taking Support | Do circulation paths support natural conversational turn-taking? |
| L57 | Disengagement Ease | Can a person leave a social situation without disrupting it? |

---

## Your assignment: implement 6 detectors

Each student team picks **6 tags** — at least 2 from each family. For each tag, you follow a 7-step scaffold.

---

## The 7-Step Scaffold

### Step 1: Panel — Write a detector design note

For each of your 6 tags, write a one-page **detector design note** that identifies:

**(a)** The upstream tags the detector consumes (what intermediate representations does it need — depth map? segmentation mask? skeleton?)

**(b)** The geometric or logical predicate that encodes the latent tag (e.g., "Sociopetal Seating = TRUE if ≥ 3 detected seating objects have pairwise facing angles < 45° and centroid distances < 2.5m in the depth-projected coordinate frame")

**(c)** The failure modes you expect (e.g., "Monocular depth is unreliable beyond 5m, so L17 Prospect may underestimate viewshed depth in large atriums")

> **Contract objective:** "I want a one-page design note for detector L__ that states what inputs it consumes, what geometric predicate it computes, and where it will fail."
> **Contract is with:** The Tagging Contractor registry (for the tag's `definition_long` and `method_family`) and the tagger's existing intermediate representations.
> **Prompt hint:** *"Read the registry entry for tag L__ in `registry_v0.2.8.json`. What does `definition_long` say? What does `method_family` say? Now design a detector: what intermediate data do I need, what geometric computation do I run, and what score do I output?"*

**Panel review:** Before moving to Step 2, critique your teammates' design notes. Does the predicate actually encode what the tag means? Are the failure modes realistic?

### Step 2: Spec — Convert to a typed function signature

Convert the design note into a **typed function signature and docstring** written in the same vocabulary as the registry's `definition_long`. The docstring IS the contract — if it drifts from the registry, the semantic gate will catch it.

```python
def detect_sociopetal_seating(
    segmentation_mask: np.ndarray,
    depth_map: np.ndarray,
    detected_objects: list[DetectedObject],
) -> TagResult:
    """Detect sociopetal seating arrangement (L44).
    
    Computes pairwise facing angles between detected seating objects
    using F-formation geometry (Kendon, 1990). Returns score > 0.5
    when >= 3 seating objects have pairwise facing angles < 45 degrees
    and centroid distances < 2.5m in the depth-projected coordinate frame.
    
    Inputs:
        segmentation_mask: COCO-133 segmentation output (H x W int array)
        depth_map: Monocular depth estimate (H x W float array, meters)
        detected_objects: List of detected objects with class, bbox, confidence
    
    Returns:
        TagResult with score (0-1), confidence, and evidence dict
    
    Failure modes:
        - Depth unreliable > 5m: facing angle estimation degrades
        - Occluded furniture: segmentation misses partially visible seats
    """
```

> **Contract objective:** "I want a typed function signature for detector L__ that matches the registry vocabulary."
> **Contract is with:** The registry's `definition_long` field.

### Step 3: Tests — Write pytest cases BEFORE implementing

Write test cases against the Sprint 1 gold-set images. **Minimum:**
- 6 passing positives (images where the tag IS present, confirmed by human labeling)
- 4 passing negatives (images where the tag is NOT present)
- Regression fixtures for every edge case the panel surfaced in Step 1

```python
def test_sociopetal_seating_positive_living_room():
    """Living room with U-shaped sofa arrangement should score > 0.5."""
    result = detect_sociopetal_seating(
        segmentation_mask=load_gold("img_042_seg.npy"),
        depth_map=load_gold("img_042_depth.npy"),
        detected_objects=load_gold("img_042_objects.json"),
    )
    assert result.score > 0.5
    assert result.confidence > 0.3

def test_sociopetal_seating_negative_corridor():
    """Empty corridor with no seating should score < 0.2."""
    result = detect_sociopetal_seating(...)
    assert result.score < 0.2
```

> **Write your tests BEFORE writing the detector.** This is test-driven development. The tests define what "correct" means.

### Step 4: Build — Implement the detector

Now implement the detector function. Rules:

- **Keep each detector under 150 lines.** If it grows beyond that, the predicate is probably wrong.
- **Use existing intermediate representations.** Don't recompute segmentation or depth — consume what the tagger already produces.
- **Make the computation transparent.** The detector should be diagnosable by reading the code, not by probing a neural network.
- **Commit to `track1/extractors/L__-your-team/`.**

Most detectors in Families A-C reduce to one of three computations over the tagger's existing intermediate representations:
- **Family A (Furniture Geometry):** Pairwise operations over COCO-133 bounding boxes + depth-projected coordinates
- **Family B (Sightlines):** Isovist computation over the monocular depth map
- **Family C (Circulation):** Graph analysis (path counting, dead-end detection) over the skeletonized floor mask

### Step 5: Validate — Run your tests

```bash
pytest track1/extractors/L44-your-team/test_L44.py -v
```

All 10 tests (6 positive + 4 negative) must pass. If they don't, either:
- Your detector has a bug (fix the code)
- Your test has a bad gold label (verify the image manually)
- The intermediate representation is poor quality (document this as a known limitation)

### Step 6: Audit — Run the semantic gate

The Tagging Contractor has an audit tool that checks whether your detector's output vocabulary matches the registry:

```bash
./bin/tc audit-semantics --extractor track1/extractors/L44-your-team/
```

If the audit fails, your docstring or output format has drifted from the registry. Fix it.

### Step 7: Document — Write the detector card

For each detector, write a short card:

| Field | Content |
|---|---|
| **Tag ID** | L44 |
| **Tag Name** | Sociopetal Seating |
| **Family** | A (Furniture Geometry) |
| **Inputs consumed** | COCO-133 segmentation, monocular depth |
| **Predicate** | ≥ 3 seating objects with pairwise facing angles < 45° and centroids < 2.5m |
| **Score range** | 0.0 - 1.0 |
| **Known failure modes** | Depth unreliable > 5m; occluded furniture |
| **Test results** | 6/6 positive, 4/4 negative |
| **Audit status** | PASS |

---

## What you submit

| Item | What it is |
|---|---|
| **6 design notes** (Step 1) | One page each, with inputs, predicate, failure modes |
| **6 typed function signatures** (Step 2) | With docstrings matching registry vocabulary |
| **6 test suites** (Step 3) | ≥ 10 tests each (6 positive + 4 negative) |
| **6 detector implementations** (Step 4) | Under 150 lines each |
| **Test results** (Step 5) | pytest output showing all tests pass |
| **Audit results** (Step 6) | `tc audit-semantics` output for each detector |
| **6 detector cards** (Step 7) | Summary table per detector |
| **Contracts** | Your written contracts for each phase |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + design notes** | 15 | Written BEFORE building. Predicates are specific. **(CONTRACT GATE)** |
| **Test suites** | 15 | Written BEFORE detectors. ≥ 10 tests per detector. |
| **Detector implementations** | 20 | Correct, under 150 lines, uses existing intermediates |
| **Audit pass** | 10 | `tc audit-semantics` passes for all 6 detectors |
| **Detector cards** | 5 | Complete, accurate, failure modes documented |
| **Verification** | 10 | Caught problems in AI's implementation, documented fixes |

> ⛔ **Contract gate**: If your design notes and contracts are missing or vague, your detectors will be flagged and will not be integrated into the tagger. Write real predicates with real failure modes.

---

## Key references

| Reference | What it provides |
|---|---|
| Kendon, A. (1990). *Conducting Interaction.* | F-formation geometry for seating arrangement analysis |
| Marquardt, N. et al. (2012). | Computational F-formation detection from spatial data |
| Benedikt, M.L. (1979). "To Take Hold of Space: Isovists and Isovist Fields." | Isovist theory for visibility analysis |
| Wiener, J.M. et al. (2007). | Isovist-based spatial cognition metrics |
| Hillier, B. & Hanson, J. (1984). *The Social Logic of Space.* | Space syntax for circulation and encounter analysis |

---

## Existing code you should know about

| Repo / File | What it gives you |
|---|---|
| `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json` | 424 tags with `definition_long`, `method_family`, and `extractability` |
| `Tagging_Contractor/contracts/localized_image_tags.schema.json` | JSON schema for tagged image output |
| `./bin/tc audit-semantics` | Checks detector output vocabulary against registry |
| `./bin/tc audit-tags` | Checks tag completeness |
| `image-tagger/docs/CONTRACT.md` | Image Tagger API contract (upload, explore, workbench) |
| Sprint 1 gold-set | Pre-computed segmentation masks, depth maps, skeletons for labeled images |

---

## Reuse

Your detectors become part of the Image Tagger's science pipeline. In Task 3, your teammates will run inter-rater agreement on the tags your detectors produce. In Task 4, you'll evaluate detector accuracy against human judgments. Build them right — they're infrastructure.
