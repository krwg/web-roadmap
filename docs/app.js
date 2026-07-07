/* global Prism */
(function () {
  const ROUTES = window.SITE_ROUTES || {};
  const WEEK_IDS = Object.keys(ROUTES.weeks || {});
  const PAGE_IDS = Object.keys(ROUTES.pages || {});
  const SEARCH_INDEX = window.SEARCH_INDEX || [];
  const PROGRESS_KEY = 'web-roadmap-progress';
  const READING_KEY = 'web-roadmap-reading';

  const weekCache = {};
  let currentRoute = '';

  function $(sel, root = document) { return root.querySelector(sel); }
  function $$(sel, root = document) { return [...root.querySelectorAll(sel)]; }

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
  }
  function toggleWeekDone(id) {
    const p = getProgress();
    setProgress(id, !p[id]);
  }

  function updateProgressUI() {
    const p = getProgress();
    const done = WEEK_IDS.filter(w => p[w]).length;
    const el = $('#progress-fill');
    const label = $('#progress-label');
    if (el) el.style.width = `${(done / WEEK_IDS.length) * 100}%`;
    if (label) label.textContent = `Прогресс: ${done} / ${WEEK_IDS.length} недель`;
  }

  function updateCards() {
    const p = getProgress();
    $$('.card[data-route]').forEach(card => {
      const id = card.getAttribute('data-route');
      card.classList.toggle('done', !!p[id]);
      let badge = card.querySelector('.done-badge');
      if (p[id]) {
        if (!badge) {
          badge = document.createElement('span');
          badge.className = 'done-badge';
          badge.textContent = '✓';
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
    const file = ROUTES.pages[id];
    const res = await fetch(`pages/${file}`);
    if (!res.ok) throw new Error('Page not found');
    const data = await res.json();
    weekCache[id] = data;
    return data;
  }

  function buildToc(toc, routeId) {
    if (!toc || !toc.length) return '';
    return `<h4>Содержание</h4>` + toc.map(t =>
      `<a href="#${routeId}--${t.id}" data-anchor="${t.id}">${t.label}</a>`
    ).join('');
  }

  function highlightCode(root) {
    if (typeof Prism !== 'undefined') {
      $$('pre code', root).forEach(el => Prism.highlightElement(el));
    }
    if (typeof mermaid !== 'undefined') {
      $$('.mermaid', root).forEach((el, i) => {
        if (el.dataset.processed) return;
        mermaid.run({ nodes: [el] }).catch(() => {});
      });
    }
  }

  function renderDoc(data, routeId) {
    const title = $('#doc-page-title');
    const tocEl = $('#doc-toc');
    const content = $('#doc-content');
    if (title) title.textContent = data.fullTitle || data.title;
    if (tocEl) tocEl.innerHTML = buildToc(data.toc, routeId);
    if (content) {
      content.innerHTML = `<div class="prose">${data.html}</div>`;
      highlightCode(content);
      setupTocScroll(content, routeId);
      setupDayNav(data.toc, routeId);
    }
    const markBtn = $('#mark-done-btn');
    if (markBtn) {
      const isWeek = /^week-\d{2}$/.test(routeId);
      markBtn.hidden = !isWeek;
      markBtn.textContent = getProgress()[routeId] ? '✓ Неделя пройдена' : 'Отметить неделю';
      markBtn.onclick = () => { toggleWeekDone(routeId); markBtn.textContent = getProgress()[routeId] ? '✓ Неделя пройдена' : 'Отметить неделю'; };
    }
  }

  function setupTocScroll(content, routeId) {
    const links = $$('#doc-toc a[data-anchor]');
    links.forEach(a => {
      a.addEventListener('click', e => {
        e.preventDefault();
        const id = a.getAttribute('data-anchor');
        const target = content.querySelector(`#${id}`) || content.querySelector(`[id="${id}"]`);
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        history.replaceState(null, '', `#${routeId}--${id}`);
      });
    });
  }

  function setupDayNav(toc, routeId) {
    const prose = $('#doc-content .prose');
    if (!prose || !toc) return;
    const days = toc.filter(t => t.id.includes('-day-'));
    if (days.length < 2) return;
    const hash = location.hash;
    const m = hash.match(/--(.+)$/);
    const currentId = m ? m[1] : days[0].id;
    const idx = days.findIndex(d => d.id === currentId);
    const prev = days[idx - 1];
    const next = days[idx + 1];
    const nav = document.createElement('div');
    nav.className = 'day-nav';
    nav.innerHTML = prev
      ? `<a class="btn btn-ghost" href="#${routeId}--${prev.id}">← ${prev.label}</a>`
      : '<span></span>';
    nav.innerHTML += next
      ? `<a class="btn btn-secondary" href="#${routeId}--${next.id}">${next.label} →</a>`
      : '';
    prose.appendChild(nav);
    nav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', e => {
        e.preventDefault();
        location.hash = a.getAttribute('href').slice(1);
      });
    });
  }

  async function route() {
    let raw = (location.hash || '#home').slice(1);
    if (!raw || raw === 'home') raw = 'home';

    let routeId = raw;
    let anchor = '';
    if (raw.includes('--')) {
      [routeId, anchor] = raw.split('--');
    }

    if (routeId === 'home') {
      showView('home');
      currentRoute = 'home';
      updateCards();
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
        renderDoc(data, routeId);
        currentRoute = routeId;
        if (anchor) {
          const target = $(`#${anchor}`, $('#doc-content')) || $(`[id="${anchor}"]`, $('#doc-content'));
          if (target) setTimeout(() => target.scrollIntoView({ behavior: 'smooth' }), 100);
        } else {
          window.scrollTo(0, 0);
        }
      } catch (err) {
        if (slot) slot.innerHTML = `<p class="loading">Не удалось загрузить. <a href="#home">На главную</a></p>`;
      }
      return;
    }

    showView('home');
    const el = document.getElementById(routeId);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
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

  function initBurger() {
    const burger = $('#burger-btn');
    const links = $('#nav-links');
    burger?.addEventListener('click', () => links?.classList.toggle('open'));
  }

  document.addEventListener('click', e => {
    const a = e.target.closest('[data-route]');
    if (a) {
      e.preventDefault();
      const r = a.getAttribute('data-route');
      location.hash = r;
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
  initSearch();
  initReadingMode();
  initBurger();
  route();

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  }

  (function rain() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const canvas = document.getElementById('code-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const snippets = ['git commit', 'useEffect', 'SELECT *', 'docker compose', 'async await'];
    let cols, drops, fontSize = 13;
    function resize() {
      canvas.width = innerWidth; canvas.height = innerHeight;
      cols = Math.floor(canvas.width / fontSize);
      drops = Array(cols).fill(1);
    }
    function draw() {
      if (document.body.classList.contains('reading-mode')) { requestAnimationFrame(draw); return; }
      ctx.fillStyle = 'rgba(5,5,8,0.09)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.font = fontSize + 'px monospace';
      for (let i = 0; i < drops.length; i++) {
        const t = snippets[Math.floor(Math.random() * snippets.length)];
        ctx.fillStyle = Math.random() > 0.97 ? '#fff' : 'rgba(160,160,170,0.5)';
        ctx.fillText(t, i * fontSize, drops[i] * fontSize);
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
      }
      requestAnimationFrame(draw);
    }
    resize();
    addEventListener('resize', resize);
    draw();
  })();
})();
