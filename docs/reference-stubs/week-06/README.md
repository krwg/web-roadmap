# Stub: week-06 DOM Todo

Скопируйте в `learning-log/week-06/` и реализуйте по [ТЗ](../projects.md#неделя-6--dom-todo-app).

```
week-06/
├── index.html
├── styles.css
├── app.js          # или src/main.js + modules
└── README.md
```

Минимальный контракт `app.js`:
- один listener на `#todo-list` (delegation)
- `load()` / `save()` через `localStorage`
- функции `addTodo`, `toggleTodo`, `removeTodo` без `innerHTML` для текста задачи
