# Неделя 17: SQL, PostgreSQL, индексы

> **Цель недели:** освоить реляционные БД, SQL-запросы, PostgreSQL и оптимизацию через индексы.
> **Литература:** [SQLBolt](https://sqlbolt.com/), [PostgreSQL Tutorial](https://www.postgresqltutorial.com/), [Use The Index, Luke](https://use-the-index-luke.com/)
> **Проект недели:** [Library Database](../../docs/projects.md#неделя-17--library-database) — PostgreSQL-схема библиотеки, 15+ запросов, индексы, EXPLAIN.
> **Git:** папка `learning-log/week-17/`, SQL-скрипты в `schema.sql`, `seed.sql`, `queries.sql`; тег `week-17-done`.

## День 113 (Пн): SQL основы — SELECT, фильтрация, сортировка

### Теория
- [SQLBolt Lessons 1–6](https://sqlbolt.com/lesson/select_queries_introduction): SQL — декларативный язык, описываешь *что* нужно, не *как*
- `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT` — базовый pipeline запроса
- Операторы: `=`, `<>`, `IN`, `BETWEEN`, `LIKE`, `IS NULL` / `IS NOT NULL`
- Агрегаты: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` — свёртка множества строк в одно значение
- `GROUP BY` группирует строки; `HAVING` фильтрует *после* агрегации (аналог WHERE для групп)
- Порядок выполнения: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT

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

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 113: SQL SELECT and aggregates"`

### Ловушки
- SELECT * в production — выбирай нужные колонки
- GROUP BY без агрегата в SELECT — ошибка в строгом SQL

---

## День 114 (Вт): JOIN, INSERT, UPDATE, DELETE

### Теория
- [SQLBolt — JOINs](https://sqlbolt.com/lesson/table_joins): связь таблиц через ключи
- INNER JOIN — только совпадающие строки; LEFT JOIN — все из левой + совпадения справа (NULL если нет)
- INSERT, UPDATE, DELETE всегда с осмысленным WHERE — иначе затронешь всю таблицу
- FOREIGN KEY, REFERENCES — целостность на уровне БД, не только приложения
- ON DELETE CASCADE / SET NULL — поведение при удалении родителя
- Транзакции BEGIN → COMMIT / ROLLBACK — атомарность нескольких операций

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

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 114: JOINs and DML with transactions"`

### Ловушки
- DELETE/UPDATE без WHERE — катастрофа
- Cartesian product — забытый ON в JOIN

---

## День 115 (Ср): Нормализация и проектирование схемы

### Теория
- 1NF — атомарные значения; 2NF — нет частичных зависимостей от составного ключа; 3NF — нет транзитивных зависимостей
- One-to-many: FK в «многих»; many-to-many: junction table с двумя FK
- [Database Design](https://www.postgresqltutorial.com/postgresql-get-started/postgresql-sample-database/) — учись на готовых схемах
- Именование: `snake_case`, plural tables (`authors`, `books`) — выбери и держись конвенции
- CHECK constraints — валидация на уровне БД (`price > 0`, `status IN (...)`)
- Денормализация — осознанный trade-off ради скорости чтения (позже)

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

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 115: library schema and ER diagram"`

### Ловушки
- Хранение списка id в одной колонке CSV — антипаттерн
- Nullable всего подряд — потеря целостности данных

---

## День 116 (Чт): PostgreSQL — установка и отличия от SQLite

### Теория
- [PostgreSQL Downloads](https://www.postgresql.org/download/) — серверная СУБД с concurrent access
- Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=pass postgres:16` — изолированный инстанс
- Типы: `SERIAL`, `VARCHAR`, `TEXT`, `TIMESTAMP`, `TIMESTAMPTZ`, `JSONB`, `UUID` — богаче SQLite
- [psql](https://www.postgresql.org/docs/current/app-psql.html), pgAdmin, DBeaver — клиенты
- SQLite — файл, zero-config; PostgreSQL — сеть, роли, extensions, production-ready
- Диалекты: `AUTOINCREMENT` (SQLite) vs `SERIAL` / `GENERATED` (PG)

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

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 116: PostgreSQL setup and schema migration"`

### Ловушки
- Забытый пароль postgres в Docker — документируй в `.env.example`
- Различия SQL диалектов: AUTOINCREMENT vs SERIAL

---

## День 117 (Пт): Индексы и EXPLAIN ANALYZE

### Теория
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html) — ускоряют чтение, замедляют запись
- B-tree index (default) — эффективен для `=`, `<`, `>`, `LIKE 'prefix%'`, ORDER BY
- [EXPLAIN ANALYZE](https://www.postgresql.org/docs/current/sql-explain.html) — реальный план и время выполнения
- Seq Scan — полный перебор; Index Scan — поиск по дереву
- [Use The Index, Luke](https://use-the-index-luke.com/) — когда индекс помогает, когда нет
- Composite index `(author_id, title)` — порядок колонок важен для составных запросов

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

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 117: indexes and EXPLAIN ANALYZE"`

### Ловушки
- Индекс на каждую колонку — замедляет INSERT/UPDATE
- `LIKE '%python'` — индекс B-tree не поможет (leading wildcard)

---

## День 118 (Сб): SQLite/PostgreSQL из Python

### Теория
- [sqlite3 module](https://docs.python.org/3/library/sqlite3.html) — встроенный, `?` placeholders
- [psycopg2](https://www.psycopg.org/docs/) / psycopg3 — `%s` placeholders для PostgreSQL
- Connection pool (обзор) — переиспользование соединений в веб-приложении
- Context managers: `with conn:` — commit/rollback автоматически
- `DATABASE_URL` из `.env` — 12-factor config
- Единый интерфейс репозитория — абстракция над разными драйверами (упрощённо)

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

### Git
- Закоммить изменения дня: `git add week-17/` → `git commit -m "week 17 day 118: Python psycopg2 library CLI"`

### Ловушки
- f-string в SQL: `f"SELECT * FROM users WHERE name = '{name}'"` — injection
- Забытый `conn.commit()` — изменения не сохраняются

---

## День 119 (Вс): Ревью SQL и подготовка к ORM

### Теория
- Views — сохранённые запросы; stored procedures — логика в БД (обзор)
- ACID: Atomicity, Consistency, Isolation, Durability — зачем транзакции
- Isolation levels — read committed vs serializable (обзор)
- [SQL Style Guide](https://www.sqlstyle.guide/) — читаемые запросы
- ORM (неделя 18) — маппинг таблиц на классы Python; плюсы и минусы

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
