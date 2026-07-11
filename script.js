const header = document.querySelector('[data-header]');
const navToggle = document.querySelector('[data-nav-toggle]');
const nav = document.querySelector('[data-nav]');
const revealTargets = document.querySelectorAll('.reveal');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const langButtons = document.querySelectorAll('[data-lang-button]');
const skipLink = document.querySelector('.skip-link');

const LANGUAGE_KEY = 'flowmatic-lang';
const LANGUAGE_LABELS = {
  en: {
    openMenu: 'Open menu',
    closeMenu: 'Close menu',
    skip: 'Skip to content',
    ct: { home: 'HOME', running: 'RUNNING', end: 'END', saved: 'SAVED' },
    amr: ['MONITORING LINE A', 'CALL REQUEST', 'AMR DISPATCHED', 'SUPPLY COMPLETE']
  },
  ko: {
    openMenu: '메뉴 열기',
    closeMenu: '메뉴 닫기',
    skip: '본문으로 건너뛰기',
    ct: { home: '대기', running: '측정중', end: '종료', saved: '저장됨' },
    amr: ['라인 A 감시 중', '호출 요청', 'AMR 배차', '보급 완료']
  }
};

function getCurrentLanguage() {
  return document.body.dataset.lang || 'ko';
}

function setToggleLabel(isOpen) {
  if (!navToggle) return;
  const label = navToggle.querySelector('.sr-only');
  const lang = getCurrentLanguage();
  const text = isOpen ? LANGUAGE_LABELS[lang].closeMenu : LANGUAGE_LABELS[lang].openMenu;
  if (label) label.textContent = text;
}

function applyLanguage(lang) {
  const safeLang = lang === 'en' ? 'en' : 'ko';
  document.body.dataset.lang = safeLang;
  document.documentElement.lang = safeLang;
  localStorage.setItem(LANGUAGE_KEY, safeLang);
  langButtons.forEach((button) => button.classList.toggle('is-active', button.dataset.langButton === safeLang));
  if (skipLink) skipLink.textContent = LANGUAGE_LABELS[safeLang].skip;
  setToggleLabel(document.body.classList.contains('nav-open'));
  scheduleSemanticFit();
}

function updateHeaderState() {
  if (!header) return;
  header.classList.toggle('is-scrolled', window.scrollY > 16 || document.body.classList.contains('technology-page'));
}

function closeNav() {
  document.body.classList.remove('nav-open');
  if (!navToggle) return;
  navToggle.setAttribute('aria-expanded', 'false');
  setToggleLabel(false);
}

function toggleNav() {
  if (!navToggle) return;
  const isOpen = document.body.classList.toggle('nav-open');
  navToggle.setAttribute('aria-expanded', String(isOpen));
  setToggleLabel(isOpen);
}

function initReveal() {
  if (prefersReducedMotion || !('IntersectionObserver' in window)) {
    revealTargets.forEach((target) => target.classList.add('is-visible'));
    return;
  }
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
  revealTargets.forEach((target) => observer.observe(target));
}

function initNavigation() {
  if (navToggle) navToggle.addEventListener('click', toggleNav);
  if (nav) nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeNav));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeNav();
  });
}

function initLanguageToggle() {
  const saved = localStorage.getItem(LANGUAGE_KEY);
  const initial = saved === 'en' || saved === 'ko' ? saved : 'ko';
  applyLanguage(initial);
  langButtons.forEach((button) => {
    button.addEventListener('click', () => applyLanguage(button.dataset.langButton));
  });
}

function initDemoVideos() {
  const players = document.querySelectorAll('[data-demo-video]');
  players.forEach((player) => {
    const video = player.querySelector('video');
    const placeholder = player.querySelector('[data-video-placeholder]');
    const base = player.dataset.videoBase;
    if (!video || !base) return;
    const candidates = [`${base}.mp4`, `${base}.webm`, `${base}.mov`];
    let candidateIndex = 0;
    let settled = false;
    const showVideo = () => {
      if (settled) return;
      settled = true;
      player.classList.add('has-video');
      video.hidden = false;
      if (placeholder) placeholder.hidden = true;
    };
    const tryNext = () => {
      if (settled) return;
      if (candidateIndex >= candidates.length) {
        video.removeAttribute('src');
        video.load();
        return;
      }
      const candidate = candidates[candidateIndex];
      candidateIndex += 1;
      const onLoaded = () => { cleanup(); showVideo(); };
      const onError = () => { cleanup(); tryNext(); };
      const cleanup = () => {
        video.removeEventListener('loadedmetadata', onLoaded);
        video.removeEventListener('canplay', onLoaded);
        video.removeEventListener('error', onError);
      };
      video.addEventListener('loadedmetadata', onLoaded, { once: true });
      video.addEventListener('canplay', onLoaded, { once: true });
      video.addEventListener('error', onError, { once: true });
      video.src = candidate;
      video.load();
    };
    tryNext();
  });
}

function formatCycleTime(seconds) {
  const safe = Math.max(0, seconds);
  const whole = Math.floor(safe);
  const tenth = Math.floor((safe - whole) * 10);
  return `00:${String(whole).padStart(2, '0')}.${tenth}`;
}

function initCtExplainer() {
  const visual = document.querySelector('[data-tech-animation="ct"]');
  if (!visual || prefersReducedMotion) return;
  const timer = visual.querySelector('[data-ct-timer]');
  const state = visual.querySelector('[data-ct-state]');
  const result = visual.querySelector('[data-ct-result]');
  const loopDuration = 4800;
  const measuredCycle = 12.4;
  const start = performance.now();
  function tick(now) {
    const phase = (now - start) % loopDuration;
    const lang = getCurrentLanguage();
    const labels = LANGUAGE_LABELS[lang].ct;
    if (phase < 700) {
      if (state) state.textContent = labels.home;
      if (timer) timer.textContent = '00:00.0';
    } else if (phase < 3900) {
      const progress = (phase - 700) / 3200;
      if (state) state.textContent = labels.running;
      if (timer) timer.textContent = formatCycleTime(progress * measuredCycle);
    } else if (phase < 4450) {
      if (state) state.textContent = labels.end;
      if (timer) timer.textContent = formatCycleTime(measuredCycle);
      if (result) result.textContent = `${measuredCycle.toFixed(1)} s`;
    } else {
      if (state) state.textContent = labels.saved;
      if (timer) timer.textContent = formatCycleTime(measuredCycle);
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

function initAmrExplainer() {
  const visual = document.querySelector('[data-tech-animation="amr"]');
  if (!visual || prefersReducedMotion) return;
  const message = visual.querySelector('[data-amr-message]');
  if (!message) return;
  const loopDuration = 5000;
  const start = performance.now();
  function tick(now) {
    const phase = (now - start) % loopDuration;
    const labels = LANGUAGE_LABELS[getCurrentLanguage()].amr;
    if (phase < 2100) message.textContent = labels[0];
    else if (phase < 3350) message.textContent = labels[1];
    else if (phase < 4400) message.textContent = labels[2];
    else message.textContent = labels[3];
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}



let fitTextTimer = 0;
function readCssNumber(element, propertyName, fallback) {
  const raw = getComputedStyle(element).getPropertyValue(propertyName).trim();
  const value = Number.parseFloat(raw);
  return Number.isFinite(value) ? value : fallback;
}

function visibleSemanticLines(element, lang) {
  const visibleCopy = element.querySelector(`.lang-${lang}`);
  if (visibleCopy && getComputedStyle(visibleCopy).display !== 'none') {
    return [...visibleCopy.querySelectorAll('.copy-line')];
  }
  if (element.querySelector('.lang-en, .lang-ko')) return [];
  return [...element.querySelectorAll('.copy-line')];
}

function semanticTextFits(element, lines, size, availableWidth, availableHeight = Infinity) {
  element.style.fontSize = `${size}px`;
  const widthFits = lines.every((line) => line.scrollWidth <= availableWidth + 0.5);
  const heightFits = element.scrollHeight <= availableHeight + 0.5;
  return widthFits && heightFits;
}

function fitSemanticText() {
  const lang = getCurrentLanguage();

  document.querySelectorAll('[data-fit-text]').forEach((element) => {
    const lines = visibleSemanticLines(element, lang);
    element.style.removeProperty('font-size');
    const availableWidth = Math.max(0, element.clientWidth - readCssNumber(element, '--fit-reserve', 2));
    const heightLimit = readCssNumber(element, '--fit-height', Infinity);
    const availableHeight = Number.isFinite(heightLimit)
      ? Math.max(0, heightLimit - readCssNumber(element, '--fit-height-reserve', 0))
      : Infinity;
    if (!lines.length || availableWidth <= 0) return;

    const computedSize = Number.parseFloat(getComputedStyle(element).fontSize) || 32;
    const minSize = Number.parseFloat(element.dataset.fitMin || '') || 18;
    const dataMax = Number.parseFloat(element.dataset.fitMax || '');
    const cssMax = readCssNumber(element, '--fit-max', computedSize);
    const maxSize = Math.max(minSize, Number.isFinite(dataMax) ? dataMax : cssMax);

    // Start from the largest allowed size. Binary search finds the largest size
    // that preserves every authored copy line without an extra wrap.
    let low = minSize;
    let high = maxSize;

    if (semanticTextFits(element, lines, high, availableWidth, availableHeight)) {
      element.style.fontSize = `${high}px`;
      return;
    }

    // The minimum should normally fit. If not, retain it rather than breaking the line contract.
    if (!semanticTextFits(element, lines, low, availableWidth, availableHeight)) {
      element.style.fontSize = `${low}px`;
      return;
    }

    for (let i = 0; i < 14; i += 1) {
      const mid = (low + high) / 2;
      if (semanticTextFits(element, lines, mid, availableWidth, availableHeight)) low = mid;
      else high = mid;
    }

    // A tiny safety margin prevents sub-pixel clipping at different zoom levels.
    element.style.fontSize = `${Math.max(minSize, low - 0.2).toFixed(2)}px`;
  });
}

function scheduleSemanticFit() {
  window.clearTimeout(fitTextTimer);
  fitTextTimer = window.setTimeout(() => {
    window.requestAnimationFrame(() => window.requestAnimationFrame(fitSemanticText));
  }, 32);
}

window.addEventListener('scroll', updateHeaderState, { passive: true });
window.addEventListener('resize', () => {
  if (window.innerWidth > 768) closeNav();
  scheduleSemanticFit();
});

updateHeaderState();
initNavigation();
initLanguageToggle();
initReveal();
initDemoVideos();
initCtExplainer();
initAmrExplainer();
scheduleSemanticFit();
if (document.fonts?.ready) document.fonts.ready.then(scheduleSemanticFit);
