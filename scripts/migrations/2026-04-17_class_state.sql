-- ═════════════════════════════════════════════════════════════════════════
-- Migration: class-state schema extension to data/ka_auth.db
-- Date:      2026-04-17
-- Authors:   CW (per docs/CLASS_STATE_DATABASE_DESIGN_2026-04-17.md §3)
-- Target:    data/ka_auth.db (SQLite 3.x)
-- ─────────────────────────────────────────────────────────────────────────
-- Adds ten new tables and one view to support per-offering class state:
-- enrollments, deliverables, submissions, grade dossiers, calibration,
-- audit samples, appeals, announcements, class-scoped audit, plus a
-- student_totals_v view that replaces the JS-side roster arithmetic.
--
-- Staging (see §4 of the design doc):
--   Stage 1 (this migration) — additive. Nothing reads yet; rollback is
--   trivial (DROP the new tables).
--   Stage 2 — dual-write hook in ka_admin.html ADMIN_API.
--   Stage 3 — per-tab read flip via /api/admin/class/*.
--   Stage 4 — remove demo arrays from ka_admin.html.
--
-- Safety:
--   - Every CREATE uses IF NOT EXISTS so the migration is idempotent.
--   - Foreign keys reference existing users(user_id) in ka_auth.db.
--   - No destructive statements on pre-existing tables.
-- ═════════════════════════════════════════════════════════════════════════

PRAGMA foreign_keys = ON;

-- ── 1. class_offerings ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS class_offerings (
  offering_id        TEXT PRIMARY KEY,           -- e.g. 'cogs160sp26'
  title              TEXT NOT NULL,
  quarter            TEXT NOT NULL,              -- 'Spring 2026' etc.
  instructor_user_id TEXT    NOT NULL REFERENCES users(user_id),
  starts_on          DATE NOT NULL,
  ends_on            DATE NOT NULL,
  status             TEXT NOT NULL DEFAULT 'active'
                       CHECK(status IN ('active','completed','archived')),
  total_points       INTEGER NOT NULL DEFAULT 100,
  created_at         TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ── 2. enrollments ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS enrollments (
  enrollment_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id            TEXT    NOT NULL REFERENCES users(user_id),
  offering_id        TEXT    NOT NULL REFERENCES class_offerings(offering_id),
  role               TEXT    NOT NULL DEFAULT 'student'
                       CHECK(role IN ('student','ta','auditor','track_lead','instructor')),
  track              TEXT    CHECK(track IN ('t1','t2','t3','t4') OR track IS NULL),
  f160_track         TEXT    CHECK(f160_track IN ('docs','site_pr','transfer','scaffolding') OR f160_track IS NULL),
  partner_user_id    TEXT    REFERENCES users(user_id),  -- T1.c pairs, T4.e
  status             TEXT    NOT NULL DEFAULT 'active'
                       CHECK(status IN ('active','dropped','at_risk','pending')),
  enrolled_at        TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_sign_in_at    TEXT,
  UNIQUE(user_id, offering_id)
);
CREATE INDEX IF NOT EXISTS ix_enrollments_offering ON enrollments(offering_id);
CREATE INDEX IF NOT EXISTS ix_enrollments_user     ON enrollments(user_id);

-- ── 3. deliverables ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS deliverables (
  deliverable_id     TEXT    NOT NULL,            -- 'A0', 'T1.b', 'F160'
  offering_id        TEXT    NOT NULL REFERENCES class_offerings(offering_id),
  track              TEXT    NOT NULL
                       CHECK(track IN ('common','t1','t2','t3','t4','f160')),
  title              TEXT    NOT NULL,
  hardness           TEXT    CHECK(hardness IN ('easy','medium','medium-hard','hard')),
  points             INTEGER NOT NULL,
  timeliness_bonus   INTEGER NOT NULL DEFAULT 0,
  span_start         DATE    NOT NULL,
  span_end           DATE    NOT NULL,
  rubric_path        TEXT    NOT NULL,            -- repo-relative
  spec_yaml          TEXT    NOT NULL DEFAULT '', -- machine-readable spec
  status             TEXT    NOT NULL DEFAULT 'active'
                       CHECK(status IN ('active','revised','retired')),
  PRIMARY KEY (offering_id, deliverable_id)
);

-- ── 4. submissions ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS submissions (
  submission_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id            TEXT    NOT NULL REFERENCES users(user_id),
  offering_id        TEXT    NOT NULL REFERENCES class_offerings(offering_id),
  deliverable_id     TEXT    NOT NULL,
  artefact_type      TEXT    NOT NULL
                       CHECK(artefact_type IN (
                         'registry_rows','tag_rows','git_commit','prose_doc',
                         'media','survey_csv','wireframe','build','pdf','other')),
  artefact_ref       TEXT    NOT NULL,      -- URL, path, DOI, SHA, or JSON array
  word_count         INTEGER,
  row_count          INTEGER,
  submitted_at       TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_late            INTEGER NOT NULL DEFAULT 0 CHECK(is_late IN (0,1)),
  days_late          INTEGER NOT NULL DEFAULT 0,
  revision_of        INTEGER REFERENCES submissions(submission_id),
  FOREIGN KEY (offering_id, deliverable_id)
    REFERENCES deliverables(offering_id, deliverable_id)
);
CREATE INDEX IF NOT EXISTS ix_subs_user_deliv
  ON submissions(user_id, deliverable_id, offering_id);
CREATE INDEX IF NOT EXISTS ix_subs_offering
  ON submissions(offering_id, submitted_at);

-- ── 5. grade_dossiers ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS grade_dossiers (
  dossier_id         INTEGER PRIMARY KEY AUTOINCREMENT,
  submission_id      INTEGER REFERENCES submissions(submission_id),   -- may be NULL if
                                                                       -- deliverable has no
                                                                       -- discrete submission row
  user_id            TEXT    NOT NULL REFERENCES users(user_id),
  offering_id        TEXT    NOT NULL REFERENCES class_offerings(offering_id),
  deliverable_id     TEXT    NOT NULL,
  completeness_raw   INTEGER NOT NULL CHECK(completeness_raw BETWEEN 0 AND 3),
  quality_raw        INTEGER NOT NULL CHECK(quality_raw BETWEEN 0 AND 3),
  reflection_raw     INTEGER NOT NULL CHECK(reflection_raw BETWEEN 0 AND 3),
  timeliness_bonus   INTEGER NOT NULL DEFAULT 0,
  late_penalty       INTEGER NOT NULL DEFAULT 0,    -- negative or zero
  points_awarded     INTEGER NOT NULL,
  confidence         TEXT    NOT NULL
                       CHECK(confidence IN ('high','medium','low')),
  dossier_markdown   TEXT    NOT NULL,              -- full dossier body
  grader_model       TEXT    NOT NULL,              -- 'claude-opus-4-6' etc.
  graded_at          TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_final           INTEGER NOT NULL DEFAULT 1 CHECK(is_final IN (0,1)),
  rubric_hash        TEXT    NOT NULL,              -- sha256 of rubric at grading
  flags_json         TEXT    NOT NULL DEFAULT '[]', -- JSON array of flag strings
  adjusted_by        TEXT    REFERENCES users(user_id),  -- instructor override
  adjustment_reason  TEXT,
  FOREIGN KEY (offering_id, deliverable_id)
    REFERENCES deliverables(offering_id, deliverable_id)
);
CREATE INDEX IF NOT EXISTS ix_dossiers_user_deliv
  ON grade_dossiers(user_id, deliverable_id, graded_at);
CREATE INDEX IF NOT EXISTS ix_dossiers_offering
  ON grade_dossiers(offering_id, is_final);

-- Data-model invariant: at most one final dossier per (user, offering,
-- deliverable). A re-grade or instructor adjustment flips the previous
-- is_final=1 row to is_final=0 before inserting the new final row;
-- historical dossiers are preserved. This partial unique index
-- enforces the invariant at the schema level so student_totals_v
-- cannot double-count even if application code has a bug.
-- (Fix for Codex P1#1, 2026-04-18.)
CREATE UNIQUE INDEX IF NOT EXISTS ux_dossiers_one_final_per_user_deliv
  ON grade_dossiers(user_id, offering_id, deliverable_id)
  WHERE is_final = 1;

-- ── 6. calibration_runs ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS calibration_runs (
  calibration_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  offering_id        TEXT    NOT NULL REFERENCES class_offerings(offering_id),
  deliverable_id     TEXT    NOT NULL,
  run_at             TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  n                  INTEGER NOT NULL,
  kappa_completeness REAL    NOT NULL,
  kappa_quality      REAL    NOT NULL,
  kappa_reflection   REAL    NOT NULL,
  pass_completeness  INTEGER NOT NULL DEFAULT 0 CHECK(pass_completeness IN (0,1)),
  pass_quality       INTEGER NOT NULL DEFAULT 0 CHECK(pass_quality      IN (0,1)),
  pass_reflection    INTEGER NOT NULL DEFAULT 0 CHECK(pass_reflection   IN (0,1)),
  reason             TEXT,
  grader_model       TEXT    NOT NULL,
  FOREIGN KEY (offering_id, deliverable_id)
    REFERENCES deliverables(offering_id, deliverable_id)
);
CREATE INDEX IF NOT EXISTS ix_calib_deliv
  ON calibration_runs(offering_id, deliverable_id, run_at DESC);

-- ── 7. audit_samples ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_samples (
  audit_id           INTEGER PRIMARY KEY AUTOINCREMENT,
  dossier_id         INTEGER NOT NULL REFERENCES grade_dossiers(dossier_id),
  assigned_to_ta     TEXT    NOT NULL REFERENCES users(user_id),
  stratum            TEXT    NOT NULL
                       CHECK(stratum IN (
                         'low_confidence','band_boundary','random','flagged_deliverable')),
  pulled_at          TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  due_by             TEXT    NOT NULL,
  ta_completeness    INTEGER CHECK(ta_completeness BETWEEN 0 AND 3),
  ta_quality         INTEGER CHECK(ta_quality      BETWEEN 0 AND 3),
  ta_reflection      INTEGER CHECK(ta_reflection   BETWEEN 0 AND 3),
  ta_notes           TEXT,
  completed_at       TEXT
);
CREATE INDEX IF NOT EXISTS ix_audit_due ON audit_samples(due_by);

-- ── 8. appeals ───────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS appeals (
  appeal_id          INTEGER PRIMARY KEY AUTOINCREMENT,
  dossier_id         INTEGER NOT NULL REFERENCES grade_dossiers(dossier_id),
  user_id            TEXT    NOT NULL REFERENCES users(user_id),
  criterion          TEXT    NOT NULL
                       CHECK(criterion IN ('completeness','quality','reflection')),
  original_band      INTEGER NOT NULL CHECK(original_band BETWEEN 0 AND 3),
  student_asks_band  INTEGER NOT NULL CHECK(student_asks_band BETWEEN 0 AND 3),
  reason             TEXT    NOT NULL,
  stage              TEXT    NOT NULL DEFAULT 'opened'
                       CHECK(stage IN ('opened','2nd_ai_grading','human_adjudication','resolved')),
  opened_at          TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  second_dossier_id  INTEGER REFERENCES grade_dossiers(dossier_id),
  adjudicator_id     TEXT    REFERENCES users(user_id),
  final_band         INTEGER CHECK(final_band BETWEEN 0 AND 3 OR final_band IS NULL),
  resolved_at        TEXT
);
CREATE INDEX IF NOT EXISTS ix_appeals_open ON appeals(stage) WHERE stage != 'resolved';

-- ── 9. announcements ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS announcements (
  announcement_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  offering_id        TEXT    NOT NULL REFERENCES class_offerings(offering_id),
  sender_user_id     TEXT    NOT NULL REFERENCES users(user_id),
  audience           TEXT    NOT NULL
                       CHECK(audience IN ('all','t1','t2','t3','t4','ta','instructor_only')),
  subject            TEXT    NOT NULL,
  body               TEXT    NOT NULL,
  sent_at            TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  recipients_count   INTEGER NOT NULL DEFAULT 0
);

-- ── 10. audit_log_class ──────────────────────────────────────────────────
-- Class-scoped audit events; companion to the existing audit_log table.
CREATE TABLE IF NOT EXISTS audit_log_class (
  log_id             INTEGER PRIMARY KEY AUTOINCREMENT,
  offering_id        TEXT    NOT NULL REFERENCES class_offerings(offering_id),
  actor_user_id      TEXT    REFERENCES users(user_id),
  event_type         TEXT    NOT NULL,           -- 'grading.pass', 'grade.viewed', etc.
  target             TEXT,                       -- student id, deliverable id, or 'all'
  detail             TEXT,
  occurred_at        TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_audit_log_class_offering
  ON audit_log_class(offering_id, occurred_at DESC);

-- ── student_totals_v (view) ──────────────────────────────────────────────
-- Per-student per-offering totals. Drop and recreate to ensure the
-- definition is current on re-run.
--
-- Defensive against dossier over-count (Codex P1#1 fix, 2026-04-18):
-- uses a CTE to select exactly ONE dossier per (user, offering,
-- deliverable) triple — the one with the maximum graded_at. The
-- ux_dossiers_one_final_per_user_deliv partial unique index already
-- enforces this invariant at insert time; the CTE is belt-and-braces
-- so totals remain correct even if the index is ever dropped.
DROP VIEW IF EXISTS student_totals_v;
CREATE VIEW student_totals_v AS
WITH latest_final_dossier AS (
  SELECT gd.*
  FROM grade_dossiers gd
  WHERE gd.is_final = 1
    AND gd.graded_at = (
      SELECT MAX(gd2.graded_at)
      FROM grade_dossiers gd2
      WHERE gd2.user_id       = gd.user_id
        AND gd2.offering_id   = gd.offering_id
        AND gd2.deliverable_id = gd.deliverable_id
        AND gd2.is_final = 1
    )
)
SELECT
  e.offering_id,
  e.user_id,
  (u.first_name || ' ' || u.last_name)               AS name,
  u.email,
  e.track,
  e.f160_track,
  COALESCE(SUM(CASE WHEN d.deliverable_id = 'A0'
                    THEN ld.points_awarded END), 0)  AS a0_pts,
  COALESCE(SUM(CASE WHEN d.deliverable_id = 'A1'
                    THEN ld.points_awarded END), 0)  AS a1_pts,
  COALESCE(SUM(CASE WHEN d.track = e.track
                    THEN ld.points_awarded END), 0)  AS track_pts,
  COALESCE(SUM(CASE WHEN d.deliverable_id = 'F160'
                    THEN ld.points_awarded END), 0)  AS f160_pts,
  COALESCE(SUM(ld.points_awarded), 0)                AS total_pts,
  MAX(ld.graded_at)                                  AS last_graded_at
FROM enrollments e
JOIN users u ON u.user_id = e.user_id
LEFT JOIN latest_final_dossier ld
       ON ld.user_id     = e.user_id
      AND ld.offering_id = e.offering_id
LEFT JOIN deliverables d
       ON d.deliverable_id = ld.deliverable_id
      AND d.offering_id    = ld.offering_id
WHERE e.role = 'student' AND e.status != 'dropped'
GROUP BY e.offering_id, e.user_id;

-- ═════════════════════════════════════════════════════════════════════════
-- End of migration.
-- To rollback:
--   DROP VIEW student_totals_v;
--   DROP TABLE audit_log_class;
--   DROP TABLE announcements;
--   DROP TABLE appeals;
--   DROP TABLE audit_samples;
--   DROP TABLE calibration_runs;
--   DROP TABLE grade_dossiers;
--   DROP TABLE submissions;
--   DROP TABLE deliverables;
--   DROP TABLE enrollments;
--   DROP TABLE class_offerings;
-- ═════════════════════════════════════════════════════════════════════════
