# Knowledge Atlas — Standing Todo (session-spanning)

**Last updated**: 2026-04-19
**Purpose**: Cross-session task queue so work continues ballistically between sessions. AI workers pick up from this list when no new user directive is pending.

---

## Tier 1 — Active / in flight

| # | Task | Owner | Notes |
|---|------|-------|-------|
| 1 | Build the five topic-page variants and the T4.b.2 evaluation rubric | CW | In flight 2026-04-19. Facet View (progressive), Heatmap, Dashboard, Full Facets, Quick Lookup. Each a real page on the site. T4.b.2 connects user-type scenarios to per-variant walkthroughs. |
| 2 | Retrofit ~30 remaining 160sp/ pages to canonical navbar | CW | Targets: ka_schedule, ka_track_signup, weekN_agenda, ka_dashboard. Each migration drops 3 validator errors. |
| 3 | Exemplar authoring for AI-grading rubrics | DK + track leads | Week-3 deliverable. Four band-exemplars per deliverable (28 deliverables × 4 = 112 exemplars in all). Without these, AI grading runs in degraded mode per prompt-template §Degraded-mode. |
| 4 | Visual regression baseline via scripts/visual_check.py | CW | Needs local Chromium via playwright; first run captures baselines; schedule weekly after. |

## Tier 2 — Design review / decisions pending

| # | Task | Owner | Notes |
|---|------|-------|-------|
| 5 | **Topic hierarchy review** | Codex (in flight) + DK | Codex is actively building the topic crosswalk (`docs/TOPIC_CROSSWALK_AND_TOPIC_PAGE_CONTRACT_2026-04-19.md`, payload `data/ka_payloads/topic_crosswalk.json`). 102 defended rows × 18 outcomes × 9 architectural families. Existing 18 topics in topics.json read as cluster labels. |
| 6 | T1.5 → Topics lattice graphs | CW | Blocked on #5. Each of the 13 T1.5 pages needs a lattice to its topic children. |
| 7 | Panel review of 11 T1 framework pages | Panel | LLM-drafted 2026-04-17, 1127–1605w each. Draft banner on every page. |
| 8 | Panel review of 71 mechanism profiles (PNUs) | Panel | 54 full (≥600w), 11 brief (300–599w), 6 stub (<300w). Only the 6 stubs need fresh authorship. |
| 9 | Expand framework deep dives beyond current range when literature warrants | Panel | Not every framework needs 1500w. |
| 10 | Reconcile dual framework naming (hierarchy PP/SN/DP/DT vs _index.md) | Panel | Noted in §122.13 of master doc. |

## Tier 3 — Class-start operational

| # | Task | Owner | Notes |
|---|------|-------|-------|
| 11 | Follow `docs/CLASS_START_CHECKLIST_2026-04-19.md` at class start | DK | 17 numbered steps. Smoke test passes currently. |
| 12 | Import real roster when Registrar CSV arrives | DK | `scripts/import_roster.py --csv ... --drop-demo`. |
| 13 | Set `KA_ADMIN_TOKEN` (or `/etc/ka/admin_token.txt`) before deploying the backend | DK | Fail-closed default — backend returns 503 without it. |
| 14 | Deploy scripts/ka_admin_refresh_endpoint.py to production | Ops | Follow SSH_SETUP_FOR_PNU_REFRESH.md. |
| 15 | Wire ka_forgot_password.html to production SMTP | Ops | Depends on SMTP credentials. |
| 16 | Wire ka_contribute.html POST to /api/articles/submit | Ops | Endpoint exists; form stubs the submission. |

## Tier 4 — AI grading infrastructure follow-ups

| # | Task | Owner | Notes |
|---|------|-------|-------|
| 17 | Implement RAG-audit crosswalk integration | CW | Blocked on Codex topic-work stabilising. Design in `docs/RAG_AUDIT_CROSSWALK_INTEGRATION_DESIGN_2026-04-18.md`. 3–4 hours when unblocked. |
| 18 | Real RAG service adapters | CW | Blocked on DK confirming services list + API credentials. Skeleton at `scripts/rag_harvest.py`; stubs in `scripts/rag_adapters/`. |
| 19 | Build `scripts/backup_to_5t.sh` rsync script | CW | Per end-of-quarter workflow §7. One-liner against rsync. Depends on 5T disk mounted at stable path. |
| 20 | Build `scripts/destruction_list.py` | CW | 2027, per end-of-quarter §7. Surfaces destruction-eligible records on July 1 of year 6 for manual review. |
| 21 | Classifier end-to-end audit on a 20-paper instructor-hand-labelled sample | DK | Audit sample CSV at `/tmp/classifier_audit_sample.csv` once regenerated; fill "instructor_agrees?" column. |
| 22 | Classifier-repair sprint: fill `primary_topic_candidate`, `canonical_triage_decision`, fix `classification_confidence` to numeric | Future | Currently 0 % populated. See `docs/CLASSIFIER_AUDIT_FINDINGS_2026-04-18.md` and UNIFIED_PIPELINE_REFERENCE addendum. |

## Tier 5 — Polish and follow-through

| # | Task | Owner | Notes |
|---|------|-------|-------|
| 23 | Near-miss review queue in ka_admin.html | CW | §4.5 of pipeline reference doc. |
| 24 | Classifier performance dashboard on admin Site Health tab | CW | §4.6 of pipeline reference. classifier_eval_*.json exists but has no dashboard. |
| 25 | atlas_shared usage cheat sheet | CW + Codex | §4.7. Help Track 2 students call AdaptiveClassifierSubsystem from their own code. |
| 26 | Shibboleth SP registration with UCSD ITS | DK + Ops | Deferred to Fall 2026 per DK 2026-04-18. See `docs/SHIBBOLETH_INTERIM_NOTE_2026-04-18.md`. |

---

## Recently completed (last ~ 10 days)

- **Class-state database backend**: SQL migration (10 new tables + student_totals_v view), seeder, FastAPI (6 GET + 2 POST endpoints), admin dual-write hook. Applied to data/ka_auth.db. (`9408a6e`, Codex-review fixes `94d07f9`)
- **Roster import scaffold** (`scripts/import_roster.py`) with column detection, dry-run, drop-demo, audit-log entries. (`f2e3084`)
- **End-to-end smoke test** (`scripts/smoke_test_e2e.sh`) — 11 stages, all passing. (`f2e3084`)
- **Complete rubric scaffold**: 40 rubric files covering every deliverable; AI-grading design doc (§10 amended for subscription-LLM orchestration); eGrades exporter; grading orchestrator; TA audit procedures. (`0e365f0`, `40f187b`)
- **T2.d.2 RAG-audit rubric + infrastructure**: rubric draft, harvest orchestrator, classify-check, pluggable service adapters, rag_services.yaml. (`94becac`, `7eb912b`)
- **Classifier audit**: 1,393-paper corpus audit; 9 × 18 modality × outcome taxonomy documented; 0 %-populated columns flagged. (`7eb912b`)
- **13 T1.5 domain-theory pages**: one full (ART), twelve panel-review stubs with real references. Generator-driven. (`84cbfbb`)
- **Crosswalk GUI mockups**: 5 patterns over Codex's live crosswalk payload; Pattern 5 progressive-disclosure added after DK overwhelm concern. (`353ad1f`, `bf39a8f`)
- **RAG-audit × crosswalk integration design** (not implemented): `docs/RAG_AUDIT_CROSSWALK_INTEGRATION_DESIGN_2026-04-18.md`. Design-only per DK while Codex finishes topic work.
- **Policy docs**: end-of-quarter workflow, Shibboleth interim note, session report for Codex review, class-start checklist. Codex confirmed the P1/P2 review fixes landed.
- **Codex's atlas_shared integration** to ka_article_endpoints.py committed under Codex's name (`f87c2c9`).
- **Grading tab** on ka_admin.html with dossier modal, calibration health, audit queue, appeals with two-stage resolution. (`f844e88`)
- **Restored ka_contribute.html** to production two-path design. (`e14066a`)
- **11 T1 framework pages** with 300w summaries + 1500w deep dives + 10 references each. (pre-session)

---

## How to use this file

**AI workers at the start of a session**: read this, pick the highest-priority unblocked task, execute ballistically until blocked or complete, update this file at session end.

**Human reviewers**: edit this file directly to add, remove, or reorder tasks. Move completed items to "Recently completed". The file is canonical; individual TODO markers scattered across code comments defer to this list.

**When something new blocks**: add it in Tier-appropriate section with the blocker clearly named. When something unblocks: move it up a tier or up in its tier.
