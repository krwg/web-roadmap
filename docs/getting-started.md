# Начало работы

## Сколько времени

| Параметр | Значение |
|----------|----------|
| Длительность | **22 недели** (154 дня) |
| Нагрузка | **6–7 часов в день** |
| Проекты | **22 недельных** + **1 capstone** (неделя 22) |
| Итог | Junior full-stack portfolio + понимание стека |

Если у вас меньше времени — растяните недели; не пропускайте **проекты недели**. Каталог: [projects.md](projects.md).

---

## Git с первого дня (обязательно)

**До недели 1, день 0** вы создаёте публичный репозиторий `learning-log` на GitHub.  
**В день 1 недели 1** вы коммитите свой первый `index.html`.

Это не «потом разберусь» — Git часть учебного процесса с первой строки HTML.

### Быстрый старт Git

```bash
# 1. GitHub → New repository → learning-log (public, без README)
git clone https://github.com/YOUR_USER/learning-log.git
cd learning-log

# 2. .gitignore
echo -e ".DS_Store\nThumbs.db\n.env\nnode_modules/\n*.log" > .gitignore
git add .gitignore
git commit -m "chore: init learning-log"
git push -u origin main

# 3. День 1 недели 1 — первый HTML
mkdir week-01
# ... создаёте index.html ...
git add week-01/index.html
git commit -m "week 01 day 1: first portfolio index.html"
git push
```

### Правила коммитов

| Правило | Пример |
|---------|--------|
| Минимум 1 коммит в день | `week 05 day 3: filter tasks by status` |
| Папка = неделя | `week-01/`, `week-14/`, `week-22-capstone/` |
| Тег после проекта | `git tag week-01-done` |
| Не коммить секреты | `.env` только в `.gitignore` |

Подробнее: [Pro Git гл. 1–2](https://git-scm.com/book/ru/v2), [week-01 день 0](../roadmap/weeks/week-01.md).

---

## Инструменты (установить до недели 1)

| Инструмент | Зачем | Ссылка |
|------------|--------|--------|
| **Git** | С дня 0 | [git-scm.com](https://git-scm.com/) |
| **GitHub** | Портфолио | [github.com](https://github.com/) |
| **VS Code** | Редактор | [code.visualstudio.com](https://code.visualstudio.com/) |
| **Live Server** | Превью HTML | расширение VS Code |
| **Google Chrome** | DevTools | — |
| **Node.js LTS** | React (с нед. 11) | [nodejs.org](https://nodejs.org/) |
| **Python 3.12+** | Backend (с нед. 15) | [python.org](https://www.python.org/) |
| **Docker Desktop** | Контейнеры (с нед. 21) | [docker.com](https://www.docker.com/) |
| **PostgreSQL** | SQL (с нед. 17) | [postgresql.org](https://www.postgresql.org/) или Docker |

### Расширения VS Code

- ESLint, Prettier, GitLens, Error Lens
- Python + Pylance (с нед. 15)

---

## Структура learning-log

```
learning-log/
├── journal.md              # дневник: что узнал, баги
├── week-01/                  # Portfolio Landing
├── week-02/
├── ...
├── week-22-capstone/         # DevHub — финальный проект
└── .gitignore
```

Полный каталог 22 проектов: [projects.md](projects.md).

---

## Распорядок дня (6–7 часов)

Pomodoro: **50 мин работа / 10 мин отдых**.

| Блок | Время | Содержание |
|------|-------|------------|
| 1. Теория | 1.5 ч | Документация, конспект, литература |
| 2. Практика | 2.5 ч | Задания дня **без копипаста из ИИ** |
| 3. Git | 15 мин | `add` → `commit` → `push` |
| 4. Ревью | 1 ч | Чеклист, дебаг, ИИ только для ревью |
| 5. Reverse engineering | 1 ч | Разбор чужого кода с GitHub |

---

## Протокол «Анти-вайбкодер»

ИИ **не пишет код за вас** на этапе обучения. Допустимо:

1. *«Объясни Event Loop аналогией, без кода»*
2. *«Найди проблемы в моём коде. Не переписывай — укажи строки»*
3. *«Какие edge cases я не учёл?»*

---

## Следующий шаг

1. Создай `learning-log` на GitHub (день 0)
2. [roadmap/introduction.md](../roadmap/introduction.md)
3. [roadmap/weeks/week-01.md](../roadmap/weeks/week-01.md)

Сайт маршрута: [krwg.github.io/web-roadmap](https://krwg.github.io/web-roadmap/)
