# AI Context: VR Production (Track 3)

## What is K-ATLAS?

K-ATLAS (Knowledge Architecture for Translating Life-science and Affective-environment Science) is a structured credibility reasoning system that transforms scientific evidence into actionable environmental design specifications. Rather than storing claims as isolated facts, K-ATLAS stores *structured credences* — beliefs tagged with how well-supported they are, where the support comes from, and why the system holds each belief with specific confidence.

The system models scientific knowledge as an Evidence Network (Web of Belief): a directed graph where nodes are claims and edges are typed, weighted warrants. A warrant is a formal justification for why evidence should change confidence in a claim. Each warrant carries a discount factor (d value, ranging from 0.25 to 1.0) that represents the epistemic distance between the type of evidence and the type of claim. When multiple independent pieces of evidence support the same claim, credences combine using Noisy-OR logic. The system is foundherentist: both empirical directness (how close evidence is to observation) and coherence with theoretical frameworks matter equally.

## How Evidence Items Describe Environment-Behavior Relationships

Each evidence item in K-ATLAS describes a specific, testable relationship between an environmental feature and a psychological or behavioral outcome. The relationship structure is:

**Environmental Feature → Psychological Mechanism → Behavioral Outcome**

Example evidence item:
- **Feature**: Ceiling height ≥ 3.0 meters
- **Mechanism**: Increased spatial openness activates attention networks (measured via fMRI)
- **Outcome**: Improved creative problem-solving (measured via Torrance Tests, effect size d = 0.68)
- **Evidence backing**: 12 studies, credence 0.71, entrenchment 0.54

Another example:
- **Feature**: Presence of biophilic elements (plants, water, nature imagery)
- **Mechanism**: Biophilia Hypothesis (E.O. Wilson): exposure to natural elements reduces amygdala threat response
- **Outcome**: Reduced cortisol, lower heart rate, self-reported stress reduction
- **Evidence backing**: 23 studies, credence 0.64, with VALIDATION gap (contested in non-Western populations)

## What a VR Environment Must Demonstrate

A VR environment created from K-ATLAS evidence should instantiate and visualize the causal chain from environmental feature to psychological mechanism to behavioral outcome. Specifically:

1. **Environmental Variable Instantiation**: The VR scene must clearly embody the environmental feature described in evidence. If the evidence specifies "ceiling height ≥ 3.0m", the scene must render a ceiling at that height (or adjustably, showing both high and low conditions). If the evidence involves "biophilic density", the scene must contain measurable quantities of natural elements.

2. **Mechanism Visualization**: Where possible, the scene should make the psychological mechanism visible or experientially salient. This can be literal (showing a stylized amygdala or attention network) or implicit (designing the scene such that users report the predicted mechanism — e.g., "I felt more focused in the high-ceiling version").

3. **Outcome Measurability**: The VR environment must include measurement points that correspond to the outcome variables in K-ATLAS evidence. If the evidence specifies "cortisol reduction measured via saliva", the VR environment should enable cortisol collection at pre/post timepoints. If the outcome is "creative problem-solving performance", the VR should include a creative task (e.g., Torrance Tests, divergent thinking tasks) executable within VR.

4. **Credence Transparency**: High-credence claims (>0.70) should be visualized with greater fidelity and more measurement points. Lower-credence claims (<0.50) may be presented as exploratory or with explicit uncertainty messaging.

## Warrant System and Confidence Structure

Each evidence item in K-ATLAS carries:
- **Warrant Type**: The epistemic relationship between the underlying studies and the claim

| Warrant Type | d value | Applied Example |
|--------------|---------|-----------------|
| CONSTITUTIVE | 1.0 | RCT measuring ceiling height & creative task in the same population |
| MECHANISM | 0.80 | fMRI study showing ceiling height → prefrontal cortex activation |
| EMPIRICAL_ASSOCIATION | 0.80 | Multiple studies showing correlation between open space & productivity |
| FUNCTIONAL | 0.65 | Effect replicates across lab & field, different participant types |
| CAPACITY | 0.55 | Plausible mechanism; limited direct evidence; expert judgment |
| ANALOGICAL | 0.40 | Evidence from museum design applied to office design |
| THEORY-DERIVED | 0.25 | Theoretical prediction not yet empirically tested |

**For VR design purposes**: Claims with warrant type CONSTITUTIVE or MECHANISM are safe to foreground in the scene; users should experience the mechanism directly. Claims with warrant type ANALOGICAL or THEORY-DERIVED should be marked as exploratory; consider showing them alongside an alternative, low-credence version for comparison.

## Data Model for VR Scene Specifications

Each VR scene designed from K-ATLAS evidence must specify:

- **scene_id**: Unique identifier (e.g., `biophilia_restoration_v1`, `lighting_attention_v2`)
- **target_evidence_items**: List of evidence_item_ids that this scene instantiates (e.g., `[EV_cortisol_biophilia_01, EV_attention_lighting_05]`)
- **environmental_variables**: Explicit specification of environmental features
  - *Example*: `{ "ceiling_height_m": 3.5, "biophilia_elements": ["potted_plants_count=8", "water_feature=fountain"], "luminance_lux": 450, "color_temperature_K": 5000 }`
- **behavioral_outcomes**: Outcome measures embedded in the VR
  - *Example*: `[{ "measure": "cortisol_saliva", "timing": "pre_scene", "timing": "post_scene" }, { "measure": "stroop_task_rt", "timing": "during_scene" }]`
- **measurement_points**: Specific locations/times in the scene where data collection occurs
  - *Example*: `[{ "type": "baseline_cortisol", "time": "0min" }, { "type": "post_exposure_cortisol", "time": "30min" }, { "type": "attention_task", "time": "15min", "location": "desk_center" }]`
- **credence_levels**: Mapping of which evidence items support which design choices
  - *Example*: `{ "ceiling_height_3.5m": { "evidence_id": "EV_creativity_ceiling_01", "credence": 0.71, "warrant_type": "EMPIRICAL_ASSOCIATION" } }`
- **platform**: Unreal Engine 5, A-Frame (WebXR), Unity, etc.
- **fidelity_level**: Photorealistic, stylized, abstract (should reflect credence; lower credence → more stylized)
- **notes**: Rationale for design choices, boundary conditions acknowledged

## Platform Flexibility

VR scenes for K-ATLAS can be produced in multiple platforms, each with different tradeoffs:

- **Unreal Engine 5**: Photorealistic fidelity, complex measurement integration, steeper learning curve
- **A-Frame**: Web-based, minimal setup, easier deployment for studies, lower fidelity
- **Unity**: Middle ground fidelity/complexity, strong measurement toolkits available
- **Custom WebGL**: Lightweight, good for research settings with strict technical constraints

Choose based on: credence of evidence (high credence → more fidelity investment), population (naive users → simpler interaction), and measurement requirements (physiological sensors → need robust integration).

## Acceptance Criteria for VR Scenes

1. **Evidence Instantiation**: Every environmental variable in the scene must map back to at least one K-ATLAS evidence item. The scene should not include environmental features that are not evidentially supported (e.g., do not add decorative art unless biophilic effects of art are in the evidence base).

2. **Mechanism Visibility**: The psychological mechanism (if specified in the evidence) should be made clear through scene design, annotation, or measurement. Users should be able to experience why the feature matters.

3. **Measurement Integrity**: Outcome measurement points must correspond exactly to the operationalization in the original evidence items. If evidence uses cortisol via saliva assay, the VR must enable saliva collection at the specified timepoints, not heart rate alone.

4. **Credence-Appropriate Design**: High-credence evidence (>0.70) should be rendered with higher visual fidelity and more measurement effort. Low-credence or exploratory evidence (<0.50) may be presented alongside a control condition or alternative design.

5. **Boundary Condition Documentation**: If the evidence includes BOUNDARY gaps (e.g., "effects stronger in Western populations" or "effect unclear for older adults"), the scene specification must note these. Do not silently overgeneralize high-credence claims across populations for which they are not validated.

6. **Scene Reusability**: Specification must be clear enough that another researcher could reconstruct the scene, modify parameters, or use it for follow-up studies. Include all environmental variable values as explicit numbers, not qualitative descriptions.

## Key References

- **Evidence Cards**: `ka_evidence.html` (shows constructs, credences, warrant types, and mechanism descriptions)
- **Construct Definitions**: `ka_topics.html` (browse organized psychological/environmental constructs)
- **Evidence Gaps**: `ka_gaps.html` (identify MECHANISM gaps where mechanism is unknown and needs VR experimentation)
- **Measurement Tools**: Validate outcome measures against `CNFA_construct_definitions.json` to ensure VR measurements are standard
- **Example Scene Specs**: Consult VR production assignment (`ka_vr_assignment.html`) for worked examples
