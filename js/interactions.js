/* =========================================================
   interactions.js — micro-interactions: magnetic buttons,
   custom cursor, program hover preview, mobile drawer
   ========================================================= */
window.GYM = window.GYM || {};

(function (G) {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const finePointer = () => window.matchMedia('(hover: hover) and (pointer: fine) and (min-width: 1025px)').matches;

  /* ---------- Magnetic buttons ---------- */
  function initButtonInteractions() {
    if (!finePointer() || !window.gsap) return;
    $$('[data-magnetic]').forEach((el) => {
      const xTo = gsap.quickTo(el, 'x', { duration: .5, ease: 'power3.out' });
      const yTo = gsap.quickTo(el, 'y', { duration: .5, ease: 'power3.out' });
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        xTo((e.clientX - (r.left + r.width / 2)) * .28);
        yTo((e.clientY - (r.top + r.height / 2)) * .38);
      });
      el.addEventListener('pointerleave', () => { xTo(0); yTo(0); });
    });
  }

  /* ---------- Custom cursor (desktop only) ---------- */
  function initCursor() {
    const cur = $('#cursor');
    if (!cur || !finePointer() || !window.gsap) return;
    document.documentElement.classList.add('cursor-on');
    const dot = $('span', cur);
    const x = gsap.quickTo(cur, 'x', { duration: .35, ease: 'power3.out' });
    const y = gsap.quickTo(cur, 'y', { duration: .35, ease: 'power3.out' });
    window.addEventListener('pointermove', (e) => { x(e.clientX); y(e.clientY); }, { passive: true });
    document.addEventListener('pointerdown', () => cur.classList.add('is-down'));
    document.addEventListener('pointerup', () => cur.classList.remove('is-down'));
    document.addEventListener('pointerleave', () => gsap.to(cur, { autoAlpha: 0, duration: .2 }));
    document.addEventListener('pointerenter', () => gsap.to(cur, { autoAlpha: 1, duration: .2 }));

    const labels = { view: 'VIEW', drag: 'DRAG', open: 'OPEN' };
    document.addEventListener('pointerover', (e) => {
      const t = e.target.closest('[data-cursor]');
      if (t && labels[t.dataset.cursor]) { dot.textContent = labels[t.dataset.cursor]; dot.style.fontSize = ''; cur.classList.add('is-label'); }
      else { cur.classList.remove('is-label'); dot.textContent = ''; }
      cur.classList.toggle('is-link', !!e.target.closest('a, button, .chip, summary') && !cur.classList.contains('is-label'));
    });
  }

  /* ---------- Programs: hover image follows cursor ---------- */
  function initProgramsHover() {
    const box = $('.prog__preview'), rows = $$('[data-prog]');
    if (!box || !rows.length || !finePointer() || !window.gsap) return;
    const img = $('img', box);
    const x = gsap.quickSetter(box, 'x', 'px'), y = gsap.quickSetter(box, 'y', 'px');
    const rot = gsap.quickTo(box, 'rotation', { duration: .5, ease: 'power3.out' });
    let tx = 0, ty = 0, cx = 0, cy = 0;
    gsap.ticker.add(() => {
      const nx = cx + (tx - cx) * .14, ny = cy + (ty - cy) * .14;
      rot(Math.max(-8, Math.min(8, (nx - cx) * .6)));
      cx = nx; cy = ny; x(cx - box.offsetWidth / 2); y(cy - box.offsetHeight / 2);
    });
    window.addEventListener('pointermove', (e) => { tx = e.clientX; ty = e.clientY; }, { passive: true });
    rows.forEach((r) => {
      r.addEventListener('pointerenter', () => { img.src = r.dataset.img; gsap.to(box, { autoAlpha: 1, scale: 1, duration: .5, ease: 'power3.out' }); });
      r.addEventListener('pointerleave', () => gsap.to(box, { autoAlpha: 0, scale: .7, duration: .4, ease: 'power3.in' }));
    });
  }

  /* ---------- Mobile drawer ---------- */
  function initNavMenu() {
    const burger = $('#burger'), drawer = $('#drawer');
    if (!burger) return;
    const set = (open) => {
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      drawer.classList.toggle('is-open', open);
      $('#nav').classList.toggle('menu-open', open);
      drawer.setAttribute('aria-hidden', String(!open));
      document.documentElement.style.overflow = open ? 'hidden' : '';
      if (G.lenis) open ? G.lenis.stop() : G.lenis.start();
      if (open && window.gsap && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
        gsap.fromTo($$('#drawer li'), { y: 50, autoAlpha: 0 }, { y: 0, autoAlpha: 1, stagger: .06, duration: .8, delay: .2, ease: 'power3.out' });
      }
    };
    G.closeDrawer = () => set(false);
    burger.addEventListener('click', () => set(burger.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') set(false); });
    window.addEventListener('resize', () => { if (innerWidth > 1024) set(false); });
  }

  /* ---------- Page transitions: lime curtain wipes between pages ---------- */
  function initPageTransitions() {
    const c = $('.curtain');
    if (!c) return;
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!window.gsap || reduced) { c.style.display = 'none'; return; }
    const label = $('span', c);
    gsap.set(c, { yPercent: 0 });
    gsap.to(label, { autoAlpha: 0, y: -20, duration: .4, delay: .15, ease: 'power2.in' });
    gsap.to(c, { yPercent: -100, duration: .9, delay: .35, ease: 'expo.inOut', onComplete: () => { c.style.display = 'none'; } });
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[href]');
      if (!a || a.target || a.hasAttribute('download') || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
      const u = new URL(a.href, location.href);
      if (u.origin !== location.origin || u.pathname === location.pathname || !/\.html$|\/$/.test(u.pathname)) return;
      e.preventDefault();
      c.style.display = 'grid'; c.style.pointerEvents = 'all';
      gsap.set(label, { autoAlpha: 1, y: 0 });
      gsap.fromTo(c, { yPercent: 100 }, { yPercent: 0, duration: .7, ease: 'expo.inOut', onComplete: () => { location.href = a.href; } });
    });
    window.addEventListener('pageshow', (e) => {            // back/forward cache
      if (e.persisted) gsap.to(c, { yPercent: -100, duration: .6, onComplete: () => { c.style.display = 'none'; } });
    });
  }

  /* ---------- Cards: cursor spotlight + gentle 3D tilt ---------- */
  function initCardFX() {
    if (!finePointer() || !window.gsap) return;
    $$('.plan, .val, .formcard, .step').forEach((c) => c.classList.add('spot'));
    $$('.spot').forEach((c) => c.addEventListener('pointermove', (e) => {
      const r = c.getBoundingClientRect();
      c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }));
    $$('.plan, .val, .tr').forEach((c) => {
      const rx = gsap.quickTo(c, 'rotationX', { duration: .6, ease: 'power3.out' }), ry = gsap.quickTo(c, 'rotationY', { duration: .6, ease: 'power3.out' }), y = gsap.quickTo(c, 'y', { duration: .5, ease: 'power3.out' });
      gsap.set(c, { transformPerspective: 900 });
      c.addEventListener('pointermove', (e) => {
        const r = c.getBoundingClientRect(), px = (e.clientX - r.left) / r.width - .5, py = (e.clientY - r.top) / r.height - .5;
        ry(px * 7); rx(-py * 7); y(-8);
      });
      c.addEventListener('pointerleave', () => { rx(0); ry(0); y(0); });
    });
  }

  G.interactions = { initButtonInteractions, initCursor, initProgramsHover, initNavMenu, initPageTransitions, initCardFX };
})(window.GYM);
