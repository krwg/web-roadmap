# Неделя 20: Auth, безопасность, тестирование

> **Цель недели:** реализовать JWT-аутентификацию, изучить OWASP и написать базовые тесты (Vitest + pytest).
> **Литература:** [JWT.io](https://jwt.io/introduction), [OWASP Top 10](https://owasp.org/www-project-top-ten/), [Vitest](https://vitest.dev/), [pytest](https://docs.pytest.org/)

## День 134 (Пн): Аутентификация и хеширование паролей

### Теория
- Auth vs Authorization — разница
- [bcrypt](https://github.com/kelektiv/node.bcrypt.js) / [passlib](https://passlib.readthedocs.io/) — хеширование паролей
- Никогда не храни plain-text пароли
- Salt rounds: 10–12 для bcrypt
- Registration flow: validate → hash → store user

### Практика
1. Таблица `users(id, email, password_hash, created_at)` — UNIQUE email
2. Express: `POST /auth/register`, `POST /auth/login`
3. `bcrypt.hash()` при register, `bcrypt.compare()` при login
4. FastAPI: те же endpoints с `passlib[bcrypt]` (параллельно или выбери один стек)

**Критерии:**
- [ ] Пароль никогда не логируется и не возвращается в JSON
- [ ] Дубликат email → 409
- [ ] Неверный пароль → 401 (не 404)

### Ловушки
- SHA256 без salt для паролей — уязвимо к rainbow tables
- Одинаковое сообщение для «user not found» и «wrong password» — timing attacks (на junior — хотя бы generic message)

---

## День 135 (Вт): JWT — выдача и проверка токенов

### Теория
- [JWT structure](https://jwt.io/introduction): header.payload.signature
- [jsonwebtoken](https://github.com/auth0/node-jsonwebtoken) (Node) / [python-jose](https://python-jose.readthedocs.io/) (FastAPI)
- Access token TTL: 15min–1h, refresh token (обзор)
- Header: `Authorization: Bearer <token>`
- Secret в `.env`: `JWT_SECRET` — длинная случайная строка

### Практика
1. Login возвращает `{ access_token, token_type: "bearer" }`
2. Middleware `authenticateToken` — проверка JWT, `req.user = payload`
3. Protected: `GET /api/notes` только с valid token
4. 401 без token, 403 при доступе к чужим данным

**Критерии:**
- [ ] JWT_SECRET в .env, не в коде
- [ ] Expired token → 401
- [ ] user_id из token, не из body

### Ловушки
- Алгоритм `none` — всегда указывай algorithm explicitly
- Sensitive data в JWT payload — payload base64, не encrypted

---

## День 136 (Ср): OWASP Top 10 — практическая защита

### Теория
- [OWASP Top 10 (2021)](https://owasp.org/Top10/): injection, broken auth, XSS, etc.
- SQL injection — parameterized queries (уже знаешь)
- XSS: escape output, [DOMPurify](https://github.com/cure53/DOMPurify) на фронте
- [Helmet.js](https://helmetjs.github.io/) — secure HTTP headers
- [express-rate-limit](https://github.com/express-rate-limit/express-rate-limit)

### Практика
1. Rate limit на `/auth/login`: 5 попыток / 15 мин
2. `helmet()` в Express
3. Аудит своего API: чеклист OWASP (10 пунктов — отметь статус)
4. `.env` в `.gitignore`, `.env.example` без секретов

**Критерии:**
- [ ] Rate limiting работает (429 Too Many Requests)
- [ ] Helmet headers в response (проверь curl -I)
- [ ] Чеклист OWASP заполнен в `security-audit.md`

### Ловушки
- CORS `origin: '*'` с credentials — небезопасно
- Секреты в git history — rotate keys если утекли

---

## День 137 (Чт): Тестирование backend — pytest

### Теория
- [pytest](https://docs.pytest.org/en/stable/getting-started.html): fixtures, assert
- [FastAPI TestClient](https://fastapi.tiangolo.com/tutorial/testing/)
- Test DB isolation, factory fixtures
- Coverage: `pytest --cov` (обзор)

### Практика
1. Тесты auth: register, login, protected route, wrong password → 401
2. Fixture: test user + valid token
3. ≥ 10 тестов для FastAPI library API

**Критерии:**
- [ ] `pytest` все зелёные
- [ ] Тесты не зависят от порядка выполнения
- [ ] conftest.py с test database

### Ловушки
- Тесты на shared DB без cleanup — flaky tests
- Hardcoded JWT secret в тестах отличается от app — 401 везде

---

## День 138 (Пт): Тестирование frontend — Vitest

### Теория
- [Vitest](https://vitest.dev/guide/): Vite-native test runner
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) — тестируй как user
- `render`, `screen`, `fireEvent`, `userEvent`
- Mock fetch: `vi.fn()`, `global.fetch = vi.fn()`

### Практика
1. `npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom`
2. Тест: Counter component — click +1
3. Тест: Login form — submit вызывает callback с email/password
4. Mock API response для PostList

**Критерии:**
- [ ] `npm test` / `vitest run` проходит
- [ ] Тесты ищут по role/label, не по className
- [ ] ≥ 6 unit/component тестов

### Ловушки
- Тестирование implementation details (state) вместо behavior
- Забытый `cleanup` — в RTL auto с RTL 13+

---

## День 139 (Сб): Интеграция auth frontend + backend

### Теория
- Token storage: localStorage vs httpOnly cookie — tradeoffs
- [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- Axios interceptors или fetch wrapper для Authorization header
- Auto logout on 401

### Практика
1. React: Login/Register pages
2. `AuthContext`: user, token, login, logout
3. `api.js` wrapper — подставляет Bearer token
4. Protected routes в React Router — redirect /login
5. Logout очищает token и context

**Критерии:**
- [ ] Full flow: register → login → access protected → logout
- [ ] 401 от API → redirect login
- [ ] Token не в URL query string

### Ловушки
- XSS + localStorage token — кража token (mitigate: CSP, sanitize)
- Token без expiration check на клиенте — UX зависание

---

## День 140 (Вс): Ревью безопасности и тестов

### Теория
- CI basics: GitHub Actions `npm test` + `pytest` (обзор)
- [Semgrep](https://semgrep.dev/) или `npm audit`

### Практика
1. `npm audit fix` и `pip audit` — отчёт
2. GitHub Action: run tests on push

**Критерии:**
- [ ] CI workflow файл в `.github/workflows/`
- [ ] npm audit — нет critical без комментария
- [ ] Auth flow задокументирован

---

## Проект недели

**Secure Notes API + React Client**:

1. Backend (Express или FastAPI): register, login, JWT, CRUD notes per user
2. bcrypt/passlib, rate limit, helmet/CORS configured
3. React: auth pages, protected dashboard, notes CRUD
4. pytest ≥ 10 tests, Vitest ≥ 8 tests
5. `security-audit.md` + CI

**Критерии:**
- [ ] User A не видит notes User B (403)
- [ ] Пароли hashed, JWT в Authorization header
- [ ] Frontend + backend тесты в CI
- [ ] OWASP чеклист пройден

## Ревью-чеклист
- JWT vs session cookie — плюсы и минусы?
- Как защититься от SQL injection и XSS?
- Зачем rate limiting на login?
- Что тестирует React Testing Library vs Enzyme-style?
- Что делать если JWT secret утёк в git?
