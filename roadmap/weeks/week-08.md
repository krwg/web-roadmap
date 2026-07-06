# Неделя 8: Async JS — promises, event loop, HTTP, API patterns

> **Цель недели:** глубоко понять асинхронность в JavaScript, Promises, Event Loop и паттерны работы с API.
> **Литература:** Kyle Simpson «You Don't Know JS: Async & Performance», [learn.javascript.ru: Промисы](https://learn.javascript.ru/promise-basics), [MDN Event Loop](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop), [JavaScript.info: Event loop](https://javascript.info/event-loop), [Philip Roberts: What the heck is the event loop?](https://www.youtube.com/watch?v=8aGhZQkoFbQ)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md#неделя-8--movie-catalog)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-08/`

## День 1 (Mon): Асинхронность и Event Loop

### Теория
- [learn.javascript.ru: Введение: колбэки](https://learn.javascript.ru/intro) — проблема callback hell
- Call stack, Web APIs, callback queue, microtask queue
- `setTimeout(fn, 0)` — не «сразу», а «после текущего кода»
- [Loupe](http://latentflip.com/loupe/) — визуализация Event Loop
- Синхронный vs асинхронный код — порядок вывода
- Main thread один — долгий синхронный код замораживает UI
- Microtasks (Promise.then) выполняются перед macrotasks (setTimeout)
- Web APIs (timer, fetch) выполняются вне main thread, колбэки возвращаются в очередь
- Понимание порядка вывода — основа отладки async-багов

### Практика
1. Предскажи порядок вывода 5 задач с `console.log`, `setTimeout`, `Promise.resolve().then`
2. Проверь в браузере, объясни через Event Loop
3. Нарисуй диаграмму выполнения в блокноте
4. Пройди 10+ примеров на [javascript.info/event-loop](https://javascript.info/event-loop)
5. Запиши правило: microtasks перед macrotasks
6. Добавь `queueMicrotask` в пример — сравни с `Promise.resolve().then`
7. Сохрани конспект Event Loop в `week-08/notes.md`

**Критерии:**
- [ ] Могу предсказать порядок вывода в 4 из 5 примеров
- [ ] Понимаю разницу microtask и macrotask
- [ ] Есть конспект Event Loop своими словами

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 08 day 1: event loop basics"`

### Ловушки
- Думать, что `setTimeout(0)` выполняется мгновенно
- Блокировка main thread тяжёлыми вычислениями — UI замрёт
- Бесконечная рекурсия Promise.then — microtask starvation

## День 2 (Tue): Promises — основы

### Теория
- [learn.javascript.ru: Промисы](https://learn.javascript.ru/promise-basics)
- Состояния: pending → fulfilled / rejected
- `new Promise((resolve, reject) => {})`, `.then`, `.catch`, `.finally`
- Возврат значения из `.then` — следующий then получает его
- Promise chaining vs nested callbacks
- Promise — объект-обёртка над будущим значением; состояние меняется один раз
- `.then` возвращает новый Promise — цепочки без вложенности
- `.catch` ловит reject в цепочке — один catch на всю цепочку
- `.finally` выполняется всегда — cleanup (скрыть loader)

### Практика
1. Оберни `setTimeout` в функцию `delay(ms)` → Promise
2. Цепочка: delay(1000) → «Шаг 1» → delay(500) → «Шаг 2»
3. `fetch` перепиши на `.then` без async/await
4. Обработай reject: fetch несуществующего URL + catch
5. `Promise.all` — загрузи posts и users параллельно
6. Добавь `.finally` для сброса loading state
7. Верни значение из `.then` и прочитай его в следующем `.then`

**Критерии:**
- [ ] Цепочка then без callback hell
- [ ] Ошибки ловятся в catch
- [ ] Promise.all для параллельных запросов

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 08 day 2: promises chaining"`

## День 3 (Wed): async/await

### Теория
- [learn.javascript.ru: Async/await](https://learn.javascript.ru/async-await)
- `async function` всегда возвращает Promise
- `await` приостанавливает только async-функцию, не main thread
- try/catch вместо `.catch` для async/await
- Параллельность: `await Promise.all([a, b])` vs последовательный await
- `await` — синтаксический сахар над Promise; читается как синхронный код
- Последовательный await в цикле медленный — собери Promise.all для параллели
- async-функция без await всё равно возвращает Promise
- Top-level await доступен в ES modules — не нужен IIFE

### Практика
1. Рефакторинг fetch-функций на async/await
2. Функция `loadUserWithPosts(userId)` — user, затем его posts
3. Параллельная загрузка 3 endpoints через `Promise.all` + await
4. try/catch с понятным сообщением для пользователя
5. Async IIFE для top-level await в модуле
6. Сравни время: последовательный vs параллельный await (console.time)
7. Оберни api-слой недели 7 в async/await

**Критерии:**
- [ ] Весь API-слой на async/await
- [ ] Параллельные запросы не последовательные без причины
- [ ] try/catch на каждом публичном API-вызове

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 08 day 3: async await refactor"`

## День 4 (Thu): HTTP углублённо

### Теория
- [MDN: HTTP Overview](https://developer.mozilla.org/ru/docs/Web/HTTP/Overview)
- Методы: GET, POST, PUT, PATCH, DELETE — идемпотентность
- Статусы: 1xx–5xx; 200 OK, 201 Created, 204 No Content, 401, 403, 404, 500
- Заголовки: Content-Type, Authorization, Cache-Control, ETag
- [MDN: CORS](https://developer.mozilla.org/ru/docs/Web/HTTP/CORS) — preflight OPTIONS
- GET идемпотентен и кэшируем; POST создаёт ресурс — разные семантики
- 401 — не авторизован; 403 — нет прав; разные сообщения для UI
- CORS настраивает сервер (`Access-Control-Allow-Origin`), не клиент
- Preflight OPTIONS — браузер проверяет разрешение до «непростого» запроса

### Практика
1. В Network изучи headers реального запроса к API
2. Реализуй wrapper `api.get/post/put/delete` с базовым URL
3. Добавь заголовок `Content-Type: application/json` автоматически
4. Маппинг статусов в ошибки: `ApiError` с полем `status`
5. Обработай 401 — сообщение «Требуется авторизация»
6. Класс `ApiError extends Error` с `status` и `body`
7. Логируй failed requests в console с status и url

**Критерии:**
- [ ] API wrapper переиспользуемый
- [ ] Разные HTTP-ошибки — разные сообщения UI
- [ ] Понимаю CORS на уровне «почему fetch заблокирован»

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 08 day 4: http api wrapper"`

## День 5 (Fri): Паттерны работы с API

### Теория
- Pagination: offset/limit vs cursor
- Retry с exponential backoff
- Request deduplication — один запрос на один ключ
- Stale-while-revalidate: покажи кэш, обнови фоном
- [JSON:API](https://jsonapi.org/) / REST conventions — обзор
- Exponential backoff: 1s, 2s, 4s — не перегружай упавший сервер
- Race condition: старый ответ приходит после нового — AbortController или request id
- Cursor pagination стабильнее offset при частых вставках данных
- Skeleton UI резервирует место — меньше CLS при загрузке

### Практика
1. Пагинация постов: кнопка «Загрузить ещё» с cursor (id последнего)
2. Retry: 3 попытки с задержкой 1s, 2s, 4s при сетевой ошибке
3. In-memory cache Map: повторный запрос того же URL — из кэша
4. Skeleton UI на время загрузки, контент без layout shift
5. Отмена устаревшего ответа: race condition при быстром поиске
6. Реализуй `fetchWithRetry(url, options, maxRetries)`
7. Дедупликация: не запускай второй identical fetch, пока первый pending

**Критерии:**
- [ ] Retry реализован
- [ ] Нет race condition в поиске
- [ ] Pagination работает без дубликатов

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 08 day 5: api patterns retry pagination"`

## День 6 (Sat): Promise utilities

### Теория
- `Promise.all`, `Promise.allSettled`, `Promise.race`, `Promise.any`
- `Promise.allSettled` — когда нужны все результаты, даже с ошибками
- Promisify callback-based API (обзор)
- Async iterators `for await...of` — базовое знакомство
- Unhandled rejection — всегда catch
- `Promise.all` fail-fast — один reject роняет всё
- `Promise.allSettled` — дашборд из нескольких API, часть может упасть
- `Promise.race` — timeout wrapper: кто первый, тот и результат
- `unhandledrejection` в window — ловушка для забытых catch в production

### Практика
1. Загрузи 5 URL через `Promise.allSettled`, покажи успешные и failed
2. Timeout wrapper: `withTimeout(promise, 5000)` через `Promise.race`
3. Последовательная обработка массива URL без Promise.all (for await)
4. Глобальный `unhandledrejection` listener — логирование
5. Рефакторинг dashboard недели 7 с новыми паттернами
6. Сравни `Promise.all` vs `allSettled` на массиве с одним failed URL
7. Добавь timeout 10s на все fetch в api wrapper

**Критерии:**
- [ ] allSettled и race использованы по назначению
- [ ] Timeout на долгие запросы
- [ ] Нет unhandled promise rejections в Console

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 08 day 6: promise utilities timeout"`

## День 7 (Sun): Асинхронная архитектура

### Теория
- YDKJS: async generators, observables — обзор (не обязательно глубоко)
- State machine для loading/data/error/empty
- Separation: api layer не знает о DOM
- Тестирование async: моки fetch (обзор)
- Подготовка к TypeScript — типизация Promise<T>
- Явные состояния UI: idle | loading | success | error — нет «зависшего» экрана
- api layer возвращает данные или бросает ApiError — ui решает, как показать
- `createAsyncState` — простой pub/sub для реактивного UI без фреймворка
- Promise<T> в TypeScript (неделя 10) документирует, что вернёт async-функция

### Практика
1. Реализуй хук-подобный паттерн `createAsyncState()` — subscribe на изменения
2. UI автоматически реагирует на idle/loading/success/error
3. Интегрируй в проект «Каталог фильмов» (OMDb или TMDB free tier / mock)
4. Поиск + детали фильма + избранное в localStorage
5. Code review своего async-кода по чеклисту
6. Empty state: «Ничего не найдено» при пустом результате поиска
7. Тег `week-08-done` на финальном коммите

**Критерии:**
- [ ] Явные состояния async-операций в UI
- [ ] api / state / ui разделены
- [ ] Проект работает без ошибок в Console

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 08 day 7: movie catalog final"`

## Проект недели

**Каталог фильмов** — async SPA с поиском, деталями, избранным и robust error handling.

Подробное описание: [docs/projects.md — Неделя 8](../../docs/projects.md#неделя-8--movie-catalog)

API: OMDb ([omdbapi.com](http://www.omdbapi.com/)) или mock JSON server.

**Критерии проекта:**
- [ ] async/await + api wrapper + retry/timeout
- [ ] Состояния loading/error/empty/data
- [ ] Promise.all для параллельной загрузки деталей
- [ ] Избранное в localStorage, синхронизация с UI
- [ ] Папка `week-08/` с README и скриншотом
- [ ] Поиск по названию с debounce и отменой устаревших запросов
- [ ] Карточка фильма: постер, год, рейтинг, описание
- [ ] Избранное: add/remove, persist, отдельная вкладка или секция
- [ ] Тег `week-08-done` на финальном коммите

## Ревью-чеклист
- Объясни Event Loop на примере setTimeout + Promise?
- Разница Promise.all и Promise.allSettled?
- Когда await блокирует UI, а когда нет?
- Что такое CORS и кто его настраивает?
- Как отменить fetch-запрос?
