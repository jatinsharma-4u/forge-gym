/* =========================================================
   components.js — self-contained UI components
   (before/after sliders, pricing toggle, testimonials, join form)
   ========================================================= */
window.GYM = window.GYM || {};

(function (G) {
  'use strict';

  /** Config — set FORM_ENDPOINT to your form backend (Formspree, Web3Forms, own API…).
   *  When empty the form simulates a successful request so the UI can be reviewed. */
  const CONFIG = { FORM_ENDPOINT: '' };

  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Before / After sliders ---------- */
  function initBeforeAfter() {
    $$('[data-ba]').forEach((box) => {
      const range = $('.ba__range', box);
      const set = (v) => box.style.setProperty('--pos', v + '%');
      range.addEventListener('input', () => set(range.value));

      // Pointer drag on the whole frame (mouse + touch) — the range input handles keyboard
      let dragging = false;
      const move = (e) => {
        const r = box.getBoundingClientRect();
        const v = Math.max(0, Math.min(100, ((e.clientX - r.left) / r.width) * 100));
        range.value = v; set(v);
      };
      box.addEventListener('pointerdown', (e) => {
        if (e.pointerType === 'touch') return;     // touch → native range drag (keeps page scroll)
        dragging = true; box.setPointerCapture(e.pointerId); move(e);
      });
      box.addEventListener('pointermove', (e) => { if (dragging) move(e); });
      box.addEventListener('pointerup', () => { dragging = false; });
      box.addEventListener('pointercancel', () => { dragging = false; });
    });
  }

  /* ---------- Pricing toggle ---------- */
  function initPricing() {
    const toggle = $('.toggle');
    if (!toggle) return;
    const btns = $$('button', toggle);
    const thumb = $('.toggle__thumb', toggle);
    const place = (b) => {
      thumb.style.width = b.offsetWidth + 'px';
      thumb.style.transform = `translateX(${b.offsetLeft}px)`;
    };
    const fmt = (n) => n.toLocaleString('en-IN');

    function apply(btn, animate) {
      btns.forEach((b) => b.setAttribute('aria-checked', String(b === btn)));
      place(btn);
      const mult = parseFloat(btn.dataset.mult);
      const months = parseInt(btn.dataset.months, 10);
      $$('[data-price]').forEach((el) => {
        const base = parseInt(el.dataset.base, 10);
        const target = mult === 1 ? base : Math.round((base * mult) / 10) * 10;
        if (animate && window.gsap && !reduced()) {
          const o = { v: parseInt(el.textContent.replace(/\D/g, ''), 10) || target };
          gsap.to(o, { v: target, duration: .6, ease: 'power3.out', onUpdate: () => { el.textContent = fmt(Math.round(o.v)); } });
        } else el.textContent = fmt(target);
        const bill = $('[data-bill]', el.closest('.plan'));
        bill.textContent = months === 1 ? btn.dataset.label : `${btn.dataset.label} · ₹${fmt(target * months)} total`;
      });
    }
    btns.forEach((b) => b.addEventListener('click', () => apply(b, true)));
    toggle.addEventListener('keydown', (e) => {
      if (!['ArrowRight', 'ArrowLeft'].includes(e.key)) return;
      const i = btns.findIndex((b) => b.getAttribute('aria-checked') === 'true');
      const n = btns[(i + (e.key === 'ArrowRight' ? 1 : btns.length - 1)) % btns.length];
      apply(n, true); n.focus();
    });
    const init = () => apply(btns[0], false);
    init();
    window.addEventListener('resize', () => place(btns.find((b) => b.getAttribute('aria-checked') === 'true')));
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(init);
  }

  /* ---------- Testimonials ---------- */
  function initTestimonials() {
    const stage = $('[data-testi]');
    if (!stage) return;
    const slides = $$('[data-quote]', stage);
    const cur = $('[data-cur]');
    let i = 0, timer;
    const show = (n) => {
      if (n === i) return;
      const from = slides[i], to = slides[n];
      i = n;
      cur.textContent = String(n + 1).padStart(2, '0');
      if (window.gsap && !reduced()) {
        from.classList.remove('is-active');
        gsap.to(from, { autoAlpha: 0, y: -30, duration: .5, ease: 'power2.in' });
        to.classList.add('is-active');
        gsap.fromTo(to, { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: .9, delay: .35, ease: 'power3.out' });
        const parts = [$('blockquote', to), $('figcaption', to)];
        gsap.fromTo(parts, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: 1, delay: .35, stagger: .12, ease: 'power3.out', clearProps: 'clipPath' });
      } else {
        from.classList.remove('is-active'); to.classList.add('is-active');
      }
    };
    const next = () => show((i + 1) % slides.length);
    const prev = () => show((i - 1 + slides.length) % slides.length);
    const restart = () => { clearInterval(timer); if (!reduced()) timer = setInterval(next, 8000); };
    $('[data-next]').addEventListener('click', () => { next(); restart(); });
    $('[data-prev]').addEventListener('click', () => { prev(); restart(); });
    stage.addEventListener('mouseenter', () => clearInterval(timer));
    stage.addEventListener('mouseleave', restart);
    // swipe
    let sx = 0;
    stage.addEventListener('touchstart', (e) => { sx = e.touches[0].clientX; }, { passive: true });
    stage.addEventListener('touchend', (e) => {
      const dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) { dx < 0 ? next() : prev(); restart(); }
    });
    restart();
  }

  /* ---------- lime confetti burst ---------- */
  function confetti(host) {
    if (!window.gsap || reduced()) return;
    const colors = ['#C8F031', '#111111', '#A9D112', '#FFFFFF'];
    const box = host.getBoundingClientRect();
    for (let i = 0; i < 36; i++) {
      const p = document.createElement('i');
      const s = 6 + Math.random() * 8;
      p.style.cssText = `position:absolute;left:50%;top:38%;width:${s}px;height:${s * (Math.random() > .5 ? 1 : .45)}px;background:${colors[i % colors.length]};border:1px solid #111;border-radius:${Math.random() > .6 ? '50%' : '2px'};pointer-events:none;z-index:5`;
      host.appendChild(p);
      gsap.fromTo(p, { x: 0, y: 0, rotation: 0, scale: 0 }, { x: (Math.random() - .5) * box.width * .9, y: -80 - Math.random() * 160, rotation: Math.random() * 540 - 270, scale: 1, duration: .7, ease: 'power3.out' });
      gsap.to(p, { y: '+=' + (260 + Math.random() * 160), autoAlpha: 0, duration: 1.2, delay: .7, ease: 'power1.in', onComplete: () => p.remove() });
    }
  }

  /* ---------- Join form ---------- */
  function initJoinForm() {
    const form = $('#joinForm');
    if (!form) return;
    const success = $('#formSuccess'), alertBox = $('#formAlert'), submit = $('.submit', form);
    const phone = $('#f-phone');

    const rules = {
      name: (f) => (f.name.value.trim().length >= 2 ? '' : 'Please enter your full name.'),
      phone: (f) => (/^[6-9]\d{9}$/.test(f.phone.value.replace(/\D/g, '')) ? '' : 'Enter a valid 10-digit mobile number.'),
      email: (f) => (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(f.email.value.trim()) ? '' : 'Enter a valid email address.'),
      goal: (f) => (f.querySelector('[name="goal"]:checked') ? '' : 'Please pick your main goal.'),
      consent: (f) => (f.consent.checked ? '' : 'Please accept to continue.'),
    };
    const holder = (name) => {
      const el = form.elements[name];
      const node = el instanceof RadioNodeList ? el[0] : el;
      return node.closest('.field') || node.closest('.consent');
    };
    const setErr = (name, msg) => {
      const h = holder(name);
      let err = h.classList.contains('consent') ? h.nextElementSibling : $('.err', h);
      if (!err || !err.classList.contains('err')) return;
      err.textContent = msg;
      h.classList.toggle('has-error', !!msg);
      err.parentElement.classList.toggle('has-error', !!msg);
      const input = form.elements[name];
      const first = input instanceof RadioNodeList ? input[0] : input;
      first.setAttribute('aria-invalid', msg ? 'true' : 'false');
    };
    const check = (name) => { const m = rules[name](form); setErr(name, m); return !m; };

    // live format for phone: 98765 43210
    phone.addEventListener('input', () => {
      const d = phone.value.replace(/\D/g, '').slice(0, 10);
      phone.value = d.length > 5 ? d.slice(0, 5) + ' ' + d.slice(5) : d;
    });
    Object.keys(rules).forEach((n) => {
      const els = form.elements[n];
      (els instanceof RadioNodeList ? Array.from(els) : [els]).forEach((el) => {
        el.addEventListener('blur', () => { if (el.value || n === 'goal') check(n); });
        el.addEventListener('input', () => { if (holder(n).classList.contains('has-error') || (el.closest('.has-error'))) check(n); });
        el.addEventListener('change', () => { if (['goal', 'consent'].includes(n)) check(n); });
      });
    });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      alertBox.hidden = true;
      const bad = Object.keys(rules).filter((n) => !check(n));
      if (bad.length) {
        const el = form.elements[bad[0]];
        (el instanceof RadioNodeList ? el[0] : el).focus({ preventScroll: false });
        if (window.gsap && !reduced()) gsap.fromTo(form, { x: -6 }, { x: 0, duration: .5, ease: 'elastic.out(1,.3)' });
        return;
      }
      submit.classList.add('is-loading'); submit.disabled = true;
      const data = Object.fromEntries(new FormData(form).entries());
      try {
        if (CONFIG.FORM_ENDPOINT) {
          const res = await fetch(CONFIG.FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) });
          if (!res.ok) throw new Error('HTTP ' + res.status);
        } else {
          await new Promise((r) => setTimeout(r, 1400));   // demo mode
        }
        form.hidden = true; success.hidden = false;
        $('[data-first]', success).textContent = data.name.trim().split(/\s+/)[0];
        success.focus();
        confetti($('.formcard'));
        if (window.gsap && !reduced()) gsap.from(success.children, { y: 24, autoAlpha: 0, stagger: .1, duration: .7, ease: 'power3.out' });
        if (G.lenis) G.lenis.resize();
      } catch (err) {
        alertBox.hidden = false; alertBox.focus && alertBox.setAttribute('tabindex', '-1'); alertBox.focus();
      } finally {
        submit.classList.remove('is-loading'); submit.disabled = false;
      }
    });

    $('#formReset').addEventListener('click', () => {
      form.reset(); form.hidden = false; success.hidden = true;
      $$('.has-error', form).forEach((n) => n.classList.remove('has-error'));
      $('#f-name').focus();
    });

    // Plan / trial buttons pre-fill the message
    document.addEventListener('click', (e) => {
      const b = e.target.closest('[data-plan],[data-trial]');
      if (!b) return;
      const msg = $('#f-msg');
      if (!msg.value) msg.value = b.dataset.plan ? `I'm interested in the ${b.dataset.plan} plan.` : 'I would like to book a free trial.';
    });
  }

  /* ---------- Gallery page: filters + lightbox ---------- */
  function initGalleryPage() {
    const wrap = $('[data-masonry]');
    if (!wrap) return;
    const items = $$('.mi', wrap);
    const chips = $$('.fchip');
    chips.forEach((c) => c.addEventListener('click', () => {
      const f = c.dataset.filter;
      chips.forEach((x) => { x.classList.toggle('is-on', x === c); x.setAttribute('aria-pressed', String(x === c)); });
      const apply = () => {
        items.forEach((it) => it.classList.toggle('is-hidden', f !== 'all' && it.dataset.cat !== f));
        if (window.gsap) {
          gsap.fromTo(items.filter((it) => !it.classList.contains('is-hidden')), { autoAlpha: 0, y: 30, scale: .96 }, { autoAlpha: 1, y: 0, scale: 1, duration: .6, stagger: .04, ease: 'power3.out', clearProps: 'all' });
          if (window.ScrollTrigger) ScrollTrigger.refresh();
        }
      };
      apply();
    }));

    const lb = $('#lightbox');
    if (!lb || !lb.showModal) return;
    const im = $('img', lb), cap = $('figcaption', lb);
    let list = [], idx = 0;
    const show = (i) => {
      idx = (i + list.length) % list.length;
      const it = list[idx];
      im.src = it.dataset.full; im.alt = it.dataset.cap; cap.textContent = it.dataset.cap + '  ·  ' + (idx + 1) + ' / ' + list.length;
      if (window.gsap) gsap.fromTo(im, { autoAlpha: 0, scale: .96 }, { autoAlpha: 1, scale: 1, duration: .5, ease: 'power3.out' });
    };
    const close = () => { lb.close(); if (G.lenis) G.lenis.start(); document.documentElement.style.overflow = ''; };
    wrap.addEventListener('click', (e) => {
      const b = e.target.closest('.mi__btn');
      if (!b) return;
      list = items.filter((it) => !it.classList.contains('is-hidden'));
      lb.showModal(); if (G.lenis) G.lenis.stop(); document.documentElement.style.overflow = 'hidden';
      show(list.indexOf(b.closest('.mi')));
    });
    $('[data-lb-close]', lb).addEventListener('click', close);
    $('[data-lb-prev]', lb).addEventListener('click', () => show(idx - 1));
    $('[data-lb-next]', lb).addEventListener('click', () => show(idx + 1));
    lb.addEventListener('close', () => { if (G.lenis) G.lenis.start(); document.documentElement.style.overflow = ''; });
    lb.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') show(idx + 1); if (e.key === 'ArrowLeft') show(idx - 1); });
    lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
  }

  /* ---------- "Open now" status ---------- */
  function initOpenStatus() {
    const el = $('[data-open]');
    if (!el) return;
    const d = new Date(), day = d.getDay(), h = d.getHours() + d.getMinutes() / 60;
    const [o, c] = day === 0 ? [6, 22] : [5, 23];
    const open = h >= o && h < c;
    const fmt = (x) => { const hh = Math.floor(x), ap = hh >= 12 ? 'PM' : 'AM'; return ((hh + 11) % 12 + 1) + ':00 ' + ap; };
    el.classList.toggle('is-open', open);
    $('span', el).textContent = open ? 'Open now · closes ' + fmt(c) : 'Closed now · opens ' + fmt(h < o ? o : (day === 6 ? 6 : 5));
  }

  /* ---------- FAQ: smooth accordion ---------- */
  function initFaq() {
    const items = $$('.qa');
    if (!items.length) return;
    items.forEach((d) => {
      const sum = $('summary', d), p = $('p', d);
      sum.addEventListener('click', (e) => {
        if (!window.gsap || reduced()) return;
        e.preventDefault();
        if (!d.open) {
          items.forEach((o) => { if (o !== d && o.open) { const op = $('p', o); gsap.to(op, { height: 0, paddingBottom: 0, opacity: 0, duration: .35, ease: 'power2.inOut', onComplete: () => { o.open = false; } }); } });
          d.open = true;
          gsap.fromTo(p, { height: 0, paddingBottom: 0, opacity: 0 }, { height: 'auto', paddingBottom: 24, opacity: 1, duration: .5, ease: 'power3.out', onComplete: () => { if (window.ScrollTrigger) ScrollTrigger.refresh(); } });
        } else {
          gsap.to(p, { height: 0, paddingBottom: 0, opacity: 0, duration: .35, ease: 'power2.inOut', onComplete: () => { d.open = false; gsap.set(p, { clearProps: 'all' }); if (window.ScrollTrigger) ScrollTrigger.refresh(); } });
        }
      });
    });
  }

  G.components = { initBeforeAfter, initPricing, initTestimonials, initJoinForm, initGalleryPage, initOpenStatus, initFaq };
})(window.GYM);
