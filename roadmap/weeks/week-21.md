# Неделя 21: Full-Stack интеграция и Docker

> **Цель недели:** связать React-фронтенд с бэкендом и упаковать всё в Docker Compose.
> **Литература:** [Docker Docs](https://docs.docker.com/get-started/), [docker-compose](https://docs.docker.com/compose/), [Vite Env](https://vitejs.dev/guide/env-and-mode.html)
> **Проект недели:** [Task Manager Docker](../../docs/projects.md#неделя-21--task-manager-docker) — React + API + PostgreSQL в `docker-compose`, healthchecks, seed.
> **Git:** папка `learning-log/week-21/`, monorepo или два репо в одной папке; тег `week-21-done`.

## День 141 (Пн): Связка Frontend + Backend

### Теория

Full-stack начинается там, где фронтенд и бэкенд встречаются в браузере. Same-origin policy: `localhost:5173` (Vite) и `localhost:3000` (API) — разные origins. Браузер блокирует cross-origin fetch без заголовков CORS от сервера. Preflight OPTIONS запрос отправляется для «непростых» запросов.

`cors` middleware в Express или `CORSMiddleware` в FastAPI с whitelist `http://localhost:5173`. `VITE_API_URL` — build-time переменная для фронтенда; `DATABASE_URL` — runtime для бэкенда. Vite proxy в dev обходит CORS, направляя `/api` на backend — same-origin для браузера.

Замени localStorage tasks/notes на API CRUD — это суть недели. Проверь Network tab: нет CORS errors. `.env.example` для обоих проектов. Hardcoded localhost в production build — сломает deploy.

**Читать:**

- [CORS (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [cors (Express)](https://expressjs.com/en/resources/middleware/cors.html)
- [Vite proxy](https://vitejs.dev/config/server-options.html#server-proxy)

**Ключевая мысль:** CORS — согласие сервера; `VITE_` prefix обязателен для клиентских env.

### Практика
1. React Dashboard (нед.14) или Secure Notes (нед.20) → fetch к Express/FastAPI API
2. `.env`: `VITE_API_URL=http://localhost:3000` (или 8000 для FastAPI)
3. CORS: allow `http://localhost:5173` в dev, credentials если нужны cookies
4. Замени localStorage tasks/notes на API CRUD
5. Проверь Network tab — нет CORS errors
6. `.env.example` для обоих проектов

**Критерии:**
- [ ] CRUD через API, не localStorage
- [ ] CORS настроен — нет ошибки в browser console
- [ ] `.env.example` для обоих проектов

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 141: frontend backend CORS integration"`

### Ловушки
- `VITE_` prefix обязателен — иначе переменная не попадёт в bundle
- Hardcoded localhost в production build

---

## День 142 (Вт): Единый API-контракт и обработка ошибок

### Теория

API contract — общий язык фронтенда и бэкенда. OpenAPI/Swagger — source of truth: типы, статусы, примеры. Единый формат ошибок `{ error: { code, message, details? } }` упрощает парсинг на клиенте. 4xx — «ты сделал что-то не так», 5xx — «попробуй позже».

Три UI-состояния на каждой data-fetching странице: loading (spinner), error (message + retry), empty (подсказка действия). `services/api.ts` — единый fetch wrapper с auth header и error parsing; не дублируй fetch в 10 компонентах. TypeScript types `Task`, `ApiError` в `types/api.ts`.

Проверяй `res.ok` перед `json()` — иначе парсишь HTML error page как JSON. React Query/SWR — опционально для кеша и retry. Сверь frontend types с OpenAPI вручную или через openapi-typescript.

**Читать:**

- [OpenAPI](https://swagger.io/specification/)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [TanStack Query](https://tanstack.com/query/latest)

**Ключевая мысль:** один api module; loading/error/empty — не опциональный UX.

### Практика
1. `services/api.ts` — единый fetch wrapper с error parsing и auth header
2. Все страницы: loading spinner, error message + retry button, empty state
3. Toast при успешном create/update/delete (или inline feedback)
4. Типы `Task`, `Note`, `ApiError` в `types/api.ts`
5. 4xx показывает user-friendly message; 5xx — «Попробуйте позже»
6. Сверь frontend types с OpenAPI schema (ручно или openapi-typescript)

**Критерии:**
- [ ] Один api module, не fetch в каждом компоненте
- [ ] Network error показывает понятное сообщение
- [ ] 4xx/5xx обрабатываются по-разному

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 142: API client loading error states"`

### Ловушки
- Дублирование fetch логики в 10 компонентах
- Игнорирование `res.ok` — парсинг error HTML как JSON

---

## День 143 (Ср): Docker — основы

### Теория

Docker упаковывает приложение с зависимостями в воспроизводимый образ. Image — неизменяемый шаблон (слои); container — запущенный экземпляр. Dockerfile: `FROM node:20-alpine`, `WORKDIR`, `COPY package*.json`, `RUN npm ci`, `COPY .`, `EXPOSE`, `CMD`. Layer caching: сначала зависимости, потом код — быстрее rebuild.

`.dockerignore` исключает `node_modules`, `.git`, `.env` из build context. `docker build -t task-api .` и `docker run -p 3000:3000 --env-file .env task-api`. Multi-stage builds (обзор): build stage + slim runtime. `curl localhost:3000/api/health` с хоста проверяет container.

Не копируй весь проект до `npm ci` — инвалидируешь cache. Root user в container — для prod consider non-root (обзор). Документируй docker commands в README.

**Читать:**

- [Docker Overview](https://docs.docker.com/get-started/overview/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore](https://docs.docker.com/build/building/context/#dockerignore-files)

**Ключевая мысль:** image = шаблон, container = процесс; слои Dockerfile — про скорость сборки.

### Практика
1. Dockerfile для backend: `node:20-alpine` или `python:3.12-slim`
2. COPY package files → install deps → COPY source → EXPOSE port → CMD
3. `docker build -t task-api .` и `docker run -p 3000:3000 --env-file .env task-api`
4. Проверь `/health` с хоста: `curl localhost:3000/api/health`
5. `.dockerignore`: node_modules, .git, .env, __pycache__
6. Задокументируй команды в README

**Критерии:**
- [ ] Image собирается без ошибок
- [ ] .dockerignore исключает node_modules
- [ ] Container стартует и отвечает на /health

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 143: backend Dockerfile"`

### Ловушки
- COPY всего проекта до npm ci — layer cache invalidation
- root user в container — для prod consider non-root (обзор)

---

## День 144 (Чт): Docker для frontend и PostgreSQL

### Теория

Production frontend в Docker — multi-stage: stage 1 `npm run build` (Node), stage 2 `nginx:alpine` копирует `dist/`. nginx отдаёт static assets с gzip; `try_files $uri /index.html` — SPA fallback для client-side routes. `VITE_API_URL` — build-time: пересобирай image при смене API URL.

Official `postgres:16` image: env `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`. Named volume `pgdata:/var/lib/postgresql/data` — данные переживают `docker rm`. `localhost` внутри container — сам container, не host machine; в compose network используй имя service `db`.

Подними три container вручную перед compose: frontend :80, API :3000, PG :5432. Backend подключается к postgres по hostname `db` в docker network. Проверь полный flow до `docker compose`.

**Читать:**

- [nginx docker](https://hub.docker.com/_/nginx)
- [postgres docker](https://hub.docker.com/_/postgres)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

**Ключевая мысль:** в docker network хост БД — имя service, не localhost.

### Практика
1. Frontend Dockerfile: stage 1 `npm run build`, stage 2 `nginx:alpine` + COPY dist
2. `docker run -d --name pg -e POSTGRES_PASSWORD=pass -v pgdata:/var/lib/postgresql/data postgres:16`
3. Backend container подключается к postgres по hostname (вручную: `--link` или host.docker.internal)
4. nginx.conf: `try_files $uri /index.html` для SPA routing
5. Проверь полный flow: 3 containers вручную
6. Frontend на port 80, API на 3000, PG на 5432

**Критерии:**
- [ ] Frontend dist отдаётся nginx на port 80
- [ ] Postgres data сохраняется после restart container
- [ ] Backend видит DB по hostname `db` (в compose network)

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 144: frontend nginx and postgres containers"`

### Ловушки
- `localhost` внутри container — это сам container, не host
- VITE_API_URL при build time — пересобирай image при смене URL

---

## День 145 (Пт): docker-compose — multi-service

### Теория

docker-compose оркестрирует multi-service приложение одним файлом. Services: `db`, `backend`, `frontend`; networks связывают их; volumes persist data. `depends_on` задаёт порядок старта, но не готовность БД — добавь healthcheck `pg_isready` и `condition: service_healthy`.

`DATABASE_URL=postgresql://user:pass@db:5432/tasks` — hostname `db` из имени service. `docker compose up --build` — одна команда для всего стека. `docker compose down -v` удаляет volumes — осторожно, потеряешь данные. Seed в entrypoint или init service.

Smoke test: open frontend → login → create task → refresh → persists. Healthchecks на db и `/api/health` на backend — обязательны для надёжного старта. Эта структура monorepo — прямой задел для DevHub capstone.

**Читать:**

- [Compose file reference](https://docs.docker.com/compose/compose-file/)
- [depends_on with healthcheck](https://docs.docker.com/compose/how-tos/startup-order/)
- [docker compose CLI](https://docs.docker.com/compose/reference/)

**Ключевая мысль:** compose + healthcheck + volumes = воспроизводимый full-stack локально.

### Практика
1. `docker-compose.yml`:
   - `db` (postgres:16 + volume `pgdata` + healthcheck)
   - `backend` (build ./backend, ports 3000, depends_on db healthy)
   - `frontend` (build ./frontend, ports 8080:80)
2. `DATABASE_URL=postgresql://user:pass@db:5432/tasks` в backend env
3. `docker compose up --build` — всё стартует одной командой
4. Seed script в backend entrypoint или отдельный `init` service
5. Проверь smoke: open frontend → login → create task

**Критерии:**
- [ ] Одна команда поднимает 3 сервиса
- [ ] Данные PG в named volume `pgdata`
- [ ] depends_on + healthcheck db

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 145: docker-compose three services"`

### Ловушки
- Backend стартует до готовности PG — connection refused (healthcheck/retry)
- `docker compose down -v` — удаляет данные (осторожно)

---

## День 146 (Сб): Dev vs Prod конфигурация

### Теория

12 Factor App: config в environment, dev/prod parity, disposability (containers стартуют быстро). `docker-compose.override.yml` автоматически мержится в dev; `docker-compose.prod.yml` — explicit `-f` для production-like local. Dev: volume mount source + nodemon/uvicorn --reload; prod: optimized image без mounts.

Логи: `docker compose logs -f backend`. Secrets в prod — Docker secrets или cloud env, не plain text в compose file. Entrypoint script: wait-for-db → migrate → seed → start server — решает race condition при старте.

Документируй порты и команды: dev `docker compose up` vs prod `docker compose -f docker-compose.prod.yml up`. Dev volume mount может перезаписать `node_modules` в container — используй named volume для node_modules (обзор). Default passwords только для local.

**Читать:**

- [12 Factor App](https://12factor.net/)
- [Compose override](https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/)
- [Docker secrets](https://docs.docker.com/engine/swarm/secrets/)

**Ключевая мысль:** dev/prod compose — разные файлы, одна документация в README.

### Практика
1. `docker-compose.dev.yml` — mount source, hot reload, exposed debug ports
2. `docker-compose.prod.yml` — optimized builds, no volume mounts
3. README: `docker compose up` (dev) vs `docker compose -f docker-compose.prod.yml up`
4. Entrypoint script: wait-for-db → migrate → seed → start server
5. `.env.example` со всеми переменными для compose
6. Документируй порты: frontend 8080, api 3000, db 5432

**Критерии:**
- [ ] Dev и prod compose файлы документированы
- [ ] Seed data появляется после первого `up`
- [ ] Логи доступны через compose logs

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 146: dev prod compose configs"`

### Ловушки
- Dev volume mount перезаписывает node_modules в container
- Production compose с default passwords — только для local

---

## День 147 (Вс): E2E smoke test и ревью архитектуры

### Теория

Smoke test — минимальный путь пользователя, не полный E2E suite. `SMOKE_TEST.md`: compose up → open app → login → CRUD task → refresh → data persists. Health endpoints нужны orchestration (Kubernetes, Render, compose healthcheck). Architecture diagram (Mermaid): client → API → DB → volumes.

Замерь cold start `docker compose up --build` — free tier deploy может иметь 30–60 сек warm-up; документируй в README. Сравни week-21 с требованиями DevHub capstone — список gaps в `notes/capstone-prep.md`. Все env vars в `.env.example`.

Неделя 21 — мост к финалу: та же структура `frontend/` + `backend/` + `docker-compose.yml`. Тег `week-21-done`. Если smoke test проходит — ты готов к DevHub.

**Читать:**

- [DevHub Capstone spec](../../docs/projects.md#неделя-22--devhub-capstone-финальный)
- [Mermaid](https://mermaid.js.org/)
- [Health check pattern](https://docs.docker.com/compose/how-tos/startup-order/)

**Ключевая мысль:** smoke test + architecture diagram — входной билет в capstone неделю.

### Практика
1. Smoke checklist в `SMOKE_TEST.md`: compose up → open app → login → CRUD task → refresh → persists
2. Mermaid diagram в README: frontend, backend, db, volumes
3. Замер cold start `docker compose up --build` — запиши время
4. Проверь все env vars в `.env.example`
5. Сравни week-21 с требованиями [DevHub Capstone](../../docs/projects.md#неделя-22--devhub-capstone-финальный) — что уже готово
6. Список gaps для capstone в `notes/capstone-prep.md`

**Критерии:**
- [ ] Smoke test checklist пройден
- [ ] Mermaid diagram в README
- [ ] Все env vars в `.env.example`

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 147: smoke test and architecture diagram"`
- Поставь тег: `git tag week-21-done`

---

## Проект недели

**Full-Stack Task Manager в Docker**. Спецификация: [docs/projects.md — неделя 21](../../docs/projects.md#неделя-21--task-manager-docker).

### Структура monorepo

```
week-21/
├── frontend/           # Vite React TS
├── backend/            # Express or FastAPI
├── docker-compose.yml
├── docker-compose.dev.yml
├── .env.example
├── SMOKE_TEST.md
└── README.md
```

### Функции

1. React frontend + Express/FastAPI backend + PostgreSQL
2. Auth (JWT из нед. 20), tasks CRUD через API
3. `docker-compose.yml` — db, backend, frontend
4. Volumes, healthchecks, seed data, wait-for-db
5. Dev и prod инструкции, architecture diagram

### Критерии проекта

- [ ] `docker compose up --build` — working app на localhost
- [ ] Данные переживают restart (named volume)
- [ ] CORS и `VITE_API_URL` корректны для docker network
- [ ] Healthcheck на db и `/api/health` на backend
- [ ] SMOKE_TEST.md пройден без ошибок
- [ ] README: architecture, env, dev vs prod commands
- [ ] Тег `week-21-done`

Этот проект — **прямой задел** для [DevHub Capstone](../../docs/projects.md#неделя-22--devhub-capstone-финальный): та же структура `frontend/` + `backend/` + `docker-compose.yml`.

## Ревью-чеклист
- Зачем Docker если можно `npm start` локально?
- Чем image отличается от container?
- Почему `localhost` внутри container не работает для host DB?
- Что такое CORS и когда браузер блокирует запрос?
- docker-compose vs kubernetes — когда что (обзор)?
