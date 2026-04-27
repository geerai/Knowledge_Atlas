"""T1 Task 3 Autograder — Image Viewer (75 pts)"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.report import GradeReport
from shared.validators import check_json_loadable, check_html_has_keyword, load_html, check_distribution_plausible

TASK_TITLE = "Track 1 · Task 3: Annotate Collection & Build Image Viewer"
TASK_DESC = "75 points. Run 6 detectors on 500 images → annotations.json. Build standalone HTML viewer with tag-mode and effect-mode browsing."
MAX_POINTS = 75

def grade(submission_dir: str, student_id: str = "unknown") -> GradeReport:
    r = GradeReport(track="t1", task=3, student_id=student_id, max_points=MAX_POINTS, task_title=TASK_TITLE, task_description=TASK_DESC)

    # 1. Contracts (10 pts GATE)
    contract = any("contract" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt")))
    r.add_check("Contracts + tests", 10, "PASS" if contract else "FAIL", "Contracts " + ("found" if contract else "missing — GATE"), is_gate=True)

    # 2. Batch annotation (15 pts)
    ok, ann, err = check_json_loadable(os.path.join(submission_dir, "annotations.json"))
    if ok and isinstance(ann, dict):
        images = ann.get("images", {})
        n = len(images)
        has_errors = "errors" in ann
        has_stats = "stats" in ann
        if n >= 490 and has_errors and has_stats:
            r.add_check("Batch annotation", 15, "PASS", f"{n} images annotated, errors+stats present")
            r.strengths.append(f"{n} images annotated with error tracking")
            # Check score distributions
            detectors = ann.get("detectors", [])
            for det in detectors[:3]:
                vals = [img["tags"][det]["value"] for img in images.values() if det in img.get("tags",{})]
                issue = check_distribution_plausible(vals, 0.5, 3.5, det)
                if issue: r.weaknesses.append(issue.message)
        elif n >= 400:
            r.add_check("Batch annotation", 15, "WARN", f"{n}/500 images", pts_earned=10)
            r.weaknesses.append(f"Only {n}/500 images annotated")
        else:
            r.add_check("Batch annotation", 15, "FAIL", f"Only {n} images annotated")
        r.add_repo_item("annotations.json", "Knowledge_Atlas", "160sp/data/annotations/", "needs_review" if n>=490 else "blocked")
    else:
        r.add_check("Batch annotation", 15, "FAIL", f"annotations.json: {err}")
        r.missing.append("annotations.json")

    # 3. Scale fixes (10 pts)
    batch_report = any("batch" in f.lower() and "report" in f.lower() for _,_,fs in os.walk(submission_dir) for f in fs)
    r.add_check("Scale fixes", 10, "PASS" if batch_report else "WARN",
                "Batch report " + ("present" if batch_report else "not found"), pts_earned=10 if batch_report else 4)

    # 4+5. Viewer (30 pts combined)
    html = load_html(os.path.join(submission_dir, "ka_image_viewer.html"))
    if html:
        tag_mode = check_html_has_keyword(html, "tag") and check_html_has_keyword(html, "domain")
        effect_mode = check_html_has_keyword(html, "effect") and check_html_has_keyword(html, "outcome")
        grid = check_html_has_keyword(html, "grid") or check_html_has_keyword(html, "thumbnail")
        detail = check_html_has_keyword(html, "detail") or check_html_has_keyword(html, "provenance")
        r.add_check("Tag browser", 15, "PASS" if tag_mode and grid else "WARN",
                     f"Tag mode: {'✓' if tag_mode else '✗'}, Grid: {'✓' if grid else '✗'}",
                     pts_earned=15 if tag_mode and grid else 8)
        r.add_check("Effect browser", 15, "PASS" if effect_mode else "WARN",
                     f"Effect mode: {'✓' if effect_mode else '✗'}",
                     pts_earned=15 if effect_mode else 5)
        r.add_repo_item("ka_image_viewer.html", "Knowledge_Atlas", "160sp/apps/", "needs_review")
        if tag_mode: r.strengths.append("Tag browsing mode implemented")
        if not effect_mode: r.weaknesses.append("Effect browsing mode weak or missing")
    else:
        r.add_check("Tag browser", 15, "FAIL", "ka_image_viewer.html not found")
        r.add_check("Effect browser", 15, "FAIL", "ka_image_viewer.html not found")
        r.missing.append("ka_image_viewer.html")

    # 6. Polish (10 pts — manual)
    r.add_check("Image detail + polish", 10, "WARN", "Manual review required", pts_earned=5)
    r.summary = f"Submitted annotations.json and viewer HTML. Score: {r.total_earned:.0f}/{MAX_POINTS}."
    return r

if __name__ == "__main__":
    print(grade(sys.argv[1] if len(sys.argv)>1 else ".", sys.argv[2] if len(sys.argv)>2 else "test").to_markdown())
