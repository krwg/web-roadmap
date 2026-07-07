# Неделя 9: JS advanced — closures, prototypes, classes, patterns



> **Цель недели:** углубить понимание JavaScript — замыкания, прототипы, классы и практические паттерны проектирования.

> **Литература:** Kyle Simpson «YDKJS: Scope & Closures», «YDKJS: this & Object Prototypes», [learn.javascript.ru: Прототипы](https://learn.javascript.ru/prototype-inheritance), [patterns.dev](https://www.patterns.dev/), [MDN: Closures](https://developer.mozilla.org/ru/docs/Web/JavaScript/Closures), [javascript.info: Продвинутая работа с функциями](https://javascript.info/advanced-functions)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)

> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-09/`



## День 1 (Mon): Scope и замыкания
<a id="week-09-day-1"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library System**

### Теория

Область видимости (scope) определяет, где переменная доступна для чтения и записи. В JavaScript действует лексическая (статическая) область: функция «видит» переменные того места, где была **объявлена**, а не где вызвана. `let` и `const` создают блочную область (`{ ... }`), а устаревший `var` — функциональную, что приводит к неожиданным утечкам переменных из циклов.

Замыкание (closure) возникает, когда внутренняя функция сохраняет доступ к переменным внешней функции даже после того, как внешняя завершила выполнение. Практически это означает: `createCounter()` возвращает функции `increment` и `getValue`, которые «помнят» переменную `count` в своём лексическом окружении. Замыкания — основа приватности данных без классов: `createBankAccount(balance)` скрывает баланс от внешнего кода.

Классическая ловушка — цикл с `var` и `setTimeout`: все колбэки ссылаются на одну и ту же переменную `i` с финальным значением. `let` в цикле создаёт новую привязку на каждой итерации, решая проблему. Замыкания удерживают ссылки на внешние переменные и могут мешать сборщику мусора — не замыкай на большие объекты без необходимости.

**Читать:**
- [learn.javascript.ru: Замыкание](https://learn.javascript.ru/closure)
- [MDN: Closures](https://developer.mozilla.org/ru/docs/Web/JavaScript/Closures)
- [javascript.info: Замыкание](https://javascript.info/closure)

**Ключевая мысль:** замыкание — это функция плюс её лексическое окружение; на этом строятся приватность, фабрики и модульный паттерн.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

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
<a id="week-09-day-2"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library System**

### Теория

Ключевое слово `this` в JavaScript определяется не местом объявления функции, а **способом вызова**. Существует четыре правила (в порядке приоритета): 1) `new` binding — `this` указывает на новый объект; 2) explicit binding — `call`/`apply`/`bind` задают `this` явно; 3) implicit binding — `obj.method()` привязывает `this` к `obj`; 4) default binding — в strict mode `this` равен `undefined`, иначе `window`.

Потеря контекста — частая ошибка: `const fn = obj.handleClick; btn.addEventListener('click', fn)` передаёт функцию без объекта, и `this` внутри станет `undefined`. Решение — `bind`: `fn.bind(obj)` или стрелочная обёртка `() => obj.handleClick()`. Методы `call` и `apply` вызывают функцию немедленно с заданным `this`; `bind` возвращает новую функцию с навсегда привязанным контекстом.

Стрелочные функции **не имеют** собственного `this` — они берут `this` из окружающего лексического scope. Это удобно для колбэков (`map`, `setTimeout`), но делает стрелочные функции плохими методами объектов. В strict mode default binding безопаснее — случайная привязка к `window` исчезает.

**Читать:**
- [learn.javascript.ru: Методы привязки контекста](https://learn.javascript.ru/bind)
- [learn.javascript.ru: Справка по оператору this](https://learn.javascript.ru/reference-type)
- [MDN: this](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Operators/this)

**Ключевая мысль:** `this` — не переменная, а результат вызова; потеря контекста лечится `bind`, а стрелочные функции наследуют `this` снаружи.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git

```bash

cd learning-log/week-09

git add day-02-this.js day-02-this.md

git commit -m "week-09 day-02: this, bind и 4 правила контекста"

```



## День 3 (Wed): Прототипы и наследование
<a id="week-09-day-3"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library System**

### Теория

Наследование в JavaScript реализовано через цепочку прототипов, а не через классы в классическом ООП-смысле. Каждый объект имеет внутреннюю ссылку `[[Prototype]]` (доступна через `Object.getPrototypeOf` или устаревшее `__proto__`). При обращении к свойству движок ищет его на самом объекте, затем на прототипе, затем на прототипе прототипа — до `null`.

Функции-конструкторы создают объекты через `new`: `new Person('Anna')` создаёт объект, привязывает `this` и устанавливает `[[Prototype]]` равным `Person.prototype`. Методы размещают на `prototype`, чтобы все экземпляры делили одну функцию, а не копировали её. `Object.create(proto)` создаёт объект с заданным прототипом без конструктора — чистый способ наследования.

`instanceof` проверяет, есть ли `Constructor.prototype` в цепочке прототипов объекта — это не проверка «типа» в смысле TypeScript. `hasOwnProperty` отличает собственные свойства от унаследованных. Классы ES6 (`class Person`) — синтаксический сахар над этой же моделью; `typeof Person === 'function'`. Никогда не модифицируй `Array.prototype` или `Object.prototype` в production — это ломает чужой код.

**Читать:**
- [learn.javascript.ru: Прототипное наследование](https://learn.javascript.ru/prototype-inheritance)
- [learn.javascript.ru: F.prototype](https://learn.javascript.ru/function-prototype)
- [MDN: Object.create()](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/Object/create)

**Ключевая мысль:** прототипная цепочка — механизм делегирования свойств; `class` лишь удобная обёртка над ним.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git

```bash

cd learning-log/week-09

git add day-03-prototypes.js

git commit -m "week-09 day-03: прототипы, Person/Student и inherits"

```



## День 4 (Thu): Классы ES6+
<a id="week-09-day-4"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library System**

### Теория

Синтаксис `class` в ES6+ делает прототипное наследование читаемым. Класс объявляется как `class TodoItem { constructor(title) { ... } toggle() { ... } }`. Методы автоматически попадают на `prototype`. `extends` связывает прототипы дочернего и родительского классов, а `super()` в конструкторе вызывает родительский конструктор — без этого `this` в дочернем классе недоступен.

Статические методы (`static fromJSON(obj)`) принадлежат самому классу, а не экземплярам — удобны для фабрик и утилит. Геттеры и сеттеры (`get isOverdue()`) выглядят как свойства, но вычисляются при обращении. С ES2022 приватные поля `#id` дают настоящую инкапсуляцию: к ним нельзя обратиться снаружи, в отличие от конвенции `_id`.

Когда выбирать `class`, а когда factory + closure? Класс хорош для сущностей с общим прототипом и иерархией (`Book extends Media`). Factory с замыканием — для объектов с приватным состоянием без наследования. Под капотом `class` всё равно функция с `prototype` — `typeof TodoItem === 'function'`.

**Читать:**
- [learn.javascript.ru: Класс](https://learn.javascript.ru/class)
- [learn.javascript.ru: Наследование классов](https://learn.javascript.ru/class-inheritance)
- [MDN: Classes](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Classes)

**Ключевая мысль:** `class` — это читаемый синтаксис над прототипами; `#private` и `static` делают модель данных явной и безопасной.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git

```bash

cd learning-log/week-09

git add src/models/

git commit -m "week-09 day-04: классы TodoItem, Movie и private fields"

```



## День 5 (Fri): Паттерны проектирования
<a id="week-09-day-5"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library System**

### Теория

Паттерны проектирования — проверенные решения типовых задач в архитектуре кода. Observer (Pub-Sub) отделяет источник событий от подписчиков: store вызывает `emit('change', data)`, а UI подписывается через `on('change', render)`. Компоненты не знают друг о друге напрямую — слабая связанность упрощает рефакторинг. EventEmitter на 50 строк — отличная учебная реализация.

Module pattern (в ES modules — через `export`/`import`) инкапсулирует детали реализации: наружу видны только публичные функции. Strategy позволяет подменять алгоритм (сортировка `byDate` / `byTitle`) без ветвления `if/else` в клиентском коде — стратегия передаётся как функция. Factory (`createNotification('error', msg)`) скрывает создание объектов за единым интерфейсом.

Singleton гарантирует один экземпляр (например, глобальный store), но усложняет тестирование и создаёт скрытое глобальное состояние — используй осознанно. MVC/MVP разделяют Model (данные), View (DOM) и Controller (логика) — твой Todo уже движется в эту сторону. Главное правило: не применяй паттерн ради паттерна в проекте на 50 строк.

**Читать:**
- [patterns.dev: Observer Pattern](https://www.patterns.dev/vanilla/observer-pattern/)
- [patterns.dev: Module Pattern](https://www.patterns.dev/vanilla/module-pattern/)
- [patterns.dev](https://www.patterns.dev/)

**Ключевая мысль:** паттерн оправдан, когда он снижает связанность или упрощает расширение — не когда добавляет абстракцию ради абстракции.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git

```bash

cd learning-log/week-09

git add src/patterns/ src/store.js

git commit -m "week-09 day-05: EventEmitter, Strategy и Store/View"

```



## День 6 (Sat): Функциональные приёмы
<a id="week-09-day-6"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library System**

### Теория

Функциональное программирование в JavaScript — набор приёмов, делающих код предсказуемым. Чистая функция (pure function) при одинаковых аргументах всегда возвращает одинаковый результат и не вызывает побочных эффектов (не мутирует внешние переменные, не пишет в DOM). `map`, `filter`, `reduce` — примеры функций высшего порядка (HOF): они принимают функцию как аргумент и абстрагируют обход коллекции.

Композиция объединяет маленькие функции в конвейер: `pipe(validate, normalize, save)(input)` читается слева направо, `compose` — справа налево. Каррирование превращает `add(a, b)` в `add(a)(b)` — полезно для частичного применения (`filterBy('status', 'active')`). Иммутабельность достигается через spread и `structuredClone` вместо прямой мутации.

Рекурсия элегантна для деревьев и вложенных структур, но глубокая рекурсия упрётся в лимит стека (stack overflow). Для горячих путей предпочитай итерацию. `memoize(fn)` кэширует результаты чистой функции по аргументам — классический приём оптимизации. Referential transparency означает: можно заменить вызов функции её результатом без изменения поведения программы.

**Читать:**
- [learn.javascript.ru: Каррирование](https://learn.javascript.ru/currying-partials)
- [MDN: Array.prototype.reduce()](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce)
- [javascript.info: Рекурсия и стек](https://javascript.info/recursion)

**Ключевая мысль:** pure functions + immutability + composition дают код, который легко тестировать, переиспользовать и рассуждать о нём.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git

```bash

cd learning-log/week-09

git add src/utils/fp.js

git commit -m "week-09 day-06: pipe, currying и memoize"

```



## День 7 (Sun): Рефакторинг и code quality
<a id="week-09-day-7"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **Library System**

### Теория

Качество кода определяется не только работоспособностью, но и читаемостью, поддерживаемостью и предсказуемостью. SOLID в JavaScript-практике чаще всего сводится к двум принципам: Single Responsibility (один модуль — одна задача: `api.js` не рендерит DOM) и Dependency Inversion (высокоуровневый код зависит от абстракций, а не от конкретных реализаций). DRY (Don't Repeat Yourself) полезен, но иногда явное дублирование лучше преждевременной абстракции (правило WET — Write Everything Twice).

ESLint ловит ошибки до runtime: неиспользуемые переменные, потерянные `await`, проблемы с `==`. Prettier унифицирует форматирование — споры о пробелах исчезают. JSDoc документирует публичный API без TypeScript: `@param {string} url`, `@returns {Promise<User>}`. Это мост к строгой типизации на следующей неделе.

ADR (Architecture Decision Record) — короткий документ «почему выбрали Store + Observer, а не один монолитный файл». Code review checklist: понятные имена, нет скрытых side effects, ошибки обработаны, модули имеют чёткие границы. Подготовка к TypeScript — явные контракты функций через JSDoc или `.ts` файлы.

**Читать:**
- [JSDoc reference](https://jsdoc.app/)
- [ESLint: Getting Started](https://eslint.org/docs/latest/use/getting-started)
- [adr.github.io](https://adr.github.io/) — формат Architecture Decision Records

**Ключевая мысль:** инструменты (ESLint, JSDoc, ADR) и принципы (SRP, явные контракты) готовят кодовую базу к росту и TypeScript.



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



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

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


## Проверь себя

<details>
<summary>Что должно получиться к концу недели?</summary>

Работающий проект **Library System** в `learning-log/week-09/`, осмысленная Git-история, тег `week-09-done`.

</details>

<details>
<summary>Главный навык недели одной фразой?</summary>

Closures, ООП и паттерны в JavaScript

</details>

<details>
<summary>Можно ли пропустить день?</summary>

Нет — дни связаны. В **лайт-режиме** сократи практику до MVP, но теорию и Git-коммит не пропускай.

</details>
