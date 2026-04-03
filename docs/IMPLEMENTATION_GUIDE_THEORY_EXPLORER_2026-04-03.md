# Implementation Guide: Theory Explorer Home Page Revision

**Date**: 2026-04-03
**Based on**: Expert Panel Review (EXPERT_PANEL_THEORY_EXPLORER_DESIGN_2026-04-03.md)
**Target Version**: Knowledge Atlas 2.1
**Status**: SPECIFICATION READY FOR DEVELOPMENT

---

## Quick Reference: What Changes Per Card

| Card | Key Changes | Effort | Timeline |
|------|-----------|--------|----------|
| **Neural Frameworks** | Minor: add domain count, link to galleries | Low | Week 1 |
| **Theory Comparison** | Major: entity-activity, level, coherence, scope, interventionist | High | Weeks 2–4 |
| **Mechanism Chain** | Major: multi-level pyramid, activities, gaps marked, empirical support | High | Weeks 2–4 |
| **Critical Test** | Major: mechanistic level, targeting, coherence impact, discrimination index | Very High | Weeks 4–6 |
| **Warrant Structure** | No changes | None | — |
| **Underdetermination Alert** | Medium: coherence comparison, interventionist divergence, timeline | Medium | Weeks 3–4 |

**Total Estimated Effort**: 10–12 weeks (development + QA + content creation)

---

## Card-by-Card Implementation Details

### Card 0: Neural Frameworks (Minor Update)

#### Current State

```
[Card showing 10 frameworks]
- Predictive Processing (12 articles, grounding score: 0.78)
- Salience Network (8 articles, grounding score: 0.72)
- [etc.]
```

#### Proposed Changes

**Add two data columns**:

1. **Domain Count**: How many distinct domains (fear, learning, attention, etc.) does each framework address?
2. **Mechanism Gallery Link**: Button linking to full mechanism schemata for that framework

#### New Data Model (Backend)

```json
{
  "framework_id": "predictive_processing",
  "name": "Predictive Processing",
  "article_count": 12,
  "grounding_score": 0.78,
  "domains_addressed": ["fear", "learning", "attention", "salience"],
  "domain_count": 4,
  "mechanism_gallery_url": "/mechanisms?framework=predictive_processing"
}
```

#### UI Template (Frontend)

```
[Card: Neural Frameworks]

[Framework Grid - 10 columns × 1 row, scrollable]

[Framework Tile]
  Title: Predictive Processing
  Subtitle: Uncertainty prediction and error signaling

  [Stat Pills]
    12 articles | Grounding: 0.78

  [Domain Badges]
    fear | learning | attention | salience (+1 more)

  [Button: "View Mechanism Schemata"]
    → /mechanisms?framework=predictive_processing
```

#### Effort: Low (1 week)

**Tasks**:
- [ ] Add `domains_addressed` and `mechanism_gallery_url` fields to framework data model
- [ ] Update frontend tile component to display domain badges
- [ ] Create mechanism gallery placeholder pages (content populated separately)
- [ ] QA: Verify all 10 frameworks have domain mappings

---

### Card 1: Theory Comparison (Major Revision)

#### Current State (Problematic)

```
Theory Comparison: Fear Extinction

Theory A: Threat Sensitization
  - Evidence: 3 papers
  - Explanation: Amygdala amplification of threat input

Theory B: Contextual Fear
  - Evidence: 4 papers
  - Explanation: Hippocampal-amygdala binding

Evidence Balance: Tied (no clear winner)
```

#### Proposed Design

**Multi-column table with panel recommendations integrated**:

```
[Card: Theory Comparison]

[Domain Selector Dropdown]
  Selected: "Fear Extinction"
  Options: [Fear Detection] [Fear Extinction] [Generalization] [Renewal] [etc.]

[Theory Comparison Table]

| Theory Name | Entities & Activities | Level | Observational Evidence | Coherence Score | Explanatory Scope | Interventionist Prediction |
|---|---|---|---|---|---|---|
| Threat Sensitization Model | Amygdala (encodes threat) → vmPFC (inhibits) | Circuit | 4 papers; R²=0.72 | **0.68** | 3/6 domains | Silencing vmPFC → extinction blocked |
| Contextual Fear Theory | Hippocampus (binds context) → Amygdala (gates threat) | Circuit | 5 papers; R²=0.78 | **0.78** | 5/6 domains | Lesioning dorsal CA3 → reduced generalization |

[Expandable detail panels below table]

[Expand: Threat Sensitization Model]
  Coherence Breakdown:
    - Breadth: 0.50 (explains 3/6 domains)
    - Depth: 0.80 (mechanistic detail, good empirical support)
    - Background coherence: 0.65 (some tension with neuroimaging literature)
    - Simplicity: 0.75 (2 core mechanisms)
    TOTAL: (0.50 × 0.3) + (0.80 × 0.3) + (0.65 × 0.2) + (0.75 × 0.2) = 0.68 ✓

  Explanatory Scope:
    Strong: threat detection, immediate fear response
    Weak: extinction learning, generalization patterns, fear renewal
    Silent: molecular mechanisms of extinction, long-term consolidation

  Interventionist Predictions (Testable):
    1. Lesioning vmPFC → fear extinction impaired
    2. Optogenetic silencing vmPFC during extinction → extinction blocked
    3. Blocking NMDA in vmPFC → extinction consolidation fails

[Expand: Contextual Fear Theory]
  Coherence Breakdown:
    - Breadth: 0.83 (explains 5/6 domains)
    - Depth: 0.75 (good circuit-level detail, weaker at molecular level)
    - Background coherence: 0.85 (strong alignment with hippocampal literature)
    - Simplicity: 0.65 (4 core mechanisms; more complex than TSM)
    TOTAL: (0.83 × 0.3) + (0.75 × 0.3) + (0.85 × 0.2) + (0.65 × 0.2) = 0.78 ✓

  Explanatory Scope:
    Strong: all domains including renewal and generalization
    Weak: molecular mechanism of context encoding still speculative
    Silent: exact role of amygdala subpopulations

  Interventionist Predictions (Testable):
    1. Lesioning dorsal CA3 → context-dependent extinction impaired
    2. Disrupting hippocampal-amygdala coupling → generalization increases
    3. Lesioning ventral DG → context fear returns on renewal

[Comparison Summary Panel]
  Current Status: Contextual Fear Theory is coherence-favored (0.78 vs. 0.68)
  Reason: Broader explanatory scope, stronger background coherence
  BUT: Both theories leave molecular mechanism unclear (Red Flag 🚩)
  Next Steps: See "Critical Tests" card for experiments that would resolve remaining gaps

[Transparency Footnote]
  Coherence scoring is based on: breadth of explanation, mechanistic detail,
  fit with background literature, and simplicity (Occam's razor). It is NOT a
  proof, but a reasoning aid. See [methodology link] for details.
```

#### Data Model (Backend)

```json
{
  "card_type": "theory_comparison",
  "phenomenon_id": "fear_extinction",
  "phenomenon_name": "Fear Extinction Learning",

  "theories": [
    {
      "theory_id": "tsm",
      "theory_name": "Threat Sensitization Model",

      "entities_and_activities": [
        {"entity": "Amygdala lateral nucleus", "activity": "encodes threat salience"},
        {"entity": "vmPFC", "activity": "inhibits amygdala output"}
      ],

      "mechanistic_level": "circuit",

      "empirical_evidence": {
        "paper_count": 4,
        "mean_r_squared": 0.72,
        "supporting_papers": ["Smith et al. 2020", "Jones et al. 2022"]
      },

      "coherence": {
        "score": 0.68,
        "breadth": 0.50,          // # domains explained / total
        "depth": 0.80,            // empirical support × mechanistic detail
        "background_coherence": 0.65,
        "simplicity": 0.75,
        "breakdown": "Breadth limited (explains threat detection and immediate fear only, not extinction); Depth strong (good circuit-level evidence); Background coherence moderate (some tension with extinction literature); Simple mechanism (2 core components)"
      },

      "explanatory_scope": {
        "domains_total": 6,
        "domains_explained": {
          "threat_detection": "strong",
          "immediate_fear": "strong",
          "fear_extinction": "weak",
          "generalization": "weak",
          "renewal": "silent",
          "molecular_consolidation": "silent"
        }
      },

      "interventionist_predictions": [
        {
          "intervention": "Lesion vmPFC",
          "predicted_outcome": "Fear extinction impaired",
          "confidence": 0.90,
          "tested": true,
          "reference": "Smith et al. 2020"
        },
        {
          "intervention": "Optogenetic silencing vmPFC during extinction",
          "predicted_outcome": "Extinction learning blocked",
          "confidence": 0.85,
          "tested": true,
          "reference": "Jones et al. 2022"
        }
      ]
    },
    // ... Theory B structure similar
  ],

  "comparison_summary": {
    "current_status": "Contextual Fear Theory is coherence-favored",
    "coherence_difference": 0.10,
    "primary_reason": "Broader explanatory scope (5/6 vs. 3/6 domains)",
    "remaining_gaps": "Molecular mechanism of extinction consolidation unclear; both theories need synaptic-level detail",
    "see_also": "Critical Tests card"
  }
}
```

#### Frontend Components

**1. Theory Row Component** (`TheoryComparisonRow.tsx`)

```typescript
interface TheoryComparisonRowProps {
  theory: Theory;
  phenomenonId: string;
  isExpanded: boolean;
  onToggleExpand: () => void;
}

export function TheoryComparisonRow({theory, isExpanded, onToggleExpand}: TheoryComparisonRowProps) {
  return (
    <>
      <TableRow onClick={onToggleExpand}>
        <TableCell>
          <Typography variant="h6">{theory.theory_name}</Typography>
        </TableCell>

        <TableCell>
          {theory.entities_and_activities.map((ea, i) => (
            <Chip
              key={i}
              label={`${ea.entity} (${ea.activity})`}
              size="small"
              variant="outlined"
            />
          ))}
        </TableCell>

        <TableCell>
          <Badge level={theory.mechanistic_level} />
        </TableCell>

        <TableCell>
          <Typography variant="body2">
            {theory.empirical_evidence.paper_count} papers
          </Typography>
          <Typography variant="caption" color="textSecondary">
            R² = {theory.empirical_evidence.mean_r_squared.toFixed(2)}
          </Typography>
        </TableCell>

        <TableCell>
          <CoherenceScorePill score={theory.coherence.score} />
        </TableCell>

        <TableCell>
          <ScopeMatrix domains={theory.explanatory_scope.domains_explained} />
        </TableCell>

        <TableCell>
          <Typography variant="body2">
            {theory.interventionist_predictions[0]?.predicted_outcome}
          </Typography>
        </TableCell>

        <TableCell>
          <ExpandButton isExpanded={isExpanded} />
        </TableCell>
      </TableRow>

      {isExpanded && (
        <DetailPanel theory={theory} />
      )}
    </>
  );
}
```

**2. Coherence Breakdown Component** (`CoherenceBreakdown.tsx`)

```typescript
export function CoherenceBreakdown({coherence}: {coherence: Coherence}) {
  return (
    <Box>
      <Typography variant="subtitle2">Coherence Score: {coherence.score.toFixed(2)}</Typography>

      <Box sx={{display: 'flex', gap: 2, mb: 2}}>
        <CoherenceSubscore label="Breadth" value={coherence.breadth} weight={0.30} />
        <CoherenceSubscore label="Depth" value={coherence.depth} weight={0.30} />
        <CoherenceSubscore label="Background Coherence" value={coherence.background_coherence} weight={0.20} />
        <CoherenceSubscore label="Simplicity" value={coherence.simplicity} weight={0.20} />
      </Box>

      <Typography variant="body2">{coherence.breakdown}</Typography>
    </Box>
  );
}

function CoherenceSubscore({label, value, weight}: {label: string; value: number; weight: number}) {
  return (
    <Box>
      <Typography variant="caption">{label}</Typography>
      <LinearProgress variant="determinate" value={value * 100} />
      <Typography variant="caption" color="textSecondary">
        {value.toFixed(2)} × {(weight * 100).toFixed(0)}% = {(value * weight).toFixed(2)}
      </Typography>
    </Box>
  );
}
```

**3. Scope Matrix Component** (`ScopeMatrix.tsx`)

```typescript
export function ScopeMatrix({domains}: {domains: Record<string, 'strong' | 'weak' | 'silent'>}) {
  return (
    <Box sx={{display: 'flex', gap: 1, flexWrap: 'wrap'}}>
      {Object.entries(domains).map(([domain, strength]) => (
        <Tooltip key={domain} title={strength}>
          <Chip
            label={domain}
            color={strength === 'strong' ? 'success' : strength === 'weak' ? 'warning' : 'default'}
            size="small"
          />
        </Tooltip>
      ))}
    </Box>
  );
}
```

#### Effort: High (3 weeks)

**Tasks**:
- [ ] Design and implement Theory Comparison data schema
- [ ] Create entity-activity pair representation
- [ ] Implement coherence scoring algorithm (backend)
- [ ] Build expandable detail panels with coherence breakdown
- [ ] Create scope matrix visualization
- [ ] Implement interventionist prediction display
- [ ] Populate data for all phenomena (content team)
- [ ] QA: Test with 3–5 domain phenomena; verify calculations
- [ ] Documentation: Write methodology link explaining coherence scoring

---

### Card 2: Mechanism Chain (Major Revision)

#### Current State (Problematic)

```
[Linear chain]
Stimulus → Amygdala → Fear Response → Behavioral Output
```

#### Proposed Design: Multi-Level Pyramid

**Visual Structure**:

```
[Card: Mechanism Chain]

[Phenomenon Selector]
  Selected: "Fear Extinction Learning"

[Multi-Level Pyramid Diagram]

                        [BEHAVIORAL LEVEL] ← GREEN (empirically confirmed)
           Fear-to-CS decreased after extinction training
                          ↑ (etiological)

                         [CIRCUIT LEVEL] ← YELLOW (tentative how-possibly)
        vmPFC (encodes CS non-threat) --inhibits--> Amygdala LA
        Hippocampus (encodes context) --gates--> Amygdala LA
                          ↑ (constitutive)

                         [SYNAPTIC LEVEL] ← YELLOW (how-possibly)
        vmPFC pyramidal → LA interneurons
        GABA release onto pyramidal and stellate cells
                          ↑ (constitutive)

                        [MOLECULAR LEVEL] ← RED (gap: [HOW?])
        GABA-A receptor binding [HOW?] → channel opening → hyperpolarization

[Legend]
  GREEN: Empirically confirmed (multiple independent studies)
  YELLOW: Tentative (how-possibly); limited evidence
  RED: Known gap; explicitly unresolved
  GRAY: Not tested; theoretically predicted

[Expandable Tables Below]

[Empirical Support by Level]
| Level | Status | Key Evidence | # Papers | Confidence |
|-------|--------|--------------|----------|-----------|
| Behavioral | GREEN | Fear extinction occurs; measured via freezing suppression | 20+ | Very High (>0.95) |
| Circuit | GREEN | vmPFC→LA and Hippocampus→LA confirmed by lesion, inactivation, optogenetics | 15+ | High (>0.85) |
| Synaptic | YELLOW | GABA release demonstrated; receptor mechanisms inferred | 5–8 | Medium (0.60–0.75) |
| Molecular | RED | GABA-A subunit composition not fully characterized | 2–3 | Low (0.30–0.40) |

[Interventionist Properties]
| Intervention | Target | Expected Outcome if Mechanism Valid | Reference |
|---|---|---|---|
| Sensory deprivation (dark, silent) | Stimulus input | Extinction learning fails → mechanism requires input | Smith 2020 |
| vmPFC lesion/inactivation | Circuit | Extinction impaired → vmPFC necessary | Jones 2022 |
| Dorsal CA3 lesion | Hippocampal context | Context-dependent extinction blocked | Brown 2021 |
| GABA antagonist in LA | Synaptic | Extinction learning impaired → GABA necessary | [Predicted] |
| GABA-A α1 knockdown in LA | Molecular | [TBD by critical test] | [Planned] |

[Schema Classification]
- Levels 1–2 (Behavioral–Circuit): "How-actually" (empirically confirmed)
- Levels 3–4 (Synaptic–Molecular): "How-possibly" (candidate mechanisms with empirical gaps)

Interpretation: We know the circuit-level mechanism works. We have candidates for the synaptic level
but need targeted experiments to confirm. The molecular mechanism is currently unknown.

[Next Steps: See "Critical Tests" card for experiments targeting molecular mechanism]
```

#### Data Model (Backend)

```json
{
  "card_type": "mechanism_chain",
  "phenomenon_id": "fear_extinction_learning",
  "phenomenon_name": "Fear Extinction Learning",

  "levels": [
    {
      "level_id": "behavioral",
      "level_name": "Behavioral/Systems",
      "description": "Learning curves, behavioral output, systems-level effects",
      "schema_status": "confirmed",
      "color_code": "green",

      "entities_and_activities": [
        {
          "entity": "Fear-to-CS",
          "activity": "decreases after repeated safe exposure",
          "measurement": "Freezing percentage in extinction session",
          "timeline": "Multiple trials (2–5 minutes) show progressive decrease"
        }
      ],

      "empirical_support": {
        "paper_count": 20,
        "confidence": 0.95,
        "key_papers": ["Pavlov 1927", "Bouton 1993", "Myers & Davis 2007"],
        "effect_size": "Large (d > 1.5 typical)"
      },

      "etiological_cause_to_lower_level": {
        "description": "Behavioral change is caused by circuit-level plasticity in vmPFC-amygdala system",
        "mechanism_detail": "vmPFC pyramidal neurons learn to encode non-threat context; their inhibitory projections to amygdala suppress threat response"
      }
    },
    {
      "level_id": "circuit",
      "level_name": "Circuit",
      "description": "Multi-region coordination; meso-scale organization",
      "schema_status": "confirmed",
      "color_code": "green",

      "entities_and_activities": [
        {
          "entity": "vmPFC (ventromedial prefrontal cortex)",
          "activity": "encodes and stores extinction memory",
          "evidence": "Lesion studies, optogenetics, fMRI",
          "role": "Plasticity-dependent learning of new CS-no-threat association"
        },
        {
          "entity": "Amygdala lateral nucleus",
          "activity": "receives inhibitory projections from vmPFC; threat response is gated",
          "evidence": "Electrophysiology, optogenetics, electron microscopy",
          "role": "Site of inhibition; output to fear responses"
        },
        {
          "entity": "Hippocampus (dorsal CA3, CA1)",
          "activity": "encodes context; gates amygdala threat response based on context",
          "evidence": "Lesion studies, immediate early genes, optogenetics",
          "role": "Context specificity; prevents overgeneralization"
        }
      ],

      "empirical_support": {
        "paper_count": 15,
        "confidence": 0.88,
        "key_papers": ["Ledoux 2000", "Quirk et al. 2006", "Milad & Quirk 2012"],
        "methods": ["Bilateral lesion", "Reversible inactivation", "Optogenetics", "Patch recording", "Electron microscopy"]
      },

      "constitutive_composition": {
        "description": "Circuit-level mechanism is constituted by synaptic-level entities",
        "components": "Synaptic strength changes (LTP/LTD), local circuit connectivity"
      }
    },
    {
      "level_id": "synaptic",
      "level_name": "Synaptic",
      "description": "Transmission, plasticity mechanisms (LTP, LTD), receptor dynamics",
      "schema_status": "tentative",
      "color_code": "yellow",

      "entities_and_activities": [
        {
          "entity": "vmPFC pyramidal neurons → LA interneurons (GABAergic)",
          "activity": "synaptic transmission via GABA release; inhibitory postsynaptic potential (IPSC) amplitude increases during extinction learning",
          "mechanism_type": "Long-term potentiation (LTP) of GABA synapses",
          "evidence": "Patch recording in slices, some in vivo recordings",
          "confidence": 0.70
        },
        {
          "entity": "vmPFC pyramidal neurons → LA pyramidal neurons (glutamatergic)",
          "activity": "synaptic transmission via glutamate; AMPA and NMDA receptor dynamics",
          "mechanism_type": "Activity-dependent plasticity; role unclear",
          "evidence": "Inference from circuit models; direct recording limited",
          "confidence": 0.50
        }
      ],

      "empirical_support": {
        "paper_count": 7,
        "confidence": 0.65,
        "key_papers": ["Chhatwal et al. 2009", "Jezernik et al. 2021"],
        "gap_note": "Most evidence from slice electrophysiology; in vivo synaptic-level recordings are rare"
      },

      "schema_status_note": "How-possibly schema: we have candidate mechanisms (GABA-LTP, NMDA-dependent consolidation) but critical experiments are not yet done"
    },
    {
      "level_id": "molecular",
      "level_name": "Molecular",
      "description": "Gene expression, protein binding, receptor subunit composition",
      "schema_status": "unknown",
      "color_code": "red",

      "entities_and_activities": [
        {
          "entity": "GABA-A receptors (α1, α2, α3 subunit variants)",
          "activity": "[HOW DO SUBUNITS CONTRIBUTE TO EXTINCTION?]",
          "mechanism_type": "Unknown",
          "evidence": "None directly testing this mechanism",
          "confidence": 0.0,
          "gap_description": "Pharmacological evidence shows GABA is necessary, but which receptor subtypes carry the signal? Do different subunits mediate different temporal phases?"
        },
        {
          "entity": "CREB (cAMP response element binding protein)",
          "activity": "[HOW DOES CREB PHOSPHORYLATION ENABLE EXTINCTION?]",
          "mechanism_type": "Transcription-dependent consolidation (hypothesized)",
          "evidence": "Global CREB phosphorylation shows correlation with memory consolidation, but causal role unclear",
          "confidence": 0.40
        }
      ],

      "empirical_support": {
        "paper_count": 2,
        "confidence": 0.25,
        "key_papers": ["Mamiya et al. 2009 (CREB)", "Generic pharmacology"],
        "gap_summary": "Molecular mechanism is a frontier. We know these molecules are involved, but the specific mechanistic roles are unspecified."
      }
    }
  ],

  "schema_gaps": [
    {
      "gap_id": "molecular_gaba_subtypes",
      "level": "molecular",
      "description": "Which GABA-A receptor subunits (α1, α2, etc.) are necessary for extinction learning?",
      "current_status": "Unknown",
      "critical_test_id": "ct_gaba_a_alpha1_knockout"
    },
    {
      "gap_id": "creb_extinction_consolidation",
      "level": "molecular",
      "description": "Does CREB phosphorylation in LA drive extinction consolidation, or is it epiphenomenal?",
      "current_status": "Unclear from existing evidence",
      "critical_test_id": "ct_conditional_creb_knockout_la"
    }
  ],

  "interventionist_properties": [
    {
      "intervention": "Sensory deprivation (dark, sound-attenuated)",
      "target_level": "behavioral_input",
      "predicted_outcome_if_valid": "Extinction learning cannot proceed (sensory input required)",
      "robustness": "Mechanism is input-dependent",
      "tested": true,
      "reference": "Bouton 1993"
    },
    {
      "intervention": "vmPFC bilateral lesion",
      "target_level": "circuit",
      "predicted_outcome_if_valid": "Extinction learning severely impaired or absent",
      "robustness": "vmPFC necessary for extinction",
      "tested": true,
      "reference": "Morgan et al. 1993"
    },
    {
      "intervention": "Reversible vmPFC inactivation (muscimol)",
      "target_level": "circuit",
      "predicted_outcome_if_valid": "Extinction blocked during inactivation; recovers after drug wears off",
      "robustness": "vmPFC necessary; role is reversible (not developmental)",
      "tested": true,
      "reference": "Quirk et al. 2006"
    },
    {
      "intervention": "Optogenetic silencing vmPFC→LA pathway",
      "target_level": "circuit",
      "predicted_outcome_if_valid": "Extinction learning blocked despite vmPFC intact",
      "robustness": "vmPFC→LA transmission necessary; other vmPFC outputs insufficient",
      "tested": true,
      "reference": "Jones et al. 2022"
    },
    {
      "intervention": "GABA antagonist (gabazine) in LA",
      "target_level": "synaptic",
      "predicted_outcome_if_valid": "Extinction learning blocked",
      "robustness": "GABA transmission necessary",
      "tested": false,
      "status": "Predicted but not yet tested"
    },
    {
      "intervention": "GABA-A α1 selective knockdown in LA",
      "target_level": "molecular",
      "predicted_outcome_if_valid": "[Depends on theory: see Critical Tests card]",
      "robustness": "Tests molecular mechanism specificity",
      "tested": false,
      "status": "This is the critical test; outcome unknown"
    }
  ]
}
```

#### Frontend Components

**1. Multi-Level Pyramid Visualization** (`MechanismPyramid.tsx`)

```typescript
export function MechanismPyramid({
  phenomenon: Phenomenon
}: {phenomenon: Phenomenon}) {
  const levels = phenomenon.mechanism_chain.levels;

  return (
    <Box sx={{position: 'relative', width: '100%', mb: 4}}>
      {/* Pyramid visualization */}
      <svg width="100%" height={400} viewBox="0 0 800 400">
        {levels.map((level, idx) => {
          const width = 600 - idx * 80;
          const height = 80;
          const x = 400 - width / 2;
          const y = 50 + idx * 85;

          return (
            <g key={level.level_id}>
              {/* Rectangle for level */}
              <rect
                x={x}
                y={y}
                width={width}
                height={height}
                fill={getLevelColor(level.schema_status)}
                stroke="#333"
                strokeWidth={2}
              />

              {/* Level label */}
              <text
                x={x + width / 2}
                y={y + height / 2}
                textAnchor="middle"
                dominantBaseline="middle"
                fontSize={16}
                fontWeight="bold"
              >
                {level.level_name} {getStatusBadge(level.schema_status)}
              </text>

              {/* Arrow between levels */}
              {idx < levels.length - 1 && (
                <path
                  d={`M ${400} ${y + height} L ${400} ${y + height + 20}`}
                  stroke="#666"
                  strokeWidth={2}
                  markerEnd="url(#arrowhead)"
                />
              )}
            </g>
          );
        })}
      </svg>

      {/* Legend */}
      <Box sx={{display: 'flex', gap: 2, mt: 2}}>
        <LegendItem color="green" label="Empirically confirmed" />
        <LegendItem color="yellow" label="Tentative (how-possibly)" />
        <LegendItem color="red" label="Known gap" />
        <LegendItem color="gray" label="Not tested" />
      </Box>
    </Box>
  );
}

function getLevelColor(status: string): string {
  const colorMap = {
    'confirmed': '#90EE90',
    'tentative': '#FFFFE0',
    'unknown': '#FFB6C6',
    'untested': '#D3D3D3'
  };
  return colorMap[status] || '#F0F0F0';
}
```

**2. Empirical Support Table** (`EmpiricalSupportTable.tsx`)

```typescript
export function EmpiricalSupportTable({levels}: {levels: Level[]}) {
  return (
    <TableContainer>
      <Table size="small">
        <TableHead>
          <TableRow sx={{backgroundColor: '#f5f5f5'}}>
            <TableCell>Level</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Key Evidence</TableCell>
            <TableCell>Papers</TableCell>
            <TableCell>Confidence</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {levels.map((level) => (
            <TableRow key={level.level_id}>
              <TableCell>{level.level_name}</TableCell>
              <TableCell>
                <StatusBadge status={level.schema_status} />
              </TableCell>
              <TableCell>
                {level.empirical_support.key_papers.join(', ')}
              </TableCell>
              <TableCell>{level.empirical_support.paper_count}</TableCell>
              <TableCell>
                <ConfidenceBar
                  confidence={level.empirical_support.confidence}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
```

#### Effort: High (3 weeks)

**Tasks**:
- [ ] Design multi-level pyramid visualization
- [ ] Implement schema-gap notation (color-coded by status)
- [ ] Create entity-activity pair display within each level
- [ ] Build empirical support tables
- [ ] Implement interventionist properties section
- [ ] Create schema-gap legend and interpretation
- [ ] Populate mechanism chain data for top 5 phenomena (content team)
- [ ] QA: Test pyramid rendering at multiple scales
- [ ] Documentation: Write interpretation guide for users

---

### Card 3: Critical Test (Major Revision)

#### Current State (Underspecified)

```
[Card: Critical Tests]

Test 1: Bilateral infusion of AP5 in amygdala lateral nucleus
  Priority: High
  Discriminates: Theory A vs. Theory B
```

#### Proposed Design: Theory-Targeted Interventionist Testing

```
[Card: Critical Test]

[Phenomenon Selector]
  Selected: "Fear Extinction Learning"

[Ranked Test List]

RANK 1: Molecular Mechanism of GABA-A Receptor Subtypes in LA Extinction

  Target Theories:
    Theory A: "GABA-A α1 subunits are sufficient for extinction"
    Theory B: "Multiple GABA-A subtypes required (α1 + α2 required)"

  Mechanistic Level: Molecular (specifically, GABA-A receptor subunit composition)

  Causal Bottleneck:
    Which GABA-A receptor subunits carry the critical inhibitory signal that suppresses
    amygdala threat response during extinction?

  Proposed Intervention:
    - Transgenic mice: conditional knockout of GABA-A α1 subunit in LA pyramidal cells
    - Method: Cre-lox system; LA-specific knockout using VGAT-Cre × loxP-α1
    - Timing: Knockout before behavioral training
    - Controls:
      * WT littermates (normal extinction)
      * Global α1 knockout (controls for developmental effects)
      * α2 subunit knockout (controls for subunit specificity)

  Specificity Assessment: 🟢 HIGH
    - Targets specific receptor subunit in specific region in specific cell type
    - Alternative explanation unlikely (conditional knockout is cell-type specific)

  Theory A Prediction:
    Extinction learning is BLOCKED in α1 KO mice
    Phenotype: Normal freezing to CS in baseline fear conditioning;
              No freezing suppression in extinction sessions (freezing remains high)
    Confidence: p > 0.85

  Theory B Prediction:
    Extinction learning PROCEEDS NORMALLY in α1 KO mice
    Phenotype: Normal extinction curve (α2 subunits compensate)
    Confidence: p > 0.80

  Coherence Impact (if Theory A is confirmed):
    Theory A: 0.68 → 0.88 (+0.20 points)
    Theory B: 0.78 → 0.45 (-0.33 points)
    Net discrimination: |0.20| + |−0.33| = 0.53 (HIGH)

  Coherence Impact (if Theory B is confirmed):
    Theory A: 0.68 → 0.35 (-0.33 points)
    Theory B: 0.78 → 0.91 (+0.13 points)
    Net discrimination: |−0.33| + |0.13| = 0.46 (HIGH)

  Discrimination Index: 0.87
    (Either outcome has >0.85 probability and strongly favors one theory)

  Robustness Checks:
    ✓ Is the knockout truly α1-specific? → Verify with immunofluorescence, patch recording
    ✓ Is the deficit in learning or memory? → Test extinction recall 24h later
    ✓ Is the deficit in extinction or in fear conditioning? → Test acquisition curve
    ✓ What about other GABA-A subunits? → Planned follow-up testing α2, α3 knockdowns

  Status: 🟡 FEASIBLE (genetics available; ~2–3 years to completion)

  Critical Test Timeline:
    - Year 1: Establish KO colony, behavioral characterization
    - Year 2: Patch recording, optogenetics to confirm molecular phenotype
    - Year 3: Publication and integration into theory

---

RANK 2: Role of vmPFC→LA GABA Transmission During Extinction (vs. Other Inhibitory Pathways)

  Target Theories:
    Theory A: "vmPFC→LA GABA transmission is necessary for extinction"
    Theory B: "Alternative inhibitory pathways (e.g., from IL cortex, from basolateral amygdala inhibitory interneurons) can substitute if vmPFC input is lost"

  Mechanistic Level: Circuit (specifically, vmPFC→LA circuit)

  Proposed Intervention:
    - Transgenic: VGAT-Cre × loxP-VGAT (silences GABAergic neurons selectively in vmPFC)
    - Anatomical specificity: Silencing vmPFC GABAergic neurons only
    - Method: cKO of VGAT in Cre-expressing cells (total loss of GABA release from vmPFC)
    - Timeline: During extinction training

  Theory A Prediction:
    Extinction learning BLOCKED when vmPFC GABA silenced
    Confidence: p > 0.90

  Theory B Prediction:
    Extinction learning PROCEEDS when vmPFC GABA silenced
    (Alternative inhibitory circuits compensate)
    Confidence: p > 0.75

  Coherence Impact: 0.35 (moderate; depends on interpretation of compensation)

  Discrimination Index: 0.78 (good but not as high as Rank 1)

  Status: 🟡 FEASIBLE (~18–24 months)

---

[See Also: Theory Comparison card for current coherence scores]
```

#### Data Model (Backend)

```json
{
  "card_type": "critical_test",
  "phenomenon_id": "fear_extinction_learning",
  "tests": [
    {
      "test_id": "ct_gaba_a_alpha1_knockout",
      "rank": 1,
      "test_name": "GABA-A α1 Subunit Knockout in Amygdala LA",

      "target_theories": [
        {"theory_id": "theory_a", "theory_name": "α1 Sufficiency Hypothesis"},
        {"theory_id": "theory_b", "theory_name": "Multiple Subtypes Required"}
      ],

      "mechanistic_level": "molecular",
      "causal_bottleneck": "Which GABA-A subunits carry extinction-related inhibition?",

      "intervention": {
        "method": "Conditional genetic knockout",
        "specifics": "VGAT-Cre × loxP-GABA-A-α1",
        "target_specificity": {
          "region": "Amygdala lateral nucleus (LA)",
          "cell_type": "Pyramidal neurons",
          "receptor_type": "GABA-A α1 subunit",
          "specificity_score": 0.95 // high
        },
        "controls": [
          "WT littermates",
          "Global α1 knockout",
          "α2 knockout"
        ],
        "timeline": "Before behavioral training"
      },

      "theory_predictions": [
        {
          "theory_id": "theory_a",
          "prediction": "Extinction learning is blocked; freezing remains high",
          "confidence": 0.85,
          "mechanistic_detail": "α1-containing GABA-A receptors are necessary for vmPFC inhibition of amygdala threat response"
        },
        {
          "theory_id": "theory_b",
          "prediction": "Extinction proceeds normally; α2 subunits compensate",
          "confidence": 0.80,
          "mechanistic_detail": "Multiple GABA-A subtypes can mediate extinction; redundancy in inhibitory signaling"
        }
      ],

      "coherence_impact": {
        "if_theory_a_confirmed": {
          "theory_a": {current: 0.68, updated: 0.88, delta: 0.20},
          "theory_b": {current: 0.78, updated: 0.45, delta: -0.33}
        },
        "if_theory_b_confirmed": {
          "theory_a": {current: 0.68, updated: 0.35, delta: -0.33},
          "theory_b": {current: 0.78, updated: 0.91, delta: 0.13}
        },
        "total_discrimination": 0.53
      },

      "discrimination_index": 0.87,
      "discrimination_rationale": "Both theories make predictions >0.80 probability; either outcome strongly discriminates",

      "robustness_checks": [
        {
          "check": "Verify α1 KO specificity",
          "method": "Immunofluorescence, patch recording",
          "purpose": "Confirm subunit-selective loss"
        },
        {
          "check": "Distinguish learning from memory",
          "method": "Test extinction recall 24h, 7d post-extinction",
          "purpose": "Is deficit in acquisition or consolidation?"
        },
        {
          "check": "Test fear conditioning (not just extinction)",
          "method": "Measure acquisition curves",
          "purpose": "Is amygdala fear encoding intact?"
        }
      ],

      "feasibility": {
        "status": "feasible",
        "timeline_years": 3,
        "effort": "high",
        "key_requirements": ["VGAT-Cre mice available", "loxP-GABA-A-α1 available or need to generate", "patch recording expertise"],
        "timeline_breakdown": {
          "year_1": "Establish KO colony; behavioral characterization (freezing, extinction, fear conditioning)",
          "year_2": "Patch recording (LA pyramidal cells, GABA-A subunit composition); optogenetics",
          "year_3": "Publication; integration into theory atlas"
        }
      }
    }
  ]
}
```

#### Frontend Components

**1. Test Card Component** (`CriticalTestCard.tsx`)

```typescript
export function CriticalTestCard({test}: {test: CriticalTest}) {
  const [expandedSection, setExpandedSection] = useState<string | null>(null);

  return (
    <Card>
      <CardContent>
        <Box sx={{mb: 3}}>
          <Chip label={`Rank ${test.rank}`} color="primary" />
          <Typography variant="h5">{test.test_name}</Typography>
        </Box>

        {/* Target Theories */}
        <Box sx={{mb: 2}}>
          <Typography variant="subtitle2">Target Theories</Typography>
          {test.target_theories.map((theory) => (
            <Box key={theory.theory_id} sx={{ml: 2}}>
              <Typography variant="body2">
                {theory.theory_name}
              </Typography>
            </Box>
          ))}
        </Box>

        {/* Mechanistic Level */}
        <Box sx={{mb: 2}}>
          <Typography variant="subtitle2">Mechanistic Level</Typography>
          <Chip label={test.mechanistic_level} variant="outlined" />
        </Box>

        {/* Causal Bottleneck */}
        <Box sx={{mb: 3, p: 2, bgcolor: '#f5f5f5', borderRadius: 1}}>
          <Typography variant="subtitle2">Causal Bottleneck</Typography>
          <Typography variant="body2">{test.causal_bottleneck}</Typography>
        </Box>

        {/* Intervention Details */}
        <ExpandableSection
          title="Intervention Details"
          isExpanded={expandedSection === 'intervention'}
          onToggle={() => setExpandedSection(expandedSection === 'intervention' ? null : 'intervention')}
        >
          <InterventionDetails intervention={test.intervention} />
        </ExpandableSection>

        {/* Theory Predictions */}
        <ExpandableSection
          title="Theory Predictions"
          isExpanded={expandedSection === 'predictions'}
          onToggle={() => setExpandedSection(expandedSection === 'predictions' ? null : 'predictions')}
        >
          <TheoryPredictions predictions={test.theory_predictions} />
        </ExpandableSection>

        {/* Discrimination Metrics */}
        <ExpandableSection
          title="Discrimination Metrics"
          isExpanded={expandedSection === 'metrics'}
          onToggle={() => setExpandedSection(expandedSection === 'metrics' ? null : 'metrics')}
        >
          <DiscriminationMetrics
            discriminationIndex={test.discrimination_index}
            coherenceImpact={test.coherence_impact}
          />
        </ExpandableSection>

        {/* Feasibility */}
        <FeasibilityBadge feasibility={test.feasibility} />
      </CardContent>
    </Card>
  );
}
```

#### Effort: Very High (4–6 weeks)

**Tasks**:
- [ ] Design critical test specification data model
- [ ] Implement discrimination index calculation
- [ ] Implement coherence impact calculation (integrate with Theory Comparison card)
- [ ] Build interventionist targeting UI (specificity score visualization)
- [ ] Create prediction comparison visualization
- [ ] Implement robustness check list
- [ ] Build feasibility timeline widget
- [ ] Populate critical tests for top 3 phenomena (content + domain experts)
- [ ] QA: Verify calculations match manual assessments
- [ ] Documentation: Write methodology for discrimination index and coherence impact

---

### Card 4: Warrant Structure (No Changes)

**Current Design**: Distribution of 7 warrant types across topics. This card is epistemologically transparent and does not require revision.

**Effort**: None (0 weeks)

---

### Card 5: Underdetermination Alert (Medium Revision)

#### Current State

```
Underdetermination Alert: 3 cases where theories tie

Case 1: Fear Extinction
  Theory A: NMDA-dependent consolidation
  Theory B: GABA-mediated inhibition
  Status: Tied on evidence (4 papers each)
```

#### Proposed Design

```
[Card: Underdetermination Alert]

[Active Underdetermined Cases: 3 total]

Case 1: Fear Extinction Molecular Mechanism

Competing Theories:
  - NMDA-dependent consolidation (Coherence: 0.68)
  - GABA-mediated inhibition (Coherence: 0.78)

Observational Status: TIED
  Both theories explain available extinction data equally well (4–5 papers each)
  No current observational experiment can discriminate them

Coherence Comparison:
  GABA-mediated inhibition is currently favored (0.78 vs. 0.68)
  Reason: Broader explanatory scope (explains extinction, generalization, renewal)
  But: This preference is tentative; more evidence needed

Interventionist Divergence: STRONG
  Theory A predicts: NMDA blockade → extinction consolidation fails
  Theory B predicts: NMDA blockade → extinction proceeds normally
  These predictions are opposite and testable

Critical Test Status: IDENTIFIED & FEASIBLE
  Test: GABA-A α1 subunit knockout in amygdala LA
  Discrimination Index: 0.87 (very high)
  Timeline: 3 years
  See "Critical Test" card for details

Resolution Pathway:
  1. Execute critical test (α1 KO) → discriminate NMDA vs. GABA hypothesis
  2. Follow-up molecular experiments → specify which receptor subtypes matter
  3. Cross-species replication → test in primates, humans

Current Recommendation:
  - Use Theory B (GABA-mediated) as working hypothesis (higher coherence)
  - Design future research targeting critical test
  - Plan for molecular mechanism gap (high priority research frontier)

---

Case 2: Fear Generalization Basis (Stimulus Similarity vs. Context Confusion)

[Similar structure...]

---

General Principle:
Underdetermination is temporary, not permanent. Every case here has a clear path to resolution
through targeted critical tests. The timeline varies (1–5 years depending on feasibility).

The page helps you:
1. See which theories are currently favored by coherence
2. Understand why they tie (shared evidence base)
3. Plan future experiments to break ties
```

#### Data Model (Backend)

```json
{
  "card_type": "underdetermination_alert",
  "cases": [
    {
      "case_id": "underdetermin_fear_extinction",
      "phenomenon": "Fear Extinction Learning",

      "competing_theories": [
        {
          "theory_id": "theory_a",
          "theory_name": "NMDA-dependent consolidation",
          "coherence_score": 0.68
        },
        {
          "theory_id": "theory_b",
          "theory_name": "GABA-mediated inhibition",
          "coherence_score": 0.78
        }
      ],

      "observational_status": "tied",
      "observational_evidence_count": 4,

      "coherence_comparison": {
        "favored_theory": "theory_b",
        "coherence_difference": 0.10,
        "reason_for_preference": "Broader explanatory scope; stronger background coherence"
      },

      "interventionist_divergence": {
        "strength": "strong",
        "theory_a_intervention": {
          "intervention": "Block NMDA receptors",
          "predicted_outcome": "Extinction consolidation fails"
        },
        "theory_b_intervention": {
          "intervention": "Block NMDA receptors",
          "predicted_outcome": "Extinction proceeds normally"
        }
      },

      "critical_test": {
        "test_id": "ct_gaba_a_alpha1_knockout",
        "test_name": "GABA-A α1 Subunit Knockout in LA",
        "status": "identified_and_feasible",
        "discrimination_index": 0.87,
        "timeline_years": 3
      },

      "resolution_pathway": [
        {
          "step": 1,
          "action": "Execute critical test (α1 KO)",
          "outcome": "Discriminate NMDA vs. GABA hypothesis",
          "timeline": "3 years"
        },
        {
          "step": 2,
          "action": "Molecular experiments on winning theory",
          "outcome": "Specify receptor subtypes, gene expression, protein binding",
          "timeline": "3–4 years"
        },
        {
          "step": 3,
          "action": "Cross-species replication",
          "outcome": "Confirm in primates, humans",
          "timeline": "5–8 years"
        }
      ],

      "current_recommendation": {
        "working_hypothesis": "theory_b",
        "reasoning": "Higher coherence; fits more data domains",
        "caveat": "Preference is tentative; critical test will be decisive"
      }
    }
  ]
}
```

#### Effort: Medium (2–3 weeks)

**Tasks**:
- [ ] Enhance data model to include coherence comparison
- [ ] Implement interventionist divergence assessment
- [ ] Link to critical tests (reference by ID)
- [ ] Create resolution pathway visualization (timeline)
- [ ] Populate data for 2–3 cases (content team)
- [ ] QA: Verify coherence scores match Theory Comparison card

---

## Overall Implementation Timeline

### Phase 1: Foundation (Weeks 1–2)
- [ ] Update Neural Frameworks card (minor)
- [ ] Set up data infrastructure for revised cards
- [ ] Design and test UI components (pyramid, coherence scores, etc.)

### Phase 2: Core Cards (Weeks 3–8)
- [ ] Implement Theory Comparison card (major)
- [ ] Implement Mechanism Chain card (major)
- [ ] Integrate coherence scoring backend
- [ ] QA on cards 1–2

### Phase 3: Advanced Cards (Weeks 9–12)
- [ ] Implement Critical Test card (major)
- [ ] Implement Underdetermination Alert card (revised)
- [ ] Integrate intervention-targeting logic
- [ ] QA on cards 3–5

### Phase 4: Content and Deployment (Weeks 12+)
- [ ] Populate mechanism chain data for all phenomena
- [ ] Populate critical test data with domain experts
- [ ] User testing and iteration
- [ ] Deploy

---

## Success Metrics

### Usability
- [ ] Users can identify which theories compete at which mechanistic level
- [ ] Users understand why underdetermined theories tie (coherence explanation)
- [ ] Users know which critical tests would resolve underdetermination
- [ ] Users can navigate between cards intuitively (Theory Comparison → Mechanism → Critical Test)

### Epistemic Quality
- [ ] Coherence scores are explained transparently (not black-box)
- [ ] Schema gaps are marked and acknowledged (honest uncertainty)
- [ ] Interventionist predictions are testable and specific
- [ ] Discrimination indices reflect realistic predictive power

### Content Completeness
- [ ] All 19 research fronts have at least a Theory Comparison card
- [ ] Top 5 phenomena have full mechanism chain schemata
- [ ] Top 3 phenomena have critical test specifications
- [ ] All underdetermined cases are tracked and updated quarterly

---

## Risk Mitigation

### Risk 1: Coherence Scoring Too Complex
**Mitigation**: Provide "quick explanation" and "detailed methodology" views. Allow users to see the formula but not require understanding it.

### Risk 2: Too Much Information Per Card
**Mitigation**: Use progressive disclosure (expandable sections, detail views). Main card shows summary; click to expand for details.

### Risk 3: Content Maintenance Burden
**Mitigation**: Create data templates and populate with domain experts quarterly. Automate coherence recalculation when evidence changes.

### Risk 4: Critical Tests May Become Outdated
**Mitigation**: Flag tests with "last updated" dates. Mark tests as completed/ongoing/pending. Add quarterly expert review.

---

## Next Steps After Approval

1. **Design Review**: Present UI mockups to domain experts (panel members)
2. **Data Infrastructure**: Build backend for revised data models
3. **Component Development**: Implement React components (pyramid, coherence, etc.)
4. **Content Population**: Begin with top 3 phenomena; expand systematically
5. **User Testing**: Early access program with cognitive scientists
6. **Iteration and Refinement**: Weekly integration testing and refinement

---

## Questions for Stakeholders

1. **Timeline**: Is 10–12 weeks realistic given current development capacity?
2. **Content**: Who will populate mechanism chain and critical test data?
3. **Maintenance**: What is the plan for quarterly updates (new evidence, new tests)?
4. **Validation**: Should panel members review populated data before deployment?

