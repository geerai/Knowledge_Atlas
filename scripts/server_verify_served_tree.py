#!/usr/bin/env python3
"""
Verify that key served Knowledge Atlas assets match the current tree.

This is intended to run on xrlab from either the staging checkout or the
production tree as part of the release cycle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import ssl
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass
class VerificationConfig:
    profile: str
    repo_root: Path
    site_base_url: str
    auth_health_url: str


@dataclass
class VerificationRow:
    label: str
    path: str
    url: str
    status: str
    detail: str


CRITICAL_FILES = (
    "ka_canonical_navbar.js",
    "ka_user_type.js",
    "ka_user_home.html",
    "ka_reset_password.html",
    "160sp/collect-articles-upload.html",
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("staging", "production"), required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--site-base-url")
    parser.add_argument("--auth-health-url")
    return parser.parse_args(argv)


def default_config(args: argparse.Namespace) -> VerificationConfig:
    if args.profile == "staging":
        return VerificationConfig(
            profile="staging",
            repo_root=args.repo_root.resolve(),
            site_base_url=(args.site_base_url or "https://xrlab.ucsd.edu/staging_KA").rstrip("/"),
            auth_health_url=args.auth_health_url or "http://127.0.0.1:8766/health",
        )
    return VerificationConfig(
        profile="production",
        repo_root=args.repo_root.resolve(),
        site_base_url=(args.site_base_url or "https://xrlab.ucsd.edu/ka").rstrip("/"),
        auth_health_url=args.auth_health_url or "http://127.0.0.1:8765/health",
    )


def read_url(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "KA release verifier"})
    with urllib.request.urlopen(request, timeout=20, context=ssl.create_default_context()) as response:
        return response.read()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def verify_file(config: VerificationConfig, rel_path: str) -> VerificationRow:
    local_path = config.repo_root / rel_path
    url = f"{config.site_base_url}/{rel_path}"
    if not local_path.exists():
        return VerificationRow(rel_path, rel_path, url, "FAIL", "local file missing")

    local_bytes = local_path.read_bytes()
    try:
        remote_bytes = read_url(url)
    except urllib.error.HTTPError as exc:
        return VerificationRow(rel_path, rel_path, url, "FAIL", f"HTTP {exc.code}")
    except Exception as exc:  # pragma: no cover - integration path
        return VerificationRow(rel_path, rel_path, url, "FAIL", str(exc))

    local_hash = sha256_bytes(local_bytes)
    remote_hash = sha256_bytes(remote_bytes)
    if local_hash != remote_hash:
        return VerificationRow(
            rel_path,
            rel_path,
            url,
            "FAIL",
            f"hash mismatch local={local_hash[:12]} remote={remote_hash[:12]}",
        )
    return VerificationRow(rel_path, rel_path, url, "PASS", f"sha256={local_hash[:12]}")


def verify_auth_health(config: VerificationConfig) -> VerificationRow:
    url = config.auth_health_url
    try:
        payload = json.loads(read_url(url).decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return VerificationRow("Auth health payload", "(health)", url, "FAIL", f"HTTP {exc.code}")
    except Exception as exc:  # pragma: no cover - integration path
        return VerificationRow("Auth health payload", "(health)", url, "FAIL", str(exc))

    status_ok = payload.get("status") == "ok" or payload.get("ok") is True
    modules = payload.get("modules")
    article_loaded = payload.get("article_module_loaded") is True
    if status_ok and isinstance(modules, list) and "auth" in modules and "articles" in modules and article_loaded:
        backend = payload.get("article_classifier_backend", "unknown")
        return VerificationRow("Auth health payload", "(health)", url, "PASS", f"modules ok; backend={backend}")
    return VerificationRow("Auth health payload", "(health)", url, "FAIL", f"unexpected payload: {payload}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = default_config(args)
    rows = [verify_auth_health(config)]
    rows.extend(verify_file(config, rel_path) for rel_path in CRITICAL_FILES)

    print("# Knowledge Atlas served-tree verification")
    print()
    print(f"- Profile: `{config.profile}`")
    print(f"- Repo root: `{config.repo_root}`")
    print(f"- Site base URL: `{config.site_base_url}`")
    print(f"- Auth health URL: `{config.auth_health_url}`")
    print()
    print("| Check | Status | Detail |")
    print("| --- | --- | --- |")
    failures = 0
    for row in rows:
        print(f"| {row.label} | {row.status} | {row.detail} |")
        if row.status != "PASS":
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
