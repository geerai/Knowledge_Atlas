# `worship_curved/` — Cohort Flagship Deliverable (Track 3 Task 3, Phase 4)

Single shared parametric module that breaks Infinigen's axis-aligned-box assumption to render curved-wall worship spaces. **Every Track 3 student contributes one sub-component**; the module ships at term end as a citable open-source artefact with all contributors as co-authors.

## Why this is the flagship

Worship is the only one of the fifteen V2.7 room types whose published environmental-psychology effect (Vartanian et al., 2015 cathedral effect; Joye, 2007 biophilic awe; Bermudez et al., 2017 contemplative architecture) is strong enough to motivate breaking out of axis-aligned geometry. A clean parametric implementation of curved-wall sacred space — Bezier wall paths, vault-curve ceilings, fractal patterning — fills a documented gap in the open-source parametric-rooms ecosystem (no equivalent exists in Infinigen Indoors, Holodeck, or HSSD).

## Sub-component allocation

Each Track 3 student picks one and only one sub-component below. Allocation is FCFS via the `OWNERS.md` file in this directory; tell the instructor in Week 4 which sub-component you want.

| File | Owner role | Specification |
|---|---|---|
| `bezier_wall_path.py` | **Geometry lead** | Parametric Bezier curve definition for the floor plan. Output: ordered (x, z) waypoints. Cite Hillier & Hanson (1984) for the convex-map projection. |
| `wall_extrusion.py` | **Geometry second** | Takes Bezier waypoints + ceiling-height-curve + thickness; extrudes wall meshes. Output: triangle mesh + per-vertex normals. |
| `ceiling_height_curve.py` | **Geometry third** | Parametric vault profile (semicircle / gothic-arch / dome) as ceiling height = f(x, z). Cite Vartanian et al. (2015) for the cathedral-effect parameter range. |
| `fractal_pattern.py` | **Surface lead** | Per-wall fractal patterning generator (mid-band fractal dimension D ≈ 1.3–1.5). Cite Joye (2007); Hagerhall et al. (2008). |
| `light_source_position.py` | **Lighting lead** | Window/clerestory/oculus parameter set with positioning constraints. Cite Bermudez et al. (2017) on contemplative-architecture light. |
| `acoustic_estimator.py` | **Honeybee couplant** | OPTIONAL: estimated reverberation from geometry via the Sabine equation. Couples to Ladybug Tools' Honeybee `Room`. |
| `cathedral_preset.py` | **Literature lead** | The named preset reproducing Vartanian et al. (2015). Companion JSON in `_presets/`. |
| `bermudez_preset.py` | **Literature second** | The named preset reproducing Bermudez et al. (2017). Companion JSON in `_presets/`. |
| `cohort_integration.py` | **Integration lead** | Composes all sub-components into the final published module. Owns the module-level test suite, the cohort-shared PR, and the term-end release tag. |

## Sub-component contract template

Each sub-component file follows this contract:

```python
"""<sub_component_name>.py — owned by <student name>.

Responsibility: <one sentence>
Cited literature: <APA citation>
"""
from typing import Any
from dataclasses import dataclass

@dataclass
class <SubComponentName>Params:
    """Typed input parameters; sub-component readers should reference these."""
    # field: type = default

@dataclass
class <SubComponentName>Result:
    """Typed output; downstream sub-components reference these field names."""
    # field: type

def <sub_component_name>(params: <SubComponentName>Params) -> <SubComponentName>Result:
    """Implementation. Pure function preferred; document any side effects."""
    raise NotImplementedError("Sprint 4: <student> implements this")
```

The `cohort_integration.py` file imports each sub-component, wires the typed `Result` of one into the typed `Params` of the next, and produces the final glTF.

## Workflow

1. **Allocation (Week 4):** open `OWNERS.md`, add your name next to the sub-component you want, push to your `track3/your-name` branch, open a PR titled `Allocation: <sub-component> — your name`. The integration lead merges allocations into `flagship/worship_curved`.

2. **Contract finalisation (Week 5):** with your owner role assigned, agree on the typed signatures with the upstream and downstream sub-component owners. Update the `<SubComponentName>Params` and `<SubComponentName>Result` dataclasses; commit and push. The integration lead reviews for typed compatibility.

3. **Implementation (Weeks 6–8):** implement your sub-component with at least one unit test in `tests/`. Cite at least two pieces of published environmental-psychology literature in the docstring.

4. **Integration (Week 9):** the integration lead merges all sub-components into a single module + integration test suite. Resolves any typed-contract drift discovered at composition.

5. **Release (Week 10):** cohort-wide PR opened by the integration lead titled `Track 3 Flagship: Curved-Wall Worship Room — Cohort SP 2026`. All contributors listed in commit history. Tagged release as `worship_curved-v0.1.0` for citable use.

## Why pure functions and typed dataclasses

The integration lead can compose pure functions in any order without per-pair coordination meetings. Typed dataclasses surface contract drift at IDE-time rather than at integration-time. Both choices specifically target the failure mode where a multi-author module ships late because integration debt was discovered too late.

## Allocation file

See `OWNERS.md` for current allocation status. If you're starting cold, that's the first place to look.

## References

Bermudez, J., Krizaj, D., Lipschitz, D. L., Bueler, C. E., Rogowska, J., Yurgelun-Todd, D., & Nakamura, Y. (2017). Externally-induced meditative states: An exploratory fMRI study of architects' responses to contemplative architecture. *Frontiers of Architectural Research*, *6*(2), 123–136.

Hagerhall, C. M., Laike, T., Taylor, R. P., Küller, M., Küller, R., & Martin, T. P. (2008). Investigations of human EEG response to viewing fractal patterns. *Perception*, *37*(10), 1488–1494.

Hillier, B., & Hanson, J. (1984). *The social logic of space*. Cambridge University Press.

Joye, Y. (2007). Architectural lessons from environmental psychology: The case of biophilic architecture. *Review of General Psychology*, *11*(4), 305–328.

Vartanian, O., Navarrete, G., Chatterjee, A., Fich, L. B., Leder, H., Modroño, C., Nadal, M., Rostrup, N., & Skov, M. (2015). Architectural design and the brain: Effects of ceiling height and perceived enclosure on beauty judgments and approach-avoidance decisions. *Journal of Environmental Psychology*, *41*, 10–18.
