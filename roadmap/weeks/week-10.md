# Неделя 10: TypeScript — типы, interfaces, generics basics, TS+React setup



> **Цель недели:** освоить основы TypeScript и подготовить проект к React с типизированной кодовой базой.

> **Литература:** [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html), [learn.javascript.ru: Типы](https://learn.javascript.ru/types), [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/), [Total TypeScript — Beginners](https://www.totaltypescript.com/tutorials/beginners-typescript), [TSConfig Reference](https://www.typescriptlang.org/tsconfig)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)

> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-10/`



## День 1 (Mon): Введение в TypeScript
<a id="week-10-day-1"></a>

> **Время (полный):** ~2ч теория · ~3ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1.5ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Typed API Client**

### Теория

TypeScript — это надмножество JavaScript со статической системой типов. Код пишется в `.ts` (или `.tsx` для JSX), компилируется компилятором `tsc` в обычный JavaScript, который выполняется в браузере или Node.js. Типы существуют только на этапе разработки и **стираются** при компиляции — в runtime никакой проверки типов нет. Зато IDE и компилятор ловят ошибки до запуска: опечатки в свойствах, неверные аргументы, забытые `null`.

Установка: `npm init -y`, `npm i -D typescript`, `npx tsc --init` создаёт `tsconfig.json`. Ключевые опции: `strict: true` (включает все строгие проверки), `target` (версия JS на выходе), `module` (система модулей), `outDir` и `rootDir`. Базовые типы: `string`, `number`, `boolean`, `null`, `undefined`, `bigint`, `symbol`. Аннотация явная: `let name: string = 'Anna'`, но чаще полагайся на вывод типов (inference): `const count = 0` → TypeScript сам определит `number`.

Команда `npx tsc --noEmit` проверяет типы без генерации файлов — удобно в CI. Разница `.ts` и `.tsx`: JSX-синтаксис допустим только в `.tsx`. Скрипт `"build": "tsc"` в `package.json` автоматизирует компиляцию, `"dev": "tsc --watch"` пересобирает при каждом сохранении.

Хорошая мысленная модель TypeScript — строительные леса вокруг здания: леса (типы) помогают безопасно и быстро строить, показывают, где не хватает опоры, но к моменту сдачи объекта (компиляции в JS) их полностью убирают — в готовом здании (браузере) лесов уже нет, только сам дом. Именно поэтому в runtime нет проверки типов: `interface User` не существует после компиляции, это чисто инструмент разработки, а не часть исполняемой программы.

Эта неделя — фундамент для всего оставшегося курса: React-компоненты, их props, состояние и API-слои в дальнейшем описываются практически исключительно на TypeScript, и большинство современных вакансий junior-frontend разработчика требуют именно TS, а не чистый JS. Инвестиция в понимание типов сейчас окупится кратно уже на неделе 11.

Частое заблуждение — думать, что TypeScript «медленнее» JavaScript в исполнении: это неверно, поскольку типы стираются до запуска, и скомпилированный `.js`-файл работает ровно с той же скоростью, что и написанный вручную JS. Единственная «цена» TypeScript — время компиляции (`tsc`) перед запуском, а не runtime-производительность. Конкретный пример пользы: `function add(a: number, b: number) { return a + b }`, вызванная как `add('2', '3')`, немедленно подсветится редактором как ошибка ещё до сохранения файла — в чистом JS та же ошибка обнаружилась бы только в runtime как склейка строк `'23'` вместо ожидаемого `5`, и такую опечатку легко пропустить в задании 4 практики («исправь все ошибки компиляции»).

**Читать:**
- [TypeScript: Getting Started](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html)
- [learn.javascript.ru: Типы](https://learn.javascript.ru/types)
- [TSConfig Reference](https://www.typescriptlang.org/tsconfig)

**Ключевая мысль:** TypeScript ловит целый класс ошибок на этапе компиляции — типы это документация, которую нельзя проигнорировать.



### Практика (полный трек)
1. Создай проект `learning-log/week-10`, инициализируй TypeScript
2. Перепиши `utils.js` из прошлых недель в `utils.ts`
3. Включи `strict: true` в `tsconfig.json`
4. Исправь все ошибки компиляции
5. Настрой скрипт `"build": "tsc"` в package.json
6. Добавь `"dev": "tsc --watch"` для автопересборки
7. Создай `src/index.ts` — точка входа, импорт utils









**Критерии:**

- [ ] `tsc` компилирует без ошибок

- [ ] `strict: true` включён

- [ ] Понимаю разницу .ts и .js на выходе

### Практика (лайт / MVP)
1. Создай проект `learning-log/week-10`, инициализируй TypeScript
2. Перепиши `utils.js` из прошлых недель в `utils.ts`
3. Включи `strict: true` в `tsconfig.json`
4. Исправь все ошибки компиляции

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Не понимаешь ошибку — прочитай её с конца: файл, строка, тип. Открой DevTools / терминал и воспроизведи на 5 строках кода.

### Git

```bash

cd learning-log/week-10

git add package.json tsconfig.json src/

git commit -m "week-10 day-01: инициализация TS-проекта и utils.ts"

```



## День 2 (Tue): Типы, union, literal, any
<a id="week-10-day-2"></a>

> **Время (полный):** ~2ч теория · ~3ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1.5ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Typed API Client**

### Теория

Union types объединяют несколько типов: `string | number` означает «или строка, или число». Literal types сужают множество до конкретных значений: `type Theme = 'light' | 'dark'` — не любая строка, а ровно два варианта. TypeScript не даст присвоить `'blue'`, если тип допускает только `'light' | 'dark'`. Это основа для моделирования состояний и флагов.

`any` отключает проверку типов — «дыра» в системе, через которую ошибки просачиваются обратно в runtime. Избегай `any`; вместо него используй `unknown` — тип «что-то есть, но мы не знаем что». С `unknown` нельзя ничего делать, пока не сузишь тип через `typeof`, `in` или type guard. Discriminated union добавляет общее поле-дискриминатор: `{ ok: true, data: T } | { ok: false, error: string }` — switch по `ok` сужает тип в каждой ветке.

`as const` делает объект readonly с literal-типами: `const STATUS = { LOADING: 'loading' } as const`. Тип `never` означает «недостижимо» — полезен в exhaustive switch: если добавишь новый вариант union, компилятор укажет на непокрытую ветку. Пользовательские type guards: `function isUser(x: unknown): x is User` — явный контракт сужения.

Мысленная модель union type — меню с ограниченным выбором, а не открытый вопрос «что хочешь съесть»: `type Theme = 'light' | 'dark'` — это меню из двух блюд, и компилятор физически не позволит «заказать» `'blue'`, потому что такого пункта нет. Это резко отличается от обычного `string`, который допускает любую строку — как меню без ограничений, где легко случайно заказать несуществующее блюдо и получить ошибку уже на кухне (в runtime).

Discriminated union и exhaustive switch — техника, которая будет использоваться постоянно при моделировании ответов API (успех/ошибка) и состояний UI (loading/success/error/empty, как в неделе 8) — только теперь эти состояния описываются типом, а не просто строкой, и компилятор гарантирует, что ни одна ветка не забыта. Это прямая подготовка к React, где состояния компонентов часто моделируются именно так.

Частое заблуждение — считать `any` и `unknown` взаимозаменяемыми, потому что оба «принимают что угодно». Разница принципиальна: `any` отключает все проверки для значения и всего, что из него получено (заражает код), а `unknown` требует явно сузить тип перед использованием — `const x: unknown = data; x.toUpperCase()` не скомпилируется, пока не добавишь `if (typeof x === 'string')`. Конкретный пример из практики: функция `formatId(id: string | number)`, где внутри нужно явно проверить `typeof id === 'string'`, прежде чем вызвать `.toUpperCase()` — иначе компилятор справедливо укажет, что у `number` такого метода нет.

**Читать:**
- [Handbook: Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)
- [Handbook: Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [Total TypeScript: Beginners](https://www.totaltypescript.com/tutorials/beginners-typescript)

**Ключевая мысль:** union + narrowing превращают TypeScript в инструмент моделирования состояний; `unknown` безопаснее `any`.



### Практика (полный трек)
1. Тип `Theme = 'light' | 'dark'` для переключателя темы
2. Функция `formatId(id: string | number): string` с narrowing
3. Замени `any` на `unknown` + проверку перед использованием
4. Discriminated union `Result = { ok: true, data: T } | { ok: false, error: string }`
5. Используй `as const` для объекта констант STATUS
6. Напиши type guard `isApiError(err): err is ApiError`
7. Exhaustive switch по union — `default: const _exhaustive: never = value`









**Критерии:**

- [ ] Нет `any` в новом коде

- [ ] Union types с корректным narrowing

- [ ] Result pattern для ошибок API

### Практика (лайт / MVP)
1. Тип `Theme = 'light' | 'dark'` для переключателя темы
2. Функция `formatId(id: string | number): string` с narrowing
3. Замени `any` на `unknown` + проверку перед использованием
4. Discriminated union `Result = { ok: true, data: T } | { ok: false, error: string }`

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Тесты/валидация красные — сначала один failing case, почини его, только потом следующий.

### Git

```bash

cd learning-log/week-10

git add src/types/

git commit -m "week-10 day-02: union, Result pattern и type guards"

```



### Ловушки

- `any` распространяется как зараза — теряется смысл TS

- Утверждение `as Type` без проверки — ложная безопасность

- Забытый `strictNullChecks` — null не ловится



## День 3 (Wed): Interfaces и type aliases
<a id="week-10-day-3"></a>

> **Время (полный):** ~2ч теория · ~3ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1.5ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Typed API Client**

### Теория

Объекты в TypeScript описываются через `interface` или `type`. `interface User { id: number; name: string; email?: string }` — `email?` опционален, его может не быть. `readonly id: number` запрещает переприсвоение после создания. Оба способа описывают форму объекта; различия тонкие: `interface` можно расширять (`extends`) и объединять (declaration merging), `type` гибче для union и mapped types.

Расширение: `interface Admin extends User { role: string }` добавляет поля. Альтернатива — intersection: `type Admin = User & { role: string }`. Index signature `[key: string]: string` описывает объекты с динамическими ключами (словари, кэши). Для объектов предпочитай `interface`, для union и вычисляемых типов — `type`.

Utility types из коробки: `Readonly<T>` делает все поля readonly, `ReadonlyArray<T>` — неизменяемый массив. В проекте заведи папку `types/` с DTO (Data Transfer Objects): `Todo`, `ApiResponse<T>`, `PaginationMeta`. Типизированный api-модуль возвращает `Promise<ApiResponse<Todo[]>>` вместо «что-то пришло с сервера». Это контракт между слоями, который компилятор проверяет.

Мысленная модель `interface`/`type` — бланк договора между частями программы: до того как API-функция вернёт данные, интерфейс уже фиксирует, какие поля там будут и какого они типа — это контракт, который компилятор проверяет на каждом использовании, а не просто комментарий-пожелание. Если сервер изменит форму ответа, а DTO забудут обновить, TypeScript не поймает несоответствие с реальным JSON (он не знает про сеть), но зато любой код внутри приложения, который ожидает поля по старому контракту, останется согласованным и предсказуемым.

Явные DTO в отдельной папке `types/` становятся особенно ценными на неделе 11: типы `Todo`, `ApiResponse<T>` из этой недели практически без изменений переедут в React-компоненты как типы props, избавляя от необходимости придумывать их заново. Хорошо спроектированные интерфейсы на этой неделе — это меньше работы на следующей.

Частое заблуждение — воспринимать `interface` и `type` как взаимоисключающий выбор «правильного» и «неправильного» инструмента: в большинстве junior-задач разница не критична, и команды чаще выбирают один стиль как конвенцию проекта, а не по глубоким техническим причинам. Единственный практический критерий, который стоит запомнить: если нужен union (`'a' | 'b'`) или вычисляемый тип — это всегда `type`, поскольку `interface` такого не умеет; если нужно расширяемое описание формы объекта с возможностью declaration merging — чуть удобнее `interface`. Задание 4 практики («расширь User → Admin») — хороший повод попробовать оба варианта (`extends` и `&`) и увидеть, что результат идентичен.

**Читать:**
- [Handbook: Objects](https://www.typescriptlang.org/docs/handbook/2/objects.html)
- [Handbook: Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

**Ключевая мысль:** interface/type — это контракт формы данных; DTO в отдельных файлах делают API и доменную модель явными.



### Практика (полный трек)
1. Интерфейсы `Todo`, `TodoFilter`, `TodoState` для Todo App
2. `interface ApiResponse<T> { data: T; meta: PaginationMeta }`
3. Type alias для функции: `type EventHandler = (e: Event) => void`
4. Расширь `User` → `Admin` с полем `permissions: string[]`
5. Рефакторинг api-модуля с типизированными ответами
6. Создай `types/api.ts` — все DTO в одном месте
7. Добавь `readonly` к id в Todo — попробуй изменить и поймай ошибку TS









**Критерии:**

- [ ] Все доменные сущности типизированы

- [ ] interface vs type — осознанный выбор

- [ ] Опциональные и readonly поля использованы

### Практика (лайт / MVP)
1. Интерфейсы `Todo`, `TodoFilter`, `TodoState` для Todo App
2. `interface ApiResponse<T> { data: T; meta: PaginationMeta }`
3. Type alias для функции: `type EventHandler = (e: Event) => void`
4. Расширь `User` → `Admin` с полем `permissions: string[]`

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Застрял >20 мин — выпиши вход/выход задачи в 3 строки. Сделай минимальный пример в `playground.*`, без копипаста из ИИ.

### Git

```bash

cd learning-log/week-10

git add src/types/ src/api/

git commit -m "week-10 day-03: интерфейсы Todo и ApiResponse"

```



## День 4 (Thu): Generics — основы
<a id="week-10-day-4"></a>

> **Время (полный):** ~2ч теория · ~3ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1.5ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Typed API Client**

### Теория

Generics (обобщения) позволяют писать функции и типы, работающие с разными типами, сохраняя связь между входом и выходом. `function identity<T>(arg: T): T` — тип возвращаемого значения совпадает с типом аргумента. Без generics пришлось бы писать отдельные функции для `string`, `number`, `User` или откатываться к `any`.

Constraints ограничивают generic сверху: `<T extends { id: number }>` гарантирует, что у `T` есть поле `id`. `keyof T` даёт union всех ключей объекта, а indexed access `T[K]` — тип значения по ключу. Это основа для `pluck(obj, 'name')` с правильным return type. Generic defaults `<T = string>` задают тип по умолчанию, если параметр не указан.

Практические применения: `async function fetchJson<T>(url: string): Promise<T>` типизирует ответ API; `getItem<T>(key: string): T | null` типизирует localStorage wrapper; `groupBy<T, K extends string>(items, keyFn)` группирует массив любых объектов. IDE будет подсказывать поля на результате `fetchJson<User[]>(url)` без ручных кастов.

Мысленная модель generic — форма для отливки, которая подходит под любой материал, но сохраняет форму: `function identity<T>(arg: T): T` — это форма, куда можно залить строку, число или объект, и на выходе гарантированно получить то же самое, что залили, а не что-то другое. Без generics пришлось бы либо копировать функцию под каждый тип материала, либо использовать `any` — и тогда форма перестаёт что-либо гарантировать, превращаясь в дырявое ведро.

Generics — пожалуй, самая мощная идея TypeScript для junior-разработчика, потому что она напрямую используется в React: `useState<Todo[]>([])`, `useRef<HTMLInputElement>(null)`, `useContext<AuthContextType>` — все эти хуки на неделе 11 и позже являются generic-функциями. Тот, кто разобрался с `fetchJson<T>` сегодня, не удивится синтаксису `useState<T>` через несколько недель.

Частое заблуждение — путать generic-параметр `<T>` с типом `any`, считая, что раз буква `T` может быть «чем угодно», значит проверки нет вообще. На самом деле после того, как `T` определён при вызове (`fetchJson<User>(url)`), TypeScript отслеживает его строго во всей функции. Конкретный пример пользы: `const user = await fetchJson<User>('/api/user')` даёт автодополнение по полям `user.name`, `user.email` прямо в IDE — тогда как `fetchJson('/api/user')` без указания типа вернёт `unknown`, и обратиться к `.name` без явной проверки не получится, что стоит заметить в задании 7 практики («проверь inference в IDE»).

Ещё один полезный приём — generic по умолчанию: `class ApiClient<T = unknown>` позволяет использовать `new ApiClient()` без явного указания типа, если он не критичен в конкретном месте, но при необходимости уточнить его как `new ApiClient<User>()`. Это балансирует гибкость и строгость, не заставляя писать `<T>` там, где тип и так очевиден из контекста.

**Читать:**
- [Handbook: Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)
- [Handbook: Keyof Types](https://www.typescriptlang.org/docs/handbook/2/keyof-types.html)
- [Total TypeScript: Beginners](https://www.totaltypescript.com/tutorials/beginners-typescript)

**Ключевая мысль:** generics связывают типы входа и выхода — `fetchJson<User>` безопаснее `fetchJson<any>`.



### Практика (полный трек)
1. `function first<T>(arr: T[]): T | undefined`
2. `async function fetchJson<T>(url: string): Promise<T>` — типизированный fetch
3. `function groupBy<T, K extends string>(items: T[], key: (item: T) => K)`
4. Типизируй localStorage wrapper: `getItem<T>(key): T | null`
5. Примени generics в api-клиенте каталога фильмов
6. `function pluck<T, K extends keyof T>(obj: T, key: K): T[K]`
7. Напиши тестовые вызовы с разными T — проверь inference в IDE









**Критерии:**

- [ ] fetchJson типизирует ответ API

- [ ] groupBy работает с разными типами

- [ ] Constraints использован хотя бы раз

### Практика (лайт / MVP)
1. `function first<T>(arr: T[]): T | undefined`
2. `async function fetchJson<T>(url: string): Promise<T>` — типизированный fetch
3. `function groupBy<T, K extends string>(items: T[], key: (item: T) => K)`
4. Типизируй localStorage wrapper: `getItem<T>(key): T | null`

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Документация не клеится — найди один официальный пример (MDN / docs) и сопоставь 1:1 со своим кодом.

### Git

```bash

cd learning-log/week-10

git add src/lib/fetch.ts src/lib/storage.ts

git commit -m "week-10 day-04: generic fetchJson и localStorage wrapper"

```



## День 5 (Fri): Функции, utility types, enums
<a id="week-10-day-5"></a>

> **Время (полный):** ~2ч теория · ~3ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1.5ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Typed API Client**

### Теория

Типизация функций в TypeScript охватывает параметры, возвращаемое значение и перегрузки. Optional параметры (`name?: string`), значения по умолчанию (`size = 'md'`) и rest (`...args: number[]`) типизируются явно. Return type можно вывести (inference), но явный return полезен для публичного API — компилятор проверит, что все ветки возвращают заявленный тип.

Utility types трансформируют существующие типы: `Partial<T>` делает все поля опциональными (удобно для update DTO), `Pick<T, 'title' | 'done'>` выбирает подмножество полей, `Omit<T, 'id'>` исключает поля, `Record<Keys, Type>` строит объект с заданными ключами. Пример: `type UpdateTodo = Partial<Pick<Todo, 'title' | 'done'>>` — обновление только разрешённых полей.

`enum` в modern TypeScript уступает union of literals: `const STATUS = { LOADING: 'loading', SUCCESS: 'success' } as const; type Status = typeof STATUS[keyof typeof STATUS]`. Такой подход лучше tree-shaking и не генерирует лишний JS. Function overloads задают несколько сигнатур для одной реализации. `Parameters<T>` и `ReturnType<T>` извлекают типы из существующих функций. Оператор `satisfies` (TS 4.9+) проверяет тип, сохраняя literal inference.

Мысленная модель utility types — конструктор Lego, где из готовых кубиков (существующих типов) собираются новые формы без ручной лепки с нуля: `Partial<Todo>` берёт тип `Todo` и говорит «все поля теперь опциональны», `Pick<Todo, 'title'>` — «оставь только эту деталь», `Omit<Todo, 'id'>` — «убери эту деталь, остальное оставь». Это избавляет от ручного дублирования почти идентичных интерфейсов для create/update/read версий одной и той же сущности.

Эти приёмы напрямую переносятся в API-слои React-приложений: типичный паттерн `type CreateTodoDto = Omit<Todo, 'id' | 'createdAt'>` (сервер сам генерирует id и дату) встречается в подавляющем большинстве реальных проектов, и понимание его сегодня избавит от копипасты интерфейсов позже. Замена `enum` на `as const` объект — тоже не просто вкусовщина: `enum` исторически генерирует дополнительный JS-код при компиляции, тогда как `as const` полностью стирается, что мельче бандл и лучше tree-shaking для production-сборки на Vite (день 6 этой недели).

Частое заблуждение — думать, что `Partial<T>` делает объект необязательным целиком, а не каждое поле по отдельности: `Partial<Todo>` всё ещё требует объект (не `undefined`), просто каждое его свойство (`title`, `done`) можно опустить. Конкретный пример из практики: `type UpdateTodo = Partial<Pick<Todo, 'title' | 'done'>>` описывает ровно то, что можно менять при PATCH-запросе — не весь Todo целиком и не произвольные поля, а только title и done, оба опционально.

**Читать:**
- [Handbook: Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)
- [Handbook: More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html)
- [TypeScript 4.9: satisfies](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html#the-satisfies-operator)

**Ключевая мысль:** utility types — конструктор из существующих типов; `Partial`/`Pick`/`Omit` заменяют ручное дублирование DTO.



### Практика (полный трек)
1. `UpdateTodo = Partial<Pick<Todo, 'title' | 'done'>>`
2. `Record<Theme, string>` для CSS-переменных по темам
3. Замени enum статусов на `as const` объект + union type
4. Overload: `createElement(tag: 'div'): HTMLDivElement` (упрощённо)
5. Типизируй EventEmitter из недели 9 generics `<T>`
6. `Required<Pick<Todo, 'title'>>` для create DTO
7. Используй `ReturnType<typeof fetchJson>` в обёртке









**Критерии:**

- [ ] Partial/Pick/Omit в рефакторинге

- [ ] const assertion вместо enum

- [ ] EventEmitter типизирован

### Практика (лайт / MVP)
1. `UpdateTodo = Partial<Pick<Todo, 'title' | 'done'>>`
2. `Record<Theme, string>` для CSS-переменных по темам
3. Замени enum статусов на `as const` объект + union type
4. Overload: `createElement(tag: 'div'): HTMLDivElement` (упрощённо)

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Не понимаешь ошибку — прочитай её с конца: файл, строка, тип. Открой DevTools / терминал и воспроизведи на 5 строках кода.

### Git

```bash

cd learning-log/week-10

git add src/lib/event-emitter.ts

git commit -m "week-10 day-05: utility types и типизированный EventEmitter"

```



## День 6 (Sat): TS + React setup
<a id="week-10-day-6"></a>

> **Время (полный):** ~2ч теория · ~3ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1.5ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Typed API Client**

### Теория

Vite — современный инструмент сборки для фронтенда с мгновенным dev-сервером и HMR (Hot Module Replacement). Создание React + TypeScript проекта: `npm create vite@latest my-app -- --template react-ts`. Структура: `src/main.tsx` — точка входа, `App.tsx` — корневой компонент, `vite-env.d.ts` — типы Vite. TypeScript настроен из коробки.

Props React-компонента типизируются через interface: `interface ButtonProps { label: string; onClick: () => void; variant?: 'primary' | 'secondary'; disabled?: boolean }`. Современная рекомендация — обычная функция `function Button({ label, onClick }: ButtonProps)`, а не `React.FC` (устаревший паттерн с неявным `children`). `React.ReactNode` описывает всё, что можно отрендерить (строки, числа, элементы, массивы, null). `React.ReactElement` — конкретно JSX-элемент.

Vite конфигурируется в `vite.config.ts`; path aliases настраиваются и в tsconfig, и в vite. React Strict Mode в dev намеренно вызывает двойной render компонентов, чтобы выявить побочные эффекты — это нормально и не баг. Команды: `npm run dev` (разработка), `npm run build` (production-сборка с проверкой типов).

Мысленная модель Vite — конвейер быстрой сборки с горячей заменой деталей на ходу: вместо того чтобы каждый раз пересобирать весь автомобиль (bundle) с нуля при малейшей правке, HMR подменяет только изменённую деталь (модуль) прямо во время движения, не перезагружая всю страницу и сохраняя текущее состояние компонентов (например, введённый в форму текст).

Всё, что изучалось эту неделю — интерфейсы, generics, utility types — сходится именно здесь: типизация props компонента — первое место, где TypeScript встречается с React напрямую, и качество этого стыка определяет, насколько безопасно можно будет рефакторить компоненты в дальнейшем на неделе 11. Хорошо типизированный `ButtonProps` — это защита от передачи `onClick={someString}` по ошибке, которую поймает компилятор, а не пользователь в браузере.

Частое заблуждение — использовать `React.FC<Props>` для типизации компонентов по старой памяти из туториалов пятилетней давности: современное сообщество React рекомендует обычную функцию с типизированными параметрами (`function Button(props: ButtonProps)`), поскольку `React.FC` неявно добавляет `children` всем компонентам (даже тем, где children не предполагается) и хуже работает с generic-компонентами. Конкретный пример из задания 4 практики — `Card` с `children: React.ReactNode`: `ReactNode` покрывает всё, что React способен отрендерить (строка, число, JSX, массив, `null`), тогда как `ReactElement` — только конкретный JSX-элемент.

Ещё одна деталь, которая экономит время: файлы Vite с JSX обязаны иметь расширение `.tsx`, а не `.ts` — компилятор попросту не поймёт синтаксис `<div>` внутри `.ts`-файла и попытается интерпретировать угловые скобки как generic-приведение типов, выдав криптичную ошибку. Эта путаница — частая причина первых «непонятных» ошибок при переносе логики из `.ts` в компонент.

**Читать:**
- [React TypeScript Cheatsheet: Setup](https://react-typescript-cheatsheet.netlify.app/docs/basic/setup)
- [Vite Guide](https://vite.dev/guide/)
- [react.dev: Quick Start](https://react.dev/learn)

**Ключевая мысль:** Vite + react-ts даёт типизированный старт за минуту; props типизируй через interface, не через React.FC.



### Практика (полный трек)
1. Создай проект Vite + React + TypeScript в `week-10/`
2. Перенеси типы Todo в `src/types/todo.ts`
3. Компонент `Button` с props: `label`, `onClick`, `variant?`, `disabled?`
4. Компонент `Card` с `children: React.ReactNode`
5. Запусти `npm run dev`, убедись что HMR работает
6. Компонент `TodoItem` с типизированными props из `types/todo.ts`
7. Проверь `npm run build` — production без ошибок TS









**Критерии:**

- [ ] Vite проект запускается

- [ ] Минимум 2 типизированных компонента

- [ ] Типы вынесены в отдельные файлы

### Практика (лайт / MVP)
1. Создай проект Vite + React + TypeScript в `week-10/`
2. Перенеси типы Todo в `src/types/todo.ts`
3. Компонент `Button` с props: `label`, `onClick`, `variant?`, `disabled?`
4. Компонент `Card` с `children: React.ReactNode`

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Тесты/валидация красные — сначала один failing case, почини его, только потом следующий.

### Git

```bash

cd learning-log/week-10

git add src/components/

git commit -m "week-10 day-06: Vite react-ts, Button и Card"

```



## День 7 (Sun): Миграция и strict mode
<a id="week-10-day-7"></a>

> **Время (полный):** ~2ч теория · ~3ч практика · ~15м Git · ~45м ревью  
> **Время (лайт):** ~55м теория · ~1.5ч практика (MVP) · ~10м Git  
> **Связь с проектом:** шаг к **Typed API Client**

### Теория

Миграция существующего JS-проекта на TypeScript может быть постепенной. В `tsconfig.json` включи `allowJs: true` — компилятор будет проверять `.js` файлы рядом с `.ts`. `checkJs: true` добавляет проверку типов в JS через JSDoc-аннотации. Переименовывай файлы по одному: `api.js` → `api.ts`, исправляй ошибки, коммить.

Типы для npm-пакетов без встроенной типизации лежат в DefinitelyTyped: `@types/react`, `@types/node`. Declaration files (`.d.ts`) описывают форму JS-модуля без реализации — нужны для legacy-библиотек. Path aliases в tsconfig (`"@/*": ["src/*"]`) и в `vite.config.ts` сокращают импорты: `import { Button } from '@/components/Button'`.

Строгие опции поверх `strict`: `noUncheckedIndexedAccess` добавляет `| undefined` к `arr[i]` и `obj[key]` — заставляет проверять границы. `exactOptionalPropertyTypes` различает «поле отсутствует» и «поле равно `undefined`». Документируй решения tsconfig в `docs/typescript.md` — будущий ты (и команда) скажут спасибо.

Мысленная модель постепенной миграции — замена деталей в работающем автомобиле на ходу, а не разбор его на запчасти в гараже на неделю: `allowJs: true` позволяет `.ts` и `.js` файлам существовать бок о бок и импортировать друг друга, пока файлы переименовываются по одному (`api.js` → `api.ts`), а не одним гигантским коммитом, который рискует сломать всё сразу и который невозможно нормально код-ревьюить.

Этот навык напрямую пригодится в реальной работе: подавляющее большинство существующих production-кодовых баз в индустрии — это не написанный с нуля на строгом TypeScript проект, а именно постепенно мигрирующий JS-код, и умение делать это безопасно, файл за файлом, ценится не меньше умения писать типы с нуля. `noUncheckedIndexedAccess` — одна из самых важных строгих опций, о которой часто не знают даже после нескольких месяцев с TypeScript.

Частое заблуждение — считать, что `strict: true` уже покрывает все возможные проверки безопасности типов: на самом деле `noUncheckedIndexedAccess` не входит в `strict` по историческим причинам обратной совместимости, и без неё `const item = arr[999]` в массиве из трёх элементов будет типизирован как обычный элемент, а не `T | undefined`, хотя в runtime там окажется `undefined` — источник классических «Cannot read property of undefined» уже после успешной компиляции. Задание 3 практики («включи noUncheckedIndexedAccess — исправь новые ошибки») специально показывает, сколько скрытых мест в коде полагались на удачу при обращении по индексу.

Не стоит включать все строгие опции разом «для галочки»: каждая новая опция может вскрыть десятки мест в существующем коде, требующих исправления, и разумнее включать их по одной, коммитить исправления отдельно и двигаться к максимальной строгости постепенно — это тот же принцип итеративной миграции, что и с самим переходом с JS на TS.

**Читать:**
- [Handbook: Migrating from JavaScript](https://www.typescriptlang.org/docs/handbook/migrating-from-javascript.html)
- [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped)
- [TSConfig: noUncheckedIndexedAccess](https://www.typescriptlang.org/tsconfig#noUncheckedIndexedAccess)

**Ключевая мысль:** миграция на TS — итеративный процесс; strict-опции и path aliases делают кодовую базу надёжнее с каждым коммитом.



### Практика (полный трек)
1. Настрой alias `@/` в tsconfig и vite.config
2. Мигрируй api-модуль в TS с полной типизацией
3. Включи `noUncheckedIndexedAccess` — исправь новые ошибки
4. Напиши `.d.ts` для маленькой JS-библиотеки без типов (mock)
5. Документируй tsconfig решения в `docs/typescript.md`
6. Собери **Typed API Client** — финальная структура пакета
7. Тег `week-10-done` после проверки strict mode









**Критерии:**

- [ ] Path aliases работают

- [ ] api модуль полностью типизирован

- [ ] noUncheckedIndexedAccess не ломает сборку

### Практика (лайт / MVP)
1. Настрой alias `@/` в tsconfig и vite.config
2. Мигрируй api-модуль в TS с полной типизацией
3. Включи `noUncheckedIndexedAccess` — исправь новые ошибки
4. Напиши `.d.ts` для маленькой JS-библиотеки без типов (mock)

> Лайт-DoD: этих шагов достаточно, если теория прочитана и есть коммит.



### Если застрял

Застрял >20 мин — выпиши вход/выход задачи в 3 строки. Сделай минимальный пример в `playground.*`, без копипаста из ИИ.

### Git

```bash

cd learning-log/week-10

git add .

git commit -m "week-10 day-07: strict tsconfig и Typed API Client"

```



## Проект недели



**Typed API Client** — TS-библиотека + Vite React shell. Подробное ТЗ: [docs/projects.md — Неделя 10](../../docs/projects.md#неделя-10--typed-api-client).



Пакет: типы, generic `fetchJson<T>`, localStorage repo, unit-типы для всех функций. React: заглушка App с Button и Card.



**Функции:**

- Generic HTTP-клиент с `Result<T>` pattern и обработкой ошибок

- Типизированный репозиторий Todo в localStorage

- DTO для create/update через `Partial`/`Pick`

- React shell: демо-компоненты, подключение типов из библиотеки



**Критерии проекта:**

- [ ] strict TypeScript, zero `any` в `src/`

- [ ] Generics в fetch и storage

- [ ] Utility types для update DTOs

- [ ] Vite react-ts scaffold с 2+ компонентами

- [ ] `docs/typescript.md` с объяснением tsconfig

- [ ] README с `npm run build` и `npm run dev`

- [ ] Тег `week-10-done`



## Ревью-чеклист

- Зачем TypeScript если есть JS?

- Разница `interface` и `type`?

- Когда `unknown` лучше `any`?

- Что делает `Partial<T>` и `Pick<T, K>`?

- Как типизировать props React-компонента?


## Проверь себя

<details>
<summary>Что должно получиться к концу недели?</summary>

Работающий проект **Typed API Client** в `learning-log/week-10/`, осмысленная Git-история, тег `week-10-done`.

</details>

<details>
<summary>Главный навык недели одной фразой?</summary>

TypeScript strict: типы без any

</details>

<details>
<summary>Можно ли пропустить день?</summary>

Нет — дни связаны. В **лайт-режиме** сократи практику до MVP, но теорию и Git-коммит не пропускай.

</details>
