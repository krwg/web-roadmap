# Неделя 13: React Router, хуки, Context

> **Цель недели:** построить многостраничное SPA с переиспользуемой логикой и глобальным состоянием.
> **Литература:** [React Router](https://reactrouter.com/en/main), [react.dev — Context](https://react.dev/learn/passing-data-deeply-with-context), [react.dev — Reusing Logic](https://react.dev/learn/reusing-logic-with-custom-hooks), [React Router Tutorial](https://reactrouter.com/en/main/start/tutorial), [useDebounce patterns](https://www.developerway.com/posts/debouncing-in-react)
> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-13/`

## День 85 (Пн): React Router — основы

### Теория
- [React Router — Tutorial](https://reactrouter.com/en/main/start/tutorial): `BrowserRouter`, `Routes`, `Route`
- [Link vs NavLink](https://reactrouter.com/en/main/components/link) — навигация без перезагрузки
- [useParams](https://reactrouter.com/en/main/hooks/use-params), [useNavigate](https://reactrouter.com/en/main/hooks/use-navigate)
- SPA vs MPA: клиентский роутинг меняет URL и компонент
- History API — `pushState` под капотом BrowserRouter
- `basename` — деплой в subdirectory (GitHub Pages)
- 404 route `path="*"` — catch-all для несуществующих путей
- Server config для SPA — все пути → index.html (обзор для деплоя)

### Практика
1. `npm install react-router-dom` в `learning-log/week-13/`
2. Страницы: `/` Home, `/about` About, `/contact` Contact
3. `Layout` с `<Outlet />` — общая шапка и навигация
4. `NavLink` с активным классом для текущей страницы
5. Страница 404 с ссылкой на главную
6. Вынеси маршруты в `src/routes.tsx` или `App.tsx`
7. Проверь: прямой переход по URL `/about` работает (dev server)

**Критерии:**
- [ ] Навигация без полной перезагрузки страницы
- [ ] 404-страница `path="*"`
- [ ] Layout оборачивает все маршруты

### Git
```bash
cd learning-log/week-13
git add src/pages/ src/components/Layout.tsx
git commit -m "week-13 day-85: React Router, Layout и 404"
```

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
- Optional params и splat `*` — обзор
- Relative links в nested routes — `relative="path"`
- `useLocation` — текущий pathname, state при navigate
- Breadcrumbs из `useMatches` (обзор RR 6.4+)

### Практика
1. `/blog` — список постов, `/blog/:slug` — детальная страница
2. Данные постов — mock JSON или JSONPlaceholder
3. Breadcrumbs: Home → Blog → Post Title
4. Query `?sort=date` — сортировка списка
5. Несуществующий slug → страница «Не найдено»
6. Nested layout для `/blog` с sidebar категорий
7. `useSearchParams` для tab: `?tab=comments`

**Критерии:**
- [ ] `useParams` корректно читает `:slug`
- [ ] Несуществующий slug → страница «Не найдено»
- [ ] Breadcrumbs обновляются при навигации

### Git
```bash
cd learning-log/week-13
git add src/pages/blog/
git commit -m "week-13 day-86: динамические маршруты и breadcrumbs"
```

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
- Правила хуков соблюдаются внутри custom hook
- Хук возвращает объект или tuple — соглашение команды
- Тестирование хуков — `@testing-library/react` renderHook (обзор)
- Разделение: хук = логика, компонент = UI

### Практика
1. Реализуй `useLocalStorage` с JSON parse/stringify
2. `useFetch(url)` — возвращает `{ data, loading, error, refetch }`
3. `useDebounce(value, 300)` — для поля поиска в FilterableList
4. Покрой хуки простыми тестами вручную (console + checklist)
5. `useMediaQuery('(min-width: 768px)')` — responsive hook
6. Вынеси хуки в `src/hooks/` с index re-export
7. JSDoc/TSDoc для публичного API каждого хука

**Критерии:**
- [ ] Хуки в папке `src/hooks/`
- [ ] `useLocalStorage` работает после F5
- [ ] `useDebounce` уменьшает количество фильтраций

### Git
```bash
cd learning-log/week-13
git add src/hooks/
git commit -m "week-13 day-87: useLocalStorage, useFetch и useDebounce"
```

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
- Разделение контекстов: ThemeContext отдельно от UserContext
- `useMemo` для value Provider — избежать лишних ререндеров
- Default value в createContext — fallback и dev-подсказки
- Context + useReducer для сложного state (обзор)

### Практика
1. `ThemeContext`: `theme`, `toggleTheme`, CSS-класс `dark` на `<html>`
2. `UserContext`: имя пользователя, setName — форма в Settings
3. Потребители на разных страницах без prop drilling
4. Вынеси Provider в `App.tsx` один раз
5. Persist theme в localStorage через useEffect в Provider
6. Custom hook `useTheme()` — обёртка над useContext
7. Проверь: смена темы на /settings отражается на /

**Критерии:**
- [ ] Тема сохраняется в localStorage
- [ ] Минимум 3 компонента используют Context без промежуточных props
- [ ] Default value в createContext для dev-подсказок

### Git
```bash
cd learning-log/week-13
git add src/contexts/
git commit -m "week-13 day-88: ThemeContext и UserContext"
```

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
- `Navigate` component vs `useNavigate` — декларативный vs императивный редирект
- `location.state` — передать данные при navigate
- Persist auth в localStorage — mock token для недели 13
- Logout: очистка context + navigate + clear storage

### Практика
1. `AuthContext` с `user`, `login`, `logout` (mock, без реального API)
2. `ProtectedRoute` — children или `<Navigate to="/login" />`
3. `/dashboard` — только для авторизованных
4. После login — `navigate('/dashboard', { replace: true })`
5. Страница `/login` — controlled form, mock credentials
6. Persist user в localStorage — переживает F5
7. Header: кнопка Logout на всех страницах

**Критерии:**
- [ ] Неавторизованный пользователь не видит /dashboard
- [ ] Logout очищает Context и редиректит на /
- [ ] Login form — controlled inputs

### Git
```bash
cd learning-log/week-13
git add src/contexts/AuthContext.tsx src/components/ProtectedRoute.tsx
git commit -m "week-13 day-89: AuthContext и protected routes"
```

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
- `React.memo` — мемоизация компонента при стабильных props
- Profiler в DevTools — найти лишние ререндеры
- Barrel exports — `index.ts` в папках (осторожно с tree-shaking)
- ARCHITECTURE.md — документирование решений

### Практика
1. Реорганизуй проект недели по папкам
2. Lazy-load страницу `/admin` с fallback-спиннером
3. `useMemo` для дорогой фильтрации списка (1000+ элементов — mock)
4. Документируй архитектуру в `ARCHITECTURE.md` (1 страница)
5. `React.memo` на `TodoItem` — измерь, есть ли выгода
6. Suspense boundary с понятным fallback UI
7. Проверь bundle size после lazy loading

**Критерии:**
- [ ] Импорты страниц через `React.lazy`
- [ ] Нет useMemo/useCallback «на всякий случай» без причины
- [ ] Понятная структура папок

### Git
```bash
cd learning-log/week-13
git add ARCHITECTURE.md src/pages/
git commit -m "week-13 day-90: lazy routes, useMemo и структура"
```

### Ловушки
- Преждевременная оптимизация — сначала работающий код, потом профилирование
- `useCallback` без memoized child — бесполезен

---

## День 91 (Вс): Ревью паттернов React

### Теория
- Сравнение: props vs Context vs внешний store (Zustand/Redux — обзор)
- [React FAQ](https://react.dev/learn#faq)
- Error Boundaries — [react.dev](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)
- Когда custom hook, когда Context, когда lifting state — decision tree
- Подготовка Portfolio SPA — финальная сборка проекта недели
- Git: осмысленная история за 7 дней
- Деплой SPA с client-side routing

### Практика
1. Добавь простой Error Boundary вокруг `<Routes>`
2. Пройди чеклист своего многостраничного приложения
3. Запиши ответы: «Когда Context, когда custom hook, когда lifting state?»
4. Подготовь skeleton для Dashboard (неделя 14)
5. Финализируй **Portfolio SPA** — все маршруты и hooks
6. Deploy preview на Vercel/Netlify
7. Тег `week-13-done`

**Критерии:**
- [ ] Error Boundary ловит ошибку в дочернем компоненте
- [ ] Написан план страниц Dashboard: /, /tasks, /weather, /settings
- [ ] Git commit за каждый день недели

### Git
```bash
cd learning-log/week-13
git add .
git commit -m "week-13 day-91: Error Boundary и Portfolio SPA deploy"
```

---

## Проект недели

**Personal Portfolio SPA** (промежуточный, перед Dashboard). Подробное ТЗ: [docs/projects.md — Неделя 13](../../docs/projects.md#неделя-13--portfolio-spa).

1. Роутинг: Home, Projects, Project Detail `:id`, Blog, Contact
2. `ThemeContext` + `useLocalStorage`
3. Custom hooks: `useFetch` для GitHub API (repos), `useDebounce` для поиска проектов
4. Protected `/admin` с mock-auth
5. Адаптивная навигация (бургер-меню на мобиле)

**Критерии:**
- [ ] ≥ 5 маршрутов, nested layout
- [ ] ≥ 2 custom hooks, ≥ 1 Context
- [ ] 404, loading states, error handling
- [ ] GitHub API repos на странице Projects
- [ ] Деплой на GitHub Pages или Vercel (preview)
- [ ] README с URL и описанием маршрутов
- [ ] Тег `week-13-done`

## Ревью-чеклист
- Чем `Link` отличается от обычной `<a>`?
- Как передать query-параметры и прочитать их?
- Зачем custom hook, если можно просто функцию?
- Когда Context вызывает лишние ререндеры?
- Как защитить маршрут от неавторизованного доступа?
