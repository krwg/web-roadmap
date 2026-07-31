# Неделя 20: Auth, безопасность, тестирование

> **Цель недели:** реализовать JWT-аутентификацию, изучить OWASP и написать базовые тесты (Vitest + pytest).
> **Литература:** [JWT.io](https://jwt.io/introduction), [OWASP Top 10](https://owasp.org/www-project-top-ten/), [Vitest](https://vitest.dev/), [pytest](https://docs.pytest.org/)
> **Проект недели:** [Secure Notes](../../docs/projects.md#неделя-20--secure-notes) — JWT auth, bcrypt, rate limit, React client, pytest + Vitest.
> **Git:** папка `learning-log/week-20/`, отдельные коммиты backend/frontend; тег `week-20-done`.

## День 134 (Пн): Аутентификация и хеширование паролей
<a id="week-20-day-134"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Secure Notes**

### Теория

Authentication отвечает на вопрос «кто ты?» — проверка личности (логин/пароль). Authorization — «что тебе можно?» — права на ресурсы. Не путай: успешный login не означает доступ ко всем endpoints. Пароли никогда не хранятся в plain text, даже в dev-базе.

bcrypt (Node) и passlib с bcrypt (Python) — adaptive hashing с встроенным salt. Salt rounds 10–12 — баланс безопасность/скорость. При register: validate email → `hash(password, 12)` → store `password_hash`. При login: `compare(plain, hash)`. SHA256 без salt уязвим к rainbow tables.

Registration flow: дубликат email → 409 Conflict. Login: неверный пароль → 401 Unauthorized с generic message «Invalid credentials» — не раскрывай, существует ли email. Пароль не логируй и не возвращай в JSON response.

Ментальная модель: хеш пароля — это цифровой отпечаток, а не сейф с ключом. Ты не «открываешь» hash обратно в пароль — bcrypt при login заново хеширует введённый пароль с тем же salt и сравнивает отпечатки. Это принципиально отличает hashing от encryption, где данные можно расшифровать зная ключ. Для junior backend-роли эта тема — почти гарантированный вопрос на собеседовании: «как ты хранишь пароли?» — и неправильный ответ («шифрую AES») сразу выдаёт незрелость. На практике каждая компания, где есть пользователи, должна закрыть этот вопрос в первый день продакшена.

Классический пример цены ошибки — утечка LinkedIn 2012 года: пароли хранились как unsalted SHA1, и после взлома миллионы паролей были восстановлены за часы перебором по rainbow tables. Частое заблуждение новичков — «добавлю к паролю секретную строку и захеширую SHA256, этого достаточно» — но без cost-фактора (salt rounds) современные GPU перебирают миллиарды SHA256-хешей в секунду, а bcrypt намеренно медленный и настраиваемый. Именно этот механизм регистрации ты сегодня реализуешь в Secure Notes, и тот же код позже переиспользуешь в DevHub capstone (неделя 22, день 151) — прочный фундамент экономит часы отладки в финале роадмапа.

Для продакшена важна и обратная сторона: слишком высокий cost factor (например, 15+ раундов) замедляет login до заметных пользователю секунд и создаёт нагрузку на CPU при пиковой регистрации — поэтому 10–12 раундов остаётся индустриальным стандартом, а не произвольным числом. Держи это в голове при код-ревью чужого auth-кода: cost factor — не «чем больше, тем безопаснее», а сознательный компромисс между защитой и latency бюджетом сервиса.

**Читать:**

- [bcrypt (Node)](https://github.com/kelektiv/node.bcrypt.js)
- [passlib](https://passlib.readthedocs.io/)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

**Ключевая мысль:** hash + salt через bcrypt; одинаковые сообщения об ошибке login — против enumeration.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. Таблица `users(id, email UNIQUE, password_hash, created_at)`
2. Express: `POST /auth/register`, `POST /auth/login`
3. `bcrypt.hash(password, 12)` при register, `bcrypt.compare()` при login

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Запутался в структуре файлов — нарисуй дерево папок на бумаге, потом создай пустые файлы и заполни по одному.

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 134: register login bcrypt"`

### Ловушки
- SHA256 без salt для паролей — уязвимо к rainbow tables
- Разные сообщения для «user not found» и «wrong password» — information leak

---

## День 135 (Вт): JWT — выдача и проверка токенов
<a id="week-20-day-135"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Secure Notes**

### Теория

JWT (JSON Web Token) — компактный способ передавать claims между клиентом и сервером. Структура: header.payload.signature. Подпись (HMAC SHA256) гарантирует целостность; payload base64-decodable — не клади пароли и PII. Стандарт передачи: `Authorization: Bearer <token>`.

Access token TTL 15min–1h; refresh token — отдельный долгоживущий механизм (обзор). `JWT_SECRET` в `.env` — минимум 32 случайных байта; при утечке — rotate немедленно. Payload: `sub` (user id), `exp`, `iat`. Явно указывай `algorithm: 'HS256'` — алгоритм `none` — уязвимость.

Middleware `authenticateToken` verify JWT и кладёт `req.user = { id, email }`. Protected routes читают `user_id` из token, не из body/query — иначе IDOR. Expired token → 401. Тест с TTL 1 секунда проверяет expiration.

Ментальная модель: JWT — это подписанная справка, а не запечатанный конверт. Любой может прочитать payload через base64-decode (проверь на jwt.io), но подделать подпись без секрета невозможно — поэтому в payload никогда не кладут пароли, номера карт или другие секреты, только неконфиденциальные claims вроде user id и роли. На собеседованиях junior-разработчиков часто путают JWT с session cookie: JWT stateless (сервер ничего не хранит, просто проверяет подпись), а session требует хранилища на сервере — эта разница определяет, как система масштабируется горизонтально.

Конкретный пример уязвимости: если backend принимает `algorithm: none` или не проверяет alg вообще, атакующий может подделать токен с любым payload и получить admin-доступ — это реальная категория уязвимостей, встречавшаяся в популярных JWT-библиотеках. Частое заблуждение — «раз токен подписан, значит зашифрован и безопасен для любых данных» — на деле подпись гарантирует только целостность, не конфиденциальность. Middleware, который ты пишешь сегодня, — это тот же паттерн защищённых маршрутов, который в неделе 22 (день 151) масштабируется на весь DevHub: `req.user` из verified JWT, а не из тела запроса, закрывает целый класс IDOR-уязвимостей.

Для продакшена короткий TTL access token (15 минут–1 час) — не паранойя, а ограничение окна атаки: если токен украли через XSS или перехват трафика, он бесполезен уже через час. Полноценный refresh-token механизм с ротацией — тема отдельного, более продвинутого модуля, но важно понимать саму идею уже сейчас: access token — расходный материал, а не постоянный пропуск, который выдаётся один раз и живёт вечно.

**Читать:**

- [JWT Introduction](https://jwt.io/introduction)
- [jsonwebtoken](https://github.com/auth0/node-jsonwebtoken)
- [python-jose](https://python-jose.readthedocs.io/)

**Ключевая мысль:** JWT — подписанный контракт, не шифрование; user_id только из verified token.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. Login возвращает `{ access_token, token_type: "bearer", expires_in }`
2. Middleware `authenticateToken` — verify JWT, `req.user = { id, email }`
3. Protected: `GET /api/notes` только с valid token

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Застрял >20 мин — выпиши вход/выход задачи в 3 строки. Сделай минимальный пример в `playground.*`, без копипаста из ИИ.

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 135: JWT middleware and protected routes"`

### Ловушки
- Алгоритм `none` — всегда указывай algorithm explicitly
- Sensitive data в JWT payload — payload base64-decodable

---

## День 136 (Ср): OWASP Top 10 — практическая защита
<a id="week-20-day-136"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Secure Notes**

### Теория

OWASP Top 10 — карта самых частых уязвимостей веб-приложений. Ты уже закрываешь injection parameterized queries (нед. 17–19). Broken authentication — слабые пароли, утечка session. XSS — неэкранированный user-generated HTML; escape output, DOMPurify для rich text.

Helmet.js выставляет security headers: `X-Content-Type-Options`, `X-Frame-Options`, CSP basics. `express-rate-limit` на `/auth/login`: 5 попыток / 15 мин per IP → 429 Too Many Requests — защита от brute-force. CORS: явный whitelist origins; `origin: '*'` с credentials — небезопасно.

Аудит: `.env` в `.gitignore`, `.env.example` без секретов, проверь `git log` на утечки. `security-audit.md` с чеклистом 10 пунктов — deliverable недели. CORS в dev: allow только `http://localhost:5173`.

Ментальная модель — думай про безопасность как про слоёный пирог (defense in depth): ни один слой не идеален сам по себе, но вместе hash + JWT + rate limit + headers + CORS перекрывают друг друга. Для junior-позиции знание OWASP Top 10 — не академическое упражнение, а практический чеклист, который спрашивают на security-ориентированных собеседованиях и которым реально пользуются на code review в компаниях с compliance-требованиями (SOC2, PCI DSS).

Конкретный пример: без rate limit на `/auth/login` атакующий может перебрать пароли скриптом за секунды — 5 попыток / 15 минут превращают brute-force в непрактичную атаку. Частое заблуждение начинающих — «у меня маленький pet-проект, кому он нужен» — но боты сканируют весь интернет автоматически, а не выбирают жертву вручную; открытый `.env` в публичном репозитории находят за минуты. Чеклист `security-audit.md`, который ты заполняешь сегодня, — прямой прообраз `SECURITY.md` в DevHub capstone (неделя 22): те же 10 пунктов OWASP, но уже против реального multi-user приложения с репутацией на кону.

Для продакшена CORS — не разовая настройка, а живой список, который меняется с каждым новым окружением: dev допускает `localhost:5173`, staging — свой домен, прод — финальный домен фронтенда. Забытая запись в whitelist после деплоя — одна из самых частых причин, почему «API работает в Postman, но не в браузере»: curl и Postman не проверяют CORS вообще, эту проверку делает только браузер, поэтому баг обнаруживается лишь при реальном использовании интерфейса. Держи чеклист OWASP под рукой не как разовое упражнение, а как привычку code review для каждого нового endpoint.

**Читать:**

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Helmet.js](https://helmetjs.github.io/)
- [express-rate-limit](https://github.com/express-rate-limit/express-rate-limit)

**Ключевая мысль:** безопасность — слои: hash, JWT, rate limit, headers, CORS, audit.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. Rate limit на `/auth/login`: 5 попыток / 15 мин per IP
2. `helmet()` в Express; FastAPI — security headers middleware (обзор)
3. Аудит API: чеклист OWASP 10 пунктов → `security-audit.md`

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Устал — сделай коммит текущего прогресса с честным сообщением `wip:` и паузу 10 минут. Не геройствуй.

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 136: OWASP audit rate limit helmet"`

### Ловушки
- CORS `origin: '*'` с credentials — небезопасно
- Секреты в git history — rotate keys если утекли

---

## День 137 (Чт): Тестирование backend — pytest
<a id="week-20-day-137"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Secure Notes**

### Теория

Backend-тесты ловят регрессии в auth и authorization. pytest + FastAPI TestClient или supertest для Express — HTTP без реального порта. Fixtures: `create_user()`, `auth_headers(token)`. Test DB изолирована: отдельная schema или rollback per test — никогда production.

Arrange-Act-Assert в каждом тесте. Покрой: register success, duplicate 409, wrong password 401, protected 401 без token, 200 с token, user A не видит notes user B. `conftest.py` — shared setup. `pytest --cov=app` показывает пробелы.

Тесты не должны зависеть от порядка выполнения. Hardcoded JWT secret в тестах должен совпадать с app config. ≥ 10 тестов — минимум для Secure Notes. Flaky tests из shared DB без cleanup — исправь до merge.

Ментальная модель: тест — это исполняемая спецификация поведения, а не бюрократическая формальность. Arrange-Act-Assert структурирует мышление: подготовь данные, вызови действие, проверь результат — один тест проверяет одну вещь. Для junior-разработчика умение писать тесты на auth и authorization — сигнал зрелости для нанимающего менеджера: код без тестов на security-критичные пути в реальной компании не пройдёт code review.

Конкретный пример пользы: тест «user A не видит notes user B» ловит IDOR-баг ещё до продакшена — без него такая уязвимость обнаруживается только в security-инциденте или пентесте, что стоит репутации и денег. Частое заблуждение новичков — «я протестировал руками через Postman, тестов достаточно» — но ручное тестирование не защищает от регрессий при следующем рефакторинге, а автоматические тесты запускаются на каждый commit. Инфраструктура тестов, которую ты строишь сегодня (fixtures, conftest.py, изоляция БД), — это ровно то, что масштабируется в неделе 22 (день 153) до ≥15 pytest-тестов в CI capstone-проекта.

Для продакшена тесты выполняют вторую важную функцию — они документируют ожидаемое поведение системы точнее, чем любой комментарий в коде: новый разработчик, зашедший в проект, читает тесты, чтобы понять контракт API, а не гадает по названиям функций. `pytest --cov=app` показывает не «сколько строк покрыто», а скорее карту слепых зон — мест, куда никто не заглядывал тестами, и именно там чаще всего прячутся баги, которые всплывают в проде. Читай отчёт покрытия критически: 100% покрытия не гарантирует отсутствие багов, если assertions в тестах слабые, но пробелы в покрытии почти всегда указывают на риск.

**Читать:**

- [pytest](https://docs.pytest.org/en/stable/getting-started.html)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [supertest](https://github.com/ladjs/supertest)

**Ключевая мысль:** тестируй auth, 403 cross-user и 401 без token — не только happy path.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. Тесты auth: register success, duplicate email 409, login, wrong password 401
2. Fixture: test user + valid token в `Authorization` header
3. Protected route: 401 без token, 200 с token

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Документация не клеится — найди один официальный пример (MDN / docs) и сопоставь 1:1 со своим кодом.

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 137: pytest auth and notes tests"`

### Ловушки
- Тесты на shared DB без cleanup — flaky tests
- Hardcoded JWT secret в тестах отличается от app — 401 везде

---

## День 138 (Пт): Тестирование frontend — Vitest
<a id="week-20-day-138"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Secure Notes**

### Теория

Vitest — test runner, нативный для Vite-проектов, API совместим с Jest. React Testing Library (RTL) тестирует поведение с точки зрения пользователя: `getByRole`, `getByLabelText`, не `getByClassName`. `userEvent` симулирует реальные клики и ввод с клавиатуры.

Mock `fetch` через `vi.fn()` или `global.fetch = vi.fn().mockResolvedValue(...)` изолирует компоненты от API. Тестируй: Login submit шлёт credentials, ProtectedRoute редиректит без token, NotesList рендерит mock data, login 401 показывает ошибку. `vi.mock()` для модулей.

≥ 8 component tests. `vitest run` в CI. Тестирование internal state вместо visible behavior — хрупкие тесты. Cleanup mocks в `afterEach` — иначе тесты влияют друг на друга.

Ментальная модель React Testing Library — «тестируй как пользователь, а не как разработчик»: пользователь не знает про internal state или имена CSS-классов, он видит кнопки, лейблы и текст на экране. Поэтому `getByRole` и `getByLabelText` устойчивее к рефакторингу компонента, чем `getByClassName` или проверка state напрямую. Для junior frontend-позиции это стандарт индустрии — большинство современных React-команд требуют RTL-подход в тестах.

Конкретный пример: если ты тестируешь `wrapper.state.isLoggedIn === true` вместо того, что видно на экране («Welcome» текст появился), рефакторинг компонента с useState на useReducer сломает тест, хотя поведение для пользователя не изменилось — это и есть хрупкий тест. Частое заблуждение — «чем больше моков, тем лучше изолирован тест» — избыточный mocking скрывает реальные баги интеграции; мокай только внешние границы (fetch, роутер), а не внутреннюю логику компонента. Компонентные тесты Login/ProtectedRoute/NotesList, которые ты пишешь сегодня, — прямой шаблон для тестов TaskList и NoteEditor в DevHub capstone (неделя 22, день 153), где потребуется уже ≥12 таких тестов.

Для продакшена связка Vitest + RTL особенно ценна на команде из нескольких frontend-разработчиков: когда кто-то меняет структуру JSX компонента ради рефакторинга, тесты, написанные через `getByRole`, продолжают проходить, а тесты через `querySelector('.btn-submit')` ломаются от простого переименования CSS-класса — разница напрямую влияет на то, сколько времени команда тратит на «починку зелёных тестов» после каждого рефакторинга вместо реальной разработки функциональности. Именно поэтому RTL стала де-факто стандартом тестирования React-компонентов в индустрии, а не просто одной из многих альтернатив — это первое, что спросят про фронтенд-тестирование на техническом собеседовании junior-разработчика.

**Читать:**

- [Vitest](https://vitest.dev/guide/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [userEvent](https://testing-library.com/docs/user-event/intro/)

**Ключевая мысль:** RTL — «как пользователь видит»; mock fetch, не implementation details.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. `npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom @testing-library/user-event`
2. Тест: Login form — submit вызывает API с email/password
3. Тест: Protected route redirect на `/login` без token

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Не понимаешь ошибку — прочитай её с конца: файл, строка, тип. Открой DevTools / терминал и воспроизведи на 5 строках кода.

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 138: Vitest auth and notes components"`

### Ловушки
- Тестирование state вместо behavior — хрупкие тесты
- Забытый mock cleanup — тесты влияют друг на друга

---

## День 139 (Сб): Интеграция auth frontend + backend
<a id="week-20-day-139"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Secure Notes**

### Теория

Full-stack auth связывает JWT backend с React frontend. Token storage: localStorage прост, но уязвим к XSS; httpOnly cookie безопаснее, сложнее с CORS. Для учебного проекта localStorage + CSP + sanitize input — приемлемо; задокументируй trade-off в README.

`AuthContext`: `user`, `token`, `login`, `logout`, `isLoading`. `api.ts` wrapper подставляет `Authorization: Bearer` и на 401 очищает token + redirect `/login`. React Router `<ProtectedRoute>` оборачивает private pages. Token не в URL query string — утечёт в logs и history.

Full flow: register → login → create note → logout → login → note visible. User A не видит notes User B — проверь вручную и тестами. Axios interceptors или fetch wrapper — один вход для всех API calls.

Ментальная модель: думай о `AuthContext` как о единственном источнике правды про личность пользователя во всём React-дереве — компоненты не хранят свою копию token, а читают из контекста через `useAuth()`. Это устраняет рассинхронизацию состояния, когда один компонент думает, что пользователь залогинен, а другой — нет. Для реальной работы junior full-stack разработчика это один из первых архитектурных паттернов, который придётся освоить: почти любое SPA с авторизацией использует похожую структуру (Context/Redux/Zustand + protected routes).

Конкретный пример проблемы без единого api-wrapper: если каждый компонент делает свой fetch и сам добавляет заголовок, то при истечении токена придётся чинить логику логаута в десятке мест — а с interceptor это одна точка изменения. Частое заблуждение — «localStorage полностью безопасен для токенов» — на деле любой XSS на странице получает доступ к localStorage через `localStorage.getItem`, поэтому в проде банки и финтех используют httpOnly cookie; для учебного проекта localStorage допустим при условии осознанного trade-off, задокументированного в README. Этот же auth flow — Context, api wrapper, protected routes — ты соберёшь заново, но уже с нуля, в DevHub capstone (неделя 22, день 151), так что качество кода сегодня напрямую экономит время через две недели.

Для продакшена полезно явно проговорить trade-off хранения токена в коде и в README: это показывает ревьюеру портфолио, что решение осознанное, а не «забыл подумать про безопасность». Многие junior-кандидаты либо вообще не упоминают эту тему, либо копируют случайный код без понимания — а один абзац в README о том, почему выбран localStorage и какие меры снижают риск (CSP, sanitize, короткий TTL), выделяет проект среди типовых учебных.

**Читать:**

- [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [React Router — Tutorial](https://reactrouter.com/6.28.0/start/tutorial)
- [MDN — HTTP Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication)

**Ключевая мысль:** auth flow end-to-end — контракт между Context, api wrapper и protected routes.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. React (Vite + TS): Login/Register pages с валидацией форм
2. `AuthContext` + `useAuth()` hook
3. `api.ts` wrapper — подставляет Bearer token, обрабатывает 401

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Тесты/валидация красные — сначала один failing case, почини его, только потом следующий.

### Git
- Закоммить изменения дня: `git add week-20/` → `git commit -m "week 20 day 139: React auth integration"`

### Ловушки
- XSS + localStorage token — кража token (mitigate: CSP, sanitize input)
- Token без expiration check на клиенте — плохой UX при expired

---

## День 140 (Вс): Ревью безопасности и CI
<a id="week-20-day-140"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Secure Notes**

### Теория

CI автоматизирует проверку качества на каждый push. GitHub Actions: matrix jobs для backend (`pytest`) и frontend (`vitest run`). Зелёный CI — сигнал, что main mergeable. Branch protection с require CI — best practice для команд (обзор).

`npm audit` и `pip audit` сканируют known vulnerabilities в зависимостях. Critical без комментария или плана фикса — красный флаг для портфолио. Semgrep — static analysis (обзор). Sequence diagram auth flow в README объясняет архитектуру ревьюеру.

Финальный security review по OWASP чеклисту. Обнови `.env.example` для backend и frontend. Smoke test checklist в README. Тег `week-20-done` — Secure Notes готов как шаблон для недель 21–22.

Ментальная модель: CI — это автоматический привратник качества, который проверяет код за тебя каждый раз, когда ты забываешь. Зелёный чек на GitHub — не формальность для галочки, а сигнал команде (или ревьюеру портфолио), что код прошёл минимальную планку: тесты, линтер, security-скан. Для junior-кандидата наличие рабочего CI pipeline в pet-проекте на GitHub — заметный плюс: рекрутеры и техлиды буквально открывают вкладку Actions, чтобы увидеть зелёную галочку до того, как откроют код.

Конкретный пример пользы: `npm audit` может найти критическую уязвимость в транзитивной зависимости, о существовании которой ты даже не знал — типичный кейс cascading vulnerability в node_modules. Частое заблуждение — «раз мой код написан безопасно, зависимости не важны» — но большая часть реальных production-инцидентов происходит именно через уязвимые библиотеки третьих сторон, а не собственный код. Workflow `ci.yml`, который ты пишешь сегодня, — это шаблон, который в неделе 21 расширится healthcheck-ами для Docker, а в неделе 22 (день 153) вырастет до полноценного pipeline с postgres service и двумя параллельными job — тег `week-20-done` фиксирует рабочую точку отсчёта для этого пути.

Для продакшена архитектурные решения без документации быстро забываются: через месяц ты сам не вспомнишь, почему выбран именно такой TTL токена или почему rate limit настроен на 5, а не на 10 попыток. Sequence diagram auth flow в README — не украшение, а инструмент передачи знаний будущему тебе или коллеге, который придёт поддерживать проект и не должен реверс-инжинирить логику по коду построчно.

**Читать:**

- [GitHub Actions](https://docs.github.com/en/actions)
- [npm audit](https://docs.npmjs.com/cli/v10/commands/npm-audit)
- [pip-audit](https://pypi.org/project/pip-audit/)

**Ключевая мысль:** CI + security audit — часть Definition of Done, не «после деплоя».

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. `.github/workflows/ci.yml`: `pytest` + `vitest run` на push
2. `npm audit` и `pip audit` — отчёт в `security-audit.md`
3. Документируй auth flow: sequence diagram в README

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Устал — сделай коммит текущего прогресса с честным сообщением `wip:` и паузу 10 минут. Не геройствуй.

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


## Проверь себя

<details>
<summary>Что должно получиться к концу недели?</summary>

Работающий проект **Secure Notes** в `learning-log/week-20/`, осмысленная Git-история, тег `week-20-done`.

</details>

<details>
<summary>Главный навык недели одной фразой?</summary>

JWT auth, безопасность, тесты

</details>

<details>
<summary>Можно ли пропустить день?</summary>

Нет — дни связаны. В **лайт-режиме** сократи практику до MVP, но теорию и Git-коммит не пропускай.

</details>
