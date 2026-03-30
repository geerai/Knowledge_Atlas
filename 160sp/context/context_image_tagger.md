# AI Context: Image Tagger (Track 1)

## What is K-ATLAS?

K-ATLAS (Knowledge Architecture for Translating Life-science and Affective-environment Science) is a structured credibility reasoning system built around a single principle: a scientific claim is only as strong as the evidence and argumentation that support it. Unlike conventional databases that store facts as binary yes/no propositions, K-ATLAS stores *structured credences* — beliefs tagged with how well-supported they are, where the support comes from, and why the system assigns each belief its particular confidence level.

The system models scientific knowledge as an Evidence Network (also called the Web of Belief): a directed graph where each node is a claim, and each edge represents a typed, weighted warrant — a formal statement of why one piece of evidence should raise or lower confidence in another claim. When multiple independent pieces of evidence support the same belief, K-ATLAS combines them using Noisy-OR logic, which rewards the accumulation of independent evidence: two independent studies with credence 0.70 each together produce a combined credence of 0.91, not 0.70. The network is foundherentist in structure, following Susan Haack's framework: both empirical directness (how close evidence is to observation) and coherence with theoretical frameworks (how well beliefs fit together) matter equally.

## The Evidence Network Model

### Claims
A claim is a testable assertion: "Forest exposure lowers cortisol" or "High ceiling heights increase creative thinking." Each claim carries:
- **credence**: A confidence value from 0 to 1 indicating how well-supported the claim is
- **entrenchment**: A Quinean measure (0–1) of how central this belief is to the theoretical web; high-entrenchment beliefs are harder to revise because they are more densely connected to other beliefs
- **credence interval**: The range [lower bound, upper bound] reflecting uncertainty
- **t_ent**: The entrenchment score for this specific claim

### Edges and Warrants
Edges in the Evidence Network are typed connections representing warrants — formal justifications for why evidence should change our confidence in a claim. Each edge carries:
- **warrant type**: The epistemic relationship between source evidence and target belief
- **discount factor d**: How much credence flows across this edge (reflects the inferential distance between evidence type and claim type)
- **direction**: supporting (→) or undercutting (⊣)

### The Seven Warrant Types (Calibrated Default Credences)

| Warrant Type | d value | Meaning | Example |
|--------------|---------|---------|---------|
| **CONSTITUTIVE** | 1.0 | The evidence defines the claim; no inferential gap | An RCT measuring the exact variable in the claim text |
| **MECHANISM** | 0.80 | The evidence demonstrates a causal pathway through a specified psychological/neurological mechanism | An fMRI study showing amygdala downregulation when viewing nature images |
| **EMPIRICAL ASSOCIATION** | 0.80 | A replicated empirical correlation; mechanism unknown but directional evidence strong | Multiple studies showing correlation between biophilia scale scores and cortisol |
| **FUNCTIONAL** | 0.65 | Cross-context replication; effect holds across different populations, settings, or measurement methods | Evidence from both lab and field settings, both undergraduate and working-age participants |
| **CAPACITY** | 0.55 | Plausible mechanism or demonstrated effect in a narrower context; coherence with theory but limited empirical support | Expert judgment that natural light "should" improve focus, or a single-context study |
| **ANALOGICAL** | 0.40 | Evidence from a similar but not identical context; requires cautious bridging | Studies on museum lighting applied to office design |
| **THEORY-DERIVED** | 0.25 | Theoretical prediction from a T1 or T2 framework; not yet empirically confirmed | Circadian Biology predicts that blue-enriched lighting should enhance alertness |

When evidence supports a claim, credence flows across the edge at strength d. When multiple independent pieces of evidence converge on the same claim, credences combine using Noisy-OR.

## Image Tagging in K-ATLAS

Image tagging means linking architectural or environmental photographs to psychological constructs in the evidence base. The 424 CNFA tags (Cognitive-Neuro-Functional Architecture tags) are measurable features extracted from photographs:
- **Luminance features** (luminance_mean, luminance_std, color_temperature)
- **Spatial geometry** (ceiling_height_m, fractal_dimension_fd, openness_ratio)
- **Biophilia markers** (green_area_fraction, water_visible, natural_material_count)
- **Acoustic properties** (reverberation_time_s, nc_curve_level)

The linking process answers: "Which psychological construct does this measurable environmental feature support evidence for?"

For example:
- Tag `luminance_mean = 400 lux` → links to construct "daylight exposure" → which has evidence for "cortisol reduction" (credence 0.68)
- Tag `ceiling_height_m = 3.5` → links to construct "vertical space" → which has evidence for "creative thinking" (credence 0.52)

Image tagging is the measurement bridge between raw environmental data and the knowledge base's psychological claims.

## The CNFA Framework

The Cognitive-Neuro-Functional Architecture (CNFA) is the system's theoretical spine. It specifies:
1. **Environmental variables** (measurable properties of physical space)
2. **Psychological mechanisms** (attention, restoration, stress response, creativity)
3. **Behavioral outcomes** (productivity, well-being, social interaction)

The framework posits that environmental features → activate psychological mechanisms → produce behavioral change. Image tags measure environmental features; the Evidence Network justifies the psychological mechanisms and behavioral links.

## Data Model for Image Tags

Each image tag record must include:
- **image_id**: Unique identifier for the photograph
- **construct**: The name of the K-ATLAS construct this tag supports (e.g., "daylight_exposure", "biophilic_density")
- **evidence_item_id**: The K-ATLAS evidence item that this tag instantiates (linking back to the credence structure)
- **tag_value**: The numerical or categorical measurement (e.g., `luminance_mean: 450`, `ceiling_height_category: high`)
- **confidence**: How reliably this tag measurement supports the construct (0–1)
- **tagger_id**: Who created the tag (for quality tracking)
- **timestamp**: When the tag was created
- **notes**: Rationale for the tag-to-construct mapping (e.g., "daylight measured per CIE definition; supports cortisol evidence via mechanism warrant")

## Acceptance Criteria for Image Tags

1. **Reference to real evidence**: Every tag must map to a construct that appears in K-ATLAS evidence. Do not invent constructs; do not tag with psychological constructs unless the Evidence Network has credence scores for them.

2. **Justified confidence**: The confidence score must be explicitly reasoned. High confidence (>0.7) requires direct empirical warrant or multiple supporting sources. Medium confidence (0.4–0.7) is appropriate when mechanism is plausible but evidence is limited. Low confidence (<0.4) should only be used for theory-derived or analogical links.

3. **No hallucinated constructs**: If a tag maps to a construct not in K-ATLAS, the tag is invalid. Check the Evidence list first. Tag only constructs that K-ATLAS recognizes and has credence scores for.

4. **Measurement validity**: The tag value must be measured using a reproducible method. Subjective aesthetic judgments ("feels warm", "looks spacious") are not acceptable unless the tag explicitly measures a subjective response (e.g., via a validated questionnaire).

5. **Traceability**: A reviewer should be able to read a tag record and trace backward: tag → construct → evidence item → claim → supporting studies. Every link must be visible and justified.

## Key References

- **Claim and Evidence Structure**: `claim_v2.py` in the epistemic module
- **Warrant Scaling**: `warrant_scaling.py` in the epistemic module
- **CNFA Tag Definitions**: `image_tag_table.html` (424 tags, searchable by domain)
- **Example Evidence Cards**: `ka_evidence.html` on the K-ATLAS site
