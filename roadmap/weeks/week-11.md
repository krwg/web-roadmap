# Неделя 11: React — компоненты, JSX, props, Vite, первые компоненты

> **Цель недели:** создать первое React-приложение на Vite, освоить компоненты, JSX, props и базовые паттерны.
> **Литература:** [react.dev Learn](https://react.dev/learn), [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/), [Vite Guide](https://vite.dev/guide/)

## День 1 (Mon): Введение в React и JSX

### Теория
- [react.dev: Describing the UI](https://react.dev/learn/describing-the-ui) — компоненты как функции
- JSX — синтаксический сахар над `React.createElement`
- Правила JSX: один корневой элемент, `className`, `htmlFor`, самозакрывающиеся теги
- Встраивание: `{expression}`, фигурные скобки для JS
- Fragments: `<>...</>` — без лишнего div

### Практика
1. Изучи структуру Vite react-ts проекта из недели 10
2. Очисти `App.tsx`, создай разметку лендинга в JSX
3. Вынеси `Header`, `Footer`, `Hero` в отдельные файлы компонентов
4. Используй Fragment вместо обёрточного div где возможно
5. Подключи CSS-модуль или отдельный `App.css`

**Критерии:**
- [ ] Минимум 3 компонента в отдельных файлах
- [ ] Корректный JSX без ошибок ESLint
- [ ] className вместо class

## День 2 (Tue): Props и композиция

### Теория
- [react.dev: Passing Props](https://react.dev/learn/passing-props-to-a-component)
- Props read-only; one-way data flow
- Деструктуризация props в сигнатуре функции
- `children` prop — композиция
- Spread props: `<Input {...fieldProps} />` — осторожно с DOM

### Практика
1. `Button` с props: `variant: 'primary' | 'secondary'`, `size`, `disabled`, `onClick`
2. `Card` с `title`, `children`, опциональным `footer`
3. `Avatar` с `src`, `alt`, `size` — значения по умолчанию
4. Композиция: `Card` внутри `Hero`, `Button` в `Card.footer`
5. Задокументируй props через TypeScript interfaces

**Критерии:**
- [ ] Все props типизированы
- [ ] children используется для композиции
- [ ] Default props через деструктуризацию

### Ловушки
- Мутация props — запрещено
- `key` не доступен как prop — отдельный атрибут
- Пропуск `alt` на img — a11y регрессия

## День 3 (Wed): Списки, keys и рендеринг

### Теория
- [react.dev: Rendering Lists](https://react.dev/learn/rendering-lists)
- `array.map()` → массив JSX элементов
- `key` — стабильный уникальный идентификатор, не index (при reorder)
- Условный рендеринг: `&&`, ternary, early return
- Не вызывай компоненты как обычные функции — только JSX

### Практика
1. Компонент `TodoList` — рендер массива `Todo[]`
2. `TodoItem` с props: `todo`, `onToggle`, `onDelete`
3. keys = `todo.id`, не индекс массива
4. Пустой список: условный рендер «Нет задач»
5. Фильтр tabs: all / active / done — условное отображение

**Критерии:**
- [ ] Стабильные keys на основе id
- [ ] Условный рендер для empty state
- [ ] map возвращает JSX, не side effects

## День 4 (Thu): События и состояние (useState)

### Теория
- [react.dev: Adding Interactivity](https://react.dev/learn/adding-interactivity)
- `useState` — [react.dev: State](https://react.dev/learn/state-a-components-memory)
- Обработчики: `onClick={() => setCount(c => c + 1)}`
- State immutable updates: spread для объектов и массивов
- Подъём state up — общий родитель (preview)

### Практика
1. Счётчик в `Hero` с `useState`
2. Controlled input: `value` + `onChange` для поля новой задачи
3. Добавление задачи в массив через immutable update
4. Toggle done: `todos.map(t => t.id === id ? {...t, done: !t.done} : t)`
5. Удаление через `filter`

**Критерии:**
- [ ] Все inputs controlled
- [ ] State обновляется иммутабельно
- [ ] Нет прямой мутации массива todos

## День 5 (Fri): Формы и подъём состояния

### Теория
- [react.dev: Reacting to Input with State](https://react.dev/learn/reacting-to-input-with-state)
- Форма: `onSubmit`, `e.preventDefault()`
- Подъём state: `TodoApp` держит todos, дети получают props
- Lifting state up — единый источник правды
- Controlled vs uncontrolled (ref) — предпочтение controlled

### Практика
1. `TodoApp` — state `todos`, `filter` наверху
2. `AddTodoForm` — submit добавляет задачу, очищает input
3. `FilterTabs` — подними filter state, передай `setFilter`
4. `TodoStats` — вычисляемые значения из props (active count)
5. Валидация: пустая задача не добавляется, показ ошибки

**Критерии:**
- [ ] State в общем родителе TodoApp
- [ ] Форма с preventDefault
- [ ] Валидация пустого ввода

## День 6 (Sat): Стилизация и структура проекта

### Теория
- CSS Modules: `import styles from './Button.module.css'`
- classnames pattern: условные классы
- Структура: `components/`, `hooks/`, `types/`, `utils/`
- [Vite: Static Assets](https://vite.dev/guide/assets.html) — импорт изображений
- react.dev — не обязательно CSS-in-JS на старте

### Практика
1. CSS Modules для Button, Card, TodoItem
2. Утилита `cn(...classes)` для объединения классов
3. Реорганизуй src: `components/todo/`, `components/ui/`
4. Перенеси типы в `types/todo.ts`, mock data в `data/`
5. Тёмная тема через class на root + CSS variables

**Критерии:**
- [ ] Логичная структура папок
- [ ] CSS Modules без глобальных конфликтов
- [ ] Тема переключается через state + class

## День 7 (Sun): Сборка Todo App и деплой

### Теория
- [react.dev: Escape Hatches](https://react.dev/learn/escape-hatches) — обзор useEffect (preview)
- `useEffect` для localStorage sync — mount + deps `[todos]`
- `npm run build` — production bundle; preview
- Vite deploy на GitHub Pages / Netlify / Vercel
- React Strict Mode — двойной render в dev, зачем

### Практика
1. Persist todos в localStorage через useEffect
2. Загрузка начального state из localStorage (lazy init useState)
3. Production build, проверь размер bundle
4. Задеплой на GitHub Pages или Vercel
5. Финальный self-review по react.dev Quick Start checklist

**Критерии:**
- [ ] Todos сохраняются между сессиями
- [ ] Production build успешен
- [ ] Live demo доступен по URL

## Проект недели

**React Todo App** — полноценное приложение на Vite + TypeScript.

Функции: CRUD задач, фильтры, счётчик, localStorage, тёмная тема, адаптивная вёрстка.

**Критерии проекта:**
- [ ] 8+ компонентов, типизированные props
- [ ] useState + lifting state + controlled forms
- [ ] CSS Modules или эквивалентная изоляция стилей
- [ ] localStorage persist, deployed demo
- [ ] Lighthouse Accessibility ≥ 90

## Ревью-чеклист
- Чем JSX отличается от HTML?
- Зачем нужен key в списках и почему не index?
- Как обновить элемент массива в state иммутабельно?
- Что такое controlled component?
- Могу ли я объяснить однонаправленный поток данных в React?
