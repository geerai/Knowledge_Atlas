#!/usr/bin/env python3
"""
server.py — Zero-dependency backend for the 160sp Grader's Page.

Uses only Python stdlib (http.server + json). No Flask needed.

Usage:
  python3 server.py
  → Open http://localhost:5050

Endpoints:
  GET  /                    → Dashboard HTML
  POST /api/grade           → Run grader on a submission
  GET  /api/roster          → Roster with grades
  POST /api/review          → Approve/reject repo items
  GET  /api/export/grades   → CSV download
"""
import json, os, sys, importlib, io
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parent.parent / "autograders"
sys.path.insert(0, str(BASE))

from shared.roster import Roster

ROSTER_PATH = str(BASE / "roster.json")
RESULTS_DIR = str(Path(__file__).resolve().parent / "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

GRADERS = {
    "t1_1": "t1_task1_grader", "t1_2": "t1_task2_grader", "t1_3": "t1_task3_grader",
    "t2_1": "t2_task1_grader", "t2_2": "t2_task2_grader", "t2_3": "t2_task3_grader",
    "t3_1": "t3_task1_grader", "t3_2": "t3_task2_grader", "t3_3": "t3_task3_grader",
}


class GraderHandler(BaseHTTPRequestHandler):

    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path, content_type="text/html"):
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _send_csv(self, csv_text, filename="export.csv"):
        body = csv_text.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/csv")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/" or path == "/index.html":
            html_path = Path(__file__).resolve().parent / "index.html"
            self._send_file(str(html_path))

        elif path == "/api/roster":
            roster = Roster.load(ROSTER_PATH)
            students = []
            for s in roster.students:
                students.append({
                    "student_id": s.student_id,
                    "first_name": s.first_name, "last_name": s.last_name,
                    "email": s.email, "track": s.track,
                    "task_1_status": s.get_task_status(1),
                    "task_1_grade": s.get_task_grade(1),
                    "task_2_status": s.get_task_status(2),
                    "task_2_grade": s.get_task_grade(2),
                    "task_3_status": s.get_task_status(3),
                    "task_3_grade": s.get_task_grade(3),
                    "total": s.total_grade,
                })
            self._send_json({"students": students})

        elif path.startswith("/api/results/"):
            student_id = path.split("/")[-1]
            report_dir = os.path.join(RESULTS_DIR, student_id)
            reports = []
            if os.path.isdir(report_dir):
                for f in sorted(os.listdir(report_dir)):
                    if f.endswith("_report.json"):
                        with open(os.path.join(report_dir, f)) as fh:
                            reports.append(json.load(fh))
            self._send_json({"reports": reports})

        elif path.startswith("/api/task-info/"):
            parts = path.rstrip("/").split("/")
            track, task = parts[-2], int(parts[-1])
            key = f"{track}_{task}"
            if key in GRADERS:
                mod = importlib.import_module(GRADERS[key])
                self._send_json({
                    "title": getattr(mod, "TASK_TITLE", ""),
                    "description": getattr(mod, "TASK_DESC", ""),
                    "max_points": getattr(mod, "MAX_POINTS", 75),
                })
            else:
                self._send_json({"error": "Unknown"}, 404)

        elif path == "/api/export/grades":
            roster = Roster.load(ROSTER_PATH)
            self._send_csv(roster.to_csv(), "160sp_grades.csv")

        else:
            self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        data = self._read_body()

        if path == "/api/grade":
            track = data.get("track", "")
            task = data.get("task", 0)
            student_id = data.get("student_id", "unknown")
            submission_dir = data.get("submission_dir", "")

            key = f"{track}_{task}"
            if key not in GRADERS:
                self._send_json({"error": f"Unknown: {key}"}, 400)
                return

            mod = importlib.import_module(GRADERS[key])

            if not submission_dir:
                roster = Roster.load(ROSTER_PATH)
                student = roster.get_student(student_id)
                if student and student.submission_dir:
                    submission_dir = student.submission_dir
                else:
                    submission_dir = os.path.join(str(BASE), "submissions",
                                                   student_id, f"task_{task}")

            try:
                report = mod.grade(submission_dir, student_id)
            except Exception as e:
                self._send_json({"error": f"Grader crashed: {e}"}, 500)
                return

            # Save reports
            report_dir = os.path.join(RESULTS_DIR, student_id)
            os.makedirs(report_dir, exist_ok=True)
            rpath = os.path.join(report_dir, f"{track}_task{task}_report.json")
            with open(rpath, "w") as f:
                json.dump(report.to_dict(), f, indent=2)
            with open(os.path.join(report_dir, f"{track}_task{task}_report.md"), "w") as f:
                f.write(report.to_markdown())

            # Update roster
            roster = Roster.load(ROSTER_PATH)
            student = roster.get_student(student_id)
            if student:
                student.set_grade(task, report.total_earned, rpath)
                roster.save()

            self._send_json(report.to_dict())

        elif path == "/api/review":
            student_id = data.get("student_id")
            track = data.get("track")
            task = data.get("task")
            filename = data.get("filename")
            action = data.get("action")

            rpath = os.path.join(RESULTS_DIR, student_id,
                                  f"{track}_task{task}_report.json")
            if not os.path.isfile(rpath):
                self._send_json({"error": "Report not found"}, 404)
                return

            with open(rpath) as f:
                report = json.load(f)
            for item in report.get("repo_items", []):
                if item["filename"] == filename:
                    item["status"] = {"approve": "ready", "reject": "blocked",
                                       "request_changes": "needs_review"}[action]
                    item["reviewed_at"] = datetime.now(timezone.utc).isoformat()
                    break
            with open(rpath, "w") as f:
                json.dump(report, f, indent=2)
            self._send_json({"ok": True, "action": action})

        else:
            self.send_error(404)

    def log_message(self, format, *args):
        print(f"  {args[0]}")  # Minimal logging


def main():
    port = 5050
    server = HTTPServer(("0.0.0.0", port), GraderHandler)
    print(f"╔══════════════════════════════════════════════╗")
    print(f"║  160sp Grader Dashboard                      ║")
    print(f"║  http://localhost:{port}                        ║")
    print(f"╚══════════════════════════════════════════════╝")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
        server.server_close()


if __name__ == "__main__":
    main()
