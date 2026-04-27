"""T2 Task 2 Autograder — Gap Targeting & Query Generation (60 pts)"""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.report import GradeReport
from shared.validators import check_json_loadable, check_file_exists, check_python_imports_ok, check_sorted_descending
from shared.ruthless import run_ruthless

TASK_TITLE = "Track 2 · Task 2: Gap Targeting & Query Generation"
TASK_DESC = "60 points. Extract knowledge gaps from PNU templates, score by VOI, generate AI Citation + Boolean query pairs."
MAX_POINTS = 60

def grade(submission_dir: str, student_id: str = "unknown") -> GradeReport:
    r = GradeReport(track="t2", task=2, student_id=student_id, max_points=MAX_POINTS, task_title=TASK_TITLE, task_description=TASK_DESC)

    # 1. Gap extraction (15 pts)
    ok, gaps, err = check_json_loadable(os.path.join(submission_dir, "gap_results.json"))
    gap_list = gaps if isinstance(gaps, list) else (gaps.get("gaps",[]) if isinstance(gaps,dict) else []) if ok else []
    n_gaps = len(gap_list)
    if n_gaps >= 10:
        voi_scores = [g.get("voi_score",0) for g in gap_list if isinstance(g,dict)]
        sorted_issue = check_sorted_descending(voi_scores, "VOI scores") if voi_scores else None
        r.add_check("Gap extraction", 15, "PASS", f"{n_gaps} gaps extracted")
        r.strengths.append(f"{n_gaps} gaps with VOI scores")
        if sorted_issue: r.weaknesses.append(sorted_issue.message)
    elif ok:
        r.add_check("Gap extraction", 15, "WARN", f"Only {n_gaps}/10 gaps", pts_earned=8)
    else:
        r.add_check("Gap extraction", 15, "FAIL", f"gap_results.json: {err}")
        r.missing.append("gap_results.json")

    # 2. VOI scoring (10 pts)
    has_voi = all(isinstance(g,dict) and "voi_score" in g for g in gap_list[:10]) if gap_list else False
    r.add_check("VOI scoring", 10, "PASS" if has_voi else ("WARN" if gap_list else "FAIL"),
                f"VOI scores {'present' if has_voi else 'missing'} in gap entries",
                pts_earned=10 if has_voi else (5 if gap_list else 0))

    # 3+4. Query pairs (20 pts)
    ok2, queries, err2 = check_json_loadable(os.path.join(submission_dir, "query_results.json"))
    query_list = queries if isinstance(queries, list) else (queries.get("queries",[]) if isinstance(queries,dict) else []) if ok2 else []
    if query_list:
        good_ai = sum(1 for q in query_list if isinstance(q,dict) and len(q.get("ai_citation_query",""))>50 and q.get("ai_citation_query","").strip().endswith("?"))
        good_bool = sum(1 for q in query_list if isinstance(q,dict) and ("AND" in q.get("boolean_query","") or "OR" in q.get("boolean_query","")) and '"' in q.get("boolean_query",""))
        r.add_check("AI Citation queries", 10, "PASS" if good_ai>=10 else ("WARN" if good_ai>=5 else "FAIL"),
                     f"{good_ai}/{len(query_list)} queries follow 5-component pattern",
                     pts_earned=10 if good_ai>=10 else (6 if good_ai>=5 else 2))
        r.add_check("Boolean queries", 10, "PASS" if good_bool>=10 else ("WARN" if good_bool>=5 else "FAIL"),
                     f"{good_bool}/{len(query_list)} use AND/OR + quoted phrases",
                     pts_earned=10 if good_bool>=10 else (6 if good_bool>=5 else 2))
        if good_ai>=10: r.strengths.append("AI Citation queries well-formed")
        if good_bool<10: r.weaknesses.append(f"Only {good_bool} Boolean queries use proper AND/OR syntax")
    else:
        r.add_check("AI Citation queries", 10, "FAIL", f"query_results.json: {err2 if not ok2 else 'empty'}")
        r.add_check("Boolean queries", 10, "FAIL", "No query data")
        r.missing.append("query_results.json")

    # 5. Spot-check (5 pts)
    spot = any("spot" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt")))
    r.add_check("Spot-check", 5, "PASS" if spot else "WARN", "Manual spot-check " + ("documented" if spot else "not found"), pts_earned=5 if spot else 2)

    # 6. Verification (10 pts)
    r.add_check("Verification questions", 10, "WARN", "Manual review required", pts_earned=5)

    # Ruthless: run gap_extractor
    extractor = os.path.join(submission_dir, "gap_extractor.py")
    if check_file_exists(extractor):
        res = run_ruthless(extractor, ["--help"], timeout_sec=10, cwd=submission_dir)
        r.ruthless_comments.extend(res.comments)
        r.add_repo_item("gap_extractor.py", "Article_Finder", "scripts/", "needs_review" if res.exit_code in (0,2) else "blocked")

    r.summary = f"Gap extraction: {n_gaps} gaps. Queries: {len(query_list)} pairs."
    return r

if __name__ == "__main__":
    print(grade(sys.argv[1] if len(sys.argv)>1 else ".", sys.argv[2] if len(sys.argv)>2 else "test").to_markdown())
