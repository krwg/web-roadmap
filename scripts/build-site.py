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
VERSION = "1.2.3"

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
    "cheatsheet-html": ("docs/cheatsheets/html-css.md", "Шпаргалка HTML/CSS"),
    "cheatsheet-js": ("docs/cheatsheets/javascript.md", "Шпаргалка JS/TS"),
    "cheatsheet-react": ("docs/cheatsheets/react.md", "Шпаргалка React"),
    "cheatsheet-sql": ("docs/cheatsheets/sql.md", "Шпаргалка SQL"),
    "cheatsheet-backend": ("docs/cheatsheets/backend.md", "Шпаргалка Backend"),
}

MD = markdown.Markdown(
    extensions=["tables", "fenced_code", "sane_lists", "md_in_html"],
    output_format="html5",
)


def fix_links(body: str) -> str:
    body = re.sub(r'href="\.\./weeks/week-(\d{2})\.md[^"]*"', r'href="#week-\1"', body)
    body = re.sub(r'href="weeks/week-(\d{2})\.md[^"]*"', r'href="#week-\1"', body)
    body = re.sub(
        r'href="\.\./\.\./docs/([^"#]+)(#[^"]*)?"',
        lambda m: f'href="#{page_slug_from_path(m.group(1))}{m.group(2) or ""}"',
        body,
    )
    body = re.sub(
        r'href="\.\./([^"#]+)(#[^"]*)?"',
        r'href="https://github.com/krwg/web-roadmap/blob/main/roadmap/\1\2"',
        body,
    )
    return body


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


def md_to_html(text: str) -> str:
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
    return fix_links(body)


def extract_toc(html_body: str, prefix: str) -> list[dict]:
    toc = []
    for m in re.finditer(r'<a id="([^"]+)"></a>\s*', html_body):
        aid = m.group(1)
        after = html_body[m.end() : m.end() + 200]
        h = re.search(r"<h2[^>]*>(.*?)</h2>", after, re.DOTALL)
        if h:
            label = re.sub(r"<[^>]+>", "", h.group(1)).strip()
            toc.append({"id": aid, "label": label[:60]})
    for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html_body, re.DOTALL):
        label = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if "Проект недели" in label:
            toc.append({"id": f"{prefix}-project", "label": "Проект недели"})
        elif "Проверь себя" in label:
            toc.append({"id": f"{prefix}-review", "label": "Проверь себя"})
        elif "Ревью" in label:
            toc.append({"id": f"{prefix}-review", "label": label[:40]})
    seen = set()
    out = []
    for t in toc:
        if t["id"] not in seen:
            seen.add(t["id"])
            out.append(t)
    return out


def strip_text(html_body: str, limit: int = 200) -> str:
    t = re.sub(r"<[^>]+>", " ", html_body)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:limit] + ("…" if len(t) > limit else "")


def build_week_json(num: str, title: str) -> dict:
    path = WEEKS_DIR / f"week-{num}.md"
    raw = path.read_text(encoding="utf-8")
    html_body = md_to_html(raw)
    rid = f"week-{num}"
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html_body, re.DOTALL)
    full = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else f"Неделя {num}: {title}"
    toc = extract_toc(html_body, rid)
    if not toc:
        for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html_body, re.DOTALL):
            label = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            slug = re.sub(r"[^\w\-]+", "-", label.lower())[:40]
            toc.append({"id": f"{rid}-{slug}", "label": label[:50]})
    return {
        "id": rid,
        "title": title,
        "fullTitle": full,
        "html": html_body,
        "toc": toc,
        "text": strip_text(html_body, 800),
    }


def build_page_json(page_id: str, rel_path: str, title: str) -> dict:
    path = ROOT / rel_path
    raw = path.read_text(encoding="utf-8")
    html_body = md_to_html(raw)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html_body, re.DOTALL)
    full = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else title
    toc = []
    for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html_body, re.DOTALL):
        label = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        slug = re.sub(r"[^\w\-а-яё]+", "-", label.lower(), flags=re.I)[:40]
        toc.append({"id": f"{page_id}-{slug}", "label": label[:60]})
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
            <a href="#cheatsheet-html" data-route="cheatsheet-html">Шпаргалки</a>
          </nav>
          <button type="button" class="icon-btn icon-only" id="search-btn" title="Поиск (Ctrl+K)"><span class="material-symbols-outlined">search</span></button>
          <button type="button" class="icon-btn icon-only" id="reading-mode-btn" title="Режим чтения"><span class="material-symbols-outlined">auto_stories</span></button>
          <a class="icon-btn" href="https://github.com/krwg/web-roadmap" target="_blank" rel="noopener"><span class="material-symbols-outlined">code</span> GitHub</a>
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
              <div class="hint">Отмечайте недели на карточках или внутри урока</div>
            </div>
            <div class="cta-row">
              <a class="btn btn-primary" href="#week-00" data-route="week-00">Начать обучение</a>
              <a class="btn btn-secondary" href="#intro" data-route="intro">О маршруте</a>
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
              <p class="sub">Автор проходит маршрут параллельно — здесь будут реальные проекты.</p>
            </div>
            <div class="examples-grid">
              <a class="example-card" href="https://github.com/krwg/learning-log" target="_blank" rel="noopener">
                <div class="tag">week-01</div><h4>Portfolio Landing</h4><small>скоро</small>
              </a>
              <a class="example-card" href="https://github.com/krwg/learning-log" target="_blank" rel="noopener">
                <div class="tag">week-14</div><h4>React Dashboard</h4><small>скоро</small>
              </a>
              <a class="example-card" href="https://github.com/krwg/learning-log" target="_blank" rel="noopener">
                <div class="tag">week-22</div><h4>DevHub Capstone</h4><small>скоро</small>
              </a>
            </div>
          </div>
        </section>

        <section class="section" id="weeks">
          <div class="section-inner">
            <div class="section-head">
              <h2>Программа курса</h2>
              <p class="sub">23 модуля · нажмите на карточку — откроется урок с оглавлением по дням</p>
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
          <h2>Помогите маршруту расти</h2>
          <p>Звезда на GitHub, репост или Issue с улучшением — всё помогает следующим ученикам.</p>
          <div class="cta-row">
            <a class="btn btn-primary" href="https://github.com/krwg/web-roadmap" target="_blank" rel="noopener"><span class="material-symbols-outlined">star</span> Star</a>
            <button type="button" class="btn btn-secondary" id="share-btn"><span class="material-symbols-outlined">share</span> Поделиться</button>
            <a class="btn btn-ghost" href="https://github.com/krwg/web-roadmap/issues/new/choose" target="_blank" rel="noopener"><span class="material-symbols-outlined">bug_report</span> Issue</a>
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
          <a class="back-link" href="#weeks" data-route="home"><span class="material-symbols-outlined">arrow_back</span> К программе курса</a>
          <h1 id="doc-page-title">Загрузка…</h1>
          <div class="page-toolbar">
            <button type="button" class="btn btn-ghost" id="mark-done-btn" hidden>Отметить неделю</button>
          </div>
        </div>
      </div>
      <div class="doc-layout">
        <aside class="doc-toc" id="doc-toc"></aside>
        <div class="prose-wrap" id="doc-content"><div class="loading">Загрузка…</div></div>
      </div>
      <div class="lesson-next" id="lesson-next" hidden>
        <div class="lesson-next-inner">
          <div class="lesson-next-label">
            <span class="material-symbols-outlined">arrow_forward</span>
            <span id="lesson-next-text">Следующий модуль</span>
          </div>
          <a class="btn btn-primary btn-sm" href="#" id="lesson-next-link">Перейти</a>
        </div>
      </div>
    </div>
  </div>

  <div class="search-overlay" id="search-overlay">
    <div class="search-box">
      <input type="search" id="search-input" placeholder="Поиск по маршруту… (Ctrl+K)" autocomplete="off">
      <div class="search-results" id="search-results"></div>
    </div>
  </div>

  <script>window.SITE_ROUTES = {site_routes};</script>
  <script>window.SEARCH_INDEX = {search_json};</script>
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

    routes = {"weeks": week_routes, "pages": page_routes}
    write_index(search_index, routes)

    idx_size = (DOCS / "index.html").stat().st_size // 1024
    print(f"Built site: index.html ({idx_size} KB), {len(WEEKS_META)} weeks, {len(PAGES)} pages")


if __name__ == "__main__":
    build()
