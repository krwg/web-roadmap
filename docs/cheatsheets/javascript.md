# JavaScript & TypeScript — шпаргалка

> После недель 5–10.

## Типы и сравнение

- Примитивы: `string`, `number`, `boolean`, `null`, `undefined`, `bigint`, `symbol`
- Всегда `===`, не `==`
- `const` по умолчанию; `let` если переприсвоение

## Массивы

```js
arr.map(x => x * 2)
arr.filter(x => x.done)
arr.find(x => x.id === id)
arr.reduce((sum, x) => sum + x, 0)
// slice — копия; splice — мутирует
```

## Async

```js
async function load() {
  const res = await fetch(url);
  if (!res.ok) throw new Error(res.status);
  return res.json();
}
```

## Event Loop (упрощённо)

```
sync code → microtasks (Promise) → macrotasks (setTimeout) → render
```

## Модули

```js
// utils.js
export function fmt(d) { ... }
// app.js
import { fmt } from './utils.js';
```

## TypeScript

```ts
interface User { id: number; name: string }
type Status = 'active' | 'done';
function wrap<T>(x: T): T { return x; }
// strict: no any
```

## DOM

```js
el.addEventListener('click', handler); // не onclick=
parent.addEventListener('click', e => {
  if (e.target.matches('.btn')) { ... } // delegation
});
```
