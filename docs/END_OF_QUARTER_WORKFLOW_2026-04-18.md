# End-of-quarter workflow — dossiers → eGrades → retention

*Date*: 2026-04-18
*Author*: CW (responding to DK's 2026-04-17 note)
*Status*: Addendum to `CLASS_STATE_DATABASE_DESIGN_2026-04-17.md` and `160sp/rubrics/AI_GRADING_DESIGN_2026-04-17.md`

---

## 1. What DK wants

Two decisions clarified on 2026-04-17:

1. **No cohort rollover.** Each COGS 160 offering is independent. Spring 2026 records do not migrate to Fall 2026; Fall 2026 starts with an empty class-state schema populated from the new roster and new rubric set. Student accounts may persist if the student takes both courses, but their enrolment, submissions, dossiers, and grades are scoped to the offering.

2. **Multi-year retention on the 5T backup disk.** Per UC records schedule (and FERPA/access-request floors discussed earlier), grade records should be retained for several years. DK confirmed the 5T external disk as the retention medium. The design below specifies the export, the backup, and the destruction policy.

## 2. End-of-quarter workflow (one page)

```
┌─────────────────┐   grading passes     ┌──────────────────────────────┐
│   submissions   │ ──── (AI grader) ──▶ │ 160sp/grading/{sid}/*.md     │
└─────────────────┘                      │  (dossier files, AI-graded)  │
                                         └──────────────┬───────────────┘
                                                        │
                                      export_egrades.py │
                                                        ▼
                                         ┌──────────────────────────────┐
                                         │ 160sp/grading/archive/       │
                                         │   {offering}_egrades_*.csv   │   ← git-tracked
                                         └──────────────┬───────────────┘
                                                        │
                                           cp to 5T     │      manual upload
                                                        ▼                  ▼
┌────────────────────────────────────┐              ┌─────────────────────┐
│ /Volumes/ka-backup-5T/             │              │  eGrades web UI     │
│   exports/                         │              │  (UCSD Registrar)   │
│   dossiers/                        │              └─────────────────────┘
│   EXPORT_LOG.md                    │
│  (authoritative, 5+ year retention)│
└────────────────────────────────────┘
```

### Concretely, Week 10 end-of-quarter steps (DK, ~ 30 minutes)

1. **Close out grading.** Run the final grading pass: `python3 scripts/ai_grader.py queue` + dispatch subagents (see `scripts/run_grading_pass.md`). Confirm every student has a dossier for every deliverable that applies to them.

2. **Review and adjust.** Spot-check the dossiers. For any deliverable where TA audit flagged disagreement, read the dossier and adjust. Mark adjustments in the dossier frontmatter (`adjusted_by: dkirsh` + `adjustment_reason`) and increment the dossier filename date.

3. **Export eGrades CSV.**

    ```bash
    python3 scripts/export_egrades.py \
        --offering cogs160sp26 \
        --letter-grades \
        --out /Volumes/ka-backup-5T/exports/cogs160sp26_egrades_2026-06-15.csv
    ```

    The script also writes a git-tracked copy to `160sp/grading/archive/cogs160sp26_egrades_2026-06-15.csv` and logs the export in `160sp/grading/archive/EXPORT_LOG.md`.

4. **Preview and fix.** The CSV is UTF-8 + CRLF (eGrades requirement). DK opens it in Excel or a text editor, confirms each row maps the right student PID to the right letter grade, and edits any cell that needs manual override. Edits are also logged to `EXPORT_LOG.md`.

5. **Upload to eGrades.** Log into https://act.ucsd.edu/egrades, select the term and course, use the "Upload CSV" option, confirm the preview, submit.

6. **Archive the dossiers.** Copy the full `160sp/grading/{sid}/` tree to `/Volumes/ka-backup-5T/dossiers/cogs160sp26/` for the multi-year retention copy. This is the authoritative record and is what FERPA requests will be answered from.

7. **Commit the archive CSV** (not the dossier files — they stay on the 5T only after the quarter closes to keep repo size manageable; the git copy of the CSV is enough for day-to-day reference). The `archive/EXPORT_LOG.md` file gets the final commit entry.

## 3. What lives where, and for how long

| Artefact | Primary home | Backup home | Retention |
|----------|--------------|-------------|-----------|
| Student roster & enrolment | `data/ka_auth.db` (once migrated) | 5T nightly snapshot | 5 years (UC schedule) |
| Grade dossiers (per-deliverable) | `160sp/grading/{sid}/*.md` during quarter; `/Volumes/ka-backup-5T/dossiers/{offering}/` after close | git archive commit (opt-in) | 5 years |
| eGrades export CSV | `/Volumes/ka-backup-5T/exports/` AND `160sp/grading/archive/` | git history | 7 years (Title IV floor) |
| Export log | `160sp/grading/archive/EXPORT_LOG.md` | git | Permanent |
| Appeal records | `data/ka_auth.db` `appeals` table | 5T nightly snapshot | 5 years |
| Raw student submissions (PDFs, tag rows, commits) | Track-specific (pipeline_registry, atlas_tag_db, student git branches) | 5T nightly snapshot | Per track |

**Destruction**: hard-delete candidates on July 1 of the sixth year after the quarter ended (Spring 2026 → destruction eligible 2032-07-01). DK runs the destruction script manually after reviewing the list; no automated destruction without instructor confirmation.

## 4. 5T disk layout

```
/Volumes/ka-backup-5T/
├── dossiers/
│   ├── cogs160sp26/
│   │   ├── s01/
│   │   │   ├── A0_2026-04-27.md
│   │   │   ├── A1_2026-05-04.md
│   │   │   ├── T1.a_2026-05-04.md
│   │   │   └── ...
│   │   └── ...
│   ├── cogs160fa26/        ← next cohort, independent
│   └── ...
├── exports/
│   ├── cogs160sp26_egrades_2026-06-15.csv
│   ├── cogs160sp26_egrades_2026-06-15.md   (provenance note)
│   └── ...
├── snapshots/              ← nightly sqlite .db backups
│   ├── ka_auth_2026-04-18.db
│   └── ...
└── README.md
```

`README.md` on the disk root records the retention policy, the mount-point expectation (`/Volumes/ka-backup-5T/`), and the destruction calendar.

## 5. No cohort rollover — mechanical implications

Every DB table that has the `offering_id` column is scoped by offering. A query that omits the `offering_id` predicate is a bug. Concretely:

- `enrollments`, `deliverables`, `submissions`, `grade_dossiers`, `calibration_runs`, `audit_samples`, `appeals`, `announcements` all carry `offering_id`.
- The `student_totals_v` view is parameterised on `offering_id`.
- The admin UI's Grading tab takes `offering_id` from a dropdown at the top of the page (default: current offering).

When Fall 2026 starts, DK creates a new `class_offerings` row (`cogs160fa26`), imports the fall roster into `enrollments`, imports the (possibly revised) rubrics into `deliverables`, and begins. The Spring schema is untouched; admin views default to the current offering but can be pointed at any past offering for audit / reference.

## 6. What this enables

Three practical wins:

1. **Audit-answerable.** A grade dispute in 2029 about a 2026 submission can be answered from the 5T dossier archive, which contains the full evidence trail — original submission, AI dossier with cited spans, TA audit result if sampled, appeal record if filed.
2. **Accreditation-ready.** WSCUC and the UCSD Academic Senate can point at a reproducible grading pipeline with specified retention.
3. **Clean institutional memory across cohorts.** No conflation between Spring and Fall; each offering's grade distribution, calibration history, and rubric revisions are queryable in isolation.

## 7. Implementation status

- [x] `scripts/export_egrades.py` — the eGrades CSV exporter with dry-run, letter-grade, and cutoffs support. Smoke-tested.
- [x] `scripts/ai_grader.py` — grading orchestrator (subscription-LLM).
- [x] `scripts/run_grading_pass.md` — instructions for Cowork/Claude Code.
- [x] `160sp/rubrics/prompts/grading_prompt_template.md` — the canonical grading prompt.
- [ ] `scripts/backup_to_5t.sh` — nightly rsync script (to be written; one-liner against existing rsync pattern).
- [ ] `scripts/destruction_list.py` — reads the archive and reports what is destruction-eligible this July (to be written in 2027).
- [ ] 5T disk mounted at a stable path and bootstrapped with the directory layout above.

## 8. References

University of California, Office of the President. (2024). *UC Records Retention Schedule*. https://recordsretention.ucop.edu/ — authoritative retention floor.

UC San Diego Academic Senate. (2023). *Regulation 500: Grades*. https://senate.ucsd.edu/operating-procedures/ — UC letter-grade scale and grade-change procedures.

UC San Diego Registrar. (2024). *eGrades instructor's guide*. https://students.ucsd.edu/academics/academic-calendars/egrades.html — CSV format spec and upload procedure.

U.S. Department of Education. (2021). *Family Educational Rights and Privacy Act (FERPA) regulations*. 34 CFR Part 99. https://studentprivacy.ed.gov/

Family Educational Rights and Privacy Act, 20 U.S.C. § 1232g (1974). — statutory authority for the access and disclosure-logging requirements.
