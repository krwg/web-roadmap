# Неделя 18: SQLAlchemy ORM + FastAPI

> **Цель недели:** построить типобезопасный REST API на Python с ORM и автодокументацией.
> **Литература:** [SQLAlchemy 2.0 ORM](https://docs.sqlalchemy.org/en/20/orm/quickstart.html), [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/), [Pydantic](https://docs.pydantic.dev/latest/)
> **Проект недели:** [Library REST API](../../docs/projects.md#неделя-18--library-rest-api) — FastAPI + SQLAlchemy, full CRUD, pytest ≥ 8, Swagger.
> **Git:** папка `learning-log/week-18/`, feature-ветки по роутерам; тег `week-18-done`.

## День 120 (Пн): SQLAlchemy — модели и сессии
<a id="week-18-day-120"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Library REST API**

### Теория

SQLAlchemy 2.0 — современный ORM для Python. DeclarativeBase, `Mapped[type]` и `mapped_column()` задают модели типобезопасно. Engine — подключение к PostgreSQL; SessionLocal — фабрика сессий. Сессия — unit of work: `session.add(obj)`, `commit()`, `refresh(obj)` для актуализации из БД.

`relationship()` с `back_populates` связывает `Author` и `Book` двусторонне без ручных JOIN в каждом запросе. ORM model (`Author` в `models/`) — внутреннее представление; Pydantic schema (`AuthorRead`) — контракт API. Не смешивай их: утечёт `password_hash` в JSON.

`get_db()` generator с `yield` и `finally: session.close()` — паттерн для FastAPI. Alembic версионирует схему (обзор); на этой неделе достаточно `create_all` + seed. Забытый `commit()` — данные «исчезают» после перезапуска.

Ментальная модель: сессия SQLAlchemy — это «корзина покупок». Ты добавляешь и меняешь объекты (`session.add(book)`, `book.title = '...'`) — они лежат в корзине как черновик, видимый только тебе. Ничего не попадает на «склад» (в таблицы БД) до `commit()`; если передумал — `rollback()` выбрасывает всё содержимое корзины без следа. Это разделение «черновик в памяти» и «зафиксированное состояние в БД» — ключ к пониманию, почему объект может «казаться сохранённым» в текущем коде, но исчезнуть при следующем запуске программы.

Синтаксис моделей, который ты пишешь сегодня, — это не просто ORM-специфика: `class Author(Base): id: Mapped[int] = mapped_column(primary_key=True)` — прямое продолжение классов и type hints с недели 16, применённое к описанию таблиц. А паттерн `get_db()` с `yield` и закрытием сессии в `finally` — это заготовка для Dependency Injection, которую ты формализуешь через `Depends()` уже послезавтра, и она же концептуально повторится в Node.js как «одно соединение из пула на один запрос» на неделе 19.

Частое заблуждение — считать ORM-модель (`Author` из `models/`) и Pydantic-схему (`AuthorRead` для API) одной и той же сущностью, которую можно возвращать из эндпоинта напрямую. Это разные слои с разными целями: ORM-модель отражает структуру таблицы и может содержать чувствительные или внутренние поля (`password_hash`, `internal_notes`), а API-схема — это явно объявленный публичный контракт. Смешение слоёв — прямой путь к утечке данных в JSON-ответе. Вторая типичная ошибка — забыть `session.commit()`, из-за чего изменения видны в рамках текущего процесса (SQLAlchemy их закэшировал), но исчезают после перезапуска сервера, потому что физически не записаны в PostgreSQL.

**Читать:**

- [SQLAlchemy 2.0 Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)
- [Alembic](https://alembic.sqlalchemy.org/)

**Ключевая мысль:** ORM model ≠ API schema; сессия — граница транзакции.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. Проект `library-api`, venv, `pip install sqlalchemy psycopg2-binary python-dotenv`
2. Модели `Author`, `Book` с one-to-many relationship
3. `database.py`: engine, SessionLocal, `get_db()` generator с yield

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Не понимаешь ошибку — прочитай её с конца: файл, строка, тип. Открой DevTools / терминал и воспроизведи на 5 строках кода.

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 120: SQLAlchemy models and init_db"`

### Ловушки
- Забытый `session.commit()` — данные не сохраняются
- Lazy loading вне session — DetachedInstanceError

---

## День 121 (Вт): CRUD через ORM и запросы
<a id="week-18-day-121"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Library REST API**

### Теория

CRUD через ORM использует SQLAlchemy 2.0 style `select()`, не legacy `session.query()`. `session.get(Model, id)` — lookup по primary key с identity map cache. `session.scalars(select(Book).where(...)).all()` возвращает список ORM-объектов. Фильтры: `.where()`, `.join()`, `.order_by()`, `.limit()`, `.offset()` для пагинации.

N+1 problem: цикл по авторам + `author.books` внутри генерирует запрос на каждую итерацию. Решение — eager loading: `selectinload(Author.books)` или `joinedload`. Замерь количество SQL-запросов до и после — наглядный урок.

`session.delete(obj)` + `commit()` удаляет с учётом cascade rules. Пагинация `page=1, size=20` — обязательна для API endpoints. Вынеси CRUD в `crud/authors.py` — routes остаются тонкими. `title.ilike('%python%')` — case-insensitive поиск в PostgreSQL.

Ментальная модель N+1: представь, что нужно доставить книги 20 авторов, но вместо одной фуры, которая привозит всё за один рейс (`selectinload` — один дополнительный запрос со списком id), курьер каждый раз едет на склад за книгами одного конкретного автора — 20 отдельных поездок. Каждое обращение к `author.books` внутри цикла без eager loading — это отдельный SQL-запрос к базе, и для 100 авторов это будет 101 запрос вместо 2.

N+1 — не теоретическая проблема из учебника: это самая частая жалоба на производительность в production API, построенных на ORM, и именно её ты научишься видеть и чинить сегодня. В любом реальном проекте на SQLAlchemy, который ты соберёшь после курса, первый вопрос при жалобе «эндпоинт тормозит» — это «сколько SQL-запросов он генерирует», и умение включить логирование запросов и посчитать их — прямой навык из сегодняшней практики.

Частое заблуждение — думать, что раз `session.query()` (SQLAlchemy 1.x) всё ещё работает и встречается в старых туториалах, значит это актуальный способ писать запросы. Однако 2.0-style `select()` — новый стандарт с лучшей типизацией и явным поведением, и весь код недели построен на нём. Вторая ошибка — включать eager loading (`selectinload`) на все связи по умолчанию «на всякий случай»: это не бесплатно, каждая дополнительная связь — дополнительный запрос или JOIN, поэтому выбор между `selectinload` и `joinedload` должен опираться на реальный паттерн использования, а не привычку. Практическая привычка на будущее: при любом подозрении на медленный endpoint включай логирование SQL (`echo=True` в engine) и считай запросы за один HTTP-вызов — это тот же диагностический рефлекс, что и `EXPLAIN ANALYZE` на прошлой неделе, только применённый к ORM-коду.

**Читать:**

- [SQLAlchemy Select](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html)
- [Loading Relationships](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)
- [N+1 problem (обзор)](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#selectin-loading)

**Ключевая мысль:** N+1 лечится eager loading; `select()` API — стандарт SQLAlchemy 2.0.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. CRUD: `create_author`, `get_authors`, `update_book`, `delete_book`
2. Запрос: все книги автора с join через relationship или explicit join
3. Пагинация: `get_books(page=1, size=20)`

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Тесты/валидация красные — сначала один failing case, почини его, только потом следующий.

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 121: ORM CRUD and N+1 fix"`

### Ловушки
- N+1: цикл по authors + author.books внутри — сотни запросов
- `session.query()` — legacy, используй `select()`

---

## День 122 (Ср): FastAPI — первый API
<a id="week-18-day-122"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Library REST API**

### Теория

FastAPI — ASGI-фреймворк с автоматической валидацией из type hints. Path params (`/notes/{id}`), query params (`?skip=0`), request body (Pydantic model) — три входа данных. Pydantic проверяет типы в runtime и генерирует OpenAPI schema для Swagger.

`uvicorn main:app --reload` — dev-сервер с hot reload. `/docs` (Swagger UI) и `/redoc` — бесплатная интерактивная документация. `response_model=NoteRead` отсекает внутренние поля ORM от публичного JSON. Невалидный body → 422 Unprocessable Entity с деталями ошибок.

Начни с in-memory CRUD для `Note` — отдели изучение FastAPI от SQLAlchemy. `NoteCreate`, `NoteRead`, `NoteUpdate` (optional fields) — три схемы для разных операций. Mutable default в Pydantic: `Field(default_factory=list)`, не `tags=[]`.

Ментальная модель FastAPI — «contract-first без отдельного контракта»: обычно документацию API пишут отдельно от кода, и она рассинхронизируется через месяц. Здесь type hints и Pydantic-модель — это *и есть* контракт: FastAPI читает их один раз при старте и генерирует из них одновременно валидацию, сериализацию и Swagger-документацию. Написал `title: str` — и невалидный запрос без title автоматически получит 422 с понятным объяснением, без единой строчки ручной проверки.

Почему это выходит за рамки одного дня: дисциплина `response_model`, которую ты закладываешь здесь на игрушечном `Note`, — это тот самый механизм, который через два дня не даст утечь внутренним полям ORM-модели (`password_hash`, `internal_id`) в публичный JSON API «Библиотеки». А привычка объявлять отдельные схемы для создания, чтения и обновления (`NoteCreate` без id, `NoteRead` с id, `NoteUpdate` с опциональными полями) — стандартный паттерн, который ты повторишь для `Author`, `Book`, `Loan` уже завтра.

Частое заблуждение — думать, что раз Pydantic валидирует типы, значит любые дефолтные значения безопасны, включая `tags: list[str] = []`. В чистом Python mutable default-аргумент функции действительно опасен — он создаётся один раз и разделяется между вызовами; Pydantic обрабатывает этот случай корректно сам, но `Field(default_factory=list)` — явный, самодокументируемый способ показать намерение и защититься от этой более общей проблемы Python, если она встретится вне Pydantic. Вторая ошибка новичков — возвращать ORM- или dict-объект напрямую без `response_model`, из-за чего в ответе оказываются лишние или чувствительные поля, которые никто не собирался показывать наружу. `/docs` и `/redoc` при этом не два независимых артефакта, а два разных представления одной и той же OpenAPI-схемы — Swagger удобен для ручного тестирования прямо из браузера, ReDoc — для чтения документации как справочника.

**Читать:**

- [FastAPI First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [Pydantic Models](https://fastapi.tiangolo.com/tutorial/body/)

**Ключевая мысль:** type hints + Pydantic = валидация и docs из коробки; response_model защищает API.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. `main.py`: FastAPI app, `GET /health` → `{"status": "ok"}`
2. In-memory CRUD для `Note` (id, title, body) — без БД пока
3. Pydantic: `NoteCreate`, `NoteRead`, `NoteUpdate` (все поля optional)

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Застрял >20 мин — выпиши вход/выход задачи в 3 строки. Сделай минимальный пример в `playground.*`, без копипаста из ИИ.

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 122: FastAPI in-memory notes API"`

### Ловушки
- Mutable default list в Pydantic — `Field(default_factory=list)`
- Возврат ORM object без `response_model` — утечка внутренних полей

---

## День 123 (Чт): Dependency Injection и подключение БД
<a id="week-18-day-123"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Library REST API**

### Теория

Dependency Injection в FastAPI — через `Depends`. `get_db()` с `yield` создаёт сессию на один request и закрывает в `finally` — не используй глобальную session (race conditions). `Depends(get_db)` в параметрах endpoint автоматически резолвит зависимость.

`HTTPException(status_code=404, detail="Author not found")` — контролируемые ошибки вместо 500. Семантика статусов: 200 OK, 201 Created, 204 No Content, 404 Not Found, 409 Conflict, 422 Validation Error. Вложенные dependencies (`get_current_user` на нед. 20) строят цепочку проверок.

Pydantic schemas `AuthorCreate` / `AuthorRead` отделяют вход и выход. Nested resource `GET /authors/{id}/books` — RESTful вложенность. Lifespan events (startup/shutdown) — для инициализации пула и закрытия соединений (обзор).

Ментальная модель `Depends()` — вендинговый автомат: ты не заботишься, как приготовлен кофе, ты просто объявляешь «мне нужна сессия БД» в параметрах функции-эндпоинта, а FastAPI сам вызывает `get_db()`, отдаёт тебе готовую сессию и гарантированно закрывает её после ответа — даже если внутри эндпоинта произошло исключение. Ты декларируешь зависимость, а не управляешь её жизненным циклом руками.

Это не разовый трюк для сегодняшнего дня: ровно тот же механизм `Depends` станет способом получить текущего аутентифицированного пользователя (`get_current_user`) на неделе 20 — сегодняшний `Depends(get_db)` это буквально тренировочная версия завтрашней цепочки проверок доступа. Понимание, что зависимости можно комбинировать и они выполняются перед телом эндпоинта, снимает половину вопросов про то, «как вообще работает auth» позже.

Частое заблуждение — считать, что одна глобальная сессия на всё приложение (созданная один раз при старте) — безобидная оптимизация, которая экономит ресурсы. На самом деле под конкурентной нагрузкой это прямой путь к состоянию гонки: два одновременных запроса начнут писать в одну и ту же сессию, и данные одного пользователя могут утечь в ответ другому или вызвать неконсистентные commit. Вторая ошибка — возвращать 200 OK при удалении несуществующего ресурса вместо честного 404 через `HTTPException`: API должен явно сообщать о промахе, а не молча делать вид, что всё прошло успешно. Nested resource `GET /authors/{id}/books` заслуживает отдельного внимания: это не отдельная таблица, а тот же relationship, показанный под другим URL — RESTful вложенность выражает связь между ресурсами через структуру пути, а не через отдельный, никак не связанный endpoint.

**Читать:**

- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [HTTPException](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Status Codes](https://fastapi.tiangolo.com/tutorial/response-status-code/)

**Ключевая мысль:** одна DB session на request через Depends; HTTPException — явные ошибки API.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. Подключи SQLAlchemy к FastAPI через `Depends(get_db)`
2. `GET /authors`, `POST /authors`, `GET /authors/{id}`
3. 404 если author не найден — `HTTPException`

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Документация не клеится — найди один официальный пример (MDN / docs) и сопоставь 1:1 со своим кодом.

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 123: FastAPI DI and authors endpoints"`

### Ловушки
- Глобальная session — race conditions и утечки
- 200 на DELETE несуществующего — должен быть 404

---

## День 124 (Пт): Полный REST API «Библиотека»
<a id="week-18-day-124"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Library REST API**

### Теория

REST — соглашения, не протокол. URL — существительные (`/books`), HTTP verbs — действия (GET читать, POST создать, PUT/PATCH обновить, DELETE удалить). GET, PUT, DELETE идемпотентны: повторный запрос даёт тот же эффект. POST — нет (каждый создаёт новый ресурс).

`APIRouter` модульно группирует endpoints: `routers/authors.py`, prefix `/api/v1`, tags для Swagger. Пагинация в едином формате: `{ items, total, page, size }`. Фильтрация через query: `?status=active&search=python`. Версионирование `/api/v1` защищает фронтенд от breaking changes.

Бизнес-правила в API: нельзя выдать уже выданную книгу → 409 Conflict, не 500. Глаголы в URL (`/getAuthors`) — антипаттерн. Отсутствие валидации FK — 500 вместо понятного 404.

Ментальная модель REST: URL — это витрина магазина с существительными на ценниках (`/books`, `/authors`), а HTTP-глагол — это то, что ты делаешь с товаром на этой витрине (посмотреть — GET, положить в корзину — POST, поменять — PUT/PATCH, убрать — DELETE). Действие никогда не должно быть зашито в само название полки; если тянет написать `/getBooks` или `/createAuthor`, это сигнал, что мышление соскользнуло с ресурсов на процедуры.

Структура `routers/authors.py`, `books.py`, `loans.py` с общим префиксом `/api/v1`, которую ты собираешь сегодня, — прямой аналог того, что ты построишь в Express на неделе 19 через `routes/`, `controllers/`, `services/`: разные языки, одна и та же архитектурная идея модульного разделения по ресурсам. Сравнение этих двух реализаций в конце месяца станет наглядным доказательством, что архитектурное мышление важнее конкретного фреймворка.

Частое заблуждение — трактовать любое нарушение бизнес-правила (книга уже выдана, лимит займов исчерпан) как ошибку сервера и возвращать 500. На деле это ожидаемая, предсказуемая ситуация в доменной логике, и правильный ответ — 409 Conflict с понятным сообщением, которое фронтенд может показать пользователю осмысленно. Вторая распространённая ошибка — не проверять существование внешнего ключа перед вставкой (например, `author_id`, которого нет), из-за чего клиент получает малопонятную 500-ю ошибку от БД вместо контролируемого 404 или 400 от приложения. Версионирование через префикс `/api/v1` — ещё одна деталь, которую легко недооценить: она защищает уже подключившийся фронтенд от breaking changes, когда через несколько месяцев понадобится изменить форму ответа — старые клиенты продолжат работать с `/api/v1`, пока новые постепенно переходят на `/api/v2`.

**Читать:**

- [FastAPI Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

**Ключевая мысль:** REST = ресурсы + HTTP semantics; 409 для нарушения бизнес-правил.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. Роутеры: `routers/authors.py`, `books.py`, `loans.py`
2. CRUD для books и loans с Pydantic validation
3. `POST /loans` — проверка: книга доступна? иначе 409

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Не понимаешь ошибку — прочитай её с конца: файл, строка, тип. Открой DevTools / терминал и воспроизведи на 5 строках кода.

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 124: full library REST routers"`

### Ловушки
- Глаголы в URL: `/getAuthors` — не REST
- Отсутствие валидации foreign key — 500 вместо 404

---

## День 125 (Сб): Тестирование API и обработка ошибок
<a id="week-18-day-125"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Library REST API**

### Теория

Тестирование API — страховка от регрессий. FastAPI `TestClient` (на базе httpx) шлёт запросы без реального сетевого сервера. pytest fixtures в `conftest.py`: client, db session, sample data. Test DB — отдельная schema или SQLite in-memory; никогда production.

Arrange-Act-Assert: подготовь данные, выполни запрос, проверь status и body. Тесты: create author 201, get missing 404, loan conflict 409. `pytest -v --tb=short` — читаемый вывод. Rollback после каждого теста — иначе flaky tests.

Global exception handlers: `IntegrityError` → 409, generic → 500 без stack trace в production. CORS middleware понадобится на нед. 21. Coverage `pytest --cov=app` показывает пробелы. ≥ 8 тестов — минимум для уверенности в CRUD и ошибках.

Ментальная модель `TestClient` — «робот-клиент», который стучится в твоё FastAPI-приложение напрямую в памяти, без реального TCP-сокета и сетевого стека. Отсюда и скорость (сотни тестов выполняются за секунды), и детерминированность (нет случайных сетевых задержек или занятых портов) — тесты можно гонять на каждый коммит без страха, что они станут узким местом разработки.

Автотесты — это не формальность для галочки в критериях: именно они дают возможность бесстрашно рефакторить код проекта недели, зная, что любая регрессия будет поймана до того, как попадёт в продакшен. Это тот же навык и тот же паттерн Arrange-Act-Assert, который ты используешь на любой позиции разработчика, независимо от языка — pytest здесь, Jest/Vitest в Node-мире.

Частое заблуждение — писать тесты только на happy path («создание автора работает») и считать это достаточным покрытием. В реальности большинство продакшен-багов живёт именно в граничных случаях: что возвращается при 404, что происходит при попытке создать конфликтующий заём (409), что при невалидном body (422) — и сегодняшняя практика целенаправленно требует именно такие тесты. Вторая ошибка — забыть откат (rollback) состояния БД после каждого теста: без него тесты начинают зависеть от порядка выполнения и от результатов друг друга, превращаясь в нестабильные (flaky) — тест то падает, то проходит без изменений в коде. Global exception handler для `IntegrityError` (например, попытка создать книгу с несуществующим `author_id`) — та же идея централизованной обработки ошибок, которую ты применишь в Express на следующей неделе через error-middleware: одно место в коде решает, как любая непойманная ошибка конкретного типа превращается в понятный HTTP-ответ.

**Читать:**

- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest](https://docs.pytest.org/en/stable/getting-started.html)
- [httpx](https://www.python-httpx.org/)

**Ключевая мысль:** изолированная test DB; тесты на auth, 404, 409 — не только happy path.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. `pip install pytest httpx`
2. Тесты: create author, get 404, create loan conflict → 409
3. `conftest.py` — fixture test client + test db (rollback после теста)

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Тесты/валидация красные — сначала один failing case, почини его, только потом следующий.

### Git
- Закоммить изменения дня: `git add week-18/` → `git commit -m "week 18 day 125: pytest suite and error handlers"`

### Ловушки
- Тесты на production DB — никогда
- Забытый rollback после теста — flaky tests

---

## День 126 (Вс): Ревью и документация API
<a id="week-18-day-126"></a>

> **Время (полный):** ~2ч теория · ~2.5ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~50м теория · ~1ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Library REST API**

### Теория

OpenAPI schema FastAPI генерирует из type hints и Pydantic — docs всегда синхронны с кодом, если ты дисциплинирован. README capstone-уровня: архитектура слоёв (routes → crud → models → db), env vars, curl-примеры, запуск postgres через docker. Postman collection — ручное тестирование для демо.

12 Factor App: config через environment, не hardcode. `.env.example` без секретов. Mermaid-диаграмма слоёв в README помогает объяснить проект за 2 минуты. Логирование через `logging` module: INFO в production, DEBUG в dev.

Финальный прогон: `pytest`, `uvicorn`, ручная проверка Swagger. Library REST API — шаблон для Express на нед. 19 и DevHub на нед. 22. Тег `week-18-done` завершает первый production-like Python backend.

Ментальная модель для ревью-дня: README и OpenAPI-документация — это витрина твоего проекта. Первые две минуты, которые незнакомый разработчик (или нанимающий менеджер) проводит с репозиторием, определяют, доверяет ли он остальному коду. Хорошо структурированный README с архитектурной диаграммой и curl-примерами говорит «этот человек умеет думать о других разработчиках», даже если он ни разу не прочитает исходники.

Дисциплина документирования, которую ты закрепляешь сегодня — env vars, архитектура слоёв, инструкции запуска, — это не разовая задача для этого проекта: ты буквально повторишь тот же набор артефактов для Express-проекта на неделе 19 и для capstone DevHub на неделе 22, так что сегодняшний README становится шаблоном, который экономит время трижды.

Частое заблуждение — считать, что автоматически сгенерированный Swagger (`/docs`) полностью заменяет README. Swagger прекрасно показывает *что* доступно (endpoints, схемы, параметры), но не объясняет *как* поднять проект с нуля — какие переменные окружения нужны, как накатить миграции, откуда взять seed-данные и в каком порядке запускать команды. Именно поэтому оба артефакта нужны вместе, и критерий «структура проекта понятна новому разработчику» проверяется человеком, а не автогенерацией. Логирование через стандартный модуль `logging` (а не `print`) — ещё одна деталь взросления проекта: `INFO` в продакшене и `DEBUG` в разработке позволяют управлять шумом логов без правки кода, просто переменной окружения. Принцип 12 Factor App («конфигурация через переменные окружения, а не хардкод») — ещё одна деталь, которая перестаёт быть абстрактной рекомендацией и становится практическим требованием, как только проект нужно развернуть в контейнере: `.env.example` документирует, какие переменные обязательны, не раскрывая ни одного реального секрета.

**Читать:**

- [OpenAPI](https://fastapi.tiangolo.com/features/#automatic-docs)
- [12 Factor App](https://12factor.net/config)
- [Mermaid](https://mermaid.js.org/)

**Ключевая мысль:** документация API — часть deliverable; OpenAPI из кода, не из Word.

### Практика (полный трек)
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

### Практика (лайт / MVP)
1. README: архитектура, запуск, env vars, примеры curl
2. `.env.example`: `DATABASE_URL`, `APP_ENV=development`
3. Export Postman collection JSON в `docs/postman/`

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Застрял >20 мин — выпиши вход/выход задачи в 3 строки. Сделай минимальный пример в `playground.*`, без копипаста из ИИ.

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


## Проверь себя

<details>
<summary>Что должно получиться к концу недели?</summary>

Работающий проект **Library REST API** в `learning-log/week-18/`, осмысленная Git-история, тег `week-18-done`.

</details>

<details>
<summary>Главный навык недели одной фразой?</summary>

FastAPI + SQLAlchemy REST API

</details>

<details>
<summary>Можно ли пропустить день?</summary>

Нет — дни связаны. В **лайт-режиме** сократи практику до MVP, но теорию и Git-коммит не пропускай.

</details>
