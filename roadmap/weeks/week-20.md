# Неделя 20: Auth, безопасность, тестирование

> **Цель недели:** реализовать JWT-аутентификацию, изучить OWASP и написать базовые тесты (Vitest + pytest).
> **Литература:** [JWT.io](https://jwt.io/introduction), [OWASP Top 10](https://owasp.org/www-project-top-ten/), [Vitest](https://vitest.dev/), [pytest](https://docs.pytest.org/)
> **Проект недели:** [Secure Notes](../../docs/projects.md#неделя-20--secure-notes) — JWT auth, bcrypt, rate limit, React client, pytest + Vitest.
> **Git:** папка `learning-log/week-20/`, отдельные коммиты backend/frontend; тег `week-20-done`.

## День 134 (Пн): Аутентификация и хеширование паролей

### Теория
- **Authentication** (кто ты) vs **Authorization** (что тебе можно) — разные слои безопасности
- [bcrypt](https://github.com/kelektiv/node.bcrypt.js) / [passlib](https://passlib.readthedocs.io/) — adaptive hashing, встроенный salt
- Никогда не храни plain-text пароли — даже в dev/test БД
- Salt rounds 10–12 для bcrypt — баланс безопасность/скорость
- Registration flow: validate email → hash password → store user → (опционально) auto-login
- Generic error messages на login — не раскрывай «email не найден» vs «неверный пароль»

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
- [JWT structure](https://jwt.io/introduction): header.payload.signature — подпись, не шифрование
- [jsonwebtoken](https://github.com/auth0/node-jsonwebtoken) (Node) / [python-jose](https://python-jose.readthedocs.io/) (FastAPI)
- Access token TTL: 15min–1h; refresh token — отдельный долгоживущий токен (обзор)
- Header: `Authorization: Bearer <token>` — стандарт передачи
- `JWT_SECRET` в `.env` — минимум 32 случайных байта, rotate при утечке
- Payload: только `sub` (user id), `exp`, `iat` — не клади пароли и PII

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
- [OWASP Top 10 (2021)](https://owasp.org/Top10/): injection, broken auth, XSS, SSRF и др.
- SQL injection — parameterized queries (уже знаешь с нед. 17–19)
- XSS: escape output, [DOMPurify](https://github.com/cure53/DOMPurify) для user-generated HTML
- [Helmet.js](https://helmetjs.github.io/) — X-Content-Type-Options, X-Frame-Options и др.
- [express-rate-limit](https://github.com/express-rate-limit/express-rate-limit) — brute-force protection
- CORS: явный whitelist origins, не `*` с credentials

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
- [pytest](https://docs.pytest.org/en/stable/getting-started.html): fixtures, parametrize, assert
- [FastAPI TestClient](https://fastapi.tiangolo.com/tutorial/testing/) — синхронные HTTP-тесты без реального сервера
- Test DB isolation — отдельная schema или transaction rollback per test
- Factory fixtures: `create_user()`, `auth_headers(token)`
- Coverage: `pytest --cov=app` — что не покрыто тестами
- Arrange-Act-Assert — структура каждого теста

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
- [Vitest](https://vitest.dev/guide/): Vite-native, совместим с Jest API
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) — тестируй поведение, не implementation
- `render`, `screen.getByRole`, `userEvent` — доступные селекторы
- Mock fetch: `vi.fn()`, `global.fetch = vi.fn().mockResolvedValue(...)`
- `vi.mock()` — изоляция модулей
- Тестируй то, что видит пользователь: кнопки, формы, сообщения об ошибках

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
- Token storage: localStorage (просто, уязвим к XSS) vs httpOnly cookie (безопаснее, сложнее CORS)
- [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- Axios interceptors или fetch wrapper — автоматический `Authorization` header
- Auto logout on 401 — очистка token и redirect
- React Router protected routes — `<ProtectedRoute>` wrapper
- AuthContext: `user`, `token`, `login`, `logout`, `isLoading`

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
- GitHub Actions: matrix jobs для backend + frontend tests
- `npm audit`, `pip audit` — known vulnerabilities
- [Semgrep](https://semgrep.dev/) — static analysis (обзор)
- CI на каждый push — раннее обнаружение регрессий
- Branch protection: require CI green before merge (обзор)

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
