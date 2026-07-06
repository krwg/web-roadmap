# Неделя 16: Python — ООП, алгоритмы, файлы

> **Цель недели:** освоить объектно-ориентированный Python, оценку сложности и работу с файловой системой.
> **Литература:** [Python OOP](https://docs.python.org/3/tutorial/classes.html), [Real Python — pathlib](https://realpython.com/python-pathlib/), [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)
> **Проект недели:** [CLI Task Manager (SQLite)](../../docs/projects.md#неделя-16--cli-task-manager-sqlite) — классы `Task`, `TaskRepository`, CRUD через `sqlite3`, теги many-to-many.
> **Git:** папка `learning-log/week-16/`, минимум 1 осмысленный коммит в день; к концу недели тег `week-16-done`.

## День 106 (Пн): Классы и объекты

### Теория
- [Classes](https://docs.python.org/3/tutorial/classes.html): `class`, `__init__`, `self` — объект = данные + поведение в одной сущности
- Атрибуты экземпляра (`self.balance`) vs атрибуты класса (`BankAccount.currency`) — общие настройки vs состояние объекта
- Методы экземпляра (`self`), `@classmethod` (фабрики, альтернативные конструкторы), `@staticmethod` (утилиты без доступа к `self`)
- `__str__` — для пользователя (`print`), `__repr__` — для отладки (`repr(obj)` в REPL)
- Инкапсуляция: соглашение `_private` и `@property` вместо прямой мутации полей снаружи
- Type hints на методах улучшают читаемость и ловят ошибки в IDE до запуска

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

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 106: BankAccount and Transaction classes"`

### Ловушки
- Забытый `self` в методах — TypeError
- Публичные атрибуты вместо свойств — нарушение инкапсуляции

---

## День 107 (Вт): Наследование, композиция, dataclasses

### Теория
- Наследование: `class Savings(BankAccount)` расширяет базовый контракт; `super().__init__()` вызывает родительский конструктор
- [Композиция vs наследование](https://realpython.com/inheritance-composition-python/) — «has-a» (Portfolio содержит счета) предпочтительнее «is-a» при сложной логике
- [@dataclass](https://docs.python.org/3/library/dataclasses.html) — автогенерация `__init__`, `__repr__`, `__eq__` для DTO без поведения
- `__post_init__` — валидация после создания dataclass (сумма > 0, непустой title)
- `frozen=True` — immutable dataclass, безопасен как ключ dict/set
- ABC (`ABC`, `@abstractmethod`) — контракт для подклассов, полезен для `TaskRepository` интерфейса

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

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 107: inheritance, composition, dataclasses"`

### Ловушки
- Глубокая иерархия наследования — хрупкий дизайн
- dataclass mutable по умолчанию — `frozen=True` для immutable

---

## День 108 (Ср): Магические методы и итераторы

### Теория
- Dunder methods делают объекты «питоничными»: `__len__`, `__getitem__`, `__contains__`, `__eq__`, `__lt__`
- [Emulating container types](https://docs.python.org/3/reference/datamodel.html#emulating-container-types) — свой класс ведёт себя как list/dict
- Итератор-протокол: `__iter__` возвращает self, `__next__` даёт элемент или `StopIteration`
- Generator functions (`yield`) — ленивые последовательности без хранения всего в RAM
- `__eq__` и `__hash__`: если переопределяешь равенство — продумай hashability для `set`/`dict`
- Сравнение объектов: `__lt__` позволяет `sorted(transactions)` без key-функции

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

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 108: dunder methods and generators"`

### Ловушки
- `__eq__` без `__hash__` — объект не hashable для set/dict keys
- Бесконечный generator без условия остановки

---

## День 109 (Чт): Алгоритмы и Big O

### Теория
- [Big O notation](https://www.bigocheatsheet.com/): O(1), O(log n), O(n), O(n log n), O(n²) — рост времени при увеличении входа
- list lookup O(n) vs dict/set lookup O(1) — выбор структуры данных важнее микрооптимизаций
- Сортировки: bubble O(n²) vs built-in Timsort O(n log n) — не изобретай wheel
- Space complexity — дополнительная память (hash map для Two Sum)
- [VisuAlgo](https://visualgo.net/) — визуализация: смотри, как растёт число операций
- Amortized analysis: `list.append` в среднем O(1), но иногда O(n) при resize

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

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 109: Big O benchmarks and Two Sum"`

### Ловушки
- Binary search на unsorted list — неверный результат
- Путаница best/average/worst case — указывай worst

---

## День 110 (Пт): pathlib и работа с файловой системой

### Теория
- [pathlib](https://docs.python.org/3/library/pathlib.html): `Path` — объектный API вместо строковых путей
- Оператор `/`: `Path("data") / "tasks.db"` — кроссплатформенная склейка
- `read_text()`, `write_text()`, `exists()`, `glob()`, `rglob()` — типичные операции
- `shutil.copy`, `move`, `rmtree` — операции над деревом файлов
- `Path(__file__).parent` — надёжный путь относительно скрипта, не cwd
- Context managers `with path.open()` — гарантированное закрытие файла

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

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 110: pathlib organize script"`

### Ловушки
- `path.write_text()` перезаписывает без confirm — сделай backup
- Относительные пути зависят от cwd — используй `Path(__file__).parent`

---

## День 111 (Сб): regex и обработка текстовых логов

### Теория
- [re module](https://docs.python.org/3/library/re.html): `match` (с начала), `search` (везде), `findall`, `sub`
- Паттерны: `\d+`, `\w+`, группы `()`, named groups `(?P<name>...)` — извлечение полей
- Raw strings `r"..."` — backslash не экранируется Python
- Построчное чтение — O(1) память на строку, не загружай 1 GB файл целиком
- [regex101.com](https://regex101.com/) — тестируй паттерн до вставки в код
- `re.compile` — переиспользование паттерна в цикле быстрее

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

### Git
- Закоммить изменения дня: `git add week-16/` → `git commit -m "week 16 day 111: log parser with regex"`

### Ловушки
- `re.match` только с начала строки — для поиска везде `re.search`
- Жадные квантификаторы `.*` — неожиданные совпадения

---

## День 112 (Вс): Ревью ООП и алгоритмов

### Теория
- SOLID на junior-уровне: SRP (один класс — одна ответственность), OCP (расширяй через композицию)
- Когда ООП, когда функции + dataclasses — не усложняй простые скрипты
- [LeetCode Easy](https://leetcode.com/problemset/) — Python тег для закрепления структур данных
- Рефакторинг: «code smells» — god class, дублирование, magic numbers
- Подготовка к неделе 17: venv с `psycopg2-binary` для PostgreSQL

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
