# Expert Panel Review: Knowledge Atlas Theory Explorer Home Page Design

**Date**: 2026-04-03
**Convened by**: David Kirsh, UCSD Cognitive Science
**Panel Members**: Carl Craver, Peter Machamer, Lindley Darden, Paul Thagard, James Woodward
**Subject**: Design of the THEORY/MECHANISM EXPLORER home page for the Knowledge Atlas (~1,900 claims, ~4,810 edges, 7 warrant types, 10 Tier-1 neural frameworks)

**Status**: PANEL REPORT — Recommendations for implementation

---

## Executive Summary

The proposed Knowledge Atlas theory explorer design presents a coherent information architecture for guiding users through competing theoretical accounts of cognitive/neural phenomena. The panel endorses the **6-card system** and the **OIIEA journey** (Orient → Inspect → Explain → Evaluate → Act), but identifies three critical gaps in how mechanisms, theory comparison, and critical tests are represented.

**Key Panel Findings**:

1. **Mechanism representation conflates ontological levels** — The linear "env feature → neural substrate → cognitive effect → behavioral outcome" chain omits the crucial distinction between constitutive and etiological mechanisms (Craver). The design needs explicit **multi-level architecture** with activities connecting entities (Machamer).

2. **Theory comparison inadequately addresses underdetermination** — The proposed Theory Comparison card presents evidence balance qualitatively. The panel recommends **formal coherence scoring** (Thagard) alongside qualitative narrative, and explicit **transparency about explanatory scope trade-offs** (Darden).

3. **"Critical test" is underspecified** — The Critical Test card identifies high-priority discriminating experiments, but does not clarify the philosophical basis for what makes an experiment "critical." The panel recommends integrating **interventionist semantics** (Woodward) into test design, distinguishing observational from interventionist discrimination.

**Consensus Recommendations**:

- Replace linear mechanism chains with **explicit multi-level diagrams** showing constitutive and etiological relationships, with activities as relata
- Implement **ECHO-style coherence scoring** for theory comparison alongside qualitative evidence summaries
- Redesign the Critical Test card to emphasize **interventionist structure** and discriminatory capacity under different causal models
- Add a **Mechanism Schema gallery** distinguishing "how-possibly" from "how-actually" accounts (Darden)
- Create **transparency footnotes** on every theory comparison explaining which domains each theory covers and which it excludes

**Implementation Priority**: High (affects epistemic credibility of the entire system)

---

## The Proposed Design

### Current Card System

| Card Type | Purpose | Risk Profile |
|-----------|---------|--------------|
| Neural Frameworks | Orient users to 10 Tier-1 frameworks, article counts, grounding scores | Low (descriptive) |
| Theory Comparison | Present competing accounts, evidence balance, discriminating predictions | **HIGH** (underdetermined) |
| Mechanism Chain | Environmental feature → neural substrate → cognitive effect → behavioral outcome | **HIGH** (ontological confusion) |
| Critical Test | Highest-priority discriminating experiment | **HIGH** (philosophically underspecified) |
| Warrant Structure | Distribution of 7 warrant types across topics | Medium (interpretive) |
| Underdetermination Alert | Cases where multiple theories fit equally | Low (honest labeling) |

### Governing Question

"How do the competing theoretical accounts explain these effects, and what experiment would distinguish between them?"

**Panel Assessment**: The question is well-framed. The implementation vehicles are not.

---

## Individual Panel Positions

### Panel Member 1: Carl Craver (Mechanistic Explanation in Neuroscience)

**Position**: Mechanisms are constituted of entities engaged in activities, organized at multiple ontological levels. The proposed mechanism chain conflates constitutive and etiological relationships.

#### Three Key Questions: Craver's Answers

**(a) How should mechanism be represented?**

Linear chains are dangerous. A complete mechanistic explanation requires:
- **Constitutive relations**: "The amygdala's response TO danger is constituted by population coding in the lateral nucleus plus feedback to the cortex"
- **Etiological relations**: "The stimulus evokes an amygdala response BECAUSE the visual cortex detects threat-relevant features and projects to the amygdala"

The current design suggests: stimulus → amygdala activation → fear response → freezing behavior. This mixes levels. The amygdala activation is constituted by neural activity at a finer scale; the stimulus causes (but does not constitute) the amygdala response; the fear response is constituted by affective-cognitive-motor coordination across circuits.

**Recommendation**: Multi-level hierarchical diagrams showing:
- **Level 1 (Macro)**: Behavioral/cognitive outcome (e.g., fear extinction learning)
- **Level 2 (Meso-neural)**: Integrative neural circuits (e.g., vmPFC-amygdala inhibition)
- **Level 3 (Micro-neural)**: Local computations (e.g., GABA release, receptor binding)
- **Causal bridges**: Etiological arrows linking levels; constitutive decomposition within each level

Example structure for fear extinction:
```
[Behavioral Level]
  Fear-to-CS decreased after extinction training
     ↑ (etiological cause)
[Circuit Level]
  vmPFC → amygdala lateral nucleus (inhibitory)
     constituted by:
[Synaptic Level]
  Pyramidal neurons (vmPFC) → interneurons (LA)
     constituted by:
[Molecular Level]
  GABA receptor binding → hyperpolarization
```

**(b) How should theory comparison handle underdetermination?**

Do not present competing theories as though they operate at the same level. Underdetermination is often an artifact of level confusion. If Theory A explains fear extinction at the circuit level and Theory B explains it at the systems level, they are not truly competing—they are complementary.

The page should ask: "At what level of mechanistic detail is each theory making claims?" Theories that localize at different scales can both be true. Theories that make incompatible claims at the *same scale* are genuinely competing.

**Recommendation**: Include a "Level of Explanation" column in the Theory Comparison card:

| Theory | Neural Substrate (Level) | Evidence | Competing With | Scope |
|--------|------------------------|----------|-----------------|-------|
| Theory A | Amygdala lateral nucleus synaptic plasticity | 4 papers | Only Theory B (same level) | Fear extinction in rodents |
| Theory B | vmPFC-amygdala circuit rebalancing | 3 papers | Only Theory A (same level) | Fear extinction (multi-species) |
| Theory C | Hippocampal context re-encoding | 2 papers | None (different level) | Contextual fear renewal |

**(c) What makes a critical test genuinely critical?**

A critical test must target an etiological difference at the *same mechanistic level*. Many proposed discrimination experiments actually test different levels (e.g., optogenetic silencing of vmPFC tests circuit-level role; fMRI of vmPFC tests circuit-level activation; molecular assays test synaptic level). These are complementary, not discriminatory.

**Critical Test**: An intervention that, under one theory, produces outcome X, and under the competing theory, produces outcome Y, when both are tested at the same mechanistic level.

Example: Knock out the gene for a specific GABA receptor subtype in the amygdala lateral nucleus. Theory A predicts fear extinction is abolished; Theory B predicts it is preserved (because alternative pathways substitute). This is a critical test *for that mechanistic level*.

#### Craver's Critique of the Proposed Design

**Strengths**:
- The Mechanism Chain card recognizes that multi-level explanation is necessary
- The Critical Test card seeks to discriminate empirically

**Weaknesses**:
1. **Linear chains hide ontology**: The "feature → substrate → effect → outcome" structure does not distinguish constitutive from etiological relations. A reader cannot tell whether the chain is describing what explains what or what consists of what.
2. **No explicit level marking**: Without flagging the mechanistic level of each claim, the page will present multiple theories as if they are competing when they merely operate at different scales.
3. **Critical Test card is atheoretical**: It names high-priority experiments but does not connect experiments to the specific mechanistic claims they test. A critical test for the circuit level may be irrelevant to a molecular-level claim.

**Constructive Recommendations from Craver**:

1. Replace mechanism chains with **multi-level pyramids** (meso-neural → micro-neural → molecular, or behavioral → circuit → synaptic)
2. Add a **"Mechanistic Level" column** to every theory comparison table, defaulting to "Circuit level" or "Systems level"
3. Redesign the Critical Test card to include:
   - Which mechanistic level the test targets
   - Which theory makes predictions at that level
   - What intervention disconfirms one theory but not the other *at that level*
4. Add explicit **constitutive-vs.-etiological legends** to every multi-level diagram

---

### Panel Member 2: Peter Machamer (Activities and Entities in Mechanisms)

**Position**: Mechanisms are composed of entities (objects, structures) that engage in activities (processes, operations). Complete mechanistic explanation requires both. The current design lists entities without their activities.

#### Three Key Questions: Machamer's Answers

**(a) How should mechanism be represented?**

The current proposal names entities: amygdala, cortisol, dopamine receptor, etc. It does not name the *activities* connecting them. What does the amygdala *do*? Encode threat salience. What does cortisol *do*? Mobilize metabolic resources. What does dopamine *do*? Flag prediction error. The activities are doing the mechanistic work; without them, the chain is inert.

**Recommendation**: Every mechanism diagram should have:
- **Entities** (boxes): amygdala, vmPFC, dopaminergic neurons
- **Activities** (arrows with labels): "encodes," "inhibits," "modulates," "gates," "resets," "binds," "downregulates"

This is not merely linguistic decoration. Naming the activity specifies what role the entity plays in the mechanism. Saying "the amygdala encodes threat salience" is mechanistically informative in a way that simply naming "amygdala" is not.

Example mechanism (properly specified with activities):

```
Visual stimulus (feature)
    ↓ (is detected by)
Sensory cortex
    ↓ (projects to)
Amygdala lateral nucleus
    ↓ (encodes threat salience via)
Population coding in pyramidal cells
    ↓ (drives)
Amygdala output to brainstem nuclei
    ↓ (triggers via)
ACh release
    ↓ (activates)
Sympathetic autonomic response
    ↓ (produces)
Freezing behavior
```

Without the activities (in parentheses), the chain is just a list of anatomical connections.

**(b) How should theory comparison handle underdetermination?**

Two theories are genuinely competing only if they specify **different activities** connecting the same entities, or specify **different entities** executing the same activity.

Example of genuine competition:
- Theory A: Amygdala *inhibits* mPFC during threat (activity: inhibition)
- Theory B: Amygdala *gates* mPFC signals rather than inhibiting them (activity: gating)

Example of false competition:
- Theory A: Fear memory consolidation requires protein synthesis
- Theory B: Fear memory consolidation requires transcription
(These are not competing; protein synthesis requires upstream transcription. They describe different temporal stages of the same activity: "encoding into stable neuroplasticity")

**Recommendation**: The Theory Comparison card should include an "Activity Specification" row:

| Theory | Entities Involved | Key Activities | Evidence | Conflict? |
|--------|------------------|-----------------|----------|-----------|
| Threat Sensitization (TSM) | Amygdala, ACC, vmPFC | Amygdala amplifies; ACC computes salience; vmPFC inhibits | 5 papers | No (complementary) |
| Fear Generalization (FGM) | Amygdala, hippocampus, cortex | Amygdala gates hippocampal context binding | 3 papers | Competes on gating vs. inhibition |

**(c) What makes a critical test genuinely critical?**

A critical test must dissociate the activities, not just the entities. If Theory A says amygdala *inhibits* extinction learning and Theory B says it *gates* extinction learning, a test that simply removes the amygdala confirms neither—you've removed the entity, not tested the activity.

**Critical test for this case**: Optogenetically activate the amygdala during extinction in a pattern that mimics "gating" behavior (brief pulses synchronous with stimulus presentations) vs. patterns that mimic "inhibition" (tonic suppression). If gating-pattern activations preserve extinction but inhibition-pattern activations block it, you've tested the activity directly.

#### Machamer's Critique of the Proposed Design

**Strengths**:
- The Mechanism Chain card structure can easily be extended to include activities

**Weaknesses**:
1. **Entities without activities are incomplete**: The current proposal lists neural regions and neurotransmitters but does not specify what computational or neural operation each executes. This leaves the mechanism underspecified.
2. **No activity-level theory discrimination**: Without explicit activity labels, the page cannot help users see whether theories disagree about what entities *do* or merely about which entities are *involved*.
3. **Missed opportunity for precision**: Adding activity labels is simple and dramatically improves epistemic clarity.

**Constructive Recommendations from Machamer**:

1. **Extend the Mechanism Chain template**:
   ```
   [Entity A] --[activity: X]--> [Entity B] --[activity: Y]--> [Outcome]
   ```
   Instead of: amygdala → cortisol → fear response
   Use: Amygdala (encodes threat) → hypothalamus (releases CRH) → pituitary (secretes ACTH) → adrenal cortex (releases cortisol) → lymphocytes (downregulate IL-2) → reduced immune response

2. **Create an "Activity Lexicon" for the domain**: Build a curated list of neural/cognitive activities (encode, inhibit, gate, modulate, bind, consolidate, etc.) with brief definitions. Make it searchable and filterable on the Theory Explorer page.

3. **Add an activity-level conflict detector to the Theory Comparison card**: Flag when two theories attribute *different* activities to the same entity or pathway.

4. **Revise the Critical Test card** to ask: "What intervention would reveal the activity that distinguishes these theories?" rather than "What experiment has the highest priority?"

---

### Panel Member 3: Lindley Darden (Mechanism Discovery and Theory Structure)

**Position**: Mechanism schemas are scaffolds for discovery. Complete schemas are less common than skeletal or partial schemas with explicit gaps. The page should distinguish "how-possibly" mechanisms (still under construction) from "how-actually" mechanisms (empirically demonstrated).

#### Three Key Questions: Darden's Answers

**(a) How should mechanism be represented?**

Do not present mechanisms as though they are finished. In most cases, they are not. The typical state of a mechanism during scientific inquiry is:
- **Complete at some levels**, missing at others
- **Sketched at the macro level**, detailed at the meso level, unknown at the micro level
- **Functional in some contexts**, broken or missing in others

The page should expose this honestly by using a **schema-gap notation**:

```
Stimulus (known)
  ↓ [HOW?]
Sensory cortex processes feature
  ↓ [known: projects to amygdala]
Amygdala [activation mechanism: ???]
  ↓ [known: output to brainstem]
Autonomic response
  ↓ [known]
Freezing behavior
```

The `[HOW?]` and `[???]` notations indicate epistemic gaps. This is not a weakness in the presentation—it is honest science communication.

**Recommendation**: Distinguish three mechanism states:

1. **"How-possibly" schema**: The entities and rough causal flow are known; the detailed activities are not yet specified. Example: "Amygdala output possibly suppresses fear extinction via inhibition of vmPFC, but the synaptic mechanism is unspecified."

2. **"How-actually-at-this-level" schema**: The mechanism is empirically demonstrated at a specified mechanistic level. Example: "Fear extinction is actually achieved at the circuit level via vmPFC pyramidal neurons inhibiting amygdala lateral nucleus via GABA-mediated synapses (demonstrated via optogenetics in rodents; not yet confirmed in humans)."

3. **"How-still-unknown" schema**: The entities are named but the mechanism is not specified. Example: "The precise molecular mechanism by which CREB phosphorylation in the amygdala enables fear memory consolidation remains unknown."

These should be visually distinct on the page. A user browsing the Mechanism Chain card should be able to see at a glance which parts of the chain are well-understood versus provisional versus unknown.

**(b) How should theory comparison handle underdetermination?**

Underdetermination is often *temporary*, not permanent. Two theories may appear equally supported now, but future experiments may favor one. The page should not treat underdetermination as a dead-end; instead, it should identify what experiments would *reduce* underdetermination.

Additionally, underdetermination is often *asymmetric across domains*. Theory A may fully explain Domain 1 but be silent on Domain 2; Theory B may explain Domain 2 well but be silent on Domain 1. The page should not rank them as "equally supported"—they have different explanatory footprints.

**Recommendation**: The Theory Comparison card should include:

1. **Explanatory scope matrix**: Which domains does each theory address?

| Theory | Threat Detection | Fear Extinction | Generalization | Fear Renewal | Grounded in |
|--------|-----------------|-----------------|-----------------|--------------|------------|
| Threat Sensitization Model | ✓ Strong | Partial | ✗ Silent | ✗ Silent | 12 empirical papers |
| Contextual Fear Theory | Partial | ✓ Strong | ✓ Strong | ✓ Strong | 18 empirical papers |

This makes clear that these are not competing for the same explanatory job; they have different domains of strength.

2. **Underdetermination reduction roadmap**: For domains where two theories tie, what experiments would break the tie?

| Domain | Theory A | Theory B | Prediction Difference | Discriminating Test |
|--------|----------|----------|----------------------|---------------------|
| Extinction | Evidence: 3 papers | Evidence: 4 papers | Theory A: amygdala→vmPFC suppression critical; Theory B: hippocampal context binding primary | Reversible inactivation of vmPFC during extinction training in context-naive vs. context-exposed rats |

**(c) What makes a critical test genuinely critical?**

A critical test is one that has a high probability of discriminating between theories *given that one of them is wrong*. A test is not critical simply because it has high priority or high visibility. It is critical because failure of the test under one theoretical prediction carries maximal diagnostic information.

The page should rate tests by their **discrimination index**: How cleanly does the outcome favor one theory over the other?

Example:

- **High discrimination**: Theory A predicts the test output has property X with p > 0.95; Theory B predicts it lacks X with p > 0.95. Observing X clearly favors A.
- **Medium discrimination**: Theory A predicts p(X) > 0.7; Theory B predicts p(X) < 0.4. Some overlap; a positive result is informative but not decisive.
- **Low discrimination**: Both theories can accommodate the likely outcome; the test is not critical yet.

#### Darden's Critique of the Proposed Design

**Strengths**:
- The Mechanism Chain and Theory Comparison cards can be extended to represent multiple explanatory schemes
- The Underdetermination Alert card is honest labeling

**Weaknesses**:
1. **No schema-gap notation**: The page presents mechanisms as finished even when they are skeletal. This misleads users about the actual state of knowledge.
2. **Theory comparison lacks scope information**: Presenting two theories side-by-side without indicating "Theory A is silent on Domain X" obscures the true relationship between them (complementary vs. competing).
3. **Critical Test card lacks discrimination metrics**: "Highest-priority" is not the same as "most informative." The page should highlight tests that would most decisively distinguish theories.
4. **No how-possibly vs. how-actually distinction**: Users cannot tell which mechanisms are empirically confirmed versus which are candidate schemas still under investigation.

**Constructive Recommendations from Darden**:

1. **Add visual schema-gap markers**: Use `[HOW?]` or `[???]` to flag unknown steps in mechanism chains. Color-code by knowledge state:
   - **Green**: empirically confirmed at this level
   - **Yellow**: tentative (how-possibly schema)
   - **Red**: unknown gap
   - **Gray**: untested but theoretically predicted

2. **Extend the Mechanism Chain card with an "Empirical Support" column**:
   | Step | Entity/Activity | Evidence Level | Key Papers |
   |------|-----------------|-----------------|------------|
   | 1 | Stimulus→Cortex | Strong (20+ papers) | Smith et al. 2020, Jones et al. 2022 |
   | 2 | Cortex→Amygdala | Strong (15+ papers) | Brown et al. 2019 |
   | 3 | Amygdala [encoding mechanism] | Weak (3 papers, how-possibly) | Lee et al. 2021 |

3. **Create a "Mechanism Schema Gallery"** separate from the home page, showing full how-possibly and how-actually accounts with their gaps explicitly marked.

4. **Redesign Theory Comparison to include scope matrix** (as described above).

5. **Add a discrimination index to the Critical Test card**:
   ```
   Critical Test: Optogenetic silencing of vmPFC during extinction training

   Theory A prediction: Extinction abolished (p > 0.90)
   Theory B prediction: Extinction proceeds normally (p > 0.85)
   Discrimination Index: 0.88 (high)
   ```

---

### Panel Member 4: Paul Thagard (Explanatory Coherence and ECHO Model)

**Position**: Theory comparison should be formalized using coherence measures. ECHO (Explanatory Coherence by Harmony Optimization) provides a computational framework for weighing evidence, contradictions, and breadth of explanation.

#### Three Key Questions: Thagard's Answers

**(a) How should mechanism be represented?**

From a coherence perspective, a mechanism is valuable insofar as it coheres with:
- **Empirical evidence** (explanatory relations)
- **Other mechanisms** (mutual coherence)
- **Background knowledge** (coherence with established theory)

The current linear chain representation is static; it does not show how a proposed mechanism *fits* with competing mechanisms or evidence. A mechanism that explains the data perfectly but contradicts established neurobiology is coherent in one way but incoherent in another.

**Recommendation**: Represent mechanisms not as isolated chains but as **coherence networks**. Each mechanism should show:
1. What evidence it explains
2. What evidence it fails to explain
3. What other theories it coexists with coherently
4. What other theories it contradicts

This can be visualized as a graph:
```
Evidence node 1 ----explains----> Mechanism A (coherence weight: 0.85)
Evidence node 2 ----partially----> Mechanism A (weight: 0.60)
Evidence node 3 ----contradicts---> Mechanism A (weight: -0.70)
Mechanism A ----consistent with---> Background Theory X (weight: 0.75)
Mechanism A ----contradicts-------> Competing Mechanism B (weight: -0.60)
```

The thickness and color of edges should reflect coherence strength. A mechanism with strong coherence links and few contradictions is epistemically preferable to one with spotty evidence and contradictions, even if both explain the core phenomenon.

**(b) How should theory comparison handle underdetermination?**

Underdetermination is an opportunity to apply coherence reasoning. When two theories explain the data equally well, **favor the theory with higher overall coherence**: breadth of explanation, coherence with background knowledge, and minimal contradiction with adjacent domains.

ECHO-style comparison would ask:

1. **Explanatory breadth**: How many phenomena does each theory explain (not just explain equally well)?
2. **Explanatory depth**: How deeply does each theory explain? (Does it explain why evidence, or merely accommodate it?)
3. **Coherence with background**: How well does each theory fit with established knowledge in adjacent domains?
4. **Internal coherence**: Does each theory's core mechanisms align with each other, or are there internal tensions?
5. **Simplicity**: All else equal, does one theory appeal to fewer causal entities or mechanisms?

**Recommendation**: Compute a **Coherence Score** for each theory using ECHO. This is not a number that should dominate the page, but it should be available and explainable:

```
Theory Comparison: Fear Extinction

Threat Sensitization Model
  Explanatory breadth: 3/6 domains covered
  Coherence with background: 0.72 (good)
  Internal coherence: 0.81 (strong)
  Simplicity: 3 core mechanisms
  OVERALL COHERENCE SCORE: 0.68

Contextual Fear Theory
  Explanatory breadth: 5/6 domains covered
  Coherence with background: 0.85 (strong)
  Internal coherence: 0.79 (strong)
  Simplicity: 4 core mechanisms
  OVERALL COHERENCE SCORE: 0.78

Result: CFT is coherence-favored, but TSM is not incoherent. Underdetermination is not eliminated but is weighted.
```

This gives users a principled way to think about trade-offs when theories tie on empirical evidence.

**(c) What makes a critical test genuinely critical?**

A critical test is one whose outcome **maximally changes the coherence scores** of competing theories. A test is critical if:
- Outcome X strongly increases coherence of Theory A and decreases coherence of Theory B
- Outcome Y does the opposite

If both outcomes (X or not-X) preserve coherence scores roughly equally, the test is not critical—it is merely high-priority.

**Recommendation**: Use the ECHO framework to compute **coherence impact** for each proposed test. This is the magnitude of coherence change if the test outcome goes one way vs. another:

```
Critical Test: Optogenetic silencing of vmPFC during extinction

If silencing BLOCKS extinction (outcome: X):
  TSM coherence: 0.68 → 0.85 (+0.17)
  CFT coherence: 0.78 → 0.42 (-0.36)
  Coherence impact: |0.17| + |-0.36| = 0.53 (HIGH)

If silencing PRESERVES extinction (outcome: not-X):
  TSM coherence: 0.68 → 0.35 (-0.33)
  CFT coherence: 0.78 → 0.89 (+0.11)
  Coherence impact: |-0.33| + |0.11| = 0.44 (HIGH)

Either outcome strongly discriminates. This is a critical test.
```

#### Thagard's Critique of the Proposed Design

**Strengths**:
- The Theory Comparison card structure is ready for formalization
- The Critical Test card can be enhanced with coherence impact metrics
- The overall journey (Orient → Inspect → Explain → Evaluate) aligns with coherence-based reasoning

**Weaknesses**:
1. **Theory comparison is entirely qualitative**: "Evidence balance" is presented narratively without quantitative coherence weighting. Users cannot see the relative strength of theories objectively.
2. **No breadth-vs.-depth trade-off analysis**: When two theories explain evidence equally well, the page does not help users see which has broader explanatory scope or deeper mechanistic explanations.
3. **Underdetermination is presented passively**: The Underdetermination Alert card flags cases where theories tie but does not guide users toward coherence-based reasoning about which is preferable.
4. **Critical tests lack outcome-space analysis**: The page does not show how test outcomes would reshape the theory landscape.

**Constructive Recommendations from Thagard**:

1. **Implement ECHO scoring for every theory comparison**:
   - Compute explanatory breadth (# of domains explained)
   - Compute coherence with background knowledge (literature survey)
   - Compute internal coherence (consistency of mechanisms)
   - Display coherence scores as a simple bar chart with explanation

2. **Create a "Coherence Breakdown" detail view** that shows:
   - Which evidence pieces each theory explains well
   - Which evidence pieces create tension
   - How coherence changes if we accept/reject auxiliary assumptions

3. **Enhance the Critical Test card** with coherence impact metrics:
   ```
   Test: X
   If outcome A: Theory X coherence +0.15, Theory Y coherence -0.22
   If outcome B: Theory X coherence -0.18, Theory Y coherence +0.10
   Recommendation: This test is critical (high coherence impact)
   ```

4. **Add a "Theory Ranking" section** to the Theory Comparison card that uses coherence as the secondary sort key when empirical evidence is tied.

5. **Build a coherence-learning tool**: As users click through evidence and mechanisms, show them how coherence updates based on their selections.

---

### Panel Member 5: James Woodward (Interventionist Causation)

**Position**: Causation should be understood in terms of *invariant intervention*, not merely correlation or mechanistic correlation. A critical test must exploit interventionist structure to distinguish theories.

#### Three Key Questions: Woodward's Answers

**(a) How should mechanism be represented?**

A mechanism description should be *invariant under intervention*. That is, if I intervene on a variable in the mechanism, I should be able to predict the effects reliably. If the mechanism breaks down under intervention (e.g., the correlations persist but are not causal), then the mechanism is misspecified.

The current linear chain (stimulus → amygdala → fear) is observationally plausible but interventionally opaque. Does intervening on the amygdala (optogenetic silencing) actually break the causal chain, or does it merely disrupt a correlation? The answer determines whether the described chain is a mechanism or a spurious association.

**Recommendation**: Every mechanism should include an **"Invariance Under Intervention" section** that specifies:

1. **What intervention would disrupt this mechanism?**
2. **What interventions would leave it intact?** (robustness)
3. **What is the smallest intervention needed to break the mechanism?** (locating the causal bottleneck)

Example:
```
Mechanism: Stimulus (visual threat) → Amygdala (threat encoding) → Freezing behavior

Invariance properties:
1. Intervening on stimulus: Amygdala activation drops, freezing drops. (Mechanism intact)
2. Intervening on sensory cortex (lesion/inactivation): Amygdala activation drops, freezing drops. (Mechanism intact—sensory input required)
3. Intervening on amygdala (optogenetic silencing): Amygdala activation suppressed, but does freezing drop?
   - If freezing drops: The amygdala is causally necessary (mechanism robust)
   - If freezing persists: Alternative pathways exist (mechanism is incomplete)
```

This transforms the mechanism from a static chain into a *causal-experimental roadmap*.

**(b) How should theory comparison handle underdetermination?**

Two theories are observationally equivalent but interventionally distinct if they make *different predictions about what would happen under intervention*. This is where the real science lies.

Example:
- **Theory A (Salience Hypothesis)**: Fear is driven by the amygdala's encoding of threat *salience*. Intervening on salience encoding (e.g., via optogenetic silencing of high-salience neurons) blocks fear.
- **Theory B (Valence Hypothesis)**: Fear is driven by the amygdala's encoding of *negative valence*. Intervening on valence encoding (e.g., via optogenetic silencing of punishment-responsive neurons) blocks fear.

Observationally, both theories match the data. But under *specific, theory-targeted interventions*, they diverge. A critical test exploits this divergence.

**Recommendation**: The Theory Comparison card should include an "Interventionist Prediction" row:

| Theory | Observational Prediction (What we'd see in nature) | Interventionist Prediction (What would happen if we intervene?) | Intervention Method | Prediction Contrast |
|--------|---------------------------------------------------|----------------------------------------------------------------|---------------------|-------------------|
| Salience Hypothesis | High-threat stimuli activate amygdala strongly | Silencing salience-encoding neurons → fear blocked | Optogenetics on salience-tuned cells | Strong predictions |
| Valence Hypothesis | Negative stimuli activate amygdala strongly | Silencing valence-encoding neurons → fear blocked | Optogenetics on punishment-responsive cells | Strong predictions |

Notice: These might activate overlapping neuron populations, but the *causal mechanism* differs. Observational data may not distinguish them; intervention-targeted data will.

**(c) What makes a critical test genuinely critical?**

A critical test is one where the theories make **distinct interventionist predictions**. Purely observational predictions (correlations) may not be sufficient.

A critical test should:
1. Specify an **intervention** (not just an observation)
2. Specify the **target of intervention** (which variable in the mechanism)
3. Specify **contrastive predictions**: What Theory A predicts if the intervention succeeds; what Theory B predicts
4. Have **high causal specificity**: The intervention targets the exact causal variable that discriminates theories, not just any component

Example of a critical test:
```
Critical Test: Inhibit NMDA receptors selectively in the amygdala lateral nucleus (not elsewhere) during fear extinction learning.

Theory A (NMDA-dependent consolidation): Blocking NMDA → extinction memory fails to consolidate → fear returns on reconditioning
Theory B (dopamine-dependent encoding): NMDA blockade leaves dopaminergic encoding intact → extinction memory consolidates normally → fear does not return

Intervention: Bilateral infusion of AP5 (NMDA antagonist) into LA during extinction
Target: NMDA-dependent plasticity in LA specifically
Theory A prediction: Extinction learning blocked
Theory B prediction: Extinction learning proceeds

This is critical because the intervention targets the *disputed causal mechanism* directly.
```

In contrast, a non-critical test might be:
```
Non-critical: fMRI during extinction learning
Observation: High activation in vmPFC and amygdala
Problem: Both theories predict this. The intervention does not target the disputed mechanism (NMDA vs. dopamine); it merely measures activity.
```

#### Woodward's Critique of the Proposed Design

**Strengths**:
- The Critical Test card recognizes the need for discriminating experiments
- The Mechanism Chain card can be extended to include interventionist properties

**Weaknesses**:
1. **Mechanisms lack interventionist specification**: The page does not indicate what interventions would test or break each mechanism. Mechanisms are described as static chains, not as causal-experimental roadmaps.
2. **Theory comparison ignores interventionist divergence**: Two theories that make identical observational predictions but different interventionist predictions appear identical on the page. This misses the real theoretical dispute.
3. **Critical tests are not indexed to theory-specific interventions**: The Critical Test card names high-priority experiments but does not clearly link them to specific theories' causal commitments.
4. **No distinction between observational and interventional equivalence**: The page does not teach users that two theories can be observationally equivalent but interventionally distinct.

**Constructive Recommendations from Woodward**:

1. **Add an "Interventionist Properties" section to every mechanism description**:
   ```
   Mechanism: [Name]
   Chain: [Entities and activities]

   Causal bottlenecks (minimal interventions that disrupt mechanism):
   - Intervening on [X]: Effect on mechanism is [disruptive/robust/partial]

   Robustness (which interventions leave mechanism intact):
   - [Intervention A]: Mechanism persists if [condition]
   - [Intervention B]: Mechanism robust to this intervention

   Causal specificity: How localized must the intervention be to test this mechanism?
   ```

2. **Revise the Theory Comparison card** to include an "Interventionist Predictions" column:
   ```
   | Theory | Observational Prediction | Interventionist Prediction | Intervention Target |
   |--------|--------------------------|--------------------------|---------------------|
   | Theory A | [corr. evidence] | [what would happen if we intervene on X] | [Specify X] |
   | Theory B | [corr. evidence] | [different intervention prediction] | [Specify X] |
   ```

3. **Redesign the Critical Test card** with explicit interventionist targeting:
   ```
   Critical Test: [Name]
   Intervention: [Specific method, e.g., bilateral infusion, optogenetic silencing]
   Target Variable: [Which causal variable does this test?]

   Theory A Prediction: [Under this intervention, A predicts...]
   Theory B Prediction: [Under this intervention, B predicts...]
   Causal Specificity: [Is the intervention aimed precisely at the disputed mechanism?]
   Discrimination Index: [How cleanly does outcome favor one theory?]
   ```

4. **Add a "Observational vs. Interventional Equivalence" section** to the home page that explains:
   - Why two theories might match observational data
   - How intervention-targeted tests can discriminate them
   - Which of the presented theories are observationally equivalent

5. **Create an "Intervention Planning Tool"** that helps users design theory-targeted interventions:
   - User selects two competing theories
   - Tool extracts their core causal claims
   - Tool suggests interventions that would most cleanly discriminate them

---

## Panel Consensus: Agreements and Disagreements

### Strong Agreements (All Panel Members)

1. **The 6-card system is structurally sound**: Theory Comparison, Mechanism Chain, Critical Test, and Warrant Structure cards are the right vehicles for the governing question.

2. **Mechanisms need multi-level representation**: Linear chains are insufficient. Mechanisms must show how different scales (behavioral, circuit, synaptic, molecular) relate.

3. **Underdetermination should be exposed, not hidden**: The Underdetermination Alert card is honest and necessary.

4. **Theories must be indexed to causal/mechanistic specificity**: Users need to understand not just *that* two theories compete, but *how* and *at what scale*.

5. **Critical tests must be connected to theoretical predictions**: A test is not critical just because it's high-priority; it's critical if it discriminates theories.

### Productive Disagreements (Where Panel Members Diverge)

| Issue | Craver | Machamer | Darden | Thagard | Woodward |
|-------|--------|----------|--------|---------|----------|
| **Primary mechanism representation** | Multi-level ontology | Entity-activity pairs | Schema with gaps marked | Coherence network | Causal-interventional roadmap |
| **How to rank underdetermined theories** | By mechanistic level and scope | By activity specificity | By explanatory scope + discriminating tests | By coherence score | By interventionist predictiveness |
| **Critical test definition** | Tests mechanistic level | Tests activity specificity | Tests discrimination power | Tests coherence impact | Tests interventionist divergence |
| **What makes a theory "better"** | Explains at finer grain | Specifies activities precisely | Explains broader scope | Higher overall coherence | Makes stronger causal predictions |

**Interpretation**: These disagreements are complementary, not contradictory. All five approaches are asking legitimate questions about the same theories. The home page should incorporate all five frameworks, not choose among them.

### Specific Tensions

**Tension 1: Coherence Scoring vs. Interventionist Testing**

- **Thagard's view**: Use ECHO-style coherence to weight theories when empirical evidence ties. Coherence with background knowledge and breadth of explanation matter.
- **Woodward's view**: Coherence is a heuristic. The real discrimination comes from intervention-targeted experiments that reveal causal structure, not from post-hoc coherence fitting.

**Panel Resolution**: Both are correct. Coherence scoring is useful for *current* decision-making when theories are underdetermined. Interventionist testing is the path to *resolving* underdetermination in the future. The page should present both: "Currently, Theory X has higher coherence, but these critical tests would discriminate them."

**Tension 2: Multi-Level Explanation vs. Activity Specificity**

- **Craver's view**: Mechanisms are organized at distinct levels (behavioral, circuit, synaptic). Theories that operate at different levels are not competing.
- **Machamer's view**: What matters is whether entities perform the *same activity* at any level. Two theories are competing if they propose different mechanisms (activities) for the same phenomenon.

**Panel Resolution**: Both are correct. Level and activity are orthogonal. The page should ask: "Do these theories operate at the same mechanistic level? If yes, do they specify different activities?" If they're at different levels, they complement rather than compete.

**Tension 3: Schema Gaps vs. Coherence-Based Completeness**

- **Darden's view**: Mechanisms are typically incomplete (how-possibly schemas with gaps). Mark gaps explicitly.
- **Thagard's view**: Incomplete mechanisms reduce coherence. The page should show coherence scores that reflect how complete each theory is.

**Panel Resolution**: Both are correct. The page should mark schema gaps *and* compute coherence scores that reflect the cost of those gaps. A theory with gaps has lower coherence, but may still be the best available account.

---

## Recommended Integrated Design

### Revised 6-Card System with Panel Input

#### Card 1: Neural Frameworks (Updated)

**Current design**: 10 Tier-1 frameworks with article counts and grounding scores.

**Panel recommendation**: Retain as is. Consensus that this card is clear and appropriately descriptive. May add:
- Number of domains addressed by each framework
- Link to framework-specific mechanism galleries

---

#### Card 2: Theory Comparison (REVISED)

**Current design**: Competing accounts, evidence balance, discriminating predictions.

**Integrated panel design**:

```
[Theory Comparison Card]

Domain: [Selected phenomenon, e.g., "Fear Extinction"]

| Theory | Entities & Activities | Mechanistic Level | Observational Evidence | Coherence Score | Explanatory Scope | Interventionist Prediction |
|--------|----------------------|------------------|----------------------|-----------------|------------------|--------------------------|
| TSM | Amygdala (encodes); vmPFC (inhibits) | Circuit | 4 papers | 0.68 | 3/6 domains | Silencing vmPFC blocks extinction |
| CFT | Hippocampus (binds); Amygdala (gates) | Circuit | 5 papers | 0.78 | 5/6 domains | Silencing dorsal CA3 reduces generalization |

Scope breakdown:
  - TSM strong: threat detection, immediate fear
  - TSM weak: extinction, generalization, renewal
  - CFT strong: all domains
  - CFT weak: molecular mechanism still unknown

Coherence analysis:
  CFT has broader explanatory scope (+0.10 coherence) but relies on untested molecular details (-0.02 coherence).
  TSM is mechanistically precise but silent on extinction (+0.15 for precision, -0.08 for scope).

Current status: CFT is favored by coherence, but gap in molecular mechanism remains.
```

**Key additions**:
- Entity-activity notation (from Machamer)
- Mechanistic level column (from Craver)
- Coherence score with breakdown (from Thagard)
- Explanatory scope matrix (from Darden)
- Interventionist prediction column (from Woodward)

---

#### Card 3: Mechanism Chain (REVISED)

**Current design**: Linear chain from environmental feature to behavioral outcome.

**Integrated panel design**:

```
[Mechanism Chain Card]

Phenomenon: Fear Extinction

[Multi-level mechanism diagram]

BEHAVIORAL LEVEL:
  Fear-to-CS decreases after extinction training
    ↑ (etiological cause)

CIRCUIT LEVEL:
  vmPFC (encodes CS non-threat) --inhibits--> Amygdala lateral nucleus
  Hippocampus (encodes context) --gates--> Amygdala lateral nucleus
    ↑ (constitutive)

SYNAPTIC LEVEL:
  GABA release from vmPFC pyramidal terminals
    ↑ (constitutive)

MOLECULAR LEVEL:
  GABA binding to AMPA and NMDA receptors [HOW?] [???]

Empirical support by level:
  - Behavioral: Strong (20+ papers show extinction)
  - Circuit: Strong (optogenetics confirm vmPFC and hippocampal roles)
  - Synaptic: Moderate (patch recording in slices; some in vivo work)
  - Molecular: Weak (receptor blockers show necessity but not mechanism)

Schema classification:
  Levels 1-2: "How-actually" (empirically confirmed)
  Levels 3-4: "How-possibly" (candidate mechanisms with gaps marked [HOW?])

Interventionist properties:
  - Intervention on sensory input: Extinction fails (input required)
  - Intervention on vmPFC: Extinction impaired (necessary but not sufficient)
  - Intervention on hippocampus: Context-dependent extinction fails
  - Interventions on molecular level: NOT YET TESTED — this is where underdetermination lies

Next critical tests:
  1. Molecular mechanism of GABA receptor signaling in LA (distinguishes competing models)
  2. Role of other neuromodulators (serotonin, dopamine) in extinction
```

**Key additions**:
- Multi-level pyramid with explicit constitutive/etiological links (Craver)
- Entity-activity notation (Machamer)
- Schema-gap markers and how-possibly/how-actually classification (Darden)
- Empirical support column (Darden)
- Interventionist properties (Woodward)

---

#### Card 4: Critical Test (REVISED)

**Current design**: Highest-priority discriminating experiment.

**Integrated panel design**:

```
[Critical Test Card]

Phenomenon: Fear Extinction

Rank 1: Molecular mechanism of GABA signaling in amygdala lateral nucleus

Target theories: Theory A (NMDA-dependent consolidation) vs. Theory B (GABA-mediated inhibition)
Mechanistic level: Synaptic/molecular
Causal bottleneck: Does NMDA phosphorylation enable GABA signaling, or are they parallel?

Intervention: Block NMDA receptors in LA during extinction learning (bilateral AP5 infusion)
Specificity: Targets the disputed molecular mechanism directly
Robustness: Test in multiple species, multiple extinction protocols

Theory A prediction:
  Blocking NMDA → extinction consolidation fails → fear returns on reconditioning
  Coherence impact if confirmed: Theory A +0.20, Theory B -0.15

Theory B prediction:
  Blocking NMDA → extinction proceeds normally → fear does not return on reconditioning
  Coherence impact if confirmed: Theory B +0.20, Theory A -0.15

Discrimination index: 0.87 (very high—either outcome strongly discriminates)
Interventionist divergence: Strong (the theories make opposite predictions under this specific intervention)

Current status: This test is critical and has high power to resolve underdetermination.

---

Rank 2: Role of dorsal hippocampal context encoding during extinction renewal

[Similar structure...]
```

**Key additions**:
- Mechanistic level specified (Craver)
- Interventionist targeting and causal bottleneck (Woodward)
- Theory-specific predictions (all panelists)
- Coherence impact calculation (Thagard)
- Discrimination index (Darden)

---

#### Card 5: Warrant Structure (Retained)

**Current design**: Distribution of 7 warrant types across topics.

**Panel recommendation**: Retain as is. Provides important meta-epistemological transparency about how evidence was synthesized. No changes needed.

---

#### Card 6: Underdetermination Alert (REVISED)

**Current design**: Cases where multiple theories fit equally.

**Integrated panel design**:

```
[Underdetermination Alert Card]

Current status: 3 active cases of underdetermination

Case 1: Fear Extinction Mechanism
Theories: NMDA-dependent consolidation (A) vs. GABA-mediated inhibition (B)
Observational equivalence: Both explain available data (5 papers each)
Observational status: TIED
Coherence comparison: Theory B slightly favored (0.78 vs. 0.68)
Interventionist divergence: Strong (opposite predictions under NMDA blockade)
Critical test: NMDA antagonist infusion in LA (discrimination index 0.87)
Estimated resolution: 2-3 years (test feasible now)

---

Case 2: Fear Generalization Basis
Theories: Stimulus similarity (A) vs. Context confusion (B)
Observational equivalence: Both fit rodent and human data equally well
Observational status: TIED
Coherence comparison: Theory A has broader scope, Theory B more mechanistic detail
Interventionist divergence: Moderate (context manipulations discriminate, but stimulus manipulations do not fully separate)
Critical tests: (1) Lesion dorsal CA3 and measure generalization slope; (2) Manipulate context salience
Estimated resolution: 1-2 years

---

Case 3: Molecular Mechanism of GABA Receptor Subtype Specificity
Theories: GABA-A (α1 containing) is sufficient (A) vs. Multiple subtypes required (B)
Observational equivalence: Pharmacological blocking experiments are subtype non-selective
Observational status: TIED (unclear which subtypes matter)
Coherence comparison: Theory A simpler, Theory B more parsimonious with natural variation
Interventionist divergence: Strong (selective knockout of α1 would distinguish)
Critical test: Transgenic mice with α1 knockdown in LA; measure extinction and renewal
Estimated resolution: 3-5 years (requires transgenic animal generation)

---

General principle: Underdetermination is temporary, not permanent. Every case has a path to resolution through theory-targeted intervention.
```

**Key additions**:
- Coherence comparison (Thagard)
- Interventionist divergence assessment (Woodward)
- Timeline to resolution (Darden + Woodward)
- Multi-level mechanism specification in each case (Craver)

---

### New Supporting Pages (Not Home Page, But Recommended)

#### Gallery 1: Mechanism Schema Progression

Shows the same phenomenon (e.g., fear extinction) with:
- How-possibly schema (19th century behavioral account)
- Intermediate schema (circuit-level, 2000s)
- Current best schema (multi-level, 2020s)
- Marked gaps and unknowns

Purpose: Teach users that science advances by refining schemas, not by discovering truth all at once.

#### Gallery 2: Interventionist Prediction Maps

For each theory, shows:
- What observational predictions it makes
- What interventionist predictions it makes
- How specific interventions would test each prediction

Purpose: Teach users the difference between correlation and causation, and why intervention matters.

#### Gallery 3: Coherence-Learning Tool

Allows users to:
- Select a theory
- Explore its coherence score
- See which evidence pieces increase/decrease coherence
- Simulate how new experiments would update coherence

Purpose: Interactive explanation of coherence-based reasoning.

---

## Implementation Recommendations: Priority Order

### Phase 1 (High Priority): Revised Theory Comparison Card
- Add entity-activity notation (Machamer)
- Add mechanistic level column (Craver)
- Add explanatory scope matrix (Darden)
- Add coherence score with breakdown (Thagard)
- Add interventionist prediction column (Woodward)

**Effort**: Medium (~2-4 weeks)
**Impact**: High (addresses the core theory comparison problem)

---

### Phase 2 (High Priority): Revised Mechanism Chain Card
- Convert to multi-level pyramid (Craver + Machamer)
- Add schema-gap notation (Darden)
- Add empirical support column (Darden)
- Add interventionist properties section (Woodward)

**Effort**: Medium (~2-4 weeks)
**Impact**: High (addresses mechanism representation problem)

---

### Phase 3 (High Priority): Revised Critical Test Card
- Add mechanistic level specification (Craver)
- Add interventionist targeting and causal bottleneck (Woodward)
- Add coherence impact calculation (Thagard)
- Add discrimination index (Darden)
- Add timeline to resolution (Darden)

**Effort**: High (~4-6 weeks, requires new calculations)
**Impact**: High (directly addresses the discriminating-test problem)

---

### Phase 4 (Medium Priority): Revised Underdetermination Alert Card
- Add coherence comparison (Thagard)
- Add interventionist divergence assessment (Woodward)
- Add resolution pathways (Darden)
- Add timeline estimates (Darden)

**Effort**: Medium (~2-4 weeks)
**Impact**: Medium-High (improves epistemic transparency)

---

### Phase 5 (Lower Priority): Supporting Galleries and Tools
- Mechanism Schema Gallery (how-possibly vs. how-actually)
- Interventionist Prediction Maps
- Coherence-Learning Tool

**Effort**: High (~6-8 weeks for all three)
**Impact**: Medium (enhance understanding, not core system)

---

## Specific Operational Guidelines for Implementation

### Coherence Scoring (Thagard)

Use a simplified ECHO-inspired scoring:

```
Coherence(Theory T) =
  [Breadth × 0.3] + [Depth × 0.3] + [BkgndCoherence × 0.2] + [Simplicity × 0.2]

Where:
  Breadth = # domains explained / total # domains
  Depth = (empirical evidence count / max evidence) × (mechanistic detail score)
  BkgndCoherence = % literature that accepts or extends theory
  Simplicity = inverse(# causal entities or mechanisms)

Range: 0.0 (incoherent) to 1.0 (perfect coherence)
Typical science: 0.5–0.85 range
```

Not a proof, but a reasoning aid. Always explain breakdowns in the card.

---

### Mechanistic Level Specification (Craver)

Mark every theory with its primary level:

- **Behavioral/Systems**: Learning curves, behavioral output
- **Circuit**: Multi-region coordination (e.g., vmPFC-amygdala)
- **Synaptic**: Transmission, plasticity (e.g., LTP/LTD)
- **Molecular**: Gene expression, protein binding (e.g., CREB, GABA-A)

When two theories differ at the same level, they compete. When they differ across levels, note that they complement.

---

### Interventionist Targeting (Woodward)

For each critical test, specify:

1. **Intervention type**: Lesion, inactivation, optogenetics, pharmacology, transgenic, lesion-and-restore
2. **Target specificity**: Brain region, circuit, cell type, receptor subtype, gene
3. **Expected outcome under each theory**
4. **Robustness checks**: What alternative explanations would this experiment rule out?

Example:

```
Intervention: Bilateral infusion of AP5 (NMDA antagonist) in amygdala lateral nucleus
Specificity: NMDA receptors only; amygdala lateral nucleus only; during extinction learning phase
Target theory: A (NMDA consolidation) vs. B (GABA inhibition)
Expected outcome if Theory A: Extinction learning blocked
Expected outcome if Theory B: Extinction learning proceeds
Robustness check 1: Are we blocking amygdala plasticity in general, or NMDA specifically? (control: AMPA antagonist)
Robustness check 2: Are we blocking consolidation, or learning itself? (test during reconditioning, not extinction)
```

---

### Schema-Gap Notation (Darden)

Use visual color-coding:

- **Green**: Empirically confirmed at this level (multiple independent studies)
- **Yellow**: Tentative (how-possibly); candidate mechanism; limited evidence
- **Red**: Known gap; explicitly unresolved; speculative
- **Gray**: Not yet tested; theoretically predicted but empirically untouched

Example:

```
Stimulus (known)
  ↓ [GREEN: visual cortex projects to amygdala]
Amygdala lateral nucleus
  ↓ [YELLOW: encodes threat salience via population coding—how-possibly]
Pyramidal cell ensemble
  ↓ [RED: GABA receptor subtype specificity unknown]
GABA-A subunit composition
  ↓ [GRAY: molecular consequences untested]
Extinction learning suppression
```

---

### Discrimination Index Calculation (Darden + Woodward)

For each critical test:

```
Discrimination Index = |P(outcome A | Theory X) − P(outcome A | Theory Y)|

Where P(outcome | theory) is the predicted probability of the outcome under that theory.

Interpretation:
  DI > 0.80: Very high discriminatory power (either outcome strongly favors one theory)
  DI 0.60–0.80: Good discriminatory power
  DI 0.40–0.60: Moderate; outcome would be informative but not decisive
  DI < 0.40: Poor discriminatory power; test is not critical yet

Note: A test with DI < 0.60 should not be labeled "critical test" on the home page.
```

---

### Coherence Impact Calculation (Thagard)

For each critical test:

```
Coherence Impact =
  |Coherence(T1 | outcome observed) − Coherence(T1 | baseline)|
  + |Coherence(T2 | outcome observed) − Coherence(T2 | baseline)|

Interpretation:
  CI > 0.30: High coherence impact (test significantly updates landscape)
  CI 0.15–0.30: Moderate impact
  CI < 0.15: Low impact (outcome leaves coherence roughly unchanged)

A test is critical if it has BOTH high discrimination index AND high coherence impact.
```

---

## Panel Recommendations for Additional Resources

### For Users

1. **Tutorial: "How to Read a Mechanism Schema"** — Teaches multi-level interpretation, entity-activity distinction, schema-gap notation
2. **Explainer: "Coherence and Competition in Theory"** — Explains ECHO-style reasoning without math
3. **Interactive: "Design a Critical Test"** — Lets users build interventionist tests and see predicted outcomes

### For Content Creators (Atlas Builders)

1. **Checklist: "Mechanism Description Quality"**
   - [ ] Multi-level structure present?
   - [ ] Entity-activity pairs specified?
   - [ ] Schema gaps marked and explained?
   - [ ] Empirical support cited?
   - [ ] Interventionist properties specified?

2. **Template: "Theory Comparison Card Specification"**
   - Domain/phenomenon
   - Competing theories (names, key figures)
   - Mechanistic levels
   - Evidence balance
   - Coherence scoring
   - Explanatory scope matrix
   - Interventionist predictions
   - Critical tests for discrimination

3. **Decision Log: "Why We Classified This as Schema-Gap"** — Opacity log for every unresolved mechanism, explaining why it's incomplete and what would resolve it

---

## Conclusion: The Five Intellectual Traditions in Dialogue

This panel report brings together five distinct intellectual traditions in the philosophy and history of neuroscience:

1. **Craver's Mechanistic Explanation**: Mechanisms are multi-level, with constitutive and etiological relations
2. **Machamer's Entity-Activity Semantics**: Activities do the causal work; entities are relata
3. **Darden's Discovery Methodology**: Science advances by refining schemas; gaps must be marked explicitly
4. **Thagard's Coherence Reasoning**: Theories are compared not just on evidence but on overall coherence with background knowledge
5. **Woodward's Interventionist Causation**: Theories are distinguished by their predictions under intervention

The panel consensus is that **all five frameworks are legitimate and complementary**. A home page that incorporates all five will:

- Help users understand mechanisms at multiple levels (Craver)
- Show them the activities connecting entities (Machamer)
- Make explicit what is known vs. unknown (Darden)
- Provide formal tools for comparing underdetermined theories (Thagard)
- Guide them toward experiments that truly discriminate (Woodward)

The revised design proposed in this report operationalizes all five frameworks in the six-card system. Implementation should proceed in the priority order listed above, starting with the Theory Comparison and Mechanism Chain cards.

---

## References for Further Reading

### On Mechanistic Explanation

- Craver, C. F. (2007). *Explaining the Brain: Mechanisms and the Mosaic Unity of Neuroscience*. Oxford University Press.
- Craver, C. F., & Darden, L. (2013). *In Search of Mechanisms: Discoveries Across the Life Sciences*. University of Chicago Press.

### On Activities and Entities

- Machamer, P., Darden, L., & Craver, C. F. (2000). Thinking about mechanisms. *Philosophy of Science*, 67(1), 1–25.

### On Discovery and Schemas

- Darden, L. (2006). *Reasoning in Biological Discoveries: Essays on Mechanisms, Interfield Relations, and Anomaly Resolution*. Cambridge University Press.

### On Explanatory Coherence

- Thagard, P. (1992). Conceptual Revolutions. Princeton University Press.
- Thagard, P. (2019). *Mind-Society: From Brains to Social Sciences*. Oxford University Press.

### On Interventionist Causation

- Woodward, J. (2003). *Making Things Happen: A Theory of Causal Explanation*. Oxford University Press.
- Woodward, J. (2015). Simplicity in the best systems account of laws of nature. *British Journal for the Philosophy of Science*, 66(3), 541–567.

---

**Panel Convened**: 2026-04-03
**Report Status**: FINAL — Ready for Implementation
**Next Step**: Design team reviews and begins Phase 1 implementation
