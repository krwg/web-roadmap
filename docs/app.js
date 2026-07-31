/* global Prism, mermaid */
(function () {
  const ROUTES = window.SITE_ROUTES || {};
  const WEEK_IDS = Object.keys(ROUTES.weeks || {});
  const PAGE_IDS = Object.keys(ROUTES.pages || {});
  const SEARCH_INDEX = window.SEARCH_INDEX || [];
  const GISCUS = window.GISCUS || null;
  const REPO = 'krwg/web-roadmap';
  const REPO_URL = `https://github.com/${REPO}`;
  const PROGRESS_KEY = 'web-roadmap-progress';
  const DAY_PROGRESS_KEY = 'web-roadmap-day-progress';
  const READING_KEY = 'web-roadmap-reading';
  const LAST_ROUTE_KEY = 'web-roadmap-last-route';
  const TRACK_KEY = 'web-roadmap-track';
  const QUIZ_KEY = 'web-roadmap-quiz';
  const TOTAL_DAYS = 154;
  const DAY_INDEX = ROUTES.dayIndex || [];

  const weekCache = {};
  let currentRoute = '';
  let currentSectionId = '';
  let giscusTerm = '';

  function $(sel, root = document) { return root.querySelector(sel); }
  function $$(sel, root = document) { return [...root.querySelectorAll(sel)]; }

  function icon(name) {
    return `<span class="material-symbols-outlined" aria-hidden="true">${name}</span>`;
  }

  function getTrackMode() {
    const v = localStorage.getItem(TRACK_KEY);
    return v === 'lite' ? 'lite' : 'full';
  }
  function setTrackMode(mode) {
    localStorage.setItem(TRACK_KEY, mode === 'lite' ? 'lite' : 'full');
    syncTrackChips();
    applyTrackFilter(document);
  }
  function syncTrackChips() {
    const mode = getTrackMode();
    $$('[data-track-mode]').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-track-mode') === mode);
    });
    document.body.dataset.track = mode;
  }
  function applyTrackFilter(root = document) {
    const mode = getTrackMode();
    $$('.practice-track', root).forEach(el => {
      const track = el.getAttribute('data-track');
      el.hidden = mode === 'lite' ? track === 'full' : track === 'lite';
    });
  }

  function getQuizProgress() {
    try { return JSON.parse(localStorage.getItem(QUIZ_KEY) || '{}'); }
    catch { return {}; }
  }
  function setQuizScore(weekId, score, total) {
    const p = getQuizProgress();
    p[weekId] = { score, total, ts: Date.now() };
    localStorage.setItem(QUIZ_KEY, JSON.stringify(p));
  }

  function findNextIncomplete() {
    const days = getDayProgress();
    for (const d of DAY_INDEX) {
      if (!days[d.id]) return d;
    }
    return null;
  }

  function getProgress() {
    try { return JSON.parse(localStorage.getItem(PROGRESS_KEY) || '{}'); }
    catch { return {}; }
  }
  function setProgress(id, done) {
    const p = getProgress();
    if (done) p[id] = Date.now(); else delete p[id];
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(p));
    updateProgressUI();
    updateCards();
    updateResumeBanner();
    renderProgressMap();
  }
  function toggleWeekDone(id) {
    const p = getProgress();
    setProgress(id, !p[id]);
  }

  function saveLastRoute(routeId, anchor) {
    if (!/^week-\d{2}$/.test(routeId)) return;
    const title = ROUTES.weeks?.[routeId] || routeId;
    localStorage.setItem(LAST_ROUTE_KEY, JSON.stringify({
      route: routeId,
      anchor: anchor || '',
      title,
      ts: Date.now(),
    }));
    updateResumeBanner();
  }

  function getLastRoute() {
    try { return JSON.parse(localStorage.getItem(LAST_ROUTE_KEY) || 'null'); }
    catch { return null; }
  }

  function updateResumeBanner() {
    const banner = $('#resume-banner');
    const link = $('#resume-link');
    const titleEl = $('#resume-title');
    const metaEl = $('#resume-meta');
    if (!banner || !link) return;

    const next = findNextIncomplete();
    const last = getLastRoute();

    if (next) {
      banner.hidden = false;
      if (titleEl) titleEl.textContent = 'Продолжить обучение';
      if (metaEl) metaEl.textContent = `${next.weekTitle}: ${next.label}`;
      link.href = `#${next.week}--${next.id}`;
      link.setAttribute('data-route', next.week);
      const cta = $('#cta-start');
      if (cta) {
        cta.textContent = 'Продолжить';
        cta.href = `#${next.week}--${next.id}`;
        cta.setAttribute('data-route', next.week);
      }
      return;
    }

    if (!last?.route) {
      banner.hidden = true;
      return;
    }

    const weekTitle = ROUTES.weeks?.[last.route] || last.title || last.route;
    banner.hidden = false;
    if (titleEl) titleEl.textContent = 'Курс пройден — повторить';
    if (metaEl) metaEl.textContent = weekTitle;
    const hash = last.anchor ? `${last.route}--${last.anchor}` : last.route;
    link.href = `#${hash}`;
    link.setAttribute('data-route', last.route);
  }

  function renderProgressMap() {
    const grid = $('#progress-map-grid');
    const sub = $('#progress-map-sub');
    if (!grid) return;
    const daysDone = getDayProgress();
    const weeksDone = getProgress();
    const byWeek = {};
    DAY_INDEX.forEach(d => {
      if (!byWeek[d.week]) byWeek[d.week] = [];
      byWeek[d.week].push(d);
    });
    const next = findNextIncomplete();
    let stuckLabel = next ? `Следующий шаг: ${next.weekTitle} · ${next.label}` : 'Все дни отмечены — можно ревьюить слабые места';
    if (sub) sub.textContent = stuckLabel;

    grid.innerHTML = WEEK_IDS.map(wid => {
      const days = byWeek[wid] || [];
      const doneCount = days.filter(d => daysDone[d.id]).length;
      const weekDone = !!weeksDone[wid];
      const title = ROUTES.weeks?.[wid] || wid;
      const dots = days.map(d => {
        const done = !!daysDone[d.id];
        const isNext = next && next.id === d.id;
        return `<a class="pmap-dot${done ? ' done' : ''}${isNext ? ' next' : ''}" href="#${wid}--${d.id}" data-route="${wid}" title="${d.label}"></a>`;
      }).join('');
      return `<div class="pmap-week${weekDone ? ' week-done' : ''}">
        <a class="pmap-title" href="#${wid}" data-route="${wid}">${wid.replace('week-', '')}. ${title}</a>
        <div class="pmap-dots">${dots || '<span class="pmap-empty">—</span>'}</div>
        <span class="pmap-meta">${doneCount}/${days.length || '—'}</span>
      </div>`;
    }).join('');
  }

  function getDayProgress() {
    try { return JSON.parse(localStorage.getItem(DAY_PROGRESS_KEY) || '{}'); }
    catch { return {}; }
  }
  function setDayDone(dayId, done) {
    const p = getDayProgress();
    if (done) p[dayId] = Date.now(); else delete p[dayId];
    localStorage.setItem(DAY_PROGRESS_KEY, JSON.stringify(p));
    updateProgressUI();
    updateResumeBanner();
    renderProgressMap();
  }
  function exportProgress() {
    return JSON.stringify({
      weeks: getProgress(),
      days: getDayProgress(),
      quizzes: getQuizProgress(),
      track: getTrackMode(),
      exportedAt: new Date().toISOString(),
      version: 2,
    }, null, 2);
  }
  function exportLearningLogPayload() {
    const next = findNextIncomplete();
    return JSON.stringify({
      schema: 'web-roadmap/learning-log-progress',
      version: 2,
      exportedAt: new Date().toISOString(),
      track: getTrackMode(),
      resume: next ? { week: next.week, day: next.id, label: next.label } : null,
      weeks: getProgress(),
      days: getDayProgress(),
      quizzes: getQuizProgress(),
      tip: 'Положите этот файл в learning-log/progress.json и коммитьте раз в неделю.',
    }, null, 2);
  }
  function importProgress(json) {
    const data = typeof json === 'string' ? JSON.parse(json) : json;
    if (data.weeks) localStorage.setItem(PROGRESS_KEY, JSON.stringify(data.weeks));
    if (data.days) localStorage.setItem(DAY_PROGRESS_KEY, JSON.stringify(data.days));
    if (data.quizzes) localStorage.setItem(QUIZ_KEY, JSON.stringify(data.quizzes));
    if (data.track) setTrackMode(data.track);
    updateProgressUI();
    updateCards();
    updateResumeBanner();
    renderProgressMap();
  }

  function updateProgressUI() {
    const p = getProgress();
    const days = getDayProgress();
    const doneWeeks = WEEK_IDS.filter(w => p[w]).length;
    const doneDays = Object.keys(days).length;
    const el = $('#progress-fill');
    const label = $('#progress-label');
    const weekRatio = WEEK_IDS.length ? doneWeeks / WEEK_IDS.length : 0;
    const dayRatio = Math.min(1, doneDays / TOTAL_DAYS);
    const ratio = Math.max(weekRatio, dayRatio * 0.85);
    if (el) el.style.width = `${ratio * 100}%`;
    if (label) {
      label.textContent = `Прогресс: ${doneWeeks}/${WEEK_IDS.length} нед. · ${doneDays} дн. отмечено`;
    }
  }

  function updateCards() {
    const p = getProgress();
    $$('.card[data-route]').forEach(card => {
      const id = card.getAttribute('data-route');
      card.classList.toggle('done', !!p[id]);
      let badge = card.querySelector('.done-badge');
      if (p[id]) {
        if (!badge) {
          badge = document.createElement('button');
          badge.type = 'button';
          badge.className = 'done-badge';
          badge.innerHTML = icon('check_circle');
          badge.title = 'Отметить непройденной';
          badge.addEventListener('click', e => { e.preventDefault(); e.stopPropagation(); toggleWeekDone(id); });
          card.appendChild(badge);
        }
      } else if (badge) badge.remove();
    });
  }

  function showView(name) {
    $$('.view').forEach(v => { v.hidden = true; });
    const el = $(`#view-${name}`);
    if (el) el.hidden = false;
  }

  function nextWeekId(routeId) {
    const m = routeId.match(/^week-(\d{2})$/);
    if (!m) return null;
    const n = parseInt(m[1], 10) + 1;
    if (n > 22) return null;
    return `week-${String(n).padStart(2, '0')}`;
  }

  async function fetchWeek(id) {
    if (weekCache[id]) return weekCache[id];
    const res = await fetch(`weeks/${id.replace('week-', '')}.json`);
    if (!res.ok) throw new Error('Week not found');
    const data = await res.json();
    weekCache[id] = data;
    return data;
  }

  async function fetchPage(id) {
    if (weekCache[id]) return weekCache[id];
    const res = await fetch(`pages/${id}.json`);
    if (!res.ok) throw new Error('Page not found');
    const data = await res.json();
    weekCache[id] = data;
    return data;
  }

  function lessonSections(data) {
    if (data.sections?.length) return data.sections;
    if (!data.toc?.length) return [];
    return data.toc.map(t => ({
      id: t.id,
      label: t.label,
      kind: t.id.includes('-day-') ? 'day' : (t.id.endsWith('-project') ? 'project' : (t.id.endsWith('-review') ? 'review' : 'section')),
      html: null,
    }));
  }

  function buildToc(sections, routeId, activeId) {
    if (!sections?.length) return '';
    const daysDone = getDayProgress();
    const items = sections.map(t => {
      const done = t.kind === 'day' && !!daysDone[t.id];
      const active = t.id === activeId ? ' active' : '';
      const doneCls = done ? ' toc-done' : '';
      let badge = '';
      if (t.kind === 'day') {
        const m = t.id.match(/-day-(\d+)$/);
        badge = `<span class="toc-num">${m ? m[1] : '·'}</span>`;
      } else if (t.kind === 'project') {
        badge = `<span class="toc-num toc-num-proj">${icon('rocket_launch')}</span>`;
      } else if (t.kind === 'review') {
        badge = `<span class="toc-num toc-num-rev">${icon('checklist')}</span>`;
      }
      return `<a class="toc-link${active}${doneCls}" href="#${routeId}--${t.id}" data-anchor="${t.id}">${badge}<span class="toc-label">${t.label}</span></a>`;
    }).join('');
    return `<h4>Уроки недели</h4>${items}`;
  }

  function highlightCode(root) {
    if (typeof Prism !== 'undefined') {
      $$('pre code', root).forEach(el => Prism.highlightElement(el));
    }
    if (typeof mermaid !== 'undefined') {
      $$('.mermaid', root).forEach((el) => {
        if (el.dataset.processed) return;
        mermaid.run({ nodes: [el] }).catch(() => {});
      });
    }
  }

  function updateGithubToolbar(routeId, sectionId, data) {
    const isWeek = /^week-\d{2}$/.test(routeId);
    const src = data?.sourcePath || (isWeek ? `roadmap/weeks/${routeId}.md` : null);
    const edit = $('#edit-github-btn');
    const issue = $('#issue-github-btn');
    const source = $('#source-github-btn');

    if (edit) {
      edit.hidden = !src;
      if (src) edit.href = `${REPO_URL}/edit/main/${src}`;
    }
    if (source) {
      source.hidden = !src;
      if (src) source.href = `${REPO_URL}/blob/main/${src}`;
    }
    if (issue) {
      issue.hidden = !isWeek;
      if (isWeek) {
        const title = encodeURIComponent(`[урок] ${routeId}${sectionId ? ' / ' + sectionId : ''}`);
        const body = encodeURIComponent(
          `**Неделя:** ${routeId}\n**Урок:** ${sectionId || '—'}\n**Страница:** https://krwg.github.io/web-roadmap/#${routeId}${sectionId ? '--' + sectionId : ''}\n\n### Описание\n\n`
        );
        issue.href = `${REPO_URL}/issues/new?title=${title}&body=${body}`;
      }
    }
  }

  function updateMarkDoneBtn(routeId) {
    const markBtn = $('#mark-done-btn');
    if (!markBtn) return;
    const isWeek = /^week-\d{2}$/.test(routeId);
    markBtn.hidden = !isWeek;
    const done = !!getProgress()[routeId];
    markBtn.innerHTML = done
      ? `${icon('check_circle')} Неделя пройдена`
      : `${icon('radio_button_unchecked')} Отметить неделю`;
    markBtn.onclick = () => {
      toggleWeekDone(routeId);
      updateMarkDoneBtn(routeId);
    };
  }

  function updateMarkDayBtn(section) {
    const btn = $('#mark-day-btn');
    if (!btn) return;
    if (!section || section.kind !== 'day') {
      btn.hidden = true;
      return;
    }
    btn.hidden = false;
    const done = !!getDayProgress()[section.id];
    btn.innerHTML = done
      ? `${icon('check_circle')} День выполнен`
      : `${icon('radio_button_unchecked')} Отметить день`;
    btn.setAttribute('aria-pressed', done ? 'true' : 'false');
    btn.onclick = () => {
      const now = !getDayProgress()[section.id];
      setDayDone(section.id, now);
      updateMarkDayBtn(section);
      const tocEl = $('#doc-toc');
      if (tocEl && currentRoute) {
        const link = tocEl.querySelector(`[data-anchor="${section.id}"]`);
        link?.classList.toggle('toc-done', now);
      }
      updateWeekProgress(currentRoute, lessonSections(weekCache[currentRoute] || {}));
    };
  }

  function updateWeekProgress(routeId, sections) {
    const wrap = $('#week-progress');
    const fill = $('#week-progress-fill');
    const label = $('#week-progress-label');
    if (!wrap || !fill) return;
    const days = (sections || []).filter(s => s.kind === 'day');
    if (!/^week-\d{2}$/.test(routeId) || !days.length) {
      wrap.hidden = true;
      return;
    }
    const doneMap = getDayProgress();
    const done = days.filter(d => doneMap[d.id]).length;
    wrap.hidden = false;
    fill.style.width = `${(done / days.length) * 100}%`;
    if (label) label.textContent = `${done} / ${days.length} дней`;
  }

  function updateBreadcrumb(weekTitle, section) {
    const el = $('#lesson-breadcrumb');
    if (!el) return;
    if (!section) {
      el.innerHTML = '';
      return;
    }
    el.innerHTML = `<span>${weekTitle}</span><span class="bc-sep">/</span><span class="bc-current">${section.label}</span>`;
  }

  function updateLessonNav(sections, routeId, sectionId) {
    const bar = $('#lesson-next');
    const nextLink = $('#lesson-next-link');
    const nextText = $('#lesson-next-text');
    const prevLink = $('#lesson-prev-link');
    const prevText = $('#lesson-prev-text');
    if (!bar || !nextLink) return;

    const idx = sections.findIndex(s => s.id === sectionId);
    const prev = idx > 0 ? sections[idx - 1] : null;
    const next = idx >= 0 && idx < sections.length - 1 ? sections[idx + 1] : null;
    const nextWeek = !next ? nextWeekId(routeId) : null;

    bar.hidden = false;

    if (prevLink) {
      if (prev) {
        prevLink.hidden = false;
        prevLink.href = `#${routeId}--${prev.id}`;
        prevLink.setAttribute('data-route', routeId);
        if (prevText) prevText.textContent = prev.label.length > 28 ? prev.label.slice(0, 28) + '…' : prev.label;
      } else {
        prevLink.hidden = true;
      }
    }

    if (next) {
      if (nextText) nextText.textContent = next.label;
      nextLink.href = `#${routeId}--${next.id}`;
      nextLink.setAttribute('data-route', routeId);
      nextLink.hidden = false;
    } else if (nextWeek && ROUTES.weeks?.[nextWeek]) {
      if (nextText) nextText.textContent = `Следующая неделя: ${ROUTES.weeks[nextWeek]}`;
      nextLink.href = `#${nextWeek}`;
      nextLink.setAttribute('data-route', nextWeek);
      nextLink.hidden = false;
    } else {
      if (nextText) nextText.textContent = 'Курс завершён';
      nextLink.hidden = true;
    }
  }

  function loadGiscus(term) {
    const block = $('#comments-block');
    const container = $('#giscus-container');
    if (!block || !container || !GISCUS) return;
    if (!term) {
      block.hidden = true;
      return;
    }
    block.hidden = false;
    if (term === giscusTerm && container.querySelector('iframe')) return;
    giscusTerm = term;
    container.innerHTML = '';
    const script = document.createElement('script');
    script.src = 'https://giscus.app/client.js';
    script.async = true;
    script.crossOrigin = 'anonymous';
    script.setAttribute('data-repo', GISCUS.repo);
    script.setAttribute('data-repo-id', GISCUS.repoId);
    script.setAttribute('data-category', GISCUS.category);
    script.setAttribute('data-category-id', GISCUS.categoryId);
    script.setAttribute('data-mapping', 'specific');
    script.setAttribute('data-term', term);
    script.setAttribute('data-strict', '1');
    script.setAttribute('data-reactions-enabled', '1');
    script.setAttribute('data-emit-metadata', '0');
    script.setAttribute('data-input-position', 'bottom');
    script.setAttribute('data-theme', 'transparent_dark');
    script.setAttribute('data-lang', 'ru');
    script.setAttribute('data-loading', 'lazy');
    container.appendChild(script);
  }

  function renderQuizBlock(quizzes, weekId) {
    if (!quizzes?.length) return '';
    const saved = getQuizProgress()[weekId];
    const header = saved
      ? `<p class="quiz-saved">Прошлый результат: ${saved.score}/${saved.total}</p>`
      : '';
    const items = quizzes.map((q, qi) => {
      const opts = (q.options || []).map((o, oi) =>
        `<button type="button" class="quiz-opt" data-q="${qi}" data-o="${oi}" data-ok="${o.ok ? '1' : '0'}">${o.t}</button>`
      ).join('');
      return `<div class="quiz-item" data-qi="${qi}">
        <p class="quiz-q"><span class="quiz-num">${qi + 1}</span> ${q.q}</p>
        <div class="quiz-opts">${opts}</div>
        <p class="quiz-feedback" hidden></p>
      </div>`;
    }).join('');
    return `<div class="quiz-block" data-week="${weekId}">
      <h3 class="quiz-title">${icon('quiz')} Интерактивный тест</h3>
      <p class="quiz-hint">Выберите ответ — feedback сразу. Можно пройти заново.</p>
      ${header}
      ${items}
      <div class="quiz-score" hidden></div>
      <button type="button" class="btn btn-ghost btn-sm quiz-reset" hidden>Пройти снова</button>
    </div>`;
  }

  function setupQuizzes(root, weekId, quizzes) {
    const block = root.querySelector('.quiz-block');
    if (!block || !quizzes?.length) return;
    const state = quizzes.map(() => null);
    const scoreEl = block.querySelector('.quiz-score');
    const resetBtn = block.querySelector('.quiz-reset');

    function finishIfDone() {
      if (state.some(s => s === null)) return;
      const score = state.filter(Boolean).length;
      setQuizScore(weekId, score, quizzes.length);
      if (scoreEl) {
        scoreEl.hidden = false;
        scoreEl.textContent = `Итого: ${score} / ${quizzes.length}`;
        scoreEl.className = 'quiz-score ' + (score === quizzes.length ? 'perfect' : score >= quizzes.length * 0.7 ? 'good' : 'retry');
      }
      if (resetBtn) resetBtn.hidden = false;
    }

    block.addEventListener('click', e => {
      const btn = e.target.closest('.quiz-opt');
      if (!btn || btn.disabled) return;
      const qi = +btn.dataset.q;
      const ok = btn.dataset.ok === '1';
      const item = block.querySelector(`.quiz-item[data-qi="${qi}"]`);
      if (!item || state[qi] !== null) return;
      state[qi] = ok;
      item.querySelectorAll('.quiz-opt').forEach(b => {
        b.disabled = true;
        if (b.dataset.ok === '1') b.classList.add('correct');
        if (b === btn && !ok) b.classList.add('wrong');
      });
      const fb = item.querySelector('.quiz-feedback');
      const explain = quizzes[qi].explain || '';
      if (fb) {
        fb.hidden = false;
        fb.className = 'quiz-feedback ' + (ok ? 'ok' : 'bad');
        fb.textContent = (ok ? 'Верно. ' : 'Неверно. ') + explain;
      }
      finishIfDone();
    });

    resetBtn?.addEventListener('click', () => {
      const wrap = block.parentElement;
      if (!wrap) return;
      const fresh = renderQuizBlock(quizzes, weekId);
      const tmp = document.createElement('div');
      tmp.innerHTML = fresh;
      const next = tmp.firstElementChild;
      block.replaceWith(next);
      setupQuizzes(wrap, weekId, quizzes);
    });
  }

  function renderWeekHub(data, routeId) {
    const sections = lessonSections(data);
    const daysDone = getDayProgress();
    const cards = sections.map(s => {
      const done = s.kind === 'day' && daysDone[s.id];
      const kindLabel = s.kind === 'day' ? 'День' : s.kind === 'project' ? 'Проект' : s.kind === 'review' ? 'Ревью' : 'Урок';
      return `<a class="lesson-card${done ? ' done' : ''}" href="#${routeId}--${s.id}" data-route="${routeId}">
        <span class="lesson-card-kind">${kindLabel}</span>
        <strong>${s.label}</strong>
        ${done ? `<span class="lesson-card-done">${icon('check_circle')}</span>` : ''}
      </a>`;
    }).join('');

    return `<div class="week-hub">
      ${data.introHtml ? `<div class="prose week-intro">${data.introHtml}</div>` : ''}
      <h2 class="week-hub-title">Выберите урок</h2>
      <div class="lesson-grid">${cards}</div>
    </div>`;
  }

  function renderDoc(data, routeId, anchor) {
    const title = $('#doc-page-title');
    const subtitle = $('#doc-lesson-subtitle');
    const tocEl = $('#doc-toc');
    const content = $('#doc-content');
    const isWeek = /^week-\d{2}$/.test(routeId);
    const sections = lessonSections(data);
    const pageTitle = data.fullTitle || data.title;

    currentRoute = routeId;
    currentSectionId = '';

    if (!isWeek) {
      if (title) title.textContent = pageTitle;
      document.title = `${pageTitle} · web-roadmap`;
      if (subtitle) { subtitle.hidden = true; subtitle.textContent = ''; }
      updateBreadcrumb('', null);
      if (tocEl) tocEl.innerHTML = buildToc(data.toc?.map(t => ({ ...t, kind: 'section' })) || [], routeId, anchor);
      if (content) {
        content.innerHTML = `<div class="prose lesson-prose">${data.html}</div>`;
        highlightCode(content);
        applyTrackFilter(content);
      }
      updateMarkDoneBtn(routeId);
      updateMarkDayBtn(null);
      updateGithubToolbar(routeId, '', data);
      updateWeekProgress('', []);
      const bar = $('#lesson-next');
      if (bar) bar.hidden = true;
      loadGiscus(null);
      const comments = $('#comments-block');
      if (comments) comments.hidden = true;
      window.scrollTo(0, 0);
      return;
    }

    let section = anchor ? sections.find(s => s.id === anchor) : null;
    if (!section && !anchor && sections.length) {
      const first = sections.find(s => s.kind === 'day') || sections[0];
      if (first && location.hash !== `#${routeId}--${first.id}`) {
        history.replaceState(null, '', `#${routeId}--${first.id}`);
        section = first;
        anchor = first.id;
      }
    }

    if (!section) {
      if (title) title.textContent = pageTitle;
      document.title = `${pageTitle} · web-roadmap`;
      if (subtitle) {
        subtitle.hidden = false;
        subtitle.textContent = 'Оглавление недели';
      }
      updateBreadcrumb(data.title || pageTitle, { label: 'Оглавление' });
      if (tocEl) tocEl.innerHTML = buildToc(sections, routeId, '');
      if (content) {
        content.innerHTML = renderWeekHub(data, routeId);
        applyTrackFilter(content);
      }
      updateMarkDoneBtn(routeId);
      updateMarkDayBtn(null);
      updateGithubToolbar(routeId, '', data);
      updateWeekProgress(routeId, sections);
      updateLessonNav(sections, routeId, sections[0]?.id);
      loadGiscus(routeId);
      saveLastRoute(routeId, '');
      window.scrollTo(0, 0);
      return;
    }

    currentSectionId = section.id;
    const html = section.html || data.html;
    if (title) title.textContent = section.label;
    document.title = `${section.label} · ${data.title} · web-roadmap`;
    if (subtitle) {
      subtitle.hidden = false;
      subtitle.textContent = pageTitle;
    }
    updateBreadcrumb(data.title || pageTitle, section);
    if (tocEl) tocEl.innerHTML = buildToc(sections, routeId, section.id);
    if (content) {
      let body = html;
      if (section.kind === 'review' && data.quizzes?.length) {
        body = html + renderQuizBlock(data.quizzes, routeId);
      }
      content.innerHTML = `<div class="prose lesson-prose">${body}</div>`;
      highlightCode(content);
      applyTrackFilter(content);
      if (section.kind === 'review') setupQuizzes(content, routeId, data.quizzes || []);
    }
    updateMarkDoneBtn(routeId);
    updateMarkDayBtn(section);
    updateGithubToolbar(routeId, section.id, data);
    updateWeekProgress(routeId, sections);
    updateLessonNav(sections, routeId, section.id);
    loadGiscus(routeId);
    saveLastRoute(routeId, section.id);
    window.scrollTo(0, 0);
  }

  async function route() {
    let raw = (location.hash || '#home').slice(1);
    if (!raw || raw === 'home') raw = 'home';

    let routeId = raw;
    let anchor = '';
    if (raw.includes('--')) {
      [routeId, anchor] = raw.split('--');
    }

    const lessonNext = $('#lesson-next');
    if (lessonNext) lessonNext.hidden = true;
    const comments = $('#comments-block');
    if (comments) comments.hidden = true;

    if (routeId === 'home') {
      showView('home');
      currentRoute = 'home';
      document.title = 'web-roadmap — Full-Stack за 22 недели';
      updateCards();
      updateResumeBanner();
      renderProgressMap();
      return;
    }

    const isWeek = /^week-\d{2}$/.test(routeId);
    const isPage = PAGE_IDS.includes(routeId);

    if (isWeek || isPage) {
      showView('doc');
      const slot = $('#doc-content');
      if (slot) slot.innerHTML = '<div class="loading">Загрузка…</div>';
      try {
        const data = isWeek ? await fetchWeek(routeId) : await fetchPage(routeId);
        renderDoc(data, routeId, anchor);
      } catch (err) {
        if (slot) slot.innerHTML = `<p class="loading">Не удалось загрузить. <a href="#home">На главную</a></p>`;
      }
      return;
    }

    showView('home');
    const el = document.getElementById(routeId);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
    updateResumeBanner();
  }

  function initSearch() {
    const overlay = $('#search-overlay');
    const input = $('#search-input');
    const results = $('#search-results');
    if (!overlay || !input) return;

    function openSearch() {
      overlay.classList.add('open');
      input.value = '';
      input.focus();
      results.innerHTML = '';
    }
    function closeSearch() {
      overlay.classList.remove('open');
    }

    $('#search-btn')?.addEventListener('click', openSearch);
    overlay.addEventListener('click', e => { if (e.target === overlay) closeSearch(); });
    document.addEventListener('keydown', e => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); openSearch(); }
      if (e.key === 'Escape') closeSearch();
    });

    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      if (q.length < 2) { results.innerHTML = ''; return; }
      const hits = SEARCH_INDEX.filter(item =>
        item.title.toLowerCase().includes(q) || item.text.toLowerCase().includes(q)
      ).slice(0, 12);
      results.innerHTML = hits.map(h =>
        `<a href="#${h.route}"><span>${h.title}</span><div class="meta">${h.snippet}</div></a>`
      ).join('') || '<p class="meta" style="padding:12px">Ничего не найдено</p>';
      results.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', () => closeSearch());
      });
    });
  }

  function initReadingMode() {
    const btn = $('#reading-mode-btn');
    if (localStorage.getItem(READING_KEY) === '1') document.body.classList.add('reading-mode');
    btn?.addEventListener('click', () => {
      document.body.classList.toggle('reading-mode');
      localStorage.setItem(READING_KEY, document.body.classList.contains('reading-mode') ? '1' : '0');
    });
  }

  function initPhaseFilters() {
    const chips = $$('#phase-filters .phase-chip');
    const cards = $$('#weeks-grid .card');
    if (!chips.length) return;
    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        const filter = chip.getAttribute('data-filter');
        chips.forEach(c => c.classList.toggle('active', c === chip));
        cards.forEach(card => {
          const phase = card.getAttribute('data-phase');
          card.style.display = filter === 'all' || phase === filter ? '' : 'none';
        });
      });
    });
  }

  function initBurger() {
    const burger = $('#burger-btn');
    const links = $('#nav-links');
    burger?.addEventListener('click', () => links?.classList.toggle('open'));
  }

  function initGithubFeatures() {
    fetch(`https://api.github.com/repos/${REPO}`)
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if (!data) return;
        const n = data.stargazers_count;
        const starLabel = $('#star-count-label');
        const navLabel = $('#nav-star-label');
        if (starLabel) starLabel.textContent = `Star · ${n}`;
        if (navLabel) navLabel.textContent = `★ ${n}`;
      })
      .catch(() => {});

    async function copyProgress() {
      const json = exportProgress();
      try {
        await navigator.clipboard.writeText(json);
        alert('Прогресс скопирован. Сохраните в learning-log/progress.json');
      } catch {
        downloadText('web-roadmap-progress.json', json);
      }
    }

    function downloadText(name, text) {
      const blob = new Blob([text], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = name;
      a.click();
      URL.revokeObjectURL(a.href);
    }

    $$('#progress-export-btn').forEach(btn => btn.addEventListener('click', copyProgress));

    $('#export-learning-log-btn')?.addEventListener('click', () => {
      downloadText('progress.json', exportLearningLogPayload());
      alert('Скачан progress.json — положите в learning-log/ и сделайте коммит.\nИли создайте private gist на gist.github.com и вставьте JSON.');
    });

    const fileInput = $('#progress-import-file');
    $$('#progress-import-btn').forEach(btn => btn.addEventListener('click', () => fileInput?.click()));
    fileInput?.addEventListener('change', async () => {
      const file = fileInput.files?.[0];
      if (!file) return;
      try {
        importProgress(await file.text());
        alert('Прогресс импортирован');
      } catch {
        alert('Не удалось прочитать файл');
      }
      fileInput.value = '';
    });

    $('#copy-clone-btn')?.addEventListener('click', async () => {
      const cmd = `git clone ${REPO_URL}.git`;
      try {
        await navigator.clipboard.writeText(cmd);
        alert('Команда clone скопирована');
      } catch {
        prompt('Скопируйте:', cmd);
      }
    });
  }

  function initTrackToggle() {
    syncTrackChips();
    document.addEventListener('click', e => {
      const btn = e.target.closest('[data-track-mode]');
      if (!btn) return;
      setTrackMode(btn.getAttribute('data-track-mode'));
    });
  }

  document.addEventListener('click', e => {
    const a = e.target.closest('[data-route]');
    if (a) {
      e.preventDefault();
      const href = a.getAttribute('href');
      if (href && href.startsWith('#') && href.length > 1) {
        location.hash = href.slice(1);
      } else {
        location.hash = a.getAttribute('data-route');
      }
    }
  });

  window.addEventListener('hashchange', route);

  $('#share-btn')?.addEventListener('click', async () => {
    const url = 'https://krwg.github.io/web-roadmap/';
    try {
      if (navigator.share) await navigator.share({ title: 'web-roadmap', text: 'Full-stack за 22 недели', url });
      else { await navigator.clipboard.writeText(url); alert('Ссылка скопирована'); }
    } catch (_) {}
  });

  updateProgressUI();
  updateCards();
  updateResumeBanner();
  renderProgressMap();
  initSearch();
  initReadingMode();
  initPhaseFilters();
  initBurger();
  initGithubFeatures();
  initTrackToggle();
  route();

  window.webRoadmapProgress = { export: exportProgress, import: importProgress };

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  }

  /* Ambient background: CSS mesh always; canvas rain for capable browsers */
  (function ambientBg() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      document.body.classList.add('bg-static');
      return;
    }

    const ua = navigator.userAgent;
    const isSafari = /Safari/i.test(ua) && !/Chrome|Chromium|Android/i.test(ua);
    const isIOS = /iP(hone|ad|od)/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);

    // CSS mesh works everywhere (including Safari)
    document.body.classList.add('bg-mesh');

    if (isSafari || isIOS) {
      // Skip heavy canvas on Safari — mesh + soft orbs only
      document.body.classList.add('bg-safari');
      return;
    }

    const canvas = document.getElementById('code-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;

    const snippets = ['git commit', 'useEffect', 'SELECT *', 'docker compose', 'async await', 'npm run'];
    let cols = 0;
    let drops = [];
    let fontSize = 14;
    let running = true;
    let raf = 0;

    function resize() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const w = window.innerWidth;
      const h = window.innerHeight;
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      fontSize = w < 700 ? 12 : 14;
      cols = Math.max(8, Math.floor(w / (fontSize * 4)));
      drops = Array.from({ length: cols }, () => Math.random() * (h / fontSize));
    }

    let last = 0;
    function draw(ts) {
      raf = requestAnimationFrame(draw);
      if (!running || document.body.classList.contains('reading-mode') || document.hidden) return;
      if (ts - last < 48) return; // ~20fps — easier on GPU
      last = ts;

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.font = `${fontSize}px ui-monospace, SFMono-Regular, Menlo, monospace`;
      const w = window.innerWidth;
      const h = window.innerHeight;
      const gap = w / cols;

      for (let i = 0; i < cols; i++) {
        const t = snippets[(i + Math.floor(drops[i])) % snippets.length];
        ctx.fillStyle = Math.random() > 0.96 ? 'rgba(255,255,255,0.55)' : 'rgba(160,160,175,0.28)';
        ctx.fillText(t, i * gap, drops[i] * fontSize);
        if (drops[i] * fontSize > h && Math.random() > 0.96) drops[i] = 0;
        drops[i] += 0.35 + Math.random() * 0.25;
      }
    }

    document.addEventListener('visibilitychange', () => {
      running = !document.hidden;
    });
    resize();
    addEventListener('resize', resize);
    raf = requestAnimationFrame(draw);
  })();
})();
