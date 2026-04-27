"""T3 Task 2 Autograder — VR Conversion & Manual Factor Testing (75 pts)"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.report import GradeReport
from shared.validators import check_html_has_keyword, load_html, count_files, check_dir_exists

TASK_TITLE = "Track 3 · Task 2: VR Conversion & Manual Factor Testing"
TASK_DESC = "75 points. Build A-Frame viewer with sliders for 8 factors, test 10 models, produce factor viability matrix with 80+ screenshots."
MAX_POINTS = 75

def grade(submission_dir: str, student_id: str = "unknown") -> GradeReport:
    r = GradeReport(track="t3", task=2, student_id=student_id, max_points=MAX_POINTS, task_title=TASK_TITLE, task_description=TASK_DESC)

    # 1. Contracts (10 pts GATE)
    contract = any("contract" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt")))
    r.add_check("Contracts + tests", 10, "PASS" if contract else "FAIL",
                "Contracts " + ("found" if contract else "missing — GATE"), is_gate=True)

    # 2. Viewer (20 pts)
    html = load_html(os.path.join(submission_dir, "ka_vr_viewer.html"))
    if html:
        features = {
            "slider/range": check_html_has_keyword(html, "range") or check_html_has_keyword(html, "slider"),
            "wall selector": check_html_has_keyword(html, "wall") and (check_html_has_keyword(html, "select") or check_html_has_keyword(html, "north")),
            "material swatch": check_html_has_keyword(html, "material") or check_html_has_keyword(html, "swatch"),
            "FPS counter": check_html_has_keyword(html, "fps"),
            "ceiling height": check_html_has_keyword(html, "ceiling"),
            "light/CCT": check_html_has_keyword(html, "temperature") or check_html_has_keyword(html, "cct") or check_html_has_keyword(html, "kelvin"),
            "HDRI/env map": check_html_has_keyword(html, "hdri") or check_html_has_keyword(html, "environment") or check_html_has_keyword(html, "hdr"),
        }
        found = sum(features.values())
        miss = [k for k,v in features.items() if not v]
        r.add_check("Viewer functionality", 20, "PASS" if found>=5 else ("WARN" if found>=3 else "FAIL"),
                     f"{found}/7 features: {', '.join(k for k,v in features.items() if v)}",
                     pts_earned=20 if found>=5 else (12 if found>=3 else 5))
        if found>=5: r.strengths.append(f"Viewer has {found}/7 key features")
        if miss: r.weaknesses.append(f"Missing viewer features: {', '.join(miss)}")
        r.add_repo_item("ka_vr_viewer.html", "Knowledge_Atlas", "160sp/apps/", "needs_review")
    else:
        r.add_check("Viewer functionality", 20, "FAIL", "ka_vr_viewer.html not found")
        r.missing.append("ka_vr_viewer.html")

    # 3. Model coverage (15 pts)
    # Check for viability matrix in any doc
    matrix_found = any("viability" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt",".csv")))
    r.add_check("Model coverage", 15, "PASS" if matrix_found else "WARN",
                "Viability matrix " + ("found" if matrix_found else "not found"), pts_earned=15 if matrix_found else 5)

    # 4. Factor viability matrix (15 pts)
    r.add_check("Factor viability matrix", 15, "PASS" if matrix_found else "WARN",
                "Matrix documentation " + ("present" if matrix_found else "needs review"), pts_earned=15 if matrix_found else 5)

    # 5. Ruthless validation (10 pts)
    ruthless = any("ruthless" in open(os.path.join(rt,f),errors="ignore").read().lower() or "12-test" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt")))
    r.add_check("Ruthless validation", 10, "PASS" if ruthless else "WARN",
                "12-test protocol " + ("documented" if ruthless else "not found"), pts_earned=10 if ruthless else 3)

    # 6. Screenshots (5 pts)
    screenshot_dirs = [d for d in ["screenshots","images","before_after"] if check_dir_exists(os.path.join(submission_dir,d))]
    n_screenshots = sum(count_files(os.path.join(submission_dir,d), ".png") + count_files(os.path.join(submission_dir,d), ".jpg") for d in screenshot_dirs)
    r.add_check("Verification", 5, "PASS" if n_screenshots>=80 else ("WARN" if n_screenshots>=20 else "FAIL"),
                f"{n_screenshots} screenshots", pts_earned=5 if n_screenshots>=80 else (3 if n_screenshots>=20 else 1))

    r.summary = f"VR viewer with {'viewer file' if html else 'no viewer'}, {n_screenshots} screenshots."
    return r

if __name__ == "__main__":
    print(grade(sys.argv[1] if len(sys.argv)>1 else ".", sys.argv[2] if len(sys.argv)>2 else "test").to_markdown())
