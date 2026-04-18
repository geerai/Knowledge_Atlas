#!/usr/bin/env python3
"""
FastAPI backend for the class-state schema (CLASS_STATE_DATABASE_DESIGN
§3, §5). Serves /api/admin/class/* endpoints that back the Grading tab
in ka_admin.html.

Usage
-----
    # Dev: auto-reload, bound to localhost:8080
    uvicorn scripts.ka_class_api:app --reload --port 8080

    # Prod: single worker behind the existing Apache reverse proxy at
    # xrlab.ucsd.edu/api/admin/class/*
    uvicorn scripts.ka_class_api:app --host 127.0.0.1 --port 8080

Auth
----
Interim: every endpoint under /api/admin/class/* requires an
X-Admin-Token header matching the value stored in
/etc/ka/admin_token.txt (or env var KA_ADMIN_TOKEN). That file is
readable only by root; DK sets the token manually.

This is the interim gate documented in docs/SHIBBOLETH_INTERIM_NOTE_
2026-04-18.md. It replaces the demo "yes"-string gate on ka_admin.html.
When Shibboleth lands, this shim is replaced by a REMOTE_USER /
mod_shib header check.

Endpoints
---------
GET  /api/admin/class/roster           — per-student totals
GET  /api/admin/class/grading          — DEMO_GRADING shape, from DB
GET  /api/admin/class/calibration      — calibration_runs latest per deliverable
GET  /api/admin/class/audit/queue      — pending audit samples
GET  /api/admin/class/appeals          — open appeals
POST /api/admin/class/grading/run      — trigger ai_grader.py queue (shells out)
POST /api/admin/class/audit/pull       — pull new stratified audit sample
POST /api/admin/class/announcements    — record an announcement (send is separate)

Dependencies
------------
    pip3 install --break-system-packages fastapi uvicorn pydantic
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from fastapi import FastAPI, HTTPException, Header, Query, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "FastAPI dependencies not installed. Run:\n"
        "  pip3 install --break-system-packages fastapi uvicorn pydantic"
    ) from e


REPO = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("KA_AUTH_DB", REPO / "data" / "ka_auth.db"))
ADMIN_TOKEN_FILE = Path(os.environ.get(
    "KA_ADMIN_TOKEN_FILE", "/etc/ka/admin_token.txt"))
ADMIN_TOKEN_ENV = os.environ.get("KA_ADMIN_TOKEN")

# Default offering — Spring 2026. Endpoints accept ?offering_id=... to
# override; without it, the default offering is returned.
DEFAULT_OFFERING = "cogs160sp26"


# ─── Connection helper ─────────────────────────────────────────────
@contextmanager
def get_db():
    con = sqlite3.connect(str(DB_PATH))
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    try:
        yield con
    finally:
        con.close()


# ─── Auth ──────────────────────────────────────────────────────────
def _load_admin_token() -> Optional[str]:
    if ADMIN_TOKEN_ENV:
        return ADMIN_TOKEN_ENV
    if ADMIN_TOKEN_FILE.exists():
        return ADMIN_TOKEN_FILE.read_text().strip()
    return None


def require_admin(x_admin_token: str = Header(default="")) -> None:
    expected = _load_admin_token()
    if not expected:
        # Dev mode: no token configured. Log but allow. In production,
        # the token file MUST exist.
        if os.environ.get("KA_ADMIN_STRICT") == "1":
            raise HTTPException(503, "No admin token configured on server")
        return
    if x_admin_token != expected:
        raise HTTPException(401, "Invalid X-Admin-Token")


# ─── Pydantic models ───────────────────────────────────────────────
class ClassSummary(BaseModel):
    avg: float
    median: float
    hi: int
    lo: int
    dossier_count: int
    appeals_open: int
    last_pass: Optional[str]


class StudentRow(BaseModel):
    sid: str
    name: str
    track: Optional[str]
    a0: int
    a1: int
    track_sub: int
    f160: int
    total: int
    audit: str
    conf: str
    flag: Optional[str] = None


class GradingResponse(BaseModel):
    class_summary: ClassSummary
    students: list[StudentRow]


class CalibrationRow(BaseModel):
    id: str
    kc: float
    kq: float
    kr: float
    n: int
    ok: bool
    reason: Optional[str] = None


class AuditRow(BaseModel):
    sid: str
    deliv: str
    ai_score: str
    stratum: str
    due: str


class AppealRow(BaseModel):
    sid: str
    deliv: str
    criterion: str
    ai: int
    asks: int
    stage: str
    opened: str


class RunPassResponse(BaseModel):
    ok: bool
    queued: int
    note: str


# ─── App ───────────────────────────────────────────────────────────
app = FastAPI(title="KA Class-State API", version="0.1.0")

# CORS for local dev (admin page served from same origin in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000",
                   "https://xrlab.ucsd.edu"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/admin/class/health")
def health():
    """Unauthenticated health check — confirms DB is reachable and schema is in place."""
    with get_db() as con:
        try:
            n = con.execute("SELECT COUNT(*) FROM class_offerings").fetchone()[0]
            return {"ok": True, "db": str(DB_PATH), "offerings": n}
        except sqlite3.Error as e:
            return {"ok": False, "error": str(e)}


@app.get("/api/admin/class/roster", dependencies=[Depends(require_admin)])
def roster(offering_id: str = Query(default=DEFAULT_OFFERING)):
    """Per-student totals from student_totals_v."""
    with get_db() as con:
        rows = con.execute("""
            SELECT user_id, name, email, track, f160_track,
                   a0_pts, a1_pts, track_pts, f160_pts, total_pts,
                   last_graded_at
            FROM student_totals_v
            WHERE offering_id = ?
            ORDER BY name
        """, (offering_id,)).fetchall()
    return {"offering_id": offering_id,
            "students": [dict(r) for r in rows]}


@app.get("/api/admin/class/grading",
         response_model=GradingResponse,
         dependencies=[Depends(require_admin)])
def grading(offering_id: str = Query(default=DEFAULT_OFFERING)):
    """Grading-tab payload: class KPIs + per-student rows."""
    with get_db() as con:
        rows = con.execute("""
            SELECT user_id, name, track,
                   a0_pts, a1_pts, track_pts, f160_pts, total_pts,
                   last_graded_at
            FROM student_totals_v
            WHERE offering_id = ?
            ORDER BY name
        """, (offering_id,)).fetchall()
        dossier_count = con.execute(
            "SELECT COUNT(*) FROM grade_dossiers WHERE offering_id = ? AND is_final = 1",
            (offering_id,)).fetchone()[0]
        appeals_open = con.execute(
            "SELECT COUNT(*) FROM appeals WHERE stage != 'resolved'"
        ).fetchone()[0]
        last_pass_row = con.execute(
            "SELECT MAX(graded_at) FROM grade_dossiers WHERE offering_id = ?",
            (offering_id,)).fetchone()
        last_pass = last_pass_row[0] if last_pass_row else None

    # Compute class-summary stats on the total_pts column
    totals = [r["total_pts"] for r in rows if r["total_pts"] is not None]
    if totals:
        avg = sum(totals) / len(totals)
        s = sorted(totals)
        n = len(s)
        median = float(s[n // 2]) if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
        hi, lo = max(totals), min(totals)
    else:
        avg = median = 0.0
        hi = lo = 0

    # Confidence + audit columns: derived from latest dossier per student.
    # If not yet populated, return '—'.
    with get_db() as con:
        conf_by_user = {}
        audit_by_user = {}
        for r in con.execute("""
            SELECT user_id, confidence, flags_json
            FROM grade_dossiers
            WHERE offering_id = ? AND is_final = 1
            GROUP BY user_id
            HAVING MAX(graded_at)
        """, (offering_id,)):
            conf_by_user[r["user_id"]] = r["confidence"]
            audit_by_user[r["user_id"]] = (
                "flag" if r["flags_json"] and r["flags_json"] != "[]" else "ok"
            )

    students = [
        StudentRow(
            sid=r["user_id"],
            name=r["name"],
            track=r["track"],
            a0=r["a0_pts"] or 0,
            a1=r["a1_pts"] or 0,
            track_sub=r["track_pts"] or 0,
            f160=r["f160_pts"] or 0,
            total=r["total_pts"] or 0,
            audit=audit_by_user.get(r["user_id"], "—"),
            conf=conf_by_user.get(r["user_id"], "—"),
        )
        for r in rows
    ]

    return GradingResponse(
        class_summary=ClassSummary(
            avg=round(avg, 1),
            median=median,
            hi=hi,
            lo=lo,
            dossier_count=dossier_count,
            appeals_open=appeals_open,
            last_pass=last_pass,
        ),
        students=students,
    )


@app.get("/api/admin/class/calibration",
         response_model=list[CalibrationRow],
         dependencies=[Depends(require_admin)])
def calibration(offering_id: str = Query(default=DEFAULT_OFFERING)):
    """Latest calibration run per deliverable."""
    with get_db() as con:
        rows = con.execute("""
            SELECT cr.deliverable_id,
                   cr.kappa_completeness, cr.kappa_quality, cr.kappa_reflection,
                   cr.n,
                   (cr.pass_completeness AND cr.pass_quality AND cr.pass_reflection) AS ok,
                   cr.reason
            FROM calibration_runs cr
            JOIN (
                SELECT deliverable_id, MAX(run_at) AS max_at
                FROM calibration_runs
                WHERE offering_id = ?
                GROUP BY deliverable_id
            ) latest
              ON latest.deliverable_id = cr.deliverable_id
             AND latest.max_at         = cr.run_at
            WHERE cr.offering_id = ?
            ORDER BY cr.deliverable_id
        """, (offering_id, offering_id)).fetchall()
    return [CalibrationRow(
                id=r["deliverable_id"],
                kc=r["kappa_completeness"],
                kq=r["kappa_quality"],
                kr=r["kappa_reflection"],
                n=r["n"],
                ok=bool(r["ok"]),
                reason=r["reason"])
            for r in rows]


@app.get("/api/admin/class/audit/queue",
         response_model=list[AuditRow],
         dependencies=[Depends(require_admin)])
def audit_queue(offering_id: str = Query(default=DEFAULT_OFFERING)):
    """Pending audit samples (not yet completed)."""
    with get_db() as con:
        rows = con.execute("""
            SELECT gd.user_id, gd.deliverable_id, gd.points_awarded,
                   d.points AS deliv_points,
                   a.stratum, a.due_by
            FROM audit_samples a
            JOIN grade_dossiers gd ON gd.dossier_id = a.dossier_id
            JOIN deliverables   d  ON d.deliverable_id = gd.deliverable_id
                                   AND d.offering_id    = gd.offering_id
            WHERE a.completed_at IS NULL
              AND gd.offering_id = ?
            ORDER BY a.due_by, gd.user_id
        """, (offering_id,)).fetchall()
    return [AuditRow(
                sid=r["user_id"],
                deliv=r["deliverable_id"],
                ai_score=f"{r['points_awarded']}/{r['deliv_points']}",
                stratum=r["stratum"],
                due=r["due_by"])
            for r in rows]


@app.get("/api/admin/class/appeals",
         response_model=list[AppealRow],
         dependencies=[Depends(require_admin)])
def appeals(offering_id: str = Query(default=DEFAULT_OFFERING)):
    """Open appeals (stage != resolved)."""
    with get_db() as con:
        rows = con.execute("""
            SELECT a.user_id, gd.deliverable_id,
                   a.criterion, a.original_band, a.student_asks_band,
                   a.stage, a.opened_at
            FROM appeals a
            JOIN grade_dossiers gd ON gd.dossier_id = a.dossier_id
            WHERE a.stage != 'resolved'
              AND gd.offering_id = ?
            ORDER BY a.opened_at
        """, (offering_id,)).fetchall()
    return [AppealRow(
                sid=r["user_id"],
                deliv=r["deliverable_id"],
                criterion=r["criterion"],
                ai=r["original_band"],
                asks=r["student_asks_band"],
                stage=r["stage"],
                opened=r["opened_at"])
            for r in rows]


@app.post("/api/admin/class/grading/run",
          response_model=RunPassResponse,
          dependencies=[Depends(require_admin)])
def run_grading_pass(offering_id: str = Query(default=DEFAULT_OFFERING)):
    """Shell out to scripts/ai_grader.py queue to build briefings.

    The actual LLM grading is dispatched by a Cowork / Claude Code
    master session — see scripts/run_grading_pass.md. This endpoint
    only builds the queue; it does not call an LLM.
    """
    try:
        result = subprocess.run(
            ["python3", str(REPO / "scripts" / "ai_grader.py"), "queue"],
            cwd=str(REPO), capture_output=True, text=True, timeout=60,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(504, "ai_grader.py queue timed out")
    if result.returncode != 0:
        raise HTTPException(500, f"ai_grader.py queue failed: {result.stderr[:500]}")

    _audit("grading.pass", offering_id, "all", result.stdout.strip())

    # Parse "Queued N new briefings." from stdout
    import re as _re
    m = _re.search(r"Queued (\d+) new briefings", result.stdout)
    queued = int(m.group(1)) if m else 0
    return RunPassResponse(
        ok=True, queued=queued,
        note="Briefings built. Dispatch subagents via Cowork / Claude Code "
             "per scripts/run_grading_pass.md.",
    )


@app.post("/api/admin/class/audit/pull",
          dependencies=[Depends(require_admin)])
def audit_pull(offering_id: str = Query(default=DEFAULT_OFFERING),
               target_rate: float = Query(default=0.20, ge=0.0, le=1.0)):
    """Pull a new stratified 20% sample of final dossiers for TA audit.

    Stratification: all low-confidence dossiers + all flagged-deliverable
    dossiers, then random-filled to target_rate.
    """
    # This is stub-level; the real stratification logic lives in the
    # design doc §5.2 and will be fleshed out when real dossiers exist.
    with get_db() as con:
        final_ids = [r[0] for r in con.execute("""
            SELECT dossier_id FROM grade_dossiers
            WHERE offering_id = ? AND is_final = 1
        """, (offering_id,)).fetchall()]
    sample_size = max(1, int(len(final_ids) * target_rate)) if final_ids else 0
    _audit("audit.pull", offering_id, "all",
           f"target_rate={target_rate} sample_size={sample_size}")
    return {"ok": True, "sample_size": sample_size,
            "note": "Stub — real stratification runs when dossiers exist."}


# ─── Helpers ───────────────────────────────────────────────────────
def _audit(event_type: str, offering_id: str, target: str, detail: str,
           actor_user_id: Optional[str] = None) -> None:
    with get_db() as con:
        con.execute("""
            INSERT INTO audit_log_class
                (offering_id, actor_user_id, event_type, target, detail)
            VALUES (?,?,?,?,?)
        """, (offering_id, actor_user_id, event_type, target, detail[:500]))
        con.commit()


if __name__ == "__main__":  # pragma: no cover
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
