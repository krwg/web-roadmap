# Неделя 5: JavaScript — переменные, типы, функции, массивы

> **Цель недели:** заложить фундамент JavaScript — синтаксис, типы данных, функции и работа с массивами.
> **Литература:** [learn.javascript.ru](https://learn.javascript.ru/), Kyle Simpson «You Don't Know JS» (Scope & Closures, Types & Grammar), [MDN JavaScript Guide](https://developer.mozilla.org/ru/docs/Web/JavaScript/Guide), [JavaScript.info](https://javascript.info/) — углублённые объяснения, [Eloquent JavaScript](https://eloquentjavascript.net/) (гл. 1–4)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md#неделя-5--console-task-manager)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-05/`

## День 1 (Mon): Введение и переменные

### Теория
- [learn.javascript.ru: Введение](https://learn.javascript.ru/intro) — как выполняется JS в браузере
- Подключение: `<script defer src="app.js">` vs модуль `type="module"`
- `let`, `const`, `var` — [разница и TDZ](https://learn.javascript.ru/var)
- Строгий режим `'use strict'`
- `console.log`, комментарии, стиль кода
- JS однопоточный: код выполняется сверху вниз в main thread — тяжёлые циклы блокируют UI
- `defer` загружает скрипт параллельно и выполняет после парсинга HTML — не блокирует рендер
- TDZ (Temporal Dead Zone): `let`/`const` недоступны до объявления — ловит ошибки раньше
- `const` запрещает переприсвоение, но объект можно мутировать — важное различие

### Практика
1. Создай `app.js`, подключи к HTML через `defer`
2. Объяви переменные `let` и `const` разных типов, выведи в console
3. Попробуй переприсвоить `const` объект — измени свойство vs переприсвоение
4. Включи `'use strict'`, спровоцируй ошибку с необъявленной переменной
5. Настрой VS Code: ESLint или встроенную проверку синтаксиса
6. Создай папку `week-05/` и файл `app.js` — старт проекта недели
7. Добавь `console.log` с шаблонной строкой и своим именем

**Критерии:**
- [ ] Используются только `let`/`const`, не `var`
- [ ] Скрипт подключён корректно, нет ошибок в Console
- [ ] Понимаю разницу переприсвоения и мутации объекта

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 05 day 1: js intro variables"`

## День 2 (Tue): Типы данных и операторы

### Теория
- [learn.javascript.ru: Типы](https://learn.javascript.ru/types) — примитивы и объекты
- `number`, `string`, `boolean`, `null`, `undefined`, `symbol`, `bigint`
- `typeof`, приведение типов, `==` vs `===`
- [learn.javascript.ru: Операторы](https://learn.javascript.ru/operators) — арифметика, сравнение, логика
- Template literals: `` `Hello, ${name}` ``
- Примитивы неизменяемы: `str.toUpperCase()` возвращает новую строку
- `===` сравнивает значение и тип — предсказуемее `==` с неявным приведением
- `null` — намеренное отсутствие; `undefined` — переменная не инициализирована
- Template literals поддерживают многострочность и выражения `${}` — чище конкатенации

### Практика
1. Напиши функцию `describeType(value)` — возвращает строку с `typeof` и значением
2. Таблица сравнений: `0 == false`, `'' == false`, `null == undefined` — предскажи, проверь
3. Калькулятор в Console: сложение, деление, остаток, возведение в степень
4. Конвертер температуры °C → °F с template literal в выводе
5. Используй только `===` в новом коде
6. Проверь `Number.isNaN(NaN)` vs `NaN === NaN` — зафиксируй в комментарии
7. Создай таблицу truthy/falsy значений в `notes.md`

**Критерии:**
- [ ] Все сравнения через `===`
- [ ] Нет неявных приведений без понимания
- [ ] Template literals для интерполяции строк

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 05 day 2: types and operators"`

### Ловушки
- `typeof null === 'object'` — исторический баг
- `NaN === NaN` → false; проверка через `Number.isNaN()`
- Сложение строки и числа: `'5' + 3` → `'53'`

## День 3 (Wed): Условия и циклы

### Теория
- [learn.javascript.ru: Условное ветвление](https://learn.javascript.ru/ifelse)
- `if/else`, тернарный оператор, `switch`
- [learn.javascript.ru: Циклы](https://learn.javascript.ru/while-for) — `while`, `do...while`, `for`
- `break`, `continue`; вложенные циклы
- Truthy/falsy значения
- Early return уменьшает вложенность `if` — код читается линейно
- `switch` с `break` — без него выполнение «проваливается» в следующий case
- `for...of` предпочтительнее классического `for` для массивов (на следующих днях)
- Falsy: `0`, `''`, `null`, `undefined`, `NaN`, `false` — всё остальное truthy

### Практика
1. Программа «FizzBuzz» (1–100) — вывод в Console
2. Калькулятор оценок: число → буква (A/B/C/D/F) через `switch`
3. Таблица умножения 10×10 в виде строки в Console
4. Найди сумму чисел 1..N через `for`
5. Рефакторинг: замени вложенные `if` на early return где уместно
6. Добавь валидацию ввода в FizzBuzz — обработай `N <= 0`
7. Перепиши один блок на тернарный оператор — оцени читаемость

**Критерии:**
- [ ] FizzBuzz работает корректно
- [ ] Нет бесконечных циклов
- [ ] Код читаем, переменные с понятными именами

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 05 day 3: conditions and loops"`

## День 4 (Thu): Функции

### Теория
- [learn.javascript.ru: Функции](https://learn.javascript.ru/function-basics)
- Declaration vs expression; arrow functions `() => {}`
- Параметры, аргументы, значения по умолчанию, rest `...args`
- `return`, неявный return в arrow functions
- Function scope: переменные внутри функции
- Чистая функция: одинаковый вход → одинаковый выход, без побочных эффектов
- Arrow functions не имеют своего `this` — важно для методов объектов (неделя 6)
- Rest `...args` собирает оставшиеся аргументы в массив — гибкие сигнатуры
- SRP: одна функция — одна ответственность; проще тестировать и переиспользовать

### Практика
1. Напиши `greet(name, greeting = 'Привет')` — declaration
2. Перепиши как arrow function; сравни поведение `this` (пока без углубления)
3. Функция `sum(...numbers)` — сумма произвольного числа аргументов
4. `isEven(n)`, `isPrime(n)`, `factorial(n)` — чистые функции
5. Организуй функции в отдельный файл `utils.js` (подключение пока без modules)
6. Добавь JSDoc к `factorial` — опиши параметр и возврат
7. Напиши `generateId()` — уникальный id на основе `Date.now()` и случайности

**Критерии:**
- [ ] Минимум 5 переиспользуемых функций
- [ ] Default parameters и rest использованы
- [ ] Функции делают одну вещь (SRP)

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 05 day 4: functions and utils"`

## День 5 (Fri): Массивы — основы

### Теория
- [learn.javascript.ru: Массивы](https://learn.javascript.ru/array)
- Создание, индексация, `length`, мутабельность
- `push`, `pop`, `shift`, `unshift`, `splice`, `slice`
- `indexOf`, `includes`; spread `[...arr]`
- `for`, `for...of` для итерации
- `slice` не мутирует, `splice` мутирует — частая путаница
- `for...in` для массивов перебирает индексы как строки — используй `for...of`
- Spread создаёт shallow copy — вложенные объекты общие
- `length` можно менять вручную — обрезает массив, но это редкий приём

### Практика
1. Список покупок: добавление, удаление, вывод через `for...of`
2. Найди min/max в массиве чисел без `Math.min` на входе массива
3. Удали дубликаты из массива (без `Set` — через цикл; потом с `Set`)
4. Объедини два массива через spread
5. Реверс массива без `.reverse()` — через цикл
6. Создай массив задач-заготовок `{id, title, done}` для Todo
7. Сравни `slice` и `splice` на одном массиве — выведи до/после

**Критерии:**
- [ ] Понимаю разницу `slice` и `splice`
- [ ] Итерация через `for...of`, не `for...in` для массивов
- [ ] Spread не мутирует оригинал

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 05 day 5: arrays basics"`

## День 6 (Sat): Методы массивов

### Теория
- [learn.javascript.ru: Методы массивов](https://learn.javascript.ru/array-methods)
- `map`, `filter`, `reduce`, `find`, `findIndex`, `some`, `every`
- `sort` с compare function — [осторожно с числами](https://learn.javascript.ru/array-methods#sort)
- `forEach` vs `map` — когда что
- Цепочки: `.filter().map().reduce()`
- `map` возвращает новый массив — идеален для трансформаций без мутации
- `reduce` — универсальный агрегатор: сумма, группировка, flatten
- `sort` без compare сортирует как строки: `[10, 5, 40]` → `[10, 40, 5]` — баг
- `forEach` для побочных эффектов; `map` когда нужен результат

### Практика
1. Массив пользователей `{name, age}`: фильтр 18+, map в имена
2. Сумма цен корзины через `reduce`
3. Найди первый товар дороже 1000 через `find`
4. Проверь, все ли оценки ≥ 3 через `every`
5. Отсортируй числа `[10, 5, 40, 25]` правильно: `(a, b) => a - b`
6. Цепочка: фильтр активных задач → map в заголовки → join в строку
7. Группировка задач по `done` через `reduce`

**Критерии:**
- [ ] Использованы map, filter, reduce в реальных задачах
- [ ] Сортировка чисел корректна
- [ ] Цепочка из 3+ методов в одной задаче

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 05 day 6: array methods"`

## День 7 (Sun): Мини-проект и закрепление

### Теория
- [MDN: Debugging JavaScript](https://developer.mozilla.org/ru/docs/Learn/JavaScript/Howto/Debugging_JavaScript)
- Чтение stack trace; `debugger` statement
- Разбиение кода на функции и файлы
- JSDoc комментарии — базовое документирование
- Stack trace читается снизу вверх — последний вызов наверху
- `debugger` останавливает выполнение, если DevTools открыты — альтернатива breakpoint
- Разделение на `addTask`, `removeTask`, `listTasks` — проще отлаживать по частям
- JSDoc помогает IDE подсказывать типы до перехода на TypeScript

### Практика
1. Консольное приложение «Todo List» (массив + функции add/remove/list)
2. Поиск по задачам через `filter`
3. Статистика: всего, выполнено, в процессе через `reduce`
4. Отладь с breakpoint в DevTools Sources
5. Напиши JSDoc для 3 ключевых функций
6. Добавь фильтр по статусу `done` / `active`
7. Финальный коммит `feat: todo manager core` и тег `week-05-done`

**Критерии:**
- [ ] Todo list работает в Console без DOM
- [ ] Код разбит на логические функции
- [ ] Отладка через breakpoint, не только console.log

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 05 day 7: console todo project"`

## Проект недели

**Консольный менеджер задач** — JS-приложение без DOM, управляемое из DevTools Console.

Подробное описание: [docs/projects.md — Неделя 5](../../docs/projects.md#неделя-5--console-task-manager)

Функции: добавить задачу, удалить по id, отметить выполненной, фильтр по статусу, статистика.

**Критерии проекта:**
- [ ] Массив объектов `{id, title, done, createdAt}`
- [ ] Использованы map, filter, reduce, find
- [ ] Минимум 8 функций, чистые где возможно
- [ ] Код в репозитории с коммитом `feat: todo manager core`
- [ ] CRUD полный: create, read, update (toggle done), delete
- [ ] Фильтры: все / активные / выполненные
- [ ] Статистика через `reduce`: всего, done, pending
- [ ] Папка `week-05/` с README и примером вызова функций в Console
- [ ] Тег `week-05-done` на финальном коммите

## Ревью-чеклист
- Разница `let`, `const` и почему не `var`?
- Что вернёт `typeof NaN` и как проверить NaN?
- Разница `map` и `forEach`?
- Как отсортировать массив чисел по возрастанию?
- Могу ли я написать FizzBuzz и объяснить каждую ветку?
