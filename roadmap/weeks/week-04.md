# Неделя 4: Git Advanced, GitHub workflow, DevTools

> **Цель недели:** углубить Git (ветки, merge, rebase, PR), оформить learning-log как OSS-проект, освоить DevTools.
> **Предусловие:** Git с [недели 1](../weeks/week-01.md) — репозиторий `learning-log` уже существует, ежедневные коммиты — привычка.
> **Литература:** Scott Chacon, Ben Straub «Pro Git» ([git-scm.com/book](https://git-scm.com/book/ru/v2)), [GitHub Docs](https://docs.github.com/ru), [Chrome DevTools Docs](https://developer.chrome.com/docs/devtools/), [Conventional Commits](https://www.conventionalcommits.org/ru/), [Oh Shit, Git!?!](https://ohshitgit.com/) — экстренные сценарии

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md#неделя-4--oss-workflow-kit)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-04/`

## День 1 (Mon): Git — ревизия основ + `git log` как инструмент

### Теория
- Повтори [Pro Git: Основы](https://git-scm.com/book/ru/v2/Начало-Основы-Git) — три состояния, SHA коммитов
- `git log --oneline --graph --all` — читать историю как историю решений
- `git show <hash>` — что именно изменилось в коммите
- `git diff` vs `git diff --staged` — незакоммиченное vs в staging
- [Conventional Commits](https://www.conventionalcommits.org/ru/): `feat:`, `fix:`, `docs:`, `chore:`

### Практика
1. В `learning-log` выполни `git log --oneline -15` — опиши в `week-04/REFLECTION.md` паттерн своих сообщений
2. Исправь 2 слабых commit message через `git rebase -i HEAD~3` **только если ещё не пушил**; иначе — лучше не переписывать историю
3. Добавь в корень `learning-log` расширенный `.gitignore` (OS, IDE, env, build)
4. Разбей незакоммиченные правки week-03 на 2 атомарных коммита через staging
5. `git blame week-03/index.html` — кто и когда менял строку (это ты — привыкай к прослеживаемости)

**Критерии:**
- [ ] Репозиторий инициализирован, секреты не в git
- [ ] Минимум 3 коммита с понятными сообщениями
- [ ] `git status` чист после коммита

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 04 day 1: git init and first commits"`

## День 2 (Tue): Ветки, слияние и конфликты

### Теория
- [Pro Git: Ветвление](https://git-scm.com/book/ru/v2/Ветвление-в-Git-Основы-ветвления-и-слияния)
- `git branch`, `git checkout -b feature/header`, `git switch` (современная альтернатива)
- Fast-forward vs merge commit; `git merge --no-ff`
- Конфликты: маркеры `<<<<<<<`, ручное разрешение, `git add`, `git commit`
- `git stash` — временно спрятать изменения
- Ветка — указатель на коммит; дешёвое ветвление — основа feature-workflow
- Fast-forward возможен, если `main` не ушёл вперёд — иначе merge commit
- Конфликт — не катастрофа: Git показывает обе версии, ты выбираешь итог
- `git stash` спасает незакоммиченные правки при срочном переключении ветки

### Практика
1. Создай ветку `feature/dark-theme`, добавь тёмную тему
2. Вернись на `main`, измени тот же файл — спровоцируй конфликт
3. Смержи ветку, разреши конфликт вручную
4. Попрактикуй `git stash` при переключении веток с незакоммиченными правками
5. Нарисуй схему веток после всех операций
6. Сравни `git merge --no-ff` и fast-forward — посмотри историю
7. После разрешения конфликта проверь, что сайт работает

**Критерии:**
- [ ] Конфликт разрешён осознанно, не удалён «всё чужое»
- [ ] История показывает merge (или осознанный ff)
- [ ] Понимаю разницу между branch и commit

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 04 day 2: branches merge conflicts"`

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
- Remote — копия репозитория на сервере; `push` публикует, `pull` синхронизирует
- PR — обсуждение изменений до merge; даже solo-проект учит дисциплине review
- Squash merge сжимает коммиты ветки в один — чистая история `main`
- Issue + `fix #12` в коммите автоматически закрывает задачу

### Практика
1. Создай репозиторий на GitHub (public), подключи remote
2. Запушь `main`, создай ветку `feature/readme`, добавь README.md
3. Открой Pull Request с описанием изменений
4. Смержи PR через GitHub UI (Squash or Merge — изучи разницу)
5. Создай Issue с багом или улучшением, закрой через коммит `fix: ...`
6. Клонируй репозиторий в другую папку — убедись, что clone работает
7. Добавь в README badges (build, license) — заготовка под неделю

**Критерии:**
- [ ] Код на GitHub, локальный и remote синхронизированы
- [ ] Минимум 1 PR с описанием
- [ ] README содержит название, описание, как запустить

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 04 day 3: github remote and PR"`

## День 4 (Thu): DevTools — Elements и Console

### Теория
- [Chrome DevTools: Overview](https://developer.chrome.com/docs/devtools/overview)
- Elements: DOM-дерево, Styles, Computed, Layout (flex/grid overlay)
- Редактирование CSS live, breakpoints в CSS (click on property)
- Console: `console.log`, `console.table`, `console.group`, уровни log/warn/error
- `$0` — выбранный элемент, `copy()`, `inspect()`
- Styles показывает все правила и их источник — быстрый поиск «кто перебил стиль»
- Computed — итоговые вычисленные значения после каскада
- Flex/Grid overlay визуализирует треки и gap — не гадай, смотри
- `$0` в Console — мост между Elements и JS без querySelector

### Практика
1. Открой лендинг, исследуй box model каждой секции в Elements
2. Включи flex/grid overlay для layout-контейнеров
3. Найди и исправь «лишний» margin через live edit, перенеси в CSS-файл
4. В Console: выбери элемент, измени текст через `$0.textContent`
5. Добавь `console.log` в будущий JS-файл (заготовка) — проверь вывод
6. Используй `console.table` для массива объектов (заготовка данных)
7. Найди перечёркнутое свойство в Styles — объясни, почему оно не применилось

**Критерии:**
- [ ] Умею найти источник стиля в панели Styles (файл и строка)
- [ ] Использовал flex/grid overlay
- [ ] Знаю разницу Computed vs Styles

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 04 day 4: devtools elements console"`

## День 5 (Fri): DevTools — Network, Sources, Performance

### Теория
- Network: фильтры, waterfall, статусы HTTP, размеры, Disable cache
- Sources: breakpoints в JS, step over/into, watch expressions
- Performance: запись профиля, FPS, long tasks
- Lighthouse в DevTools — аудит страницы
- Application: Local Storage, Cookies, Service Workers (обзор)
- Waterfall показывает порядок и время загрузки — найди bottleneck
- Disable cache при разработке — иначе видишь устаревшие файлы
- Breakpoint останавливает выполнение — inspect переменных в момент бага
- Lighthouse даёт actionable рекомендации: контраст, размеры, best practices

### Практика
1. Перезагрузи страницу с Network open — проанализируй waterfall
2. Найди самый тяжёлый ресурс, оптимизируй (сжатие изображения)
3. Запусти Lighthouse, сохрани отчёт, исправь 2+ замечания
4. В Sources поставь breakpoint (на inline script или будущий JS)
5. Запиши Performance profile при скролле — есть ли jank?
6. Отфильтруй Network по CSS/JS — оцени общий вес страницы
7. Проверь Application → Local Storage (пока пусто — заготовка под неделю 7)

**Критерии:**
- [ ] Понимаю статусы 200, 304, 404 в Network
- [ ] Lighthouse score улучшен после правок
- [ ] Умею ставить breakpoint и читать call stack

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 04 day 5: devtools network performance"`

## День 6 (Sat): Workflow разработчика

### Теория
- Git Flow vs GitHub Flow vs Trunk-Based — когда что
- Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`
- Pre-commit checklist: lint, test, build
- VS Code: Git panel, diff view, extensions (GitLens, Prettier, ESLint)
- Парное программирование и code review — культура
- GitHub Flow: main + feature branches + PR — достаточно для большинства проектов
- Conventional Commits позволяют автогенерировать CHANGELOG
- Prettier убирает споры о форматировании — один стиль в команде
- Self-review перед push: открой diff глазами ревьюера

### Практика
1. Переименуй последние коммиты сообщениями в стиле Conventional Commits (если нужно — `git rebase` осторожно или новые коммиты)
2. Настрой Prettier в VS Code, отформатируй CSS/HTML
3. Создай PR template в `.github/pull_request_template.md`
4. Проведи self-review: открой diff последнего PR глазами ревьюера
5. Составь личный чеклист перед каждым push (5 пунктов)
6. Добавь `.prettierrc` с базовыми настройками (semi, singleQuote)
7. Напиши CHANGELOG.md с секцией для недель 1–4

**Критерии:**
- [ ] Коммиты следуют единому стилю сообщений
- [ ] Prettier настроен и применён
- [ ] Есть PR template или чеклист в заметках

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 04 day 6: conventional commits prettier"`

## День 7 (Sun): Интеграция и практика

### Теория
- `git log`, `git diff`, `git show`, `git blame` — расследование истории
- `git revert` vs `git reset` — безопасность shared branches
- GitHub Pages — деплой статики (обзор)
- Резервное клонирование: `git clone`, работа offline
- `git blame` показывает, кто и когда изменил строку — расследование регрессий
- `git revert` создаёт новый коммит-отмену — безопасно для shared `main`
- `git reset --hard` переписывает историю — только на локальных ветках
- GitHub Pages публикует статику из `gh-pages` или Actions — live demo бесплатно

### Практика
1. Клонируй свой репозиторий в новую папку — проверь, что всё работает
2. Найди автора строки через `git blame` для одного CSS-файла
3. Задеплой лендинг на GitHub Pages (branch `gh-pages` или Actions)
4. Проверь live URL в DevTools Network и Lighthouse
5. Напиши `CONTRIBUTING.md` с правилами коммитов и веток
6. Добавь LICENSE (MIT) и обнови README со скриншотами недель 1–3
7. Поставь тег `week-04-done` на финальный коммит

**Критерии:**
- [ ] Сайт доступен по публичному URL
- [ ] Clone → open работает без ручных правок
- [ ] CONTRIBUTING.md или раздел в README описывает workflow

### Git
- Закоммить изменения дня: `git add ...` → `git commit -m "week 04 day 7: github pages contributing"`

## Проект недели

**Open-source мини-проект** — публичный репозиторий с лендингом, полным Git-историей и деплоем.

Подробное описание: [docs/projects.md — Неделя 4](../../docs/projects.md#неделя-4--oss-workflow-kit)

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
- [ ] README с badges, скриншотами проектов недель 1–3
- [ ] ≥ 2 feature-ветки, осознанный выбор merge vs rebase
- [ ] CHANGELOG.md с записями по Conventional Commits
- [ ] GitHub Pages деплоит week-03 лендинг по публичному URL
- [ ] Тег `week-04-done` на финальном коммите

## Ревью-чеклист
- В чём разница `git add`, `git commit`, `git push`?
- Как отменить последний коммит, не потеряв изменения?
- Что показывает `git log --oneline --graph`?
- Как найти, какой CSS-файл задаёт конкретное свойство в DevTools?
- Могу ли я объяснить flow: branch → commit → push → PR → merge?
