"""T3 Task 1 Autograder — Model Collection (75 pts)"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.report import GradeReport
from shared.validators import check_json_loadable, check_file_exists, check_dir_exists, count_files

TASK_TITLE = "Track 3 · Task 1: Build a 3D Model Library"
TASK_DESC = "75 points. Collect ≥20 VR-ready 3D models with mesh annotations, viability scores, and ruthless validation."
MAX_POINTS = 75

def grade(submission_dir: str, student_id: str = "unknown") -> GradeReport:
    r = GradeReport(track="t3", task=1, student_id=student_id, max_points=MAX_POINTS, task_title=TASK_TITLE, task_description=TASK_DESC)

    # 1. Contracts (15 pts GATE)
    contract = any("contract" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt")))
    r.add_check("Contracts + tests", 15, "PASS" if contract else "FAIL",
                "Contracts " + ("found" if contract else "missing — GATE"), is_gate=True)

    # 2. Model sources (10 pts)
    ok, src, err = check_json_loadable(os.path.join(submission_dir, "model_sources.json"))
    if ok:
        sources = src.get("sources", src) if isinstance(src,dict) else src
        sources = sources if isinstance(sources, list) else []
        tested = sum(1 for s in sources if isinstance(s,dict) and s.get("tested"))
        r.add_check("Model sources", 10, "PASS" if len(sources)>=5 and tested>=3 else "WARN",
                     f"{len(sources)} sources, {tested} tested",
                     pts_earned=10 if len(sources)>=5 and tested>=3 else (6 if len(sources)>=3 else 2))
    else:
        r.add_check("Model sources", 10, "FAIL", f"model_sources.json: {err}")
        r.missing.append("model_sources.json")

    # 3. Model catalog (15 pts)
    # Look for catalog as JSON or CSV
    catalog_files = glob.glob(os.path.join(submission_dir, "*catalog*")) + glob.glob(os.path.join(submission_dir, "*models*.*"))
    model_dir = os.path.join(submission_dir, "models")
    n_models = count_files(model_dir, ".glb") + count_files(model_dir, ".gltf") if check_dir_exists(model_dir) else 0
    # Also check root
    n_models += count_files(submission_dir, ".glb") + count_files(submission_dir, ".gltf")

    if n_models >= 20:
        r.add_check("Model catalog", 15, "PASS", f"{n_models} model files found")
        r.strengths.append(f"{n_models} 3D model files present")
    elif n_models >= 10:
        r.add_check("Model catalog", 15, "WARN", f"Only {n_models}/20 models", pts_earned=8)
        r.weaknesses.append(f"Only {n_models}/20 model files")
    else:
        r.add_check("Model catalog", 15, "FAIL", f"Only {n_models}/20 models")
        r.weaknesses.append(f"Only {n_models} model files (need ≥20)")

    # 4. Mesh annotations (15 pts)
    roles_dir = os.path.join(submission_dir, "mesh_roles")
    role_files = glob.glob(os.path.join(roles_dir, "*.json")) if check_dir_exists(roles_dir) else []
    valid_roles = 0
    wall_ids_ok = 0
    for rf in role_files:
        ok2, data, _ = check_json_loadable(rf)
        if ok2 and isinstance(data, dict):
            meshes = data.get("meshes", {})
            has_dims = "room_dimensions" in data
            walls = [v for v in meshes.values() if isinstance(v,dict) and v.get("role")=="wall"]
            has_wall_ids = all(w.get("wall_id") for w in walls)
            if meshes and has_dims:
                valid_roles += 1
            if has_wall_ids:
                wall_ids_ok += 1

    r.add_check("Mesh annotations", 15, "PASS" if valid_roles>=15 else ("WARN" if valid_roles>=8 else "FAIL"),
                f"{valid_roles}/{len(role_files)} valid mesh_roles, {wall_ids_ok} with wall_ids",
                pts_earned=15 if valid_roles>=15 else (10 if valid_roles>=8 else (5 if valid_roles>=3 else 0)))

    if valid_roles >= 10:
        r.add_repo_item("mesh_roles/", "Knowledge_Atlas", "160sp/data/vr_models/", "needs_review",
                        f"{valid_roles} valid annotation files")
        r.strengths.append(f"{valid_roles} mesh annotation files with room dimensions")
    if wall_ids_ok < valid_roles:
        r.weaknesses.append(f"Only {wall_ids_ok}/{valid_roles} annotations have per-wall IDs")

    # 5. Ruthless validation (10 pts)
    ruthless = any("ruthless" in open(os.path.join(rt,f),errors="ignore").read().lower() for rt,_,fs in os.walk(submission_dir) for f in fs if f.endswith((".md",".txt")))
    r.add_check("Ruthless validation", 10, "PASS" if ruthless else "WARN",
                "Ruthless report " + ("present" if ruthless else "not found"), pts_earned=10 if ruthless else 3)

    # 6. Verification (10 pts)
    r.add_check("Verification", 10, "WARN", "Manual review required", pts_earned=5)

    r.summary = f"{n_models} models, {valid_roles} mesh annotations, {len(role_files)} role files."
    return r

if __name__ == "__main__":
    print(grade(sys.argv[1] if len(sys.argv)>1 else ".", sys.argv[2] if len(sys.argv)>2 else "test").to_markdown())
