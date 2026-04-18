#!/usr/bin/env python3
"""
Seed data/ka_auth.db with COGS 160 Spring 2026 class state.

Run this AFTER scripts/migrations/2026-04-17_class_state.sql has been
applied. It populates:

  class_offerings   — one row, 'cogs160sp26'
  deliverables      — 31 rows (A0, A1, 7×T1, 7×T2, 7×T3, 7×T4, F160),
                      reading rubric paths + YAML specs from disk
  enrollments       — 15 demo students if users table has them,
                      otherwise creates the users first

Usage
-----
    # Dry-run: print what would be inserted, don't touch DB
    python3 scripts/seed_class_state.py --dry-run

    # Apply to default DB
    python3 scripts/seed_class_state.py

    # Target a different DB file
    python3 scripts/seed_class_state.py --db /tmp/ka_auth_test.db

The script is idempotent: running it twice against the same DB is safe.
Existing rows are left alone; missing rows are inserted.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sqlite3
import sys
from datetime import date
from pathlib import Path
from typing import Optional

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO / "data" / "ka_auth.db"
RUBRICS = REPO / "160sp" / "rubrics"

OFFERING = {
    "offering_id": "cogs160sp26",
    "title": "COGS 160 — Spring 2026 (Knowledge Atlas Sprint)",
    "quarter": "Spring 2026",
    "starts_on": "2026-04-06",
    "ends_on": "2026-06-15",
    "total_points": 100,
}

# Mirrors scripts/ai_grader.py DELIVERABLES — keep in sync.
#   deliverable_id, track, title, hardness, points, span_start, span_end, rubric_rel
DELIVERABLES = [
    ("A0",   "common", "Orientation + first articles",            "easy",        5,  "2026-04-06", "2026-04-20", "common/a0.md"),
    ("A1",   "common", "Schema study + second batch + reflection", "medium",     5,  "2026-04-13", "2026-04-27", "common/a1.md"),
    ("T1.a", "t1",     "Tag-schema study + 20 tagged images",     "easy",        5,  "2026-04-27", "2026-05-04", "t1/T1.a_schema_study.md"),
    ("T1.b", "t1",     "Tag 100 images against full schema",      "medium",     10,  "2026-04-27", "2026-05-11", "t1/T1.b_tag_100.md"),
    ("T1.c", "t1",     "Inter-rater kappa >= 0.7",                "medium-hard",10,  "2026-05-04", "2026-05-11", "t1/T1.c_interrater_kappa.md"),
    ("T1.d", "t1",     "HITL on 50 confusing cases",              "medium",     10,  "2026-05-04", "2026-05-18", "t1/T1.d_hitl_validation.md"),
    ("T1.e", "t1",     "Classifier + error analysis",             "hard",       15,  "2026-05-11", "2026-05-25", "t1/T1.e_classifier.md"),
    ("T1.f", "t1",     "Published tag set (500 images)",          "hard",       15,  "2026-05-18", "2026-06-01", "t1/T1.f_published_500.md"),
    ("T1.g", "t1",     "Final report + reflection",               "medium",     10,  "2026-06-01", "2026-06-15", "t1/T1.g_final_report.md"),
    ("T2.a", "t2",     "Pipeline onboarding + 15 articles",       "easy",        5,  "2026-04-27", "2026-05-04", "t2/T2.a_onboarding.md"),
    ("T2.b", "t2",     "Weekly 20-article batches (x 3)",         "medium",     15,  "2026-04-27", "2026-05-18", "t2/T2.b_weekly_batches.md"),
    ("T2.c", "t2",     "VOI-banding calibration",                 "medium-hard",10,  "2026-05-11", "2026-05-18", "t2/T2.c_voi_calibration.md"),
    ("T2.d", "t2",     "50-article topical sweep",                "hard",       15,  "2026-05-11", "2026-05-25", "t2/T2.d_topical_sweep.md"),
    ("T2.e", "t2",     "Near-miss triage (30 cases)",             "medium",     10,  "2026-05-18", "2026-05-25", "t2/T2.e_near_miss_triage.md"),
    ("T2.f", "t2",     "150-article cumulative + coverage audit", "hard",       15,  "2026-06-01", "2026-06-15", "t2/T2.f_cumulative_150.md"),
    ("T2.g", "t2",     "Final report",                            "easy",        5,  "2026-06-08", "2026-06-15", "t2/T2.g_final_report.md"),
    ("T3.a", "t3",     "Unity hello-scene",                       "easy",        5,  "2026-04-27", "2026-05-04", "t3/T3.a_hello_scene.md"),
    ("T3.b", "t3",     "First interactive scene",                 "medium",     10,  "2026-04-27", "2026-05-11", "t3/T3.b_first_scene.md"),
    ("T3.c", "t3",     "Second scene + component library",        "medium-hard",12,  "2026-05-04", "2026-05-18", "t3/T3.c_second_scene.md"),
    ("T3.d", "t3",     "Performance: 72 Hz on target",            "hard",       10,  "2026-05-11", "2026-05-18", "t3/T3.d_performance.md"),
    ("T3.e", "t3",     "User-study pilot (n=3)",                  "hard",       15,  "2026-05-18", "2026-06-01", "t3/T3.e_user_pilot.md"),
    ("T3.f", "t3",     "Polish + Fall handoff",                   "medium-hard",13,  "2026-06-01", "2026-06-15", "t3/T3.f_polish.md"),
    ("T3.g", "t3",     "Final demo",                              "easy",       10,  "2026-06-08", "2026-06-15", "t3/T3.g_final_demo.md"),
    ("T4.a", "t4",     "Heuristic audit (10 findings)",           "medium",     12,  "2026-04-27", "2026-05-11", "t4/T4.a_heuristic_audit.md"),
    ("T4.b", "t4",     "Scenario walkthroughs (3 roles)",         "medium",     10,  "2026-05-04", "2026-05-11", "t4/T4.b_scenarios.md"),
    ("T4.c", "t4",     "Moderated usability pilot (n=5)",         "hard",       15,  "2026-05-11", "2026-05-25", "t4/T4.c_usability_pilot.md"),
    ("T4.d", "t4",     "Severity rubric + prioritised backlog",   "medium-hard",10,  "2026-05-18", "2026-05-25", "t4/T4.d_severity_backlog.md"),
    ("T4.e", "t4",     "Reproducibility check (5 findings)",      "hard",       13,  "2026-05-25", "2026-06-01", "t4/T4.e_reproducibility.md"),
    ("T4.f", "t4",     "Redesign proposal",                       "medium",     10,  "2026-06-01", "2026-06-15", "t4/T4.f_redesign.md"),
    ("T4.g", "t4",     "Final report",                            "easy",        5,  "2026-06-08", "2026-06-15", "t4/T4.g_final_report.md"),
    ("F160", "f160",   "Work on 160F (Fall-2026 contribution)",   "medium",     15,  "2026-05-11", "2026-06-15", "f160/README.md"),
]

# Demo roster — 15 students, matches scripts/ai_grader.py DEMO_ROSTER.
# first_name, last_name, email, track, f160_track
DEMO_ROSTER = [
    ("Aisha",   "Rahman",      "arahman@ucsd.edu",   "t1", "docs"),
    ("Ben",     "Choi",        "bchoi@ucsd.edu",     "t1", "site_pr"),
    ("Carla",   "Mendoza",     "cmendoza@ucsd.edu",  "t1", "transfer"),
    ("Derek",   "O'Neill",     "doneill@ucsd.edu",   "t2", "scaffolding"),
    ("Elena",   "Petrov",      "epetrov@ucsd.edu",   "t2", "docs"),
    ("Farid",   "Al-Hassan",   "falhassan@ucsd.edu", "t2", "site_pr"),
    ("Grace",   "Nakamura",    "gnakamura@ucsd.edu", "t3", "docs"),
    ("Hiro",    "Tanaka",      "htanaka@ucsd.edu",   "t3", "scaffolding"),
    ("Isabela", "Santos",      "isantos@ucsd.edu",   "t3", "transfer"),
    ("James",   "Park",        "jpark@ucsd.edu",     "t4", "docs"),
    ("Kira",    "Volkov",      "kvolkov@ucsd.edu",   "t4", "site_pr"),
    ("Liam",    "McCarthy",    "lmccarthy@ucsd.edu", "t4", "scaffolding"),
    ("Maya",    "Johnson",     "mjohnson@ucsd.edu",  "t1", "docs"),
    ("Nikhil",  "Patel",       "npatel@ucsd.edu",    "t2", "transfer"),
    ("Olivia",  "Sullivan",    "osullivan@ucsd.edu", "t3", "docs"),
]


def read_spec_yaml(rel_path: str) -> str:
    """Extract the ```yaml … ``` block after 'Machine-readable spec' if any."""
    p = RUBRICS / rel_path
    if not p.exists():
        return ""
    m = re.search(
        r"## Machine-readable spec\s*```yaml\s*(.*?)\s*```",
        p.read_text(), re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def _new_user_id(email: str) -> str:
    """Generate a TEXT user_id matching the existing 'u_{16-hex}' convention."""
    h = hashlib.sha256(email.encode("utf-8")).hexdigest()[:16]
    return f"u_{h}"


def ensure_user(c: sqlite3.Cursor, first: str, last: str, email: str) -> str:
    """Look up user by email; insert if absent. Returns user_id (TEXT)."""
    row = c.execute(
        "SELECT user_id FROM users WHERE email = ?", (email,)).fetchone()
    if row:
        return row[0]
    # The existing users table shape may vary. Insert the minimum columns
    # that exist in the schema; skip unknown columns.
    cols = [r[1] for r in c.execute("PRAGMA table_info(users)").fetchall()]
    values: dict[str, str] = {
        "user_id": _new_user_id(email),
        "email": email,
        "first_name": first,
        "last_name": last,
    }
    if "password_hash" in cols:
        values["password_hash"] = "pending_dk_set"
    if "status" in cols:
        values["status"] = "pending"
    if "role" in cols:
        values["role"] = "student"
    if "created_at" in cols:
        values["created_at"] = date.today().isoformat()
    if "institution" in cols:
        values["institution"] = "UC San Diego"
    present = [k for k in values if k in cols]
    placeholders = ",".join("?" for _ in present)
    cols_sql = ",".join(present)
    c.execute(
        f"INSERT INTO users ({cols_sql}) VALUES ({placeholders})",
        tuple(values[k] for k in present))
    return values["user_id"]


def seed_offering(c: sqlite3.Cursor, instructor_uid: int) -> None:
    row = c.execute(
        "SELECT 1 FROM class_offerings WHERE offering_id = ?",
        (OFFERING["offering_id"],)).fetchone()
    if row:
        print(f"  class_offerings[{OFFERING['offering_id']}]: already present")
        return
    c.execute(
        """INSERT INTO class_offerings
           (offering_id, title, quarter, instructor_user_id,
            starts_on, ends_on, total_points)
           VALUES (?,?,?,?,?,?,?)""",
        (OFFERING["offering_id"], OFFERING["title"], OFFERING["quarter"],
         instructor_uid, OFFERING["starts_on"], OFFERING["ends_on"],
         OFFERING["total_points"]))
    print(f"  class_offerings[{OFFERING['offering_id']}]: inserted")


def seed_deliverables(c: sqlite3.Cursor) -> int:
    n_inserted = 0
    for d in DELIVERABLES:
        (did, track, title, hardness, points, span_start, span_end, rel) = d
        row = c.execute(
            "SELECT 1 FROM deliverables WHERE offering_id = ? AND deliverable_id = ?",
            (OFFERING["offering_id"], did)).fetchone()
        if row:
            continue
        spec = read_spec_yaml(rel)
        c.execute(
            """INSERT INTO deliverables
               (deliverable_id, offering_id, track, title, hardness, points,
                timeliness_bonus, span_start, span_end, rubric_path, spec_yaml)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (did, OFFERING["offering_id"], track, title, hardness, points,
             1 if points >= 10 else 0,
             span_start, span_end,
             f"160sp/rubrics/{rel}", spec))
        n_inserted += 1
    return n_inserted


def seed_enrollments(c: sqlite3.Cursor) -> tuple[int, int]:
    n_new_users = 0
    n_new_enrolls = 0
    for (first, last, email, track, f160) in DEMO_ROSTER:
        before = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        uid = ensure_user(c, first, last, email)
        if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] > before:
            n_new_users += 1
        row = c.execute(
            "SELECT 1 FROM enrollments WHERE user_id = ? AND offering_id = ?",
            (uid, OFFERING["offering_id"])).fetchone()
        if row:
            continue
        c.execute(
            """INSERT INTO enrollments
               (user_id, offering_id, role, track, f160_track, status)
               VALUES (?,?,?,?,?,?)""",
            (uid, OFFERING["offering_id"], "student", track, f160, "active"))
        n_new_enrolls += 1
    return n_new_users, n_new_enrolls


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB,
                    help="SQLite DB path (default: data/ka_auth.db)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Roll back the transaction instead of committing")
    ap.add_argument("--instructor-email", default="dkirsh@ucsd.edu",
                    help="Instructor email (row in users); created if missing")
    args = ap.parse_args()

    if not args.db.exists():
        print(f"error: DB not found at {args.db}", file=sys.stderr)
        sys.exit(1)

    con = sqlite3.connect(str(args.db))
    con.execute("PRAGMA foreign_keys = ON")
    c = con.cursor()

    # Confirm migration has been applied
    need = ("class_offerings", "enrollments", "deliverables",
            "grade_dossiers", "student_totals_v")
    have = {r[0] for r in c.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
    missing = [t for t in need if t not in have]
    if missing:
        print(f"error: migration not applied. Missing: {missing}", file=sys.stderr)
        print("       Run: python3 scripts/migrations/apply.py "
              "(or apply the .sql file via sqlite CLI)", file=sys.stderr)
        sys.exit(2)

    print(f"Seeding {args.db} {'(DRY RUN)' if args.dry_run else ''}")
    print()

    # 1. Instructor user (must exist before class_offerings FK points at them)
    print("Instructor:")
    instr_uid = ensure_user(c, "David", "Kirsh", args.instructor_email)
    print(f"  users[{args.instructor_email}]: user_id = {instr_uid}")
    print()

    # 2. class_offerings
    print("class_offerings:")
    seed_offering(c, instr_uid)
    print()

    # 3. deliverables
    print("deliverables:")
    n_deliv = seed_deliverables(c)
    total_deliv = c.execute(
        "SELECT COUNT(*) FROM deliverables WHERE offering_id = ?",
        (OFFERING["offering_id"],)).fetchone()[0]
    print(f"  inserted {n_deliv} new, {total_deliv} total for this offering")
    print()

    # 4. enrollments (creates demo users if absent)
    print("enrollments (+ demo users):")
    n_users, n_enrolls = seed_enrollments(c)
    total_enrolls = c.execute(
        "SELECT COUNT(*) FROM enrollments WHERE offering_id = ?",
        (OFFERING["offering_id"],)).fetchone()[0]
    print(f"  created {n_users} new users, inserted {n_enrolls} new "
          f"enrollments; {total_enrolls} total for this offering")
    print()

    if args.dry_run:
        con.rollback()
        print("Dry run — transaction rolled back.")
    else:
        con.commit()
        print("Committed.")
    con.close()


if __name__ == "__main__":
    main()
