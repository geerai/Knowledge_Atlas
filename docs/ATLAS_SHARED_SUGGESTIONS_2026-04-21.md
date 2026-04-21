# atlas_shared — improvement suggestions

*Started 2026-04-21 · owner: DK*

This file collects observations about the `atlas_shared` package
(https://github.com/dkirsh/atlas_shared) from consumers of the module.
The rule is: read, do not edit. Any suggestion that lands here is a
note for DK to triage and act on upstream as a separate commit to the
atlas_shared repo itself. Every entry should state what was observed,
where, what change would help, and why.

Each reviewer writes under a section marked with their initials and a
date. Never edit another reviewer's section.

---

## CW review — 2026-04-21

Review scope: the eight `.py` files under `src/atlas_shared/`, the six
contract markdown files under `contracts/`, the `__init__.py` exports,
and a sampled reading of the six test files. The review prompted by a
pass over Track 2's graded deliverables T2.a through T2.f on the
Knowledge_Atlas hub, which now explicitly name atlas_shared symbols in
each acceptance criterion. The observations below are the places where
that naming exposed something worth discussing.

### Structural observations

#### S1. `RegistryFact` lacks a top-level `paper_id` field while `BundleRoutingResult` has one

`RegistryFact` carries `question_id`, `bundle_id`, `topic_label`, and
`edge_case_kind` at the top level, but the article identity lives
buried inside `details_json["paper_id"]`. `BundleRoutingResult` does
the opposite — `paper_id` is a top-level field. The two canonical
result dataclasses therefore disagree about whether article identity
is first-class.

Evidence: `registry_sink.py` lines 11–22; `bundle_router.py` line 44.

Downstream cost: every consumer that needs to correlate a
`RegistryFact` with a specific paper has to parse `details_json`,
which is typed as `Mapping[str, Any]`. A direct field access would be
cheaper and typed.

Proposed change: add `paper_id: str | None = None` to `RegistryFact`
and populate it in `intake.py` where the facts are built (the field
is already in `details_json`, so this is a lift, not a new write).
Keep the `details_json` copy for one release to preserve consumers
that already read from there; remove the duplicate in the following
release once consumers have migrated.

Severity: medium. Cleanliness, not correctness — consumers work today
by reaching into `details_json`.

#### S2. Naming: `paper_id` vs `article_id` across the Atlas system

`ArticleCandidate.paper_id`, `RegistryFact.details_json["paper_id"]`,
`BundleRoutingResult.paper_id`, and `PreExtractionArticleIntake.paper_id`
all use `paper_id`. The rest of the Atlas stack — Knowledge_Atlas HTML
spec pages, the Article_Eater registry tables, and most external
documentation — uses `article_id`. The two are the same thing; the
name just drifts.

Evidence: `relevance.py` line 183 (`paper_id: str`); Knowledge_Atlas
`160sp/ka_track2_hub.html` Region 3.5 uses "article ID" and "topic ID"
in student-facing copy.

Proposed change: pick one and stick to it. If `paper_id` is the
canonical choice (reasonable — it's already the field name in the
package) document that decision in `contracts/ATLAS_SHARED_SCOPE_CONTRACT_2026-04-07.md`
so downstream repos can align. If `article_id` is preferred, rename
throughout — but that's a breaking change.

Severity: medium. No bugs today, but new readers will consistently
confuse the two names.

#### S3. Domain vocabulary hardcoded in source (`DOMAIN_SIGNAL_TERMS`, `CLEAR_FALSE_POSITIVE_TERMS`)

`intake.py` defines a 32-word `DOMAIN_SIGNAL_TERMS` tuple and a
10-word `CLEAR_FALSE_POSITIVE_TERMS` tuple as module-level constants.
They encode the Atlas's current domain (architectural cognition) and
hard-reject list. Expanding the Atlas to a second domain, or
correcting a false-positive keyword, requires editing source.

Evidence: `intake.py` lines 55–95, 98–110.

Downstream cost: `CLEAR_FALSE_POSITIVE_TERMS` includes "protein
folding" and "enzyme" — any workplace-stress study that mentions
enzymes in passing (cortisol is an enzyme; urinary cortisol is a
common stress marker) would be hard-rejected before reaching the
classifier. The lexicon is brittle.

Proposed change: move both tuples into
`src/atlas_shared/data/domain_lexicon.json` (next to the existing
`question_constitutions_curated_30.json`). Load them at package
import time with the same `importlib.resources` pattern that
`topic_bank.py` already uses. Allow a downstream repo to pass an
override to `PreExtractionIntakeGate.__init__` for non-architectural
domains.

Severity: medium-high. The hard-reject list can mask legitimate
stress research today.

#### S4. `QuestionConstitution` article-type vocabularies hardcoded as default field values

`QuestionConstitution.allowed_article_types`, `marginal_article_types`,
and `rejected_article_types` carry 8 / 3 / 4 domain-specific defaults.
Any change to the Atlas's article-type vocabulary requires editing the
dataclass default tuples.

Evidence: `relevance.py` lines 129–151.

Proposed change: pull the default tuples into
`src/atlas_shared/data/article_type_defaults.json` and load them when
`QuestionConstitution.from_panel_spec` is called without explicit
overrides. Declares article-type policy as data rather than code.

Severity: medium. Same flavour as S3; less urgent because the classes
are already stable.

#### S5. `bundle_id` collision risk across constitutions sharing a topic

`QuestionConstitution.bundle_id` is a property:
`return f"bundle-{_slug(stem)}"` where `stem = self.topic or
self.question_text or self.question_id`. Two constitutions that share
a topic (legitimate: one question on "lighting × attention" and one
on "lighting × mood" both have topic "lighting") will produce
identical bundle IDs. The bundle system then silently merges
responses from distinct questions.

Evidence: `relevance.py` lines 175–178.

Proposed change: include `question_id` in the slug so bundle IDs are
unique per question, or — if the merging is intentional — document
that merge semantics explicitly in a comment on the property and in
`contracts/PANEL_TOPIC_EVIDENCE_CONTRACT_2026-04-17.md`.

Severity: high if merging is unintentional; low if it is the design.
Ask DK which.

#### S6. `schema_version` values proliferate without a registry

`RegistryFact.schema_version` defaults to `"v1"` in `registry_sink.py`,
but `intake.py` passes `schema_version="pre_extraction_intake_v1"` on
every fact it emits. Future dimensions will presumably pass their own
version strings. With no central registry of schema-version tokens,
migration tooling that looks for specific schemas may miss records
written under a slightly different string.

Evidence: `registry_sink.py` line 17; `intake.py` multiple sites
passing `"pre_extraction_intake_v1"`.

Proposed change: collect all schema-version tokens into a `Literal`
type in `registry_sink.py` (e.g., `SchemaVersion = Literal["v1",
"pre_extraction_intake_v1", ...]`) and reference the Literal wherever
a version is passed. That gives mypy the ability to catch drift.

Severity: low-medium. No bug today; maintenance hazard as dimensions
proliferate.

### Correctness observations

#### C1. `QuestionBundleRouter.route_article` silently collapses constitutions with no topic

When a `QuestionConstitution` has no `topic` field, `route_article`
falls back to `"untitled-topic"` and buckets all such constitutions
into one shared pseudo-topic. A paper accepted by two untopiced
constitutions ends up in a single bundle that cannot be
disambiguated.

Evidence: `bundle_router.py` line 91 (`... or "untitled-topic"`).

Proposed change: raise an explicit error when a constitution without
a topic is asked to route an article, or log a warning and skip.
Silently pooling is the worst of the three options.

Severity: medium. Panel workflow is meant to set `topic`, but a
partial panel ingestion could leave it empty.

#### C2. `CLEAR_FALSE_POSITIVE_TERMS` keyword-rejects before classifier runs

`PreExtractionIntakeGate` inspects the abstract / title for
`CLEAR_FALSE_POSITIVE_TERMS` substrings and returns a
`reject_clear_false_positive` decision without letting the classifier
see the paper. Any paper whose title or abstract mentions one of ten
biomedical-physics terms is cut off, regardless of whether the rest
of the content is on-domain.

Evidence: `intake.py`, keyword check in the `classify` method.

Proposed change: either narrow the false-positive list to terms that
are virtually never in architectural-cognition (even "enzyme" is
risky given stress-biomarker research), or downgrade the keyword hit
to a "low confidence, route to manual review" decision instead of a
hard reject. The latter preserves the novel-topic preservation rule
that the contract already asserts.

Severity: medium-high. This is the suggestion most likely to change
observed behaviour.

### Hygiene observations

#### H1. `_split_terms` duplicated across three modules

Identical or near-identical `_split_terms` helpers exist in
`intake.py`, `relevance.py`, and `classifier_system.py`. Same story
for `_assessment_weight` between `classifier_system.py` and
`bundle_router.py`.

Proposed change: pull shared helpers into
`src/atlas_shared/_util.py` (leading underscore to signal private).
Small cleanup; avoids drift where one module tightens the helper
and the other two don't.

Severity: low.

#### H2. `__init__.py` re-exports 40+ symbols in a flat `__all__`

Every symbol in `__all__` is a public-API commitment — renaming,
removing, or re-typing any of them is technically a breaking change.
Forty-plus symbols is a lot of simultaneous promises.

Proposed change: trim `__all__` to the ~10 most-used entry points
(`AdaptiveClassifierSubsystem`, `PreExtractionIntakeGate`,
`QuestionArticleRelevanceFilter`, `QuestionBundleRouter`,
`load_topic_constitution_bank`, `RegistryFact`, `ArticleCandidate`,
`QuestionConstitution`, `RelevanceAssessment`, `BundleRoutingResult`)
and document that the rest are internals consumers should import
from submodules. Gives the package room to refactor internals.

Severity: low. Worth doing before consumers ossify around rarely-used
exports.

### Infrastructure observations

#### I1. No `__version__` on the package

`src/atlas_shared/__init__.py` has no `__version__` attribute, so
downstream repos can't pin a specific atlas_shared build at runtime.
The `pyproject.toml` presumably carries one, but that's not visible
to code.

Proposed change: add `__version__ = "0.x.y"` to `__init__.py` and
bump on each release.

Severity: low.

#### I2. No `CHANGELOG.md`

Two commits (`8749349` initial, `5dee5ea` adaptive classifier
subsystem) with no changelog. At release cadence this is still OK;
once the atlas_shared repo starts versioning, downstream repos will
need a changelog to know what to upgrade for.

Proposed change: add `CHANGELOG.md` at repo root. Update on each
commit that adds or changes a public symbol.

Severity: low.

### Positives (so the review isn't all red ink)

`AGENTS.md` sets a very clear "read before reinventing" norm, with
specific canonical symbols listed. Every time I wrote a paragraph of
copy for Track 2 about relevance or classification I could go look
for the symbol and find it quickly. That is a nontrivial piece of
repo discipline and I wish every shared repo in the system had it.

`Protocol`-based registry sink (`SupportsClassificationRegistry`) is
the right abstraction for keeping atlas_shared free of repo-specific
database code. The separation survived the review cleanly.

`frozen=True` dataclasses throughout (`ArticleCandidate`,
`QuestionConstitution`, `RelevanceAssessment`, `RegistryFact`,
`BundleRoutingResult`, `TopicBundleCandidate`) is a good default —
makes concurrency reasoning much easier and prevents accidental
mutation of fact records after they're emitted.

Test coverage is reasonable (six test files totalling ≈ 823 lines for
≈ 2,500 lines of implementation — not dense but hits the main paths).
`test_intake.py`, `test_relevance.py`, and `test_classifier_system.py`
each exercise the key decision-making code.

`QuestionConstitution.from_panel_spec` accepts multiple legacy key
names (`environment_terms` or `iv_terms`, `outcome_terms` or
`dv_terms`, etc.). That pragmatism lets old panel JSON keep working
through a vocabulary migration. Good for the short term; the legacy
keys should be documented as deprecated and removed after a release.

### Triage summary

| ID | Severity | Effort | Notes |
|----|----------|--------|-------|
| S1 | medium | small | Add `paper_id` to `RegistryFact` |
| S2 | medium | medium | Settle `paper_id` vs `article_id` naming |
| S3 | medium-high | small | Move domain lexicon to data file |
| S4 | medium | small | Move article-type defaults to data file |
| S5 | high / low (tbd) | small | Disambiguate `bundle_id` or document merge |
| S6 | low-medium | small | Literal-type for schema-version tokens |
| C1 | medium | trivial | Raise / warn when topic missing |
| C2 | medium-high | small | Narrow `CLEAR_FALSE_POSITIVE_TERMS` or downgrade |
| H1 | low | trivial | Move helpers to `_util.py` |
| H2 | low | small | Trim `__all__` |
| I1 | low | trivial | Add `__version__` |
| I2 | low | ongoing | Start `CHANGELOG.md` |

None of these are blockers for today's deploy. S5 (bundle collision)
and C2 (keyword hard-reject) are the two most likely to actually
change observed behaviour if addressed. Everything else is hygiene.

---

## Codex section (empty — append here)

*Codex should add observations under a heading `## Codex review — <date>`
using the same format as the CW section above. Do not edit the CW
section.*

---
