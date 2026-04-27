"""
validators.py — Shared validation functions for all 9 autograders.

Covers JSON schema, file existence, HTML DOM patterns, provenance,
and data quality checks.
"""
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Issue:
    level: str  # "error", "warning", "info"
    message: str


# ── JSON ─────────────────────────────────────────────────────
def check_json_loadable(path: str) -> tuple[bool, Any, str]:
    """Load a JSON file. Returns (ok, data, error_message)."""
    if not os.path.isfile(path):
        return False, None, f"File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return True, data, ""
    except json.JSONDecodeError as e:
        return False, None, f"Invalid JSON: {e}"
    except Exception as e:
        return False, None, f"Error reading file: {e}"


def check_required_keys(data: dict, keys: list[str]) -> list[Issue]:
    """Check that a dict has all required keys."""
    issues = []
    for k in keys:
        if k not in data:
            issues.append(Issue("error", f"Missing required key: '{k}'"))
    return issues


def check_min_items(data, min_n: int, label: str) -> Issue | None:
    """Check that a list or dict has at least min_n items."""
    count = len(data) if data else 0
    if count < min_n:
        return Issue("error", f"{label}: expected ≥ {min_n} items, found {count}")
    return None


def check_each_item_has_keys(items: list[dict], keys: list[str],
                              label: str = "item") -> list[Issue]:
    """Check that every item in a list has the required keys."""
    issues = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            issues.append(Issue("error", f"{label}[{i}]: expected dict, got {type(item).__name__}"))
            continue
        for k in keys:
            if k not in item:
                issues.append(Issue("warning", f"{label}[{i}]: missing key '{k}'"))
    return issues


# ── File system ──────────────────────────────────────────────
def check_file_exists(path: str) -> bool:
    return os.path.isfile(path)


def check_dir_exists(path: str) -> bool:
    return os.path.isdir(path)


def check_dir_has_min_files(dir_path: str, ext: str, min_n: int) -> Issue | None:
    """Check that a directory has at least min_n files with given extension."""
    if not os.path.isdir(dir_path):
        return Issue("error", f"Directory not found: {dir_path}")
    files = [f for f in os.listdir(dir_path) if f.endswith(ext)]
    if len(files) < min_n:
        return Issue("error",
                     f"Expected ≥ {min_n} {ext} files in {dir_path}, found {len(files)}")
    return None


def check_file_under_lines(path: str, max_lines: int) -> Issue | None:
    """Check that a file has at most max_lines lines."""
    if not os.path.isfile(path):
        return Issue("error", f"File not found: {path}")
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        count = sum(1 for _ in f)
    if count > max_lines:
        return Issue("warning", f"{path}: {count} lines (max {max_lines})")
    return None


def count_files(dir_path: str, ext: str = "") -> int:
    """Count files in a directory, optionally filtered by extension."""
    if not os.path.isdir(dir_path):
        return 0
    if ext:
        return len([f for f in os.listdir(dir_path) if f.endswith(ext)])
    return len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])


# ── HTML DOM (regex, no browser) ─────────────────────────────
def load_html(path: str) -> str | None:
    """Load an HTML file as a string."""
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def check_html_has_element(html: str, tag: str,
                            attrs: dict | None = None) -> bool:
    """Check if HTML contains an element with given tag and attributes."""
    if attrs:
        for attr, val in attrs.items():
            pattern = rf"<{tag}\b[^>]*{attr}\s*=\s*[\"']{val}[\"'][^>]*>"
            if re.search(pattern, html, re.IGNORECASE):
                return True
        return False
    return bool(re.search(rf"<{tag}\b", html, re.IGNORECASE))


def check_html_has_pattern(html: str, pattern: str) -> bool:
    """Check if HTML contains a regex pattern."""
    return bool(re.search(pattern, html, re.IGNORECASE))


def check_html_has_input_type(html: str, input_type: str) -> bool:
    """Check if HTML has an input of a given type."""
    return bool(re.search(
        rf'<input\b[^>]*type\s*=\s*["\']?{input_type}["\']?',
        html, re.IGNORECASE
    ))


def check_html_has_keyword(html: str, keyword: str) -> bool:
    """Check if keyword appears anywhere in HTML (including scripts)."""
    return keyword.lower() in html.lower()


# ── Source code checks ───────────────────────────────────────
def check_no_api_keys(source: str) -> list[Issue]:
    """Check that source code doesn't contain hardcoded API keys."""
    issues = []
    patterns = [
        (r'["\']sk-[a-zA-Z0-9]{20,}["\']', "Possible OpenAI API key"),
        (r'["\'][a-f0-9]{32,}["\']', "Possible hardcoded hex key"),
        (r'api_key\s*=\s*["\'][^"\']{10,}["\']', "Hardcoded api_key assignment"),
        (r'SERPAPI_KEY\s*=\s*["\'][^"\']+["\']', "Hardcoded SerpAPI key"),
    ]
    for pat, msg in patterns:
        if re.search(pat, source):
            issues.append(Issue("warning", msg))
    return issues


def check_python_imports_ok(path: str) -> tuple[bool, str]:
    """Check that a Python file can be parsed (not executed)."""
    if not os.path.isfile(path):
        return False, f"File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        compile(source, path, "exec")
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"


def check_python_has_pattern(path: str, pattern: str) -> bool:
    """Check if a Python file contains a regex pattern."""
    if not os.path.isfile(path):
        return False
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return bool(re.search(pattern, f.read()))


# ── Provenance ───────────────────────────────────────────────
VALID_LICENSES = {
    "cc0", "cc-by", "cc-by-sa", "cc-by-nc", "cc-by-nc-sa",
    "public domain", "unsplash license", "pexels license",
    "creative commons", "mit", "apache",
}


def check_license_valid(license_str: str) -> bool:
    """Check that a licence string looks valid."""
    if not license_str:
        return False
    return any(lic in license_str.lower() for lic in VALID_LICENSES)


def check_url_format(url: str) -> bool:
    """Basic URL format check (not reachability)."""
    return bool(re.match(r'https?://', url))


# ── Data quality ─────────────────────────────────────────────
def check_distribution_plausible(values: list[float],
                                  min_mean: float, max_mean: float,
                                  label: str) -> Issue | None:
    """Check that mean of values falls in a plausible range."""
    if not values:
        return Issue("error", f"{label}: no values to check")
    mean = sum(values) / len(values)
    if mean < min_mean or mean > max_mean:
        return Issue("warning",
                     f"{label}: mean={mean:.2f} outside plausible range "
                     f"[{min_mean}, {max_mean}]")
    return None


def check_sorted_descending(values: list[float], label: str) -> Issue | None:
    """Check that values are sorted descending."""
    for i in range(len(values) - 1):
        if values[i] < values[i + 1]:
            return Issue("warning",
                         f"{label}: not sorted descending (index {i}: "
                         f"{values[i]} < {values[i + 1]})")
    return None


def count_unique(items: list, key=None) -> int:
    """Count unique items, optionally by a key function."""
    if key:
        return len(set(key(item) for item in items))
    return len(set(items))


def count_matching(items: list[dict], key: str, value) -> int:
    """Count items where item[key] == value."""
    return sum(1 for item in items if item.get(key) == value)
