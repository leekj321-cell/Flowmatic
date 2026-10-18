/* Product evidence follows native document scrolling. No wheel/touch interception. */
(() => {
  'use strict';
  const shots = JSON.parse(document.getElementById('product-evidence').textContent);
  const byId = new Map(shots.map(shot => [shot.id, shot]));
  const tabs = [...document.querySelectorAll('[data-shot]')];
  const steps = [...document.querySelectorAll('[data-step]')];
  const panel = document.getElementById('product-panel');
  const story = document.getElementById('product-story');
  const shotImage = panel.querySelector('.shot-image');
  const galleryOpen = document.getElementById('gallery-open');
  const dialog = document.getElementById('image-dialog');
  const header = document.querySelector('.site-header');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let activeId = '', frame = 0, lastOpener = null;

  function select(id) {
    if (id === activeId || !byId.has(id)) return;
    const shot = byId.get(id);
    activeId = id;
    panel.dataset.activeShot = id;
    tabs.forEach(tab => {
      if (tab.dataset.shot === id) tab.setAttribute('aria-current', 'step');
      else tab.removeAttribute('aria-current');
    });
    steps.forEach(step => step.classList.toggle('is-active', step.dataset.step === id));
    document.getElementById('shot-status').textContent = shot.status;
    document.getElementById('shot-caption').textContent = shot.caption;
    shotImage.src = shot.src;
    shotImage.alt = shot.alt;
    galleryOpen.dataset.openShot = id;
  }

  function activationLine() {
    // On narrow screens the reading area begins below the sticky product view.
    if (innerWidth <= 820 && getComputedStyle(panel).position === 'sticky') {
      const bottom = header.getBoundingClientRect().height + 10 + panel.offsetHeight;
      return Math.min(innerHeight - 60, bottom + Math.max(32, (innerHeight - bottom) * .25));
    }
    return header.offsetHeight + 70;
  }

  function update() {
    frame = 0;
    const line = activationLine();
    let selected = steps[0];
    for (const step of steps) {
      if (step.getBoundingClientRect().top <= line) selected = step;
    }
    select(selected.dataset.step);
  }

  function schedule() {
    if (!frame) frame = requestAnimationFrame(update);
  }

  function jump(id) {
    const step = steps.find(item => item.dataset.step === id);
    if (!step) return;
    // Align the selected text with the reading area, then let native scroll own state.
    const top = Math.max(0, scrollY + step.getBoundingClientRect().top - activationLine() + 24);
    scrollTo({top, behavior: reducedMotion.matches ? 'instant' : 'smooth'});
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', event => {
      if (event.button || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      history.replaceState(null, '', tab.getAttribute('href'));
      jump(tab.dataset.shot);
    });
    tab.addEventListener('keydown', event => {
      const rtl = document.documentElement.dir === 'rtl';
      let next = null;
      if (event.key === 'ArrowRight') next = (index + (rtl ? tabs.length-1 : 1)) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + (rtl ? 1 : tabs.length-1)) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length-1;
      if (next !== null) {
        event.preventDefault();
        tabs[next].focus({preventScroll:true});
        tabs[next].click();
      }
    });
  });

  document.querySelectorAll('[data-open-shot]').forEach(button => button.addEventListener('click', () => {
    const shot = byId.get(button.dataset.openShot);
    lastOpener = button;
    document.getElementById('dialog-title').textContent = shot.label + ' · ' + shot.status;
    document.getElementById('dialog-image').src = shot.src;
    document.getElementById('dialog-image').alt = shot.alt;
    document.getElementById('dialog-note').textContent = shot.caption + '. ' + shot.boundary;
    dialog.showModal();
    document.body.classList.add('modal-open');
  }));
  document.getElementById('dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    lastOpener?.focus({preventScroll:true});
  });

  const menuButton = document.getElementById('menu-toggle');
  const navigation = document.getElementById('navigation');
  function closeMenu() {
    menuButton.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('open');
  }
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('open', open);
  });
  navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      closeMenu(); menuButton.focus();
    }
  });
  document.addEventListener('click', event => {
    if (!header.contains(event.target)) closeMenu();
  });

  const form = document.querySelector('[data-contact-form]');
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const button = form.querySelector('button[type=submit]');
    const status = form.querySelector('.form-status');
    button.disabled = true;
    status.textContent = form.dataset.sending;
    try {
      const response = await fetch(form.action, {method:'POST',body:new FormData(form),headers:{Accept:'application/json'}});
      if (!response.ok) throw new Error('Submission failed');
      status.textContent = form.dataset.success;
      form.reset();
    } catch (_) {
      status.textContent = form.dataset.failed;
    } finally {
      button.disabled = false;
    }
  });

  document.documentElement.classList.add('js');
  // Cache all four real captures, so a later scroll transition has no network delay.
  shots.slice(1).forEach(shot => { const preload = new Image(); preload.src = shot.src; });
  addEventListener('scroll', schedule, {passive:true});
  addEventListener('resize', schedule);
  addEventListener('pageshow', schedule);
  if ('ResizeObserver' in window) new ResizeObserver(schedule).observe(story);
  document.fonts?.ready.then(schedule);
  function followStepHash() {
    const id = location.hash.replace('#step-', '');
    if (location.hash.startsWith('#step-') && byId.has(id)) jump(id);
    else schedule();
  }
  addEventListener('hashchange', followStepHash);
  addEventListener('load', followStepHash);
  update();
})();
