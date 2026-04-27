"""T2 Task 3 Autograder — Search Execution & Abstract-First Triage (75 pts)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.report import GradeReport
from shared.validators import check_json_loadable, check_file_exists, check_html_has_keyword, load_html, check_python_imports_ok
from shared.ruthless import run_ruthless

TASK_TITLE = "Track 2 · Task 3: Search Execution & Abstract-First Triage"
TASK_DESC = "75 points. Run SerpAPI searches, collect abstracts via fallback chain, triage by classifier+VOI, produce PRISMA funnel dashboard."
MAX_POINTS = 75

def grade(submission_dir: str, student_id: str = "unknown") -> GradeReport:
    r = GradeReport(track="t2", task=3, student_id=student_id, max_points=MAX_POINTS, task_title=TASK_TITLE, task_description=TASK_DESC)

    # 1. SerpAPI integration (10 pts)
    runner = os.path.join(submission_dir, "search_runner.py")
    if check_file_exists(runner):
        ok, err = check_python_imports_ok(runner)
        with open(runner, "r", errors="ignore") as f: src = f.read()
        has_scholar = "google_scholar" in src
        r.add_check("SerpAPI integration", 10, "PASS" if ok and has_scholar else "WARN",
                     f"Compiles: {'✓' if ok else '✗'}, google_scholar engine: {'✓' if has_scholar else '✗'}",
                     pts_earned=10 if ok and has_scholar else 5)
        if has_scholar: r.strengths.append("Uses google_scholar engine correctly")
    else:
        r.add_check("SerpAPI integration", 10, "FAIL", "search_runner.py not found")
        r.missing.append("search_runner.py")

    # 2. Abstract collection (15 pts)
    collector = os.path.join(submission_dir, "abstract_collector.py")
    if check_file_exists(collector):
        with open(collector, "r", errors="ignore") as f: src = f.read()
        apis = sum(1 for api in ["semantic_scholar","crossref","pubmed","openalex"] if api.lower() in src.lower())
        r.add_check("Abstract collection", 15, "PASS" if apis>=3 else "WARN",
                     f"{apis}/4 API sources in fallback chain",
                     pts_earned=15 if apis>=3 else (8 if apis>=2 else 4))
        if apis>=3: r.strengths.append(f"Fallback chain covers {apis}/4 abstract sources")
        r.add_repo_item("abstract_collector.py", "Article_Finder", "scripts/", "needs_review")
    else:
        r.add_check("Abstract collection", 15, "FAIL", "abstract_collector.py not found")
        r.missing.append("abstract_collector.py")

    # 3. Triage (15 pts)
    ok, triage, err = check_json_loadable(os.path.join(submission_dir, "triage_results.json"))
    if ok:
        items = triage if isinstance(triage, list) else triage.get("results", []) if isinstance(triage, dict) else []
        decisions = set(i.get("decision","") for i in items if isinstance(i,dict))
        expected = {"ACCEPT","EDGE_CASE","REJECT","MISSING_ABSTRACT","DUPLICATE"}
        coverage = len(decisions & expected)
        r.add_check("Abstract triage", 15, "PASS" if coverage>=3 else "WARN",
                     f"{len(items)} papers triaged, {coverage}/5 decision types used",
                     pts_earned=15 if coverage>=3 else 8)
    else:
        r.add_check("Abstract triage", 15, "FAIL", f"triage_results.json: {err}")
        r.missing.append("triage_results.json")

    # 4. PRISMA funnel (10 pts)
    html = load_html(os.path.join(submission_dir, "ka_topic_proposer.html"))
    if html:
        has_prisma = check_html_has_keyword(html, "prisma") or check_html_has_keyword(html, "funnel")
        has_numbers = check_html_has_keyword(html, "identified") or check_html_has_keyword(html, "screened")
        r.add_check("PRISMA funnel", 10, "PASS" if has_prisma and has_numbers else "WARN",
                     f"PRISMA: {'✓' if has_prisma else '✗'}, numbers: {'✓' if has_numbers else '✗'}",
                     pts_earned=10 if has_prisma and has_numbers else 5)
        r.add_repo_item("ka_topic_proposer.html", "Knowledge_Atlas", "160sp/apps/", "needs_review")
    else:
        r.add_check("PRISMA funnel", 10, "FAIL", "ka_topic_proposer.html not found")
        r.missing.append("PRISMA dashboard")

    # 5. End-to-end trace (10 pts)
    trace = any("trace" in open(os.path.join(rt,f),errors="ignore").read().lower() or "end-to-end" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt")))
    r.add_check("End-to-end trace", 10, "PASS" if trace else "WARN",
                "Trace " + ("documented" if trace else "not found"), pts_earned=10 if trace else 3)

    # 6. Null results (5 pts)
    r.add_check("Null results + MISSING_ABSTRACT", 5, "WARN", "Manual review", pts_earned=3)

    # 7. Verification (10 pts)
    r.add_check("Verification questions", 10, "WARN", "Manual review required", pts_earned=5)

    # Ruthless
    if check_file_exists(collector):
        res = run_ruthless(collector, ["--help"], timeout_sec=10, cwd=submission_dir)
        r.ruthless_comments.extend(res.comments)

    r.summary = f"Search pipeline submission with triage results and PRISMA dashboard."
    return r

if __name__ == "__main__":
    print(grade(sys.argv[1] if len(sys.argv)>1 else ".", sys.argv[2] if len(sys.argv)>2 else "test").to_markdown())
