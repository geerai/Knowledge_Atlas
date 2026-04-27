# Track 2: Article Finder — All Tasks

**Track overview:** You will build and operate a PRISMA-compliant article discovery pipeline for the Knowledge Atlas. Starting from a broken contribute page, you'll wire in a working classifier, extract knowledge gaps from PNU templates, generate targeted search queries, execute those searches via SerpAPI, triage results at the abstract level, and report everything through a PRISMA funnel dashboard.

**Three tasks, one pipeline:**

| Task | What you build | Points |
|---|---|---|
| Task 1 | Fix the contribute page — wire in the classifier | Graded on diagnosis, spec, fix, and validation |
| Task 2 | Gap targeting — extract gaps, score by VOI, generate queries | 60 points |
| Task 3 | Search execution — SerpAPI, abstract collection, triage, PRISMA | 75 points |

**Contract gate (all tasks):** Every task requires written contracts with inputs, processing, outputs, success conditions, and test checklists. If your contracts are insufficient, your work will be flagged as not ready for integration. 20 bonus points for contract quality on Tasks 2 and 3.

---

# Task 1: Fix the Contribute Page

**Track:** Article Finder  
**What's wrong:** The contribute page accepts PDFs but does nothing with them — no classification, no storage, no feedback.  
**Your job:** Fix it so that submitted papers are classified, stored correctly, and the user sees what happened.

---

## What This Assignment Teaches

You will use AI to fix a broken page. But the point is not the fix — AI writes the code. The point is:

- Can you **diagnose** what's broken by asking your AI the right questions?
- Can you **spec** the fix precisely enough that AI builds the right thing?
- Can you **verify** that the AI's fix actually works — and catch the cases where it silently doesn't?

---

## Setup: Clone the Repositories

You need four repositories. All are at [github.com/dkirsh](https://github.com/dkirsh):

```bash
# 1. The Knowledge Atlas site (contains the contribute page you'll fix)
git clone https://github.com/dkirsh/Knowledge_Atlas.git

# 2. The Article Finder pipeline (the discovery half of the system)
git clone https://github.com/dkirsh/Article_Finder.git

# 3. The Article Eater extraction engine (the processing half)
git clone https://github.com/dkirsh/Article_Eater.git

# 4. The shared classifier module (the ID function you'll wire in)
git clone https://github.com/dkirsh/atlas_shared.git
cd atlas_shared && pip install -e . && cd ..
```

Verify `atlas_shared` installed correctly:
```bash
python3 -c "from atlas_shared.classifier_system import AdaptiveClassifierSubsystem; print('OK')"
```

---

## Phase 1: Diagnose — What's Broken?

You need to understand two programs before you can connect them.

### 1A. Ask your AI to explain the contribute page

Open `Knowledge_Atlas/ka_contribute_public.html`. Give the full source to your AI and ask:

> *"Walk me through exactly what happens when a user drops a PDF and clicks 'Send suggestion.' For each step, tell me: what function runs, what data is created, and where it goes. Then tell me everything that is MISSING that a working version would need."*

Then ask:

> *"Draw a box-and-arrow diagram showing the data flow. Label every missing component."*

**Your deliverable:** A boxology diagram and a short "Current State" paragraph describing what the page does and does not do.

### 1B. Ask your AI to explain the classifier

Open `atlas_shared/src/atlas_shared/classifier_system.py`. Give it to your AI and ask:

> *"This is the classifier for the Knowledge Atlas. Explain two things:*
> 1. *How does it decide what TYPE of article a PDF is? (empirical, review, theoretical, etc.)*
> 2. *How does it decide what TOPIC a paper belongs to? (daylight + cognition, ceiling height + creativity, etc.)*
> 
> *For each, tell me the class name, the method, and what data it looks at. Then draw a box-and-arrow diagram showing what happens inside `classify()`."*

**Your deliverable:** A boxology diagram of the classifier's internal steps.

### 1C. Identify the gap

Now you have two diagrams: what the contribute page does, and what the classifier does. The gap between them is your assignment.

> *Ask your AI: "Given these two programs, what would I need to build to connect them? Be specific — what endpoint, what data transformations, what storage?"*

> *Also ask: "Are there any existing files in the Knowledge Atlas repo that already handle article submission? Search for files with 'article' or 'submit' in their names."*

This second question is critical. Your AI should find existing infrastructure. Ask it to explain what's already built and what's missing.

**Your deliverable:** A one-paragraph gap statement: "The contribute page currently does X. The classifier can do Y. The existing backend already does Z. To complete the integration, we need W."

---

## Phase 2: Spec — Write the Contract

Write a contract called **"Classifier Integration Contract"** that specifies exactly what the fixed version should do. Your contract must include:

- **Inputs:** What the user provides (PDF, citation, or both)
- **Processing:** What the backend does with it (build evidence, call classifier)
- **Outputs on the page:** What the user sees in a results section — for each paper:
  - Whether it was **accepted**, **edge case**, or **rejected**
  - What type of article it is
  - What topic(s) it matches
  - Confidence score
- **Storage rules:**
  - Accepted papers: stored (PDF + database entry)
  - Edge-case papers: stored but flagged as edge cases
  - Rejected papers: shown in results but NOT stored
- **Success conditions:** At least 3 specific test cases with expected outcomes

### Check for duplicates before storing

Before storing any contributed PDF, check if it's already in the corpus. We provide a foolproof probe that works even on hard-to-read files:

```bash
python3 /Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/scripts/course_scaffolding.py \
  probe-collection-pdf --pdf-path /absolute/path/to/file.pdf
```

**Interpreting results:**
- `sha256_exact` or `doi_exact` → **This file is already in the corpus. Do not re-ingest it.**
- `title_fuzzy` or `page_text_match` → Possible duplicate. Inspect manually before deciding.
- No match → Safe to store as a new paper.

If you are working inside Article Finder code (not at the terminal), use the function `probe_pdf_against_article_eater(...)` in `ae_waiting_room_probe.py`.

Your contract's storage rules must include this check. A submission that stores duplicates is a bug.

### Ask your AI about storage

You need to know where PDFs go and where database entries go. Ask:

> *"In the Knowledge Atlas project, where are article PDFs stored? There's a lifecycle database — what tables does it have, and what should a new paper's entry look like when it first arrives? Show me the schema."*

> *"The pipeline has defined stages. What is the first stage a newly contributed paper should be at? What status should it have?"*

Do not accept the AI's answer at face value. Open the database yourself and check:

```bash
sqlite3 Knowledge_Atlas/160sp/pipeline_lifecycle_full.db ".schema papers"
sqlite3 Knowledge_Atlas/160sp/pipeline_lifecycle_full.db ".schema lifecycle_events"
sqlite3 Knowledge_Atlas/160sp/pipeline_lifecycle_full.db "SELECT stage_name, stage_order FROM stage_definitions ORDER BY stage_order;"
```

**Your deliverable:** The completed contract with storage paths, database column values, and duplicate-check logic filled in.

---

## Phase 3: Fix — Delegate to Your AI

Give your AI:
1. Your contract
2. The source of `ka_contribute_public.html`
3. The source of `classifier_system.py`
4. Any existing backend files your AI found in Phase 1C

Ask it to build:
1. A backend endpoint that receives the form submission and runs the classifier
2. A results section on the contribute page that shows classification results
3. Storage logic for accepted and edge-case papers

### Questions you must ask your AI to verify the fix

After your AI produces code, do NOT just run it. Ask these questions first:

> *"Show me exactly where in your code the PDF file gets saved to disk. What path does it use? What happens if that directory doesn't exist?"*

> *"Show me the line where you call `AdaptiveClassifierSubsystem.classify()`. What are you passing in as the `evidence_like` argument? Walk me through which fields of ClassificationEvidence get populated from the user's submission."*

> *"Show me where you write to the database. Which table? What values go in each column? What happens if the paper_id already exists?"*

> *"What happens when the classifier returns `next_action = 'need_abstract_or_keywords'`? Does your code handle that case, or does it silently ignore it?"*

> *"How do you distinguish an accepted paper from an edge case in storage? Show me the exact field or flag."*

> *"If I submit 5 PDFs in one session, does the results section show all 5? Or does each new submission overwrite the previous result?"*

If the AI can't answer any of these clearly, the fix is incomplete. Push back.

**Your deliverable:** The working code, plus a log of which verification questions revealed problems and how you fixed them.

---

## Phase 4: Prove — Run the Tests

### Prepare test papers

Get at least 4 PDFs:
1. A known on-topic empirical paper (e.g., one already in the Atlas)
2. A clearly off-topic paper (e.g., a machine learning paper)
3. An edge case (e.g., an architectural theory paper with no empirical data)
4. A citation-only submission (no PDF)

### Run each test and record

| Test | Input | Expected verdict | Actual verdict | Expected type | Actual type | Stored? | DB entry? | PASS? |
|------|-------|-----------------|----------------|---------------|-------------|---------|-----------|-------|
| 1 | On-topic PDF | accept | | empirical | | yes | yes | |
| 2 | Off-topic PDF | reject | | — | | no | no | |
| 3 | Edge-case PDF | edge_case | | theoretical | | yes (flagged) | yes | |
| 4 | Citation only | varies | | varies | | — | — | |

### Verify storage

For every paper that should be stored, check:

```bash
# Does the PDF file exist?
ls -la <expected_path>

# Does the database entry exist?
sqlite3 pipeline_lifecycle_full.db \
  "SELECT paper_id, article_type, current_stage, current_status FROM papers WHERE paper_id='<id>';"

# Is there a lifecycle event?
sqlite3 pipeline_lifecycle_full.db \
  "SELECT stage_name, status, agent FROM lifecycle_events WHERE paper_id='<id>';"

# Is the edge case distinguishable from the accepted paper?
sqlite3 pipeline_lifecycle_full.db \
  "SELECT paper_id, current_status FROM papers ORDER BY created_at DESC LIMIT 5;"
```

### When something fails — diagnose

For each failure, determine: **Is the spec wrong, or is the AI's implementation wrong?**

- If the classifier produces the wrong verdict → the spec may be right but the constitutions may not cover the topic. That's a classifier issue, not your bug.
- If the classifier produces the right verdict but the page doesn't show it → the AI's code has a rendering bug. That IS your bug.
- If the PDF is stored but the database entry is missing → the AI's code has a storage bug. That IS your bug.

**Your deliverable:** The completed validation matrix, plus a diagnosis note for any failures explaining whether it was a spec bug or an implementation bug.

---

## What You Submit

| Item | What it is |
|------|-----------|
| **Boxology diagrams** (Phase 1) | Two diagrams: the contribute page data flow, and the classifier's internal steps |
| **Gap statement** (Phase 1) | One paragraph: what exists, what the classifier does, what's missing |
| **Classifier Integration Contract** (Phase 2) | Your spec with inputs, outputs, storage, and success conditions |
| **Working code** (Phase 3) | The fixed contribute page, endpoint, and storage logic |
| **Verification log** (Phase 3) | Which questions you asked your AI, which revealed problems, how you fixed them |
| **Validation matrix** (Phase 4) | Test results for all 4+ test cases |
| **Storage proof** (Phase 4) | Terminal output showing the PDF exists and the DB entries are correct |
| **Diagnosis notes** (Phase 4) | For any failures: spec bug or implementation bug? |

---

## Files You Must Submit

Your submission must include a **file manifest** listing every file you changed or created, with a one-line description. The instructor will diff your repo against the upstream to verify.

Expected files (your list may differ, but these are the minimum):

| File | Change Type | What It Does |
|------|------------|-------------|
| `ka_contribute_public.html` | Modified | Form now posts to a real endpoint; results section added below the form |
| Backend endpoint file (e.g., added to `ka_article_endpoints.py` or a new file) | Modified or New | Receives form submission, runs `atlas_shared` classifier, returns JSON result |
| `data/storage/` or `data/pnu_articles/` | New files | Stored PDFs for accepted and edge-case papers |
| Database (e.g., `data/ka_auth.db` or `pipeline_lifecycle_full.db`) | Modified | New rows for submitted papers |

**How to generate your manifest:**
```bash
cd Knowledge_Atlas
git diff --name-only HEAD    # shows files you changed
git status --short           # shows new files
```

Include the output of both commands in your submission.

---

## Grading

| Criterion | What we check |
|-----------|--------------|
| **Diagnosis** | Your boxology diagrams are accurate, your gap statement is correct |
| **Spec quality** | Your contract is complete, specific, and testable |
| **Verification questions** | You asked probing questions that caught real problems in the AI's code |
| **Validation** | At least 3 of 4 test papers produce correct results and storage |
| **Diagnosis of failures** | You correctly identified whether failures were spec bugs or implementation bugs |
| **File manifest** | Your manifest is complete and matches your actual changes |
---

# Task 2: Gap Targeting & Query Generation

**Track:** Article Finder  
**What you build:** A gap extractor that reads the Article Eater's 166 PNU templates, identifies knowledge gaps, scores them by Value of Information (VOI), and generates targeted search queries in two formats: Google AI Citation (natural language) and Google Scholar Boolean.  
**Core lesson:** Before you search for anything, you must know *what* you're looking for and *why*. VOI scoring tells you which gaps matter most. Query design determines whether you find relevant papers or noise.

---

## Setup

You should already have the four repositories from Task 1:
- `Knowledge_Atlas` — the site (with your fixed contribute page)
- `Article_Finder` — the discovery pipeline  
- `Article_Eater` — the extraction engine (contains the gap data AND the VOI functions)
- `atlas_shared` — the shared classifier (installed as `pip install -e .`)

---

## Phase 1: Understand the Gap Data and VOI System

### 1A. Understand the PNU templates

The Article Eater has 166 PNU (Plausible Neural Underpinning) templates. Each describes a mechanism chain: how an environmental feature (e.g., ceiling height) leads to a psychological outcome (e.g., creativity) through neural processes. Each step has a **confidence score**. Low-confidence steps are **knowledge gaps**.

Pick 3 templates from `Article_Eater/data/templates/`. Ask your AI:

> *"These are PNU templates from the Knowledge Atlas. Walk me through one template completely: what does each step in the `mechanism_chain` represent, what does `confidence` mean for each step, and what does a low-confidence step (< 0.6) tell us about what's missing from the research corpus?"*

> *"Now look at all three templates and identify: which steps have confidence below 0.6? For each gap, tell me what specific study would fill it."*

### 1B. Understand the VOI scoring system

The Article Eater has VOI functions for scoring knowledge gaps. You will use one in this task. Ask your AI:

> *"Read `Article_Eater/src/services/voi_search.py`. Find `VOICalculator` and its `calculate_voi()` method. What inputs does it take? What does the combined VOI score mean? When would a gap get a HIGH score vs. a LOW score?"*

**What you should learn:** A gap at a hub in the belief network (high centrality, many downstream beliefs) with confidence ~0.4 scores much higher VOI than an isolated gap with confidence 0.45. VOI = "how much would knowing this change our predictions?"

### 1C. Know what's already in the corpus

Before you search for new papers, you need to know what you already have. The lifecycle database tracks every PDF in the system.

**Primary source:** `pipeline_lifecycle_full.db`, table `pdf_corpus_inventory`

This table lists every known PDF and its state:
- Whether it's in `CURRENT_GOLD` (fully processed and validated)
- Whether it's admitted but not yet gold
- Whether it's staged only
- Whether it's registry-backed

**Easiest readable version:** `pdf_corpus_inventory/latest.csv`

The summary report is at `pdf_corpus_inventory/latest.md`.

Ask your AI:

> *"Read `pdf_corpus_inventory/latest.csv`. How many papers are in CURRENT_GOLD? What topics do they cover? This tells me what we already have — I should NOT generate search queries for papers that are already in the corpus."*

If you also need to check for duplicates (same paper under different filenames or DOIs), use the companion table:

**Dedupe source:** `pipeline_lifecycle_full.db`, table `pdf_identity_inventory`  
**CSV:** `pdf_identity_inventory/latest.csv`

### 1D. Understand the two query types

You will generate queries in two formats. Read `160sp/ka_google_search_guide.html` for the full tutorial, then ask your AI:

> *"Explain the difference between a Google AI Citation query and a Google Scholar Boolean query. When would I use each? What makes one better than the other for finding specific mechanism-level evidence?"*

**Google AI Citation** (natural language — what you type into Google):
```
What neuroimaging evidence shows that exposure to natural versus urban 
environments reduces amygdala reactivity, and does this explain the 
stress-buffering effect attributed to Stress Recovery Theory?
```

**Google Scholar Boolean** (structured — what SerpAPI sends to Google Scholar):
```
("amygdala" OR "amygdala reactivity") AND ("natural environment" OR 
"nature exposure") AND ("stress" OR "cortisol") AND ("fMRI" OR 
"neuroimaging") -review
```

The key differences:
- **AI Citation** uses full sentences with theory names and mechanism descriptions. Google's AI understands synonyms and intent.
- **Boolean** uses exact keywords connected by AND/OR with quotes for phrases. Add `-review` to exclude review articles when you want primary research. Use `intitle:` to require terms in the title.

### 1D. Get a boxology diagram of the full pipeline

> *"Draw a box-and-arrow diagram of this complete pipeline (Tasks 2 and 3 combined):*
> 1. *Read PNU templates → extract gaps with confidence < 0.5*
> 2. *Score gaps using VOICalculator → sort by priority*
> 3. *Generate search queries (AI Citation + Boolean)*
> 4. *Execute searches via SerpAPI → get titles, snippets, DOIs*
> 5. *Collect full abstracts via Semantic Scholar / CrossRef / PubMed / OpenAlex*
> 6. *Triage abstracts through classifier + VOI scoring*
> 7. *Classify papers: ACCEPT / EDGE_CASE / REJECT / MISSING_ABSTRACT*
> 8. *Display PRISMA funnel on dashboard"*

**Your deliverable:** The boxology diagram, plus a list of 5 specific gaps with confidence scores.

---

## Phase 2: Build the Gap Extractor

### 2A. Write YOUR OWN contract

> **Contract objective:** "I want a program that reads PNU template JSON files and tells me which knowledge gaps are most worth searching for."
> **Contract is with:** The `VOICalculator` in `Article_Eater/src/services/voi_search.py` and the PNU templates in `Article_Eater/data/templates/`.
> **Prompt hint:** *"I need to write a contract for a gap extraction program. The program reads PNU template JSON files, walks their mechanism_chain, and uses VOICalculator.calculate_voi() to score each gap. Help me write the Inputs, Processing, Outputs, and Success Conditions sections."*

Before you ask an AI to build anything, you must write the contract yourself. This is the most important skill in this course: **if you can't spec what you want, you can't verify what you get.**

Your contract must have these four sections:

1. **Inputs** — What files does the program read? What format are they?
2. **Processing** — What does the program do, step by step?
3. **Outputs** — What does the program produce? What fields? What format?
4. **Success conditions** — How do you know it worked? Be specific. "It works" is not a success condition. "Extracts at least 10 gaps across 166 templates, each with template_id, step_number, confidence < 0.6, and gap_type" IS a success condition.

**Minimum bar** (your contract must cover at least these):
- Reads PNU template JSON files and walks `mechanism_chain`
- Extracts steps with confidence below a threshold you specify
- Scores each gap using `VOICalculator.calculate_voi()`
- Outputs structured JSON with gap_type, voi_score, and what's missing

### 2B. Write your tests BEFORE building

Ask your AI:

> *"Given my contract, what are 5 things that could go wrong? For each, write a test I can run to check. For example: 'What if a template has no mechanism_chain field?'"*

Write your tests as a checklist:
- [ ] Handles templates with no low-confidence steps (skips, doesn't crash)
- [ ] VOI scores are between 0 and 1
- [ ] Output JSON is valid and parseable
- [ ] At least 10 gaps found (if fewer, is the threshold wrong?)
- [ ] Gaps are sorted by VOI (highest first)

### 2C. Delegate to your AI, then validate

Give your AI the contract and ask it to build a Python script. Then run your tests:

> *"Show me how you read the mechanism_chain from a template. Which field has the confidence? What threshold do you use?"*

> *"Show me the VOI scores for 3 gaps. Why does one score higher than another?"*

> *"Run the script on 3 templates. Does the output match my contract's output spec? Show me the JSON."*

---

## Phase 3: Generate Search Queries

### 3A. Write YOUR OWN query generator contract

> **Contract objective:** "I want a program that takes my ranked gap list and generates search queries I can use to find papers that fill those gaps."
> **Contract is with:** The `QueryGenerator` in `Article_Eater/src/services/voi_search.py` and the patterns in `ka_google_search_guide.html`.
> **Prompt hint:** *"I need to write a contract for a query generator. It takes a JSON list of knowledge gaps (with VOI scores) and produces two search queries per gap: a Google AI Citation natural-language query and a Google Scholar Boolean query. Help me write the contract."*

Same discipline as Phase 2: **you** write the contract. Include:
1. **Inputs** — the gap list from Phase 2
2. **Processing** — how queries are generated (reference `ka_google_search_guide.html`)
3. **Outputs** — what fields per gap (both query types + gap summary)
4. **Success conditions** — at minimum:
   - At least 10 gaps have both AI Citation and Boolean queries
   - AI Citation queries are full sentences following the 5-component pattern
   - Boolean queries use `"exact phrases"`, `AND`, `OR`, and `-review`
   - At least 3 queries tested manually in Google with relevant first-page results

### 3B. Write your validation tests

> *"What makes a bad Boolean query? Give me 3 examples of common mistakes and how to detect them automatically."*

Your validation checklist:
- [ ] No Boolean query is just comma-separated words (must have AND/OR)
- [ ] Every AI Citation query ends with `?` and is > 50 characters
- [ ] Every Boolean query has at least one `"exact phrase"`
- [ ] At least 3 queries produce relevant results when tested in Google

### 3C. Use the query generation prompt

We provide a prompt template to help generate high-quality queries. See `query_generator_skill.md` in this rubrics folder.

> *Give your AI the prompt template along with 3 gaps from your extractor. Ask it to generate queries. Then manually test one AI Citation query in Google — does the first page of results contain relevant papers?*

### 3D. Verification questions

> *"Show me the Boolean query for one gap. Does it use exact-phrase quotes? Does it have OR groups for synonyms? Would Google Scholar parse this correctly?"*

> *"Show me the AI Citation query for the same gap. Does it follow the 5-component pattern? Could a researcher read this as a real research question?"*

> *"Take a gap about [specific mechanism]. Generate both query types. Now explain: which query would find a broader set of papers, and which would find more precisely targeted papers?"*

---

## Phase 4: Prove It Works

### Step 1: Run the gap extractor

```bash
python3 gap_extractor.py --templates Article_Eater/data/templates/
```

Verify:
- [ ] At least 10 gaps identified
- [ ] Gaps sorted by VOI score
- [ ] Each gap has template_id, step number, confidence, gap_type, voi_score

### Step 2: Generate queries for top 10 gaps

```bash
python3 query_generator.py --gaps gap_results.json
```

Verify:
- [ ] Each gap has both AI Citation and Boolean queries
- [ ] AI Citation queries are full sentences (not keyword lists)
- [ ] Boolean queries use AND/OR/quotes properly

### Step 3: Manual spot-check

Pick 3 queries and paste the AI Citation version into Google. For each:

| Gap | Query (first 50 chars) | First-page relevant? | Top result title |
|-----|----------------------|---------------------|-----------------|
| 1 | | Yes / No / Partial | |
| 2 | | | |
| 3 | | | |

### Step 4: Review your query quality

> *Ask your AI: "Review these 10 queries against the patterns in ka_google_search_guide.html. Which queries are strong? Which are weak? How would you improve the weak ones?"*

**Your deliverable:** Gap list, query pairs, spot-check table, and AI review of query quality.

---

## What You Submit

| Item | What it is |
|---|---|
| **Gap analysis** (Phase 1) | Boxology diagram + 5 gaps with VOI scores |
| **Gap extractor** (Phase 2) | Working script + contract |
| **Query pairs** (Phase 3) | 10+ gaps with AI Citation + Boolean queries |
| **Spot-check** (Phase 4) | Manual test of 3 queries in Google |
| **Query review** (Phase 4) | AI review of query quality |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Files You Must Change or Create

| File | Type | What It Does |
|---|---|---|
| `gap_extractor.py` | New | Reads templates, extracts gaps, scores by VOI |
| `query_generator.py` | New | Generates AI Citation + Boolean queries per gap |
| `gap_results.json` | New | Ranked gap list with VOI scores |
| `query_results.json` | New | Query pairs for each gap |

---

## Grading (60 points)

| Criterion | Points | What we check |
|---|---|---|
| **Gap extraction** | 15 | Correctly identified low-confidence steps from templates |
| **VOI scoring** | 10 | Gaps ranked by VOI; can explain why one scores higher |
| **AI Citation queries** | 10 | Follow 5-component pattern, specific enough for retrieval |
| **Boolean queries** | 10 | Proper AND/OR/quotes, not just comma-separated words |
| **Spot-check** | 5 | Tested 3 queries manually in Google, reported results |
| **Verification questions** | 10 | Caught problems in AI's implementation |

---

## A Note About Reuse

The contract → success conditions → test → validate workflow you're learning here is not a one-off. **You will reuse this exact approach in Task 3** (where you execute searches and triage results through a PRISMA funnel) and in every subsequent task. The PRISMA funnel in particular becomes a recurring deliverable — any time you add papers to the corpus, you must show the funnel proving you did it rigorously.

---

## Existing Code You Should Know About

| File | What it provides |
|---|---|
| `src/services/voi_search.py` | `VOICalculator.calculate_voi()` — scores gaps |
| `src/services/voi_search.py` | `QueryGenerator.generate_queries()` — baseline query generation |
| `src/services/voi_search.py` | `CrossFieldVocabulary.expand_query()` — cross-discipline synonyms |
| `pipeline_lifecycle_full.db` | Table `pdf_corpus_inventory` — every PDF and its state (CURRENT_GOLD, staged, etc.) |
| `pdf_corpus_inventory/latest.csv` | Readable export of the corpus inventory — check what you already have |
| `pdf_identity_inventory/latest.csv` | Dedupe info — catch duplicate papers under different names |
| `course_scaffolding.py probe-collection-pdf` | Foolproof duplicate check — run on any PDF to see if it's already in the corpus |
| `ae_waiting_room_probe.py` | `probe_pdf_against_article_eater()` — same check, callable from Python |
| `build_pdf_corpus_inventory_surface.py` | Builds the inventory surface from the lifecycle DB |
| `refresh_v7_state_surfaces.py` | Regenerates all state surfaces (run this to get fresh data) |
| `160sp/ka_google_search_guide.html` | Full tutorial on writing AI Citation queries |
| `query_generator_skill.md` | Prompt template for generating queries from gaps |
---

# Task 3: Search Execution & Abstract-First Triage

**Track:** Article Finder  
**Prerequisite:** Task 2 (you need your ranked gap list and query pairs)  
**What you build:** Execute your search queries via SerpAPI (Google Scholar), collect abstracts through a multi-source fallback chain, triage papers at the abstract level, and report results in a PRISMA-style dashboard.  
**Core lesson:** Never download a PDF to decide if it's relevant. Triage at the cheapest level — abstracts — using free APIs. Then prove your pipeline works with real PRISMA funnel numbers.

---

## What Is PRISMA and Why You're Building One

PRISMA (**Preferred Reporting Items for Systematic Reviews and Meta-Analyses**) is the gold standard for reporting systematic literature searches. It forces you to document your funnel transparently:

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

Your dashboard must show these numbers. This is proof that your pipeline works.

---

## Setup

### Get your SerpAPI key

1. Go to [serpapi.com](https://serpapi.com) and sign up (free plan)
2. Free plan gives you **250 searches/month** (non-commercial use)
3. After email + phone verification, get your API key from the dashboard
4. Store it as an environment variable: `export SERPAPI_KEY=your_key_here`

> **Budget your searches.** At 250/month, you have enough for ~10-15 gaps × 2 queries each, plus retries. Don't waste searches on test queries — test your Boolean syntax in Google Scholar manually first.

### Verify your Task 2 outputs

You need these files from Task 2:
- `gap_results.json` — ranked gaps with VOI scores
- `query_results.json` — AI Citation + Boolean query pairs per gap

---

## Phase 1: Understand the Search & Triage Architecture

### 1A. Understand SerpAPI

SerpAPI scrapes Google Scholar and returns structured JSON. Ask your AI:

> *"Read the SerpAPI Google Scholar documentation. What fields does it return per result? Does it return full abstracts? What about DOIs?"*

**What you should learn:** SerpAPI returns per result:
- `title`, `link`, `snippet` (2-3 sentence fragment, NOT the full abstract)
- `publication_info` (authors, venue, year)
- `inline_links.cited_by.total` (citation count)
- Sometimes a `resource.link` (direct PDF link)
- **It does NOT reliably return DOIs or full abstracts**

So after SerpAPI, you need a second step: look up each paper by title/DOI to get the full abstract.

### 1B. Understand the abstract fallback chain

The Article Eater has working API clients that return abstracts. When SerpAPI gives you a title but no abstract, you try each source in order:

```
SerpAPI result (title + snippet + maybe DOI)
  ↓ extract DOI from link if possible
  1. Semantic Scholar (fetch_by_doi or search by title) → abstract?
  2. CrossRef (fetch by DOI) → abstract?
  3. PubMed (search by title) → abstract?
  4. OpenAlex (api.openalex.org/works/doi:XXX) → abstract?
  5. If ALL fail → tag: MISSING_ABSTRACT
```

Ask your AI:

> *"Read `Article_Eater/src/services/paper_fetcher.py`. Find `SemanticScholarClient`, `CrossRefClient`, and `PubMedClient`. Each has a `search()` method and a `fetch()` or `fetch_by_doi()` method. Show me how I would: (1) take a title from SerpAPI, (2) search Semantic Scholar for it, (3) get the abstract from the result."*

### 1C. Understand the triage logic

After collecting abstracts, you classify each paper:

| Decision | Criteria | What happens |
|---|---|---|
| **ACCEPT** | On-topic (classifier) AND voi_score ≥ 0.5 | Stored in lifecycle DB |
| **EDGE_CASE** | On-topic but voi_score < 0.5, OR borderline topic match | Stored separately, flagged |
| **REJECT** | Off-topic per classifier | Logged but not stored |
| **MISSING_ABSTRACT** | No abstract found from any source | Stored with flag, not triaged |
| **DUPLICATE** | Already in `pdf_corpus_inventory` | Counted in PRISMA funnel, not re-triaged |

Ask your AI:

> *"Read `Article_Eater/src/cmr/voi_scoring.py`. Find `score_voi()`. What does it score — the abstract text? The finding type? How does it decide between high (0.8+), medium (0.5-0.8), and low (< 0.5)?"*

### 1D. Know what's already in the corpus (deduplication)

Before triaging a paper, check if it's already in the corpus. The lifecycle database tracks every PDF:

**Primary source:** `pipeline_lifecycle_full.db`, table `pdf_corpus_inventory`  
**Easiest readable version:** `pdf_corpus_inventory/latest.csv`

This table tells you whether a paper is in `CURRENT_GOLD` (already processed), admitted, or staged. If a search result matches a paper already in the inventory, mark it `DUPLICATE` in your PRISMA funnel — it counts as "identified" but is removed at the deduplication stage.

For matching by DOI or title, use the companion table:

**Dedupe source:** `pipeline_lifecycle_full.db`, table `pdf_identity_inventory`  
**CSV:** `pdf_identity_inventory/latest.csv`

### Foolproof duplicate check (use this)

If you have a PDF in hand and want to know whether it's already anywhere in the pipeline or corpus, use the probe tool:

```bash
python3 /Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/scripts/course_scaffolding.py \
  probe-collection-pdf --pdf-path /absolute/path/to/file.pdf
```

**Interpreting results:**
- `sha256_exact` or `doi_exact` → **Existing duplicate. Do not re-ingest.**
- `title_fuzzy` or `page_text_match` → Possible duplicate. Inspect manually before deciding.
- No match → New paper, safe to triage and store.

If you are working inside Article Finder code (not at the terminal), use `probe_pdf_against_article_eater(...)` in `ae_waiting_room_probe.py`. The test that proves this works is `test_cataloger_skips_article_eater_duplicate_before_db_insert` in `test_import.py`.

To refresh the inventory tables before starting:
```bash
python refresh_v7_state_surfaces.py
```

---

## Phase 2: Build the Search Runner

### 2A. Write YOUR OWN search runner contract

> **Contract objective:** "I want a program that takes my search queries and runs them against Google Scholar via SerpAPI, collecting structured results."
> **Contract is with:** The SerpAPI `google_scholar` engine and your query pairs from Task 2.
> **Prompt hint:** *"I need a contract for a search runner that sends Boolean queries to SerpAPI's Google Scholar endpoint, extracts DOIs from result URLs, de-duplicates by title, and records null results. Help me write Inputs, Processing, Outputs, and Success Conditions."*

Same discipline as Task 2: **you** write the contract with Inputs, Processing, Outputs, and Success Conditions.

**Minimum bar** your contract must cover:
- Takes query pairs from Task 2 as input
- Sends Boolean queries to SerpAPI's `google_scholar` engine
- Extracts DOI from result URLs where possible
- De-duplicates by title
- Records null results (gap searched, zero papers found)
- Tracks API credit usage

### 2B. Write your tests BEFORE building

Your test checklist:
- [ ] SerpAPI call uses `engine: google_scholar` (not regular Google)
- [ ] Each search costs exactly 1 credit (verify in SerpAPI dashboard)
- [ ] Total searches stay under 250
- [ ] Zero-result searches are recorded, not skipped
- [ ] Output JSON is valid and parseable
- [ ] DOI extraction regex works on 3 sample URLs

### 2C. Build and validate

Ask your AI to build it. The SerpAPI call should look like:
```python
import serpapi
params = {
    "engine": "google_scholar",
    "q": your_boolean_query,
    "api_key": os.environ["SERPAPI_KEY"],
    "num": 10
}
results = serpapi.search(params)
```

Then run your tests and verify:

> *"Show me the exact SerpAPI call. What engine are you using? What parameters?"*

> *"How many API credits does each search cost? How many searches will my pipeline run total? Will I stay under 250?"*

---

## Phase 3: Collect Abstracts

### 3A. Write YOUR OWN abstract collector contract

> **Contract objective:** "I want a program that takes SerpAPI results (which have snippets, not abstracts) and finds the full abstract for each paper from free academic APIs."
> **Contract is with:** The `SemanticScholarClient`, `CrossRefClient`, `PubMedClient` in `Article_Eater/src/services/paper_fetcher.py`, and the OpenAlex API.
> **Prompt hint:** *"I need a contract for an abstract collector. It takes search results with DOIs and tries to find full abstracts from Semantic Scholar, CrossRef, PubMed, and OpenAlex in fallback order. Papers with no abstract from any source get tagged MISSING_ABSTRACT. Help me write the contract."*

**Minimum bar** your contract must cover:
- Takes SerpAPI results as input (with DOIs where available)
- Tries multiple abstract sources in fallback order (S2 → CrossRef → PubMed → OpenAlex)
- For papers without DOIs, falls back to title-based search
- Tags papers with no abstract as `MISSING_ABSTRACT` (not silently dropped)
- Records which source provided the abstract
- Respects rate limits (Semantic Scholar: ≤ 20 req/min without API key)

**Success conditions you must define:**
- What % abstract hit rate is acceptable? (aim for ≥ 70% on papers with DOIs)
- What counts as a "found" abstract vs. a snippet?
- How do you handle ambiguous title matches?

### 3B. Write your tests BEFORE building

- [ ] Fallback chain actually tries multiple sources (not just Semantic Scholar)
- [ ] Rate limiting delays are present (check for `time.sleep` or `_RateLimiter`)
- [ ] MISSING_ABSTRACT count is tracked and reported
- [ ] Each paper's `abstract_source` field is set correctly
- [ ] Output includes `study_type` from `estimate_study_type()`

### 3C. Build and validate

> *"Show me the fallback chain. If Semantic Scholar has no abstract for a DOI, what's the next source you try?"*

> *"How do you handle rate limits? Do you add delays between API calls?"*

> *"For papers without DOIs, how do you search by title? What happens if the title match is ambiguous?"*

---

## Phase 4: Triage Abstracts

### 4A. Write YOUR OWN triage contract

> **Contract objective:** "I want a program that reads each paper's abstract and decides: is this paper worth downloading?"
> **Contract is with:** The `atlas_shared` classifier (from Task 1) and `score_voi()` from `Article_Eater/src/cmr/voi_scoring.py`.
> **Prompt hint:** *"I need a contract for an abstract triage module. It runs each abstract through the atlas_shared topic classifier, then scores it with score_voi(). Output is a 4-way classification: ACCEPT, EDGE_CASE, REJECT, or MISSING_ABSTRACT, each with a human-readable reason. Help me write the contract."*

**Minimum bar** your contract must cover:
- Runs each abstract through `atlas_shared` classifier (topic matching)
- Scores each abstract using `score_voi()` from `cmr/voi_scoring.py`
- Produces a 4-way classification: ACCEPT / EDGE_CASE / REJECT / MISSING_ABSTRACT
- Each decision includes a human-readable `triage_reason`
- ACCEPT papers stored in lifecycle DB; EDGE_CASE stored separately

**Success conditions you must define:**
- What's the minimum number of papers triaged?
- What classifier confidence threshold separates on-topic from off-topic?
- What VOI threshold separates ACCEPT from EDGE_CASE?

### 4B. Write your tests BEFORE building

- [ ] Every triaged paper has a `triage_decision` field
- [ ] Every triaged paper has a `triage_reason` (not empty)
- [ ] ACCEPT papers appear in the database
- [ ] EDGE_CASE papers are stored but flagged
- [ ] REJECT papers are logged (not silently dropped)
- [ ] MISSING_ABSTRACT papers skip triage (not scored as REJECT)

---

## Phase 5: Build the PRISMA Dashboard

### 5A. Dashboard requirements

Create a web page (`ka_topic_proposer.html` or similar) that shows:

1. **Gap Summary** — how many gaps identified, top 5 by VOI
2. **Search Summary** — how many queries run, how many results returned
3. **Abstract Collection** — how many abstracts found vs. MISSING_ABSTRACT
4. **Triage Results** — ACCEPT / EDGE_CASE / REJECT counts
5. **PRISMA Funnel** — the complete funnel with real numbers
6. **Null Results** — gaps where no papers were found

Data must persist after page refresh (use JSON file, localStorage, or API endpoint).

### 5B. The PRISMA funnel table (required deliverable)

| Funnel Stage | Count |
|---|---|
| Gaps targeted (from Task 2) | |
| Queries executed (SerpAPI) | |
| Records returned | |
| Duplicates removed | |
| Abstracts collected | |
| MISSING_ABSTRACT (no abstract found) | |
| Screened by classifier | |
| → ACCEPT (on-topic, high VOI) | |
| → EDGE_CASE (borderline) | |
| → REJECT (off-topic) | |

---

## Phase 6: Prove It Works

### Step 1: Run the full pipeline

```bash
python3 search_runner.py --queries query_results.json
python3 abstract_collector.py --results search_results.json
python3 abstract_triage.py --papers papers_with_abstracts.json
```

### Step 2: Trace one paper end-to-end

Pick ONE paper that made it through the entire pipeline:

```
Gap source: Template T__ step __ (confidence: 0.__, VOI: 0.__)
  → Boolean query: "_______________"
  → SerpAPI result #__ of __
  → Title: [paper title]
  → DOI: [if found]
  → Abstract source: Semantic Scholar / CrossRef / PubMed / OpenAlex
  → Abstract: [first 100 chars...]
  → Classifier: topic=Q__, confidence=0.__
  → VOI score: 0.__, bucket=high/medium/low
  → Triage: ACCEPT / EDGE_CASE
  → Stored at: [DB entry or file path]
```

### Step 3: Report null results

For high-VOI gaps with zero search results:

```
Gap: Template T__ step __ (VOI: 0.__)
  Description: _______________
  Queries tried: [list]
  Result: NO PAPERS FOUND
  Implication: This gap may be genuinely unfilled in the literature.
```

### Step 4: Report MISSING_ABSTRACT papers

```
Papers with MISSING_ABSTRACT: N out of M total
  Example: [title] — no abstract from any source
  These papers cannot be triaged but are stored for future manual review.
```

---

## What You Submit

| Item | What it is |
|---|---|
| **Search results** | Raw SerpAPI results as JSON |
| **Abstract collection** | Papers with abstracts + source attribution |
| **Triage results** | ACCEPT/EDGE_CASE/REJECT/MISSING_ABSTRACT decisions |
| **PRISMA funnel** | Completed funnel table with real numbers |
| **Dashboard** | Working web page showing pipeline results |
| **End-to-end trace** | One paper from gap → SerpAPI → abstract → triage → store |
| **Null result report** | Gaps where no papers were found |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Files You Must Change or Create

| File | Type | What It Does |
|---|---|---|
| `search_runner.py` | New | Calls SerpAPI with Boolean queries |
| `abstract_collector.py` | New | Collects abstracts via fallback chain |
| `abstract_triage.py` | New | Runs classifier + VOI on abstracts |
| `search_results.json` | New | Raw SerpAPI results |
| `triage_results.json` | New | Triage decisions with reasons |
| `ka_topic_proposer.html` | New | PRISMA dashboard |
| Database | Modified | New entries for ACCEPT papers |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **SerpAPI integration** | 10 | Successfully queried Google Scholar, got results |
| **Abstract collection** | 15 | Fallback chain works; ≥70% abstract hit rate on DOI papers |
| **Abstract triage** | 15 | Classifier + VOI → defensible ACCEPT/EDGE_CASE/REJECT |
| **PRISMA funnel** | 10 | Dashboard shows real numbers at each stage |
| **End-to-end trace** | 10 | One paper fully traced through pipeline |
| **Null results + MISSING_ABSTRACT** | 5 | Documented, not treated as failures |
| **Verification questions** | 10 | Caught real problems in AI's implementation |

---

## A Note About Reuse

The contract → success conditions → test → validate workflow is not a one-off. **You will reuse this PRISMA approach in every future task** that involves adding papers to the corpus. Your PRISMA dashboard should be designed for reuse — when you run new searches in future tasks, the same funnel should update with new numbers. Think of it as infrastructure, not a throwaway deliverable.

---

## Existing Code You Should Know About

| File | What it provides |
|---|---|
| `src/services/paper_fetcher.py` | `SemanticScholarClient.search()` + `fetch_by_doi()` |
| `src/services/paper_fetcher.py` | `CrossRefClient.search()` + `fetch()` |
| `src/services/paper_fetcher.py` | `PubMedClient.search()` + `fetch()` |
| `src/services/paper_fetcher.py` | `PaperFetcher.search()` — unified multi-source |
| `src/services/paper_fetcher.py` | `estimate_study_type()` — auto from abstract |
| `src/services/paper_fetcher.py` | `UnpaywallClient` — checks OA availability |
| `src/cmr/voi_scoring.py` | `score_voi()` — scores findings by information value |
| `src/services/discovery_funnel.py` | `classify_closure()` — FULL/PARTIAL/NONE/NEGATIVE |
| `pipeline_lifecycle_full.db` | Table `pdf_corpus_inventory` — every PDF and its state |
| `pdf_corpus_inventory/latest.csv` | Readable export — check what's already in the corpus |
| `pdf_identity_inventory/latest.csv` | Dedupe info — catch duplicate papers under different names |
| `course_scaffolding.py probe-collection-pdf` | Foolproof duplicate check — run on any PDF to see if it's already in the corpus |
| `ae_waiting_room_probe.py` | `probe_pdf_against_article_eater()` — same check, callable from Python |
| `refresh_v7_state_surfaces.py` | Regenerates all state surfaces (run before starting) |
| `atlas_shared` | Topic classifier (from Task 1) |
