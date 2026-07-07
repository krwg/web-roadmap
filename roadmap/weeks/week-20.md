# Неделя 20: Auth, безопасность, тестирование

> **Цель недели:** реализовать JWT-аутентификацию, изучить OWASP и написать базовые тесты (Vitest + pytest).
> **Литература:** [JWT.io](https://jwt.io/introduction), [OWASP Top 10](https://owasp.org/www-project-top-ten/), [Vitest](https://vitest.dev/), [pytest](https://docs.pytest.org/)
> **Проект недели:** [Secure Notes](../../docs/projects.md#неделя-20--secure-notes) — JWT auth, bcrypt, rate limit, React client, pytest + Vitest.
> **Git:** папка `learning-log/week-20/`, отдельные коммиты backend/frontend; тег `week-20-done`.

## День 134 (Пн): Аутентификация и хеширование паролей

### Теория

Authentication отвечает на вопрос «кто ты?» — проверка личности (логин/пароль). Authorization — «что тебе можно?» — права на ресурсы. Не путай: успешный login не означает доступ ко всем endpoints. Пароли никогда не хранятся в plain text, даже в dev-базе.

bcrypt (Node) и passlib с bcrypt (Python) — adaptive hashing с встроенным salt. Salt rounds 10–12 — баланс безопасность/скорость. При register: validate email → `hash(password, 12)` → store `password_hash`. При login: `compare(plain, hash)`. SHA256 без salt уязвим к rainbow tables.

Registration flow: дубликат email → 409 Conflict. Login: неверный пароль → 401 Unauthorized с generic message «Invalid credentials» — не раскрывай, существует ли email. Пароль не логируй и не возвращай в JSON response.

**Читать:**

- [bcrypt (Node)](https://github.com/kelektiv/node.bcrypt.js)
- [passlib](https://passlib.readthedocs.io/)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

**Ключевая мысль:** hash + salt через bcrypt; одинаковые сообщения об ошибке login — против enumeration.

### Практика
1. Таблица `users(id, email UNIQUE, password_hash, created_at)`
2. Express: `POST /auth/register`, `POST /auth/login`
3. `bcrypt.hash(password, 12)` при register, `bcrypt.compare()` при login
4. FastAPI параллельно (или выбери один стек): `passlib[bcrypt]`, `CryptContext`
5. Дубликат email → 409 Conflict
6. Неверный пароль → 401 Unauthorized

**Критерии:**
- [ ] Пароль никогда не логируется и не возвращается в JSON
- [ ] Дубликат email → 409
- [ ] Неверный пароль → 401 (не 404)

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 134: register login bcrypt"`

### Ловушки
- SHA256 без salt для паролей — уязвимо к rainbow tables
- Разные сообщения для «user not found» и «wrong password» — information leak

---

## День 135 (Вт): JWT — выдача и проверка токенов

### Теория

JWT (JSON Web Token) — компактный способ передавать claims между клиентом и сервером. Структура: header.payload.signature. Подпись (HMAC SHA256) гарантирует целостность; payload base64-decodable — не клади пароли и PII. Стандарт передачи: `Authorization: Bearer <token>`.

Access token TTL 15min–1h; refresh token — отдельный долгоживущий механизм (обзор). `JWT_SECRET` в `.env` — минимум 32 случайных байта; при утечке — rotate немедленно. Payload: `sub` (user id), `exp`, `iat`. Явно указывай `algorithm: 'HS256'` — алгоритм `none` — уязвимость.

Middleware `authenticateToken` verify JWT и кладёт `req.user = { id, email }`. Protected routes читают `user_id` из token, не из body/query — иначе IDOR. Expired token → 401. Тест с TTL 1 секунда проверяет expiration.

**Читать:**

- [JWT Introduction](https://jwt.io/introduction)
- [jsonwebtoken](https://github.com/auth0/node-jsonwebtoken)
- [python-jose](https://python-jose.readthedocs.io/)

**Ключевая мысль:** JWT — подписанный контракт, не шифрование; user_id только из verified token.

### Практика
1. Login возвращает `{ access_token, token_type: "bearer", expires_in }`
2. Middleware `authenticateToken` — verify JWT, `req.user = { id, email }`
3. Protected: `GET /api/notes` только с valid token
4. 401 без token, 403 при доступе к чужим данным (user_id из token)
5. Expired token test — измени TTL на 1 сек для проверки
6. Явно укажи algorithm: `algorithm: 'HS256'`

**Критерии:**
- [ ] JWT_SECRET в .env, не в коде
- [ ] Expired token → 401
- [ ] user_id из token, не из body/query

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 135: JWT middleware and protected routes"`

### Ловушки
- Алгоритм `none` — всегда указывай algorithm explicitly
- Sensitive data в JWT payload — payload base64-decodable

---

## День 136 (Ср): OWASP Top 10 — практическая защита

### Теория

OWASP Top 10 — карта самых частых уязвимостей веб-приложений. Ты уже закрываешь injection parameterized queries (нед. 17–19). Broken authentication — слабые пароли, утечка session. XSS — неэкранированный user-generated HTML; escape output, DOMPurify для rich text.

Helmet.js выставляет security headers: `X-Content-Type-Options`, `X-Frame-Options`, CSP basics. `express-rate-limit` на `/auth/login`: 5 попыток / 15 мин per IP → 429 Too Many Requests — защита от brute-force. CORS: явный whitelist origins; `origin: '*'` с credentials — небезопасно.

Аудит: `.env` в `.gitignore`, `.env.example` без секретов, проверь `git log` на утечки. `security-audit.md` с чеклистом 10 пунктов — deliverable недели. CORS в dev: allow только `http://localhost:5173`.

**Читать:**

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Helmet.js](https://helmetjs.github.io/)
- [express-rate-limit](https://github.com/express-rate-limit/express-rate-limit)

**Ключевая мысль:** безопасность — слои: hash, JWT, rate limit, headers, CORS, audit.

### Практика
1. Rate limit на `/auth/login`: 5 попыток / 15 мин per IP
2. `helmet()` в Express; FastAPI — security headers middleware (обзор)
3. Аудит API: чеклист OWASP 10 пунктов → `security-audit.md`
4. `.env` в `.gitignore`, `.env.example` без реальных секретов
5. Проверь: нет секретов в `git log` (`git log -p | grep SECRET`)
6. CORS: allow только `http://localhost:5173` в dev

**Критерии:**
- [ ] Rate limiting работает (429 Too Many Requests)
- [ ] Helmet headers в response (проверь `curl -I`)
- [ ] Чеклист OWASP заполнен в `security-audit.md`

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 136: OWASP audit rate limit helmet"`

### Ловушки
- CORS `origin: '*'` с credentials — небезопасно
- Секреты в git history — rotate keys если утекли

---

## День 137 (Чт): Тестирование backend — pytest

### Теория

Backend-тесты ловят регрессии в auth и authorization. pytest + FastAPI TestClient или supertest для Express — HTTP без реального порта. Fixtures: `create_user()`, `auth_headers(token)`. Test DB изолирована: отдельная schema или rollback per test — никогда production.

Arrange-Act-Assert в каждом тесте. Покрой: register success, duplicate 409, wrong password 401, protected 401 без token, 200 с token, user A не видит notes user B. `conftest.py` — shared setup. `pytest --cov=app` показывает пробелы.

Тесты не должны зависеть от порядка выполнения. Hardcoded JWT secret в тестах должен совпадать с app config. ≥ 10 тестов — минимум для Secure Notes. Flaky tests из shared DB без cleanup — исправь до merge.

**Читать:**

- [pytest](https://docs.pytest.org/en/stable/getting-started.html)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [supertest](https://github.com/ladjs/supertest)

**Ключевая мысль:** тестируй auth, 403 cross-user и 401 без token — не только happy path.

### Практика
1. Тесты auth: register success, duplicate email 409, login, wrong password 401
2. Fixture: test user + valid token в `Authorization` header
3. Protected route: 401 без token, 200 с token
4. CRUD notes per user — user A не видит notes user B
5. ≥ 10 pytest тестов для выбранного backend (FastAPI или Express через supertest)
6. `conftest.py` с test database и cleanup

**Критерии:**
- [ ] `pytest` все зелёные
- [ ] Тесты не зависят от порядка выполнения
- [ ] conftest.py с test database

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 137: pytest auth and notes tests"`

### Ловушки
- Тесты на shared DB без cleanup — flaky tests
- Hardcoded JWT secret в тестах отличается от app — 401 везде

---

## День 138 (Пт): Тестирование frontend — Vitest

### Теория

Vitest — test runner, нативный для Vite-проектов, API совместим с Jest. React Testing Library (RTL) тестирует поведение с точки зрения пользователя: `getByRole`, `getByLabelText`, не `getByClassName`. `userEvent` симулирует реальные клики и ввод с клавиатуры.

Mock `fetch` через `vi.fn()` или `global.fetch = vi.fn().mockResolvedValue(...)` изолирует компоненты от API. Тестируй: Login submit шлёт credentials, ProtectedRoute редиректит без token, NotesList рендерит mock data, login 401 показывает ошибку. `vi.mock()` для модулей.

≥ 8 component tests. `vitest run` в CI. Тестирование internal state вместо visible behavior — хрупкие тесты. Cleanup mocks в `afterEach` — иначе тесты влияют друг на друга.

**Читать:**

- [Vitest](https://vitest.dev/guide/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [userEvent](https://testing-library.com/docs/user-event/intro/)

**Ключевая мысль:** RTL — «как пользователь видит»; mock fetch, не implementation details.

### Практика
1. `npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom @testing-library/user-event`
2. Тест: Login form — submit вызывает API с email/password
3. Тест: Protected route redirect на `/login` без token
4. Mock API: register success, login 401 показывает ошибку
5. Тест NotesList — рендерит заметки из mock response
6. `npm test` / `vitest run` в package.json scripts

**Критерии:**
- [ ] `vitest run` проходит
- [ ] Тесты ищут по role/label, не по className
- [ ] ≥ 8 unit/component тестов

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 138: Vitest auth and notes components"`

### Ловушки
- Тестирование state вместо behavior — хрупкие тесты
- Забытый mock cleanup — тесты влияют друг на друга

---

## День 139 (Сб): Интеграция auth frontend + backend

### Теория

Full-stack auth связывает JWT backend с React frontend. Token storage: localStorage прост, но уязвим к XSS; httpOnly cookie безопаснее, сложнее с CORS. Для учебного проекта localStorage + CSP + sanitize input — приемлемо; задокументируй trade-off в README.

`AuthContext`: `user`, `token`, `login`, `logout`, `isLoading`. `api.ts` wrapper подставляет `Authorization: Bearer` и на 401 очищает token + redirect `/login`. React Router `<ProtectedRoute>` оборачивает private pages. Token не в URL query string — утечёт в logs и history.

Full flow: register → login → create note → logout → login → note visible. User A не видит notes User B — проверь вручную и тестами. Axios interceptors или fetch wrapper — один вход для всех API calls.

**Читать:**

- [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [React Router — protected routes](https://reactrouter.com/en/main/examples/auth)
- [MDN — HTTP Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication)

**Ключевая мысль:** auth flow end-to-end — контракт между Context, api wrapper и protected routes.

### Практика
1. React (Vite + TS): Login/Register pages с валидацией форм
2. `AuthContext` + `useAuth()` hook
3. `api.ts` wrapper — подставляет Bearer token, обрабатывает 401
4. Protected routes — redirect `/login` если не авторизован
5. Logout очищает token и context, redirect на login
6. Full flow manual test: register → login → create note → logout → login again

**Критерии:**
- [ ] Full flow: register → login → access protected → logout
- [ ] 401 от API → redirect login
- [ ] Token не в URL query string

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 139: React auth integration"`

### Ловушки
- XSS + localStorage token — кража token (mitigate: CSP, sanitize input)
- Token без expiration check на клиенте — плохой UX при expired

---

## День 140 (Вс): Ревью безопасности и CI

### Теория

CI автоматизирует проверку качества на каждый push. GitHub Actions: matrix jobs для backend (`pytest`) и frontend (`vitest run`). Зелёный CI — сигнал, что main mergeable. Branch protection с require CI — best practice для команд (обзор).

`npm audit` и `pip audit` сканируют known vulnerabilities в зависимостях. Critical без комментария или плана фикса — красный флаг для портфолио. Semgrep — static analysis (обзор). Sequence diagram auth flow в README объясняет архитектуру ревьюеру.

Финальный security review по OWASP чеклисту. Обнови `.env.example` для backend и frontend. Smoke test checklist в README. Тег `week-20-done` — Secure Notes готов как шаблон для недель 21–22.

**Читать:**

- [GitHub Actions](https://docs.github.com/en/actions)
- [npm audit](https://docs.npmjs.com/cli/v10/commands/npm-audit)
- [pip-audit](https://pypi.org/project/pip-audit/)

**Ключевая мысль:** CI + security audit — часть Definition of Done, не «после деплоя».

### Практика
1. `.github/workflows/ci.yml`: `pytest` + `vitest run` на push
2. `npm audit` и `pip audit` — отчёт в `security-audit.md`
3. Документируй auth flow: sequence diagram в README
4. Финальный security review по OWASP чеклисту
5. Обнови `.env.example` для backend и frontend
6. Smoke test checklist в README

**Критерии:**
- [ ] CI workflow файл в `.github/workflows/`
- [ ] npm audit — нет critical без комментария
- [ ] Auth flow задокументирован

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 140: CI workflow and security docs"`
- Поставь тег: `git tag week-20-done`

---

## Проект недели

**Secure Notes API + React Client**. Спецификация: [docs/projects.md — неделя 20](../../docs/projects.md#неделя-20--secure-notes).

### Стек

- Backend: Express **или** FastAPI — register, login, JWT, CRUD notes per user
- Security: bcrypt/passlib, rate limit на login, helmet/CORS
- Frontend: React + TypeScript — auth pages, protected dashboard, notes CRUD
- Tests: pytest ≥ 10, Vitest ≥ 8
- CI: GitHub Actions green on push

### Функции

1. Регистрация и логин с JWT access token
2. Notes привязаны к `user_id` из token
3. User A не может читать/менять notes User B → 403
4. React: AuthContext, protected routes, API wrapper
5. `security-audit.md` с OWASP чеклистом

### Критерии проекта

- [ ] Пароли hashed, JWT в `Authorization: Bearer` header
- [ ] Rate limiting на `/auth/login`
- [ ] Frontend + backend тесты в CI
- [ ] OWASP чеклист пройден и задокументирован
- [ ] Full auth flow работает end-to-end в браузере
- [ ] README: env vars, run backend, run frontend, run tests
- [ ] Тег `week-20-done`

## Ревью-чеклист
- JWT vs session cookie — плюсы и минусы?
- Как защититься от SQL injection и XSS?
- Зачем rate limiting на login?
- Что тестирует React Testing Library?
- Что делать если JWT secret утёк в git?
