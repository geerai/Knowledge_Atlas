# Class-start deployment checklist — COGS 160 Spring 2026

*Last updated: 2026-04-19*
*Audience: DK (instructor of record)*
*Purpose: a single runbook for going live with the rubric + grading + admin stack built across commits `0e365f0` through `bf39a8f`. Follow the order; each step has a single-command verification.*

---

## Before Week 1 (one-time setup)

### 1. Confirm the production machine and paths

On the machine where `xrlab.ucsd.edu` will serve from (or on your Mac if we're running locally for now):

```bash
cd /Users/davidusa/REPOS/Knowledge_Atlas
git status             # should show clean; if not, stash or commit first
git log --oneline -3   # tip should be bf39a8f or newer
```

Verify the sibling AE-recovery repo is reachable from here:

```bash
ls /Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/data/pipeline_registry_unified.db
# should show ~ 9.3 MB; don't worry about the contents
```

### 2. Apply the class-state migration

```bash
python3 -c "
import sqlite3
con = sqlite3.connect('data/ka_auth.db')
con.executescript(open('scripts/migrations/2026-04-17_class_state.sql').read())
con.close()
print('migration applied')
"
```

The migration is idempotent — re-running is safe. Expected output: `migration applied`.

### 3. Seed the offering + deliverables + demo students

```bash
python3 scripts/seed_class_state.py
```

Expected: `class_offerings` gains the `cogs160sp26` row, 31 deliverables land, 15 demo students populate `enrollments`. If the demo students are already there the seeder skips them (idempotent). Dry-run first with `--dry-run` if you want to preview.

### 4. Run the full smoke test

```bash
bash scripts/smoke_test_e2e.sh
```

Expected: `all 11 stages passed`, green ✓ for each. If any stage fails the script stops and prints the failure; re-run after fixing. This is the one-command confirmation that every moving part is wired correctly.

### 5. Set the admin token

For the FastAPI backend's admin endpoints. Two options; pick one.

**Option A — production path** (`/etc/ka/admin_token.txt`):

```bash
sudo mkdir -p /etc/ka
echo "<pick a long random string>" | sudo tee /etc/ka/admin_token.txt
sudo chmod 600 /etc/ka/admin_token.txt
```

**Option B — environment variable** (for local dev or a process you control):

```bash
export KA_ADMIN_TOKEN="<pick a long random string>"
```

**Do not use `KA_ADMIN_ALLOW_OPEN=1` in production.** That flag exists only for local development and the smoke test. If neither the file nor the env var is set, the admin endpoints return 503.

After setting: the same token must be stored in each admin browser's session storage under `ka.adminToken` so `ka_admin.html` can send it in the `X-Admin-Token` header.

### 6. Start the backend

Development, with auto-reload:

```bash
uvicorn scripts.ka_class_api:app --reload --port 8080
```

Production, single worker, bound to localhost for the reverse proxy:

```bash
nohup uvicorn scripts.ka_class_api:app --host 127.0.0.1 --port 8080 >/tmp/ka_class_api.log 2>&1 &
```

Verify:

```bash
curl -s http://127.0.0.1:8080/api/admin/class/health | python3 -m json.tool
```

Expected: `{"ok": true, "db": "...", "offerings": 1}`.

---

## When the real roster arrives

### 7. Import the real roster

Drop the Registrar CSV somewhere and run:

```bash
python3 scripts/import_roster.py --csv ~/Downloads/roster.csv --dry-run
# Review the summary; confirm column detection matched
python3 scripts/import_roster.py --csv ~/Downloads/roster.csv
# Then to retire the demo students:
python3 scripts/import_roster.py --csv ~/Downloads/roster.csv --drop-demo
```

Expected: new users are created, enrollments inserted, demo students flipped to `status='dropped'`. Unassigned-track students are listed at the end so you can assign them at the Week-3 planning meeting.

---

## Before students arrive (Week 1)

### 8. Verify every T1–T4 rubric is readable

Every student should be able to open these from the 160sp site:

```
160sp/rubrics/README.md
160sp/rubrics/common/a0.md  common/a1.md
160sp/rubrics/t{1,2,3,4}/README.md   plus T{1,2,3,4}.{a..g}
160sp/rubrics/f160/README.md
160sp/rubrics/verification/README.md
```

Spot-check one rubric per track.

### 9. Verify the `ka_contribute.html` submission path works

Open `ka_contribute.html` in a browser (served locally or from the production VM). Attempt a test submission of one article. Confirm the row lands in `pipeline_registry_unified.db` (cross-repo). The adapter `scripts/ka_af_intake_adapter.py` is the bridge.

### 10. Verify the admin page loads and the Grading tab shows the (empty) roster

Open `160sp/ka_admin.html`, go to the Grading tab. Expected: 15 demo students listed if the real roster isn't imported yet; real students after step 7. All totals should be 0/100 because no dossiers exist yet.

---

## During the sprint

### 11. Run a grading pass (end of each week)

Follow `scripts/run_grading_pass.md`. The Cowork / Claude Code master session builds briefings with `python3 scripts/ai_grader.py queue`, then dispatches subagents via the Task tool. Check progress with `python3 scripts/ai_grader.py status`.

### 12. Spot-check the audit queue weekly

Open the Grading tab; review the Audit Queue card. 20 % of graded dossiers are sampled for TA blind re-grading. Follow the TA audit procedure in `160sp/rubrics/verification/README.md`.

### 13. Review calibration health

Same tab, Calibration Health card. Three κ columns per deliverable with pass/fail gates (0.70 / 0.65 / 0.55). Any deliverable with κ below a gate should have grading paused and exemplars revised before resuming.

---

## End of quarter

### 14. Final grading pass + review

One more grading pass; read every final report; adjust any grades that need it in the `grade_dossiers` table (bump a new row with `is_final=1`, flip the old row's `is_final=0`).

### 15. Export eGrades CSV

```bash
python3 scripts/export_egrades.py --offering cogs160sp26 --dry-run --letter-grades
# Review the dry-run table for every student; fix any cell that needs manual override
python3 scripts/export_egrades.py --offering cogs160sp26 --letter-grades \
    --out /Volumes/ka-backup-5T/exports/cogs160sp26_egrades_2026-06-15.csv
```

### 16. Upload to the UCSD Registrar

https://act.ucsd.edu/egrades → select the term and course → upload CSV → confirm preview → submit. The CSV format (UTF-8, CRLF, four columns) matches the Registrar's 2025–26 spec.

### 17. Archive to the 5 TB disk

Per `docs/END_OF_QUARTER_WORKFLOW_2026-04-18.md`. Copy `160sp/grading/` and `data/ka_auth.db` to `/Volumes/ka-backup-5T/{dossiers,snapshots}/cogs160sp26/`. Five-year retention minimum; hard-delete candidates surface on July 1 of year six.

---

## Troubleshooting

| Symptom | First thing to check |
|---|---|
| Admin page shows demo data even after real roster import | `KA_ADMIN_TOKEN` unset; admin page falling back to `DEMO_*`. Set token in browser sessionStorage. |
| Smoke test fails at stage 4 (backend boot) | Port 8099 already in use. `lsof -ti:8099 \| xargs -r kill`. |
| Smoke test fails at stage 3 (classifier DB) | Sibling repo not reachable. Set `KA_UNIFIED_REGISTRY_DB=/path/to/unified_registry.db`. |
| `ai_grader.py queue` says 0 briefings | Students may already have dossiers (idempotent). Add `--force` to rebuild. |
| FastAPI backend returns 503 on every call | Admin token not configured. See step 5. |
| Grading run stalls | Briefing stuck in `in_progress/`. Move back to `queue/` and redispatch (see `run_grading_pass.md`). |

## What this checklist does not cover

- Shibboleth SSO. Deferred to Fall 2026; see `docs/SHIBBOLETH_INTERIM_NOTE_2026-04-18.md`. Until then, password auth against `data/ka_auth.db`.
- SMTP for password-reset emails. Depends on SMTP credentials we don't have.
- RAG-audit deliverable T2.d.2. In design only; waiting for Codex's topic work to stabilise. See `docs/RAG_AUDIT_CROSSWALK_INTEGRATION_DESIGN_2026-04-18.md`.
- Exemplar authoring for AI-grading. Week-3 track-lead deliverable; until exemplars land, grading runs in degraded mode per `160sp/rubrics/prompts/grading_prompt_template.md` § Degraded mode.

## References

UC San Diego Registrar. (2024). *eGrades instructor's guide*. https://students.ucsd.edu/academics/academic-calendars/egrades.html

University of California, Office of the President. (2024). *UC Records Retention Schedule*. https://recordsretention.ucop.edu/

Family Educational Rights and Privacy Act, 20 U.S.C. § 1232g; 34 CFR Part 99. U.S. Department of Education. https://studentprivacy.ed.gov/
