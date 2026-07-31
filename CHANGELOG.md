# CHANGELOG

Формат основан на [Keep a Changelog](https://keepachangelog.com/).

## [1.2.3] — 2026-08-01

### Fixed
- TOC дней на сайте: якоря переносятся на `<h2 id>`, day-nav снова работает
- Ссылки на `projects.md#…` → `#projects--projects-…` (больше не `#projects#…`)
- `getting-started`: создание **своего** пустого `learning-log`, не clone автора
- week-00: убраны AI-хвосты, уникальные якоря дней, честные часы
- Версии выровнены на **1.2.3** (README, week-meta, сайт)

### Added
- Лайт / полный: два блока практики на день (`rebalance-weeks.py`)
- Пересчёт часов дня по объёму теории и практики (не копипаст 1.5+2.5)
- Разнообразные «Если застрял» по теме дня
- Расширенные ТЗ проектов 6 / 8 / 14 / 18 (+ лайт DoD у capstone)
- Reference stubs: `docs/reference-stubs/week-{06,08,14,18,22}/`
- Прогресс по дням + `window.webRoadmapProgress.export/import` для sync
- Prerender URL: `docs/w/NN.html` + `sitemap.xml`
- SEO: `og:type`, Twitter card, canonical

### Changed
- Homepage: вместо «скоро» — ссылки на старт / каталог проектов / capstone

## [1.2.3] — 2026-07-08 (patch notes retained)

### Fixed
- CI link-check: обновлены битые URL (React Router v6, MDN, SQLBolt, DOM Enlightenment → архив)
- Исправлены локальные ссылки в `week-00.md` (`weeks/week-01.md` → `week-01.md`)
- CI: `scripts/check-links.py` вместо lychee (стабильнее, без 7-минутных таймаутов)

## [1.2.2] — 2026-07-08

### Added
- GoatCounter analytics (`krwg.goatcounter.com`)
- [Material Symbols](https://fonts.google.com/icons) вместо эмодзи в интерфейсе
- «Продолжить обучение» — возврат к последней неделе
- Секция «Как устроено обучение» (4 шага)
- FAQ с аккордеоном
- Панель «Следующий модуль» в уроке

### Removed
- Бейдж «Full-Stack · 22 проекта · Бесплатно»

## [1.2.1] — 2026-07-07

### Added
- Визуальный редизайн в стиле профессиональной школы: жёлтый акцент, Inter, карточки модулей с фазами
- Секции «Путь обучения», треки полный/лайт, фильтр по фазам на главной
- Scroll-spy в оглавлении урока

### Fixed
- Загрузка статических страниц (`intro`, `start`, `projects`, шпаргалки)
- Кэш service worker для обновлённых стилей

### Removed
- GoatCounter (требует ручной регистрации аккаунта)

## [1.2.0] — 2026-07-07

### Added
- Неделя 0 (онбординг)
- Шпаргалки: HTML/CSS, JS, React, SQL, FastAPI
- Сайт: lazy-load недель, TOC, поиск, прогресс, reading mode, PWA
- Блоки «Если застрял», время полный/лайт, «Проверь себя» во всех неделях
- GoatCounter analytics, OG-баннер, Prism подсветка кода
- CI: link-check, сборка сайта
- `author-notes/` для живых заметок автора

### Changed
- Теория всех 22 недель — проза + ссылки
- Сборка: `index.html` лёгкий shell + `weeks/*.json`

## [1.1.0] — 2026-07-06

### Added
- GitHub Pages лендинг (неон ч/б)
- 22 проекта + DevHub capstone
- Git с дня 1

## [1.0.0] — 2026-07-06

### Added
- Первый релиз: 22 недели full-stack маршрута

[1.2.3]: https://github.com/krwg/web-roadmap/compare/v1.2.2...v1.2.3
[1.2.2]: https://github.com/krwg/web-roadmap/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/krwg/web-roadmap/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/krwg/web-roadmap/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/krwg/web-roadmap/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/krwg/web-roadmap/releases/tag/v1.0.0
