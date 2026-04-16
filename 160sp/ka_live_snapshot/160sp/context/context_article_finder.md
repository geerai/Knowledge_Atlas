# AI Context: Article Finder (Track 2)

## What is K-ATLAS?

K-ATLAS (Knowledge Architecture for Translating Life-science and Affective-environment Science) is a structured credibility reasoning system that stores scientific knowledge not as simple facts, but as *structured credences* — beliefs tagged with how well-supported they are, where the support comes from, and why the system holds each belief with the confidence it does. Unlike a conventional literature database, K-ATLAS explicitly tracks warrant types, credence scores, and the chain of reasoning that connects evidence to claims.

The system models knowledge as an Evidence Network (Web of Belief): a directed graph where each node is a claim and each edge is a typed, weighted warrant. Warrants represent the epistemic relationship between evidence and claims, with discount factors (d values ranging from 0.25 to 1.0) controlling how much confidence flows across each edge. When new evidence is added, credences propagate through the network and the system re-equilibrates. The network is foundherentist: both empirical directness (how close evidence is to observation) and coherence with theoretical frameworks matter equally.

## The Corpus: Structure and Scale

K-ATLAS currently contains:
- **~760 research papers** across 11 topic clusters (Lighting, Biophilia, Acoustics, Spatial Geometry, Color, Thermal Comfort, etc.)
- **~1,900 evidence items** (specific empirical findings or theoretical claims extracted from those papers)
- **~425 psychological constructs** organized hierarchically (T1 frameworks → T2 mechanisms → T3 specific claims)

Papers in the corpus are fully processed (extracted evidence, warrants assigned, credences calculated) or classified as stubs (metadata only, awaiting full processing). The corpus skews Western and laboratory-based; this is a known limitation flagged in the system.

## What "Relevance" Means

A paper is relevant to a K-ATLAS question if it provides empirical evidence about **the specific environmental variable, population, and outcome measure** mentioned in that question.

### Non-relevant papers (common mistakes):
- Papers about biophilia in general, but not your specific question (e.g., general "plants improve mood" when you need "indoor plant density × office worker productivity")
- Papers about the mechanism (e.g., "nature improves amygdala function") when the question asks about the behavioral outcome
- Papers using completely different measurement methods from what ATLAS expects (e.g., a study using EEG when all existing ATLAS evidence uses cortisol)
- Papers that are theoretically related but do not measure the variables in question

### Relevant papers (what to look for):
- Papers with the exact outcome measure (cortisol, attention task performance, social behavior)
- Papers with clearly defined participant populations (age, profession, culture, health status)
- Papers with transparent study design (RCT, observational, longitudinal) and sufficient detail to extract causal claims
- Papers that either directly test a claim ATLAS makes or provide evidence that would strengthen/weaken existing credences

## Question Format in K-ATLAS

Questions are structured as natural-language queries with embedded components:

**Example question**: "Does exposure to natural sunlight in office environments improve concentration and reduce stress in working-age adults in Western countries?"

**Components**:
- **Environmental variable**: Natural sunlight / daylight
- **Population**: Working-age adults, Western countries
- **Outcome measure**: Concentration (measured via attention task), stress (measured via cortisol, self-report)
- **Setting**: Office environments
- **Implied mechanism**: Circadian regulation / stress recovery

A relevant paper must address **all components simultaneously** or provide a bridge warrant if it uses analogous populations/settings/measures.

## Data Model for Articles

Each article record added to K-ATLAS must include:
- **doi**: Digital Object Identifier (primary key; must be valid and unique)
- **title**: Paper title (verbatim)
- **authors**: List of author names (first, last, or "et al." format)
- **year**: Publication year
- **journal**: Journal name
- **abstract**: Full abstract text (or structured summary if paywalled)
- **pdf_path**: Local path to full text PDF (must be verified accessible)
- **relevance_score**: (0–1) How directly does this paper address ATLAS questions? 1.0 = directly measures the question variables; 0.5 = moderate bridge warrant needed; <0.3 = marginal
- **assigned_question_id**: Which ATLAS question(s) this paper supports (may be multiple)

Optional fields:
- **study_design**: RCT, observational, longitudinal, meta-analysis, review
- **sample_size**: N participants
- **population_tags**: WEIRD, non-Western, clinical, etc.
- **measurement_method**: How outcomes were measured (cortisol assay, Stroop task, etc.)
- **effect_size**: d, r, or Cohen's d if reported
- **notes**: Methodological concerns, limitations, or boundary conditions

## The Deduplication Problem

A single paper can be found through multiple search paths:
- Searching "daylight AND cortisol" finds Smith et al. 2018
- Searching "natural light AND stress" also finds Smith et al. 2018
- Searching "circadian rhythm AND office environment" finds the same paper again

**Task**: Before adding any article to ATLAS, check whether it already exists by DOI. K-ATLAS maintains a master article index; duplicates waste processing effort and create confusion when the same paper gets mapped to different evidence items.

**Workflow**:
1. Extract DOI from the paper
2. Search ATLAS article index for that DOI
3. If found, note which questions it is already assigned to; do not re-add
4. If not found, add as new record

## Acceptance Criteria for Articles

1. **Unique DOI**: No paper with this DOI already exists in ATLAS. Check the article index first.

2. **Accessible PDF**: The full-text PDF must be accessible (not paywalled without university access, not behind a captcha). If a paper is found but inaccessible, note it as a "stub" with metadata only.

3. **Relevance justified**: The relevance score (0–1) must be explicitly reasoned in the notes field. A relevance of 0.8 needs explanation: "Directly measures cortisol via HPLC (ATLAS standard); population is Western office workers (partial match); setting is lab not field (requires bridge warrant d=0.65)."

4. **No hallucinated citations**: Do not invent papers or confabulate details. If unsure whether a paper exists, search Google Scholar, Semantic Scholar, or Elicit first.

5. **Metadata accuracy**: Title, authors, year, and journal must be verbatim from the source (verify against the PDF). Typos in metadata make papers unsearchable and cause deduplication failures.

6. **Question mapping specificity**: If the paper is assigned to a question, the notes field must explain which variables in the question the paper addresses. Example: "Addresses daylight variable (high relevance, d=0.90); uses proxy outcome measure for stress (cortisol via saliva, ATLAS-standard method); WEIRD population (no bridge needed); lab setting (moderate bridge needed, d=0.65 per bridge_warrants.py)."

## Key References

- **Article Index**: `ka_article_search.html` (searchable corpus)
- **Relevance Guidance**: `ka_article_propose.html` (submission form with field definitions)
- **Bridge Warrants**: `bridge_warrants.py` in the epistemic module (explains how to justify relevance across population, setting, and measurement differences)
- **Example Evidence Integration**: `ka_evidence.html` (shows how articles map to claims and credences)
