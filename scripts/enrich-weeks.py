#!/usr/bin/env python3
"""Add anchors, time blocks, stuck tips, self-check to week files."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEEKS = ROOT / "roadmap" / "weeks"
META = json.loads((Path(__file__).parent / "week-meta.json").read_text(encoding="utf-8"))

SELF_CHECK = """
## Проверь себя

<details>
<summary>Что должно получиться к концу недели?</summary>

Работающий проект **{project}** в `learning-log/week-{num}/`, осмысленная Git-история, тег `week-{num}-done`.

</details>

<details>
<summary>Главный навык недели одной фразой?</summary>

{skill}

</details>

<details>
<summary>Можно ли пропустить день?</summary>

Нет — дни связаны. В **лайт-режиме** сократи практику до MVP, но теорию и Git-коммит не пропускай.

</details>
"""

SKILLS = {
    "01": "Валидный семантический HTML с формами и базовой доступностью",
    "02": "CSS: селекторы, box model, типографика, design tokens",
    "03": "Адаптивная вёрстка на Flexbox и Grid",
    "04": "Профессиональный Git-workflow и DevTools",
    "05": "JavaScript: типы, функции, массивы, чистый синтаксис",
    "06": "DOM, события, интерактивный UI без фреймворков",
    "07": "Модули, Fetch, localStorage — мини-SPA на ванильном JS",
    "08": "Async/await, HTTP, работа с REST API",
    "09": "Closures, ООП и паттерны в JavaScript",
    "10": "TypeScript strict: типы без any",
    "11": "React: компоненты, props, state",
    "12": "React hooks, effects, формы",
    "13": "React Router, Context, custom hooks",
    "14": "Полноценное frontend SPA",
    "15": "Python основы и CLI",
    "16": "Python ООП, SQLite, алгоритмы",
    "17": "SQL и PostgreSQL на практике",
    "18": "FastAPI + SQLAlchemy REST API",
    "19": "Node.js + Express layered API",
    "20": "JWT auth, безопасность, тесты",
    "21": "Full-stack в Docker Compose",
    "22": "Production capstone: DevHub full-stack",
}

DAY_HEADER = re.compile(r"^## (День[^\n]+)$", re.MULTILINE)


def process_day_section(week_num: str, project: str, header: str, body: str) -> str:
    dm = re.search(r"День\s+(\d+)", header, re.I)
    day = dm.group(1) if dm else "0"
    anchor = f'<a id="week-{week_num}-day-{day}"></a>\n'

    if "> **Время (полный):**" not in body:
        meta = (
            f"\n> **Время (полный):** {META['time_full']}  \n"
            f"> **Время (лайт):** {META['time_light']}  \n"
            f"> **Связь с проектом:** шаг к **{project}**\n\n"
        )
        body = meta + body.lstrip("\n")

    if "### Если застрял" not in body:
        stuck = f"\n### Если застрял\n\n{META['stuck_default']}\n"
        inserted = False
        for marker in ("\n### Git", "\n### Ловушки", "\n---\n\n## "):
            if marker in body:
                body = body.replace(marker, stuck + marker, 1)
                inserted = True
                break
        if not inserted:
            body = body.rstrip() + stuck

    return f"## {header}\n{anchor}{body}"


def enrich_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"week-(\d{2})", path.name)
    if not m:
        return
    num = m.group(1)
    project = META["projects"].get(num, "проект недели")

    parts = DAY_HEADER.split(text)
    if len(parts) < 2:
        path.write_text(text, encoding="utf-8")
        return

    out = [parts[0]]
    for i in range(1, len(parts), 2):
        header = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        out.append(process_day_section(num, project, header, body))

    text = "".join(out)

    if "## Проверь себя" not in text:
        text = text.rstrip() + "\n\n" + SELF_CHECK.format(
            project=project, num=num, skill=SKILLS.get(num, project)
        )

    path.write_text(text, encoding="utf-8")
    print(f"Enriched {path.name}")


def main() -> None:
    for p in sorted(WEEKS.glob("week-*.md")):
        enrich_file(p)


if __name__ == "__main__":
    main()
