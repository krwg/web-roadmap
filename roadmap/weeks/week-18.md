# Неделя 18: SQLAlchemy ORM + FastAPI

> **Цель недели:** построить типобезопасный REST API на Python с ORM и автодокументацией.
> **Литература:** [SQLAlchemy 2.0 ORM](https://docs.sqlalchemy.org/en/20/orm/quickstart.html), [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/), [Pydantic](https://docs.pydantic.dev/latest/)
> **Проект недели:** [Library REST API](../../docs/projects.md#неделя-18--library-rest-api) — FastAPI + SQLAlchemy, full CRUD, pytest ≥ 8, Swagger.
> **Git:** папка `learning-log/week-18/`, feature-ветки по роутерам; тег `week-18-done`.

## День 120 (Пн): SQLAlchemy — модели и сессии

### Теория
- [SQLAlchemy Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html): DeclarativeBase, `Mapped`, `mapped_column` — SQLAlchemy 2.0 style
- Engine — подключение к БД; SessionLocal — фабрика сессий; сессия = unit of work
- `session.add()`, `commit()`, `refresh()` — жизненный цикл объекта в БД
- `relationship()` + `back_populates` — двусторонняя связь без ручных JOIN в каждом запросе
- [Alembic](https://alembic.sqlalchemy.org/) — версионирование схемы (обзор, полная настройка позже)
- Отличие ORM model от Pydantic schema — внутреннее представление vs API-контракт

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
- `session.get(Model, id)` — primary key lookup O(1) с кешем identity map
- [SQLAlchemy Select](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html): `select()`, `where()`, `join()`, `order_by()`
- `session.scalars(select(...)).all()` — список ORM-объектов
- Eager loading: `selectinload()`, `joinedload()` — решение N+1 problem
- `session.delete(obj)` + commit — удаление с учётом cascade
- Пагинация: `limit` + `offset` — для API endpoints

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
- [FastAPI First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) — ASGI, автоматическая валидация
- Path params, query params, request body — три способа входных данных
- [Pydantic models](https://fastapi.tiangolo.com/tutorial/body/) — runtime validation + OpenAPI schema
- Auto docs: `/docs` (Swagger UI), `/redoc` — бесплатная документация API
- `uvicorn main:app --reload` — hot reload в dev
- Response model отделяет внутренние поля ORM от публичного JSON

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
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) — переиспользуемая логика через `Depends`
- `Depends(get_db)` — сессия на один request; yield + finally close
- `HTTPException(status_code=404, detail="...")` — контролируемые ошибки
- Status codes: 200 OK, 201 Created, 204 No Content, 404, 409 Conflict, 422
- Dependency можно вкладывать — `get_current_user` позже на нед. 20
- Lifespan events — startup/shutdown hooks (обзор)

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
- REST conventions: существительные в URL, HTTP verbs, идемпотентность GET/PUT/DELETE
- [FastAPI Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/) — APIRouter, модульность
- Pagination response: `{ items, total, page, size }` — единый формат
- Filtering: query params `?status=active&search=python`
- Версионирование: `/api/v1/...` — задел на будущие breaking changes
- 409 Conflict — бизнес-правило нарушено (книга уже выдана)

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
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/): `TestClient`, pytest fixtures
- Test database — SQLite in-memory или отдельная PG schema
- `conftest.py` — shared fixtures: client, db session, sample data
- Global exception handlers — `IntegrityError` → 409, generic → 500 без stack trace
- CORS middleware (обзор) — понадобится на нед. 21
- `pytest -v --tb=short` — читаемый вывод

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
- OpenAPI schema — FastAPI генерирует из type hints и Pydantic
- Versioning API: `/api/v1` — стабильный контракт для фронтенда
- [12 Factor App](https://12factor.net/config) — config через env, не hardcode
- Postman / Insomnia — коллекции для ручного тестирования
- Логирование: `logging` module, уровни INFO/DEBUG

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
