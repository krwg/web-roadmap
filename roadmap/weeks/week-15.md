# Неделя 15: Python — основы

> **Цель недели:** освоить синтаксис Python, структуры данных, функции и изолированное окружение.
> **Литература:** [Python Tutorial](https://docs.python.org/3/tutorial/), [Real Python](https://realpython.com/), «Python. Ускоренный курс» (Теллез), [PEP 8](https://peps.python.org/pep-0008/), [Python venv](https://docs.python.org/3/library/venv.html)
> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-15/`

## День 99 (Пн): Установка, синтаксис, venv

### Теория
- [Installing Python](https://docs.python.org/3/using/index.html) — python.org, PATH, `py` launcher на Windows
- [venv](https://docs.python.org/3/library/venv.html): `python -m venv .venv`, активация Windows/Mac
- Переменные, типы: `int`, `float`, `str`, `bool`, `None`
- f-strings, `input()`, базовые операторы, `//` и `%`
- Отступы — часть синтаксиса, 4 пробела (PEP 8)
- `python -m pip` — установка в активный venv
- REPL — интерактивная проверка выражений
- Shebang `#!/usr/bin/env python3` — для скриптов (обзор)

### Практика
1. Установи Python 3.11+, проверь `python --version`
2. Создай проект `learning-log/week-15`, venv, `pip install --upgrade pip`
3. `hello.py` — приветствие по имени из `input()`
4. `calculator.py` — меню: +, -, *, /, выход
5. `.gitignore` с `.venv/` и `__pycache__/`
6. Обработка `ValueError` при неверном вводе числа
7. `README.md` с инструкцией активации venv

**Критерии:**
- [ ] venv активирован, зависимости не в global Python
- [ ] `requirements.txt` пустой или с комментарием (пока без пакетов)
- [ ] Обработка деления на ноль

### Git
```bash
cd learning-log/week-15
git add hello.py calculator.py .gitignore README.md
git commit -m "week-15 day-99: venv, hello.py и calculator"
```

### Ловушки
- Забытая активация venv — пакеты ставятся глобально
- `input()` всегда возвращает str — нужен `int()` / `float()`

---

## День 100 (Вт): Условия, циклы, comprehensions

### Теория
- `if/elif/else`, truthiness: `[]`, `""`, `0`, `None` — falsy
- `for`, `while`, `break`, `continue`, `range()`
- [List comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- `enumerate()`, `zip()` — идиоматичный Python
- `else` у цикла `for` — выполняется если не было `break`
- Walrus operator `:=` (3.8+) — присваивание в выражении (обзор)
- Nested comprehensions — читаемость vs краткость
- `pass` — заглушка для пустого блока

### Практика
1. FizzBuzz 1–100
2. Таблица умножения 10×10 через nested loops
3. Список квадратов чётных чисел 0–20 через comprehension
4. Игра «Угадай число» с ограничением попыток
5. `fizzbuzz.py` с функцией `fizzbuzz(n) -> list[str]`
6. Dict comprehension: `{x: x**2 for x in range(10)}`
7. Подсчёт гласных в строке через `for` и `in`

**Критерии:**
- [ ] FizzBuzz выводит корректно
- [ ] Хотя бы 2 задачи через comprehension
- [ ] `while` с условием выхода, не `while True` без break

### Git
```bash
cd learning-log/week-15
git add fizzbuzz.py exercises/
git commit -m "week-15 day-100: FizzBuzz, циклы и comprehensions"
```

### Ловушки
- Изменение списка во время итерации по нему — пропуск элементов
- `is` vs `==` для сравнения строк и чисел

---

## День 101 (Ср): Функции и type hints

### Теория
- `def`, return, default arguments, `*args`, `**kwargs`
- [Type hints](https://docs.python.org/3/library/typing.html): `def greet(name: str) -> str`
- Docstrings: `"""Описание функции."""` — PEP 257
- Scope: local vs global, `global` keyword (избегай)
- Keyword-only arguments после `*`
- `-> None` для функций без return
- `mypy` — статическая проверка типов (обзор, опционально)
- Pure functions — предсказуемость и тестируемость

### Практика
1. Модуль `utils.py`: `celsius_to_fahrenheit`, `format_currency`, `truncate_text`
2. CLI-конвертер валют (фиксированные курсы в dict)
3. Добавь type hints и docstrings ко всем функциям
4. `if __name__ == "__main__":` — точка входа
5. Функция `parse_positive_float(s: str) -> float` с валидацией
6. `*args` demo: `sum_all(*numbers)` 
7. Импорт utils из другого файла — проверь, main не запускается

**Критерии:**
- [ ] Функции чистые где возможно (без side effects)
- [ ] Type hints на аргументах и return
- [ ] Модуль импортируется без запуска main-логики

### Git
```bash
cd learning-log/week-15
git add utils.py currency_converter.py
git commit -m "week-15 day-101: функции, type hints и utils"
```

### Ловушки
- Mutable default argument `def f(x=[])` — общий список на все вызовы
- Функция без return → `None` неожиданно

---

## День 102 (Чт): Структуры данных — list, tuple, dict, set

### Теория
- [Data structures](https://docs.python.org/3/tutorial/datastructures.html)
- list: mutable, методы `append`, `extend`, `sort`, slicing
- dict: ключи hashable, `.get()`, `.items()`, dict comprehension
- set: уникальность, операции union/intersection/difference
- tuple: immutable, распаковка `a, b = pair`, namedtuple (обзор)
- `collections.Counter` — подсчёт элементов (обзор)
- Big-O: dict lookup O(1) avg vs list O(n)
- Копирование: `copy()`, `list()`, shallow vs deep

### Практика
1. Телефонная книга: `dict[name] = phone`, CRUD через меню
2. Подсчёт частоты слов в тексте через `dict`
3. Удаление дубликатов из списка через `set`, сохраняя порядок (bonus)
4. Сортировка списка словарей по ключу `score`
5. `phonebook.py` — функции add, remove, search, list_all
6. Поиск по частичному совпадению имени
7. Валидация формата телефона (простой regex или len)

**Критерии:**
- [ ] Телефонная книга persist в JSON-файл
- [ ] `.get()` вместо KeyError для отсутствующих ключей
- [ ] Понимаешь O(1) lookup в dict vs O(n) в list

### Git
```bash
cd learning-log/week-15
git add phonebook.py
git commit -m "week-15 day-102: телефонная книга и структуры данных"
```

### Ловушки
- Использование list как ключа dict — TypeError (unhashable)
- `list.sort()` vs `sorted(list)` — in-place vs новый список

---

## День 103 (Пт): Работа с файлами и JSON

### Теория
- `open()`, context manager `with open(...) as f`
- modes: `r`, `w`, `a`, encoding `utf-8`
- [json module](https://docs.python.org/3/library/json.html): `load`, `dump`, `loads`, `dumps`
- Обработка `FileNotFoundError`, `JSONDecodeError`
- `pathlib.Path` — современный путь к файлам (обзор)
- `ensure_ascii=False`, `indent=2` для читаемого JSON
- Atomic write: запись во временный файл + rename (bonus)
- Логирование vs print — `logging` module (обзор)

### Практика
1. Расширь телефонную книгу: save/load `contacts.json`
2. Логгер: append строки в `app.log` с timestamp
3. Чтение CSV вручную (split по запятой) → list of dicts
4. Backup: копия JSON перед перезаписью
5. `storage.py` — функции `load_contacts()`, `save_contacts(data)`
6. Graceful start если `contacts.json` не существует
7. Импорт контактов из CSV файла

**Критерии:**
- [ ] Все файлы через `with open`
- [ ] `ensure_ascii=False` для кириллицы в JSON
- [ ] Graceful handling если файл не существует

### Git
```bash
cd learning-log/week-15
git add storage.py data/
git commit -m "week-15 day-103: JSON persist, логгер и CSV import"
```

### Ловушки
- Забытый `encoding='utf-8'` на Windows — кракозябры
- `json.dump` без `indent` — нечитаемый файл для человека

---

## День 104 (Сб): Модули, пакеты, pip

### Теория
- [Modules](https://docs.python.org/3/tutorial/modules.html): `import`, `from ... import`
- Структура пакета: `__init__.py`, относительные импорты
- [pip](https://pip.pypa.io/en/stable/): `pip install`, `requirements.txt`, `pip freeze`
- [PyPI](https://pypi.org/) — `requests`, `rich` (обзор)
- `python -m package.module` — запуск как модуль
- `__all__` — публичный API пакета
- Виртуальное окружение и reproducible builds
- Pin versions в requirements: `rich==13.x.x`

### Практика
1. Разбей телефонную книгу: `models.py`, `storage.py`, `cli.py`
2. `pip install rich` — красивый вывод таблицы контактов
3. `requirements.txt` с `rich==...`
4. Запуск: `python -m phonebook.cli`
5. Пакет `phonebook/` с `__init__.py`
6. Rich Table для `list contacts` с колонками name, phone
7. Цветной вывод ошибок через `rich.print`

**Критерии:**
- [ ] Пакетная структура с `__init__.py`
- [ ] requirements.txt актуален
- [ ] rich Table для list contacts

### Git
```bash
cd learning-log/week-15
git add phonebook/ requirements.txt
git commit -m "week-15 day-104: пакет phonebook и rich CLI"
```

### Ловушки
- Циклические импорты — раздели слои (models не импортирует cli)
- Имя файла `json.py` — затеняет стандартный модуль

---

## День 105 (Вс): Ревью основ Python

### Теория
- [PEP 8](https://peps.python.org/pep-0008/) — стиль кода, именование, длина строк
- [Python REPL](https://docs.python.org/3/tutorial/interpreter.html) и `python -i script.py`
- Отличия Python от JavaScript: отступы, typing, None vs null, truthiness
- Подготовка к CLI Expense Tracker — финальный проект недели
- `python -m py_compile` — проверка синтаксиса
- HackerRank / Codewars — практика алгоритмов
- Документация проекта: README, примеры команд

### Практика
1. Реши 10 задач на [HackerRank Python](https://www.hackerrank.com/domains/python) (Easy)
2. Рефакторинг телефонной книги по PEP 8
3. Напиши шпаргалку: list vs tuple vs dict vs set
4. Начни скелет **CLI Expense Tracker** — `expense_tracker/`
5. `notes/python-structures.md` — шпаргалка структур
6. Прогони `python -m py_compile` на всех модулях
7. Тег `week-15-done`

**Критерии:**
- [ ] 10 задач HackerRank решены
- [ ] Код проходит `python -m py_compile` без ошибок
- [ ] Шпаргалка в `notes/python-structures.md`

### Git
```bash
cd learning-log/week-15
git add notes/ expense_tracker/
git commit -m "week-15 day-105: HackerRank, PEP 8 и Expense Tracker скелет"
```

---

## Проект недели

**CLI Expense Tracker** — трекер расходов в терминале. Подробное ТЗ: [docs/projects.md — Неделя 15](../../docs/projects.md#неделя-15--cli-expense-tracker).

1. Категории: food, transport, entertainment, other
2. Добавление, список, удаление, сумма по категории, общий итог
3. Хранение в `expenses.json`
4. `rich` — таблица и цветной вывод
5. Фильтр по дате (строка YYYY-MM-DD)

**Функции:**
- CLI-меню или subcommands: add, list, delete, summary, filter
- Валидация суммы (> 0) и формата даты
- Сводка по категориям с итогами
- Цветной вывод: доход зелёный, расход красный (опционально)

**Критерии:**
- [ ] venv + requirements.txt с pinned versions
- [ ] Модульная структура (≥ 3 файла: models, storage, cli)
- [ ] Валидация суммы (> 0) и даты
- [ ] README с примерами команд
- [ ] rich Table для списка расходов
- [ ] Persist в JSON, переживает перезапуск
- [ ] Тег `week-15-done`

## Ревью-чеклист
- Зачем venv и чем отличается от global Python?
- list vs tuple — когда использовать каждый?
- Что такое list comprehension и зачем?
- Как работает `with open()`?
- Чем `==` отличается от `is`?
