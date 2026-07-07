# Неделя 7: JavaScript — localStorage, Fetch, формы, модули ES

> **Цель недели:** научиться сохранять данные в браузере, работать с API и организовывать код в ES-модули.
> **Литература:** [learn.javascript.ru: Fetch](https://learn.javascript.ru/fetch), [MDN Web Storage](https://developer.mozilla.org/ru/docs/Web/API/Web_Storage_API), [MDN JavaScript modules](https://developer.mozilla.org/ru/docs/Web/JavaScript/Guide/Modules), [JSONPlaceholder Guide](https://jsonplaceholder.typicode.com/guide/), [web.dev Storage for the web](https://web.dev/storage-for-the-web/)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md#неделя-7--notes-dashboard)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-07/`

## День 1 (Mon): localStorage и sessionStorage

### Теория

Web Storage API даёт браузеру простое key-value хранилище, привязанное к origin (протокол + домен + порт). `localStorage` и `sessionStorage` работают одинаково по API, но различаются временем жизни: localStorage сохраняет данные между сессиями, а sessionStorage очищается при закрытии вкладки. Оба интерфейса принимают только строки — если нужно сохранить объект или массив, сначала сериализуй его через `JSON.stringify`, а при чтении восстанови через `JSON.parse`.

Основные методы: `setItem(key, value)`, `getItem(key)` (возвращает `null`, если ключа нет), `removeItem(key)` и `clear()`. API синхронный: каждая операция выполняется на main thread, поэтому не стоит записывать большие объёмы данных за раз. Типичный лимит — около 5 МБ на origin; при переполнении браузер выбросит `QuotaExceededError`.

Для настроек UI (тема, язык, черновики форм) localStorage — естественный выбор. Но это не защищённое хранилище: любой JavaScript на странице (в том числе внедрённый через XSS) может прочитать все ключи. Пароли, JWT и API-ключи в localStorage хранить нельзя. Пользователь или расширение браузера могут вручную изменить значение в DevTools — поэтому `JSON.parse` всегда оборачивай в `try/catch` и задавай разумные значения по умолчанию при ошибке.

**Читать:**
- [MDN: Window.localStorage](https://developer.mozilla.org/ru/docs/Web/API/Window/localStorage)
- [MDN: Web Storage API](https://developer.mozilla.org/ru/docs/Web/API/Web_Storage_API)
- [web.dev: Storage for the web](https://web.dev/storage-for-the-web/)

**Ключевая мысль:** localStorage — удобный кэш для UI-состояния, но не сейф для секретов и не замена серверной базе данных.

### Практика
1. Сохрани Todo-список в `localStorage` при каждом изменении
2. При загрузке страницы восстанови задачи из storage
3. Кнопка «Очистить всё» — `removeItem` + обновление UI
4. Сохрани тему оформления (light/dark) между сессиями
5. Обработай случай битого JSON в `getItem` (try/catch)
6. Создай ключ `week-07-notes` — заготовка для проекта недели
7. Вынеси работу со storage в функции `saveState` / `loadState`

**Критерии:**
- [ ] Данные переживают перезагрузку страницы
- [ ] Объекты сериализуются через JSON
- [ ] Ошибки парсинга обработаны gracefully

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 07 day 1: localStorage persist"`

### Ловушки
- Хранение паролей и токенов в localStorage — уязвимость XSS
- Забытый `JSON.parse` — строка `"[object Object]"`
- QuotaExceededError при переполнении — редко, но возможно

## День 2 (Tue): JSON и работа с данными

### Теория

JSON (JavaScript Object Notation) — текстовый формат обмена данными между клиентом, сервером и файлами. Он поддерживает объекты, массивы, строки, числа, `true`/`false` и `null`, но не функции, `undefined` и комментарии. При `JSON.stringify` объекты `Date` превращаются в ISO-строки, а `undefined` в свойствах объекта просто опускаются — это важно помнить при экспорте данных.

Метод `JSON.stringify(obj, replacer, space)` умеет фильтровать поля (через массив ключей или функцию-replacer) и форматировать вывод: `space: 2` делает JSON читаемым для человека при отладке. Обратная операция — `JSON.parse`, которая бросает `SyntaxError` на невалидном тексте. Импорт из файла всегда требует валидации: проверь наличие обязательных полей, типы и допустимые значения до того, как смешаешь чужие данные со своим состоянием.

В приложениях с localStorage данные со временем меняют форму. Добавь поле `schemaVersion` в сохраняемый объект — при загрузке сравни версию и при необходимости мигрируй старый формат в новый. Обновления списков объектов делай иммутабельно: `items.map(item => item.id === id ? { ...item, title } : item)` вместо прямой мутации элемента массива. Так проще отслеживать изменения и избегать побочных эффектов.

**Читать:**
- [MDN: Working with JSON](https://developer.mozilla.org/ru/docs/Learn/JavaScript/Objects/JSON)
- [MDN: JSON.stringify()](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)
- [learn.javascript.ru: Формат JSON](https://learn.javascript.ru/json)

**Ключевая мысль:** JSON — контракт обмена данными; валидация и версионирование схемы защищают приложение от битых импортов и устаревших сохранений.

### Практика
1. Экспорт Todo в JSON-файл (download через Blob + URL.createObjectURL)
2. Импорт: `<input type="file">` → FileReader → parse → merge в список
3. Функция `validateTodo(data)` — проверка обязательных полей
4. Статистика: группировка задач по дате создания
5. Миграция данных: если версия схемы старая — обнови формат
6. Добавь `exportedAt` в экспортируемый JSON
7. Отклони импорт с понятным сообщением при невалидном файле

**Критерии:**
- [ ] Экспорт/импорт JSON работает
- [ ] Валидация отклоняет невалидные данные
- [ ] Иммутабельные обновления, не мутация массива напрямую

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 07 day 2: json import export"`

## День 3 (Wed): Fetch API — основы

### Теория

Fetch API — современный способ делать HTTP-запросы из браузера. Вызов `fetch(url)` сразу возвращает Promise, который разрешается объектом `Response`, ещё до того как тело ответа полностью загружено. Чтобы получить JSON, нужна вторая асинхронная операция: `response.json()`, которая тоже возвращает Promise. Типичная цепочка: `fetch(url).then(r => r.json()).then(data => ...)`.

Важная особенность: fetch **не отклоняет** Promise при HTTP-ошибках вроде 404 или 500. Promise reject происходит только при сетевых сбоях (нет интернета, CORS, таймаут DNS). Поэтому всегда проверяй `response.ok` (это shorthand для статусов 200–299) и обрабатывай неуспешные ответы явно — выброси ошибку или верни понятное сообщение пользователю.

Для POST-запросов передай объект опций вторым аргументом: `method: 'POST'`, `headers: { 'Content-Type': 'application/json' }` и `body: JSON.stringify(data)`. Без правильного `Content-Type` сервер может не распознать тело как JSON. Для обучения удобен [JSONPlaceholder](https://jsonplaceholder.typicode.com/) — бесплатный mock REST API без регистрации, имитирующий посты, пользователей и комментарии.

**Читать:**
- [learn.javascript.ru: Fetch](https://learn.javascript.ru/fetch)
- [MDN: Using Fetch](https://developer.mozilla.org/ru/docs/Web/API/Fetch_API/Using_Fetch)
- [JSONPlaceholder Guide](https://jsonplaceholder.typicode.com/guide/)

**Ключевая мысль:** fetch различает «сеть упала» (reject) и «сервер ответил ошибкой» (resolve с `ok: false`) — проверяй оба случая.

### Практика
1. Загрузи посты с [JSONPlaceholder](https://jsonplaceholder.typicode.com/posts)
2. Отобрази список заголовков в DOM
3. Обработай loading state (текст «Загрузка...») и error state
4. POST новый пост на API, выведи ответ в Console
5. Используй `async/await` (предпросмотр, углубление на неделе 8)
6. Создай функцию `fetchJson(url)` с проверкой `response.ok`
7. Покажи empty state, если массив постов пуст

**Критерии:**
- [ ] Данные с API отображаются в UI
- [ ] Обработаны loading и error
- [ ] Проверяется `response.ok`

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 07 day 3: fetch api basics"`

## День 4 (Thu): Работа с публичными API

### Теория

Публичные REST API организуют данные вокруг ресурсов — сущностей вроде «пользователь», «пост» или «город». URL описывает *что* запрашиваешь (`/users/42`), а HTTP-метод — *какое действие* выполняешь (GET — прочитать, POST — создать). Ответ сервера сопровождается статус-кодом: 200 — успех, 201 — создано, 400 — ошибка клиента, 404 — не найдено, 500 — ошибка сервера. Умение читать статус и тело ответа — базовый навык интеграции.

Параметры запроса передаются в query string: `?q=moscow&page=2`. Спецсимволы и пробелы кодируй через `URLSearchParams`, а не вручную — иначе поиск по «New York» сломается. Перед интеграцией изучи документацию API: какие endpoints доступны, какие поля обязательны, есть ли лимиты на количество запросов (rate limiting). OpenAPI/Swagger-спецификация — стандартный формат, где всё это описано машиночитаемо.

CORS (Cross-Origin Resource Sharing) — механизм безопасности браузера. Если твой сайт на `localhost:5500`, а API на другом домене, браузер спросит сервер: «разрешён ли этот origin?». Если сервер не вернёт нужные заголовки (`Access-Control-Allow-Origin`), fetch заблокируется — это не баг твоего кода, а политика браузера. API-ключи в production-коде на клиенте видны всем — для секретных ключей нужен backend-прокси.

**Читать:**
- [MDN: CORS](https://developer.mozilla.org/ru/docs/Web/HTTP/CORS)
- [MDN: HTTP Overview](https://developer.mozilla.org/ru/docs/Web/HTTP/Overview)
- [Open-Meteo API](https://open-meteo.com/en/docs)

**Ключевая мысль:** интеграция с API начинается с чтения документации и понимания HTTP-семантики, а не с написания fetch.

### Практика
1. Погода: [Open-Meteo API](https://open-meteo.com/) — без ключа
2. Форма поиска города → fetch → отображение температуры и иконки
3. Пагинация: загрузи страницы постов JSONPlaceholder по кнопке «Ещё»
4. Обработай 404 и сетевую ошибку разными сообщениями
5. Дебаг запросов в DevTools → Network
6. GitHub Users API: поиск по логину — заготовка для проекта
7. Документируй используемые endpoints в комментарии `api.js`

**Критерии:**
- [ ] Реальный API интегрирован в UI
- [ ] Пользователь видит понятные сообщения об ошибках
- [ ] Network panel использован для отладки

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 07 day 4: public apis weather github"`

## День 5 (Fri): ES-модули

### Теория

ES-модули — стандартный способ организации JavaScript-кода в файлах с явными зависимостями. Каждый файл — отдельный модуль со своей областью видимости: переменные не попадают в глобальный `window`. Чтобы сделать функцию или константу доступной снаружи, используй `export`. Импорт: `import { fetchPosts } from './api.js'` для именованного экспорта или `import render from './render.js'` для default.

В HTML подключай модули через `<script type="module" src="main.js">`. Такой скрипт выполняется в strict mode, откладывается (defer) и загружается как модуль — браузер сам разрешит дерево зависимостей. В пути импорта обязательно указывай расширение `.js` — в отличие от bundler-ов, нативные модули в браузере этого требуют. Открытие файла через `file://` не сработает из-за CORS; нужен локальный HTTP-сервер (Live Server, `npx serve`).

Именованный export предпочтителен, когда из файла экспортируется несколько сущностей — имена явные при импорте и рефакторинге. Default export удобен для «главной» сущности файла (один компонент, один класс). Типичная структура проекта: `api/` — запросы, `ui/` — рендер DOM, `utils/` — хелперы, `main.js` — точка входа, которая только связывает модули.

**Читать:**
- [learn.javascript.ru: Модули](https://learn.javascript.ru/modules-intro)
- [MDN: JavaScript modules](https://developer.mozilla.org/ru/docs/Web/JavaScript/Guide/Modules)
- [javascript.info: Модули](https://javascript.info/modules-intro)

**Ключевая мысль:** модули превращают монолитный скрипт в граф зависимостей с изолированными областями видимости — основа масштабируемого фронтенда.

### Практика
1. Разбей Todo App на модули: `storage.js`, `todo.js`, `render.js`, `main.js`
2. `api.js` — функции fetch с экспортом
3. Переименование при импорте: `import { fetchPosts as getPosts }`
4. Запуск через Live Server (модули требуют HTTP, не file://)
5. Циклические зависимости — избегай, рефакторинг при необходимости
6. Создай `week-07/js/` с 5+ модулями
7. Точка входа `main.js` только импортирует и инициализирует

**Критерии:**
- [ ] Все скрипты — ES modules с `type="module"`
- [ ] Нет глобальных переменных в `window`
- [ ] Логичная структура папок js/

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 07 day 5: es modules structure"`

## День 6 (Sat): Формы и API вместе

### Теория

Связка HTML-форм и fetch — типичный сценарий создания данных на сервере. Перехвати событие `submit`, вызови `e.preventDefault()`, собери данные из полей и отправь POST-запрос с `body: JSON.stringify(formData)` и заголовком `Content-Type: application/json`. Для форм с файлами удобнее `FormData` — он автоматически формирует multipart-тело. На время запроса отключай кнопку submit, чтобы пользователь не отправил дубликат.

Поиск по API при каждом нажатии клавиши создаёт лишнюю нагрузку. Debounce откладывает вызов функции до паузы в вводе (обычно 300 мс): пока пользователь печатает, запросы не уходят. Если запрос уже в полёте, а пользователь изменил запрос, старый ответ может прийти позже нового и перезаписать актуальные данные — race condition. `AbortController` решает это: передай `signal` в fetch и вызови `abort()` при новом вводе или в cleanup.

Optimistic UI обновляет интерфейс до ответа сервера («пост уже в списке»), создавая ощущение мгновенности. Но при ошибке сервера нужен rollback — убрать добавленный элемент и показать сообщение. Баланс между скоростью отклика и надёжностью — ключевой навык при работе с формами и API.

**Читать:**
- [MDN: Using Fetch — отправка данных](https://developer.mozilla.org/ru/docs/Web/API/Fetch_API/Using_Fetch#%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85)
- [MDN: AbortController](https://developer.mozilla.org/ru/docs/Web/API/AbortController)
- [learn.javascript.ru: debounce](https://learn.javascript.ru/task/debounce)

**Ключевая мысль:** форма + fetch требуют защиты от двойной отправки, debounce для поиска и отмены устаревших запросов.

### Практика
1. Форма «Добавить пост» → POST на JSONPlaceholder → добавь в список
2. Поиск пользователей GitHub API с debounce 300ms
3. Отмена предыдущего запроса при новом вводе (AbortController)
4. Disable кнопки submit на время запроса
5. Показ success/error toast после отправки
6. Реализуй `debounce(fn, ms)` самостоятельно или из learn.javascript.ru
7. Покажи спиннер в поле поиска во время загрузки

**Критерии:**
- [ ] POST отправляет корректный JSON
- [ ] Debounce на поиске работает
- [ ] UI не дублирует запросы при быстром вводе

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 07 day 6: forms api debounce"`

## День 7 (Sun): Интеграционный проект

### Теория

Интеграционный проект недели объединяет всё изученное: модули, localStorage, fetch, формы. Архитектурно раздели код на слои: `api` — HTTP-запросы и парсинг ответов, `cache` — чтение/запись в storage с TTL, `ui` — рендер DOM и обработка событий, `app` — связывание слоёв. Модуль api не должен знать о DOM, а ui не должен формировать URL запросов — так проще тестировать и менять каждую часть отдельно.

Кэш с TTL (time-to-live) сохраняет объект `{ data, cachedAt }` в localStorage. При загрузке сравни `Date.now() - cachedAt` с лимитом (например, 5 минут): если кэш свежий — покажи данные мгновенно, если нет — запроси с сервера и обнови кэш. При offline (можно симулировать в DevTools) покажи устаревший кэш с предупреждением вместо пустого экрана — это базовый offline-first подход.

Оборачивай асинхронные операции в `try/catch` на границе слоёв: пользователь должен видеть понятное сообщение об ошибке, а не пустую страницу. Простой retry — повторить запрос 2–3 раза с задержкой при сетевом сбое. На следующей неделе этот код перепишется на async/await и Promise-утилиты, но принципы слоёв и обработки ошибок останутся.

**Читать:**
- [web.dev: Storage for the web](https://web.dev/storage-for-the-web/)
- [MDN: Fetch API](https://developer.mozilla.org/ru/docs/Web/API/Fetch_API)
- [learn.javascript.ru: Промисы](https://learn.javascript.ru/promise-basics) — подготовка к неделе 8

**Ключевая мысль:** зрелое клиентское приложение — это слои (api/cache/ui) плюс явная обработка ошибок, кэша и offline-сценариев.

### Практика
1. Собери «Панель постов»: список + детали + форма создания
2. Кэшируй список постов в localStorage на 5 минут
3. При offline (DevTools → Offline) покажи кэш и предупреждение
4. Модули: api, cache, ui, app
5. Финальный рефакторинг и коммит `feat: posts dashboard`
6. Собери Notes Dashboard: заметки + погода + GitHub search
7. Тег `week-07-done` на финальном коммите

**Критерии:**
- [ ] Полный CRUD UI (create + read, delete опционально)
- [ ] Кэш с TTL работает
- [ ] Модульная архитектура

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 07 day 7: notes dashboard final"`

## Проект недели

**Dashboard заметок** — SPA на ванильном JS с модулями, localStorage и внешним API.

Подробное описание: [docs/projects.md — Неделя 7](../../docs/projects.md#неделя-7--notes-dashboard)

Функции: локальные заметки (CRUD + persist), виджет погоды с API, поиск по GitHub users.

**Критерии проекта:**
- [ ] ES modules, минимум 5 файлов
- [ ] localStorage + Fetch к 2 API
- [ ] Loading/error/empty states
- [ ] Debounced search, form validation
- [ ] Папка `week-07/` с README и скриншотом
- [ ] Заметки: create, edit, delete, persist между сессиями
- [ ] Виджет погоды по городу (Open-Meteo или аналог)
- [ ] GitHub user search с debounce и отменой запроса
- [ ] Тег `week-07-done` на финальном коммите

## Ревью-чеклист
- Как сохранить массив объектов в localStorage?
- Почему fetch не reject при HTTP 404?
- Разница named export и default export?
- Зачем `type="module"` и почему не file://?
- Могу ли я отправить JSON POST через fetch?
