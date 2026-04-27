#!/usr/bin/env python3
"""
T2 Task 2 — Grading & Comment Tool (PRISMA / Abstract-First Architecture)
==========================================================================
Run against a student's Knowledge_Atlas clone to assign grades and comments
for the "Search Pipeline (Abstract-First Triage)" assignment.

Usage
-----
    python3 t2_task2_grader.py /path/to/student/Knowledge_Atlas
    python3 t2_task2_grader.py --auto-only /path/to/student/Knowledge_Atlas
"""

import argparse
import ast
import json
import os
import re
import sqlite3
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ════════════════════════════════════════════════
# DATA MODEL
# ════════════════════════════════════════════════

@dataclass
class TestResult:
    name: str
    passed: bool
    weight: str  # "critical", "important", "minor"
    details: str = ""

@dataclass
class RubricScore:
    criterion: str
    max_points: int
    points: int = 0
    comment: str = ""

@dataclass
class GradeReport:
    student_name: str = ""
    student_email: str = ""
    grader: str = ""
    timestamp: str = ""
    rubric_scores: list = field(default_factory=list)
    auto_tests: list = field(default_factory=list)
    total_points: int = 0
    max_points: int = 0
    overall_comment: str = ""
    file_manifest: list = field(default_factory=list)


# ════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════

def _find_py(repo: Path, hints: list[str], content_markers: list[str]) -> list[Path]:
    """Find Python files by name hints or content markers."""
    found = []
    for h in hints:
        for p in repo.rglob(h):
            if p.is_file():
                found.append(p)
    if not found:
        for py in repo.glob("*.py"):
            try:
                src = py.read_text(errors="replace")
                if any(m in src for m in content_markers):
                    found.append(py)
            except Exception:
                pass
    return found


def _source_contains(path: Path, markers: list[str]) -> list[str]:
    """Return which markers appear in the source file."""
    try:
        src = path.read_text(errors="replace")
        return [m for m in markers if m in src]
    except Exception:
        return []


def _all_py_sources(repo: Path) -> list[tuple[Path, str]]:
    """Read all Python files at top level and common subdirs."""
    results = []
    for pattern in ["*.py", "scripts/*.py", "pipeline/*.py", "src/*.py"]:
        for p in repo.glob(pattern):
            try:
                results.append((p, p.read_text(errors="replace")))
            except Exception:
                pass
    return results


# ════════════════════════════════════════════════
# AUTOMATED TESTS
# ════════════════════════════════════════════════

def test_gap_extractor_exists(repo: Path) -> TestResult:
    """Check that a gap extractor / topic proposer script exists."""
    name = "Gap extractor script exists"
    found = _find_py(repo,
        ["gap_extractor.py", "topic_proposer.py", "search_pipeline.py",
         "gap_analyzer.py", "proposer.py"],
        ["mechanism_chain", "gap_type", "voi_score"])
    if found:
        return TestResult(name, True, "critical",
                          f"Found: {', '.join(str(f.relative_to(repo)) for f in found)}")
    return TestResult(name, False, "critical", "No gap extractor script found")


def test_reads_templates_and_confidence(repo: Path) -> TestResult:
    """Check the extractor reads PNU templates and checks confidence."""
    name = "Reads templates + checks confidence"
    sources = _all_py_sources(repo)
    for path, src in sources:
        reads_json = "json.load" in src or "json.loads" in src
        reads_chain = "mechanism_chain" in src
        reads_conf = "confidence" in src and ("< 0.5" in src or "<0.5" in src or "threshold" in src)
        if reads_json and reads_chain:
            detail = "Reads JSON + mechanism_chain"
            if reads_conf:
                detail += " + confidence threshold"
            return TestResult(name, True, "critical", f"{detail} ({path.name})")
    return TestResult(name, False, "critical",
                      "No script reads mechanism_chain from template JSON")


def test_voi_integration(repo: Path) -> TestResult:
    """Check if VOI scoring functions are imported/used."""
    name = "VOI scoring integration"
    voi_markers = ["VOICalculator", "calculate_voi", "score_voi",
                   "voi_score", "classify_closure", "voi_search",
                   "aggregate_paper_voi"]
    sources = _all_py_sources(repo)
    found = []
    for path, src in sources:
        hits = [m for m in voi_markers if m in src]
        if hits:
            found.extend(hits)
    found = list(set(found))
    if len(found) >= 2:
        return TestResult(name, True, "important",
                          f"Uses VOI functions: {found}")
    elif found:
        return TestResult(name, True, "important",
                          f"Partial VOI use: {found}")
    return TestResult(name, False, "important",
                      "No VOI scoring functions found in any script")


def test_api_integration(repo: Path) -> TestResult:
    """Check if Semantic Scholar / CrossRef / PubMed APIs are used."""
    name = "API integration (Semantic Scholar / CrossRef / PubMed)"
    api_markers = ["SemanticScholarClient", "CrossRefClient", "PubMedClient",
                   "PaperFetcher", "paper_fetcher", "api.semanticscholar",
                   "api.crossref", "semantic_scholar", "crossref"]
    sources = _all_py_sources(repo)
    found = []
    for path, src in sources:
        hits = [m for m in api_markers if m in src]
        if hits:
            found.extend(hits)
    found = list(set(found))
    if found:
        return TestResult(name, True, "critical",
                          f"API clients used: {found}")
    return TestResult(name, False, "critical",
                      "No Semantic Scholar / CrossRef / PubMed integration found")


def test_abstract_triage(repo: Path) -> TestResult:
    """Check if abstract-level triage is implemented (classifier + VOI on abstracts)."""
    name = "Abstract-level triage (classifier + VOI before PDF download)"
    triage_markers = ["abstract", "triage", "ACCEPT", "EDGE_CASE", "REJECT",
                      "classifier", "classify", "AdaptiveClassifier"]
    sources = _all_py_sources(repo)
    abstract_ref = False
    triage_logic = False
    for path, src in sources:
        if "abstract" in src.lower() and ("classify" in src.lower() or "score_voi" in src):
            abstract_ref = True
        if ("ACCEPT" in src and "REJECT" in src) or "triage" in src.lower():
            triage_logic = True
    if abstract_ref and triage_logic:
        return TestResult(name, True, "critical",
                          "Abstract triage with classifier + accept/reject logic")
    elif abstract_ref or triage_logic:
        return TestResult(name, True, "important",
                          "Partial triage logic found")
    return TestResult(name, False, "critical",
                      "No abstract-level triage found — may be downloading PDFs blindly")


def test_search_results_exist(repo: Path) -> TestResult:
    """Check that search results were produced."""
    name = "Search results exist"
    results = []
    for pattern in ["search_results*.json", "data/search*.json",
                     "data/storage/search*.json", "**/search_results*.json",
                     "triage_results*.json", "**/triage*.json"]:
        results.extend(repo.glob(pattern))
    if results:
        total = 0
        for r in results:
            try:
                data = json.loads(r.read_text())
                if isinstance(data, list):
                    total += len(data)
                elif isinstance(data, dict) and "results" in data:
                    total += len(data["results"])
            except Exception:
                pass
        return TestResult(name, True, "critical",
                          f"{len(results)} result file(s), {total} total entries")
    return TestResult(name, False, "critical", "No search result JSON files found")


def test_prisma_dashboard(repo: Path) -> TestResult:
    """Check that a PRISMA-style dashboard exists."""
    name = "PRISMA dashboard exists"
    candidates = ["ka_topic_proposer.html", "ka_search_dashboard.html",
                   "ka_pipeline_dashboard.html", "topic_proposer.html",
                   "search_pipeline.html", "prisma_dashboard.html"]
    for c in candidates:
        p = repo / c
        if p.exists():
            src = p.read_text(errors="replace").lower()
            has_funnel = any(w in src for w in ["funnel", "prisma", "screened",
                                                  "identified", "included"])
            has_counts = any(w in src for w in ["accept", "reject", "edge",
                                                  "triage", "result"])
            features = []
            if has_funnel:
                features.append("PRISMA funnel")
            if has_counts:
                features.append("triage counts")
            return TestResult(name, True, "important",
                              f"Found: {c} — features: {features}")
    return TestResult(name, False, "important", "No dashboard page found")


def test_dashboard_persistence(repo: Path) -> TestResult:
    """Check dashboard reads from persistent storage."""
    name = "Dashboard data persistence"
    for c in ["ka_topic_proposer.html", "ka_search_dashboard.html",
              "ka_pipeline_dashboard.html", "topic_proposer.html"]:
        p = repo / c
        if p.exists():
            src = p.read_text(errors="replace")
            if any(k in src for k in ["fetch(", "localStorage", ".json",
                                        "XMLHttpRequest", "sqlite"]):
                return TestResult(name, True, "minor",
                                  "Dashboard uses persistent data source")
            return TestResult(name, False, "minor",
                              "Dashboard may not persist data after refresh")
    return TestResult(name, False, "minor", "No dashboard found")


def test_null_result_handling(repo: Path) -> TestResult:
    """Check if null results (zero papers found) are handled."""
    name = "Null result handling"
    sources = _all_py_sources(repo)
    for path, src in sources:
        if any(m in src.lower() for m in ["null result", "no results",
                                            "zero results", "no papers found",
                                            "result_count == 0", "len(results) == 0"]):
            return TestResult(name, True, "minor",
                              f"Null results handled in {path.name}")
    return TestResult(name, False, "minor",
                      "No null result handling found — pipeline may crash on empty searches")


def test_classifier_integration(repo: Path) -> TestResult:
    """Check classifier integration from atlas_shared."""
    name = "Classifier integration (atlas_shared)"
    sources = _all_py_sources(repo)
    for path, src in sources:
        if any(m in src for m in ["atlas_shared", "AdaptiveClassifier",
                                    "classifier_system", "classify"]):
            return TestResult(name, True, "important",
                              f"Classifier integration in {path.name}")
    return TestResult(name, False, "important",
                      "No atlas_shared classifier integration found")


def test_db_entries(repo: Path) -> TestResult:
    """Check if vetted papers appear in the database."""
    name = "Vetted papers stored in database"
    for candidate in [repo / "data" / "ka_auth.db", repo / "ka_auth.db"]:
        if candidate.exists():
            try:
                db = sqlite3.connect(str(candidate), timeout=5.0)
                count = db.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
                db.close()
                if count > 0:
                    return TestResult(name, True, "important",
                                      f"{count} articles in database")
                return TestResult(name, False, "important",
                                  "articles table exists but is empty")
            except Exception as e:
                return TestResult(name, False, "important", f"DB error: {e}")
    return TestResult(name, False, "important", "Database not found")


# ════════════════════════════════════════════════
# MANUAL RUBRIC (matches assignment grading table)
# ════════════════════════════════════════════════

RUBRIC_CRITERIA = [
    RubricScore("Gap extraction: Identified low-confidence steps, scored by VOI", 15),
    RubricScore("VOI understanding: Can explain why one gap scores higher than another", 10),
    RubricScore("API integration: Queried Semantic Scholar/CrossRef, got abstracts back", 15),
    RubricScore("Abstract triage: Classifier + VOI → defensible ACCEPT/EDGE_CASE/REJECT", 20),
    RubricScore("PRISMA funnel: Dashboard shows real numbers at each stage", 15),
    RubricScore("End-to-end trace: One paper traced gap → API → abstract → triage → store", 10),
    RubricScore("Null results: Documented gaps where no papers exist", 5),
    RubricScore("Verification questions: Caught real problems in AI's implementation", 10),
    RubricScore("Automated tests (auto-scored)", 15),
]


def prompt_manual_score(criterion: RubricScore) -> RubricScore:
    """Prompt the TA for a score and comment."""
    print(f"\n{'─' * 60}")
    print(f"  {criterion.criterion}")
    print(f"  Max points: {criterion.max_points}")
    print(f"{'─' * 60}")
    while True:
        try:
            raw = input(f"  Score (0–{criterion.max_points}): ").strip()
            score = int(raw) if raw else 0
            if 0 <= score <= criterion.max_points:
                break
            print(f"  Must be between 0 and {criterion.max_points}")
        except ValueError:
            print("  Enter a number")
        except (EOFError, KeyboardInterrupt):
            score = 0
            break
    comment = input("  Comment (optional): ").strip()
    criterion.points = score
    criterion.comment = comment
    return criterion


# ════════════════════════════════════════════════
# SCORING & REPORT
# ════════════════════════════════════════════════

def compute_auto_score(results: list[TestResult]) -> tuple[int, int]:
    """Compute points from automated tests. Max 15 points."""
    max_pts = 15
    weights = {"critical": 3, "important": 2, "minor": 1}
    total_weight = sum(weights[r.weight] for r in results)
    earned_weight = sum(weights[r.weight] for r in results if r.passed)
    if total_weight == 0:
        return 0, max_pts
    return round(max_pts * earned_weight / total_weight), max_pts


def render_report(report: GradeReport) -> str:
    """Render the grade report as markdown."""
    lines = [
        "# T2 Task 2 — Grade Report (Search Pipeline / Abstract-First Triage)",
        "",
        f"**Student:** {report.student_name or '(not set)'}",
        f"**Email:** {report.student_email or '(not set)'}",
        f"**Grader:** {report.grader or '(not set)'}",
        f"**Date:** {report.timestamp}",
        "",
        "---",
        "",
        f"## Total: {report.total_points} / {report.max_points}",
        "",
        "## Rubric Scores",
        "",
        "| Criterion | Score | Comment |",
        "|-----------|-------|---------|",
    ]
    for s in report.rubric_scores:
        comment = s.comment.replace("|", "\\|") if s.comment else "—"
        lines.append(f"| {s.criterion} | {s.points}/{s.max_points} | {comment} |")

    lines += [
        "",
        "## Automated Test Results",
        "",
        "| Test | Status | Weight | Details |",
        "|------|--------|--------|---------|",
    ]
    for t in report.auto_tests:
        icon = "✅" if t.passed else "❌"
        details = t.details.replace("|", "\\|")[:100]
        lines.append(f"| {t.name} | {icon} | {t.weight} | {details} |")

    if report.file_manifest:
        lines += ["", "## File Manifest", "", "```"]
        lines.extend(report.file_manifest)
        lines += ["```", ""]

    if report.overall_comment:
        lines += ["", "## Overall Comments", "", report.overall_comment, ""]

    return "\n".join(lines)


def collect_file_manifest(repo: Path) -> list[str]:
    """Get list of changed/new files via git."""
    manifest = []
    try:
        diff = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=str(repo), capture_output=True, text=True, timeout=10)
        if diff.stdout.strip():
            manifest.extend(diff.stdout.strip().split("\n"))
        status = subprocess.run(
            ["git", "status", "--short"],
            cwd=str(repo), capture_output=True, text=True, timeout=10)
        for line in status.stdout.strip().split("\n"):
            if line.strip():
                parts = line.strip().split(None, 1)
                if len(parts) == 2 and parts[1] not in manifest:
                    manifest.append(f"[{parts[0]}] {parts[1]}")
    except Exception:
        manifest.append("(git not available)")
    return manifest


# ════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Grade a student's T2 Task 2 submission (PRISMA pipeline)")
    parser.add_argument("repo", type=Path,
                        help="Path to the student's Knowledge_Atlas clone")
    parser.add_argument("--student-name", default="")
    parser.add_argument("--student-email", default="")
    parser.add_argument("--grader", default="")
    parser.add_argument("--auto-only", action="store_true",
                        help="Run automated tests only, skip manual rubric")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not repo.exists():
        print(f"Error: {repo} does not exist")
        sys.exit(1)

    print("=" * 60)
    print("  T2 Task 2 Grader — Search Pipeline (Abstract-First Triage)")
    print("=" * 60)
    print(f"  Repo: {repo}\n")

    student_name = args.student_name or input("Student name: ").strip()
    student_email = args.student_email or input("Student email: ").strip()
    grader = args.grader or input("Grader name: ").strip()

    # ── Automated tests
    print("\n" + "=" * 60)
    print("  Running automated tests...")
    print("=" * 60)

    auto_results = [
        test_gap_extractor_exists(repo),
        test_reads_templates_and_confidence(repo),
        test_voi_integration(repo),
        test_api_integration(repo),
        test_abstract_triage(repo),
        test_search_results_exist(repo),
        test_prisma_dashboard(repo),
        test_dashboard_persistence(repo),
        test_null_result_handling(repo),
        test_classifier_integration(repo),
        test_db_entries(repo),
    ]

    for r in auto_results:
        icon = "✅" if r.passed else "❌"
        print(f"  {icon} [{r.weight:>9s}] {r.name}: {r.details}")

    auto_score, auto_max = compute_auto_score(auto_results)
    print(f"\n  Automated score: {auto_score}/{auto_max}")

    # ── File manifest
    print("\n" + "=" * 60)
    print("  Collecting file manifest...")
    print("=" * 60)
    manifest = collect_file_manifest(repo)
    for f in manifest:
        print(f"    {f}")

    # ── Manual rubric
    rubric_scores = []
    if not args.auto_only:
        print("\n" + "=" * 60)
        print("  Manual rubric scoring")
        print("=" * 60)
        for criterion in RUBRIC_CRITERIA:
            if "auto-scored" in criterion.criterion.lower():
                criterion.points = auto_score
                criterion.comment = (
                    f"Auto: {sum(1 for r in auto_results if r.passed)}"
                    f"/{len(auto_results)} tests passed"
                )
                rubric_scores.append(criterion)
            else:
                rubric_scores.append(prompt_manual_score(criterion))
    else:
        for criterion in RUBRIC_CRITERIA:
            if "auto-scored" in criterion.criterion.lower():
                criterion.points = auto_score
                criterion.comment = (
                    f"Auto: {sum(1 for r in auto_results if r.passed)}"
                    f"/{len(auto_results)} tests passed"
                )
            else:
                criterion.comment = "(auto-only mode — not scored)"
            rubric_scores.append(criterion)

    # ── Overall comment
    overall_comment = ""
    if not args.auto_only:
        print(f"\n{'─' * 60}")
        print("  Overall comment (multi-line, end with empty line):")
        comment_lines = []
        while True:
            try:
                line = input("  > ")
                if line == "":
                    break
                comment_lines.append(line)
            except (EOFError, KeyboardInterrupt):
                break
        overall_comment = "\n".join(comment_lines)

    # ── Build and write report
    total = sum(s.points for s in rubric_scores)
    max_total = sum(s.max_points for s in rubric_scores)

    report = GradeReport(
        student_name=student_name,
        student_email=student_email,
        grader=grader,
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        rubric_scores=rubric_scores,
        auto_tests=auto_results,
        total_points=total,
        max_points=max_total,
        overall_comment=overall_comment,
        file_manifest=manifest,
    )

    output_path = args.output
    if output_path is None:
        output_dir = repo / "160sp" / "rubrics" / "t2"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "GRADE_REPORT_T2_TASK2.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_report(report))

    print("\n" + "=" * 60)
    print(f"  TOTAL: {total} / {max_total}")
    print(f"  Report written to: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
