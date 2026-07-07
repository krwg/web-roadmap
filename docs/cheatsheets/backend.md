# FastAPI & Backend — шпаргалка

> После недель 18–21.

## FastAPI минимум

```python
from fastapi import FastAPI, Depends, HTTPException
app = FastAPI()

@app.get("/api/v1/tasks")
def list_tasks(db = Depends(get_db)):
    return db.query(Task).all()
```

## Pydantic

```python
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
```

## JWT flow

```
register → hash password (bcrypt)
login → issue access token (short) + optional refresh
protected route → Depends(get_current_user)
```

## Express слои

```
routes → controllers → services → db
middleware: cors, helmet, rateLimit, errorHandler
```

## Docker Compose

```yaml
services:
  db: { image: postgres:16, environment: {...}, volumes: [...] }
  api: { build: ./backend, depends_on: [db], ports: ["8000:8000"] }
  web: { build: ./frontend, ports: ["5173:80"] }
```

## Security checklist

- [ ] Пароли hashed, не plain
- [ ] CORS ограничен
- [ ] `.env` не в git
- [ ] SQL только параметризованный
- [ ] Rate limit на auth
