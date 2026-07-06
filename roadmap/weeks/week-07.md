# Неделя 7: JavaScript — localStorage, Fetch, формы, модули ES

> **Цель недели:** научиться сохранять данные в браузере, работать с API и организовывать код в ES-модули.
> **Литература:** [learn.javascript.ru: Fetch](https://learn.javascript.ru/fetch), [MDN Web Storage](https://developer.mozilla.org/ru/docs/Web/API/Web_Storage_API), [MDN JavaScript modules](https://developer.mozilla.org/ru/docs/Web/JavaScript/Guide/Modules)

## День 1 (Mon): localStorage и sessionStorage

### Теория
- [MDN: Window.localStorage](https://developer.mozilla.org/ru/docs/Web/API/Window/localStorage)
- `setItem`, `getItem`, `removeItem`, `clear` — только строки
- `JSON.stringify` / `JSON.parse` для объектов и массивов
- `sessionStorage` — данные до закрытия вкладки
- Лимиты (~5MB), синхронный API, не для секретов

### Практика
1. Сохрани Todo-список в `localStorage` при каждом изменении
2. При загрузке страницы восстанови задачи из storage
3. Кнопка «Очистить всё» — `removeItem` + обновление UI
4. Сохрани тему оформления (light/dark) между сессиями
5. Обработай случай битого JSON в `getItem` (try/catch)

**Критерии:**
- [ ] Данные переживают перезагрузку страницы
- [ ] Объекты сериализуются через JSON
- [ ] Ошибки парсинга обработаны gracefully

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

### Практика
1. Экспорт Todo в JSON-файл (download через Blob + URL.createObjectURL)
2. Импорт: `<input type="file">` → FileReader → parse → merge в список
3. Функция `validateTodo(data)` — проверка обязательных полей
4. Статистика: группировка задач по дате создания
5. Миграция данных: если версия схемы старая — обнови формат

**Критерии:**
- [ ] Экспорт/импорт JSON работает
- [ ] Валидация отклоняет невалидные данные
- [ ] Иммутабельные обновления, не мутация массива напрямую

## День 3 (Wed): Fetch API — основы

### Теория
- [learn.javascript.ru: Fetch](https://learn.javascript.ru/fetch)
- `fetch(url)` возвращает Promise; цепочка `.then(r => r.json())`
- HTTP-методы: GET, POST; заголовки `headers`
- Проверка `response.ok` — fetch не reject на 404
- [MDN: Using Fetch](https://developer.mozilla.org/ru/docs/Web/API/Fetch_API/Using_Fetch)

### Практика
1. Загрузи посты с [JSONPlaceholder](https://jsonplaceholder.typicode.com/posts)
2. Отобрази список заголовков в DOM
3. Обработай loading state (текст «Загрузка...») и error state
4. POST новый пост на API, выведи ответ в Console
5. Используй `async/await` (предпросмотр, углубление на неделе 8)

**Критерии:**
- [ ] Данные с API отображаются в UI
- [ ] Обработаны loading и error
- [ ] Проверяется `response.ok`

## День 4 (Thu): Работа с публичными API

### Теория
- REST basics: ресурсы, endpoints, статусы 200/201/400/404/500
- Query parameters: `?q=search&page=2`
- API keys — никогда в клиентском коде для production (обзор)
- Rate limiting, CORS — [MDN CORS](https://developer.mozilla.org/ru/docs/Web/HTTP/CORS)
- Документация API: читать OpenAPI/Swagger

### Практика
1. Погода: [Open-Meteo API](https://open-meteo.com/) — без ключа
2. Форма поиска города → fetch → отображение температуры и иконки
3. Пагинация: загрузи страницы постов JSONPlaceholder по кнопке «Ещё»
4. Обработай 404 и сетевую ошибку разными сообщениями
5. Дебаг запросов в DevTools → Network

**Критерии:**
- [ ] Реальный API интегрирован в UI
- [ ] Пользователь видит понятные сообщения об ошибках
- [ ] Network panel использован для отладки

## День 5 (Fri): ES-модули

### Теория
- [learn.javascript.ru: Модули](https://learn.javascript.ru/modules-intro)
- `export`, `export default`, `import { x } from './file.js'`
- `type="module"` в script — defer по умолчанию, strict mode
- Именованный vs default export — когда что
- Структура проекта: `api/`, `ui/`, `utils/`, `main.js`

### Практика
1. Разбей Todo App на модули: `storage.js`, `todo.js`, `render.js`, `main.js`
2. `api.js` — функции fetch с экспортом
3. Переименование при импорте: `import { fetchPosts as getPosts }`
4. Запуск через Live Server (модули требуют HTTP, не file://)
5. Циклические зависимости — избегай, рефакторинг при необходимости

**Критерии:**
- [ ] Все скрипты — ES modules с `type="module"`
- [ ] Нет глобальных переменных в `window`
- [ ] Логичная структура папок js/

## День 6 (Sat): Формы и API вместе

### Теория
- `FormData` для отправки форм: `new FormData(form)`
- `fetch` с `method: 'POST'`, `body: JSON.stringify`, `Content-Type`
- Optimistic UI — обнови UI до ответа сервера (осторожно)
- Debounce для поиска — [learn.javascript.ru: debounce](https://learn.javascript.ru/task/debounce) (задача)
- AbortController для отмены запросов

### Практика
1. Форма «Добавить пост» → POST на JSONPlaceholder → добавь в список
2. Поиск пользователей GitHub API с debounce 300ms
3. Отмена предыдущего запроса при новом вводе (AbortController)
4. Disable кнопки submit на время запроса
5. Показ success/error toast после отправки

**Критерии:**
- [ ] POST отправляет корректный JSON
- [ ] Debounce на поиске работает
- [ ] UI не дублирует запросы при быстром вводе

## День 7 (Sun): Интеграционный проект

### Теория
- Error boundaries на уровне приложения (try/catch вокруг async)
- Retry logic — простой повтор при сетевой ошибке
- Кэширование в localStorage с TTL (timestamp)
- Подготовка к async/await и promises (следующая неделя)

### Практика
1. Собери «Панель постов»: список + детали + форма создания
2. Кэшируй список постов в localStorage на 5 минут
3. При offline (DevTools → Offline) покажи кэш и предупреждение
4. Модули: api, cache, ui, app
5. Финальный рефакторинг и коммит `feat: posts dashboard`

**Критерии:**
- [ ] Полный CRUD UI (create + read, delete опционально)
- [ ] Кэш с TTL работает
- [ ] Модульная архитектура

## Проект недели

**Dashboard заметок** — SPA на ванильном JS с модулями, localStorage и внешним API.

Функции: локальные заметки (CRUD + persist), виджет погоды с API, поиск по GitHub users.

**Критерии проекта:**
- [ ] ES modules, минимум 5 файлов
- [ ] localStorage + Fetch к 2 API
- [ ] Loading/error/empty states
- [ ] Debounced search, form validation

## Ревью-чеклист
- Как сохранить массив объектов в localStorage?
- Почему fetch не reject при HTTP 404?
- Разница named export и default export?
- Зачем `type="module"` и почему не file://?
- Могу ли я отправить JSON POST через fetch?
