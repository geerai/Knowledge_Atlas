# Paper-Quality Blackboard Coordination — Design

**Document**: `PAPER_QUALITY_BLACKBOARD_DESIGN_2026-04-25.md`
**Companions**: `PAPER_QUALITY_BUILD_PROMPT_FOR_CODEX_2026-04-23.md`
(§1.6 references this), `PAPER_QUALITY_TESTING_PROMPT_FOR_CODEX_2026-04-25.md`,
`PAPER_QUALITY_V7_PIPELINE_INTEGRATION_2026-04-23.md`.
**Authorising reviewer**: DK, 2026-04-25.

---

## 0. Why this exists

The existing HTTP coordination server at `localhost:8420`, together
with the `coord.py` CLI and the `COORDINATION_COMMUNICATION_SLA_v1.0`
document, has decayed into disuse. The state file
(`scripts/coordination/coord_state.json`) records last heartbeats
from 2026-03-11 and 2026-03-12, despite substantial multi-agent work
having taken place since. This is a structural failure of
heartbeat-based coordination, not a discipline failure of the
particular workers, and it is the same failure mode that distributed-
systems literature has documented since Lamport's early work in the
1980s: self-reported liveness drifts away from progress; once one
worker stops reporting, social pressure on others to keep reporting
collapses; within several weeks the system is decorative.

`docs/CW_COORDINATION_NOTES.md` is a literal catalogue of this
decay. Five of its six lessons concern *information flow between
workers being unreliable* — SQLite sandbox isolation, uncommitted
files, skim-reading colleague output, hierarchy creep, and testing
infrastructure from the wrong sandbox's perspective. The sixth is
about pointing to existing utilities. The pattern is consistent: the
coordination layer assumes self-report fidelity that the workers,
through no fault of their own, do not sustain.

Per DK's instruction on 2026-04-25, the paper-quality build adopts a
*blackboard architecture* — a shared workspace where the artifacts
themselves are the source of truth, and self-report is advisory only.
The architectural lineage is Hayes-Roth (1985, ~3,500 Google Scholar
citations) and Erman, Hayes-Roth, Lesser & Reddy's Hearsay-II speech-
understanding system (1980, ~3,000 citations). The same idea
re-emerges as event-sourcing in modern distributed systems
(Fowler 2005) and as commit-log-as-source-of-truth in Kafka's
design (Kreps 2014). The principle in all variants is the same: the
artifact is the receipt; reading the artifacts gives the true
shared state without requiring trust in any participant's self-report.

## 1. Architectural overview

The coordination layer is built around five rules. None depend on
the HTTP coord server being available; all depend only on the
database and the git repository.

1. **The database is the blackboard.** Two new tables in
   `pipeline_lifecycle_full.db` (per DK's confirmation: same DB as
   the lifecycle, not a new one) record what work exists, who
   claimed it, and what artifacts were produced. The database's
   atomic-write semantics settle race conditions for free.

2. **Work is batched, not ranged.** The unit of allocation is a
   batch of 25–30 papers (per DK's preference, 2026-04-25). Workers
   claim one batch at a time, process every paper in it, and claim
   another. There is no upfront partition of the corpus.

3. **Artifact existence is the truth-of-completion.** A row in
   `paper_quality_fingerprints` (or `fingerprint_staging` for in-
   flight work) is the receipt that the work was done. A worker's
   claim is meaningful only insofar as it produces such a row.

4. **No preemptive reclamation.** Per DK's instruction: if a worker
   is processing a batch, let it finish. Reclamation is only
   relevant for the *tail* of the queue, when the last batch is
   held by a possibly-dead worker and the queue would otherwise
   never drain.

5. **Cross-sandbox visibility via the git repo.** A JSON mirror of
   the blackboard view (`data/paper_quality_progress.json`) is
   updated after every paper completion, committed locally
   frequently, and pushed to GitHub every roughly 50 papers. AG and
   any other sandbox-bound worker reads this mirror via `git pull`.
   Lesson 1 from `CW_COORDINATION_NOTES` — that AI sandboxes cannot
   share SQLite databases — is structurally addressed rather than
   left as a discipline obligation.

The HTTP coord server can remain running for a human-visible
dashboard (its primary residual value) but it is not in the
critical path for any work-claiming or completion semantics.
Heartbeats become decorative rather than load-bearing.

## 2. Schema

Two new tables and one view, added to the schema migration in
Commit 7 of the build prompt (alongside `paper_quality_fingerprints`,
`fingerprint_staging`, `quality_adjudication_queue`,
`quality_calibration_history`, `hard_rule_violations`, `holding_pen`,
and `paper_interpretation`).

```sql
-- Batches: the unit of claiming. A batch is 25-30 papers
-- belonging to one pass_type. Workers claim batches; they do not
-- claim individual papers.
CREATE TABLE paper_quality_batches (
  batch_id TEXT PRIMARY KEY,                  -- "PQ-BATCH-CLAUDE-001"
  pass_type TEXT NOT NULL CHECK (pass_type IN
    ('extract_codex', 'extract_claude', 'verify_gemini')),
  paper_ids TEXT NOT NULL,                    -- JSON-encoded list of paper IDs
  batch_size INTEGER NOT NULL CHECK (batch_size BETWEEN 25 AND 30),
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN
      ('pending', 'in_progress', 'done',
       'timeout_warning', 'reclaimable', 'failed')),
  current_assignee TEXT,                      -- worker that claimed this batch
  claimed_at TIMESTAMP,
  last_progress_at TIMESTAMP,                 -- updated after each paper completes
  completed_at TIMESTAMP,
  papers_done INTEGER NOT NULL DEFAULT 0,
  papers_failed INTEGER NOT NULL DEFAULT 0,
  notification_events TEXT,                   -- JSON-encoded list of events
  reclamation_count INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX paper_quality_batches_pending_idx
  ON paper_quality_batches (pass_type, status)
  WHERE status IN ('pending', 'reclaimable');

-- Jobs: one row per (paper_id, pass_type). Created at batch
-- creation; updated as each paper is processed.
CREATE TABLE paper_quality_jobs (
  job_id TEXT PRIMARY KEY,                    -- "PQ-PDF-0001-CLAUDE"
  paper_id TEXT NOT NULL,
  pass_type TEXT NOT NULL,
  batch_id TEXT REFERENCES paper_quality_batches(batch_id),
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN
      ('pending', 'in_progress', 'done', 'failed')),
  claimed_at TIMESTAMP,
  completed_at TIMESTAMP,
  artifact_path TEXT,                         -- where the fingerprint row landed
  attempt_count INTEGER NOT NULL DEFAULT 0,
  UNIQUE(paper_id, pass_type)
);

CREATE INDEX paper_quality_jobs_paper_idx
  ON paper_quality_jobs (paper_id);

-- View: per-paper completion state across pass types
CREATE VIEW paper_quality_progress AS
SELECT
  paper_id,
  MAX(CASE WHEN pass_type = 'extract_codex' AND status='done'
           THEN completed_at END) AS codex_done_at,
  MAX(CASE WHEN pass_type = 'extract_claude' AND status='done'
           THEN completed_at END) AS claude_done_at,
  MAX(CASE WHEN pass_type = 'verify_gemini' AND status='done'
           THEN completed_at END) AS gemini_done_at,
  MAX(CASE WHEN status='in_progress' THEN
           pass_type || ':' || COALESCE((
             SELECT current_assignee
             FROM paper_quality_batches b
             WHERE b.batch_id = paper_quality_jobs.batch_id), '?')
           END) AS active_workers,
  COUNT(*) AS pass_count,
  SUM(CASE WHEN status='done' THEN 1 ELSE 0 END) AS pass_done_count
FROM paper_quality_jobs
GROUP BY paper_id;
```

The `UNIQUE(paper_id, pass_type)` constraint on `paper_quality_jobs`
is the atomic-claim primitive: two workers attempting to insert the
same `(paper_id, pass_type)` will see one succeed and one fail. The
status transition `pending → in_progress` is a separate atomic
update guarded by `WHERE status='pending'`.

## 3. The pre-allocation pass

A pre-flight script generates the manifest once, at build start:

```bash
python3 scripts/paper_quality_blackboard_init.py \
  --corpus data/production/paper_corpus.json \
  --batch-size 28 \
  --pools "claude-max:4,codex-pro:4,gemini:1" \
  --out-mirror data/paper_quality_progress.json
```

What it does:

1. Reads the paper corpus list (1 400 papers expected).
2. Generates `paper_quality_jobs` rows for each `(paper_id, pass_type)`
   triple — 4 200 rows total. Status starts as `pending`.
3. Groups jobs into batches of 28 papers per `pass_type` (50
   batches per pass × 3 passes = 150 batches). Writes the
   `paper_quality_batches` rows. Status starts as `pending`.
4. Initial assignment: round-robin across the worker pools named in
   `--pools`. The assignment is *advisory* — recorded in the
   `current_assignee` column with a special prefix
   `pre-allocated:<pool>` to distinguish it from a real claim. This
   gives initial work to each pool but does not preempt
   opportunistic gap-filling.
5. Writes the empty mirror file
   `data/paper_quality_progress.json` so workers have a known path
   to update.
6. Commits the manifest:
   `git add data/paper_quality_progress.json
    contracts/schemas/paper_quality.sql
    scripts/paper_quality_blackboard_init.py
    && git commit -m "Paper-quality blackboard: initial manifest"
    && git push`

The pre-allocated batch IDs are deterministic (e.g.,
`PQ-BATCH-CLAUDE-001` through `PQ-BATCH-CLAUDE-050`) so workers can
recover from interruptions without confusion about which batch is
which.

## 4. The worker loop

Every worker — Claude CLI, Codex CLI, Gemini verifier — runs the
same loop. The pseudocode below assumes a Python implementation
shared across the three adapter wrappers (`atlas_shared.
worker_loop`). Each adapter supplies the per-pass extraction or
verification function.

```python
def run_worker(worker_id: str,
               pass_type: str,
               extractor: Callable[[str], Artifact]) -> None:
    while True:
        batch = blackboard.claim_next_batch(worker_id, pass_type)
        if batch is None:
            log.info("No more batches for %s. Exiting cleanly.",
                     pass_type)
            return

        log.info("Claimed batch %s (%d papers).",
                 batch.batch_id, len(batch.paper_ids))

        for paper_id in batch.paper_ids:
            if blackboard.job_already_done(paper_id, pass_type):
                # Defensive: another worker may have completed this
                # paper between batch creation and now (gap-fill).
                blackboard.mark_paper_skipped_in_batch(
                    batch, paper_id, reason="already_done")
                continue

            try:
                artifact = extractor(paper_id)
                blackboard.mark_paper_done(
                    batch, paper_id,
                    artifact_path=artifact.path)
                # Per-paper update: mirror file refresh
                blackboard.refresh_mirror_for_paper(paper_id)
                # Per-paper update: local git commit
                blackboard.commit_local(
                    f"{pass_type}: {paper_id} done by {worker_id}")
            except SubscriptionRateLimit as e:
                log.warning("Rate-limited on %s; backing off %ds.",
                            paper_id, e.retry_after)
                time.sleep(e.retry_after)
                # Re-attempt the same paper next loop iteration
                continue
            except HardRuleViolation as e:
                blackboard.record_hard_rule_violation(
                    paper_id, e.rule_id, e.violation_state)
                blackboard.mark_paper_failed_in_batch(
                    batch, paper_id, reason=str(e))
                # Per build prompt §5.1: do NOT halt; continue.
                continue
            except Exception as e:
                blackboard.mark_paper_failed_in_batch(
                    batch, paper_id, reason=str(e))
                continue

        blackboard.mark_batch_done(batch)
        # Push to GitHub if 50 papers' worth of commits accumulated
        if blackboard.papers_since_last_push() >= 50:
            blackboard.push_to_github(
                msg=f"Paper-quality progress: through "
                    f"{blackboard.most_recent_paper_id()}")
```

The `claim_next_batch` function is where the atomic claim happens:

```sql
-- pseudocode for the claim
UPDATE paper_quality_batches
   SET status = 'in_progress',
       current_assignee = :worker_id,
       claimed_at = NOW(),
       last_progress_at = NOW()
 WHERE batch_id = (
   SELECT batch_id FROM paper_quality_batches
    WHERE pass_type = :pass_type
      AND status IN ('pending', 'reclaimable')
    ORDER BY
      -- Prefer pre-allocated to my pool first; then any pending;
      -- then anything reclaimable.
      CASE WHEN current_assignee = 'pre-allocated:' || :my_pool
           THEN 0 ELSE 1 END,
      CASE WHEN status = 'pending' THEN 0 ELSE 1 END,
      batch_id
    LIMIT 1
 )
 AND status IN ('pending', 'reclaimable')
RETURNING *;
```

If the `RETURNING` is empty, somebody else won the race; the worker
loops and tries again. If non-empty, the worker has the batch.

## 5. The JSON mirror

The mirror file `data/paper_quality_progress.json` is the cross-
sandbox face of the blackboard. Per DK 2026-04-25:

- **Per-paper update.** After each paper's pass completes
  successfully, the mirror is rewritten atomically (temp file +
  rename). The mirror is therefore always fresh enough that any
  worker, in any sandbox, can read the truth of what is done.
- **Local commit cadence: frequent.** Every paper completion
  commits the updated mirror locally with a deterministic message
  (`paper-quality progress: <paper_id> <pass_type> done by
  <worker_id>`). This keeps the git history fine-grained for
  forensics.
- **GitHub push cadence: every ~50 papers.** Pushes happen when 50
  papers' worth of commits have accumulated since the last push.
  Pushes are non-blocking; if a push fails (network issue, auth
  expiry), the worker logs the failure and continues; the next
  batch's worker will retry. There is no point at which a worker
  stops working because of a push failure.

Mirror file schema:

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-04-25T14:32:11Z",
  "manifest": {
    "total_papers": 1400,
    "total_batches": 150,
    "total_jobs": 4200
  },
  "progress": {
    "papers_with_codex_done": 487,
    "papers_with_claude_done": 462,
    "papers_with_gemini_done": 412,
    "papers_fully_complete": 405,
    "papers_in_holding_pen": 4,
    "papers_with_hard_rule_violations": 7
  },
  "batches": {
    "in_progress": [
      {"batch_id": "PQ-BATCH-CLAUDE-018",
       "assignee": "claude-max-w2",
       "papers_done": 17, "batch_size": 28,
       "claimed_at": "2026-04-25T13:55:02Z",
       "last_progress_at": "2026-04-25T14:31:45Z"},
      ...
    ],
    "pending": ["PQ-BATCH-CODEX-031", "PQ-BATCH-CODEX-032", ...],
    "reclaimable": [],
    "done_count": 87
  },
  "papers_recent": [
    {"paper_id": "PDF-0487", "pass_type": "extract_claude",
     "completed_at": "2026-04-25T14:31:45Z",
     "worker_id": "claude-max-w2"},
    ...
  ]
}
```

The `papers_recent` array carries the last 100 completions so
workers in other sandboxes can confirm activity without parsing the
full history.

## 6. Failure recovery — minimal and tail-only

Per DK 2026-04-25: no preemptive reclamation. Reclamation is
designed to handle one specific failure mode — a worker dies during
its tail batch, leaving the queue stuck. For most of the run the
mechanism does not fire.

Two timeouts, both based on `last_progress_at` (which is updated
after every paper completion within the batch):

1. **Per-paper progress timeout: 30 minutes.** If a batch's
   `last_progress_at` is more than 30 minutes ago AND the batch is
   still `in_progress`, status transitions to `timeout_warning`.
   This does not reclaim the batch. It writes a notification event
   to the batch's `notification_events` JSON column and posts a
   message to the worker's inbox via the standing message system:

   ```bash
   python3 scripts/coordination/coord.py msg system \
     "TIMEOUT_WARNING" \
     "Batch PQ-BATCH-CLAUDE-018 has not progressed in 30 min. \
      Are you still alive? Reply COMPLETE or RELEASE." \
     :assignee:
   ```

   If the worker is alive but slow (say, hit a paper that takes
   long to extract because of OCR pathology), it can either ignore
   the warning and keep working — its next paper completion clears
   the timeout — or release the batch explicitly.

2. **Per-batch reclamation timeout: 4 hours.** If a batch's
   `last_progress_at` is more than 4 hours ago, status transitions
   to `reclaimable`. The next worker that asks for a batch will
   pick it up. The original worker, if it returns, sees its batch
   has been reassigned and moves on; the artifacts of any papers it
   completed are still safely in the database (the unique
   constraint protects them) and the new claimant skips those via
   the `job_already_done` check. The new claimant only redoes the
   unfinished portion.

The 4-hour reclamation timeout is intentionally lax for the bulk of
the run, but it bounds the worst-case tail latency: if every other
worker has finished and one stuck worker holds the last batch, the
queue drains within 4 hours rather than waiting indefinitely.

A `reclamation_count` column on the batch tracks how many times a
batch has been reclaimed. A batch reclaimed three times triggers a
hard-rule violation entry — the batch is presumed unprocessable and
goes to the holding pen for DK review.

## 7. Worker pool and concurrency given DK's subscriptions

Per DK 2026-04-25 (Codex Pro, Claude Max, high-tier Gemini access):

| Pool | Concurrency | Per-worker cadence | Throughput |
|------|-------------|--------------------|------------|
| Claude CLI (`claude -p`) | 4 workers | 1 paper / 12-15 min (5-sample SC) | ~16 papers / hour |
| Codex CLI (`codex exec`) | 4 workers | 1 paper / 12-15 min | ~16 papers / hour |
| Gemini verifier | 1-2 workers | 1 paper / 3-5 min (single-pass verify) | ~12-24 papers / hour |
| Mirror / dashboard | 1 process | Continuous | n/a |

Combined extraction throughput at peak: roughly 32 paper-extracts
per hour, with verification keeping pace. Over an 8-hour working
day that is 256 paper-extracts × 2 model families = roughly 130
papers fully processed per day. The 1 400-paper retrofit completes
in 11 working days.

If self-consistency drops from five samples to three on the
retrofit (calibration still uses five), per-worker cadence drops to
8-10 minutes per paper and the retrofit completes in 7-8 working
days. This is the recommended tuning unless you specifically want
the tighter five-sample variance estimates on every paper.

## 8. Interaction with the existing coord server

The `localhost:8420` HTTP server is repositioned as follows:

- **Retained**: the dashboard (`GET /` HTML page) provides a
  real-time view of worker status for human consumption. The
  message-passing endpoints (`POST /message`, `GET /messages`)
  remain in use for the timeout-warning notifications and for any
  ad-hoc human-to-worker messages.
- **Demoted**: the task-claiming endpoints (`POST /claim`, `POST
  /release`, `POST /complete`) are no longer authoritative. The
  blackboard tables are. The endpoints can either be removed in a
  follow-up cleanup or kept as a thin proxy over the database.
- **Optional**: heartbeat (`POST /heartbeat`) remains as advisory
  signal for the dashboard. A worker that does not heartbeat is
  not blocked from working; it simply does not appear on the
  dashboard.

A subsequent cleanup pass can prune `coord_server.py` to the
dashboard role. That work is out of scope for the paper-quality
build but should be filed as a TASKS.md entry.

## 9. Migration path

The schema migration in Commit 7 of the build prompt adds the two
new tables and the view. The pre-flight script
`paper_quality_blackboard_init.py` is added in a new Commit 6.5
(immediately before the worker-loop wrapper, so the manifest can be
generated before any worker starts).

Existing workers (CW, AG, Codex) read this design doc and the
revised build prompt before claiming any paper-quality work. The
HTTP coord server can stay running but workers do not depend on it
for claims. The `CW_COORDINATION_NOTES.md` file gains a new lesson:

> **Lesson 7: Use blackboards, not heartbeats.** When multiple
> workers process work in parallel, the source of truth is the
> artifact, not anyone's status report. Build claim semantics on
> atomic database writes; build cross-sandbox visibility on
> committed git artifacts; treat heartbeats as decorative. The
> 2026-04-25 paper-quality blackboard design is the canonical
> example.

## 10. Open questions deferred to implementation

These are things the build will surface but which do not need DK's
decision in advance:

- **Conflict resolution when two workers race on the same batch.**
  The `RETURNING` clause guarantees only one wins; the other
  retries. We expect contention to be rare given pre-allocation,
  but the metric should be logged.
- **Concurrent JSON mirror writes.** The temp-file-and-rename
  pattern is correct but loses recent updates if two workers
  rename within the same millisecond. A short file-lock around the
  rename is sufficient; implementation will use Python's `fcntl`.
- **GitHub push contention.** Two workers attempting `git push`
  simultaneously will produce one fast-forward failure. The handler
  re-pulls, re-commits if needed, and retries. Acceptable noise.
- **Backfill of the existing 1 400-paper corpus.** The blackboard
  treats backfill identically to new work: the manifest includes
  every paper in the corpus, including the existing 1 400. The
  retrofit pass after the build is just running the workers
  against the pre-populated batches.

## References

Erman, L. D., Hayes-Roth, F., Lesser, V. R., & Reddy, D. R. (1980).
The Hearsay-II speech-understanding system: Integrating knowledge
to resolve uncertainty. *ACM Computing Surveys*, 12(2), 213–253.
https://doi.org/10.1145/356810.356816 (Google Scholar: ~3,000)

Hayes-Roth, B. (1985). A blackboard architecture for control.
*Artificial Intelligence*, 26(3), 251–321.
https://doi.org/10.1016/0004-3702(85)90063-3 (Google Scholar: ~3,500)

Lamport, L. (1978). Time, clocks, and the ordering of events in a
distributed system. *Communications of the ACM*, 21(7), 558–565.
https://doi.org/10.1145/359545.359563 (Google Scholar: ~17,000)

Fowler, M. (2005). *Event sourcing*. martinfowler.com.
https://martinfowler.com/eaaDev/EventSourcing.html

Kreps, J. (2014). I ♥ logs: Event data, stream processing, and
data integration. O'Reilly Media. (Foundational essay reprinted as
a short book.)

---

*End of design. Implementation lands in build-prompt Commits 6.5
and 7.*
