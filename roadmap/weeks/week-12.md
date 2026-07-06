# Неделя 12: React — state, эффекты, формы

> **Цель недели:** научиться управлять состоянием компонентов, побочными эффектами и формами в React.
> **Литература:** [react.dev — Learn](https://react.dev/learn), [React — State](https://react.dev/learn/state-a-components-memory), [React — Effects](https://react.dev/learn/synchronizing-with-effects)

## День 78 (Пн): useState — память компонента

### Теория
- [useState](https://react.dev/reference/react/useState) — хук для локального состояния компонента
- State обновляется **иммутабельно**: `[...arr, item]`, `{...obj, field: value}`
- Ререндер происходит после вызова setter-функции, не после прямой мутации
- Начальное значение и lazy initialization: `useState(() => expensiveCalc())`

### Практика
1. Создай Vite-проект: `npm create vite@latest react-state-lab -- --template react`
2. Компонент `Counter` с кнопками `+1`, `-1`, `Сброс`
3. Компонент `ColorPicker` — state цвета фона, кнопки переключения темы
4. Счётчик кликов в `App`, передавай `count` и `setCount` в дочерний компонент

**Критерии:**
- [ ] Нет прямой мутации state (`arr.push` без копии)
- [ ] Каждый компонент в отдельном файле
- [ ] DevTools React показывает обновления state

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

### Практика
1. Перепиши Todo App (vanilla JS) на React с `useState`
2. Поля: добавление задачи, чекбокс «выполнено», удаление
3. Фильтр: All / Active / Completed — отдельный state `filter`
4. Счётчик активных задач в шапке

**Критерии:**
- [ ] Input полностью controlled
- [ ] `onSubmit` формы с `preventDefault`
- [ ] Фильтрация не мутирует исходный массив

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

### Практика
1. `DocumentTitle` — меняет `document.title` при смене страницы/задачи
2. Таймер Pomodoro: 25 мин countdown, cleanup при unmount
3. `useEffect` с `localStorage`: загрузка при mount, сохранение при изменении todos
4. Нарисуй схему: render → effect → cleanup → re-render

**Критерии:**
- [ ] Таймер очищается при размонтировании
- [ ] Зависимости effect указаны корректно (ESLint react-hooks)
- [ ] Нет бесконечного цикла effect → setState → effect

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

### Практика
1. Компонент `PostList` — GET `/posts`, спиннер при загрузке
2. Обработка ошибки сети — блок с кнопкой «Повторить»
3. `PostDetail` — загрузка `/posts/:id` по клику
4. Skeleton-заглушки вместо пустого экрана

**Критерии:**
- [ ] AbortController в cleanup effect
- [ ] UI для loading, error, empty, success
- [ ] Нет setState на размонтированном компоненте

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

### Практика
1. Форма регистрации: имя, email, пароль, роль (select)
2. Валидация перед submit: email формат, пароль ≥ 8 символов
3. Ошибки под полями, disabled кнопка при невалидной форме
4. После успешного submit — очистка формы и toast-сообщение

**Критерии:**
- [ ] Все поля controlled
- [ ] Ошибки показываются только после blur или submit
- [ ] `type="password"` и `autoComplete` настроены

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

### Практика
1. `FilterableList`: родитель хранит `items` + `searchQuery`
2. `SearchBar` — только input, вызывает `onSearchChange`
3. `ItemList` — получает отфильтрованный массив, рендерит список
4. `ItemCount` — показывает «Найдено: N из M»
5. Добавь сортировку (A–Z / Z–A) — ещё один поднятый state

**Критерии:**
- [ ] SearchBar не знает про items — только про query
- [ ] Фильтрация в родителе или через useMemo
- [ ] Нет дублирования state в siblings

### Ловушки
- Дублирование одного state в двух дочерних компонентах — рассинхрон
- Слишком глубокий drilling — пока терпимо, Context на неделе 13

---

## День 84 (Вс): Ревью и углубление

### Теория
- [React DevTools](https://react.dev/learn/react-developer-tools) — инспекция props/state
- Правила хуков: только на верхнем уровне, только в React-функциях
- [React Strict Mode](https://react.dev/reference/react/StrictMode) — двойной mount в dev

### Практика
1. Пройди [React Tutorial — Tic-Tac-Toe](https://react.dev/learn/tutorial-tic-tac-toe) до конца
2. Рефакторинг Todo App: вынеси логику в `useTodos` (заготовка под custom hook)
3. Code review своего кода: immutability, deps, cleanup
**Критерии:**
- [ ] Tic-Tac-Toe работает с историей ходов
- [ ] ESLint `react-hooks/exhaustive-deps` без warnings
- [ ] Конспект «useState vs useEffect — когда что» на 1 страницу

---

## Проект недели

**React Todo Pro** — полнофункциональное приложение задач:

1. CRUD задач с приоритетом (low/medium/high) и дедлайном
2. Фильтры: статус, приоритет, поиск по тексту
3. Persist в `localStorage` через `useEffect`
4. Загрузка «мотивационной цитаты» с [Quotable API](https://github.com/lukePeavey/quotable)
5. Адаптивная вёрстка, тёмная тема через CSS-переменные

**Критерии:**
- [ ] useState + useEffect без антипаттернов
- [ ] Controlled форма добавления задачи
- [ ] Lifting state: фильтры и список согласованы
- [ ] README с инструкцией запуска

## Ревью-чеклист
- Могу объяснить, почему `setState` асинхронный и что такое batching?
- Чем controlled отличается от uncontrolled input?
- Зачем cleanup в useEffect? Приведи 2 примера.
- Когда поднимать state, а когда оставить локальным?
- Что произойдёт, если мутировать массив в state напрямую?
