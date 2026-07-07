# React — шпаргалка

> После недель 11–14.

## Компонент

```tsx
type Props = { title: string; onSave: () => void };
export function Card({ title, onSave }: Props) {
  return <article><h2>{title}</h2><button onClick={onSave}>Save</button></article>;
}
```

## State & effects

```tsx
const [count, setCount] = useState(0);
useEffect(() => {
  document.title = `Tasks: ${count}`;
  return () => { /* cleanup */ };
}, [count]);
```

## Формы (controlled)

```tsx
const [text, setText] = useState('');
<input value={text} onChange={e => setText(e.target.value)} />
```

## Router

```tsx
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/tasks/:id" element={<TaskDetail />} />
</Routes>
```

## Context

```tsx
const ThemeCtx = createContext<'light'|'dark'>('light');
// Provider вверху, useContext внизу — без prop drilling
```

## Правила

- Список: стабильный `key={item.id}`, не index
- Не мутировать state — новый объект/массив
- Выносить fetch в custom hook `useFetch`
