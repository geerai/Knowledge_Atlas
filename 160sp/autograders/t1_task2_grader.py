"""
T1 Task 2 Autograder — Latent Tag Detectors (75 pts)
"""
import os, sys, glob, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.report import GradeReport
from shared.validators import check_file_exists, check_file_under_lines, check_python_imports_ok
from shared.ruthless import check_python_importable

TASK_TITLE = "Track 1 · Task 2: Build Latent Tag Detectors"
TASK_DESC = "75 points. Implement 6 latent-tag detectors with design notes, typed signatures, test suites, implementations ≤150 lines, audit pass, and detector cards."
MAX_POINTS = 75

def grade(submission_dir: str, student_id: str = "unknown") -> GradeReport:
    r = GradeReport(track="t1", task=2, student_id=student_id, max_points=MAX_POINTS, task_title=TASK_TITLE, task_description=TASK_DESC)
    detector_files = glob.glob(os.path.join(submission_dir, "**/detect_*.py"), recursive=True)
    test_files = glob.glob(os.path.join(submission_dir, "**/test_*.py"), recursive=True)
    design_notes = [f for f in glob.glob(os.path.join(submission_dir, "**/*"), recursive=True)
                    if any(kw in os.path.basename(f).lower() for kw in ["design","note","contract"]) and f.endswith((".md",".txt"))]
    card_files = [f for f in glob.glob(os.path.join(submission_dir, "**/*card*"), recursive=True) if f.endswith((".md",".json",".txt"))]

    # 1. Contracts (15 pts, GATE)
    n = len(design_notes)
    r.add_check("Contracts + design notes", 15, "PASS" if n>=6 else ("WARN" if n>=3 else "FAIL"),
                f"{n}/6 design notes found", pts_earned=15 if n>=6 else (8 if n>=3 else 0), is_gate=True)

    # 2. Test suites (15 pts)
    good_tests = sum(1 for tf in test_files if len(re.findall(r"def test_", open(tf, errors="ignore").read())) >= 10)
    r.add_check("Test suites", 15, "PASS" if good_tests>=6 else ("WARN" if good_tests>=3 else "FAIL"),
                f"{good_tests}/6 suites with ≥10 tests", pts_earned=15 if good_tests>=6 else (8 if good_tests>=3 else 0))

    # 3. Implementations (20 pts)
    valid = sum(1 for df in detector_files if check_python_imports_ok(df)[0])
    over = sum(1 for df in detector_files if check_file_under_lines(df, 150))
    r.add_check("Detector implementations", 20, "PASS" if valid>=6 else ("WARN" if valid>=3 else "FAIL"),
                f"{valid}/6 compile; {over} exceed 150 lines", pts_earned=20 if valid>=6 and over==0 else (15 if valid>=6 else (10 if valid>=3 else 0)))

    # 4. Audit (10 pts)
    audit = any("audit" in open(os.path.join(r2,f), errors="ignore").read().lower() for r2,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt",".log")))
    r.add_check("Audit pass", 10, "PASS" if audit else "WARN", "Audit results " + ("present" if audit else "not found"), pts_earned=10 if audit else 3)

    # 5. Cards (5 pts)
    r.add_check("Detector cards", 5, "PASS" if len(card_files)>=6 else "WARN",
                f"{len(card_files)}/6 cards", pts_earned=5 if len(card_files)>=6 else 2)

    # 6. Verification (10 pts)
    r.add_check("Verification", 10, "WARN", "Manual review required", pts_earned=5)

    # Ruthless
    for df in detector_files[:6]:
        r.ruthless_comments.extend(check_python_importable(df).comments)

    if valid >= 6:
        r.add_repo_item("detectors/", "image-tagger", "extractors/", "needs_review")
    r.summary = f"Submitted {valid} detectors, {good_tests} test suites, {n} design notes, {len(card_files)} cards."
    if valid >= 6: r.strengths.append(f"{valid} detectors compile")
    if good_tests >= 6: r.strengths.append("All test suites have ≥10 tests")
    if valid < 6: r.weaknesses.append(f"Only {valid}/6 detectors compile")
    return r

if __name__ == "__main__":
    print(grade(sys.argv[1] if len(sys.argv)>1 else ".", sys.argv[2] if len(sys.argv)>2 else "test").to_markdown())
