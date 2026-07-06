# Неделя 19: Node.js + Express REST API

> **Цель недели:** построить REST API на JavaScript в среде Node.js с Express и PostgreSQL.
> **Литература:** [Node.js Docs](https://nodejs.org/en/docs), [Express Guide](https://expressjs.com/en/guide/routing.html), [node-postgres](https://node-postgres.com/)

## День 127 (Пн): Node.js — среда и модули

### Теория
- [Node.js Introduction](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs): нет DOM, есть `process`, `global`
- CommonJS vs [ES Modules](https://nodejs.org/api/esm.html): `"type": "module"` в package.json
- npm: `npm init`, `package.json`, `node_modules`, scripts
- Встроенные модули: [fs](https://nodejs.org/api/fs.html), [path](https://nodejs.org/api/path.html), [http](https://nodejs.org/api/http.html)

### Практика
1. `mkdir notes-api && npm init -y`, добавь `"type": "module"`
2. CLI: `node scripts/greet.js --name=Alex` (parse process.argv)
3. Чтение/запись `notes.json` через `fs.promises`
4. `path.join`, `import.meta.url` для `__dirname` equivalent

**Критерии:**
- [ ] ES modules (import/export)
- [ ] fs.promises, не callback fs.readFile
- [ ] npm script `"greet": "node scripts/greet.js"`

### Ловушки
- require() в ESM project — SyntaxError
- Относительные пути без path.join — ломается на Windows

---

## День 128 (Вт): Асинхронность в Node

### Теория
- Callback → Promise → async/await в Node
- [Event Loop в Node](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) — обзор
- [EventEmitter](https://nodejs.org/api/events.html) — `on`, `emit`
- `fs.watch` — отслеживание файлов

### Практика
1. Перепиши file I/O на async/await
2. File watcher: логирует изменения `notes.json`
3. Промисификация: `const readFile = promisify(fs.readFile)` (для понимания)
4. Обработка unhandledRejection в entry point

**Критерии:**
- [ ] Нет callback hell — только async/await
- [ ] Watcher корректно останавливается (SIGINT)
- [ ] try/catch вокруг await

### Ловушки
- Забытый await — Promise вместо данных
- Синхронный `fs.readFileSync` в сервере — блокирует event loop

---

## День 129 (Ср): Express — REST API основы

### Теория
- [Express Hello World](https://expressjs.com/en/starter/hello-world.html)
- Routes: `app.get/post/put/delete`, `req.params`, `req.query`, `req.body`
- [express.json()](https://expressjs.com/en/api.html#express.json) middleware
- [HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) — 200, 201, 400, 404, 500

### Практика
1. `npm install express`, `src/app.js`, `src/server.js`
2. CRUD `/api/notes` — хранение в JSON-файле
3. `GET /api/notes/:id` — 404 если нет
4. `nodemon` для dev: `npm install -D nodemon`

**Критерии:**
- [ ] express.json() подключён
- [ ] RESTful URLs и методы
- [ ] 201 на POST, 204 на DELETE

### Ловушки
- POST без body parser — req.body undefined
- Один огромный app.js — разбей на routes

---

## День 130 (Чт): Middleware, валидация, ошибки

### Теория
- [Writing middleware](https://expressjs.com/en/guide/using-middleware.html): `(req, res, next)`
- Error middleware: 4 аргумента `(err, req, res, next)`
- [Zod](https://zod.dev/) для валидации body
- [morgan](https://github.com/expressjs/morgan) — HTTP logging

### Практика
1. Logger middleware: method, url, duration
2. Zod schema для Note: title min 1, body optional
3. Centralized error handler — JSON `{ error: message }`
4. 400 при validation error с деталями zod

**Критерии:**
- [ ] Все ошибки проходят через error middleware
- [ ] Zod на POST и PUT
- [ ] morgan или custom logger

### Ловушки
- Забытый `next(err)` — зависший request
- Error middleware без 4 параметров — не вызывается

---

## День 131 (Пт): Express + PostgreSQL

### Теория
- [node-postgres](https://node-postgres.com/): `Pool`, `pool.query()`
- Connection string: `DATABASE_URL`
- Prepared statements: `$1, $2` placeholders
- [Prisma](https://www.prisma.io/) — обзор как альтернатива raw pg

### Практика
1. `npm install pg dotenv`
2. Pool из `DATABASE_URL`, тест подключения
3. Перепиши notes API на таблицу `notes(id, title, body, created_at)`
4. `schema.sql` + migration script

**Критерии:**
- [ ] Pool, не Client на каждый запрос
- [ ] Параметризованные запросы ($1, $2)
- [ ] dotenv, `.env.example`

### Ловушки
- SQL injection через template strings — только placeholders
- Pool не закрывается при shutdown — graceful exit

---

## День 132 (Сб): Структура проекта и роутеры

### Теория
- [Express Router](https://expressjs.com/en/guide/routing.html#express-router)
- Layered architecture: routes → controllers → services → db
- [dotenv](https://github.com/motdotla/dotenv) — secrets
- Environment: development vs production

### Практика
1. Структура: `src/routes/`, `controllers/`, `services/`, `db/pool.js`
2. Вынеси логику из routes в controller/service
3. `GET /api/health` — проверка DB connection

**Критерии:**
- [ ] Routes тонкие — только маршрутизация
- [ ] Service переиспользуется из controller
- [ ] health check возвращает 503 если DB down

### Ловушки
- Бизнес-логика в route handler — не тестируется
- Циклические импорты между modules

---

## День 133 (Вс): Ревью Node.js и сравнение с FastAPI

### Теория
- Node vs Python backend: когда что (обзор)
- [npm scripts](https://docs.npmjs.com/cli/v10/using-npm/scripts) best practices
- Package lock: `package-lock.json` в git

### Практика
1. Сравнительная таблица: FastAPI (нед.18) vs Express — 10 критериев
2. Postman collection для Express API
3. README с curl примерами
4. Подготовь skeleton auth routes для недели 20

**Критерии:**
- [ ] README полный (install, env, run, test)
- [ ] Сравнительная таблица в docs
- [ ] `npm start` и `npm run dev` работают

---

## Проект недели

**Express Notes API** с PostgreSQL:

1. Full CRUD `/api/notes`
2. Zod validation, error middleware, request logging
3. Layered architecture (routes/controllers/services)
4. PostgreSQL + migrations + seed
5. Health check, README, Postman collection

**Критерии:**
- [ ] Production-like структура папок
- [ ] Все SQL через pool.query с placeholders
- [ ] Graceful shutdown (SIGTERM)
- [ ] Совместим по стилю с FastAPI проектом недели 18

## Ревью-чеклист
- Node vs Browser JS — 3 главных отличия?
- Что делает middleware `next()`?
- Зачем connection pool вместо одного client?
- Как валидировать body в Express?
- ESM vs CommonJS — что выбрал и почему?
