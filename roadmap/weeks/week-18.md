# Неделя 18: SQLAlchemy ORM + FastAPI

> **Цель недели:** построить типобезопасный REST API на Python с ORM и автодокументацией.
> **Литература:** [SQLAlchemy 2.0 ORM](https://docs.sqlalchemy.org/en/20/orm/quickstart.html), [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/), [Pydantic](https://docs.pydantic.dev/latest/)
> **Проект недели:** [Library REST API](../../docs/projects.md#неделя-18--library-rest-api) — FastAPI + SQLAlchemy, full CRUD, pytest ≥ 8, Swagger.
> **Git:** папка `learning-log/week-18/`, feature-ветки по роутерам; тег `week-18-done`.

## День 120 (Пн): SQLAlchemy — модели и сессии

### Теория

SQLAlchemy 2.0 — современный ORM для Python. DeclarativeBase, `Mapped[type]` и `mapped_column()` задают модели типобезопасно. Engine — подключение к PostgreSQL; SessionLocal — фабрика сессий. Сессия — unit of work: `session.add(obj)`, `commit()`, `refresh(obj)` для актуализации из БД.

`relationship()` с `back_populates` связывает `Author` и `Book` двусторонне без ручных JOIN в каждом запросе. ORM model (`Author` в `models/`) — внутреннее представление; Pydantic schema (`AuthorRead`) — контракт API. Не смешивай их: утечёт `password_hash` в JSON.

`get_db()` generator с `yield` и `finally: session.close()` — паттерн для FastAPI. Alembic версионирует схему (обзор); на этой неделе достаточно `create_all` + seed. Забытый `commit()` — данные «исчезают» после перезапуска.

**Читать:**

- [SQLAlchemy 2.0 Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)
- [Alembic](https://alembic.sqlalchemy.org/)

**Ключевая мысль:** ORM model ≠ API schema; сессия — граница транзакции.

### Практика
1. Проект `library-api`, venv, `pip install sqlalchemy psycopg2-binary python-dotenv`
2. Модели `Author`, `Book` с one-to-many relationship
3. `database.py`: engine, SessionLocal, `get_db()` generator с yield
4. `init_db.py` — create tables, seed 3 authors, 10 books
5. Проверь таблицы в psql/DBeaver после init
6. `models/__init__.py` — чистая структура пакета

**Критерии:**
- [ ] SQLAlchemy 2.0 style (Mapped, mapped_column)
- [ ] relationship двусторонний с back_populates
- [ ] Таблицы создаются в PostgreSQL

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 120: SQLAlchemy models and init_db"`

### Ловушки
- Забытый `session.commit()` — данные не сохраняются
- Lazy loading вне session — DetachedInstanceError

---

## День 121 (Вт): CRUD через ORM и запросы

### Теория

CRUD через ORM использует SQLAlchemy 2.0 style `select()`, не legacy `session.query()`. `session.get(Model, id)` — lookup по primary key с identity map cache. `session.scalars(select(Book).where(...)).all()` возвращает список ORM-объектов. Фильтры: `.where()`, `.join()`, `.order_by()`, `.limit()`, `.offset()` для пагинации.

N+1 problem: цикл по авторам + `author.books` внутри генерирует запрос на каждую итерацию. Решение — eager loading: `selectinload(Author.books)` или `joinedload`. Замерь количество SQL-запросов до и после — наглядный урок.

`session.delete(obj)` + `commit()` удаляет с учётом cascade rules. Пагинация `page=1, size=20` — обязательна для API endpoints. Вынеси CRUD в `crud/authors.py` — routes остаются тонкими. `title.ilike('%python%')` — case-insensitive поиск в PostgreSQL.

**Читать:**

- [SQLAlchemy Select](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html)
- [Loading Relationships](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)
- [N+1 problem (обзор)](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#selectin-loading)

**Ключевая мысль:** N+1 лечится eager loading; `select()` API — стандарт SQLAlchemy 2.0.

### Практика
1. CRUD: `create_author`, `get_authors`, `update_book`, `delete_book`
2. Запрос: все книги автора с join через relationship или explicit join
3. Пагинация: `get_books(page=1, size=20)`
4. Замер N+1: цикл authors без selectinload vs с selectinload — считай запросы
5. Фильтр: книги где `title.ilike('%python%')`
6. Вынеси CRUD в `crud/authors.py`, `crud/books.py`

**Критерии:**
- [ ] select() API, не legacy Query (1.x)
- [ ] N+1 продемонстрирован и исправлен
- [ ] Пагинация работает

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 121: ORM CRUD and N+1 fix"`

### Ловушки
- N+1: цикл по authors + author.books внутри — сотни запросов
- `session.query()` — legacy, используй `select()`

---

## День 122 (Ср): FastAPI — первый API

### Теория

FastAPI — ASGI-фреймворк с автоматической валидацией из type hints. Path params (`/notes/{id}`), query params (`?skip=0`), request body (Pydantic model) — три входа данных. Pydantic проверяет типы в runtime и генерирует OpenAPI schema для Swagger.

`uvicorn main:app --reload` — dev-сервер с hot reload. `/docs` (Swagger UI) и `/redoc` — бесплатная интерактивная документация. `response_model=NoteRead` отсекает внутренние поля ORM от публичного JSON. Невалидный body → 422 Unprocessable Entity с деталями ошибок.

Начни с in-memory CRUD для `Note` — отдели изучение FastAPI от SQLAlchemy. `NoteCreate`, `NoteRead`, `NoteUpdate` (optional fields) — три схемы для разных операций. Mutable default в Pydantic: `Field(default_factory=list)`, не `tags=[]`.

**Читать:**

- [FastAPI First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [Pydantic Models](https://fastapi.tiangolo.com/tutorial/body/)

**Ключевая мысль:** type hints + Pydantic = валидация и docs из коробки; response_model защищает API.

### Практика
1. `main.py`: FastAPI app, `GET /health` → `{"status": "ok"}`
2. In-memory CRUD для `Note` (id, title, body) — без БД пока
3. Pydantic: `NoteCreate`, `NoteRead`, `NoteUpdate` (все поля optional)
4. Проверь Swagger UI — все endpoints с примерами
5. Отправь невалидный body — убедись в 422 Unprocessable Entity
6. Настрой `pyproject.toml` или `requirements.txt` с версиями

**Критерии:**
- [ ] 422 при невалидном body
- [ ] Response model отделён от create model
- [ ] `uvicorn --reload` работает

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 122: FastAPI in-memory notes API"`

### Ловушки
- Mutable default list в Pydantic — `Field(default_factory=list)`
- Возврат ORM object без `response_model` — утечка внутренних полей

---

## День 123 (Чт): Dependency Injection и подключение БД

### Теория

Dependency Injection в FastAPI — через `Depends`. `get_db()` с `yield` создаёт сессию на один request и закрывает в `finally` — не используй глобальную session (race conditions). `Depends(get_db)` в параметрах endpoint автоматически резолвит зависимость.

`HTTPException(status_code=404, detail="Author not found")` — контролируемые ошибки вместо 500. Семантика статусов: 200 OK, 201 Created, 204 No Content, 404 Not Found, 409 Conflict, 422 Validation Error. Вложенные dependencies (`get_current_user` на нед. 20) строят цепочку проверок.

Pydantic schemas `AuthorCreate` / `AuthorRead` отделяют вход и выход. Nested resource `GET /authors/{id}/books` — RESTful вложенность. Lifespan events (startup/shutdown) — для инициализации пула и закрытия соединений (обзор).

**Читать:**

- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [HTTPException](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Status Codes](https://fastapi.tiangolo.com/tutorial/response-status-code/)

**Ключевая мысль:** одна DB session на request через Depends; HTTPException — явные ошибки API.

### Практика
1. Подключи SQLAlchemy к FastAPI через `Depends(get_db)`
2. `GET /authors`, `POST /authors`, `GET /authors/{id}`
3. 404 если author не найден — `HTTPException`
4. `GET /authors/{id}/books` — nested resource
5. Pydantic schemas: `AuthorCreate`, `AuthorRead`, `BookRead`
6. Проверь в Swagger: create → get by id → list books

**Критерии:**
- [ ] DB session закрывается после каждого request
- [ ] HTTPException с detail message
- [ ] Endpoints покрывают CRUD authors

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 123: FastAPI DI and authors endpoints"`

### Ловушки
- Глобальная session — race conditions и утечки
- 200 на DELETE несуществующего — должен быть 404

---

## День 124 (Пт): Полный REST API «Библиотека»

### Теория

REST — соглашения, не протокол. URL — существительные (`/books`), HTTP verbs — действия (GET читать, POST создать, PUT/PATCH обновить, DELETE удалить). GET, PUT, DELETE идемпотентны: повторный запрос даёт тот же эффект. POST — нет (каждый создаёт новый ресурс).

`APIRouter` модульно группирует endpoints: `routers/authors.py`, prefix `/api/v1`, tags для Swagger. Пагинация в едином формате: `{ items, total, page, size }`. Фильтрация через query: `?status=active&search=python`. Версионирование `/api/v1` защищает фронтенд от breaking changes.

Бизнес-правила в API: нельзя выдать уже выданную книгу → 409 Conflict, не 500. Глаголы в URL (`/getAuthors`) — антипаттерн. Отсутствие валидации FK — 500 вместо понятного 404.

**Читать:**

- [FastAPI Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

**Ключевая мысль:** REST = ресурсы + HTTP semantics; 409 для нарушения бизнес-правил.

### Практика
1. Роутеры: `routers/authors.py`, `books.py`, `loans.py`
2. CRUD для books и loans с Pydantic validation
3. `POST /loans` — проверка: книга доступна? иначе 409
4. `GET /books?author_id=1&search=python` — фильтрация
5. Подключи роутеры в `main.py` с prefix `/api/v1`
6. Обнови Swagger — все endpoints сгруппированы по тегам

**Критерии:**
- [ ] APIRouter + prefix `/api/v1`
- [ ] Бизнес-правило: нельзя выдать уже выданную книгу → 409
- [ ] Swagger актуален

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 124: full library REST routers"`

### Ловушки
- Глаголы в URL: `/getAuthors` — не REST
- Отсутствие валидации foreign key — 500 вместо 404

---

## День 125 (Сб): Тестирование API и обработка ошибок

### Теория

Тестирование API — страховка от регрессий. FastAPI `TestClient` (на базе httpx) шлёт запросы без реального сетевого сервера. pytest fixtures в `conftest.py`: client, db session, sample data. Test DB — отдельная schema или SQLite in-memory; никогда production.

Arrange-Act-Assert: подготовь данные, выполни запрос, проверь status и body. Тесты: create author 201, get missing 404, loan conflict 409. `pytest -v --tb=short` — читаемый вывод. Rollback после каждого теста — иначе flaky tests.

Global exception handlers: `IntegrityError` → 409, generic → 500 без stack trace в production. CORS middleware понадобится на нед. 21. Coverage `pytest --cov=app` показывает пробелы. ≥ 8 тестов — минимум для уверенности в CRUD и ошибках.

**Читать:**

- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest](https://docs.pytest.org/en/stable/getting-started.html)
- [httpx](https://www.python-httpx.org/)

**Ключевая мысль:** изолированная test DB; тесты на auth, 404, 409 — не только happy path.

### Практика
1. `pip install pytest httpx`
2. Тесты: create author, get 404, create loan conflict → 409
3. `conftest.py` — fixture test client + test db (rollback после теста)
4. Exception handler для SQLAlchemy `IntegrityError`
5. Тест пагинации и фильтрации books
6. Добавь `pytest` в README и CI-заготовку

**Критерии:**
- [ ] ≥ 8 pytest тестов, все проходят
- [ ] Test DB изолирована от dev
- [ ] `pytest -v` в README

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 125: pytest suite and error handlers"`

### Ловушки
- Тесты на production DB — никогда
- Забытый rollback после теста — flaky tests

---

## День 126 (Вс): Ревью и документация API

### Теория

OpenAPI schema FastAPI генерирует из type hints и Pydantic — docs всегда синхронны с кодом, если ты дисциплинирован. README capstone-уровня: архитектура слоёв (routes → crud → models → db), env vars, curl-примеры, запуск postgres через docker. Postman collection — ручное тестирование для демо.

12 Factor App: config через environment, не hardcode. `.env.example` без секретов. Mermaid-диаграмма слоёв в README помогает объяснить проект за 2 минуты. Логирование через `logging` module: INFO в production, DEBUG в dev.

Финальный прогон: `pytest`, `uvicorn`, ручная проверка Swagger. Library REST API — шаблон для Express на нед. 19 и DevHub на нед. 22. Тег `week-18-done` завершает первый production-like Python backend.

**Читать:**

- [OpenAPI](https://fastapi.tiangolo.com/features/#automatic-docs)
- [12 Factor App](https://12factor.net/config)
- [Mermaid](https://mermaid.js.org/)

**Ключевая мысль:** документация API — часть deliverable; OpenAPI из кода, не из Word.

### Практика
1. README: архитектура, запуск, env vars, примеры curl
2. `.env.example`: `DATABASE_URL`, `APP_ENV=development`
3. Export Postman collection JSON в `docs/postman/`
4. Mermaid-диаграмма слоёв: routes → crud → models → db
5. curl-примеры для всех основных endpoints в README
6. Финальный прогон: `pytest`, `uvicorn`, Swagger manual check

**Критерии:**
- [ ] curl примеры для всех основных endpoints
- [ ] Структура проекта понятна новому разработчику
- [ ] `docker run postgres` документирован

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 126: API docs and Postman collection"`
- Поставь тег: `git tag week-18-done`

---

## Проект недели

**REST API «Библиотека»** — production-ready Python backend. Спецификация: [docs/projects.md — неделя 18](../../docs/projects.md#неделя-18--library-rest-api).

### Стек и структура

```
week-18/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── crud/
│   └── routers/
├── tests/
│   └── conftest.py
├── requirements.txt
├── .env.example
└── README.md
```

### Функции

1. FastAPI + SQLAlchemy 2.0 + PostgreSQL
2. Authors, Books, Borrowers, Loans — full CRUD
3. Dependency injection, Pydantic schemas, APIRouter
4. Seed script, pytest (≥ 8 тестов)
5. Swagger `/docs`, Postman collection, README

### Критерии проекта

- [ ] Данные в PostgreSQL, не in-memory
- [ ] Foreign keys и бизнес-правила займов (409 при конфликте)
- [ ] 404/409/422 обработаны корректно
- [ ] Все тесты зелёные: `pytest -v`
- [ ] OpenAPI `/docs` актуален и совпадает с реализацией
- [ ] README: clone → venv → migrate → seed → run → test
- [ ] Тег `week-18-done`

## Ревью-чеклист
- Чем ORM отличается от raw SQL? Плюсы и минусы?
- Что такое N+1 и как исправить в SQLAlchemy?
- Зачем Pydantic models отдельно от ORM models?
- Как работает Depends(get_db)?
- Что такое idempotent HTTP method? Примеры.
