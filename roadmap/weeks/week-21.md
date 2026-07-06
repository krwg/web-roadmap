# Неделя 21: Full-Stack интеграция и Docker

> **Цель недели:** связать React-фронтенд с бэкендом и упаковать всё в Docker Compose.
> **Литература:** [Docker Docs](https://docs.docker.com/get-started/), [docker-compose](https://docs.docker.com/compose/), [Vite Env](https://vitejs.dev/guide/env-and-mode.html)

## День 141 (Пн): Связка Frontend + Backend

### Теория
- [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS): `Access-Control-Allow-Origin`
- [cors package](https://expressjs.com/en/resources/middleware/cors.html) в Express
- FastAPI: `CORSMiddleware`
- Env vars: `VITE_API_URL` (frontend), `DATABASE_URL` (backend)
- [Vite proxy](https://vitejs.dev/config/server-options.html#server-proxy) для dev

### Практика
1. React Dashboard (нед.14) → fetch к Express/FastAPI API
2. `.env`: `VITE_API_URL=http://localhost:3000`
3. CORS: allow `http://localhost:5173` в dev
4. Замени localStorage tasks на API CRUD

**Критерии:**
- [ ] CRUD tasks через API, не localStorage
- [ ] CORS настроен — нет ошибки в browser console
- [ ] `.env.example` для обоих проектов

### Ловушки
- `VITE_` prefix обязателен — иначе переменная не попадёт в bundle
- Hardcoded localhost в production build

---

## День 142 (Вт): Единый API-контракт и обработка ошибок

### Теория
- API contract: OpenAPI/Swagger как source of truth
- Consistent error format: `{ error: { code, message } }`
- Loading states, optimistic updates (обзор)
- [React Query](https://tanstack.com/query/latest) / SWR — обзор (опционально)

### Практика
1. `services/api.js` — единый fetch wrapper с error parsing
2. Все страницы Dashboard: loading, error, retry UI
3. Toast при успешном create/update/delete
4. TypeScript types из OpenAPI (bonus) или ручные JSDoc types

**Критерии:**
- [ ] Один api module, не fetch в каждом компоненте
- [ ] Network error показывает понятное сообщение
- [ ] 4xx/5xx обрабатываются по-разному

### Ловушки
- Дублирование fetch логики в 10 компонентах
- Игнорирование `res.ok` — парсинг error HTML как JSON

---

## День 143 (Ср): Docker — основы

### Теория
- [Docker Overview](https://docs.docker.com/get-started/overview/): image, container, registry
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/): FROM, WORKDIR, COPY, RUN, CMD, EXPOSE
- [.dockerignore](https://docs.docker.com/build/building/context/#dockerignore-files)
- Multi-stage builds для Node (обзор)

### Практика
1. Dockerfile для backend: `node:20-alpine`, COPY package*.json → npm ci → COPY . → EXPOSE 3000
2. `docker build -t notes-api .` и `docker run -p 3000:3000 --env-file .env notes-api`
3. Проверь API с хоста

**Критерии:**
- [ ] Image собирается без ошибок
- [ ] .dockerignore исключает node_modules
- [ ] Container стартует и отвечает на /health

### Ловушки
- COPY всего проекта до npm ci — layer cache invalidation
- root user в container — для prod consider non-root (обзор)

---

## День 144 (Чт): Docker для frontend и PostgreSQL

### Теория
- Nginx для static React build или `vite preview`
- Multi-stage: build stage (node) → nginx stage
- [Official postgres image](https://hub.docker.com/_/postgres)
- Volumes для persistence данных БД

### Практика
1. Frontend Dockerfile: build → nginx serve `dist/`
2. `docker run postgres:16` с volume `pgdata`
3. Backend container подключается к postgres по service name (подготовка к compose)
4. Проверь полный flow вручную (3 containers)

**Критерии:**
- [ ] Frontend dist отдаётся nginx на port 80
- [ ] Postgres data сохраняется после restart container
- [ ] Backend видит DB по hostname `db` (в compose network)

### Ловушки
- `localhost` внутри container — это сам container, не host
- VITE_API_URL при build time — пересобирай image при смене URL

---

## День 145 (Пт): docker-compose — multi-service

### Теория
- [Compose file reference](https://docs.docker.com/compose/compose-file/)
- services, networks, volumes, depends_on
- `docker compose up --build`, `docker compose down -v`
- Healthchecks в compose

### Практика
1. `docker-compose.yml`:
   - `db` (postgres:16 + volume)
   - `backend` (build ./backend, ports 3000, depends_on db)
   - `frontend` (build ./frontend, ports 5173:80)
2. Environment через compose `environment:` или env_file
3. `docker compose up --build` — всё стартует одной командой

**Критерии:**
- [ ] Одна команда поднимает 3 сервиса
- [ ] Данные PG в named volume `pgdata`
- [ ] depends_on + healthcheck db (или wait script)

### Ловушки
- Backend стартует до готовности PG — connection refused (healthcheck/retry)
- `docker compose down -v` — удаляет данные (осторожно)

---

## День 146 (Сб): Dev vs Prod конфигурация

### Теория
- [12 Factor App](https://12factor.net/): config, logs, disposability
- compose override: `docker-compose.override.yml` для dev
- Логирование: `docker compose logs -f backend`
- Secrets в prod: не в compose file (обзор Docker secrets / cloud)

### Практика
1. `docker-compose.dev.yml` — mount source code, hot reload
2. `docker-compose.prod.yml` — optimized builds
3. README: `docker compose -f docker-compose.yml up`
4. Seed script при первом старте (entrypoint)

**Критерии:**
- [ ] Dev и prod compose файлы документированы
- [ ] Seed data появляется после первого `up`
- [ ] Логи доступны через compose logs

### Ловушки
- Dev volume mount перезаписывает node_modules в container
- Production compose с default passwords — только для local

---

## День 147 (Вс): E2E smoke test и ревью архитектуры

### Теория
- Monitoring: health endpoints

### Практика
1. Smoke checklist: open app → login → create task → refresh → task persists
2. Нарисуй architecture diagram (Mermaid в README)
3. Замер cold start `docker compose up`

**Критерии:**
- [ ] Smoke test checklist пройден
- [ ] Mermaid diagram в README
- [ ] Все env vars в `.env.example`

---

## Проект недели

**Full-Stack Task Manager в Docker**:

1. React frontend + Express/FastAPI backend + PostgreSQL
2. Auth (JWT), tasks CRUD через API
3. `docker-compose.yml` — db, backend, frontend
4. Volumes, healthchecks, seed data
5. README: architecture, `docker compose up`, smoke test

**Критерии:**
- [ ] `docker compose up --build` — working app на localhost
- [ ] Данные переживают restart (volume)
- [ ] CORS и VITE_API_URL корректны
- [ ] Dev и prod инструкции в README

## Ревью-чеклист
- Зачем Docker если можно `npm start` локально?
- Чем image отличается от container?
- Почему `localhost` внутри container не работает для host DB?
- Что такое CORS и когда браузер блокирует запрос?
- docker-compose vs kubernetes — когда что (обзор)?
