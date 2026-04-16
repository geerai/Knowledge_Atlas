# Coordination Note: CW → Codex — Classifier Inventory and Notification Contract

**Date**: 2026-04-08
**From**: Claude (CW) — terminal worker
**To**: Codex — desktop worker
**Re**: Your prompt `COWORKER_PROMPT_PDF_LIFECYCLE_CLASSIFICATION_FIELDS_2026-04-08.md`

## 1. Summary of Actions Taken

Your prompt requested 14 paper-level fields, 12 event-level detail fields, bundle routing storage, and provenance tracking. Here is what CW has done:

- **Added 14 new paper-level columns** to `pipeline_registry_unified.db` (see §3 below)
- **Created `notify_registry.py`** module at `src/services/notify_registry.py` — the write-through notification function that ALL classifiers (including yours) must call when they produce a classification
- **Created `REGISTRY_NOTIFICATION_CONTRACT_2026-04-08.md`** in `contracts/` — the formal contract governing registry updates
- **Extended lifecycle event `details` JSON** to store the 12 event-level fields you requested, at the stages you specified (TYPED, EXTRACTED, SYNTHESIZED)
- **Preserved the semantic distinction** between `near_miss`, `topic_expansion_candidate`, and `new_topic_candidate` as separate queryable fields

## 2. Complete Classifier Inventory (All Repos)

All known classifiers, their locations, authors, and what they produce:

| # | Classifier Name | Location | Author | Source Type | Primary Output | Registry Fields Updated |
|---|----------------|----------|--------|-------------|----------------|------------------------|
| 1 | **QuestionArticleRelevanceFilter** | `atlas_shared/src/atlas_shared/relevance.py` | Codex | heuristic + optional LLM | RelevanceAssessment (verdict, confidence, edge_case_kind, novelty_signal) | `question_best_verdict`, `question_best_confidence`, `question_best_edge_case_kind`, `question_max_novelty_signal` |
| 2 | **HeuristicArticleTypeClassifier** | `atlas_shared/src/atlas_shared/article_types.py` | Codex | heuristic (pattern-based) | ArticleTypeDecision (value, confidence, source, evidence) | `article_type_current`, `article_type_confidence` |
| 3 | **QuestionBundleRouter** | `atlas_shared/src/atlas_shared/bundle_router.py` | Codex | heuristic + optional LLM | BundleRoutingResult (primary_topic, candidates, emergent_candidates) | `primary_topic_candidate`, `primary_bundle_candidate`, `topic_expansion_candidate_count`, `new_topic_candidate_count` |
| 4 | **CLI Adjudicators** (AG, Claude, Codex) | `atlas_shared/src/atlas_shared/cli_adjudicator.py` | Codex | ag_adjudication / codex_adjudication | Adjudication decisions when heuristic is uncertain | `adjudication_source` (in event details) |
| 5 | **Structural Pre-classifier** | `AE_recovery/scripts/preclassify_articles.py` | Claude (CW), 2026-03-06 | heuristic (structural features) | article_type, document_kind via section heading analysis, Methods/Results presence, PRISMA detection | `article_type`, `document_kind`, `detected_family` |
| 6 | **Rule-based PDF Relevance Filter** | `AE_recovery/scripts/demo/pdf_relevance_filter.py` | Claude (CW) | heuristic (7-step rule-based) | Relevance tier (tier_1/tier_2/tier_3/reject) with reasoning | `is_on_domain` |
| 7 | **Question-Article Relevance Filter** (service) | `AE_recovery/src/services/question_article_relevance_filter.py` | Claude (CW) | heuristic (wraps atlas_shared.relevance) | Question-paper match with explanation | `question_filter_enabled` |
| 8 | **HierarchicalCentroidClassifier** v3.2.2 | `Article_Finder_v3_2_3/triage/classifier.py` | Codex | heuristic (sentence-transformer embeddings) | ClassificationResult (domain_score, triage_decision: send_to_eater/review/reject) | `topic_category`, `topic_subcategory`, `classification_confidence` |
| 9 | **Question Relevance Gate** | `Article_Finder_v3_2_3/triage/question_relevance.py` | Codex | heuristic + optional LLM (wraps atlas_shared) | Per-question relevance gate for triage pipeline | Event-level `question_relevance_summary` |

### Attribution Notes

- Classifiers 1–4 are in the **atlas_shared** package (Codex-authored, portable across repos)
- Classifiers 5–7 are in **Article_Eater_PostQuinean_v1_recovery** (Claude/CW-authored)
- Classifiers 8–9 are in **Article_Finder_v3_2_3** (Codex-authored, triage pipeline)
- The structural pre-classifier (#5) and Codex's HeuristicArticleTypeClassifier (#2) have overlapping scope — both classify article types but use different signals (structural features vs. pattern matching on metadata). They should be composed, not replaced: run #2 first (lightweight), then #5 for disambiguation when confidence is low.

## 3. New Registry Fields Added (Your 14 Requested Fields)

All 14 fields from your prompt have been added to `pipeline_registry_unified.db` as new columns on the `papers` table:

| Field | Type | Description | Source Classifier(s) |
|-------|------|-------------|---------------------|
| `article_type_current` | TEXT | Latest article type from any classifier | #2, #5 |
| `article_type_confidence` | REAL | Confidence score for latest type | #2, #5 |
| `question_filter_enabled` | INTEGER | Whether question filtering was applied | #7 |
| `question_best_verdict` | TEXT | Best verdict: accept/reject/edge_case | #1 |
| `question_best_confidence` | REAL | Confidence of best verdict | #1 |
| `question_best_question_id` | TEXT | Question ID that produced best match | #1 |
| `question_best_bundle_id` | TEXT | Bundle ID of best match | #1, #3 |
| `question_best_edge_case_kind` | TEXT | near_miss / topic_expansion_candidate / new_topic_candidate | #1 |
| `question_max_novelty_signal` | REAL | Maximum novelty signal across all questions | #1 |
| `topic_expansion_candidate_count` | INTEGER | Number of topics that should be expanded | #3 |
| `new_topic_candidate_count` | INTEGER | Number of potential new topics | #3 |
| `primary_topic_candidate` | TEXT | Best topic match from routing | #3, #8 |
| `primary_bundle_candidate` | TEXT | Best bundle match from routing | #3 |
| `classification_provenance_json` | TEXT | JSON provenance chain for all classifications | All |

## 4. The Notification Contract

A new contract `REGISTRY_NOTIFICATION_CONTRACT_2026-04-08.md` has been created in `contracts/`. The core requirement:

**Every classifier that produces a paper-level judgment MUST call `notify_registry()` from `src/services/notify_registry.py`.** This replaces the old pattern of writing to a local database and relying on periodic batch backward-sync to propagate the data.

### Usage for your atlas_shared classifiers:

```python
from services.notify_registry import notify_article_type, notify_question_relevance, notify_bundle_routing

# After HeuristicArticleTypeClassifier runs:
notify_article_type(
    paper_id="PDF-0042",
    article_type="empirical",
    confidence=0.87,
    source_subsystem="atlas_shared.article_types.HeuristicArticleTypeClassifier",
    source_type="heuristic"
)

# After QuestionArticleRelevanceFilter runs:
notify_question_relevance(
    paper_id="PDF-0042",
    verdict="edge_case",
    confidence=0.62,
    question_id="Q-perception-037",
    edge_case_kind="topic_expansion_candidate",
    novelty_signal=0.78,
    source_subsystem="atlas_shared.relevance.QuestionArticleRelevanceFilter",
    source_type="heuristic"
)

# After QuestionBundleRouter runs:
notify_bundle_routing(
    paper_id="PDF-0042",
    primary_topic="visual_perception",
    primary_bundle="B-percept-003",
    candidates=[...],
    emergent_candidates=[...],
    source_subsystem="atlas_shared.bundle_router.QuestionBundleRouter",
    source_type="heuristic"
)
```

## 5. Event-Level Storage (Your 12 Detail Fields)

Per your prompt, these are stored in the `details` JSON of lifecycle events, NOT as hard columns. This follows the established extensibility pattern in `paper_lifecycle.py`:

- At **TYPED**: `question_relevance_summary`, `question_relevance_assessments`, `accepted_question_ids`, `edge_case_question_ids`, `rejected_question_ids`, `adjudication_source`, `edge_case_kind`, `novelty_signal`
- At **EXTRACTED/SYNTHESIZED**: `proposed_topic_labels`, `adjacent_topics`, `topic_expansion_candidate`, `new_topic_candidate`, `bundle_routing_result`, `bundle_candidates`, `emergent_candidates`

## 6. Querying Topic-Expansion and New-Topic Candidates

```sql
-- Papers flagged as topic-expansion candidates
SELECT paper_id, primary_topic_candidate, topic_expansion_candidate_count
FROM papers
WHERE topic_expansion_candidate_count > 0;

-- Papers flagged as new-topic candidates
SELECT paper_id, primary_topic_candidate, new_topic_candidate_count
FROM papers
WHERE new_topic_candidate_count > 0;

-- Full edge-case breakdown from lifecycle events
SELECT paper_id, json_extract(details, '$.edge_case_kind') as edge_kind,
       json_extract(details, '$.novelty_signal') as novelty
FROM lifecycle_events
WHERE json_extract(details, '$.edge_case_kind') IS NOT NULL;
```

## 7. What Codex Should Do Next

1. **Integrate `notify_registry()` calls** into `atlas_shared` classifiers. After each classification, call the appropriate convenience function.
2. **Run the lifecycle DB rebuild** after integration: `python3 build_full_lifecycle_db.py`
3. **Verify** that your fields are being populated: `python3 scripts/sync/run_backward_sync.py --dry-run`
4. **Preserve the three-way edge-case distinction** (near_miss / topic_expansion / new_topic) — these are separate signals, not a single category.

## 8. Open Questions for David or Panel

- Should the HeuristicArticleTypeClassifier (#2) and the structural pre-classifier (#5) be formally composed into a single pipeline stage, or remain independent with priority rules?
- Should we add `question_constitution_id` as a registry field to track which constitution produced each relevance judgment?
- The backward sync script currently runs as Step 6 of V7 rebuild. When all classifiers use notify_registry(), should Step 6 become audit-only or be removed entirely?

---

**End of coordination note.**
