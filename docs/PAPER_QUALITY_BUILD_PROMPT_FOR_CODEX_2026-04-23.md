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
design document. A migration script
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
   template, send it to their respective endpoint, parse the
   response, and write the result to `fingerprint_staging`
   independently. No "skip the second model when the first is
   confident" optimisation. No re-using the first model's parsed
   output as context for the second. No batching that lets two
   papers' contexts mingle in either adapter. The adjudication
   step's input must be two structurally-independent fingerprint
   records keyed by `(paper_id, model_pair_id)`. A test asserts
   that across 50 papers, every paper produced at least one Claude
   call and one OpenAI call, with non-overlapping prompt hashes per
   field. Faking multi-LLM agreement by running one model twice
   (whatever the temperature) is a regression and the build fails.
   The whole calibration strategy depends on this rule; cutting it
   invalidates everything downstream.

9. **Confidence is reported with a distributional summary, not a
   single point estimate.** Every per-field confidence in
   `fingerprint_staging` records (a) the point estimate, (b) the
   per-token logprob mean for the field assertion's tokens, (c)
   self-consistency across three samples at temperature 0.3, and (d)
   a list of any field-assertion tokens whose logprob falls below
   the per-field minimum. Adjudication-queue routing reads (c) — a
   field that drifts across self-consistency samples is queued
   even if the point confidence is above the 0.85 threshold. A
   reporting test runs the calibration set and asserts that no
   field's confidence distribution has its mass spiked at exactly
   the 0.85 threshold or any single threshold-adjacent value
   (0.86–0.89): that pattern indicates threshold-gaming and the
   build fails.

## 5. Failure handling

If any step errors in a way that is not a simple code fix, stop.
Post the failing command, the full error output, and a one-sentence
hypothesis about the cause to `COORDINATION.md` under `### CW
paper-quality build — blocker`. Do not guess past the error.

If the calibration-report precision on any field falls below 70 %
after Commit 6, stop. That is the panel's stop-condition: the
extractor is not trustworthy for that field and DK needs to decide
whether to exclude the field or tune the prompt.

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
  three-sample temperature-0.3 runs: mean Jaccard similarity for
  list-valued fields, mean absolute difference for numeric fields.
  Variance close to zero on a field where the calibration set shows
  legitimate paper-to-paper variation indicates a deterministic
  shortcut and is a flag.
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

---

*End of build prompt. Companion testing prompt:
`PAPER_QUALITY_TESTING_PROMPT_FOR_CODEX_2026-04-25.md`.*
