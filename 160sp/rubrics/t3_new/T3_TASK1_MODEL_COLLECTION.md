# Track 3 · Task 1: Collect & Catalog VR-Ready 3D Interior Models

**Track:** VR Studio  
**Points:** 75  
**What you'll have when you're done:** A curated library of ≥ 20 VR-ready 3D interior models in glTF/GLB format, each evaluated against 8 manipulation classes, cataloged in a Google Sheet with viability scores, and accompanied by a mesh annotation file that maps every mesh to its semantic role (ceiling, wall_north, floor, window, etc.).

---

## The big picture

The Knowledge Atlas stores evidence that specific environmental features alter human cognition and affect. Researchers have manipulated these features experimentally:

| Manipulation Class | Registry tags | What researchers change |
|---|---|---|
| **Geometry** (ceiling height, volume, enclosure) | 46 tags | Ceiling height ≥ 3.0m vs ≤ 2.4m; room proportions; isovist area |
| **Lighting** (intensity, spectrum, direction) | 33 tags | Illuminance (lux); color temperature (2700K–6500K); daylight vs artificial |
| **Materials** (surface texture, roughness) | 13 tags | Wood vs concrete vs glass; natural material ratio; texture density |
| **Color** (hue, warmth, saturation) | 5 tags | Warm vs cool palettes; color diversity; chroma levels |
| **Biophilic elements** (plants, water, nature views) | 6 tags | Plant count; window view content (greenery vs built-up) |
| **Furniture layout** (density, arrangement) | 17 tags | Seating count; sociopetal vs sociofugal arrangement; clutter density |
| **Acoustic properties** | 5 tags | Acoustic privacy; natural sound sources |
| **Visual complexity** (detail, order, fractals) | 22 tags | Fractal dimension; symmetry; ornament density |

To test these relationships in VR, researchers need 3D room models where each factor can be **varied independently while holding others constant**. Your job is to collect models that make this possible.

---

## What makes a model "VR-ready"

Not every 3D model can be parametrically modified. These are hard constraints:

### Constraint 1: Separable Named Meshes

The ceiling must be a **separate mesh** from the walls. Each wall must be individually identifiable. This rules out:
- ❌ Photogrammetry scans (single fused mesh)
- ❌ "Baked" models (one mesh with texture atlas)
- ✅ Architectural models with separate named objects

**Test:** Open in Blender → check the Outliner. Named objects like "Ceiling", "Wall_North", "Floor" = viable. One object called "mesh_001" = not viable.

### Constraint 2: PBR Materials (not baked textures)

Models must use **PBR material slots** (base color, roughness, metalness), not a single pre-baked lightmap. This enables material swapping.

### Constraint 3: Architectural Scale

Models must be at **real-world scale** (meters). Ceiling height manipulation requires knowing the actual height. VR immersion breaks if scale is wrong.

### Constraint 4: VR-Compatible Polygon Count

For WebXR at ≥ 72 fps: < 500K polygons per scene, < 20 unique materials, textures ≤ 4096×4096.

### Constraint 5: Open License

CC0, CC-BY, CC-BY-SA. No "editorial use only" or "All Rights Reserved."

---

## Phase 1: Find model sources

> **Contract objective:** "I want a tested, documented list of 3D model sources I can use to collect VR-ready interior models."
> **Contract is with:** 3D model repositories and their APIs.
> **Prompt hint:** *"I need 5+ sources of openly-licensed architectural interior 3D models in glTF/GLB/FBX/OBJ format. For each: license, API availability, format, and whether models have separable meshes. Test one search per source."*

Write YOUR OWN contract. Include Inputs, Processing, Outputs, Success Conditions.

### Starting points

- **Sketchfab** — CC-licensed, API available, downloadable glTF, many architectural interiors
- **3D Warehouse** — SketchUp models with groups/components, export via Blender
- **BlenderKit** — Free tier, natively separable meshes
- **TurboSquid** (free section) — Check license per model
- **Poly Haven** — CC0, excellent HDRIs and some room models
- **CGTrader** (free section) — Mixed quality, check license

### Advanced source: World Labs Marble (image → 3D world)

[World Labs Marble](https://marble.worldlabs.ai/) uses spatial AI to generate explorable 3D worlds from a single photograph, text prompt, or video. Instead of downloading someone else's model, you photograph a real space and generate a 3D version. This is directly relevant to neuroarchitecture research — [Champalimaud Foundation and King's College London already use Marble to generate patient-specific VR environments for OCD exposure therapy](https://www.worldlabs.ai/case-studies/3-health-systems).

#### Step 1: Generate a world

**Option A — Web UI (easiest to start):**
Go to [marble.worldlabs.ai](https://marble.worldlabs.ai/) → click Create → upload a photo of an interior or type a text prompt → wait ~5 minutes.

**Option B — API (automatable, required for batch processing):**

```bash
# Generate a world from a text prompt
curl -X POST 'https://api.worldlabs.ai/marble/v1/worlds:generate' \
  -H 'Content-Type: application/json' \
  -H 'WLT-Api-Key: YOUR_API_KEY' \
  -d '{
    "display_name": "Clinical Office Baseline",
    "model": "marble-1.1",
    "world_prompt": {
      "type": "text",
      "text_prompt": "A clinical white office with 3m ceilings, fluorescent lighting, one window on the south wall, a desk and two chairs"
    }
  }'

# Generate a world from a photograph
curl -X POST 'https://api.worldlabs.ai/marble/v1/worlds:generate' \
  -H 'Content-Type: application/json' \
  -H 'WLT-Api-Key: YOUR_API_KEY' \
  -d '{
    "display_name": "Psychology Lab Room 204",
    "model": "marble-1.1",
    "world_prompt": {
      "type": "image",
      "image_prompt": {
        "source": "uri",
        "uri": "https://your-host.com/photo_of_room_204.jpg"
      },
      "text_prompt": "Interior of a university research lab"
    }
  }'

# Poll for completion (~5 min)
curl -X GET 'https://api.worldlabs.ai/marble/v1/operations/OPERATION_ID' \
  -H 'WLT-Api-Key: YOUR_API_KEY'
```

**Generation times:** Text/image → pano: ~30 sec. Pano → full world: ~5 min. High-quality mesh export: ~1 hour.

#### Step 2: Export the mesh

In the Marble web viewer, click Export → **High-quality mesh (GLB)**. This runs server-side for ~1 hour and produces:
- A **600K triangle mesh** with texture maps
- A **1M triangle mesh** with vertex colors
- Both in GLB format (loadable in Blender and Three.js)

> **Important:** The exported mesh is a **single fused object** — all walls, ceiling, floor are one continuous surface. You cannot select individual walls yet. That's what Step 3 fixes.

#### Step 3: Segment in Blender (AI-assisted)

The fused mesh must be separated into discrete architectural elements (ceiling, walls, floor, furniture). There are three approaches, from manual to AI-assisted:

**Approach A — Manual segmentation (~30 min per model):**
1. Import GLB: `File → Import → glTF 2.0`
2. Enter Edit Mode (`Tab`)
3. Select ceiling faces: `Select → Select All by Trait → Normal` (faces pointing downward)
4. Separate: `Mesh → Separate → Selection` (`P`)
5. Name the new object "Ceiling" in the Outliner
6. Repeat for floor (upward normals), each wall (by face orientation), furniture
7. Assign PBR materials to each separated object
8. Export: `File → Export → glTF 2.0` with "Selected Objects" checked

**Approach B — AI-assisted via BlenderGPT (~10 min per model):**

[BlenderGPT](https://github.com/gd3kr/BlenderGPT) (4.9k stars, MIT license) is a Blender addon that lets you control Blender with natural language via GPT-4. Install it, then:

```
Prompt: "Select all faces on the imported mesh that face downward 
(normal Z < -0.8). Separate them into a new object called 'Ceiling'. 
Then select all faces facing upward (normal Z > 0.8) and separate them 
into a new object called 'Floor'."
```

```
Prompt: "For the remaining mesh, select all faces facing in the -Y 
direction (normal Y < -0.7) and separate them into 'Wall_North'. 
Repeat for +Y as 'Wall_South', -X as 'Wall_West', +X as 'Wall_East'."
```

```
Prompt: "Assign a new Principled BSDF material to each separated 
object. Set Ceiling to white (0.9, 0.9, 0.9), Floor to gray 
(0.4, 0.4, 0.4), all walls to light beige (0.85, 0.82, 0.75). 
Set roughness to 0.7 for all."
```

**What the LLM actually does:** It generates Blender Python (`bpy`) code and executes it. The LLM doesn't "see" the mesh — it writes selection scripts based on face normals. This works well for architectural geometry (walls are planar) and poorly for organic shapes.

**Approach C — Headless Blender Python script (fully automatable):**

You can write the segmentation logic once and apply it to every Marble export:

```python
# segment_marble_export.py — Run: blender --background --python segment_marble_export.py -- input.glb output.glb
import bpy, bmesh, sys, math

argv = sys.argv[sys.argv.index("--") + 1:]
input_path, output_path = argv[0], argv[1]

# Clear scene, import
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=input_path)
obj = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
bpy.context.view_layer.objects.active = obj

# Enter edit mode
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(obj.data)

# Classify faces by normal direction
def classify_face(face):
    n = face.normal
    if n.z > 0.7: return 'Floor'      # Facing up
    if n.z < -0.7: return 'Ceiling'    # Facing down
    angle = math.atan2(n.y, n.x)       # Horizontal direction
    if -0.785 < angle <= 0.785: return 'Wall_East'
    if 0.785 < angle <= 2.356: return 'Wall_North'
    if angle > 2.356 or angle <= -2.356: return 'Wall_West'
    return 'Wall_South'

# Select and separate each category
for role in ['Ceiling', 'Floor', 'Wall_North', 'Wall_South', 'Wall_East', 'Wall_West']:
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.from_edit_mesh(obj.data)
    for face in bm.faces:
        if classify_face(face) == role:
            face.select = True
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.mesh.separate(type='SELECTED')
    # Rename the newly created object
    new_obj = [o for o in bpy.context.scene.objects if o.name.startswith(obj.name) and o != obj][-1]
    new_obj.name = role

bpy.ops.object.mode_set(mode='OBJECT')

# Assign PBR materials
for obj in bpy.context.scene.objects:
    if obj.type != 'MESH': continue
    mat = bpy.data.materials.new(name=f"PBR_{obj.name}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Roughness'].default_value = 0.7
    obj.data.materials.clear()
    obj.data.materials.append(mat)

# Export
bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
```

Run it: `blender --background --python segment_marble_export.py -- marble_room.glb room_segmented.glb`

This is fully automatable — one command per model, no GUI interaction needed.

#### Marble pricing

| Plan | Worlds/month | Mesh export | Cost |
|---|---|---|---|
| **Free** | 4 | ❌ No export | $0 |
| **Standard** | 12 | ✅ Collider mesh | Check [pricing page](https://marble.worldlabs.ai/pricing) |
| **Pro** | 25 | ✅ High-quality mesh + commercial rights | Check [pricing page](https://marble.worldlabs.ai/pricing) |
| **Max** | 75 | ✅ Everything | Check [pricing page](https://marble.worldlabs.ai/pricing) |
| **API** | Pay-per-use (credits) | ✅ Via API | [API pricing](https://docs.worldlabs.ai/api/pricing) |

For this assignment, the **Free plan** (4 worlds) is enough to try the workflow. The **Standard plan** is enough for 12 Marble-generated rooms. Use Sketchfab for the remaining models.

Use Marble for at least 3 of your 20 models to demonstrate the photo → 3D → parametric pipeline.

**Deliverable:** `model_sources.json`

---

## Phase 2: Collect and evaluate ≥ 20 models

For each model, evaluate it against all 8 manipulation classes. Can you actually change the ceiling? Can you swap the wall material? Can you modify individual walls independently?

### Google Sheet columns (minimum)

| Column | What it records |
|---|---|
| `model_id` | Unique ID (e.g., `SKF_office_001`) |
| `source` / `source_url` | Where you got it |
| `license` | CC0 / CC-BY / CC-BY-SA |
| `room_type` | office / classroom / living_room / etc. |
| `format` | glTF / GLB / FBX (must convert to glTF) |
| `poly_count` | Total polygons |
| `named_meshes` | Yes/No — are architectural elements separate? |
| `pbr_materials` | Yes/No — PBR workflow? |
| `realistic_scale` | Yes/No — meters, not arbitrary? |
| `individual_walls` | Yes/No — can you select and modify each wall independently? |
| `ceiling_modifiable` | Yes/No |
| `lighting_modifiable` | Yes/No — are lights separate objects? |
| `materials_modifiable` | Yes/No |
| `windows_identifiable` | Yes/No — can you find and resize window meshes? |
| `furniture_separable` | Yes/No — is furniture separate from architecture? |
| `viability_score` | 0–8 (count of modifiable classes) |
| `resolution` | Low / Medium / High |
| `naturalness` | 1–5 (visual realism) |
| `notes` | Issues, conversion needed, what's missing |

### Minimum bar

- ≥ 20 models total
- ≥ 10 with viability score ≥ 4
- ≥ 5 different room types
- ≥ 3 different sources

---

## Phase 3: Create mesh annotation files

For each model, create a `mesh_roles.json` that maps every mesh name to its semantic role. This is what the AI front-end (Task 3) will use to know which mesh to modify.

```json
{
  "model_id": "SKF_office_001",
  "meshes": {
    "Cube.003": { "role": "ceiling", "notes": "single plane, height=3.0m" },
    "Cube.004": { "role": "wall", "wall_id": "north", "notes": "back wall" },
    "Cube.005": { "role": "wall", "wall_id": "south", "notes": "front wall with window cutout" },
    "Cube.006": { "role": "wall", "wall_id": "east" },
    "Cube.007": { "role": "wall", "wall_id": "west" },
    "Plane.001": { "role": "floor" },
    "Cube.010": { "role": "window", "parent_wall": "south", "position": "center" },
    "Cube.011": { "role": "furniture", "subtype": "desk" },
    "Cube.012": { "role": "furniture", "subtype": "chair" },
    "Lamp": { "role": "light", "light_type": "point" }
  },
  "room_dimensions": { "width_m": 6.0, "depth_m": 5.0, "height_m": 3.0 }
}
```

> **Each wall must have a `wall_id`** (north/south/east/west or left/right/back/front). This enables per-wall material and geometry changes.

---

## Phase 4: Write a ruthless validation prompt

Before declaring a model "ready," you must test it with a **ruthless prompt** — an adversarial instruction designed to break things.

### What a ruthless prompt is

A ruthless prompt is an AI instruction that systematically probes every failure mode. Instead of "does it work?", you ask "in exactly which ways does it fail?" The structure:

> *"You are a hostile QA engineer. Your job is to find every way this 3D model catalog entry could be wrong, misleading, or unusable. For model {model_id}:*
> 1. *Open the model in Blender. Count the actual meshes and compare to the mesh_roles.json. Are any missing or mislabeled?*
> 2. *Try to move the ceiling mesh up by 1 meter. Does the room still look correct? Do walls gap?*
> 3. *Try to change the north wall material to a different color. Does only that wall change, or do others change too (shared material)?*
> 4. *Check every material — is it PBR or is it a baked texture that can't be swapped?*
> 5. *Measure the room in Blender. Does it match room_dimensions in the JSON?*
> 6. *Is the model oriented correctly (Y-up or Z-up)? Does the 'north' wall actually face north?*
> *Report every discrepancy found."*

Write a ruthless validation prompt for your catalog. Run it on at least 5 models. Document what broke.

---

## What you submit

| Item | What it is |
|---|---|
| `model_sources.json` | ≥ 5 sources, ≥ 3 tested |
| Google Sheet catalog | ≥ 20 models with all columns filled |
| `models/` directory | All glTF/GLB files |
| `mesh_roles/` directory | One `mesh_roles.json` per model |
| Conversion scripts | Any Blender scripts used for format conversion |
| Ruthless validation report | Results of running adversarial prompt on ≥ 5 models |
| Contracts + tests | Written BEFORE building |
| File manifest | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 15 | Written BEFORE collecting. Specific success conditions. **(CONTRACT GATE)** |
| **Model sources** | 10 | ≥ 5 sources, ≥ 3 tested, licenses documented |
| **Model catalog** | 15 | ≥ 20 models, ≥ 10 viable, ≥ 5 room types, viability scores accurate |
| **Mesh annotations** | 15 | Per-wall IDs, roles correct, dimensions measured |
| **Ruthless validation** | 10 | Run on ≥ 5 models, failures documented, fixes applied |
| **Verification** | 10 | Spot-checked claims, caught discrepancies |

> ⛔ **Contract gate**: If your contracts and tests are missing or vague, your models will not be usable by the VR pipeline. Write real contracts with real success conditions.

---

## Existing code you should know about

| Repo / File | What it gives you |
|---|---|
| `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json` | 424 tags — 330 are continuous/ordinal and represent manipulable environmental features |
| `Article_Eater/data/templates/` | 166 PNU templates showing what IVs researchers actually manipulate (ceiling height, lighting, materials, etc.) |
| `Outcome_Contractor/contracts/oc_export/outcome_vocab.json` | 839 effect terms — the dependent variables these manipulations affect |
| `160sp/context/context_vr_production.md` | VR production context including K-ATLAS evidence model and scene specification format |
| [World Labs Marble](https://marble.worldlabs.ai/) | Photo/text → 3D world generation; [API docs](https://docs.worldlabs.ai/api); [SparkJS](https://sparkjs.dev/) for Gaussian Splat rendering |
| [BlenderGPT](https://github.com/gd3kr/BlenderGPT) (4.9k ★) | Natural language → Blender Python code execution; use for AI-assisted mesh segmentation |
| Blender CLI: `blender --background --python script.py` | Run segmentation/conversion scripts headlessly (no GUI); batch-process all models |

---

## Reuse

Your model library and mesh annotations are infrastructure. In Task 2, you'll manually test modifications in A-Frame. In Task 3, you'll build the AI front-end that uses your `mesh_roles.json` files to know which mesh to modify. Accurate annotations now save hours of debugging later.
