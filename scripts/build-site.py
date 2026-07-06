#!/usr/bin/env python3
"""Build single-file GitHub Pages site from roadmap markdown."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
WEEKS_DIR = ROOT / "roadmap" / "weeks"
OUT = ROOT / "docs" / "index.html"
LOGO_SRC = ROOT / "assets" / "logo.png"
LOGO_DOCS = ROOT / "docs" / "assets" / "logo.png"

WEEKS_META = [
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

MD = markdown.Markdown(
    extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
    output_format="html5",
)


def fix_internal_links(body: str) -> str:
    body = re.sub(
        r'href="\.\./weeks/week-(\d{2})\.md[^"]*"',
        r'href="#week-\1"',
        body,
    )
    body = re.sub(
        r'href="\.\./\.\./docs/([^"#]+)(#[^"]*)?"',
        r'href="https://github.com/krwg/web-roadmap/blob/main/docs/\1\2"',
        body,
    )
    body = re.sub(
        r'href="\.\./([^"#]+)(#[^"]*)?"',
        r'href="https://github.com/krwg/web-roadmap/blob/main/roadmap/\1\2"',
        body,
    )
    return body


def md_to_html(text: str) -> str:
    MD.reset()
    body = MD.convert(text)
    # GitHub-style task lists
    body = re.sub(
        r'<li>\[ \] ',
        r'<li class="task"><input type="checkbox" disabled> ',
        body,
    )
    body = re.sub(
        r'<li>\[x\] ',
        r'<li class="task"><input type="checkbox" checked disabled> ',
        body,
        flags=re.I,
    )
    return fix_internal_links(body)


def load_week_html(num: str) -> str:
    path = WEEKS_DIR / f"week-{num}.md"
    return md_to_html(path.read_text(encoding="utf-8"))


def crop_logo() -> None:
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(LOGO_SRC).convert("RGBA")
    px = im.load()
    w, h = im.size
    minx, miny, maxx, maxy = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 30:
                continue
            if r < 28 and g < 32 and b < 32:
                px[x, y] = (r, g, b, 0)
                continue
            minx, miny = min(minx, x), min(miny, y)
            maxx, maxy = max(maxx, x), max(maxy, y)
    if maxx > minx:
        cropped = im.crop((max(minx - 8, 0), max(miny - 8, 0), min(maxx + 8, w), min(maxy + 8, h)))
        cropped.save(LOGO_SRC)
        cropped.save(LOGO_DOCS)
    LOGO_DOCS.parent.mkdir(parents=True, exist_ok=True)
    if not LOGO_DOCS.exists():
        import shutil
        shutil.copy(LOGO_SRC, LOGO_DOCS)


def week_cards() -> str:
    items = []
    for num, title, desc in WEEKS_META:
        items.append(
            f'<a class="card" href="#week-{num}" data-route="week-{num}">'
            f'<div class="week">Неделя {num}</div><h3>{html.escape(title)}</h3>'
            f"<p>{html.escape(desc)}</p></a>"
        )
    return "\n".join(items)


def week_views() -> str:
    parts = []
    for num, title, _ in WEEKS_META:
        content = load_week_html(num)
        parts.append(
            f'<article id="view-week-{num}" class="view prose-wrap" hidden>'
            f'<div class="prose">{content}</div></article>'
        )
    return "\n".join(parts)


def build() -> None:
    crop_logo()
    cards = week_cards()
    views = week_views()
    week_titles_json = json.dumps({f"week-{n}": t for n, t, _ in WEEKS_META}, ensure_ascii=False)

    page = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>web-roadmap — Full-Stack за 22 недели</title>
  <meta name="description" content="Структурированный путь к junior full-stack: 22 недели, 22 проекта, Git с первого дня, финальный capstone DevHub.">
  <meta name="theme-color" content="#050508">
  <link rel="icon" href="assets/logo.png" type="image/png">
  <meta property="og:title" content="web-roadmap — Full-Stack за 22 недели">
  <meta property="og:description" content="От первого index.html до production full-stack за 22 недели.">
  <meta property="og:image" content="assets/logo.png">
  <style>
    :root {{
      color-scheme: dark;
      --bg: #050508;
      --bg-elevated: rgba(14, 14, 18, 0.92);
      --bg-card: rgba(18, 18, 22, 0.78);
      --border: rgba(255, 255, 255, 0.1);
      --text: #f5f5f7;
      --muted: #86868b;
      --neon: #ffffff;
      --neon-glow: rgba(255, 255, 255, 0.35);
      --cyan: #64d2ff;
      --cyan-dim: rgba(100, 210, 255, 0.12);
      --font: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif;
      --font-mono: "SF Mono", ui-monospace, Menlo, Monaco, Consolas, monospace;
      --max: 1080px;
      --pad: clamp(20px, 4vw, 48px);
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      font-family: var(--font);
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }}
    #code-canvas {{ position: fixed; inset: 0; z-index: 0; opacity: 0.28; pointer-events: none; }}
    .scanlines {{
      position: fixed; inset: 0; z-index: 1; pointer-events: none;
      background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px);
    }}
    .app {{ position: relative; z-index: 2; min-height: 100vh; display: flex; flex-direction: column; }}
    a {{ color: var(--cyan); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .nav-bar {{
      width: 100%;
      border-bottom: 1px solid var(--border);
      background: rgba(5, 5, 8, 0.72);
      backdrop-filter: saturate(180%) blur(20px);
      -webkit-backdrop-filter: saturate(180%) blur(20px);
      position: sticky; top: 0; z-index: 100;
    }}
    .nav-inner, .footer-inner, .section-inner, .hero-inner, .prose-wrap {{
      max-width: var(--max);
      margin: 0 auto;
      padding-left: var(--pad);
      padding-right: var(--pad);
    }}
    .nav-inner {{
      display: flex; align-items: center; justify-content: space-between;
      gap: 16px; min-height: 52px; padding-top: 12px; padding-bottom: 12px;
    }}
    .brand {{
      display: flex; align-items: center; gap: 10px;
      font-weight: 600; font-size: 17px; letter-spacing: -0.02em;
      color: var(--text); text-decoration: none;
    }}
    .brand:hover {{ text-decoration: none; opacity: 0.9; }}
    .brand img {{ width: 32px; height: 32px; object-fit: contain; }}
    .nav-links {{ display: flex; flex-wrap: wrap; gap: 22px; font-size: 14px; }}
    .nav-links a {{ color: var(--muted); }}
    .nav-links a:hover {{ color: var(--text); text-decoration: none; }}
    main {{ flex: 1; }}
    .hero {{
      text-align: center;
      padding: clamp(48px, 8vw, 96px) 0 clamp(40px, 6vw, 72px);
    }}
    .hero-logo {{ margin-bottom: 20px; }}
    .hero-logo img {{ width: 88px; height: 88px; object-fit: contain; filter: drop-shadow(0 0 24px rgba(255,255,255,0.2)); }}
    .hero h1 {{
      font-size: clamp(2.5rem, 6vw, 3.75rem);
      font-weight: 700; letter-spacing: -0.04em; line-height: 1.08;
      margin: 0 0 16px; color: var(--neon);
      text-shadow: 0 0 48px var(--neon-glow);
    }}
    .hero .lead {{
      font-size: clamp(1.05rem, 2.2vw, 1.35rem);
      color: var(--muted); max-width: 640px; margin: 0 auto 32px;
      font-weight: 400; letter-spacing: -0.01em;
    }}
    .stats {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-bottom: 36px; }}
    .stat {{
      min-width: 100px; padding: 14px 20px;
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 14px; backdrop-filter: blur(8px);
    }}
    .stat strong {{ display: block; font-size: 28px; font-weight: 600; letter-spacing: -0.03em; color: var(--text); }}
    .stat span {{ font-size: 12px; color: var(--muted); }}
    .cta-row {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }}
    .btn {{
      display: inline-flex; align-items: center; gap: 8px;
      padding: 12px 22px; border-radius: 980px; font-size: 15px; font-weight: 500;
      border: 1px solid var(--border); transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
      cursor: pointer; font-family: inherit; text-decoration: none;
    }}
    .btn:hover {{ transform: scale(1.02); text-decoration: none; }}
    .btn-primary {{ background: var(--neon); color: #000; border-color: var(--neon); box-shadow: 0 0 32px rgba(255,255,255,0.2); }}
    .btn-secondary {{ background: rgba(255,255,255,0.06); color: var(--text); }}
    .btn-ghost {{ background: transparent; color: var(--muted); }}
    .section {{ padding: clamp(48px, 7vw, 80px) 0; }}
    .section-alt {{ background: rgba(255,255,255,0.02); border-block: 1px solid var(--border); }}
    .section h2 {{
      font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 700;
      letter-spacing: -0.03em; margin: 0 0 12px; text-align: center;
    }}
    .section .sub {{
      text-align: center; color: var(--muted); font-size: 1.1rem;
      max-width: 620px; margin: 0 auto 40px; letter-spacing: -0.01em;
    }}
    .feature-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;
    }}
    .feature {{
      padding: 28px; border-radius: 18px;
      background: var(--bg-card); border: 1px solid var(--border);
      backdrop-filter: blur(8px);
    }}
    .feature h3 {{ margin: 0 0 8px; font-size: 19px; font-weight: 600; letter-spacing: -0.02em; }}
    .feature p {{ margin: 0; color: var(--muted); font-size: 15px; line-height: 1.55; }}
    .compare {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px;
    }}
    .compare-col {{
      padding: 24px; border-radius: 18px; border: 1px solid var(--border);
      background: var(--bg-card);
    }}
    .compare-col.highlight {{ border-color: rgba(255,255,255,0.28); box-shadow: 0 0 40px rgba(255,255,255,0.06); }}
    .compare-col h3 {{ margin: 0 0 12px; font-size: 17px; }}
    .compare-col ul {{ margin: 0; padding-left: 18px; color: var(--muted); font-size: 14px; }}
    .compare-col li {{ margin-bottom: 8px; }}
    .stack-flow {{
      display: flex; flex-wrap: wrap; align-items: center; justify-content: center;
      gap: 8px; font-size: 13px; font-family: var(--font-mono);
      padding: 20px; border-radius: 14px; border: 1px dashed var(--border);
      color: var(--muted); margin-bottom: 8px;
    }}
    .stack-flow span {{ color: var(--text); }}
    .stack-flow .arrow {{ color: var(--cyan); opacity: 0.6; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }}
    .card {{
      display: block; padding: 20px; border-radius: 16px;
      background: var(--bg-card); border: 1px solid var(--border);
      transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
      text-decoration: none; color: inherit;
    }}
    .card:hover {{
      border-color: rgba(255,255,255,0.22);
      transform: translateY(-2px);
      box-shadow: 0 8px 32px rgba(0,0,0,0.35);
      text-decoration: none;
    }}
    .card .week {{ font-size: 11px; color: var(--cyan); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px; }}
    .card h3 {{ margin: 0 0 6px; font-size: 17px; font-weight: 600; }}
    .card p {{ margin: 0; font-size: 13px; color: var(--muted); }}
    .community {{
      text-align: center; padding: 48px var(--pad);
      border-radius: 20px; margin: 0 var(--pad) 48px;
      max-width: calc(var(--max) + var(--pad) * 2);
      margin-left: auto; margin-right: auto;
      background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
      border: 1px solid var(--border);
    }}
    .community h2 {{ margin-bottom: 12px; }}
    .community p {{ color: var(--muted); max-width: 520px; margin: 0 auto 24px; font-size: 15px; }}
    .footer-bar {{
      width: 100%; border-top: 1px solid var(--border);
      background: rgba(5, 5, 8, 0.85); margin-top: auto;
    }}
    .footer-inner {{
      padding: 32px var(--pad) 40px; text-align: center;
      color: var(--muted); font-size: 13px;
    }}
    .footer-inner p {{ margin: 0 0 8px; }}
    /* Week / prose view */
    .page-header {{
      padding: 32px var(--pad) 24px;
      border-bottom: 1px solid var(--border);
      background: rgba(5,5,8,0.6);
      backdrop-filter: blur(12px);
    }}
    .page-header-inner {{ max-width: var(--max); margin: 0 auto; }}
    .back-link {{
      display: inline-flex; align-items: center; gap: 6px;
      font-size: 14px; color: var(--cyan); margin-bottom: 12px;
    }}
    .page-header h1 {{ margin: 0; font-size: clamp(1.5rem, 4vw, 2rem); font-weight: 700; letter-spacing: -0.03em; }}
    .prose-wrap {{ padding: 32px var(--pad) 64px; }}
    .prose {{
      max-width: var(--max); margin: 0 auto;
      font-size: 15px; line-height: 1.65;
    }}
    .prose h1 {{ font-size: 1.75rem; margin: 1.5em 0 0.6em; letter-spacing: -0.03em; color: var(--neon); }}
    .prose h2 {{ font-size: 1.35rem; margin: 1.8em 0 0.5em; padding-top: 0.5em; border-top: 1px solid var(--border); color: var(--text); }}
    .prose h3 {{ font-size: 1.1rem; margin: 1.2em 0 0.4em; color: var(--cyan); }}
    .prose p, .prose li {{ color: #d2d2d7; }}
    .prose blockquote {{
      margin: 1em 0; padding: 12px 16px;
      border-left: 3px solid var(--cyan);
      background: var(--cyan-dim); border-radius: 0 10px 10px 0;
      color: var(--muted); font-size: 14px;
    }}
    .prose code {{
      font-family: var(--font-mono); font-size: 0.88em;
      background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px;
    }}
    .prose pre {{
      background: rgba(0,0,0,0.45); border: 1px solid var(--border);
      border-radius: 12px; padding: 16px; overflow-x: auto;
    }}
    .prose pre code {{ background: none; padding: 0; font-size: 13px; color: #e8e8ed; }}
    .prose a {{ color: var(--cyan); }}
    .prose table {{ width: 100%; border-collapse: collapse; margin: 1em 0; font-size: 14px; }}
    .prose th, .prose td {{ border: 1px solid var(--border); padding: 10px 12px; text-align: left; }}
    .prose th {{ background: rgba(255,255,255,0.04); color: var(--text); }}
    .prose ul, .prose ol {{ padding-left: 1.4em; }}
    .prose li.task {{ list-style: none; margin-left: -1.4em; }}
    .prose hr {{ border: none; border-top: 1px solid var(--border); margin: 2em 0; }}
    .prose strong {{ color: var(--text); }}
    @media (max-width: 640px) {{
      .nav-links {{ display: none; }}
      .nav-links.open {{ display: flex; width: 100%; flex-direction: column; padding-bottom: 12px; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      #code-canvas, .scanlines {{ display: none; }}
      .btn:hover, .card:hover {{ transform: none; }}
    }}
  </style>
</head>
<body>
  <canvas id="code-canvas" aria-hidden="true"></canvas>
  <div class="scanlines" aria-hidden="true"></div>
  <div class="app">
    <header class="nav-bar">
      <div class="nav-inner">
        <a class="brand" href="#home" data-route="home">
          <img src="assets/logo.png" alt="" width="32" height="32">
          web-roadmap
        </a>
        <nav class="nav-links" id="nav-links">
          <a href="#why">Зачем</a>
          <a href="#weeks">22 недели</a>
          <a href="#community">Сообщество</a>
          <a href="https://github.com/krwg/web-roadmap">GitHub</a>
        </nav>
      </div>
    </header>

    <div id="view-home" class="view">
      <main>
        <header class="hero">
          <div class="hero-inner">
            <div class="hero-logo"><img src="assets/logo.png" alt="web-roadmap" width="88" height="88"></div>
            <h1>Стать full-stack разработчиком — по плану, не по хаосу</h1>
            <p class="lead">
              22 недели ежедневной практики: от первого <code>index.html</code> и коммита в Git
              до production-приложения с тестами, Docker и деплоем.
              Не видеокурс — <strong>маршрут с проектами</strong>, которые останутся в портфолио.
            </p>
            <div class="stats">
              <div class="stat"><strong>22</strong><span>недели</span></div>
              <div class="stat"><strong>22</strong><span>проекта</span></div>
              <div class="stat"><strong>1</strong><span>capstone</span></div>
              <div class="stat"><strong>154</strong><span>дня</span></div>
            </div>
            <div class="cta-row">
              <a class="btn btn-primary" href="#week-01" data-route="week-01">Начать с недели 1</a>
              <a class="btn btn-secondary" href="#why">Узнать больше</a>
            </div>
          </div>
        </header>

        <section class="section section-alt" id="why">
          <div class="section-inner">
            <h2>Что вы получите</h2>
            <p class="sub">Не обещание «стань сеньором за месяц» — реалистичный путь к уровню junior full-stack с доказуемыми навыками.</p>
            <div class="feature-grid">
              <div class="feature">
                <h3>Понятный порядок тем</h3>
                <p>HTML → CSS → JS → React → Python → SQL → API → Docker. Без скачков «сразу на фреймворк» и дыр в фундаменте.</p>
              </div>
              <div class="feature">
                <h3>22 проекта в GitHub</h3>
                <p>Каждая неделя — работающий артефакт в <code>learning-log</code>. К концу — портфолио, которое можно показать рекрутеру.</p>
              </div>
              <div class="feature">
                <h3>Git с первого дня</h3>
                <p>Первый коммит — ваш <code>index.html</code> на неделе 1. Привычка версионировать код с самого начала, как в реальной команде.</p>
              </div>
              <div class="feature">
                <h3>Теория + практика + ревью</h3>
                <p>Каждый день: что читать, что сделать руками, типичные ловушки и чеклист самопроверки. Протокол «анти-вайбкодер».</p>
              </div>
              <div class="feature">
                <h3>Финальный DevHub capstone</h3>
                <p>Неделя 22 — полноценное приложение: React, API, PostgreSQL, JWT, Docker, CI и deploy. Всё, что вы учили, в одном проекте.</p>
              </div>
              <div class="feature">
                <h3>Литература и ссылки</h3>
                <p>MDN, Pro Git, learn.javascript.ru, react.dev, FastAPI — подобранные материалы, а не бесконечный Google без направления.</p>
              </div>
            </div>
          </div>
        </section>

        <section class="section" id="who">
          <div class="section-inner">
            <h2>Кому подойдёт</h2>
            <p class="sub">Маршрут создан для тех, кто готов учиться системно — 6–7 часов в день, с дисциплиной и любопытством.</p>
            <div class="feature-grid">
              <div class="feature">
                <h3>Новичкам с нуля</h3>
                <p>Нет опыта в коде — не страшно. Недели 1–3 дают базу вёрстки, дальше плавный вход в JavaScript и full-stack.</p>
              </div>
              <div class="feature">
                <h3>Самоучкам</h3>
                <p>Уже пробовали туториалы, но «всё в куче»? Здесь порядок, проекты и чеклисты закрывают пробелы.</p>
              </div>
              <div class="feature">
                <h3>Junior'ам</h3>
                <p>Работаете с React, но слабый SQL или Git? Пройдите выборочно слабые недели и соберите capstone.</p>
              </div>
            </div>
          </div>
        </section>

        <section class="section section-alt" id="compare">
          <div class="section-inner">
            <h2>Почему этот роадмап</h2>
            <p class="sub">Мы не против roadmap.sh или видеокурсов — мы за то, чтобы у самоучки был один связный маршрут с практикой каждый день.</p>
            <div class="compare">
              <div class="compare-col">
                <h3>Обычный путь</h3>
                <ul>
                  <li>Случайные туториалы без связи</li>
                  <li>ИИ пишет код — вы не понимаете</li>
                  <li>Нет проектов в портфолио</li>
                  <li>Git «когда-нибудь потом»</li>
                  <li>Фреймворк без основ JS/HTML</li>
                </ul>
              </div>
              <div class="compare-col highlight">
                <h3>web-roadmap</h3>
                <ul>
                  <li>154 дня с конкретными заданиями</li>
                  <li>Практика руками, ИИ только для ревью</li>
                  <li>22 проекта + capstone DevHub</li>
                  <li>Коммит каждый день с недели 1</li>
                  <li>Full-stack: фронт, бэк, БД, DevOps</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section class="section" id="stack">
          <div class="section-inner">
            <h2>Стек маршрута</h2>
            <p class="sub">От разметки до деплоя — технологии, которые востребованы у junior full-stack в 2026.</p>
            <div class="stack-flow">
              <span>HTML</span><span class="arrow">→</span>
              <span>CSS</span><span class="arrow">→</span>
              <span>Git</span><span class="arrow">→</span>
              <span>JS</span><span class="arrow">→</span>
              <span>TS</span><span class="arrow">→</span>
              <span>React</span><span class="arrow">→</span>
              <span>Python</span><span class="arrow">→</span>
              <span>SQL</span><span class="arrow">→</span>
              <span>FastAPI</span><span class="arrow">→</span>
              <span>Node</span><span class="arrow">→</span>
              <span>Docker</span><span class="arrow">→</span>
              <span>Deploy</span>
            </div>
          </div>
        </section>

        <section class="section section-alt" id="weeks">
          <div class="section-inner">
            <h2>22 недели</h2>
            <p class="sub">Нажмите на карточку — откроется план недели с теорией, практикой и проектом.</p>
            <div class="grid">{cards}</div>
          </div>
        </section>

        <section class="community" id="community">
          <h2>Помогите маршруту расти</h2>
          <p>
            Если материал помог вам — поставьте звезду репозиторию, поделитесь с тем, кто только начинает,
            или предложите улучшение через Issue. Так роадмап становится лучше для следующих учеников.
          </p>
          <div class="cta-row">
            <a class="btn btn-primary" href="https://github.com/krwg/web-roadmap" target="_blank" rel="noopener">★ Star на GitHub</a>
            <button type="button" class="btn btn-secondary" id="share-btn">Поделиться</button>
            <a class="btn btn-ghost" href="https://github.com/krwg/web-roadmap/issues/new/choose" target="_blank" rel="noopener">Предложить улучшение</a>
          </div>
        </section>
      </main>

      <footer class="footer-bar">
        <div class="footer-inner">
          <p>web-roadmap · маршрут к профессии full-stack разработчика</p>
          <p><a href="https://github.com/krwg/web-roadmap">GitHub</a> · <a href="https://github.com/krwg/web-roadmap/blob/main/license">License</a></p>
        </div>
      </footer>
    </div>

    <div id="view-week" class="view" hidden>
      <div class="page-header">
        <div class="page-header-inner">
          <a class="back-link" href="#weeks" data-route="home">← Все недели</a>
          <h1 id="week-page-title">Неделя</h1>
        </div>
      </div>
      <div id="week-content-slot"></div>
    </div>

    <div id="week-sources" hidden aria-hidden="true">
{views}
    </div>
  </div>

  <script>
    const WEEK_TITLES = {week_titles_json};

    function route() {{
      const raw = (location.hash || '#home').slice(1);
      const isWeek = /^week-\\d{{2}}$/.test(raw);
      document.querySelectorAll('.view').forEach(v => {{ v.hidden = true; }});
      if (isWeek) {{
        const slot = document.getElementById('week-content-slot');
        const src = document.getElementById('view-' + raw);
        const weekView = document.getElementById('view-week');
        if (src && slot) {{
          slot.innerHTML = '';
          const wrap = document.createElement('div');
          wrap.className = 'prose-wrap';
          wrap.appendChild(src.querySelector('.prose').cloneNode(true));
          slot.appendChild(wrap);
          document.getElementById('week-page-title').textContent = WEEK_TITLES[raw] || raw;
          weekView.hidden = false;
        }}
      }} else {{
        const home = document.getElementById('view-home');
        if (home) home.hidden = false;
        if (raw && raw !== 'home') {{
          const el = document.getElementById(raw);
          if (el) el.scrollIntoView({{ behavior: 'smooth' }});
        }}
      }}
      window.scrollTo(0, 0);
    }}

    document.addEventListener('click', e => {{
      const a = e.target.closest('[data-route]');
      if (!a) return;
      e.preventDefault();
      const r = a.getAttribute('data-route');
      location.hash = r === 'home' ? 'weeks' : r;
    }});

    window.addEventListener('hashchange', route);
    route();

    document.getElementById('share-btn')?.addEventListener('click', async () => {{
      const url = 'https://krwg.github.io/web-roadmap/';
      const data = {{ title: 'web-roadmap', text: 'Full-stack веб за 22 недели', url }};
      try {{
        if (navigator.share) await navigator.share(data);
        else {{ await navigator.clipboard.writeText(url); alert('Ссылка скопирована'); }}
      }} catch (_) {{}}
    }});

    (function rain() {{
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      const canvas = document.getElementById('code-canvas');
      const ctx = canvas.getContext('2d');
      const snippets = ['git commit -m "week-01"', 'useEffect(() => {{}})', 'SELECT * FROM users',
        'docker compose up', 'export default function App()', 'async function fetchData()',
        'interface User {{', 'CREATE TABLE tasks', 'npm run build', 'pytest -v'];
      let cols, drops, fontSize = 13;
      function resize() {{
        canvas.width = innerWidth; canvas.height = innerHeight;
        cols = Math.floor(canvas.width / fontSize);
        drops = Array(cols).fill(1);
      }}
      function draw() {{
        ctx.fillStyle = 'rgba(5,5,8,0.09)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.font = fontSize + 'px ' + getComputedStyle(document.body).fontFamily;
        for (let i = 0; i < drops.length; i++) {{
          const t = snippets[Math.floor(Math.random() * snippets.length)];
          const bright = Math.random() > 0.97;
          ctx.fillStyle = bright ? '#fff' : 'rgba(160,160,170,0.5)';
          ctx.fillText(t, i * fontSize, drops[i] * fontSize);
          if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
          drops[i]++;
        }}
        requestAnimationFrame(draw);
      }}
      resize();
      addEventListener('resize', resize);
      draw();
    }})();
  </script>
</body>
</html>"""

    OUT.write_text(page, encoding="utf-8")
    print(f"Built {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    build()
