# Неделя 13: React Router, хуки, Context



> **Цель недели:** построить многостраничное SPA с переиспользуемой логикой и глобальным состоянием.

> **Литература:** [React Router](https://reactrouter.com/en/main), [react.dev — Context](https://react.dev/learn/passing-data-deeply-with-context), [react.dev — Reusing Logic](https://react.dev/learn/reusing-logic-with-custom-hooks), [React Router Tutorial](https://reactrouter.com/en/main/start/tutorial), [useDebounce patterns](https://www.developerway.com/posts/debouncing-in-react)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)

> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-13/`



## День 85 (Пн): React Router — основы



### Теория

Одностраничное приложение (SPA) живёт в одной HTML-странице, но пользователь ожидает поведение «настоящего сайта»: разные URL, кнопка «Назад» в браузере, закладки на конкретные экраны. React Router решает эту задачу на клиенте: при смене маршрута он размонтирует один набор компонентов и смонтирует другой, не перезагружая документ целиком.

Три кита базовой настройки — `BrowserRouter`, `Routes` и `Route`. Router подключает приложение к History API браузера (`pushState` под капотом); `Routes` выбирает единственный подходящий маршрут; `Route` связывает путь с компонентом. Для навигации внутри SPA используй `Link` или `NavLink`: они меняют URL без полной перезагрузки, в отличие от обычного `<a href>`, который сбрасывает состояние приложения.

Layout с `<Outlet />` — стандартный паттерн общей оболочки: шапка и меню остаются на месте, а содержимое страницы подставляется в outlet. Catch-all маршрут `path="*"` обязателен для 404. При деплое в subdirectory (GitHub Pages) понадобится `basename`; сервер должен отдавать `index.html` на все пути, иначе прямой заход по URL `/about` вернёт 404 от nginx, а не твой React-компонент.

**Читать:**

- [React Router — Tutorial](https://reactrouter.com/en/main/start/tutorial)
- [Link vs NavLink](https://reactrouter.com/en/main/components/link)
- [useParams](https://reactrouter.com/en/main/hooks/use-params)
- [useNavigate](https://reactrouter.com/en/main/hooks/use-navigate)

**Ключевая мысль:** SPA-навигация — смена компонентов без перезагрузки; для внутренних ссылок — `Link`, не `<a>`.



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

Статический маршрут `/about` покрывает фиксированную страницу, но реальные приложения оперируют сущностями с идентификаторами: посты, проекты, профили. Динамический сегмент `/blog/:slug` превращает часть URL в параметр, который компонент читает через `useParams`. Помни: все параметры приходят строками — для чисел нужны `Number()` или явная валидация.

Вложенные маршруты (nested routes) строят иерархию UI: общий layout для раздела `/blog` и дочерние страницы списка и детали. Родительский `Route` рендерит layout с `<Outlet />`; без outlet дочерние страницы просто не появятся — классическая ловушка. Index route задаёт страницу по умолчанию, когда пользователь открывает родительский путь без суффикса.

Query string (`?sort=date&tab=comments`) описывает фильтры и вкладки, не меняя структуру пути. `useSearchParams` даёт к ним доступ в React-стиле. `useLocation` полезен для breadcrumbs и для передачи временного state при `navigate('/path', { state: { from: 'list' } })`. В React Router 6.4+ `useMatches` помогает строить цепочку навигации из дерева маршрутов.

**Читать:**

- [Nested Routes](https://reactrouter.com/en/main/start/tutorial#nested-routes)
- [useSearchParams](https://reactrouter.com/en/main/hooks/use-search-params)
- [useLocation](https://reactrouter.com/en/main/hooks/use-location)

**Ключевая мысль:** путь описывает «где», query — «как показать»; параметры маршрута всегда строки.



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

Custom hook — обычная функция с префиксом `use`, внутри которой вызываются другие хуки. Она не добавляет новых возможностей React, а выносит повторяющуюся логику из компонентов: синхронизацию с `localStorage`, загрузку данных, debounce ввода. Компонент остаётся про UI, хук — про поведение.

Типичный `useLocalStorage(key, initial)` комбинирует `useState` и `useEffect`: при изменении state значение пишется в storage, при монтировании — читается обратно. Оборачивай `JSON.parse` в try/catch — битые данные не должны ронять приложение. `useFetch(url)` инкапсулирует три состояния (loading, error, data) и избавляет каждую страницу от копипасты `useEffect`.

`useDebounce(value, delay)` откладывает обновление: пока пользователь печатает в поиске, тяжёлая фильтрация не запускается на каждый символ. Правила хуков действуют и внутри custom hook — нельзя вызывать хуки условно. Возвращай объект `{ data, loading }` или tuple, но придерживайся одного стиля в проекте.

**Читать:**

- [Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
- [useDebounce patterns](https://www.developerway.com/posts/debouncing-in-react)
- [renderHook (Testing Library)](https://testing-library.com/docs/react-testing-library/api/#renderhook)

**Ключевая мысль:** custom hook извлекает логику, а не UI; правила хуков обязательны внутри него.



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

Prop drilling — передача props через пять уровней дерева — быстро превращает код в лабиринт. Context API даёт альтернативу: Provider в корне публикует значение, любой потомок читает его через `useContext` без промежуточных компонентов. Классические кандидаты: тема оформления, язык интерфейса, данные текущего пользователя.

`createContext(defaultValue)` создаёт контекст; default нужен для подсказок в dev и как fallback, если забыли Provider. Разделяй контексты по доменам: `ThemeContext` отдельно от `UserContext`, иначе смена темы перерисует всё дерево, включая компоненты, которым нужен только user. Оборачивай `value` Provider в `useMemo`, если передаёшь объект или функции.

Context не заменяет локальный state и не является полноценным store. Документация React предупреждает: не тащи в Context часто меняющиеся данные. Для сложного глобального state комбинация Context + `useReducer` — разумный следующий шаг, но для учебного проекта двух отдельных контекстов (theme + user) достаточно.

**Читать:**

- [createContext](https://react.dev/reference/react/createContext)
- [useContext](https://react.dev/reference/react/useContext)
- [Context — Caveats](https://react.dev/learn/passing-data-deeply-with-context#before-you-use-context)

**Ключевая мысль:** Context — для редко меняющихся глобальных данных; разделяй провайдеры и мемоизируй value.



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

На этой неделе складываются три слоя: Router отвечает за URL, Context — за глобальное состояние (auth, theme), custom hooks — за переиспользуемую логику. Protected route — тонкая обёртка: если в `AuthContext` нет пользователя, рендерится `<Navigate to="/login" replace />`, иначе — дочерняя страница.

Mock-авторизация без реального API — нормальная ступень обучения: сохраняй объект user в `localStorage`, восстанавливай при старте. Без persist пользователь «разлогинится» после F5. Logout должен атомарно очистить Context, storage и перенаправить на публичную страницу через `useNavigate` или декларативный `<Navigate>`.

Разделяй ответственность: форма логина — controlled inputs; проверка доступа — в `ProtectedRoute`; данные сессии — в Context. `location.state` позволяет передать, откуда пришёл пользователь, чтобы после login вернуть его на исходную страницу, а не всегда на `/dashboard`.

**Читать:**

- [React Router — Auth pattern](https://reactrouter.com/en/main/examples/auth)
- [Navigate](https://reactrouter.com/en/main/components/navigate)
- [useNavigate](https://reactrouter.com/en/main/hooks/use-navigate)

**Ключевая мысль:** protected route проверяет сессию на уровне маршрута; persist в storage переживает перезагрузку.



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

К концу недели проект обрастает папками: `pages/`, `components/`, `hooks/`, `contexts/`, `utils/`. Предсказуемая структура важнее идеальной: новый разработчик (или ты через месяц) должен за минуту найти, где живут маршруты и где — хуки. `ARCHITECTURE.md` фиксирует решения, а не дублирует README с командами запуска.

Оптимизация в React начинается с измерения, а не с `useMemo` на каждой функции. Profiler в DevTools показывает лишние ререндеры. `React.lazy` + `Suspense` разбивают bundle: тяжёлая страница `/admin` загружается только при переходе. `useMemo` оправдан для дорогих вычислений; `useCallback` — когда передаёшь колбэк в `React.memo`-компонент.

Barrel exports (`index.ts`) ускоряют импорты, но могут ухудшить tree-shaking — используй осознанно. `useCallback` без memoized child бесполезен. Преждевременная мемоизация усложняет код без выигрыша: сначала работающее приложение, потом профилирование, потом точечные правки.

**Читать:**

- [useMemo](https://react.dev/reference/react/useMemo)
- [useCallback](https://react.dev/reference/react/useCallback)
- [React — Performance](https://react.dev/learn/render-and-commit)
- [React.lazy](https://react.dev/reference/react/lazy)

**Ключевая мысль:** оптимизируй после профилирования; lazy routes уменьшают начальный bundle.



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

За семь дней ты собрал многостраничное SPA с роутингом, глобальным state и переиспользуемыми хуками. Полезно явно сравнить инструменты: локальный state для UI формы, lifting state когда нужно двум соседям, custom hook для логики, Context для редких глобальных данных, внешний store (Zustand/Redux) — когда Context разрастается.

Error Boundary ловит ошибки рендеринга в дочерних компонентах и показывает fallback вместо белого экрана. Оберни `<Routes>` или отдельные страницы, чтобы сбой на `/blog/:slug` не убивал всё приложение. Boundary не ловит ошибки в event handlers и async-коде — только синхронный render.

Перед деплоем проверь client-side routing: хостинг должен отдавать `index.html` на все пути. Portfolio SPA — витрина навыков недели: осмысленные коммиты за 7 дней, preview URL, README с картой маршрутов. Скелет Dashboard на неделю 14 логично начать с тех же паттернов Layout + Context + hooks.

**Читать:**

- [React FAQ](https://react.dev/learn#faq)
- [Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)

**Ключевая мысль:** выбор инструмента state — по частоте изменений и глубине дерева, не «всё в Context».



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


