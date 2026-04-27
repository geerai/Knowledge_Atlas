#!/usr/bin/env python3
"""
T1 Task 1 — Grading & Comment Tool (Image Collection Pipeline)
===============================================================
Usage:  python3 t1_task1_grader.py /path/to/student/Knowledge_Atlas
        python3 t1_task1_grader.py --auto-only /path/to/student/Knowledge_Atlas
"""

import argparse, json, os, re, subprocess, sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Import contract evaluator from t2 (shared)
sys.path.insert(0, str(Path(__file__).parent.parent / "t2"))
try:
    from contract_evaluator import scan_for_contracts, ContractGateResult
except ImportError:
    # Fallback stub if contract_evaluator not found
    @dataclass
    class ContractGateResult:
        gate_passed: bool = False; gate_reason: str = "contract_evaluator not found"
        score: int = 0; max_score: int = 20; contracts_found: list = field(default_factory=list)
        summary: str = ""; contracts_expected: int = 0
        def render_table(self): return "## Contract Quality Assessment\n\n(contract_evaluator.py not found — copy from t2/)\n"
    def scan_for_contracts(repo, expected_contracts=3):
        return ContractGateResult()


@dataclass
class TestResult:
    name: str; passed: bool; weight: str; details: str = ""

@dataclass
class RubricScore:
    criterion: str; max_points: int; points: int = 0; comment: str = ""

@dataclass
class GradeReport:
    student_name: str = ""; student_email: str = ""; grader: str = ""
    timestamp: str = ""; rubric_scores: list = field(default_factory=list)
    auto_tests: list = field(default_factory=list); total_points: int = 0
    max_points: int = 0; overall_comment: str = ""
    file_manifest: list = field(default_factory=list)
    contract_gate: ContractGateResult = field(default_factory=ContractGateResult)


def _all_py(repo):
    r = []
    for pat in ["*.py", "scripts/*.py", "pipeline/*.py"]:
        for p in repo.glob(pat):
            try: r.append((p, p.read_text(errors="replace")))
            except: pass
    return r


# ── Tests ──

def test_taxonomy_exists(repo):
    name = "Space-type taxonomy JSON exists"
    for pat in ["space_type_taxonomy.json", "*taxonomy*.json", "data/*taxonomy*.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                if isinstance(data, dict):
                    space_types = [k for k in data.keys() if k not in ("version", "schema", "metadata")]
                    if len(space_types) >= 10:
                        return TestResult(name, True, "critical",
                                          f"{f.name}: {len(space_types)} space types")
                    return TestResult(name, True, "critical",
                                      f"{f.name}: only {len(space_types)} space types (need 20+)")
            except: pass
    return TestResult(name, False, "critical", "No taxonomy JSON found")


def test_taxonomy_quality(repo):
    name = "Taxonomy maps to registry tags"
    for pat in ["space_type_taxonomy.json", "*taxonomy*.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                has_tags = 0
                has_search = 0
                for k, v in data.items():
                    if not isinstance(v, dict): continue
                    if any(fld in v for fld in ["expected_tags", "tags", "registry_tags"]):
                        has_tags += 1
                    if any(fld in v for fld in ["search_terms", "keywords", "queries"]):
                        has_search += 1
                if has_tags >= 10 and has_search >= 10:
                    return TestResult(name, True, "important",
                                      f"{has_tags} types with tags, {has_search} with search terms")
                elif has_tags >= 5:
                    return TestResult(name, True, "important",
                                      f"Partial: {has_tags} types with tags")
            except: pass
    return TestResult(name, False, "important", "Cannot verify taxonomy tag mapping")


def test_database_list(repo):
    name = "Database list JSON exists"
    for pat in ["image_databases.json", "*database*.json", "data/*database*.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                dbs = data.get("databases", data) if isinstance(data, dict) else data
                if isinstance(dbs, list):
                    tested = sum(1 for d in dbs if isinstance(d, dict) and d.get("tested"))
                    return TestResult(name, True, "critical",
                                      f"{f.name}: {len(dbs)} databases, {tested} tested")
            except: pass
    return TestResult(name, False, "critical", "No database list found")


def test_search_pipeline(repo):
    name = "Search pipeline script exists"
    for pat in ["search_pipeline.py", "image_search*.py", "image_collector*.py"]:
        if (repo / pat).exists():
            src = (repo / pat).read_text(errors="replace")
            features = []
            if "requests" in src or "httpx" in src or "urllib" in src: features.append("HTTP")
            if "api_key" in src.lower() or "API_KEY" in src: features.append("auth")
            if "time.sleep" in src or "rate_limit" in src: features.append("rate_limit")
            if "license" in src.lower(): features.append("license_check")
            return TestResult(name, True, "critical", f"{pat}: {features}")
    for p, src in _all_py(repo):
        if ("unsplash" in src.lower() or "pexels" in src.lower() or
                "flickr" in src.lower() or "wikimedia" in src.lower()):
            return TestResult(name, True, "critical", f"Search logic in {p.name}")
    return TestResult(name, False, "critical", "No search pipeline found")


def test_search_results(repo):
    name = "Search results JSON exists"
    for pat in ["search_results.json", "data/search*.json", "*_results.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                items = data if isinstance(data, list) else data.get("results", [])
                return TestResult(name, True, "important", f"{f.name}: {len(items)} results")
            except: pass
    return TestResult(name, False, "important", "No search results found")


def test_collection_page(repo):
    name = "Collection dashboard exists"
    for c in ["ka_image_collection.html", "image_collection.html",
              "collection_dashboard.html", "image_collector.html"]:
        p = repo / c
        if p.exists():
            src = p.read_text(errors="replace").lower()
            features = []
            if "search" in src: features.append("search")
            if "upload" in src or "drop" in src: features.append("upload")
            if "provenance" in src or "source" in src: features.append("provenance")
            if "accept" in src or "reject" in src: features.append("triage")
            if "500" in src or "counter" in src or "progress" in src: features.append("counter")
            return TestResult(name, True, "critical", f"{c}: {features}")
    return TestResult(name, False, "critical", "No collection dashboard found")


def test_collection_json(repo):
    name = "Collection JSON with 500 images"
    for pat in ["collection.json", "image_collection.json", "data/collection*.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                items = data if isinstance(data, list) else data.get("images", data.get("collection", []))
                return TestResult(name, True, "critical", f"{f.name}: {len(items)} images")
            except: pass
    return TestResult(name, False, "critical", "No collection JSON found")


def test_provenance(repo):
    name = "Provenance fields present on images"
    required = {"source_page_url", "source_name", "license", "source_database"}
    for pat in ["collection.json", "image_collection.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                items = data if isinstance(data, list) else data.get("images", data.get("collection", []))
                if not items: continue
                # Check first 10
                complete = 0
                for img in items[:10]:
                    if isinstance(img, dict):
                        present = set(img.keys()) & required
                        if len(present) >= 3: complete += 1
                if complete >= 7:
                    return TestResult(name, True, "critical",
                                      f"{complete}/10 sampled images have provenance")
                elif complete >= 3:
                    return TestResult(name, True, "critical",
                                      f"Only {complete}/10 sampled images have full provenance")
            except: pass
    return TestResult(name, False, "critical", "Cannot verify provenance")


def test_license_compliance(repo):
    name = "License fields present"
    for pat in ["collection.json", "image_collection.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                items = data if isinstance(data, list) else data.get("images", data.get("collection", []))
                has_license = sum(1 for img in items if isinstance(img, dict) and img.get("license"))
                pct = round(100 * has_license / max(len(items), 1))
                if pct >= 90:
                    return TestResult(name, True, "important", f"{has_license}/{len(items)} ({pct}%) have license")
                elif pct >= 50:
                    return TestResult(name, True, "important", f"Only {pct}% have license field")
            except: pass
    return TestResult(name, False, "important", "Cannot verify license fields")


def test_space_type_coverage(repo):
    name = "Space type coverage (≥ 15 types)"
    for pat in ["collection.json", "image_collection.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                items = data if isinstance(data, list) else data.get("images", data.get("collection", []))
                types = set()
                for img in items:
                    if isinstance(img, dict):
                        st = img.get("space_type", img.get("room_type", img.get("category")))
                        if st: types.add(st)
                if len(types) >= 15:
                    return TestResult(name, True, "important", f"{len(types)} space types")
                elif len(types) >= 5:
                    return TestResult(name, True, "important", f"Only {len(types)} types (need 15+)")
            except: pass
    return TestResult(name, False, "important", "Cannot verify space type coverage")


RUBRIC = [
    RubricScore("Taxonomy: ≥ 20 space types, maps to registry tags", 10),
    RubricScore("Database curation: ≥ 5 tested, APIs verified, licenses documented", 10),
    RubricScore("Search pipeline: Automated, respects licenses, tracks provenance", 10),
    RubricScore("Collection dashboard: Search + browse + upload + provenance + export", 10),
    RubricScore("500 images with provenance: Full provenance, ≥ 15 types, diversity", 10),
    RubricScore("Verification questions: Caught problems in AI implementation", 5),
]


def prompt_manual(c):
    print(f"\n{'─'*60}\n  {c.criterion}\n  Max: {c.max_points}\n{'─'*60}")
    while True:
        try:
            raw = input(f"  Score (0–{c.max_points}): ").strip()
            s = int(raw) if raw else 0
            if 0 <= s <= c.max_points: break
            print(f"  0–{c.max_points}")
        except ValueError: print("  Number please")
        except (EOFError, KeyboardInterrupt): s = 0; break
    c.points = s; c.comment = input("  Comment: ").strip()
    return c


def compute_auto(results):
    w = {"critical": 3, "important": 2, "minor": 1}
    total = sum(w[r.weight] for r in results)
    earned = sum(w[r.weight] for r in results if r.passed)
    return round(15 * earned / total) if total else 0


def render(report):
    lines = [
        "# T1 Task 1 — Grade Report (Image Collection Pipeline)", "",
        f"**Student:** {report.student_name or '(not set)'}",
        f"**Email:** {report.student_email or '(not set)'}",
        f"**Grader:** {report.grader or '(not set)'}",
        f"**Date:** {report.timestamp}", "", "---", "",
        f"## Total: {report.total_points} / {report.max_points}", "",
        "## Rubric Scores", "", "| Criterion | Score | Comment |",
        "|-----------|-------|---------|",
    ]
    for s in report.rubric_scores:
        lines.append(f"| {s.criterion} | {s.points}/{s.max_points} | {(s.comment or '—').replace('|','\\|')} |")
    lines.append("")
    lines.append(report.contract_gate.render_table())
    lines += ["", "## Automated Tests", "", "| Test | Status | Details |",
              "|------|--------|---------|"]
    for t in report.auto_tests:
        lines.append(f"| {t.name} | {'✅' if t.passed else '❌'} | {t.details[:100].replace('|','\\|')} |")
    if report.file_manifest:
        lines += ["", "## File Manifest", "", "```"] + report.file_manifest + ["```"]
    if report.overall_comment:
        lines += ["", "## Overall Comments", "", report.overall_comment]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Grade T1 Task 1")
    ap.add_argument("repo", type=Path)
    ap.add_argument("--student-name", default="")
    ap.add_argument("--student-email", default="")
    ap.add_argument("--grader", default="")
    ap.add_argument("--auto-only", action="store_true")
    ap.add_argument("--output", type=Path, default=None)
    args = ap.parse_args()

    repo = args.repo.resolve()
    if not repo.exists(): print(f"Error: {repo} not found"); sys.exit(1)

    print(f"{'='*60}\n  T1 Task 1 Grader — Image Collection Pipeline\n{'='*60}\n  Repo: {repo}\n")

    sn = args.student_name or input("Student name: ").strip()
    se = args.student_email or input("Student email: ").strip()
    gr = args.grader or input("Grader name: ").strip()

    auto = [
        test_taxonomy_exists(repo), test_taxonomy_quality(repo),
        test_database_list(repo), test_search_pipeline(repo),
        test_search_results(repo), test_collection_page(repo),
        test_collection_json(repo), test_provenance(repo),
        test_license_compliance(repo), test_space_type_coverage(repo),
    ]

    print(f"\n{'='*60}\n  Automated tests\n{'='*60}")
    for r in auto: print(f"  {'✅' if r.passed else '❌'} [{r.weight:>9s}] {r.name}: {r.details}")
    auto_score = compute_auto(auto)
    print(f"\n  Auto: {auto_score}/15")

    # Contract gate
    print(f"\n{'='*60}\n  Contract quality evaluation\n{'='*60}")
    contract_gate = scan_for_contracts(repo, expected_contracts=4)
    print(f"  {contract_gate.summary}")
    for c in contract_gate.contracts_found:
        print(f"    {c.source_file}: {c.quality} "
              f"(sections={c.section_count}/4, tests={c.test_count})")
    if not contract_gate.gate_passed:
        print(f"\n  ⛔ GATE FAILED: {contract_gate.gate_reason}")
        print(f"  ⛔ Student outputs should NOT be integrated.")

    manifest = []
    try:
        d = subprocess.run(["git","diff","--name-only","HEAD"], cwd=str(repo),
                          capture_output=True, text=True, timeout=10)
        if d.stdout.strip(): manifest.extend(d.stdout.strip().split("\n"))
        s = subprocess.run(["git","status","--short"], cwd=str(repo),
                          capture_output=True, text=True, timeout=10)
        for l in s.stdout.strip().split("\n"):
            if l.strip():
                p = l.strip().split(None,1)
                if len(p)==2 and p[1] not in manifest: manifest.append(f"[{p[0]}] {p[1]}")
    except: manifest.append("(git not available)")

    rubric = []
    if not args.auto_only:
        print(f"\n{'='*60}\n  Manual rubric\n{'='*60}")
        for c in RUBRIC: rubric.append(prompt_manual(c))
    else:
        for c in RUBRIC: c.comment = "(auto-only)"; rubric.append(c)

    total = sum(s.points for s in rubric) + auto_score + contract_gate.score
    max_t = sum(s.max_points for s in rubric) + 15 + contract_gate.max_score

    rpt = GradeReport(sn, se, gr,
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        rubric, auto, total, max_t, "", manifest, contract_gate)

    out = args.output or (repo/"160sp"/"rubrics"/"t1"/"GRADE_REPORT_T1_TASK1.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(rpt))

    gate_icon = '✅' if contract_gate.gate_passed else '⛔'
    print(f"\n{'='*60}")
    print(f"  TOTAL: {total}/{max_t}")
    print(f"  Contract gate: {gate_icon} {contract_gate.gate_reason}")
    print(f"  Report: {out}")
    print(f"{'='*60}")


if __name__ == "__main__": main()
