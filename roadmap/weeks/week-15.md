# Неделя 15: Python — основы



> **Цель недели:** освоить синтаксис Python, структуры данных, функции и изолированное окружение.

> **Литература:** [Python Tutorial](https://docs.python.org/3/tutorial/), [Real Python](https://realpython.com/), «Python. Ускоренный курс» (Теллез), [PEP 8](https://peps.python.org/pep-0008/), [Python venv](https://docs.python.org/3/library/venv.html)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)

> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-15/`



## День 99 (Пн): Установка, синтаксис, venv
<a id="week-15-day-99"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Expense Tracker**

### Теория

Python — первый шаг в backend после фронтенда. Установка с python.org (или `py` launcher на Windows) и проверка `python --version` — база. Главная привычка с первого дня: виртуальное окружение `python -m venv .venv` изолирует зависимости проекта от системного Python. Без активации venv пакеты ставятся глобально и ломают другие проекты.

Синтаксис Python читается почти как псевдокод: отступы (4 пробела, PEP 8) — часть языка, не стиль. Типы: `int`, `float`, `str`, `bool`, `None`. f-strings (`f"Привет, {name}"`) — современный способ форматирования. `input()` всегда возвращает строку — для чисел нужен `int()` или `float()` с обработкой `ValueError`.

Операторы `//` (целочисленное деление) и `%` (остаток) пригодятся в задачах. REPL (`python` без аргументов) — быстрая проверка выражений. `python -m pip install` ставит пакеты в активный venv. Shebang `#!/usr/bin/env python3` полезен для скриптов на Unix, на Windows — вторично.

**Читать:**

- [Installing Python](https://docs.python.org/3/using/index.html)
- [venv](https://docs.python.org/3/library/venv.html)
- [PEP 8](https://peps.python.org/pep-0008/)

**Ключевая мысль:** venv на каждый проект; `input()` — всегда str, отступы — синтаксис.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

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
<a id="week-15-day-100"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Expense Tracker**

### Теория

Условия и циклы — скелет любой программы. `if/elif/else` опирается на truthiness: пустой список `[]`, строка `""`, ноль `0` и `None` — falsy. Это отличается от JavaScript, где только некоторые значения falsy. Циклы `for` итерируют по итерируемым объектам; `while` — пока условие истинно; `break` и `continue` управляют потоком.

`range(n)` генерирует последовательность без создания списка в памяти. `enumerate(items)` даёт пары (индекс, элемент) — идиоматичнее, чем `for i in range(len(items))`. `zip(a, b)` объединяет два списка попарно. У цикла `for` есть необязательный `else`, выполняющийся, если не было `break` — редкий, но полезный приём.

List comprehension `[x**2 for x in range(10) if x % 2 == 0]` компактно строит список. Не увлекайся вложенностью — читаемость важнее одной строки. Walrus `:=` (3.8+) присваивает в выражении. Не изменяй список во время итерации по нему — пропустишь элементы.

**Читать:**

- [List comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [More control flow](https://docs.python.org/3/tutorial/controlflow.html)
- [Truth Value Testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)

**Ключевая мысль:** comprehension — сахар над циклом; `is` vs `==` — разные вещи для объектов.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

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
<a id="week-15-day-101"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Expense Tracker**

### Теория

Функции в Python — первый уровень абстракции. `def name(args) -> return_type:` с type hints документирует контракт для IDE и будущего `mypy`. Docstring в тройных кавычках (PEP 257) объясняет назначение, аргументы и возвращаемое значение. `if __name__ == "__main__":` отделяет точку входа от импортируемого модуля.

Аргументы по умолчанию должны быть immutable: `def f(x=[])` — антипаттерн, один список на все вызовы. Используй `None` и создавай список внутри. `*args` собирает позиционные аргументы, `**kwargs` — именованные. После `*` в сигнатуре — только keyword-only аргументы.

Чистые функции (без side effects) проще тестировать: `celsius_to_fahrenheit(0)` всегда даёт 32.0. Функция без `return` неявно возвращает `None` — частая ловушка. Scope: избегай `global`, передавай данные аргументами.

**Читать:**

- [Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Type hints](https://docs.python.org/3/library/typing.html)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)

**Ключевая мысль:** mutable default argument — баг; type hints и docstrings — часть API функции.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

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
<a id="week-15-day-102"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Expense Tracker**

### Теория

Выбор структуры данных определяет скорость и читаемость кода. `list` — упорядоченная изменяемая коллекция: `append`, `extend`, срезы `lst[1:3]`, сортировка in-place (`sort`) или новый список (`sorted`). `dict` — словарь по hashable-ключам: lookup в среднем O(1) против O(n) у списка. `.get(key, default)` безопаснее прямого `dict[key]`.

`set` хранит уникальные элементы и поддерживает union, intersection, difference — удобно для удаления дубликатов. `tuple` неизменяем: подходит для координат, записей из БД, ключей словаря. `collections.Counter` ускоряет подсчёт частот. Копирование: `copy.copy` — shallow, `copy.deepcopy` — вложенные структуры.

Телефонная книга на `dict[name] = phone` — классический CRUD. Список нельзя использовать как ключ dict (unhashable). Для сортировки списка словарей: `sorted(items, key=lambda x: x['score'])`.

**Читать:**

- [Data structures](https://docs.python.org/3/tutorial/datastructures.html)
- [dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
- [collections.Counter](https://docs.python.org/3/library/collections.html#collections.Counter)

**Ключевая мысль:** dict для поиска по ключу, list для порядка; выбор структуры — это Big-O.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

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
<a id="week-15-day-103"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Expense Tracker**

### Теория

Файлы и JSON — мост между программой и диском. Context manager `with open(path, 'r', encoding='utf-8') as f:` гарантирует закрытие файла даже при исключении. На Windows `encoding='utf-8'` критичен для кириллицы. Режимы: `r` чтение, `w` перезапись, `a` дополнение в конец.

Модуль `json`: `load`/`dump` для файлов, `loads`/`dumps` для строк. `ensure_ascii=False` сохраняет Unicode, `indent=2` делает файл читаемым для человека. Обрабатывай `FileNotFoundError` (первый запуск) и `JSONDecodeError` (битый файл) — graceful start важнее краша.

`pathlib.Path` — современная альтернатива строковым путям: `Path('data') / 'contacts.json'`. Atomic write (запись во временный файл + rename) защищает от потери данных при сбое. Для отладки — `print`, для production — модуль `logging` с уровнями.

**Читать:**

- [Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [json module](https://docs.python.org/3/library/json.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)

**Ключевая мысль:** всегда `with open` и `encoding='utf-8'`; JSON — контракт persist между запусками.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

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
<a id="week-15-day-104"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Expense Tracker**

### Теория

Модули и пакеты масштабируют код за пределы одного файла. `import module` и `from package import name` — два стиля; второй удобнее, но может засорить namespace. Пакет — папка с `__init__.py` (в Python 3.3+ namespace packages возможны без него, но для учебных проектов `__init__.py` явно). `__all__` объявляет публичный API пакета.

`pip install package` ставит зависимости в venv; `pip freeze > requirements.txt` фиксирует версии для воспроизводимых сборок. Pin versions (`rich==13.x.x`) защищает от неожиданных breaking changes. PyPI — реестр пакетов: `requests`, `rich` и тысячи других.

Запуск `python -m phonebook.cli` выполняет модуль как скрипт с корректными относительными импортами. Избегай циклических импортов: `models` не должен импортировать `cli`. Не называй файл `json.py` — затенишь стандартный модуль.

**Читать:**

- [Modules](https://docs.python.org/3/tutorial/modules.html)
- [pip documentation](https://pip.pypa.io/en/stable/)
- [PyPI](https://pypi.org/)
- [rich](https://rich.readthedocs.io/)

**Ключевая мысль:** пакетная структура + `requirements.txt` — основа любого Python-проекта.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

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
<a id="week-15-day-105"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Expense Tracker**

### Теория

Ревью недели закрепляет фундамент перед CLI Expense Tracker. PEP 8 — не догма, а общий язык: snake_case для функций и переменных, 79–88 символов в строке, два пустых ряда между top-level определениями. `python -m py_compile file.py` проверяет синтаксис без запуска.

Сравни Python с JavaScript: отступы вместо `{}`, `None` вместо `null`, иная truthiness, явный `self` в методах. HackerRank/Codewars на Easy уровне тренируют синтаксис вне контекста проекта. Шпаргалка list vs tuple vs dict vs set — шпаргалка на всю карьеру.

CLI Expense Tracker объединяет всё: venv, модули, JSON persist, rich для таблиц, валидацию ввода. README с примерами команд — обязателен. Осмысленные коммиты за 7 дней и тег `week-15-done` завершают неделю.

**Читать:**

- [PEP 8](https://peps.python.org/pep-0008/)
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [HackerRank Python](https://www.hackerrank.com/domains/python)

**Ключевая мысль:** Python-проект = venv + модули + persist + README; стиль PEP 8 с первого коммита.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

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


## Проверь себя

<details>
<summary>Что должно получиться к концу недели?</summary>

Работающий проект **CLI Expense Tracker** в `learning-log/week-15/`, осмысленная Git-история, тег `week-15-done`.

</details>

<details>
<summary>Главный навык недели одной фразой?</summary>

Python основы и CLI

</details>

<details>
<summary>Можно ли пропустить день?</summary>

Нет — дни связаны. В **лайт-режиме** сократи практику до MVP, но теорию и Git-коммит не пропускай.

</details>
