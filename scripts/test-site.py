#!/usr/bin/env python3
"""Lightweight structural tests for site build artifacts (run after build-site.py)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def main() -> int:
    index = DOCS / "index.html"
    if not index.exists():
        fail("docs/index.html missing")
    html = index.read_text(encoding="utf-8")
    for needle in (
        'id="giscus-container"',
        "window.GISCUS",
        'id="mark-day-btn"',
        'id="lesson-breadcrumb"',
        'id="edit-github-btn"',
    ):
        if needle not in html:
            fail(f"index.html missing {needle}")

    weeks = sorted((DOCS / "weeks").glob("*.json"))
    if len(weeks) != 23:
        fail(f"expected 23 week JSON files, got {len(weeks)}")

    day_files = list((DOCS / "d").glob("*.html")) if (DOCS / "d").is_dir() else []
    if len(day_files) < 140:
        fail(f"expected ≥140 day prerenders in docs/d/, got {len(day_files)}")

    total_sections = 0
    total_days = 0
    for path in weeks:
        data = json.loads(path.read_text(encoding="utf-8"))
        sections = data.get("sections") or []
        if not sections:
            fail(f"{path.name}: missing sections[]")
        if "sourcePath" not in data:
            fail(f"{path.name}: missing sourcePath")
        days = [s for s in sections if s.get("kind") == "day"]
        if path.stem != "00" and len(days) < 5:
            fail(f"{path.name}: expected ≥5 day sections, got {len(days)}")
        for s in sections:
            if not s.get("html") or not s.get("id"):
                fail(f"{path.name}: section missing id/html")
        total_sections += len(sections)
        total_days += len(days)

        # theory depth smoke: at least one day with substantial HTML
        max_len = max(len(s.get("html") or "") for s in days) if days else 0
        if max_len < 800:
            fail(f"{path.name}: day HTML suspiciously short (max {max_len})")

    app = (DOCS / "app.js").read_text(encoding="utf-8")
    for needle in ("loadGiscus", "bg-safari", "renderWeekHub", "updateLessonNav"):
        if needle not in app:
            fail(f"app.js missing {needle}")

    if not (ROOT / "giscus.json").exists():
        fail("giscus.json missing at repo root")

    print(
        f"OK: {len(weeks)} weeks, {total_sections} sections, "
        f"{total_days} days, {len(day_files)} day prerenders"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
