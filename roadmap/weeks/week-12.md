# Неделя 12: React — state, эффекты, формы

> **Цель недели:** научиться управлять состоянием компонентов, побочными эффектами и формами в React.
> **Литература:** [react.dev — Learn](https://react.dev/learn), [React — State](https://react.dev/learn/state-a-components-memory), [React — Effects](https://react.dev/learn/synchronizing-with-effects), [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect), [React — Forms](https://react.dev/reference/react-dom/components/form)
> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-12/`

## День 78 (Пн): useState — память компонента

### Теория
- [useState](https://react.dev/reference/react/useState) — хук для локального состояния компонента
- State обновляется **иммутабельно**: `[...arr, item]`, `{...obj, field: value}`
- Ререндер происходит после вызова setter-функции, не после прямой мутации
- Начальное значение и lazy initialization: `useState(() => expensiveCalc())`
- Функциональный апдейт: `setCount(c => c + 1)` — актуальное значение при batching
- State изолирован между экземплярами одного компонента
- Несколько `useState` vs один объект state — когда что удобнее
- State как снимок — чтение state сразу после setState даёт старое значение

### Практика
1. Создай Vite-проект: `npm create vite@latest week-12 -- --template react-ts` в `learning-log/`
2. Компонент `Counter` с кнопками `+1`, `-1`, `Сброс`
3. Компонент `ColorPicker` — state цвета фона, кнопки переключения темы
4. Счётчик кликов в `App`, передавай `count` и `setCount` в дочерний компонент
5. Демонстрация функционального апдейта: три `setCount(c => c + 1)` подряд
6. Lazy init: `useState(() => JSON.parse(localStorage.getItem('x') ?? '0'))`
7. Раздели сложный state на несколько useState

**Критерии:**
- [ ] Нет прямой мутации state (`arr.push` без копии)
- [ ] Каждый компонент в отдельном файле
- [ ] DevTools React показывает обновления state

### Git
```bash
cd learning-log/week-12
git add src/components/Counter.tsx src/components/ColorPicker.tsx
git commit -m "week-12 day-78: useState, Counter и ColorPicker"
```

### Ловушки
- Мутация объекта/массива напрямую — UI не обновится
- Вызов `setCount(count + 1)` три раза подряд в одном обработчике даёт +1, не +3 — используй функциональный апдейт

---

## День 79 (Вт): События и controlled components

### Теория
- [React — Responding to Events](https://react.dev/learn/responding-to-events): `onClick`, `onChange`, `onSubmit`
- Controlled input: `value={text}` + `onChange={e => setText(e.target.value)}`
- [React — Forms](https://react.dev/reference/react-dom/components/input): один источник правды — state
- Synthetic events: `e.preventDefault()`, `e.stopPropagation()`
- Controlled checkbox: `checked` + `onChange`, не `value`
- Controlled select: `value` на `<select>`, не `selected` на `<option>`
- Группа radio: один state, разные `value` у input
- `readOnly` vs `disabled` — различие для UX и a11y

### Практика
1. Перепиши Todo App (vanilla JS) на React с `useState`
2. Поля: добавление задачи, чекбокс «выполнено», удаление
3. Фильтр: All / Active / Completed — отдельный state `filter`
4. Счётчик активных задач в шапке
5. Textarea для описания задачи — controlled
6. Select приоритета: low / medium / high
7. Проверь tab-навигацию по всем полям формы

**Критерии:**
- [ ] Input полностью controlled
- [ ] `onSubmit` формы с `preventDefault`
- [ ] Фильтрация не мутирует исходный массив

### Git
```bash
cd learning-log/week-12
git add src/components/todo/
git commit -m "week-12 day-79: controlled inputs и Todo на React"
```

### Ловушки
- `defaultValue` вместо `value` — компонент становится uncontrolled
- Забытый `key` при рендере списка задач — баги при удалении

---

## День 80 (Ср): useEffect — побочные эффекты

### Теория
- [useEffect](https://react.dev/reference/react/useEffect): синхронизация с внешним миром
- Массив зависимостей `[]` — mount; `[dep]` — при изменении dep
- Cleanup function: `return () => { ... }` — отписки, таймеры, abort
- [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) — не всё требует effect
- Effect vs event handler — побочный эффект по событию не в useEffect
- Strict Mode — двойной mount в dev для проверки cleanup
- Stale closure в effect — deps должны включать используемые значения
- `useLayoutEffect` — синхронно после DOM, до paint (обзор)

### Практика
1. `DocumentTitle` — меняет `document.title` при смене страницы/задачи
2. Таймер Pomodoro: 25 мин countdown, cleanup при unmount
3. `useEffect` с `localStorage`: загрузка при mount, сохранение при изменении todos
4. Нарисуй схему: render → effect → cleanup → re-render
5. Подписка на `window.resize` с cleanup removeEventListener
6. Исправь намеренно сломанный effect с missing deps
7. Рефакторинг: убери лишний effect, перенеси логику в обработчик

**Критерии:**
- [ ] Таймер очищается при размонтировании
- [ ] Зависимости effect указаны корректно (ESLint react-hooks)
- [ ] Нет бесконечного цикла effect → setState → effect

### Git
```bash
cd learning-log/week-12
git add src/hooks/ src/components/DocumentTitle.tsx
git commit -m "week-12 day-80: useEffect, Pomodoro и localStorage sync"
```

### Ловушки
- Пустой `[]` при использовании props/state внутри — stale closure
- Effect без deps при каждом рендере — лишние запросы и лаги

---

## День 81 (Чт): Fetch и паттерн loading/error/data

### Теория
- Загрузка данных в `useEffect` + [fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- Паттерн трёх состояний: `loading`, `error`, `data`
- [AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController) для отмены запроса
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) — тестовый REST API
- Race condition: быстрая смена id — старый ответ перезаписывает новый
- `res.ok` — fetch не бросает на 404, проверяй вручную
- Discriminated union для async state: `{ status: 'loading' } | { status: 'error', error } | { status: 'success', data }`
- Отдельный custom hook `useFetch` — инкапсуляция паттерна

### Практика
1. Компонент `PostList` — GET `/posts`, спиннер при загрузке
2. Обработка ошибки сети — блок с кнопкой «Повторить»
3. `PostDetail` — загрузка `/posts/:id` по клику
4. Skeleton-заглушки вместо пустого экрана
5. AbortController в cleanup при смене id или unmount
6. Вынеси логику в `useFetch<T>(url)`
7. Empty state: «Постов не найдено» при пустом массиве

**Критерии:**
- [ ] AbortController в cleanup effect
- [ ] UI для loading, error, empty, success
- [ ] Нет setState на размонтированном компоненте

### Git
```bash
cd learning-log/week-12
git add src/hooks/useFetch.ts src/components/PostList.tsx
git commit -m "week-12 day-81: fetch, loading/error/data и useFetch"
```

### Ловушки
- Забытый cleanup → warning «Can't perform state update on unmounted component»
- Race condition: старый запрос перезаписывает новый — используй abort или id запроса

---

## День 82 (Пт): Формы в React

### Теория
- Controlled: `input`, `textarea`, `select`, `checkbox`, `radio`
- Групповой state формы: один объект `{ name, email, role }` или отдельные useState
- Валидация на клиенте: required, minLength, regex, отображение ошибок
- [React 19 — Actions](https://react.dev/reference/react-dom/components/form) (обзор, опционально)
- Touched/dirty state — показывать ошибки после blur, не при первом символе
- `useId()` для связки label и input — уникальные id
- Сброс формы: контролируемый state → начальные значения
- `noValidate` на form — своя валидация вместо браузерной

### Практика
1. Форма регистрации: имя, email, пароль, роль (select)
2. Валидация перед submit: email формат, пароль ≥ 8 символов
3. Ошибки под полями, disabled кнопка при невалидной форме
4. После успешного submit — очистка формы и toast-сообщение
5. Checkbox «согласен с условиями» — обязательный для submit
6. Показ/скрытие пароля кнопкой-иконкой
7. `useId()` для всех label/input пар

**Критерии:**
- [ ] Все поля controlled
- [ ] Ошибки показываются только после blur или submit
- [ ] `type="password"` и `autoComplete` настроены

### Git
```bash
cd learning-log/week-12
git add src/components/RegisterForm.tsx
git commit -m "week-12 day-82: форма регистрации и валидация"
```

### Ловушки
- `onChange` на checkbox без `checked={}` — неконтролируемый чекбокс
- Валидация только на submit без UX-подсказок — плохой UX

---

## День 83 (Сб): Подъём state (lifting state up)

### Теория
- [Sharing State Between Components](https://react.dev/learn/sharing-state-between-components)
- Общий state поднимается к ближайшему общему родителю
- Данные вниз через props, события вверх через callback props
- Композиция vs prop drilling (1–2 уровня — норма)
- Derived state — вычисляй из props/state, не дублируй в useState
- `useMemo` для дорогой фильтрации (preview)
- Siblings не общаются напрямую — только через родителя
- Container/Presentational split — логика vs отображение

### Практика
1. `FilterableList`: родитель хранит `items` + `searchQuery`
2. `SearchBar` — только input, вызывает `onSearchChange`
3. `ItemList` — получает отфильтрованный массив, рендерит список
4. `ItemCount` — показывает «Найдено: N из M»
5. Добавь сортировку (A–Z / Z–A) — ещё один поднятый state
6. Вынеси фильтрацию в `useMemo` при 100+ элементах (mock)
7. Рефакторинг Todo: filter + search в одном родителе

**Критерии:**
- [ ] SearchBar не знает про items — только про query
- [ ] Фильтрация в родителе или через useMemo
- [ ] Нет дублирования state в siblings

### Git
```bash
cd learning-log/week-12
git add src/components/FilterableList/
git commit -m "week-12 day-83: lifting state, FilterableList и сортировка"
```

### Ловушки
- Дублирование одного state в двух дочерних компонентах — рассинхрон
- Слишком глубокий drilling — пока терпимо, Context на неделе 13

---

## День 84 (Вс): Ревью и углубление

### Теория
- [React DevTools](https://react.dev/learn/react-developer-tools) — инспекция props/state
- Правила хуков: только на верхнем уровне, только в React-функциях
- [React Strict Mode](https://react.dev/reference/react/StrictMode) — двойной mount в dev
- Custom hooks — вынос повторяющейся логики (заготовка `useTodos`)
- Чеклист code review: immutability, deps, controlled inputs
- Подготовка к React Todo Pro — приоритеты, дедлайны, API
- ESLint `react-hooks/exhaustive-deps` — не отключай без причины

### Практика
1. Пройди [React Tutorial — Tic-Tac-Toe](https://react.dev/learn/tutorial-tic-tac-toe) до конца
2. Рефакторинг Todo App: вынеси логику в `useTodos` (заготовка под custom hook)
3. Code review своего кода: immutability, deps, cleanup
4. Начни скелет **React Todo Pro** — типы с priority и deadline
5. Конспект «useState vs useEffect — когда что» на 1 страницу
6. Прогони ESLint без warnings
7. Тег `week-12-done` после финальной сборки

**Критерии:**
- [ ] Tic-Tac-Toe работает с историей ходов
- [ ] ESLint `react-hooks/exhaustive-deps` без warnings
- [ ] Конспект «useState vs useEffect — когда что» на 1 страницу

### Git
```bash
cd learning-log/week-12
git add .
git commit -m "week-12 day-84: useTodos, Tic-Tac-Toe и React Todo Pro скелет"
```

---

## Проект недели

**React Todo Pro** — полнофункциональное приложение задач. Подробное ТЗ: [docs/projects.md — Неделя 12](../../docs/projects.md#неделя-12--react-todo-pro).

1. CRUD задач с приоритетом (low/medium/high) и дедлайном
2. Фильтры: статус, приоритет, поиск по тексту
3. Persist в `localStorage` через `useEffect`
4. Загрузка «мотивационной цитаты» с [Quotable API](https://github.com/lukePeavey/quotable)
5. Адаптивная вёрстка, тёмная тема через CSS-переменные

**Критерии:**
- [ ] useState + useEffect без антипаттернов
- [ ] Controlled форма добавления задачи
- [ ] Lifting state: фильтры и список согласованы
- [ ] Quotable API с loading/error states
- [ ] Custom hook `useTodos` для логики CRUD
- [ ] README с инструкцией запуска
- [ ] Тег `week-12-done`

## Ревью-чеклист
- Могу объяснить, почему `setState` асинхронный и что такое batching?
- Чем controlled отличается от uncontrolled input?
- Зачем cleanup в useEffect? Приведи 2 примера.
- Когда поднимать state, а когда оставить локальным?
- Что произойдёт, если мутировать массив в state напрямую?
