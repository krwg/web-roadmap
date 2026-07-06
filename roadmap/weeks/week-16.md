# Неделя 16: Python — ООП, алгоритмы, файлы

> **Цель недели:** освоить объектно-ориентированный Python, оценку сложности и работу с файловой системой.
> **Литература:** [Python OOP](https://docs.python.org/3/tutorial/classes.html), [Real Python — pathlib](https://realpython.com/python-pathlib/), [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)

## День 106 (Пн): Классы и объекты

### Теория
- [Classes](https://docs.python.org/3/tutorial/classes.html): `class`, `__init__`, `self`
- Атрибуты экземпляра vs атрибуты класса
- Методы экземпляра, `@classmethod`, `@staticmethod` — когда что
- `__str__` и `__repr__` для читаемого вывода

### Практика
1. Класс `BankAccount`: `deposit`, `withdraw`, `balance`, защита от отрицательного баланса
2. Класс `Transaction` с датой, суммой, типом
3. Список счетов, перевод между счетами
4. `print(account)` использует `__str__`

**Критерии:**
- [ ] Инкапсуляция: баланс не меняется напрямую снаружи
- [ ] `__repr__` для отладки
- [ ] Type hints на методах

### Ловушки
- Забытый `self` в методах — TypeError
- Публичные атрибуты вместо свойств — нарушение инкапсуляции

---

## День 107 (Вт): Наследование, композиция, dataclasses

### Теория
- Наследование: `class Savings(BankAccount)`, `super()`
- [Композиция vs наследование](https://realpython.com/inheritance-composition-python/)
- [@dataclass](https://docs.python.org/3/library/dataclasses.html) — boilerplate для data objects
- `__post_init__` для валидации

### Практика
1. `SavingsAccount` с `interest_rate`, метод `apply_interest()`
2. `Portfolio` содержит list of `Account` (композиция)
3. `@dataclass Expense` из недели 15 — рефакторинг
4. ABC обзор: `from abc import ABC, abstractmethod` (опционально)

**Критерии:**
- [ ] `super().__init__()` в дочернем классе
- [ ] Portfolio не наследует Account — композиция
- [ ] dataclass с валидацией суммы > 0

### Ловушки
- Глубокая иерархия наследования — хрупкий дизайн
- dataclass mutable по умолчанию — `frozen=True` для immutable

---

## День 108 (Ср): Магические методы и итераторы

### Теория
- Dunder methods: `__len__`, `__getitem__`, `__eq__`, `__lt__`
- [Emulating container types](https://docs.python.org/3/reference/datamodel.html#emulating-container-types)
- Итератор: `__iter__`, `__next__`, `StopIteration`
- Generator functions: `yield` вместо списка в памяти

### Практика
1. Класс `Playlist` с `__len__`, `__getitem__`, итерацией по трекам
2. Generator `fibonacci(n)` — первые n чисел без хранения всего списка
3. `Playlist` поддерживает `for track in playlist`
4. Перегрузка `==` для сравнения Transaction по id

**Критерии:**
- [ ] Playlist итерируется в for-loop
- [ ] Generator не хранит весь ряд Фибоначчи в памяти
- [ ] `__eq__` согласован с hash (если используешь в set)

### Ловушки
- `__eq__` без `__hash__` — объект не hashable для set/dict keys
- Бесконечный generator без условия остановки

---

## День 109 (Чт): Алгоритмы и Big O

### Теория
- [Big O notation](https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/how-to-create-an-object-graph): O(1), O(n), O(n²), O(log n)
- list lookup O(n) vs dict lookup O(1)
- Сортировки: bubble O(n²) vs built-in Timsort O(n log n)
- [VisuAlgo](https://visualgo.net/) — визуализация алгоритмов

### Практика
1. Реализуй linear search и binary search (sorted list)
2. Замерь время на списке 10⁴ и 10⁶ элементов (`time.perf_counter`)
3. Two Sum: brute force O(n²) vs hash map O(n)
4. Напиши таблицу: операция → сложность для list, dict, set

**Критерии:**
- [ ] Binary search работает только на sorted input
- [ ] Замеры подтверждают разницу O(n) vs O(n²)
- [ ] Two Sum hash map решение за один проход

### Ловушки
- Binary search на unsorted list — неверный результат
- Путаница best/average/worst case — указывай worst

---

## День 110 (Пт): pathlib и работа с файловой системой

### Теория
- [pathlib](https://docs.python.org/3/library/pathlib.html): `Path`, `/` operator
- `path.read_text()`, `path.write_text()`, `path.exists()`, `glob()`, `rglob()`
- `shutil` — copy, move, rmtree
- Кроссплатформенные пути vs строковая конкатенация

### Практика
1. Скрипт `organize.py` — сортирует файлы по расширению в папки
2. Рекурсивный поиск `*.py` через `rglob`
3. Подсчёт размера директории в MB
4. Безопасное создание: `path.mkdir(parents=True, exist_ok=True)`

**Критерии:**
- [ ] Только pathlib, не `os.path` (кроме env vars)
- [ ] Dry-run режим: `--dry-run` показывает план без перемещения
- [ ] Обработка PermissionError

### Ловушки
- `path.write_text()` перезаписывает без confirm — сделай backup
- Относительные пути зависят от cwd — используй `Path(__file__).parent`

---

## День 111 (Сб): regex и обработка текстовых логов

### Теория
- [re module](https://docs.python.org/3/library/re.html): `match`, `search`, `findall`, `sub`
- Паттерны: `\d+`, `\w+`, группы `()`, raw strings `r"..."`
- Чтение больших файлов построчно — не `read()` всего файла
- [regex101.com](https://regex101.com/) — тестирование паттернов

### Практика
1. Генератор mock `server.log` (1000 строк: timestamp, level, message)
2. Парсер: извлечь все ERROR с датой
3. Топ-5 часов с наибольшим числом ERROR
4. Замена IP-адресов на `[REDACTED]` в копии лога

**Критерии:**
- [ ] Парсинг построчно (memory-efficient)
- [ ] regex с named groups для timestamp и level
- [ ] Итоговая статистика в читаемом виде

### Ловушки
- `re.match` только с начала строки — для поиска везде `re.search`
- Жадные квантификаторы `.*` — неожиданные совпадения

---

## День 112 (Вс): Ревью ООП и алгоритмов

### Теория
- SOLID — обзор (S и O достаточно на junior уровне)
- Когда ООП, когда функции + dataclasses
- [LeetCode Easy](https://leetcode.com/problemset/) — Python тег (обзор)

### Практика
1. Реши 3 задачи LeetCode Easy: Two Sum, Valid Parentheses, Merge Sorted Array
2. Рефакторинг Expense Tracker на классы `Expense`, `ExpenseStore`
3. Напиши ответы: «3 магических метода и зачем»
4. Подготовь venv для SQL (неделя 17)

**Критерии:**
- [ ] 3 LeetCode задачи приняты
- [ ] ExpenseStore с save/load через pathlib
- [ ] Конспект Big O на 1 страницу

---

## Проект недели

**CLI Task Manager (SQLite)** — расширенная версия с ООП:

1. Классы: `Task`, `TaskRepository` (SQLite), `TaskCLI`
2. CRUD через `sqlite3`, параметризованные запросы (`?`)
3. Теги many-to-many: `tasks`, `tags`, `task_tags`
4. `rich` — таблица, цвет по статусу
5. Транзакции: `try/except` + `rollback`

**Критерии:**
- [ ] ORM не используем — чистый sqlite3 (ORM на нед. 18)
- [ ] Все SQL с placeholders, не f-string
- [ ] Поиск и фильтр по статусу/тегу
- [ ] README + схема БД

## Ревью-чеклист
- `__init__` vs `__new__` — в чём разница (обзор)?
- list.pop(0) — какая сложность и почему?
- Когда dataclass, когда полноценный class?
- pathlib vs os.path — что предпочтительнее в 2024+?
- Как защититься от SQL injection в sqlite3?
