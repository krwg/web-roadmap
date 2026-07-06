# Неделя 6: JavaScript — объекты, DOM, события

> **Цель недели:** освоить объекты JavaScript, манипуляции DOM и обработку пользовательских событий.
> **Литература:** [learn.javascript.ru: Объекты](https://learn.javascript.ru/object), [learn.javascript.ru: DOM](https://learn.javascript.ru/searching-elements-dom), [MDN DOM](https://developer.mozilla.org/ru/docs/Web/API/Document_Object_Model)

## День 1 (Mon): Объекты — основы

### Теория
- [learn.javascript.ru: Объекты](https://learn.javascript.ru/object) — литералы, свойства, методы
- Точечная и скобочная нотация: `obj.key`, `obj['key']`
- `delete`, `in`, `for...in` vs `for...of` для объектов
- Копирование: shallow copy `{...obj}`, `Object.assign`
- `Object.keys`, `Object.values`, `Object.entries`

### Практика
1. Объект `user` с полями name, email, age — чтение и изменение
2. Метод `user.greet()` — function внутри объекта
3. Перебери свойства через `Object.entries` и выведи пары ключ-значение
4. Shallow copy: измени копию, убедись что вложенный объект общий
5. Массив пользователей — 3+ объекта в массиве

**Критерии:**
- [ ] Объект с минимум одним методом
- [ ] Использованы keys/values/entries
- [ ] Понимаю shallow vs deep copy (на уровне концепции)

## День 2 (Tue): Деструктуризация и spread для объектов

### Теория
- [learn.javascript.ru: Деструктурирующее присваивание](https://learn.javascript.ru/destructuring-assignment)
- `const {name, age} = user`; переименование `{name: userName}`
- Значения по умолчанию при деструктуризации
- Spread в объектах: `{...defaults, ...overrides}`
- Rest в объектах: `const {id, ...rest} = product`

### Практика
1. Функция `printUser({name, email, role = 'user'})` — деструктуризация параметров
2. Объедини настройки: `const config = {...defaults, ...userConfig}`
3. Исключи поле `password` из объекта перед логированием (rest)
4. Swap двух переменных через деструктуризацию массива `[a, b] = [b, a]`
5. Рефакторинг Todo из недели 5 с деструктуризацией

**Критерии:**
- [ ] Деструктуризация в параметрах функций
- [ ] Spread для иммутабельного обновления объекта
- [ ] Rest для исключения полей

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

### Практика
1. Подключи JS к лендингу, выбери заголовок и измени `textContent`
2. По клику на кнопку меняй класс `theme-dark` на `document.documentElement`
3. Динамически создай 5 элементов списка через `createElement` + `append`
4. Удали элемент через `remove()`
5. Читай data-атрибуты: `data-price` на карточках товаров

**Критерии:**
- [ ] Используется `querySelector`, не устаревшие методы без причины
- [ ] `textContent` для текста, не `innerHTML` с пользовательскими данными
- [ ] Элементы создаются через DOM API, не строками HTML

## День 4 (Thu): События — основы

### Теория
- [learn.javascript.ru: Введение в события](https://learn.javascript.ru/introduction-browser-events)
- `addEventListener('click', handler)` vs inline `onclick`
- Event object: `target`, `currentTarget`, `preventDefault`, `stopPropagation`
- Фазы: capturing, target, bubbling
- `{ once: true }`, `{ passive: true }` — опции

### Практика
1. Кнопка «Наверх» — плавный скролл (пока `window.scrollTo`, событие click)
2. Форма: `submit` → `preventDefault()`, вывод данных в Console
3. Делегирование: один listener на `ul`, обработка кликов по `li`
4. Клавиатура: `keydown` — закрытие модалки по Escape
5. Удали listener через `removeEventListener` (именованная функция)

**Критерии:**
- [ ] `preventDefault` на форме предотвращает перезагрузку
- [ ] Event delegation на списке
- [ ] Именованные handler-функции для removeEventListener

## День 5 (Fri): Интерактивный UI

### Теория
- [learn.javascript.ru: Действия браузера](https://learn.javascript.ru/default-browser-action)
- Toggle visibility: `hidden`, `aria-hidden`, класс `.is-open`
- Tab-интерфейс: переключение активного таба
- Модальное окно: focus trap (базово), закрытие по overlay
- `event.target.closest('.card')` — паттерн делегирования

### Практика
1. Аккордеон: 3 секции, открыта одна; клик переключает
2. Табы: панели контента показываются по активному табу
3. Модалка «Подписаться» — открытие/закрытие, блокировка скролла body
4. Счётчик лайков на карточках с делегированием
5. Добавь `aria-expanded` на кнопки аккордеона

**Критерии:**
- [ ] Аккордеон и табы работают без библиотек
- [ ] Модалка закрывается по Escape и клику вне
- [ ] ARIA-атрибуты на интерактивных элементах

## День 6 (Sat): Формы и валидация на JS

### Теория
- [learn.javascript.ru: Формы, элементы управления](https://learn.javascript.ru/forms-controls)
- `form.elements`, `FormData`, `input.value`, `checkbox.checked`
- События: `input`, `change`, `submit`
- Constraint Validation API: `validity`, `setCustomValidity`
- Показ ошибок рядом с полями

### Практика
1. Валидация формы регистрации перед отправкой
2. Live-валидация email при `input`
3. Пароли должны совпадать — `setCustomValidity` при несовпадении
4. Вывод ошибок в `<span class="error">` под полями
5. При успехе — сообщение «Регистрация успешна» без перезагрузки

**Критерии:**
- [ ] HTML5 + JS валидация работают вместе
- [ ] Ошибки понятны и привязаны к полям
- [ ] Форма не сабмитится при невалидных данных

## День 7 (Sun): DOM-проект — интерактивный лендинг

### Теория
- Разделение: data / logic / DOM (базовый MVC)
- `DocumentFragment` для batch insert
- `requestAnimationFrame` — обзор для анимаций
- Производительность: минимизируй reflow, кэшируй DOM-ссылки

### Практика
1. Оживи лендинг: тёмная тема, мобильное меню, плавный скролл к секциям
2. Фильтр портфолио: кнопки категорий скрывают/показывают карточки
3. Счётчик «осталось мест» с анимацией числа
4. Рефакторинг: вынеси DOM-операции в функции `render*`
5. Протестируй весь UI с клавиатуры

**Критерии:**
- [ ] Минимум 5 интерактивных фич
- [ ] Код структурирован: utils, dom, app
- [ ] Нет ошибок в Console при типичном сценарии

## Проект недели

**Интерактивный Todo App** — одностраничное приложение с DOM.

Функции: добавление, удаление, toggle done, фильтр (all/active/done), счётчик, localStorage (заготовка на след. неделю).

**Критерии проекта:**
- [ ] CRUD задач через DOM, не innerHTML с user input
- [ ] Event delegation на списке задач
- [ ] Фильтры и счётчик активных
- [ ] Доступность: labels, keyboard, aria на toggle

## Ревью-чеклист
- Разница `textContent` и `innerHTML`? Когда опасен innerHTML?
- Что такое event bubbling и зачем делегирование?
- Как предотвратить перезагрузку страницы при submit?
- Как скопировать объект без мутации оригинала (shallow)?
- Могу ли я создать элемент и добавить его в DOM с нуля?
