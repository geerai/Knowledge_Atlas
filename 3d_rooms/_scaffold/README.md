# `3d_rooms/_scaffold/` — copy this for every new room

This directory is the **starter kit for one room**. When you author your assigned room (Task 1, Phase 3), copy this folder, rename it to your room type (e.g., `3d_rooms/library/`), and fill in the TODOs.

## What's here

| File | Purpose |
|---|---|
| `manifest_template.json` | JSON-Schema parameter manifest skeleton with TODOs and one worked example parameter (ceiling height with Vartanian-2015 citation). |
| `viewer_starter.html` | A working `<model-viewer>` page with three parameter sliders bound to JSON. Adapt the controls to your manifest. |
| `README.md` | This file. |

## Workflow

1. **Copy:** `cp -r 3d_rooms/_scaffold 3d_rooms/<your_room_type>` (e.g. `library`, `museum`, `gym`)
2. **Fill manifest:** edit `manifest_template.json` → rename to `<your_room_type>.schema.json`. Replace every TODO. Cite at least one published environmental-psychology study per parameter (per the t3_task1 page Phase 3).
3. **Default params file:** create `<your_room_type>_default.json` with the manifest's defaults.
4. **Smoke render:** `python3 scripts/track3/infinigen_wrapper.py --room <your_room_type> --manifest 3d_rooms/<your_room_type>/<your_room_type>.schema.json --params 3d_rooms/<your_room_type>/<your_room_type>_default.json --out 3d_rooms/<your_room_type>/renders/default.gltf`
5. **Adapt the viewer:** edit `viewer_starter.html` so the sliders correspond to your manifest's parameters. Save as `viewer.html`.
6. **Sweep gallery (Task 2):** generate one render per parameter at low/mid/high. The infinigen_wrapper accepts a directory of params files.

## What you do NOT need to write yourself

The course supplies these as ready-to-use scaffolds:

- `scripts/track3/setup_track3.sh` — installs Blender + Infinigen + venv, runs a smoke test
- `scripts/track3/infinigen_wrapper.py` — JSON params → Infinigen → glTF (the central artifact)
- `scripts/track3/extract_infinigen_params.py` — introspects an Infinigen room class → emits a draft manifest you can adapt
- `scripts/track3/validation_gate.py` — JSON-Schema patch validation (used by Task 3 LLM front-end)
- `scripts/track3/llm_wrapper_starter.py` — function-calling LLM adapter with system prompt (Task 3)
- `3d_rooms/_presets/` — three starter literature-grounded presets you can extend

## A note on the `_panel_required_fields`

Every manifest must declare the four panel-mandated fields from Sprint 1 + 2:

- `interaction_mode`: focused / unfocused / mixed (Goffman)
- `valence_polarity`: positive / negative / neutral / mixed (Russell)
- `temporal_window`: snapshot / short_period / sustained / longitudinal (Sprint 2 panel)
- `cross_cultural_variance`: low / medium / high (Hall)

The ratified per-room defaults are in `docs/sprint2_panel_disposition_2026-04-28.md` §3 in the Tagging_Contractor repo. Follow those defaults unless you have a documented reason to deviate.

## If you're working on the curved-wall worship room

Don't copy this scaffold — go to `3d_rooms/worship_curved/` instead. That's the cohort flagship and has its own sub-component allocation table.
