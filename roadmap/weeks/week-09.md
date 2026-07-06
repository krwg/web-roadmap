# Неделя 9: JS advanced — closures, prototypes, classes, patterns

> **Цель недели:** углубить понимание JavaScript — замыкания, прототипы, классы и практические паттерны проектирования.
> **Литература:** Kyle Simpson «YDKJS: Scope & Closures», «YDKJS: this & Object Prototypes», [learn.javascript.ru: Прототипы](https://learn.javascript.ru/prototype-inheritance), [patterns.dev](https://www.patterns.dev/)

## День 1 (Mon): Scope и замыкания

### Теория
- [learn.javascript.ru: Замыкание](https://learn.javascript.ru/closure)
- Lexical scope — функция видит переменные места объявления
- Closure: внутренняя функция «помнит» внешнее окружение
- Практики: data privacy, factory functions
- YDKJS: IIFE, module pattern

### Практика
1. `createCounter()` — increment, decrement, getValue через closure
2. Ловушка цикла: `for (var i=0; ...)` + setTimeout — исправь через let и closure
3. `createMultiplier(n)` → функция умножения на n
4. Приватное поле в factory `createBankAccount(balance)`
5. Объясни замыкание вслух за 2 минуты без кода

**Критерии:**
- [ ] Counter работает без глобальных переменных
- [ ] Классическая ловушка var+setTimeout исправлена
- [ ] Могу объяснить closure своими словами

### Ловушки
- Создание функций в цикле с var — все ссылаются на финальный i
- Утечки памяти через closure на большие объекты
- Путаница closure и this

## День 2 (Tue): this и контекст вызова

### Теория
- [learn.javascript.ru: Методы привязки контекста](https://learn.javascript.ru/bind)
- Правила `this`: default, implicit, explicit, new binding
- `call`, `apply`, `bind` — различия
- Arrow functions не имеют своего `this` — lexical this
- Потеря контекста в callback: `obj.method` как reference

### Практика
1. Демонстрация 4 правил `this` — 4 примера в Console
2. Исправь `button.addEventListener('click', obj.handleClick)` через bind
3. Заимствование метода: `[].slice.call(arguments)`
4. Сравни обычную и arrow function как метод объекта
5. `partial` через bind: `const double = multiply.bind(null, 2)`

**Критерии:**
- [ ] bind использован для сохранения контекста
- [ ] Понимаю, почему arrow не подходит как метод
- [ ] 4 правила this — конспект

## День 3 (Wed): Прототипы и наследование

### Теория
- [learn.javascript.ru: Прототипное наследование](https://learn.javascript.ru/prototype-inheritance)
- `[[Prototype]]`, `__proto__`, `Object.getPrototypeOf`
- `F.prototype`, `new F()`, цепочка прототипов
- `Object.create(proto)` — создание с заданным прототипом
- Классы — синтаксический сахар над прототипами

### Практика
1. Constructor `Person(name)` + `Person.prototype.greet`
2. `Student` наследует `Person` через `Object.create(Person.prototype)`
3. Проверь цепочку: `student instanceof Student`, `instanceof Person`
4. Добавь метод на `Array.prototype` — пойми, почему это плохая идея
5. Нарисуй prototype chain для своих объектов

**Критерии:**
- [ ] Наследование без class syntax (хотя бы один пример)
- [ ] Понимаю разницу __proto__ и prototype
- [ ] Не поллю глобальные прототипы в production-коде

## День 4 (Thu): Классы ES6+

### Теория
- [learn.javascript.ru: Класс](https://learn.javascript.ru/class)
- `class`, `constructor`, методы, `static`, `extends`, `super`
- Геттеры/сеттеры; private fields `#field`
- Переопределение методов; `super.method()`
- Когда class, когда factory + closure

### Практика
1. `class TodoItem { constructor(title) ... toggle() }`
2. `class TodoList extends Array` или композиция — список с методами add/remove
3. Static `TodoItem.fromJSON(obj)` — фабричный метод
4. Private `#id` в классе
5. Рефакторинг каталога фильмов: class `Movie`, `MovieCollection`

**Критерии:**
- [ ] extends + super корректны
- [ ] Static method для десериализации
- [ ] Private field использован

## День 5 (Fri): Паттерны проектирования

### Теория
- [patterns.dev](https://www.patterns.dev/vanilla) — Module, Observer, Singleton
- Observer/Pub-Sub: subscribe, publish, unsubscribe
- Module pattern в ES modules — уже используешь
- Strategy — interchangeable algorithms
- Factory — создание объектов без new в клиентском коде

### Практика
1. EventEmitter: `on`, `off`, `emit` — 50 строк
2. Подпиши UI на изменения store через Observer
3. Strategy: сортировка `byDate`, `byTitle` — переключаемые функции
4. Factory `createNotification(type, message)` → toast/error/success
5. Рефакторинг Todo: Store (state) + View (DOM) + Controller

**Критерии:**
- [ ] EventEmitter работает с несколькими подписчиками
- [ ] Store отделён от DOM
- [ ] Минимум 2 паттерна применены осознанно

## День 6 (Sat): Функциональные приёмы

### Теория
- Pure functions, side effects, immutability
- Higher-order functions: map, filter как примеры
- Composition: `compose(f, g)(x)` = f(g(x))
- Currying — [learn.javascript.ru: Каррирование](https://learn.javascript.ru/currying-partials)
- Recursion vs iteration

### Практика
1. Перепиши обработку списка только pure functions
2. `pipe(...fns)` — композиция справа налево
3. Curried `add(a)(b)(c)` или практичный `filterBy(prop, value)`
4. Рекурсивный обход вложенного меню (tree)
5. Сравни производительность recursion vs loop для factorial(100) — stack overflow?

**Критерии:**
- [ ] Минимум 3 pure functions
- [ ] pipe/compose реализован
- [ ] Понимаю риск stack overflow в рекурсии

## День 7 (Sun): Рефакторинг и code quality

### Теория
- SOLID в JS — SRP и DIP на практике
- DRY vs WET — когда дублирование оправдано
- ESLint + Prettier — единый стиль
- JSDoc для публичного API
- Подготовка кодовой базы к TypeScript

### Практика
1. Подключи ESLint (eslint:recommended) к проекту
2. Исправь все warnings
3. Рефакторинг каталога: classes + observer store + api module
4. JSDoc для всех публичных функций api-модуля
5. Напиши ADR (Architecture Decision Record) на 1 страницу — почему выбрана структура

**Критерии:**
- [ ] ESLint проходит без ошибок
- [ ] Архитектура store/view/api
- [ ] JSDoc на ключевых экспортах

## Проект недели

**Библиотечная система** — OOP + паттерны на ванильном JS.

Сущности: `Book`, `Member`, `Library` (выдача/возврат). Observer уведомляет UI. Store в localStorage.

**Критерии проекта:**
- [ ] Минимум 2 класса с наследованием или композицией
- [ ] EventEmitter/Observer для UI updates
- [ ] Closure или private fields для инкапсуляции
- [ ] ESLint + модульная структура

## Ревью-чеклист
- Что такое замыкание и зачем `createCounter`?
- 4 правила определения `this`?
- Разница `__proto__` и `prototype`?
- Class vs factory function — когда что?
- Могу ли я реализовать простой pub/sub с нуля?
