# Неделя 14: Frontend Capstone — React Dashboard

> **Цель недели:** собрать полноценное SPA-приложение, объединяющее все навыки React-фронтенда.
> **Литература:** [react.dev](https://react.dev/learn), [React Router](https://reactrouter.com/en/main), [OpenWeatherMap API](https://openweathermap.org/api), [Vite Env Variables](https://vitejs.dev/guide/env-and-mode.html), [web.dev — Web Vitals](https://web.dev/vitals/)
> **Проект недели:** см. [docs/projects.md](../../docs/projects.md)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-14/`

## День 92 (Пн): Архитектура и скелет проекта

### Теория
- Планирование SPA: страницы, shared state, API-контракты
- [Vite — Env Variables](https://vitejs.dev/guide/env-and-mode.html): `VITE_*` для ключей API
- Структура: `pages/`, `components/ui/`, `hooks/`, `contexts/`, `services/api.js`
- Mobile-first CSS, CSS Modules или простой BEM
- Feature-based vs layer-based структура — выбор для Dashboard
- Shared UI kit: Button, Card, Input — переиспользование
- `.env.example` — документирование переменных без секретов
- Git: отдельная папка `learning-log/week-14/` с чистой историей

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
- Композиция UI: `Card`, `StatWidget`, `Grid`
- [MDN — CSS Grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout)
- Мемоизация вычислений: `useMemo` для агрегатов
- Доступность: семантика, `aria-label` на иконках
- Derived state — статистика из tasks, не дублировать в useState
- Skeleton cards — placeholder при загрузке
- Responsive grid: `grid-template-columns: repeat(auto-fit, minmax(...))`
- Иконки: SVG inline или lucide-react (обзор)

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
- Custom hook `useTasks` — единый источник правды для задач
- Immutability: add, toggle, delete, edit
- Фильтры и сортировка как derived state
- [React — Keys](https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key)
- Optimistic UI — обзор (не обязательно на этой неделе)
- Inline edit vs modal — UX trade-offs
- Приоритет и дедлайн — расширение модели Todo
- Синхронизация tasks между Dashboard и Tasks page через общий hook/context

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
- [OpenWeatherMap Current Weather](https://openweathermap.org/current) — endpoint, units
- `useFetch` + обработка 401/404/429
- Кэширование в sessionStorage на 10 минут
- UX: skeleton, retry, empty state (город не найден)
- API key в `import.meta.env.VITE_WEATHER_API_KEY`
- Units: metric vs imperial — настройка из Settings
- Иконки погоды: URL от OWM или emoji fallback
- Rate limits free tier — не спамить запросами

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
- `ThemeContext` + `UserContext` — разделение ответственности
- Controlled settings form, sync с localStorage
- [React — useId](https://react.dev/reference/react/useId) для связки label/input
- Валидация: имя ≥ 2 символов, город не пустой
- Settings как single source для default city, units, theme
- Cross-page sync — изменения в Settings отражаются сразу
- Confirm dialog для destructive actions
- Export/import settings JSON — bonus feature

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
- [MDN — Responsive design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- `:focus-visible`, keyboard navigation
- Empty states, micro-interactions (CSS transitions)
- [Web Vitals](https://web.dev/vitals/) — LCP, CLS (обзор)
- Toast notifications — паттерн feedback
- Hamburger menu — mobile nav pattern
- `prefers-reduced-motion` — уважение к настройкам ОС
- Touch targets ≥ 44px на мобиле

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
- Чеклист E2E вручную vs автотесты (Vitest — неделя 20)
- README: установка, env, скриншоты, архитектура
- [Conventional Commits](https://www.conventionalcommits.org/) для истории
- Production checklist: build, env, routing, 404
- Vercel/Netlify deploy для Vite SPA
- Screenshot/GIF в README — демонстрация для портфолио
- Frontend milestone — крупнейший фронтенд-проект до бэкенда

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
