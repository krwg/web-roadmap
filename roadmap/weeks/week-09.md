# Неделя 9: JS advanced — closures, prototypes, classes, patterns

> **Цель недели:** углубить понимание JavaScript — замыкания, прототипы, классы и практические паттерны проектирования.
> **Литература:** Kyle Simpson «YDKJS: Scope & Closures», «YDKJS: this & Object Prototypes», [learn.javascript.ru: Прототипы](https://learn.javascript.ru/prototype-inheritance), [patterns.dev](https://www.patterns.dev/), [MDN: Closures](https://developer.mozilla.org/ru/docs/Web/JavaScript/Closures), [javascript.info: Продвинутая работа с функциями](https://javascript.info/advanced-functions)
> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-09/`

## День 1 (Mon): Scope и замыкания

### Теория
- [learn.javascript.ru: Замыкание](https://learn.javascript.ru/closure)
- Lexical scope — функция видит переменные места объявления, не места вызова
- Closure: внутренняя функция «помнит» внешнее окружение даже после завершения внешней функции
- Практики: data privacy, factory functions, модульный паттерн
- YDKJS: IIFE, module pattern — изоляция от глобальной области
- `let`/`const` — блочная область видимости; `var` — функциональная (исторический legacy)
- Замыкание в циклах: почему `let` решает проблему, а `var` — нет
- Garbage collection и замыкания: ссылки на внешние переменные удерживают память

### Практика
1. `createCounter()` — increment, decrement, getValue через closure
2. Ловушка цикла: `for (var i=0; ...)` + setTimeout — исправь через let и closure
3. `createMultiplier(n)` → функция умножения на n
4. Приватное поле в factory `createBankAccount(balance)`
5. Объясни замыкание вслух за 2 минуты без кода
6. Реализуй `once(fn)` — функция, которая вызывает `fn` только один раз
7. Создай папку `learning-log/week-09/` и файл `day-01-closures.js` с примерами

**Критерии:**
- [ ] Counter работает без глобальных переменных
- [ ] Классическая ловушка var+setTimeout исправлена
- [ ] Могу объяснить closure своими словами

### Git
```bash
cd learning-log/week-09
git add day-01-closures.js
git commit -m "week-09 day-01: замыкания, createCounter и once"
```

### Ловушки
- Создание функций в цикле с var — все ссылаются на финальный i
- Утечки памяти через closure на большие объекты
- Путаница closure и this

## День 2 (Tue): this и контекст вызова

### Теория
- [learn.javascript.ru: Методы привязки контекста](https://learn.javascript.ru/bind)
- Правила `this`: default, implicit, explicit, new binding — четыре способа определения
- `call`, `apply`, `bind` — различия: немедленный вызов vs частичное применение
- Arrow functions не имеют своего `this` — lexical this из окружающего scope
- Потеря контекста в callback: `obj.method` как reference без вызова
- Strict mode: в default binding `this` = `undefined`, не `window`
- Методы массивов (`forEach`, `map`) и потеря `this` в callback
- `new` создаёт объект и привязывает `this` к нему; стрелочные функции нельзя вызывать с `new`

### Практика
1. Демонстрация 4 правил `this` — 4 примера в Console
2. Исправь `button.addEventListener('click', obj.handleClick)` через bind
3. Заимствование метода: `[].slice.call(arguments)`
4. Сравни обычную и arrow function как метод объекта
5. `partial` через bind: `const double = multiply.bind(null, 2)`
6. Реализуй `call`/`apply` вручную для одного примера — пойми механику
7. Запиши конспект «4 правила this» в `day-02-this.md`

**Критерии:**
- [ ] bind использован для сохранения контекста
- [ ] Понимаю, почему arrow не подходит как метод
- [ ] 4 правила this — конспект

### Git
```bash
cd learning-log/week-09
git add day-02-this.js day-02-this.md
git commit -m "week-09 day-02: this, bind и 4 правила контекста"
```

## День 3 (Wed): Прототипы и наследование

### Теория
- [learn.javascript.ru: Прототипное наследование](https://learn.javascript.ru/prototype-inheritance)
- `[[Prototype]]`, `__proto__`, `Object.getPrototypeOf` — как читать цепочку
- `F.prototype`, `new F()`, цепочка прототипов до `Object.prototype`
- `Object.create(proto)` — создание объекта с заданным прототипом без конструктора
- Классы — синтаксический сахар над прототипами, не отдельная модель
- `instanceof` проверяет наличие в цепочке прототипов, не тип переменной
- `hasOwnProperty` vs унаследованные свойства — различие own vs inherited
- Дескрипторы свойств: `writable`, `enumerable`, `configurable`

### Практика
1. Constructor `Person(name)` + `Person.prototype.greet`
2. `Student` наследует `Person` через `Object.create(Person.prototype)`
3. Проверь цепочку: `student instanceof Student`, `instanceof Person`
4. Добавь метод на `Array.prototype` — пойми, почему это плохая идея
5. Нарисуй prototype chain для своих объектов
6. Реализуй `inherits(Child, Parent)` без `class` — утилита наследования
7. Сравни размер объектов: factory vs constructor — когда что выгоднее

**Критерии:**
- [ ] Наследование без class syntax (хотя бы один пример)
- [ ] Понимаю разницу __proto__ и prototype
- [ ] Не поллю глобальные прототипы в production-коде

### Git
```bash
cd learning-log/week-09
git add day-03-prototypes.js
git commit -m "week-09 day-03: прототипы, Person/Student и inherits"
```

## День 4 (Thu): Классы ES6+

### Теория
- [learn.javascript.ru: Класс](https://learn.javascript.ru/class)
- `class`, `constructor`, методы, `static`, `extends`, `super`
- Геттеры/сеттеры; private fields `#field` — настоящая инкапсуляция в ES2022
- Переопределение методов; `super.method()` — вызов родительской реализации
- Когда class, когда factory + closure — критерии выбора
- Static blocks и static fields — инициализация на уровне класса
- `#private` недоступен снаружи даже через reflection — в отличие от `_convention`
- Под капотом: `class` всё равно использует `prototype`, `typeof` класса — `function`

### Практика
1. `class TodoItem { constructor(title) ... toggle() }`
2. `class TodoList extends Array` или композиция — список с методами add/remove
3. Static `TodoItem.fromJSON(obj)` — фабричный метод десериализации
4. Private `#id` в классе — генерация уникального id
5. Рефакторинг каталога фильмов: class `Movie`, `MovieCollection`
6. Добавь геттер `isOverdue` для задачи с дедлайном
7. Напиши unit-проверки вручную (assert) для `TodoItem.toggle()`

**Критерии:**
- [ ] extends + super корректны
- [ ] Static method для десериализации
- [ ] Private field использован

### Git
```bash
cd learning-log/week-09
git add src/models/
git commit -m "week-09 day-04: классы TodoItem, Movie и private fields"
```

## День 5 (Fri): Паттерны проектирования

### Теория
- [patterns.dev](https://www.patterns.dev/vanilla) — Module, Observer, Singleton
- Observer/Pub-Sub: subscribe, publish, unsubscribe — слабая связанность компонентов
- Module pattern в ES modules — уже используешь, но осознанно
- Strategy — interchangeable algorithms без if/else в клиенте
- Factory — создание объектов без `new` в клиентском коде
- Singleton — один экземпляр; осторожно с глобальным состоянием и тестами
- MVC/MVP — разделение Model, View, Controller (обзор для Todo)
- Когда паттерн — overkill: не усложняй проект из 50 строк

### Практика
1. EventEmitter: `on`, `off`, `emit` — 50 строк
2. Подпиши UI на изменения store через Observer
3. Strategy: сортировка `byDate`, `byTitle` — переключаемые функции
4. Factory `createNotification(type, message)` → toast/error/success
5. Рефакторинг Todo: Store (state) + View (DOM) + Controller
6. Добавь `once(event, handler)` в EventEmitter
7. Задокументируй в README, какие паттерны где применены

**Критерии:**
- [ ] EventEmitter работает с несколькими подписчиками
- [ ] Store отделён от DOM
- [ ] Минимум 2 паттерна применены осознанно

### Git
```bash
cd learning-log/week-09
git add src/patterns/ src/store.js
git commit -m "week-09 day-05: EventEmitter, Strategy и Store/View"
```

## День 6 (Sat): Функциональные приёмы

### Теория
- Pure functions, side effects, immutability — предсказуемость и тестируемость
- Higher-order functions: map, filter, reduce как примеры абстракции
- Composition: `compose(f, g)(x)` = f(g(x)); pipe — слева направо
- Currying — [learn.javascript.ru: Каррирование](https://learn.javascript.ru/currying-partials)
- Recursion vs iteration — читаемость vs stack limit
- Referential transparency — одинаковый вход → одинаковый выход
- Partial application vs currying — различие и практическое применение
- Immutability в JS: spread, `structuredClone`, библиотеки не обязательны на старте

### Практика
1. Перепиши обработку списка только pure functions
2. `pipe(...fns)` — композиция справа налево
3. Curried `add(a)(b)(c)` или практичный `filterBy(prop, value)`
4. Рекурсивный обход вложенного меню (tree)
5. Сравни производительность recursion vs loop для factorial(100) — stack overflow?
6. Реализуй `memoize(fn)` для чистой функции с кэшем
7. Рефакторинг фильтрации каталога через pipe из pure-функций

**Критерии:**
- [ ] Минимум 3 pure functions
- [ ] pipe/compose реализован
- [ ] Понимаю риск stack overflow в рекурсии

### Git
```bash
cd learning-log/week-09
git add src/utils/fp.js
git commit -m "week-09 day-06: pipe, currying и memoize"
```

## День 7 (Sun): Рефакторинг и code quality

### Теория
- SOLID в JS — SRP и DIP на практике в модульной структуре
- DRY vs WET — когда дублирование оправдано (например, явность vs абстракция)
- ESLint + Prettier — единый стиль, ловля ошибок до runtime
- JSDoc для публичного API — типы без TypeScript
- Подготовка кодовой базы к TypeScript — явные контракты
- ADR (Architecture Decision Record) — фиксация «почему так»
- Code review checklist: naming, side effects, error handling
- `.eslintrc` vs flat config — обзор для будущих недель

### Практика
1. Подключи ESLint (eslint:recommended) к проекту
2. Исправь все warnings
3. Рефакторинг каталога: classes + observer store + api module
4. JSDoc для всех публичных функций api-модуля
5. Напиши ADR (Architecture Decision Record) на 1 страницу — почему выбрана структура
6. Собери скелет **Library System** — папки `models/`, `store/`, `ui/`
7. Прогони финальный self-review по ревью-чеклисту недели

**Критерии:**
- [ ] ESLint проходит без ошибок
- [ ] Архитектура store/view/api
- [ ] JSDoc на ключевых экспортах

### Git
```bash
cd learning-log/week-09
git add .
git commit -m "week-09 day-07: ESLint, ADR и скелет Library System"
```

## Проект недели

**Library System** — OOP + паттерны на ванильном JS. Подробное ТЗ: [docs/projects.md — Неделя 9](../../docs/projects.md#неделя-9--library-system-js).

Сущности: `Book` (title, author, isbn), `Member` (name, id), `Library` (выдача/возврат, учёт копий). Observer уведомляет UI об изменениях. Store в localStorage.

**Функции:**
- CRUD книг и читателей; выдача и возврат с проверкой доступности
- Поиск по названию/автору; история выдач для члена библиотеки
- UI: список книг, форма добавления, панель «на руках у читателей»
- Модульная структура ES modules, без глобальных переменных

**Критерии проекта:**
- [ ] Минимум 2 класса с наследованием или композицией (`Book` / `Member` / `Library`)
- [ ] EventEmitter/Observer для UI updates при изменении store
- [ ] Closure или private fields (`#`) для инкапсуляции внутреннего состояния
- [ ] ESLint + модульная структура (`models/`, `store/`, `ui/`, `patterns/`)
- [ ] Persist в localStorage с миграцией схемы при необходимости
- [ ] README с инструкцией запуска и описанием архитектуры
- [ ] Тег `week-09-done` после финальной проверки

## Ревью-чеклист
- Что такое замыкание и зачем `createCounter`?
- 4 правила определения `this`?
- Разница `__proto__` и `prototype`?
- Class vs factory function — когда что?
- Могу ли я реализовать простой pub/sub с нуля?
