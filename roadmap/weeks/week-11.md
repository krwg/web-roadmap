# Неделя 11: React — компоненты, JSX, props, Vite, первые компоненты

> **Цель недели:** создать первое React-приложение на Vite, освоить компоненты, JSX, props и базовые паттерны.
> **Литература:** [react.dev Learn](https://react.dev/learn), [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/), [Vite Guide](https://vite.dev/guide/), [Thinking in React](https://react.dev/learn/thinking-in-react), [React — Quick Start](https://react.dev/learn)
> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-11/`

## День 1 (Mon): Введение в React и JSX

### Теория
- [react.dev: Describing the UI](https://react.dev/learn/describing-the-ui) — компоненты как функции, возвращающие UI
- JSX — синтаксический сахар над `React.createElement`, не HTML
- Правила JSX: один корневой элемент, `className`, `htmlFor`, самозакрывающиеся теги
- Встраивание: `{expression}`, фигурные скобки для JS в разметке
- Fragments: `<>...</>` — без лишнего div в DOM
- PascalCase для компонентов, camelCase для props
- JSX экранирует значения — защита от XSS по умолчанию
- `return` в компоненте — один корень или Fragment

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

### Git
```bash
cd learning-log/week-11
git add src/components/
git commit -m "week-11 day-01: JSX, Header, Footer и Hero"
```

## День 2 (Tue): Props и композиция

### Теория
- [react.dev: Passing Props](https://react.dev/learn/passing-props-to-a-component)
- Props read-only; one-way data flow — данные сверху вниз
- Деструктуризация props в сигнатуре функции — читаемость
- `children` prop — композиция, slot-паттерн
- Spread props: `<Input {...fieldProps} />` — осторожно с лишними DOM-атрибутами
- Default values через деструктуризацию: `{ size = 'md' }`
- Props drilling на 1–2 уровня — норма; Context позже
- Типизация props в TypeScript: `interface ButtonProps`

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

### Теория
- [react.dev: Rendering Lists](https://react.dev/learn/rendering-lists)
- `array.map()` → массив JSX элементов
- `key` — стабильный уникальный идентификатор, не index (при reorder/delete)
- Условный рендеринг: `&&`, ternary, early return
- Не вызывай компоненты как обычные функции — только JSX `<Component />`
- `key` нужен React для reconciliation — сопоставление элементов между рендерами
- Пустой массив и `&&` — осторожно с `0` как falsy
- Fragment с key: `<Fragment key={id}>` при map списков фрагментов

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

### Git
```bash
cd learning-log/week-11
git add src/components/todo/ src/data/
git commit -m "week-11 day-03: TodoList, keys и условный рендер"
```

## День 4 (Thu): События и состояние (useState)

### Теория
- [react.dev: Adding Interactivity](https://react.dev/learn/adding-interactivity)
- `useState` — [react.dev: State](https://react.dev/learn/state-a-components-memory)
- Обработчики: `onClick={() => setCount(c => c + 1)}` — функциональный апдейт
- State immutable updates: spread для объектов и массивов
- Подъём state up — общий родитель (preview недели 5)
- Batching — несколько setState в одном обработчике → один ререндер
- State — снимок на момент рендера, не «живая» переменная
- Инициализация: `useState(0)` vs `useState(() => expensive())`

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

### Git
```bash
cd learning-log/week-11
git add src/components/todo/
git commit -m "week-11 day-04: useState, CRUD задач и controlled input"
```

## День 5 (Fri): Формы и подъём состояния

### Теория
- [react.dev: Reacting to Input with State](https://react.dev/learn/reacting-to-input-with-state)
- Форма: `onSubmit`, `e.preventDefault()` — не перезагружать страницу
- Подъём state: `TodoApp` держит todos, дети получают props + callbacks
- Lifting state up — единый источник правды в ближайшем общем родителе
- Controlled vs uncontrolled (ref) — предпочтение controlled для форм
- Колбэки вниз: `onToggle(id)`, `onDelete(id)` — события вверх
- Валидация: клиентская до submit vs после blur
- `name` на input — для autofill и семантики форм

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

### Git
```bash
cd learning-log/week-11
git add src/components/todo/TodoApp.tsx
git commit -m "week-11 day-05: lifting state, форма и фильтры"
```

## День 6 (Sat): Стилизация и структура проекта

### Теория
- CSS Modules: `import styles from './Button.module.css'`
- classnames pattern: условные классы через template или утилита `cn()`
- Структура: `components/`, `hooks/`, `types/`, `utils/`
- [Vite: Static Assets](https://vite.dev/guide/assets.html) — импорт изображений
- react.dev — не обязательно CSS-in-JS на старте
- BEM vs CSS Modules — изоляция стилей
- CSS variables для темы: `:root` и `.dark`
- `prefers-color-scheme` — системная тема как default

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

### Git
```bash
cd learning-log/week-11
git add src/ src/**/*.module.css
git commit -m "week-11 day-06: CSS Modules, структура и тёмная тема"
```

## День 7 (Sun): Сборка Todo App и деплой

### Теория
- [react.dev: Escape Hatches](https://react.dev/learn/escape-hatches) — обзор useEffect (preview)
- `useEffect` для localStorage sync — mount + deps `[todos]`
- `npm run build` — production bundle; `npm run preview` локально
- Vite deploy на GitHub Pages / Netlify / Vercel
- React Strict Mode — двойной render в dev, выявление side effects
- `base` в vite.config для GitHub Pages subdirectory
- Environment variables: только `VITE_*` попадают в клиент
- Lighthouse — Performance, Accessibility перед деплоем

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
