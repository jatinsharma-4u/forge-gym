/* =========================================================
   main.js — boot sequence. Decides which animation set runs
   (desktop / mobile / reduced-motion) via gsap.matchMedia().
   ========================================================= */
(function () {
  'use strict';
  const G = window.GYM;
  const $ = (s) => document.querySelector(s);

  function boot() {
    // Always-on, library-independent features
    $('#year') && ($('#year').textContent = new Date().getFullYear());
    G.components.initBeforeAfter();
    G.components.initPricing();
    G.components.initTestimonials();
    G.components.initJoinForm();
    G.components.initGalleryPage();
    G.components.initOpenStatus();
    G.components.initFaq();
    G.interactions.initNavMenu();
    G.scroll.initNavState();
    G.scroll.initFab();

    if (!window.gsap || !window.ScrollTrigger) {            // graceful fallback: static, fully usable page
      document.documentElement.classList.remove('js');
      G.scroll.initSmoothScroll(false);
      return;
    }
    gsap.registerPlugin(ScrollTrigger);
    ScrollTrigger.config({ ignoreMobileResize: true });

    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    G.scroll.initSmoothScroll(!reduce);                      // Lenis only when motion is welcome
    G.scroll.resetToTop();
    G.scroll.initFooterReveal();

    const A = G.anim;
    const mm = gsap.matchMedia();

    // ---- Desktop (full cinematic experience)
    mm.add('(min-width: 1025px) and (prefers-reduced-motion: no-preference)', () => {
      A.initHeroAnimation(true);
      A.initTextReveal(true);
      A.initImageReveal(true);
      A.initParallax();
      A.initPinnedSections();
      A.initHorizontalScroll();
      A.initCounters();
      A.initGalleryAnimations();
      A.initSectionTransitions();
      A.initScrollExtras();
      A.initTextBands();
      A.initPageHero();
      A.initNavIntro();
      A.initProgramShift();
      A.initParagraphScrub();
      A.initGridParallax();
      A.initPriceCount();
      G.interactions.initCardFX();
      G.interactions.initButtonInteractions();
      G.interactions.initCursor();
      G.interactions.initProgramsHover();
    });

    // ---- Tablet / mobile (light: fade, slide, scale, swipe)
    mm.add('(max-width: 1024px) and (prefers-reduced-motion: no-preference)', () => {
      A.initHeroAnimation(false);
      A.initTextReveal(false);
      A.initImageReveal(false);
      A.initMobileParallax();
      A.initNavIntro();
      A.initPageHero();
      A.initTextBands();
      A.initMarquee();
      A.initCounters();
      A.initSectionTransitions();
    });

    // ---- Reduced motion: content simply visible
    mm.add('(prefers-reduced-motion: reduce)', () => {
      document.documentElement.classList.remove('js');
    });

    window.addEventListener('pageshow', (e) => { if (e.persisted) G.scroll.resetToTop(); });
    window.addEventListener('load', () => {
      ScrollTrigger.refresh(); document.documentElement.classList.add('is-ready');
      const h = location.hash && document.querySelector(location.hash);
      if (h) setTimeout(() => (G.lenis ? G.lenis.scrollTo(h, { offset: -72, immediate: true }) : h.scrollIntoView()), 900);
    });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => ScrollTrigger.refresh());
  }

  // Scripts are deferred, so DOM is parsed; just wait until GSAP/Lenis globals exist.
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
