#!/usr/bin/env python3
"""Link checker for CI: external URLs + local markdown file references."""
from __future__ import annotations

import concurrent.futures
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlparse

ROOT = Path(__file__).resolve().parents[1]
SCAN = [
    ROOT / "roadmap" / "weeks",
    ROOT / "docs",
    ROOT / "docs" / "cheatsheets",
]
CTX = ssl.create_default_context()
UA = "web-roadmap-link-check/1.0"
TIMEOUT = 20
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
URL_RE = re.compile(r"https?://[^\s)\]\"<>]+")


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for base in SCAN:
        if base.is_dir():
            files.extend(sorted(base.glob("*.md")))
    return files


def collect_external_urls(files: list[Path]) -> set[str]:
    urls: set[str] = set()
    for path in files:
        text = path.read_text(encoding="utf-8")
        urls.update(URL_RE.findall(text))
    return {u.rstrip(".,;`)'\"") for u in urls if "localhost" not in u}


def collect_local_links(files: list[Path]) -> list[tuple[Path, str, Path]]:
    refs: list[tuple[Path, str, Path]] = []
    for path in files:
        for raw in LINK_RE.findall(path.read_text(encoding="utf-8")):
            target = raw.strip()
            if not target or target.startswith(("#", "mailto:", "http://", "https://")):
                continue
            clean, _frag = urldefrag(unquote(target))
            if clean.startswith("/"):
                continue
            resolved = (path.parent / clean).resolve()
            refs.append((path, target, resolved))
    return refs


def check_external(url: str) -> tuple[str, bool, str]:
    headers = {"User-Agent": UA}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=CTX) as resp:
                code = resp.status
            if code in (200, 403, 429):
                return url, True, str(code)
            return url, False, str(code)
        except urllib.error.HTTPError as e:
            if e.code in (200, 403, 429):
                return url, True, str(e.code)
            if method == "HEAD" and e.code in (405, 501):
                continue
            return url, False, f"HTTP {e.code}"
        except Exception as e:
            if method == "HEAD":
                continue
            return url, False, type(e).__name__
    return url, False, "failed"


def main() -> int:
    files = markdown_files()
    external = sorted(collect_external_urls(files))
    local = collect_local_links(files)

    bad_external: list[tuple[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        for url, ok, info in pool.map(check_external, external):
            if not ok:
                bad_external.append((url, info))

    bad_local: list[tuple[str, str, str]] = []
    for src, target, resolved in local:
        if not resolved.exists():
            bad_local.append((str(src.relative_to(ROOT)), target, str(resolved.relative_to(ROOT))))

    print(f"Checked {len(external)} external URLs, {len(local)} local refs")
    if bad_external:
        print(f"External failures: {len(bad_external)}")
        for url, info in sorted(bad_external):
            print(f"  [{info}] {url}")
    if bad_local:
        print(f"Local failures: {len(bad_local)}")
        for src, target, resolved in bad_local:
            print(f"  [{src}] {target} -> missing {resolved}")

    return 1 if bad_external or bad_local else 0


if __name__ == "__main__":
    sys.exit(main())
