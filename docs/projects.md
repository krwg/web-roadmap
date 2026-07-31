# Каталог проектов: 22 + Capstone

Каждая неделя заканчивается **работающим проектом** в вашем репозитории `learning-log`.  
Недели 1–21 накапливают навыки; **неделя 22** — единый крупномасштабный capstone со всем стеком.

**Правило:** проект недели = отдельная папка `week-NN/` (или `week-NN-project-name/`), тег `week-NN-done`, README внутри папки.

---

## Обзор

| Нед. | Проект | Стек | Папка |
|------|--------|------|-------|
| 01 | **Portfolio Landing** | HTML, a11y, формы | `week-01/` |
| 02 | **Styled Blog Post** | CSS, design tokens | `week-02/` |
| 03 | **SaaS Landing** | Flexbox, Grid, адаптив | `week-03/` |
| 04 | **OSS Workflow Kit** | Git, PR, GitHub Pages | `week-04/` |
| 05 | **Console Task Manager** | Vanilla JS, массивы | `week-05/` |
| 06 | **DOM Todo App** | DOM, события | `week-06/` |
| 07 | **Notes Dashboard** | ES modules, Fetch, storage | `week-07/` |
| 08 | **Movie Catalog** | async/await, REST API | `week-08/` |
| 09 | **Library System** | OOP, паттерны, Observer | `week-09/` |
| 10 | **Typed API Client** | TypeScript strict | `week-10/` |
| 11 | **React Todo** | React, Vite, TS | `week-11/` |
| 12 | **React Todo Pro** | hooks, effects, API | `week-12/` |
| 13 | **Portfolio SPA** | Router, Context | `week-13/` |
| 14 | **React Dashboard** | Frontend SPA capstone | `week-14/` |
| 15 | **CLI Expense Tracker** | Python, JSON, rich | `week-15/` |
| 16 | **CLI Task Manager** | Python OOP, SQLite | `week-16/` |
| 17 | **Library Database** | PostgreSQL, SQL | `week-17/` |
| 18 | **Library REST API** | FastAPI, SQLAlchemy | `week-18/` |
| 19 | **Express Notes API** | Node, Express, Zod | `week-19/` |
| 20 | **Secure Notes** | JWT, auth, tests | `week-20/` |
| 21 | **Task Manager Docker** | docker-compose full-stack | `week-21/` |
| 22 | **DevHub Capstone** | Всё вместе + deploy | `week-22-capstone/` |

---

## Неделя 1 — Portfolio Landing

**Цель:** многостраничный статический сайт-портфолио с формами и доступностью.

**Функции:**
- 3 страницы: главная, «Обо мне», «Контакты» (или галерея)
- Семантическая разметка, единая навигация
- Форма обратной связи с HTML5-валидацией
- Галерея работ (заглушки), таблица навыков
- Skip-link, Lighthouse a11y ≥ 90, W3C valid

**Git:** репозиторий создан в день 1; к концу недели ≥ 7 коммитов, тег `week-01-done`.

→ [week-01.md](../roadmap/weeks/week-01.md)

---

## Неделя 2 — Styled Blog Post

**Цель:** одна страница статьи с дизайн-системой на CSS-переменных.

**Функции:**
- Design tokens в `:root` (цвета, spacing, radius, шрифты)
- Hero, article (`max-width: 65ch`), sidebar, footer
- Карточки «похожих статей», тёмная тема через класс
- `clamp()` для заголовков, типографическая шкала

**Git:** ветка `feature/dark-theme`, merge в `main`, тег `week-02-done`.

→ [week-02.md](../roadmap/weeks/week-02.md)

---

## Неделя 3 — SaaS Landing

**Цель:** адаптивный одностраничник вымышленного SaaS-продукта.

**Функции:**
- 5+ секций: hero, features, pricing, testimonials, CTA, footer
- Mobile-first, 2+ breakpoint, sticky nav
- CSS Grid (features/pricing), Flexbox (header/cards)
- Анимации появления + `prefers-reduced-motion`

**Git:** ≥ 10 коммитов за неделю, осмысленные сообщения, тег `week-03-done`.

→ [week-03.md](../roadmap/weeks/week-03.md)

---

## Неделя 4 — OSS Workflow Kit

**Цель:** оформить learning-log как open-source проект с профессиональным Git-workflow.

**Функции:**
- README с badges, скриншотами недель 1–3
- CONTRIBUTING.md, LICENSE (MIT для learning-log)
- ≥ 2 feature-ветки, 1 merged PR (можно self-merge через branch protection off)
- GitHub Pages для week-03 лендинга
- CHANGELOG.md, Conventional Commits

**Git:** rebase или merge — осознанный выбор, тег `week-04-done`.

→ [week-04.md](../roadmap/weeks/week-04.md)

---

## Неделя 5 — Console Task Manager

**Цель:** менеджер задач в консоли браузера (без DOM).

**Функции:** CRUD, фильтры, статистика (`reduce`), объекты `{id, title, done, createdAt}`.

→ [week-05.md](../roadmap/weeks/week-05.md)

---

## Неделя 6 — DOM Todo App

**Цель:** интерактивный Todo на ванильном JS с **event delegation**, без `innerHTML` для пользовательского текста.

**Стек:** HTML + CSS + один (или модульный) JS, без фреймворков.

### Функции (полный)
- Список задач: добавить / отметить done / удалить / редактировать (inline или modal)
- Фильтры: All / Active / Completed; счётчик оставшихся
- Persist в `localStorage`; восстановление после reload
- Клавиатура: Enter — добавить, Escape — отменить edit
- Event delegation на контейнере списка (не listener на каждую кнопку)
- Текст задачи через `textContent` / `createElement`, не конкатенация HTML

### Лайт / MVP
- Add + toggle done + delete
- Persist в localStorage
- Delegation на списке

### DoD
- [ ] Нет XSS через ввод названия задачи
- [ ] После F5 список тот же
- [ ] README: скрин + как открыть (Live Server)
- [ ] Тег `week-06-done`

**Reference stub:** [`docs/reference-stubs/week-06/`](reference-stubs/week-06/README.md)

→ [week-06.md](../roadmap/weeks/week-06.md)

---

## Неделя 7 — Notes Dashboard

**Цель:** SPA на ванильном JS: заметки + погода + GitHub user search.

**Функции:** ES modules (5+ файлов), localStorage, 2 внешних API.

→ [week-07.md](../roadmap/weeks/week-07.md)

---

## Неделя 8 — Movie Catalog

**Цель:** async-каталог фильмов (OMDb или аналог) с поиском, избранным и явными UI-состояниями.

**Стек:** ES modules, `fetch` + `async/await`, CSS на ваш вкус.

### Функции (полный)
- Поиск по названию; debounce ≥ 300 мс
- Карточки: постер (placeholder если нет), название, год
- Детали фильма (модалка или отдельный view): plot, rating, runtime
- Избранное в `localStorage`
- Состояния: loading / empty / error (сеть, 401 ключа, 0 результатов)
- Ключ API только в конфиге, который в `.gitignore` (или demo-режим с mock JSON)

### Лайт / MVP
- Поиск + список карточек + loading/error
- Без избранного и без детальной модалки

### DoD
- [ ] Нет необработанных Promise rejection в Console
- [ ] README: как получить API key / как включить mock
- [ ] Тег `week-08-done`

**Reference stub:** [`docs/reference-stubs/week-08/`](reference-stubs/week-08/README.md)

→ [week-08.md](../roadmap/weeks/week-08.md)

---

## Неделя 9 — Library System (JS)

**Цель:** OOP: `Book`, `Member`, `Library`, Observer, localStorage.

→ [week-09.md](../roadmap/weeks/week-09.md)

---

## Неделя 10 — Typed API Client

**Цель:** TS-библиотека fetch + storage, strict mode, zero `any`.

→ [week-10.md](../roadmap/weeks/week-10.md)

---

## Неделя 11 — React Todo

**Цель:** первое React-приложение на Vite + TS, 8+ компонентов.

→ [week-11.md](../roadmap/weeks/week-11.md)

---

## Неделя 12 — React Todo Pro

**Цель:** приоритеты, дедлайны, фильтры, Quotable API, persist.

→ [week-12.md](../roadmap/weeks/week-12.md)

---

## Неделя 13 — Portfolio SPA

**Цель:** роутинг, ThemeContext, custom hooks, mock-auth `/admin`.

→ [week-13.md](../roadmap/weeks/week-13.md)

---

## Неделя 14 — React Dashboard (Frontend milestone)

**Цель:** SPA на React + TypeScript с 4 маршрутами — крупнейший фронтенд до бэкенда.

**Стек:** Vite, React 18+, React Router, Context (или лёгкий store), CSS Modules / обычный CSS.

### Маршруты (полный)
1. `/` — Dashboard: 2–3 виджета статистики (задачи, mock metrics)
2. `/tasks` — CRUD задач (клиентский state + persist)
3. `/weather` или `/github` — данные с внешнего API + loading/error
4. `/settings` — тема, имя пользователя, reset данных

### Дополнительно (полный)
- Protected mock-route или feature-flag секция
- Responsive layout, пустые состояния
- Deploy preview (Vercel/Netlify) + URL в README

### Лайт / MVP
- 3 маршрута: home stats, tasks CRUD, settings
- Без внешнего API; persist localStorage

### DoD
- [ ] TypeScript strict, нет `any` в своих файлах
- [ ] Роутинг работает по прямому URL (refresh на `/tasks`)
- [ ] Live demo или screenshots
- [ ] Тег `week-14-done`

**Reference stub:** [`docs/reference-stubs/week-14/`](reference-stubs/week-14/README.md)

→ [week-14.md](../roadmap/weeks/week-14.md)

---

## Неделя 15 — CLI Expense Tracker

**Цель:** Python CLI, категории, JSON, `rich` таблицы.

→ [week-15.md](../roadmap/weeks/week-15.md)

---

## Неделя 16 — CLI Task Manager (SQLite)

**Цель:** ООП, SQLite, теги many-to-many, транзакции.

→ [week-16.md](../roadmap/weeks/week-16.md)

---

## Неделя 17 — Library Database

**Цель:** PostgreSQL схема библиотеки, 15+ запросов, индексы, EXPLAIN.

→ [week-17.md](../roadmap/weeks/week-17.md)

---

## Неделя 18 — Library REST API

**Цель:** REST API «Библиотека» на FastAPI + SQLAlchemy (или SQLModel) поверх схемы недели 17.

**Стек:** Python 3.12+, FastAPI, PostgreSQL, Alembic (или SQL-миграции), pytest, uvicorn.

### Эндпоинты (полный)
- CRUD авторов и книг; связь many-to-one / many-to-many по вашей схеме
- Пагинация списка (`limit`/`offset` или cursor)
- Фильтры (автор, год, наличие)
- Валидация Pydantic; единый error envelope
- OpenAPI/Swagger из коробки; healthcheck `/health`
- ≥ 8 pytest: happy path + 404 + валидация

### Лайт / MVP
- CRUD книг + список авторов
- 4 pytest
- Swagger открывается

### DoD
- [ ] `README` с `docker compose` **или** локальным Postgres + `.env.example`
- [ ] Нет секретов в git
- [ ] Тег `week-18-done`

**Reference stub:** [`docs/reference-stubs/week-18/`](reference-stubs/week-18/README.md)

→ [week-18.md](../roadmap/weeks/week-18.md)

---

## Неделя 19 — Express Notes API

**Цель:** layered Express API, Zod, PostgreSQL, Postman collection.

→ [week-19.md](../roadmap/weeks/week-19.md)

---

## Неделя 20 — Secure Notes

**Цель:** JWT auth, bcrypt, rate limit, React client, pytest + Vitest.

→ [week-20.md](../roadmap/weeks/week-20.md)

---

## Неделя 21 — Task Manager Docker

**Цель:** React + API + PostgreSQL в `docker-compose`, healthchecks, seed.

→ [week-21.md](../roadmap/weeks/week-21.md)

---

## Неделя 22 — DevHub Capstone (финальный)

**Единственный проект, объединяющий весь стек.** Не начинайте с нуля в последний день — планируйте в день 148, кодите 149–153, полируйте и деплойте в день 154.

### Концепция: DevHub

Персональная **платформа разработчика**: дашборд + заметки + задачи + интеграция с GitHub API — full-stack production app.

### Обязательный стек

| Слой | Технологии |
|------|------------|
| Frontend | React 18+, TypeScript, React Router, Context/Zustand |
| Backend | FastAPI **или** Express (один основной) |
| БД | PostgreSQL, миграции, seed |
| Auth | JWT (register/login/refresh), protected routes |
| Infra | Docker Compose локально, CI (GitHub Actions) |
| Deploy | Frontend → Vercel/Netlify, Backend + DB → Render/Railway/Neon |
| Quality | pytest ≥ 15, Vitest ≥ 12, ESLint, README, `.env.example` |

### Функции MVP (минимум)

1. **Auth:** регистрация, логин, logout, защищённые маршруты
2. **Tasks:** CRUD с приоритетом, статусом, дедлайном (per user)
3. **Notes:** markdown-заметки с тегами, поиск
4. **Dashboard:** статистика задач, виджет погоды или GitHub repos
5. **Profile:** аватар URL, bio, смена пароля
6. **API:** REST, OpenAPI/Swagger, пагинация, валидация
7. **Security:** bcrypt, CORS, helmet, rate limit, OWASP checklist в `SECURITY.md`
8. **Tests:** auth flow, CRUD tasks, 401 без токена
9. **Docs:** architecture diagram, setup за 5 команд, live demo URLs

### Лайт / MVP (capstone)

Если времени мало — сузьте scope, но не ломайте «сквозной» путь:

- Auth + Tasks CRUD + один Dashboard-виджет
- Один backend на выбор (FastAPI **или** Express)
- Deploy хотя бы frontend; API можно на Render free / туннель
- Тесты: ≥ 5 backend + ≥ 5 frontend
- `FINAL_REVIEW.md` обязателен

Полный MVP (9 пунктов выше) — для сильного портфолио.

### Reference stub

Каркас монорепо: [`docs/reference-stubs/week-22/`](reference-stubs/week-22/README.md)

### Структура репозитория

```
week-22-capstone/
├── frontend/          # Vite React TS
├── backend/           # FastAPI or Express
├── docker-compose.yml
├── .github/workflows/ci.yml
├── SECURITY.md
├── ARCHITECTURE.md
└── README.md          # demo links, screenshots
```

### Критерии сдачи capstone

- [ ] Live HTTPS demo (frontend + API)
- [ ] `docker compose up` поднимает всё локально
- [ ] Auth end-to-end работает
- [ ] ≥ 5 сущностей в БД со связями
- [ ] CI green на push
- [ ] `FINAL_REVIEW.md`: что узнал, что бы сделал иначе
- [ ] GitHub profile README обновлён со ссылками на все 22 проекта

→ [week-22.md](../roadmap/weeks/week-22.md)

---

## Портфолио после 22 недель

В README `learning-log` добавьте таблицу:

| Неделя | Проект | Demo | Стек |
|--------|--------|------|------|
| 01 | Portfolio Landing | link | HTML |
| … | … | … | … |
| 22 | DevHub | link | Full-Stack |

Это главное доказательство навыков для рекрутера.
