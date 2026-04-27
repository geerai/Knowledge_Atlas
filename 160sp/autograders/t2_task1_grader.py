"""T2 Task 1 Autograder — Fix Contribute Page"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.report import GradeReport
from shared.validators import check_file_exists, check_html_has_keyword, load_html, check_python_imports_ok

TASK_TITLE = "Track 2 · Task 1: Fix the Contribute Page"
TASK_DESC = "Wire the classifier into the contribute page so submitted papers get classified, stored, and reported back."
MAX_POINTS = 75

def grade(submission_dir: str, student_id: str = "unknown") -> GradeReport:
    r = GradeReport(track="t2", task=1, student_id=student_id, max_points=MAX_POINTS, task_title=TASK_TITLE, task_description=TASK_DESC)

    # 1. Diagnosis (15 pts)
    diagrams = [f for _,_,fs in os.walk(submission_dir) for f in fs if any(k in f.lower() for k in ["diagram","boxology","flow"])]
    gap_stmt = any("gap" in open(os.path.join(rt,f),errors="ignore").read().lower() and "missing" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt")))
    r.add_check("Diagnosis", 15, "PASS" if len(diagrams)>=2 and gap_stmt else ("WARN" if len(diagrams)>=1 else "FAIL"),
                f"{len(diagrams)} diagrams, gap statement {'found' if gap_stmt else 'missing'}",
                pts_earned=15 if len(diagrams)>=2 and gap_stmt else (8 if len(diagrams)>=1 else 0))

    # 2. Spec quality (15 pts, GATE)
    contract = any(all(k in open(os.path.join(rt,f),errors="ignore").read().lower() for k in ["input","output","success"]) for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt")))
    r.add_check("Spec quality", 15, "PASS" if contract else "FAIL",
                "Contract with I/O/success " + ("found" if contract else "missing — GATE"), is_gate=True)

    # 3. Verification questions (15 pts)
    verif = any("verification" in open(os.path.join(rt,f),errors="ignore").read().lower() or "interrogat" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt")))
    r.add_check("Verification questions", 15, "PASS" if verif else "WARN",
                "Verification log " + ("present" if verif else "not found"), pts_earned=15 if verif else 5)

    # 4. Validation (15 pts)
    html = load_html(os.path.join(submission_dir, "ka_contribute_public.html"))
    if html:
        has_results = check_html_has_keyword(html, "result") or check_html_has_keyword(html, "verdict")
        has_classifier = check_html_has_keyword(html, "classif") or check_html_has_keyword(html, "endpoint")
        r.add_check("Validation", 15, "PASS" if has_results and has_classifier else "WARN",
                     f"Results section: {'✓' if has_results else '✗'}, Classifier: {'✓' if has_classifier else '✗'}",
                     pts_earned=15 if has_results and has_classifier else 8)
        r.add_repo_item("ka_contribute_public.html", "Knowledge_Atlas", "/", "needs_review")
    else:
        r.add_check("Validation", 15, "FAIL", "ka_contribute_public.html not found")
        r.missing.append("ka_contribute_public.html")

    # 5. Diagnosis of failures (10 pts)
    r.add_check("Diagnosis of failures", 10, "WARN", "Manual review required", pts_earned=5)

    # 6. File manifest (5 pts)
    manifest = any("git diff" in open(os.path.join(rt,f),errors="ignore").read() or "git status" in open(os.path.join(rt,f),errors="ignore").read() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt",".log")))
    r.add_check("File manifest", 5, "PASS" if manifest else "WARN",
                "Git manifest " + ("present" if manifest else "not found"), pts_earned=5 if manifest else 2)

    r.summary = f"Contribute page fix submission. Diagrams: {len(diagrams)}, contract: {'yes' if contract else 'no'}."
    if contract: r.strengths.append("Contract with inputs/outputs/success conditions")
    if not contract: r.missing.append("Contract gate: no structured contract found")
    return r

if __name__ == "__main__":
    print(grade(sys.argv[1] if len(sys.argv)>1 else ".", sys.argv[2] if len(sys.argv)>2 else "test").to_markdown())
