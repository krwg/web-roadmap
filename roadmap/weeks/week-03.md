# Неделя 3: CSS — Flexbox, Grid, адаптив, анимации

> **Цель недели:** научиться строить современные макеты и адаптивные интерфейсы с Flexbox, Grid и анимациями.
> **Литература:** Ионетт Дакетт «HTML и CSS» (гл. 12–14), [CSS Tricks: Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/), [CSS Tricks: Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/), [web.dev Learn CSS](https://web.dev/learn/css), [Every Layout: Sidebar](https://every-layout.dev/layouts/sidebar/) — готовые адаптивные паттерны

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md#неделя-3--saas-landing)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-03/`

## День 1 (Mon): Flexbox — основы

### Теория
- [MDN: Flexbox](https://developer.mozilla.org/ru/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox)
- Контейнер: `display: flex`, `flex-direction`, `flex-wrap`, `gap`
- Выравнивание: `justify-content`, `align-items`, `align-content`
- Элементы: `flex-grow`, `flex-shrink`, `flex-basis`, сокращение `flex: 1`
- Flexbox — одномерный layout: выравнивает элементы вдоль главной оси (row или column)
- `gap` заменяет margin-хаки между элементами — чище и предсказуемее
- `align-items: stretch` (по умолчанию) растягивает детей по поперечной оси — карточки одной высоты
- `flex: 1` = `flex: 1 1 0%` — элемент занимает свободное пространство пропорционально

### Практика
1. Сверстай шапку сайта: логотип слева, навигация справа (`justify-content: space-between`)
2. Сделай ряд из 3 карточек одинаковой высоты с `align-items: stretch`
3. Центрируй блок по вертикали и горизонтали через flex на родителе
4. Поэкспериментируй с `flex-wrap` при сужении окна
5. Используй [Flexbox Froggy](https://flexboxfroggy.com/) — пройди 12+ уровней
6. Добавь `gap` вместо margin между карточками — сравни читаемость CSS
7. Попробуй `flex-direction: column` для мобильной шапки

**Критерии:**
- [ ] Шапка не ломается при 768px ширине
- [ ] Карточки одной высоты без фиксированного `height`
- [ ] Flexbox Froggy пройден

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 03 day 1: flexbox basics"`

## День 2 (Tue): Flexbox — практические паттерны

### Теория
- `order`, `align-self` — когда уместны (редко)
- Паттерн «Holy Grail» layout на flex
- `flex: 1 1 auto` vs `flex: 1 1 0` — разница в поведении
- Навигация, card footer с кнопкой внизу (`margin-top: auto`)
- `margin-top: auto` на последнем элементе карточки прижимает его к низу — без фиксированной высоты
- Holy Grail: `body { min-height: 100vh; display: flex; flex-direction: column }` + `main { flex: 1 }`
- `min-width: 0` на flex-ребёнке позволяет сжимать контент — иначе длинный текст ломает ряд
- `order` меняет визуальный порядок, но не tab-order — осторожно с a11y

### Практика
1. Карточка товара: изображение, заголовок, описание, цена, кнопка прижата к низу
2. Sticky footer: `body` как flex-column, `main { flex: 1 }`
3. Горизонтальный скролл галереи: `flex-wrap: nowrap`, `overflow-x: auto`
4. Pagination: ряд кнопок по центру с `gap`
5. Рефакторинг шапки: мобильное меню-иконка (пока без JS — скрытый блок)
6. Добавь `min-width: 0` на карточку с длинным текстом — проверь, что ряд не ломается
7. Сверстай card grid на flex с `flex-wrap` и `flex: 1 1 280px`

**Критерии:**
- [ ] Кнопка в карточке всегда внизу при разной длине текста
- [ ] Footer прижат к низу viewport на короткой странице
- [ ] Галерея скроллится горизонтально на мобильном

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 03 day 2: flexbox patterns"`

### Ловушки
- `flex: 1` на всех детях — не всегда равная ширина, смотри `flex-basis`
- Забытый `min-width: 0` — flex-элемент не сжимается, ломает вёрстку
- Вертикальное центрирование через margin auto вместо flex — устаревший подход

## День 3 (Wed): CSS Grid — основы

### Теория
- [MDN: Grid Layout](https://developer.mozilla.org/ru/docs/Web/CSS/CSS_grid_layout)
- `display: grid`, `grid-template-columns`, `grid-template-rows`, `gap`
- Единица `fr`, `repeat()`, `minmax()`
- `grid-column`, `grid-row`, `grid-area`
- `grid-template-areas` — именованные зоны
- Grid — двумерный layout: одновременно строки и колонки
- `1fr` распределяет свободное пространство пропорционально — удобнее процентов
- `grid-template-areas` делает макет читаемым: имена зон в CSS = карта страницы
- `span 2` растягивает элемент на несколько ячеек без лишней разметки

### Практика
1. Сетка 3×2 карточек через `grid-template-columns: repeat(3, 1fr)`
2. Макет страницы через areas: header, sidebar, main, footer
3. Один элемент растяни на 2 колонки (`grid-column: span 2`)
4. Пройди [Grid Garden](https://cssgridgarden.com/) — 12+ уровней
5. Сравни тот же макет на flex vs grid — запиши вывод
6. Добавь `minmax(200px, 1fr)` в колонки — проверь поведение при сужении
7. Нарисуй схему areas на бумаге, затем перенеси в CSS

**Критерии:**
- [ ] Grid Garden пройден
- [ ] Макет с areas читаем в CSS без HTML-подсказок
- [ ] Адаптив: при 600px — одна колонка

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 03 day 3: css grid basics"`

## День 4 (Thu): Grid — продвинутые макеты

### Теория
- `auto-fill` vs `auto-fit` с `minmax(250px, 1fr)` — responsive без media queries
- `subgrid` (базовое знакомство) — выравнивание вложенных сеток
- Наложение элементов через совпадающие grid-ячейки
- Когда grid, когда flex: grid для 2D, flex для 1D
- `auto-fill` оставляет пустые треки, `auto-fit` схлопывает их — визуальная разница на широком экране
- Grid stack: два элемента в одной ячейке — overlay-текст на изображении
- Вложенный grid внутри `main` — sidebar фиксирован, контент адаптивен
- Flex для навигации и кнопок, grid для карточных сеток — правило большинства макетов

### Практика
1. Галерея с `grid-template-columns: repeat(auto-fill, minmax(200px, 1fr))`
2. Dashboard: sidebar 250px, main `1fr`, виджеты внутри main — вложенный grid
3. Карточка с overlay-текстом поверх изображения (grid stack)
4. Pinterest-подобная сетка разной высоты (разный `grid-row: span N`)
5. Рефакторинг блога недели 2 на grid-layout
6. Сравни `auto-fill` и `auto-fit` на одной сетке — зафиксируй разницу скриншотом
7. Добавь `subgrid` (если браузер поддерживает) или запиши fallback

**Критерии:**
- [ ] Галерея адаптируется без единой media query
- [ ] Dashboard читаем на 1024px и 375px
- [ ] Осознанный выбор flex vs grid в каждом блоке

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 03 day 4: advanced grid layouts"`

## День 5 (Fri): Адаптивный дизайн

### Теория
- [MDN: Responsive design](https://developer.mozilla.org/ru/docs/Learn/CSS/CSS_layout/Responsive_Design)
- Mobile-first: базовые стили для мобильного, `@media (min-width: ...)` 
- Breakpoints: 480px, 768px, 1024px, 1280px — не догма, а контент
- `meta viewport`, относительные единицы, fluid images `max-width: 100%`
- Container queries: `@container` (ознакомительно)
- Mobile-first проще расширять, чем «отрезать» лишнее с десктопа
- Breakpoint выбирай по тому, где ломается контент, а не по модели телефона
- `max-width: 100%` на изображениях предотвращает горизонтальный скролл
- Touch targets ≥ 44×44px — пальцу нужно больше места, чем курсору мыши

### Практика
1. Перепиши стили mobile-first: база 375px, затем 768px, 1024px
2. Навигация: горизонтальная на десктопе, вертикальный список на мобильном
3. Типографика: уменьши `font-size` и spacing на мобильном
4. Таблица: горизонтальный скролл или card-view на узком экране
5. Проверь в DevTools Device Mode минимум 4 размера
6. Добавь `meta viewport` если отсутствует — проверь масштабирование
7. Увеличь padding кнопок на мобильном до touch-friendly размеров

**Критерии:**
- [ ] Нет горизонтального скролла на 375px
- [ ] Touch targets ≥ 44×44px на мобильном
- [ ] Breakpoints логичны, не «магические» без причины

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 03 day 5: responsive mobile-first"`

## День 6 (Sat): Переходы и анимации

### Теория
- [MDN: CSS transitions](https://developer.mozilla.org/ru/docs/Web/CSS/CSS_transitions/Using_CSS_transitions)
- `transition: property duration timing-function delay`
- [MDN: CSS animations](https://developer.mozilla.org/ru/docs/Web/CSS/CSS_animations/Using_CSS_animations)
- `@keyframes`, `animation-name`, `animation-iteration-count`
- `prefers-reduced-motion` — уважение к настройкам пользователя
- Анимируй только `transform` и `opacity` — они не вызывают reflow/repaint всей страницы
- `transition` — простые A→B состояния; `@keyframes` — сложные многошаговые анимации
- `prefers-reduced-motion: reduce` отключает анимации для людей с вестибулярными нарушениями
- Длительность UI-переходов 150–300ms — дольше кажется «тормозным»

### Практика
1. Плавные hover-эффекты на кнопках и карточках (`transition: 0.2s ease`)
2. Анимация появления модального блока через `@keyframes fadeIn`
3. Skeleton loader для карточки (пульсирующий градиент)
4. Оберни анимации в `@media (prefers-reduced-motion: no-preference)`
5. Избегай анимации `width`/`height` — используй `transform` и `opacity`
6. Добавь `will-change: transform` на анимируемый элемент (осторожно, не везде)
7. Сравни `ease`, `ease-in-out`, `cubic-bezier` — выбери для кнопок

**Критерии:**
- [ ] Анимации на GPU-свойствах (`transform`, `opacity`)
- [ ] `prefers-reduced-motion` учтён
- [ ] Переходы не медленнее 300ms для UI-интеракций

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 03 day 6: transitions and animations"`

## День 7 (Sun): Сборка адаптивного лендинга

### Теория
- Паттерн mobile navigation (CSS-only: checkbox hack или `:target`)
- `position: sticky` для шапки при скролле
- `aspect-ratio` для медиа-блоков
- Чеклист перед сдачей: Lighthouse, разные браузеры, реальное устройство
- `position: sticky` держит элемент в viewport при скролле — без JS
- `aspect-ratio: 16/9` резервирует место под медиа — меньше layout shift
- Checkbox hack для меню — доступность спорна; на неделе 6 заменишь на JS
- Перед сдачей: 375px, 768px, 1280px + Lighthouse ≥ 85

### Практика
1. Собери полноценный лендинг: hero, features (grid), testimonials (flex), CTA, footer
2. Sticky header с тенью при скролле (CSS `position: sticky`)
3. Протестируй на Chrome, Firefox, Edge
4. Lighthouse: Performance, Accessibility, Best Practices — все ≥ 85
5. Задокументируй breakpoints и grid-решения в комментариях CSS
6. Добавь `aspect-ratio` на hero-изображение или видео-заглушку
7. Собери проект в `week-03/` — финальная версия SaaS-лендинга

**Критерии:**
- [ ] Лендинг адаптивен 375px–1440px
- [ ] Использованы и flex, и grid осознанно
- [ ] Lighthouse ≥ 85 по трём категориям

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 03 day 7: saas landing final"`

## Проект недели

**Адаптивный лендинг SaaS-продукта** (вымышленный) — одностраничник с 5+ секциями.

Подробное описание: [docs/projects.md — Неделя 3](../../docs/projects.md#неделя-3--saas-landing)

Требования:
- Mobile-first, минимум 2 breakpoint
- Grid для features и pricing, flex для header/footer/cards
- CSS-анимации появления секций, `prefers-reduced-motion`
- Sticky nav, адаптивная типографика через `clamp()`

**Критерии проекта:**
- [ ] Корректный вид на 375px, 768px, 1280px
- [ ] Нет layout shift при загрузке
- [ ] Код разделён: variables, layout, components, utilities
- [ ] Репозиторий с README-screenshot (опционально)
- [ ] 5+ секций: hero, features, pricing, testimonials, CTA, footer
- [ ] ≥ 10 осмысленных коммитов за неделю, тег `week-03-done`
- [ ] Sticky nav работает при скролле без «прыжков»
- [ ] Секции появляются с анимацией, но отключаются при `prefers-reduced-motion`
- [ ] Pricing и features на CSS Grid, header/footer на Flexbox

## Ревью-чеклист
- Когда выбираю flex, а когда grid?
- Что делает `repeat(auto-fill, minmax(200px, 1fr))`?
- Как центрировать элемент по обеим осям через flex?
- Зачем `prefers-reduced-motion` и как его применить?
- Могу ли я сверстать карточку с кнопкой внизу без фиксированной высоты?
