# Registry Notification Contract for ATLAS Pipeline Event-Driven Sync

**Date**: 2026-04-08
**Version**: 1.0
**Status**: Active
**Extends**: Backward Sync Contract (2026-04-07); V7 Canonical Rebuild Operation Contract (2026-03-29)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-08 | Initial contract defining write-through notification pattern and 9-subsystem classifier inventory |

---

## Purpose

- Replace periodic batch backward-sync with event-driven write-through updates to pipeline registry
- Establish contract for `notify_registry()` as the primary mechanism for all paper-level state changes
- Provide unified provenance tracking (source subsystem, source type, broker identifier, timestamps)
- Codify all 9 registered classifiers that must use this contract
- Support new Codex-built classifier system (atlas_shared) with explicit lifecycle event tracking
- Preserve backward sync as reconciliation/audit tool, not primary sync mechanism
- Ensure no paper-level field update occurs without corresponding lifecycle event

---

## Operational Scope

### Pipeline Integration

Registry notifications are invoked in real-time as classifiers compute results:

```
Classifier Computes Result
        ↓
notify_registry(paper_id, fields, source_subsystem, ...)
        ├─ Update papers table (canonical state)
        ├─ Insert lifecycle_events row (audit trail)
        └─ Return notification_id
        ↓
Paper is immediately visible in unified registry
        ↓
Backward sync (Step 6) reads from registry, compares to source-of-truth DBs, detects drift
```

### Core Principle

**Write-through, not write-back**: Classifiers write to the registry directly, immediately. The registry becomes the source of truth for paper-level state. Backward sync verifies consistency, not generates it.

---

## Notification API

### Core Function Signature

```python
def notify_registry(
    paper_id: str,
    fields: dict[str, Any],
    source_subsystem: str,
    source_type: str,
    broker_string: str | None = None,
    event_stage: str | None = None,
    details_json: dict | None = None,
) -> dict:
    """
    Write-through notification to unified registry.

    Args:
        paper_id: Canonical paper identifier (e.g., "PDF-0001", "ARXIV-2024-12345")
        fields: Dict of {column_name: new_value} for papers table
        source_subsystem: Dotted path to classifier (e.g., "atlas_shared.relevance", "preclassify_articles")
        source_type: One of: "heuristic" | "llm" | "ag_adjudication" | "codex_adjudication" | "manual"
        broker_string: Model/service identifier if source_type in ["llm", "ag_adjudication", "codex_adjudication"]
                       (e.g., "gemini-2.5-pro", "claude-opus-4", "internal-heuristic-v3")
        event_stage: Lifecycle stage for this update (e.g., "TYPED", "EXTRACTED", "SYNTHESIZED", "CLASSIFIED")
        details_json: Optional dict of event-specific fields stored in lifecycle_events.details

    Returns:
        {
            "notification_id": str,
            "paper_id": str,
            "timestamp": str (ISO 8601 UTC),
            "fields_written": int,
            "lifecycle_event_id": str,
            "status": "success" | "partial" | "error"
        }

    Side Effects:
        - Updates papers table with provided fields + provenance columns
        - Inserts row into lifecycle_events table
        - If update fails on any field, rolls back entire transaction (atomicity)
    """
```

### Provenance Columns (Auto-populated)

Every notification write auto-populates these columns in the `papers` table:

| Column | Type | Source | Description |
|--------|------|--------|-------------|
| `computed_at` | TEXT (ISO 8601) | `datetime.utcnow()` | Timestamp of computation |
| `source_subsystem` | TEXT | Parameter | Dotted path to classifier |
| `source_type` | TEXT | Parameter | One of: heuristic/llm/ag_adjudication/codex_adjudication/manual |
| `broker_string` | TEXT | Parameter | Model/service (null if source_type = heuristic/manual) |

These four columns are **MANDATORY** and **NEVER NULL** after a notification-driven update.

---

## Registered Subsystems (Classifier Inventory)

All 9 known classifiers that must use this contract:

| # | Subsystem | Location | Author | Source Type | Output Fields (Updated via notify_registry) |
|---|-----------|----------|--------|-------------|---------------------------------------------|
| 1 | QuestionArticleRelevanceFilter | `atlas_shared/src/atlas_shared/relevance.py` | Codex | heuristic/llm | `question_best_verdict`, `question_best_confidence`, `question_best_edge_case_kind`, `question_max_novelty_signal` |
| 2 | HeuristicArticleTypeClassifier | `atlas_shared/src/atlas_shared/article_types.py` | Codex | heuristic | `article_type_current`, `article_type_confidence` |
| 3 | QuestionBundleRouter | `atlas_shared/src/atlas_shared/bundle_router.py` | Codex | heuristic/llm | `primary_topic_candidate`, `primary_bundle_candidate`, `topic_expansion_candidate_count`, `new_topic_candidate_count` |
| 4 | CLI Adjudicators (AG/Claude/Codex) | `atlas_shared/src/atlas_shared/cli_adjudicator.py` | Codex | ag_adjudication/codex_adjudication | `adjudication_source`, `edge_case_kind`, `adjudicated_verdict` |
| 5 | Structural Pre-classifier | `AE_recovery/scripts/preclassify_articles.py` | Claude (CW) | heuristic | `article_type`, `document_kind`, `detected_family` |
| 6 | Rule-based Relevance Filter | `AE_recovery/scripts/demo/pdf_relevance_filter.py` | Claude (CW) | heuristic | `is_on_domain` |
| 7 | Question-Article Relevance Filter | `AE_recovery/src/services/question_article_relevance_filter.py` | Claude (CW) | heuristic | `question_filter_enabled` |
| 8 | HierarchicalCentroidClassifier | `Article_Finder_v3_2_3/triage/classifier.py` | Codex | heuristic (embeddings) | `topic_category`, `topic_subcategory`, `classification_confidence` |
| 9 | Question Relevance Gate | `Article_Finder_v3_2_3/triage/question_relevance.py` | Codex | heuristic/llm | `question_relevance_summary` |

### Classifier Onboarding (MANDATORY)

Any new classifier must:
1. Add itself to the registered inventory with row number, location, author, source types, output fields
2. Implement call to `notify_registry()` at the point where paper-level results are computed
3. Pass `source_subsystem` as module dotted path (e.g., `atlas_shared.relevance`)
4. Ensure `source_type` is one of the five allowed values
5. For LLM-based classifiers: pass `broker_string` (model identifier)
6. Include event-level details in `details_json` (see Section 7)
7. Document in classifier's docstring: "This classifier is registered with REGISTRY_NOTIFICATION_CONTRACT_2026-04-08"

---

## New Paper-Level Fields (Codex Classifier System)

14 new columns to add to `papers` table in `pipeline_registry_unified.db`:

| Field | Type | Classifier Source | Description |
|-------|------|------------------|-------------|
| `article_type_current` | TEXT | HeuristicArticleTypeClassifier | Latest article type classification (e.g., "EMPIRICAL", "OPINION", "FRAMEWORK") |
| `article_type_confidence` | REAL | HeuristicArticleTypeClassifier | Confidence of latest article type (0.0–1.0) |
| `question_filter_enabled` | INTEGER (0/1) | Question-Article Relevance Filter | Whether question-article matching is active for this paper |
| `question_best_verdict` | TEXT | QuestionArticleRelevanceFilter | Accept/reject/edge_case |
| `question_best_confidence` | REAL | QuestionArticleRelevanceFilter | Confidence of verdict (0.0–1.0) |
| `question_best_question_id` | TEXT | QuestionArticleRelevanceFilter | question_id of best-matching question |
| `question_best_bundle_id` | TEXT | QuestionArticleRelevanceFilter | bundle_id associated with best match |
| `question_best_edge_case_kind` | TEXT | QuestionArticleRelevanceFilter | If verdict is edge_case: near_miss/topic_expansion_candidate/new_topic_candidate |
| `question_max_novelty_signal` | REAL | QuestionArticleRelevanceFilter | Maximum novelty score from question matching (0.0–1.0) |
| `topic_expansion_candidate_count` | INTEGER | QuestionBundleRouter | Number of questions suggesting topic boundary expansion |
| `new_topic_candidate_count` | INTEGER | QuestionBundleRouter | Number of questions suggesting entirely new topic |
| `primary_topic_candidate` | TEXT | QuestionBundleRouter | Most likely topic label from routing |
| `primary_bundle_candidate` | TEXT | QuestionBundleRouter | Most likely bundle_id from routing |
| `classification_provenance_json` | TEXT | (all) | JSON blob with full provenance chain: [{subsystem, source_type, broker_string, computed_at, confidence_scores}] |

### Design Rationale for 14 Fields

- **Article Type (2 fields)**: Current state of article classification; single source of truth
- **Question Filtering (1 field)**: Gate for downstream question-article operations
- **Question Relevance (6 fields)**: Verdict + confidence + matching question/bundle + edge case details + novelty signal
- **Topic Routing (3 fields)**: Candidate labels and bundle IDs from question-driven topic discovery
- **Provenance Chain (1 field)**: JSON array of all classifiers that have touched this paper

---

## Event-Level Detail Fields

When `notify_registry()` is called with `details_json`, the following fields may be populated for relevant lifecycle stages:

### At TYPED Stage
```json
{
  "article_type_hypothesis": "EMPIRICAL",
  "article_family_signals": ["has_methods", "has_results"],
  "classifier_version": "HeuristicArticleTypeClassifier-v2.1"
}
```

### At EXTRACTED Stage
```json
{
  "question_relevance_summary": "Highly relevant to Q-001",
  "question_relevance_assessments": [
    {
      "question_id": "Q-001",
      "verdict": "accept",
      "confidence": 0.87,
      "reasoning": "Directly addresses mechanism theory"
    }
  ],
  "accepted_question_ids": ["Q-001", "Q-005"],
  "rejected_question_ids": ["Q-002"],
  "edge_case_question_ids": ["Q-003"]
}
```

### At SYNTHESIZED Stage
```json
{
  "proposed_topic_labels": ["Epistemology", "Foundationalism"],
  "adjacent_topics": ["Internalism", "Externalism"],
  "topic_expansion_signals": ["Q-001 suggests boundary expansion"],
  "new_topic_signals": ["Q-004 describes novel mechanism not in existing topics"],
  "bundle_routing_result": "primary=EPISTEMOLOGY_BUNDLE_001, secondary=INTERNALISM_BUNDLE_002",
  "emergent_candidates": [
    {
      "candidate_name": "Phenomenal Concept Strategy",
      "signal_count": 3,
      "evidence": ["appears in Q-006", "appears in Q-008"]
    }
  ]
}
```

### At CLASSIFIED Stage
```json
{
  "adjudication_source": "codex_adjudication",
  "adjudicated_verdict": "accept",
  "edge_case_kind": "near_miss",
  "novelty_signal": 0.65,
  "panel_notes": "Question-article boundary is clear; topic is established"
}
```

---

## Semantic Distinctions (MANDATORY)

Preserve these as separate, queryable categories in `question_best_edge_case_kind`:

| Category | Definition | When to Use | Typical Next Step |
|----------|-----------|------------|-------------------|
| `near_miss` | Paper is relevant but falls outside current question scope by narrow margin | When paper score is just below acceptance threshold | Manual review for potential question boundary adjustment |
| `topic_expansion_candidate` | Paper suggests current topic boundaries should be widened | When paper introduces related concepts existing topic could incorporate | Consider widening acceptance criteria for this topic |
| `new_topic_candidate` | Paper describes mechanism/phenomenon not in any existing topic | When paper is highly novel; proposes new conceptual domain | Consider creating new topic; investigate related papers |

---

## Success Conditions

### SC-NOTIFY-1: Registration and Invocation Compliance

Every registered subsystem (§5) must call `notify_registry()` at the point where paper-level classifications are computed.

**Test Procedure**:
1. For each of the 9 registered classifiers:
   - Run classifier on sample 50 papers
   - Check application logs: did `notify_registry()` get called for every paper?
   - Verify call included required parameters: `paper_id`, `fields`, `source_subsystem`, `source_type`
2. Count classifiers with ≥95% invocation rate
3. **Pass criterion**: All 9 classifiers have ≥95% invocation rate (≥ 9/9)

**Failure Mode**:
- Classifier runs but does not call `notify_registry()` → SC-NOTIFY-1 FAIL
- Classifier calls `notify_registry()` but with NULL `paper_id` or missing fields → SC-NOTIFY-1 FAIL

**Repair Action**:
- Add logging to classifier: print(f"notify_registry called for {paper_id}")
- Re-run sample
- Verify all 9 are calling before proceeding

---

### SC-NOTIFY-2: No Orphaned Field Updates

No paper-level field update occurs without a corresponding lifecycle event in `lifecycle_events` table.

**Test Procedure**:
1. Run backward sync report (Step 6 of V7 pipeline)
2. For each paper with newly-updated field in `papers` table:
   - Query `lifecycle_events` for corresponding event (matching paper_id, timestamp within 1 second)
   - Verify event includes this paper in event_scope
3. Count papers with orphaned updates (update in papers, no matching event)
4. **Pass criterion**: ≤ 5 papers with orphaned updates (0.4% of 1,341)

**Failure Mode**:
- Paper field updated, but lifecycle_events table has no corresponding entry → SC-NOTIFY-2 FAIL

**Repair Action**:
- For each orphaned update:
  - Determine which classifier should have triggered it (from field name)
  - Check classifier logs: was this paper processed?
  - If yes: manually insert lifecycle event with retroactive timestamp
  - If no: restore field to previous value
- Recount orphaned updates

---

### SC-NOTIFY-3: Provenance Fields Never Null

For every notification-driven update, provenance fields (`computed_at`, `source_subsystem`, `source_type`, `broker_string`) must be non-null (except `broker_string` for heuristic/manual).

**Test Procedure**:
1. For every paper in `papers` table where any Codex classifier field is non-null:
   - Check: `computed_at` IS NOT NULL
   - Check: `source_subsystem` IS NOT NULL
   - Check: `source_type` IS NOT NULL
   - Check: If `source_type` in ["llm", "ag_adjudication", "codex_adjudication"] then `broker_string` IS NOT NULL
2. Count papers failing any check
3. **Pass criterion**: ≤ 2 papers with missing provenance (0.1%)

**Failure Mode**:
- Paper has `question_best_verdict = "accept"` but `computed_at` IS NULL → SC-NOTIFY-3 FAIL

**Repair Action**:
- For papers with missing provenance:
  - Query lifecycle_events for recent events involving this paper
  - Extract provenance from most recent event
  - Populate provenance fields in papers table
- Recount missing provenance

---

### SC-NOTIFY-4: Backward Sync Zero Drift

After all classifiers have run and notified registry, backward sync (Step 6) detects zero discrepancies between notification-driven state and source-of-truth databases.

**Test Procedure**:
1. Run full V7 pipeline including backward sync
2. Generate backward sync report (JSON)
3. In report, for each paper:
   - Check: Does papers table field match source-of-truth DB value?
   - Record any mismatches
4. Count papers with drift (>0 mismatches)
5. **Pass criterion**: ≤ 10 papers with drift (0.7%)

**Drift Sources**:
- Classifier updated registry but did not update source-of-truth DB
- Classifier updated source DB but did not call notify_registry()
- Concurrent update from two classifiers (race condition)

**Failure Mode**:
- >10 papers show drift between papers table and source DBs → SC-NOTIFY-4 FAIL

**Repair Action**:
- For each drifting paper:
  - Determine which classifier owns the field
  - Check if classifier was interrupted or failed
  - Re-run classifier for this paper
  - Verify notify_registry() call succeeded
- Recount drift

---

### SC-NOTIFY-5: Codex Fields Populated for Processed Papers

For all papers processed by Codex classifiers (atlas_shared), the 14 new Codex fields (§6) have non-NULL values.

**Test Procedure**:
1. Run QuestionArticleRelevanceFilter on all 1,341 papers
2. For each paper:
   - Check: `question_best_verdict` IS NOT NULL
   - Check: `question_best_confidence` IS NOT NULL
   - Check: `question_best_edge_case_kind` IS NOT NULL (if verdict = edge_case)
3. Count papers with NULL values
4. **Pass criterion**: ≤ 10 papers with NULL values (0.7%)

**Failure Mode**:
- >10 papers have `question_best_verdict` IS NULL after classifier run → SC-NOTIFY-5 FAIL

**Repair Action**:
- Identify papers with NULL verdicts
- Check classifier logs: was paper processed?
- If yes but verdict is NULL: classifier failed to compute verdict; re-run
- If no: classifier skipped paper; determine why (filtering rule? format issue?)
- Re-run classifier with logging
- Recount NULL fields

---

## Success Condition Summary

| SC | Condition | Threshold |
|----|-----------|-----------|
| SC-NOTIFY-1 | All 9 classifiers invoke notify_registry() | ≥95% per classifier, all 9 ≥9/9 |
| SC-NOTIFY-2 | No orphaned field updates (update without lifecycle event) | ≤5 papers |
| SC-NOTIFY-3 | Provenance fields never NULL | ≤2 papers |
| SC-NOTIFY-4 | Backward sync detects zero drift | ≤10 papers |
| SC-NOTIFY-5 | Codex fields populated for processed papers | ≤10 papers with NULL |

**Overall Pass**: All five SCs meet thresholds.

---

## Implementation Roadmap

### Phase 1: Infrastructure (Immediate)

1. Add 14 new columns to `papers` table in `pipeline_registry_unified.db`
2. Implement `notify_registry()` function in `src/services/registry_notification.py`:
   - Parse parameters
   - Validate paper_id exists in registry
   - Build provenance dict
   - Update papers table (atomic)
   - Insert lifecycle event
   - Return notification_id
3. Write unit tests for notify_registry() (5 tests, 100% path coverage)
4. Add logging: every notify_registry() call logs to file with timestamp, paper_id, fields, status

### Phase 2: Classifier Retrofit (Next Sprint)

For each of 9 registered classifiers (§5):
1. Add `from src.services.registry_notification import notify_registry`
2. At point of classification completion, construct fields dict
3. Call `notify_registry(paper_id=..., fields=fields, source_subsystem="...", source_type="...", ...)`
4. Log the notification_id returned
5. Add unit test: run classifier on 10 papers, verify notify_registry() called for each
6. Update classifier docstring with registry contract reference

Priority order (based on output frequency):
1. QuestionArticleRelevanceFilter (atlas_shared) — highest frequency
2. HeuristicArticleTypeClassifier (atlas_shared)
3. QuestionBundleRouter (atlas_shared)
4. CLI Adjudicators (atlas_shared)
5. Structural Pre-classifier (AE_recovery)
6. Rule-based Relevance Filter (AE_recovery)
7. Question-Article Relevance Filter (AE_recovery)
8. HierarchicalCentroidClassifier (Article_Finder_v3_2_3)
9. Question Relevance Gate (Article_Finder_v3_2_3)

### Phase 3: Backward Sync Transition (After Phase 2)

1. Backward sync script remains at Step 6, unchanged operationally
2. Add new validation: detect drift (SC-NOTIFY-4)
3. Add new report section: "Classifier Invocation Summary" (which classifiers called notify_registry, how many papers each processed)
4. Backward sync is now purely reconciliation/audit; not the primary sync mechanism

---

## Lifecycle Events Schema (pipeline_lifecycle_full.db)

When `notify_registry()` inserts a row into `lifecycle_events`:

```sql
INSERT INTO lifecycle_events (
    event_id,
    paper_id,
    event_type,        -- "notification" (from notify_registry)
    event_stage,       -- "TYPED" | "EXTRACTED" | "SYNTHESIZED" | "CLASSIFIED" (from parameter)
    source_subsystem,  -- from parameter
    source_type,       -- "heuristic" | "llm" | "ag_adjudication" | "codex_adjudication" | "manual"
    broker_string,     -- from parameter (NULL for heuristic/manual)
    computed_at,       -- from parameter
    details,           -- JSON blob from parameter
    created_at         -- datetime.utcnow()
) VALUES (...)
```

---

## Integration with Backward Sync Contract

- **Backward Sync Contract (2026-04-07)** defines six pathways to synchronize *existing* downstream DBs back to unified registry
- **Registry Notification Contract (this document)** defines forward-sync: classifiers write to registry immediately
- Both contracts are **complementary**, not contradictory:
  - Notification: write-through, real-time, per-classification event
  - Backward sync: reconciliation, batch, detects drift and repairs

**Operational timeline**:
1. Classifiers compute results
2. Classifiers call notify_registry() → papers table + lifecycle_events updated
3. (Other systems may independently update their own DBs: web_persistence_v5.db, ae.db, etc.)
4. Step 6 (backward sync) runs as audit: compares papers table to source DBs, detects drift, logs in report
5. If drift exists, report flags it; next-sprint fix applies

---

## Codex Classifier System Integration (atlas_shared)

The new Codex-built classifier system (atlas_shared) is the primary consumer of this contract.

### Expected Codex Workflow

```python
# In atlas_shared/src/atlas_shared/relevance.py
def classify_question_relevance(paper_id, paper_text, questions):
    # ... compute relevance ...

    verdict = "accept" if score > threshold else "reject"
    edge_case_kind = None
    if threshold - 0.1 < score < threshold:
        edge_case_kind = "near_miss"

    # WRITE-THROUGH: Call notify_registry immediately
    notify_registry(
        paper_id=paper_id,
        fields={
            "question_best_verdict": verdict,
            "question_best_confidence": score,
            "question_best_question_id": best_q_id,
            "question_best_edge_case_kind": edge_case_kind,
            "question_max_novelty_signal": max_novelty
        },
        source_subsystem="atlas_shared.relevance",
        source_type="llm" if self.use_llm else "heuristic",
        broker_string="gemini-2.5-pro" if self.use_llm else None,
        event_stage="EXTRACTED",
        details_json={
            "question_relevance_summary": summary,
            "question_relevance_assessments": assessments,
            "accepted_question_ids": accepted_ids
        }
    )

    return {
        "verdict": verdict,
        "confidence": score,
        "notification_id": notif_id  # returned from notify_registry
    }
```

---

## Known Limitations and Future Work

1. **Race Conditions**: If two classifiers call `notify_registry()` for the same paper simultaneously, SQLite locking may cause conflicts. Mitigation: use `BEGIN EXCLUSIVE` transaction in notify_registry(). Future: migrate to PostgreSQL for concurrent writes.

2. **Classifier Discrepancy**: If two registered classifiers assign conflicting verdicts (e.g., QuestionArticleRelevanceFilter says "accept", HierarchicalCentroidClassifier says "reject" for same paper), registry will reflect the most recent call. Mitigation: classify one topic at a time; ensure no overlapping classifier scope. Future: implement classifier consensus protocol.

3. **Broker String Standardization**: Broker strings are informal (model names). Future: create mapping table `classifier_brokers` with canonical names, version, API endpoint.

4. **Details JSON Versioning**: Event-level details schema may evolve. Future: add `details_schema_version` field to lifecycle_events.

---

## Testing Strategy

### Unit Tests (notify_registry function)

- `test_notify_registry_basic.py` — Minimal call with required parameters
- `test_notify_registry_provenance.py` — Verify provenance fields auto-populated
- `test_notify_registry_atomicity.py` — Rollback on partial field failure
- `test_notify_registry_lifecycle_insert.py` — Verify lifecycle_events row created
- `test_notify_registry_null_validation.py` — Reject NULL paper_id, source_subsystem, source_type

### Integration Tests (Classifier Retrofit)

For each of 9 classifiers:
- `test_classifier_X_calls_notify_registry.py` — Run classifier on 20 papers, verify notify_registry() called
- `test_classifier_X_field_mapping.py` — Verify fields dict matches classifier output
- `test_classifier_X_provenance_chain.py` — Verify classification_provenance_json accumulates correctly

### End-to-End Tests (Full Pipeline)

- `test_notify_registry_full_v7_pipeline.py` — Run full V7 rebuild including backward sync
- `test_notify_registry_sc_all.py` — Verify all five SCs pass
- `test_notify_registry_drift_detection.py` — Trigger drift, verify backward sync detects it
- `test_notify_registry_concurrent_classifiers.py` — Run 3 classifiers in parallel, verify no lost updates

---

## Master-Doc Relevance

- **Part V**: Registry notification as primary sync mechanism; lifecycle event sourcing
- **Part VI**: Event-driven architecture; provenance chain for audit and reproduction
- **Appendix C**: SC definitions and test procedures (formal success criteria)
- **Appendix D**: Integration with backward sync (complementary contracts)

---

## Sign-Off

This contract is effective immediately upon merge to `contracts/` directory in the Article_Eater_PostQuinean_v1_recovery repository.

**Approved by**: Professor David Kirsh, UCSD Cognitive Science
**Date**: 2026-04-08
**Status**: Active

---

*End of Contract*
