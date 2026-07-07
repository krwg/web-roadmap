# Неделя 16: Python — ООП, алгоритмы, файлы

> **Цель недели:** освоить объектно-ориентированный Python, оценку сложности и работу с файловой системой.
> **Литература:** [Python OOP](https://docs.python.org/3/tutorial/classes.html), [Real Python — pathlib](https://realpython.com/python-pathlib/), [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)
> **Проект недели:** [CLI Task Manager (SQLite)](../../docs/projects.md#неделя-16--cli-task-manager-sqlite) — классы `Task`, `TaskRepository`, CRUD через `sqlite3`, теги many-to-many.
> **Git:** папка `learning-log/week-16/`, минимум 1 осмысленный коммит в день; к концу недели тег `week-16-done`.

## День 106 (Пн): Классы и объекты
<a id="week-16-day-106"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Task Manager**

### Теория

Объектно-ориентированное программирование в Python объединяет данные и поведение в одной сущности — классе. `class BankAccount:` с методом `__init__(self, ...)` инициализирует экземпляр; `self` — ссылка на конкретный объект. Атрибуты экземпляра (`self.balance`) хранят состояние; атрибуты класса (`currency = 'RUB'`) — общие настройки для всех счетов.

Три вида методов: обычные (работают с `self`), `@classmethod` (альтернативные конструкторы, фабрики), `@staticmethod` (утилиты без доступа к экземпляру). `__str__` — для пользователя (`print(account)`), `__repr__` — для отладки в REPL, должен однозначно идентифицировать объект.

Инкапсуляция в Python — соглашение: префикс `_balance` сигнализирует «не трогай снаружи», `@property` даёт контролируемое чтение без прямой мутации. Type hints на методах помогают IDE ловить ошибки до запуска. Баланс меняется только через `deposit` и `withdraw` — это и есть защита инвариантов.

**Читать:**

- [Classes](https://docs.python.org/3/tutorial/classes.html)
- [@property](https://docs.python.org/3/library/functions.html#property)
- [Real Python — OOP](https://realpython.com/python3-object-oriented-programming/)

**Ключевая мысль:** класс = данные + поведение; `self` обязателен; инкапсуляция через методы, не публичные поля.

### Практика
1. Класс `BankAccount`: `deposit`, `withdraw`, `balance`, защита от отрицательного баланса
2. Класс `Transaction` с датой, суммой, типом (`deposit` / `withdraw`)
3. Список счетов, перевод между счетами с записью двух транзакций
4. `print(account)` использует `__str__`, в отладке — `repr(account)`
5. Добавь `@property balance` — чтение без setter, изменение только через методы
6. Напиши 3 unit-подобных assert-теста в `if __name__ == "__main__"` для happy path и ошибок

**Критерии:**
- [ ] Инкапсуляция: баланс не меняется напрямую снаружи
- [ ] `__repr__` однозначно идентифицирует объект
- [ ] Type hints на аргументах и return всех публичных методов

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 106: BankAccount and Transaction classes"`

### Ловушки
- Забытый `self` в методах — TypeError
- Публичные атрибуты вместо свойств — нарушение инкапсуляции

---

## День 107 (Вт): Наследование, композиция, dataclasses
<a id="week-16-day-107"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Task Manager**

### Теория

Наследование (`class Savings(BankAccount)`) расширяет базовый класс: дочерний получает методы родителя и добавляет свои. `super().__init__(...)` вызывает конструктор родителя — забудешь, и поля родителя не инициализируются. Но глубокие иерархии хрупки: предпочитай композицию («has-a»), когда объект содержит другие объекты, а не наследует их («is-a»).

`Portfolio` с `list[Account]` — композиция: портфель не «является» счётом, он их «содержит». Это гибче, чем `class Portfolio(Account)`. `@dataclass` автогенерирует `__init__`, `__repr__`, `__eq__` для DTO без сложного поведения — идеально для `Expense` или `Task`.

`__post_init__` валидирует поля после создания dataclass (сумма > 0). `frozen=True` делает объект immutable — безопасен как ключ dict. ABC (`ABC`, `@abstractmethod`) задаёт контракт для `TaskRepository` — подкласс обязан реализовать методы.

**Читать:**

- [Inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance)
- [Композиция vs наследование](https://realpython.com/inheritance-composition-python/)
- [@dataclass](https://docs.python.org/3/library/dataclasses.html)

**Ключевая мысль:** композиция чаще наследования; dataclass — для данных, class — для поведения.

### Практика
1. `SavingsAccount` с `interest_rate`, метод `apply_interest()` через `super()`
2. `Portfolio` содержит `list[Account]` — композиция, не наследование
3. Рефакторинг `@dataclass Expense` из недели 15 с `__post_init__` валидацией
4. Абстрактный `BaseRepository` с `get`, `add`, `delete` — заготовка для SQLite
5. Сравни размер кода: dataclass vs ручной класс для `Expense`
6. Задокументируй в `notes/oop.md`: когда наследование, когда композиция

**Критерии:**
- [ ] `super().__init__()` в дочернем классе
- [ ] Portfolio не наследует Account — композиция
- [ ] dataclass с валидацией суммы > 0

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 107: inheritance, composition, dataclasses"`

### Ловушки
- Глубокая иерархия наследования — хрупкий дизайн
- dataclass mutable по умолчанию — `frozen=True` для immutable

---

## День 108 (Ср): Магические методы и итераторы
<a id="week-16-day-108"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Task Manager**

### Теория

Магические методы (dunder) делают объекты «питоничными»: `__len__` для `len(obj)`, `__getitem__` для `obj[i]`, `__contains__` для `x in obj`. Класс `Playlist` с этими методами ведёт себя как встроенная коллекция — пользователь API не знает о внутреннем `list`.

Итератор-протокол: `__iter__` возвращает объект с `__next__`, который выдаёт элементы или бросает `StopIteration`. Generator function с `yield` — ленивая последовательность: `fibonacci(n)` не хранит весь ряд в RAM. Generator `read_log_lines(path)` читает файл построчно — O(1) память на строку.

`__eq__` определяет равенство; если переопределяешь его и хочешь использовать объекты в `set`/`dict`, продумай `__hash__` (или используй `frozen dataclass`). `__lt__` позволяет `sorted(transactions)` без key-функции.

**Читать:**

- [Emulating container types](https://docs.python.org/3/reference/datamodel.html#emulating-container-types)
- [Iterator Types](https://docs.python.org/3/library/stdtypes.html#iterator-types)
- [Generators](https://docs.python.org/3/tutorial/classes.html#generators)

**Ключевая мысль:** dunder-методы — контракт с Python; generators — ленивость и экономия памяти.

### Практика
1. Класс `Playlist` с `__len__`, `__getitem__`, итерацией по трекам
2. Generator `fibonacci(n)` — первые n чисел без списка в памяти
3. `Playlist` поддерживает `for track in playlist` и `len(playlist)`
4. Перегрузка `==` для `Transaction` по `id`; проверь поведение в `set`
5. Generator `read_log_lines(path)` — построчное чтение большого файла
6. Напиши в `notes/dunder.md` три dunder-метода и зачем они нужны

**Критерии:**
- [ ] Playlist итерируется в for-loop
- [ ] Generator не хранит весь ряд Фибоначчи в памяти
- [ ] `__eq__` согласован с hash (если используешь в set)

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 108: dunder methods and generators"`

### Ловушки
- `__eq__` без `__hash__` — объект не hashable для set/dict keys
- Бесконечный generator без условия остановки

---

## День 109 (Чт): Алгоритмы и Big O
<a id="week-16-day-109"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Task Manager**

### Теория

Big O описывает, как растёт время или память при увеличении входа, а не абсолютные миллисекунды. O(1) — константа, O(log n) — бинарный поиск, O(n) — один проход, O(n log n) — эффективная сортировка, O(n²) — вложенные циклы. Выбор структуры данных важнее микрооптимизаций: dict lookup O(1) в среднем vs list O(n).

Linear search перебирает все элементы; binary search требует отсортированный массив и делит пополам — O(log n). На 10⁶ элементов разница колоссальна. Two Sum: brute force O(n²) vs hash map O(n) — классический пример, когда дополнительная память покупает скорость.

Встроенная сортировка Python (Timsort) — O(n log n); bubble sort O(n²) — учебный, не production. `list.append` амортизированно O(1), но иногда O(n) при resize. VisuAlgo помогает увидеть рост операций. Замеры через `time.perf_counter()` убеждают лучше теории.

**Читать:**

- [Big O Cheat Sheet](https://www.bigocheatsheet.com/)
- [VisuAlgo](https://visualgo.net/)
- [Python TimeComplexity (wiki)](https://wiki.python.org/moin/TimeComplexity)

**Ключевая мысль:** сначала правильная структура данных и алгоритм, потом микрооптимизации.

### Практика
1. Реализуй linear search и binary search (sorted list)
2. Замерь время на списке 10⁴ и 10⁶ элементов (`time.perf_counter`)
3. Two Sum: brute force O(n²) vs hash map O(n) — сравни замеры
4. Таблица в `notes/big-o.md`: операция → сложность для list, dict, set
5. Реши на бумаге: сложность вложенных циклов и `dict.get` в цикле
6. Опционально: визуализируй binary search на VisuAlgo

**Критерии:**
- [ ] Binary search работает только на sorted input
- [ ] Замеры подтверждают разницу O(n) vs O(n²)
- [ ] Two Sum hash map решение за один проход

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 109: Big O benchmarks and Two Sum"`

### Ловушки
- Binary search на unsorted list — неверный результат
- Путаница best/average/worst case — указывай worst

---

## День 110 (Пт): pathlib и работа с файловой системой
<a id="week-16-day-110"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Task Manager**

### Теория

`pathlib.Path` — объектный API для путей вместо конкатенации строк и `os.path.join`. Оператор `/` склеивает кроссплатформенно: `Path('data') / 'tasks.db'`. `read_text()`, `write_text()`, `exists()`, `glob('*.py')`, `rglob('**/*.py')` покрывают 90% задач с файловой системой.

`Path(__file__).parent` даёт каталог скрипта — надёжнее относительных путей от cwd, который меняется при запуске из другой папки. `shutil.copy`, `move`, `rmtree` — операции над деревом. Context manager `with path.open()` гарантирует закрытие файла.

Скрипт `organize.py` сортирует файлы по расширению — практика обхода директорий. `--dry-run` показывает план без изменений — хорошая привычка для деструктивных операций. `PermissionError` на системных файлах логируй, не падай целиком.

**Читать:**

- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [shutil](https://docs.python.org/3/library/shutil.html)
- [argparse](https://docs.python.org/3/library/argparse.html)

**Ключевая мысль:** `Path(__file__).parent` — якорь для путей; pathlib вместо строк.

### Практика
1. Скрипт `organize.py` — сортирует файлы по расширению в подпапки
2. Рекурсивный поиск `*.py` через `rglob`
3. Подсчёт размера директории в MB
4. Флаг `--dry-run`: показать план без перемещения
5. Обработка `PermissionError` и логирование пропущенных файлов
6. Подготовь `data/` для SQLite БД проекта недели

**Критерии:**
- [ ] Только pathlib, не `os.path` (кроме env vars)
- [ ] Dry-run режим работает
- [ ] Обработка PermissionError

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 110: pathlib organize script"`

### Ловушки
- `path.write_text()` перезаписывает без confirm — сделай backup
- Относительные пути зависят от cwd — используй `Path(__file__).parent`

---

## День 111 (Сб): regex и обработка текстовых логов
<a id="week-16-day-111"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Task Manager**

### Теория

Регулярные выражения — мини-язык поиска по тексту. Модуль `re`: `match` — с начала строки, `search` — везде, `findall` — все совпадения, `sub` — замена. Raw-строки `r"\d+"` — backslash не экранируется Python. Группы `()` и именованные `(?P<name>...)` извлекают поля из лога.

Построчное чтение большого файла — O(1) память на строку; не загружай гигабайтный лог в `read()`. `re.compile(pattern)` переиспользуй в цикле — быстрее, чем компилировать каждый раз. regex101.com — тестируй паттерн до вставки в код.

Парсер server.log с named groups для timestamp, level, message — типичная задача DevOps/junior backend. Топ ERROR по часам — агрегация в dict. Замена IP на `[REDACTED]` — `re.sub`. Жадный `.*` может «съесть» лишнее — будь осторожен с квантификаторами.

**Читать:**

- [re module](https://docs.python.org/3/library/re.html)
- [regex101](https://regex101.com/)
- [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html)

**Ключевая мысль:** для поиска везде — `search`, не `match`; большие файлы — построчно.

### Практика
1. Генератор mock `server.log` (1000 строк: timestamp, level, message)
2. Парсер: извлечь все ERROR с датой через named groups
3. Топ-5 часов с наибольшим числом ERROR
4. Замена IP-адресов на `[REDACTED]` в копии лога
5. CLI: `python parse_log.py server.log --level ERROR`
6. Сохрани итоговую статистику в `reports/error-summary.txt`

**Критерии:**
- [ ] Парсинг построчно (memory-efficient)
- [ ] regex с named groups для timestamp и level
- [ ] Итоговая статистика в читаемом виде

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 111: log parser with regex"`

### Ловушки
- `re.match` только с начала строки — для поиска везде `re.search`
- Жадные квантификаторы `.*` — неожиданные совпадения

---

## День 112 (Вс): Ревью ООП и алгоритмов
<a id="week-16-day-112"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **CLI Task Manager**

### Теория

Ревью ООП и алгоритмов готовит к SQLite-проекту недели. SOLID на junior-уровне: Single Responsibility — один класс, одна причина для изменения; Open/Closed — расширяй через композицию, не правь базовый класс везде. Не усложняй: простой скрипт — функции + dataclasses, сложный домен — классы с поведением.

Code smells: god class на 500 строк, дублирование, magic numbers без констант. LeetCode Easy (Two Sum, Valid Parentheses) закрепляет структуры данных вне pet-проекта. Рефакторинг Expense Tracker на `Expense` + `ExpenseStore` — мост к `TaskRepository`.

Подготовь venv для недели 17 с `psycopg2-binary` и `python-dotenv`. Конспект Big O на одну страницу — пригодится при EXPLAIN и выборе индексов. Тег `week-16-done` на финальном коммите.

**Читать:**

- [LeetCode Easy](https://leetcode.com/problemset/)
- [SOLID (обзор)](https://realpython.com/solid-principles-python/)
- [sqlite3](https://docs.python.org/3/library/sqlite3.html)

**Ключевая мысль:** ООП — инструмент, не цель; простые данные — dataclass, сложная логика — классы.

### Практика
1. Реши 3 задачи LeetCode Easy: Two Sum, Valid Parentheses, Merge Sorted Array
2. Рефакторинг Expense Tracker на классы `Expense`, `ExpenseStore`
3. `ExpenseStore.save()` / `load()` через pathlib + JSON
4. Напиши ответы в `notes/oop-review.md`: 3 магических метода и зачем
5. Конспект Big O на 1 страницу с примерами из недели
6. Создай venv и `requirements.txt` для недели 17

**Критерии:**
- [ ] 3 LeetCode задачи приняты
- [ ] ExpenseStore с save/load через pathlib
- [ ] Конспект Big O на 1 страницу

### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 112: OOP review and LeetCode"`
- Поставь тег: `git tag week-16-done`

---

## Проект недели

**CLI Task Manager (SQLite)** — расширенная версия с ООП и реляционной БД. Полное описание: [docs/projects.md — неделя 16](../../docs/projects.md#неделя-16--cli-task-manager-sqlite).

### Архитектура

1. **Классы:** `Task`, `Tag`, `TaskRepository` (SQLite), `TaskCLI` (меню и ввод)
2. **Схема БД:** `tasks`, `tags`, `task_tags` (many-to-many)
3. **CRUD:** создание, список, обновление статуса, удаление, поиск по тегу
4. **Транзакции:** `try/except` + `conn.rollback()` при ошибке
5. **UI:** `rich` — таблица задач, цвет по статусу (`pending` / `done`)

### Требования

- ORM не используем — чистый `sqlite3` (SQLAlchemy на нед. 18)
- Все SQL с placeholders (`?`), никогда f-string в запросах
- `schema.sql` + seed с 5+ задачами и 3+ тегами
- README: установка, команды CLI, ER-диаграмма схемы
- `.env` не нужен — SQLite локальный файл `data/tasks.db`

### Критерии проекта

- [ ] `python -m task_cli` или `python main.py` запускает интерактивное меню
- [ ] Поиск и фильтр по статусу и тегу работают
- [ ] Many-to-many: задача может иметь несколько тегов
- [ ] Транзакция откатывается при нарушении FK
- [ ] README + схема БД + скриншот `rich`-таблицы
- [ ] Тег `week-16-done` на финальном коммите

## Ревью-чеклист
- `__init__` vs `__new__` — в чём разница (обзор)?
- list.pop(0) — какая сложность и почему?
- Когда dataclass, когда полноценный class?
- pathlib vs os.path — что предпочтительнее в 2024+?
- Как защититься от SQL injection в sqlite3?


## Проверь себя

<details>
<summary>Что должно получиться к концу недели?</summary>

Работающий проект **CLI Task Manager** в `learning-log/week-16/`, осмысленная Git-история, тег `week-16-done`.

</details>

<details>
<summary>Главный навык недели одной фразой?</summary>

Python ООП, SQLite, алгоритмы

</details>

<details>
<summary>Можно ли пропустить день?</summary>

Нет — дни связаны. В **лайт-режиме** сократи практику до MVP, но теорию и Git-коммит не пропускай.

</details>
