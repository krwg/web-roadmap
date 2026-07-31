#!/usr/bin/env python3
"""Rebalance week markdown: realistic day hours, lite/full practice, diverse hints."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEEKS = ROOT / "roadmap" / "weeks"
META = json.loads((Path(__file__).parent / "week-meta.json").read_text(encoding="utf-8"))

DAY_HEADER = re.compile(r"^## (День[^\n]+)$", re.MULTILINE)
TIME_BLOCK = re.compile(
    r"\n?> \*\*Время \(полный\):\*\*[^\n]*\n"
    r"> \*\*Время \(лайт\):\*\*[^\n]*\n"
    r"(?:> \*\*Связь с проектом:\*\*[^\n]*\n)?\n?",
    re.MULTILINE,
)
STUCK_BLOCK = re.compile(
    r"\n### Если застрял\n\n.*?(?=\n### |\n---|\n## |\Z)",
    re.DOTALL,
)

STUCK_POOL = [
    "Застрял >20 мин — выпиши вход/выход задачи в 3 строки. Сделай минимальный пример в `playground.*`, без копипаста из ИИ.",
    "Не понимаешь ошибку — прочитай её с конца: файл, строка, тип. Открой DevTools / терминал и воспроизведи на 5 строках кода.",
    "Слишком много концептов сразу — вернись к одному примеру из теории и повтори его руками, меняя имена.",
    "UI «не работает» — проверь селекторы в Elements, слушатели в Event Listeners, сеть во вкладке Network.",
    "Код «магический» — объясни вслух каждый шаг как пятилетке. Где споткнулся — там дыра в понимании.",
    "Скопировал из чата ИИ — удали и перепиши с нуля по своему чеклисту. ИИ только для ревью уже написанного.",
    "Запутался в структуре файлов — нарисуй дерево папок на бумаге, потом создай пустые файлы и заполни по одному.",
    "Тесты/валидация красные — сначала один failing case, почини его, только потом следующий.",
    "Документация не клеится — найди один официальный пример (MDN / docs) и сопоставь 1:1 со своим кодом.",
    "Устал — сделай коммит текущего прогресса с честным сообщением `wip:` и паузу 10 минут. Не геройствуй.",
]


def fmt_hours(minutes: int) -> str:
    # Round to 5 minutes for readable estimates
    minutes = max(10, int(round(minutes / 5) * 5))
    if minutes < 60:
        return f"~{minutes}м"
    h = minutes // 60
    m = minutes % 60
    if m == 0:
        return f"~{h}ч"
    if m <= 10:
        return f"~{h}ч"
    if m < 45:
        return f"~{h}.5ч"
    return f"~{h + 1}ч"


def estimate_times(body: str, header: str) -> tuple[str, str]:
    """Estimate full/lite minutes from practice density and theory length."""
    theory = ""
    m = re.search(r"### Теория\n(.*?)(?=\n### |\Z)", body, re.DOTALL)
    if m:
        theory = m.group(1)
    practice = ""
    m = re.search(r"### Практика(?:[^\n]*)\n(.*?)(?=\n### |\Z)", body, re.DOTALL)
    if m:
        practice = m.group(1)

    theory_words = len(re.findall(r"\w+", theory, re.U))
    steps = len(re.findall(r"^\s*\d+\.", practice, re.M))
    checks = len(re.findall(r"- \[[ x]\]", practice, re.I))
    has_project = bool(re.search(r"проект|MVP|сдай|DoD|спецификац", header + body, re.I))
    is_review = bool(re.search(r"ревью|итог|самопровер|воскресен|Sun\)", header, re.I))
    is_onboarding = "0." in header or "подготовк" in header.lower()

    theory_m = max(25, min(120, 20 + theory_words // 4))
    practice_m = max(40, min(210, 25 + steps * 18 + checks * 8))
    git_m = 10 if is_onboarding else 15
    review_m = 45 if is_review or has_project else 25
    if is_onboarding:
        theory_m = max(20, theory_m // 2)
        practice_m = max(30, min(90, practice_m))
        review_m = 15

    # Capstone / heavy project days
    if has_project and (is_review or "проект недели" in body.lower()):
        practice_m = max(practice_m, 150)
        review_m = max(review_m, 40)

    full_total = theory_m + practice_m + git_m + review_m
    # Keep full track roughly 4–7.5h unless onboarding
    if not is_onboarding and full_total < 240:
        practice_m += 240 - full_total
    if full_total > 450:
        scale = 420 / full_total
        theory_m = int(theory_m * scale)
        practice_m = int(practice_m * scale)
        review_m = int(review_m * scale)

    lite_theory = max(15, int(theory_m * 0.45))
    lite_practice = max(30, int(practice_m * 0.45))
    lite_git = 10

    full = (
        f"{fmt_hours(theory_m)} теория · {fmt_hours(practice_m)} практика · "
        f"~{git_m}м Git · {fmt_hours(review_m)} ревью"
    )
    lite = (
        f"{fmt_hours(lite_theory)} теория · {fmt_hours(lite_practice)} практика (MVP) · "
        f"~{lite_git}м Git"
    )
    return full, lite


def stuck_tip(week_num: str, header: str, body: str, idx: int) -> str:
    blob = f"{header} {body[:400]}".lower()
    families = {
        "dom": [3, 1, 4, 0],
        "async": [1, 7, 0, 8],
        "css": [3, 2, 6, 0],
        "sql": [7, 6, 1, 8],
        "docker": [6, 7, 9, 0],
        "react": [4, 2, 0, 5],
        "git": [6, 0, 9, 2],
        "sec": [7, 1, 8, 5],
        "ts": [2, 4, 0, 8],
    }
    key = "default"
    if re.search(r"dom|событ|event|делегир", blob):
        key = "dom"
    elif re.search(r"async|fetch|http|api|promise", blob):
        key = "async"
    elif re.search(r"css|flex|grid|селектор|layout", blob):
        key = "css"
    elif re.search(r"sql|postgres|миграц|join", blob):
        key = "sql"
    elif re.search(r"docker|compose|deploy|ci", blob):
        key = "docker"
    elif re.search(r"react|hook|jsx|component", blob):
        key = "react"
    elif re.search(r"git|github|pr|ветк", blob):
        key = "git"
    elif re.search(r"тест|jwt|auth|security|owasp", blob):
        key = "sec"
    elif re.search(r"typescript|тип|generic", blob):
        key = "ts"

    if key == "default":
        tip = STUCK_POOL[(int(week_num) * 7 + idx) % len(STUCK_POOL)]
    else:
        tip = STUCK_POOL[families[key][idx % len(families[key])]]
    return f"\n### Если застрял\n\n{tip}\n"


def split_practice(body: str) -> str:
    """Turn single Практика into full + lite MVP blocks."""
    if "### Практика (полный" in body or "### Практика (лайт" in body:
        return body

    m = re.search(r"(### Практика)\n(.*?)(?=\n### |\Z)", body, re.DOTALL)
    if not m:
        return body

    block = m.group(2)
    lines = block.strip("\n").split("\n")
    numbered = [ln for ln in lines if re.match(r"^\s*\d+\.", ln)]
    other = [ln for ln in lines if not re.match(r"^\s*\d+\.", ln)]

    if len(numbered) <= 2:
        # Short practice: mark all as both, add lite note
        lite_body = block.rstrip() + "\n\n> Лайт: выполни пункты выше в минимальном виде (без полировки).\n"
        full_body = block
    else:
        cut = max(2, (len(numbered) + 1) // 2)
        lite_steps = numbered[:cut]
        full_body = "\n".join(numbered + other).strip() + "\n"
        lite_body = (
            "\n".join(lite_steps).strip()
            + "\n\n> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.\n"
        )

    replacement = (
        f"### Практика (полный трек)\n{full_body.rstrip()}\n\n"
        f"### Практика (лайт / MVP)\n{lite_body.rstrip()}\n"
    )
    return body[: m.start()] + replacement + body[m.end() :]


def process_day(week_num: str, project: str, header: str, body: str, idx: int) -> str:
    # Unique day anchor: prefer explicit day number from header
    dm = re.search(r"День\s+(\d+(?:\.\d+)?)", header, re.I)
    day_key = dm.group(1).replace(".", "-") if dm else str(idx)
    # week-00 uses 0.1 style → week-00-day-0-1
    anchor_id = f"week-{week_num}-day-{day_key}"

    body = TIME_BLOCK.sub("\n", body)
    body = re.sub(r'<a id="week-[^"]+"></a>\n?', "", body)
    body = STUCK_BLOCK.sub("\n", body)

    body = split_practice(body)

    full, lite = estimate_times(body, header)
    meta = (
        f"\n> **Время (полный):** {full}  \n"
        f"> **Время (лайт):** {lite}  \n"
        f"> **Связь с проектом:** шаг к **{project}**\n\n"
    )
    body = meta + body.lstrip("\n")
    stuck = stuck_tip(week_num, header, body, idx)

    inserted = False
    for marker in ("\n### Git", "\n### Ловушки", "\n---\n"):
        if marker in body:
            body = body.replace(marker, stuck + marker, 1)
            inserted = True
            break
    if not inserted:
        body = body.rstrip() + stuck

    return f"## {header}\n<a id=\"{anchor_id}\"></a>\n{body}"


def enrich_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"week-(\d{2})", path.name)
    if not m:
        return
    num = m.group(1)
    project = META["projects"].get(num, "проект недели")

    parts = DAY_HEADER.split(text)
    if len(parts) < 2:
        return

    out = [parts[0]]
    day_idx = 0
    for i in range(1, len(parts), 2):
        header = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        out.append(process_day(num, project, header, body, day_idx))
        day_idx += 1

    path.write_text("".join(out), encoding="utf-8")
    print(f"Rebalanced {path.name} ({day_idx} days)")


def main() -> None:
    for p in sorted(WEEKS.glob("week-*.md")):
        if p.name == "week-00.md":
            continue  # rewritten separately
        enrich_file(p)


if __name__ == "__main__":
    main()
