# Неделя 14: Frontend Capstone — React Dashboard



> **Цель недели:** собрать полноценное SPA-приложение, объединяющее все навыки React-фронтенда.

> **Литература:** [react.dev](https://react.dev/learn), [React Router](https://reactrouter.com/en/main), [OpenWeatherMap API](https://openweathermap.org/api), [Vite Env Variables](https://vitejs.dev/guide/env-and-mode.html), [web.dev — Web Vitals](https://web.dev/vitals/)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)

> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-14/`



## День 92 (Пн): Архитектура и скелет проекта



### Теория

Frontend capstone начинается с архитектуры, а не с кода. Прежде чем писать компоненты, зафиксируй страницы (`/`, `/tasks`, `/weather`, `/settings`), источники данных (localStorage, Context, внешний API) и границы ответственности модулей. Хороший скелет экономит дни рефакторинга на середине недели.

Vite отделяет переменные окружения по префиксу: только `VITE_*` попадают в клиентский bundle. API-ключи OpenWeather никогда не хардкодь — `import.meta.env.VITE_WEATHER_API_KEY` и `.env.example` без реальных значений. Файл `.env` в `.gitignore`, иначе ключ утечёт на GitHub.

Структура папок: `pages/` для маршрутов, `components/ui/` для переиспользуемых кнопок и карточек, `hooks/` и `contexts/` для логики, `services/` для HTTP. Mobile-first CSS с CSS-переменными для темы закладывает адаптив с первого дня. Отдельная папка `learning-log/week-14/` с чистой git-историей — привычка, которая пригодится в capstone.

**Читать:**

- [Vite — Env Variables](https://vitejs.dev/guide/env-and-mode.html)
- [React Router](https://reactrouter.com/en/main)
- [Mobile-first CSS (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries)

**Ключевая мысль:** спланируй страницы и state до кода; секреты — только через `VITE_*` и `.env`.



### Практика

1. `npm create vite@latest week-14 -- --template react-ts` в `learning-log/`

2. Установи `react-router-dom`, настрой Layout + 4 маршрута

3. Заглушки страниц: Dashboard, Tasks, Weather, Settings

4. `App.css` — CSS-переменные для светлой/тёмной темы

5. `.env.example` с `VITE_WEATHER_API_KEY=`

6. Sidebar + main content area — responsive skeleton

7. `ARCHITECTURE.md` — план страниц и state на 1 страницу



**Критерии:**

- [ ] 4 маршрута с общим Layout

- [ ] Адаптивная sidebar/nav

- [ ] `.env` в `.gitignore`



### Git

```bash

cd learning-log/week-14

git add .

git commit -m "week-14 day-92: скелет Dashboard, Layout и 4 маршрута"

```



### Ловушки

- API-ключ в коде — утечка при push на GitHub

- Монолитный `App.jsx` на 500 строк — сразу дроби на модули



---



## День 93 (Вт): Dashboard — статистика и карточки



### Теория

Главная страница Dashboard — витрина приложения: несколько независимых виджетов в единой сетке. Композиция через мелкие компоненты (`StatCard`, `Grid`) проще в поддержке, чем один монолитный `Dashboard.tsx`. Каждая карточка получает данные через props или hooks и не знает о соседях.

CSS Grid с `repeat(auto-fit, minmax(240px, 1fr))` даёт адаптив без десятка media queries: на мобиле одна колонка, на desktop — четыре. Статистика задач — derived state: вычисляй `total` и `done` из массива tasks, не дублируй в отдельном `useState`, иначе рассинхрон неизбежен.

`useMemo` здесь оправдан, если фильтрация или агрегация затратна. Skeleton-карточки при загрузке предотвращают layout shift (CLS). Для иконок предпочитай inline SVG или библиотеку вроде lucide-react; у декоративных иконок добавляй `aria-hidden`, у смысловых — `aria-label`.

**Читать:**

- [MDN — CSS Grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout)
- [React — useMemo](https://react.dev/reference/react/useMemo)
- [Web Vitals — CLS](https://web.dev/articles/cls)

**Ключевая мысль:** статистика — производная от данных tasks, не отдельный источник правды.



### Практика

1. Главная `/` — 4 карточки: задачи (total/done), погода, имя user, дата

2. Данные задач из `useLocalStorage('tasks')`

3. Приветствие из `UserContext`

4. Responsive grid: 1 колонка мобила → 2 → 4 на desktop

5. Компонент `StatCard` с title, value, icon, trend (опционально)

6. Форматирование даты через `Intl.DateTimeFormat`

7. Empty state на карточке задач: «Добавьте первую задачу»



**Критерии:**

- [ ] Карточки обновляются при изменении tasks

- [ ] Нет layout shift при загрузке

- [ ] Контраст текста ≥ WCAG AA (проверь в DevTools)



### Git

```bash

cd learning-log/week-14

git add src/pages/Dashboard.tsx src/components/ui/StatCard.tsx

git commit -m "week-14 day-93: Dashboard stats и StatCard grid"

```



### Ловушки

- Хардкод статистики вместо вычисления из реальных данных

- Иконки без текстовой альтернативы для screen readers



---



## День 94 (Ср): Tasks — CRUD и фильтрация



### Теория

Страница Tasks — сердце Dashboard: здесь проверяется, насколько чисто организован state. Custom hook `useTasks` становится единственным источником правды: и Dashboard, и `/tasks` читают одни данные через один hook (или Context-обёртку над ним). Дублирование логики в двух страницах — прямой путь к багам.

CRUD в React всегда иммутабелен: `setTasks(prev => [...prev, newTask])`, toggle через `map`, delete через `filter`. Фильтры и сортировка — derived state от `tasks` + `filter` + `sortBy`, а не отдельные копии списка. Стабильный `key={task.id}` обязателен: `key={index}` ломает фокус и анимации при удалении.

Расширенная модель (приоритет, дедлайн) учит проектировать типы заранее. Просроченные задачи — вычисляемое свойство: `deadline < today`. Поиск с debounce (hook из недели 13) снижает нагрузку при больших списках. Persist в `localStorage` через hook сохраняет данные между сессиями.

**Читать:**

- [React — Keys](https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key)
- [React — Updating arrays in state](https://react.dev/learn/updating-arrays-in-state)
- [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)

**Ключевая мысль:** один `useTasks` на всё приложение; фильтры — derived state, не копия списка.



### Практика

1. Страница `/tasks`: форма добавления, список, фильтры (all/active/done)

2. Редактирование inline или modal

3. Приоритет (цветовая метка) и дедлайн

4. Сортировка: по дате, приоритету

5. Поиск по тексту задачи — filter + debounce

6. `useTasks` hook с persist в localStorage

7. Подсветка просроченных задач (deadline < today)



**Критерии:**

- [ ] CRUD полностью работает, persist в localStorage

- [ ] Фильтры не ломают редактирование

- [ ] `key` стабильный (id), не index



### Git

```bash

cd learning-log/week-14

git add src/hooks/useTasks.ts src/pages/Tasks.tsx

git commit -m "week-14 day-94: useTasks, CRUD и фильтры"

```



### Ловушки

- `key={index}` при удалении — скачки фокуса и баги

- Дублирование логики tasks в Dashboard и Tasks page



---



## День 95 (Чт): Weather — интеграция внешнего API



### Теория

Интеграция внешнего API — переход от учебного localStorage к реальному асинхронному миру. OpenWeather Current Weather API принимает город и ключ, возвращает температуру, влажность, описание и код иконки. Единицы (`metric` / `imperial`) лучше брать из Settings, а не хардкодить.

Три UI-состояния обязательны: loading (skeleton или spinner), error (сообщение + retry), success (данные). Проверяй `res.ok` — 401 (битый ключ), 404 (город не найден) и 429 (лимит free tier) должны давать понятный текст, а не «белый экран смерти». Кэш в `sessionStorage` на 10 минут с timestamp экономит квоту API.

`useFetch` или dedicated `weatherApi.ts` изолируют HTTP от компонента. Мини-виджет на Dashboard и полная страница `/weather` должны использовать один hook — иначе дублируется логика кэша. Debounce или submit по кнопке: запрос на каждый keystroke в поле города быстро исчерпает лимит.

**Читать:**

- [OpenWeatherMap Current Weather](https://openweathermap.org/current)
- [Fetch API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Vite Env Variables](https://vitejs.dev/guide/env-and-mode.html)

**Ключевая мысль:** API-слой отдельно от UI; loading/error/success — на каждом экране с данными.



### Практика

1. Страница `/weather`: input города, кнопка поиска

2. Отображение: температура, описание, иконка, влажность, ветер

3. Сохрани последний город в localStorage

4. Обработка неверного API key и лимита запросов

5. Кэш ответа в sessionStorage с timestamp

6. Мини-виджет погоды на Dashboard (тот же hook)

7. Retry кнопка при сетевой ошибке



**Критерии:**

- [ ] Loading / error / success states

- [ ] Кэш 10 мин — повторный запрос не уходит в сеть

- [ ] Город по умолчанию из Settings



### Git

```bash

cd learning-log/week-14

git add src/pages/Weather.tsx src/services/weatherApi.ts

git commit -m "week-14 day-95: OpenWeather API и кэш"

```



### Ловушки

- Запрос на каждый keystroke — debounce или submit по кнопке

- Не обработанный `res.ok === false` — «белый экран смерти»



---



## День 96 (Пт): Settings — Context и персонализация



### Теория

Settings — центр персонализации и хороший тест на Context. Разделяй `ThemeContext` и `UserContext`: смена имени пользователя не должна перерисовывать подписчиков темы. Controlled form синхронизирует поля с state; изменения сразу отражаются на Dashboard и Weather без перезагрузки.

`useId()` генерирует стабильные id для связки `label` + `input` — важно для доступности и для избежания коллизий при нескольких формах. Валидация на клиенте (имя ≥ 2 символов, город не пустой) улучшает UX, даже если позже добавишь серверную проверку.

Деструктивные действия («Сбросить настройки») требуют confirm dialog. Persist через `localStorage` в Provider или custom hook. Бонус export/import JSON — учит сериализовать state целиком. Toast при успешном сохранении даёт обратную связь без блокировки UI.

**Читать:**

- [React — useId](https://react.dev/reference/react/useId)
- [React — Forms](https://react.dev/reference/react-dom/components/form)
- [Context](https://react.dev/learn/passing-data-deeply-with-context)

**Ключевая мысль:** Settings — single source для темы, города и единиц; разделяй контексты по доменам.



### Практика

1. `/settings`: имя, город по умолчанию, переключатель темы, единицы °C/°F

2. Изменения сразу отражаются на Dashboard и Weather

3. Кнопка «Сбросить настройки» с confirm dialog

4. Экспорт/импорт настроек JSON (bonus)

5. `useId()` для всех полей формы

6. Валидация с сообщениями под полями

7. Toast при успешном сохранении



**Критерии:**

- [ ] Тема применяется ко всему приложению

- [ ] Настройки переживают F5

- [ ] Form labels связаны с inputs



### Git

```bash

cd learning-log/week-14

git add src/contexts/ src/pages/Settings.tsx

git commit -m "week-14 day-96: Settings, Context и персонализация"

```



### Ловушки

- Один Context на theme + user + settings — лишние ререндеры

- Сброс без confirm — случайная потеря данных



---



## День 97 (Сб): Полировка UX и адаптив



### Теория

Полировка UX отличает «работает» от «приятно пользоваться». Адаптив — не опция: начни с 320px ширины, убедись, что нет horizontal scroll. Hamburger-меню на мобиле превращает sidebar в drawer; на desktop — постоянная навигация. Touch targets ≥ 44px снижают mis-tap на телефоне.

Доступность: `:focus-visible` вместо `outline: none`, tab-навигация по всем интерактивным элементам, контраст текста ≥ WCAG AA (проверь в DevTools). `prefers-reduced-motion` уважает настройки ОС — отключи лишние анимации для пользователей с вестибулярными расстройствами.

Toast-уведомления — лёгкий паттерн feedback при CRUD. Empty states («Нет задач — добавьте первую») лучше пустой таблицы. Lighthouse audit: цель Performance ≥ 80, Accessibility ≥ 90. Микро-анимации через CSS transitions добавляют «живости» без тяжёлых библиотек.

**Читать:**

- [MDN — Responsive design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [Web Vitals](https://web.dev/vitals/)
- [prefers-reduced-motion (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)

**Ключевая мысль:** a11y и mobile-first — часть Definition of Done, не «потом».



### Практика

1. Мобильное меню (hamburger → drawer)

2. Toast-уведомления: задача добавлена, ошибка API

3. Empty state: «Нет задач — добавьте первую»

4. Lighthouse audit — цель Performance ≥ 80, Accessibility ≥ 90

5. Focus styles на всех интерактивных элементах

6. Проверка на 320px ширине — нет horizontal scroll

7. CSS transitions на hover/focus (с reduced-motion fallback)



**Критерии:**

- [ ] Tab-навигация по всем интерактивным элементам

- [ ] Нет горизонтального скролла на 320px

- [ ] Lighthouse Accessibility ≥ 90



### Git

```bash

cd learning-log/week-14

git add src/components/

git commit -m "week-14 day-97: mobile nav, toast и a11y polish"

```



### Ловушки

- `outline: none` без замены — ломает a11y

- Фиксированная sidebar на мобиле закрывает контент



---



## День 98 (Вс): Тестирование вручную и документация



### Теория

React Dashboard — крупнейший фронтенд-проект до бэкенда; день ревью фиксирует качество, а не добавляет фичи. Пройди user flow глазами новичка: первый визит → настройки → задачи → погода → смена темы → F5. Каждый шаг должен работать без инструкции в README.

Production build (`npm run build`) часто выявляет warnings, которые dev-сервер скрывает: неиспользуемые импорты, env без fallback. Deploy на Vercel/Netlify требует настройки SPA fallback для client-side routes. README с GIF или скриншотами — визитная карточка для портфолио.

Conventional Commits за неделю показывают зрелость: `feat:`, `fix:`, `docs:` в сообщениях. `ARCHITECTURE.md` обнови финальной схемой state. Этот проект станет основой для full-stack интеграции на неделях 21–22 — чистая структура сейчас сэкономит часы потом.

**Читать:**

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Vercel — Vite](https://vercel.com/docs/frameworks/vite)
- [Vitest (обзор для нед. 20)](https://vitest.dev/)

**Ключевая мысль:** capstone-качество начинается с README, deploy preview и осмысленной git-истории.



### Практика

1. Пройди user flow: первый визит → настройки → задачи → погода → смена темы → F5

2. Напиши README с GIF или 3 скриншотами

3. `npm run build` — исправь warnings

4. Deploy preview на [Vercel](https://vercel.com/docs/frameworks/vite)

5. Обнови `ARCHITECTURE.md` — финальная схема state

6. Self-review по ревью-чеклисту недели

7. Тег `week-14-done`



**Критерии:**

- [ ] Production build без ошибок

- [ ] README понятен новичку

- [ ] Preview URL в README



### Git

```bash

cd learning-log/week-14

git add README.md ARCHITECTURE.md

git commit -m "week-14 day-98: README, deploy и React Dashboard capstone"

```



---



## Проект недели



**React Dashboard SPA** — итоговый deliverable недели, крупнейший фронтенд-проект до бэкенда. Подробное ТЗ: [docs/projects.md — Неделя 14](../../docs/projects.md#неделя-14--react-dashboard-frontend-milestone).



Маршруты: `/` статистика, `/tasks` CRUD, `/weather` API, `/settings` тема и user. React Router, hooks, Context, адаптив, deploy preview.



**Функции:**

- Dashboard с live-статистикой из tasks и user context

- Tasks: CRUD, приоритет, дедлайн, фильтры, поиск

- Weather: OpenWeatherMap, кэш, retry, единицы из settings

- Settings: тема, имя, город, export/import (bonus)



**Критерии:**

- [ ] Все 4 страницы полностью функциональны

- [ ] Нет prop drilling глубже 2 уровней

- [ ] GitHub repo с понятной историей коммитов (≥ 7 за неделю)

- [ ] Vercel/Netlify preview работает

- [ ] Lighthouse Accessibility ≥ 90

- [ ] `.env.example` без реальных ключей

- [ ] Тег `week-14-done`



## Ревью-чеклист

- Могу объяснить архитектуру проекта за 2 минуты?

- Где хранится state задач и почему именно там?

- Как бы добавил авторизацию к этому Dashboard?

- Что произойдёт при истечении API-ключа OpenWeather?

- Какие 3 улучшения сделал бы в v2?


