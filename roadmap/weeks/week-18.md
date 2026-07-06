# Неделя 18: SQLAlchemy ORM + FastAPI

> **Цель недели:** построить типобезопасный REST API на Python с ORM и автодокументацией.
> **Литература:** [SQLAlchemy 2.0 ORM](https://docs.sqlalchemy.org/en/20/orm/quickstart.html), [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/), [Pydantic](https://docs.pydantic.dev/latest/)

## День 120 (Пн): SQLAlchemy — модели и сессии

### Теория
- [SQLAlchemy Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html): DeclarativeBase, Mapped, mapped_column
- Engine, SessionLocal, `session.add()`, `commit()`, `refresh()`
- Relationships: `relationship()`, `back_populates`
- [Alembic](https://alembic.sqlalchemy.org/) — миграции (обзор)

### Практика
1. Проект `library-api`, venv, `pip install sqlalchemy psycopg2-binary`
2. Модели `Author`, `Book` с one-to-many
3. `database.py`: engine, SessionLocal, `get_db()` generator
4. Скрипт `init_db.py` — create tables, seed 3 authors, 10 books

**Критерии:**
- [ ] SQLAlchemy 2.0 style (Mapped, mapped_column)
- [ ] relationship двусторонний с back_populates
- [ ] Таблицы создаются в PostgreSQL

### Ловушки
- Забытый `session.commit()` — данные не сохраняются
- Lazy loading вне session — DetachedInstanceError

---

## День 121 (Вт): CRUD через ORM и запросы

### Теория
- `session.get(Model, id)`, `session.scalars(select(...))`
- [SQLAlchemy Select](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html): filter, join, order_by
- Eager loading: `selectinload()` — N+1 problem
- Delete: `session.delete(obj)`

### Практика
1. CRUD функции: `create_author`, `get_authors`, `update_book`, `delete_book`
2. Запрос: все книги автора с join
3. Пагинация: `limit` + `offset`
4. Замер N+1: без selectinload vs с selectinload

**Критерии:**
- [ ] select() API, не legacy Query (1.x)
- [ ] N+1 продемонстрирован и исправлен
- [ ] Пагинация работает

### Ловушки
- N+1: цикл по authors + author.books внутри — сотни запросов
- `session.query()` — legacy, используй `select()`

---

## День 122 (Ср): FastAPI — первый API

### Теория
- [FastAPI First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- Path params, query params, request body
- [Pydantic models](https://fastapi.tiangolo.com/tutorial/body/) для validation
- Auto docs: `/docs` (Swagger), `/redoc`
- `uvicorn main:app --reload`

### Практика
1. `main.py`: FastAPI app, `GET /health`
2. In-memory CRUD для `Note` (id, title, body) — без БД пока
3. Pydantic: `NoteCreate`, `NoteRead`, `NoteUpdate`
4. Проверь Swagger UI — все endpoints документированы

**Критерии:**
- [ ] 422 при невалидном body
- [ ] Response model отделён от create model
- [ ] `uvicorn --reload` работает

### Ловушки
- Mutable default list в Pydantic v1 style — в v2 используй `Field(default_factory=list)`
- Возврат ORM object без `response_model` — утечка внутренних полей

---

## День 123 (Чт): Dependency Injection и подключение БД

### Теория
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- `Depends(get_db)` — сессия на запрос, yield + finally close
- HTTPException: 404, 400, 409
- Status codes: [HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

### Практика
1. Подключи SQLAlchemy к FastAPI через Depends
2. `GET /authors`, `POST /authors`, `GET /authors/{id}`
3. 404 если author не найден
4. `GET /authors/{id}/books` — nested resource

**Критерии:**
- [ ] DB session закрывается после каждого request
- [ ] HTTPException с detail message
- [ ] Endpoints покрывают CRUD authors

### Ловушки
- Глобальная session — race conditions и утечки
- 200 на DELETE несуществующего — должен быть 404

---

## День 124 (Пт): Полный REST API «Библиотека»

### Теория
- REST conventions: nouns, HTTP verbs, idempotency
- [FastAPI Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/) — APIRouter
- Pagination response: `{ items, total, page, size }`
- Filtering query params: `?status=active`

### Практика
1. Роутеры: `authors.py`, `books.py`, `loans.py`
2. CRUD для books и loans
3. `POST /loans` — проверка: книга доступна?
4. `GET /books?author_id=1&search=python`

**Критерии:**
- [ ] APIRouter + prefix `/api/v1`
- [ ] Бизнес-правило: нельзя выдать уже выданную книгу → 409
- [ ] Swagger актуален

### Ловушки
- Глаголы в URL: `/getAuthors` — не REST
- Отсутствие валидации foreign key — 500 вместо 404

---

## День 125 (Сб): Тестирование API и обработка ошибок

### Теория
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/): `TestClient`, pytest
- Test database (SQLite in-memory или отдельная PG)
- Global exception handlers
- CORS middleware (обзор для недели 21)

### Практика
1. `pip install pytest httpx`
2. Тесты: create author, get 404, create loan conflict
3. `conftest.py` — fixture test client + test db
4. Exception handler для SQLAlchemy IntegrityError → 409

**Критерии:**
- [ ] ≥ 5 pytest тестов, все проходят
- [ ] Test DB изолирована от dev
- [ ] `pytest -v` в README

### Ловушки
- Тесты на production DB — никогда
- Забытый rollback после теста — грязные данные

---

## День 126 (Вс): Ревью и документация API

### Теория
- OpenAPI schema — что генерирует FastAPI
- Versioning API: `/api/v1`
- [12 Factor App](https://12factor.net/config) — config через env

### Практика
1. README: архитектура, запуск, env vars, примеры curl
2. `.env.example`: `DATABASE_URL`
3. Postman collection (export JSON)

**Критерии:**
- [ ] curl примеры для всех основных endpoints
- [ ] Структура проекта понятна
- [ ] `docker run postgres` документирован

---

## Проект недели

**REST API «Библиотека»** — production-ready backend:

1. FastAPI + SQLAlchemy 2.0 + PostgreSQL
2. Authors, Books, Borrowers, Loans — full CRUD
3. Dependency injection, Pydantic schemas, APIRouter
4. Seed script, pytest (≥ 8 тестов)
5. Swagger `/docs`, README, `.env.example`

**Критерии:**
- [ ] Данные в PostgreSQL, не in-memory
- [ ] Foreign keys и бизнес-правила займов
- [ ] 404/409/422 обработаны корректно
- [ ] Все тесты зелёные

## Ревью-чеклист
- Чем ORM отличается от raw SQL? Плюсы и минусы?
- Что такое N+1 и как исправить в SQLAlchemy?
- Зачем Pydantic models отдельно от ORM models?
- Как работает Depends(get_db)?
- Что такое idempotent HTTP method? Примеры.
