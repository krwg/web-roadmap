# Неделя 13: React Router, хуки, Context

> **Цель недели:** построить многостраничное SPA с переиспользуемой логикой и глобальным состоянием.
> **Литература:** [React Router](https://reactrouter.com/en/main), [react.dev — Context](https://react.dev/learn/passing-data-deeply-with-context), [react.dev — Reusing Logic](https://react.dev/learn/reusing-logic-with-custom-hooks)

## День 85 (Пн): React Router — основы

### Теория
- [React Router — Tutorial](https://reactrouter.com/en/main/start/tutorial): `BrowserRouter`, `Routes`, `Route`
- [Link vs NavLink](https://reactrouter.com/en/main/components/link) — навигация без перезагрузки
- [useParams](https://reactrouter.com/en/main/hooks/use-params), [useNavigate](https://reactrouter.com/en/main/hooks/use-navigate)
- SPA vs MPA: клиентский роутинг меняет URL и компонент

### Практика
1. `npm install react-router-dom`
2. Страницы: `/` Home, `/about` About, `/contact` Contact
3. `Layout` с `<Outlet />` — общая шапка и навигация
4. `NavLink` с активным классом для текущей страницы

**Критерии:**
- [ ] Навигация без полной перезагрузки страницы
- [ ] 404-страница `path="*"`
- [ ] Layout оборачивает все маршруты

### Ловушки
- `BrowserRouter` внутри `BrowserRouter` — ошибка вложенности
- `<a href>` вместо `<Link>` — полная перезагрузка, теряется SPA

---

## День 86 (Вт): Динамические маршруты и nested routes

### Теория
- Динамические сегменты: `/projects/:id`
- [Nested Routes](https://reactrouter.com/en/main/start/tutorial#nested-routes) — вложенные `<Route>` и `<Outlet />`
- [useSearchParams](https://reactrouter.com/en/main/hooks/use-search-params) — query string `?tab=settings`
- Index routes — маршрут по умолчанию для родителя

### Практика
1. `/blog` — список постов, `/blog/:slug` — детальная страница
2. Данные постов — mock JSON или JSONPlaceholder
3. Breadcrumbs: Home → Blog → Post Title
4. Query `?sort=date` — сортировка списка

**Критерии:**
- [ ] `useParams` корректно читает `:slug`
- [ ] Несуществующий slug → страница «Не найдено»
- [ ] Breadcrumbs обновляются при навигации

### Ловушки
- Параметр `:id` всегда string — нужен `Number(id)` или валидация
- Забытый `<Outlet />` в layout — дочерние страницы не рендерятся

---

## День 87 (Ср): Custom Hooks — переиспользование логики

### Теория
- [Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks): функция `use*` вызывает другие хуки
- `useLocalStorage(key, initial)` — синхронизация state с localStorage
- `useFetch(url)` — обёртка над loading/error/data
- [useDebounce](https://www.developerway.com/posts/debouncing-in-react) — задержка для поиска

### Практика
1. Реализуй `useLocalStorage` с JSON parse/stringify
2. `useFetch(url)` — возвращает `{ data, loading, error, refetch }`
3. `useDebounce(value, 300)` — для поля поиска в FilterableList
4. Покрой хуки простыми тестами вручную (console + checklist)

**Критерии:**
- [ ] Хуки в папке `src/hooks/`
- [ ] `useLocalStorage` работает после F5
- [ ] `useDebounce` уменьшает количество фильтраций

### Ловушки
- Условный вызов хуков внутри custom hook — нарушение Rules of Hooks
- `useLocalStorage` без try/catch при битом JSON в storage

---

## День 88 (Чт): Context API — глобальное состояние

### Теория
- [createContext](https://react.dev/reference/react/createContext), [useContext](https://react.dev/reference/react/useContext)
- Provider оборачивает дерево, Consumer (или useContext) читает значение
- Когда Context: тема, язык, auth user — редко меняющиеся глобальные данные
- [Context — Caveats](https://react.dev/learn/passing-data-deeply-with-context#before-you-use-context): не замена всему state management

### Практика
1. `ThemeContext`: `theme`, `toggleTheme`, CSS-класс `dark` на `<html>`
2. `UserContext`: имя пользователя, setName — форма в Settings
3. Потребители на разных страницах без prop drilling
4. Вынеси Provider в `App.jsx` один раз

**Критерии:**
- [ ] Тема сохраняется в localStorage
- [ ] Минимум 3 компонента используют Context без промежуточных props
- [ ] Default value в createContext для dev-подсказок

### Ловушки
- Один Context на всё приложение — лишние ререндеры при любом изменении
- Забытый Provider — useContext возвращает default, баги «молча»

---

## День 89 (Пт): Комбинация Router + Context + Hooks

### Теория
- Protected routes: редирект на `/login` если нет user в Context
- [React Router — Auth pattern](https://reactrouter.com/en/main/examples/auth) (обзор)
- Loader pattern (React Router 6.4+) — опционально для data fetching
- Разделение: UI state локально, auth/theme — Context

### Практика
1. `AuthContext` с `user`, `login`, `logout` (mock, без реального API)
2. `ProtectedRoute` — children или `<Navigate to="/login" />`
3. `/dashboard` — только для авторизованных
4. После login — `navigate('/dashboard', { replace: true })`

**Критерии:**
- [ ] Неавторизованный пользователь не видит /dashboard
- [ ] Logout очищает Context и редиректит на /
- [ ] Login form — controlled inputs

### Ловушки
- Хранение «авторизации» только в state без persist — F5 разлогинивает
- Protected route проверяет только наличие объекта, не валидность token (позже на нед. 20)

---

## День 90 (Сб): Оптимизация и структура проекта

### Теория
- Структура: `pages/`, `components/`, `hooks/`, `contexts/`, `utils/`
- [useMemo](https://react.dev/reference/react/useMemo), [useCallback](https://react.dev/reference/react/useCallback) — когда нужны
- Code splitting: `React.lazy` + `Suspense` для тяжёлых страниц
- [React — Performance](https://react.dev/learn/render-and-commit)

### Практика
1. Реорганизуй проект недели по папкам
2. Lazy-load страницу `/admin` с fallback-спиннером
3. `useMemo` для дорогой фильтрации списка (1000+ элементов — mock)
4. Документируй архитектуру в `ARCHITECTURE.md` (1 страница)

**Критерии:**
- [ ] Импорты страниц через `React.lazy`
- [ ] Нет useMemo/useCallback «на всякий случай» без причины
- [ ] Понятная структура папок

### Ловушки
- Преждевременная оптимизация — сначала работающий код, потом профилирование
- `useCallback` без memoized child — бесполезен

---

## День 91 (Вс): Ревью паттернов React

### Теория
- Сравнение: props vs Context vs внешний store (Zustand/Redux — обзор)
- [React FAQ](https://react.dev/learn#faq)
- Error Boundaries — [react.dev](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)

### Практика
1. Добавь простой Error Boundary вокруг `<Routes>`
2. Пройди чеклист своего многостраничного приложения
3. Запиши ответы: «Когда Context, когда custom hook, когда lifting state?»
4. Подготовь skeleton для Dashboard (неделя 14)

**Критерии:**
- [ ] Error Boundary ловит ошибку в дочернем компоненте
- [ ] Написан план страниц Dashboard: /, /tasks, /weather, /settings
- [ ] Git commit за каждый день недели

---

## Проект недели

**Personal Portfolio SPA** (промежуточный, перед Dashboard):

1. Роутинг: Home, Projects, Project Detail `:id`, Blog, Contact
2. `ThemeContext` + `useLocalStorage`
3. Custom hooks: `useFetch` для GitHub API (repos), `useDebounce` для поиска проектов
4. Protected `/admin` с mock-auth
5. Адаптивная навигация (бургер-меню на мобиле)

**Критерии:**
- [ ] ≥ 5 маршрутов, nested layout
- [ ] ≥ 2 custom hooks, ≥ 1 Context
- [ ] 404, loading states, error handling
- [ ] Деплой на GitHub Pages или Vercel (preview)

## Ревью-чеклист
- Чем `Link` отличается от обычной `<a>`?
- Как передать query-параметры и прочитать их?
- Зачем custom hook, если можно просто функцию?
- Когда Context вызывает лишние ререндеры?
- Как защитить маршрут от неавторизованного доступа?
