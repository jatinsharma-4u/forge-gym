/* =========================================================
   animations.js — GSAP + ScrollTrigger animation modules.
   Each init* function is independent; main.js wires them up
   inside gsap.matchMedia() so desktop / mobile get different treatment.
   ========================================================= */
window.GYM = window.GYM || {};

(function (G) {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const EASE = 'expo.out';

  /* ---------- helper: wrap every word of an element in a masked span ---------- */
  function splitWords(el, cls = 'w') {
    if (el.dataset.splitDone) return $$('.wi', el);
    const walk = (node) => {
      Array.from(node.childNodes).forEach((n) => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            const w = document.createElement('span'); w.className = cls;
            const i = document.createElement('span'); i.className = 'wi'; i.textContent = part;
            w.appendChild(i); frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
      });
    };
    walk(el);
    el.dataset.splitDone = '1';
    return $$('.wi', el);
  }

  /* ---------- HERO: load sequence + scroll-out ---------- */
  function initHeroAnimation(isDesktop) {
    const frame = $('[data-hero-frame]'), media = $('[data-hero-media]'), content = $('[data-hero-content]');
    if (!frame) return;
    const lines = $$('[data-hero="line"]'), label = $('[data-hero="label"]'), text = $('[data-hero="text"]'),
      cta = $('[data-hero="cta"]'), chips = $$('[data-hero="chip"]');

    const tl = gsap.timeline({ defaults: { ease: EASE }, delay: .15 });
    tl.fromTo(frame, { clipPath: 'inset(8% 8% 8% 8% round 18px)' }, { clipPath: 'inset(0% 0% 0% 0% round 10px)', duration: 1.5, clearProps: 'clipPath' })
      .fromTo(media, { scale: 1.3 }, { scale: 1, duration: 2.2 }, 0)
      .fromTo(lines, { yPercent: 115, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: 1.3, stagger: .12 }, .65)
      .fromTo(text, { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, duration: 1 }, 1.15)
      .fromTo(cta, { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, duration: 1 }, 1.3)
      .fromTo(chips, { autoAlpha: 0, scale: .9, y: -14 }, { autoAlpha: 1, scale: 1, y: 0, duration: 1, stagger: .1 }, 1.4);

    if (isDesktop && !matchMedia('(hover: none)').matches) {
      const mx = gsap.quickTo(media, 'x', { duration: 1.2, ease: 'power3.out' }), my = gsap.quickTo(media, 'y', { duration: 1.2, ease: 'power3.out' });
      frame.addEventListener('pointermove', (e) => {
        const r = frame.getBoundingClientRect();
        mx(-((e.clientX - r.left) / r.width - .5) * 26); my(-((e.clientY - r.top) / r.height - .5) * 18);
      });
    }

    // Scroll-out
    if (isDesktop) {
      // Pinned cinematic exit: photo pushes in, headline lines slide apart, UI fades, frame tucks in
      const hero = $('.hero');
      const brand = $('[data-hero-brand]');
      gsap.set(brand, { autoAlpha: 0 });
      const out = gsap.timeline({ defaults: { ease: 'none' },
        scrollTrigger: { trigger: hero, start: 'top top', end: '+=170%', scrub: .8, pin: true, anticipatePin: 1 } });
      const F = (el, from, to, at) => el && out.fromTo(el, from, { ...to, immediateRender: false }, at);
      out.fromTo(media, { scale: 1, yPercent: 0 }, { scale: 1.25, yPercent: 6, duration: 1.7, immediateRender: false }, 0);
      F(content, { autoAlpha: 1, y: 0 }, { autoAlpha: 0, y: -90, duration: .5 }, 0);
      F($('.hero__shade'), { opacity: 1 }, { opacity: 1.3, duration: .6 }, 0);
      // Big FORGE wordmark: fades in once the copy is gone, then drops down with the scroll
      F(brand, { autoAlpha: 0, scale: .82, yPercent: -22 }, { autoAlpha: 1, scale: 1, yPercent: -22, duration: .5, ease: 'power2.out' }, .4);
      F(brand, { yPercent: -22 }, { yPercent: 62, duration: .9, ease: 'power1.inOut' }, .95);
      F(frame, { scale: 1, borderRadius: 14 }, { scale: .94, borderRadius: 34, duration: .8 }, .9);
    } else {
      const st = { trigger: frame, start: 'top top', end: 'bottom top', scrub: true };
      gsap.to(media, { scale: 1.1, ease: 'none', scrollTrigger: st });
      gsap.to(content, { y: -30, autoAlpha: .2, ease: 'none', scrollTrigger: { ...st, end: 'bottom 40%' } });
    }
  }

  /* ---------- TEXT: split headings, scroll-scrubbed intro, fade-up groups ---------- */
  function initTextReveal(isDesktop) {
    // 1. masked word reveal for every [data-split]
    $$('[data-split]').forEach((el) => {
      const words = splitWords(el);
      ScrollTrigger.create({ trigger: el, start: 'top 88%', once: true, onEnter: () => $$('.hl', el).forEach((h, i) => setTimeout(() => h.classList.add('is-on'), 450 + i * 150)) });
      gsap.from(words, { yPercent: 115, rotate: isDesktop ? 7 : 0, transformOrigin: '0% 100%', duration: 1.2, ease: EASE, stagger: isDesktop ? .05 : .03,
        scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
    });

    // 2. Intro statement — opacity + y + clip scrubbed to scroll position
    $$('[data-scrub-text]').forEach((el) => {
      const words = splitWords(el, 'word');
      words.forEach((w) => { w.parentElement.style.overflow = 'visible'; });
      const spans = $$('.word', el);
      gsap.set(spans, { opacity: .14 });
      gsap.fromTo(spans, { opacity: .14, y: isDesktop ? 22 : 10 },
        { opacity: 1, y: 0, ease: 'none', stagger: .12,
          scrollTrigger: { trigger: el, start: 'top 82%', end: 'bottom 45%', scrub: true } });
      if (isDesktop) gsap.fromTo(el, { clipPath: 'inset(0 0 12% 0)' }, { clipPath: 'inset(0 0 -10% 0)', ease: 'none', scrollTrigger: { trigger: el, start: 'top 90%', end: 'top 50%', scrub: true } });
    });

    // 3. generic fade-up
    $$('[data-reveal]').forEach((el) => {
      gsap.from(el, { autoAlpha: 0, y: isDesktop ? 40 : 24, duration: 1, ease: 'power3.out',
        scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
    });

    // 4. staggered groups (ticks, plans, programs list, perks)
    $$('[data-reveal-group]').forEach((group) => {
      const items = group.children;
      gsap.from(items, { autoAlpha: 0, y: isDesktop ? 80 : 36, rotationX: isDesktop ? -14 : 0, scale: isDesktop ? .95 : 1, transformPerspective: 900, transformOrigin: '50% 100%', duration: 1.1, ease: 'power3.out', stagger: .14, clearProps: 'transform,opacity,visibility',
        scrollTrigger: { trigger: group, start: 'top 85%', once: true } });
    });

    // 5. Why-choose-us items
    $$('[data-why]').forEach((el) => {
      gsap.from(el, { autoAlpha: 0, y: 50, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
      gsap.from($('.why__no', el), { x: -20, autoAlpha: 0, duration: 1, delay: .1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
    });

  }

  /* ---------- IMAGES: clip-path reveal + scale-settle ---------- */
  function initImageReveal(isDesktop) {
    const wipes = ['inset(0% 0% 100% 0%)', 'inset(100% 0% 0% 0%)', 'inset(0% 100% 0% 0%)', 'inset(0% 0% 0% 100%)'];
    $$('[data-img-reveal]').forEach((box, idx) => {
      const img = $('img', box);
      gsap.set(box, { clipPath: wipes[idx % wipes.length] });
      const settle = img && img.classList.contains('parallax-img') ? (isDesktop ? 1.12 : 1.06) : 1;
      gsap.to(box, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.5, ease: 'expo.inOut', scrollTrigger: { trigger: box, start: 'top 90%', once: true }, onComplete: () => box.classList.add('is-in') });
      if (img) gsap.fromTo(img, { scale: settle + .25 }, { scale: settle, duration: 1.9, ease: EASE, scrollTrigger: { trigger: box, start: 'top 90%', once: true } });
    });
  }

  /* ---------- PARALLAX (desktop) ---------- */
  function initParallax() {
    $$('.parallax-img').forEach((img) => {
      gsap.fromTo(img, { yPercent: -5 }, { yPercent: 5, ease: 'none', scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
    // final CTA image zooms slowly as you scroll through
    const m = $('[data-cta-media]');
    if (m) {
      gsap.fromTo(m, { scale: 1.02, yPercent: -5 }, { scale: 1.22, yPercent: 5, ease: 'none', scrollTrigger: { trigger: '[data-cta]', start: 'top bottom', end: 'bottom top', scrub: true } });
    }
  }

  /** light-weight mobile version: only the CTA zoom */
  function initMobileParallax() {
    const m = $('[data-cta-media]');
    if (m) gsap.fromTo(m, { scale: 1 }, { scale: 1.12, ease: 'none', scrollTrigger: { trigger: '[data-cta]', start: 'top bottom', end: 'bottom top', scrub: true } });
  }

  /* ---------- PINNED FACILITIES STORY (desktop) ---------- */
  function initPinnedSections() {
    const pin = $('[data-fac-pin]');
    if (!pin) return;
    const items = $$('[data-fac-item]', pin), imgs = $$('[data-fac-img]', pin), tabs = $$('[data-fac-tab]', pin), bar = $('[data-fac-bar]', pin);
    const n = items.length;

    gsap.set(items.slice(1), { autoAlpha: 0, y: 60 });
    gsap.set(imgs.slice(1), { clipPath: 'inset(100% 0% 0% 0%)' });
    gsap.set(imgs[0], { clipPath: 'inset(0% 0% 0% 0%)' });
    imgs.forEach((w) => gsap.set($('img', w), { scale: 1.15 }));
    gsap.set($('img', imgs[0]), { scale: 1 });
    imgs.forEach((w, i) => (w.style.zIndex = i + 1));
    tabs[0].classList.add('is-active');

    let active = 0;
    const setActive = (i) => {
      if (i === active) return; active = i;
      tabs.forEach((t, k) => t.classList.toggle('is-active', k === i));
    };

    const tl = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: {
        trigger: pin, start: 'top top', end: '+=' + (n - 1) * 100 + '%', pin: true, scrub: .7, anticipatePin: 1, invalidateOnRefresh: true,
        onUpdate: (self) => {
          setActive(Math.max(0, Math.min(n - 1, Math.floor(self.progress * tl.duration() + .4))));
        },
      },
    });
    for (let i = 1; i < n; i++) {
      const s = (i - 1) + .12;
      tl.to(items[i - 1], { autoAlpha: 0, y: -60, duration: .4, ease: 'power2.in' }, s)
        .to($('img', imgs[i - 1]), { scale: 1.12, duration: 1 }, s)
        .to(imgs[i], { clipPath: 'inset(0% 0% 0% 0%)', duration: .95, ease: 'power2.inOut' }, s)
        .to($('img', imgs[i]), { scale: 1, duration: 1 }, s)
        .to(items[i], { autoAlpha: 1, y: 0, duration: .45, ease: 'power2.out' }, s + .5);
    }
    tl.to({}, { duration: .35 });                      // hold on the last panel
    if (bar) tl.to(bar, { scaleX: 1, duration: tl.duration() }, 0);
  }

  /* ---------- HORIZONTAL SCROLL (desktop) ---------- */
  function initHorizontalScroll() {
    const pin = $('[data-hs-pin]'), track = $('[data-hs-track]'), bar = $('[data-hs-bar]');
    if (!pin || !track) return;
    const dist = () => Math.max(0, track.scrollWidth - document.documentElement.clientWidth);
    const tween = gsap.to(track, {
      x: () => -dist(), ease: 'none',
      scrollTrigger: { trigger: pin, start: 'top top', end: () => '+=' + dist(), pin: true, scrub: 1, anticipatePin: 1, invalidateOnRefresh: true,
        onUpdate: (s) => bar && (bar.style.transform = `scaleX(${.2 + s.progress * .8})`) },
    });
    // inner image drifts opposite to the track — subtle depth
    $$('.eq__img img', track).forEach((img) => {
      img.style.transition = 'none';
      gsap.fromTo(img, { xPercent: -7, scale: 1.18 }, { xPercent: 7, ease: 'none', scrollTrigger: { trigger: img.closest('.eq'), containerAnimation: tween, start: 'left right', end: 'right left', scrub: true } });
    });
  }

  /* ---------- COUNTERS ---------- */
  function initCounters() {
    $$('[data-count]').forEach((el) => {
      const end = parseFloat(el.dataset.count), suf = el.dataset.suffix || '';
      const o = { v: 0 };
      el.textContent = '0' + suf;
      gsap.to(o, { v: end, duration: 2.2, ease: 'power3.out',
        onUpdate: () => { el.textContent = Math.round(o.v) + suf; },
        scrollTrigger: { trigger: el, start: 'top 92%', once: true } });
    });
  }

  /* ---------- GALLERY: floating tiles ---------- */
  function initGalleryAnimations() {
    const speeds = { g2: -50, g4: 36, g5: -30, g6: 28, g7: -44, g8: 32, g1: -20, g3: 22 };
    $$('.gal').forEach((el) => {
      const key = Object.keys(speeds).find((k) => el.classList.contains(k));
      gsap.fromTo(el, { y: -speeds[key] / 2 }, { y: speeds[key] / 2, ease: 'none', scrollTrigger: { trigger: '.gal__grid', start: 'top bottom', end: 'bottom top', scrub: 1 } });
    });
  }

  /* ---------- Mobile-safe, lightweight section reveals ---------- */
  function initSectionTransitions() {
    if ($('.strip')) gsap.from('.strip', { yPercent: 100, duration: 1, ease: EASE, delay: 1.2 });
    // plans sequential reveal handled by [data-reveal-group]; testimonials fade
    if ($('.testi__stage')) gsap.from('.testi__stage', { autoAlpha: 0, y: 60, duration: 1.2, ease: 'power3.out', scrollTrigger: { trigger: '.testi__stage', start: 'top 85%', once: true } });
    gsap.from('.footer__big span', { yPercent: 110, duration: 1.3, ease: EASE, stagger: .12, scrollTrigger: { trigger: '.footer__big', start: 'top 92%', once: true } });
  }


  /* ---------- scrub-linked extras (desktop) ---------- */
  function initScrollExtras() {
    // image grows out of a small mask as it scrolls in
    $$('[data-scale-reveal]').forEach((box) => {
      gsap.fromTo(box, { clipPath: 'inset(16% 14% 16% 14% round 28px)' }, { clipPath: 'inset(0% 0% 0% 0% round 8px)', ease: 'none', scrollTrigger: { trigger: box, start: 'top 92%', end: 'top 25%', scrub: .6 } });
      const im = $('img', box);
      if (im) gsap.fromTo(im, { scale: 1.35 }, { scale: 1.12, ease: 'none', scrollTrigger: { trigger: box, start: 'top 92%', end: 'top 25%', scrub: .6 } });
    });
    // floating layers drift at different speeds
    $$('[data-float]').forEach((el) => {
      const d = parseFloat(el.dataset.float);
      gsap.fromTo(el, { y: -d / 2 }, { y: d / 2, ease: 'none', scrollTrigger: { trigger: el.closest('section'), start: 'top bottom', end: 'bottom top', scrub: 1 } });
    });
    // final CTA frame blooms open
    const cta = $('.cta__frame');
    if (cta) gsap.fromTo(cta, { scale: .88, borderRadius: 64 }, { scale: 1, borderRadius: 14, ease: 'none', scrollTrigger: { trigger: cta, start: 'top 98%', end: 'top 25%', scrub: .6 } });
    initMarquee();
  }


  /* ---------- giant text bands slide with scroll ---------- */
  function initTextBands() {
    $$('[data-band]').forEach((t, i) => {
      const dir = i % 2 ? 1 : -1;
      gsap.fromTo(t, { xPercent: dir > 0 ? -34 : 0 }, { xPercent: dir > 0 ? 0 : -34, ease: 'none', scrollTrigger: { trigger: t.parentElement, start: 'top bottom', end: 'bottom top', scrub: .8 } });
    });
  }

  /* ---------- nav items drop in after the page curtain ---------- */
  function initNavIntro() {
    const items = $$('.nav .logo, .nav__menu li, .nav__cta, .burger');
    if (!items.length) return;
    gsap.from(items, { y: -26, autoAlpha: 0, duration: .9, stagger: .05, delay: .3, ease: EASE, clearProps: 'transform,opacity,visibility' });
  }

  /* ---------- inner-page hero: title/lead drift at different speeds ---------- */
  function initPageHero() {
    const hero = $('.phero');
    if (!hero) return;
    const st = { trigger: hero, start: 'top top', end: 'bottom top', scrub: true };
    gsap.to('.phero__title', { yPercent: -22, ease: 'none', scrollTrigger: st });
    gsap.to('.phero__lead', { yPercent: -30, ease: 'none', scrollTrigger: st });   // y only — opacity is owned by the reveal
    gsap.to('.crumbs', { yPercent: -60, ease: 'none', scrollTrigger: st });
    const box = $('.phero__img');
    if (box) gsap.fromTo(box, { scale: .94 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: box, start: 'top 95%', end: 'top 35%', scrub: .6 } });
  }

  /* ---------- program rows slide in from alternating sides ---------- */
  function initProgramShift() {
    $$('.prog__a').forEach((a, i) => {
      gsap.fromTo(a, { x: i % 2 ? -50 : 50 }, { x: 0, ease: 'none', scrollTrigger: { trigger: a, start: 'top 98%', end: 'top 60%', scrub: .5 } });
    });
  }

  /* ---------- paragraphs fill in word-by-word as you scroll ---------- */
  function initParagraphScrub() {
    $$('.about__copy .lead, .story__lead .lead, .faq__lead .lead, .join__lead .lead').forEach((p) => {
      splitWords(p, 'word');
      $$('.word', p).forEach((w) => { w.style.overflow = 'visible'; w.style.paddingBottom = '0'; w.style.marginBottom = '0'; });
      gsap.fromTo($$('.word .wi', p), { opacity: .18 }, { opacity: 1, ease: 'none', stagger: .08,
        scrollTrigger: { trigger: p, start: 'top 85%', end: 'bottom 55%', scrub: true } });
    });
  }

  /* ---------- trainer photos drift at different speeds (parallax, no tilt) ---------- */
  function initGridParallax() {
    $$('.tr__grid .tr__img').forEach((img, i) => {
      gsap.fromTo(img, { y: i % 2 ? 46 : -10 }, { y: i % 2 ? -26 : 26, ease: 'none', scrollTrigger: { trigger: '.tr__grid', start: 'top bottom', end: 'bottom top', scrub: .8 } });
    });
  }

  /* ---------- prices count up when plans appear ---------- */
  function initPriceCount() {
    $$('[data-price]').forEach((el) => {
      const end = parseInt(el.dataset.base, 10);
      ScrollTrigger.create({ trigger: el, start: 'top 90%', once: true, onEnter: () => {
        const o = { v: 0 };
        gsap.to(o, { v: end, duration: 1.6, ease: 'power3.out', onUpdate: () => { el.textContent = Math.round(o.v).toLocaleString('en-IN'); }, onComplete: () => { el.textContent = end.toLocaleString('en-IN'); } });
      } });
    });
  }

  /** crossing strips: two opposite marquees that speed up with scroll velocity */
  function initMarquee() {
    const tweens = $$('.strip__track').map((track) => {
      const dir = parseFloat(track.dataset.dir) || -1;
      return gsap.fromTo(track, { xPercent: dir < 0 ? 0 : -50 }, { xPercent: dir < 0 ? -50 : 0, duration: 38, ease: 'none', repeat: -1 });
    });
    if (!tweens.length) return;
    ScrollTrigger.create({ onUpdate: (self) => {
      const boost = 1 + Math.min(5, Math.abs(self.getVelocity()) / 300);
      tweens.forEach((tw) => { gsap.to(tw, { timeScale: boost, duration: .3, overwrite: true }); gsap.to(tw, { timeScale: 1, duration: 1.2, delay: .3, overwrite: false }); });
    } });
  }

  G.anim = { initParagraphScrub, initGridParallax, initNavIntro, initPageHero, initProgramShift, initPriceCount, initTextBands, initScrollExtras, initMarquee, splitWords, initHeroAnimation, initTextReveal, initImageReveal, initParallax, initMobileParallax, initPinnedSections, initHorizontalScroll, initCounters, initGalleryAnimations, initSectionTransitions };
})(window.GYM);
