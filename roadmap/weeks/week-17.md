# Неделя 17: SQL, PostgreSQL, индексы

> **Цель недели:** освоить реляционные БД, SQL-запросы, PostgreSQL и оптимизацию через индексы.
> **Литература:** [SQLBolt](https://sqlbolt.com/), [PostgreSQL Tutorial](https://www.postgresqltutorial.com/), [Use The Index, Luke](https://use-the-index-luke.com/)
> **Проект недели:** [Library Database](../../docs/projects.md#неделя-17--library-database) — PostgreSQL-схема библиотеки, 15+ запросов, индексы, EXPLAIN.
> **Git:** папка `learning-log/week-17/`, SQL-скрипты в `schema.sql`, `seed.sql`, `queries.sql`; тег `week-17-done`.

## День 113 (Пн): SQL основы — SELECT, фильтрация, сортировка
<a id="week-17-day-113"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library Database**

### Теория

SQL — декларативный язык: ты описываешь, *какие* данные нужны, а СУБД решает, *как* их достать. Базовый pipeline: `SELECT` колонки `FROM` таблицы `WHERE` условие `ORDER BY` сортировка `LIMIT` ограничение. `DISTINCT` убирает дубликаты строк в результате.

Операторы фильтрации: `=`, `<>`, `IN (...)`, `BETWEEN`, `LIKE 'Py%'` (префикс), `IS NULL` / `IS NOT NULL`. Агрегаты `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` сворачивают множество строк. `GROUP BY` группирует перед агрегацией; `HAVING` фильтрует группы *после* агрегации — не путай с `WHERE`, который фильтрует строки *до*.

Порядок выполнения SQL: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT. Понимание этого порядка объясняет, почему нельзя использовать алиас SELECT в WHERE той же фазы. `SELECT *` удобно в учебе, в production выбирай нужные колонки.

**Читать:**

- [SQLBolt Lessons 1–6](https://sqlbolt.com/lesson/select_queries_introduction)
- [PostgreSQL SELECT](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-select/)
- [SQL Style Guide](https://www.sqlstyle.guide/)

**Ключевая мысль:** WHERE фильтрует строки, HAVING — группы; SQL описывает результат, не алгоритм.

### Практика
1. Установи [DB Browser for SQLite](https://sqlitebrowser.org/) или `sqlite3` CLI для быстрых экспериментов
2. Создай БД «shop»: `products`, `categories`, `orders` с PRIMARY KEY
3. 10+ SELECT-запросов: топ-5 дорогих, средняя цена, count по категории
4. Запрос с `GROUP BY category_id` и `HAVING count(*) > 2`
5. Запрос с `DISTINCT` и сортировкой по двум колонкам
6. Сохрани все запросы в `queries/day113.sql` с комментариями

**Критерии:**
- [ ] Схема с PRIMARY KEY на каждой таблице
- [ ] ≥ 10 осмысленных запросов в `queries.sql`
- [ ] Понимаешь разницу WHERE vs HAVING

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 113: SQL SELECT and aggregates"`

### Ловушки
- SELECT * в production — выбирай нужные колонки
- GROUP BY без агрегата в SELECT — ошибка в строгом SQL

---

## День 114 (Вт): JOIN, INSERT, UPDATE, DELETE
<a id="week-17-day-114"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library Database**

### Теория

Реляционная модель связывает таблицы ключами. `INNER JOIN` возвращает только строки с совпадением в обеих таблицах. `LEFT JOIN` сохраняет все строки «слева» и подставляет NULL справа, если совпадения нет — идеально для «клиенты без заказов» (`WHERE orders.id IS NULL`).

DML — изменение данных: `INSERT`, `UPDATE`, `DELETE`. Золотое правило: UPDATE и DELETE всегда с осмысленным `WHERE`. Без WHERE ты изменишь или удалишь всю таблицу — катастрофа, даже в учебной БД. `FOREIGN KEY` и `REFERENCES` обеспечивают целостность на уровне СУБД, не только приложения.

`ON DELETE CASCADE` удаляет дочерние записи вместе с родителем; `SET NULL` обнуляет FK. Транзакция `BEGIN` → операции → `COMMIT` или `ROLLBACK` — атомарность: либо всё, либо ничего. Забытый `ON` в JOIN даёт декартово произведение — взрыв числа строк.

**Читать:**

- [SQLBolt — JOINs](https://sqlbolt.com/lesson/select_queries_with_joins)
- [PostgreSQL JOINs](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-joins/)
- [Transactions](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-transaction/)

**Ключевая мысль:** JOIN связывает таблицы; DELETE/UPDATE без WHERE — инцидент.

### Практика
1. Расширь shop: `customers`, `order_items` с FK
2. Запрос: заказы с именами клиентов (INNER JOIN)
3. Клиенты без заказов (LEFT JOIN + `WHERE orders.id IS NULL`)
4. UPDATE цены категории «sale» −10% в транзакции
5. DELETE тестовых записей с ROLLBACK для проверки
6. Запрос «выручка по клиенту» через JOIN + SUM

**Критерии:**
- [ ] FOREIGN KEY между таблицами
- [ ] JOIN-запрос возвращает ожидаемые строки
- [ ] DELETE только с WHERE (не без него!)

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 114: JOINs and DML with transactions"`

### Ловушки
- DELETE/UPDATE без WHERE — катастрофа
- Cartesian product — забытый ON в JOIN

---

## День 115 (Ср): Нормализация и проектирование схемы
<a id="week-17-day-115"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library Database**

### Теория

Нормализация убирает избыточность и аномалии обновления. 1NF — атомарные значения в ячейке (не CSV списка id). 2NF — нет частичных зависимостей от составного ключа. 3NF — нет транзитивных зависимостей (город заёмщика не должен дублироваться в каждой записи loan, если borrower уже хранит город).

One-to-many: FK в таблице «многих» (`books.author_id → authors.id`). Many-to-many: junction table (`task_tags` с двумя FK). Именование: `snake_case`, plural tables (`authors`, `books`) — выбери конвенцию и держись её. `CHECK (price > 0)` и `NOT NULL` валидируют на уровне БД.

Денормализация — осознанный trade-off ради скорости чтения, не лень проектировать. ER-диаграмма на dbdiagram.io или Mermaid фиксирует связи до написания SQL. Антипаттерн: хранить список id в одной TEXT-колонке.

**Читать:**

- [PostgreSQL Tutorial — Getting Started](https://www.postgresqltutorial.com/postgresql-getting-started/)
- [Normalization (обзор)](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-foreign-key/)
- [dbdiagram.io](https://dbdiagram.io/)

**Ключевая мысль:** нормализация защищает от дублирования; many-to-many — всегда junction table.

### Практика
1. Спроектируй БД «Библиотека»: `authors`, `books`, `borrowers`, `loans`
2. ER-диаграмма на [dbdiagram.io](https://dbdiagram.io/) или Mermaid в README
3. `CREATE TABLE` с NOT NULL, UNIQUE, CHECK constraints
4. Seed: 5 авторов, 20 книг, 3 заёмщика, 10 займов
5. Документируй связи: 1:N author→books, N:M если нужны genres
6. Проверь: нет дублирования `author_name` в `books`

**Критерии:**
- [ ] Нет дублирования author name в books
- [ ] Junction table для many-to-many (если нужна)
- [ ] ER-диаграмма в repo

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 115: library schema and ER diagram"`

### Ловушки
- Хранение списка id в одной колонке CSV — антипаттерн
- Nullable всего подряд — потеря целостности данных

---

## День 116 (Чт): PostgreSQL — установка и отличия от SQLite
<a id="week-17-day-116"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library Database**

### Теория

PostgreSQL — серверная СУБД для production: concurrent access, роли, extensions, богатые типы (`JSONB`, `UUID`, `TIMESTAMPTZ`). SQLite — один файл, zero-config, идеален для прототипов и встроенных приложений. На этой неделе ты переносишь схему «Библиотека» из SQLite в PG.

Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=pass postgres:16` поднимает изолированный инстанс за секунды. Клиенты: `psql`, pgAdmin, DBeaver. Диалектные отличия: `AUTOINCREMENT` (SQLite) vs `SERIAL` / `GENERATED ALWAYS AS IDENTITY` (PostgreSQL).

`DATABASE_URL=postgresql://user:pass@localhost:5432/library` — стандартная строка подключения для приложений. Документируй пароль в `.env.example` без реальных значений. Сравни SQLite vs PG письменно: когда файл достаточен, когда нужен сервер.

**Читать:**

- [PostgreSQL Downloads](https://www.postgresql.org/download/)
- [psql](https://www.postgresql.org/docs/current/app-psql.html)
- [Docker — postgres image](https://hub.docker.com/_/postgres)

**Ключевая мысль:** PostgreSQL — для multi-user и production; миграция учит диалектные различия.

### Практика
1. Подними PostgreSQL (Docker или локально)
2. Перенеси схему «Библиотека» в PostgreSQL через `schema.sql`
3. Подключись через psql или DBeaver, выполни `\dt` и `\d books`
4. `seed.sql` — вставка тестовых данных
5. Сравни SQLite vs PG — запиши 5 пунктов в `notes/pg-vs-sqlite.md`
6. Создай `.env.example` с `DATABASE_URL=postgresql://user:pass@localhost:5432/library`

**Критерии:**
- [ ] Подключение к PG работает
- [ ] Схема создана через SQL-скрипт `schema.sql`
- [ ] Seed script `seed.sql` выполняется без ошибок

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 116: PostgreSQL setup and schema migration"`

### Ловушки
- Забытый пароль postgres в Docker — документируй в `.env.example`
- Различия SQL диалектов: AUTOINCREMENT vs SERIAL

---

## День 117 (Пт): Индексы и EXPLAIN ANALYZE
<a id="week-17-day-117"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library Database**

### Теория

Индекс — структура данных (обычно B-tree), ускоряющая поиск по колонке ценой замедления INSERT/UPDATE. `CREATE INDEX idx_books_title ON books(title)` помогает `WHERE title = '...'` и `LIKE 'Python%'` (префикс), но не `LIKE '%python'` (leading wildcard).

`EXPLAIN ANALYZE` показывает реальный план выполнения: Seq Scan (полный перебор) vs Index Scan (по дереву). Сравни `cost`, `rows`, `actual time` до и после индекса на таблице с 10 000+ строк. Составной индекс `(author_id, title)` — порядок колонок важен для составных запросов.

Use The Index, Luke объясняет, когда индекс помогает, а когда оптимизатор его игнорирует. Индекс на каждую колонку — перебор: каждая запись обновляет все индексы. Документируй замеры в `notes/indexes.md` — это навык для собеседований.

**Читать:**

- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [EXPLAIN ANALYZE](https://www.postgresql.org/docs/current/sql-explain.html)
- [Use The Index, Luke](https://use-the-index-luke.com/)

**Ключевая мысль:** индекс — trade-off read vs write; EXPLAIN — единственный честный ответ «почему медленно».

### Практика
1. Таблица `books` с 10 000+ строк (скрипт `scripts/generate_books.sql`)
2. `EXPLAIN ANALYZE SELECT * FROM books WHERE title LIKE 'Python%'` — без индекса
3. `CREATE INDEX idx_books_title ON books(title)`
4. Повтори EXPLAIN — сравни cost, rows, actual time
5. Запиши выводы в `notes/indexes.md` с скриншотами или копией планов
6. Эксперимент: индекс на `(author_id)` для JOIN-запроса

**Критерии:**
- [ ] Индекс создан на колонке поиска
- [ ] EXPLAIN показывает Index Scan (или объясни почему Seq Scan)
- [ ] Записаны выводы в `notes/indexes.md`

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 117: indexes and EXPLAIN ANALYZE"`

### Ловушки
- Индекс на каждую колонку — замедляет INSERT/UPDATE
- `LIKE '%python'` — индекс B-tree не поможет (leading wildcard)

---

## День 118 (Сб): SQLite/PostgreSQL из Python
<a id="week-17-day-118"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library Database**

### Теория

Приложение общается с БД через драйвер. Встроенный `sqlite3` использует placeholders `?`; `psycopg2` / `psycopg3` для PostgreSQL — `%s`. Никогда не вставляй пользовательский ввод в SQL через f-string — это SQL injection. Только параметризованные запросы: `cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))`.

Context manager `with conn:` коммитит при успехе и откатывает при исключении. `DATABASE_URL` из `.env` через `python-dotenv` — 12-factor config. Connection pool (в веб-приложении) переиспользует соединения под нагрузкой; в CLI достаточно одного подключения на операцию.

Абстракция репозитория с методами `fetch_all`, `execute` позволяет переключать SQLite и PostgreSQL флагом `--db`. Скрипт миграции sqlite → postgres учит переносу данных между СУБД. Забытый `conn.commit()` — изменения не сохранятся.

**Читать:**

- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [psycopg2](https://www.psycopg.org/docs/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

**Ключевая мысль:** placeholders — не опция, а требование безопасности; commit явный или через context manager.

### Практика
1. Расширь CLI Task Manager (нед.16): опция `--db postgres` vs sqlite
2. `DATABASE_URL` из `.env` через `python-dotenv`
3. Репозиторий с методами `fetch_all`, `execute` для обеих БД
4. Скрипт миграции sqlite → postgres (`migrate_to_pg.py`)
5. 3 операции в `library_cli.py`: список книг, добавить заём, вернуть книгу
6. Все запросы — только placeholders

**Критерии:**
- [ ] Нет SQL injection — только placeholders
- [ ] `with conn:` или try/finally close
- [ ] `.env.example` с DATABASE_URL

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 118: Python psycopg2 library CLI"`

### Ловушки
- f-string в SQL: `f"SELECT * FROM users WHERE name = '{name}'"` — injection
- Забытый `conn.commit()` — изменения не сохраняются

---

## День 119 (Вс): Ревью SQL и подготовка к ORM
<a id="week-17-day-119"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library Database**

### Теория

Ревью SQL закрепляет фундамент перед ORM на неделе 18. ACID: Atomicity (всё или ничего), Consistency (инварианты БД), Isolation (параллельные транзакции не мешают), Durability (commit переживает сбой). Транзакции — не абстракция, а гарантия при переводе денег или выдаче книги.

Views — сохранённые запросы; stored procedures — логика внутри БД (обзор). Isolation levels (read committed, serializable) влияют на фантомные чтения — на junior достаточно знать, что они существуют. SQL Style Guide делает запросы читаемыми для команды.

ORM (SQLAlchemy) маппит таблицы на классы Python: меньше boilerplate SQL, но риск N+1 и «магических» запросов. Понимание raw SQL остаётся обязательным для отладки и оптимизации. Установи `sqlalchemy fastapi uvicorn` в venv — старт недели 18.

**Читать:**

- [SQLBolt](https://sqlbolt.com/)
- [ACID (PostgreSQL)](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [SQL Style Guide](https://www.sqlstyle.guide/)

**Ключевая мысль:** SQL — база; ORM — удобство поверх, не замена понимания JOIN и индексов.

### Практика
1. Пройди 15 уроков SQLBolt без подсказок — отметь слабые темы
2. Напиши 5 сложных запросов: JOIN + агрегат + HAVING + ORDER BY
3. Ответь письменно: «INNER vs LEFT JOIN» с примерами из библиотеки
4. Запрос «кто не вернул книгу» — просроченные loans
5. Установи `pip install sqlalchemy fastapi uvicorn` в venv
6. Финализируй `queries.sql` — 15+ запросов для проекта

**Критерии:**
- [ ] 5 сложных запросов с JOIN и агрегатами
- [ ] Ответы на «INNER vs LEFT JOIN» письменно
- [ ] venv готов для недели 18

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 119: SQL review and 15 queries"`
- Поставь тег: `git tag week-17-done`

---

## Проект недели

**База «Библиотека»** — полный SQL-проект на PostgreSQL. Спецификация: [docs/projects.md — неделя 17](../../docs/projects.md#неделя-17--library-database).

### Структура репозитория

```
week-17/
├── schema.sql          # CREATE TABLE, FK, constraints
├── seed.sql            # тестовые данные
├── queries.sql         # 15+ запросов с комментариями
├── notes/
│   └── indexes.md      # EXPLAIN до/после
├── scripts/
│   └── generate_books.sql
├── library_cli.py      # 3+ операции через psycopg2
├── er-diagram.png      # или Mermaid в README
└── README.md
```

### Функции

1. Таблицы: `authors`, `books`, `borrowers`, `loans` с FK и CHECK
2. Запросы: топ авторов, просроченные займы, книги без займов, статистика
3. Индекс на `books.title` — EXPLAIN до и после с замерами
4. Python CLI: подключение, 3 операции, параметризованные запросы
5. docker-compose только для postgres (опционально, пригодится на нед. 21)

### Критерии проекта

- [ ] FK constraints работают — нельзя удалить автора с книгами без CASCADE
- [ ] Запрос «кто не вернул книгу» корректен и документирован
- [ ] Индекс документирован с цифрами из EXPLAIN ANALYZE
- [ ] `queries.sql` содержит ≥ 15 осмысленных запросов
- [ ] README: как поднять PG, выполнить schema/seed, запустить CLI
- [ ] Тег `week-17-done`

## Ревью-чеклист
- INNER JOIN vs LEFT JOIN — пример каждого?
- Зачем PRIMARY KEY и FOREIGN KEY?
- Что показывает EXPLAIN ANALYZE?
- Как защититься от SQL injection?
- PostgreSQL vs SQLite — 3 случая когда PG?


## Проверь себя

<details>
<summary>Что должно получиться к концу недели?</summary>

Работающий проект **Library Database** в `learning-log/week-17/`, осмысленная Git-история, тег `week-17-done`.

</details>

<details>
<summary>Главный навык недели одной фразой?</summary>

SQL и PostgreSQL на практике

</details>

<details>
<summary>Можно ли пропустить день?</summary>

Нет — дни связаны. В **лайт-режиме** сократи практику до MVP, но теорию и Git-коммит не пропускай.

</details>
