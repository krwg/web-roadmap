# Неделя 7: JavaScript — localStorage, Fetch, формы, модули ES

> **Цель недели:** научиться сохранять данные в браузере, работать с API и организовывать код в ES-модули.
> **Литература:** [learn.javascript.ru: Fetch](https://learn.javascript.ru/fetch), [MDN Web Storage](https://developer.mozilla.org/ru/docs/Web/API/Web_Storage_API), [MDN JavaScript modules](https://developer.mozilla.org/ru/docs/Web/JavaScript/Guide/Modules), [JSONPlaceholder Guide](https://jsonplaceholder.typicode.com/guide/), [web.dev Storage for the web](https://web.dev/storage-for-the-web/)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md#неделя-7--notes-dashboard)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-07/`

## День 1 (Mon): localStorage и sessionStorage

### Теория
- [MDN: Window.localStorage](https://developer.mozilla.org/ru/docs/Web/API/Window/localStorage)
- `setItem`, `getItem`, `removeItem`, `clear` — только строки
- `JSON.stringify` / `JSON.parse` для объектов и массивов
- `sessionStorage` — данные до закрытия вкладки
- Лимиты (~5MB), синхронный API, не для секретов
- localStorage переживает перезагрузку и закрытие браузера — идеален для настроек UI
- Синхронный API блокирует main thread — не пиши мегабайты за раз
- XSS может прочитать localStorage — не храни пароли и JWT в клиенте
- Всегда оборачивай `JSON.parse` в try/catch — пользователь мог испортить данные

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
- [MDN: Working with JSON](https://developer.mozilla.org/ru/docs/Learn/JavaScript/Objects/JSON)
- Формат JSON: объекты, массивы, типы, невалидный JSON
- `JSON.stringify(obj, replacer, space)` — форматирование
- Иммутабельные обновления массива объектов: map + spread
- Валидация структуры данных (ручная, без библиотек)
- JSON — текстовый формат обмена; даты сериализуются как строки
- `JSON.stringify` с `space: 2` — читаемый экспорт для отладки
- Иммутабельный update: `notes.map(n => n.id === id ? {...n, title} : n)`
- Версионирование схемы (`schemaVersion: 1`) упрощает миграции данных

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
- [learn.javascript.ru: Fetch](https://learn.javascript.ru/fetch)
- `fetch(url)` возвращает Promise; цепочка `.then(r => r.json())`
- HTTP-методы: GET, POST; заголовки `headers`
- Проверка `response.ok` — fetch не reject на 404
- [MDN: Using Fetch](https://developer.mozilla.org/ru/docs/Web/API/Fetch_API/Using_Fetch)
- Fetch resolve даже при HTTP 404 — проверяй `response.ok` вручную
- Сетевые ошибки (offline) reject Promise — нужен catch
- `Content-Type: application/json` обязателен при отправке JSON
- JSONPlaceholder — бесплатный mock API для обучения без регистрации

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
- REST basics: ресурсы, endpoints, статусы 200/201/400/404/500
- Query parameters: `?q=search&page=2`
- API keys — никогда в клиентском коде для production (обзор)
- Rate limiting, CORS — [MDN CORS](https://developer.mozilla.org/ru/docs/Web/HTTP/CORS)
- Документация API: читать OpenAPI/Swagger
- REST: URL = ресурс, HTTP-метод = действие; предсказуемые endpoints
- CORS блокирует браузер, если сервер не разрешил origin — не баг fetch
- Query params кодируй через `URLSearchParams` — корректные спецсимволы
- Open-Meteo не требует ключа — хороший старт для виджета погоды

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
- [learn.javascript.ru: Модули](https://learn.javascript.ru/modules-intro)
- `export`, `export default`, `import { x } from './file.js'`
- `type="module"` в script — defer по умолчанию, strict mode
- Именованный vs default export — когда что
- Структура проекта: `api/`, `ui/`, `utils/`, `main.js`
- Модули имеют собственную область видимости — нет загрязнения `window`
- Расширение `.js` в import обязательно в браузере
- Default export — один на файл; named — несколько, явные имена
- `file://` не загружает модули — нужен Live Server или dev server

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
- `FormData` для отправки форм: `new FormData(form)`
- `fetch` с `method: 'POST'`, `body: JSON.stringify`, `Content-Type`
- Optimistic UI — обнови UI до ответа сервера (осторожно)
- Debounce для поиска — [learn.javascript.ru: debounce](https://learn.javascript.ru/task/debounce) (задача)
- AbortController для отмены запросов
- Debounce 300ms — не спамить API на каждый символ поиска
- AbortController отменяет устаревший запрос при новом вводе
- Disable submit на время запроса — защита от double-submit
- Optimistic UI улучшает UX, но нужен rollback при ошибке

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
- Error boundaries на уровне приложения (try/catch вокруг async)
- Retry logic — простой повтор при сетевой ошибке
- Кэширование в localStorage с TTL (timestamp)
- Подготовка к async/await и promises (следующая неделя)
- TTL-кэш: сохраняй `{data, cachedAt}` и проверяй возраст при чтении
- Offline-first: покажи кэш + баннер «нет сети» вместо пустого экрана
- api / cache / ui — слои не смешиваются; api не трогает DOM
- try/catch вокруг каждого await — пользователь видит ошибку, не white screen

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
