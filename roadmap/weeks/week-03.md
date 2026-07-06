# Неделя 3: CSS — Flexbox, Grid, адаптив, анимации

> **Цель недели:** научиться строить современные макеты и адаптивные интерфейсы с Flexbox, Grid и анимациями.
> **Литература:** Ионетт Дакетт «HTML и CSS» (гл. 12–14), [CSS Tricks: Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/), [CSS Tricks: Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/), [web.dev Learn CSS](https://web.dev/learn/css)

## День 1 (Mon): Flexbox — основы

### Теория
- [MDN: Flexbox](https://developer.mozilla.org/ru/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox)
- Контейнер: `display: flex`, `flex-direction`, `flex-wrap`, `gap`
- Выравнивание: `justify-content`, `align-items`, `align-content`
- Элементы: `flex-grow`, `flex-shrink`, `flex-basis`, сокращение `flex: 1`

### Практика
1. Сверстай шапку сайта: логотип слева, навигация справа (`justify-content: space-between`)
2. Сделай ряд из 3 карточек одинаковой высоты с `align-items: stretch`
3. Центрируй блок по вертикали и горизонтали через flex на родителе
4. Поэкспериментируй с `flex-wrap` при сужении окна
5. Используй [Flexbox Froggy](https://flexboxfroggy.com/) — пройди 12+ уровней

**Критерии:**
- [ ] Шапка не ломается при 768px ширине
- [ ] Карточки одной высоты без фиксированного `height`
- [ ] Flexbox Froggy пройден

## День 2 (Tue): Flexbox — практические паттерны

### Теория
- `order`, `align-self` — когда уместны (редко)
- Паттерн «Holy Grail» layout на flex
- `flex: 1 1 auto` vs `flex: 1 1 0` — разница в поведении
- Навигация, card footer с кнопкой внизу (`margin-top: auto`)

### Практика
1. Карточка товара: изображение, заголовок, описание, цена, кнопка прижата к низу
2. Sticky footer: `body` как flex-column, `main { flex: 1 }`
3. Горизонтальный скролл галереи: `flex-wrap: nowrap`, `overflow-x: auto`
4. Pagination: ряд кнопок по центру с `gap`
5. Рефакторинг шапки: мобильное меню-иконка (пока без JS — скрытый блок)

**Критерии:**
- [ ] Кнопка в карточке всегда внизу при разной длине текста
- [ ] Footer прижат к низу viewport на короткой странице
- [ ] Галерея скроллится горизонтально на мобильном

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

### Практика
1. Сетка 3×2 карточек через `grid-template-columns: repeat(3, 1fr)`
2. Макет страницы через areas: header, sidebar, main, footer
3. Один элемент растяни на 2 колонки (`grid-column: span 2`)
4. Пройди [Grid Garden](https://cssgridgarden.com/) — 12+ уровней
5. Сравни тот же макет на flex vs grid — запиши вывод

**Критерии:**
- [ ] Grid Garden пройден
- [ ] Макет с areas читаем в CSS без HTML-подсказок
- [ ] Адаптив: при 600px — одна колонка

## День 4 (Thu): Grid — продвинутые макеты

### Теория
- `auto-fill` vs `auto-fit` с `minmax(250px, 1fr)` — responsive без media queries
- `subgrid` (базовое знакомство) — выравнивание вложенных сеток
- Наложение элементов через совпадающие grid-ячейки
- Когда grid, когда flex: grid для 2D, flex для 1D

### Практика
1. Галерея с `grid-template-columns: repeat(auto-fill, minmax(200px, 1fr))`
2. Dashboard: sidebar 250px, main `1fr`, виджеты внутри main — вложенный grid
3. Карточка с overlay-текстом поверх изображения (grid stack)
4. Pinterest-подобная сетка разной высоты (разный `grid-row: span N`)
5. Рефакторинг блога недели 2 на grid-layout

**Критерии:**
- [ ] Галерея адаптируется без единой media query
- [ ] Dashboard читаем на 1024px и 375px
- [ ] Осознанный выбор flex vs grid в каждом блоке

## День 5 (Fri): Адаптивный дизайн

### Теория
- [MDN: Responsive design](https://developer.mozilla.org/ru/docs/Learn/CSS/CSS_layout/Responsive_Design)
- Mobile-first: базовые стили для мобильного, `@media (min-width: ...)`
- Breakpoints: 480px, 768px, 1024px, 1280px — не догма, а контент
- `meta viewport`, относительные единицы, fluid images `max-width: 100%`
- Container queries: `@container` (ознакомительно)

### Практика
1. Перепиши стили mobile-first: база 375px, затем 768px, 1024px
2. Навигация: горизонтальная на десктопе, вертикальный список на мобильном
3. Типографика: уменьши `font-size` и spacing на мобильном
4. Таблица: горизонтальный скролл или card-view на узком экране
5. Проверь в DevTools Device Mode минимум 4 размера

**Критерии:**
- [ ] Нет горизонтального скролла на 375px
- [ ] Touch targets ≥ 44×44px на мобильном
- [ ] Breakpoints логичны, не «магические» без причины

## День 6 (Sat): Переходы и анимации

### Теория
- [MDN: CSS transitions](https://developer.mozilla.org/ru/docs/Web/CSS/CSS_transitions/Using_CSS_transitions)
- `transition: property duration timing-function delay`
- [MDN: CSS animations](https://developer.mozilla.org/ru/docs/Web/CSS/CSS_animations/Using_CSS_animations)
- `@keyframes`, `animation-name`, `animation-iteration-count`
- `prefers-reduced-motion` — уважение к настройкам пользователя

### Практика
1. Плавные hover-эффекты на кнопках и карточках (`transition: 0.2s ease`)
2. Анимация появления модального блока через `@keyframes fadeIn`
3. Skeleton loader для карточки (пульсирующий градиент)
4. Оберни анимации в `@media (prefers-reduced-motion: no-preference)`
5. Избегай анимации `width`/`height` — используй `transform` и `opacity`

**Критерии:**
- [ ] Анимации на GPU-свойствах (`transform`, `opacity`)
- [ ] `prefers-reduced-motion` учтён
- [ ] Переходы не медленнее 300ms для UI-интеракций

## День 7 (Sun): Сборка адаптивного лендинга

### Теория
- Паттерн mobile navigation (CSS-only: checkbox hack или `:target`)
- `position: sticky` для шапки при скролле
- `aspect-ratio` для медиа-блоков
- Чеклист перед сдачей: Lighthouse, разные браузеры, реальное устройство

### Практика
1. Собери полноценный лендинг: hero, features (grid), testimonials (flex), CTA, footer
2. Sticky header с тенью при скролле (CSS `position: sticky`)
3. Протестируй на Chrome, Firefox, Edge
4. Lighthouse: Performance, Accessibility, Best Practices — все ≥ 85
5. Задокументируй breakpoints и grid-решения в комментариях CSS

**Критерии:**
- [ ] Лендинг адаптивен 375px–1440px
- [ ] Использованы и flex, и grid осознанно
- [ ] Lighthouse ≥ 85 по трём категориям

## Проект недели

**Адаптивный лендинг SaaS-продукта** (вымышленный) — одностраничник с 5+ секциями.

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

## Ревью-чеклист
- Когда выбираю flex, а когда grid?
- Что делает `repeat(auto-fill, minmax(200px, 1fr))`?
- Как центрировать элемент по обеим осям через flex?
- Зачем `prefers-reduced-motion` и как его применить?
- Могу ли я сверстать карточку с кнопкой внизу без фиксированной высоты?
