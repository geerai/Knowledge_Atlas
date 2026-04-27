# Paper-Quality Build Prompt — for Codex

**Document**: `PAPER_QUALITY_BUILD_PROMPT_FOR_CODEX_2026-04-23.md`
**Target executor**: Codex in terminal with access to
`/Users/davidusa/REPOS/` on DK's Mac, plus push rights on
`github.com/dkirsh/atlas_shared`, `github.com/dkirsh/Knowledge_Atlas`,
and the Article_Eater repo.
**Authorising reviewer**: DK, 2026-04-23. Hardened 2026-04-25.
**Companion reading**:
`PAPER_QUALITY_PANEL_CONSULTATION_2026-04-23.md` (methodology);
`PAPER_QUALITY_SYSTEM_DESIGN_2026-04-23.md` (ground-truth
specification);
`PAPER_QUALITY_TESTING_PROMPT_FOR_CODEX_2026-04-25.md` (adversarial
tests run *after* this build completes — read it now so you understand
which behaviours will be probed). Read all three before writing code.

---

## 0. Read first

- The panel consultation. Do not re-open any design question it
  settles (field list, threshold values, weighting function,
  rhetorical-flag treatment, open-science-norm dating).
- The system design document. It names every file path, every
  contract you must write, every test that must exist at the end,
  and every SQL table. If the design document and this prompt ever
  disagree, the design document wins.
- `atlas_shared/AGENTS.md` — the "Do Not Reinvent" contract.
- The existing atlas_shared contract-naming convention. Every contract
  you produce follows the seven-section template used in
  `atlas_shared/contracts/` already: Scope / Inputs / Outputs /
  Success conditions / Non-promises / Test coverage / References.

## 1. Scope boundary

This prompt covers the paper-quality fingerprint layer end-to-end —
extraction, adjudication, storage, aggregation, HTTP surface, UI
block, overseer rollup, master-doc update. It does **not** cover:
retrofitting fingerprints onto the existing 1 400-paper corpus
(that is a separate follow-up run once the pipeline is live); adding
any new fields beyond the eleven in the design document; altering the
warrant graph, the argumentation layer, or any other atlas layer.

If you believe any of those things are necessary, stop and post the
blocker to `COORDINATION.md` under `### CW paper-quality build —
blocker`. Do not proceed past the blocker without DK's sign-off.

## 1.5 LLM access constraint — subscription-only, ballistic operation (added 2026-04-25)

**Hard constraint**: every LLM call in this build, in calibration runs,
in the testing pass, and in the live pipeline must be made through
subscription-based chat interfaces, not through per-call API
endpoints. The cost of API-billed multi-LLM agreement at the scale of
1 400 papers × 11 fields × 5 self-consistency samples × 2 model
families is not in budget; subscription-billed automation is.

**What "ballistic" means here**, borrowing the cognitive-science
sense: the build runs as automated, fire-and-forget conversation
sequences through the chat interfaces, without halting for human
input mid-run. State is logged; errors are recorded; the next paper
is processed; review happens after the run completes. This pairs
with the failure-handling change in §5: hard-rule violations are
recorded and skipped, not raised as halt-the-build exceptions.

**Implementation implications**:

- The Claude-class adapter drives Claude through Claude Desktop or
  Cowork, not the Anthropic API. The OpenAI-class adapter drives
  ChatGPT Plus through its desktop or browser interface, not the
  OpenAI API.
- The audit log records subscription session ID, conversation ID,
  and message timestamps in place of API call IDs. The schema for
  `fingerprint_extraction_events` is updated accordingly.
- Per-token logprobs are not exposed by subscription chat interfaces.
  Hard Rule 9 specifies a sampling-based proxy that does not need
  logprobs.
- A unit test asserts that no `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`
  environment variable is read during extraction. If either is
  read, the test fails. The test is part of the CI matrix.
- Throughput differs from API. Subscription rate limits, conversation
  context limits, and re-authentication requirements all apply. The
  retrofit pass on the existing 1 400-paper corpus may take weeks
  rather than hours; that is acceptable.
- "Ballistic" automation is via Cowork agents, browser automation
  (Playwright or equivalent), or desktop automation — whatever
  pattern the rest of the lab's tooling uses. Do not invent a new
  harness; reuse what exists.

**What is *not* affected**: the eleven extractable fields, the four
sidecars, the seven-section contract template, the
`PaperQualityFingerprint` dataclass shape, the schema, the HTTP
endpoints, the UI block. Only the LLM-call layer changes.

If subscription-based access proves infeasible for a specific field
(for example, ChatGPT Plus rate limits prevent dual-model agreement
on the construct-validity field at the required cadence), stop and
post the blocker per the standard procedure. Do not silently fall
back to API.

**Implementation note (revised 2026-04-25)**: The CLI subprocess
pattern used by `atlas_shared.cli_adjudicator` is the canonical
adapter. `claude -p --output-format json` for Claude-class;
`codex exec -m <model>` for OpenAI-class. Both authenticate via
subscription OAuth login, never API keys. The build extends the
existing pattern with eleven per-field prompts and the paper-quality
output schema; it does not invent new harness infrastructure.

## 1.6 Coordination model — blackboard, not heartbeat (added 2026-04-25)

Per DK 2026-04-25: the existing HTTP coordination server has decayed
into disuse (state file timestamps from 2026-03-11 / 03-12 despite
substantial multi-agent work since), and the failure mode is
structural rather than disciplinary. This build adopts a *blackboard
architecture* in which the database itself is the source of truth
and self-report is decorative.

**Read first**: `docs/PAPER_QUALITY_BLACKBOARD_DESIGN_2026-04-25.md`.
That document specifies the tables, the worker loop, the JSON
mirror cadence, and the failure-recovery semantics in full. It is
companion reading for this prompt and you must follow its rules.

Summary for orientation:

- Two new tables (`paper_quality_batches`, `paper_quality_jobs`)
  and one view (`paper_quality_progress`) added to
  `pipeline_lifecycle_full.db` in Commit 7.
- Work is batched: 25–30 papers per batch (per DK Q-2 of 2026-04-25,
  smaller than the 350-paper ranges originally proposed).
- Workers claim one batch at a time via atomic DB update; finish all
  papers in it; claim another. No upfront partition of the corpus.
- Per-paper progress signal: `last_progress_at` is updated after
  each paper completion. 30-min stall → `timeout_warning`; 4-hour
  stall → batch becomes `reclaimable`. Per DK: no preemptive
  reclamation; the 4-hour timeout is a tail-only mechanism.
- Cross-sandbox visibility via `data/paper_quality_progress.json`,
  updated per-paper, committed locally frequently, pushed to GitHub
  every roughly 50 papers (per DK Q-3 of 2026-04-25).
- Heartbeats remain advisory for the dashboard; they are not
  load-bearing for any work-claiming or completion semantics.

**Concurrency given DK's subscriptions** (Codex Pro, Claude Max,
high-tier Gemini):

- 4 Claude CLI workers, 4 Codex CLI workers, 1-2 Gemini verifiers,
  1 mirror/dashboard process.
- Combined extraction throughput at peak: ~130 papers fully
  processed per day, completing the 1 400-paper retrofit in
  ~11 working days (5-sample SC) or ~7-8 days (3-sample SC on
  retrofit only, 5-sample on calibration).

A new commit in the execution plan handles the blackboard
initialiser:

**Commit 6.5 (new)** —
`scripts/paper_quality_blackboard_init.py`:
the pre-flight script that generates the manifest (4 200 jobs in
150 batches), populates `paper_quality_jobs` and
`paper_quality_batches` rows, writes the empty mirror at
`data/paper_quality_progress.json`, and commits/pushes. Idempotent
(safe to re-run; `INSERT OR IGNORE`). Lands between Pass 2's golden-
file tests (Commit 6) and Pass 3's schema migration (Commit 7).

**Worker loop wrapper** —
`atlas_shared/src/atlas_shared/worker_loop.py` (added in Commit 1
alongside the dataclass): the shared loop that the three adapter
wrappers (Claude CLI, Codex CLI, Gemini) all import. Contains the
`claim_next_batch`, `mark_paper_done`, `record_hard_rule_violation`,
`refresh_mirror_for_paper`, `commit_local`, `push_to_github`
helpers. Per the design doc §4.

## 2. Pre-flight

```bash
cd /Users/davidusa/REPOS/atlas_shared
git fetch origin && git checkout master && git pull --ff-only
git checkout -b paper-quality-2026-04-23

cd /Users/davidusa/REPOS/Knowledge_Atlas
git fetch origin && git checkout main && git pull --ff-only
git checkout -b paper-quality-2026-04-23

cd /Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery
git fetch origin && git checkout <current-branch> && git pull --ff-only
git checkout -b paper-quality-2026-04-23

# Baseline tests — record counts before touching any code
cd /Users/davidusa/REPOS/atlas_shared && pytest -q | tail -5
cd /Users/davidusa/REPOS/Knowledge_Atlas/backend && pytest -q | tail -5
cd /Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery \
    && pytest -q 2>&1 | tail -5
```

Record the three baseline pass/fail/skip counts in a scratch file.
Every commit below must preserve or improve these counts. Any
regression stops the work pending DK review.

## 3. Execution plan — twelve commits across three repos

The build is sequenced so that each commit lands in a runnable,
testable state. Do not batch. After each commit, run the repo's
test suite; if it regresses, revert and fix before the next commit.

### Pass 1 — atlas_shared foundations (commits 1–4)

**Commit 1** — `atlas_shared/src/atlas_shared/paper_quality.py`:
the `PaperQualityFingerprint` dataclass and Pydantic schema, the
`FingerprintField[T]` generic wrapper, the `PreregRecord`,
`EffectSize`, `PowerRecord` dataclasses. All `frozen=True` per
atlas_shared convention. Exported from `atlas_shared/__init__.py`
under a new group-import. Add the module name to `__all__`. Follow
the existing atlas_shared code style exactly.

**Commit 2** —
`atlas_shared/contracts/PAPER_QUALITY_FINGERPRINT_CONTRACT_2026-04-23.md`:
the contract following the seven-section template, body text
cribbed from §2 of the design document. Also updates
`atlas_shared/AGENTS.md` with one new "canonical shared module"
line pointing at `atlas_shared.paper_quality.PaperQualityFingerprint`.

**Commit 3** — `atlas_shared/src/atlas_shared/claim_strengths.py`:
the `ClaimStrengthsWeaknesses` dataclass, the aggregation function
`aggregate_claim_strengths(claim_id, warrants, fingerprints,
overlap_edges) -> ClaimStrengthsWeaknesses`, the weighting function
with a `WEIGHTING_FUNCTION_VERSION` constant, the I²
computation, the Egger funnel-plot-asymmetry test, the sample-overlap
deduplication using the overlap-edges graph. Pure functions, no
database access. Prose-summary generation via a template with named
slots, not an LLM.

**Commit 4** — `atlas_shared/src/atlas_shared/literature_body.py`:
the `LiteratureBodyQuality` dataclass and aggregation function.
Five summary statistics per §6 of the design doc. Pure functions.
Ship companion contract
`LITERATURE_BODY_QUALITY_CONTRACT_2026-04-23.md` in the same commit.

After Pass 1: atlas_shared pytest should be green. A synthetic
five-paper fixture produces the expected claim- and
literature-body aggregates; tests in `atlas_shared/tests/`.

### Pass 2 — Article_Eater extraction (commits 5–6)

**Commit 5** —
`Article_Eater_PostQuinean_v1_recovery/src/services/paper_quality_extraction.py`:
the LLM-based eleven-field extractor. Uses the same LLM-adapter
interface as existing `atlas_shared.cli_adjudicator`. Per-field
prompts stored in
`Article_Eater_PostQuinean_v1_recovery/prompts/paper_quality/*.md`,
one file per field, so prompts are reviewable. The extractor writes
an entry to `fingerprint_extraction_events` (new table in the AE
registry; see Commit 8 for the migration) on every run.

**Commit 6** —
`Article_Eater_PostQuinean_v1_recovery/tests/test_paper_quality_extraction.py`:
twenty golden-file tests, each with a fixture PDF excerpt and an
expected fingerprint. Use the 20-paper calibration subset DK
curates in `atlas_shared/tests/fixtures/paper_quality_calibration/`.
The first five fixtures must span: lab experiment, field study,
secondary analysis, meta-analysis, theoretical paper.

**Adversarial fixtures (mandatory addition, four extra fixtures
beyond the twenty).** These are designed to catch heuristic
shortcuts. Every one must extract correctly via LLM and produce a
distinct flag in the fingerprint when it does:

1. *Multi-effect paper* — a primary empirical paper that reports
   five effect sizes across three studies and whose abstract foregrounds
   the largest. The fixture's expected fingerprint records all five
   effect sizes with their CIs and flags abstract–results emphasis
   asymmetry. A regex-based extractor will mis-pick the single largest
   effect; the test fails if `effect_sizes_count != 5`.
2. *OSF-mentioned-but-not-preregistered paper* — mentions OSF in the
   discussion as a place data will be deposited but has no
   preregistration URL or timestamp. The expected fingerprint marks
   `preregistered = False` and `osf_present_but_not_prereg = True`. A
   keyword extractor will mark this preregistered; the test fails if
   `preregistered == True`.
3. *Scattered-sample paper* — sample composition is described in four
   separate paragraphs (recruitment in §2.1, demographics in §2.3,
   exclusions in §2.5, final analytic sample in §3.1). The expected
   fingerprint records the final analytic N and the country
   composition, and notes the reconstruction. A pattern-based extractor
   will record the recruitment N as the sample N; the test fails if
   `sample_n_total != analytic_N`.
4. *Hedged construct paper* — the construct claim uses hedging language
   ("may suggest", "consistent with", "appears to support") that a
   regex will pass over. The expected fingerprint records the hedge
   spans and elevates the construct-validity verdict to multi-LLM
   adjudication. A keyword detector will record an unqualified claim;
   the test fails if `rhetorical_hedge_count == 0`.

If any of the four adversarial fixtures passes without flags, the
extractor is using shortcuts and the build halts pending DK review.
This is non-negotiable.

Add a calibration-run script that reports precision/recall per field
over the full 20-paper anchor set plus the four adversarial fixtures;
run it and commit the baseline report.

After Pass 2: `pytest -q` in Article_Eater stays green; the
calibration-report baseline is recorded in
`Article_Eater_PostQuinean_v1_recovery/reports/paper_quality_calibration_2026-04-23.md`.

### Pass 3 — Knowledge_Atlas storage + surface + UI (commits 7–11)

**Commit 7** — `contracts/schemas/paper_quality.sql` in
Knowledge_Atlas: the three tables and two views from §4 of the
design document, plus the new `hard_rule_violations` and
`holding_pen` view from §5.1, plus the `paper_interpretation`
stub table from PQ-INTERP-001 (per DK 2026-04-25, Q21), plus the
`paper_quality_batches` and `paper_quality_jobs` tables and the
`paper_quality_progress` view from
`PAPER_QUALITY_BLACKBOARD_DESIGN_2026-04-25.md` (added 2026-04-25
per §1.6 of this prompt).

The `paper_interpretation` stub has columns:
`paper_id PRIMARY KEY`, `interpretation_cue TEXT NULL`,
`interpretation_layer_version TEXT NULL`,
`fingerprint_id REFERENCES paper_quality_fingerprints(id)`,
`created_at`, `updated_at`. No logic populates it in this build;
the table exists so the eventual interpretation pass lands its
schema migration as an additive change rather than a structural
one. A FK constraint to `paper_quality_fingerprints` is created
so the relationship is explicit even before rows exist.

A migration script
`scripts/migrations/2026_04_23_paper_quality.sql` applies the
schema to the existing atlas database. Idempotent (safe to re-run).

**Commit 8** — `backend/app/api/v1/routes/quality.py`: the three
HTTP endpoints (claim strengths, literature-body quality, per-paper
fingerprint). Each endpoint has a Pydantic `response_model` per the
atlas's existing F3 convention. Endpoints return 503 with a
`Retry-After` header when the materialised view is refreshing.
Pytest fixtures seed a five-paper fixture corpus and assert each
endpoint's response shape.

**Commit 9** — `160sp/ka_admin.html`: add an Adjudication Queue tab.
Per the design doc §3, the tab shows every fingerprint routed to
adjudication, with the LLM suggestion, the source excerpt, and the
confidence score visible for every field. Adjudication writes back
via `POST /api/v1/admin/paper_quality/adjudicate`. Authorization
gated by the existing instructor-tier JWT check.

**Commit 10** —
`ka_claim_quality.js` + an expandable block on
`ka_journey_interpretation.html` and `ka_journey_evidence.html`:
the UI component that renders strengths-and-weaknesses on every
claim-detail page. Hover tooltips on each listed field link to the
glossary (glossary already exists; add four new entries for
"construct validity", "Egger test", "I² heterogeneity", "WEIRD
sample"). Follow the existing `ka_journey_surface.js` style.

**Commit 11** — `scripts/overseer_paper_quality_rollup.py`: the
daily/weekly rollup generator from §8 of the design doc. Writes
`docs/PAPER_QUALITY_OVERSEER_LOG_<date>.md` and appends to
`COORDINATION.md` under a dedicated heading. Cron entry example in
the docstring.

After Pass 3: Knowledge_Atlas pytest green; manual smoke through the
admin adjudication queue with a synthetic low-confidence fingerprint;
manual smoke through the claim-strengths block on a fixture claim;
overseer rollup script produces a valid markdown file.

**Forced-disagreement smoke (mandatory addition).** Beyond the
single low-confidence fingerprint, construct a deliberately
disagreeing pair: the same paper run through both extraction
adapters with the second adapter's prompt nudged to produce a
different construct-validity verdict. Confirm that the adjudication
queue (a) catches the disagreement, (b) presents both candidate
verdicts side-by-side with the source excerpts each cited, and (c)
records the adjudication outcome with the `WEIGHTING_FUNCTION_VERSION`
and `model_pair_id` so the calibration history can attribute drift
correctly. A queue that silently picks the higher-confidence verdict
without surfacing the disagreement is a regression and the build
fails.

### Pass 4 — integration + master doc (commit 12)

**Commit 12** — the integration pass that makes the layer live end
to end:

- Update `docs/MASTER_DOC_CMR_ASSEMBLED.md` with the new section
  on the paper-quality fingerprint layer per §9 of the design doc.
- Update `docs/AUDIT_README.md` with the SHA-pinned entries for the
  panel consultation, design document, six contracts, and build
  prompt. One-line summary per entry.
- Register the new route under `app/api/v1/routes/__init__.py` so
  the endpoints are exposed.
- Run the full three-repo test matrix:
  `cd atlas_shared && pytest -q`
  `cd Knowledge_Atlas/backend && pytest -q`
  `cd Article_Eater/... && pytest -q`
  All three must match or exceed their pre-flight baselines. Any
  regression stops the commit pending DK review.
- Post the post-build rollup to `COORDINATION.md` under
  `### CW paper-quality build — landed`.

## 4. Hard rules

1. **Do not modify atlas_shared outside this branch.** The
   don't-alter-atlas_shared rule from the deploy handoff is paused
   for this session only, per DK's sign-off on the panel's design.
   When this branch merges, the don't-alter rule resumes for the
   next session.
2. **Do not bypass the adjudication queue.** A fingerprint whose
   extractor confidence is below the 0.85 auto-accept threshold on
   any field must route to the queue. No temporary flag to disable.
3. **Do not weight by paper age.** The panel explicitly rejected
   age-dependent quality deductions. If you find yourself writing a
   coefficient keyed on year, stop.
4. **Do not aggregate rhetorical flags into numeric scores.** Per
   the panel's rule on Simmons's lens, these are human-review-only
   and surfaced to readers as observations.
5. **Every schema change ships its migration.** If you add a column
   to `paper_quality_fingerprints` after Commit 7, a new migration
   script with a later date suffix ships in the same commit.
6. **No force-push. No rebase of shared history.** Branch work only.

7. **LLM-required fields cannot be extracted by regex, keyword
   match, or other heuristic.** Of the eleven fingerprint fields,
   seven are *semantic* and *must* be extracted by LLM call:
   construct claim parsing, sample composition narrative,
   multiple-comparisons handling, conflict-of-interest disclosure
   interpretation, replication-record search, rhetorical-flag
   detection, and effect-size precision (because units, direction,
   and CI structure require semantic reading, not regex). The
   remaining four (preregistration URL, data-availability statement
   text, code-availability statement text, raw N digits) may use
   programmatic verification *as a redundant check after the LLM
   call*, never *instead of* it. Each LLM-required field's unit test
   asserts the LLM was actually invoked: it counts API calls, checks
   the model name in the call log, and fails if zero calls were
   made. A future PR that swaps in a regex shortcut breaks the test
   suite by construction. The four programmatic-eligible fields
   still log every regex match for audit. There is no "fast path"
   that disables LLM calls, even temporarily, even in CI. If the
   build needs a faster local-development mode, gate it behind an
   explicit `PAPER_QUALITY_DEV_FAST=1` env variable that the test
   suite refuses to honour.

8. **Multi-LLM agreement runs both adapters as independent
   processes.** The Claude-class and OpenAI-class extractions must
   each construct their own prompt from the per-field prompt
   template, send it to their respective subscription chat
   interface, parse the response, and write the result to
   `fingerprint_staging` independently. No "skip the second model
   when the first is confident" optimisation. No re-using the first
   model's parsed output as context for the second. No batching that
   lets two papers' contexts mingle in either adapter. The
   adjudication step's input must be two structurally-independent
   fingerprint records keyed by `(paper_id, model_pair_id)`. A test
   asserts that across 50 papers, every paper produced at least one
   Claude conversation and one ChatGPT conversation, with
   non-overlapping prompt hashes per field. Faking multi-LLM
   agreement by running one model twice (whatever the sampling
   parameter) is a regression and the build fails. The whole
   calibration strategy depends on this rule; cutting it invalidates
   everything downstream.

   **Sanctioned exception — adjudication UI display only.** The
   adjudication queue UI displays both verdicts side-by-side for
   the human adjudicator (DK or instructor). This is the only
   context where the two outputs sit together. The exception
   applies to *display*, never to *extraction* or *automated
   downstream consumption*. Code that reads both verdicts
   simultaneously must be the adjudication-UI render path, period.

9. **Confidence is reported with a distributional summary, not a
   single point estimate.** Subscription chat interfaces do not
   expose per-token logprobs, so the distributional summary is built
   from sampling rather than from the underlying probability stream.
   Every per-field confidence in `fingerprint_staging` records:
   (a) the point estimate (the model's self-reported confidence in
   the structured response, parsed from a confidence field in the
   conversation output);
   (b) **self-consistency across five samples** at the chat
   interface's nearest equivalent of temperature 0.3 — for Claude
   Desktop / Cowork, this is the default conversational
   distribution at "balanced" creativity; for ChatGPT Plus,
   equivalent. Five rather than three (per DK 2026-04-25, Q6) for a
   tighter variance estimate;
   (c) a sampling-based logprob proxy: the across-sample agreement
   rate on the field's primary value, scaled to [0, 1]. The empirical
   correlation between this proxy and Anthropic-API logprobs (where
   the API has been used historically for this lab) is documented
   in `atlas_shared/contracts/SAMPLING_LOGPROB_PROXY_2026-04-25.md`
   and is sufficient for adjudication routing;
   (d) for list-valued fields (effect sizes, rhetorical flags,
   sample-composition entries), the per-element agreement rate
   across the five samples.

   Adjudication-queue routing reads (b) and (c) — a field that
   drifts across self-consistency samples is queued even if the
   point confidence is above the 0.85 threshold.

   A reporting test runs the calibration set and asserts that no
   field's confidence distribution has its mass spiked at exactly
   the 0.85 threshold or any single threshold-adjacent value
   (0.86–0.89): that pattern indicates threshold-gaming and the
   build fails.

## 5. Failure handling — log-and-continue (revised 2026-04-25, Q15)

Per DK's 2026-04-25 instruction, the build operates *ballistically*:
hard-rule violations and per-paper extraction failures are recorded
and the next paper is processed. The build does not halt for human
intervention mid-run. Review happens after the run completes.

### 5.1 Per-paper hard-rule violations

When a hard-rule violation is detected on a specific paper during
extraction (e.g., Hard Rule 7's LLM-required canary fails because
the per-field prompt was misconfigured for that paper, or Hard
Rule 8's independence check sees the second model timed out and a
shortcut was attempted), the violation is recorded and the paper
is held back from the live aggregation:

- A row is written to a new table `hard_rule_violations` with
  columns: `paper_id`, `rule_id` (e.g., `HARD_RULE_7`,
  `HARD_RULE_8`, `HARD_RULE_9`), `field_name`, `violation_state`
  (machine-readable JSON capturing prompt hash, conversation IDs,
  parsed responses, and the specific assertion that failed),
  `violation_timestamp`, `requires_dk_review` (boolean, default
  TRUE).
- The paper's fingerprint is *not* committed to
  `paper_quality_fingerprints`. It stays in `fingerprint_staging`
  with status `held_for_review`.
- The build proceeds to the next paper. There is no halt.
- A summary row is added to a `holding_pen` view that DK reads
  after the run.

A migration script ships in Commit 7 (alongside the schema
migration) creating `hard_rule_violations`, `holding_pen`, and the
status enum addition.

### 5.2 Build-time errors that halt anyway

Two classes of error still halt the build, because they invalidate
*every subsequent paper*, not just the one in flight:

1. **Calibration-set precision below 70 % on any field after
   Commit 6.** The extractor is not trustworthy for that field on
   any paper; continuing produces 1 400 unreliable fingerprints.
2. **Schema migration failure or test-suite regression after any
   commit.** The next commit cannot land cleanly on broken
   foundations.

In both cases, post the failing command, the full error output, and
a one-sentence hypothesis to `COORDINATION.md` under `### CW
paper-quality build — blocker`. Do not guess past the error.

### 5.3 Subscription-interface errors

Rate-limit errors, authentication-expiry errors, and conversation-
context-overflow errors from the subscription chat interfaces are
*expected* and are handled with retry-with-backoff up to three
attempts per paper. A fourth failure is recorded as a hard-rule
violation per §5.1 and the paper is held. The retry policy is
implemented in `atlas_shared.subscription_adapter` and shared
between the Claude and ChatGPT adapters.

## 6. Reporting

At the end of the build, post to `COORDINATION.md`:

- Twelve commit SHAs (one per commit above), with repo and commit
  message.
- Three-repo pytest counts pre and post (expect identical or
  improved).
- Calibration-report baseline numbers for every field.
- Any fields that landed at auto-accept confidence < 0.90 (not a
  blocker, but worth DK's eyes).
- Any deviations from this prompt and why.
- Adjudication-queue depth after the synthetic smoke test (expect
  zero before real papers enter).
- **Per-field LLM call counts** across the 24-fixture calibration
  run: one row per field, columns for Claude-class call count,
  OpenAI-class call count, mean tokens per call, and total
  wall-clock seconds. A field with suspiciously low token counts
  (< 50 mean tokens for a semantic field) or zero calls in either
  column triggers an automatic flag for DK review.
- **Self-consistency variance** per LLM-required field across the
  five-sample runs (per DK 2026-04-25, Q6): mean Jaccard similarity
  for list-valued fields, mean absolute difference for numeric
  fields, Krippendorff's α for categorical fields. Variance close
  to zero on a field where the calibration set shows legitimate
  paper-to-paper variation indicates a deterministic shortcut and
  is a flag.
- **Hard-rule-violation tally** from `hard_rule_violations`: count
  per rule, per field, per offending model adapter; one-line summary
  of the most common violation pattern. The tally is the primary
  artefact DK reads to decide what to do with the
  `held_for_review` papers.
- **Subscription-interface error tally**: count of rate-limit
  retries, authentication-expiry events, and context-overflow
  events per adapter. A spike here indicates the throughput plan
  needs revision before the retrofit pass on the 1 400-paper
  corpus.
- **Confidence-distribution histogram** per LLM-required field
  across the calibration run: ten bins from 0.0 to 1.0, count of
  fields landing in each bin. A bin spike at 0.85–0.89 across
  multiple fields indicates threshold-gaming and the build does not
  ship pending DK sign-off.

Tag CW on COORDINATION.md when done.

## 7. Timeline

This is a two-to-three-day build. Pass 1 (atlas_shared) is one day.
Pass 2 (Article_Eater) is half a day plus a half-day calibration
run. Pass 3 (Knowledge_Atlas) is one day. Pass 4 (integration) is a
few hours.

If Pass 2's calibration run takes more than four hours of wall-clock
time, post progress to COORDINATION.md and continue.

## 8. After the build

The layer goes live for new papers immediately after Commit 12.
Retrofitting fingerprints onto the existing 1 400-paper corpus is a
separate follow-up run DK will schedule. Do not start that run from
this branch.

A DK review of the twelve commits follows. On approval, the branches
merge to `master`/`main` in the standard order: atlas_shared first
(because Knowledge_Atlas and Article_Eater depend on it), then
Article_Eater, then Knowledge_Atlas.

After merge, run the testing prompt
(`PAPER_QUALITY_TESTING_PROMPT_FOR_CODEX_2026-04-25.md`) against the
landed branches before the layer goes live to real papers. The
testing prompt is the second gate; this build prompt is only the
first.

## 9. Why these rules look paranoid

These hardening rules — particularly Hard Rules 7, 8, and 9, the
adversarial fixtures, the forced-disagreement smoke, and the
distributional confidence reporting — exist because a previous
generation of automation in this lab has shown a reliable habit of
substituting Python heuristics for LLM calls when work feels
repetitive, of parallelising in ways that re-use one model's output
as the other model's "agreement" check, and of converging confidence
estimates onto threshold-adjacent values that bypass adjudication.
Those shortcuts are individually plausible engineering decisions
that, taken together, invalidate the calibration strategy and
silently degrade fingerprint quality below what the design package
claims.

The rules in this document are written so that each shortcut, if
attempted, fails a specific test rather than slipping through. The
rules are not optional and the tests are not adjustable from inside
the build branch. If a rule looks unnecessary on a particular paper,
post the case to `COORDINATION.md` under `### CW paper-quality build
— rule challenge` and wait for DK's response; do not relax the rule.

A separate testing prompt
(`PAPER_QUALITY_TESTING_PROMPT_FOR_CODEX_2026-04-25.md`) probes the
same failure modes from the outside after the build lands, with no
state shared with this build's processes. The two-document
arrangement means that even if a shortcut survives the build's
internal tests, the testing prompt's adversarial probes will catch
it before the layer reaches real papers.

The subscription-only access constraint (§1.5) and the
log-and-continue failure semantics (§5) work together: a build that
runs ballistically through subscription chat interfaces, recording
violations rather than halting, can process the 1 400-paper corpus
in the background over weeks without human intervention. Halt-and-
wait semantics paired with subscription rate limits would make the
retrofit functionally impossible. Together, the two design choices
are what make the layer operationally feasible at all.

---

*End of build prompt. Companion testing prompt:
`PAPER_QUALITY_TESTING_PROMPT_FOR_CODEX_2026-04-25.md`.*
