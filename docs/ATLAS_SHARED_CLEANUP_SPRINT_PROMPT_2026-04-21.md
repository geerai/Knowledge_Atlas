# Codex prompt — atlas_shared cleanup sprint

**Date**: 2026-04-21
**Authorising reviewer**: DK
**Target repo**: `/Users/davidusa/REPOS/atlas_shared` (github.com/dkirsh/atlas_shared)
**Baseline tip**: `5dee5ea` — "Add adaptive classifier subsystem and topic bank"
**Estimated effort**: 2 days spread across 4 passes, 12 commits

---

## Context — read before starting

This prompt authorises specific, scoped edits to atlas_shared that
are normally prohibited. The "do not alter atlas_shared" rule in
`docs/ATLAS_SHARED_HANDOFF_FOR_CODEX_2026-04-21.md` applies during
deployment sessions — it stops a deploy from sneaking in upstream
changes. **This is a different kind of session.** This is a cleanup
sprint DK has explicitly commissioned based on a review in
`docs/ATLAS_SHARED_SUGGESTIONS_2026-04-21.md`.

Two rules for this session:

1. **Do not run a deploy in the same session as this cleanup.** Finish
   the cleanup, push atlas_shared to origin/master, then return to
   DK for a separate deploy session that picks up the updated tip.
2. **Do not implement any suggestion not listed below.** If you see
   other improvements during the sprint, add them to the suggestions
   file under a new `## Codex review — <date>` heading. DK will
   triage them later.

Read before starting:

- `docs/ATLAS_SHARED_HANDOFF_FOR_CODEX_2026-04-21.md` (what the module is)
- `docs/ATLAS_SHARED_SUGGESTIONS_2026-04-21.md` (CW's twelve observations)
- `github.com/dkirsh/atlas_shared/AGENTS.md` (the repo's own contract)
- `github.com/dkirsh/atlas_shared/contracts/ATLAS_SHARED_SCOPE_CONTRACT_2026-04-07.md`

## Pre-flight

```bash
cd /Users/davidusa/REPOS/atlas_shared
git fetch origin
git checkout master && git pull --ff-only origin master
git checkout -b cleanup-sprint-2026-04-21
```

Establish the test baseline:

```bash
pytest -q 2>&1 | tail -5
```

Record the pass/fail/skip counts. Every commit below must not
regress these.

## Pass 1 — Behaviour-affecting fixes (2–3 hours)

Two commits. These are the highest-risk items and therefore the ones
DK wants validated first.

### Commit 1 of 12 — Fix `bundle_id` collision (suggestion S5)

`QuestionConstitution.bundle_id` at `src/atlas_shared/relevance.py:175-178`
derives from `_slug(stem)` where stem is topic-or-question_text-or-
question_id. Two constitutions that share a topic (e.g., one on
"lighting × attention" and one on "lighting × mood") produce
identical bundle IDs. The bundle system then silently merges their
routing. DK has confirmed this is a bug, not intentional merging.

**Change**: include `question_id` in the slug so each question gets
its own bundle:

```python
@property
def bundle_id(self) -> str:
    stem = self.topic or self.question_text or self.question_id
    return f"bundle-{_slug(stem)}-{_slug(self.question_id)}"
```

**Test**: in `tests/test_relevance.py`, add a test that two
constitutions with the same `topic` but different `question_id`
produce different `bundle_id` values. Add a second test confirming
the old single-question case still produces a stable bundle ID
derived from its topic — the collision fix must not change the
bundle ID of a uniquely-topiced question.

**Commit message**:
```
fix(relevance): disambiguate bundle_id when constitutions share a topic

QuestionConstitution.bundle_id previously collided for any two
constitutions sharing a topic (e.g., "lighting × attention" and
"lighting × mood"), silently merging their bundle routing.

Include question_id in the slug so each question gets a unique
bundle_id. Uniquely-topiced questions still get stable bundle IDs
derived from topic.

Suggestion S5 from docs/ATLAS_SHARED_SUGGESTIONS_2026-04-21.md
(Knowledge_Atlas repo).
```

### Commit 2 of 12 — Downgrade `CLEAR_FALSE_POSITIVE_TERMS` hard-reject (suggestion C2)

`intake.py` hard-rejects any paper whose title or abstract contains
one of ten biomedical-physics terms. "Enzyme" and "protein folding"
are on that list. A workplace-stress paper mentioning cortisol (an
enzyme) would be rejected before the classifier saw it.

**Change**: downgrade the keyword hit from a `reject_clear_false_positive`
decision to a `manual_review` decision. Preserve the hard-reject
only for a narrower core list (suggest: `"particle physics",
"quantum chromodynamics", "plasma turbulence", "semiconductor wafer",
"galactic"`). Move "enzyme", "protein folding", "gene expression",
"molecular dynamics", "astrophysics" to a new
`SOFT_FALSE_POSITIVE_TERMS` tuple whose hit triggers manual review.

**Test**: add to `tests/test_intake.py` three cases. (a) A paper
whose abstract mentions "particle physics" gets
`reject_clear_false_positive`. (b) A paper whose abstract mentions
"enzyme" in the context of cortisol + workplace stress gets
`manual_review`, not rejection. (c) A paper mentioning no
false-positive terms passes through normally.

**Commit message**:
```
fix(intake): downgrade keyword false-positive hits to manual_review

CLEAR_FALSE_POSITIVE_TERMS previously hard-rejected any paper
containing enzyme / protein folding / gene expression / molecular
dynamics / astrophysics, masking legitimate workplace-stress papers
that mention cortisol (an enzyme) as a biomarker.

Split into a narrower CLEAR list (particle physics, QCD, plasma,
semiconductor wafer, galactic) that still hard-rejects, and a new
SOFT list (enzyme, protein folding, gene expression, molecular
dynamics, astrophysics) that downgrades to manual_review.

Suggestion C2 from docs/ATLAS_SHARED_SUGGESTIONS_2026-04-21.md
(Knowledge_Atlas repo).
```

## Pass 2 — Data vs code migration (3–4 hours)

Two commits. Mechanical changes. Lift domain vocabulary out of
source into data files.

### Commit 3 of 12 — Move domain lexicon to data file (suggestion S3)

`intake.py` has `DOMAIN_SIGNAL_TERMS` (32 words) and
`CLEAR_FALSE_POSITIVE_TERMS` + `SOFT_FALSE_POSITIVE_TERMS` (from
commit 2) as module-level constants.

**Change**: create `src/atlas_shared/data/domain_lexicon.json`:

```json
{
  "domain_signal_terms": ["architecture", "architectural", ...],
  "clear_false_positive_terms": ["particle physics", ...],
  "soft_false_positive_terms": ["enzyme", "protein folding", ...]
}
```

Load at package import via the same `importlib.resources` pattern
`topic_bank.py` uses. Keep the module-level tuples as loader-populated
defaults so existing imports still work. Allow
`PreExtractionIntakeGate.__init__` to accept a `lexicon_override`
argument for future domain expansion; if None, load the default.

**Test**: add `tests/test_intake.py` case confirming that
overriding the lexicon changes the gate's accept/reject behaviour.

**Commit message**: `refactor(intake): move domain lexicon to data/domain_lexicon.json`

### Commit 4 of 12 — Move article-type defaults to data file (suggestion S4)

`QuestionConstitution.allowed_article_types`, `marginal_article_types`,
and `rejected_article_types` carry 8 / 3 / 4 domain-specific defaults
as dataclass field defaults.

**Change**: create `src/atlas_shared/data/article_type_defaults.json`
with the three tuples. Load at import. Have `QuestionConstitution`
use a classmethod or module-level `_DEFAULTS` lookup rather than
baking the tuples into the dataclass declaration.

**Test**: existing `tests/test_relevance.py` should still pass. Add
one case confirming that a `from_panel_spec` call with no explicit
article-type keys populates from the data file, not from a hardcoded
default.

**Commit message**: `refactor(relevance): move article-type defaults to data/article_type_defaults.json`

## Pass 3 — Structural clarity (3–4 hours)

Three commits.

### Commit 5 of 12 — Promote `paper_id` to top-level `RegistryFact` field (suggestion S1)

Add `paper_id: str | None = None` to `RegistryFact` in
`registry_sink.py`. Populate it in `intake.py` at every site that
currently writes `paper_id` into `details_json`. Keep the
`details_json` duplicate for this commit — deprecation happens in a
later, separate commit after consumers have migrated.

**Test**: add a case to `tests/test_intake.py` that emitted
`RegistryFact` tuples have `fact.paper_id` match
`fact.details_json["paper_id"]`.

**Commit message**: `refactor(registry_sink): promote paper_id to top-level RegistryFact field`

### Commit 6 of 12 — Add `SchemaVersion` Literal (suggestion S6)

Declare in `registry_sink.py`:

```python
SchemaVersion = Literal[
    "v1",
    "pre_extraction_intake_v1",
]
```

Annotate `RegistryFact.schema_version: SchemaVersion`. Run `mypy` on
the package to confirm no new errors; update any call site whose
schema-version string is not in the Literal.

**Test**: existing tests must still pass. No new test needed; mypy
clean is the bar.

**Commit message**: `chore(registry_sink): type-constrain RegistryFact.schema_version as Literal`

### Commit 7 of 12 — Document `paper_id` as canonical naming (suggestion S2)

This is a documentation-only commit unless DK has decided to rename.
Default action (pending DK's answer to "paper_id or article_id?"):
keep `paper_id` everywhere in atlas_shared, document the decision in
`contracts/ATLAS_SHARED_SCOPE_CONTRACT_2026-04-07.md`.

**Change**: add a section to the contract file:

```markdown
## Canonical identity field

The canonical article-identity field is `paper_id`. All atlas_shared
dataclasses, record methods, and registry facts use `paper_id`.
Consumer repos (Knowledge_Atlas, Article_Finder, Article_Eater) may
alias to `article_id` in their own APIs, but when crossing the
atlas_shared boundary the canonical name is `paper_id`.
```

**Test**: none — documentation only.

**Commit message**: `docs(contract): name paper_id as the canonical article-identity field`

## Pass 4 — Hygiene (2 hours)

Four commits. Low-risk, no behaviour change.

### Commit 8 of 12 — Consolidate `_split_terms` and `_assessment_weight` into `_util.py` (suggestion H1)

Create `src/atlas_shared/_util.py`. Move `_split_terms` (currently
duplicated in `intake.py`, `relevance.py`, `classifier_system.py`)
and `_assessment_weight` (currently in `classifier_system.py` and
`bundle_router.py`) into it. Update the three / two modules to
import from `_util.py`.

**Test**: all existing tests must still pass. Mechanical refactor.

**Commit message**: `chore(util): consolidate duplicate helpers into _util.py`

### Commit 9 of 12 — Trim `__all__` to ten canonical entries (suggestion H2)

In `src/atlas_shared/__init__.py`, reduce `__all__` from 40+ entries
to the ten public-contract entry points:

```python
__all__ = [
    "AdaptiveClassifierSubsystem",
    "ArticleCandidate",
    "BundleRoutingResult",
    "PreExtractionIntakeGate",
    "QuestionArticleRelevanceFilter",
    "QuestionBundleRouter",
    "QuestionConstitution",
    "RegistryFact",
    "RelevanceAssessment",
    "load_topic_constitution_bank",
]
```

Keep the internal imports so that downstream code importing (e.g.)
`atlas_shared.relevance.ArticleBundle` still works; the change is to
`__all__` only, not to the from-imports. Document the policy in
`AGENTS.md`: "The ten symbols in `__all__` are public-API. Anything
else is internal; consumers should import from submodules if they
need it and accept that those imports may break on refactor."

**Test**: existing tests must still pass.

**Commit message**: `chore(api): trim __all__ to ten canonical public-API entry points`

### Commit 10 of 12 — Add `__version__` (suggestion I1)

In `src/atlas_shared/__init__.py`, add `__version__ = "0.2.0"`
(reflecting: initial publish was 0.1, adaptive classifier was 0.2).
Keep in sync with `pyproject.toml`.

**Test**: add `tests/test_package.py::test_version_exposed` that
asserts `atlas_shared.__version__` is a non-empty string matching a
semver-ish pattern.

**Commit message**: `chore(package): expose __version__ = 0.2.0`

### Commit 11 of 12 — Start `CHANGELOG.md` (suggestion I2)

Create `CHANGELOG.md` at repo root. Backfill the two existing
commits (`8749349`, `5dee5ea`) plus all eleven cleanup-sprint
commits ending at this one. Use Keep-A-Changelog format:

```markdown
# Changelog

## [0.3.0] — 2026-04-21
### Added
- `RegistryFact.paper_id` top-level field (S1).
- `SchemaVersion` Literal type (S6).
- Module `_util.py` holding shared helpers (H1).
- `__version__` attribute on the package (I1).

### Changed
- `QuestionConstitution.bundle_id` now includes `question_id` in the
  slug (S5 bug fix).
- Soft-vs-clear false-positive term split in intake (C2).
- Domain lexicon moved to `data/domain_lexicon.json` (S3).
- Article-type defaults moved to `data/article_type_defaults.json` (S4).
- `__all__` trimmed to ten canonical entries (H2).

### Deprecated
- `RegistryFact.details_json["paper_id"]` duplicate of top-level
  field; will be removed in 0.4.

## [0.2.0] — 2026-04-xx
- Added adaptive classifier subsystem and topic bank.

## [0.1.0] — 2026-04-07
- Initial atlas_shared publish.
```

Bump `__version__` in the previous commit to `"0.3.0"` (amend if
easier than a follow-up).

**Test**: none.

**Commit message**: `docs(changelog): start CHANGELOG.md with backfilled history through 0.3.0`

### Commit 12 of 12 — Final sweep + PR / push

Run the full test suite one more time:

```bash
pytest -q 2>&1 | tail -5
mypy src/atlas_shared 2>&1 | tail -10
```

Baseline pass count must match or exceed Pre-flight. Zero new mypy
errors.

Push the branch:

```bash
git push -u origin cleanup-sprint-2026-04-21
```

Open a pull request against master with the title:

> atlas_shared cleanup sprint — 11 commits, S1/S2/S3/S4/S5/S6 + C2 + H1/H2 + I1/I2

And the body summarising the twelve commits in order. Reference
`docs/ATLAS_SHARED_SUGGESTIONS_2026-04-21.md` in the Knowledge_Atlas
repo as the originating review.

DK reviews the PR. On merge, the tip of master becomes the
atlas_shared version the next Knowledge_Atlas deploy should pin to.

## Reporting back

At the end of the sprint, append a block to Knowledge_Atlas
`COORDINATION.md` under "### Codex atlas_shared cleanup — 2026-04-21":

- Commits landed: list the 11 SHAs (commit 12 is the push, not a
  content commit).
- PR URL.
- Test baseline before: `<pass> / <fail> / <skip>`.
- Test baseline after: `<pass> / <fail> / <skip>`.
- Any suggestions written to
  `docs/ATLAS_SHARED_SUGGESTIONS_2026-04-21.md` as new Codex-review
  entries (list their headings, not their bodies).
- Anything that needed a DK decision and was deferred rather than
  implemented. For each: the suggestion ID and the decision needed.

Ping CW on COORDINATION.md when done.

## Failure modes

If any commit breaks the test baseline, stop immediately. Do not
proceed to the next commit. Post the failing test names to
COORDINATION.md and wait for DK to intervene. Do not patch around
the failure with a hack — the sprint's value depends on each commit
being a clean, revertable unit.

If the PR cannot be merged cleanly (because atlas_shared has diverged
on master since this branch was cut), rebase. Do not merge-commit the
cleanup sprint into a messy history.

If during the sprint a new observation arises that changes the shape
of a later commit (e.g., Pass 3's S1 commit would be cleaner if
something from Pass 4 landed first), stop and post the reorder
proposal to COORDINATION.md. Do not silently re-order.

## Out of scope for this sprint

- Implementing the unified paper-journey view in Knowledge_Atlas.
  That is a separate task specified in
  `docs/PAPER_JOURNEY_VIEW_TASK_SPEC_2026-04-21.md`.
- Renaming `paper_id` to `article_id` throughout the Atlas stack.
  That is a coordinated breaking change across three repos; Commit 7
  documents `paper_id` as canonical, which settles the question for
  atlas_shared but does not touch the consumers.
- Adding any new public API to atlas_shared. The sprint is purely
  subtractive or isomorphic — trim, migrate, document, version.
- Changing the `Protocol`-based registry sink architecture or the
  dataclass `frozen=True` invariant. Both are working well per CW's
  review and must stay.

---
