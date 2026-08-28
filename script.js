const header = document.querySelector('[data-header]');
const navToggle = document.querySelector('[data-nav-toggle]');
const nav = document.querySelector('[data-nav]');
const revealTargets = document.querySelectorAll('.reveal');
const productCards = Array.from(document.querySelectorAll('.product-card')).filter((card) => card.querySelector('.product-link'));
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const langButtons = document.querySelectorAll('[data-lang-button], [data-lang-link]');
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
  },
  ar: {
    openMenu: 'فتح القائمة',
    closeMenu: 'إغلاق القائمة',
    skip: 'تجاوز إلى المحتوى',
    ct: { home: 'الوضع الأساسي', running: 'قيد القياس', end: 'النهاية', saved: 'محفوظ' },
    amr: ['مراقبة الخط A', 'طلب استدعاء', 'تم إرسال AMR', 'اكتمل التزويد']
  }
};

const SUPPORTED_LANGUAGES = new Set(['ko', 'en', 'ar']);

const ARABIC_TRANSLATIONS = Object.freeze({});

function getCurrentLanguage() {
  return document.body.dataset.lang || 'ko';
}

function getControlLanguage(control) {
  return control.dataset.langButton || control.dataset.langLink || '';
}

function normalizeLanguageText(element) {
  const copyLines = element.querySelectorAll('.copy-line');
  if (copyLines.length) {
    return Array.from(copyLines).map((line) => line.textContent.trim()).join(' ').replace(/\s+/g, ' ').trim();
  }
  return element.textContent.replace(/\s+/g, ' ').trim();
}

function splitArabicCopy(text, preferredLineCount) {
  const explicitLines = text.split('|').map((line) => line.trim()).filter(Boolean);
  if (explicitLines.length > 1 || preferredLineCount <= 1) return explicitLines;
  const words = text.split(/\s+/).filter(Boolean);
  if (words.length <= preferredLineCount) return words;
  const lines = [];
  const wordsPerLine = Math.ceil(words.length / preferredLineCount);
  for (let i = 0; i < preferredLineCount; i += 1) {
    const start = i * wordsPerLine;
    const end = i === preferredLineCount - 1 ? words.length : start + wordsPerLine;
    const line = words.slice(start, end).join(' ');
    if (line) lines.push(line);
  }
  return lines;
}

function createArabicSpan(source, translation) {
  const span = document.createElement('span');
  span.className = Array.from(source.classList)
    .map((className) => (className === 'lang-en' ? 'lang-ar' : className))
    .join(' ');
  span.lang = 'ar';
  span.dir = 'rtl';
  const sourceLines = source.querySelectorAll('.copy-line');
  if (source.classList.contains('copy-lines') || sourceLines.length) {
    const lineCount = Math.max(sourceLines.length, 1);
    splitArabicCopy(translation, lineCount).forEach((line) => {
      const lineSpan = document.createElement('span');
      lineSpan.className = 'copy-line';
      lineSpan.textContent = line;
      span.appendChild(lineSpan);
    });
  } else {
    span.textContent = translation.replace(/\s*\|\s*/g, ' ');
  }
  return span;
}

function initArabicLanguageSpans() {
  document.querySelectorAll('.lang-en').forEach((source) => {
    const key = normalizeLanguageText(source);
    const translation = ARABIC_TRANSLATIONS[key];
    if (!translation || source.parentElement?.querySelector(':scope > .lang-ar')) return;
    const arabicSpan = createArabicSpan(source, translation);
    const koreanSibling = source.nextElementSibling?.classList.contains('lang-ko') ? source.nextElementSibling : null;
    (koreanSibling || source).after(arabicSpan);
  });
}

function setToggleLabel(isOpen) {
  if (!navToggle) return;
  const label = navToggle.querySelector('.sr-only');
  const lang = getCurrentLanguage();
  const text = isOpen ? LANGUAGE_LABELS[lang].closeMenu : LANGUAGE_LABELS[lang].openMenu;
  if (label) label.textContent = text;
}

function applyLanguage(lang) {
  const safeLang = SUPPORTED_LANGUAGES.has(lang) ? lang : 'ko';
  document.body.dataset.lang = safeLang;
  document.documentElement.lang = safeLang;
  document.documentElement.dir = safeLang === 'ar' ? 'rtl' : 'ltr';
  localStorage.setItem(LANGUAGE_KEY, safeLang);
  langButtons.forEach((button) => button.classList.toggle('is-active', getControlLanguage(button) === safeLang));
  if (skipLink) skipLink.textContent = LANGUAGE_LABELS[safeLang].skip;
  setToggleLabel(document.body.classList.contains('nav-open'));
  scheduleSemanticFit();
}

function applyStaticLanguage(lang) {
  const safeLang = SUPPORTED_LANGUAGES.has(lang) ? lang : 'ko';
  document.body.dataset.lang = safeLang;
  document.documentElement.lang = safeLang;
  document.documentElement.dir = safeLang === 'ar' ? 'rtl' : 'ltr';
  langButtons.forEach((button) => button.classList.toggle('is-active', getControlLanguage(button) === safeLang));
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
  if (prefersReducedMotion || !('requestAnimationFrame' in window)) {
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

function initProductCtas() {
  if (!productCards.length) return;
  if (prefersReducedMotion || !('IntersectionObserver' in window)) {
    productCards.forEach((card) => {
      const link = card.querySelector('.product-link');
      if (!link) return;
      card.classList.add('is-cta-active');
      link.style.setProperty('--cta-progress', '1');
      link.style.setProperty('--cta-click-offset', '0%');
      link.style.setProperty('--cta-mondrian-offset', '0%');
      link.style.setProperty('--cta-left-padding', 'calc(var(--cta-click-width) + 14px)');
      link.style.setProperty('--cta-right-padding', '58px');
    });
    return;
  }
  let isScheduled = false;
  const smoothStep = (value) => value * value * (3 - (2 * value));
  const getLayoutTop = (element) => {
    let top = 0;
    let node = element;
    while (node) {
      top += node.offsetTop;
      node = node.offsetParent;
    }
    return top;
  };
  const getRows = () => {
    const rows = [];
    productCards.forEach((card) => {
      const link = card.querySelector('.product-link');
      if (!link) return;
      const top = getLayoutTop(card);
      let row = rows.find((item) => Math.abs(item.top - top) < 8);
      if (!row) {
        row = { top, items: [] };
        rows.push(row);
      }
      row.items.push({ card, link });
    });
    return rows;
  };
  const setCtaState = (card, link, progress) => {
    const rect = link.getBoundingClientRect();
    const clickWidth = Math.max(82, Math.min(rect.width * 0.32, 132));
    link.style.setProperty('--cta-progress', progress.toFixed(3));
    link.style.setProperty('--cta-click-offset', `${(-100 + (progress * 100)).toFixed(2)}%`);
    link.style.setProperty('--cta-mondrian-offset', `${(100 - (progress * 100)).toFixed(2)}%`);
    link.style.setProperty('--cta-left-padding', `${(16 + (progress * (clickWidth - 2))).toFixed(2)}px`);
    link.style.setProperty('--cta-right-padding', `${(16 + (progress * 42)).toFixed(2)}px`);
    card.classList.toggle('is-cta-active', progress >= 0.995);
  };
  const updateCtas = () => {
    isScheduled = false;
    const startY = window.innerHeight * 0.9;
    const completeY = window.innerHeight * 0.7;
    const travel = Math.max(startY - completeY, 1);
    const scrollY = window.scrollY || document.documentElement.scrollTop || 0;
    getRows().forEach((row) => {
      const rowBottom = Math.max(...row.items.map(({ card }) => getLayoutTop(card) + card.offsetHeight));
      const centerY = rowBottom - 32 - scrollY;
      const rawProgress = (startY - centerY) / travel;
      const progress = smoothStep(Math.min(Math.max(rawProgress, 0), 1));
      row.items.forEach(({ card, link }) => setCtaState(card, link, progress));
    });
  };
  const requestUpdate = () => {
    if (isScheduled) return;
    isScheduled = true;
    requestAnimationFrame(updateCtas);
  };
  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
  window.addEventListener('flowmatic:layout-change', requestUpdate);
  updateCtas();
}

function initEvidenceSequence() {
  const section = document.querySelector('[data-evidence-sequence]');
  if (!section) return;
  const cards = Array.from(section.querySelectorAll('[data-evidence-card]'));
  if (!cards.length) return;

  let scheduled = false;
  let activeIndex = -1;
  const setActiveCard = (nextIndex) => {
    if (nextIndex === activeIndex) return;
    activeIndex = nextIndex;
    cards.forEach((card, index) => card.classList.toggle('is-scroll-active', index === nextIndex));
  };
  const update = () => {
    scheduled = false;
    const rect = section.getBoundingClientRect();
    const enterLine = window.innerHeight * 0.78;
    const leaveLine = window.innerHeight * 0.28;
    if (rect.top > enterLine || rect.bottom < leaveLine) {
      setActiveCard(-1);
      return;
    }
    const travel = Math.max(rect.height + enterLine - leaveLine, 1);
    const progress = Math.min(Math.max((enterLine - rect.top) / travel, 0), 0.999999);
    setActiveCard(Math.min(cards.length - 1, Math.floor(progress * cards.length)));
  };
  const requestUpdate = () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(update);
  };

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
  window.addEventListener('flowmatic:layout-change', requestUpdate);
  update();
}

function initNavigation() {
  if (navToggle) navToggle.addEventListener('click', toggleNav);
  if (nav) nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeNav));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeNav();
  });
}

function initLanguageToggle() {
  if (document.body.dataset.staticLang === 'true') {
    applyStaticLanguage(document.body.dataset.lang || document.documentElement.lang || 'ko');
    langButtons.forEach((button) => {
      if (button.dataset.langButton) {
        button.addEventListener('click', () => applyStaticLanguage(button.dataset.langButton));
      }
    });
    return;
  }
  const saved = localStorage.getItem(LANGUAGE_KEY);
  const initial = SUPPORTED_LANGUAGES.has(saved) ? saved : 'ko';
  applyLanguage(initial);
  langButtons.forEach((button) => {
    if (button.dataset.langButton) {
      button.addEventListener('click', () => applyLanguage(button.dataset.langButton));
    }
  });
}

function initContactInterest() {
  const label = document.querySelector('[data-interest-label]');
  const select = document.querySelector('[data-contact-product]');
  if (!label && !select) return;
  const params = new URLSearchParams(window.location.search);
  const legacyInterestMap = {
    nc: 'machining-intelligence',
    ct: 'machining-intelligence',
    'work-standard': 'machining-intelligence',
    tms: 'machining-intelligence',
    amr: 'logistics-intelligence',
  };
  const requestedInterest = params.get('interest') || 'all';
  const interest = legacyInterestMap[requestedInterest] || requestedInterest;
  const labels = {
    ko: {
      all: '전체 / 미정',
      nc: 'Flowmatic NC',
      ct: 'Flowmatic CT',
      quality: 'Flowmatic Quality',
      'work-standard': 'Flowmatic Work Standard',
      tms: 'Flowmatic TMS',
      amr: 'Flowmatic Fleet + Material Flow'
    },
    en: {
      all: 'All / undecided',
      nc: 'Flowmatic NC',
      ct: 'Flowmatic CT',
      quality: 'Flowmatic Quality',
      'work-standard': 'Flowmatic Work Standard',
      tms: 'Flowmatic TMS',
      amr: 'Flowmatic Fleet + Material Flow'
    },
    ar: {
      all: 'الكل / غير محدد',
      nc: 'Flowmatic NC',
      ct: 'Flowmatic CT',
      quality: 'Flowmatic Quality',
      'work-standard': 'Flowmatic Work Standard',
      tms: 'Flowmatic TMS',
      amr: 'Flowmatic Fleet + Material Flow'
    }
  };
  const lang = getCurrentLanguage();
  if (label) label.textContent = labels[lang]?.[interest] || labels[lang]?.all || interest;
  if (select && [...select.options].some((option) => option.value === interest)) select.value = interest;
}

const CONTACT_EMAIL = 'contact@flowmatic-os.com';
async function copyContactEmail(button, status) {
  let copied = false;
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(CONTACT_EMAIL);
      copied = true;
    } else {
      const helper = document.createElement('textarea');
      helper.value = CONTACT_EMAIL;
      helper.setAttribute('readonly', '');
      helper.style.position = 'fixed';
      helper.style.opacity = '0';
      document.body.appendChild(helper);
      helper.select();
      copied = document.execCommand('copy');
      helper.remove();
    }
  } catch (_) {
    copied = false;
  }
  if (status) status.textContent = copied ? button.dataset.copySuccess : button.dataset.copyFailed;
}

function initContactForm() {
  const form = document.querySelector('[data-contact-form]');
  const copyButton = document.querySelector('[data-copy-email]');
  const copyStatus = document.querySelector('[data-copy-status]');
  if (copyButton) copyButton.addEventListener('click', () => copyContactEmail(copyButton, copyStatus));
  if (!form) return;
  const formStatus = form.querySelector('[data-contact-form-status]');
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) {
      if (formStatus) formStatus.textContent = form.dataset.requiredMessage || '';
      return;
    }
    const endpoint = form.getAttribute('action')?.trim();
    if (!endpoint) {
      if (formStatus) formStatus.textContent = form.dataset.unavailableMessage || '';
      return;
    }
    const submitButton = form.querySelector('[type="submit"]');
    if (submitButton) submitButton.disabled = true;
    if (formStatus) formStatus.textContent = form.dataset.sendingMessage || '';
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      });
      if (!response.ok) throw new Error(`Contact request failed: ${response.status}`);
      const brief = form.querySelector('[name="brief"]')?.defaultValue || '';
      form.reset();
      const briefField = form.querySelector('[name="brief"]');
      if (briefField) briefField.value = brief;
      if (formStatus) formStatus.textContent = form.dataset.successMessage || '';
    } catch (_) {
      if (formStatus) formStatus.textContent = form.dataset.failedMessage || '';
    } finally {
      if (submitButton) submitButton.disabled = false;
    }
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

function initV156Convergence() {
  const convergenceBoxes = Array.from(document.querySelectorAll('.v156-platform [data-convergence]'));
  if (!convergenceBoxes.length) return;

  const svgNamespace = 'http://www.w3.org/2000/svg';
  let animationFrame = 0;

  const drawBox = (box) => {
    const field = box.querySelector('[data-convergence-field]');
    const svg = box.querySelector('[data-connection-svg]');
    if (!field || !svg) return;

    svg.replaceChildren();
    const fieldRect = field.getBoundingClientRect();
    const fieldStyle = window.getComputedStyle(field);
    const fieldIsHidden = fieldStyle.display === 'none'
      || fieldStyle.visibility === 'hidden'
      || fieldRect.width < 1
      || fieldRect.height < 1;
    if (window.innerWidth <= 1100 || fieldIsHidden) {
      svg.removeAttribute('viewBox');
      return;
    }

    const width = fieldRect.width;
    const height = fieldRect.height;
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);

    const targets = new Map();
    box.querySelectorAll('[data-solution]').forEach((target) => {
      if (target.dataset.solution) targets.set(target.dataset.solution, target);
    });

    const paths = document.createDocumentFragment();
    box.querySelectorAll('.source-node[data-solutions]').forEach((source) => {
      const solutionIds = (source.dataset.solutions || '').trim().split(/\s+/).filter(Boolean);
      if (!solutionIds.length) return;

      const sourceRect = source.getBoundingClientRect();
      const sourceX = (sourceRect.left + (sourceRect.width / 2)) - fieldRect.left;
      solutionIds.forEach((solutionId) => {
        const target = targets.get(solutionId);
        if (!target) return;

        const targetRect = target.getBoundingClientRect();
        const targetX = (targetRect.left + (targetRect.width / 2)) - fieldRect.left;
        const bend = Math.max(70, height * 0.38);
        const path = document.createElementNS(svgNamespace, 'path');
        path.setAttribute('data-solution', solutionId);
        path.setAttribute('d', `M ${sourceX} 0 C ${sourceX} ${bend}, ${targetX} ${height - bend}, ${targetX} ${height}`);
        paths.appendChild(path);
      });
    });
    svg.appendChild(paths);
  };

  const drawAll = () => {
    animationFrame = 0;
    convergenceBoxes.forEach(drawBox);
  };
  const requestDraw = () => {
    if (animationFrame) return;
    animationFrame = window.requestAnimationFrame(drawAll);
  };

  window.addEventListener('load', requestDraw);
  window.addEventListener('resize', requestDraw);
  window.addEventListener('flowmatic:layout-change', requestDraw);
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver(requestDraw);
    convergenceBoxes.forEach((box) => observer.observe(box));
  }
  requestDraw();
}

function initHomeCompositionMotion() {
  const roots = Array.from(document.querySelectorAll('[data-composition-motion]'));
  if (!roots.length) return;

  const svgNamespace = 'http://www.w3.org/2000/svg';
  const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
  const mix = (from, to, amount) => from + ((to - from) * amount);
  const smoothStep = (value) => {
    const bounded = clamp(value);
    return bounded * bounded * (3 - (2 * bounded));
  };
  const rangeProgress = (value, start, end) => smoothStep((value - start) / (end - start));
  const splitIds = (value) => (value || '').trim().split(/\s+/).filter(Boolean);

  const hashString = (value) => {
    let hash = 2166136261;
    for (let index = 0; index < value.length; index += 1) {
      hash ^= value.charCodeAt(index);
      hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
  };
  const deterministicUnit = (value, salt) => hashString(`${value}:${salt}`) / 4294967295;

  const timelineState = (progress) => {
    if (progress <= .16) return { from: 0, to: 0, amount: 0 };
    if (progress < .32) return { from: 0, to: 1, amount: rangeProgress(progress, .16, .32) };
    if (progress <= .42) return { from: 1, to: 1, amount: 0 };
    if (progress < .60) return { from: 1, to: 2, amount: rangeProgress(progress, .42, .60) };
    if (progress <= .70) return { from: 2, to: 2, amount: 0 };
    if (progress < .88) return { from: 2, to: 3, amount: rangeProgress(progress, .70, .88) };
    return { from: 3, to: 3, amount: 0 };
  };

  const stageForProgress = (progress) => {
    if (progress < .25) return 'field';
    if (progress < .51) return 'context-engine';
    if (progress < .79) return 'modules';
    return 'intelligence';
  };

  const interpolateFrame = (frames, timeline) => {
    const from = frames[timeline.from];
    const to = frames[timeline.to];
    const amount = timeline.amount;
    return {
      x: mix(from.x, to.x, amount),
      y: mix(from.y, to.y, amount),
      rotation: mix(from.rotation || 0, to.rotation || 0, amount),
      scale: mix(from.scale ?? 1, to.scale ?? 1, amount),
      opacity: mix(from.opacity ?? 1, to.opacity ?? 1, amount),
    };
  };

  roots.forEach((root) => {
    const canvas = root.querySelector('[data-motion-canvas]');
    if (!canvas) return;

    const tokens = Array.from(root.querySelectorAll('[data-motion-token]'));
    const modules = Array.from(root.querySelectorAll('[data-motion-module]'));
    const axes = Array.from(root.querySelectorAll('[data-motion-axis][data-axis]'));
    const composeSvg = root.querySelector('[data-compose-svg]');
    const axisSvg = root.querySelector('[data-axis-svg]');
    const contextSpine = root.querySelector('[data-context-spine]');
    const stageLabels = Array.from(root.querySelectorAll('[data-composition-stage]'));
    const progressText = root.querySelector('[data-motion-progress]');
    const progressBar = root.querySelector('[data-motion-progress-bar]');

    if (!tokens.length || !modules.length || !axes.length) return;

    const tokenById = new Map(tokens.map((token) => [token.dataset.tokenId || '', token]));
    const moduleById = new Map(modules.map((module) => [module.dataset.moduleId || '', module]));
    const axisById = new Map(axes.map((axis) => [axis.dataset.axis || '', axis]));
    const tokenSet = new Set(tokens);
    const moduleSet = new Set(modules);
    const axisSet = new Set(axes);
    const moduleIndex = new Map(modules.map((module, index) => [module, index]));
    const axisLinks = new Map(axes.map((axis) => {
      const links = Array.from(axis.querySelectorAll('a[href]'));
      if (axis.matches('a[href]')) links.unshift(axis);
      links.forEach((link) => { link.tabIndex = -1; });
      return [axis, links];
    }));
    const alignmentTargets = new Map(
      Array.from(root.querySelectorAll('[data-motion-align-target]'))
        .map((target) => [target.dataset.motionAlignTarget || '', target])
    );
    const assemblyTargets = new Map(
      Array.from(root.querySelectorAll('[data-motion-assembly-target]'))
        .map((target) => [target.dataset.motionAssemblyTarget || '', target])
    );
    const moduleAxisTargets = new Map(
      Array.from(root.querySelectorAll('[data-motion-axis-target]'))
        .map((target) => [target.dataset.motionAxisTarget || '', target])
    );
    const axisCardTargets = new Map(
      Array.from(root.querySelectorAll('[data-motion-axis-card-target]'))
        .map((target) => [target.dataset.motionAxisCardTarget || '', target])
    );

    const ensureEdgeGroup = (svg, layerName) => {
      if (!svg) return null;
      let group = svg.querySelector(`[data-edge-layer="${layerName}"]`);
      if (!group) {
        group = document.createElementNS(svgNamespace, 'g');
        group.setAttribute('data-edge-layer', layerName);
        svg.appendChild(group);
      }
      group.replaceChildren();
      svg.setAttribute('aria-hidden', 'true');
      svg.setAttribute('focusable', 'false');
      return group;
    };

    const makeEdge = (group, attributes) => {
      if (!group) return null;
      const path = document.createElementNS(svgNamespace, 'path');
      Object.entries(attributes).forEach(([name, value]) => path.setAttribute(name, value));
      path.setAttribute('pathLength', '1');
      path.setAttribute('fill', 'none');
      path.setAttribute('vector-effect', 'non-scaling-stroke');
      path.style.strokeDasharray = '1';
      path.style.strokeDashoffset = '1';
      path.style.opacity = '0';
      group.appendChild(path);
      return path;
    };

    const composeGroup = ensureEdgeGroup(composeSvg, 'engine-module');
    const axisGroup = ensureEdgeGroup(axisSvg, 'module-axis');
    const composeEdges = [];
    const axisEdges = [];

    modules.forEach((module) => {
      const moduleId = module.dataset.moduleId || '';
      splitIds(module.dataset.engines).forEach((engineId) => {
        const engine = tokenById.get(`engine-${engineId}`);
        const path = makeEdge(composeGroup, {
          'data-engine': engineId,
          'data-module': moduleId,
          'data-from': `engine-${engineId}`,
          'data-to': moduleId,
        });
        if (engine && path) {
          path.setAttribute('data-edge-index', String(composeEdges.length));
          composeEdges.push({ from: engine, to: module, path, moduleIndex: moduleIndex.get(module) || 0 });
        }
      });
      splitIds(module.dataset.solutions).forEach((axisId) => {
        const axis = axisById.get(axisId);
        const path = makeEdge(axisGroup, {
          'data-module': moduleId,
          'data-axis': axisId,
          'data-from': moduleId,
          'data-to': axisId,
        });
        if (axis && path) {
          path.setAttribute('data-edge-index', String(axisEdges.length));
          axisEdges.push({ from: module, to: axis, path });
        }
      });
    });

    root.dataset.composeEdgeCount = String(composeEdges.length);
    root.dataset.axisEdgeCount = String(axisEdges.length);

    const motionLabels = {
      ko: { pause: '움직임 멈춤', play: '움직임 재생' },
      en: { pause: 'Pause motion', play: 'Resume motion' },
      ar: { pause: 'إيقاف الحركة', play: 'استئناف الحركة' },
    };
    let pauseButton = root.querySelector('[data-motion-pause]');
    if (!pauseButton) {
      pauseButton = document.createElement('button');
      pauseButton.type = 'button';
      pauseButton.className = 'composition-motion-pause';
      pauseButton.setAttribute('data-motion-pause', '');
      (root.querySelector('[data-motion-controls]') || canvas).appendChild(pauseButton);
    }
    if (!pauseButton.hasAttribute('type')) pauseButton.setAttribute('type', 'button');
    let pauseLabel = pauseButton.querySelector('[data-motion-pause-label]');
    if (!pauseLabel) {
      pauseLabel = document.createElement('span');
      pauseLabel.setAttribute('data-motion-pause-label', '');
      pauseButton.replaceChildren(pauseLabel);
    }

    let driftPaused = false;
    let driftElapsed = 0;
    let lastFrameTime = performance.now();
    let frameRequest = 0;
    let layoutDirty = true;
    let compactLayout = window.innerWidth <= 900;
    let cachedLayout = null;
    let lastStage = '';

    const updatePauseButton = () => {
      const lang = SUPPORTED_LANGUAGES.has(getCurrentLanguage()) ? getCurrentLanguage() : 'ko';
      const labels = motionLabels[lang];
      const pauseText = pauseButton.dataset.pauseLabel || root.dataset.pauseLabel || labels.pause;
      const playText = pauseButton.dataset.resumeLabel
        || root.dataset.resumeLabel
        || pauseButton.dataset.playLabel
        || root.dataset.playLabel
        || labels.play;
      pauseButton.setAttribute('aria-pressed', String(driftPaused));
      pauseLabel.textContent = driftPaused ? playText : pauseText;
      root.dataset.motionPaused = String(driftPaused);
      pauseButton.hidden = prefersReducedMotion || compactLayout;
      pauseButton.disabled = prefersReducedMotion || compactLayout;
    };

    const prepareMovingNode = (node) => {
      node.style.position = 'absolute';
      node.style.left = '0';
      node.style.top = '0';
      node.style.margin = '0';
      node.style.transformOrigin = 'center';
      node.style.willChange = prefersReducedMotion ? 'auto' : 'transform, opacity';
    };
    [...tokens, ...modules, ...axes].forEach(prepareMovingNode);

    const targetCenter = (target, canvasRect) => {
      if (!target) return null;
      const rect = target.getBoundingClientRect();
      if (rect.width < 1 && rect.height < 1) return null;
      return {
        x: (rect.left - canvasRect.left) + (rect.width / 2),
        y: (rect.top - canvasRect.top) + (rect.height / 2),
      };
    };

    const gridCenters = (items, region, columns) => {
      const result = new Map();
      const safeColumns = Math.max(1, Math.min(columns, items.length));
      const rows = Math.max(1, Math.ceil(items.length / safeColumns));
      const cellWidth = region.width / safeColumns;
      const cellHeight = region.height / rows;
      items.forEach((item, index) => {
        const column = index % safeColumns;
        const row = Math.floor(index / safeColumns);
        result.set(item, {
          x: region.x + ((column + .5) * cellWidth),
          y: region.y + ((row + .5) * cellHeight),
        });
      });
      return result;
    };

    const buildLayout = () => {
      compactLayout = window.innerWidth <= 900;
      updatePauseButton();

      const canvasRect = canvas.getBoundingClientRect();
      const width = Math.max(canvas.clientWidth, canvasRect.width, 320);
      const height = Math.max(canvas.clientHeight, canvasRect.height, compactLayout ? 720 : 620);
      const padding = compactLayout ? 14 : 28;
      const usableWidth = Math.max(1, width - (padding * 2));
      const usableHeight = Math.max(1, height - (padding * 2));
      const contextTokens = tokens.filter((token) => (token.dataset.tokenKind || token.dataset.kind) === 'context');
      const engineTokens = tokens.filter((token) => (token.dataset.tokenKind || token.dataset.kind) === 'engine');

      const fallbackContext = gridCenters(contextTokens, {
        x: padding,
        y: padding + (usableHeight * .04),
        width: usableWidth,
        height: usableHeight * .18,
      }, compactLayout ? 5 : 10);
      const fallbackEngine = gridCenters(engineTokens, {
        x: padding,
        y: padding + (usableHeight * .27),
        width: usableWidth,
        height: usableHeight * .23,
      }, compactLayout ? 4 : 12);
      const fallbackAssembly = gridCenters(modules, {
        x: padding,
        y: padding + (usableHeight * .58),
        width: usableWidth,
        height: usableHeight * .30,
      }, compactLayout ? 3 : 6);
      const fallbackAxisModules = gridCenters(modules, {
        x: padding,
        y: padding + (usableHeight * .08),
        width: usableWidth,
        height: usableHeight * .38,
      }, compactLayout ? 3 : 6);
      const fallbackAxes = gridCenters(axes, {
        x: padding,
        y: padding + (usableHeight * .72),
        width: usableWidth,
        height: usableHeight * .22,
      }, compactLayout ? 2 : 4);

      const scatterColumns = compactLayout ? 4 : (width >= 1100 ? 6 : 5);
      const scatterCells = [];
      const scatterRows = Math.ceil(tokens.length / scatterColumns);
      const scatterCellWidth = usableWidth / scatterColumns;
      const scatterCellHeight = (usableHeight * .86) / scatterRows;
      for (let index = 0; index < tokens.length; index += 1) {
        scatterCells.push({
          x: padding + (((index % scatterColumns) + .5) * scatterCellWidth),
          y: padding + ((Math.floor(index / scatterColumns) + .5) * scatterCellHeight),
        });
      }
      const scatterOrder = [...tokens].sort((first, second) => {
        const firstId = first.dataset.tokenId || first.textContent;
        const secondId = second.dataset.tokenId || second.textContent;
        return hashString(firstId) - hashString(secondId);
      });
      const scatter = new Map();
      scatterOrder.forEach((token, index) => {
        const id = token.dataset.tokenId || token.textContent;
        const cell = scatterCells[index];
        scatter.set(token, {
          x: cell.x + ((deterministicUnit(id, 'scatter-x') - .5) * scatterCellWidth * .38),
          y: cell.y + ((deterministicUnit(id, 'scatter-y') - .5) * scatterCellHeight * .38),
          rotation: mix(-8, 8, deterministicUnit(id, 'scatter-rotation')),
        });
      });

      const frames = new Map();
      tokens.forEach((token) => {
        const tokenId = token.dataset.tokenId || '';
        const kind = token.dataset.tokenKind || token.dataset.kind || '';
        const fallback = kind === 'context' ? fallbackContext.get(token) : fallbackEngine.get(token);
        const aligned = targetCenter(alignmentTargets.get(tokenId), canvasRect) || fallback;
        const scattered = scatter.get(token) || aligned;
        frames.set(token, [
          { ...scattered, scale: 1, opacity: 1 },
          { ...aligned, rotation: 0, scale: 1, opacity: 1 },
          { ...aligned, rotation: 0, scale: .92, opacity: .24 },
          { ...aligned, rotation: 0, scale: .84, opacity: 0 },
        ]);
      });

      modules.forEach((module) => {
        const moduleId = module.dataset.moduleId || '';
        const assembled = targetCenter(assemblyTargets.get(moduleId), canvasRect) || fallbackAssembly.get(module);
        const axisPosition = targetCenter(moduleAxisTargets.get(moduleId), canvasRect) || fallbackAxisModules.get(module);
        frames.set(module, [
          { ...assembled, rotation: 0, scale: .72, opacity: 0 },
          { ...assembled, rotation: 0, scale: .72, opacity: 0 },
          { ...assembled, rotation: 0, scale: 1, opacity: 1 },
          { ...axisPosition, rotation: 0, scale: 1, opacity: 1 },
        ]);
      });

      axes.forEach((axis) => {
        const axisId = axis.dataset.axis || '';
        const axisPosition = targetCenter(axisCardTargets.get(axisId), canvasRect) || fallbackAxes.get(axis);
        frames.set(axis, [
          { ...axisPosition, rotation: 0, scale: .84, opacity: 0 },
          { ...axisPosition, rotation: 0, scale: .84, opacity: 0 },
          { ...axisPosition, rotation: 0, scale: .84, opacity: 0 },
          { ...axisPosition, rotation: 0, scale: 1, opacity: 1 },
        ]);
      });

      [...tokens, ...modules, ...axes].forEach((node) => {
        const rect = node.getBoundingClientRect();
        const widthValue = node.offsetWidth || rect.width || 1;
        const heightValue = node.offsetHeight || rect.height || 1;
        node.dataset.motionWidth = String(widthValue);
        node.dataset.motionHeight = String(heightValue);
      });

      [composeSvg, axisSvg].forEach((svg) => {
        if (!svg) return;
        svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
        svg.setAttribute('preserveAspectRatio', 'none');
      });

      cachedLayout = { width, height, frames };
      layoutDirty = false;
    };

    const rootProgress = () => {
      if (prefersReducedMotion || compactLayout) return 1;
      const rect = root.getBoundingClientRect();
      const viewportHeight = Math.max(window.innerHeight, 1);
      const scrollTravel = rect.height - viewportHeight;
      if (scrollTravel > 24) return clamp(-rect.top / scrollTravel);
      return clamp(((viewportHeight * .78) - rect.top) / (viewportHeight + rect.height));
    };

    const pathBetween = (from, to) => {
      const deltaY = to.y - from.y;
      const direction = deltaY >= 0 ? 1 : -1;
      const bend = Math.max(42, Math.abs(deltaY) * .42);
      return `M ${from.x.toFixed(2)} ${from.y.toFixed(2)} C ${from.x.toFixed(2)} ${(from.y + (bend * direction)).toFixed(2)}, ${to.x.toFixed(2)} ${(to.y - (bend * direction)).toFixed(2)}, ${to.x.toFixed(2)} ${to.y.toFixed(2)}`;
    };

    const setPathProgress = (edge, draw, opacity) => {
      edge.path.style.strokeDashoffset = String(1 - clamp(draw));
      edge.path.style.opacity = String(clamp(opacity));
    };

    const updateStage = (stage) => {
      if (stage === lastStage) return;
      lastStage = stage;
      root.dataset.compositionState = stage;
      canvas.dataset.compositionState = stage;
      stageLabels.forEach((label) => {
        const active = label.dataset.compositionStage === stage;
        label.classList.toggle('is-active', active);
        if (active) label.setAttribute('aria-current', 'step');
        else label.removeAttribute('aria-current');
      });
    };

    const render = (now) => {
      frameRequest = 0;
      if (layoutDirty || !cachedLayout) buildLayout();
      if (!cachedLayout) return;

      const progress = rootProgress();
      const timeline = timelineState(progress);
      const stage = stageForProgress(progress);
      const rootRect = root.getBoundingClientRect();
      const viewportHeight = Math.max(window.innerHeight, 1);
      const nearViewport = rootRect.bottom > -(viewportHeight * .25) && rootRect.top < viewportHeight * 1.25;
      const driftActive = !prefersReducedMotion && !compactLayout && !driftPaused && stage === 'field' && nearViewport;

      if (driftActive) driftElapsed += Math.min(50, Math.max(0, now - lastFrameTime));
      lastFrameTime = now;

      updateStage(stage);
      root.dataset.compositionProgress = progress.toFixed(4);
      root.style.setProperty('--composition-progress', progress.toFixed(4));
      const progressPercent = clamp(progress) * 100;
      if (progressText) progressText.textContent = `${Math.round(progressPercent)}%`;
      if (progressBar) {
        progressBar.style.width = `${progressPercent.toFixed(2)}%`;
        progressBar.setAttribute('aria-valuemin', '0');
        progressBar.setAttribute('aria-valuemax', '100');
        progressBar.setAttribute('aria-valuenow', String(Math.round(progressPercent)));
      }

      const currentCenters = new Map();
      const scatterWeight = 1 - rangeProgress(progress, .16, .32);
      [...tokens, ...modules, ...axes].forEach((node) => {
        const frames = cachedLayout.frames.get(node);
        if (!frames) return;
        const frame = interpolateFrame(frames, timeline);
        if (moduleSet.has(node)) {
          const index = moduleIndex.get(node) || 0;
          const stagger = modules.length > 1 ? (index / (modules.length - 1)) * .055 : 0;
          frame.opacity *= rangeProgress(progress, .43 + stagger, .535 + stagger);
        }
        let x = frame.x;
        let y = frame.y;
        let rotation = frame.rotation;
        if (tokenSet.has(node) && scatterWeight > 0 && !compactLayout && !prefersReducedMotion) {
          const id = node.dataset.tokenId || node.textContent;
          const phase = deterministicUnit(id, 'drift-phase') * Math.PI * 2;
          const frequency = mix(.00042, .00072, deterministicUnit(id, 'drift-frequency'));
          const amplitudeX = mix(4, 11, deterministicUnit(id, 'drift-amplitude-x')) * scatterWeight;
          const amplitudeY = mix(3, 8, deterministicUnit(id, 'drift-amplitude-y')) * scatterWeight;
          x += Math.sin((driftElapsed * frequency) + phase) * amplitudeX;
          y += Math.cos((driftElapsed * frequency * .83) + phase) * amplitudeY;
          rotation += Math.sin((driftElapsed * frequency * .55) + phase) * 1.6 * scatterWeight;
        }

        const nodeWidth = Number.parseFloat(node.dataset.motionWidth || '0') || node.offsetWidth || 1;
        const nodeHeight = Number.parseFloat(node.dataset.motionHeight || '0') || node.offsetHeight || 1;
        node.style.transform = `translate3d(${(x - (nodeWidth / 2)).toFixed(2)}px, ${(y - (nodeHeight / 2)).toFixed(2)}px, 0) rotate(${rotation.toFixed(2)}deg) scale(${frame.scale.toFixed(4)})`;
        node.style.opacity = frame.opacity.toFixed(4);
        if (axisSet.has(node)) {
          const interactive = frame.opacity > .7 && stage === 'intelligence';
          node.style.pointerEvents = interactive ? 'auto' : 'none';
          (axisLinks.get(node) || []).forEach((link) => {
            link.style.pointerEvents = interactive ? 'auto' : 'none';
            link.tabIndex = interactive ? 0 : -1;
          });
        } else {
          node.style.pointerEvents = frame.opacity > .7 ? '' : 'none';
        }
        currentCenters.set(node, { x, y });
      });

      const composeDraw = rangeProgress(progress, .38, .61);
      const composeFade = 1 - rangeProgress(progress, .70, .84);
      const composeOpacity = composeDraw * composeFade;
      const activeComposeModule = Math.min(
        modules.length - 1,
        Math.floor(rangeProgress(progress, .38, .60) * modules.length)
      );
      modules.forEach((module, index) => {
        module.classList.toggle(
          'is-active',
          stage === 'modules' && progress < .60 && index === activeComposeModule
        );
      });
      composeEdges.forEach((edge, index) => {
        const from = currentCenters.get(edge.from);
        const to = currentCenters.get(edge.to);
        if (!from || !to) return;
        edge.path.setAttribute('d', pathBetween(from, to));
        const stagger = composeEdges.length > 1 ? (index / (composeEdges.length - 1)) * .075 : 0;
        const edgeDraw = rangeProgress(progress, .365 + stagger, .535 + stagger);
        const emphasis = progress >= .60
          ? .24
          : (edge.moduleIndex === activeComposeModule ? .88 : .16);
        setPathProgress(edge, edgeDraw, edgeDraw * composeFade * emphasis);
      });

      const axisDraw = rangeProgress(progress, .72, .92);
      axisEdges.forEach((edge, index) => {
        const from = currentCenters.get(edge.from);
        const to = currentCenters.get(edge.to);
        if (!from || !to) return;
        edge.path.setAttribute('d', pathBetween(from, to));
        const stagger = axisEdges.length > 1 ? (index / (axisEdges.length - 1)) * .07 : 0;
        const edgeDraw = rangeProgress(progress, .705 + stagger, .855 + stagger);
        setPathProgress(edge, edgeDraw, edgeDraw);
      });

      const contextVisibility = rangeProgress(progress, .18, .32) * (1 - rangeProgress(progress, .70, .84));
      if (contextSpine) contextSpine.style.opacity = contextVisibility.toFixed(4);
      root.style.setProperty('--compose-line-progress', composeDraw.toFixed(4));
      root.style.setProperty('--compose-line-opacity', composeOpacity.toFixed(4));
      root.style.setProperty('--axis-line-progress', axisDraw.toFixed(4));

      if (driftActive) frameRequest = window.requestAnimationFrame(render);
    };

    const requestRender = () => {
      if (frameRequest) return;
      frameRequest = window.requestAnimationFrame(render);
    };
    const requestLayout = () => {
      layoutDirty = true;
      requestRender();
    };

    pauseButton.addEventListener('click', () => {
      if (prefersReducedMotion || compactLayout) return;
      driftPaused = !driftPaused;
      lastFrameTime = performance.now();
      updatePauseButton();
      requestRender();
    });
    window.addEventListener('scroll', requestRender, { passive: true });
    window.addEventListener('resize', requestLayout);
    window.addEventListener('flowmatic:layout-change', requestLayout);
    if ('ResizeObserver' in window) {
      const observer = new ResizeObserver(requestLayout);
      observer.observe(root);
      observer.observe(canvas);
    }
    if (document.fonts?.ready) document.fonts.ready.then(requestLayout);

    updatePauseButton();
    root.dataset.motionReady = 'true';
    if (prefersReducedMotion) root.dataset.motionReduced = 'true';
    requestLayout();
  });
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
    const cssMin = readCssNumber(element, '--fit-min', NaN);
    const dataMin = Number.parseFloat(element.dataset.fitMin || '');
    const minSize = Number.isFinite(cssMin)
      ? cssMin
      : (Number.isFinite(dataMin) ? dataMin : 18);
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
    window.requestAnimationFrame(() => window.requestAnimationFrame(() => {
      fitSemanticText();
      window.dispatchEvent(new Event('flowmatic:layout-change'));
    }));
  }, 32);
}

window.addEventListener('scroll', updateHeaderState, { passive: true });
window.addEventListener('resize', () => {
  if (window.innerWidth > 768) closeNav();
  scheduleSemanticFit();
});

updateHeaderState();
initNavigation();
initArabicLanguageSpans();
initLanguageToggle();
initContactInterest();
initContactForm();
initReveal();
initProductCtas();
initEvidenceSequence();
initDemoVideos();
initCtExplainer();
initAmrExplainer();
initV156Convergence();
initHomeCompositionMotion();
scheduleSemanticFit();
if (document.fonts?.ready) document.fonts.ready.then(scheduleSemanticFit);
