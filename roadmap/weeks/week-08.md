# Неделя 8: Async JS — promises, event loop, HTTP, API patterns

> **Цель недели:** глубоко понять асинхронность в JavaScript, Promises, Event Loop и паттерны работы с API.
> **Литература:** Kyle Simpson «You Don't Know JS: Async & Performance», [learn.javascript.ru: Промисы](https://learn.javascript.ru/promise-basics), [MDN Event Loop](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop)

## День 1 (Mon): Асинхронность и Event Loop

### Теория
- [learn.javascript.ru: Введение: колбэки](https://learn.javascript.ru/intro) — проблема callback hell
- Call stack, Web APIs, callback queue, microtask queue
- `setTimeout(fn, 0)` — не «сразу», а «после текущего кода»
- [Loupe](http://latentflip.com/loupe/) — визуализация Event Loop
- Синхронный vs асинхронный код — порядок вывода

### Практика
1. Предскажи порядок вывода 5 задач с `console.log`, `setTimeout`, `Promise.resolve().then`
2. Проверь в браузере, объясни через Event Loop
3. Нарисуй диаграмму выполнения в блокноте
4. Пройди 10+ примеров на [javascript.info/event-loop](https://javascript.info/event-loop)
5. Запиши правило: microtasks перед macrotasks

**Критерии:**
- [ ] Могу предсказать порядок вывода в 4 из 5 примеров
- [ ] Понимаю разницу microtask и macrotask
- [ ] Есть конспект Event Loop своими словами

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

### Практика
1. Оберни `setTimeout` в функцию `delay(ms)` → Promise
2. Цепочка: delay(1000) → «Шаг 1» → delay(500) → «Шаг 2»
3. `fetch` перепиши на `.then` без async/await
4. Обработай reject: fetch несуществующего URL + catch
5. `Promise.all` — загрузи posts и users параллельно

**Критерии:**
- [ ] Цепочка then без callback hell
- [ ] Ошибки ловятся в catch
- [ ] Promise.all для параллельных запросов

## День 3 (Wed): async/await

### Теория
- [learn.javascript.ru: Async/await](https://learn.javascript.ru/async-await)
- `async function` всегда возвращает Promise
- `await` приостанавливает только async-функцию, не main thread
- try/catch вместо `.catch` для async/await
- Параллельность: `await Promise.all([a, b])` vs последовательный await

### Практика
1. Рефакторинг fetch-функций на async/await
2. Функция `loadUserWithPosts(userId)` — user, затем его posts
3. Параллельная загрузка 3 endpoints через `Promise.all` + await
4. try/catch с понятным сообщением для пользователя
5. Async IIFE для top-level await в модуле

**Критерии:**
- [ ] Весь API-слой на async/await
- [ ] Параллельные запросы не последовательные без причины
- [ ] try/catch на каждом публичном API-вызове

## День 4 (Thu): HTTP углублённо

### Теория
- [MDN: HTTP Overview](https://developer.mozilla.org/ru/docs/Web/HTTP/Overview)
- Методы: GET, POST, PUT, PATCH, DELETE — идемпотентность
- Статусы: 1xx–5xx; 200 OK, 201 Created, 204 No Content, 401, 403, 404, 500
- Заголовки: Content-Type, Authorization, Cache-Control, ETag
- [MDN: CORS](https://developer.mozilla.org/ru/docs/Web/HTTP/CORS) — preflight OPTIONS

### Практика
1. В Network изучи headers реального запроса к API
2. Реализуй wrapper `api.get/post/put/delete` с базовым URL
3. Добавь заголовок `Content-Type: application/json` автоматически
4. Маппинг статусов в ошибки: `ApiError` с полем `status`
5. Обработай 401 — сообщение «Требуется авторизация»

**Критерии:**
- [ ] API wrapper переиспользуемый
- [ ] Разные HTTP-ошибки — разные сообщения UI
- [ ] Понимаю CORS на уровне «почему fetch заблокирован»

## День 5 (Fri): Паттерны работы с API

### Теория
- Pagination: offset/limit vs cursor
- Retry с exponential backoff
- Request deduplication — один запрос на один ключ
- Stale-while-revalidate: покажи кэш, обнови фоном
- [JSON:API](https://jsonapi.org/) / REST conventions — обзор

### Практика
1. Пагинация постов: кнопка «Загрузить ещё» с cursor (id последнего)
2. Retry: 3 попытки с задержкой 1s, 2s, 4s при сетевой ошибке
3. In-memory cache Map: повторный запрос того же URL — из кэша
4. Skeleton UI на время загрузки, контент без layout shift
5. Отмена устаревшего ответа: race condition при быстром поиске

**Критерии:**
- [ ] Retry реализован
- [ ] Нет race condition в поиске
- [ ] Pagination работает без дубликатов

## День 6 (Sat): Promise utilities

### Теория
- `Promise.all`, `Promise.allSettled`, `Promise.race`, `Promise.any`
- `Promise.allSettled` — когда нужны все результаты, даже с ошибками
- Promisify callback-based API (обзор)
- Async iterators `for await...of` — базовое знакомство
- Unhandled rejection — всегда catch

### Практика
1. Загрузи 5 URL через `Promise.allSettled`, покажи успешные и failed
2. Timeout wrapper: `withTimeout(promise, 5000)` через `Promise.race`
3. Последовательная обработка массива URL без Promise.all (for await)
4. Глобальный `unhandledrejection` listener — логирование
5. Рефакторинг dashboard недели 7 с новыми паттернами

**Критерии:**
- [ ] allSettled и race использованы по назначению
- [ ] Timeout на долгие запросы
- [ ] Нет unhandled promise rejections в Console

## День 7 (Sun): Асинхронная архитектура

### Теория
- YDKJS: async generators, observables — обзор (не обязательно глубоко)
- State machine для loading/data/error/empty
- Separation: api layer не знает о DOM
- Тестирование async: моки fetch (обзор)
- Подготовка к TypeScript — типизация Promise<T>

### Практика
1. Реализуй хук-подобный паттерн `createAsyncState()` — subscribe на изменения
2. UI автоматически реагирует на idle/loading/success/error
3. Интегрируй в проект «Каталог фильмов» (OMDb или TMDB free tier / mock)
4. Поиск + детали фильма + избранное в localStorage
5. Code review своего async-кода по чеклисту

**Критерии:**
- [ ] Явные состояния async-операций в UI
- [ ] api / state / ui разделены
- [ ] Проект работает без ошибок в Console

## Проект недели

**Каталог фильмов** — async SPA с поиском, деталями, избранным и robust error handling.

API: OMDb ([omdbapi.com](http://www.omdbapi.com/)) или mock JSON server.

**Критерии проекта:**
- [ ] async/await + api wrapper + retry/timeout
- [ ] Состояния loading/error/empty/data
- [ ] Promise.all для параллельной загрузки деталей
- [ ] Избранное в localStorage, синхронизация с UI

## Ревью-чеклист
- Объясни Event Loop на примере setTimeout + Promise?
- Разница Promise.all и Promise.allSettled?
- Когда await блокирует UI, а когда нет?
- Что такое CORS и кто его настраивает?
- Как отменить fetch-запрос?
