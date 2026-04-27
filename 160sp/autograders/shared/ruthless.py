"""
ruthless.py — Run student code in a subprocess with timeout.

Used for the 4 hardest tasks: T1.2 (detectors), T2.2 (gap extractor),
T2.3 (search/abstract), T3.3 (AI front-end DOM check).
"""
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass, field


@dataclass
class RuthlessResult:
    exit_code: int = -1
    stdout: str = ""
    stderr: str = ""
    output_file_exists: bool = False
    output_data: dict | list | None = None
    schema_valid: bool = False
    comments: list[str] = field(default_factory=list)
    timed_out: bool = False


def run_ruthless(script_path: str,
                 args: list[str] | None = None,
                 timeout_sec: int = 30,
                 expected_output_file: str | None = None,
                 expected_keys: list[str] | None = None,
                 cwd: str | None = None,
                 python: str = "python3") -> RuthlessResult:
    """
    Run a student's Python script in a subprocess with timeout.

    1. Execute with subprocess.run, capture stdout/stderr
    2. If expected_output_file: check it was created, load JSON, validate keys
    3. Collect structured comments for each issue found
    """
    result = RuthlessResult()

    if not os.path.isfile(script_path):
        result.comments.append(f"Script not found: {script_path}")
        return result

    cmd = [python, script_path] + (args or [])
    work_dir = cwd or os.path.dirname(script_path) or "."

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=timeout_sec, cwd=work_dir
        )
        result.exit_code = proc.returncode
        result.stdout = proc.stdout[-2000:] if len(proc.stdout) > 2000 else proc.stdout
        result.stderr = proc.stderr[-2000:] if len(proc.stderr) > 2000 else proc.stderr

        if proc.returncode != 0:
            result.comments.append(f"Script exited with code {proc.returncode}")
            # Parse common errors from stderr
            if "ImportError" in proc.stderr or "ModuleNotFoundError" in proc.stderr:
                for line in proc.stderr.split("\n"):
                    if "ImportError" in line or "ModuleNotFoundError" in line:
                        result.comments.append(line.strip())
            elif "SyntaxError" in proc.stderr:
                result.comments.append("SyntaxError in student code")
            elif "FileNotFoundError" in proc.stderr:
                result.comments.append("FileNotFoundError — missing input data")
            else:
                # Last meaningful line of stderr
                err_lines = [l.strip() for l in proc.stderr.strip().split("\n") if l.strip()]
                if err_lines:
                    result.comments.append(f"Error: {err_lines[-1][:200]}")
        else:
            result.comments.append("✅ Script runs without errors")

    except subprocess.TimeoutExpired:
        result.timed_out = True
        result.comments.append(f"⏱️ Script timed out after {timeout_sec}s")
        return result
    except Exception as e:
        result.comments.append(f"Failed to execute: {e}")
        return result

    # Check expected output file
    if expected_output_file:
        out_path = os.path.join(work_dir, expected_output_file)
        if os.path.isfile(out_path):
            result.output_file_exists = True
            result.comments.append(f"✅ Output file created: {expected_output_file}")
            try:
                with open(out_path, "r", encoding="utf-8") as f:
                    result.output_data = json.load(f)
                result.comments.append("✅ Output is valid JSON")

                # Check expected keys
                if expected_keys and isinstance(result.output_data, dict):
                    missing = [k for k in expected_keys if k not in result.output_data]
                    if missing:
                        result.comments.append(
                            f"⚠️ Output missing keys: {', '.join(missing)}")
                    else:
                        result.schema_valid = True
                        result.comments.append("✅ Output has all expected keys")
                elif expected_keys and isinstance(result.output_data, list):
                    if len(result.output_data) > 0 and isinstance(result.output_data[0], dict):
                        missing = [k for k in expected_keys
                                   if k not in result.output_data[0]]
                        if missing:
                            result.comments.append(
                                f"⚠️ First item missing keys: {', '.join(missing)}")
                        else:
                            result.schema_valid = True
                    else:
                        result.comments.append("⚠️ Output is a list but items are not dicts")
                else:
                    result.schema_valid = True  # no keys to check

            except json.JSONDecodeError:
                result.comments.append("❌ Output file is not valid JSON")
            except Exception as e:
                result.comments.append(f"❌ Error reading output: {e}")
        else:
            result.comments.append(f"❌ Expected output file not created: {expected_output_file}")

    return result


def check_python_importable(script_path: str,
                             python: str = "python3",
                             timeout_sec: int = 10) -> RuthlessResult:
    """Try to import a Python file (compile only, no execution)."""
    result = RuthlessResult()
    if not os.path.isfile(script_path):
        result.comments.append(f"Script not found: {script_path}")
        return result

    check_code = f"""
import sys, py_compile
try:
    py_compile.compile('{script_path}', doraise=True)
    print('OK')
except py_compile.PyCompileError as e:
    print(f'COMPILE_ERROR: {{e}}', file=sys.stderr)
    sys.exit(1)
"""
    try:
        proc = subprocess.run(
            [python, "-c", check_code],
            capture_output=True, text=True, timeout=timeout_sec
        )
        result.exit_code = proc.returncode
        if proc.returncode == 0:
            result.comments.append("✅ Python file compiles without errors")
        else:
            result.comments.append(f"❌ Compile error: {proc.stderr.strip()[:200]}")
    except subprocess.TimeoutExpired:
        result.timed_out = True
        result.comments.append("⏱️ Compile check timed out")
    except Exception as e:
        result.comments.append(f"Error: {e}")

    return result
