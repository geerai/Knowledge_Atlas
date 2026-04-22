# Task Spec — Unified paper-journey read-only view

**Date**: 2026-04-21
**Requested by**: DK
**Target executor**: any AI worker under DK's control (Codex or AG recommended; Codex if terminal + tests are in scope, AG if analysis-only first pass)
**Effort estimate**: 4–6 hours for a first cut, another 2–3 for tests + HTTP endpoint
**Priority**: P2 — useful infrastructure; not blocking any student deliverable

---

## 1. Why this task exists

The Atlas currently tracks a paper's journey through two different
databases owned by two different repos:

- **Article_Finder_v3_2_3/data/article_finder.db** — the `papers` table
  holds 16,257 rows of candidates that Article Finder has proposed
  (harvested from reference lists, DOI-resolved, topic-typed,
  triage-scored). Fields include `paper_id`, `status`, `triage_score`,
  `triage_decision`, `triage_reasons`, `ae_job_path`, `ae_run_id`,
  `ae_output_path`, `ae_status`.
- **Article_Eater_PostQuinean_v1_recovery/data/pipeline_lifecycle_full.db** —
  the `lifecycle_events` table (14,265 rows) + `papers` (949 rows) +
  `stage_summary` (26,572 rows) + `paper_artifact_provenance` (6,840 rows)
  together track every paper through 28 canonical stages from
  `acquisition` (stage 1) through `site_display` (stage 28). V7
  extraction itself is stage 7.

The two databases join on `paper_id`. No existing code unifies them.
A user (student, instructor, researcher, admin) who wants to see the
full journey of one paper — from first proposal as a candidate all
the way through to site display — has to run two separate queries
and manually stitch the result.

This task builds the unifying view. Read-only: the view never writes
to either database.

## 2. Exact scope

Build a small Python module at `Knowledge_Atlas/scripts/paper_journey_view.py`
with the following public surface:

```python
@dataclass(frozen=True)
class CandidateStageInfo:
    """Pre-acquisition existence inside Article Finder."""
    paper_id: str
    doi: str | None
    title: str
    triage_decision: str | None     # accept / reject / edge_case / unset
    triage_score: float | None
    triage_reasons: tuple[str, ...]
    discovered_from: tuple[str, ...] # upstream paper IDs that cite this
    finder_run_id: str | None
    retrieved_at: str | None
    status: str | None               # proposed / retrieved / acquired / rejected
    af_pdf_path: str | None
    af_pdf_sha256: str | None


@dataclass(frozen=True)
class LifecycleStageRecord:
    """One stage transition from pipeline_lifecycle_full.db.lifecycle_events."""
    stage_name: str
    status: str                      # complete / in_progress / failed / blocked
    entered_at: str | None
    completed_at: str | None
    agent: str | None
    evidence: Mapping[str, Any]      # parsed from evidence JSON
    metrics: Mapping[str, Any]       # parsed from metrics_json
    notes: str | None


@dataclass(frozen=True)
class PaperJourney:
    """Unified candidate-through-site-display view of one paper."""
    paper_id: str
    candidate: CandidateStageInfo | None    # None if not found in AF DB
    lifecycle_events: tuple[LifecycleStageRecord, ...]   # ordered by stage
    current_stage: str | None               # from pipeline_lifecycle papers.current_stage
    current_status: str | None
    is_blocked: bool
    blocked_reason: str | None
    artifact_count: int                     # from paper_artifact_provenance


def get_paper_journey(paper_id: str, *, config: JourneyConfig | None = None) -> PaperJourney:
    """Return the unified journey for one paper. Raises KeyError if paper_id
    is in neither database."""


def iter_paper_journeys(
    *,
    config: JourneyConfig | None = None,
    limit: int | None = None,
    only_current_stage: str | None = None,
    only_blocked: bool = False,
) -> Iterator[PaperJourney]:
    """Stream journeys with optional filters."""


@dataclass(frozen=True)
class JourneyConfig:
    """Where the two databases live. Defaults pull from environment
    variables KA_AF_DB_PATH and KA_AE_LIFECYCLE_DB_PATH, falling back
    to repo-relative locations."""
    af_db_path: Path
    ae_lifecycle_db_path: Path
```

## 3. What the module must not do

1. No INSERT, UPDATE, or DELETE against either database. Open both
   SQLite connections with `isolation_level=None` + a read-only URI
   (`file:<path>?mode=ro`) so attempting to write raises.
2. No modification of either database's schema.
3. No caching layer that writes to a third database. An in-process
   LRU cache on `get_paper_journey` is fine; a filesystem or DB
   cache is out of scope.
4. No modification of `atlas_shared`. This module consumes the two
   repo-specific databases directly; it does not reach up into the
   shared contract layer.
5. No network fetches. If the abstract or PDF path is missing in the
   local databases, the journey reports the gap rather than hitting
   a remote source.

## 4. Where the module lives and why

Three candidate locations were considered:

- **atlas_shared** — rejected. atlas_shared is domain-neutral and
  database-path-neutral per its own `ATLAS_SHARED_SCOPE_CONTRACT`.
  Concrete SQLite paths do not belong there.
- **Article_Eater** — rejected. AE has the richer half of the data,
  but the view is also consumed by Knowledge_Atlas (site display,
  admin console) and putting the unifier inside AE would force KA
  to import from AE.
- **Knowledge_Atlas/scripts/paper_journey_view.py** — accepted. KA
  is where the frontend rendering of the view will eventually live,
  and keeping the module in the same repo as its primary consumer
  is the simplest arrangement. Secondary consumers (AE's own admin
  tooling) can import it via a file path or via a future shared
  package.

Config defaults find the two databases by walking up the parent
directories until both repos are found. Fall back to environment
variables `KA_AF_DB_PATH` and `KA_AE_LIFECYCLE_DB_PATH` if the walk
fails.

## 5. Acceptance criteria

1. **Happy path**: given a `paper_id` present in both databases (e.g.,
   `PDF-0001`), `get_paper_journey(paper_id)` returns a `PaperJourney`
   with non-None `candidate`, a non-empty `lifecycle_events` tuple
   ordered by canonical stage (per `stage_definitions.stage_order`
   in pipeline_lifecycle_full.db), and a resolved `current_stage`.

2. **Candidate-only path**: given a `paper_id` that appears in
   Article Finder's `papers` table but never made it to
   `pipeline_lifecycle_full.db.papers`, the journey has a non-None
   `candidate`, empty `lifecycle_events`, and `current_stage = None`.
   This is legitimate: the paper is proposed but not yet acquired.

3. **Lifecycle-only path**: given a `paper_id` that exists in
   `pipeline_lifecycle_full.db` but has no row in Article Finder's
   `papers` (legacy V6 ingestion, manual upload, or direct-to-AE
   submissions), the journey has `candidate = None` and a populated
   `lifecycle_events`. No error.

4. **Not found**: given a `paper_id` in neither database,
   `get_paper_journey` raises `KeyError(paper_id)`.

5. **Duplicate handling**: if Article Finder's `papers` has more than
   one row for the same `paper_id` (multiple retrieval attempts under
   the same canonical ID), the view returns the row with the latest
   `retrieved_at`. Document this disambiguation rule in the module
   docstring.

6. **Ordering**: `lifecycle_events` is returned in canonical stage
   order (1 through 28), with within-stage events ordered by
   `entered_at`. A paper that has been through stages 1, 2, 3, 5
   (skipped 4) reports an ordered tuple of four events; the gap is
   visible in `current_stage` which reads as `"indexing"` (stage 5)
   rather than as an inferred "next stage would be 4."

7. **Streaming**: `iter_paper_journeys()` yields in `paper_id`
   order, defaults to no limit, supports `only_current_stage` and
   `only_blocked` filters, and does not load all rows into memory
   before yielding the first one. Use SQL cursors, not `fetchall()`.

8. **Read-only enforcement**: attempting to write to either database
   through this module's exposed connections must raise
   `sqlite3.OperationalError: attempt to write a readonly database`.

## 6. Test requirements

Add `Knowledge_Atlas/tests/test_paper_journey_view.py` with at least
eight tests covering the acceptance criteria above, plus:

- Test that `get_paper_journey` does not mutate either database
  (assert `PRAGMA data_version` is unchanged before and after).
- Test that `iter_paper_journeys(limit=5)` yields exactly five and
  streams (does not call `fetchall()` internally — verify via a
  cursor mock or by reading the source of the implementation).
- Test that malformed `evidence` JSON in `lifecycle_events` is
  handled gracefully: the record still appears in the tuple, with
  `evidence = {}` and a `notes` entry flagging the parse failure.

Use `pytest`. Test fixtures can use in-memory SQLite databases with
minimal schemas mirroring the two real schemas — no need for the full
28-stage content. See `Knowledge_Atlas/tests/test_site_runtime_smoke.py`
for the existing test style.

## 7. CLI surface

Add an `if __name__ == "__main__":` block that accepts a `paper_id`
and prints the journey as pretty-printed JSON:

```bash
python3 scripts/paper_journey_view.py PDF-0001
python3 scripts/paper_journey_view.py PDF-0001 --format text
python3 scripts/paper_journey_view.py --all --current-stage extraction
```

## 8. HTTP endpoint (optional, lands second)

If the first-cut CLI + library works, add a minimal FastAPI route in
the existing Knowledge_Atlas backend:

```
GET /api/paper_journey/{paper_id}
    → 200 with PaperJourney JSON
    → 404 if paper_id not found

GET /api/paper_journey?current_stage=extraction&limit=50
    → 200 with array of PaperJourney JSON, streamed
```

Gate the endpoint behind the existing instructor-auth middleware.
Student users see paper_journey only for papers they submitted via
`paper_submissions` (AE DB).

## 9. Deliverables

1. `Knowledge_Atlas/scripts/paper_journey_view.py` — the module.
2. `Knowledge_Atlas/tests/test_paper_journey_view.py` — the tests.
3. Optional: new route in `Knowledge_Atlas/scripts/ka_class_api.py`
   or equivalent existing FastAPI router file.
4. One commit per numbered deliverable above. Commit messages follow
   the existing `<type>: <description>` convention visible in
   `git log --oneline -20`.
5. Update `TASKS.md` "Completed" section with the commit hashes
   when done.

## 10. Handoff notes

- DK's memory file names `ka_article_endpoints.classify_single_paper`
  as a wrapper; if a parallel `ka_article_endpoints.journey_for_paper`
  wrapper makes sense, add it so the naming pattern stays consistent.
- If during implementation the executor notices that `paper_id`
  conventions disagree between the two databases (e.g., Article
  Finder uses DOIs where Article Eater uses `PDF-NNNN` slugs), flag
  it in `docs/ATLAS_SHARED_SUGGESTIONS_2026-04-21.md` under a new
  Codex/AG/other section. Do not unify the IDs — just report.
- Empty / 0-byte `pipeline_lifecycle_full.db` at
  `Knowledge_Atlas__track2rev/data/ka_payloads/` is a stale
  placeholder. The real DB is in the Article_Eater repo path. Do not
  attempt to read from the placeholder.

## 11. Out of scope

- A write-back layer that lets admins edit journey records from
  Knowledge_Atlas. Separate ticket if DK wants it.
- A GraphQL surface. REST is sufficient.
- Historical re-computation of `triage_score` from a saved model.
  The view reads stored fields only.
- Cross-paper analytics (average stages per paper, longest-blocked,
  etc.). Consume this module from a separate analytics script.

---
