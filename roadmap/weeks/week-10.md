# Неделя 10: TypeScript — типы, interfaces, generics basics, TS+React setup



> **Цель недели:** освоить основы TypeScript и подготовить проект к React с типизированной кодовой базой.

> **Литература:** [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html), [learn.javascript.ru: TypeScript](https://learn.javascript.ru/typescript), [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/), [Total TypeScript — Beginners](https://www.totaltypescript.com/tutorials/beginners-typescript), [TSConfig Reference](https://www.typescriptlang.org/tsconfig)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)

> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-10/`



## День 1 (Mon): Введение в TypeScript



### Теория

TypeScript — это надмножество JavaScript со статической системой типов. Код пишется в `.ts` (или `.tsx` для JSX), компилируется компилятором `tsc` в обычный JavaScript, который выполняется в браузере или Node.js. Типы существуют только на этапе разработки и **стираются** при компиляции — в runtime никакой проверки типов нет. Зато IDE и компилятор ловят ошибки до запуска: опечатки в свойствах, неверные аргументы, забытые `null`.

Установка: `npm init -y`, `npm i -D typescript`, `npx tsc --init` создаёт `tsconfig.json`. Ключевые опции: `strict: true` (включает все строгие проверки), `target` (версия JS на выходе), `module` (система модулей), `outDir` и `rootDir`. Базовые типы: `string`, `number`, `boolean`, `null`, `undefined`, `bigint`, `symbol`. Аннотация явная: `let name: string = 'Anna'`, но чаще полагайся на вывод типов (inference): `const count = 0` → TypeScript сам определит `number`.

Команда `npx tsc --noEmit` проверяет типы без генерации файлов — удобно в CI. Разница `.ts` и `.tsx`: JSX-синтаксис допустим только в `.tsx`. Скрипт `"build": "tsc"` в `package.json` автоматизирует компиляцию, `"dev": "tsc --watch"` пересобирает при каждом сохранении.

**Читать:**
- [TypeScript: Getting Started](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html)
- [learn.javascript.ru: TypeScript](https://learn.javascript.ru/typescript)
- [TSConfig Reference](https://www.typescriptlang.org/tsconfig)

**Ключевая мысль:** TypeScript ловит целый класс ошибок на этапе компиляции — типы это документация, которую нельзя проигнорировать.



### Практика

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



### Git

```bash

cd learning-log/week-10

git add package.json tsconfig.json src/

git commit -m "week-10 day-01: инициализация TS-проекта и utils.ts"

```



## День 2 (Tue): Типы, union, literal, any



### Теория

Union types объединяют несколько типов: `string | number` означает «или строка, или число». Literal types сужают множество до конкретных значений: `type Theme = 'light' | 'dark'` — не любая строка, а ровно два варианта. TypeScript не даст присвоить `'blue'`, если тип допускает только `'light' | 'dark'`. Это основа для моделирования состояний и флагов.

`any` отключает проверку типов — «дыра» в системе, через которую ошибки просачиваются обратно в runtime. Избегай `any`; вместо него используй `unknown` — тип «что-то есть, но мы не знаем что». С `unknown` нельзя ничего делать, пока не сузишь тип через `typeof`, `in` или type guard. Discriminated union добавляет общее поле-дискриминатор: `{ ok: true, data: T } | { ok: false, error: string }` — switch по `ok` сужает тип в каждой ветке.

`as const` делает объект readonly с literal-типами: `const STATUS = { LOADING: 'loading' } as const`. Тип `never` означает «недостижимо» — полезен в exhaustive switch: если добавишь новый вариант union, компилятор укажет на непокрытую ветку. Пользовательские type guards: `function isUser(x: unknown): x is User` — явный контракт сужения.

**Читать:**
- [Handbook: Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)
- [Handbook: Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [Total TypeScript: Beginners](https://www.totaltypescript.com/tutorials/beginners-typescript)

**Ключевая мысль:** union + narrowing превращают TypeScript в инструмент моделирования состояний; `unknown` безопаснее `any`.



### Практика

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



### Теория

Объекты в TypeScript описываются через `interface` или `type`. `interface User { id: number; name: string; email?: string }` — `email?` опционален, его может не быть. `readonly id: number` запрещает переприсвоение после создания. Оба способа описывают форму объекта; различия тонкие: `interface` можно расширять (`extends`) и объединять (declaration merging), `type` гибче для union и mapped types.

Расширение: `interface Admin extends User { role: string }` добавляет поля. Альтернатива — intersection: `type Admin = User & { role: string }`. Index signature `[key: string]: string` описывает объекты с динамическими ключами (словари, кэши). Для объектов предпочитай `interface`, для union и вычисляемых типов — `type`.

Utility types из коробки: `Readonly<T>` делает все поля readonly, `ReadonlyArray<T>` — неизменяемый массив. В проекте заведи папку `types/` с DTO (Data Transfer Objects): `Todo`, `ApiResponse<T>`, `PaginationMeta`. Типизированный api-модуль возвращает `Promise<ApiResponse<Todo[]>>` вместо «что-то пришло с сервера». Это контракт между слоями, который компилятор проверяет.

**Читать:**
- [Handbook: Objects](https://www.typescriptlang.org/docs/handbook/2/objects.html)
- [Handbook: Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/docs/basic/typography)

**Ключевая мысль:** interface/type — это контракт формы данных; DTO в отдельных файлах делают API и доменную модель явными.



### Практика

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



### Git

```bash

cd learning-log/week-10

git add src/types/ src/api/

git commit -m "week-10 day-03: интерфейсы Todo и ApiResponse"

```



## День 4 (Thu): Generics — основы



### Теория

Generics (обобщения) позволяют писать функции и типы, работающие с разными типами, сохраняя связь между входом и выходом. `function identity<T>(arg: T): T` — тип возвращаемого значения совпадает с типом аргумента. Без generics пришлось бы писать отдельные функции для `string`, `number`, `User` или откатываться к `any`.

Constraints ограничивают generic сверху: `<T extends { id: number }>` гарантирует, что у `T` есть поле `id`. `keyof T` даёт union всех ключей объекта, а indexed access `T[K]` — тип значения по ключу. Это основа для `pluck(obj, 'name')` с правильным return type. Generic defaults `<T = string>` задают тип по умолчанию, если параметр не указан.

Практические применения: `async function fetchJson<T>(url: string): Promise<T>` типизирует ответ API; `getItem<T>(key: string): T | null` типизирует localStorage wrapper; `groupBy<T, K extends string>(items, keyFn)` группирует массив любых объектов. IDE будет подсказывать поля на результате `fetchJson<User[]>(url)` без ручных кастов.

**Читать:**
- [Handbook: Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)
- [Handbook: Keyof Types](https://www.typescriptlang.org/docs/handbook/2/keyof-types.html)
- [Total TypeScript: Generics](https://www.totaltypescript.com/tutorials/type-transformations)

**Ключевая мысль:** generics связывают типы входа и выхода — `fetchJson<User>` безопаснее `fetchJson<any>`.



### Практика

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



### Git

```bash

cd learning-log/week-10

git add src/lib/fetch.ts src/lib/storage.ts

git commit -m "week-10 day-04: generic fetchJson и localStorage wrapper"

```



## День 5 (Fri): Функции, utility types, enums



### Теория

Типизация функций в TypeScript охватывает параметры, возвращаемое значение и перегрузки. Optional параметры (`name?: string`), значения по умолчанию (`size = 'md'`) и rest (`...args: number[]`) типизируются явно. Return type можно вывести (inference), но явный return полезен для публичного API — компилятор проверит, что все ветки возвращают заявленный тип.

Utility types трансформируют существующие типы: `Partial<T>` делает все поля опциональными (удобно для update DTO), `Pick<T, 'title' | 'done'>` выбирает подмножество полей, `Omit<T, 'id'>` исключает поля, `Record<Keys, Type>` строит объект с заданными ключами. Пример: `type UpdateTodo = Partial<Pick<Todo, 'title' | 'done'>>` — обновление только разрешённых полей.

`enum` в modern TypeScript уступает union of literals: `const STATUS = { LOADING: 'loading', SUCCESS: 'success' } as const; type Status = typeof STATUS[keyof typeof STATUS]`. Такой подход лучше tree-shaking и не генерирует лишний JS. Function overloads задают несколько сигнатур для одной реализации. `Parameters<T>` и `ReturnType<T>` извлекают типы из существующих функций. Оператор `satisfies` (TS 4.9+) проверяет тип, сохраняя literal inference.

**Читать:**
- [Handbook: Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)
- [Handbook: More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html)
- [TypeScript 4.9: satisfies](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html#the-satisfies-operator)

**Ключевая мысль:** utility types — конструктор из существующих типов; `Partial`/`Pick`/`Omit` заменяют ручное дублирование DTO.



### Практика

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



### Git

```bash

cd learning-log/week-10

git add src/lib/event-emitter.ts

git commit -m "week-10 day-05: utility types и типизированный EventEmitter"

```



## День 6 (Sat): TS + React setup



### Теория

Vite — современный инструмент сборки для фронтенда с мгновенным dev-сервером и HMR (Hot Module Replacement). Создание React + TypeScript проекта: `npm create vite@latest my-app -- --template react-ts`. Структура: `src/main.tsx` — точка входа, `App.tsx` — корневой компонент, `vite-env.d.ts` — типы Vite. TypeScript настроен из коробки.

Props React-компонента типизируются через interface: `interface ButtonProps { label: string; onClick: () => void; variant?: 'primary' | 'secondary'; disabled?: boolean }`. Современная рекомендация — обычная функция `function Button({ label, onClick }: ButtonProps)`, а не `React.FC` (устаревший паттерн с неявным `children`). `React.ReactNode` описывает всё, что можно отрендерить (строки, числа, элементы, массивы, null). `React.ReactElement` — конкретно JSX-элемент.

Vite конфигурируется в `vite.config.ts`; path aliases настраиваются и в tsconfig, и в vite. React Strict Mode в dev намеренно вызывает двойной render компонентов, чтобы выявить побочные эффекты — это нормально и не баг. Команды: `npm run dev` (разработка), `npm run build` (production-сборка с проверкой типов).

**Читать:**
- [React TypeScript Cheatsheet: Setup](https://react-typescript-cheatsheet.netlify.app/docs/basic/setup)
- [Vite Guide](https://vite.dev/guide/)
- [react.dev: Quick Start](https://react.dev/learn)

**Ключевая мысль:** Vite + react-ts даёт типизированный старт за минуту; props типизируй через interface, не через React.FC.



### Практика

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



### Git

```bash

cd learning-log/week-10

git add src/components/

git commit -m "week-10 day-06: Vite react-ts, Button и Card"

```



## День 7 (Sun): Миграция и strict mode



### Теория

Миграция существующего JS-проекта на TypeScript может быть постепенной. В `tsconfig.json` включи `allowJs: true` — компилятор будет проверять `.js` файлы рядом с `.ts`. `checkJs: true` добавляет проверку типов в JS через JSDoc-аннотации. Переименовывай файлы по одному: `api.js` → `api.ts`, исправляй ошибки, коммить.

Типы для npm-пакетов без встроенной типизации лежат в DefinitelyTyped: `@types/react`, `@types/node`. Declaration files (`.d.ts`) описывают форму JS-модуля без реализации — нужны для legacy-библиотек. Path aliases в tsconfig (`"@/*": ["src/*"]`) и в `vite.config.ts` сокращают импорты: `import { Button } from '@/components/Button'`.

Строгие опции поверх `strict`: `noUncheckedIndexedAccess` добавляет `| undefined` к `arr[i]` и `obj[key]` — заставляет проверять границы. `exactOptionalPropertyTypes` различает «поле отсутствует» и «поле равно `undefined`». Документируй решения tsconfig в `docs/typescript.md` — будущий ты (и команда) скажут спасибо.

**Читать:**
- [Handbook: Migrating from JavaScript](https://www.typescriptlang.org/docs/handbook/migrating-from-javascript.html)
- [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped)
- [TSConfig: noUncheckedIndexedAccess](https://www.typescriptlang.org/tsconfig#noUncheckedIndexedAccess)

**Ключевая мысль:** миграция на TS — итеративный процесс; strict-опции и path aliases делают кодовую базу надёжнее с каждым коммитом.



### Практика

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


