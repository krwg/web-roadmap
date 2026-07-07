# Неделя 12: React — state, эффекты, формы



> **Цель недели:** научиться управлять состоянием компонентов, побочными эффектами и формами в React.

> **Литература:** [react.dev — Learn](https://react.dev/learn), [React — State](https://react.dev/learn/state-a-components-memory), [React — Effects](https://react.dev/learn/synchronizing-with-effects), [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect), [React — Forms](https://react.dev/reference/react-dom/components/form)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)

> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-12/`



## День 78 (Пн): useState — память компонента



### Теория

`useState` — фундаментальный hook React, дающий функциональному компоненту локальное состояние. При первом рендере React создаёт ячейку state; при последующих — возвращает сохранённое значение. `setState` не меняет переменную мгновенно — он планирует ререндер с новым значением. Поэтому `console.log(count)` сразу после `setCount(5)` покажет старое значение.

Иммутабельные обновления обязательны: `[...arr, item]` для добавления, `arr.filter(...)` для удаления, `arr.map(...)` для изменения элемента. Прямая мутация (`arr.push`, `obj.field = x`) не вызовет ререндер, потому что ссылка на объект не изменилась. Lazy initialization `useState(() => expensiveCalc())` вычисляет начальное значение только при первом рендере — важно для чтения localStorage.

Функциональный апдейт `setCount(c => c + 1)` получает актуальное значение из очереди обновлений. Три таких вызова подряд дадут +3, в отличие от `setCount(count + 1)`. State изолирован между экземплярами: два `<Counter />` на странице имеют независимые счётчики. Несколько `useState` лучше одного объекта — проще обновлять и меньше риск случайной мутации.

**Читать:**
- [useState](https://react.dev/reference/react/useState)
- [react.dev: State: A Component's Memory](https://react.dev/learn/state-a-components-memory)
- [react.dev: Queueing a Series of State Updates](https://react.dev/learn/queueing-a-series-of-state-updates)

**Ключевая мысль:** state — снимок на рендер; обновляй иммутабельно и используй функциональный апдейт при последовательных изменениях.



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

Обработка событий в React похожа на DOM, но есть отличия. Атрибуты пишутся в camelCase: `onClick`, `onChange`, `onSubmit`. React использует Synthetic Events — обёртку над нативными событиями с единым API и пулингом для производительности. `e.preventDefault()` отменяет действие по умолчанию (перезагрузка формы), `e.stopPropagation()` останавливает всплытие.

Controlled component — input, значение которого полностью контролируется React state. Для text input: `value={text}` + `onChange={e => setText(e.target.value)}`. Для checkbox: `checked={done}` + `onChange`, не `value`. Для select: `value={priority}` на `<select>`, не `selected` на `<option>`. Группа radio: один state, разные `value` у `<input type="radio">`.

Разница `readOnly` и `disabled`: disabled элемент не участвует в tab-навигации и не отправляется с формой; readOnly виден и фокусируем, но не редактируется. `defaultValue` вместо `value` делает компонент uncontrolled — React не управляет значением после первого рендера. Для форм с валидацией и сбросом предпочитай controlled.

**Читать:**
- [React — Responding to Events](https://react.dev/learn/responding-to-events)
- [React — Forms](https://react.dev/reference/react-dom/components/input)
- [react.dev: Controlled vs Uncontrolled](https://react.dev/learn/sharing-state-between-components#controlled-and-uncontrolled-components)

**Ключевая мысль:** controlled input = React state единственный источник правды; `value` + `onChange` для каждого поля.



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

`useEffect` синхронизирует React-компонент с внешними системами: DOM API, таймеры, подписки, fetch, localStorage. Сигнатура: `useEffect(() => { /* effect */ return () => { /* cleanup */ }; }, [deps])`. Пустой массив deps `[]` — effect выполнится один раз при mount (аналог componentDidMount). `[dep]` — при изменении dep. Без массива deps — при каждом рендере (почти всегда ошибка).

Cleanup function вызывается перед повторным effect и при unmount: отписка от событий, очистка таймера, abort fetch. Без cleanup — утечки памяти и warnings. React Strict Mode в dev намеренно mount → unmount → mount, чтобы выявить missing cleanup.

Не всё требует effect. [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect): вычисление derived state, обработка клика, валидация формы — это event handlers, не effects. Effect — для синхронизации с внешним миром, когда нет события-повода. Stale closure — классический баг: effect с `[]` использует устаревший props/state; добавь их в deps. `useLayoutEffect` выполняется синхронно после DOM-мутаций, до paint — для измерений layout (обзор).

**Читать:**
- [useEffect](https://react.dev/reference/react/useEffect)
- [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
- [react.dev: Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects)

**Ключевая мысль:** useEffect — для синхронизации с внешним миром; cleanup обязателен; не дублируй логику обработчиков событий.



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

Загрузка данных в React-компоненте — классический сценарий для `useEffect` + `fetch`. Паттерн трёх (или четырёх) состояний: `loading` → `success` / `error` / `empty`. Реализуй через отдельные `useState` или discriminated union: `{ status: 'loading' } | { status: 'error', error: string } | { status: 'success', data: T }`. UI рендерит разную разметку в зависимости от `status`.

В effect: `fetch(url).then(res => { if (!res.ok) throw new Error(); return res.json() }).then(setData).catch(setError).finally(() => setLoading(false))`. Fetch не reject на HTTP 404 — проверяй `res.ok`. Race condition: пользователь быстро переключает id, старый ответ приходит последним. Решение — `AbortController` в cleanup: `const ctrl = new AbortController(); fetch(url, { signal: ctrl.signal }); return () => ctrl.abort()`.

Не вызывай `setState` на размонтированном компоненте — abort или флаг `let cancelled = false` в cleanup. Custom hook `useFetch<T>(url)` инкапсулирует весь паттерн: loading, error, data, refetch. Skeleton UI вместо пустого экрана улучшает perceived performance.

**Читать:**
- [MDN: Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [MDN: AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/)

**Ключевая мысль:** fetch в effect требует loading/error states, проверки `res.ok`, abort в cleanup и защиты от race condition.



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

Формы в React строятся на controlled components: каждое поле связано с state. Для формы из нескольких полей два подхода: отдельный `useState` на поле (проще для маленьких форм) или один объект `const [form, setForm] = useState({ name: '', email: '' })` с обновлением `setForm(f => ({ ...f, name: e.target.value }))`. Второй удобен для submit целиком и сброса.

Валидация на клиенте: `required`, `minLength`, regex для email, кастомные правила (пароль ≥ 8 символов). UX-паттерн touched/dirty: показывай ошибки после blur или submit, не при первом символе — это меньше раздражает. `useId()` генерирует стабильный уникальный id для связки `<label htmlFor={id}>` и `<input id={id}>` — важно для accessibility.

Сброс формы: верни state к начальным значениям. `noValidate` на `<form>` отключает браузерную валидацию, если реализуешь свою. Checkbox «согласен с условиями» — отдельный boolean state, блокирующий submit. React 19 Form Actions (обзор) упрощают submit через `action` prop, но controlled подход остаётся фундаментом.

**Читать:**
- [React — Forms](https://react.dev/reference/react-dom/components/form)
- [React — input](https://react.dev/reference/react-dom/components/input)
- [useId](https://react.dev/reference/react/useId)

**Ключевая мысль:** форма = набор controlled fields + валидация + сброс state; ошибки показывай после blur/submit, не мгновенно.



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

Lifting state up (подъём состояния) решает задачу, когда два или более компонента должны отображать или изменять одни данные. State перемещается к **ближайшему общему родителю**. Родитель хранит данные и передаёт вниз через props; дети сообщают об изменениях через callback props (`onSearchChange`, `onSortChange`). Siblings никогда не общаются напрямую — только через родителя.

Derived state — значения, вычисляемые из props или state при рендере: `const filtered = items.filter(i => i.title.includes(query))`. Не дублируй их в отдельном `useState` — иначе рассинхрон при обновлении источника. Prop drilling на 1–2 уровня — нормально; при глубокой вложенности (неделя 13) поможет Context.

Container/Presentational split: «умный» компонент управляет state и логикой, «глупый» — только рендерит по props. `useMemo` (preview) кэширует результат дорогой фильтрации: `useMemo(() => items.filter(...), [items, query])` — пересчёт только при изменении deps. Для 10 элементов не нужен; для 1000+ — заметная оптимизация.

**Читать:**
- [Sharing State Between Components](https://react.dev/learn/sharing-state-between-components)
- [react.dev: Extracting State Logic into a Reducer](https://react.dev/learn/extracting-state-logic-into-a-reducer) — preview
- [useMemo](https://react.dev/reference/react/useMemo)

**Ключевая мысль:** общий state — у ближайшего родителя; derived values вычисляй, не дублируй в useState.



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

Ревью недели — время закрепить правила hooks и подготовиться к React Todo Pro. Правила hooks: вызывай только на верхнем уровне (не в if/for) и только в React-функциях (компонентах или custom hooks). Нарушение ломает порядок hooks между рендерами. Custom hook — функция `useTodos()`, внутри которой `useState` + handlers; компонент остаётся тонким, логика переиспользуема.

React DevTools показывают дерево компонентов, props и state в реальном времени — незаменимый инструмент отладки. ESLint `react-hooks/exhaustive-deps` предупреждает о missing dependencies в useEffect — не отключай правило без веской причины и комментария. Strict Mode двойной mount — норма в dev, не баг.

Чеклист code review: state обновляется иммутабельно, effects имеют cleanup, inputs controlled, deps корректны, нет setState на unmounted компоненте. Конспект «useState vs useEffect»: state — для данных UI, effect — для синхронизации с внешним миром. Подготовка к Todo Pro: приоритеты, дедлайны, Quotable API — всё на базе изученных паттернов.

**Читать:**
- [React DevTools](https://react.dev/learn/react-developer-tools)
- [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks)
- [React Strict Mode](https://react.dev/reference/react/StrictMode)

**Ключевая мысль:** custom hooks выносят логику из компонентов; правила hooks и exhaustive-deps — страховка от типичных багов.



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


