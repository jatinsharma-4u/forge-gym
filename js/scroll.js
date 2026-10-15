/* =========================================================
   scroll.js — Lenis smooth scroll ⇄ GSAP ScrollTrigger sync,
   anchor navigation, navbar state, progress bar
   ========================================================= */
window.GYM = window.GYM || {};

(function (G) {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));

  function initSmoothScroll(enabled) {
    if (enabled && window.Lenis) {
      const lenis = new Lenis({ duration: 1.1, easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true, wheelMultiplier: 1 });
      G.lenis = lenis;
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add((t) => lenis.raf(t * 1000));
      gsap.ticker.lagSmoothing(0);
    }
    // anchors
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[href^="#"]');
      if (!a) return;
      const id = a.getAttribute('href');
      if (id.length < 2) return;
      const target = $(id);
      if (!target) return;
      e.preventDefault();
      G.closeDrawer && G.closeDrawer(true);
      const offset = id === '#home' ? 0 : -72;
      if (G.lenis) G.lenis.scrollTo(target, { offset, duration: 1.6 });
      else window.scrollTo({ top: target.getBoundingClientRect().top + scrollY + offset, behavior: 'smooth' });
      history.replaceState(null, '', id);
    });
    const top = $('#toTop');
    top && top.addEventListener('click', () => (G.lenis ? G.lenis.scrollTo(0, { duration: 1.8 }) : scrollTo({ top: 0, behavior: 'smooth' })));
  }

  /** Sticky navbar state, active link, progress bar */
  function initNavState() {
    const nav = $('#nav'), bar = $('#progress');
    let lastY = window.scrollY || 0, wasInHero = false;
    const onScroll = () => {
      const y = window.scrollY || document.documentElement.scrollTop;
      const hero = $('.hero');
      let inHero = false;
      if (hero) {
        const st = window.ScrollTrigger && ScrollTrigger.getAll().find((t) => t.pin && t.trigger === hero);
        inHero = y < (st ? st.end - 12 : hero.offsetTop + hero.offsetHeight - 90);
      }
      const over = !!hero && y < 40;                            // transparent only at the very top of the home page
      nav.classList.toggle('nav--over', over);
      nav.classList.toggle('is-stuck', !over && y > 40);        // shrinks into a compact bar as soon as you scroll
      const menuOpen = document.documentElement.style.overflow === 'hidden';
      if (inHero || wasInHero) { nav.classList.remove('is-hidden'); lastY = y; }
      else if (!menuOpen) {
        if (y > lastY + 6 && y > 480) nav.classList.add('is-hidden');
        else if (y < lastY - 6 || y < 200) nav.classList.remove('is-hidden');
      }
      lastY = y; wasInHero = inHero;
      const h = document.documentElement.scrollHeight - innerHeight;
      if (bar) bar.style.transform = `scaleX(${h > 0 ? Math.min(1, y / h) : 0})`;
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    const links = $$('.nav__link');
    const map = new Map(links.map((l) => [l.getAttribute('href').slice(1), l]));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        links.forEach((l) => l.classList.remove('is-active'));
        const l = map.get(en.target.id);
        if (l) l.classList.add('is-active');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    ['home', 'about', 'facilities', 'programs', 'trainers', 'membership', 'contact'].forEach((id) => { const s = document.getElementById(id); s && io.observe(s); });
  }

  /** floating "Free trial" pill: shows after the hero, hides near the form / footer */
  function initFab() {
    const fab = $('.fab');
    if (!fab) return;
    let hidden = 0;
    const after = () => {
      const hero = $('.hero');
      const st = hero && window.ScrollTrigger && ScrollTrigger.getAll().find((t) => t.pin && t.trigger === hero);
      return st ? st.end + 40 : 700;                       // only after the hero has finished
    };
    const upd = () => fab.classList.toggle('is-on', (window.scrollY || 0) > after() && !hidden);
    window.addEventListener('scroll', upd, { passive: true });
    const seen = new Set();
    const io = new IntersectionObserver((es) => { es.forEach((e) => { e.isIntersecting ? seen.add(e.target) : seen.delete(e.target); }); hidden = seen.size; upd(); });
    ['#join', '.footer'].forEach((q) => { const el = $(q); el && io.observe(el); });
    upd();
  }

  /** Footer sits fixed behind the page and is uncovered as you reach the end (desktop) */
  function initFooterReveal() {
    const f = $('.footer');
    if (!f || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const apply = () => {
      document.body.classList.remove('footer-reveal');
      const ok = innerWidth > 1024 && f.offsetHeight < innerHeight - 24;
      if (ok) { document.body.style.setProperty('--fh', f.offsetHeight + 'px'); document.body.classList.add('footer-reveal'); }
      else document.body.style.removeProperty('--fh');
      if (window.ScrollTrigger) ScrollTrigger.refresh();
    };
    apply();
    let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(apply, 250); });
    window.addEventListener('load', apply);
  }

  /** every page opens at the very top */
  function resetToTop() {
    if (location.hash) return;
    window.scrollTo(0, 0);
    if (G.lenis) G.lenis.scrollTo(0, { immediate: true });
  }

  G.scroll = { initSmoothScroll, initNavState, initFab, initFooterReveal, resetToTop };
})(window.GYM);
