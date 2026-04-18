# How to run a grading pass

*Last updated: 2026-04-17*
*Audience*: DK or any Claude Code / Cowork session dispatching a grading pass
*LLM model*: Claude via subscription (claude.ai, Cowork, Claude Code) — **no API key required, no per-call cost**

---

## The pattern in one sentence

`scripts/ai_grader.py` is a pure Python orchestrator that builds prompt briefings into a file-based queue; a master Claude Code / Cowork session reads the queue and spawns one subagent per briefing via the Task/Agent tool. Each subagent is a fresh Claude conversation running on the subscription, not an API call.

---

## From Cowork or Claude Code, run a full pass

Open Cowork (or a Claude Code terminal in this repo) and paste the following request to the master session:

> Run a grading pass for COGS 160sp. Use `scripts/ai_grader.py` to build the queue, then dispatch one subagent per briefing using the Agent tool (general-purpose agent, medium thoroughness). Each subagent must follow the briefing's instructions end-to-end: read the rubric, read the submission artefacts, produce the dossier at the path named in §6 of the briefing, then shell out to `python3 scripts/ai_grader.py complete {sid} {deliverable_id}` to close the loop. Dispatch up to 8 subagents in parallel. Stop when the queue is empty.

The master session will then:

1. `python3 scripts/ai_grader.py queue` → build briefings for every ungraded submission.
2. `python3 scripts/ai_grader.py status` → show the queue size.
3. `python3 scripts/ai_grader.py dispatch 8` → pop 8 briefings from `queue/` to `in_progress/` and print their paths.
4. For each briefing path: launch a subagent with a prompt like *"Read this briefing and follow its instructions end-to-end: {briefing_path}"*.
5. Wait for subagents to complete (each ends with the `complete` shell-out).
6. Loop: dispatch 8 more, until the queue is empty.

---

## Running only part of a pass

### One student, one deliverable

```
python3 scripts/ai_grader.py queue --student s03 --deliverable T1.b
```

Then ask the master session to dispatch one subagent for the single briefing.

### One deliverable across all students

```
python3 scripts/ai_grader.py queue --deliverable T1.b
```

### All deliverables for one student (catchup)

```
python3 scripts/ai_grader.py queue --student s03
```

### Re-grade something that was already graded

```
python3 scripts/ai_grader.py queue --student s03 --deliverable T1.b --force
```

`--force` rebuilds the briefing even if a dossier already exists. The old dossier is not deleted; a new one is written at today's date. The grading sheet will use the most recent non-superseded dossier.

---

## Inspecting progress mid-pass

```
python3 scripts/ai_grader.py status
```

Prints: queue size, in-progress size, done size, and the first 10 queued briefings.

---

## If a subagent gets stuck

Briefings in `in_progress/` for > 2 hours without a `complete` callback are considered stuck. Two options:

1. **Re-dispatch**: manually move the briefing back to `queue/`, then re-dispatch.

    ```
    mv 160sp/grading/in_progress/s03_T1.b.md 160sp/grading/queue/
    ```

2. **Abandon and re-queue**: delete the in_progress briefing and re-run `queue --student s03 --deliverable T1.b --force`.

---

## Why this architecture, not an API script

Two reasons:

1. **Cost.** The subscription is fixed-cost; API calls are per-token. A 40-student × 30-deliverable quarter is ~ 1,200 dossiers; at typical dossier sizes (~ 15 k input + 2 k output tokens), API cost would run $180–$360 per quarter. Subscription cost is zero marginal.
2. **Human oversight is easy.** Because each grading dispatch is visible in the master Cowork session, DK or a TA can watch it happen, intervene mid-pass, or pause the dispatch if something looks off. An API-driven batch script runs silently and harder to inspect.

The trade-off is slightly higher per-dossier latency (subagent spin-up is ~ 3–5 seconds) and more master-session context tokens. Both are acceptable at the class scale.

---

## When this moves to the admin UI

The Grading tab in `ka_admin.html` has a **Run grading pass** button that currently calls `ADMIN_API.runGradingPass()` (a demo stub). Once the DB migration (see `docs/CLASS_STATE_DATABASE_DESIGN_2026-04-17.md`) lands, that stub is replaced by a POST to `/api/admin/class/grading/run`, which shells out to `python3 scripts/ai_grader.py queue` on the server. The actual dispatching still happens via a Claude Code / Cowork master session — the admin UI only triggers the queue build and reports progress.

This keeps the architecture consistent: the admin UI is the control surface, Python is the orchestrator, and Claude (subscription) is the grader.

---

## Files this pass touches

| Path | Read | Write |
|------|------|-------|
| `160sp/rubrics/**` | ✓ | — |
| `160sp/rubrics/prompts/grading_prompt_template.md` | ✓ | — |
| `pipeline_registry_unified.db` | ✓ | — |
| `data/ka_auth.db` (roster) | ✓ | — |
| `160sp/grading/queue/**.md` | ✓ | ✓ |
| `160sp/grading/in_progress/**.md` | ✓ | ✓ |
| `160sp/grading/done/**.md` | ✓ | ✓ |
| `160sp/grading/{sid}/{deliv}_{YYYY-MM-DD}.md` | — | ✓ (by subagents) |
