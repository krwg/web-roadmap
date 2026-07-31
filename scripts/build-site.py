#!/usr/bin/env python3
"""Build GitHub Pages site: shell index + lazy-loaded week/page JSON."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
WEEKS_DIR = ROOT / "roadmap" / "weeks"
OUT_WEEKS = DOCS / "weeks"
OUT_PAGES = DOCS / "pages"
LOGO_SRC = ROOT / "assets" / "logo.png"
LOGO_DOCS = DOCS / "assets" / "logo.png"
VERSION = "1.4.0"

PHASE_MAP = {
    "00": ("setup", "Старт"),
    "01": ("markup", "Вёрстка"), "02": ("markup", "Вёрстка"), "03": ("markup", "Вёрстка"),
    "04": ("setup", "Git & Tools"),
    "05": ("js", "JavaScript"), "06": ("js", "JavaScript"), "07": ("js", "JavaScript"),
    "08": ("js", "JavaScript"), "09": ("js", "JavaScript"), "10": ("js", "JavaScript"),
    "11": ("fe", "Frontend"), "12": ("fe", "Frontend"), "13": ("fe", "Frontend"), "14": ("fe", "Frontend"),
    "15": ("be", "Backend"), "16": ("be", "Backend"), "17": ("be", "Backend"),
    "18": ("be", "Backend"), "19": ("be", "Backend"),
    "20": ("ship", "Продакшен"), "21": ("ship", "Продакшен"), "22": ("ship", "Продакшен"),
}

WEEK_META_JSON = json.loads((Path(__file__).parent / "week-meta.json").read_text(encoding="utf-8"))

WEEKS_META = [
    ("00", "Онбординг", "Инструменты, GitHub, как учиться"),
    ("01", "HTML", "Семантика, формы, a11y · Git с дня 1"),
    ("02", "CSS основы", "Селекторы, box model, типографика"),
    ("03", "CSS layouts", "Flexbox, Grid, адаптив"),
    ("04", "Git advanced", "Ветки, PR, DevTools, CI"),
    ("05", "JavaScript", "Типы, функции, массивы"),
    ("06", "DOM", "События, делегирование"),
    ("07", "Modules & API", "Fetch, storage, ES modules"),
    ("08", "Async & HTTP", "Event loop, REST"),
    ("09", "JS advanced", "Closures, ООП, паттерны"),
    ("10", "TypeScript", "Типы, generics, strict"),
    ("11", "React basics", "JSX, компоненты, props"),
    ("12", "React state", "Hooks, effects, формы"),
    ("13", "Router & Context", "SPA, custom hooks"),
    ("14", "Frontend SPA", "Dashboard — проект #14"),
    ("15", "Python", "Синтаксис, venv, CLI"),
    ("16", "Python OOP", "SQLite, алгоритмы"),
    ("17", "SQL", "PostgreSQL, индексы"),
    ("18", "FastAPI", "REST, SQLAlchemy"),
    ("19", "Node.js", "Express, layered API"),
    ("20", "Auth & tests", "JWT, OWASP, pytest"),
    ("21", "Docker", "Full-stack compose"),
    ("22", "Capstone", "DevHub — финальный проект"),
]

PAGES = {
    "intro": ("roadmap/introduction.md", "Введение"),
    "start": ("docs/getting-started.md", "Как начать"),
    "projects": ("docs/projects.md", "22 проекта"),
    "changelog": ("CHANGELOG.md", "Changelog"),
    "cheatsheet-html": ("docs/cheatsheets/html-css.md", "Шпаргалка HTML/CSS"),
    "cheatsheet-js": ("docs/cheatsheets/javascript.md", "Шпаргалка JS/TS"),
    "cheatsheet-react": ("docs/cheatsheets/react.md", "Шпаргалка React"),
    "cheatsheet-sql": ("docs/cheatsheets/sql.md", "Шпаргалка SQL"),
    "cheatsheet-backend": ("docs/cheatsheets/backend.md", "Шпаргалка Backend"),
}

QUIZ_BANK = json.loads((Path(__file__).parent / "quiz-bank.json").read_text(encoding="utf-8"))

MD = markdown.Markdown(
    extensions=["tables", "fenced_code", "sane_lists", "md_in_html"],
    output_format="html5",
)


def heading_slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[^\w\-а-яё0-9]+", "-", text, flags=re.I)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")[:48] or "section"


def page_slug_from_path(path: str) -> str:
    mapping = {
        "getting-started.md": "start",
        "projects.md": "projects",
        "cheatsheets/html-css.md": "cheatsheet-html",
        "cheatsheets/javascript.md": "cheatsheet-js",
        "cheatsheets/react.md": "cheatsheet-react",
        "cheatsheets/sql.md": "cheatsheet-sql",
        "cheatsheets/backend.md": "cheatsheet-backend",
    }
    return mapping.get(path, path.replace("/", "-").replace(".md", ""))


def fix_links(body: str) -> str:
    body = re.sub(r'href="\.\./weeks/week-(\d{2})\.md[^"]*"', r'href="#week-\1"', body)
    body = re.sub(r'href="weeks/week-(\d{2})\.md[^"]*"', r'href="#week-\1"', body)

    def docs_link(m: re.Match) -> str:
        path = m.group(1)
        frag = m.group(2) or ""
        route = page_slug_from_path(path)
        if not frag:
            return f'href="#{route}"'
        slug = heading_slug(frag.lstrip("#"))
        return f'href="#{route}--{route}-{slug}"'

    body = re.sub(
        r'href="(?:\.\./)+docs/([^"#]+\.md)(#[^"]*)?"',
        docs_link,
        body,
    )
    body = re.sub(
        r'href="\.\./([^"#]+)(#[^"]*)?"',
        r'href="https://github.com/krwg/web-roadmap/blob/main/roadmap/\1\2"',
        body,
    )
    return body


def normalize_heading_ids(html_body: str, prefix: str) -> str:
    """Move day anchors onto <h2 id="..."> (markdown emits h2 then empty <p><a id>)."""
    # IMPORTANT: do not use DOTALL on (.*?) inside h2 — backtracking would skip to a later empty anchor.
    html_body = re.sub(
        r"<h2([^>]*)>(.*?)</h2>\s*<p>\s*<a id=\"([^\"]+)\"></a>\s*</p>",
        r'<h2\1 id="\3">\2</h2>',
        html_body,
        flags=re.I,
    )
    html_body = re.sub(
        r"<a id=\"([^\"]+)\"></a>\s*<h2([^>]*)>(.*?)</h2>",
        r'<h2\2 id="\1">\3</h2>',
        html_body,
        flags=re.I,
    )

    def stamp_section(label_re: str, sid: str, html: str) -> str:
        pattern = re.compile(
            rf"<h2([^>]*)>([^<]*{label_re}[^<]*)</h2>",
            re.I,
        )

        def repl(m: re.Match) -> str:
            attrs = m.group(1)
            if re.search(r"\bid=", attrs):
                return m.group(0)
            return f'<h2{attrs} id="{sid}">{m.group(2)}</h2>'

        return pattern.sub(repl, html, count=1)

    html_body = stamp_section(r"Проект недели", f"{prefix}-project", html_body)
    html_body = stamp_section(r"Проверь себя", f"{prefix}-review", html_body)
    html_body = stamp_section(r"Ревью", f"{prefix}-review", html_body)
    return html_body


def wrap_practice_tracks(html_body: str) -> str:
    """Mark full/lite practice blocks so the SPA can filter by track."""
    html_body = re.sub(
        r"(<h3[^>]*>\s*Практика \(полный трек\)\s*</h3>)(.*?)(?=<h3[\s>]|<h2[\s>]|$)",
        r'<section class="practice-track practice-full" data-track="full">\1\2</section>',
        html_body,
        flags=re.I | re.DOTALL,
    )
    html_body = re.sub(
        r"(<h3[^>]*>\s*Практика \(лайт[^<]*</h3>)(.*?)(?=<h3[\s>]|<h2[\s>]|$)",
        r'<section class="practice-track practice-lite" data-track="lite">\1\2</section>',
        html_body,
        flags=re.I | re.DOTALL,
    )
    return html_body


def md_to_html(text: str, prefix: str = "") -> str:
    text = re.sub(r"```mermaid\n(.*?)```", r'<pre class="mermaid">\1</pre>', text, flags=re.DOTALL)
    MD.reset()
    body = MD.convert(text)
    body = re.sub(r"<li>\[ \] ", r'<li class="task"><input type="checkbox" disabled> ', body)
    body = re.sub(r"<li>\[x\] ", r'<li class="task"><input type="checkbox" checked disabled> ', body, flags=re.I)
    body = re.sub(
        r'<pre><code class="language-(\w+)">',
        r'<pre><code class="language-\1">',
        body,
    )
    body = fix_links(body)
    body = wrap_practice_tracks(body)
    if prefix:
        body = normalize_heading_ids(body, prefix)
    return body


def extract_toc(html_body: str, prefix: str) -> list[dict]:
    toc: list[dict] = []
    for m in re.finditer(r"<h2([^>]*)>(.*?)</h2>", html_body, re.I):
        attrs, inner = m.group(1), m.group(2)
        label = re.sub(r"<[^>]+>", "", inner).strip()
        id_m = re.search(r'\bid="([^"]+)"', attrs)
        if id_m:
            aid = id_m.group(1)
        else:
            aid = f"{prefix}-{heading_slug(label)}"
        toc.append({"id": aid, "label": label[:60]})

    seen: set[str] = set()
    out: list[dict] = []
    for t in toc:
        if t["id"] in seen:
            continue
        seen.add(t["id"])
        out.append(t)
    return out


def ensure_all_h2_ids(html_body: str, prefix: str) -> str:
    def repl(m: re.Match) -> str:
        attrs, inner = m.group(1), m.group(2)
        if re.search(r"\bid=", attrs):
            return m.group(0)
        label = re.sub(r"<[^>]+>", "", inner).strip()
        return f'<h2{attrs} id="{prefix}-{heading_slug(label)}">{inner}</h2>'

    return re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, html_body, flags=re.I)


def strip_text(html_body: str, limit: int = 200) -> str:
    t = re.sub(r"<[^>]+>", " ", html_body)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:limit] + ("…" if len(t) > limit else "")


def split_week_sections(html_body: str, toc: list[dict]) -> tuple[str, list[dict]]:
    """Split week HTML into intro + per-h2 lesson sections (days, project, review)."""
    h2_iter = list(re.finditer(r"<h2\b", html_body, re.I))
    if not h2_iter:
        return html_body, []

    intro = html_body[: h2_iter[0].start()].strip()
    # Drop leading h1 from intro if present — shown in page chrome
    intro = re.sub(r"^<h1\b[^>]*>.*?</h1>\s*", "", intro, count=1, flags=re.I | re.DOTALL)

    sections: list[dict] = []
    id_to_label = {t["id"]: t["label"] for t in toc}

    for i, match in enumerate(h2_iter):
        start = match.start()
        end = h2_iter[i + 1].start() if i + 1 < len(h2_iter) else len(html_body)
        chunk = html_body[start:end].strip()
        id_m = re.search(r'<h2[^>]*\bid="([^"]+)"', chunk, re.I)
        if not id_m:
            continue
        sid = id_m.group(1)
        label = id_to_label.get(sid) or re.sub(
            r"<[^>]+>", "", re.search(r"<h2[^>]*>(.*?)</h2>", chunk, re.I | re.DOTALL).group(1)
        ).strip()
        kind = "day" if "-day-" in sid else ("project" if sid.endswith("-project") else ("review" if sid.endswith("-review") else "section"))
        sections.append({
            "id": sid,
            "label": label[:80],
            "kind": kind,
            "html": chunk,
            "text": strip_text(chunk, 400),
        })
    return intro, sections


def build_week_json(num: str, title: str) -> dict:
    path = WEEKS_DIR / f"week-{num}.md"
    raw = path.read_text(encoding="utf-8")
    rid = f"week-{num}"
    html_body = md_to_html(raw, prefix=rid)
    html_body = ensure_all_h2_ids(html_body, rid)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html_body, re.DOTALL | re.I)
    full = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else f"Неделя {num}: {title}"
    toc = extract_toc(html_body, rid)
    intro, sections = split_week_sections(html_body, toc)
    return {
        "id": rid,
        "title": title,
        "fullTitle": full,
        "html": html_body,
        "introHtml": intro,
        "sections": sections,
        "toc": toc,
        "quizzes": QUIZ_BANK.get(num, []),
        "text": strip_text(html_body, 800),
        "sourcePath": f"roadmap/weeks/week-{num}.md",
    }


def build_page_json(page_id: str, rel_path: str, title: str) -> dict:
    path = ROOT / rel_path
    raw = path.read_text(encoding="utf-8")
    html_body = md_to_html(raw, prefix=page_id)
    # Ensure h2 ids match link scheme used by fix_links
    def ensure_h2_ids(html: str) -> str:
        def repl(m: re.Match) -> str:
            attrs, inner = m.group(1), m.group(2)
            if re.search(r"\bid=", attrs):
                return m.group(0)
            label = re.sub(r"<[^>]+>", "", inner).strip()
            sid = f"{page_id}-{heading_slug(label)}"
            return f'<h2{attrs} id="{sid}">{inner}</h2>'

        return re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, html, flags=re.DOTALL | re.I)

    html_body = ensure_h2_ids(html_body)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html_body, re.DOTALL)
    full = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else title
    toc = extract_toc(html_body, page_id)
    return {
        "id": page_id,
        "title": title,
        "fullTitle": full,
        "html": html_body,
        "toc": toc,
        "text": strip_text(html_body, 800),
    }


def crop_logo() -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        LOGO_DOCS.parent.mkdir(parents=True, exist_ok=True)
        if LOGO_SRC.exists() and not LOGO_DOCS.exists():
            import shutil
            shutil.copy(LOGO_SRC, LOGO_DOCS)
        return
    im = Image.open(LOGO_SRC).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 30 and r < 28 and g < 32 and b < 32:
                px[x, y] = (r, g, b, 0)
    LOGO_DOCS.parent.mkdir(parents=True, exist_ok=True)
    im.save(LOGO_DOCS)

    og = Image.new("RGBA", (1200, 630), (5, 5, 8, 255))
    draw = ImageDraw.Draw(og)
    logo = im.copy()
    logo.thumbnail((200, 200))
    og.paste(logo, (80, 215), logo)
    try:
        font = ImageFont.truetype("arial.ttf", 48)
        font_s = ImageFont.truetype("arial.ttf", 28)
    except OSError:
        font = ImageFont.load_default()
        font_s = font
    draw.text((320, 240), "web-roadmap", fill=(255, 255, 255, 255), font=font)
    draw.text((320, 310), "Full-Stack за 22 недели", fill=(100, 210, 255, 255), font=font_s)
    draw.text((320, 360), "22 проекта · Git с дня 1 · DevHub capstone", fill=(134, 134, 139, 255), font=font_s)
    og.convert("RGB").save(DOCS / "assets" / "og-cover.png")


def week_cards() -> str:
    projects = WEEK_META_JSON.get("projects", {})
    items = []
    for num, title, desc in WEEKS_META:
        phase_id, phase_name = PHASE_MAP.get(num, ("js", ""))
        project = projects.get(num, "")
        duration = "3 дня" if num == "00" else "7 дней"
        num_display = int(num)
        project_html = (
            f'<span class="card-project">{html.escape(project)}</span>' if project else ""
        )
        items.append(
            f'<a class="card" href="#week-{num}" data-route="week-{num}" data-phase="{phase_id}">'
            f'<div class="card-top">'
            f'<span class="card-num">{num_display:02d}</span>'
            f'<span class="card-phase phase-{phase_id}">{html.escape(phase_name)}</span>'
            f'</div>'
            f'<div class="card-body"><h3>{html.escape(title)}</h3>'
            f"<p>{html.escape(desc)}</p></div>"
            f'<div class="card-footer">'
            f'{project_html}'
            f'<span class="card-duration">{duration}</span>'
            f"</div></a>"
        )
    return "\n".join(items)


def write_index(search_index: list, routes: dict) -> None:
    cards = week_cards()
    site_routes = json.dumps(routes, ensure_ascii=False)
    search_json = json.dumps(search_index, ensure_ascii=False)

    page = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>web-roadmap — Full-Stack за 22 недели</title>
  <meta name="description" content="Структурированный путь к junior full-stack: 22 недели, 22 проекта, Git с первого дня.">
  <meta name="theme-color" content="#050508">
  <link rel="icon" href="assets/logo.png" type="image/png">
  <link rel="manifest" href="manifest.json">
  <meta property="og:title" content="web-roadmap — Full-Stack за 22 недели">
  <meta property="og:description" content="От первого index.html до production full-stack.">
  <meta property="og:image" content="https://krwg.github.io/web-roadmap/assets/og-cover.png">
  <meta property="og:url" content="https://krwg.github.io/web-roadmap/">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="web-roadmap — Full-Stack за 22 недели">
  <meta name="twitter:description" content="22 недели, 22 проекта, Git с первого дня.">
  <link rel="canonical" href="https://krwg.github.io/web-roadmap/">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css">
  <script data-goatcounter="https://krwg.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head>
<body>
  <a class="skip-link" href="#main-content">Перейти к содержимому</a>
  <div class="hero-glow" aria-hidden="true"></div>
  <canvas id="code-canvas" aria-hidden="true"></canvas>
  <div class="scanlines" aria-hidden="true"></div>
  <div class="app">
    <header class="nav-bar">
      <div class="nav-inner">
        <a class="brand" href="#home" data-route="home">
          <img src="assets/logo.png" alt="" width="32" height="32"> web-roadmap
        </a>
        <div class="nav-right">
          <button type="button" class="icon-btn burger" id="burger-btn" aria-label="Меню"><span class="material-symbols-outlined">menu</span></button>
          <nav class="nav-links" id="nav-links">
            <a href="#week-00" data-route="week-00">Старт</a>
            <a href="#intro" data-route="intro">Введение</a>
            <a href="#weeks">Недели</a>
            <a href="#projects" data-route="projects">Проекты</a>
            <a href="#changelog" data-route="changelog">Changelog</a>
            <a href="#cheatsheet-html" data-route="cheatsheet-html">Шпаргалки</a>
          </nav>
          <button type="button" class="icon-btn icon-only" id="search-btn" title="Поиск (Ctrl+K)"><span class="material-symbols-outlined">search</span></button>
          <button type="button" class="icon-btn icon-only" id="reading-mode-btn" title="Режим чтения"><span class="material-symbols-outlined">auto_stories</span></button>
          <a class="icon-btn" href="https://github.com/krwg/web-roadmap" target="_blank" rel="noopener" id="nav-github"><span class="material-symbols-outlined">code</span> <span id="nav-star-label">GitHub</span></a>
        </div>
      </div>
    </header>

    <div id="view-home" class="view">
      <main id="main-content">
        <header class="hero">
          <div class="hero-inner">
            <div class="hero-logo"><img src="assets/logo.png" alt="web-roadmap" width="80" height="80"></div>
            <h1>Full-Stack разработчик за 22 недели</h1>
            <p class="lead">Структурированный маршрут как в профессиональной школе: теория своими словами, практика каждый день, Git с первого <code>index.html</code>, финальный capstone в production.</p>
            <div class="resume-banner" id="resume-banner" hidden>
              <div class="resume-banner-inner">
                <span class="material-symbols-outlined resume-icon">play_circle</span>
                <div class="resume-text">
                  <strong id="resume-title">Продолжить обучение</strong>
                  <span id="resume-meta" class="resume-meta"></span>
                </div>
                <a class="btn btn-primary btn-sm" href="#" id="resume-link">Продолжить</a>
              </div>
            </div>
            <div class="stats">
              <div class="stat"><strong>23</strong><span>модуля</span></div>
              <div class="stat"><strong>22</strong><span>проекта</span></div>
              <div class="stat"><strong>2</strong><span>трека</span></div>
              <div class="stat"><strong>154</strong><span>дня</span></div>
            </div>
            <div class="progress-panel">
              <div class="label" id="progress-label">Ваш прогресс: 0 / 23</div>
              <div class="progress-track"><div class="progress-fill" id="progress-fill"></div></div>
              <div class="hint">Отмечайте дни и недели — прогресс хранится локально и экспортируется в learning-log</div>
              <div class="track-toggle" id="track-toggle" role="group" aria-label="Трек практики">
                <button type="button" class="track-chip active" data-track-mode="full">Полный трек</button>
                <button type="button" class="track-chip" data-track-mode="lite">Лайт</button>
              </div>
            </div>
            <div class="cta-row">
              <a class="btn btn-primary" href="#week-00" data-route="week-00" id="cta-start">Начать обучение</a>
              <a class="btn btn-secondary" href="#progress-map">Карта прогресса</a>
              <a class="btn btn-ghost" href="#start" data-route="start">Как учиться</a>
            </div>
          </div>
        </header>

        <section class="section section-alt" id="path">
          <div class="section-inner">
            <div class="section-head">
              <h2>Путь обучения</h2>
              <p class="sub">Шесть блоков — от вёрстки до деплоя. Каждый блок заканчивается проектом в портфолио.</p>
            </div>
            <div class="curriculum-path">
              <div class="path-step"><span class="num">1</span> Вёрстка</div>
              <span class="path-arrow material-symbols-outlined">chevron_right</span>
              <div class="path-step"><span class="num">2</span> JavaScript</div>
              <span class="path-arrow material-symbols-outlined">chevron_right</span>
              <div class="path-step"><span class="num">3</span> React</div>
              <span class="path-arrow material-symbols-outlined">chevron_right</span>
              <div class="path-step"><span class="num">4</span> Python & SQL</div>
              <span class="path-arrow material-symbols-outlined">chevron_right</span>
              <div class="path-step"><span class="num">5</span> API</div>
              <span class="path-arrow material-symbols-outlined">chevron_right</span>
              <div class="path-step"><span class="num">6</span> DevOps</div>
            </div>
            <div class="tracks-row">
              <div class="track-card featured">
                <h3>Полный трек</h3>
                <div class="hours">6–7 часов / день</div>
                <p>Все задания, все проекты, максимальная глубина. Рекомендуется для цели junior full-stack.</p>
              </div>
              <div class="track-card">
                <h3>Лайт-трек</h3>
                <div class="hours">3–4 часа / день</div>
                <p>Теория + Git обязательны. Практика в MVP-объёме. Проект недели — в урезанном виде.</p>
              </div>
            </div>
          </div>
        </section>

        <section class="section" id="how-it-works">
          <div class="section-inner">
            <div class="section-head">
              <h2>Как устроено обучение</h2>
              <p class="sub">Каждый день — структура как в профессиональной школе: теория, практика, Git, проверка</p>
            </div>
            <div class="steps-row">
              <div class="step-card">
                <div class="step-icon"><span class="material-symbols-outlined">menu_book</span></div>
                <span class="step-num">01</span>
                <h3>Теория</h3>
                <p>Объяснение своими словами и ссылки на MDN, learn.javascript.ru и книги</p>
              </div>
              <div class="step-card">
                <div class="step-icon"><span class="material-symbols-outlined">code</span></div>
                <span class="step-num">02</span>
                <h3>Практика</h3>
                <p>Задания на день: полный трек 6–7 ч или лайт 3–4 ч — выбираете сами</p>
              </div>
              <div class="step-card">
                <div class="step-icon"><span class="material-symbols-outlined">terminal</span></div>
                <span class="step-num">03</span>
                <h3>Git</h3>
                <p>Каждый день — коммит в <code>learning-log</code>, к концу недели — тег <code>week-XX-done</code></p>
              </div>
              <div class="step-card">
                <div class="step-icon"><span class="material-symbols-outlined">rocket_launch</span></div>
                <span class="step-num">04</span>
                <h3>Проект</h3>
                <p>Работающий артефакт в портфолио: от лендинга до DevHub capstone</p>
              </div>
            </div>
          </div>
        </section>

        <section class="section" id="why">
          <div class="section-inner">
            <div class="section-head">
              <h2>Что вы получите</h2>
              <p class="sub">Не видеокурс — пошаговый план с проверкой себя и артефактами в GitHub.</p>
            </div>
            <div class="feature-grid">
              <div class="feature"><div class="feature-icon"><span class="material-symbols-outlined">route</span></div><h3>Понятный порядок</h3><p>HTML → CSS → JS → React → Python → SQL → API → Docker без хаоса «что учить дальше».</p></div>
              <div class="feature"><div class="feature-icon"><span class="material-symbols-outlined">folder</span></div><h3>22 проекта</h3><p>Каждая неделя — работающий код в <code>learning-log</code> для портфолио.</p></div>
              <div class="feature"><div class="feature-icon"><span class="material-symbols-outlined">alt_route</span></div><h3>Два трека</h3><p>Полный или лайт — выбирайте нагрузку, не пропуская фундамент.</p></div>
              <div class="feature"><div class="feature-icon"><span class="material-symbols-outlined">auto_stories</span></div><h3>Теория своими словами</h3><p>Не только ссылки — объяснения, «если застрял», самопроверка.</p></div>
              <div class="feature"><div class="feature-icon"><span class="material-symbols-outlined">rocket_launch</span></div><h3>DevHub capstone</h3><p>React + API + PostgreSQL + JWT + Docker + CI + deploy.</p></div>
              <div class="feature"><div class="feature-icon"><span class="material-symbols-outlined">description</span></div><h3>Шпаргалки</h3><p>HTML/CSS, JS, React, SQL, Backend — для быстрого ревью.</p></div>
            </div>
          </div>
        </section>

        <section class="section section-alt" id="examples">
          <div class="section-inner">
            <div class="section-head">
              <h2>Портфолио learning-log</h2>
              <p class="sub">Ведите свой публичный репозиторий с первой недели — это и есть портфолио для рекрутера.</p>
            </div>
            <div class="examples-grid">
              <a class="example-card" href="#start" data-route="start">
                <div class="tag">старт</div><h4>Создать learning-log</h4><small>пустой репо под вашим аккаунтом</small>
              </a>
              <a class="example-card" href="#projects" data-route="projects">
                <div class="tag">22+</div><h4>Каталог проектов</h4><small>ТЗ, MVP и DoD по неделям</small>
              </a>
              <a class="example-card" href="#week-22" data-route="week-22">
                <div class="tag">week-22</div><h4>DevHub Capstone</h4><small>финальный full-stack</small>
              </a>
            </div>
          </div>
        </section>

        <section class="section" id="progress-map">
          <div class="section-inner">
            <div class="section-head">
              <h2>Карта прогресса</h2>
              <p class="sub" id="progress-map-sub">Отмеченные дни подсвечены. Следующий шаг — кнопка «Продолжить».</p>
            </div>
            <div class="progress-map-grid" id="progress-map-grid"></div>
            <div class="cta-row" style="margin-top:24px">
              <button type="button" class="btn btn-primary" id="export-learning-log-btn"><span class="material-symbols-outlined">download</span> Экспорт в learning-log</button>
              <button type="button" class="btn btn-secondary" id="progress-export-btn"><span class="material-symbols-outlined">content_copy</span> Копировать JSON</button>
              <button type="button" class="btn btn-ghost" id="progress-import-btn"><span class="material-symbols-outlined">upload</span> Импорт</button>
            </div>
            <p class="export-hint">Сохраните файл как <code>learning-log/progress.json</code> или создайте private gist и положите ссылку в README.</p>
          </div>
        </section>

        <section class="section" id="weeks">
          <div class="section-inner">
            <div class="section-head">
              <h2>Программа курса</h2>
              <p class="sub">23 модуля · откройте модуль — уроки по дням на отдельных страницах</p>
            </div>
            <div class="phase-filters" id="phase-filters">
              <button type="button" class="phase-chip active" data-filter="all">Все</button>
              <button type="button" class="phase-chip" data-filter="setup">Старт</button>
              <button type="button" class="phase-chip" data-filter="markup">Вёрстка</button>
              <button type="button" class="phase-chip" data-filter="js">JavaScript</button>
              <button type="button" class="phase-chip" data-filter="fe">Frontend</button>
              <button type="button" class="phase-chip" data-filter="be">Backend</button>
              <button type="button" class="phase-chip" data-filter="ship">Продакшен</button>
            </div>
            <div class="grid" id="weeks-grid">{cards}</div>
          </div>
        </section>

        <section class="section section-alt" id="faq">
          <div class="section-inner">
            <div class="section-head">
              <h2>Частые вопросы</h2>
              <p class="sub">Коротко о том, как проходить маршрут</p>
            </div>
            <div class="faq-list">
              <details class="faq-item">
                <summary><span class="material-symbols-outlined">help</span> Нужен ли опыт программирования?</summary>
                <p>Нет. Неделя 0 готовит инструменты, неделя 1 начинается с HTML. Главное — 3–7 часов в день и дисциплина.</p>
              </details>
              <details class="faq-item">
                <summary><span class="material-symbols-outlined">help</span> Чем полный трек отличается от лайт?</summary>
                <p>В лайте обязательны теория и Git; практика в MVP-объёме. Полный трек — все задания и максимальная глубина проектов.</p>
              </details>
              <details class="faq-item">
                <summary><span class="material-symbols-outlined">help</span> Зачем репозиторий learning-log?</summary>
                <p>Это ваше портфолио: каждая неделя — папка с кодом и README. Рекрутер видит прогресс и коммиты, а не только финальный проект.</p>
              </details>
              <details class="faq-item">
                <summary><span class="material-symbols-outlined">help</span> Сколько времени займёт весь маршрут?</summary>
                <p>Полный трек: ~900–1100 часов за 22 недели. Лайт: ~500–650 часов. Можно растянуть — отмечайте прогресс на сайте.</p>
              </details>
              <details class="faq-item">
                <summary><span class="material-symbols-outlined">help</span> Это замена курсу?</summary>
                <p>Это структурированный план с материалами и проектами — без видео и менторов. Бесплатно, open source, можно учиться в своём темпе.</p>
              </details>
            </div>
          </div>
        </section>

        <section class="community section-alt" id="community">
          <h2>Связь с GitHub</h2>
          <p>Звезда, Discussions, Issues и правки в репозитории — маршрут живёт вместе с кодом.</p>
          <div class="cta-row">
            <a class="btn btn-primary" href="https://github.com/krwg/web-roadmap" target="_blank" rel="noopener" id="star-btn"><span class="material-symbols-outlined">star</span> <span id="star-count-label">Star</span></a>
            <a class="btn btn-secondary" href="https://github.com/krwg/web-roadmap/discussions" target="_blank" rel="noopener"><span class="material-symbols-outlined">forum</span> Discussions</a>
            <button type="button" class="btn btn-secondary" id="share-btn"><span class="material-symbols-outlined">share</span> Поделиться</button>
            <a class="btn btn-ghost" href="https://github.com/krwg/web-roadmap/issues/new/choose" target="_blank" rel="noopener"><span class="material-symbols-outlined">bug_report</span> Issue</a>
          </div>
          <div class="github-actions-row">
            <button type="button" class="btn btn-ghost btn-sm" id="progress-export-btn"><span class="material-symbols-outlined">download</span> Экспорт прогресса</button>
            <button type="button" class="btn btn-ghost btn-sm" id="progress-import-btn"><span class="material-symbols-outlined">upload</span> Импорт прогресса</button>
            <button type="button" class="btn btn-ghost btn-sm" id="copy-clone-btn"><span class="material-symbols-outlined">content_copy</span> git clone</button>
          </div>
        </section>
      </main>
      <footer class="footer-bar">
        <div class="footer-inner">
          <p>web-roadmap v{VERSION} · <a href="https://github.com/krwg/web-roadmap/blob/main/CHANGELOG.md">Changelog</a></p>
          <p><a href="https://github.com/krwg/web-roadmap">GitHub</a> · <a href="#start" data-route="start">Старт</a> · <a href="#projects" data-route="projects">Проекты</a></p>
        </div>
      </footer>
    </div>

    <div id="view-doc" class="view" hidden>
      <div class="page-header">
        <div class="page-header-inner">
          <a class="back-link" href="#weeks" data-route="home"><span class="material-symbols-outlined">arrow_back</span> К программе</a>
          <nav class="lesson-breadcrumb" id="lesson-breadcrumb" aria-label="Навигация по уроку"></nav>
          <h1 id="doc-page-title">Загрузка…</h1>
          <p class="lesson-subtitle" id="doc-lesson-subtitle" hidden></p>
          <div class="page-toolbar" id="page-toolbar">
            <div class="track-toggle track-toggle-sm" id="track-toggle-lesson" role="group" aria-label="Трек практики">
              <button type="button" class="track-chip" data-track-mode="full">Полный</button>
              <button type="button" class="track-chip" data-track-mode="lite">Лайт</button>
            </div>
            <button type="button" class="btn btn-ghost btn-sm" id="mark-done-btn" hidden>Отметить неделю</button>
            <button type="button" class="btn btn-ghost btn-sm" id="mark-day-btn" hidden>Отметить день</button>
            <a class="btn btn-ghost btn-sm" id="edit-github-btn" href="#" target="_blank" rel="noopener" hidden><span class="material-symbols-outlined">edit</span> Править</a>
            <a class="btn btn-ghost btn-sm" id="issue-github-btn" href="#" target="_blank" rel="noopener" hidden><span class="material-symbols-outlined">bug_report</span> Issue</a>
            <a class="btn btn-ghost btn-sm" id="source-github-btn" href="#" target="_blank" rel="noopener" hidden><span class="material-symbols-outlined">code</span> Исходник</a>
          </div>
          <div class="week-progress" id="week-progress" hidden>
            <div class="week-progress-track"><div class="week-progress-fill" id="week-progress-fill"></div></div>
            <span class="week-progress-label" id="week-progress-label"></span>
          </div>
        </div>
      </div>
      <div class="doc-layout">
        <aside class="doc-toc" id="doc-toc"></aside>
        <div class="prose-wrap">
          <div id="doc-content"><div class="loading">Загрузка…</div></div>
          <section class="comments-block" id="comments-block" hidden>
            <h2 class="comments-title"><span class="material-symbols-outlined">forum</span> Обсуждение недели</h2>
            <p class="comments-hint">Комментарии через GitHub Discussions (Giscus). Войдите аккаунтом GitHub, чтобы ответить.</p>
            <div class="giscus" id="giscus-container"></div>
          </section>
        </div>
      </div>
      <div class="lesson-next" id="lesson-next" hidden>
        <div class="lesson-next-inner">
          <a class="btn btn-ghost btn-sm" href="#" id="lesson-prev-link" hidden><span class="material-symbols-outlined">arrow_back</span> <span id="lesson-prev-text">Назад</span></a>
          <div class="lesson-next-label">
            <span class="material-symbols-outlined">arrow_forward</span>
            <span id="lesson-next-text">Следующий урок</span>
          </div>
          <a class="btn btn-primary btn-sm" href="#" id="lesson-next-link">Перейти</a>
        </div>
      </div>
    </div>
  </div>

  <input type="file" id="progress-import-file" accept="application/json,.json" hidden>

  <div class="search-overlay" id="search-overlay">
    <div class="search-box">
      <input type="search" id="search-input" placeholder="Поиск по маршруту… (Ctrl+K)" autocomplete="off">
      <div class="search-results" id="search-results"></div>
    </div>
  </div>

  <script>window.SITE_ROUTES = {site_routes};</script>
  <script>window.SEARCH_INDEX = {search_json};</script>
  <script>window.GISCUS = {{
    repo: "krwg/web-roadmap",
    repoId: "R_kgDOTPhP4Q",
    category: "General",
    categoryId: "DIC_kwDOTPhP4c4DCau6"
  }};</script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-bash.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-python.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-typescript.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-jsx.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-sql.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-yaml.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({{ startOnLoad: false, theme: 'dark' }});</script>
  <script src="app.js"></script>
</body>
</html>"""

    (DOCS / "index.html").write_text(page, encoding="utf-8")


def build() -> None:
    crop_logo()
    OUT_WEEKS.mkdir(parents=True, exist_ok=True)
    OUT_PAGES.mkdir(parents=True, exist_ok=True)

    search_index: list[dict] = []
    week_routes = {}
    day_index: list[dict] = []

    for num, title, _ in WEEKS_META:
        data = build_week_json(num, title)
        (OUT_WEEKS / f"{num}.json").write_text(
            json.dumps(data, ensure_ascii=False), encoding="utf-8"
        )
        week_routes[f"week-{num}"] = title
        search_index.append({
            "route": data["id"],
            "title": data["fullTitle"],
            "text": data["text"],
            "snippet": data["text"][:120],
        })
        for sec in data.get("sections") or []:
            search_index.append({
                "route": f"{data['id']}--{sec['id']}",
                "title": f"{title}: {sec['label']}",
                "text": sec.get("text", ""),
                "snippet": (sec.get("text") or "")[:120],
            })
            if sec.get("kind") == "day":
                day_index.append({
                    "week": data["id"],
                    "id": sec["id"],
                    "label": sec["label"],
                    "weekTitle": title,
                })

    page_routes = {}
    for pid, (rel, title) in PAGES.items():
        data = build_page_json(pid, rel, title)
        (OUT_PAGES / f"{pid}.json").write_text(
            json.dumps(data, ensure_ascii=False), encoding="utf-8"
        )
        page_routes[pid] = title
        search_index.append({
            "route": pid,
            "title": data["fullTitle"],
            "text": data["text"],
            "snippet": data["text"][:120],
        })

    (DOCS / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False), encoding="utf-8"
    )

    routes = {"weeks": week_routes, "pages": page_routes, "dayIndex": day_index}
    write_index(search_index, routes)
    write_prerender_pages(week_routes)
    write_sitemap(week_routes, page_routes)

    idx_size = (DOCS / "index.html").stat().st_size // 1024
    print(f"Built site: index.html ({idx_size} KB), {len(WEEKS_META)} weeks, {len(PAGES)} pages")


def write_prerender_pages(week_routes: dict) -> None:
    """Static shareable URLs: /w/01.html and /d/01-3.html → SPA hashes."""
    out = DOCS / "w"
    out.mkdir(parents=True, exist_ok=True)
    dout = DOCS / "d"
    dout.mkdir(parents=True, exist_ok=True)
    for num, title, _ in WEEKS_META:
        data = json.loads((OUT_WEEKS / f"{num}.json").read_text(encoding="utf-8"))
        route = f"week-{num}"
        page = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(data['fullTitle'])} · web-roadmap</title>
  <meta name="description" content="{html.escape(title)} — неделя {num} маршрута web-roadmap.">
  <link rel="canonical" href="https://krwg.github.io/web-roadmap/#{route}">
  <meta property="og:title" content="{html.escape(data['fullTitle'])}">
  <meta property="og:url" content="https://krwg.github.io/web-roadmap/w/{num}.html">
  <link rel="stylesheet" href="../styles.css">
</head>
<body class="reading-mode">
  <main class="prose-wrap" style="max-width:820px;margin:24px auto;padding:0 16px">
    <p><a href="../#{route}">Открыть в приложении маршрута</a> · <a href="../">На главную</a></p>
    <article class="prose">{data['html']}</article>
  </main>
  <script>if (location.hash) location.replace('../' + location.hash);</script>
</body>
</html>"""
        (out / f"{num}.html").write_text(page, encoding="utf-8")

        for sec in data.get("sections") or []:
            if sec.get("kind") != "day":
                continue
            day_m = re.search(r"-day-(.+)$", sec["id"])
            day_n = day_m.group(1) if day_m else heading_slug(sec["id"])
            hash_url = f"{route}--{sec['id']}"
            dpage = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(sec['label'])} · {html.escape(title)} · web-roadmap</title>
  <meta name="description" content="{html.escape(sec['label'])} — неделя {num}.">
  <link rel="canonical" href="https://krwg.github.io/web-roadmap/#{hash_url}">
  <meta http-equiv="refresh" content="0;url=../#{hash_url}">
  <link rel="stylesheet" href="../styles.css">
</head>
<body class="reading-mode">
  <main class="prose-wrap" style="max-width:820px;margin:24px auto;padding:0 16px">
    <p><a href="../#{hash_url}">Открыть урок</a></p>
    <article class="prose">{sec['html']}</article>
  </main>
  <script>location.replace('../#{hash_url}');</script>
</body>
</html>"""
            (dout / f"{num}-{day_n}.html").write_text(dpage, encoding="utf-8")


def write_sitemap(week_routes: dict, page_routes: dict) -> None:
    urls = ["https://krwg.github.io/web-roadmap/"]
    for num, _, _ in WEEKS_META:
        urls.append(f"https://krwg.github.io/web-roadmap/w/{num}.html")
        data = json.loads((OUT_WEEKS / f"{num}.json").read_text(encoding="utf-8"))
        for sec in data.get("sections") or []:
            if sec.get("kind") != "day":
                continue
            day_m = re.search(r"-day-(.+)$", sec["id"])
            if day_m:
                urls.append(f"https://krwg.github.io/web-roadmap/d/{num}-{day_m.group(1)}.html")
    for pid in page_routes:
        urls.append(f"https://krwg.github.io/web-roadmap/#{pid}")
    body = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        body.append(f"  <url><loc>{html.escape(u)}</loc></url>")
    body.append("</urlset>")
    (DOCS / "sitemap.xml").write_text("\n".join(body) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
