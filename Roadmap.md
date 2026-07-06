# 🗺️ Детализированный роадмап (архив: 55 дней × 6-7 часов)

> **⚠️ Актуальная версия:** [22 недели / 154 дня](roadmap/README.md) в папке `roadmap/weeks/`.  
> Этот файл сохранён как архив первой итерации (8 недель). Используйте [week-01.md](roadmap/weeks/week-01.md) для обучения.

> **Стек:** HTML → CSS → JavaScript → React → Python → SQL/PostgreSQL → Node.js → Full-Stack

> **Легенда:**
> - 📖 **Теория** — что читать/смотреть
> - 🛠 **ТЗ** — пошаговое задание с критериями готовности
> - 🪤 **Ловушки** — типичные ошибки
> - 🔍 **Ревью-чеклист** — самопроверка после выполнения
> - 🔗 **Ресурсы** — ссылки

---

## 🎯 Введение

Это **55-дневный** путь от полного нуля до junior full-stack разработчика. Рассчитан на 6-7 часов в день.

**Принцип прогрессии:** сначала простое и наглядное (HTML → CSS → JS), потом сложное (асинхронность, React, бэкенд, БД). Не прыгаем сразу в BFC и drag-and-drop — сначала строим фундамент.

**Цель:** перестать быть «вайбкодером» и стать инженером, который понимает *почему* код работает именно так, и может переписать его без ИИ.

**Главный враг — иллюзия компетентности.** Туториал посмотрел — кажется, всё понятно. Мы ломаем эту иллюзию практикой.

---

## 🗓️ Карта роадмапа (обзор)

| Неделя | Дни | Тема |
|--------|-----|------|
| 1 | 1–7 | HTML + CSS с нуля |
| 2 | 8–14 | JavaScript основы + DOM |
| 3 | 15–21 | JavaScript продвинутый |
| 4 | 22–28 | React |
| 5 | 29–35 | Python основы |
| 6 | 36–42 | SQL, PostgreSQL, FastAPI |
| 7 | 43–49 | Node.js + Express |
| 8 | 50–55 | Full-Stack, Docker, деплой |

---

## 🧬 Ежедневный распорядок (6-7 часов)

Pomodoro: 50 мин работа / 10 мин отдых.

1. **Блок 1 (1.5 ч): Теория.** Читаешь документацию, конспектируешь *своими словами*.
2. **Блок 2 (2.5 ч): Практика (ТЗ).** Пишешь код. Без ИИ. Застрял на 30 мин — прогулка.
3. **Блок 3 (1 ч): Ревью и дебаг.** Разбираешь ошибки. ИИ только для ревью: *"Найди проблемы в моём коде. Не переписывай — укажи на ошибки"*.
4. **Блок 4 (1 ч): Reverse Engineering.** Разбираешь чужой код с GitHub построчно.

---

## 🧠 Протокол «Анти-Вайбкодер»

ИИ **не пишет код за тебя**. Только:

1. **Объясни как для 5 лет:** *"Объясни Event Loop через аналогию с рестораном. Без кода"*.
2. **Ревью:** *"Оцени мой код по читаемости, производительности, безопасности. Укажи строки"*.
3. **Слепые зоны:** *"Какие edge cases я не учёл?"*
4. **Рефакторинг:** *"Перепиши этот кусок через [паттерн] и объясни почему"*.

---

## 🩸 Как не бросить

1. **Правило «Тупого часа»:** не понял тему — не иди дальше. Сиди, рисуй схемы, пиши микро-примеры.
2. **Правило 20 минут:** ошибка не решается 20 мин — прогулка.
3. **Коммит каждый день:** `git commit -m "day 4: flexbox layout"`.
4. **Дневник багов:** Симптом → Причина → Решение.
5. **Не копипасть:** повторяй код руками, меняй переменные.
6. **Читай ошибки** в консоли — они говорят, где и что сломалось.

---

## 🛠 Инструменты (День 1)

1. **VS Code** + расширение **Live Server**
2. **Google Chrome** + DevTools (F12)
3. **Git** + аккаунт на GitHub
4. **Node.js** (LTS) — понадобится с недели 4
5. **Python** (галочка *Add to PATH*)
6. **Docker Desktop** — установить к неделе 6

---

## 🟢 НЕДЕЛЯ 1: HTML + CSS с нуля

*Цель: понять, из чего состоит веб-страница и как её стилизовать. Без JS, без фреймворков.*

**Литература:** Ионетт Дакетт «HTML и CSS» (главы 1–12), [MDN Learn](https://developer.mozilla.org/ru/docs/Learn)

---

### День 1: HTML — структура страницы

#### 📖 Теория

**1. Что такое HTML**
- [MDN: Introduction to HTML](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML)
- HTML — это **структура**, не дизайн. Браузер читает теги и строит DOM-дерево.

**2. Базовые теги**
- `html`, `head`, `body`, `title`, `meta charset`
- `h1`–`h6`, `p`, `a`, `img`, `ul/ol/li`, `div`, `span`
- Атрибуты: `href`, `src`, `alt`, `id`, `class`

**3. Семантика**
- [MDN: Semantic HTML](https://developer.mozilla.org/en-US/docs/Glossary/Semantics)
- `header`, `nav`, `main`, `section`, `article`, `footer` — зачем они нужны

#### 🛠 ТЗ: Страница «Обо мне»

1. Создай `index.html` с правильной структурой `<!DOCTYPE html>`
2. Секции: шапка с именем, навигация (3 ссылки-якоря), блок «О себе», «Навыки» (список), «Контакты»
3. Добавь изображение с `alt`-текстом
4. Ссылка на внешний ресурс (`target="_blank"`)
5. Открой через Live Server, проверь в DevTools → Elements

**Критерии:**
- [ ] Валидный HTML (проверь на [validator.w3.org](https://validator.w3.org/))
- [ ] Использованы семантические теги, не только `div`
- [ ] У каждого `img` есть `alt`

#### 🪤 Ловушки
- Забыл `<!DOCTYPE html>` — браузер включает «quirks mode»
- `h1` используешь для размера текста — это заголовок, размер через CSS
- Вложенность нарушена: `<p><div>...</div></p>` — невалидно

---

### День 2: HTML — формы, таблицы, доступность

#### 📖 Теория

**1. Формы**
- [MDN: Forms](https://developer.mozilla.org/en-US/docs/Learn/Forms)
- `form`, `input` (text, email, password, checkbox, radio), `textarea`, `select`, `button`, `label`
- Атрибут `for` у `label` связывает его с `input`

**2. Таблицы**
- `table`, `thead`, `tbody`, `tr`, `th`, `td` — только для табличных *данных*, не для вёрстки

**3. Accessibility (a11y)**
- [MDN: Accessibility](https://developer.mozilla.org/en-US/docs/Learn/Accessibility)
- `aria-label`, tabindex, контраст, клавиатурная навигация

#### 🛠 ТЗ: Форма регистрации

1. Форма: имя, email, пароль, выбор роли (radio), согласие (checkbox)
2. Таблица: расписание занятий (3+ строк)
3. К каждому полю — `<label>`
4. Кнопка отправки (пока без JS — `type="submit"`)

**Критерии:**
- [ ] Tab-навигация работает по всем полям
- [ ] У `input` указаны `type` и `name`
- [ ] Таблица имеет `<thead>` с заголовками

---

### Дни 3–4: CSS основы

#### 📖 Теория

**1. Как подключить CSS**
- `<link rel="stylesheet" href="style.css">`, inline vs external

**2. Селекторы**
- Элемент, класс `.`, id `#`, потомки, `:hover`, `:focus`

**3. Box Model**
- [MDN: Box Model](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/The_box_model)
- `content → padding → border → margin`
- **`box-sizing: border-box`** — поставь глобально с первого дня!

**4. Цвета, шрифты, единицы**
- `rem` для текста, `%`/`vw` для ширины
- Google Fonts, `font-family`, `line-height`

#### 🛠 ТЗ: Стилизованная страница «Обо мне»

1. ~~Подключи CSS к HTML из Дня 1~~
2. ~~CSS-переменные для цветов в `:root`~~
3. ~~Сброс: `* { box-sizing: border-box; margin: 0; }`~~
4. ~~Типографика: один шрифт для текста, другой для заголовков~~
5. ~~Ссылки: underline убрать, `:hover` — смена цвета~~
6. ~~Карточки навыков с `border`, `border-radius`, `padding`~~

**Критерии:**
- [x] Нет inline-стилей в HTML
- [x] Все размеры текста в `rem`
- [x] Страница читаема на 320px ширины

#### 🪤 Ловушки
- `width: 100%` + padding ломает layout → `box-sizing: border-box`
- Специфичность: `#id` побеждает `.class` — не злоупотребляй id для стилей

---

### Дни 5–6: Flexbox и Grid

#### 📖 Теория

**1. Flexbox**
- [Flexbox Froggy](https://flexboxfroggy.com/) — пройди все уровни
- `display: flex`, `justify-content`, `align-items`, `gap`, `flex-wrap`

**2. Grid**
- [Grid Garden](https://cssgridgarden.com/) — пройди все уровни
- `grid-template-columns`, `gap`, `grid-area`

**3. Адаптивность**
- [MDN: Media queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries)
- Mobile-first: базовые стили для мобилы, `@media (min-width: 768px)` для десктопа

#### 🛠 ТЗ: Адаптивная галерея

1. Grid: `repeat(auto-fill, minmax(250px, 1fr))`
2. Карточки с изображением (placeholder через [picsum.photos](https://picsum.photos/300/200)) и подписью
3. Шапка на Flexbox: логотип слева, навигация справа
4. На мобиле (<768px): одна колонка, навигация под логотипом

**Критерии:**
- [ ] На 320px всё в одну колонку, ничего не обрезается
- [ ] Flexbox и Grid использованы по назначению (не Grid для одной строки кнопок)

---

### День 7: 🏆 Проект недели — Личный лендинг

#### 🛠 ТЗ

Собери всё в один сайт из 3+ секций:

1. **Hero** — имя, должность, CTA-кнопка
2. **Проекты** — 3 карточки (Grid)
3. **Контакты** — форма из Дня 2
4. Плавный скролл к секциям (`scroll-behavior: smooth` или якоря)
5. `:focus-visible` на интерактивных элементах

**Критерии:**
- [ ] Адаптив: мобила + десктоп
- [ ] Семантический HTML + отдельный CSS-файл
- [ ] Залито на GitHub

#### 🔍 Ревью-чеклист
- Могу объяснить разницу `block`, `inline`, `inline-block`?
- Знаю, когда Flexbox, а когда Grid?
- Понимаю Box Model?

---

## 🟡 НЕДЕЛЯ 2: JavaScript основы + DOM

*Цель: научиться программировать на JS и оживлять страницы.*

**Литература:** [learn.javascript.ru](https://learn.javascript.ru/) (разделы 1–5), [JavaScript.info](https://javascript.info/)

---

### День 8: Переменные, типы, операторы

#### 📖 Теория

**1. Переменные:** `let`, `const`, `var` (и почему `var` — legacy)
**2. Типы:** string, number, boolean, null, undefined, object
**3. Операторы:** `===` vs `==`, `&&`, `||`, `??`
**4. Строки и числа:** template literals `` `${name}` ``, `parseInt`, `toFixed`

#### 🛠 ТЗ: Калькулятор чаевых (консоль)

Напиши функции (пока без DOM):
```javascript
function calculateTip(bill, tipPercent) { /* ... */ }
function splitBill(bill, tipPercent, people) { /* ... */ }
```
Протестируй: `splitBill(1000, 15, 4)` → `{ total: 1150, perPerson: 287.5 }`

**Критерии:**
- [ ] Используешь `const`/`let`, не `var`
- [ ] Строгое сравнение `===`
- [ ] Обработка edge cases: 0 людей, отрицательный bill

---

### День 9: Функции, массивы, объекты

#### 📖 Теория

**1. Функции:** declaration, expression, arrow functions
**2. Массивы:** `push`, `pop`, `map`, `filter`, `reduce`, `find`
**3. Объекты:** создание, доступ к свойствам, деструктуризация
**4. Spread/rest:** `...arr`, `...obj`

#### 🛠 ТЗ: Менеджер закладок (данные в памяти)

```javascript
const bookmarks = [];

function addBookmark(title, url) { /* ... */ }
function removeBookmark(id) { /* ... */ }
function searchBookmarks(query) { /* filter по title */ }
function getBookmarksByTag(tag) { /* ... */ }
```

**Критерии:**
- [ ] `map`/`filter`/`find` использованы, не циклы for где можно без них
- [ ] Каждая закладка имеет уникальный `id`

---

### День 10: Условия, циклы, отладка

#### 📖 Теория

**1.** `if/else`, `switch`, тернарный оператор
**2.** `for`, `for...of`, `while` — когда что
**3.** DevTools → Console, breakpoints, `console.log` vs `debugger`

#### 🛠 ТЗ: FizzBuzz + валидация формы (логика)

1. FizzBuzz 1–100 (вывод в консоль)
2. Функция `validateEmail(email)` → `{ valid: bool, error: string }`
3. Функция `validatePassword(pw)` → минимум 8 символов, 1 цифра, 1 буква

---

### Дни 11–12: DOM — первые шаги

#### 📖 Теория

**1. DOM Tree:** [MDN: Introduction to the DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)
**2. Поиск элементов:** `querySelector`, `querySelectorAll`, `getElementById`
**3. Изменение:** `textContent`, `innerHTML` (осторожно!), `classList`, `style`
**4. События:** `addEventListener`, `click`, `input`, `submit`, `keydown`
**5. Event bubbling:** [MDN: Event bubbling](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events)

#### 🛠 ТЗ: Интерактивный счётчик + переключатель темы

1. Кнопки `+` / `-` / `Reset` меняют число на странице
2. Toggle тёмной темы через класс на `<body>` (CSS уже готов)
3. Счётчик не уходит ниже 0

**Критерии:**
- [ ] JS в отдельном файле, подключён в конце `<body>`
- [ ] Нет inline `onclick` в HTML
- [ ] `textContent`, не `innerHTML` для текста

#### 🪤 Ловушки
- `getElementById` в цикле на каждый кадр — кэшируй ссылки на элементы
- `innerHTML` с пользовательским вводом — XSS-уязвимость

---

### День 13: localStorage и Fetch (введение)

#### 📖 Теория

**1. localStorage:** `setItem`, `getItem`, `JSON.stringify/parse`
**2. Fetch:** [MDN: Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
**3. async/await** — базовое знакомство (глубже на неделе 3)

#### 🛠 ТЗ: Список задач с сохранением

1. Добавление/удаление задач через DOM
2. Сохранение массива задач в `localStorage`
3. При загрузке страницы — восстановление из `localStorage`
4. Бонус: загрузи случайную цитату с [api.quotable.io](https://api.quotable.io/random)

---

### День 14: 🏆 Проект недели — Todo App (Vanilla JS)

#### 🛠 ТЗ

Полноценное приложение:

1. Добавить задачу (Enter или кнопка)
2. Отметить выполненной (checkbox, зачёркивание)
3. Удалить задачу
4. Фильтры: All / Active / Completed
5. Счётчик оставшихся задач
6. Persist через `localStorage`

**Критерии:**
- [ ] Работает без перезагрузки (SPA-feel на одной странице)
- [ ] Данные переживают F5
- [ ] Чистый HTML/CSS/JS, без библиотек

---

## 🔵 НЕДЕЛЯ 3: JavaScript продвинутый

*Цель: понять «магию» JS — замыкания, асинхронность, работа с API.*

**Литература:** Кайл Симпсон «You Don't Know JS» (Scope & Closures, Async & Performance)

---

### День 15: Замыкания и `this`

#### 📖 Теория

**1. Closures:** [MDN: Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)
**2. `this`:** 4 правила + стрелочные функции
**3.** Реализуй свой `.bind()`

#### 🛠 ТЗ

1. `createCounter()` с приватным `count` через замыкание
2. `myBind(fn, context, ...args)` — своя версия bind
3. Модуль настроек: `createSettings(defaults)` → `get/set/reset`

**Критерии:**
- [ ] `count` недоступен снаружи
- [ ] Могу объяснить, почему `setTimeout(obj.method)` теряет `this`

---

### День 16: Прототипы и классы

#### 📖 Теория

**1.** Prototype chain: `__proto__` vs `prototype`
**2.** ES6 classes — синтаксический сахар
**3.** `extends`, `super`, `instanceof`

#### 🛠 ТЗ: Система заклинаний (ООП)

Классы `Spell`, `Fireball extends Spell`, `Heal extends Spell`, `Mage` — как в оригинальном роадмапе.

**Критерии:**
- [ ] Наследование работает
- [ ] `Heal.cast()` лечит, а не наносит урон
- [ ] Ошибки: мало маны, заклинание не выучено

---

### Дни 17–18: Асинхронность и Event Loop

#### 📖 Теория

**1.** Видео: [Jake Archibald: In The Loop](https://www.youtube.com/watch?v=cCOL7MC4Pl0) — **обязательно**
**2.** Promises, `async/await`
**3.** Микротаски vs макротаски: [Jake Archibald: Tasks, microtasks](https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules/)

#### 🛠 ТЗ

1. Свой `promiseAll()`
2. Асинхронный загрузчик с прогресс-баром и `AbortController`
3. Задачки на порядок вывода:
```javascript
console.log('1');
setTimeout(() => console.log('2'), 0);
Promise.resolve().then(() => console.log('3'));
console.log('4');
// Предскажи порядок ДО запуска
```

---

### День 19: Продвинутый CSS + производительность

#### 📖 Теория

**1.** BFC, margin collapse — теперь, когда CSS-база есть
**2.** `z-index` и stacking context
**3.** Reflow/Repaint, `requestAnimationFrame`
**4.** Debounce/Throttle, Intersection Observer

#### 🛠 ТЗ: Бесконечный скролл галереи

Grid + Intersection Observer + lazy loading + DocumentFragment — как в оригинале, но HTML/CSS уже знаешь.

---

### День 20: HTTP, API, кэширование

#### 📖 Теория

**1.** HTTP методы, статус-коды
**2.** CORS — что это и зачем
**3.** localStorage vs sessionStorage vs cookies

#### 🛠 ТЗ: Погодный дашборд

OpenWeatherMap API + кэш на 10 минут + обработка ошибок + спиннер.

---

### День 21: 🏆 Проект недели — Markdown-редактор

Split-view: Markdown слева → HTML справа. Regex-парсер, debounce автосохранения, localStorage.

**Критерии:**
- [ ] Заголовки, bold, italic, code, списки
- [ ] Нет лагов при быстром вводе
- [ ] Черновик восстанавливается после F5

---

## 🟣 НЕДЕЛЯ 4: React

*Цель: освоить современный фронтенд-фреймворк. Vanilla JS ты уже знаешь — React станет логичным следующим шагом.*

**Литература:** [React Docs (react.dev)](https://react.dev/learn), [React — русскоязычная документация](https://ru.react.dev/)

---

### День 22: Введение в React

#### 📖 Теория

**1.** Зачем React: компоненты, декларативный UI, Virtual DOM
**2.** Vite + React: `npm create vite@latest my-app -- --template react`
**3.** JSX: `{}`, `className`, `{condition && <El/>}`, `{items.map(...)}`
**4.** Структура проекта: `main.jsx`, `App.jsx`, компоненты в `/components`

#### 🛠 ТЗ: Карточки профиля

1. Компонент `ProfileCard({ name, role, avatar, skills })`
2. Рендер массива карточек из массива данных
3. Props validation (PropTypes или TypeScript — опционально)

**Критерии:**
- [ ] Каждый компонент в отдельном файле
- [ ] `key` при рендере списка
- [ ] Проект запускается через `npm run dev`

---

### День 23: State и события

#### 📖 Теория

**1.** `useState` — [React: State](https://react.dev/learn/state-a-components-memory)
**2.** Обработка событий: `onClick`, `onChange`, `onSubmit`
**3.** Controlled components: input value привязан к state
**4.** Immutability: `[...arr, newItem]`, `{...obj, field: value}`

#### 🛠 ТЗ: Todo App на React

Перепиши Todo из Дня 14 на React. Тот же функционал, но через `useState`.

---

### День 24: useEffect и работа с API

#### 📖 Теория

**1.** `useEffect(fn, [deps])` — side effects
**2.** Fetch в useEffect, cleanup function
**3.** Loading/error/data паттерн

#### 🛠 ТЗ: Список постов

1. Загрузка с [JSONPlaceholder](https://jsonplaceholder.typicode.com/posts)
2. States: loading, error, posts
3. Skeleton/spinner пока грузится

---

### День 25: Формы и подъём state

#### 📖 Теория

**1.** Lifting state up
**2.** Формы: controlled inputs, `e.preventDefault()`
**3.** Передача callbacks через props

#### 🛠 ТЗ: Фильтруемый список

Родитель хранит filter + items, ребёнок `SearchBar` сообщает об изменении фильтра, `ItemList` рендерит отфильтрованное.

---

### День 26: React Router

#### 📖 Теория

**1.** `npm install react-router-dom`
**2.** `BrowserRouter`, `Routes`, `Route`, `Link`, `useParams`, `useNavigate`
**3.** Layout routes, nested routes

#### 🛠 ТЗ: Многостраничный сайт

Страницы: Home, About, Projects, Contact. Навигация через `<Link>`. Страница Project Detail с `:id` из URL.

---

### День 27: Custom Hooks и Context

#### 📖 Теория

**1.** Custom hook: `useLocalStorage`, `useFetch`
**2.** Context API: `createContext`, `useContext` — для темы или auth
**3.** Когда Context, когда props

#### 🛠 ТЗ

1. Hook `useLocalStorage(key, initialValue)`
2. `ThemeContext` — переключатель тёмной темы для всего приложения

---

### День 28: 🏆 Проект недели — React Dashboard

#### 🛠 ТЗ

Приложение с роутингом:

1. **/** — дашборд с карточками статистики
2. **/tasks** — CRUD задач (localStorage через custom hook)
3. **/weather** — погода по городу (OpenWeatherMap API)
4. **/settings** — тема, имя пользователя
5. Адаптивная вёрстка, loading states, обработка ошибок

**Критерии:**
- [ ] React Router, минимум 4 страницы
- [ ] Custom hook + Context
- [ ] Нет «prop drilling» глубже 2 уровней

---

## 🟤 НЕДЕЛЯ 5: Python основы

*Цель: второй язык — бэкенд, скрипты, автоматизация.*

**Литература:** «Python. Ускоренный курс» (Теллез), [docs.python.org tutorial](https://docs.python.org/3/tutorial/)

---

### День 29: Синтаксис Python

#### 📖 Теория

**1.** Установка, `python --version`, venv: `python -m venv venv`
**2.** Переменные, типы, f-strings, `input()`
**3.** `if/elif/else`, `for`, `while`, `range()`
**4.** Функции, `*args`, `**kwargs`, type hints (базово)

#### 🛠 ТЗ: Калькулятор и конвертер

CLI-скрипт: меню (арифметика, °C↔°F, валюта), цикл до `exit`.

---

### День 30: Структуры данных

#### 📖 Теория

**1.** list, tuple, dict, set — когда что
**2.** List/dict comprehensions
**3.** `enumerate`, `zip`, `sorted(key=...)`

#### 🛠 ТЗ: Анализ текста

Функции: `word_count(text)`, `top_n_words(text, n)`, `unique_words(text)`.

---

### День 31: ООП в Python

#### 📖 Теория

**1.** `class`, `__init__`, `self`
**2.** Наследование, `super()`
**3.** `@property`, `@staticmethod`, `@classmethod`

#### 🛠 ТЗ: Библиотека книг

Классы `Book`, `Library` — add/remove/search/list_by_author.

---

### День 32: Алгоритмы и Big O

#### 📖 Теория

**1.** «Грокаем алгоритмы» — глава 1
**2.** O(1), O(n), O(n²), O(log n)
**3.** [Python Time Complexity](https://wiki.python.org/moin/TimeComplexity)

#### 🛠 ТЗ: Two Sum

Brute O(n²) vs hash map O(n) + замер через `timeit`.

---

### День 33: Магические методы и декораторы

#### 📖 Теория

**1.** `__str__`, `__repr__`, `__eq__`, `__len__`, `__getitem__`
**2.** Декораторы — [Real Python: Decorators](https://realpython.com/primer-on-python-decorators/)
**3.** Singleton (понимание паттерна)

#### 🛠 ТЗ: Класс `Stack` с dunder methods

`push`, `pop`, `peek`, `__len__`, `__str__`, `__bool__`.

---

### День 34: Файлы, pathlib, regex

#### 📖 Теория

**1.** `pathlib.Path` — современный путь к файлам
**2.** `re.match`, `re.search`, `re.findall`, `re.sub`
**3.** Чтение больших файлов построчно

#### 🛠 ТЗ: Анализатор логов

Парсинг 100k строк, группировка ERROR по дате, топ-5 дней.

---

### День 35: 🏆 Проект недели — CLI Task Manager (SQLite)

#### 🛠 ТЗ

CRUD задач в SQLite + красивый вывод через `rich`:

1. `pip install rich`
2. Таблица `tasks(id, title, description, status, created_at)`
3. Меню: add / list / complete / delete / exit
4. Транзакции с `try/except` + `rollback`

**Критерии:**
- [ ] Все CRUD-операции
- [ ] Таблица через `rich.table`
- [ ] Параметризованные SQL-запросы (`?` placeholders)

---

## 🔴 НЕДЕЛЯ 6: SQL, PostgreSQL, FastAPI

*Цель: реляционные БД и REST API на Python.*

---

### День 36: SQL основы

#### 📖 Теория

**1.** [SQLBolt](https://sqlbolt.com/) или [W3Schools SQL](https://www.w3schools.com/sql/) — пройди основы
**2.** SELECT, WHERE, ORDER BY, LIMIT
**3.** INSERT, UPDATE, DELETE
**4.** JOIN: INNER, LEFT — one-to-many
**5.** PRIMARY KEY, FOREIGN KEY, INDEX

#### 🛠 ТЗ: База «Библиотека»

Схема: `authors`, `books`, `borrowers`, `loans`. Напиши 10+ запросов:
- Все книги автора
- Кто не вернул книгу
- Топ-5 авторов по количеству книг

Используй SQLite через [DB Browser for SQLite](https://sqlitebrowser.org/) или `sqlite3` CLI.

---

### День 37: SQLite из Python (углубление)

#### 📖 Теория

**1.** `sqlite3` module: connection, cursor, commit
**2.** Context manager: `with conn:`
**3.** Migrations вручную (ALTER TABLE)

#### 🛠 ТЗ: Расширь Task Manager

Добавь: теги (many-to-many), поиск, фильтр по статусу, экспорт в CSV.

---

### День 38: PostgreSQL

#### 📖 Теория

**1.** PostgreSQL vs SQLite — когда что
**2.** Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=pass postgres:15`
**3.** psql / pgAdmin / DBeaver — подключение
**4.** Типы: SERIAL, VARCHAR, TEXT, TIMESTAMP, JSONB

#### 🛠 ТЗ

1. Перенеси схему «Библиотека» в PostgreSQL
2. Создай индекс на `books.title`
3. EXPLAIN ANALYZE на поиск по title — с индексом и без

---

### День 39: SQLAlchemy ORM

#### 📖 Теория

**1.** [SQLAlchemy ORM Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
**2.** Models, Session, relationships
**3.** `relationship()`, `back_populates`

#### 🛠 ТЗ: ORM-модели

```python
class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("Book", back_populates="author")
```

CRUD через ORM: create author + books, query with join.

---

### День 40: FastAPI — первый API

#### 📖 Теория

**1.** [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
**2.** Pydantic models, path/query parameters
**3.** Auto Swagger на `/docs`

#### 🛠 ТЗ: API заметок (in-memory)

`POST /notes`, `GET /notes`, `GET /notes/{id}`, `DELETE /notes/{id}` — Pydantic validation.

---

### Дни 41–42: 🏆 FastAPI + PostgreSQL

#### 🛠 ТЗ: REST API «Библиотека»

1. SQLAlchemy + PostgreSQL
2. Эндпоинты: authors CRUD, books CRUD, loans
3. Dependency injection: `get_db()` session
4. Обработка 404, 422
5. Seed script — начальные данные

**Критерии:**
- [ ] Swagger документация актуальна
- [ ] Данные в PostgreSQL, не in-memory
- [ ] Foreign keys работают

---

## 🟠 НЕДЕЛЯ 7: Node.js + Express

*Цель: бэкенд на JavaScript — тот же язык, другая среда.*

**Литература:** [Node.js Docs](https://nodejs.org/en/docs), [Express Guide](https://expressjs.com/en/guide/routing.html)

---

### День 43: Node.js основы

#### 📖 Теория

**1.** Node vs Browser JS: нет DOM, есть `global`, `process`
**2.** CommonJS vs ES Modules (`"type": "module"` в package.json)
**3.** npm, package.json, node_modules
**4.** Встроенные модули: `fs`, `path`, `http`

#### 🛠 ТЗ

1. CLI: `node scripts/greet.js --name=Alex`
2. Чтение/запись JSON-файла (база «заметок»)
3. `path.join`, `__dirname` / `import.meta.url`

---

### День 44: Асинхронность в Node

#### 📖 Теория

**1.** Callback → Promise → async/await в Node
**2.** `fs.promises.readFile`, `fs.promises.writeFile`
**3.** EventEmitter basics

#### 🛠 ТЗ: File watcher

Скрипт следит за изменением файла (`fs.watch`) и логирует изменения.

---

### День 45: Express — REST API

#### 📖 Теория

**1.** `npm init`, `npm install express`
**2.** Routes, `req.params`, `req.query`, `req.body`
**3.** Middleware chain
**4.** `express.json()` для парсинга body

#### 🛠 ТЗ: Express API заметок

```javascript
app.get('/api/notes', ...)
app.post('/api/notes', ...)
app.put('/api/notes/:id', ...)
app.delete('/api/notes/:id', ...)
```

Хранение в JSON-файле (потом заменим на БД).

---

### День 46: Middleware, валидация, ошибки

#### 📖 Теория

**1.** Custom middleware, `next()`
**2.** Error handling middleware (4 args)
**3.** `zod` или `express-validator` для валидации
**4.** HTTP status codes — правильное использование

#### 🛠 ТЗ

1. Middleware логирования запросов
2. Валидация body через zod
3. Centralized error handler

---

### День 47: Node.js + PostgreSQL

#### 📖 Теория

**1.** `pg` (node-postgres) или Prisma
**2.** Connection pool
**3.** Prepared statements (защита от SQL injection)

#### 🛠 ТЗ

Перепиши Express API на PostgreSQL:
```javascript
import pg from 'pg';
const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
```

---

### Дни 48–49: 🏆 Express API + Auth

#### 🛠 ТЗ: API с аутентификацией

1. `POST /auth/register`, `POST /auth/login`
2. JWT tokens (`jsonwebtoken` + `bcrypt`)
3. Protected routes: middleware проверки token
4. CRUD ресурса (tasks/notes) — только для авторизованного пользователя

**Критерии:**
- [ ] Пароли хешируются (bcrypt)
- [ ] JWT в header `Authorization: Bearer <token>`
- [ ] 401 без token, 403 при чужих данных

---

## ⚫ НЕДЕЛЯ 8: Full-Stack + DevOps

*Цель: связать React + Node/FastAPI + PostgreSQL, задеплоить.*

---

### День 50: Связка Frontend + Backend

#### 📖 Теория

**1.** CORS в Express: `cors` package
**2.** Environment variables: `.env`, `VITE_API_URL`
**3.** Proxy в Vite dev server (опционально)

#### 🛠 ТЗ

1. React-приложение (День 28) → fetch к Express API (День 49)
2. Login/register flow в React
3. Token в localStorage, автоматическая подстановка в headers
4. Protected routes в React (redirect на /login)

---

### День 51: Безопасность и шифрование

#### 📖 Теория

**1.** OWASP Top 10 (обзор)
**2.** SQL injection, XSS, CSRF — как защищаться
**3.** HTTPS, env secrets, `.env` в `.gitignore`
**4.** Rate limiting (`express-rate-limit`)

#### 🛠 ТЗ

1. Добавь rate limiting на `/auth/login`
2. Helmet.js для HTTP headers
3. Аудит: пройди чеклист OWASP для своего API

---

### День 52: Docker

#### 📖 Теория

**1.** [Docker Getting Started](https://docs.docker.com/get-started/)
**2.** Dockerfile, image, container, volume
**3.** docker-compose: multi-service

#### 🛠 ТЗ: docker-compose.yml

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: appdb
    volumes:
      - pgdata:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://user:password@db/appdb
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "5173:80"
    depends_on:
      - backend

volumes:
  pgdata:
```

**Критерии:**
- [ ] `docker-compose up --build` поднимает всё
- [ ] Данные PostgreSQL сохраняются в volume

---

### Дни 53–54: 🏆 ФИНАЛЬНЫЙ ПРОЕКТ

#### 🛠 ТЗ: Full-Stack приложение на выбор

**Вариант A: Task Manager Pro**
- React frontend (drag-and-drop задач, фильтры, теги)
- Express или FastAPI backend
- PostgreSQL
- Auth (register/login)
- Docker Compose

**Вариант B: Secret Notes**
- React UI для создания/чтения зашифрованных записок
- FastAPI + Fernet encryption + bcrypt
- PostgreSQL + SQLAlchemy
- Shareable links

**Обязательно для обоих:**
1. GitHub repo с README (архитектура, запуск, скриншоты)
2. `.env.example` — без секретов
3. docker-compose для локального запуска
4. Минимум 5 API endpoints
5. Error handling на фронте и бэке

---

### День 55: Деплой + финальное ревью

#### 🛠 ТЗ: Деплой

**Backend:**
- [Render](https://render.com/) или [Railway](https://railway.app/) — Docker deploy
- Managed PostgreSQL (Neon, Supabase, или Render Postgres)

**Frontend:**
- [Vercel](https://vercel.com/) или [Netlify](https://www.netlify.com/)
- `VITE_API_URL` → production backend URL
- CORS: добавь домен фронтенда в allow_origins

**Финальное ревью** — ответь письменно (Markdown-файл):

### HTML/CSS
- `block` vs `inline` vs `inline-block`?
- Box Model и `box-sizing: border-box`?
- Flexbox vs Grid — когда что?

### JavaScript
- Замыкание — пример?
- Event Loop: порядок sync → microtasks → macrotasks?
- `var` vs `let` vs `const`?

### React
- Зачем `key` в списках?
- `useState` vs `useEffect` — когда что?
- Controlled vs uncontrolled components?

### Python
- Big O: list vs dict lookup?
- 3 магических метода и зачем?
- venv — зачем?

### SQL/PostgreSQL
- INNER JOIN vs LEFT JOIN?
- Зачем индексы?
- SQL injection — как защититься?

### Node.js
- Node vs Browser — главные отличия?
- Middleware в Express — что это?
- Зачем connection pool?

### Full-Stack
- REST — что это?
- CORS — зачем?
- JWT vs session cookies?
- Docker — зачем?

**Если 80%+ ответов уверенные — ты больше не вайбкодер.**

---

## 📚 Библиотека ресурсов

### HTML/CSS
- [MDN Learn](https://developer.mozilla.org/ru/docs/Learn)
- [Flexbox Froggy](https://flexboxfroggy.com/) · [Grid Garden](https://cssgridgarden.com/)
- [CSS Tricks](https://css-tricks.com/)

### JavaScript
- [learn.javascript.ru](https://learn.javascript.ru/)
- [JavaScript.info](https://javascript.info/)
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS)

### React
- [react.dev](https://react.dev/learn)
- [React Router Docs](https://reactrouter.com/en/main)

### Python
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/ru/)

### SQL/PostgreSQL
- [SQLBolt](https://sqlbolt.com/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)

### Node.js
- [Node.js Docs](https://nodejs.org/en/docs)
- [Express.js Guide](https://expressjs.com/en/guide/routing.html)
- [npm Docs](https://docs.npmjs.com/)

### DevOps
- [Docker Docs](https://docs.docker.com/)
- [Draw.io](https://app.diagrams.net/) — диаграммы

### Алгоритмы
- «Грокаем алгоритмы» (Бхargava)
- [Big O Cheat Sheet](https://www.bigocheatsheet.com/)

---

## 🚀 Напутствие

55 дней — это марафон, не спринт. **Первые 2 недели — самые важные.** Если HTML/CSS/JS-бasics не на месте, React и бэкенд будут мучением.

Не пропускай проекты недель — они связывают теорию в навык.

**Код — это навык, не знание.** Пиши каждый день. Через 55 дней ты будешь смотреть на веб-приложения другими глазами: React-компонент, Express middleware, SQL-запрос — всё будет знакомо.

Поехали! 🚀
