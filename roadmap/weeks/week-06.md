# Неделя 6: JavaScript — объекты, DOM, события

> **Цель недели:** освоить объекты JavaScript, манипуляции DOM и обработку пользовательских событий.
> **Литература:** [learn.javascript.ru: Объекты](https://learn.javascript.ru/object), [learn.javascript.ru: DOM](https://learn.javascript.ru/searching-elements-dom), [MDN DOM](https://developer.mozilla.org/ru/docs/Web/API/Document_Object_Model), [DOM Enlightenment](http://domenlightenment.com/) — глубокое понимание DOM, [web.dev Learn Forms](https://web.dev/learn/forms/)

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md#неделя-6--dom-todo-app)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-06/`

## День 1 (Mon): Объекты — основы

### Теория
- [learn.javascript.ru: Объекты](https://learn.javascript.ru/object) — литералы, свойства, методы
- Точечная и скобочная нотация: `obj.key`, `obj['key']`
- `delete`, `in`, `for...in` vs `for...of` для объектов
- Копирование: shallow copy `{...obj}`, `Object.assign`
- `Object.keys`, `Object.values`, `Object.entries`
- Объекты хранятся по ссылке — присвоение копирует ссылку, не объект
- Методы — функции как свойства; `this` внутри метода ссылается на объект
- Скобочная нотация нужна для динамических ключей: `obj[variable]`
- `Object.entries` удобен для рендеринга пар ключ-значение в DOM

### Практика
1. Объект `user` с полями name, email, age — чтение и изменение
2. Метод `user.greet()` — function внутри объекта
3. Перебери свойства через `Object.entries` и выведи пары ключ-значение
4. Shallow copy: измени копию, убедись что вложенный объект общий
5. Массив пользователей — 3+ объекта в массиве
6. Создай объект `task` с `{id, title, done}` — модель для Todo
7. Добавь метод `task.toggle()` — переключает `done`

**Критерии:**
- [ ] Объект с минимум одним методом
- [ ] Использованы keys/values/entries
- [ ] Понимаю shallow vs deep copy (на уровне концепции)

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 06 day 1: objects basics"`

## День 2 (Tue): Деструктуризация и spread для объектов

### Теория
- [learn.javascript.ru: Деструктурирующее присваивание](https://learn.javascript.ru/destructuring-assignment)
- `const {name, age} = user`; переименование `{name: userName}`
- Значения по умолчанию при деструктуризации
- Spread в объектах: `{...defaults, ...overrides}`
- Rest в объектах: `const {id, ...rest} = product`
- Деструктуризация параметров делает сигнатуру функции самодокументируемой
- Spread для иммутабельного update: `{...task, done: true}` — не мутируй оригинал
- Rest исключает поля: `const {password, ...safeUser} = user` перед логированием
- Порядок spread важен: `{...defaults, ...overrides}` — overrides побеждают

### Практика
1. Функция `printUser({name, email, role = 'user'})` — деструктуризация параметров
2. Объедини настройки: `const config = {...defaults, ...userConfig}`
3. Исключи поле `password` из объекта перед логированием (rest)
4. Swap двух переменных через деструктуризацию массива `[a, b] = [b, a]`
5. Рефакторинг Todo из недели 5 с деструктуризацией
6. Иммутабельное обновление задачи: `updateTask(tasks, id, {done: true})`
7. Деструктурируй массив: `const [first, ...rest] = tasks`

**Критерии:**
- [ ] Деструктуризация в параметрах функций
- [ ] Spread для иммутабельного обновления объекта
- [ ] Rest для исключения полей

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 06 day 2: destructuring spread"`

### Ловушки
- `for...in` перебирает унаследованные свойства — используй `hasOwnProperty` или `Object.keys`
- Shallow copy не клонирует вложенные объекты
- Мутация объекта, переданного в функцию — ожидаемое поведение

## День 3 (Wed): DOM — поиск и изменение элементов

### Теория
- [learn.javascript.ru: DOM-дерево](https://learn.javascript.ru/dom-nodes)
- `document.querySelector`, `querySelectorAll`, `getElementById`
- Свойства: `textContent` vs `innerHTML` (безопасность!)
- `classList.add/remove/toggle/contains`
- Атрибуты: `getAttribute`, `setAttribute`, `dataset`
- DOM — живое дерево: изменения в JS сразу видны на странице
- `textContent` экранирует HTML — безопасно для пользовательского ввода
- `innerHTML` с user input — XSS-уязвимость; используй `createElement`
- `dataset` маппит `data-*` атрибуты: `el.dataset.price` ↔ `data-price`
- Кэшируй частые `querySelector` в переменные — меньше обходов DOM

### Практика
1. Подключи JS к лендингу, выбери заголовок и измени `textContent`
2. По клику на кнопку меняй класс `theme-dark` на `document.documentElement`
3. Динамически создай 5 элементов списка через `createElement` + `append`
4. Удали элемент через `remove()`
5. Читай data-атрибуты: `data-price` на карточках товаров
6. Создай `week-06/index.html` — заготовка Todo App
7. Вынеси DOM-ссылки в объект `elements = { form, list, input }`

**Критерии:**
- [ ] Используется `querySelector`, не устаревшие методы без причины
- [ ] `textContent` для текста, не `innerHTML` с пользовательскими данными
- [ ] Элементы создаются через DOM API, не строками HTML

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 06 day 3: dom manipulation"`

## День 4 (Thu): События — основы

### Теория
- [learn.javascript.ru: Введение в события](https://learn.javascript.ru/introduction-browser-events)
- `addEventListener('click', handler)` vs inline `onclick`
- Event object: `target`, `currentTarget`, `preventDefault`, `stopPropagation`
- Фазы: capturing, target, bubbling
- `{ once: true }`, `{ passive: true }` — опции
- Bubbling: событие всплывает от target к document — основа делегирования
- `preventDefault()` отменяет действие браузера (submit, ссылка), не останавливает всплытие
- `addEventListener` позволяет несколько обработчиков; `onclick` перезаписывает
- Именованная функция нужна для `removeEventListener` — анонимную не снять

### Практика
1. Кнопка «Наверх» — плавный скролл (пока `window.scrollTo`, событие click)
2. Форма: `submit` → `preventDefault()`, вывод данных в Console
3. Делегирование: один listener на `ul`, обработка кликов по `li`
4. Клавиатура: `keydown` — закрытие модалки по Escape
5. Удали listener через `removeEventListener` (именованная функция)
6. Добавь `stopPropagation` на вложенной кнопке — наблюдай разницу
7. Подключи `{ passive: true }` на scroll listener (если добавишь)

**Критерии:**
- [ ] `preventDefault` на форме предотвращает перезагрузку
- [ ] Event delegation на списке
- [ ] Именованные handler-функции для removeEventListener

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 06 day 4: events delegation"`

## День 5 (Fri): Интерактивный UI

### Теория
- [learn.javascript.ru: Действия браузера](https://learn.javascript.ru/default-browser-action)
- Toggle visibility: `hidden`, `aria-hidden`, класс `.is-open`
- Tab-интерфейс: переключение активного таба
- Модальное окно: focus trap (базово), закрытие по overlay
- `event.target.closest('.card')` — паттерн делегирования
- `hidden` и `aria-hidden` вместе — скрытие и для скринридеров
- Focus trap в модалке: Tab не уходит за пределы диалога
- `closest` поднимается по DOM от клика — удобно для карточек и строк списка
- Блокировка `body { overflow: hidden }` при открытой модалке — нет скролла фона

### Практика
1. Аккордеон: 3 секции, открыта одна; клик переключает
2. Табы: панели контента показываются по активному табу
3. Модалка «Подписаться» — открытие/закрытие, блокировка скролла body
4. Счётчик лайков на карточках с делегированием
5. Добавь `aria-expanded` на кнопки аккордеона
6. Закрой модалку по клику на overlay и по Escape
7. Переключи таб с клавиатуры (стрелки или Tab)

**Критерии:**
- [ ] Аккордеон и табы работают без библиотек
- [ ] Модалка закрывается по Escape и клику вне
- [ ] ARIA-атрибуты на интерактивных элементах

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 06 day 5: accordion tabs modal"`

## День 6 (Sat): Формы и валидация на JS

### Теория
- [learn.javascript.ru: Формы, элементы управления](https://learn.javascript.ru/forms-controls)
- `form.elements`, `FormData`, `input.value`, `checkbox.checked`
- События: `input`, `change`, `submit`
- Constraint Validation API: `validity`, `setCustomValidity`
- Показ ошибок рядом с полями
- `input` срабатывает на каждый символ; `change` — при потере фокуса или выборе
- `setCustomValidity('текст')` переопределяет сообщение браузера
- `form.checkValidity()` программная проверка перед submit
- Ошибки рядом с полем (`aria-describedby`) — лучше, чем один alert

### Практика
1. Валидация формы регистрации перед отправкой
2. Live-валидация email при `input`
3. Пароли должны совпадать — `setCustomValidity` при несовпадении
4. Вывод ошибок в `<span class="error">` под полями
5. При успехе — сообщение «Регистрация успешна» без перезагрузки
6. Свяжи ошибки с полями через `aria-describedby`
7. Disable кнопку submit, пока форма невалидна

**Критерии:**
- [ ] HTML5 + JS валидация работают вместе
- [ ] Ошибки понятны и привязаны к полям
- [ ] Форма не сабмитится при невалидных данных

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 06 day 6: form validation"`

## День 7 (Sun): DOM-проект — интерактивный лендинг

### Теория
- Разделение: data / logic / DOM (базовый MVC)
- `DocumentFragment` для batch insert
- `requestAnimationFrame` — обзор для анимаций
- Производительность: минимизируй reflow, кэшируй DOM-ссылки
- Data layer не знает о DOM — массив задач отдельно от `renderTasks()`
- `DocumentFragment` — один reflow вместо N при вставке списка
- Частые чтения layout + записи style вызывают thrashing — группируй операции
- `render*` функции принимают data и обновляют DOM — единая точка отрисовки

### Практика
1. Оживи лендинг: тёмная тема, мобильное меню, плавный скролл к секциям
2. Фильтр портфолио: кнопки категорий скрывают/показывают карточки
3. Счётчик «осталось мест» с анимацией числа
4. Рефакторинг: вынеси DOM-операции в функции `render*`
5. Протестируй весь UI с клавиатуры
6. Собери Todo App: add, delete, toggle, filter — без innerHTML для input
7. Финальный коммит и тег `week-06-done`

**Критерии:**
- [ ] Минимум 5 интерактивных фич
- [ ] Код структурирован: utils, dom, app
- [ ] Нет ошибок в Console при типичном сценарии

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 06 day 7: dom todo app final"`

## Проект недели

**Интерактивный Todo App** — одностраничное приложение с DOM.

Подробное описание: [docs/projects.md — Неделя 6](../../docs/projects.md#неделя-6--dom-todo-app)

Функции: добавление, удаление, toggle done, фильтр (all/active/done), счётчик, localStorage (заготовка на след. неделю).

**Критерии проекта:**
- [ ] CRUD задач через DOM, не innerHTML с user input
- [ ] Event delegation на списке задач
- [ ] Фильтры и счётчик активных
- [ ] Доступность: labels, keyboard, aria на toggle
- [ ] Папка `week-06/` с README и скриншотом
- [ ] Форма добавления с валидацией пустого ввода
- [ ] Кнопка «Очистить выполненные» через filter + re-render
- [ ] Код разделён: `app.js`, `dom.js`, `tasks.js` (или аналог)
- [ ] Тег `week-06-done` на финальном коммите

## Ревью-чеклист
- Разница `textContent` и `innerHTML`? Когда опасен innerHTML?
- Что такое event bubbling и зачем делегирование?
- Как предотвратить перезагрузку страницы при submit?
- Как скопировать объект без мутации оригинала (shallow)?
- Могу ли я создать элемент и добавить его в DOM с нуля?
