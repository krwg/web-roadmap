# Неделя 14: Frontend Capstone — React Dashboard

> **Цель недели:** собрать полноценное SPA-приложение, объединяющее все навыки React-фронтенда.
> **Литература:** [react.dev](https://react.dev/learn), [React Router](https://reactrouter.com/en/main), [OpenWeatherMap API](https://openweathermap.org/api)

## День 92 (Пн): Архитектура и скелет проекта

### Теория
- Планирование SPA: страницы, shared state, API-контракты
- [Vite — Env Variables](https://vitejs.dev/guide/env-and-mode.html): `VITE_*` для ключей API
- Структура: `pages/`, `components/ui/`, `hooks/`, `contexts/`, `services/api.js`
- Mobile-first CSS, CSS Modules или простой BEM

### Практика
1. `npm create vite@latest dashboard-app -- --template react`
2. Установи `react-router-dom`, настрой Layout + 4 маршрута
3. Заглушки страниц: Dashboard, Tasks, Weather, Settings
4. `App.css` — CSS-переменные для светлой/тёмной темы
5. `.env.example` с `VITE_WEATHER_API_KEY=`

**Критерии:**
- [ ] 4 маршрута с общим Layout
- [ ] Адаптивная sidebar/nav
- [ ] `.env` в `.gitignore`

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

### Практика
1. Главная `/` — 4 карточки: задачи (total/done), погода, имя user, дата
2. Данные задач из `useLocalStorage('tasks')`
3. Приветствие из `UserContext`
4. Responsive grid: 1 колонка мобила → 2 → 4 на desktop

**Критерии:**
- [ ] Карточки обновляются при изменении tasks
- [ ] Нет layout shift при загрузке
- [ ] Контраст текста ≥ WCAG AA (проверь в DevTools)

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

### Практика
1. Страница `/tasks`: форма добавления, список, фильтры (all/active/done)
2. Редактирование inline или modal
3. Приоритет (цветовая метка) и дедлайн
4. Сортировка: по дате, приоритету

**Критерии:**
- [ ] CRUD полностью работает, persist в localStorage
- [ ] Фильтры не ломают редактирование
- [ ] `key` стабильный (id), не index

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

### Практика
1. Страница `/weather`: input города, кнопка поиска
2. Отображение: температура, описание, иконка, влажность, ветер
3. Сохрани последний город в localStorage
4. Обработка неверного API key и лимита запросов

**Критерии:**
- [ ] Loading / error / success states
- [ ] Кэш 10 мин — повторный запрос не уходит в сеть
- [ ] Город по умолчанию из Settings

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

### Практика
1. `/settings`: имя, город по умолчанию, переключатель темы, единицы °C/°F
2. Изменения сразу отражаются на Dashboard и Weather
3. Кнопка «Сбросить настройки» с confirm dialog
4. Экспорт/импорт настроек JSON (bonus)

**Критерии:**
- [ ] Тема применяется ко всему приложению
- [ ] Настройки переживают F5
- [ ] Form labels связаны с inputs

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

### Практика
1. Мобильное меню (hamburger → drawer)
2. Toast-уведомления: задача добавлена, ошибка API
3. Empty state: «Нет задач — добавьте первую»
4. Lighthouse audit — цель Performance ≥ 80, Accessibility ≥ 90

**Критерии:**
- [ ] Tab-навигация по всем интерактивным элементам
- [ ] Нет горизонтального скролла на 320px
- [ ] Lighthouse Accessibility ≥ 90

### Ловушки
- `outline: none` без замены — ломает a11y
- Фиксированная sidebar на мобиле закрывает контент

---

## День 98 (Вс): Тестирование вручную и документация

### Теория
- Чеклист E2E вручную vs автотесты (Vitest — неделя 20)
- README: установка, env, скриншоты, архитектура
- [Conventional Commits](https://www.conventionalcommits.org/) для истории

### Практика
1. Пройди user flow: первый визит → настройки → задачи → погода → смена темы → F5
2. Напиши README с GIF или 3 скриншотами
3. `npm run build` — исправь warnings
4. Deploy preview на [Vercel](https://vercel.com/docs/frameworks/vite)

**Критерии:**
- [ ] Production build без ошибок
- [ ] README понятен новичку
- [ ] Preview URL в README

---

## Проект недели

**React Dashboard SPA** — итоговый deliverable недели:

Маршруты: `/` статистика, `/tasks` CRUD, `/weather` API, `/settings` тема и user. React Router, hooks, Context, адаптив, deploy preview.

**Критерии:**
- [ ] Все 4 страницы полностью функциональны
- [ ] Нет prop drilling глубже 2 уровней
- [ ] GitHub repo с понятной историей коммитов
- [ ] Vercel/Netlify preview работает

## Ревью-чеклист
- Могу объяснить архитектуру проекта за 2 минуты?
- Где хранится state задач и почему именно там?
- Как бы добавил авторизацию к этому Dashboard?
- Что произойдёт при истечении API-ключа OpenWeather?
- Какие 3 улучшения сделал бы в v2?
