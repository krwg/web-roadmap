# SQL & PostgreSQL — шпаргалка

> После недели 17.

## CRUD

```sql
SELECT id, title FROM tasks WHERE user_id = $1 ORDER BY created_at DESC;
INSERT INTO tasks (title, user_id) VALUES ($1, $2) RETURNING *;
UPDATE tasks SET done = true WHERE id = $1 AND user_id = $2;
DELETE FROM tasks WHERE id = $1 AND user_id = $2;
```

## JOIN

```sql
SELECT b.title, a.name FROM books b
JOIN authors a ON b.author_id = a.id;
```

## Индексы

```sql
CREATE INDEX idx_tasks_user ON tasks(user_id);
EXPLAIN ANALYZE SELECT ...;
```

## Нормализация (кратко)

- 1NF: атомарные значения
- 2NF: нет частичных зависимостей от составного ключа
- 3NF: нет транзитивных зависимостей

## Транзакции

```sql
BEGIN;
-- ops
COMMIT; -- или ROLLBACK;
```

## Миграции

Версионируй схему: `schema.sql`, `migrations/001_*.sql`, seed отдельно.
