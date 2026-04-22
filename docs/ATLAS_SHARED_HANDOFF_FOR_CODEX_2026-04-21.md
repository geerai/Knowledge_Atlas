# atlas_shared — handoff report for Codex

**Date**: 2026-04-21
**Audience**: Codex (terminal / xrlab deploy)
**Purpose**: Give Codex the full picture of the `atlas_shared` module
— what it is, where it lives, how Knowledge_Atlas now names it, and
what Codex must and must not do with it.

---

## 1. What the module is

`atlas_shared` is the canonical classification, relevance, topic-ID,
and article-ID layer for every Atlas repo. It is a small shared
Python package that owns, in one place, the decisions that Article
Finder, Article Eater, and Knowledge Atlas used to make three
slightly different ways. Specifically it owns:

- article-type classification (empirical / review / meta-analysis /
  theory / method / etc.)
- pre-extraction intake gating (accept / edge-case / manual-review /
  reject-clear-false-positive)
- question-article relevance assessment (for each pair, does this
  paper belong to this question?)
- topic-constitution loading and topic-ID assignment from the
  panel-derived bank
- question-to-bundle routing (given one accepted article, which
  topic bundles should it land in?)
- registry-fact emission (the dataclass the three repos write into
  their own sinks)

## 2. Where it lives

- **GitHub repo**: https://github.com/dkirsh/atlas_shared
- **Local path on DK's Mac**: `/Users/davidusa/REPOS/atlas_shared`
- **Local path in the sandbox (if relevant)**:
  `/sessions/brave-great-tesla/mnt/REPOS/atlas_shared`
- **Current tip**: `5dee5ea` — "Add adaptive classifier subsystem and
  topic bank" (one commit beyond the initial publish `8749349`)
- **Package root**: `src/atlas_shared/`
- **Canonical contract docs**: `contracts/` (six markdown files)
- **Test suite**: `tests/` (six test files, ~823 lines)

## 3. The five canonical entry points

Per atlas_shared's own `AGENTS.md` ("Do Not Reinvent"), these are the
symbols every downstream repo must call. Do not rewrite any of them.

| Symbol | Lives in | What it does |
|--------|----------|--------------|
| `atlas_shared.intake.PreExtractionIntakeGate` | `intake.py` | Conservative pre-extraction intake gate. Preserves adjacent and novel-topic papers. Emits a `PreExtractionIntakeResult` plus the `RegistryFact` tuples that go to the registry sink. |
| `atlas_shared.topic_bank.load_topic_constitution_bank` | `topic_bank.py` | Loads the panel-derived topic constitutions (canonical topic IDs) from the JSON data file. |
| `atlas_shared.relevance.QuestionArticleRelevanceFilter` | `relevance.py` | Per-candidate relevance check against a given `QuestionConstitution`. Emits a `RelevanceAssessment` with verdict {accept / edge_case / reject}. |
| `atlas_shared.classifier_system.AdaptiveClassifierSubsystem` | `classifier_system.py` | The article-type classifier of record. Callable in-process or via `ka_article_endpoints.classify_single_paper`. |
| `atlas_shared.bundle_router.QuestionBundleRouter` | `bundle_router.py` | Given one accepted article and a list of `QuestionConstitution` objects, routes the article to the topic bundles it belongs to. Emits a `BundleRoutingResult` with `paper_id` + ranked `candidates`. |

Two governing contracts (do not edit, but read before touching any
downstream code that calls the above):

- `contracts/PRE_EXTRACTION_INTAKE_CONTRACT_2026-04-17.md`
- `contracts/PANEL_TOPIC_EVIDENCE_CONTRACT_2026-04-17.md`

## 4. How Knowledge_Atlas calls it

`atlas_shared` is imported at runtime inside the Knowledge_Atlas
backend. Codex's own recent commit `15d6569` — "Restore A0 endpoints
without atlas_shared checkout" — patched a case where the A0
endpoints needed to function when atlas_shared was not present on the
staging server. That hotfix implies atlas_shared is a real runtime
dependency when available, and the backend gracefully degrades when
it is not. Do not change that behaviour.

The path into atlas_shared from Knowledge_Atlas is
`ka_article_endpoints.classify_single_paper`, which wraps
`AdaptiveClassifierSubsystem` per DK's memory file entry.

## 5. What changed in Knowledge_Atlas today

Three commits (most recent first):

- `1287369` — Seed atlas_shared suggestions file with CW review.
  Created `docs/ATLAS_SHARED_SUGGESTIONS_2026-04-21.md` (this file's
  sibling). Twelve observations by CW, no code changes.
- `ada7a8c` — Name atlas_shared as canonical classification and ID
  layer; link admin. Added a shared-contract callout at the top of
  `160sp/ka_track2_hub.html` Region 3.5 that names the five canonical
  entry points by fully qualified symbol path. Added per-card module
  references to T2.a / T2.b / T2.c / T2.d / T2.e / T2.f acceptance
  criteria. Linked the instructor admin console at
  `/160sp/ka_admin.html` from T2.b (ambiguous-queue review) and T2.d
  (approval queue). Updated two AF journey page file entries to name
  `atlas_shared.bundle_router.QuestionBundleRouter` and
  `atlas_shared.classifier_system.AdaptiveClassifierSubsystem`
  directly.
- `d684010` — Set Track 2 point allocations: 10/10/10/13/13/13/6 = 75.
  Not atlas_shared-related but sequential in the deploy.

The practical effect: Track 2 student documentation no longer says
"run the classifier" abstractly. It names the symbol, points at the
GitHub repo, and says "import, do not reinvent."

## 6. The do-not-alter rule

Codex: you must not alter atlas_shared during this or any future
deploy. Specifically:

- **No pull requests** against `dkirsh/atlas_shared` from this deploy
  context.
- **No local edits** to `/Users/davidusa/REPOS/atlas_shared/` or
  `/sessions/brave-great-tesla/mnt/REPOS/atlas_shared/`.
- **No vendored copies** with local modifications inside
  Knowledge_Atlas.
- **No monkey-patching** of atlas_shared symbols from
  Knowledge_Atlas backend code. If a behaviour needs to change, it
  changes in atlas_shared by DK, not in the consumer.

Read, import, call. That's the contract.

## 7. What to do if you see an improvement

Write it to `docs/ATLAS_SHARED_SUGGESTIONS_2026-04-21.md` in the
Knowledge_Atlas repo. Use the existing format — one `## Codex review
— <date>` heading, then sub-headings per suggestion with what you
observed, where (file + line), what change would help, and why.

Do not edit CW's section. Do not implement any of the suggestions.
DK triages the combined file and decides what goes upstream as a
separate commit to the atlas_shared repo itself.

CW has already written twelve suggestions in that file, covering:

- **Structural** (S1–S6): `RegistryFact.paper_id` promotion, `paper_id`
  vs `article_id` naming, domain lexicon data-vs-code, article-type
  defaults as data, `bundle_id` collision risk, schema-version
  Literal type.
- **Correctness** (C1–C2): `QuestionBundleRouter` silently pooling
  untopiced constitutions; `CLEAR_FALSE_POSITIVE_TERMS` hard-reject
  potentially masking cortisol-marker stress research.
- **Hygiene** (H1–H2): `_split_terms` duplicated across three
  modules; `__all__` exports 40+ symbols (large public commitment).
- **Infrastructure** (I1–I2): no `__version__` on the package; no
  `CHANGELOG.md`.

Do not duplicate those observations. If you notice something
different, write a new heading for it.

## 8. Deploy-time checks that touch atlas_shared

During the deploy cycle, do these five things that involve
atlas_shared:

1. **Import check on the staging Python env**:

   ```bash
   python3 -c "from atlas_shared import AdaptiveClassifierSubsystem, \
     PreExtractionIntakeGate, QuestionArticleRelevanceFilter, \
     QuestionBundleRouter, load_topic_constitution_bank; \
     print('atlas_shared imports OK')"
   ```

   If that errors, the staging environment is missing atlas_shared
   and the A0-endpoints graceful-degrade path (from your 15d6569
   commit) is the only reason the site works. Worth flagging in
   COORDINATION.md.

2. **Version probe** (once an atlas_shared `__version__` exists —
   currently does not; see I1 in the suggestions file):

   ```bash
   python3 -c "import atlas_shared; print(atlas_shared.__version__)"
   ```

   For now, `git -C /Users/davidusa/REPOS/atlas_shared log --oneline -1`
   is the closest available version probe.

3. **Track 2 hub copy check** — confirm the canonical-module callout
   landed on the deployed site:

   ```bash
   curl -s https://<prod host>/ka/160sp/ka_track2_hub.html | \
     grep -c 'github.com/dkirsh/atlas_shared'
   ```

   Expect: ≥ 1.

4. **Canonical symbol presence in deployed HTML**:

   ```bash
   curl -s https://<prod host>/ka/160sp/ka_track2_hub.html | \
     grep -cE 'PreExtractionIntakeGate|AdaptiveClassifierSubsystem|QuestionArticleRelevanceFilter|QuestionBundleRouter|load_topic_constitution_bank'
   ```

   Expect: ≥ 6 (all five canonical entry points named at least once,
   some more).

5. **Admin-page links** — confirm the new `ka_admin.html` links in
   T2.b and T2.d render on the deployed hub:

   ```bash
   curl -s https://<prod host>/ka/160sp/ka_track2_hub.html | \
     grep -cE 'href="ka_admin\.html"'
   ```

   Expect: ≥ 2.

Report the numbers in your deployment status block in
COORDINATION.md.

## 9. Known open questions

Three things the review surfaced that DK has not yet decided:

- Whether `bundle_id` collisions across constitutions sharing a topic
  are intentional merging or a bug (S5 in the suggestions file).
  Deploy should not depend on the answer; it's an upstream question.
- Whether the `CLEAR_FALSE_POSITIVE_TERMS` list should be narrowed or
  downgraded from hard-reject to manual-review (C2).
- Whether `paper_id` or `article_id` is the canonical name across
  the Atlas stack (S2).

Codex does not need to resolve any of these. If you notice them
coming up during deploy, note in COORDINATION.md and move on.

## 10. One-line summary

`atlas_shared` is DK's canonical classification and ID layer at
https://github.com/dkirsh/atlas_shared; Knowledge_Atlas now names it
explicitly in Track 2's graded deliverables; you import from it and
report suggestions to `docs/ATLAS_SHARED_SUGGESTIONS_2026-04-21.md`
but never edit it.

---
