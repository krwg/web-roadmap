# Неделя 17: SQL, PostgreSQL, индексы

> **Цель недели:** освоить реляционные БД, SQL-запросы, PostgreSQL и оптимизацию через индексы.
> **Литература:** [SQLBolt](https://sqlbolt.com/), [PostgreSQL Tutorial](https://www.postgresqltutorial.com/), [Use The Index, Luke](https://use-the-index-luke.com/)

## День 113 (Пн): SQL основы — SELECT, фильтрация, сортировка

### Теория
- [W3Schools SQL](https://www.w3schools.com/sql/) или [SQLBolt Lessons 1–6](https://sqlbolt.com/lesson/select_queries_introduction)
- SELECT, WHERE, ORDER BY, LIMIT, DISTINCT
- Операторы: `=`, `<>`, `IN`, `BETWEEN`, `LIKE`, `IS NULL`
- Агрегаты: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, `HAVING`

### Практика
1. Установи [DB Browser for SQLite](https://sqlitebrowser.org/) или используй `sqlite3` CLI
2. Создай БД «shop»: `products`, `categories`, `orders`
3. 10+ SELECT-запросов: топ-5 дорогих, средняя цена, count по категории
4. Запрос с `GROUP BY` и `HAVING count(*) > 2`

**Критерии:**
- [ ] Схема с PRIMARY KEY
- [ ] ≥ 10 осмысленных запросов в `queries.sql`
- [ ] Понимаешь разницу WHERE vs HAVING

### Ловушки
- SELECT * в production — выбирай нужные колонки
- GROUP BY без агрегата в SELECT — ошибка в строгом SQL

---

## День 114 (Вт): JOIN, INSERT, UPDATE, DELETE

### Теория
- [SQLBolt — JOINs](https://sqlbolt.com/lesson/table_joins)
- INNER JOIN vs LEFT JOIN — когда какой
- INSERT, UPDATE, DELETE с WHERE
- FOREIGN KEY, REFERENCES, ON DELETE CASCADE / SET NULL
- Транзакции: BEGIN, COMMIT, ROLLBACK

### Практика
1. Расширь shop: `customers`, `order_items`
2. Запрос: заказы с именами клиентов (INNER JOIN)
3. Клиенты без заказов (LEFT JOIN + WHERE orders.id IS NULL)
4. UPDATE цены категории «sale» -10%, DELETE тестовых записей в транзакции

**Критерии:**
- [ ] FOREIGN KEY между таблицами
- [ ] JOIN-запрос возвращает ожидаемые строки
- [ ] DELETE только с WHERE (не без него!)

### Ловушки
- DELETE/UPDATE без WHERE — катастрофа
- Cartesian product — забытый ON в JOIN

---

## День 115 (Ср): Нормализация и проектирование схемы

### Теория
- 1NF, 2NF, 3NF — практический смысл
- One-to-many, many-to-many (junction table)
- [Database Design](https://www.postgresqltutorial.com/postgresql-get-started/postgresql-sample-database/) — примеры
- Именование: snake_case, singular vs plural tables (выбери конвенцию)

### Практика
1. Спроектируй БД «Библиотека»: authors, books, borrowers, loans
2. ER-диаграмма на бумаге или [dbdiagram.io](https://dbdiagram.io/)
3. CREATE TABLE с constraints: NOT NULL, UNIQUE, CHECK
4. Seed data: 5 авторов, 20 книг, 3 заёмщика, 10 займов

**Критерии:**
- [ ] Нет дублирования author name в books
- [ ] Junction table для many-to-many (если нужна)
- [ ] ER-диаграмма в repo

### Ловушки
- Хранение списка id в одной колонке CSV — антипаттерн
- Nullable всего подряд — потеря целостности данных

---

## День 116 (Чт): PostgreSQL — установка и отличия от SQLite

### Теория
- [PostgreSQL Downloads](https://www.postgresql.org/download/)
- Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=pass postgres:16`
- Типы: SERIAL/BIGSERIAL, VARCHAR, TEXT, TIMESTAMP, TIMESTAMPTZ, JSONB, UUID
- [psql](https://www.postgresql.org/docs/current/app-psql.html), pgAdmin, DBeaver

### Практика
1. Подними PostgreSQL (Docker или локально)
2. Перенеси схему «Библиотека» в PostgreSQL
3. Подключись через psql или DBeaver
4. Сравни: SQLite vs PG — когда что использовать (запиши 5 пунктов)

**Критерии:**
- [ ] Подключение к PG работает
- [ ] Схема создана через SQL-скрипт `schema.sql`
- [ ] Seed script `seed.sql` выполняется без ошибок

### Ловушки
- Забытый пароль postgres в Docker — документируй в `.env.example`
- Различия SQL диалектов: AUTOINCREMENT vs SERIAL

---

## День 117 (Пт): Индексы и EXPLAIN ANALYZE

### Теория
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- B-tree index — default, когда помогает WHERE/JOIN/ORDER BY
- [EXPLAIN ANALYZE](https://www.postgresql.org/docs/current/sql-explain.html) — Seq Scan vs Index Scan
- [Use The Index, Luke](https://use-the-index-luke.com/) — глава 1–2

### Практика
1. Таблица `books` с 10 000+ строк (скрипт генерации)
2. Запрос `WHERE title LIKE 'Python%'` — EXPLAIN без индекса
3. `CREATE INDEX idx_books_title ON books(title)`
4. Повтори EXPLAIN — сравни cost и время

**Критерии:**
- [ ] Индекс создан на колонке поиска
- [ ] EXPLAIN показывает Index Scan (или объясни почему Seq Scan)
- [ ] Записаны выводы в `notes/indexes.md`

### Ловушки
- Индекс на каждую колонку — замедляет INSERT/UPDATE
- `LIKE '%python'` — индекс B-tree не поможет (leading wildcard)

---

## День 118 (Сб): SQLite/PostgreSQL из Python

### Теория
- [sqlite3 module](https://docs.python.org/3/library/sqlite3.html)
- [psycopg2](https://www.psycopg.org/docs/) или psycopg3 — подключение к PG
- Connection pool (обзор), context managers
- Параметризованные запросы: `cursor.execute("SELECT * FROM books WHERE id = %s", (id,))`

### Практика
1. Расширь CLI Task Manager: опция `--db postgres` vs sqlite
2. `DATABASE_URL` из `.env`
3. Репозиторий с единым интерфейсом для обеих БД (упрощённо)
4. Миграция данных sqlite → postgres (скрипт)

**Критерии:**
- [ ] Нет SQL injection — только placeholders
- [ ] `with conn:` или try/finally close
- [ ] .env.example с DATABASE_URL

### Ловушки
- f-string в SQL: `f"SELECT * FROM users WHERE name = '{name}'"` — injection
- Забытый `conn.commit()` — изменения не сохраняются

---

## День 119 (Вс): Ревью SQL и подготовка к ORM

### Теория
- Views, stored procedures — обзор (не обязательно писать)
- ACID, isolation levels — обзор
- [SQL Style Guide](https://www.sqlstyle.guide/)

### Практика
1. 15 вопросов SQLBolt — пройди без подсказок
2. 15 вопросов SQLBolt — пройди без подсказок
3. Установи `pip install sqlalchemy fastapi uvicorn` в venv

**Критерии:**
- [ ] 5 сложных запросов с JOIN и агрегатами
- [ ] Ответы на «INNER vs LEFT JOIN» письменно
- [ ] venv готов для недели 18

---

## Проект недели

**База «Библиотека»** — полный SQL-проект:

1. PostgreSQL: authors, books, borrowers, loans
2. `schema.sql`, `seed.sql`, `queries.sql` (15+ запросов)
3. Индекс на `books.title`, EXPLAIN до/после
4. Python-скрипт `library_cli.py` — 3 операции через psycopg2
5. ER-диаграмма в README

**Критерии:**
- [ ] FK constraints работают
- [ ] Запрос «кто не вернул книгу» корректен
- [ ] Индекс документирован с замерами
- [ ] docker-compose только для postgres (опционально)

## Ревью-чеклист
- INNER JOIN vs LEFT JOIN — пример каждого?
- Зачем PRIMARY KEY и FOREIGN KEY?
- Что показывает EXPLAIN ANALYZE?
- Как защититься от SQL injection?
- PostgreSQL vs SQLite — 3 случая когда PG?
