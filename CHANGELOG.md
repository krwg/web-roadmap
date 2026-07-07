# CHANGELOG

Формат основан на [Keep a Changelog](https://keepachangelog.com/).

## [1.2.3] — 2026-07-08

### Fixed
- CI link-check: обновлены битые URL (React Router v6, MDN, SQLBolt, DOM Enlightenment → архив)
- `.lychee.toml` с retry и exclude для placeholder-ссылок

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
