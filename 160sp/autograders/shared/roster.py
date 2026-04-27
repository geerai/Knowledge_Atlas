"""
roster.py — Student roster data model for the Grader's Page.

Loads from roster.json, tracks submissions and grades.
"""
import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Submission:
    task: int
    status: str  # "submitted", "late", "missing"
    submitted_at: Optional[str] = None
    grade: Optional[float] = None
    report_path: Optional[str] = None


@dataclass
class Student:
    student_id: str
    first_name: str
    last_name: str
    email: str
    track: str  # "t1", "t2", "t3"
    submission_dir: str = ""
    submissions: dict[str, Submission] = field(default_factory=dict)
    # key = "task_1", "task_2", "task_3"

    @property
    def full_name(self) -> str:
        return f"{self.last_name}, {self.first_name}"

    @property
    def total_grade(self) -> float:
        return sum(
            s.grade for s in self.submissions.values()
            if s.grade is not None
        )

    def get_task_status(self, task: int) -> str:
        key = f"task_{task}"
        if key in self.submissions:
            return self.submissions[key].status
        return "missing"

    def get_task_grade(self, task: int) -> Optional[float]:
        key = f"task_{task}"
        if key in self.submissions and self.submissions[key].grade is not None:
            return self.submissions[key].grade
        return None

    def set_grade(self, task: int, grade: float, report_path: str = ""):
        key = f"task_{task}"
        if key not in self.submissions:
            self.submissions[key] = Submission(task=task, status="submitted")
        self.submissions[key].grade = grade
        self.submissions[key].report_path = report_path


class Roster:
    def __init__(self):
        self.students: list[Student] = []
        self._path: str = ""

    @classmethod
    def load(cls, path: str) -> "Roster":
        """Load roster from JSON file."""
        roster = cls()
        roster._path = path
        if not os.path.isfile(path):
            return roster
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for s in data.get("students", []):
            submissions = {}
            for key, sub_data in s.get("submissions", {}).items():
                submissions[key] = Submission(
                    task=sub_data.get("task", 0),
                    status=sub_data.get("status", "missing"),
                    submitted_at=sub_data.get("submitted_at"),
                    grade=sub_data.get("grade"),
                    report_path=sub_data.get("report_path"),
                )
            roster.students.append(Student(
                student_id=s["student_id"],
                first_name=s["first_name"],
                last_name=s["last_name"],
                email=s["email"],
                track=s["track"],
                submission_dir=s.get("submission_dir", ""),
                submissions=submissions,
            ))
        return roster

    def save(self, path: str | None = None):
        """Save roster to JSON file."""
        path = path or self._path
        data = {"students": []}
        for s in self.students:
            subs = {}
            for key, sub in s.submissions.items():
                subs[key] = {
                    "task": sub.task,
                    "status": sub.status,
                    "submitted_at": sub.submitted_at,
                    "grade": sub.grade,
                    "report_path": sub.report_path,
                }
            data["students"].append({
                "student_id": s.student_id,
                "first_name": s.first_name,
                "last_name": s.last_name,
                "email": s.email,
                "track": s.track,
                "submission_dir": s.submission_dir,
                "submissions": subs,
            })
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_student(self, student_id: str) -> Optional[Student]:
        for s in self.students:
            if s.student_id == student_id:
                return s
        return None

    def get_by_track(self, track: str) -> list[Student]:
        return [s for s in self.students if s.track == track]

    def to_csv(self) -> str:
        """Export roster as CSV."""
        lines = ["Last,First,Email,Track,T1,T2,T3,Total"]
        for s in self.students:
            t1 = s.get_task_grade(1)
            t2 = s.get_task_grade(2)
            t3 = s.get_task_grade(3)
            t1s = f"{t1:.0f}" if t1 is not None else ""
            t2s = f"{t2:.0f}" if t2 is not None else ""
            t3s = f"{t3:.0f}" if t3 is not None else ""
            total = s.total_grade
            lines.append(
                f"{s.last_name},{s.first_name},{s.email},{s.track},"
                f"{t1s},{t2s},{t3s},{total:.0f}"
            )
        return "\n".join(lines)
