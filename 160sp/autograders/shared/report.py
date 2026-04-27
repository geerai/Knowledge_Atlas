"""
GradeReport — structured grading output (JSON + Markdown).

Each autograder produces a GradeReport. The Grader's Page consumes it.
"""
import json
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Literal

Result = Literal["PASS", "FAIL", "WARN", "SKIP"]
RepoStatus = Literal["ready", "needs_review", "blocked"]


@dataclass
class CheckResult:
    criterion: str
    points_earned: float
    points_possible: float
    result: Result
    detail: str
    is_gate: bool = False  # contract gate


@dataclass
class RepoItem:
    filename: str
    target_repo: str
    target_path: str
    status: RepoStatus
    reason: str = ""


@dataclass
class GradeReport:
    track: str
    task: int
    student_id: str
    max_points: float
    task_title: str = ""
    task_description: str = ""
    checks: list[CheckResult] = field(default_factory=list)
    repo_items: list[RepoItem] = field(default_factory=list)
    ruthless_comments: list[str] = field(default_factory=list)
    summary: str = ""
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    graded_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # ── scoring ──────────────────────────────────────────────
    @property
    def total_earned(self) -> float:
        return sum(c.points_earned for c in self.checks)

    @property
    def gate_passed(self) -> bool:
        return all(c.result != "FAIL" for c in self.checks if c.is_gate)

    # ── builders ─────────────────────────────────────────────
    def add_check(self, criterion: str, pts_possible: float,
                  result: Result, detail: str, *,
                  pts_earned: float | None = None,
                  is_gate: bool = False):
        if pts_earned is None:
            pts_earned = pts_possible if result == "PASS" else (
                pts_possible * 0.5 if result == "WARN" else 0
            )
        self.checks.append(CheckResult(
            criterion=criterion, points_earned=pts_earned,
            points_possible=pts_possible, result=result,
            detail=detail, is_gate=is_gate
        ))

    def add_repo_item(self, filename: str, target_repo: str,
                      target_path: str, status: RepoStatus,
                      reason: str = ""):
        self.repo_items.append(RepoItem(
            filename=filename, target_repo=target_repo,
            target_path=target_path, status=status, reason=reason
        ))

    # ── serialisation ────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "track": self.track,
            "task": self.task,
            "student_id": self.student_id,
            "task_title": self.task_title,
            "task_description": self.task_description,
            "max_points": self.max_points,
            "total_earned": self.total_earned,
            "gate_passed": self.gate_passed,
            "graded_at": self.graded_at,
            "summary": self.summary,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "missing": self.missing,
            "checks": [
                {"criterion": c.criterion, "earned": c.points_earned,
                 "possible": c.points_possible, "result": c.result,
                 "detail": c.detail, "is_gate": c.is_gate}
                for c in self.checks
            ],
            "repo_items": [
                {"filename": r.filename, "target_repo": r.target_repo,
                 "target_path": r.target_path, "status": r.status,
                 "reason": r.reason}
                for r in self.repo_items
            ],
            "ruthless_comments": self.ruthless_comments,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def to_markdown(self) -> str:
        lines = []
        lines.append(f"# {self.task_title}")
        lines.append(f"**Student:** {self.student_id}  ")
        lines.append(f"**Score:** {self.total_earned:.0f} / {self.max_points:.0f}  ")
        lines.append(f"**Contract Gate:** {'✅ Passed' if self.gate_passed else '❌ FAILED'}  ")
        lines.append(f"**Graded:** {self.graded_at}  ")
        lines.append("")

        if self.task_description:
            lines.append("## Task Description")
            lines.append(self.task_description[:500] + ("..." if len(self.task_description) > 500 else ""))
            lines.append("")

        if self.summary:
            lines.append("## What They Did")
            lines.append(self.summary)
            lines.append("")

        # Critique
        lines.append("## Critique")
        lines.append("")
        for s in self.strengths:
            lines.append(f"✅ **Strong:** {s}")
        for w in self.weaknesses:
            lines.append(f"⚠️ **Weak:** {w}")
        for m in self.missing:
            lines.append(f"❌ **Missing:** {m}")
        lines.append("")

        # Detail table
        lines.append("## Check Details")
        lines.append("")
        lines.append("| Criterion | Pts | Result | Detail |")
        lines.append("|---|---|---|---|")
        for c in self.checks:
            gate = " 🚪" if c.is_gate else ""
            lines.append(
                f"| {c.criterion}{gate} | {c.points_earned:.0f}/{c.points_possible:.0f} "
                f"| {c.result} | {c.detail[:80]} |"
            )
        lines.append("")

        # Repo items
        if self.repo_items:
            lines.append("## Repo-Worthy Items")
            lines.append("")
            for r in self.repo_items:
                icon = {"ready": "✅", "needs_review": "⚠️", "blocked": "❌"}[r.status]
                lines.append(f"- {icon} `{r.filename}` → `{r.target_repo}/{r.target_path}` ({r.status})")
                if r.reason:
                    lines.append(f"  {r.reason}")
            lines.append("")

        # Ruthless
        if self.ruthless_comments:
            lines.append("## Ruthless Test Output")
            lines.append("")
            for c in self.ruthless_comments:
                lines.append(f"- {c}")
            lines.append("")

        return "\n".join(lines)
