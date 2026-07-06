# Неделя 21: Full-Stack интеграция и Docker

> **Цель недели:** связать React-фронтенд с бэкендом и упаковать всё в Docker Compose.
> **Литература:** [Docker Docs](https://docs.docker.com/get-started/), [docker-compose](https://docs.docker.com/compose/), [Vite Env](https://vitejs.dev/guide/env-and-mode.html)
> **Проект недели:** [Task Manager Docker](../../docs/projects.md#неделя-21--task-manager-docker) — React + API + PostgreSQL в `docker-compose`, healthchecks, seed.
> **Git:** папка `learning-log/week-21/`, monorepo или два репо в одной папке; тег `week-21-done`.

## День 141 (Пн): Связка Frontend + Backend

### Теория
- [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS): браузер блокирует cross-origin без заголовков сервера
- [cors package](https://expressjs.com/en/resources/middleware/cors.html) в Express; FastAPI `CORSMiddleware`
- Env vars: `VITE_API_URL` (frontend, build-time), `DATABASE_URL` (backend, runtime)
- [Vite proxy](https://vitejs.dev/config/server-options.html#server-proxy) — обход CORS в dev через same-origin
- Same-origin policy — почему `localhost:5173` ≠ `localhost:3000`
- Preflight OPTIONS request — когда браузер спрашивает разрешение

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
- API contract: OpenAPI/Swagger — source of truth для frontend и backend
- Consistent error format: `{ error: { code, message, details? } }`
- Loading states, error states, empty states — три обязательных UI-состояния
- Optimistic updates (обзор) — UI обновляется до ответа сервера
- [React Query](https://tanstack.com/query/latest) / SWR — кеширование и retry (опционально)
- TypeScript types для API responses — меньше runtime-сюрпризов

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
- [Docker Overview](https://docs.docker.com/get-started/overview/): image (шаблон) vs container (экземпляр)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/): FROM, WORKDIR, COPY, RUN, CMD, EXPOSE
- [.dockerignore](https://docs.docker.com/build/building/context/#dockerignore-files) — не копируй node_modules в context
- Layer caching: COPY package*.json → npm ci → COPY . — быстрее rebuild
- Multi-stage builds — build stage + slim runtime (обзор)
- `docker build -t name .` и `docker run -p host:container`

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
- Multi-stage frontend: Node build → nginx serve `dist/` — production pattern
- `vite build` создаёт static assets; nginx отдаёт с gzip
- [Official postgres image](https://hub.docker.com/_/postgres): env `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- Named volumes — данные PG переживают `docker rm container`
- `localhost` внутри container ≠ host machine — используй service names в compose network
- `VITE_API_URL` — build-time arg, пересобирай image при смене API URL

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
- [Compose file reference](https://docs.docker.com/compose/compose-file/): services, networks, volumes
- `depends_on` — порядок старта (не гарантирует готовность БД!)
- Healthchecks: `healthcheck: test: ["CMD-SHELL", "pg_isready ..."]`
- `docker compose up --build`, `docker compose down`, `docker compose down -v` (удаляет volumes!)
- Environment через `env_file:` или `environment:` в compose
- Default network — все services видят друг друга по имени service

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
- [12 Factor App](https://12factor.net/): config, logs, disposability, dev/prod parity
- `docker-compose.override.yml` — автоматически мержится в dev
- `docker-compose.prod.yml` — explicit `-f` для production-like local
- Логирование: `docker compose logs -f backend`
- Secrets в prod: Docker secrets, cloud provider env (не в compose file plain text)
- Hot reload в dev: volume mount source + nodemon/uvicorn --reload

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
- Smoke test — минимальный путь пользователя, не полный E2E suite
- Health endpoints для orchestration (Kubernetes, Render, compose)
- Architecture diagram — слои: client → API → DB
- Cold start time — документируй для free tier deploy
- Подготовка к неделе 22: DevHub Capstone объединит всё + deploy

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
