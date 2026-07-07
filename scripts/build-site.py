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
VERSION = "1.2.0"

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
    items = []
    for num, title, desc in WEEKS_META:
        items.append(
            f'<a class="card" href="#week-{num}" data-route="week-{num}">'
            f'<div class="week">Неделя {num}</div><h3>{html.escape(title)}</h3>'
            f"<p>{html.escape(desc)}</p></a>"
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
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css">
  <script defer src="https://gc.zgo.at/count.js" data-goatcounter="https://web-roadmap.goatcounter.com/count"></script>
</head>
<body>
  <a class="skip-link" href="#main-content">Перейти к содержимому</a>
  <canvas id="code-canvas" aria-hidden="true"></canvas>
  <div class="scanlines" aria-hidden="true"></div>
  <div class="app">
    <header class="nav-bar">
      <div class="nav-inner">
        <a class="brand" href="#home" data-route="home">
          <img src="assets/logo.png" alt="" width="32" height="32"> web-roadmap
        </a>
        <div class="nav-right">
          <button type="button" class="icon-btn burger" id="burger-btn" aria-label="Меню">☰</button>
          <nav class="nav-links" id="nav-links">
            <a href="#week-00" data-route="week-00">Старт</a>
            <a href="#intro" data-route="intro">Введение</a>
            <a href="#weeks">Недели</a>
            <a href="#projects" data-route="projects">Проекты</a>
            <a href="#cheatsheet-html" data-route="cheatsheet-html">Шпаргалки</a>
          </nav>
          <button type="button" class="icon-btn" id="search-btn" title="Поиск (Ctrl+K)">⌕</button>
          <button type="button" class="icon-btn" id="reading-mode-btn" title="Режим чтения">Aa</button>
          <a class="icon-btn" href="https://github.com/krwg/web-roadmap" target="_blank" rel="noopener">GitHub</a>
        </div>
      </div>
    </header>

    <div id="view-home" class="view">
      <main id="main-content">
        <header class="hero">
          <div class="hero-inner">
            <div class="hero-logo"><img src="assets/logo.png" alt="web-roadmap" width="88" height="88"></div>
            <h1>Стать full-stack разработчиком — по плану, не по хаосу</h1>
            <p class="lead">22 недели: от первого <code>index.html</code> до DevHub capstone с Docker и deploy. Теория своими словами, практика каждый день, Git с недели 1.</p>
            <div class="stats">
              <div class="stat"><strong>22</strong><span>недели</span></div>
              <div class="stat"><strong>22</strong><span>проекта</span></div>
              <div class="stat"><strong>2</strong><span>трека</span></div>
              <div class="stat"><strong>154</strong><span>дня</span></div>
            </div>
            <div class="progress-bar-wrap">
              <div class="label" id="progress-label">Прогресс: 0 / 23 недель</div>
              <div class="progress-track"><div class="progress-fill" id="progress-fill"></div></div>
            </div>
            <div class="cta-row">
              <a class="btn btn-primary" href="#week-00" data-route="week-00">Неделя 0: подготовка</a>
              <a class="btn btn-secondary" href="#week-01" data-route="week-01">Неделя 1: HTML</a>
              <a class="btn btn-ghost" href="#start" data-route="start">Как учиться</a>
            </div>
          </div>
        </header>

        <section class="section section-alt" id="why">
          <div class="section-inner">
            <h2>Что вы получите</h2>
            <p class="sub">Реалистичный путь к junior full-stack с доказуемыми проектами в GitHub.</p>
            <div class="feature-grid">
              <div class="feature"><h3>Порядок тем</h3><p>HTML → CSS → JS → React → Python → SQL → API → Docker без скачков.</p></div>
              <div class="feature"><h3>22 проекта</h3><p>Каждая неделя — артефакт в <code>learning-log</code>.</p></div>
              <div class="feature"><h3>Два трека</h3><p>Полный 6–7 ч/день или лайт 3–4 ч с MVP-практикой.</p></div>
              <div class="feature"><h3>Теория + практика</h3><p>Проза, не только ссылки. «Если застрял» и «Проверь себя».</p></div>
              <div class="feature"><h3>DevHub capstone</h3><p>React + API + PostgreSQL + JWT + Docker + deploy.</p></div>
              <div class="feature"><h3>Шпаргалки</h3><p>HTML/CSS, JS, React, SQL, Backend — для ревью.</p></div>
            </div>
          </div>
        </section>

        <section class="section" id="examples">
          <div class="section-inner">
            <h2>Примеры из learning-log</h2>
            <p class="sub">Автор проходит маршрут параллельно — скоро здесь появятся скрины недель.</p>
            <div class="examples-grid">
              <div class="example-card">week-01 · Portfolio<br><small>скоро</small></div>
              <div class="example-card">week-14 · Dashboard<br><small>скоро</small></div>
              <div class="example-card">week-22 · DevHub<br><small>скоро</small></div>
            </div>
            <p style="text-align:center;margin-top:20px"><a href="https://github.com/krwg/learning-log">github.com/krwg/learning-log</a></p>
          </div>
        </section>

        <section class="section section-alt" id="weeks">
          <div class="section-inner">
            <h2>23 недели (0 + 22)</h2>
            <p class="sub">Клик — план недели с оглавлением по дням. Отмечайте прогресс галочкой на карточке.</p>
            <div class="grid">{cards}</div>
          </div>
        </section>

        <section class="community" id="community">
          <h2>Помогите маршруту расти</h2>
          <p>Звезда на GitHub, репост или Issue с улучшением — всё помогает следующим ученикам.</p>
          <div class="cta-row">
            <a class="btn btn-primary" href="https://github.com/krwg/web-roadmap" target="_blank" rel="noopener">★ Star</a>
            <button type="button" class="btn btn-secondary" id="share-btn">Поделиться</button>
            <a class="btn btn-ghost" href="https://github.com/krwg/web-roadmap/issues/new/choose" target="_blank" rel="noopener">Issue</a>
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
          <a class="back-link" href="#weeks" data-route="home">← Назад</a>
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
