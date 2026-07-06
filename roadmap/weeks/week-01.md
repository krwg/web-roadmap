# Неделя 1: HTML — структура, семантика, формы, a11y

> **Цель недели:** научиться создавать валидные, семантические HTML-страницы с формами и базовой доступностью.
> **Литература:** Ионетт Дакетт «HTML и CSS» (гл. 1–6), [MDN Learn HTML](https://developer.mozilla.org/ru/docs/Learn/HTML), [web.dev Learn HTML](https://web.dev/learn/html)

## День 1 (Mon): Структура документа и базовые теги

### Теория
- [MDN: Введение в HTML](https://developer.mozilla.org/ru/docs/Learn/HTML/Introduction_to_HTML) — что такое разметка и DOM-дерево
- Обязательная структура: `<!DOCTYPE html>`, `html`, `head`, `body`, `meta charset`, `title`
- Блочные и строчные элементы: `h1`–`h6`, `p`, `div`, `span`, `ul/ol/li`, `a`, `img`
- Атрибуты: `id`, `class`, `href`, `src`, `alt` — зачем каждый нужен

### Практика
1. Создай папку `week-01` и файл `index.html` с корректным DOCTYPE
2. Добавь секции: шапка с именем, навигация из 3 якорных ссылок, «О себе», «Навыки» (список), «Контакты»
3. Вставь изображение с осмысленным `alt`, добавь внешнюю ссылку с `target="_blank"` и `rel="noopener"`
4. Открой через Live Server, изучи DOM в DevTools → Elements
5. Проверь страницу на [validator.w3.org](https://validator.w3.org/)

**Критерии:**
- [ ] Валидный HTML без ошибок валидатора
- [ ] Корректная иерархия заголовков (один `h1`, логичные `h2`)
- [ ] У каждого `img` есть `alt`

### Ловушки
- Пропуск `<!DOCTYPE html>` включает quirks mode в старых браузерах
- Использование `h1`–`h6` только для размера шрифта — размер задаёт CSS
- Невалидная вложенность: блочный элемент внутри `p`

## День 2 (Tue): Семантическая разметка

### Теория
- [MDN: Семантика](https://developer.mozilla.org/ru/docs/Glossary/Semantics) — смысл тега важнее внешнего вида
- Структурные теги: `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`
- [learn.javascript.ru: Семантика в HTML](https://learn.javascript.ru/intro) — связь HTML и доступности
- `figure`, `figcaption`, `time`, `address` — когда применять

### Практика
1. Перепиши страницу «Обо мне» без «супа из div» — используй семантические теги
2. Добавь `article` с мини-постом (заголовок, дата через `time`, текст)
3. Вынеси боковую панель в `aside` со списком ссылок
4. Проверь outline документа в DevTools или расширении HeadingsMap
5. Сравни читаемость кода «до» и «после» рефакторинга

**Критерии:**
- [ ] `main` содержит уникальный контент страницы (один на страницу)
- [ ] `nav` оборачивает только навигационные ссылки
- [ ] Структура понятна без просмотра CSS

## День 3 (Wed): Ссылки, изображения и медиа

### Теория
- [MDN: Ссылки](https://developer.mozilla.org/ru/docs/Learn/HTML/Introduction_to_HTML/Creating_hyperlinks) — относительные и абсолютные пути
- `img`: `src`, `alt`, `width`/`height`, `loading="lazy"`, форматы WebP/AVIF
- [MDN: Responsive images](https://developer.mozilla.org/ru/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images) — `srcset`, `sizes`
- `picture`, `audio`, `video` — базовое встраивание медиа

### Практика
1. Создай многостраничный мини-сайт: `index.html`, `about.html`, `gallery.html`
2. Настрой относительные ссылки между страницами и якоря `#section-id`
3. Добавь галерею из 4+ изображений с `alt` и lazy loading
4. Вставь одно видео с `controls` и постером (`poster`)
5. Проверь все ссылки вручную и через Lighthouse → Accessibility

**Критерии:**
- [ ] Нет битых ссылок и путей к изображениям
- [ ] Внешние ссылки с `rel="noopener noreferrer"`
- [ ] Изображения не ломают вёрстку (заданы размеры или aspect-ratio)

## День 4 (Thu): Формы — основы

### Теория
- [MDN: Your first form](https://developer.mozilla.org/ru/docs/Learn/Forms/Your_first_form)
- Элементы: `form`, `label`, `input`, `textarea`, `select`, `option`, `button`
- Типы `input`: `text`, `email`, `password`, `number`, `checkbox`, `radio`, `date`
- Связка `label[for]` ↔ `input[id]`, атрибут `name` для отправки данных

### Практика
1. Сверстай форму обратной связи: имя, email, тема (`select`), сообщение (`textarea`)
2. Добавь radio-группу «Способ связи» и checkbox «Согласие на обработку»
3. Каждое поле оберни в `label` или свяжи через `for`/`id`
4. Кнопки: `type="submit"` и `type="reset"` — проверь поведение
5. Открой форму в браузере, заполни и посмотри данные в DevTools (без JS)

**Критерии:**
- [ ] Все поля имеют видимые или скрытые (`aria-label`) подписи
- [ ] Radio с одинаковым `name` работают как группа
- [ ] `email`-поле показывает нативную валидацию при неверном формате

## День 5 (Fri): Формы — валидация и атрибуты

### Теория
- [MDN: Form validation](https://developer.mozilla.org/ru/docs/Learn/Forms/Form_validation)
- HTML5-атрибуты: `required`, `min`, `max`, `minlength`, `maxlength`, `pattern`
- `fieldset` и `legend` для группировки полей
- `datalist`, `placeholder` — разница между подсказкой и меткой

### Практика
1. Создай форму регистрации: логин, email, пароль, подтверждение пароля, возраст
2. Добавь `required`, `minlength="8"` для пароля, `pattern` для логина (латиница)
3. Сгруппируй «Личные данные» и «Учётные данные» через `fieldset`/`legend`
4. Настрой `datalist` для поля «Город» (5+ вариантов)
5. Протестируй отправку с пустыми и невалидными полями — браузер должен блокировать

**Критерии:**
- [ ] Нативная валидация срабатывает до отправки
- [ ] Сообщения об ошибках понятны (при необходимости — `title` у `pattern`)
- [ ] `placeholder` не заменяет `label`

### Ловушки
- `placeholder` как единственная подпись поля — плохо для a11y
- `type="button"` vs `type="submit"` — вторая кнопка в форме сабмитит по умолчанию
- Забытый `name` — данные не попадут в запрос при отправке

## День 6 (Sat): Доступность (a11y)

### Теория
- [MDN: Accessibility](https://developer.mozilla.org/ru/docs/Learn/Accessibility)
- [web.dev: Learn Accessibility](https://web.dev/learn/accessibility) — WCAG-принципы POUR
- Клавиатурная навигация: `tabindex`, focus states, skip links
- ARIA: `aria-label`, `aria-labelledby`, `aria-describedby`, `role` — только когда HTML недостаточно
- Контраст текста, масштабирование до 200%

### Практика
1. Пройди по всем страницам недели только с клавиатуры (Tab, Enter, Space)
2. Добавь skip-link «Перейти к содержимому» в начало `body`
3. Проверь контраст цветов через DevTools или [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
4. Запусти Lighthouse Accessibility на главной — цель ≥ 90
5. Исправь найденные проблемы: отсутствующие labels, низкий контраст, пустые `alt`

**Критерии:**
- [ ] Все интерактивные элементы доступны с клавиатуры
- [ ] Видимый focus indicator на ссылках и кнопках
- [ ] Lighthouse Accessibility ≥ 90

## День 7 (Sun): Таблицы, метаданные и ревью

### Теория
- [MDN: HTML table basics](https://developer.mozilla.org/ru/docs/Learn/HTML/Tables/Basics) — `table`, `thead`, `tbody`, `th`, `td`, `scope`
- Метатеги: `description`, Open Graph (`og:title`, `og:image`) — зачем нужны
- [MDN: Document and website metadata](https://developer.mozilla.org/ru/docs/Learn/HTML/Introduction_to_HTML/The_head_metadata_in_HTML)
- Favicon: `link rel="icon"`

### Практика
1. Добавь на сайт таблицу расписания (3+ колонки, заголовки в `th` с `scope`)
2. Заполни `meta description` и базовые OG-теги в `head`
3. Подключи favicon
4. Прогони все HTML-файлы через валидатор и Lighthouse
5. Напиши в `notes.md` конспект: 5 правил хорошего HTML своими словами

**Критерии:**
- [ ] Таблица используется для данных, не для вёрстки
- [ ] У каждой страницы уникальный `title` и `description`
- [ ] Все файлы недели валидны

## Проект недели

**Лендинг портфолио** — многостраничный статический сайт (3 страницы) о себе как о начинающем разработчике.

Требования:
- Семантическая разметка, форма обратной связи с нативной валидацией
- Галерея работ (можно заглушки), таблица навыков или расписания обучения
- Skip-link, корректные `alt`, Lighthouse Accessibility ≥ 90
- Валидный HTML, favicon, meta description

**Критерии проекта:**
- [ ] 3 связанные страницы с единой навигацией
- [ ] Форма с `fieldset`, валидацией и доступными labels
- [ ] Пройден валидатор W3C без ошибок
- [ ] Код в репозитории с понятной структурой папок

## Ревью-чеклист
- Могу ли я объяснить разницу между `div` и `section`?
- Знаю ли я, зачем нужен `alt` и когда его оставить пустым (`alt=""`)?
- Понимаю ли я, как `label[for]` связан с полем формы?
- Могу ли я назвать 5 семантических тегов и их роль?
- Умею ли я проверить страницу на валидность и доступность без подсказок?
