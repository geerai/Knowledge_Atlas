"""T3 Task 3 Autograder — AI Front-End for Parametric Scene Modification (75 pts)"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.report import GradeReport
from shared.validators import check_html_has_keyword, load_html, check_file_exists

TASK_TITLE = "Track 3 · Task 3: AI Front-End for Parametric Scene Modification"
TASK_DESC = "75 points. Build NL→JSON→3D scene modification tool with validation gate, research presets, and 15-test protocol on 10 models."
MAX_POINTS = 75

def grade(submission_dir: str, student_id: str = "unknown") -> GradeReport:
    r = GradeReport(track="t3", task=3, student_id=student_id, max_points=MAX_POINTS, task_title=TASK_TITLE, task_description=TASK_DESC)

    # 1. Contracts (10 pts GATE)
    contract = any("contract" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt")))
    r.add_check("Contracts + tests", 10, "PASS" if contract else "FAIL",
                "Contracts " + ("found" if contract else "missing — GATE"), is_gate=True)

    # 2. LLM integration (15 pts)
    html = load_html(os.path.join(submission_dir, "ka_vr_ai_modifier.html"))
    if html:
        has_llm = check_html_has_keyword(html, "openai") or check_html_has_keyword(html, "anthropic") or check_html_has_keyword(html, "api") or check_html_has_keyword(html, "llm")
        has_json = check_html_has_keyword(html, "json") and check_html_has_keyword(html, "parse")
        has_wall = check_html_has_keyword(html, "wall_north") or check_html_has_keyword(html, "per-wall") or check_html_has_keyword(html, "wall_id")
        r.add_check("LLM integration", 15, "PASS" if has_llm and has_json else ("WARN" if has_llm else "FAIL"),
                     f"LLM call: {'✓' if has_llm else '✗'}, JSON parse: {'✓' if has_json else '✗'}, per-wall: {'✓' if has_wall else '✗'}",
                     pts_earned=15 if has_llm and has_json and has_wall else (10 if has_llm and has_json else (5 if has_llm else 0)))
        if has_llm and has_json: r.strengths.append("LLM integration with constrained JSON output")
        if not has_wall: r.weaknesses.append("Per-wall addressing not detected")

        # 3. Validation gate (10 pts)
        has_gate = check_html_has_keyword(html, "viability") or check_html_has_keyword(html, "validation") or check_html_has_keyword(html, "supported")
        r.add_check("Validation gate", 10, "PASS" if has_gate else "WARN",
                     "Viability check " + ("present" if has_gate else "not detected"),
                     pts_earned=10 if has_gate else 3)
        if has_gate: r.strengths.append("Validation gate checks viability before applying")

        # Check presets
        preset_matches = re.findall(r'preset|meyers.levy|ceiling.height.*condition|research.*scenario', html, re.IGNORECASE)
        n_presets = min(len(preset_matches), 10)
        r.add_check("Research presets", 10, "PASS" if n_presets>=5 else ("WARN" if n_presets>=2 else "FAIL"),
                     f"~{n_presets} preset references detected",
                     pts_earned=10 if n_presets>=5 else (5 if n_presets>=2 else 0))

        # Check material library
        materials = re.findall(r'wood|brick|concrete|glass|marble|tile|plaster|carpet|slate|metal', html, re.IGNORECASE)
        unique_mats = len(set(m.lower() for m in materials))
        has_history = check_html_has_keyword(html, "history") or check_html_has_keyword(html, "log")

        r.add_repo_item("ka_vr_ai_modifier.html", "Knowledge_Atlas", "160sp/apps/", "needs_review")
    else:
        r.add_check("LLM integration", 15, "FAIL", "ka_vr_ai_modifier.html not found")
        r.add_check("Validation gate", 10, "FAIL", "No HTML file")
        r.add_check("Research presets", 10, "FAIL", "No HTML file")
        r.missing.append("ka_vr_ai_modifier.html")

    # 4. Model coverage / 15-test (15 pts)
    test_results = any("15-test" in open(os.path.join(rt,f),errors="ignore").read().lower() or "test protocol" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt",".csv")))
    r.add_check("Model coverage", 15, "PASS" if test_results else "WARN",
                "15-test protocol " + ("documented" if test_results else "not found"), pts_earned=15 if test_results else 5)

    # 5. Ruthless testing (10 pts)
    ruthless = any("adversarial" in open(os.path.join(rt,f),errors="ignore").read().lower() or "ruthless" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt")))
    r.add_check("Ruthless testing", 10, "PASS" if ruthless else "WARN",
                "Adversarial testing " + ("documented" if ruthless else "not found"), pts_earned=10 if ruthless else 3)

    # 6. Polish (5 pts)
    r.add_check("Polish", 5, "WARN", "Manual review: slider sync, reset, export, history, FPS", pts_earned=3)

    # Demo video
    video = any(f.endswith((".mp4",".webm",".mov")) for _,_,fs in os.walk(submission_dir) for f in fs)
    if video: r.strengths.append("Demo video included")
    else: r.weaknesses.append("No demo video found")

    r.summary = f"AI front-end submission with {'HTML file' if html else 'no HTML'}."
    return r

if __name__ == "__main__":
    print(grade(sys.argv[1] if len(sys.argv)>1 else ".", sys.argv[2] if len(sys.argv)>2 else "test").to_markdown())
