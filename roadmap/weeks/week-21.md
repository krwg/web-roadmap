# Неделя 21: Full-Stack интеграция и Docker

> **Цель недели:** связать React-фронтенд с бэкендом и упаковать всё в Docker Compose.
> **Литература:** [Docker Docs](https://docs.docker.com/get-started/), [docker-compose](https://docs.docker.com/compose/), [Vite Env](https://vitejs.dev/guide/env-and-mode.html)
> **Проект недели:** [Task Manager Docker](../../docs/projects.md#неделя-21--task-manager-docker) — React + API + PostgreSQL в `docker-compose`, healthchecks, seed.
> **Git:** папка `learning-log/week-21/`, monorepo или два репо в одной папке; тег `week-21-done`.

## День 141 (Пн): Связка Frontend + Backend
<a id="week-21-day-141"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Task Manager Docker**

### Теория

Full-stack начинается там, где фронтенд и бэкенд встречаются в браузере. Same-origin policy: `localhost:5173` (Vite) и `localhost:3000` (API) — разные origins. Браузер блокирует cross-origin fetch без заголовков CORS от сервера. Preflight OPTIONS запрос отправляется для «непростых» запросов.

`cors` middleware в Express или `CORSMiddleware` в FastAPI с whitelist `http://localhost:5173`. `VITE_API_URL` — build-time переменная для фронтенда; `DATABASE_URL` — runtime для бэкенда. Vite proxy в dev обходит CORS, направляя `/api` на backend — same-origin для браузера.

Замени localStorage tasks/notes на API CRUD — это суть недели. Проверь Network tab: нет CORS errors. `.env.example` для обоих проектов. Hardcoded localhost в production build — сломает deploy.

Ментальная модель: origin — это тройка (протокол, домен, порт), и браузер по умолчанию блокирует любой fetch между разными origin, если сервер явно не разрешил это через CORS-заголовки. Это защита пользователя, а не бага фреймворка — без same-origin policy любой сайт мог бы читать твою банковскую сессию через скрытый fetch. Для junior full-stack разработчика непонимание CORS — источник часа-двух бесполезной отладки почти в каждом первом проекте; умение быстро прочитать ошибку CORS в консоли и понять, на чьей она стороне (сервер не разрешил origin) — практический навык уровня middle.

Конкретный пример: если `VITE_API_URL` не имеет префикса `VITE_`, Vite просто не включит переменную в bundle — переменная будет `undefined` в runtime, и ошибка проявится не как CORS, а как fetch на `undefined/api/tasks`, что сбивает с толку новичков. Частое заблуждение — «CORS настраивается на клиенте» — на самом деле разрешение полностью на стороне сервера (заголовки `Access-Control-Allow-Origin`), клиент только соблюдает то, что разрешил браузер. Именно этот CORS-контракт между React-клиентом и API — фундамент для docker-compose сети в этой же неделе (день 145), где origin меняются на container hostnames, и для production deploy в DevHub capstone, где появится третий origin — Vercel domain.

Для продакшена preflight OPTIONS-запрос — источник ещё одной частой путаницы: браузер отправляет его автоматически перед «непростыми» запросами (с кастомными заголовками вроде `Authorization` или методом `PUT`/`DELETE`), и сервер должен явно ответить на OPTIONS без падения — иначе основной запрос до сервера вообще не дойдёт, а в Network tab будет видна только неудачная preflight-строка, что сбивает с толку при первой отладке.

**Читать:**

- [CORS (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [cors (Express)](https://expressjs.com/en/resources/middleware/cors.html)
- [Vite proxy](https://vitejs.dev/config/server-options.html#server-proxy)

**Ключевая мысль:** CORS — согласие сервера; `VITE_` prefix обязателен для клиентских env.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. React Dashboard (нед.14) или Secure Notes (нед.20) → fetch к Express/FastAPI API
2. `.env`: `VITE_API_URL=http://localhost:3000` (или 8000 для FastAPI)
3. CORS: allow `http://localhost:5173` в dev, credentials если нужны cookies

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Не понимаешь ошибку — прочитай её с конца: файл, строка, тип. Открой DevTools / терминал и воспроизведи на 5 строках кода.

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 141: frontend backend CORS integration"`

### Ловушки
- `VITE_` prefix обязателен — иначе переменная не попадёт в bundle
- Hardcoded localhost в production build

---

## День 142 (Вт): Единый API-контракт и обработка ошибок
<a id="week-21-day-142"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Task Manager Docker**

### Теория

API contract — общий язык фронтенда и бэкенда. OpenAPI/Swagger — source of truth: типы, статусы, примеры. Единый формат ошибок `{ error: { code, message, details? } }` упрощает парсинг на клиенте. 4xx — «ты сделал что-то не так», 5xx — «попробуй позже».

Три UI-состояния на каждой data-fetching странице: loading (spinner), error (message + retry), empty (подсказка действия). `services/api.ts` — единый fetch wrapper с auth header и error parsing; не дублируй fetch в 10 компонентах. TypeScript types `Task`, `ApiError` в `types/api.ts`.

Проверяй `res.ok` перед `json()` — иначе парсишь HTML error page как JSON. React Query/SWR — опционально для кеша и retry. Сверь frontend types с OpenAPI вручную или через openapi-typescript.

Ментальная модель: API contract — это письменный договор между командами (или между тобой сегодняшним и тобой через месяц), а не подразумеваемое соглашение в голове. Если backend меняет форму ошибки без предупреждения, frontend ломается тихо — вот почему OpenAPI-схема и типизированные ошибки экономят часы интеграционной отладки. В реальных компаниях frontend и backend часто пишут разные люди или разные команды, и контракт — единственное, что синхронизирует их работу без созвонов на каждый чих.

Конкретный пример: если API возвращает `{ error: "Not found" }` в одном endpoint и `{ message: "Not found", code: 404 }` в другом, frontend не может написать один универсальный error handler — придётся городить if-ветки под каждый случай, что быстро превращается в технический долг. Частое заблуждение junior-разработчиков — «раз fetch не выбросил exception, значит всё ок» — но fetch не бросает ошибку на HTTP 404/500, только на сетевой сбой, поэтому проверка `res.ok` обязательна перед `res.json()`, иначе распарсишь HTML-страницу ошибки как JSON и получишь непонятный краш. Три состояния — loading/error/empty, которые ты добавляешь сегодня на каждую страницу, станут обязательным критерием приёмки для Dashboard и Tasks в DevHub capstone (неделя 22, день 150) — привычка, заложенная сейчас, там уже не потребует отдельного обдумывания.

Для продакшена единый `services/api.ts` даёт ещё один практический бонус — единую точку для будущих улучшений вроде retry с exponential backoff или отмены запроса при размонтировании компонента (AbortController). Если fetch-логика раскидана по компонентам, добавление такой функциональности требует правки в десятке мест и почти гарантированно приводит к рассинхронизации поведения между страницами.

**Читать:**

- [OpenAPI](https://swagger.io/specification/)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [TanStack Query](https://tanstack.com/query/latest)

**Ключевая мысль:** один api module; loading/error/empty — не опциональный UX.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. `services/api.ts` — единый fetch wrapper с error parsing и auth header
2. Все страницы: loading spinner, error message + retry button, empty state
3. Toast при успешном create/update/delete (или inline feedback)

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Тесты/валидация красные — сначала один failing case, почини его, только потом следующий.

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 142: API client loading error states"`

### Ловушки
- Дублирование fetch логики в 10 компонентах
- Игнорирование `res.ok` — парсинг error HTML как JSON

---

## День 143 (Ср): Docker — основы
<a id="week-21-day-143"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Task Manager Docker**

### Теория

Docker упаковывает приложение с зависимостями в воспроизводимый образ. Image — неизменяемый шаблон (слои); container — запущенный экземпляр. Dockerfile: `FROM node:20-alpine`, `WORKDIR`, `COPY package*.json`, `RUN npm ci`, `COPY .`, `EXPOSE`, `CMD`. Layer caching: сначала зависимости, потом код — быстрее rebuild.

`.dockerignore` исключает `node_modules`, `.git`, `.env` из build context. `docker build -t task-api .` и `docker run -p 3000:3000 --env-file .env task-api`. Multi-stage builds (обзор): build stage + slim runtime. `curl localhost:3000/api/health` с хоста проверяет container.

Не копируй весь проект до `npm ci` — инвалидируешь cache. Root user в container — для prod consider non-root (обзор). Документируй docker commands в README.

Ментальная модель: Dockerfile — рецепт, image — испечённый и замороженный пирог по рецепту, container — кусок этого пирога у тебя на тарелке прямо сейчас, который можно есть (запускать), выбросить и отрезать заново. Слои Dockerfile кешируются построчно сверху вниз, поэтому порядок инструкций — это оптимизация скорости сборки, а не просто стиль. Для junior-разработчика Docker — это уже не «плюс», а базовое требование в большинстве вакансий 2026 года: почти любая современная инфраструктура (Kubernetes, ECS, Render, Railway) ожидает готовый Docker image.

Конкретный пример цены ошибки: если скопировать весь проект (`COPY . .`) до `npm ci`, то любое изменение в исходном коде инвалидирует кеш зависимостей — пересборка занимает минуты вместо секунд при каждом маленьком изменении кода. Частое заблуждение новичков — «Docker — это как виртуальная машина» — на деле контейнеры используют namespaces и cgroups ядра хоста, а не эмулируют железо, поэтому стартуют за миллисекунды, а не минуты, и делят ядро ОС с хостом. Dockerfile для backend, который ты пишешь сегодня, станет первым сервисом в `docker-compose.yml` (день 145), а затем — основой Docker-инфраструктуры DevHub capstone (неделя 22, день 152), где та же логика слоёв применится уже к production-сборке.

Для продакшена размер образа тоже имеет значение: `node:20-alpine` весит десятки мегабайт против сотен у полного `node:20`, а меньший образ быстрее скачивается при деплое и содержит меньше поверхности для атак (меньше системных пакетов — меньше потенциальных CVE). Привычка сразу выбирать slim/alpine базовые образы, а не «full», экономит время и деньги на облачном биллинге по трафику и storage в масштабе реальной инфраструктуры.

**Читать:**

- [Docker Overview](https://docs.docker.com/get-started/overview/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore](https://docs.docker.com/build/building/context/#dockerignore-files)

**Ключевая мысль:** image = шаблон, container = процесс; слои Dockerfile — про скорость сборки.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. Dockerfile для backend: `node:20-alpine` или `python:3.12-slim`
2. COPY package files → install deps → COPY source → EXPOSE port → CMD
3. `docker build -t task-api .` и `docker run -p 3000:3000 --env-file .env task-api`

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Устал — сделай коммит текущего прогресса с честным сообщением `wip:` и паузу 10 минут. Не геройствуй.

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 143: backend Dockerfile"`

### Ловушки
- COPY всего проекта до npm ci — layer cache invalidation
- root user в container — для prod consider non-root (обзор)

---

## День 144 (Чт): Docker для frontend и PostgreSQL
<a id="week-21-day-144"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Task Manager Docker**

### Теория

Production frontend в Docker — multi-stage: stage 1 `npm run build` (Node), stage 2 `nginx:alpine` копирует `dist/`. nginx отдаёт static assets с gzip; `try_files $uri /index.html` — SPA fallback для client-side routes. `VITE_API_URL` — build-time: пересобирай image при смене API URL.

Official `postgres:16` image: env `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`. Named volume `pgdata:/var/lib/postgresql/data` — данные переживают `docker rm`. `localhost` внутри container — сам container, не host machine; в compose network используй имя service `db`.

Подними три container вручную перед compose: frontend :80, API :3000, PG :5432. Backend подключается к postgres по hostname `db` в docker network. Проверь полный flow до `docker compose`.

Ментальная модель: named volume — это внешний жёсткий диск, который ты подключаешь к контейнеру; сам контейнер — расходный, а volume переживает `docker rm` и пересоздание контейнера. Путаница «localhost внутри контейнера = localhost на хосте» — одна из самых частых ошибок новичков в Docker: у каждого контейнера своя сетевая изоляция, и «localhost» там означает сам контейнер, а не машину разработчика. В production-командах эта путаница стоит часов отладки connection refused, поэтому понимание docker network — маркер зрелости junior DevOps-навыков.

Конкретный пример: если backend в контейнере пытается подключиться к Postgres по `localhost:5432`, он получит connection refused, даже если Postgres реально запущен и слушает порт — потому что это два разных сетевых namespace; правильный hostname — имя service (`db`) в общей docker-сети. Частое заблуждение — «раз я указал `-p 5432:5432`, значит порт открыт для всех контейнеров» — port mapping открывает порт наружу на хост-машину, а между контейнерами используется внутренняя docker network с DNS по именам сервисов. Multi-stage сборка frontend (build + nginx), которую ты делаешь сегодня, и правильное именование сервисов — прямая подготовка к `docker-compose.yml` завтрашнего дня и к продовому образу DevHub capstone.

Для продакшена nginx как раздатчик статики — не случайный выбор: он эффективнее Node.js-сервера для отдачи файлов благодаря event-driven архитектуре, умеет gzip/brotli-сжатие «из коробки» и не тратит ресурсы на интерпретацию JavaScript ради банальной раздачи HTML/CSS/JS. `try_files $uri /index.html` решает специфичную для SPA проблему: без этой директивы прямой заход на `/tasks` (не через клик в приложении) вернёт 404, потому что физического файла `/tasks` на диске не существует — весь роутинг живёт в JS-бандле.

**Читать:**

- [nginx docker](https://hub.docker.com/_/nginx)
- [postgres docker](https://hub.docker.com/_/postgres)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

**Ключевая мысль:** в docker network хост БД — имя service, не localhost.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. Frontend Dockerfile: stage 1 `npm run build`, stage 2 `nginx:alpine` + COPY dist
2. `docker run -d --name pg -e POSTGRES_PASSWORD=pass -v pgdata:/var/lib/postgresql/data postgres:16`
3. Backend container подключается к postgres по hostname (вручную: `--link` или host.docker.internal)

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Документация не клеится — найди один официальный пример (MDN / docs) и сопоставь 1:1 со своим кодом.

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 144: frontend nginx and postgres containers"`

### Ловушки
- `localhost` внутри container — это сам container, не host
- VITE_API_URL при build time — пересобирай image при смене URL

---

## День 145 (Пт): docker-compose — multi-service
<a id="week-21-day-145"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Task Manager Docker**

### Теория

docker-compose оркестрирует multi-service приложение одним файлом. Services: `db`, `backend`, `frontend`; networks связывают их; volumes persist data. `depends_on` задаёт порядок старта, но не готовность БД — добавь healthcheck `pg_isready` и `condition: service_healthy`.

`DATABASE_URL=postgresql://user:pass@db:5432/tasks` — hostname `db` из имени service. `docker compose up --build` — одна команда для всего стека. `docker compose down -v` удаляет volumes — осторожно, потеряешь данные. Seed в entrypoint или init service.

Smoke test: open frontend → login → create task → refresh → persists. Healthchecks на db и `/api/health` на backend — обязательны для надёжного старта. Эта структура monorepo — прямой задел для DevHub capstone.

Ментальная модель: docker-compose.yml — это партитура для оркестра из нескольких контейнеров, где каждый service — отдельный музыкант, а networks и volumes — то, что позволяет им играть вместе и не терять данные между выступлениями. `depends_on` говорит Docker только порядок запуска процессов, а не готовность приложения внутри — Postgres-контейнер стартует за миллисекунды, но самому PostgreSQL нужны секунды на инициализацию, поэтому без healthcheck backend может упасть с connection refused при первом старте.

Конкретный пример: `condition: service_healthy` вместе с `pg_isready` в healthcheck заставляет Docker дождаться реальной готовности БД принимать соединения, а не просто факта, что контейнер запущен — это разница между «процесс существует» и «процесс готов работать», критичная для надёжного `docker compose up` без ручных перезапусков. Частое заблуждение — «`docker compose down` безопасен всегда» — но флаг `-v` удаляет volumes вместе с данными, и разработчики теряли демо-данные перед показом проекта именно так. Инфраструктура из трёх сервисов с healthcheck, которую ты собираешь сегодня, — это практически готовый `docker-compose.yml` для DevHub capstone (неделя 22, день 152), где добавится только auth layer и production-нюансы.

Для продакшена важно понимать разницу между healthcheck и readiness: даже здоровый (`healthy`) контейнер может быть временно не готов принимать нагрузку (например, прогревает кеш) — в managed-оркестраторах вроде Kubernetes это два разных сигнала (liveness/readiness probes), но идея та же самая, что и в compose healthcheck: не отправляй трафик туда, где сервис формально жив, но фактически ещё не готов отвечать корректно. Эта идея пригодится и за пределами Docker — в любой системе с несколькими зависимыми сервисами.

**Читать:**

- [Compose file reference](https://docs.docker.com/compose/compose-file/)
- [depends_on with healthcheck](https://docs.docker.com/compose/how-tos/startup-order/)
- [docker compose CLI](https://docs.docker.com/compose/reference/)

**Ключевая мысль:** compose + healthcheck + volumes = воспроизводимый full-stack локально.

### Практика (полный трек)
1. `docker-compose.yml`:
2. `DATABASE_URL=postgresql://user:pass@db:5432/tasks` в backend env
3. `docker compose up --build` — всё стартует одной командой
4. Seed script в backend entrypoint или отдельный `init` service
5. Проверь smoke: open frontend → login → create task
   - `db` (postgres:16 + volume `pgdata` + healthcheck)
   - `backend` (build ./backend, ports 3000, depends_on db healthy)
   - `frontend` (build ./frontend, ports 8080:80)

**Критерии:**
- [ ] Одна команда поднимает 3 сервиса
- [ ] Данные PG в named volume `pgdata`
- [ ] depends_on + healthcheck db

### Практика (лайт / MVP)
1. `docker-compose.yml`:
2. `DATABASE_URL=postgresql://user:pass@db:5432/tasks` в backend env
3. `docker compose up --build` — всё стартует одной командой

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Запутался в структуре файлов — нарисуй дерево папок на бумаге, потом создай пустые файлы и заполни по одному.

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 145: docker-compose three services"`

### Ловушки
- Backend стартует до готовности PG — connection refused (healthcheck/retry)
- `docker compose down -v` — удаляет данные (осторожно)

---

## День 146 (Сб): Dev vs Prod конфигурация
<a id="week-21-day-146"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Task Manager Docker**

### Теория

12 Factor App: config в environment, dev/prod parity, disposability (containers стартуют быстро). `docker-compose.override.yml` автоматически мержится в dev; `docker-compose.prod.yml` — explicit `-f` для production-like local. Dev: volume mount source + nodemon/uvicorn --reload; prod: optimized image без mounts.

Логи: `docker compose logs -f backend`. Secrets в prod — Docker secrets или cloud env, не plain text в compose file. Entrypoint script: wait-for-db → migrate → seed → start server — решает race condition при старте.

Документируй порты и команды: dev `docker compose up` vs prod `docker compose -f docker-compose.prod.yml up`. Dev volume mount может перезаписать `node_modules` в container — используй named volume для node_modules (обзор). Default passwords только для local.

Ментальная модель 12 Factor App: конфигурация должна жить в environment variables, а не в коде — тот же image должен уметь запускаться и в dev, и в staging, и в проде, отличаясь только переменными окружения снаружи. Dev/prod parity — принцип, по которому окружения должны быть максимально похожи, чтобы баг «работает у меня, не работает в проде» случался как можно реже. Для junior-разработчика эта дисциплина — то, что отличает pet-проект от продакшен-готового кода: собеседующие часто спрашивают именно про разделение dev/prod конфигурации.

Конкретный пример проблемы: volume mount исходников в dev-режиме (`-v ./backend:/app`) может незаметно перезаписать `node_modules` внутри контейнера локальной версией с хоста, если не выделить отдельный named volume под `node_modules` — итог: контейнер падает с «module not found», хотя на хосте всё установлено. Частое заблуждение — «дефолтные пароли postgres в compose-файле не проблема, это же локально» — но такие compose-файлы часто копируют в staging без изменений, и default password утекает в реальную инфраструктуру. Entrypoint-скрипт wait-for-db → migrate → seed, который ты пишешь сегодня, решает ту же race condition, что встретится в проде DevHub capstone при первом деплое (неделя 22, день 154) — паттерн одинаков в любом окружении.

Для продакшена явное разделение dev/prod compose файлов вместо одного «универсального» с кучей `if`-подобных условий — это разница между конфигурацией, которую можно быстро прочитать и понять, и конфигурацией, требующей мысленно эмулировать все возможные комбинации флагов. Команды, где такое разделение принято с самого начала, тратят заметно меньше времени на «почему в проде включился dev-режим» — классический класс инцидентов из-за спутанной конфигурации.

**Читать:**

- [12 Factor App](https://12factor.net/)
- [Compose override](https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/)
- [Docker secrets](https://docs.docker.com/engine/swarm/secrets/)

**Ключевая мысль:** dev/prod compose — разные файлы, одна документация в README.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. `docker-compose.dev.yml` — mount source, hot reload, exposed debug ports
2. `docker-compose.prod.yml` — optimized builds, no volume mounts
3. README: `docker compose up` (dev) vs `docker compose -f docker-compose.prod.yml up`

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Тесты/валидация красные — сначала один failing case, почини его, только потом следующий.

### Git
- Закоммить изменения дня: `git add week-21/` → `git commit -m "week 21 day 146: dev prod compose configs"`

### Ловушки
- Dev volume mount перезаписывает node_modules в container
- Production compose с default passwords — только для local

---

## День 147 (Вс): E2E smoke test и ревью архитектуры
<a id="week-21-day-147"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Task Manager Docker**

### Теория

Smoke test — минимальный путь пользователя, не полный E2E suite. `SMOKE_TEST.md`: compose up → open app → login → CRUD task → refresh → data persists. Health endpoints нужны orchestration (Kubernetes, Render, compose healthcheck). Architecture diagram (Mermaid): client → API → DB → volumes.

Замерь cold start `docker compose up --build` — free tier deploy может иметь 30–60 сек warm-up; документируй в README. Сравни week-21 с требованиями DevHub capstone — список gaps в `notes/capstone-prep.md`. Все env vars в `.env.example`.

Неделя 21 — мост к финалу: та же структура `frontend/` + `backend/` + `docker-compose.yml`. Тег `week-21-done`. Если smoke test проходит — ты готов к DevHub.

Ментальная модель: smoke test — это не полный regression suite, а быстрая проверка «дым идёт, значит мотор хотя бы завёлся» — минимальный путь, который ловит catastrophic failures за минуту вместо часа полного прогона тестов. Architecture diagram решает другую задачу — она переводит код в общий язык для ревьюера, коллеги или будущего тебя, который забыл детали через полгода. Для junior-разработчика умение за 2 минуты нарисовать архитектуру своего проекта на созвоне — практический навык, который прямо оценивают на техническом интервью.

Конкретный пример: если `docker compose up --build` первый раз занимает 45 секунд из-за скачивания base images и сборки, а команда об этом не знает, они решат, что деплой завис, и начнут паниковать — задокументированный cold start снимает эту неопределённость. Частое заблуждение — «раз у меня всё работает локально, значит и в capstone заработает» — но сравнение чек-листа week-21 с требованиями DevHub (список gaps в `notes/capstone-prep.md`) именно для того и нужно, чтобы найти пробелы заранее, а не в последний день недели 22, когда времени на исправление уже не будет. Mermaid-диаграмма и smoke-checklist, которые ты создаёшь сегодня, станут прямыми шаблонами для `ARCHITECTURE.md` и `SMOKE_TEST.md` капстоуна.

Для продакшена регулярный smoke test — это то, что команды запускают сразу после каждого деплоя, ещё до того как объявить релиз завершённым: если базовый путь пользователя (login → основное действие → выход) не работает, откатывать деплой нужно немедленно, не дожидаясь жалоб реальных пользователей. Привычка писать такой чек-лист за 10 минут до того, как считать задачу «готовой», экономит часы разбора инцидентов в проде.

**Читать:**

- [DevHub Capstone spec](../../docs/projects.md#неделя-22--devhub-capstone-финальный)
- [Mermaid](https://mermaid.js.org/)
- [Health check pattern](https://docs.docker.com/compose/how-tos/startup-order/)

**Ключевая мысль:** smoke test + architecture diagram — входной билет в capstone неделю.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. Smoke checklist в `SMOKE_TEST.md`: compose up → open app → login → CRUD task → refresh → persists
2. Mermaid diagram в README: frontend, backend, db, volumes
3. Замер cold start `docker compose up --build` — запиши время

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Устал — сделай коммит текущего прогресса с честным сообщением `wip:` и паузу 10 минут. Не геройствуй.

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


## Проверь себя

<details>
<summary>Что должно получиться к концу недели?</summary>

Работающий проект **Task Manager Docker** в `learning-log/week-21/`, осмысленная Git-история, тег `week-21-done`.

</details>

<details>
<summary>Главный навык недели одной фразой?</summary>

Full-stack в Docker Compose

</details>

<details>
<summary>Можно ли пропустить день?</summary>

Нет — дни связаны. В **лайт-режиме** сократи практику до MVP, но теорию и Git-коммит не пропускай.

</details>
