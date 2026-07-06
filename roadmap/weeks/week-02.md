# Неделя 2: CSS — селекторы, box model, типографика, переменные

> **Цель недели:** освоить фундамент CSS — от селекторов до типографики и кастомных свойств.
> **Литература:** Ионетт Дакетт «HTML и CSS» (гл. 10–13), [MDN Learn CSS](https://developer.mozilla.org/ru/docs/Learn/CSS), [CSS Reference](https://developer.mozilla.org/ru/docs/Web/CSS/Reference)

## День 1 (Mon): Подключение CSS и селекторы

### Теория
- [MDN: CSS first steps](https://developer.mozilla.org/ru/docs/Learn/CSS/First_steps) — inline, `<style>`, внешний файл
- Селекторы: элемент, `.class`, `#id`, `[attr]`, `*`, группировка через запятую
- Комбинаторы: потомок (пробел), дочерний `>`, соседний `+`, общий `~`
- Псевдоклассы: `:hover`, `:focus`, `:nth-child()`, `:not()`
- Псевдоэлементы: `::before`, `::after`, `::placeholder`

### Практика
1. Создай `styles.css` и подключи к HTML из недели 1
2. Стилизуй навигацию: базовый вид, `:hover`, `:focus-visible`
3. Чередуй фон строк в списке через `:nth-child(even)`
4. Добавь декоративный `::before` к заголовкам секций
5. В DevTools поэкспериментируй с селекторами в панели Styles

**Критерии:**
- [ ] CSS вынесен во внешний файл, нет inline-стилей в HTML
- [ ] Использованы минимум 3 типа селекторов
- [ ] Состояния `:hover` и `:focus-visible` различимы

## День 2 (Tue): Каскад, специфичность и наследование

### Теория
- [MDN: Cascade and inheritance](https://developer.mozilla.org/ru/docs/Learn/CSS/Building_blocks/Cascade_and_inheritance)
- Специфичность: inline > ID > class > элемент; `!important` — крайняя мера
- Наследуемые свойства (`color`, `font-family`) vs ненаследуемые (`margin`, `border`)
- `inherit`, `initial`, `unset`, `revert`
- Порядок правил при равной специфичности — побеждает последний

### Практика
1. Создай конфликт специфичности: стилизуй `p` тремя способами, предскажи результат
2. Проверь предсказание в браузере, зафиксируй в комментарии CSS
3. Используй `inherit` для единообразия цвета ссылок внутри `footer`
4. Убери лишние `!important` если появились — перепиши селекторы
5. Изучи Computed styles в DevTools для одного элемента

**Критерии:**
- [ ] Могу объяснить, какое правило победит в конфликте
- [ ] Нет `!important` без веской причины
- [ ] Наследование используется осознанно

### Ловушки
- Война специфичности: цепочки `#id .class div span` — признак плохого CSS
- `!important` лечит симптом, не причину
- Стилизация через ID — хрупко при рефакторинге

## День 3 (Wed): Box Model

### Теория
- [MDN: Box model](https://developer.mozilla.org/ru/docs/Learn/CSS/Building_blocks/The_box_model)
- `content` → `padding` → `border` → `margin`; `box-sizing: border-box`
- `width`/`height`, `min-*`, `max-*`, `overflow: hidden/auto/scroll`
- Схлопывание margin: вертикальные margin соседних блоков
- `display`: `block`, `inline`, `inline-block`, `none`

### Практика
1. Нарисуй на бумаге box model для карточки, затем сверстай её
2. Примени `box-sizing: border-box` глобально через `*, *::before, *::after`
3. Создай три карточки с одинаковой шириной, разным padding — проверь выравнивание
4. Продемонстрируй margin collapse двумя блоками с вертикальными отступами
5. В DevTools включи overlay box model для визуализации

**Критерии:**
- [ ] `border-box` подключён глобально
- [ ] Карточки визуально одинаковой ширины при разном padding
- [ ] Понимаю разницу `inline` vs `inline-block`

## День 4 (Thu): Типографика и текст

### Теория
- [MDN: Typography](https://developer.mozilla.org/ru/docs/Learn/CSS/Styling_text)
- `font-family`, стеки шрифтов, `font-size`, `font-weight`, `line-height`
- [web.dev: Learn Typography](https://web.dev/learn/css/typography) — вертикальный ритм
- `text-align`, `text-decoration`, `letter-spacing`, `text-transform`
- Подключение веб-шрифтов: Google Fonts, `font-display: swap`

### Практика
1. Подключи пару шрифтов (заголовки + текст) через Google Fonts
2. Задай базовый `font-size: 16px`, `line-height: 1.6` для `body`
3. Настрой иерархию заголовков: размер, вес, отступы
4. Ограничь ширину текстового блока `max-width: 65ch` для читаемости
5. Стилизуй цитату: `blockquote`, курсив, левая граница

**Критерии:**
- [ ] Текст читаем на мобильном и десктопе
- [ ] Не более 2–3 семейств шрифтов на странице
- [ ] `line-height` задан для основного текста

## День 5 (Fri): Цвета, фоны и тени

### Теория
- Форматы цвета: hex, `rgb()`, `hsl()`, `oklch()` — [MDN color](https://developer.mozilla.org/ru/docs/Web/CSS/color_value)
- `background-color`, `background-image`, `linear-gradient`, `background-size: cover`
- `border`, `border-radius`, `box-shadow`, `opacity` vs `rgba`/`hsla`
- `filter: drop-shadow()` — отличие от `box-shadow`

### Практика
1. Создай hero-секцию с градиентным фоном и полупрозрачным оверлеем
2. Стилизуй кнопки: обычное, hover, active состояния с плавным переходом цвета
3. Добавь карточкам `border-radius` и лёгкую `box-shadow`
4. Проверь контраст текста на фоне (минимум 4.5:1 для обычного текста)
5. Сделай тёмный вариант hero через другой градиент (подготовка к переменным)

**Критерии:**
- [ ] Контраст текста соответствует WCAG AA
- [ ] Градиент не мешает читаемости
- [ ] Кнопки имеют distinct states

## День 6 (Sat): CSS-переменные (Custom Properties)

### Теория
- [MDN: Using CSS custom properties](https://developer.mozilla.org/ru/docs/Web/CSS/Using_CSS_custom_properties)
- Объявление: `--color-primary: #3366cc` в `:root`
- Использование: `color: var(--color-primary, fallback)`
- Переменные наследуются — можно переопределять в `.dark-theme`
- Разница между CSS variables и препроцессорными `$variables`

### Практика
1. Вынеси палитру в `:root`: primary, secondary, text, bg, border
2. Переведи все цвета страницы на `var(--...)`
3. Создай класс `.theme-dark` с переопределением переменных в `html` или `body`
4. Добавь кнопку переключения темы (пока через класс на `html`, без JS — второй HTML-файл)
5. Задай `--spacing-sm/md/lg` и используй для отступов

**Критерии:**
- [ ] Нет «магических» hex-значений вне `:root`
- [ ] Тёмная тема работает через переопределение переменных
- [ ] Есть fallback у критичных `var()`

## День 7 (Sun): Единицы измерения и финальная стилизация

### Теория
- [MDN: CSS values and units](https://developer.mozilla.org/ru/docs/Learn/CSS/Building_blocks/Values_and_units)
- Абсолютные: `px`; относительные: `em`, `rem`, `%`, `vw`, `vh`, `ch`
- Когда `rem` лучше `em` для `font-size` и spacing
- `clamp(min, preferred, max)` — адаптивный размер без media queries

### Практика
1. Переведи все `font-size` на `rem` (база 16px в `html`)
2. Отступы секций задай через `rem` или spacing-переменные
3. Заголовок hero сделай через `clamp(1.5rem, 4vw, 3rem)`
4. Полностью стилизуй лендинг недели 1 — он должен выглядеть профессионально
5. Прогони Lighthouse Best Practices и исправь замечания

**Критерии:**
- [ ] Размеры шрифтов в `rem`, не в произвольных `px`
- [ ] Страница выглядит цельно: палитра, типографика, отступы
- [ ] Lighthouse Performance ≥ 85 на статике

## Проект недели

**Стилизованный блог-пост** — одна HTML-страница статьи с богатой типографикой и дизайн-системой на CSS-переменных.

Требования:
- Дизайн-токены в `:root` (цвета, шрифты, spacing, radius)
- Hero, article body, sidebar, footer; card-компонент для «похожих статей»
- Тёмная тема через класс и переменные
- `clamp()` для заголовка, `max-width: 65ch` для текста

**Критерии проекта:**
- [ ] Единая система переменных, нет разбросанных литералов
- [ ] Контраст и типографика на уровне профессионального блога
- [ ] Адаптивность базового уровня (читаемо на 375px)
- [ ] Код CSS структурирован комментариями по секциям

## Ревью-чеклист
- Могу ли я вычислить специфичность селектора `#nav .item a:hover`?
- В чём разница `content-box` и `border-box`?
- Почему для `font-size` предпочтительнее `rem`, а не `px`?
- Как переопределить CSS-переменную для дочернего элемента?
- Могу ли я объяснить каскад без обращения к документации?
