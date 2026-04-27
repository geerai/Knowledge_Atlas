# Track 2 · Task 2: Build the Search Pipeline (Abstract-First Triage)

**Track:** Article Finder  
**What you build:** A pipeline that identifies knowledge gaps in the Article Eater's 166 PNU templates, searches for papers that could fill them using free APIs (Semantic Scholar, CrossRef, PubMed), triages candidates at the abstract level before downloading anything, and produces a PRISMA-style dashboard proving the pipeline works.  
**Core lesson:** Don't vibe-code a search. *Target* your searches using VOI (Value of Information), *triage* at the cheapest level (abstracts, not PDFs), and *prove* your pipeline produces audit-ready results.

---

## What Is PRISMA and Why You're Building One

PRISMA (**Preferred Reporting Items for Systematic Reviews and Meta-Analyses**) is the international gold standard for conducting and reporting systematic literature searches. Published in 2009, updated 2020, it forces researchers to document their search funnel transparently:

```
Records identified through database searching        (n = ?)
    ↓
Duplicates removed                                    (n = ?)
    ↓
Records screened by title + abstract                  (n = ?)  →  Excluded (n = ?)
    ↓
Full-text articles assessed for eligibility           (n = ?)  →  Excluded with reasons (n = ?)
    ↓
Studies included in final synthesis                   (n = ?)
```

Your pipeline **is** an automated PRISMA funnel. Your dashboard must show these exact numbers. This is the proof that you didn't just dump random papers into the system.

---

## What This Assignment Teaches

Task 1 taught you to **fix** existing code. Task 2 teaches you to **design a research pipeline** — not just "find papers," but find the *right* papers for *specific* knowledge gaps, using the scoring infrastructure that already exists in the codebase.

The pipeline has three stages, each cheaper than the next:

```
Stage 1: IDENTIFY gaps → score by VOI → generate targeted queries
    ↓ (cost: zero — just reading local JSON files)
Stage 2: SEARCH APIs → collect abstracts → triage by classifier + VOI
    ↓ (cost: low — free API calls, no PDFs downloaded)
Stage 3: DOWNLOAD PDFs → only for papers that passed triage
    ↓ (cost: high — only do this for winners)
```

The key insight: **you never download a PDF to decide if it's relevant.** You triage at the abstract level using free APIs.

---

## Setup

You should already have the four repositories from Task 1:
- `Knowledge_Atlas` — the site (with your fixed contribute page from Task 1)
- `Article_Finder` — the discovery pipeline
- `Article_Eater` — the extraction engine (contains the gap data AND the VOI functions)
- `atlas_shared` — the shared classifier (installed as `pip install -e .`)

---

## Phase 1: Understand the Gap Data and the VOI System

### 1A. Understand the PNU templates

The Article Eater has 166 PNU (Plausible Neural Underpinning) templates. Each describes a mechanism chain: how an environmental feature (e.g., ceiling height) leads to a psychological outcome (e.g., creativity) through neural processes. Each step has a **confidence score**. Low-confidence steps are **knowledge gaps**.

Pick 3 templates from `Article_Eater/data/templates/`. Ask your AI:

> *"These are PNU templates from the Knowledge Atlas. Walk me through one template completely: what does each step in the `mechanism_chain` represent, what does `confidence` mean for each step, and what does a low-confidence step (< 0.5) tell us about what's missing from the research corpus?"*

> *"Now look at all three templates and identify: which steps have confidence below 0.5? For each gap, tell me what specific study would fill it."*

### 1B. Understand the VOI scoring system

The Article Eater already has **7 VOI functions** for scoring knowledge gaps. You will use three of them. Ask your AI:

> *"Read these three files from Article_Eater and explain what each VOI function does:*
> 1. *`src/services/voi_search.py` — find the `VOICalculator` class and its `calculate_voi()` method*
> 2. *`src/cmr/voi_scoring.py` — find `score_voi()` and `aggregate_paper_voi()`*
> 3. *`src/services/discovery_funnel.py` — find `classify_closure()`*
>
> *For each function, explain: What inputs does it take? What does the output score mean? When would a gap get a HIGH score vs. a LOW score?"*

**What you should learn from this:**
- `VOICalculator.calculate_voi()` scores gaps by combining structural VOI (how central is this belief in the network?) with epistemic VOI (how uncertain are we?). A gap with VOI=0.82 at a hub node matters more than a gap with VOI=0.3 at a leaf node.
- `score_voi()` scores individual findings: a contradiction against a well-calibrated template = 1.0 (highest); a confirmation of something we already know = 0.2 (lowest).
- `classify_closure()` tells you if finding a paper actually closed the gap: FULL (VOI dropped below 0.1), PARTIAL (≥30% reduction), NONE, or NEGATIVE (the paper made things worse).

### 1C. Understand the existing API clients

The Article Eater already has **working API clients** for searching the literature. Ask your AI:

> *"Read `Article_Eater/src/services/paper_fetcher.py`. Find the `SemanticScholarClient`, `CrossRefClient`, and `PubMedClient` classes. For each:*
> 1. *What API does it call?*
> 2. *What does `search(query, max_results)` return?*
> 3. *Does the `PaperMetadata` result include the `abstract`?*
> 4. *What are the rate limits? (Look at the `_RateLimiter` init in each class)*
> 5. *Do I need an API key?*"

**What you should learn from this:**
- Semantic Scholar: free, no key needed, but rate-limited to ~20 requests/minute without a key. Returns title, abstract, authors, year, citation count, open_access status, and study type.
- CrossRef: free, no key needed, uses "polite pool" (your email in the User-Agent header). Returns title, abstract, authors, DOI, venue, references.
- PubMed: free, optional API key (faster with one). Returns title, abstract, authors, MeSH terms.
- **All three return abstracts.** You never need to download a PDF to decide if a paper is relevant.

### 1D. Get a boxology diagram

> *"Draw a box-and-arrow diagram of this complete pipeline:*
> 1. *Read PNU templates → extract gaps with confidence < 0.5*
> 2. *Score gaps using VOICalculator → sort by priority*
> 3. *Generate search queries using QueryGenerator (with cross-field vocabulary)*
> 4. *Hit Semantic Scholar + CrossRef APIs → collect abstracts*
> 5. *Triage abstracts: run through atlas_shared classifier + score_voi*
> 6. *Classify each paper as ACCEPT / EDGE_CASE / REJECT*
> 7. *Download PDFs only for ACCEPT + EDGE_CASE papers*
> 8. *Assess gap closure using classify_closure()*
> 9. *Display PRISMA funnel on dashboard"*

**Your deliverable:** The boxology diagram, plus a list of 5 specific gaps you found in the templates with their confidence scores and VOI priorities.

---

## Phase 2: Spec — Write the Pipeline Contract

### 2A. The Gap Extractor + VOI Scorer

```markdown
## Gap Extractor Contract

### Inputs
- PNU template JSON files from Article_Eater/data/templates/
- Web of Belief (from Article_Eater database)

### Processing
For each template:
1. Walk the mechanism_chain
2. Extract steps with confidence < 0.5
3. Also extract: key_references not in our corpus,
   competing_accounts, and falsification_conditions (rebuttals)
4. Score each gap using VOICalculator.calculate_voi():
   - Gap type: MECHANISM (low-confidence steps), VALIDATION (missing refs),
     DIRECTION (competing accounts), BOUNDARY (rebuttals)
   - Returns: combined_voi, structural_voi, epistemic_voi

### Outputs (per gap)
- template_id and step number
- gap_type (MECHANISM, VALIDATION, DIRECTION, BOUNDARY)
- confidence_current
- voi_score (combined), structural_voi, epistemic_voi
- description (what is missing)

### Success conditions
- At least 10 gaps identified across the 166 templates
- Gaps are sorted by VOI score (highest first)
- Each gap has a gap_type and a description of what's missing
```

### 2B. The Search Runner (Abstract-First)

```markdown
## Search Runner Contract

### Inputs
- Scored gaps from the Gap Extractor (top 10–20 by VOI)

### Processing
For each gap:
1. Generate queries using QueryGenerator.generate_queries()
   (from src/services/voi_search.py)
2. Optionally expand queries using CrossFieldVocabulary.expand_query()
3. Call PaperFetcher.search() with sources=['semantic_scholar', 'pubmed']
4. Collect PaperMetadata results (title, abstract, DOI, year, study_type,
   citation_count, open_access)
5. De-duplicate by DOI

### Outputs (per search)
- gap_id and query used
- results: [ PaperMetadata with abstracts ]
- result_count, search_timestamp

### Success conditions
- At least 5 gaps searched
- Results include abstracts (not just titles)
- Rate limits respected (≤ 20 req/min for Semantic Scholar)
- Results stored as structured JSON
```

### 2C. The Abstract Triage (Classifier + VOI)

This is the critical stage — where you decide which papers are worth downloading.

```markdown
## Abstract Triage Contract

### Inputs
- PaperMetadata results from the Search Runner (with abstracts)

### Processing
For each paper:
1. Run the abstract through atlas_shared classifier:
   - Does this paper match one of Q01–Q30?
   - What topic does it map to?
2. Score the abstract using score_voi() from cmr/voi_scoring.py:
   - Does the abstract suggest contradiction (1.0), gap-fill (0.8),
     extension (0.6), or confirmation (0.2)?
3. Classify the paper:
   - ACCEPT: on-topic AND voi_score ≥ 0.5
   - EDGE_CASE: on-topic but voi_score < 0.5, OR borderline topic match
   - REJECT: off-topic

### Outputs (per paper)
- doi, title, authors, year
- classifier_verdict: { matched_topic, confidence }
- voi_score, voi_bucket (high / medium / low)
- triage_decision: ACCEPT / EDGE_CASE / REJECT
- triage_reason: why this decision was made

### Success conditions
- At least 30 abstracts triaged
- ACCEPT and EDGE_CASE papers stored separately from REJECTs
- The triage log is human-readable (not just "accepted: true")
```

### 2D. The PRISMA Dashboard

> *Ask your AI: "I need a web page that shows a PRISMA-style funnel for my search pipeline. It should display:*
> 1. *How many gaps were identified and their VOI scores*
> 2. *How many queries were run and against which APIs*
> 3. *How many abstracts were collected*
> 4. *How many passed classifier triage (ACCEPT vs EDGE_CASE vs REJECT)*
> 5. *How many PDFs were downloaded (if any)*
> 6. *Gap closure assessment: did any found papers actually reduce VOI?*
>
> *Design a layout for this dashboard. It must show the PRISMA funnel numbers and update as the pipeline runs. Data must persist after page refresh."*

**Your deliverable:** The complete contract for all four sub-systems, plus the dashboard wireframe.

---

## Phase 3: Build — Delegate to Your AI

Give your AI the four contracts and ask it to build:

1. A Python script that reads templates, extracts gaps, scores by VOI, and generates search queries
2. A search module that calls Semantic Scholar + CrossRef APIs and collects abstracts
3. An abstract triage module that runs classifier + VOI scoring
4. A dashboard page (`ka_topic_proposer.html` or similar)

### Verification questions you MUST ask

> *"Show me how you read the mechanism_chain from a template JSON. Which field do you check for low confidence? What threshold do you use?"*

> *"Show me the VOI scores for 3 gaps. Explain why one scored higher than another. Is the ranking reasonable?"*

> *"Show me the API call to Semantic Scholar. What fields are you requesting? Does the response include the abstract?"*

> *"Run a search for one gap. Show me the raw API response. How many results have abstracts vs. how many are abstract-less?"*

> *"Show me how the classifier decides if an abstract is on-topic. What happens if the abstract is too short for the classifier?"*

> *"What happens if a search returns zero results? Is that a pipeline failure, or a valid 'null result' that should be recorded? (Hint: null results are scientifically important — they mean the gap may be genuinely unfilled.)"*

> *"How does the dashboard get its data? Does it read from a file, a database, or memory? What happens if I refresh the page?"*

**Your deliverable:** Working code, plus a log of which verification questions revealed problems.

---

## Phase 4: Prove — Run the Pipeline End-to-End

### Step 1: Run the Gap Extractor

```bash
python3 gap_extractor.py --templates Article_Eater/data/templates/
```

Verify:
- [ ] At least 10 gaps identified
- [ ] Gaps sorted by VOI score
- [ ] Each gap has template_id, step number, confidence, gap_type, voi_score

### Step 2: Run the Search Runner

```bash
python3 search_runner.py --gaps gap_results.json --sources semantic_scholar,crossref
```

Verify:
- [ ] At least 5 gaps searched
- [ ] Results include abstracts
- [ ] Rate limits respected
- [ ] Null results recorded (not silently dropped)

### Step 3: Run Abstract Triage

```bash
python3 abstract_triage.py --results search_results.json
```

Verify:
- [ ] At least 30 abstracts triaged
- [ ] Each paper classified as ACCEPT / EDGE_CASE / REJECT
- [ ] ACCEPT papers stored in lifecycle DB
- [ ] EDGE_CASE papers stored separately with flags

### Step 4: Fill in the PRISMA funnel

| Funnel Stage | Count |
|---|---|
| Gaps identified (total) | |
| Gaps searched (top VOI) | |
| API queries executed | |
| Records returned (with abstracts) | |
| Duplicates removed | |
| Records screened by classifier | |
| → ACCEPT (on-topic, high VOI) | |
| → EDGE_CASE (borderline) | |
| → REJECT (off-topic) | |
| PDFs downloaded (if any) | |
| Gaps with closure assessment | |

### Step 5: Trace one paper end-to-end

Pick ONE paper that made it through the entire pipeline and document:

```
Gap source: Template T__ step __ (confidence: 0.__)
  VOI score: 0.__ (gap_type: ___________)
  → Search query: "_______________"
  → API source: Semantic Scholar / CrossRef / PubMed
  → Found: [paper title] by [authors] ([year])
  → Abstract: [first 100 chars...]
  → Classifier verdict: topic=Q__, confidence=0.__
  → VOI assessment: score=0.__, bucket=high/medium/low
  → Triage decision: ACCEPT / EDGE_CASE
  → Stored at: [path / DB entry]
```

### Step 6: Report null results

If any high-VOI gaps returned zero search results, document them:

```
Gap: Template T__ step __ (VOI: 0.__)
  Description: _______________
  Searches tried: [list queries]
  Result: NO PAPERS FOUND
  Implication: This gap may be genuinely unfilled in the literature.
               This is a research opportunity, not a pipeline failure.
```

**Your deliverable:** The PRISMA funnel table, one end-to-end trace, and null result report.

---

## What You Submit

| Item | What it is |
|---|---|
| **Gap analysis** (Phase 1) | Boxology diagram + 5 specific gaps with VOI scores |
| **Pipeline contract** (Phase 2) | Spec for Gap Extractor, Search Runner, Abstract Triage, Dashboard |
| **Working code** (Phase 3) | Gap extractor, search runner, triage module, dashboard page |
| **Verification log** (Phase 3) | Which questions you asked AI, which revealed problems |
| **PRISMA funnel** (Phase 4) | The completed funnel table with real numbers |
| **End-to-end trace** (Phase 4) | One paper traced from gap → search → abstract → triage → store |
| **Null result report** (Phase 4) | High-VOI gaps where no papers were found |
| **File manifest** (Phase 4) | `git diff` and `git status` output |

**How to generate your manifest:**
```bash
cd Knowledge_Atlas
git diff --name-only HEAD
git status --short
```

---

## Files You Must Change or Create

| File | Change Type | What It Does |
|---|---|---|
| `gap_extractor.py` (or similar) | New | Reads templates, extracts gaps, scores by VOI |
| `search_runner.py` (or similar) | New | Calls Semantic Scholar/CrossRef APIs, collects abstracts |
| `abstract_triage.py` (or similar) | New | Runs classifier + VOI scoring on abstracts |
| Search results JSON | New | Structured results with abstracts |
| Triage results JSON | New | ACCEPT/EDGE_CASE/REJECT decisions with reasons |
| Dashboard page (`ka_topic_proposer.html`) | New | PRISMA funnel + gap status |
| Database | Modified | New entries for triaged papers |

---

## Grading

| Criterion | Points | What we check |
|---|---|---|
| **Gap extraction** | 15 | Correctly identified low-confidence steps and scored by VOI |
| **VOI understanding** | 10 | Can explain why one gap scores higher than another |
| **API integration** | 15 | Successfully queried Semantic Scholar/CrossRef, got abstracts back |
| **Abstract triage** | 20 | Classifier + VOI scoring produces defensible ACCEPT/EDGE_CASE/REJECT |
| **PRISMA funnel** | 15 | Dashboard shows real numbers at each stage |
| **End-to-end trace** | 10 | One paper traced from gap → API → abstract → triage → store |
| **Null results** | 5 | Documented gaps where no papers exist (not treated as failures) |
| **Verification questions** | 10 | Caught real problems in the AI's implementation |

---

## Existing Code You Should Know About

These files already exist in Article_Eater. **You do not need to write them.** You need to *use* them.

| File | What it provides |
|---|---|
| `src/services/voi_search.py` | `VOICalculator.calculate_voi()` — scores gaps by structural + epistemic value |
| `src/services/voi_search.py` | `QueryGenerator.generate_queries()` — turns gaps into search queries |
| `src/services/voi_search.py` | `CrossFieldVocabulary.expand_query()` — adds cross-discipline synonyms |
| `src/cmr/voi_scoring.py` | `score_voi()` — scores findings (contradiction=1.0, confirmation=0.2) |
| `src/cmr/voi_scoring.py` | `aggregate_paper_voi()` — paper-level VOI summary |
| `src/services/discovery_funnel.py` | `classify_closure()` — FULL/PARTIAL/NONE/NEGATIVE gap closure |
| `src/services/paper_fetcher.py` | `SemanticScholarClient.search()` — free API, returns abstracts |
| `src/services/paper_fetcher.py` | `CrossRefClient.search()` — free API, returns abstracts |
| `src/services/paper_fetcher.py` | `PubMedClient.search()` — free API, returns abstracts |
| `src/services/paper_fetcher.py` | `PaperFetcher.search()` — unified multi-source search |
| `src/services/paper_fetcher.py` | `estimate_study_type()` — auto-classifies study type from abstract |
