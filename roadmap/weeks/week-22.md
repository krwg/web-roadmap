# Неделя 22: Финальный capstone, деплой, карьера

> **Цель недели:** задеплоить full-stack проект в production, оформить портфолио и подготовиться к поиску работы.
> **Литература:** [Vercel Docs](https://vercel.com/docs), [Render Docs](https://render.com/docs), [freeCodeCamp Portfolio](https://www.freecodecamp.org/news/how-to-create-a-great-portfolio/)

## День 148 (Пн): Финальный проект — планирование

### Теория
- Capstone requirements: full-stack, auth, DB, deploy, tests, docs
- Выбор проекта: Task Manager Pro vs Secret Notes (или свой)
- MVP vs nice-to-have — scope control
- [User stories](https://www.atlassian.com/agile/project-management/user-stories): As a user, I want...

### Практика
1. Выбери вариант capstone и опиши MVP (≤ 1 страница)
2. User stories: минимум 8 штук с acceptance criteria
3. ER-диаграмма, API endpoints list, page map
4. GitHub repo: branch strategy `main` + feature branches
5. Project board (GitHub Projects) — To Do / In Progress / Done

**Критерии:**
- [ ] MVP scope зафиксирован — не расползается
- [ ] ≥ 8 user stories
- [ ] Repo создан с README skeleton

### Ловушки
- Scope creep: drag-and-drop + chat + notifications в MVP
- Нет плана — хаотичная разработка в последний день

---

## День 149 (Вт): Backend deploy — Render / Railway

### Теория
- [Render Web Services](https://render.com/docs/web-services): Docker или native Node/Python
- [Render PostgreSQL](https://render.com/docs/databases) или [Neon](https://neon.tech/) / [Supabase](https://supabase.com/)
- Environment variables в cloud dashboard
- `DATABASE_URL` — connection string для prod

### Практика
1. Push backend в GitHub
2. Render: New Web Service → connect repo → Docker или build command
3. Managed PostgreSQL — скопируй Internal/External URL
4. Env vars: `DATABASE_URL`, `JWT_SECRET`, `NODE_ENV=production`
5. Run migrations/seed на prod DB
6. Проверь `https://your-api.onrender.com/health`

**Критерии:**
- [ ] API доступен по HTTPS
- [ ] Swagger `/docs` работает (FastAPI) или health endpoint
- [ ] DB migrations applied

### Ловушки
- Free tier cold start — 30–60 сек (документируй в README)
- SQLite на Render — ephemeral filesystem, данные теряются

---

## День 150 (Ср): Frontend deploy — Vercel

### Теория
- [Vercel — Deploy Vite](https://vercel.com/docs/frameworks/vite)
- Build command: `npm run build`, output: `dist`
- Environment: `VITE_API_URL=https://your-api.onrender.com`
- [Netlify](https://docs.netlify.com/) — альтернатива

### Практика
1. Import GitHub repo в Vercel
2. Root directory: `frontend/` (если monorepo)
3. Set `VITE_API_URL` в Vercel Environment Variables
4. Deploy → получи `https://your-app.vercel.app`
5. Обнови CORS на backend — добавь Vercel domain в allow_origins

**Критерии:**
- [ ] Frontend на HTTPS
- [ ] API calls идут на production backend (проверь Network tab)
- [ ] Login/register работает end-to-end

### Ловушки
- Забытый CORS update — API works in curl, fails in browser
- `VITE_API_URL` изменён без redeploy — stale build

---

## День 151 (Чт): Production hardening

### Теория
- HTTPS everywhere, HSTS (обзор)
- Error monitoring: [Sentry](https://sentry.io/) free tier (обзор)
- Logging: structured logs в production
- Database backups — managed PG обычно автоматически

### Практика
1. Проверь security headers на prod (securityheaders.com)
2. Rate limiting включён на prod
3. `.env.example` актуален, секреты не в git
4. Custom domain (опционально) — Vercel DNS
5. Fix любых critical issues из smoke test

**Критерии:**
- [ ] security-audit.md обновлён для production
- [ ] Нет secrets в client bundle (grep VITE_)
- [ ] 404/500 pages на фронте

### Ловушки
- JWT_SECRET тот же что в dev — rotate для prod
- Debug mode `LOG_LEVEL=debug` в prod — утечка информации

---

## День 152 (Пт): README, документация, демо

### Теория
- [Awesome README](https://github.com/matiassingers/awesome-readme): badges, screenshots, demo link
- Architecture section: stack, diagram, folder structure
- «How to run locally» vs «Live demo»
- GIF recording: [ScreenToGif](https://www.screentogif.com/) (Windows)

### Практика
1. README: badges, live demo URL, screenshots, tech stack, local + docker setup
2. License: MIT в repo

**Критерии:**
- [ ] README понятен рекрутеру за 3 минуты
- [ ] Live demo link работает
- [ ] Local setup воспроизводим с нуля (попроси друга или проверь сам на чистой машине — checklist)

### Ловушки
- README без demo link — рекрутер не запустит docker
- Устаревшие скриншоты после UI changes

---

## День 153 (Сб): Портфолио и карьера

### Теория
- [GitHub Profile README](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme)
- Portfolio site: 3–5 лучших проектов, не все подряд
- Resume для junior: projects > certificates
- [LinkedIn](https://www.linkedin.com/) — headline, featured projects

### Практика
1. GitHub Profile README: кто ты, стек, топ-3 проекта с ссылками
2. Portfolio page (можно fork [github.com/krwg](https://github.com) style или свой React site)
3. Резюме 1 страница с live links
4. 2-минутный pitch проекта (запиши голосом)

**Критерии:**
- [ ] GitHub profile оформлен
- [ ] Резюме PDF с live links
- [ ] Pitch записан — можешь рассказать без шпаргалки

### Ловушки
- 20 мелких проектов вместо 3 сильных
- «Знаю React» без ссылки на deployed app

---

## День 154 (Вс): Финальное ревью и собеседования

### Теория
- Junior interview topics: HTML/CSS/JS/React/Node/SQL/Git
- [Tech interview handbook](https://www.techinterviewhandbook.org/) — behavioral questions
- STAR method для ответов о проектах
- Whiteboard: объясни архитектуру capstone

### Практика
1. Пройди ревью-чеклист (ниже) — ответы в `FINAL_REVIEW.md`
2. Mock interview: 10 вопросов, план post-roadmap на 30 дней

**Критерии:**
- [ ] FINAL_REVIEW.md — ≥ 80% уверенных ответов
- [ ] Capstone deployed и в портфолио
- [ ] План post-roadmap написан

---

## Проект недели

**Финальный Full-Stack Capstone** — Task Manager Pro или Secret Notes: React + Express/FastAPI + PostgreSQL + JWT + Docker local + Vercel + Render.

**Критерии:**
- [ ] Live demo + API на HTTPS, docker-compose local
- [ ] README, auth, ≥ 5 endpoints, tests, CI green
- [ ] `FINAL_REVIEW.md` и портфолио обновлено

## Ревью-чеклист
- HTML/CSS: block vs inline, box-sizing, Flexbox vs Grid?
- JS: замыкание, Event Loop, var/let/const?
- React: key, useState vs useEffect, controlled inputs?
- Python: Big O list vs dict, магические методы, venv?
- SQL: INNER vs LEFT JOIN, индексы, SQL injection?
- Node: Node vs Browser, middleware, connection pool?
- Full-Stack: REST, CORS, JWT vs cookies, Docker?

**80%+ уверенных ответов — ты готов к junior full-stack. Поздравляем с завершением 22-недельного роадмапа!**
