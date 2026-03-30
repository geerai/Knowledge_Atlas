# Topic Hierarchy Repair Queue And Plan

Date: 2026-03-30

## Rule

The topic hierarchy viewer now follows a strict policy.

- show a paper only if it can be placed into at least one defensible topic pair
- a topic pair means an IV branch plus a DV focus
- allow multiple topic memberships per paper
- hide unresolved papers from the public topic hierarchy
- separate obvious non-topic contamination into an exclusion queue rather than pretending it is repairable topic work

## Current State

Canonical artifacts:

- `/Users/davidusa/REPOS/Knowledge_Atlas/data/ka_payloads/topic_hierarchy.json`
- `/Users/davidusa/REPOS/Knowledge_Atlas/data/ka_payloads/topic_repair_queue.json`
- `/Users/davidusa/REPOS/Knowledge_Atlas/data/ka_payloads/topic_exclusion_queue.json`

Current counts:

- total papers in article payload: `760`
- visible in hierarchy viewer: `679`
- still hidden for repair: `75`
- excluded as safe non-topic contamination: `6`

Repair queue composition:

- missing IV: `26`
- missing DV: `67`
- missing both: `12`

Queue size by claim count:

- `70` papers have only `1` claim
- `3` papers have `3` claims
- `1` paper has `2` claims
- `1` paper has `4` claims

This means the high-value failures have largely been repaired. The remaining queue is mostly a long tail of single-claim papers.

## What The Repair Tranches Already Did

### Tranche 1: IV recovery

Recovered IV branches from:

- `iv_raw`
- title
- abstract
- main conclusion

This repaired many papers that had blank or misleading structured IV nodes.

### Tranche 2: DV repair by concept collapse

Recovered DV focuses by collapsing raw measures upward into concept-level outcomes.

Examples:

- stress and anxiety rows -> `Stress`
- attention and vigilance rows -> `Attention`
- EEG and fMRI rows -> `Neural Activity`
- performance rows -> `Performance`
- restoration rows -> `Restoration / Recovery`

### Tranche 3: multi-topic membership

Papers are no longer forced into a single brittle dominant topic.

They can now enter several topic nodes when the paper genuinely studies several outcomes or relations.

### Tranche 4: theory and overview overlay

If a paper has a clear domain branch but no measured DV, and the paper is plainly explanatory or review-like, it can now enter through `Mechanism Or Pathway`.

### Tranche 5: exclusion queue

Obvious contamination or non-topic material is no longer left inside the repair queue.

## Clear Wins

These were hidden before and are now visible in the hierarchy:

- `PDF-0650` -> `Spatial Form -> Neural Activity`, `Spatial Form -> Attention`
- `PDF-0681` -> `Biophilia -> Wellbeing`, `Biophilia -> Neural Activity`
- `PDF-1320` -> `Spatial Form -> Neural Activity`, `Spatial Form -> Performance`, `Spatial Form -> Physiology`
- `PDF-1336` -> `Spatial Form -> Wellbeing`
- `PDF-1375` -> `Spatial Form -> Mechanism Or Pathway`, `Spatial Form -> Attention`
- `PDF-1357` -> `Spatial Form -> Mechanism Or Pathway`, `Spatial Form -> Stress`
- `PDF-0095` -> `Sensory Conditions -> Mechanism Or Pathway`
- `PDF-0565` -> `Spatial Form -> Mechanism Or Pathway`
- `PDF-0453` -> `Spatial Form -> Mechanism Or Pathway`, `Material and Surface Conditions -> Mechanism Or Pathway`

## Exclusion Queue

These are currently treated as safe non-topic contamination candidates rather than repair targets:

- `PDF-0264` — *Hybrid Visualization of the Medical Images Data Sets*
- `PDF-0789` — *Japan's 2011 earthquake and tsunami (Fukushima disaster)*
- `PDF-1348` — *A case in psychopathology*
- `PDF-1424` — *The Relation of Strength of Stimulus to Rapidity of Habit-Formation*
- `PDF-1434` — *Taylor & Francis Not for distribution*
- `PDF-1438` — duplicate of the habit-formation item above

## Remaining Highest-Priority Repairs

The remaining queue is small enough that targeted repairs are now sensible.

### Small number of higher-claim hidden papers

- `PDF-0984` — `3` claims — missing DV
- `PDF-1297` — `2` claims — missing DV
- `PDF-1431` — `1` claim — missing both
- `PDF-1445` — `1` claim — missing both

Most of the rest are single-claim tails.

### Remaining missing-both papers

These need either:

- a domain-preserving topic assignment, or
- reclassification into the exclusion queue

Examples:

- `PDF-0423` — *Interaction with nature and natural shapes*
- `PDF-0477` — *The Aesthetic Appreciation of Ruins*
- `PDF-0976` — *Two opposing perspectives on synesthesia*
- `PDF-1431` — *Neurociencia del aprendizaje y la poiesis somática de la arquitectura*
- `PDF-1432` — bare placeholder title
- `PDF-1445` — duplicate Spanish architecture-neuroscience item

### Remaining missing-DV papers

These typically have an IV branch but still need a cleaner concept-level DV collapse.

Examples:

- `PDF-0160` — *Red or rough, what makes materials warmer?*
- `PDF-0280` — *The aesthetic experience of interior spaces with curvilinear boundaries...*
- `PDF-0449` — *Lighting color temperature and teacher self-efficacy...*
- `PDF-0630` — *Monochromatic light exposures at wavelengths 420-600nm...*
- `PDF-0652` — *Nature experience and cognitive function relationship*
- `PDF-0671` — *Powerful Patina: The Value of Odors in a Tibetan Buddhist Temple*
- `PDF-0764` — *LEED certified buildings vs non-LEED rated buildings*
- `PDF-0767` — *Working in office with electrochromic glass...*
- `PDF-0811` — *IEQ aspects of 351 office buildings...*

## Next Repair Order

1. Resolve the small set of higher-claim remaining hidden papers.
2. Classify the remaining missing-both papers into:
   - genuine repair targets
   - exclusion candidates
3. Improve DV collapse for:
   - aesthetics
   - self-efficacy and perceived control
   - IEQ and comfort aggregates
   - material-perception outcomes
4. Re-run the hierarchy payload after each tranche and keep the public viewer hidden set shrinking.
