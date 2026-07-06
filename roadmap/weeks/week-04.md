# Неделя 4: Git, GitHub, DevTools, workflow разработчика

> **Цель недели:** освоить систему контроля версий, платформу GitHub и инструменты отладки в браузере.
> **Литература:** Scott Chacon, Ben Straub «Pro Git» ([git-scm.com/book](https://git-scm.com/book/ru/v2)), [GitHub Docs](https://docs.github.com/ru), [Chrome DevTools Docs](https://developer.chrome.com/docs/devtools/)

## День 1 (Mon): Git — основы

### Теория
- [Pro Git: Основы Git](https://git-scm.com/book/ru/v2/Начало-Основы-Git) — снимки, а не различия
- `git init`, `git status`, `git add`, `git commit -m "message"`
- `.gitignore` — node_modules, .env, OS-файлы
- Три состояния: working directory → staging → repository
- Хорошие commit messages: императив, до 50 символов в заголовке

### Практика
1. Установи Git, настрой `user.name` и `user.email` (локально для репо)
2. Инициализируй репозиторий в папке лендинга недели 3
3. Создай `.gitignore` для типичного фронтенд-проекта
4. Сделай 3 осмысленных коммита: structure, styles, responsive
5. Изучи историю: `git log --oneline --graph`

**Критерии:**
- [ ] Репозиторий инициализирован, секреты не в git
- [ ] Минимум 3 коммита с понятными сообщениями
- [ ] `git status` чист после коммита

## День 2 (Tue): Ветки, слияние и конфликты

### Теория
- [Pro Git: Ветвление](https://git-scm.com/book/ru/v2/Ветвление-в-Git-Основы-ветвления-и-слияния)
- `git branch`, `git checkout -b feature/header`, `git switch` (современная альтернатива)
- Fast-forward vs merge commit; `git merge --no-ff`
- Конфликты: маркеры `<<<<<<<`, ручное разрешение, `git add`, `git commit`
- `git stash` — временно спрятать изменения

### Практика
1. Создай ветку `feature/dark-theme`, добавь тёмную тему
2. Вернись на `main`, измени тот же файл — спровоцируй конфликт
3. Смержи ветку, разреши конфликт вручную
4. Попрактикуй `git stash` при переключении веток с незакоммиченными правками
5. Нарисуй схему веток после всех операций

**Критерии:**
- [ ] Конфликт разрешён осознанно, не удалён «всё чужое»
- [ ] История показывает merge (или осознанный ff)
- [ ] Понимаю разницу между branch и commit

### Ловушки
- Коммит в detached HEAD — изменения не на ветке
- `git add .` без проверки — случайно добавил .env
- Разрешение конфликта без тестирования — сломанный код в main

## День 3 (Wed): GitHub и удалённый workflow

### Теория
- [GitHub: Hello World](https://docs.github.com/ru/get-started/start-your-journey/hello-world)
- `git remote add origin`, `git push -u origin main`, `git pull`
- Pull Request: описание, review, merge strategies
- Fork, clone, upstream — open source workflow
- GitHub Issues, Projects — трекинг задач

### Практика
1. Создай репозиторий на GitHub (public), подключи remote
2. Запушь `main`, создай ветку `feature/readme`, добавь README.md
3. Открой Pull Request с описанием изменений
4. Смержи PR через GitHub UI (Squash or Merge — изучи разницу)
5. Создай Issue с багом или улучшением, закрой через коммит `fix: ...`

**Критерии:**
- [ ] Код на GitHub, локальный и remote синхронизированы
- [ ] Минимум 1 PR с описанием
- [ ] README содержит название, описание, как запустить

## День 4 (Thu): DevTools — Elements и Console

### Теория
- [Chrome DevTools: Overview](https://developer.chrome.com/docs/devtools/overview)
- Elements: DOM-дерево, Styles, Computed, Layout (flex/grid overlay)
- Редактирование CSS live, breakpoints в CSS (click on property)
- Console: `console.log`, `console.table`, `console.group`, уровни log/warn/error
- `$0` — выбранный элемент, `copy()`, `inspect()`

### Практика
1. Открой лендинг, исследуй box model каждой секции в Elements
2. Включи flex/grid overlay для layout-контейнеров
3. Найди и исправь «лишний» margin через live edit, перенеси в CSS-файл
4. В Console: выбери элемент, измени текст через `$0.textContent`
5. Добавь `console.log` в будущий JS-файл (заготовка) — проверь вывод

**Критерии:**
- [ ] Умею найти источник стиля в панели Styles (файл и строка)
- [ ] Использовал flex/grid overlay
- [ ] Знаю разницу Computed vs Styles

## День 5 (Fri): DevTools — Network, Sources, Performance

### Теория
- Network: фильтры, waterfall, статусы HTTP, размеры, Disable cache
- Sources: breakpoints в JS, step over/into, watch expressions
- Performance: запись профиля, FPS, long tasks
- Lighthouse в DevTools — аудит страницы
- Application: Local Storage, Cookies, Service Workers (обзор)

### Практика
1. Перезагрузи страницу с Network open — проанализируй waterfall
2. Найди самый тяжёлый ресурс, оптимизируй (сжатие изображения)
3. Запусти Lighthouse, сохрани отчёт, исправь 2+ замечания
4. В Sources поставь breakpoint (на inline script или будущий JS)
5. Запиши Performance profile при скролле — есть ли jank?

**Критерии:**
- [ ] Понимаю статусы 200, 304, 404 в Network
- [ ] Lighthouse score улучшен после правок
- [ ] Умею ставить breakpoint и читать call stack

## День 6 (Sat): Workflow разработчика

### Теория
- Git Flow vs GitHub Flow vs Trunk-Based — когда что
- Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`
- Pre-commit checklist: lint, test, build
- VS Code: Git panel, diff view, extensions (GitLens, Prettier, ESLint)
- Парное программирование и code review — культура

### Практика
1. Переименуй последние коммиты сообщениями в стиле Conventional Commits (если нужно — `git rebase` осторожно или новые коммиты)
2. Настрой Prettier в VS Code, отформатируй CSS/HTML
3. Создай PR template в `.github/pull_request_template.md`
4. Проведи self-review: открой diff последнего PR глазами ревьюера
5. Составь личный чеклист перед каждым push (5 пунктов)

**Критерии:**
- [ ] Коммиты следуют единому стилю сообщений
- [ ] Prettier настроен и применён
- [ ] Есть PR template или чеклист в заметках

## День 7 (Sun): Интеграция и практика

### Теория
- `git log`, `git diff`, `git show`, `git blame` — расследование истории
- `git revert` vs `git reset` — безопасность shared branches
- GitHub Pages — деплой статики (обзор)
- Резервное клонирование: `git clone`, работа offline

### Практика
1. Клонируй свой репозиторий в новую папку — проверь, что всё работает
2. Найди автора строки через `git blame` для одного CSS-файла
3. Задеплой лендинг на GitHub Pages (branch `gh-pages` или Actions)
4. Проверь live URL в DevTools Network и Lighthouse
5. Напиши `CONTRIBUTING.md` с правилами коммитов и веток

**Критерии:**
- [ ] Сайт доступен по публичному URL
- [ ] Clone → open работает без ручных правок
- [ ] CONTRIBUTING.md или раздел в README описывает workflow

## Проект недели

**Open-source мини-проект** — публичный репозиторий с лендингом, полным Git-историей и деплоем.

Требования:
- Минимум 10 коммитов, 2+ ветки, 1 merged PR
- README, .gitignore, LICENSE (MIT)
- GitHub Pages или аналог — live demo
- CONTRIBUTING.md с Conventional Commits

**Критерии проекта:**
- [ ] История коммитов читаема и атомарна
- [ ] PR с описанием и self-review
- [ ] Live demo работает
- [ ] Нет секретов и лишних файлов в репозитории

## Ревью-чеклист
- В чём разница `git add`, `git commit`, `git push`?
- Как отменить последний коммит, не потеряв изменения?
- Что показывает `git log --oneline --graph`?
- Как найти, какой CSS-файл задаёт конкретное свойство в DevTools?
- Могу ли я объяснить flow: branch → commit → push → PR → merge?
