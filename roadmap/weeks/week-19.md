# Неделя 19: Node.js + Express REST API

> **Цель недели:** построить REST API на JavaScript в среде Node.js с Express и PostgreSQL.
> **Литература:** [Node.js Docs](https://nodejs.org/en/docs), [Express Guide](https://expressjs.com/en/guide/routing.html), [node-postgres](https://node-postgres.com/)
> **Проект недели:** [Express Notes API](../../docs/projects.md#неделя-19--express-notes-api) — layered Express API, Zod, PostgreSQL, Postman collection.
> **Git:** папка `learning-log/week-19/`, ветки `feature/routes`, `feature/pg`; тег `week-19-done`.

## День 127 (Пн): Node.js — среда и модули

### Теория
- [Node.js Introduction](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs): нет DOM/BOM, есть `process`, `global`, модули
- CommonJS (`require`) vs [ES Modules](https://nodejs.org/api/esm.html) (`import`) — `"type": "module"` в package.json
- npm: `package.json`, semver, `node_modules`, scripts — стандарт экосистемы JS backend
- Встроенные модули: [fs](https://nodejs.org/api/fs.html), [path](https://nodejs.org/api/path.html), [http](https://nodejs.org/api/http.html)
- `process.argv`, `process.env` — CLI и конфигурация
- `import.meta.url` + `fileURLToPath` — ESM-эквивалент `__dirname`

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

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 127: Node ESM setup and file CLI"`

### Ловушки
- require() в ESM project — SyntaxError
- Относительные пути без path.join — ломается на Windows

---

## День 128 (Вт): Асинхронность в Node

### Теория
- Callback → Promise → async/await — эволюция асинхронного Node-кода
- [Event Loop в Node](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) — libuv, phases, не блокируй main thread
- [EventEmitter](https://nodejs.org/api/events.html) — `on`, `emit`, `once` — основа многих Node API
- `fs.watch` / `chokidar` — реакция на изменения файлов
- `process.on('unhandledRejection')` — лови необработанные Promise rejections
- `promisify` из `util` — обёртка callback API в Promise

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

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 128: async file watcher and error handling"`

### Ловушки
- Забытый await — Promise вместо данных
- Синхронный `fs.readFileSync` в сервере — блокирует event loop

---

## День 129 (Ср): Express — REST API основы

### Теория
- [Express Hello World](https://expressjs.com/en/starter/hello-world.html) — минимальный HTTP-сервер
- Routes: `app.get/post/put/delete`, `req.params`, `req.query`, `req.body`
- [express.json()](https://expressjs.com/en/api.html#express.json) middleware — парсинг JSON body
- HTTP status codes: 200, 201, 204, 400, 404, 500 — семантика ответа
- Разделение `app.js` (конфигурация) и `server.js` (listen) — тестируемость
- `nodemon` — автоперезапуск в dev

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

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 129: Express CRUD notes in-memory JSON"`

### Ловушки
- POST без body parser — req.body undefined
- Один огромный app.js — разбей на routes

---

## День 130 (Чт): Middleware, валидация, ошибки

### Теория
- [Writing middleware](https://expressjs.com/en/guide/using-middleware.html): `(req, res, next)` — цепочка обработки
- Error middleware: 4 аргумента `(err, req, res, next)` — централизованные ошибки
- [Zod](https://zod.dev/) — schema validation с TypeScript inference
- [morgan](https://github.com/expressjs/morgan) — HTTP request logging
- Порядок middleware важен: logger → parser → routes → error handler
- `next(err)` передаёт управление error middleware

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

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 130: Zod validation and error middleware"`

### Ловушки
- Забытый `next(err)` — зависший request
- Error middleware без 4 параметров — не вызывается

---

## День 131 (Пт): Express + PostgreSQL

### Теория
- [node-postgres](https://node-postgres.com/): `Pool`, `pool.query(text, params)`
- Connection string: `DATABASE_URL=postgresql://user:pass@host:5432/db`
- Prepared statements: `$1, $2` placeholders — защита от SQL injection
- [Prisma](https://www.prisma.io/) — ORM-альтернатива (обзор, на этой неделе raw pg)
- Pool vs Client — pool переиспользует соединения под нагрузкой
- Graceful shutdown: `pool.end()` на SIGTERM

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

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 131: Express notes with PostgreSQL pool"`

### Ловушки
- SQL injection через template strings — только placeholders
- Pool не закрывается при shutdown — graceful exit

---

## День 132 (Сб): Структура проекта и роутеры

### Теория
- [Express Router](https://expressjs.com/en/guide/routing.html#express-router) — модульные маршруты
- Layered architecture: routes → controllers → services → db — разделение ответственности
- [dotenv](https://github.com/motdotla/dotenv) — secrets из `.env`, не из кода
- Environment: `NODE_ENV=development|production` — разное поведение
- Health check pattern — `/api/health` для мониторинга и Docker
- `package-lock.json` в git — воспроизводимые сборки

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

### Git
- Закоммить изменения дня: `git add week-19/` → `git commit -m "week 19 day 132: layered architecture and health check"`

### Ловушки
- Бизнес-логика в route handler — не тестируется
- Циклические импорты между modules

---

## День 133 (Вс): Ревью Node.js и сравнение с FastAPI

### Теория
- Node vs Python backend: I/O-bound → оба хороши; CPU-bound → Python часто проще
- [npm scripts](https://docs.npmjs.com/cli/v10/using-npm/scripts) best practices: `start`, `dev`, `test`, `db:migrate`
- Package lock в git — обязательно для командной работы
- Express vs Fastify vs Nest — обзор (Express — минимализм и экосистема)
- Подготовка к неделе 20: skeleton auth routes

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
