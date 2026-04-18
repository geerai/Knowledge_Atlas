#!/usr/bin/env python3
"""
Export final grades to UCSD eGrades CSV format.

Usage
-----
    # Dry-run preview
    python3 scripts/export_egrades.py --offering cogs160sp26 --dry-run

    # Real export
    python3 scripts/export_egrades.py --offering cogs160sp26 \
        --out /Volumes/ka-backup-5T/exports/cogs160sp26_egrades.csv

    # Export with letter-grade mapping (otherwise numeric only)
    python3 scripts/export_egrades.py --offering cogs160sp26 \
        --letter-grades --out ...

What eGrades wants
------------------
The UCSD Registrar's eGrades CSV uploader expects the following columns
(per the 2025-26 Registrar's instructor upload guide; DK to verify the
format exactly before the first real submission):

    StudentID, Name, Grade, [Incomplete_Default_Grade]

where:
  - StudentID is the 9-digit PID (e.g. A12345678)
  - Name is "Last, First" (the Registrar's canonical form)
  - Grade is a UC letter grade (A+, A, A-, B+, ..., F, P, NP, I, W)
  - Incomplete_Default_Grade is the letter grade that replaces an 'I'
    if the incomplete is not cleared within the deadline (optional)

The CSV must be saved with UTF-8 encoding and Windows CRLF line endings;
the eGrades uploader rejects LF-only files.

Data sources
------------
Reads dossiers from 160sp/grading/{sid}/*.md and aggregates per-student
totals against the 100-point allocation (5 A0 + 5 A1 + 75 Track + 15 F160).
After the class-state DB migration lands (CLASS_STATE_DATABASE_DESIGN §4)
this will be replaced by a single query against student_totals_v.

Default UCSD letter-grade scale (UCSD Academic Senate regulation 500):
  A+ 97–100, A 93–96, A- 90–92, B+ 87–89, B 83–86, B- 80–82,
  C+ 77–79, C 73–76, C- 70–72, D+ 67–69, D 63–66, D- 60–62, F <60
Cutoffs are customisable via --cutoffs cutoffs.json.

Retention
---------
eGrades exports are the canonical end-of-quarter artefact. Every export
must be:
  1. Saved to the 5T backup disk at /Volumes/ka-backup-5T/exports/
     (or the configured --out path).
  2. Committed-in-place to the git repo under 160sp/grading/archive/
     {offering_id}_egrades_{YYYY-MM-DD}.csv.
  3. Logged in 160sp/grading/archive/EXPORT_LOG.md with a one-line entry.

Retention period: per UC records schedule (five years minimum) and UCSD
Academic Senate Regulation 500. Hard deletion happens on July 1 of the
fifth year after the quarter's end. The 5T disk is the primary retention
medium; the git repo provides a second redundant copy for the most
recent three quarters.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GRADING = REPO / "160sp" / "grading"
ARCHIVE = GRADING / "archive"

# Mirrors DELIVERABLES in scripts/ai_grader.py. Keep in sync manually
# until the class-state DB is authoritative.
DELIVERABLE_POINTS = {
    "A0": 5, "A1": 5,
    "T1.a": 5, "T1.b": 10, "T1.c": 10, "T1.d": 10, "T1.e": 15, "T1.f": 15, "T1.g": 10,
    "T2.a": 5, "T2.b": 15, "T2.c": 10, "T2.d": 15, "T2.e": 10, "T2.f": 15, "T2.g": 5,
    "T3.a": 5, "T3.b": 10, "T3.c": 12, "T3.d": 10, "T3.e": 15, "T3.f": 13, "T3.g": 10,
    "T4.a": 12, "T4.b": 10, "T4.c": 15, "T4.d": 10, "T4.e": 13, "T4.f": 10, "T4.g": 5,
    "F160": 15,
}

DELIVERABLE_TRACK = {
    "A0": "common", "A1": "common", "F160": "f160",
    **{f"T1.{x}": "t1" for x in "abcdefg"},
    **{f"T2.{x}": "t2" for x in "abcdefg"},
    **{f"T3.{x}": "t3" for x in "abcdefg"},
    **{f"T4.{x}": "t4" for x in "abcdefg"},
}

DEFAULT_CUTOFFS = [
    (97, "A+"), (93, "A"), (90, "A-"),
    (87, "B+"), (83, "B"), (80, "B-"),
    (77, "C+"), (73, "C"), (70, "C-"),
    (67, "D+"), (63, "D"), (60, "D-"),
    (0,  "F"),
]

# Demo roster (same source as ai_grader.py DEMO_ROSTER).
# PID column is a placeholder; DK populates the real PIDs before export.
# Real export uses the class-state DB once it's populated.
DEMO_STUDENTS = [
    ("s01", "Rahman, Aisha",      "A00000001", "t1"),
    ("s02", "Choi, Ben",          "A00000002", "t1"),
    ("s03", "Mendoza, Carla",     "A00000003", "t1"),
    ("s04", "O'Neill, Derek",     "A00000004", "t2"),
    ("s05", "Petrov, Elena",      "A00000005", "t2"),
    ("s06", "Al-Hassan, Farid",   "A00000006", "t2"),
    ("s07", "Nakamura, Grace",    "A00000007", "t3"),
    ("s08", "Tanaka, Hiro",       "A00000008", "t3"),
    ("s09", "Santos, Isabela",    "A00000009", "t3"),
    ("s10", "Park, James",        "A00000010", "t4"),
    ("s11", "Volkov, Kira",       "A00000011", "t4"),
    ("s12", "McCarthy, Liam",     "A00000012", "t4"),
    ("s13", "Johnson, Maya",      "A00000013", "t1"),
    ("s14", "Patel, Nikhil",      "A00000014", "t2"),
    ("s15", "Sullivan, Olivia",   "A00000015", "t3"),
]


@dataclass
class StudentTotal:
    sid: str
    name: str
    pid: str
    track: str
    a0_pts: int = 0
    a1_pts: int = 0
    track_pts: int = 0
    f160_pts: int = 0

    @property
    def total(self) -> int:
        return self.a0_pts + self.a1_pts + self.track_pts + self.f160_pts


# ─── Dossier reader ───────────────────────────────────────────────
POINTS_AWARDED_RE = re.compile(
    r"^\s*-?\s*\*?\*?points[_\s]awarded\*?\*?\s*[:=]\s*(\d+)",
    re.IGNORECASE | re.MULTILINE)

POINTS_TOTAL_LINE_RE = re.compile(
    r"points[_\s]awarded[^\d]*(\d+)\s*/\s*\d+", re.IGNORECASE)


def parse_dossier(path: Path) -> int | None:
    """Return points awarded in a dossier, or None if unreadable."""
    try:
        md = path.read_text()
    except OSError:
        return None
    for rx in (POINTS_AWARDED_RE, POINTS_TOTAL_LINE_RE):
        m = rx.search(md)
        if m:
            return int(m.group(1))
    return None


def load_totals(student: tuple) -> StudentTotal:
    sid, name, pid, track = student
    st = StudentTotal(sid=sid, name=name, pid=pid, track=track)
    sdir = GRADING / sid
    if not sdir.exists():
        return st
    for deliv, pts in DELIVERABLE_POINTS.items():
        # Skip other-track deliverables
        dtrack = DELIVERABLE_TRACK[deliv]
        if dtrack not in ("common", "f160") and dtrack != track:
            continue
        # Most recent dossier wins
        candidates = sorted(sdir.glob(f"{deliv}_*.md"))
        if not candidates:
            continue
        awarded = parse_dossier(candidates[-1])
        if awarded is None:
            continue
        awarded = max(0, min(awarded, pts))
        if deliv == "A0":
            st.a0_pts = awarded
        elif deliv == "A1":
            st.a1_pts = awarded
        elif deliv == "F160":
            st.f160_pts = awarded
        else:
            st.track_pts += awarded
    return st


# ─── Letter-grade mapping ─────────────────────────────────────────
def letter_for(score: int, cutoffs) -> str:
    for cut, letter in cutoffs:
        if score >= cut:
            return letter
    return "F"


def load_cutoffs(path: Path | None):
    if path is None:
        return DEFAULT_CUTOFFS
    data = json.loads(path.read_text())
    return sorted(data, key=lambda r: -r[0])


# ─── CSV writer ───────────────────────────────────────────────────
def write_egrades_csv(totals: list[StudentTotal],
                      out_path: Path,
                      use_letters: bool,
                      cutoffs,
                      incomplete_default: str = "F") -> None:
    """Write the eGrades-compliant CSV (UTF-8, CRLF)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="\r\n", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\r\n")
        writer.writerow(["StudentID", "Name", "Grade", "Incomplete_Default_Grade"])
        for t in totals:
            grade = letter_for(t.total, cutoffs) if use_letters else str(t.total)
            writer.writerow([t.pid, t.name, grade, incomplete_default])


# ─── CLI ───────────────────────────────────────────────────────────
def main() -> None:
    p = argparse.ArgumentParser(description="Export final grades to eGrades CSV",
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog=__doc__)
    p.add_argument("--offering", required=True,
                   help="Offering id (e.g. 'cogs160sp26')")
    p.add_argument("--out", type=Path,
                   help="Output CSV path. If omitted, writes to "
                        "160sp/grading/archive/{offering}_egrades_{date}.csv")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the table to stdout instead of writing the CSV")
    p.add_argument("--letter-grades", action="store_true",
                   help="Emit UC letter grades instead of numeric totals")
    p.add_argument("--cutoffs", type=Path,
                   help="JSON file with custom cutoffs "
                        "(list of [min_score, letter] pairs)")
    p.add_argument("--incomplete-default", default="F",
                   help="Incomplete default grade (default F)")
    args = p.parse_args()

    cutoffs = load_cutoffs(args.cutoffs)
    totals = [load_totals(s) for s in DEMO_STUDENTS]
    # Sort by name (lastname, firstname convention)
    totals.sort(key=lambda t: t.name)

    if args.dry_run:
        print(f"{'SID':<5} {'PID':<10} {'Name':<25} {'Track':<6} "
              f"{'A0':>3} {'A1':>3} {'Track':>6} {'F160':>4} {'Total':>6} {'Grade':>5}")
        print("-" * 80)
        for t in totals:
            grade = letter_for(t.total, cutoffs) if args.letter_grades else str(t.total)
            print(f"{t.sid:<5} {t.pid:<10} {t.name:<25} {t.track:<6} "
                  f"{t.a0_pts:>3} {t.a1_pts:>3} {t.track_pts:>6} "
                  f"{t.f160_pts:>4} {t.total:>6} {grade:>5}")
        print(f"\n(dry-run — no CSV written; {len(totals)} students)")
        return

    out = args.out or (ARCHIVE / f"{args.offering}_egrades_{date.today().isoformat()}.csv")
    write_egrades_csv(totals, out, args.letter_grades, cutoffs, args.incomplete_default)
    print(f"Wrote {out} — {len(totals)} rows.")

    # Log the export
    log = ARCHIVE / "EXPORT_LOG.md"
    log.parent.mkdir(parents=True, exist_ok=True)
    line = (f"- {datetime.now().isoformat(timespec='seconds')} · "
            f"offering={args.offering} · rows={len(totals)} · "
            f"out={out.relative_to(REPO) if out.is_relative_to(REPO) else out}\n")
    if not log.exists():
        log.write_text("# eGrades export log\n\n")
    with log.open("a") as f:
        f.write(line)
    print(f"Logged to {log.relative_to(REPO)}.")


if __name__ == "__main__":
    main()
