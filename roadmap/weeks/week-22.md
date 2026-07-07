# Неделя 22: DevHub Capstone — финальный full-stack проект

> **Цель недели:** собрать, протестировать и задеплоить **DevHub** — единый capstone, объединяющий весь стек 22 недель обучения.
> **Литература:** [docs/projects.md — DevHub Capstone](../../docs/projects.md#неделя-22--devhub-capstone-финальный), [Vercel Docs](https://vercel.com/docs), [Render Docs](https://render.com/docs), [GitHub Actions](https://docs.github.com/en/actions)
> **Проект недели:** [DevHub Capstone](../../docs/projects.md#неделя-22--devhub-capstone-финальный) — персональная платформа разработчика: дашборд + заметки + задачи + GitHub API.
> **Git:** папка `learning-log/week-22-capstone/`, feature-ветки по дням 149–153; тег `week-22-done` + обновление GitHub Profile README.

**Не начинайте с нуля в последний день.** Планируйте в день 148, кодите 149–153, деплой и портфолио — в день 154. Полная спецификация MVP, стека и критериев сдачи — в [каталоге проектов](../../docs/projects.md#неделя-22--devhub-capstone-финальный).

---

## День 148 (Пн): Планирование DevHub Capstone

### Теория

DevHub Capstone — синтез 22 недель обучения. Не начинай код в последний день: день 148 — планирование, 149–153 — реализация, 154 — deploy и портфолио. Прочитай полную спецификацию в projects.md: концепция (дашборд + заметки + задачи + GitHub API), обязательный стек, MVP vs nice-to-have.

Scope control критичен: 7 дней, фиксированный MVP из 9 пунктов. WebSocket, kanban drag-and-drop, chat — после MVP. User stories формата «As a developer, I want…» с acceptance criteria превращают размытые идеи в проверяемые задачи.

Структура repo: `frontend/`, `backend/`, `docker-compose.yml`, `.github/workflows/ci.yml`. Выбери один backend: FastAPI (нед. 18) или Express (нед. 19). ER-диаграмма ≥ 5 сущностей, API endpoints list, page map React — артефакты до первой строки кода. Скопируй структуру week-21 как стартовую точку.

**Читать:**

- [DevHub Capstone](../../docs/projects.md#неделя-22--devhub-capstone-финальный)
- [Концепция DevHub](../../docs/projects.md#концепция-devhub)
- [Функции MVP](../../docs/projects.md#функции-mvp-минимум)

**Ключевая мысль:** PLAN.md фиксирует scope; два backend одновременно — ловушка недели.

### Практика
1. Прочитай [весь раздел capstone](../../docs/projects.md#неделя-22--devhub-capstone-финальный) и выпиши чеклист MVP (9 пунктов из projects.md)
2. Выбери backend: FastAPI (нед. 18) или Express (нед. 19) — один основной стек
3. User stories: минимум 10 штук (auth, tasks, notes, dashboard, profile, API, security, tests, docs)
4. ER-диаграмма: `users`, `tasks`, `notes`, `tags`, `note_tags` — ≥ 5 сущностей со связями
5. API endpoints list: `/auth/*`, `/api/v1/tasks`, `/api/v1/notes`, `/api/v1/profile`, `/api/v1/dashboard`
6. Page map React: `/login`, `/register`, `/dashboard`, `/tasks`, `/notes`, `/profile`
7. GitHub repo `week-22-capstone`, README skeleton, GitHub Projects board
8. Скопируй структуру из [week-21](../../docs/projects.md#неделя-21--task-manager-docker) как стартовую точку

**Критерии:**
- [ ] MVP scope зафиксирован в `PLAN.md` — не расползается
- [ ] ≥ 10 user stories с acceptance criteria
- [ ] ER-диаграмма и API list в repo
- [ ] Repo создан, ветка `main` + strategy feature branches

### Git
- Закоммить изменения дня: `git add week-22-capstone/` → `git commit -m "week 22 day 148: DevHub planning PLAN.md and ER diagram"`

### Ловушки
- Scope creep: drag-and-drop kanban + WebSocket + chat в MVP
- Два backend одновременно — выбери один, второй только для сравнения в README

---

## День 149 (Вт): Backend DevHub

### Теория

Backend DevHub — layered API: routers → services → repositories → PostgreSQL. Переиспользуй паттерны Library REST API (нед. 18) или Express Notes (нед. 19): APIRouter/Express Router, Pydantic/Zod validation, пагинация `{ items, total, page, size }`, OpenAPI/Swagger.

Схема БД: `users`, `tasks`, `notes`, `tags`, `note_tags` — минимум 5 сущностей со связями. CRUD tasks с `user_id` FK; notes с markdown body и тегами many-to-many. `GET /api/v1/dashboard/stats` — агрегаты для виджетов. Пока без auth — заглушка `user_id`, auth на день 151.

Миграции: Alembic (FastAPI) или SQL scripts (Express). Seed: demo user + sample data для демо и тестов. `.env.example`: `DATABASE_URL`, `JWT_SECRET`, `APP_ENV`. God router на 500 строк — разбей по доменам. Пагинация с первого дня — иначе сломается на реальных данных.

**Читать:**

- [Library REST API (нед. 18)](../../docs/projects.md#неделя-18--library-rest-api)
- [Express Notes (нед. 19)](../../docs/projects.md#неделя-19--express-notes-api)
- [FastAPI Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

**Ключевая мысль:** backend capstone = CRUD + schema + seed + OpenAPI до auth layer.

### Практика
1. Инициализируй `backend/` — FastAPI или Express по выбору из дня 148
2. Модели/таблицы: `users`, `tasks`, `notes`, `tags`, `note_tags` (many-to-many)
3. CRUD `/api/v1/tasks`: title, priority, status, deadline, `user_id` FK
4. CRUD `/api/v1/notes`: title, body (markdown), tags, search query param
5. `GET /api/v1/dashboard/stats` — count tasks by status, recent notes
6. Swagger `/docs` (FastAPI) или OpenAPI export; пагинация `{ items, total, page, size }`
7. `schema.sql` / Alembic migration + `seed.sql` с demo данными
8. `.env.example`: `DATABASE_URL`, `JWT_SECRET`, `APP_ENV`

**Критерии:**
- [ ] ≥ 5 сущностей в БД со связями (см. [критерии сдачи](../../docs/projects.md#критерии-сдачи-capstone))
- [ ] Tasks и Notes CRUD работают (пока без auth — заглушка user_id)
- [ ] OpenAPI/Swagger актуален
- [ ] Seed выполняется одной командой

### Git
- Закоммить изменения дня: `git add week-22-capstone/backend/` → `git commit -m "week 22 day 149: DevHub backend models and CRUD API"`

### Ловушки
- God router на 500 строк — разбей по доменам
- Нет пагинации — сломается на реальных данных

---

## День 150 (Ср): Frontend DevHub (React + TypeScript)

### Теория

Frontend DevHub собирает навыки Portfolio SPA (нед. 13) и React Dashboard (нед. 14). React 18+ TypeScript, React Router, Context или Zustand для глобального state. Структура: `pages/`, `components/`, `hooks/`, `services/api.ts`, `types/`. `VITE_API_URL` — base URL API.

Четыре+ маршрута с Layout: `/dashboard`, `/tasks`, `/notes`, `/profile`. Shared UI kit: `Button`, `Card`, `Spinner`, `ErrorMessage` — консистентность. Loading / error / empty на каждой data-fetching странице — не «потом». Mobile-first layout для dashboard.

`services/api.ts` — typed fetch wrapper; не fetch в каждом компоненте. Tasks: CRUD, фильтр status/priority. Notes: markdown textarea + preview, теги. Dashboard: виджеты статистики, placeholder GitHub repos. TypeScript strict, без `any` в api layer. Auth подключишь на день 151.

**Читать:**

- [React Dashboard (нед. 14)](../../docs/projects.md#неделя-14--react-dashboard-frontend-milestone)
- [Portfolio SPA (нед. 13)](../../docs/projects.md#неделя-13--portfolio-spa)
- [Vite Env](https://vitejs.dev/guide/env-and-mode.html)

**Ключевая мысль:** один `api.ts`, три UI-состояния, shared components — фронтенд capstone в миниатюре.

### Практика
1. `npm create vite@latest frontend -- --template react-ts`
2. React Router: Layout + routes `/dashboard`, `/tasks`, `/notes`, `/profile`
3. `services/api.ts` — typed fetch wrapper (пока без auth token)
4. **Dashboard:** статистика задач (виджеты), placeholder для GitHub repos или погоды
5. **Tasks:** список, create/edit form, фильтр по status/priority
6. **Notes:** список с preview, markdown editor (textarea + preview), теги
7. **Profile:** форма bio, avatar URL (пока mock)
8. Shared UI: `Button`, `Card`, `Spinner`, `ErrorMessage`

**Критерии:**
- [ ] 4+ маршрута с общим Layout
- [ ] Tasks и Notes CRUD через API (без auth пока)
- [ ] TypeScript strict, нет `any` в api layer
- [ ] Loading и error states на всех data-fetching страницах

### Git
- Закоммить изменения дня: `git add week-22-capstone/frontend/` → `git commit -m "week 22 day 150: DevHub React TS pages and API client"`

### Ловушки
- Fetch в каждом компоненте — один `api.ts`
- Забытый `VITE_API_URL` — API calls на undefined

---

## День 151 (Чт): Auth — JWT end-to-end

### Теория

Auth end-to-end — обязательный MVP пункт. Переиспользуй Secure Notes (нед. 20): bcrypt/passlib, JWT, middleware на protected routes. Backend: `POST /auth/register`, `POST /auth/login`; все `/api/v1/*` требуют `Authorization: Bearer`. `user_id` из JWT payload — не из request body (IDOR уязвимость).

Frontend: `AuthProvider`, `useAuth()`, `/login`, `/register`, protected routes с redirect. `api.ts` — auto Bearer header, logout on 401. Rate limit на login, CORS whitelist, helmet — из недели 20. Начни `SECURITY.md` с OWASP checklist.

E2E manual test: register → login → create task → logout → login → task visible. User A не видит данные User B → 403. JWT secret в git — rotate немедленно. Задокументируй выбор localStorage vs httpOnly cookie.

**Читать:**

- [Secure Notes (нед. 20)](../../docs/projects.md#неделя-20--secure-notes)
- [JWT Introduction](https://jwt.io/introduction)
- [Auth в MVP](../../docs/projects.md#функции-mvp-минимум)

**Ключевая мысль:** auth — сквозной слой; user_id только из verified JWT.

### Практика
1. Backend auth: register, login, JWT middleware на все protected routes
2. Привяжи tasks и notes к `user_id` из token — миграция если нужно
3. React: `/login`, `/register` pages; `AuthProvider` + `useAuth()`
4. Protected routes — redirect на `/login` без token
5. `api.ts` — автоматический `Authorization: Bearer`, logout on 401
6. Rate limit на `/auth/login`, helmet/CORS настроены
7. Начни `SECURITY.md` — OWASP checklist (из нед. 20)
8. E2E manual: register → login → create task → logout → login → task visible

**Критерии:**
- [ ] Auth end-to-end работает (см. [критерии сдачи](../../docs/projects.md#критерии-сдачи-capstone))
- [ ] User A не видит данные User B
- [ ] 401 без token, 403 на чужие ресурсы
- [ ] `SECURITY.md` начат

### Git
- Закоммить изменения дня: `git add week-22-capstone/` → `git commit -m "week 22 day 151: DevHub JWT auth frontend backend"`

### Ловушки
- user_id из body вместо JWT — IDOR уязвимость
- JWT secret в git — rotate немедленно

---

## День 152 (Пт): Docker — локальный full-stack

### Теория

Docker Compose — критерий сдачи capstone: `docker compose up` поднимает всё локально. Переиспользуй Task Manager Docker (нед. 21): services `db`, `backend`, `frontend`; healthchecks; named volumes; entrypoint wait-for-db → migrate → seed → start.

Multi-stage frontend Dockerfile (nginx + dist). Backend Dockerfile slim. `VITE_API_URL` как build arg — в docker network указывает на backend service, не localhost. `.dockerignore` в обоих папках. `ARCHITECTURE.md` с Mermaid: client → API → DB → volumes.

README «запуск за 5 команд»: clone → copy `.env` → `docker compose up --build` → open browser. Backend стартует до PG — healthcheck + retry в entrypoint. Полный smoke: auth + CRUD через dockerized frontend.

**Читать:**

- [Task Manager Docker (нед. 21)](../../docs/projects.md#неделя-21--task-manager-docker)
- [Docker Compose](https://docs.docker.com/compose/)
- [Infra в стеке](../../docs/projects.md#обязательный-стек)

**Ключевая мысль:** docker compose — часть MVP; `VITE_API_URL` для docker network, не localhost.

### Практика
1. `docker-compose.yml`: postgres + backend + frontend (nginx)
2. Backend Dockerfile, Frontend multi-stage Dockerfile
3. Healthcheck на db (`pg_isready`) и backend (`/api/health`)
4. Entrypoint: wait-for-db → migrate → seed → start
5. `.dockerignore` в frontend и backend
6. `docker compose up --build` — полный smoke test
7. `ARCHITECTURE.md` — Mermaid diagram (client → API → DB → volumes)
8. Обнови README: «запуск за 5 команд» (клон → env → compose up → open browser)

**Критерии:**
- [ ] `docker compose up` поднимает всё локально ([критерии сдачи](../../docs/projects.md#критерии-сдачи-capstone))
- [ ] Auth + CRUD работают через dockerized frontend
- [ ] `ARCHITECTURE.md` с диаграммой
- [ ] README local setup ≤ 5 команд

### Git
- Закоммить изменения дня: `git add week-22-capstone/` → `git commit -m "week 22 day 152: DevHub docker-compose and ARCHITECTURE.md"`

### Ловушки
- Backend стартует до PG — добавь healthcheck и retry
- `VITE_API_URL` указывает на localhost внутри docker network

---

## День 153 (Сб): Тесты и CI

### Теория

Quality gate capstone: pytest ≥ 15, Vitest ≥ 12, ESLint без ошибок, CI green on push. Тесты из MVP: auth flow, CRUD tasks, 401 без token, 403 cross-user. GitHub Actions: job `backend` (postgres service + pytest) + job `frontend` (vitest + lint). Badge CI в README.

Test DB isolation — postgres service в CI или SQLite in-memory; не production. Flaky tests из shared state — изолируй fixtures с rollback. `npm audit` / `pip audit` — зафиксируй в `SECURITY.md`. Auth flow должен быть покрыт тестами, не только manual E2E.

Локально все тесты зелёные перед push. CI без postgres service — тесты падают на GitHub. Это последний рубеж перед deploy: если CI красный, deploy откладывается.

**Читать:**

- [Quality в стеке](../../docs/projects.md#обязательный-стек)
- [GitHub Actions](https://docs.github.com/en/actions)
- [pytest](https://docs.pytest.org/) · [Vitest](https://vitest.dev/)

**Ключевая мысль:** CI green — критерий сдачи; тесты на auth и isolation обязательны.

### Практика
1. Backend pytest: auth (register, login, 401), tasks CRUD, notes CRUD, 403 cross-user — ≥ 15 тестов
2. Frontend Vitest: Login form, ProtectedRoute, TaskList, NoteEditor — ≥ 12 тестов
3. ESLint + `npm run lint` в frontend; ruff или flake8 в backend (опционально)
4. `.github/workflows/ci.yml`: job `backend` (postgres service, pytest) + job `frontend` (vitest, lint)
5. Badge CI в README
6. `npm audit` / `pip audit` — зафиксируй в `SECURITY.md`
7. Все тесты зелёные локально перед push

**Критерии:**
- [ ] pytest ≥ 15, Vitest ≥ 12 — все проходят
- [ ] CI green on push
- [ ] ESLint без ошибок (или задокументированные исключения)
- [ ] Auth flow покрыт тестами

### Git
- Закоммить изменения дня: `git add week-22-capstone/` → `git commit -m "week 22 day 153: DevHub tests and GitHub Actions CI"`

### Ловушки
- CI без postgres service — тесты падают на GitHub
- Flaky tests из-за shared state — изолируй fixtures

---

## День 154 (Вс): Deploy, портфолио и финальное ревью

### Теория

Финальный день — deploy, портфолио и рефлексия. Frontend → Vercel/Netlify (root `frontend/`, `VITE_API_URL` = production API). Backend + managed PostgreSQL → Render/Railway/Neon. После deploy: обнови CORS для Vercel domain, rotate `JWT_SECRET` если был в git, env vars в cloud dashboard.

Live HTTPS demo — критерий сдачи: register → login → CRUD в браузере. `FINAL_REVIEW.md`: что узнал за 22 недели, что бы сделал иначе. GitHub Profile README — таблица всех 22 проектов со ссылками. README DevHub: badges, demo URL, screenshots, docker setup, architecture.

Free tier cold start 30–60 сек — документируй. Забытый CORS update — API works in curl, fails в browser на Vercel. 2-минутный pitch DevHub — устная репетиция архитектуры. Тег `week-22-done` — финиш роадмапа. Поздравляем: ты junior full-stack ready.

**Читать:**

- [Критерии сдачи capstone](../../docs/projects.md#критерии-сдачи-capstone)
- [Vercel Docs](https://vercel.com/docs)
- [Render Docs](https://render.com/docs)
- [Портфолио после 22 недель](../../docs/projects.md#портфолио-после-22-недель)

**Ключевая мысль:** deploy + FINAL_REVIEW + profile README — три грани финиша capstone.

### Практика
1. **Deploy backend:** Render/Railway — connect repo, `DATABASE_URL` + `JWT_SECRET`
2. **Deploy DB:** managed PostgreSQL, run migrations + seed
3. **Deploy frontend:** Vercel — root `frontend/`, `VITE_API_URL` = production API URL
4. Update CORS — добавь Vercel domain
5. Проверь live demo: HTTPS, register → login → CRUD
6. README: badges, live demo URLs, screenshots/GIF, tech stack
7. `FINAL_REVIEW.md`: что узнал, что бы сделал иначе
8. GitHub Profile README: таблица 22 проектов (как в [projects.md](../../docs/projects.md#портфолио-после-22-недель))
9. Резюме PDF с live links; 2-мин pitch DevHub
10. Пройди [ревью-чеклист](#ревью-чеклист) — ≥ 80% уверенных ответов

**Критерии:**
- [ ] Live HTTPS demo (frontend + API)
- [ ] `FINAL_REVIEW.md` заполнен
- [ ] GitHub profile README обновлён со ссылками на все 22 проекта
- [ ] README DevHub — demo link, docker setup, architecture, tests

### Git
- Закоммить изменения дня: `git add week-22-capstone/` → `git commit -m "week 22 day 154: DevHub deploy portfolio FINAL_REVIEW"`
- Поставь тег: `git tag week-22-done`
- Push tags: `git push origin main --tags`

### Ловушки
- Забытый CORS update — API works in curl, fails in browser on Vercel
- Free tier cold start 30–60 сек — документируй в README

---

## Проект недели

# DevHub Capstone — финальный проект роадмапа

Полная спецификация: **[docs/projects.md — Неделя 22, DevHub Capstone](../../docs/projects.md#неделя-22--devhub-capstone-финальный)**

### Концепция

Персональная **платформа разработчика**: дашборд + заметки + задачи + интеграция с GitHub API (или виджет погоды) — production full-stack app.

### Обязательный стек

| Слой | Технологии |
|------|------------|
| Frontend | React 18+, TypeScript, React Router, Context/Zustand |
| Backend | FastAPI **или** Express (один основной) |
| БД | PostgreSQL, миграции, seed |
| Auth | JWT (register/login), protected routes |
| Infra | Docker Compose локально, CI (GitHub Actions) |
| Deploy | Frontend → Vercel/Netlify, Backend + DB → Render/Railway/Neon |
| Quality | pytest ≥ 15, Vitest ≥ 12, ESLint, README, `.env.example` |

### Функции MVP

См. [projects.md](../../docs/projects.md#функции-mvp-минимум): Auth, Tasks, Notes, Dashboard, Profile, API, Security, Tests, Docs.

### Структура репозитория

```
week-22-capstone/
├── frontend/
├── backend/
├── docker-compose.yml
├── .github/workflows/ci.yml
├── SECURITY.md
├── ARCHITECTURE.md
├── FINAL_REVIEW.md
└── README.md
```

### Критерии сдачи

- [ ] Live HTTPS demo (frontend + API)
- [ ] `docker compose up` поднимает всё локально
- [ ] Auth end-to-end работает
- [ ] ≥ 5 сущностей в БД со связями
- [ ] CI green on push
- [ ] `FINAL_REVIEW.md` заполнен
- [ ] GitHub profile README — ссылки на все 22 проекта
- [ ] Тег `week-22-done`

### Связь с проектами 13–21

| Неделя | Переиспользуешь |
|--------|-----------------|
| [14 — Dashboard](../../docs/projects.md#неделя-14--react-dashboard-frontend-milestone) | UI виджеты, fetch |
| [18/19 — API](../../docs/projects.md#неделя-18--library-rest-api) | CRUD, Swagger |
| [20 — Secure Notes](../../docs/projects.md#неделя-20--secure-notes) | JWT, тесты |
| [21 — Docker](../../docs/projects.md#неделя-21--task-manager-docker) | compose, monorepo |

Nice-to-have: [projects.md](../../docs/projects.md#nice-to-have-после-mvp).

---

## Ревью-чеклист

- HTML/CSS: block vs inline, Flexbox vs Grid?
- JS: замыкание, Event Loop, var/let/const?
- React: key, useState vs useEffect?
- Python: Big O, магические методы, venv?
- SQL: JOIN, индексы, injection?
- Node: middleware, connection pool?
- Full-Stack: REST, CORS, JWT, Docker?
- DevHub: архитектура за 2 минуты?

**80%+ уверенных ответов — ты готов к junior full-stack. Поздравляем с завершением 22-недельного роадмапа!**
