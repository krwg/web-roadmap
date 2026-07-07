# Неделя 19: Node.js + Express REST API

> **Цель недели:** построить REST API на JavaScript в среде Node.js с Express и PostgreSQL.
> **Литература:** [Node.js Docs](https://nodejs.org/en/docs), [Express Guide](https://expressjs.com/en/guide/routing.html), [node-postgres](https://node-postgres.com/)
> **Проект недели:** [Express Notes API](../../docs/projects.md#неделя-19--express-notes-api) — layered Express API, Zod, PostgreSQL, Postman collection.
> **Git:** папка `learning-log/week-19/`, ветки `feature/routes`, `feature/pg`; тег `week-19-done`.

## День 127 (Пн): Node.js — среда и модули
<a id="week-19-day-127"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Express Notes API**

### Теория

Node.js — среда выполнения JavaScript вне браузера. Нет DOM и `window`, зато есть `process`, встроенные модули и npm-экосистема. Backend на Node разделяет язык с фронтендом — один TypeScript/JavaScript на обе стороны, но runtime другой: event loop libuv, не браузерный.

CommonJS (`require`) vs ES Modules (`import`) — выбери `"type": "module"` в `package.json` для современного стиля. `import.meta.url` + `fileURLToPath` заменяют `__dirname` в ESM. Встроенные модули: `fs`, `path`, `http`. `process.argv` — аргументы CLI, `process.env` — переменные окружения.

npm управляет зависимостями: `package.json`, semver, `node_modules`. npm scripts (`"greet": "node scripts/greet.js"`) — стандартный способ запуска задач. `.gitignore`: `node_modules`, `.env`. `fs.promises` вместо callback — async/await без callback hell.

**Читать:**

- [Node.js Introduction](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs)
- [ES Modules](https://nodejs.org/api/esm.html)
- [fs.promises](https://nodejs.org/api/fs.html#promises-api)

**Ключевая мысль:** Node — JS без браузера; ESM + fs.promises — современный baseline.

### Практика
1. `mkdir notes-api && npm init -y`, добавь `"type": "module"`
2. CLI: `node scripts/greet.js --name=Alex` (parse `process.argv`)
3. Чтение/запись `notes.json` через `fs.promises`
4. `path.join`, `import.meta.url` для путей к файлам данных
5. npm script `"greet": "node scripts/greet.js"`
6. `.gitignore`: `node_modules`, `.env`, `dist`

**Критерии:**
- [ ] ES modules (import/export)
- [ ] fs.promises, не callback fs.readFile
- [ ] npm script `"greet"` работает

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 127: Node ESM setup and file CLI"`

### Ловушки
- require() в ESM project — SyntaxError
- Относительные пути без path.join — ломается на Windows

---

## День 128 (Вт): Асинхронность в Node
<a id="week-19-day-128"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Express Notes API**

### Теория

Асинхронность — сердце Node. Эволюция: callback → Promise → async/await. Event loop libuv обрабатывает I/O неблокирующе, но синхронный `fs.readFileSync` в сервере заморозит все запросы — используй async API. `await` без `try/catch` — необработанный rejection.

EventEmitter (`on`, `emit`, `once`) — основа многих Node API и паттерн pub/sub. `process.on('unhandledRejection')` ловит забытые rejections — настрой в entry point. `util.promisify` оборачивает legacy callback API в Promise — для понимания, не для нового кода.

File watcher на `notes.json` учит реагировать на изменения; SIGINT корректно останавливает watcher. `Promise.all` читает три файла параллельно. Замер sync vs async на 10 файлах — наглядная демонстрация блокировки main thread.

**Читать:**

- [Event Loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick)
- [EventEmitter](https://nodejs.org/api/events.html)
- [async/await (MDN)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)

**Ключевая мысль:** не блокируй event loop; await + try/catch на каждом I/O.

### Практика
1. Перепиши file I/O на async/await с try/catch
2. File watcher: логирует изменения `notes.json`, останавливается на SIGINT
3. Промисификация: `const readFile = promisify(fs.readFile)` — для понимания legacy
4. Обработка `unhandledRejection` и `uncaughtException` в entry point
5. Параллельное чтение 3 файлов через `Promise.all`
6. Замер: sync `readFileSync` vs async на 10 файлах — почувствуй блокировку

**Критерии:**
- [ ] Нет callback hell — только async/await
- [ ] Watcher корректно останавливается (SIGINT)
- [ ] try/catch вокруг await

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 128: async file watcher and error handling"`

### Ловушки
- Забытый await — Promise вместо данных
- Синхронный `fs.readFileSync` в сервере — блокирует event loop

---

## День 129 (Ср): Express — REST API основы
<a id="week-19-day-129"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Express Notes API**

### Теория

Express — минималистичный HTTP-фреймворк поверх Node `http`. `app.get/post/put/delete` маппят метод + путь на handler. `req.params` — path params, `req.query` — query string, `req.body` — JSON после `express.json()` middleware. Без body parser `req.body` будет `undefined` — классическая ловушка.

HTTP semantics: 200 OK, 201 Created, 204 No Content (DELETE без body), 400 Bad Request, 404 Not Found. Раздели `app.js` (конфигурация, middleware, routes) и `server.js` (`listen`) — app экспортируется для тестов. `nodemon` автоперезапускает в dev.

CRUD `/api/notes` с хранением в JSON-файле — мост к PostgreSQL завтра. Единый формат ответа `{ data }` или `{ error: { message } }` упрощает фронтенд. RESTful URLs: существительные, не глаголы.

**Читать:**

- [Express Hello World](https://expressjs.com/en/starter/hello-world.html)
- [express.json()](https://expressjs.com/en/api.html#express.json)
- [Express Routing](https://expressjs.com/en/guide/routing.html)

**Ключевая мысль:** express.json() обязателен; app отдельно от server — тестируемость.

### Практика
1. `npm install express`, `src/app.js`, `src/server.js`
2. CRUD `/api/notes` — хранение в JSON-файле через fs
3. `GET /api/notes/:id` — 404 если нет (`res.status(404).json(...)`)
4. `npm install -D nodemon`, script `"dev": "nodemon src/server.js"`
5. Проверь все методы через curl или Thunder Client
6. Единый формат ответа: `{ data }` или `{ error: { message } }`

**Критерии:**
- [ ] express.json() подключён
- [ ] RESTful URLs и методы
- [ ] 201 на POST, 204 на DELETE

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 129: Express CRUD notes in-memory JSON"`

### Ловушки
- POST без body parser — req.body undefined
- Один огромный app.js — разбей на routes

---

## День 130 (Чт): Middleware, валидация, ошибки
<a id="week-19-day-130"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Express Notes API**

### Теория

Middleware в Express — функции `(req, res, next)` в цепочке. Порядок критичен: logger → `express.json()` → routes → 404 handler → error middleware (4 аргумента: `err, req, res, next`). `next()` передаёт управление дальше; `next(err)` — в error handler.

Zod валидирует body с TypeScript inference: `title` min 1 символ, `body` optional. При ошибке — 400 с `zodError.flatten()`. Centralized error handler возвращает JSON `{ error: { code, message } }` — единый контракт для клиента. morgan логирует HTTP-запросы в dev.

404 handler для неизвестных routes — последний middleware перед error handler. Custom logger с duration (Date.now до/после) дополняет morgan. Error middleware без 4 параметров Express не распознает — не вызовется.

**Читать:**

- [Writing middleware](https://expressjs.com/en/guide/using-middleware.html)
- [Zod](https://zod.dev/)
- [morgan](https://github.com/expressjs/morgan)

**Ключевая мысль:** порядок middleware; Zod на входе, error handler на выходе цепочки.

### Практика
1. Logger middleware: method, url, duration (Date.now до/после)
2. Zod schema для Note: `title` min 1, `body` optional string
3. Centralized error handler — JSON `{ error: { code, message } }`
4. 400 при validation error с деталями Zod (`zodError.flatten()`)
5. 404 handler для неизвестных routes (`app.use((req,res) => ...)`)
6. morgan `'dev'` format в development

**Критерии:**
- [ ] Все ошибки проходят через error middleware
- [ ] Zod на POST и PUT
- [ ] morgan или custom logger

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 130: Zod validation and error middleware"`

### Ловушки
- Забытый `next(err)` — зависший request
- Error middleware без 4 параметров — не вызывается

---

## День 131 (Пт): Express + PostgreSQL
<a id="week-19-day-131"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Express Notes API**

### Теория

`node-postgres` (`pg`) — драйвер PostgreSQL для Node. `Pool` переиспользует соединения под нагрузкой; `new Client()` на каждый запрос — антипаттерн. `pool.query('SELECT * FROM notes WHERE id = $1', [id])` — placeholders `$1, $2` защищают от SQL injection.

`DATABASE_URL=postgresql://user:pass@host:5432/db` из `.env` через dotenv. Prisma — ORM-альтернатива (обзор); на этой неделе raw `pg` учит SQL и placeholders. Graceful shutdown: `pool.end()` на SIGTERM.

Перепиши notes API с JSON-файла на таблицу `notes(id, title, body, created_at)`. `schema.sql` + migrate script. Все запросы только через `pool.query` с массивом параметров — template strings в SQL запрещены.

**Читать:**

- [node-postgres](https://node-postgres.com/)
- [Connection Pooling](https://node-postgres.com/features/pooling)
- [dotenv](https://github.com/motdotla/dotenv)

**Ключевая мысль:** Pool, не Client; `$1` placeholders — единственный безопасный способ.

### Практика
1. `npm install pg dotenv`
2. `src/db/pool.js` — Pool из `DATABASE_URL`, тест `SELECT NOW()`
3. Перепиши notes API на таблицу `notes(id, title, body, created_at)`
4. `schema.sql` + `scripts/migrate.js` или `npm run db:migrate`
5. `seed.sql` с 5 тестовыми заметками
6. Все запросы через `pool.query('... WHERE id = $1', [id])`

**Критерии:**
- [ ] Pool, не Client на каждый запрос
- [ ] Параметризованные запросы ($1, $2)
- [ ] dotenv, `.env.example`

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 131: Express notes with PostgreSQL pool"`

### Ловушки
- SQL injection через template strings — только placeholders
- Pool не закрывается при shutdown — graceful exit

---

## День 132 (Сб): Структура проекта и роутеры
<a id="week-19-day-132"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Express Notes API**

### Теория

Express Router модульно группирует маршруты: `notes.routes.js` монтируется с prefix `/api/notes`. Layered architecture: routes (тонкие) → controllers (HTTP) → services (бизнес-логика) → db (SQL). Бизнес-логика в route handler не тестируется — вынеси в service.

`dotenv` загружает secrets из `.env`; `NODE_ENV=development|production` меняет поведение (morgan 'dev' vs 'combined'). Health check `GET /api/health` возвращает `{ status, db: 'ok'|'down', uptime }` — нужен для Docker и мониторинга. 503 если БД недоступна.

Graceful shutdown: SIGTERM → `server.close()` → `pool.end()`. `package-lock.json` в git — воспроизводимые сборки. README описывает слои папок — onboarding нового разработчика.

**Читать:**

- [Express Router](https://expressjs.com/en/guide/routing.html#express-router)
- [dotenv](https://github.com/motdotla/dotenv)
- [Graceful Shutdown](https://expressjs.com/en/advanced/healthcheck-graceful-shutdown.html)

**Ключевая мысль:** routes тонкие, logic в services; health check — контракт с инфраструктурой.

### Практика
1. Структура: `src/routes/`, `controllers/`, `services/`, `db/pool.js`
2. Вынеси логику из routes в controller/service
3. `GET /api/health` — `{ status, db: 'ok'|'down', uptime }`
4. Router `notes.routes.js` → controller `notes.controller.js` → service `notes.service.js`
5. Graceful shutdown: SIGTERM → close server → pool.end()
6. README: структура папок с описанием слоёв

**Критерии:**
- [ ] Routes тонкие — только маршрутизация
- [ ] Service переиспользуется из controller
- [ ] health check возвращает 503 если DB down

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 132: layered architecture and health check"`

### Ловушки
- Бизнес-логика в route handler — не тестируется
- Циклические импорты между modules

---

## День 133 (Вс): Ревью Node.js и сравнение с FastAPI
<a id="week-19-day-133"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Express Notes API**

### Теория

Ревью недели — сравнение двух backend-стеков, которые ты теперь знаешь. FastAPI: автодоки, Pydantic, async, Python ecosystem. Express: минимализм, npm, один язык с React. Для I/O-bound оба отличны; CPU-bound тяжёлая работа чаще уходит в Python или отдельный worker.

npm scripts best practices: `start` (production), `dev` (nodemon), `test`, `db:migrate`. Postman collection — демо и ручное QA. Skeleton `auth.routes.js` — мост к неделе 20. `npm audit` показывает уязвимости в зависимостях.

Сравнительная таблица FastAPI vs Express по 10 критериям учит аргументировать выбор стека. Express Notes API — parity с Library REST API недели 18: те же статусы, формат ошибок, layered structure. Тег `week-19-done`.

**Читать:**

- [npm scripts](https://docs.npmjs.com/cli/v10/using-npm/scripts)
- [Express vs Fastify (обзор)](https://expressjs.com/)
- [npm audit](https://docs.npmjs.com/cli/v10/commands/npm-audit)

**Ключевая мысль:** Express и FastAPI решают одну задачу разными инструментами — выбор по команде и экосистеме.

### Практика
1. Сравнительная таблица: FastAPI (нед.18) vs Express — 10 критериев в `docs/compare.md`
2. Postman collection для Express API — export JSON
3. README с curl примерами для всех endpoints
4. Skeleton: `src/routes/auth.routes.js` с заглушками register/login
5. `npm audit` — отчёт об уязвимостях
6. Финальный smoke test: CRUD notes через API

**Критерии:**
- [ ] README полный (install, env, run, test)
- [ ] Сравнительная таблица в docs
- [ ] `npm start` и `npm run dev` работают

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 133: docs, Postman, auth skeleton"`
- Поставь тег: `git tag week-19-done`

---

## Проект недели

**Express Notes API** с PostgreSQL. Спецификация: [docs/projects.md — неделя 19](../../docs/projects.md#неделя-19--express-notes-api).

### Структура

```
week-19/
├── src/
│   ├── app.js
│   ├── server.js
│   ├── routes/
│   ├── controllers/
│   ├── services/
│   ├── db/
│   └── middleware/
├── schema.sql
├── docs/
│   ├── postman-collection.json
│   └── compare.md
├── package.json
├── .env.example
└── README.md
```

### Функции

1. Full CRUD `/api/notes`
2. Zod validation, error middleware, request logging (morgan)
3. Layered architecture: routes → controllers → services → db
4. PostgreSQL + migrations + seed
5. Health check, graceful shutdown, Postman collection

### Критерии проекта

- [ ] Production-like структура папок
- [ ] Все SQL через `pool.query` с placeholders
- [ ] Graceful shutdown (SIGTERM) закрывает pool
- [ ] Health endpoint возвращает статус БД
- [ ] Postman collection покрывает все endpoints
- [ ] Стиль API согласован с FastAPI проектом недели 18 (статусы, формат ошибок)
- [ ] Тег `week-19-done`

## Ревью-чеклист
- Node vs Browser JS — 3 главных отличия?
- Что делает middleware `next()`?
- Зачем connection pool вместо одного client?
- Как валидировать body в Express?
- ESM vs CommonJS — что выбрал и почему?


## Проверь себя

<details>
<summary>Что должно получиться к концу недели?</summary>

Работающий проект **Express Notes API** в `learning-log/week-19/`, осмысленная Git-история, тег `week-19-done`.

</details>

<details>
<summary>Главный навык недели одной фразой?</summary>

Node.js + Express layered API

</details>

<details>
<summary>Можно ли пропустить день?</summary>

Нет — дни связаны. В **лайт-режиме** сократи практику до MVP, но теорию и Git-коммит не пропускай.

</details>
