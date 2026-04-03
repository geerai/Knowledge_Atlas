# Expert Panel Summary: Quick Reference

**Date**: 2026-04-03
**Full Report**: `EXPERT_PANEL_THEORY_EXPLORER_DESIGN_2026-04-03.md`
**Implementation Guide**: `IMPLEMENTATION_GUIDE_THEORY_EXPLORER_2026-04-03.md`

---

## The Five Panelists and Their Core Insights

### 1. Carl Craver (Mechanistic Explanation)
**Key Problem**: Linear mechanism chains conflate ontological levels.

**Solution**: Multi-level pyramids showing:
- Behavioral → Circuit → Synaptic → Molecular levels
- Explicit constitutive vs. etiological relations
- Level of explanation for each theory

**Implementation**: Replace linear chains with pyramid diagrams; add "Mechanistic Level" column to theory tables.

---

### 2. Peter Machamer (Entity-Activity Semantics)
**Key Problem**: Listing entities (amygdala, dopamine) without specifying what they *do*.

**Solution**: Always specify activities connecting entities:
- "Amygdala **encodes** threat salience" not just "Amygdala"
- "vmPFC **inhibits** amygdala output" not just "vmPFC → Amygdala"

**Implementation**: Entity-activity pair notation in all mechanism descriptions; create activity lexicon (encode, inhibit, gate, modulate, etc.).

---

### 3. Lindley Darden (Mechanism Discovery)
**Key Problem**: Mechanisms are presented as finished when they're typically skeletal with gaps.

**Solution**: Mark gaps explicitly with schema-gap notation:
- GREEN: Empirically confirmed
- YELLOW: Tentative (how-possibly)
- RED: Known gap (HOW?)
- GRAY: Not tested yet

**Implementation**: Color-coded pyramid levels; distinguish how-possibly from how-actually schemas; add empirical support table.

---

### 4. Paul Thagard (Explanatory Coherence)
**Key Problem**: When theories tie on evidence, no principled way to rank them.

**Solution**: Compute ECHO-style coherence scores:

```
Coherence = (Breadth × 0.3) + (Depth × 0.3) + (Background Fit × 0.2) + (Simplicity × 0.2)
```

Where:
- **Breadth** = how many domains explained (fear, learning, attention, etc.)
- **Depth** = empirical support × mechanistic detail
- **Background Fit** = coherence with established literature
- **Simplicity** = inverse(# causal entities)

**Implementation**: Display coherence scores with transparent breakdowns; explain why one theory is favored when tied on evidence.

---

### 5. James Woodward (Interventionist Causation)
**Key Problem**: Theory comparison ignores prediction differences *under intervention*.

**Solution**: For each theory, show:
- Observational predictions (what we see in nature)
- Interventionist predictions (what would happen if we intervene)
- Specific interventions that distinguish theories

**Implementation**: "Interventionist Prediction" column in theory tables; target-specific critical tests.

---

## What Each Card Should Show

### Card 1: Neural Frameworks
**Add**: Domain count, mechanism gallery links

---

### Card 2: Theory Comparison (MAJOR REVISION)
**Show for each theory**:

| What | Craver | Machamer | Darden | Thagard | Woodward |
|------|--------|----------|--------|---------|----------|
| **Entities & Activities** | ✓ (what entities?) | ✓✓ (what do they do?) | — | — | — |
| **Mechanistic Level** | ✓✓ (circuit? molecular?) | — | — | — | — |
| **Empirical Support** | — | — | ✓ (# papers, confidence) | — | — |
| **Coherence Score** | — | — | — | ✓✓ (with breakdown) | — |
| **Explanatory Scope** | — | — | ✓ (which domains?) | ✓ (breadth) | — |
| **Interventionist Prediction** | — | — | — | — | ✓✓ (test this) |

---

### Card 3: Mechanism Chain (MAJOR REVISION)
**Show**:
- Multi-level pyramid (Behavioral → Circuit → Synaptic → Molecular)
- Activities connecting entities
- Schema-gap markers (color-coded)
- Empirical support per level
- Interventionist properties (what breaks the mechanism?)

---

### Card 4: Critical Test (MAJOR REVISION)
**Show for each test**:
- **Mechanistic level** it targets (Craver)
- **Entities and activities** it tests (Machamer)
- **Causal bottleneck** it addresses (Craver + Woodward)
- **Theory-specific predictions** (Thagard + Woodward)
- **Discrimination index** (0.0–1.0; how cleanly does outcome favor one theory?)
- **Coherence impact** (how much do test outcomes change coherence scores?)
- **Interventionist specificity** (is this intervention precisely targeted?)

**Example**:
```
Test: GABA-A α1 knockout in amygdala LA

Theory A predicts: Extinction BLOCKED (p > 0.85)
Theory B predicts: Extinction proceeds normally (p > 0.80)

Discrimination Index: 0.87 (very high ← either outcome discriminates)
Coherence Impact: 0.53 (high ← test significantly updates coherence landscape)

→ This is a CRITICAL TEST (high discrimination, high coherence impact)
```

---

### Card 5: Warrant Structure
**No changes** — already epistemologically sound.

---

### Card 6: Underdetermination Alert (REVISED)
**Show for each underdetermined case**:
- Which theories tie and why
- Coherence comparison (which is preferred?)
- **Interventionist divergence** (what opposite predictions distinguish them?)
- Which critical test would resolve the underdetermination
- Timeline to resolution

---

## Three Key Principles (All Five Panelists Agree)

### Principle 1: Mechanisms Have Multiple Levels
- Behavioral, circuit, synaptic, molecular
- Theories can operate at different levels (they complement rather than compete)
- Mark which level each theory explains

### Principle 2: Underdetermination is Temporary
- When theories tie now, identify critical tests that would break the tie
- Give timeline to resolution (1–5 years depending on feasibility)
- Guide research toward experiments that matter

### Principle 3: Transparency About Gaps
- Mark explicitly what is known vs. unknown
- Distinguish how-possibly schemas (candidates) from how-actually schemas (confirmed)
- Don't present skeletal mechanisms as finished

---

## What the Panel Accomplished

**Disagreements**: Healthy tension between different intellectual traditions
- Craver: Focus on ontological levels
- Machamer: Focus on activities
- Darden: Focus on empirical support and gaps
- Thagard: Focus on coherence reasoning
- Woodward: Focus on intervention

**Resolution**: All five perspectives are **complementary**, not contradictory. The redesigned system incorporates all five.

**Result**: A home page that:
1. Helps users understand mechanisms at multiple scales (Craver)
2. Shows them what entities *do*, not just what they are (Machamer)
3. Makes explicit what is known vs. unknown (Darden)
4. Provides principled ranking of underdetermined theories (Thagard)
5. Guides them toward experiments that truly discriminate (Woodward)

---

## Implementation Priority

| Phase | Card | Effort | Timeline |
|-------|------|--------|----------|
| 1 | Neural Frameworks | Low | Week 1 |
| 2 | Theory Comparison | High | Weeks 2–4 |
| 2 | Mechanism Chain | High | Weeks 2–4 |
| 3 | Critical Test | Very High | Weeks 5–8 |
| 3 | Underdetermination Alert | Medium | Weeks 3–4 |
| — | Warrant Structure | None | — |

**Total**: 10–12 weeks for full implementation

---

## For Content Creators: The Checklist

Every mechanism description should include:

- [ ] Multi-level structure (behavioral down to molecular)
- [ ] Entity-activity pairs (what does each entity *do*?)
- [ ] Schema-gap markers (known vs. unknown vs. tentative)
- [ ] Empirical support (# papers, confidence level, key references)
- [ ] Interventionist properties (what interventions test this mechanism?)
- [ ] Mechanistic level specification (which theories operate at same level?)

Every theory comparison should include:

- [ ] Coherence score with transparent breakdown
- [ ] Explanatory scope matrix (which domains each theory addresses)
- [ ] Mechanistic level (circuit? molecular?)
- [ ] Interventionist predictions (opposite predictions under specific intervention?)
- [ ] Link to critical tests (which tests would discriminate them?)

Every critical test should include:

- [ ] Mechanistic level it targets
- [ ] Theory-specific predictions (and their probabilities)
- [ ] Discrimination index (0.0–1.0)
- [ ] Coherence impact (how much would outcomes change theory landscape?)
- [ ] Causal bottleneck (what specific mechanism does this test?)
- [ ] Specificity of intervention (how targeted is it?)
- [ ] Feasibility and timeline

---

## Key References (For Implementers)

### On Multi-Level Mechanisms
Craver, C. F. (2007). *Explaining the Brain*. Oxford University Press.

### On Entities and Activities
Machamer, P., Darden, L., & Craver, C. F. (2000). Thinking about mechanisms. *Philosophy of Science* 67(1).

### On Schema Gaps
Darden, L. (2006). *Reasoning in Biological Discoveries*. Cambridge University Press.

### On Coherence Scoring
Thagard, P. (1992). *Conceptual Revolutions*. Princeton University Press.

### On Interventionist Causation
Woodward, J. (2003). *Making Things Happen*. Oxford University Press.

---

## Questions to Ask During Implementation

1. **For Craver's framework**: Which mechanistic level is each theory making claims at? Are they competing or complementary?

2. **For Machamer's framework**: What *activities* connect these entities? What would break the mechanism?

3. **For Darden's framework**: What is the current empirical support for each step? Where are the gaps? Is this how-possibly or how-actually?

4. **For Thagard's framework**: How broadly does this theory explain? What is its coherence with background literature? How does it rank vs. competitors on multiple criteria?

5. **For Woodward's framework**: What opposite predictions would distinguish these theories if we intervened? How specific can we be about the target?

---

## Success Looks Like

Users report:
- "I can see why these theories are competing vs. complementary"
- "I understand which parts of the mechanism are proven vs. speculative"
- "I know what experiments would settle the dispute"
- "I can see the path forward for research"
- "The page doesn't hide uncertainty; it makes it productive"

---

**Status**: PANEL REPORT FINAL — Ready for Implementation
**Next Step**: Design and development team reviews specifications, begins Phase 1
