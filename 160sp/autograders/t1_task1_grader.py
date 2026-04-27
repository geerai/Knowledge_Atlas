"""
T1 Task 1 Autograder — Image Collection (75 points)

Validates: space_types.json, image_sources.json, search_pipeline.py,
search_results.json, ka_image_collection.html, collection.json, contracts.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.report import GradeReport
from shared.validators import (
    check_json_loadable, check_required_keys, check_min_items,
    check_each_item_has_keys, check_file_exists, check_python_imports_ok,
    check_python_has_pattern, check_html_has_keyword, check_license_valid,
    check_url_format, count_unique, load_html, check_no_api_keys,
)

TASK_TITLE = "Track 1 · Task 1: Build an Image Collection"
TASK_DESC = (
    "75 points. Build a 500-image collection of openly-licensed "
    "interior photos with full provenance across ≥12 of 15 room types "
    "from ≥3 sources. Deliverables: space_types.json, image_sources.json, "
    "search_pipeline.py, search_results.json, ka_image_collection.html, "
    "collection.json."
)
MAX_POINTS = 75


def grade(submission_dir: str, student_id: str = "unknown") -> GradeReport:
    r = GradeReport(track="t1", task=1, student_id=student_id,
                    max_points=MAX_POINTS, task_title=TASK_TITLE,
                    task_description=TASK_DESC)

    # ── 1. Contracts (20 pts, GATE) ──────────────────────────
    contract_found = False
    for root, dirs, files in os.walk(submission_dir):
        for f in files:
            path = os.path.join(root, f)
            if f.endswith((".md", ".txt", ".json")):
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                        text = fh.read().lower()
                    if "success condition" in text or "contract" in text:
                        contract_found = True
                        break
                except:
                    pass
        if contract_found:
            break

    if contract_found:
        r.add_check("Contracts + tests", 20, "PASS",
                     "Contract/success conditions found in submission",
                     is_gate=True)
        r.strengths.append("Contracts with success conditions present")
    else:
        r.add_check("Contracts + tests", 20, "FAIL",
                     "No contract or success conditions found — CONTRACT GATE FAILED",
                     is_gate=True)
        r.missing.append("No contracts or success conditions found (gate failure)")

    # ── 2. Image sources (10 pts) ────────────────────────────
    src_path = os.path.join(submission_dir, "image_sources.json")
    ok, sources_data, err = check_json_loadable(src_path)
    if ok:
        sources = sources_data.get("sources", sources_data) if isinstance(sources_data, dict) else sources_data
        if isinstance(sources, list) and len(sources) >= 5:
            tested = sum(1 for s in sources if s.get("tested", False))
            if tested >= 3:
                r.add_check("Image sources", 10, "PASS",
                            f"{len(sources)} sources, {tested} tested")
                r.strengths.append(f"{len(sources)} image sources documented, {tested} tested")
            else:
                r.add_check("Image sources", 10, "WARN",
                            f"{len(sources)} sources but only {tested}/3 tested",
                            pts_earned=6)
                r.weaknesses.append(f"Only {tested}/3 sources tested")
        else:
            count = len(sources) if isinstance(sources, list) else 0
            r.add_check("Image sources", 10, "FAIL",
                        f"Only {count} sources (need ≥5)")
            r.weaknesses.append(f"Only {count} image sources (need ≥5)")
    else:
        r.add_check("Image sources", 10, "FAIL", f"image_sources.json: {err}")
        r.missing.append("image_sources.json missing or invalid")

    # ── 3. Search pipeline (10 pts) ──────────────────────────
    pipe_path = os.path.join(submission_dir, "search_pipeline.py")
    if check_file_exists(pipe_path):
        ok, compile_err = check_python_imports_ok(pipe_path)
        with open(pipe_path, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()
        has_sleep = "time.sleep" in source or "sleep(" in source
        api_issues = check_no_api_keys(source)

        if ok and has_sleep and not api_issues:
            r.add_check("Search pipeline", 10, "PASS",
                        "Compiles, has rate limiting, no hardcoded keys")
            r.strengths.append("Search pipeline has rate limiting")
        elif ok:
            detail_parts = []
            if not has_sleep:
                detail_parts.append("no rate limiting (time.sleep)")
                r.weaknesses.append("Search pipeline missing rate limiting")
            if api_issues:
                detail_parts.append("possible hardcoded API keys")
                r.weaknesses.append("Possible hardcoded API keys in source")
            r.add_check("Search pipeline", 10, "WARN",
                        f"Compiles but: {'; '.join(detail_parts)}",
                        pts_earned=6)
        else:
            r.add_check("Search pipeline", 10, "FAIL",
                        f"Compile error: {compile_err[:100]}")
            r.weaknesses.append(f"search_pipeline.py has syntax errors")
    else:
        r.add_check("Search pipeline", 10, "FAIL", "search_pipeline.py not found")
        r.missing.append("search_pipeline.py")

    # ── 4. Collection page (15 pts) ──────────────────────────
    page_path = os.path.join(submission_dir, "ka_image_collection.html")
    html = load_html(page_path)
    if html:
        features = {
            "search/filter": check_html_has_keyword(html, "filter") or check_html_has_keyword(html, "search"),
            "accept/reject": check_html_has_keyword(html, "accept") and check_html_has_keyword(html, "reject"),
            "upload": check_html_has_keyword(html, "upload") or check_html_has_keyword(html, "drop"),
            "progress": check_html_has_keyword(html, "progress") or check_html_has_keyword(html, "/500"),
            "export": check_html_has_keyword(html, "export") or check_html_has_keyword(html, "download"),
        }
        found = sum(features.values())
        missing_features = [k for k, v in features.items() if not v]
        if found >= 4:
            r.add_check("Collection page", 15, "PASS",
                        f"{found}/5 features found")
            r.strengths.append(f"Collection page has {found}/5 required features")
        elif found >= 2:
            r.add_check("Collection page", 15, "WARN",
                        f"{found}/5 features; missing: {', '.join(missing_features)}",
                        pts_earned=8)
            r.weaknesses.append(f"Collection page missing: {', '.join(missing_features)}")
        else:
            r.add_check("Collection page", 15, "FAIL",
                        f"Only {found}/5 features found")
            r.weaknesses.append(f"Collection page has only {found}/5 required features")
    else:
        r.add_check("Collection page", 15, "FAIL", "ka_image_collection.html not found")
        r.missing.append("ka_image_collection.html")

    # ── 5. 500 images (15 pts) ───────────────────────────────
    coll_path = os.path.join(submission_dir, "collection.json")
    ok, coll_data, err = check_json_loadable(coll_path)
    if ok:
        images = coll_data if isinstance(coll_data, list) else coll_data.get("images", [])
        n = len(images)
        required_fields = ["source_page_url", "source_name", "license", "space_type"]
        complete = sum(1 for img in images
                       if all(img.get(f) for f in required_fields))
        room_types = set(img.get("space_type", "") for img in images) - {""}
        sources = set(img.get("source_name", "") for img in images) - {""}

        if n >= 500 and complete >= 490 and len(room_types) >= 12 and len(sources) >= 3:
            r.add_check("500 images", 15, "PASS",
                        f"{n} images, {len(room_types)} types, {len(sources)} sources, "
                        f"{complete} with full provenance")
            r.strengths.append(f"{n} images across {len(room_types)} room types from {len(sources)} sources")
        elif n >= 400:
            pts = 10 if n >= 450 else 7
            issues = []
            if n < 500: issues.append(f"{n}/500 images")
            if len(room_types) < 12: issues.append(f"{len(room_types)}/12 room types")
            if len(sources) < 3: issues.append(f"{len(sources)}/3 sources")
            r.add_check("500 images", 15, "WARN",
                        "; ".join(issues), pts_earned=pts)
            r.weaknesses.append("; ".join(issues))
        else:
            r.add_check("500 images", 15, "FAIL",
                        f"Only {n} images (need ≥500)")
            r.weaknesses.append(f"Only {n}/500 images collected")

        # Repo worthiness
        if n >= 450 and complete >= 440:
            r.add_repo_item("collection.json", "Knowledge_Atlas",
                            "160sp/data/", "needs_review",
                            f"{n} images, {complete} with full provenance")
        elif n >= 500:
            r.add_repo_item("collection.json", "Knowledge_Atlas",
                            "160sp/data/", "ready",
                            f"{n} images, all provenance fields present")
    else:
        r.add_check("500 images", 15, "FAIL", f"collection.json: {err}")
        r.missing.append("collection.json missing or invalid")

    # ── 6. Verification (5 pts) ──────────────────────────────
    # Check for spot-check evidence
    spot_check_found = False
    for root, dirs, files in os.walk(submission_dir):
        for f in files:
            try:
                with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fh:
                    text = fh.read().lower()
                if "spot" in text and "check" in text:
                    spot_check_found = True
                    break
            except:
                pass
        if spot_check_found:
            break

    if spot_check_found:
        r.add_check("Verification", 5, "PASS", "Spot-check evidence found")
    else:
        r.add_check("Verification", 5, "WARN",
                     "No spot-check evidence found", pts_earned=2)
        r.weaknesses.append("No provenance spot-check documented")

    # ── Summary ──────────────────────────────────────────────
    r.summary = _build_summary(r, submission_dir)
    return r


def _build_summary(r: GradeReport, submission_dir: str) -> str:
    parts = []
    for c in r.checks:
        if c.result == "PASS":
            parts.append(f"{c.criterion}: {c.detail}")
        elif c.result == "WARN":
            parts.append(f"{c.criterion}: partial — {c.detail}")
    if parts:
        return "Student submitted: " + ". ".join(parts[:4]) + "."
    return "Submission incomplete — most deliverables missing."


if __name__ == "__main__":
    import sys
    sub_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    sid = sys.argv[2] if len(sys.argv) > 2 else "test_student"
    report = grade(sub_dir, sid)
    print(report.to_markdown())
