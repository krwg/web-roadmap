# Неделя 4: Git Advanced, GitHub workflow, DevTools

> **Цель недели:** углубить Git (ветки, merge, rebase, PR), оформить learning-log как OSS-проект, освоить DevTools.
> **Предусловие:** Git с [недели 1](../weeks/week-01.md) — репозиторий `learning-log` уже существует, ежедневные коммиты — привычка.
> **Литература:** Scott Chacon, Ben Straub «Pro Git» ([git-scm.com/book](https://git-scm.com/book/ru/v2)), [GitHub Docs](https://docs.github.com/ru), [Chrome DevTools Docs](https://developer.chrome.com/docs/devtools/), [Conventional Commits](https://www.conventionalcommits.org/ru/), [Oh Shit, Git!?!](https://ohshitgit.com/) — экстренные сценарии

> **Проект недели:** см. [docs/projects.md](../../docs/projects.md#неделя-4--oss-workflow-kit)
> **Git:** минимум 1 осмысленный коммит каждый день в `learning-log/week-04/`

## День 1 (Mon): Git — ревизия основ + `git log` как инструмент

### Теория

Перед углублением в ветки стоит закрепить фундамент: Git отслеживает три **состояния** каждого файла — изменён (modified), проиндексирован (staged), зафиксирован (committed). Каждый коммит получает уникальный SHA-хеш — «отпечаток» снимка. `git log --oneline --graph --all` показывает историю как дерево решений, а не список сохранений.

`git show <hash>` раскрывает конкретный коммит: автор, дата, diff. `git diff` — разница между working directory и staging; `git diff --staged` — что войдёт в следующий коммит. Это инструменты **расследования**: «что я наменял и зачем?».

**Conventional Commits** — соглашение об именовании: `feat:`, `fix:`, `docs:`, `chore:`. Префикс сразу говорит тип изменения; в будущем из таких сообщений автогенерируется CHANGELOG. Хорошее сообщение отвечает на вопрос «зачем», а не «что нажал».

**Ключевая мысль:** `git log` — дневник решений; осмысленные сообщения коммитов = документация для будущего себя.

**Читать:**
- [Pro Git: Основы](https://git-scm.com/book/ru/v2/Начало-Основы-Git) — три состояния, SHA коммитов
- [Conventional Commits](https://www.conventionalcommits.org/ru/)

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

Ветка в Git — просто **указатель** на коммит. Создать ветку дёшево: `git switch -c feature/header` ответвляет от текущего состояния, и ты работаешь изолированно, не ломая `main`. Когда фича готова — **слияние** (merge) переносит изменения обратно.

**Fast-forward merge** возможен, если `main` не получил новых коммитов с момента ответвления: указатель `main` просто «перепрыгнет» на конец feature-ветки. Иначе Git создаёт **merge commit** — коммит с двумя родителями. `git merge --no-ff` принудительно создаёт merge commit даже при возможности ff — сохраняет видимость ветки в истории.

**Конфликт** возникает, когда одна и та же строка изменена в обеих ветках. Git вставляет маркеры `<<<<<<<`, `=======`, `>>>>>>>` — ты вручную выбираешь итог, `git add`, `git commit`. Конфликт — не катастрофа, а диалог между версиями. `git stash` временно прячет незакоммиченные правки, если нужно срочно переключить ветку.

**Ключевая мысль:** ветка — дешёвый черновик; merge — слияние черновика с основной линией.

**Читать:**
- [Pro Git: Ветвление](https://git-scm.com/book/ru/v2/Ветвление-в-Git-Основы-ветвления-и-слияния)

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

Локальный Git — половина workflow. **Remote** (обычно `origin` на GitHub) — копия репозитория на сервере. `git push` публикует коммиты; `git pull` забирает чужие и сливает с твоими. Флаг `-u` при первом push связывает локальную ветку с удалённой — дальше достаточно `git push`.

**Pull Request** — запрос на слияние ветки с описанием изменений. Даже в solo-проекте PR учит дисциплине review: ты смотришь diff глазами «чужого» разработчика до merge. Стратегии merge на GitHub: обычный merge, squash (все коммиты ветки → один), rebase. Squash даёт чистую линейную историю `main`.

**Issues** — трекер задач: баг, улучшение, идея. Коммит с `fix #12` в сообщении автоматически закрывает issue №12. Fork + upstream — паттерн open source: форкаешь чужой репозиторий, вносишь правки, открываешь PR в оригинал.

**Ключевая мысль:** GitHub = remote + социальный слой; PR — разговор о коде до попадания в main.

**Читать:**
- [GitHub: Hello World](https://docs.github.com/ru/get-started/start-your-journey/hello-world)

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

Chrome DevTools — рентген твоей страницы. Панель **Elements** показывает живое DOM-дерево: кликни на узел — увидишь применённые стили, box model, flex/grid overlay. Вкладка **Styles** перечисляет все CSS-правила с указанием файла и строки; перечёркнутое свойство проиграло в каскаде — ищи победителя выше. **Computed** — итоговые вычисленные значения после каскада, наследования и браузерных дефолтов.

Live-редактирование CSS в DevTools — быстрый эксперимент: подобрал отступ — перенеси в файл. Flex/Grid overlay рисует треки и gap поверх страницы — не гадай, смотри. В **Console** `$0` — ссылка на элемент, выбранный в Elements; мост между визуальным и программным исследованием.

`console.log` — базовый вывод; `console.table` — таблица для массивов объектов; `console.group` — группировка связанных логов. Уровни `warn` и `error` выделяются визуально и фильтруются.

**Ключевая мысль:** Styles — «кто перебил?», Computed — «что в итоге?»; overlay — «как устроена сетка?».

**Читать:**
- [Chrome DevTools: Overview](https://developer.chrome.com/docs/devtools/overview)

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

Панель **Network** показывает каждый HTTP-запрос при загрузке страницы: URL, статус, размер, время. **Waterfall** — диаграмма «кто за кем»: видно, что блокирует рендер (тяжёлые картинки, синхронные скрипты). Статусы: **200** OK, **304** Not Modified (из кэша), **404** Not Found. При разработке включай **Disable cache**, иначе видишь устаревшие файлы.

**Sources** — отладка JavaScript: breakpoint останавливает выполнение в точке; step over/into проходят по строкам; watch expressions следят за переменными. **Performance** записывает профиль: FPS, long tasks, jank при скролле. **Lighthouse** в DevTools — аудит Performance, Accessibility, Best Practices с конкретными рекомендациями.

Вкладка **Application** — хранилища браузера: Local Storage, Cookies, Service Workers (обзор на будущее). Тяжёлый ресурс в Network — первый кандидат на оптимизацию: сжатие, WebP, lazy loading.

**Ключевая мысль:** Network waterfall — карта загрузки; Lighthouse — чеклист перед сдачей.

**Читать:**
- [Chrome DevTools: Network](https://developer.chrome.com/docs/devtools/network)
- [Chrome DevTools: Performance](https://developer.chrome.com/docs/devtools/performance)

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

Workflow — это привычки, которые масштабируются от solo до команды. **GitHub Flow** — простейший: `main` всегда deployable, каждая фича в ветке → PR → merge. Git Flow сложнее (develop, release) — избыточен для учебных проектов. **Trunk-Based** — короткоживущие ветки, частые merge в main — для зрелых команд с CI.

**Conventional Commits** (`feat:`, `fix:`, `docs:`) — единый язык сообщений; из них генерируется CHANGELOG. **Pre-commit checklist**: `git diff` глазами ревьюера, нет ли `.env` в staging, страница открывается, Lighthouse не упал. Prettier убирает споры о форматировании — один `.prettierrc` на проект.

VS Code Git panel, diff view, GitLens — ускоряют ежедневную работу. Code review — не придирка, а передача знаний: даже self-review перед push ловит опечатки и лишние файлы.

**Ключевая мысль:** GitHub Flow + Conventional Commits + self-review = профессиональный минимум.

**Читать:**
- [Conventional Commits](https://www.conventionalcommits.org/ru/)
- [GitHub Flow](https://docs.github.com/ru/get-started/using-github/github-flow)

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

Инструменты **расследования истории**: `git log` — хронология; `git diff` — разница между состояниями; `git show` — один коммит целиком; `git blame` — кто и когда изменил каждую строку файла. Blame не для поиска виноватых, а для понимания контекста: «зачем эта строка появилась?».

Отмена изменений — два разных инструмента. `git revert <hash>` создаёт **новый** коммит, отменяющий старый — безопасно для shared `main`, история не переписывается. `git reset --hard` откатывает указатель ветки — **переписывает** историю; только на локальных ветках, никогда на запушенном main без согласования.

**GitHub Pages** публикует статику из ветки `gh-pages` или через Actions — бесплатный live demo для портфолио. `git clone` в новую папку — тест: «смогу ли я развернуть проект с нуля?» — must-have перед сдачей.

**Ключевая мысль:** `revert` — безопасная отмена; `reset --hard` — только локально; clone — финальный тест переносимости.

**Читать:**
- [Pro Git: Отмена изменений](https://git-scm.com/book/ru/v2/Приложение-C%3A-Команды-Git-Отмена-изменений)
- [GitHub Pages](https://docs.github.com/ru/pages)

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
