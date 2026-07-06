# Неделя 1: HTML — структура, семантика, формы, a11y

> **Цель недели:** научиться создавать валидные, семантические HTML-страницы с формами и базовой доступностью — и **с первого дня** вести код в Git.
> **Проект недели:** [Portfolio Landing](../../docs/projects.md#неделя-1--portfolio-landing) — 3 страницы, форма, a11y ≥ 90.
> **Git:** репозиторий `learning-log` создаётся в **день 1**; первый коммит — `index.html`. К концу недели ≥ 7 коммитов, тег `week-01-done`.

### Литература (обязательно + по желанию)

| Приоритет | Источник | Главы / разделы |
|-----------|----------|-----------------|
| ★★★ | Ионетт Дакетт «HTML и CSS» | гл. 1–6 |
| ★★★ | [MDN Learn HTML](https://developer.mozilla.org/ru/docs/Learn/HTML) | весь трек |
| ★★ | [web.dev Learn HTML](https://web.dev/learn/html) | семантика, формы |
| ★★ | Scott Chacon «Pro Git» | [гл. 1–2](https://git-scm.com/book/ru/v2) — основы и коммиты |
| ★ | [HTML5 Doctor](http://html5doctor.com/) | семантические элементы |
| ★ | [A11y Project Checklist](https://www.a11yproject.com/checklist/) | доступность |

---

## День 0 (до понедельника): Git и GitHub — подготовка

> Если Git уже установлен и аккаунт GitHub есть — пройди чеклист и переходи к дню 1.

### Теория
- [Pro Git: Введение](https://git-scm.com/book/ru/v2/Введение-О-системе-контроля-версий) — зачем VCS: история, откат, ветки
- Git хранит **снимки** файлов, а не патчи — каждый коммит = слепок проекта
- GitHub — удалённое зеркало + портфолио; публичный `learning-log` видят рекрутеры
- Три зоны: **working directory** → `git add` → **staging** → `git commit` → **repository**

### Практика
1. Установи [Git](https://git-scm.com/downloads), проверь: `git --version`
2. Настрой имя и email (они попадут в каждый коммит):
   ```bash
   git config --global user.name "Твоё Имя"
   git config --global user.email "you@example.com"
   ```
3. Создай аккаунт на [GitHub](https://github.com/) если нет
4. Создай **пустой** публичный репозиторий `learning-log` (без README — добавишь локально)
5. Склонируй: `git clone https://github.com/YOUR_USER/learning-log.git`
6. Создай `.gitignore` в корне:
   ```
   .DS_Store
   Thumbs.db
   .env
   *.log
   node_modules/
   ```
7. Первый коммит инфраструктуры:
   ```bash
   cd learning-log
   git add .gitignore
   git commit -m "chore: init learning-log with gitignore"
   git push -u origin main
   ```

**Критерии:**
- [ ] `git status` работает в папке `learning-log`
- [ ] Репозиторий виден на GitHub
- [ ] `.gitignore` закоммичен

---

## День 1 (Mon): Структура документа, первый index.html, первый коммит страницы

### Теория
- [MDN: Введение в HTML](https://developer.mozilla.org/ru/docs/Learn/HTML/Introduction_to_HTML) — разметка описывает **смысл**, браузер строит **DOM-дерево**
- `<!DOCTYPE html>` — режим standards; без него возможен quirks mode
- `head`: метаданные (`charset`, `viewport`, `title`); `body`: видимый контент
- Блочные элементы (`div`, `p`, `h1`–`h6`, `ul`) занимают строку; строчные (`span`, `a`, `img`) — внутри строки
- `h1`–`h6` — **иерархия**, не размер шрифта; на странице один логический `h1`
- Атрибуты: `id` (уникальный якорь), `class` (группа стилей), `href`, `src`, `alt` (обязателен для смысла картинки)

### Практика
1. В `learning-log` создай папку `week-01/`
2. Файл `week-01/index.html` — корректный DOCTYPE, `lang="ru"`, `meta charset="UTF-8"`, `viewport`
3. Секции: шапка с именем, `nav` из 3 якорных ссылок (`#about`, `#skills`, `#contact`)
4. Блоки «О себе», «Навыки» (`ul`), «Контакты» (`p` + ссылка `mailto:`)
5. Изображение-аватар с осмысленным `alt`; внешняя ссылка GitHub с `target="_blank"` `rel="noopener noreferrer"`
6. Live Server → DevTools → Elements: найди DOM-узлы, соответствующие тегам
7. [validator.w3.org](https://validator.w3.org/) — 0 errors
8. В `week-01/README.md` — 3 предложения: что за страница, как открыть локально

**Критерии:**
- [ ] Валидный HTML
- [ ] Один `h1`, логичные `h2`
- [ ] У `img` есть `alt`

### Git
```bash
cd learning-log
git add week-01/index.html week-01/README.md
git commit -m "week 01 day 1: first portfolio index.html with semantic sections"
git push
```
Это твой **первый коммит кода** — зафиксируй дату в `journal.md` (создай в корне, если ещё нет).

### Ловушки
- Пропуск DOCTYPE → непредсказуемая вёрстка в старых браузерах
- `h3` сразу после `h1` без `h2` — плохой document outline
- `div` внутри `p` — невалидная вложенность

---

## День 2 (Tue): Семантическая разметка

### Теория
- [MDN: Семантика](https://developer.mozilla.org/ru/docs/Glossary/Semantics) — тег несёт смысл для браузера, скринридера, SEO
- Landmark-роли: `header`, `nav`, `main`, `footer` — навигация с клавиатуры и AT
- `section` — тематическая группа с заголовком; `article` — самодостаточный контент (пост, карточка)
- `aside` — дополнение к `main`, не основной поток
- `figure` + `figcaption` — иллюстрация с подписью; `time datetime="2026-07-06"` — машиночитаемая дата

### Практика
1. Рефакторинг `index.html`: убери «суп из div», введи `header`, `nav`, `main`, `section`, `footer`
2. `article` — мини-пост «Почему я учу веб» с `time`
3. `aside` — список «Сейчас изучаю: HTML, Git»
4. HeadingsMap или DevTools Accessibility — проверь outline
5. Сравни diff в Git: `git diff` до коммита — видишь только структурные изменения?

**Критерии:**
- [ ] Один `main` на страницу
- [ ] `nav` только для навигации
- [ ] Структура читается без CSS

### Git
```bash
git add week-01/index.html
git commit -m "week 01 day 2: refactor to semantic landmarks and article"
git push
```

---

## День 3 (Wed): Ссылки, изображения, медиа

### Теория
- Относительные пути: `./about.html`, `../images/photo.jpg` — переносимость проекта
- `img`: всегда `alt`; декоративное — `alt=""`; не дублируй подпись в `alt` и `figcaption`
- `loading="lazy"` — отложенная загрузка ниже fold
- `srcset` + `sizes` — responsive images без лишних байт
- `video`: `controls`, `poster`, вложенный текст для fallback

### Практика
1. `week-01/about.html`, `week-01/gallery.html` — единый `header`/`nav`/`footer`
2. Относительные ссылки между страницами + якоря `#section-id`
3. Галерея 4+ `figure` с WebP/JPG, lazy loading
4. Одно `video` с `poster` (короткий клип о себе или placeholder)
5. Lighthouse Accessibility на `index.html`
6. Обнови `nav` на всех страницах — активная страница через `aria-current="page"` на текущей ссылке

**Критерии:**
- [ ] Нет битых ссылок
- [ ] Внешние ссылки с `rel="noopener noreferrer"`
- [ ] `aria-current` на активном пункте nav

### Git
```bash
git add week-01/
git commit -m "week 01 day 3: multi-page site with gallery and media"
git push
```

---

## День 4 (Thu): Формы — основы

### Теория
- [MDN: Your first form](https://developer.mozilla.org/ru/docs/Learn/Forms/Your_first_form)
- `form` без `action` — отправка на тот же URL (для статики достаточно для демо)
- `label[for]` ↔ `input[id]` — клик по label фокусирует поле; критично для a11y
- `name` — ключ в данных формы при submit
- `button type="submit"` vs `type="button"` — вторая кнопка в форме по умолчанию submit!

### Практика
1. На `contact.html` — форма: имя, email, тема (`select`), сообщение (`textarea`)
2. Radio «Способ связи», checkbox «Согласие» с `required`
3. Каждое поле с видимым `label`
4. `fieldset`/`legend` для группы radio
5. Submit — посмотри в DevTools → Network что ушло бы (или закрой форму `onsubmit="return false"` для статики)

**Критерии:**
- [ ] Все поля с labels
- [ ] Radio с общим `name`
- [ ] `email` type даёт нативную валидацию

### Git
```bash
git add week-01/contact.html week-01/
git commit -m "week 01 day 4: contact form with labels and fieldsets"
git push
```

---

## День 5 (Fri): Валидация форм

### Теория
- [MDN: Form validation](https://developer.mozilla.org/ru/docs/Learn/Forms/Form_validation)
- Constraint validation API: `validity`, `validationMessage`, `:invalid` в CSS
- `required`, `minlength`, `pattern` — клиентская валидация до JS
- `placeholder` ≠ `label` — placeholder исчезает при вводе
- `datalist` — подсказки без ограничения свободного ввода

### Практика
1. Форма регистрации на отдельной секции или `register.html`
2. Пароль `minlength="8"`, логин `pattern="[A-Za-z0-9_]{3,20}"`
3. Два `fieldset`: «Личные данные», «Учётные данные»
4. `datalist` для города (5+ городов)
5. Тест: пустая отправка, неверный email, короткий пароль — браузер блокирует

**Критерии:**
- [ ] Нативная валидация без JS
- [ ] `placeholder` не единственная подпись
- [ ] Понятные `title` у полей с `pattern`

### Git
```bash
git add week-01/
git commit -m "week 01 day 5: registration form with HTML5 validation"
git push
```

### Ловушки
- Две кнопки submit в одной форме
- `type="number"` для телефона — лучше `type="tel"`

---

## День 6 (Sat): Доступность (a11y)

### Теория
- [web.dev: Learn Accessibility](https://web.dev/learn/accessibility) — POUR: Perceivable, Operable, Understandable, Robust
- Клавиатура: Tab order = порядок в DOM; не ломай `tabindex` без причины
- Skip link: первый фокусируемый элемент → `#main-content`
- Контраст WCAG AA: 4.5:1 для обычного текста
- ARIA только когда нативного HTML недостаточно

### Практика
1. Пройди все страницы только Tab/Enter/Space
2. Skip-link в начале `body` на каждой странице
3. [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) — исправь слабый контраст (временный inline style допустим)
4. Lighthouse a11y ≥ 90 на `index.html`
5. Запиши в `week-01/A11Y.md` — 5 найденных проблем и как исправил

**Критерии:**
- [ ] Skip-link работает
- [ ] Видимый `:focus-visible` на ссылках
- [ ] Lighthouse ≥ 90

### Git
```bash
git add week-01/
git commit -m "week 01 day 6: accessibility fixes and A11Y audit doc"
git push
```

---

## День 7 (Sun): Таблицы, метаданные, проект недели

### Теория
- [MDN: Tables](https://developer.mozilla.org/ru/docs/Learn/HTML/Tables) — `th scope="col|row"`, `caption`
- Таблицы для **данных**, не для layout
- `meta name="description"`, Open Graph для шаринга
- Favicon: `link rel="icon"` 32×32 или SVG

### Практика
1. Таблица «План обучения» (неделя, тема, статус) на `index.html`
2. Уникальные `title` и `description` на каждой странице
3. OG-теги на главной, favicon
4. Финальный прогон W3C + Lighthouse на всех HTML
5. **Собери проект недели** — чеклист ниже
6. `notes.md` в `week-01/`: 5 правил хорошего HTML своими словами

**Критерии:**
- [ ] Таблица с `thead`/`tbody`/`th`
- [ ] Все страницы валидны
- [ ] Проект недели выполнен

### Git
```bash
git add week-01/
git commit -m "week 01 day 7: tables, meta, favicon, week project complete"
git tag -a week-01-done -m "Portfolio Landing complete"
git push && git push --tags
```

---

## Проект недели: Portfolio Landing

Полное ТЗ: [docs/projects.md#неделя-1--portfolio-landing](../../docs/projects.md#неделя-1--portfolio-landing)

**Итоговые требования:**
- 3+ связанные страницы, единая навигация с `aria-current`
- Форма контакта + форма регистрации с валидацией
- Галерея, таблица навыков/плана, skip-links
- Lighthouse a11y ≥ 90, W3C 0 errors
- `week-01/README.md` со скриншотом и инструкцией запуска
- ≥ 7 коммитов за неделю, тег `week-01-done`

**Критерии проекта:**
- [ ] Демо можно открыть через Live Server или GitHub Pages
- [ ] Рекрутер понимает структуру без объяснений
- [ ] `git log --oneline week-01/` показывает осмысленную историю

## Ревью-чеклист
- Объясняю разницу `div` vs `section` vs `article`?
- Знаю, когда `alt=""` уместен?
- Связал `label[for]` с полем?
- Настроил Git и сделал первый коммит `index.html` в день 1?
- Могу проверить страницу валидатором и Lighthouse без подсказок?
