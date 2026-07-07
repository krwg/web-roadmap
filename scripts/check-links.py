#!/usr/bin/env python3
"""Fast concurrent link checker for markdown files."""
from __future__ import annotations

import concurrent.futures
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ssl.create_default_context()
UA = "web-roadmap-link-check/1.0"
TIMEOUT = 15


def collect_urls() -> set[str]:
    urls: set[str] = set()
    for path in list((ROOT / "roadmap" / "weeks").glob("*.md")):
        urls.update(re.findall(r"https?://[^\s)\]\"<>]+", path.read_text(encoding="utf-8")))
    for path in list((ROOT / "docs").glob("*.md")) + list((ROOT / "docs" / "cheatsheets").glob("*.md")):
        urls.update(re.findall(r"https?://[^\s)\]\"<>]+", path.read_text(encoding="utf-8")))
    return {u.rstrip(".,;`)'\"") for u in urls if "localhost" not in u}


def normalize(url: str) -> str:
    return url


def check(url: str) -> tuple[str, bool, str]:
    headers = {"User-Agent": UA}
    target = normalize(url)
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(target, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=CTX) as resp:
                code = resp.status
            if code in (200, 403):
                return url, True, str(code)
            return url, False, str(code)
        except urllib.error.HTTPError as e:
            if e.code in (200, 403):
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
    urls = sorted(collect_urls())
    bad: list[tuple[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for url, ok, info in pool.map(check, urls):
            if not ok:
                bad.append((url, info))
    print(f"Checked {len(urls)} URLs, {len(bad)} failures")
    for url, info in sorted(bad):
        print(f"  [{info}] {url}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
