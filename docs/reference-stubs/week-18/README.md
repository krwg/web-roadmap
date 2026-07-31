# Stub: week-18 Library REST API

```
week-18/
├── pyproject.toml / requirements.txt
├── .env.example
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
├── tests/
├── alembic/          # optional
└── README.md
```

Поднимите Postgres (локально или Docker). Первый эндпоинт — `GET /health` → `{ "status": "ok" }`.
