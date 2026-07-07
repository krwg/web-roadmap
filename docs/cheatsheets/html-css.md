# HTML & CSS — шпаргалка

> После недель 1–3. [Полный маршрут](https://krwg.github.io/web-roadmap/)

## HTML семантика

```
header → nav → main → section/article → aside → footer
```

- Один `h1` на страницу, иерархия без пропусков
- `label[for]` ↔ `input[id]`
- `img` + `alt`; декоративное → `alt=""`
- Формы: `required`, `pattern`, `fieldset`/`legend`

## Box model

```
content → padding → border → margin
```

```css
*, *::before, *::after { box-sizing: border-box; }
```

## Flexbox

```css
.container { display: flex; gap: 1rem; justify-content: center; align-items: center; }
.item { flex: 1; } /* grow */
```

## Grid

```css
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; }
```

## Адаптив

```css
/* mobile-first */
.hero { font-size: clamp(1.5rem, 4vw, 2.5rem); }
@media (min-width: 768px) { ... }
```

## Design tokens

```css
:root {
  --color-bg: #050508;
  --space-md: 1rem;
  --radius: 12px;
}
```
