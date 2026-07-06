# Неделя 10: TypeScript — типы, interfaces, generics basics, TS+React setup

> **Цель недели:** освоить основы TypeScript и подготовить проект к React с типизированной кодовой базой.
> **Литература:** [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html), [learn.javascript.ru: TypeScript](https://learn.javascript.ru/typescript), [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

## День 1 (Mon): Введение в TypeScript

### Теория
- [TypeScript: Getting Started](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html)
- TS = JS + статические типы; компиляция в JS (`tsc`)
- Установка: `npm init -y`, `npm i -D typescript`, `npx tsc --init`
- Базовые типы: `string`, `number`, `boolean`, `null`, `undefined`
- Аннотации: `let name: string = 'Anna'`; вывод типов (inference)

### Практика
1. Создай проект `ts-basics`, инициализируй TypeScript
2. Перепиши `utils.js` из прошлых недель в `utils.ts`
3. Включи `strict: true` в `tsconfig.json`
4. Исправь все ошибки компиляции
5. Настрой скрипт `"build": "tsc"` в package.json

**Критерии:**
- [ ] `tsc` компилирует без ошибок
- [ ] `strict: true` включён
- [ ] Понимаю разницу .ts и .js на выходе

## День 2 (Tue): Типы, union, literal, any

### Теория
- [Handbook: Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)
- Union: `string | number`; Literal types: `'light' | 'dark'`
- `any` — отключение проверки (избегать); `unknown` — безопасная альтернатива
- Type narrowing: `typeof`, `in`, discriminated unions
- `as const` — readonly literal types

### Практика
1. Тип `Theme = 'light' | 'dark'` для переключателя темы
2. Функция `formatId(id: string | number): string` с narrowing
3. Замени `any` на `unknown` + проверку перед использованием
4. Discriminated union `Result = { ok: true, data: T } | { ok: false, error: string }`
5. Используй `as const` для объекта констант STATUS

**Критерии:**
- [ ] Нет `any` в новом коде
- [ ] Union types с корректным narrowing
- [ ] Result pattern для ошибок API

### Ловушки
- `any` распространяется как зараза — теряется смысл TS
- Утверждение `as Type` без проверки — ложная безопасность
- Забытый `strictNullChecks` — null не ловится

## День 3 (Wed): Interfaces и type aliases

### Теория
- [Handbook: Objects](https://www.typescriptlang.org/docs/handbook/2/objects.html)
- `interface User { id: number; name: string; }` vs `type User = { ... }`
- Расширение: `interface Admin extends User`
- Опциональные поля `email?`, readonly `readonly id`
- Index signatures: `[key: string]: string`

### Практика
1. Интерфейсы `Todo`, `TodoFilter`, `TodoState` для Todo App
2. `interface ApiResponse<T> { data: T; meta: PaginationMeta }`
3. Type alias для функции: `type EventHandler = (e: Event) => void`
4. Расширь `User` → `Admin` с полем `permissions: string[]`
5. Рефакторинг api-модуля с типизированными ответами

**Критерии:**
- [ ] Все доменные сущности типизированы
- [ ] interface vs type — осознанный выбор
- [ ] Опциональные и readonly поля использованы

## День 4 (Thu): Generics — основы

### Теория
- [Handbook: Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)
- `function identity<T>(arg: T): T`
- Generic interfaces: `interface Box<T> { value: T }`
- Constraints: `<T extends { id: number }>`
- Generic defaults: `<T = string>`

### Практика
1. `function first<T>(arr: T[]): T | undefined`
2. `async function fetchJson<T>(url: string): Promise<T>` — типизированный fetch
3. `function groupBy<T, K extends string>(items: T[], key: (item: T) => K)`
4. Типизируй localStorage wrapper: `getItem<T>(key): T | null`
5. Примени generics в api-клиенте каталога фильмов

**Критерии:**
- [ ] fetchJson типизирует ответ API
- [ ] groupBy работает с разными типами
- [ ] Constraints использован хотя бы раз

## День 5 (Fri): Функции, utility types, enums

### Теория
- Параметры: optional, default, rest — типизация
- [Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html): `Partial`, `Pick`, `Omit`, `Record`
- `enum` vs union of literals — предпочтение union в modern TS
- Function overloads — когда несколько сигнатур
- Return type inference vs explicit

### Практика
1. `UpdateTodo = Partial<Pick<Todo, 'title' | 'done'>>`
2. `Record<Theme, string>` для CSS-переменных по темам
3. Замени enum статусов на `as const` объект + union type
4. Overload: `createElement(tag: 'div'): HTMLDivElement` (упрощённо)
5. Типизируй EventEmitter из недели 9 generics `<T>`

**Критерии:**
- [ ] Partial/Pick/Omit в рефакторинге
- [ ] const assertion вместо enum
- [ ] EventEmitter типизирован

## День 6 (Sat): TS + React setup

### Теория
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/docs/basic/setup)
- `npm create vite@latest my-app -- --template react-ts`
- Структура: `src/`, `main.tsx`, `App.tsx`, `vite-env.d.ts`
- Типизация props: `interface Props { title: string }`
- `React.FC` vs обычная функция — современные рекомендации

### Практика
1. Создай проект Vite + React + TypeScript
2. Перенеси типы Todo в `src/types/todo.ts`
3. Компонент `Button` с props: `label`, `onClick`, `variant?`, `disabled?`
4. Компонент `Card` с `children: React.ReactNode`
5. Запусти `npm run dev`, убедись что HMR работает

**Критерии:**
- [ ] Vite проект запускается
- [ ] Минимум 2 типизированных компонента
- [ ] Типы вынесены в отдельные файлы

## День 7 (Sun): Миграция и strict mode

### Теория
- Постепенная миграция JS → TS: `allowJs`, `checkJs`
- `@types/node`, `@types/react`, `@types/react-dom`
- Declaration files `.d.ts` — когда нужны
- `satisfies` operator (TS 4.9+) — сохранение literal types
- tsconfig paths: `"@/*": ["src/*"]`

### Практика
1. Настрой alias `@/` в tsconfig и vite.config
2. Мигрируй api-модуль в TS с полной типизацией
3. Включи `noUncheckedIndexedAccess` — исправь новые ошибки
4. Напиши `.d.ts` для маленькой JS-библиотеки без типов (mock)
5. Документируй tsconfig решения в `docs/typescript.md`

**Критерии:**
- [ ] Path aliases работают
- [ ] api модуль полностью типизирован
- [ ] noUncheckedIndexedAccess не ломает сборку

## Проект недели

**Типизированный Todo API client** — TS-библиотека + Vite React shell.

Пакет: типы, generic fetch, localStorage repo, unit-типы для всех функций. React: заглушка App с Button и Card.

**Критерии проекта:**
- [ ] strict TypeScript, zero `any`
- [ ] Generics в fetch и storage
- [ ] Utility types для update DTOs
- [ ] Vite react-ts scaffold с 2+ компонентами

## Ревью-чеклист
- Зачем TypeScript если есть JS?
- Разница `interface` и `type`?
- Когда `unknown` лучше `any`?
- Что делает `Partial<T>` и `Pick<T, K>`?
- Как типизировать props React-компонента?
