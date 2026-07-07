# Неделя 8: Async JS — promises, event loop, HTTP, API patterns

> **Цель недели:** глубоко понять асинхронность в JavaScript, Promises, Event Loop и паттерны работы с API.
> **Литература:** Kyle Simpson «You Don't Know JS: Async & Performance», [learn.javascript.ru: Промисы](https://learn.javascript.ru/promise-basics), [MDN Event Loop](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop), [JavaScript.info: Event loop](https://javascript.info/event-loop), [Philip Roberts: What the heck is the event loop?](https://www.youtube.com/watch?v=8aGhZQkoFbQ)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md#неделя-8--movie-catalog)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-08/`

## День 1 (Mon): Асинхронность и Event Loop

### Теория

JavaScript однопоточен: в каждый момент времени выполняется только один фрагмент кода на main thread. Синхронные операции (циклы, тяжёлые вычисления) блокируют интерфейс — кнопки не реагируют, анимации замирают. Асинхронность решает это: долгие задачи (таймеры, сетевые запросы, чтение файлов) делегируются Web APIs браузера, а результат возвращается через колбэки, когда main thread освободится.

Event Loop — механизм, который координирует выполнение. Call stack выполняет текущий синхронный код. Когда стек пуст, Loop проверяет очереди задач. Сначала выполняются **microtasks** (колбэки Promise: `.then`, `.catch`, `queueMicrotask`), и только потом **macrotasks** (`setTimeout`, `setInterval`, I/O). Поэтому `Promise.resolve().then(...)` всегда выполнится раньше `setTimeout(fn, 0)` — даже с нулевой задержкой.

Классическая ловушка — думать, что `setTimeout(fn, 0)` выполнится «сразу». На самом деле он попадёт в macrotask queue и дождётся завершения всего синхронного кода и всех microtasks. Понимание этого порядка — основа отладки «почему console.log выводится не в том порядке, который я ожидал». Визуализатор [Loupe](http://latentflip.com/loupe/) помогает увидеть движение задач по очередям.

**Читать:**
- [learn.javascript.ru: Введение: колбэки](https://learn.javascript.ru/intro)
- [javascript.info: Event loop](https://javascript.info/event-loop)
- [MDN: Event Loop](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop)
- [Loupe — визуализация Event Loop](http://latentflip.com/loupe/)

**Ключевая мысль:** microtasks (Promise) всегда опережают macrotasks (setTimeout) — запомни это правило, и половина async-багов исчезнет.

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

Promise — объект-обёртка над результатом асинхронной операции, который ещё неизвестен. У Promise три состояния: `pending` (ожидание), `fulfilled` (успех) и `rejected` (ошибка). Переход из pending возможен только один раз — после resolve или reject состояние не меняется. Это делает Promise предсказуемым контрактом: либо данные, либо ошибка.

Создание: `new Promise((resolve, reject) => { ... })`. Потребление: `.then(onFulfilled)` для успеха, `.catch(onRejected)` для ошибок, `.finally(onFinally)` для cleanup в любом случае (скрыть loader, сбросить флаг загрузки). Каждый `.then` возвращает **новый** Promise — поэтому цепочки `.then().then().catch()` читаются сверху вниз без «callback hell» вложенных функций.

Если `.then`-колбэк возвращает значение, следующий `.then` получит его. Если возвращает Promise, следующий `.then` дождётся его разрешения. Один `.catch` в конце цепочки перехватит reject из любого предыдущего звена. `Promise.all([p1, p2])` запускает несколько Promise параллельно и ждёт все — но один reject роняет весь результат.

**Читать:**
- [learn.javascript.ru: Промисы](https://learn.javascript.ru/promise-basics)
- [learn.javascript.ru: Цепочка промисов](https://learn.javascript.ru/promise-chaining)
- [MDN: Promise](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/Promise)

**Ключевая мысль:** Promise — это цепочка, а не вложенность; `.then` возвращает новый Promise, и один `.catch` обслуживает всю цепочку.

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

`async/await` — синтаксический сахар над Promise, делающий асинхронный код похожим на синхронный. Функция с ключевым словом `async` всегда возвращает Promise: даже `return 42` превратится в `Promise.resolve(42)`. Ключевое слово `await` можно использовать только внутри `async`-функции — оно приостанавливает выполнение **только этой функции**, отдавая управление Event Loop. Main thread при этом не блокируется.

Вместо `.catch` в цепочке используй `try/catch` вокруг `await`:

```js
try {
  const data = await fetchJson(url);
} catch (err) {
  showError(err.message);
}
```

Главная ловушка — последовательный `await` в цикле: `for (const id of ids) { await fetch(id) }` выполнит N запросов по очереди. Если запросы независимы, собери массив Promise и дождись всех: `await Promise.all(ids.map(id => fetch(id)))`. В ES-модулях доступен top-level `await` — можно писать `const config = await fetch('/config.json')` прямо в `main.js` без обёртки.

**Читать:**
- [learn.javascript.ru: Async/await](https://learn.javascript.ru/async-await)
- [MDN: async function](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Statements/async_function)
- [javascript.info: Async/await](https://javascript.info/async-await)

**Ключевая мысль:** `await` не блокирует браузер — он лишь ставит на паузу текущую async-функцию, пока Promise не разрешится.

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

HTTP — протокол обмена сообщениями между клиентом и сервером. Каждый запрос состоит из метода, URL, заголовков и опционального тела. Ответ содержит статус-код, заголовки и тело. Методы несут семантику: GET читает ресурс (идемпотентен, кэшируем), POST создаёт новый, PUT/PATCH обновляют, DELETE удаляет. Понимание семантики помогает проектировать API и правильно обрабатывать ответы.

Статус-коды сгруппированы: 1xx — информация, 2xx — успех (200 OK, 201 Created, 204 No Content), 3xx — перенаправление, 4xx — ошибка клиента (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found), 5xx — ошибка сервера. Для UI важно различать 401 («войдите в систему») и 403 («у вас нет прав») — пользователю нужны разные сообщения.

Заголовки передают метаданные: `Content-Type` описывает формат тела, `Authorization` — токен доступа, `Cache-Control` и `ETag` управляют кэшированием. CORS настраивается **на сервере** через заголовки вроде `Access-Control-Allow-Origin`. «Непростые» запросы (нестандартные заголовки, методы кроме GET/POST) вызывают preflight — браузер сначала отправит OPTIONS и спросит разрешение.

**Читать:**
- [MDN: HTTP Overview](https://developer.mozilla.org/ru/docs/Web/HTTP/Overview)
- [MDN: CORS](https://developer.mozilla.org/ru/docs/Web/HTTP/CORS)
- [MDN: HTTP response status codes](https://developer.mozilla.org/ru/docs/Web/HTTP/Status)

**Ключевая мысль:** HTTP-метод + статус-код + заголовки — это язык, на котором клиент и сервер договариваются о результате операции.

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

Работа с API в production выходит за рамки простого `fetch(url)`. Пагинация делит большие наборы данных на страницы: offset/limit (`?page=2&limit=20`) прост в реализации, но нестабилен при вставках новых записей; cursor-based пагинация (`?after=lastId`) надёжнее для лент и поиска. Retry с exponential backoff повторяет упавший запрос с растущей задержкой (1с, 2с, 4с), не перегружая сервер при временных сбоях.

Race condition возникает, когда быстрый новый запрос завершается раньше старого, но старый ответ приходит последним и перезаписывает актуальные данные. Решения: `AbortController` (отменить предыдущий fetch) или счётчик/request id (игнорировать устаревший ответ). Request deduplication не запускает второй идентичный запрос, пока первый ещё в полёте — полезно для кэширования в памяти.

Паттерн stale-while-revalidate: сначала покажи кэшированные данные (мгновенный отклик), затем обнови фоном. Skeleton UI резервирует место под контент во время загрузки, снижая layout shift (CLS). Эти приёмы превращают «голый fetch» в устойчивый клиентский слой данных.

**Читать:**
- [JSON:API — Pagination](https://jsonapi.org/format/#fetching-pagination)
- [web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp) — skeleton и perceived performance
- [MDN: AbortController](https://developer.mozilla.org/ru/docs/Web/API/AbortController)

**Ключевая мысль:** надёжный API-клиент обрабатывает не только успех, но и повторы, гонки запросов, пагинацию и кэширование.

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

Помимо базового `Promise.all`, в JavaScript есть набор утилит для разных сценариев. `Promise.allSettled` ждёт завершения **всех** Promise и возвращает массив `{ status, value/reason }` — идеально, когда нужны результаты нескольких независимых API, даже если часть упала. `Promise.race` отдаёт результат первого завершившегося Promise — удобно для timeout-обёртки. `Promise.any` возвращает первый успешный, игнорируя reject (если все упали — `AggregateError`).

`Promise.all` работает по принципу fail-fast: один reject ломает весь результат. Используй его, когда все данные обязательны (загрузка профиля + настроек одновременно). `Promise.allSettled` — когда частичный успех допустим (дашборд с виджетами от разных сервисов). Timeout через race: `Promise.race([fetch(url), delay(5000).then(() => Promise.reject('timeout'))])`.

Необработанный reject (`unhandledrejection`) — сигнал, что где-то забыли `.catch` или `try/catch`. В production повесь глобальный listener `window.addEventListener('unhandledrejection', ...)` для логирования. `for await...of` позволяет последовательно обрабатывать асинхронные итерируемые источники без гонки параллельных запросов.

**Читать:**
- [MDN: Promise.allSettled()](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled)
- [MDN: Promise.race()](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/Promise/race)
- [learn.javascript.ru: Promise API](https://learn.javascript.ru/promise-api)

**Ключевая мысль:** выбирай Promise-утилиту по сценарию — all для «всё или ничего», allSettled для «что получилось», race для таймаутов.

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

Асинхронная архитектура приложения определяет, как слои общаются между собой. API-слой возвращает данные или бросает типизированную ошибку (`ApiError` со статусом) — он не знает о DOM и не решает, показать спиннер или toast. UI-слой подписывается на состояние и рендерит соответствующий экран. Между ними — слой состояния с явными фазами: `idle | loading | success | error | empty`.

Явная state machine убирает «зависшие» экраны: в каждый момент UI находится ровно в одном состоянии, и переходы предсказуемы (loading → success или loading → error). Простой pub/sub (`createAsyncState` с `subscribe`/`setState`) даёт реактивность без фреймворка — задел на React hooks. При тестировании async-кода fetch можно подменить mock-функцией, возвращающей фиксированный Promise.

На следующих неделях TypeScript добавит `Promise<T>` как контракт: async-функция документирует, какой тип данных вернётся. Сейчас зафиксируй принцип: асинхронность — это не только синтаксис, а разделение ответственности между запросом, состоянием и отображением.

**Читать:**
- [javascript.info: Промисы](https://javascript.info/promise-basics)
- [patterns.dev: Observer Pattern](https://www.patterns.dev/vanilla/observer-pattern/)
- [TypeScript Handbook: Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html) — подготовка к неделе 10

**Ключевая мысль:** async-архитектура — это явные состояния UI и чёткие границы между api, state и render.

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
