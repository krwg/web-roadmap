# Неделя 15: Python — основы

> **Цель недели:** освоить синтаксис Python, структуры данных, функции и изолированное окружение.
> **Литература:** [Python Tutorial](https://docs.python.org/3/tutorial/), [Real Python](https://realpython.com/), «Python. Ускоренный курс» (Теллез)

## День 99 (Пн): Установка, синтаксис, venv

### Теория
- [Installing Python](https://docs.python.org/3/using/index.html) — python.org, PATH
- [venv](https://docs.python.org/3/library/venv.html): `python -m venv .venv`, активация Windows/Mac
- Переменные, типы: `int`, `float`, `str`, `bool`, `None`
- f-strings, `input()`, базовые операторы, `//` и `%`

### Практика
1. Установи Python 3.11+, проверь `python --version`
2. Создай проект `python-basics`, venv, `pip install --upgrade pip`
3. `hello.py` — приветствие по имени из `input()`
4. `calculator.py` — меню: +, -, *, /, выход

**Критерии:**
- [ ] venv активирован, зависимости не в global Python
- [ ] `requirements.txt` пустой или с комментарием (пока без пакетов)
- [ ] Обработка деления на ноль

### Ловушки
- Забытая активация venv — пакеты ставятся глобально
- `input()` всегда возвращает str — нужен `int()` / `float()`

---

## День 100 (Вт): Условия, циклы, comprehensions

### Теория
- `if/elif/else`, truthiness: `[]`, `""`, `0` — falsy
- `for`, `while`, `break`, `continue`, `range()`
- [List comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- `enumerate()`, `zip()` — идиоматичный Python

### Практика
1. FizzBuzz 1–100
2. Таблица умножения 10×10 через nested loops
3. Список квадратов чётных чисел 0–20 через comprehension
4. Игра «Угадай число» с ограничением попыток

**Критерии:**
- [ ] FizzBuzz выводит корректно
- [ ] Хотя бы 2 задачи через comprehension
- [ ] `while` с условием выхода, не `while True` без break

### Ловушки
- Изменение списка во время итерации по нему — пропуск элементов
- `is` vs `==` для сравнения строк и чисел

---

## День 101 (Ср): Функции и type hints

### Теория
- `def`, return, default arguments, `*args`, `**kwargs`
- [Type hints](https://docs.python.org/3/library/typing.html): `def greet(name: str) -> str`
- Docstrings: `"""Описание функции."""`
- Scope: local vs global, `global` keyword (избегай)

### Практика
1. Модуль `utils.py`: `celsius_to_fahrenheit`, `format_currency`, `truncate_text`
2. CLI-конвертер валют (фиксированные курсы в dict)
3. Добавь type hints и docstrings ко всем функциям
4. `if __name__ == "__main__":` — точка входа

**Критерии:**
- [ ] Функции чистые где возможно (без side effects)
- [ ] Type hints на аргументах и return
- [ ] Модуль импортируется без запуска main-логики

### Ловушки
- Mutable default argument `def f(x=[])` — общий список на все вызовы
- Функция без return → `None` неожиданно

---

## День 102 (Чт): Структуры данных — list, tuple, dict, set

### Теория
- [Data structures](https://docs.python.org/3/tutorial/datastructures.html)
- list: mutable, методы `append`, `extend`, `sort`, slicing
- dict: ключи hashable, `.get()`, `.items()`, dict comprehension
- set: уникальность, операции union/intersection
- tuple: immutable, распаковка `a, b = pair`

### Практика
1. Телефонная книга: `dict[name] = phone`, CRUD через меню
2. Подсчёт частоты слов в тексте через `dict`
3. Удаление дубликатов из списка через `set`, сохраняя порядок (bonus)
4. Сортировка списка словарей по ключу `score`

**Критерии:**
- [ ] Телефонная книга persist в JSON-файл
- [ ] `.get()` вместо KeyError для отсутствующих ключей
- [ ] Понимаешь O(1) lookup в dict vs O(n) в list

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

### Практика
1. Расширь телефонную книгу: save/load `contacts.json`
2. Логгер: append строки в `app.log` с timestamp
3. Чтение CSV вручную (split по запятой) → list of dicts
4. Backup: копия JSON перед перезаписью

**Критерии:**
- [ ] Все файлы через `with open`
- [ ] `ensure_ascii=False` для кириллицы в JSON
- [ ] Graceful handling если файл не существует

### Ловушки
- Забытый `encoding='utf-8'` на Windows — кракозябры
- `json.dump` без `indent` — нечитаемый файл для человека

---

## День 104 (Сб): Модули, пакеты, pip

### Теория
- [Modules](https://docs.python.org/3/tutorial/modules.html): `import`, `from ... import`
- Структура пакета: `__init__.py`, относительные импорты
- [pip](https://pip.pypa.io/en/stable/): `pip install`, `requirements.txt`
- [PyPI](https://pypi.org/) — `requests`, `rich` (обзор)

### Практика
1. Разбей телефонную книгу: `models.py`, `storage.py`, `cli.py`
2. `pip install rich` — красивый вывод таблицы контактов
3. `requirements.txt` с `rich==...`
4. Запуск: `python -m phonebook.cli`

**Критерии:**
- [ ] Пакетная структура с `__init__.py`
- [ ] requirements.txt актуален
- [ ] rich Table для list contacts

### Ловушки
- Циклические импорты — раздели слои (models не импортирует cli)
- Имя файла `json.py` — затеняет стандартный модуль

---

## День 105 (Вс): Ревью основ Python

### Теория
- [PEP 8](https://peps.python.org/pep-0008/) — стиль кода
- [Python REPL](https://docs.python.org/3/tutorial/interpreter.html) и `python -i script.py`
- Отличия Python от JavaScript: отступы, typing, None vs null

### Практика
1. Реши 10 задач на [HackerRank Python](https://www.hackerrank.com/domains/python) (Easy)
2. Рефакторинг телефонной книги по PEP 8
3. Напиши шпаргалку: list vs tuple vs dict vs set

**Критерии:**
- [ ] 10 задач HackerRank решены
- [ ] Код проходит `python -m py_compile` без ошибок
- [ ] Шпаргалка в `notes/python-structures.md`

---

## Проект недели

**CLI Expense Tracker** — трекер расходов в терминале:

1. Категории: food, transport, entertainment, other
2. Добавление, список, удаление, сумма по категории, общий итог
3. Хранение в `expenses.json`
4. `rich` — таблица и цветной вывод
5. Фильтр по дате (строка YYYY-MM-DD)

**Критерии:**
- [ ] venv + requirements.txt
- [ ] Модульная структура (≥ 3 файла)
- [ ] Валидация суммы (> 0) и даты
- [ ] README с примерами команд

## Ревью-чеклист
- Зачем venv и чем отличается от global Python?
- list vs tuple — когда использовать каждый?
- Что такое list comprehension и зачем?
- Как работает `with open()`?
- Чем `==` отличается от `is`?
