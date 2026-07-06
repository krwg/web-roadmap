# Неделя 5: JavaScript — переменные, типы, функции, массивы

> **Цель недели:** заложить фундамент JavaScript — синтаксис, типы данных, функции и работа с массивами.
> **Литература:** [learn.javascript.ru](https://learn.javascript.ru/), Kyle Simpson «You Don't Know JS» (Scope & Closures, Types & Grammar), [MDN JavaScript Guide](https://developer.mozilla.org/ru/docs/Web/JavaScript/Guide)

## День 1 (Mon): Введение и переменные

### Теория
- [learn.javascript.ru: Введение](https://learn.javascript.ru/intro) — как выполняется JS в браузере
- Подключение: `<script defer src="app.js">` vs модуль `type="module"`
- `let`, `const`, `var` — [разница и TDZ](https://learn.javascript.ru/var)
- Строгий режим `'use strict'`
- `console.log`, комментарии, стиль кода

### Практика
1. Создай `app.js`, подключи к HTML через `defer`
2. Объяви переменные `let` и `const` разных типов, выведи в console
3. Попробуй переприсвоить `const` объект — измени свойство vs переприсвоение
4. Включи `'use strict'`, спровоцируй ошибку с необъявленной переменной
5. Настрой VS Code: ESLint или встроенную проверку синтаксиса

**Критерии:**
- [ ] Используются только `let`/`const`, не `var`
- [ ] Скрипт подключён корректно, нет ошибок в Console
- [ ] Понимаю разницу переприсвоения и мутации объекта

## День 2 (Tue): Типы данных и операторы

### Теория
- [learn.javascript.ru: Типы](https://learn.javascript.ru/types) — примитивы и объекты
- `number`, `string`, `boolean`, `null`, `undefined`, `symbol`, `bigint`
- `typeof`, приведение типов, `==` vs `===`
- [learn.javascript.ru: Операторы](https://learn.javascript.ru/operators) — арифметика, сравнение, логика
- Template literals: `` `Hello, ${name}` ``

### Практика
1. Напиши функцию `describeType(value)` — возвращает строку с `typeof` и значением
2. Таблица сравнений: `0 == false`, `'' == false`, `null == undefined` — предскажи, проверь
3. Калькулятор в Console: сложение, деление, остаток, возведение в степень
4. Конвертер температуры °C → °F с template literal в выводе
5. Используй только `===` в новом коде

**Критерии:**
- [ ] Все сравнения через `===`
- [ ] Нет неявных приведений без понимания
- [ ] Template literals для интерполяции строк

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

### Практика
1. Программа «FizzBuzz» (1–100) — вывод в Console
2. Калькулятор оценок: число → буква (A/B/C/D/F) через `switch`
3. Таблица умножения 10×10 в виде строки в Console
4. Найди сумму чисел 1..N через `for`
5. Рефакторинг: замени вложенные `if` на early return где уместно

**Критерии:**
- [ ] FizzBuzz работает корректно
- [ ] Нет бесконечных циклов
- [ ] Код читаем, переменные с понятными именами

## День 4 (Thu): Функции

### Теория
- [learn.javascript.ru: Функции](https://learn.javascript.ru/function-basics)
- Declaration vs expression; arrow functions `() => {}`
- Параметры, аргументы, значения по умолчанию, rest `...args`
- `return`, неявный return в arrow functions
- Function scope: переменные внутри функции

### Практика
1. Напиши `greet(name, greeting = 'Привет')` — declaration
2. Перепиши как arrow function; сравни поведение `this` (пока без углубления)
3. Функция `sum(...numbers)` — сумма произвольного числа аргументов
4. `isEven(n)`, `isPrime(n)`, `factorial(n)` — чистые функции
5. Организуй функции в отдельный файл `utils.js` (подключение пока без modules)

**Критерии:**
- [ ] Минимум 5 переиспользуемых функций
- [ ] Default parameters и rest использованы
- [ ] Функции делают одну вещь (SRP)

## День 5 (Fri): Массивы — основы

### Теория
- [learn.javascript.ru: Массивы](https://learn.javascript.ru/array)
- Создание, индексация, `length`, мутабельность
- `push`, `pop`, `shift`, `unshift`, `splice`, `slice`
- `indexOf`, `includes`; spread `[...arr]`
- `for`, `for...of` для итерации

### Практика
1. Список покупок: добавление, удаление, вывод через `for...of`
2. Найди min/max в массиве чисел без `Math.min` на входе массива
3. Удали дубликаты из массива (без `Set` — через цикл; потом с `Set`)
4. Объедини два массива через spread
5. Реверс массива без `.reverse()` — через цикл

**Критерии:**
- [ ] Понимаю разницу `slice` и `splice`
- [ ] Итерация через `for...of`, не `for...in` для массивов
- [ ] Spread не мутирует оригинал

## День 6 (Sat): Методы массивов

### Теория
- [learn.javascript.ru: Методы массивов](https://learn.javascript.ru/array-methods)
- `map`, `filter`, `reduce`, `find`, `findIndex`, `some`, `every`
- `sort` с compare function — [осторожно с числами](https://learn.javascript.ru/array-methods#sort)
- `forEach` vs `map` — когда что
- Цепочки: `.filter().map().reduce()`

### Практика
1. Массив пользователей `{name, age}`: фильтр 18+, map в имена
2. Сумма цен корзины через `reduce`
3. Найди первый товар дороже 1000 через `find`
4. Проверь, все ли оценки ≥ 3 через `every`
5. Отсортируй числа `[10, 5, 40, 25]` правильно: `(a, b) => a - b`

**Критерии:**
- [ ] Использованы map, filter, reduce в реальных задачах
- [ ] Сортировка чисел корректна
- [ ] Цепочка из 3+ методов в одной задаче

## День 7 (Sun): Мини-проект и закрепление

### Теория
- [MDN: Debugging JavaScript](https://developer.mozilla.org/ru/docs/Learn/JavaScript/Howto/Debugging_JavaScript)
- Чтение stack trace; `debugger` statement
- Разбиение кода на функции и файлы
- JSDoc комментарии — базовое документирование

### Практика
1. Консольное приложение «Todo List» (массив + функции add/remove/list)
2. Поиск по задачам через `filter`
3. Статистика: всего, выполнено, в процессе через `reduce`
4. Отладь с breakpoint в DevTools Sources
5. Напиши JSDoc для 3 ключевых функций

**Критерии:**
- [ ] Todo list работает в Console без DOM
- [ ] Код разбит на логические функции
- [ ] Отладка через breakpoint, не только console.log

## Проект недели

**Консольный менеджер задач** — JS-приложение без DOM, управляемое из DevTools Console.

Функции: добавить задачу, удалить по id, отметить выполненной, фильтр по статусу, статистика.

**Критерии проекта:**
- [ ] Массив объектов `{id, title, done, createdAt}`
- [ ] Использованы map, filter, reduce, find
- [ ] Минимум 8 функций, чистые где возможно
- [ ] Код в репозитории с коммитом `feat: todo manager core`

## Ревью-чеклист
- Разница `let`, `const` и почему не `var`?
- Что вернёт `typeof NaN` и как проверить NaN?
- Разница `map` и `forEach`?
- Как отсортировать массив чисел по возрастанию?
- Могу ли я написать FizzBuzz и объяснить каждую ветку?
