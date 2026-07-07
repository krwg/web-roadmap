# Неделя 11: React — компоненты, JSX, props, Vite, первые компоненты



> **Цель недели:** создать первое React-приложение на Vite, освоить компоненты, JSX, props и базовые паттерны.

> **Литература:** [react.dev Learn](https://react.dev/learn), [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/), [Vite Guide](https://vite.dev/guide/), [Thinking in React](https://react.dev/learn/thinking-in-react), [React — Quick Start](https://react.dev/learn)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)

> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-11/`



## День 1 (Mon): Введение в React и JSX
<a id="week-11-day-1"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **React Todo**

### Теория

React — библиотека для построения пользовательских интерфейсов на основе компонентов. Компонент — это JavaScript-функция (или класс), которая принимает props и возвращает описание UI. React берёт это описание и обновляет реальный DOM эффективно через Virtual DOM и reconciliation. Философия React: UI = f(state) — интерфейс является функцией от состояния.

JSX — синтаксическое расширение, которое выглядит как HTML, но компилируется в вызовы `React.createElement`. Правила JSX отличаются от HTML: `className` вместо `class`, `htmlFor` вместо `for`, все теги закрываются (`<img />`, `<br />`). В фигурных скобках `{expression}` встраивается любое JavaScript-выражение: переменные, вызовы функций, тернарные операторы.

Компоненты именуются в PascalCase (`Header`, `TodoItem`), а props — в camelCase. JSX автоматически экранирует строки — вставка пользовательского текста безопасна от XSS. Компонент должен возвращать один корневой элемент; если нужно несколько соседних без обёрточного `<div>`, используй Fragment: `<>...</>`. Не вызывай компоненты как обычные функции `Header()` — только через JSX `<Header />`, иначе React не отследит жизненный цикл и hooks.

**Читать:**
- [react.dev: Describing the UI](https://react.dev/learn/describing-the-ui)
- [react.dev: Writing Markup with JSX](https://react.dev/learn/writing-markup-with-jsx)
- [React — Quick Start](https://react.dev/learn)

**Ключевая мысль:** компонент — функция от props к UI; JSX — удобный синтаксис описания, а не HTML.



### Практика

1. Изучи структуру Vite react-ts проекта из недели 10

2. Очисти `App.tsx`, создай разметку лендинга в JSX

3. Вынеси `Header`, `Footer`, `Hero` в отдельные файлы компонентов

4. Используй Fragment вместо обёрточного div где возможно

5. Подключи CSS-модуль или отдельный `App.css`

6. Создай `learning-log/week-11/` — новый Vite-проект или форк week-10

7. Проверь ESLint rules для React (`eslint-plugin-react`)



**Критерии:**

- [ ] Минимум 3 компонента в отдельных файлах

- [ ] Корректный JSX без ошибок ESLint

- [ ] className вместо class



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git

```bash

cd learning-log/week-11

git add src/components/

git commit -m "week-11 day-01: JSX, Header, Footer и Hero"

```



## День 2 (Tue): Props и композиция
<a id="week-11-day-2"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **React Todo**

### Теория

Props (properties) — единственный способ передать данные от родителя к ребёнку в React. Props **read-only**: дочерний компонент не должен их мутировать. Это основа однонаправленного потока данных (one-way data flow): состояние живёт выше, данные текут вниз через props, события — вверх через callback-функции.

Деструктуризация в сигнатуре делает код читаемым: `function Button({ label, onClick, variant = 'primary' })` вместо `props.label`. Значения по умолчанию задавай прямо в деструктуризации. Специальный prop `children` — содержимое между открывающим и закрывающим тегами: `<Card>Это children</Card>`. Паттерн slot: `Card` рендерит `children` внутри своей разметки, а родитель решает, что туда положить.

Spread props (`<Input {...fieldProps} />`) передаёт все свойства объекта разом — удобно, но осторожно: лишние props могут попасть на DOM-элемент и вызвать warning. Props drilling на 1–2 уровня — нормальная практика; Context (неделя 13+) понадобится при глубокой вложенности. В TypeScript каждый компонент получает `interface XxxProps` с явными типами.

**Читать:**
- [react.dev: Passing Props to a Component](https://react.dev/learn/passing-props-to-a-component)
- [react.dev: Thinking in React](https://react.dev/learn/thinking-in-react)
- [React TypeScript Cheatsheet: Components](https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/basic_type_example)

**Ключевая мысль:** props — read-only вход компонента; данные вниз, события вверх через callbacks.



### Практика

1. `Button` с props: `variant: 'primary' | 'secondary'`, `size`, `disabled`, `onClick`

2. `Card` с `title`, `children`, опциональным `footer`

3. `Avatar` с `src`, `alt`, `size` — значения по умолчанию

4. Композиция: `Card` внутри `Hero`, `Button` в `Card.footer`

5. Задокументируй props через TypeScript interfaces

6. Компонент `Icon` с `name` и `aria-label` для a11y

7. Story-подобная страница: все варианты Button на одном экране



**Критерии:**

- [ ] Все props типизированы

- [ ] children используется для композиции

- [ ] Default props через деструктуризацию



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git

```bash

cd learning-log/week-11

git add src/components/ui/

git commit -m "week-11 day-02: Button, Card, Avatar и композиция"

```



### Ловушки

- Мутация props — запрещено

- `key` не доступен как prop — отдельный атрибут

- Пропуск `alt` на img — a11y регрессия



## День 3 (Wed): Списки, keys и рендеринг
<a id="week-11-day-3"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **React Todo**

### Теория

Списки в React рендерятся через `array.map()`: каждый элемент массива превращается в JSX. React нужен атрибут `key` на элементе верхнего уровня в map — уникальный и **стабильный** идентификатор (обычно `item.id`). Key помогает reconciliation: React сопоставляет элементы между рендерами и обновляет только изменившиеся, а не пересоздаёт весь список.

Использование индекса массива как key (`key={index}`) допустимо только для статических списков без reorder/delete. При удалении элемента из середины индексы сдвигаются — React перепутает компоненты, и state (например, фокус input) «переедет» к другому элементу. Всегда предпочитай `key={todo.id}`.

Условный рендеринг: `{isLoggedIn && <Dashboard />}` (осторожно — `0` falsy и отрендерится как текст), тернарный `{loading ? <Spinner /> : <List />}`, early return `if (!data) return null`. Не вызывай компоненты как функции `TodoItem(todo)` — только `<TodoItem todo={todo} />`. Fragment с key нужен при map фрагментов: `<Fragment key={id}>...</Fragment>`.

**Читать:**
- [react.dev: Rendering Lists](https://react.dev/learn/rendering-lists)
- [react.dev: Conditional Rendering](https://react.dev/learn/conditional-rendering)
- [react.dev: Fragment](https://react.dev/reference/react/Fragment)

**Ключевая мысль:** стабильный `key` по id — не оптимизация, а корректность при изменении порядка и удалении элементов.



### Практика

1. Компонент `TodoList` — рендер массива `Todo[]`

2. `TodoItem` с props: `todo`, `onToggle`, `onDelete`

3. keys = `todo.id`, не индекс массива

4. Пустой список: условный рендер «Нет задач»

5. Фильтр tabs: all / active / done — условное отображение

6. Добавь mock-данные в `data/todos.ts` — 5+ задач

7. Проверь: удаление средней задачи не ломает state остальных



**Критерии:**

- [ ] Стабильные keys на основе id

- [ ] Условный рендер для empty state

- [ ] map возвращает JSX, не side effects



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git

```bash

cd learning-log/week-11

git add src/components/todo/ src/data/

git commit -m "week-11 day-03: TodoList, keys и условный рендер"

```



## День 4 (Thu): События и состояние (useState)
<a id="week-11-day-4"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **React Todo**

### Теория

Интерактивность в React начинается с `useState` — hook, дающий компоненту «память». `const [count, setCount] = useState(0)` возвращает текущее значение и функцию обновления. Вызов `setCount` планирует ререндер компонента с новым значением. State — это снимок на момент рендера: если вызвать `setCount(count + 1)` три раза подряд в одном обработчике, счётчик увеличится на 1, не на 3. Для последовательных обновлений используй функциональную форму: `setCount(c => c + 1)`.

Обновления state должны быть **иммутабельными**: вместо `todos.push(item)` пиши `setTodos([...todos, item])`; вместо `todo.done = true` — `setTodos(todos.map(t => t.id === id ? { ...t, done: true } : t))`. React сравнивает ссылки — мутация не вызовет ререндер. Controlled input связывает `<input value={text} onChange={e => setText(e.target.value)} />` — React state единственный источник правды для значения поля.

Несколько `useState` предпочтительнее одного большого объекта state — проще обновлять отдельные поля. Derived values (счётчик активных задач) вычисляй из state при рендере, а не храни в отдельном `useState`. Batching: React объединяет несколько `setState` в одном обработчике события в один ререндер.

**Читать:**
- [react.dev: State: A Component's Memory](https://react.dev/learn/state-a-components-memory)
- [react.dev: Adding Interactivity](https://react.dev/learn/adding-interactivity)
- [react.dev: Queueing a Series of State Updates](https://react.dev/learn/queueing-a-series-of-state-updates)

**Ключевая мысль:** state обновляй иммутабельно; функциональный апдейт `setX(x => ...)` даёт актуальное значение при batching.



### Практика

1. Счётчик в `Hero` с `useState`

2. Controlled input: `value` + `onChange` для поля новой задачи

3. Добавление задачи в массив через immutable update

4. Toggle done: `todos.map(t => t.id === id ? {...t, done: !t.done} : t)`

5. Удаление через `filter`

6. Счётчик «активных» задач — derived из state, не отдельный useState

7. Добавь `createdAt: Date.now()` при создании задачи



**Критерии:**

- [ ] Все inputs controlled

- [ ] State обновляется иммутабельно

- [ ] Нет прямой мутации массива todos



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git

```bash

cd learning-log/week-11

git add src/components/todo/

git commit -m "week-11 day-04: useState, CRUD задач и controlled input"

```



## День 5 (Fri): Формы и подъём состояния
<a id="week-11-day-5"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **React Todo**

### Теория

Формы в React обрабатываются через событие `onSubmit` на `<form>` с обязательным `e.preventDefault()` — иначе браузер перезагрузит страницу. Подъём состояния (lifting state up) — ключевой паттерн: если два компонента (`TodoList` и `FilterTabs`) должны разделять данные, state поднимается к их **ближайшему общему родителю** (`TodoApp`). Родитель хранит `todos` и `filter`, детям передаёт данные и колбэки.

Controlled components — стандарт для форм: значение input, textarea, select и checkbox полностью управляется React state. Uncontrolled (через `ref`) допустим для простых случаев, но controlled даёт полный контроль: валидация, disabled, сброс. Колбэки вниз: `onToggle(id)`, `onDelete(id)`, `onFilterChange('active')` — дочерний компонент сообщает родителю о действии, не меняя state напрямую.

Валидация на клиенте: проверяй перед submit (пустая задача не добавляется), показывай ошибку рядом с полем. Атрибут `name` на input важен для autofill и семантики. Disabled кнопка submit при невалидной форме — простая и эффективная UX-защита. Enter в поле ввода сабмитит форму, если input внутри `<form>`.

**Читать:**
- [react.dev: Reacting to Input with State](https://react.dev/learn/reacting-to-input-with-state)
- [react.dev: Sharing State Between Components](https://react.dev/learn/sharing-state-between-components)
- [react.dev: Form](https://react.dev/reference/react-dom/components/form)

**Ключевая мысль:** общий state — у ближайшего общего родителя; форма controlled, события — через callbacks вверх.



### Практика

1. `TodoApp` — state `todos`, `filter` наверху

2. `AddTodoForm` — submit добавляет задачу, очищает input

3. `FilterTabs` — подними filter state, передай `setFilter`

4. `TodoStats` — вычисляемые значения из props (active count)

5. Валидация: пустая задача не добавляется, показ ошибки

6. `AddTodoForm` — disabled кнопка при пустом поле

7. Enter в поле ввода сабмитит форму



**Критерии:**

- [ ] State в общем родителе TodoApp

- [ ] Форма с preventDefault

- [ ] Валидация пустого ввода



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git

```bash

cd learning-log/week-11

git add src/components/todo/TodoApp.tsx

git commit -m "week-11 day-05: lifting state, форма и фильтры"

```



## День 6 (Sat): Стилизация и структура проекта
<a id="week-11-day-6"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **React Todo**

### Теория

Стилизация React-приложения начинается с организации, а не с выбора CSS-in-JS библиотеки. CSS Modules изолируют стили: `import styles from './Button.module.css'` и `className={styles.primary}` — классы уникальны на уровне файла, нет конфликтов имён. Условные классы удобно собирать через template literal или утилиту `cn(...classes)`, которая фильтрует falsy-значения.

Структура `src/` по назначению: `components/ui/` — переиспользуемые (Button, Card), `components/todo/` — предметные, `types/` — TypeScript-интерфейсы, `hooks/` — custom hooks (позже), `utils/` — чистые функции, `data/` — mock-данные. Vite позволяет импортировать изображения как модули: `import logo from './logo.svg'` — URL подставится автоматически.

Тёмная тема через CSS variables: в `:root` задай `--bg: #fff; --text: #111`, в `.dark` переопредели `--bg: #111; --text: #fff`. Переключение — class на `<html>` или корневом div, управляемый React state. `prefers-color-scheme: dark` в media query задаёт системную тему по умолчанию. Mobile-first: базовые стили для узкого экрана, `@media (min-width: 768px)` для расширения.

**Читать:**
- [Vite: Static Assets](https://vite.dev/guide/assets.html)
- [CSS Modules — spec](https://github.com/css-modules/css-modules)
- [MDN: CSS custom properties](https://developer.mozilla.org/ru/docs/Web/CSS/Using_CSS_custom_properties)

**Ключевая мысль:** CSS Modules + логичная структура папок + CSS variables для темы — достаточный фундамент без CSS-in-JS.



### Практика

1. CSS Modules для Button, Card, TodoItem

2. Утилита `cn(...classes)` для объединения классов

3. Реорганизуй src: `components/todo/`, `components/ui/`

4. Перенеси типы в `types/todo.ts`, mock data в `data/`

5. Тёмная тема через class на root + CSS variables

6. Адаптив: mobile-first для TodoApp (min-width breakpoints)

7. Проверь контраст текста в обеих темах



**Критерии:**

- [ ] Логичная структура папок

- [ ] CSS Modules без глобальных конфликтов

- [ ] Тема переключается через state + class



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git

```bash

cd learning-log/week-11

git add src/ src/**/*.module.css

git commit -m "week-11 day-06: CSS Modules, структура и тёмная тема"

```



## День 7 (Sun): Сборка Todo App и деплой
<a id="week-11-day-7"></a>

> **Время (полный):** ~1.5ч теория · ~2.5ч практика · ~15м Git · ~1ч ревью  
> **Время (лайт):** ~45м теория · ~1.5ч практика (MVP) · ~15м Git  
> **Связь с проектом:** шаг к **React Todo**

### Теория

Завершение Todo App объединяет state, effects и production-сборку. `useEffect` — hook для синхронизации React state с внешним миром (localStorage, document.title, подписки). Для persist: `useEffect(() => { localStorage.setItem('todos', JSON.stringify(todos)) }, [todos])` — сохраняй при каждом изменении. Начальное значение загружай через lazy init: `useState(() => JSON.parse(localStorage.getItem('todos') ?? '[]'))`.

Production-сборка: `npm run build` создаёт оптимизированный bundle в `dist/`, `npm run preview` проверяет его локально. Деплой на GitHub Pages, Netlify или Vercel — статический хостинг для SPA. Для GitHub Pages задай `base` в `vite.config.ts` (путь репозитория). Environment variables в Vite доступны только с префиксом `VITE_` — они встраиваются в клиентский код и видны всем.

React Strict Mode в dev вызывает двойной mount/unmount — это помогает найти missing cleanup в effects. Перед деплоем прогони Lighthouse: Performance, Accessibility, Best Practices. Escape Hatches (useEffect, useRef) — инструменты «выхода» из чистой модели React, когда нужна интеграция с браузерными API.

**Читать:**
- [react.dev: Escape Hatches](https://react.dev/learn/escape-hatches)
- [react.dev: useEffect](https://react.dev/reference/react/useEffect)
- [Vite: Deploy](https://vite.dev/guide/static-deploy.html)

**Ключевая мысль:** useEffect связывает React с внешним миром; production build + deploy завершают цикл от кода до живого приложения.



### Практика

1. Persist todos в localStorage через useEffect

2. Загрузка начального state из localStorage (lazy init useState)

3. Production build, проверь размер bundle

4. Задеплой на GitHub Pages или Vercel

5. Финальный self-review по react.dev Quick Start checklist

6. README с live demo URL и скриншотом

7. Тег `week-11-done`



**Критерии:**

- [ ] Todos сохраняются между сессиями

- [ ] Production build успешен

- [ ] Live demo доступен по URL



### Если застрял

Застрял >20 мин — остановись. Нарисуй схему на бумаге, сделай минимальный пример в отдельном файле `playground.*`, не копируй готовое решение. ИИ — только объяснить концепцию без кода.

### Git

```bash

cd learning-log/week-11

git add .

git commit -m "week-11 day-07: persist, deploy и React Todo App"

```



## Проект недели



**React Todo App** — полноценное приложение на Vite + TypeScript. Подробное ТЗ: [docs/projects.md — Неделя 11](../../docs/projects.md#неделя-11--react-todo).



Функции: CRUD задач, фильтры, счётчик, localStorage, тёмная тема, адаптивная вёрстка.



**Функции:**

- Добавление, toggle, удаление задач с валидацией

- Фильтры: all / active / completed + счётчик оставшихся

- Переключение светлой/тёмной темы с persist

- Адаптивная вёрстка от 320px



**Критерии проекта:**

- [ ] 8+ компонентов, типизированные props

- [ ] useState + lifting state + controlled forms

- [ ] CSS Modules или эквивалентная изоляция стилей

- [ ] localStorage persist, deployed demo

- [ ] Lighthouse Accessibility ≥ 90

- [ ] README с URL деплоя и инструкцией `npm run dev`

- [ ] Тег `week-11-done`



## Ревью-чеклист

- Чем JSX отличается от HTML?

- Зачем нужен key в списках и почему не index?

- Как обновить элемент массива в state иммутабельно?

- Что такое controlled component?

- Могу ли я объяснить однонаправленный поток данных в React?


## Проверь себя

<details>
<summary>Что должно получиться к концу недели?</summary>

Работающий проект **React Todo** в `learning-log/week-11/`, осмысленная Git-история, тег `week-11-done`.

</details>

<details>
<summary>Главный навык недели одной фразой?</summary>

React: компоненты, props, state

</details>

<details>
<summary>Можно ли пропустить день?</summary>

Нет — дни связаны. В **лайт-режиме** сократи практику до MVP, но теорию и Git-коммит не пропускай.

</details>
