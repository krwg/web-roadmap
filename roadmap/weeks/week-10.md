# Неделя 10: TypeScript — типы, interfaces, generics basics, TS+React setup

> **Цель недели:** освоить основы TypeScript и подготовить проект к React с типизированной кодовой базой.
> **Литература:** [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html), [learn.javascript.ru: TypeScript](https://learn.javascript.ru/typescript), [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/), [Total TypeScript — Beginners](https://www.totaltypescript.com/tutorials/beginners-typescript), [TSConfig Reference](https://www.typescriptlang.org/tsconfig)
> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-10/`

## День 1 (Mon): Введение в TypeScript

### Теория
- [TypeScript: Getting Started](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html)
- TS = JS + статические типы; компиляция в JS (`tsc`) — типы стираются в runtime
- Установка: `npm init -y`, `npm i -D typescript`, `npx tsc --init`
- Базовые типы: `string`, `number`, `boolean`, `null`, `undefined`, `bigint`, `symbol`
- Аннотации: `let name: string = 'Anna'`; вывод типов (inference) — TS угадывает тип
- `tsconfig.json` — `target`, `module`, `outDir`, `rootDir`, `strict`
- `.ts` vs `.tsx` — JSX только в `.tsx`
- `npx tsc --noEmit` — проверка без генерации файлов (удобно в CI)

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
- [Handbook: Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)
- Union: `string | number`; Literal types: `'light' | 'dark'` — сужение множества значений
- `any` — отключение проверки (избегать); `unknown` — безопасная альтернатива, требует narrowing
- Type narrowing: `typeof`, `in`, discriminated unions с общим полем-дискриминатором
- `as const` — readonly literal types, tuple inference
- `never` — недостижимый тип, exhaustive switch
- Type guards: пользовательские `function isUser(x): x is User`
- `void` vs `undefined` в return type функций

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
- [Handbook: Objects](https://www.typescriptlang.org/docs/handbook/2/objects.html)
- `interface User { id: number; name: string; }` vs `type User = { ... }` — сходства и отличия
- Расширение: `interface Admin extends User`; intersection types: `type Admin = User & { role: string }`
- Опциональные поля `email?`, readonly `readonly id` — иммутабельность на уровне типов
- Index signatures: `[key: string]: string` — динамические ключи
- Declaration merging — только у `interface`, не у `type`
- `interface` предпочтительнее для объектов, `type` — для union и mapped types
- `Readonly<T>`, `ReadonlyArray<T>` — обзор utility types

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
- [Handbook: Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)
- `function identity<T>(arg: T): T` — параметр типа
- Generic interfaces: `interface Box<T> { value: T }`
- Constraints: `<T extends { id: number }>` — ограничение сверху
- Generic defaults: `<T = string>` — значение по умолчанию
- Multiple type parameters: `<T, U>` — независимые типы
- `keyof T` — union ключей объекта; indexed access `T[K]`
- Generic constraints с `extends string | number` для ключей

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
- Параметры: optional `?`, default, rest `...args` — типизация каждого варианта
- [Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html): `Partial`, `Pick`, `Omit`, `Record`, `Required`
- `enum` vs union of literals — предпочтение union в modern TS (tree-shaking)
- Function overloads — когда несколько сигнатур для одной реализации
- Return type inference vs explicit — когда явный return полезен
- `Parameters<T>`, `ReturnType<T>` — извлечение типов из функций
- `satisfies` (TS 4.9+) — проверка без расширения типа

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
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/docs/basic/setup)
- `npm create vite@latest my-app -- --template react-ts`
- Структура: `src/`, `main.tsx`, `App.tsx`, `vite-env.d.ts`
- Типизация props: `interface Props { title: string }`
- `React.FC` vs обычная функция — современные рекомендации: без FC
- `React.ReactNode`, `React.ReactElement` — children и возвращаемые значения
- Vite + TS: `vite.config.ts`, path aliases
- Strict mode React — двойной render в dev

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
- Постепенная миграция JS → TS: `allowJs`, `checkJs`
- `@types/node`, `@types/react`, `@types/react-dom` — DefinitelyTyped
- Declaration files `.d.ts` — когда нужны для JS-библиотек без типов
- `satisfies` operator (TS 4.9+) — сохранение literal types при проверке
- tsconfig paths: `"@/*": ["src/*"]` — алиасы импортов
- `noUncheckedIndexedAccess` — `arr[i]` может быть `undefined`
- `exactOptionalPropertyTypes` — строгое различие отсутствующего и `undefined`

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
