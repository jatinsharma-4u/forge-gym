#!/usr/bin/env python3
"""Generates index.html (static output) so repeated markup + responsive image
srcsets stay consistent. Run:  python tools/build.py
The generated index.html is the deliverable; this script is only a convenience."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ---- Photo library (Unsplash IDs). Swap for the client's own photos later. ----
P = dict(
    dumbbells='1534438327276-14e5300c3a48', lunge='1517836357463-d25dfeac3438',
    bright='1540497077202-7c8a3999166f', tread='1593079831268-3381b0db4a77',
    man='1581009146145-b5ef050c2e1e', pullup='1526506118085-60ce8714f8c5',
    rack='1558611848-73f7eb4001a1', deadlift='1605296867304-46d5465a13f1',
    woman='1574680096145-d05b474e2155', ropes='1599058917212-d750089bc07e',
    row='1546483875-ad9014c88eba', squat='1590487988256-9ed24133863e',
    barbell='1517963879433-6ad2b056d712', bw='1571902943202-507ec2618e8f',
    rows='1576678927484-cc907957088c', situp='1594381898411-846e7d193883',
    ropes2='1534258936925-c58bed479fcb', back='1541534741688-6078c6bfb5c5',
    plate='1521805103424-d8f8430e8933', run='1552674605-db6ffd4facb5',
    bikes='1598289431512-b97b0917affc', curl='1583454110551-21f2fa2afe61',
)


def url(key, w, h=None, extra=''):
    s = f"https://images.unsplash.com/photo-{P[key]}?auto=format&fit=crop&w={w}&q=72"
    if h:
        s += f"&h={h}"
    return s + extra


def srcset(key, ratio, widths, extra=''):
    return ", ".join(f"{url(key, w, round(w / ratio), extra)} {w}w" for w in widths)


def img(key, alt, w, h, sizes="100vw", cls="", eager=False, extra="", widths=(480, 800, 1200, 1800), attrs=""):
    ratio = w / h
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="{url(key, widths[1], round(widths[1] / ratio), extra)}" '
            f'srcset="{srcset(key, ratio, widths, extra)}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{alt}" {load} {attrs}>')


ARROW = '<svg class="arr" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"/></svg>'
ARROW_UR = '<svg class="arr" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square"/></svg>'
LOGO = '<svg class="logo__mark" viewBox="0 0 32 32" width="30" height="30" aria-hidden="true"><rect width="32" height="32" rx="4" fill="#111"/><path d="M5 12v8M9 9v14M23 9v14M27 12v8M9 16h14" stroke="#C8F031" stroke-width="2.6" stroke-linecap="square" fill="none"/></svg>'


PLAN_ICO = {
    'Basic': '<svg viewBox="0 0 24 24" width="22" height="22"><path d="M3 9v6M6 6v12M18 6v12M21 9v6M6 12h12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"/></svg>',
    'Pro': '<svg viewBox="0 0 24 24" width="22" height="22"><path d="M13 2 4 14h7l-1 8 9-12h-7z" fill="currentColor"/></svg>',
    'Elite': '<svg viewBox="0 0 24 24" width="22" height="22"><path d="m3 8 4.5 4L12 5l4.5 7L21 8l-2 11H5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
}


def more_btn(m):
    return f'<div class="more-row" data-reveal>{btn(m[0], m[1], "dark")}</div>' if m else ''


def btn(label, href, kind="primary", extra=""):
    return f'<a class="btn btn--{kind}" href="{href}" data-magnetic data-cursor="open" {extra}><span class="btn__fill"></span><span class="btn__label">{label}</span><span class="btn__icon">{ARROW}</span></a>'


# ------------------------------------------------------------------ data
FACILITIES = [
    ('Strength Area', 'strength', 'squat',
     'Platform-ready racks, calibrated plates and a dumbbell wall that runs up to 60 kg.',
     ['Squat racks', 'Barbells', 'Dumbbells', 'Benches']),
    ('Cardio Zone', 'cardio', 'bikes',
     'A bright, ventilated floor with the latest treadmills, air bikes and rowers.',
     ['Treadmills', 'Cycles', 'Rowing machines']),
    ('Functional Area', 'functional', 'ropes',
     'Open turf for conditioning, sled pushes and circuit work with your coach.',
     ['Battle ropes', 'Kettlebells', 'Sleds', 'TRX']),
    ('Recovery', 'recovery', 'situp',
     'Dedicated mobility and stretch space so you leave better than you arrived.',
     ['Stretching', 'Mobility', 'Recovery equipment']),
]

EQUIPMENT = [
    ('Free Weights', 'Hex dumbbells from 2 to 60 kg and fractional plates for progressive overload.', 'dumbbells'),
    ('Olympic Platform', 'Shock-absorbing lifting platforms with competition bars and bumper plates.', 'deadlift'),
    ('Cable Machines', 'Dual-stack adjustable cables for smooth, constant-tension work.', 'row'),
    ('Strength Machines', 'Plate-loaded and selectorised machines with biomechanically tuned paths.', 'rack'),
    ('Cardio Equipment', 'Treadmills, spin and air bikes with live performance tracking.', 'tread'),
]

PROGRAMS = [
    ('Strength Training', 'Progressive barbell programming built around the big lifts.', 'barbell'),
    ('Muscle Building', 'Hypertrophy splits, tempo work and nutrition guidance.', 'man'),
    ('Fat Loss', 'Metabolic circuits, conditioning and sustainable habits.', 'run'),
    ('Personal Training', 'One-to-one coaching, fully tailored to your goal.', 'woman'),
    ('Functional Training', 'Move better with mobility, carries, sleds and ropes.', 'ropes'),
    ('Athletic Performance', 'Speed, power and agility for competitive athletes.', 'pullup'),
]

TRAINERS = [
    ('Arjun Rathore', 'Head Strength Coach', '12 yrs', 'Powerlifting & hypertrophy', 'man', '0.5', '0.25'),
    ('Meera Kapoor', 'Performance Coach', '9 yrs', 'Fat loss & conditioning', 'situp', '0.5', '0.35'),
    ('Kabir Malhotra', 'Athletic Trainer', '10 yrs', 'Speed, power & agility', 'pullup', '0.5', '0.3'),
    ('Riya Sen', 'Mobility Specialist', '7 yrs', 'Recovery & functional fitness', 'row', '0.5', '0.3'),
]

GALLERY = [
    ('bright', 'Bright main training floor', 'g1'), ('ropes2', 'Athlete working with battle ropes', 'g2'),
    ('squat', 'Squat racks on the strength floor', 'g3'), ('rows', 'Row of dumbbells on the rack', 'g4'),
    ('run', 'Members running at sunrise', 'g5'), ('situp', 'Member doing core work', 'g6'),
    ('plate', 'Close-up of an Olympic plate', 'g7'), ('curl', 'Dumbbell curl detail', 'g8'),
]

PLANS = [
    ('Basic', 'Gym access', 1499, ['Full gym floor access', '5 AM – 11 PM entry', 'Locker & shower', 'Free fitness assessment'], False),
    ('Pro', 'Gym + Group Training', 2499, ['Everything in Basic', 'Unlimited group classes', 'Monthly body analysis', 'Diet starter guide', 'Free guest pass / month'], True),
    ('Elite', 'Gym + Personal Training + Recovery', 4499, ['Everything in Pro', '12 personal sessions / month', 'Custom training & nutrition plan', 'Recovery & mobility access', 'Priority slot booking'], False),
]

WHY = [
    ('Premium Equipment', 'Commercial-grade machines and platforms, serviced weekly.'),
    ('Expert Coaches', 'Certified trainers who coach technique, not just count reps.'),
    ('Clean Environment', 'Hospital-grade cleaning, fresh air and spacious floors.'),
    ('Strong Community', 'People who show up, push each other and celebrate wins.'),
    ('Flexible Hours', 'Open 5 AM to 11 PM, six days — train around your life.'),
]

TESTI = [
    ('I didn’t just change my body.<br>I changed how I train.', 'Rohan Mehta', 'Member · 2 years', 'RM'),
    ('Coaches who notice everything.<br>+60 kg on my deadlift.', 'Ananya Iyer', 'Member · 14 months', 'AI'),
    ('Clean, spacious, motivating.<br>The gym I never skip.', 'Vikram Singh', 'Member · 3 years', 'VS'),
]

STATS = [(10, 'K+', 'Workouts / month'), (25, '+', 'Pro machines'), (15, '+', 'Expert trainers'), (5, 'K+', 'Active members')]

# ------------------------------------------------------------------ markup
PAGES = [('Home', 'index.html'), ('About', 'about.html'), ('Facilities', 'facilities.html'), ('Training', 'programs.html'),
         ('Gallery', 'gallery.html'), ('Trainers', 'trainers.html'), ('Membership', 'membership.html'), ('Contact', 'contact.html')]


def nav(active='index.html'):
    def link(t, h):
        on = h == active
        return f'<li><a class="nav__link{" is-active" if on else ""}" href="{h}"' + (' aria-current="page"' if on else '') + f'>{t}</a></li>'
    li = "".join(link(t, h) for t, h in PAGES)
    dr = "".join(f'<li><a href="{h}"><span>0{i+1}</span>{t}</a></li>' for i, (t, h) in enumerate(PAGES))
    return f"""
<a class="skip" href="#main">Skip to content</a>
<header class="nav{" nav--over" if active == "index.html" else ""}" id="nav">
  <div class="nav__bar">
    <a class="logo" href="index.html" aria-label="Forge Fitness — home">{LOGO}<span class="logo__text">FORGE<small>FITNESS</small></span></a>
    <nav class="nav__menu" aria-label="Primary"><ul>{li}</ul></nav>
    <div class="nav__right">
      <a class="btn btn--primary btn--sm nav__cta" href="#join" data-magnetic><span class="btn__fill"></span><span class="btn__label">Join Now</span><span class="btn__icon">{ARROW}</span></a>
      <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="drawer"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <nav aria-label="Mobile"><ul>{dr}</ul></nav>
  <div class="drawer__foot"><a class="btn btn--primary btn--block" href="#join"><span class="btn__fill"></span><span class="btn__label">Join Now</span><span class="btn__icon">{ARROW}</span></a>
  <p>5:00 AM – 11:00 PM · Mon–Sat<br><a href="tel:+910000000000">+91 XXXXX XXXXX</a></p></div>
</div>"""


def hero():
    m_set = srcset('pullup', 4 / 5.6, (480, 720, 960, 1200), '&crop=focalpoint&fp-x=0.5&fp-y=0.4')
    d_set = srcset('man', 16 / 9, (1200, 1800, 2400), '&crop=focalpoint&fp-x=0.5&fp-y=0.3')
    words = ['Strength', 'Conditioning', 'Mobility', 'Coaching', 'Community', 'Recovery']
    def trk(d):
        return f'<div class="strip__track" data-dir="{d}">' + "".join(f'<span>{w}</span><b>✦</b>' for w in words * 4) + '</div>'
    ticker = f'<div class="strip__row strip__row--b">{trk(1)}</div><div class="strip__row strip__row--a">{trk(-1)}</div>'
    return f"""
<section class="hero" id="home" aria-label="Welcome">
  <div class="hero__frame" data-hero-frame>
    <div class="hero__media" data-hero-media>
      <picture>
        <source media="(max-width: 767px)" srcset="{m_set}" sizes="100vw">
        <img src="{url('man', 1800, 1013, '&crop=focalpoint&fp-x=0.5&fp-y=0.3')}" srcset="{d_set}" sizes="100vw"
             width="1800" height="1013" alt="Athlete training with heavy dumbbells in a premium gym" fetchpriority="high" decoding="async">
      </picture>
    </div>
    <div class="hero__shade"></div>
    <p class="hero__side hero-in" data-hero="chip" aria-hidden="true">EST. 2010 &nbsp;·&nbsp; YOUR CITY &nbsp;·&nbsp; OPEN 5 AM – 11 PM</p>
    <div class="hero__brand" data-hero-brand aria-hidden="true"><span>FORGE</span></div>
    <div class="hero__content" data-hero-content>
      <div class="hero__top">
        <div class="hero__chip hero-in" data-hero="chip"><span class="avs" aria-hidden="true"><i>RM</i><i>AI</i><i>VS</i></span><div><strong data-count="5" data-suffix="K+">5K+</strong><span>happy members<br>★ 4.9 rating</span></div></div>
      </div>
      <div class="hero__mid">
        <aside class="hero__card hero-in" data-hero="chip"><div class="hero__card-img">{img('rack', '', 240, 240, '90px', '', widths=(240, 360), attrs='aria-hidden="true"')}</div><div><b>Free trial week</b><span>Meet a coach &amp; train on us</span></div><a href="#join" aria-label="Book a free trial">{ARROW_UR}</a></aside>
      </div>
      <div class="hero__stack">
        <h1 class="hero__title" aria-label="Built for performance.">
          <span class="hl-line"><span class="hl-in" data-hero="line">BUILT FOR</span></span>
          <span class="hl-line"><span class="hl-in" data-hero="line">PERFORMANCE<b>.</b></span></span>
        </h1>
        <div class="hero__foot">
          <p class="hero__lead hero-in" data-hero="text">Train in a premium environment with professional equipment, expert coaching and a community built to push you further.</p>
          <div class="hero__cta hero-in" data-hero="cta">{btn('Join Now', '#join')}{btn('Explore the Gym', 'facilities.html', 'ghost')}</div>
        </div>
      </div>
    </div>
  </div>
</section>
<div class="strip" aria-hidden="true">{ticker}</div>"""


def intro():
    return '''
<section class="intro" id="intro">
  <div class="wrap">
    <p class="eyebrow"><i></i>Welcome to Forge</p>
    <h2 class="intro__text" data-scrub-text>MORE THAN A GYM.<br><span class="hl">YOUR TRAINING GROUND.</span></h2>
  </div>
</section>'''


def stats():
    items = "".join(f'<div class="stat" data-reveal><div class="stat__n"><span data-count="{n}" data-suffix="{s}">{n}{s}</span></div><p>{l}</p></div>' for n, s, l in STATS)
    return f'<section class="stats" id="stats" aria-label="Key numbers"><div class="wrap stats__grid">{items}</div></section>'


def about():
    return f'''
<section class="about section" id="about">
  <div class="wrap about__grid">
    <div class="about__media">
      <div class="about__img about__img--a" data-scale-reveal data-cursor="view">{img('bright', 'Spacious main floor of Forge Fitness', 1200, 1500, '(max-width:900px) 100vw, 46vw', 'parallax-img', extra='&crop=focalpoint&fp-x=0.5')}</div>
      <div class="about__img about__img--b" data-float="-70" data-cursor="view">{img('man', 'Athlete training with focus', 700, 900, '(max-width:900px) 45vw, 22vw', '', widths=(360, 600, 900))}</div>
      <div class="about__badge" data-float="40"><strong>15</strong><span>Years of<br>Excellence</span></div>
    </div>
    <div class="about__copy">
      <p class="eyebrow" data-reveal><i></i>About the gym</p>
      <h2 class="h2" data-split>BUILT FOR <span class="hl">SERIOUS</span> TRAINING.</h2>
      <p class="lead" data-reveal>Forge started with a simple idea — a gym that feels like a performance lab, not a crowded warehouse. Our philosophy is progress through discipline: smart programming, honest coaching and an environment that makes showing up easy.</p>
      <ul class="ticks" data-reveal-group>
        <li data-reveal-item>{CHECK}<div><b>Our mission</b><span>Help every member get measurably stronger, safely.</span></div></li>
        <li data-reveal-item>{CHECK}<div><b>The environment</b><span>Natural light, clean floors, premium equipment.</span></div></li>
        <li data-reveal-item>{CHECK}<div><b>The community</b><span>Members who train hard and lift each other up.</span></div></li>
      </ul>
      <div data-reveal>{btn('Our Story', 'about.html', 'dark')}</div>
    </div>
  </div>
</section>'''


def facilities(more=None):
    tabs = "".join(f'<li data-fac-tab><span>0{i+1}</span>{t.split()[0].upper()}</li>' for i, (t, *_ ) in enumerate(FACILITIES))
    imgs = "".join(f'<div class="fac__img" data-fac-img>{img(k, t, 1200, 900, "(max-width:1024px) 100vw, 50vw", "fac__photo", widths=(600, 900, 1200))}</div>' for t, _, k, _, _ in FACILITIES)
    items = ""
    for i, (t, _, k, d, li) in enumerate(FACILITIES):
        lis = "".join(f"<li>{x}</li>" for x in li)
        items += f'''<article class="fac__item" data-fac-item>
          <div class="fac__mimg">{img(k, t, 900, 700, "100vw", "", widths=(480, 800))}</div>
          <span class="fac__no">0{i+1} / 04</span><h3 class="h3">{t.upper()}</h3><p>{d}</p><ul class="chips">{lis}</ul></article>'''
    return f'''
<section class="fac" id="facilities">
  <div class="fac__pin" data-fac-pin>
    <div class="wrap fac__inner">
      <div class="fac__text">
        <div class="fac__head"><p class="eyebrow" data-reveal><i></i>Facilities</p>
        <h2 class="h2" data-split>TRAIN AT <span class="hl">YOUR BEST.</span></h2></div>
        <ol class="fac__tabs" aria-hidden="true">{tabs}</ol>
        <div class="fac__items">{items}</div>
      </div>
      <div class="fac__stage" data-cursor="view">{imgs}<div class="fac__bar"><i data-fac-bar></i></div></div>
    </div>
  </div>
  {more_btn(more)}
</section>'''


def equipment():
    cards = ""
    for i, (t, d, k) in enumerate(EQUIPMENT):
        cards += f'''<article class="eq" data-cursor="drag"><div class="eq__img">{img(k, t, 1000, 1250, "(max-width:1024px) 80vw, 34vw", "", widths=(480, 800, 1000))}</div>
        <div class="eq__meta"><span class="eq__no">0{i+1}</span><div><h3>{t.upper()}</h3><p>{d}</p></div></div></article>'''
    return f'''
<section class="hs" id="equipment" data-hs>
  <div class="hs__pin" data-hs-pin>
    <div class="wrap hs__head">
      <div><p class="eyebrow" data-reveal><i></i>Equipment showcase</p>
      <h2 class="h2" data-split>ENGINEERED TO <span class="hl">PERFORM.</span></h2></div>
      <p class="hs__hint"><span>Scroll</span><i><b data-hs-bar></b></i><span>05 pieces</span></p>
    </div>
    <div class="hs__viewport"><div class="hs__track" data-hs-track>{cards}<div class="hs__end"><p>And<br>much<br>more.</p>{btn('Visit the gym', '#contact', 'dark')}</div></div></div>
  </div>
</section>'''


def programs(more=None):
    rows = ""
    for i, (t, d, k) in enumerate(PROGRAMS):
        rows += f'''<li class="prog" data-prog data-img="{url(k, 700, 900)}" data-cursor="open">
          <a href="#join" class="prog__a"><span class="prog__no">0{i+1}</span><span class="prog__t">{t.upper()}</span><span class="prog__d">{d}</span>
          <span class="prog__thumb">{img(k, '', 240, 300, '120px', '', widths=(240, 360), attrs='aria-hidden="true"')}</span><span class="prog__arrow">{ARROW}</span></a></li>'''
    return f'''
<section class="programs section" id="programs">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow" data-reveal><i></i>Training programs</p>
    <h2 class="h2" data-split>TRAIN WITH <span class="hl">PURPOSE.</span></h2></div>
    <ul class="prog__list" data-reveal-group>{rows}</ul>
    {more_btn(more)}
  </div>
  <div class="prog__preview" aria-hidden="true"><img alt="" width="350" height="450"></div>
</section>'''


def trainers(more=None):
    cards = ""
    for i, (n, r, e, s, k, fx, fy) in enumerate(TRAINERS):
        cards += f'''<article class="tr" data-cursor="view">
          <div class="tr__img" data-img-reveal>{img(k, f'{n}, {r}', 800, 1040, "(max-width:640px) 70vw, (max-width:1024px) 45vw, 24vw", "parallax-img", widths=(400, 640, 900), extra=f"&crop=focalpoint&fp-x={fx}&fp-y={fy}")}<span class="tr__exp">{e}</span></div>
          <div class="tr__body" data-reveal><h3>{n}</h3><p class="tr__role">{r}</p><p class="tr__spec">{s}</p></div></article>'''
    return f'''
<section class="trainers section" id="trainers">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow" data-reveal><i></i>Our trainers</p>
    <h2 class="h2" data-split>MEET YOUR <span class="hl">COACHES.</span></h2></div>
    <div class="tr__grid">{cards}</div>
    {more_btn(more)}
  </div>
</section>'''


def gallery(more=None):
    items = "".join(f'<figure class="gal {c}" data-img-reveal data-cursor="view">{img(k, a, 900, 1100 if c in ("g1","g3","g6") else 800, "(max-width:640px) 50vw, 33vw", "parallax-img", widths=(400, 700, 1000))}</figure>' for k, a, c in GALLERY)
    return f'''
<section class="gallery section" id="gallery">
  <div class="wrap">
    <div class="sec-head sec-head--row"><div><p class="eyebrow" data-reveal><i></i>Inside Forge</p>
    <h2 class="h2" data-split>LIFE ON <span class="hl">THE FLOOR.</span></h2></div>
    <p class="muted" data-reveal>Light, space and serious equipment — a look at where the work happens.</p></div>
    <div class="gal__grid">{items}</div>
    {more_btn(more)}
  </div>
</section>'''


def results():
    def slider(name, goal, dur, res, key, fx):
        return f'''<article class="ba" data-reveal>
          <div class="ba__view" data-ba data-cursor="drag" style="--pos:50%">
            {img(key, f'{name} after transformation', 900, 1100, "(max-width:760px) 92vw, 40vw", "ba__after", widths=(480, 800, 1000), extra=fx)}
            <div class="ba__before-wrap">{img(key, f'{name} before transformation', 900, 1100, "(max-width:760px) 92vw, 40vw", "ba__before", widths=(480, 800, 1000), extra=fx)}</div>
            <span class="ba__tag ba__tag--l">Before</span><span class="ba__tag ba__tag--r">After</span>
            <div class="ba__handle"><span>{ARROW}{ARROW}</span></div>
            <input class="ba__range" type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after for {name}">
          </div>
          <div class="ba__meta"><h3>{name}</h3><dl><div><dt>Duration</dt><dd>{dur}</dd></div><div><dt>Goal</dt><dd>{goal}</dd></div><div><dt>Result</dt><dd>{res}</dd></div></dl></div></article>'''
    return f'''
<section class="results section" id="results">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow" data-reveal><i></i>Transformations</p>
    <h2 class="h2" data-split>REAL PEOPLE. <span class="hl">REAL RESULTS.</span></h2></div>
    <div class="ba__grid">
      {slider('Rohan M.', 'Muscle gain', '6 months', '+9 kg lean mass', 'man', '&crop=focalpoint&fp-y=0.35')}
      {slider('Priya S.', 'Fat loss', '5 months', '−14 kg body fat', 'woman', '&crop=focalpoint&fp-y=0.35')}
    </div>
    <p class="note" data-reveal>Sample imagery shown — replace with consented member photos.</p>
  </div>
</section>'''


def membership(more=None, eyebrow='Membership', title='CHOOSE YOUR <span class="hl">PLAN.</span>'):
    cards = ""
    for i, (n, sub, price, feats, hot) in enumerate(PLANS):
        fl = "".join(f"<li>{CHECK}{f}</li>" for f in feats)
        tag = '<span class="plan__tag">Most popular</span>' if hot else ''
        cards += f'''<article class="plan{' plan--hot' if hot else ''}" data-reveal-item>{tag}
          <div class="plan__top"><div><p class="plan__name">{n.upper()}</p><p class="plan__sub">{sub}</p></div><span class="plan__ico" aria-hidden="true">{PLAN_ICO[n]}</span></div>
          <div class="plan__price"><span class="cur">₹</span><span class="amt" data-price data-base="{price}">{price:,}</span><span class="per">/ month</span></div>
          <p class="plan__bill" data-bill>Billed monthly</p>
          <ul class="plan__list">{fl}</ul>
          {btn('Get ' + n, '#join', 'dark' if not hot else 'primary', f'data-plan="{n}"')}</article>'''
    return f'''
<section class="membership section" id="membership">
  <div class="wrap">
    <div class="sec-head sec-head--row"><div><p class="eyebrow" data-reveal><i></i>{eyebrow}</p>
    <h2 class="h2" data-split>{title}</h2></div>
    <div class="toggle" role="radiogroup" aria-label="Billing duration" data-reveal>
      <button role="radio" aria-checked="true" data-mult="1" data-label="Billed monthly" data-months="1">Monthly</button>
      <button role="radio" aria-checked="false" data-mult="0.9" data-label="Billed quarterly · save 10%" data-months="3">3 Months</button>
      <button role="radio" aria-checked="false" data-mult="0.75" data-label="Billed yearly · save 25%" data-months="12">12 Months</button>
      <i class="toggle__thumb"></i></div></div>
    <div class="plans" data-reveal-group>{cards}</div>
    {more_btn(more)}
  </div>
</section>'''


def why():
    items = "".join(f'<li class="why__item" data-why><span class="why__no">0{i+1}</span><h3>{t.upper()}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(WHY))
    return f'''
<section class="why section" id="why">
  <div class="wrap why__grid">
    <div class="why__lead"><p class="eyebrow" data-reveal><i></i>Why choose us</p>
    <h2 class="h2" data-split>WHY MEMBERS <span class="hl">STAY.</span></h2>
    <div class="why__img" data-img-reveal>{img('bw', 'Quiet early-morning training floor', 900, 1100, '(max-width:900px) 90vw, 34vw', 'parallax-img', widths=(480, 800, 1000))}</div></div>
    <ol class="why__list">{items}</ol>
  </div>
</section>'''


REVIEWS = [
    ('Rohan Mehta', 'Member · 2 yrs', 'Best gym I have trained in. Clean, spacious and the coaches actually coach.'),
    ('Ananya Iyer', 'Member · 14 mo', 'My deadlift went up 60 kg in six months. The programming here is next level.'),
    ('Vikram Singh', 'Member · 3 yrs', 'Never crowded, always spotless. The only gym I never feel like skipping.'),
    ('Priya Sharma', 'Member · 8 mo', 'Lost 14 kg with the Elite plan. My trainer kept me honest every single week.'),
    ('Aditya Verma', 'Member · 1 yr', 'The equipment is top class. Never waiting for a rack, even at 6 PM.'),
    ('Neha Kapoor', 'Member · 2 yrs', 'Group classes are brilliant. Great energy, great trainers, zero ego.'),
    ('Karan Malhotra', 'Member · 6 mo', 'Started as a total beginner. Now I train five days a week and love it.'),
    ('Sneha Reddy', 'Member · 11 mo', 'Recovery zone is a game changer. My back pain is finally gone.'),
    ('Rahul Gupta', 'Member · 4 yrs', 'Four years in and still improving. The community keeps you showing up.'),
    ('Divya Nair', 'Member · 9 mo', 'Friendly staff, flexible hours and a proper platform for lifting.'),
    ('Arjun Bhatia', 'Member · 18 mo', 'Free trial convinced me in one session. Joined the same day.'),
    ('Meera Joshi', 'Member · 1 yr', 'Spotless showers, great music, and coaches who remember your goals.'),
]


def testimonials():
    star = '<span class="rv__stars" aria-label="5 out of 5">' + '★' * 5 + '</span>'

    def card(n, r, t):
        ini = "".join(w[0] for w in n.split()[:2])
        return f'<figure class="rv"><blockquote>{star}<p>“{t}”</p></blockquote><figcaption><span class="av">{ini}</span><div><b>{n}</b><span>{r}</span></div></figcaption></figure>'
    row1 = "".join(card(*r) for r in REVIEWS)
    row2 = "".join(card(*r) for r in REVIEWS[6:] + REVIEWS[:6])
    return f"""
<section class="reviews section" id="testimonials" aria-label="Member reviews">
  <div class="wrap sec-head sec-head--row">
    <div><p class="eyebrow" data-reveal><i></i>Member reviews</p><h2 class="h2" data-split>LOVED BY <span class="hl">5,000+</span> MEMBERS.</h2></div>
    <div class="rating" data-reveal><b>4.9</b><div><span class="rv__stars" aria-hidden="true">★★★★★</span><small>from 1,200+ Google reviews</small></div></div>
  </div>
  <div class="rv__row"><div class="rv__track">{row1}{row1}</div></div>
  <div class="rv__row rv__row--rev"><div class="rv__track">{row2}{row2}</div></div>
</section>"""


def cta():
    return f'''
<section class="cta" id="cta">
  <div class="cta__frame" data-cta>
    <div class="cta__media" data-cta-media>{img('deadlift', 'Athlete preparing for a heavy deadlift', 2000, 1100, '100vw', '', widths=(800, 1400, 2200), extra='&crop=focalpoint&fp-y=0.5')}</div>
    <div class="cta__shade"></div>
    <div class="cta__content">
      <p class="eyebrow eyebrow--light"><i></i>Your next level starts here</p>
      <h2 class="cta__title" data-split>READY TO GET <span class="hl">STRONGER?</span></h2>
      <p class="cta__lead" data-reveal>Your next level starts here. Walk in, meet a coach and train free for a day.</p>
      <div class="cta__btns" data-reveal>{btn('Join Now', '#join')}{btn('Book a Free Trial', '#join', 'ghost', 'data-trial')}</div>
    </div>
  </div>
</section>'''


def contact():
    return f'''
<section class="contact section" id="contact">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow" data-reveal><i></i>Contact</p>
    <h2 class="h2" data-split>COME <span class="hl">TRAIN</span> WITH US.</h2></div>
    <div class="contact__grid">
      <div class="contact__info">
        <div class="info" data-reveal><h3>Address</h3><p>Forge Fitness, 21 Performance Avenue,<br>Sector 18, Your City – 110001</p></div>
        <div class="info" data-reveal><h3>Phone</h3><p><a href="tel:+910000000000">+91 XXXXX XXXXX</a></p></div>
        <div class="info" data-reveal><h3>Email</h3><p><a href="mailto:hello@gymname.com">hello@gymname.com</a></p></div>
        <div class="info" data-reveal><h3>Opening hours</h3><table class="hours"><tr><td>Monday – Saturday</td><td>5:00 AM – 11:00 PM</td></tr><tr><td>Sunday</td><td>6:00 AM – 10:00 PM</td></tr></table></div>
        <div class="contact__btns" data-reveal>
          <a class="btn btn--dark btn--sm" href="https://www.google.com/maps/search/?api=1&query=gym" target="_blank" rel="noopener"><span class="btn__fill"></span><span class="btn__label">Get Directions</span><span class="btn__icon">{ARROW_UR}</span></a>
          <a class="btn btn--ghost-dark btn--sm" href="tel:+910000000000"><span class="btn__fill"></span><span class="btn__label">Call Now</span><span class="btn__icon">{ARROW}</span></a>
          <a class="btn btn--ghost-dark btn--sm" href="mailto:hello@gymname.com"><span class="btn__fill"></span><span class="btn__label">Email</span><span class="btn__icon">{ARROW}</span></a>
        </div>
      </div>
      <div class="map" data-img-reveal><iframe title="Forge Fitness location map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Connaught%20Place%20New%20Delhi&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=&amp;output=embed"></iframe></div>
    </div>
  </div>
</section>'''


def form_card():
    goals = ['Build muscle', 'Lose fat', 'Get stronger', 'Improve fitness', 'Sports performance']
    trains = ['Gym floor', 'Group classes', 'Personal training', 'Not sure yet']
    g = ''.join(f'<option>{x}</option>' for x in goals)
    t = ''.join(f'<option>{x}</option>' for x in trains)
    sl = ''.join(f'<option>{x}</option>' for x in ['Morning', 'Afternoon', 'Evening'])
    return f'''
    <div class="formcard" data-reveal>
      <form class="form" id="joinForm" novalidate>
        <div class="form__head"><span class="form__badge"><i></i>Reply within 24 hours</span><h3>Book your free trial</h3><p>Tell us a little about you — a coach will plan your first session.</p></div>
        <div class="form__row">
          <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" type="text" autocomplete="name" placeholder="e.g. Rahul Sharma" required minlength="2"><p class="err" role="alert"></p></div>
          <div class="field"><label for="f-phone">Phone number</label><div class="phone"><span>+91</span><input id="f-phone" name="phone" type="tel" inputmode="numeric" autocomplete="tel-national" placeholder="98765 43210" required maxlength="11"></div><p class="err" role="alert"></p></div>
        </div>
        <div class="field"><label for="f-email">Email address</label><input id="f-email" name="email" type="email" autocomplete="email" placeholder="you@example.com" required><p class="err" role="alert"></p></div>
        <div class="form__row form__row--3">
          <div class="field"><label for="f-goal">Fitness goal</label><div class="sel"><select id="f-goal" name="goal" required><option value="" selected disabled>Select goal</option>{g}</select></div><p class="err" role="alert"></p></div>
          <div class="field"><label for="f-train">Training <em>(optional)</em></label><div class="sel"><select id="f-train" name="training"><option value="" selected>No preference</option>{t}</select></div></div>
          <div class="field"><label for="f-slot">Call me <em>(optional)</em></label><div class="sel"><select id="f-slot" name="slot"><option value="" selected>Any time</option>{sl}</select></div></div>
        </div>
        <div class="field"><label for="f-msg">Message <em>(optional)</em></label><textarea id="f-msg" name="message" rows="3" maxlength="400" placeholder="Anything we should know — injuries, schedule, experience…"></textarea></div>
        <label class="consent"><input type="checkbox" name="consent" required><span class="box">{CHECK}</span><span>I agree to be contacted about my enquiry and accept the <a href="#footer">Privacy Policy</a>.</span></label><p class="err" role="alert"></p>
        <div class="form__alert" id="formAlert" role="alert" hidden><b>Couldn’t send your request.</b> Please check your connection and try again, or call us on +91 XXXXX XXXXX.</div>
        <button class="btn btn--primary btn--lg btn--block submit" type="submit" data-magnetic><span class="btn__fill"></span><span class="btn__label">Start my journey</span><span class="btn__icon">{ARROW}</span><span class="spin" aria-hidden="true"></span></button>
      </form>
      <div class="success" id="formSuccess" hidden tabindex="-1">
        <div class="success__tick"><svg viewBox="0 0 52 52" width="64" height="64"><circle cx="26" cy="26" r="24" fill="none" stroke="#111" stroke-width="2"/><path d="m15 27 8 8 15-17" fill="none" stroke="#111" stroke-width="3" stroke-linecap="square"/></svg></div>
        <h3>You’re in, <span data-first>champ</span>!</h3><p>We’ve received your request. A coach will call you within 24 hours to book your free session.</p>
        <button class="btn btn--ghost-dark btn--sm" type="button" id="formReset"><span class="btn__fill"></span><span class="btn__label">Submit another</span><span class="btn__icon">{ARROW}</span></button>
      </div>
    </div>'''


def join_form():
    goals = ['Build muscle', 'Lose fat', 'Get stronger', 'Improve fitness', 'Sports performance']
    trains = ['Gym floor', 'Group classes', 'Personal training', 'Not sure yet']
    g = "".join(f'<label class="chip"><input type="radio" name="goal" value="{x}" {"required" if i == 0 else ""}><span>{x}</span></label>' for i, x in enumerate(goals))
    t = "".join(f'<label class="chip"><input type="radio" name="training" value="{x}"><span>{x}</span></label>' for x in trains)
    return f'''
<section class="join section" id="join">
  <div class="wrap join__grid">
    <div class="join__lead">
      <p class="eyebrow" data-reveal><i></i>Join the gym</p>
      <h2 class="h2" data-split>START YOUR <span class="hl">JOURNEY.</span></h2>
      <p class="lead" data-reveal>Tell us your goal and a coach will call you within 24 hours to plan your free first session. No pressure, no hard sell.</p>
      <ul class="join__perks" data-reveal-group>
        <li data-reveal-item>{CHECK}Free fitness assessment</li><li data-reveal-item>{CHECK}Complimentary trial day</li>
        <li data-reveal-item>{CHECK}Personalised plan from a certified coach</li><li data-reveal-item>{CHECK}Zero joining fee on annual plans</li>
      </ul>
      <div class="join__img" data-img-reveal>{img('curl', 'Member training with dumbbells', 900, 700, '(max-width:900px) 90vw, 36vw', 'parallax-img', widths=(480, 800, 1000))}</div>
    </div>
    {form_card()}
  </div>
</section>'''


def footer():
    return f"""
<footer class="footer" id="footer">
  <div class="wrap">
    <div class="fcta" data-reveal>
      <div><p class="fcta__k">Your first week is on us</p><h2 class="fcta__t">Ready to start?</h2></div>
      <div class="fcta__r"><a class="btn btn--dark" href="#join" data-magnetic><span class="btn__fill"></span><span class="btn__label">Book free trial</span><span class="btn__icon">{ARROW}</span></a><a class="fcta__tel" href="tel:+910000000000">+91 XXXXX XXXXX</a></div>
    </div>
    <div class="footer__top">
      <div class="footer__brand"><a class="logo" href="index.html" aria-label="Forge Fitness — home">{LOGO}<span class="logo__text">FORGE<small>FITNESS</small></span></a><p>A premium gym built around serious training, expert coaching and a community that shows up.</p>
        <form class="news" onsubmit="event.preventDefault();this.classList.add('is-done');this.querySelector('button').textContent='Subscribed ✓';"><label class="sr" for="nl">Email for updates</label><input id="nl" type="email" placeholder="Your email for offers" required><button type="submit">Join</button></form></div>
      <nav aria-label="Footer"><h4>Explore</h4><ul><li><a href="about.html">About</a></li><li><a href="facilities.html">Facilities</a></li><li><a href="programs.html">Training</a></li><li><a href="trainers.html">Trainers</a></li><li><a href="gallery.html">Gallery</a></li><li><a href="membership.html">Membership</a></li></ul></nav>
      <div><h4>Visit</h4><ul><li>21 Performance Avenue,<br>Sector 18, Your City</li><li><a href="tel:+910000000000">+91 XXXXX XXXXX</a></li><li><a href="mailto:hello@gymname.com">hello@gymname.com</a></li></ul></div>
      <div><h4>Hours</h4><ul><li><b>Mon – Sat</b><br>5:00 AM – 11:00 PM</li><li><b>Sunday</b><br>6:00 AM – 10:00 PM</li></ul></div>
      <div><h4>Follow</h4><ul class="social"><li><a href="#" aria-label="Instagram">Instagram</a></li><li><a href="#" aria-label="YouTube">YouTube</a></li><li><a href="#" aria-label="Facebook">Facebook</a></li><li><a href="#" aria-label="X / Twitter">X / Twitter</a></li></ul></div>
    </div>
    <p class="footer__big" aria-label="Train. Perform. Evolve."><span>TRAIN.</span><span>PERFORM.</span><span class="hl">EVOLVE.</span></p>
    <div class="footer__bottom"><p>© <span id="year">2026</span> Forge Fitness. All rights reserved.</p><p><a href="#footer">Privacy Policy</a> <a href="#footer">Terms</a></p><button class="totop" id="toTop" aria-label="Back to top">Top {ARROW.replace('class="arr"', 'class="arr up"')}</button></div>
  </div>
</footer>
<div class="cursor" id="cursor" aria-hidden="true"><span></span></div>
<div class="progress" aria-hidden="true"><i id="progress"></i></div>
<a class="fab" href="#join" aria-label="Book a free trial"><span>Free trial</span><i>✦</i></a>"""


SCHEMA = json.dumps({
    "@context": "https://schema.org", "@type": "HealthClub", "name": "Forge Fitness",
    "description": "Premium gym with expert coaching, professional equipment and a strong fitness community.",
    "url": "https://www.example.com/", "telephone": "+91-XXXXXXXXXX", "email": "hello@gymname.com",
    "priceRange": "₹₹",
    "address": {"@type": "PostalAddress", "streetAddress": "21 Performance Avenue, Sector 18", "addressLocality": "Your City", "postalCode": "110001", "addressCountry": "IN"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "05:00", "closes": "23:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "06:00", "closes": "22:00"}],
    "image": url('bright', 1200)}, ensure_ascii=False)



# =================================================================== multi-page additions
def page_hero(crumb, title, lead, key=None, alt='', fy='0.5'):
    media = ''
    if key:
        media = (f'<div class="wrap"><div class="phero__img" data-img-reveal>'
                 f'{img(key, alt, 1800, 760, "100vw", "parallax-img", widths=(800, 1400, 2000), extra=f"&crop=focalpoint&fp-y={fy}", eager=True)}</div></div>')
    return f"""
<section class="phero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><b>{crumb}</b></nav>
    <div class="phero__row">
      <h1 class="phero__title" data-split>{title}</h1>
      <p class="phero__lead" data-reveal>{lead}</p>
    </div>
  </div>
  {media}
</section>"""


def story():
    items = [('2010', 'The first rack', 'Forge opens in a 2,000 sq ft garage with six racks and a handful of obsessive lifters.'),
             ('2014', 'A real home', 'We move into our current 18,000 sq ft facility with a full strength floor and cardio zone.'),
             ('2018', 'First champions', 'Our members start placing at state and national powerlifting and fitness meets.'),
             ('2021', 'Coaching academy', 'Launch of our in-house coach education programme and group training studio.'),
             ('2025', '5,000 members', 'A community of five thousand people training, recovering and evolving together.')]
    rows = "".join(f'<li class="tl__item" data-reveal-item><span class="tl__year">{y}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for y, t, d in items)
    return f"""
<section class="story section" id="story">
  <div class="wrap story__grid">
    <div class="story__lead"><p class="eyebrow" data-reveal><i></i>Our story</p>
    <h2 class="h2" data-split>FROM A GARAGE TO <span class="hl">A GYM.</span></h2>
    <p class="lead" data-reveal>Every plate, rack and coach here exists for one reason: to help you get measurably better. Fifteen years on, that is still the only metric we care about.</p></div>
    <ol class="tl" data-reveal-group>{rows}</ol>
  </div>
</section>"""


def values():
    vs = [('Discipline', 'Showing up is the work. We build routines that survive busy weeks and low-motivation days.'),
          ('Honesty', 'Straight feedback, realistic timelines and no gimmicks. Progress you can measure.'),
          ('Community', 'Members who push, spot and celebrate each other. Nobody trains alone here.')]
    c = "".join(f'<article class="val" data-reveal-item><span class="val__no">0{i+1}</span><h3>{t.upper()}</h3><p>{d}</p></article>' for i, (t, d) in enumerate(vs))
    return f"""
<section class="values section">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow" data-reveal><i></i>What we stand for</p><h2 class="h2" data-split>THREE RULES. <span class="hl">NO EXCEPTIONS.</span></h2></div>
    <div class="values__grid" data-reveal-group>{c}</div>
  </div>
</section>"""


def process(title="HOW IT <span class=\"hl\">WORKS.</span>"):
    steps = [('Assess', 'A free movement, strength and body-composition assessment with a coach.'),
             ('Plan', 'A written programme and nutrition outline built around your goal and schedule.'),
             ('Train', 'Coached sessions, progressive overload and weekly check-ins to keep you honest.'),
             ('Evolve', 'Re-test every 8 weeks, adjust the plan and set the next target.')]
    c = "".join(f'<li class="step" data-reveal-item><span class="step__no">0{i+1}</span><h3>{t.upper()}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(steps))
    return f"""
<section class="process section">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow" data-reveal><i></i>Our method</p><h2 class="h2" data-split>{title}</h2></div>
    <ol class="steps" data-reveal-group>{c}</ol>
  </div>
</section>"""


def timetable():
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    slots = [('6:00 AM', ['Strength', 'HIIT', 'Mobility', 'Strength', 'Boxing Fit', 'Power']),
             ('8:00 AM', ['Yoga Flow', 'Strength', 'HIIT', 'Yoga Flow', 'Strength', 'Functional']),
             ('12:30 PM', ['Express 30', 'Express 30', 'Express 30', 'Express 30', 'Express 30', '—']),
             ('5:30 PM', ['Functional', 'Power', 'Strength', 'HIIT', 'Functional', 'Open Floor']),
             ('7:30 PM', ['HIIT', 'Boxing Fit', 'Functional', 'Power', 'Mobility', '—'])]
    head = "".join(f'<th scope="col">{d}</th>' for d in days)
    rows = "".join(f'<tr><th scope="row">{t}</th>' + "".join(f'<td><span class="cls cls--{c.split()[0].lower().replace("—", "none")}">{c}</span></td>' for c in cl) + '</tr>' for t, cl in slots)
    return f"""
<section class="timetable section" id="timetable">
  <div class="wrap">
    <div class="sec-head sec-head--row"><div><p class="eyebrow" data-reveal><i></i>Weekly timetable</p><h2 class="h2" data-split>FIND YOUR <span class="hl">SLOT.</span></h2></div>
    <p class="muted" data-reveal>Group classes are included in Pro and Elite. Floor access is open throughout.</p></div>
    <div class="tt" data-reveal><table><thead><tr><th scope="col"><span class="sr">Time</span></th>{head}</tr></thead><tbody>{rows}</tbody></table></div>
  </div>
</section>"""


GALLERY_ALL = [
    ('bright', 'Bright main training floor', 'facility', 5, 6), ('deadlift', 'Heavy deadlift setup', 'training', 4, 5),
    ('ropes2', 'Battle rope conditioning', 'training', 4, 3), ('squat', 'Squat racks on the strength floor', 'facility', 4, 5),
    ('run', 'Members running at sunrise', 'community', 4, 3), ('rows', 'Dumbbell rack', 'facility', 4, 4),
    ('situp', 'Core session', 'community', 4, 5), ('barbell', 'Barbell on the platform', 'training', 4, 3),
    ('bikes', 'Studio cycling zone', 'facility', 4, 3), ('man', 'Heavy dumbbell work', 'training', 4, 5),
    ('plate', 'Olympic plate detail', 'facility', 4, 4), ('pullup', 'Pull-up training', 'training', 4, 5),
    ('row', 'Seated cable row', 'community', 4, 5), ('tread', 'Cardio zone', 'facility', 4, 3),
    ('curl', 'Dumbbell curl', 'training', 4, 5), ('back', 'Member after a pull session', 'community', 4, 5),
]


def gallery_full():
    filters = "".join(f'<button class="fchip{" is-on" if i == 0 else ""}" data-filter="{k}" aria-pressed="{"true" if i == 0 else "false"}">{t}</button>'
                      for i, (k, t) in enumerate([('all', 'All'), ('facility', 'Facility'), ('training', 'Training'), ('community', 'Community')]))
    items = ""
    for k, a, cat, w, h in GALLERY_ALL:
        items += (f'<figure class="mi" data-cat="{cat}" data-full="{url(k, 1800)}" data-cap="{a}"><button class="mi__btn" aria-label="Open photo: {a}" data-cursor="view">'
                  f'{img(k, a, w * 200, h * 200, "(max-width:640px) 50vw, (max-width:1024px) 33vw, 25vw", "", widths=(400, 700, 1000))}</button><figcaption>{a}</figcaption></figure>')
    return f"""
<section class="galfull section" id="gallery">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter photos" data-reveal>{filters}</div>
    <div class="masonry" data-masonry>{items}</div>
  </div>
</section>
<dialog class="lb" id="lightbox" aria-label="Photo viewer">
  <button class="lb__x" data-lb-close aria-label="Close viewer">×</button>
  <button class="lb__nav lb__nav--prev" data-lb-prev aria-label="Previous photo">{ARROW.replace('class="arr"', 'class="arr flip"')}</button>
  <figure class="lb__fig"><img alt="" src=""><figcaption></figcaption></figure>
  <button class="lb__nav lb__nav--next" data-lb-next aria-label="Next photo">{ARROW}</button>
</dialog>"""


def compare():
    rows = [('Gym floor access', 1, 1, 1), ('Locker & shower', 1, 1, 1), ('Free fitness assessment', 1, 1, 1),
            ('Unlimited group classes', 0, 1, 1), ('Monthly body analysis', 0, 1, 1), ('Guest pass / month', 0, 1, 1),
            ('Personal training sessions', 0, 0, 12), ('Custom nutrition plan', 0, 0, 1), ('Recovery & mobility zone', 0, 0, 1), ('Priority slot booking', 0, 0, 1)]
    def cell(v):
        if v is True or v == 1: return f'<td class="y">{CHECK}</td>'
        if v == 0: return '<td class="n">—</td>'
        return f'<td class="y"><b>{v}</b>/mo</td>'
    body = "".join(f'<tr><th scope="row">{r[0]}</th>{cell(r[1])}{cell(r[2])}{cell(r[3])}</tr>' for r in rows)
    return f"""
<section class="compare section">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow" data-reveal><i></i>Compare plans</p><h2 class="h2" data-split>WHAT’S <span class="hl">INCLUDED.</span></h2></div>
    <div class="cmp" data-reveal><table><thead><tr><th scope="col"><span class="sr">Feature</span></th><th scope="col">BASIC</th><th scope="col" class="hot">PRO</th><th scope="col">ELITE</th></tr></thead><tbody>{body}</tbody></table></div>
  </div>
</section>"""


def faq():
    qa = [('Is there a joining fee?', 'No joining fee on 12-month plans. Monthly and quarterly plans carry a one-time ₹999 enrolment fee.'),
          ('Can I try the gym before joining?', 'Yes — book a free trial day or a trial week. You will meet a coach and get a free fitness assessment.'),
          ('I have never trained before. Is that okay?', 'Absolutely. Most of our members started as beginners. Your coach builds a programme at your level.'),
          ('Can I freeze or transfer my membership?', 'Quarterly and annual plans can be frozen for up to 30 days a year and transferred once with a small admin fee.'),
          ('What are your opening hours?', 'Monday to Saturday 5:00 AM – 11:00 PM, Sunday 6:00 AM – 10:00 PM. Group classes follow the weekly timetable.'),
          ('Do you offer lockers, showers and parking?', 'Yes. Secure lockers, hot showers, towels on request and free two-wheeler and car parking.')]
    items = "".join(f'<details class="qa"><summary><span>{q}</span><i aria-hidden="true"></i></summary><p>{a}</p></details>' for q, a in qa)
    return f"""
<section class="faq section" id="faq">
  <div class="wrap faq__grid">
    <div class="faq__lead"><p class="eyebrow" data-reveal><i></i>FAQ</p><h2 class="h2" data-split>QUESTIONS, <span class="hl">ANSWERED.</span></h2>
    <p class="lead" data-reveal>Still unsure? Call us on <a href="tel:+910000000000"><b>+91 XXXXX XXXXX</b></a> or drop by — we are happy to show you around.</p></div>
    <div class="faq__list" data-reveal-group>{items}</div>
  </div>
</section>"""




def textband(words=('STRENGTH', 'SPEED', 'ENDURANCE', 'DISCIPLINE')):
    row = "".join(f'<span>{w}</span><i aria-hidden="true">✺</i>' for w in words) * 2
    return f'<div class="band" aria-hidden="true"><div class="band__track" data-band>{row}</div></div>'


IC = {
    'phone': '<svg viewBox="0 0 24 24" width="20" height="20"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
    'wa': '<svg viewBox="0 0 24 24" width="20" height="20"><path d="M4 20l1.3-4.2A8 8 0 1 1 8.3 18.8z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 9c.5 3 2.5 5 6 6l1.2-1.4-2-1-1 .7c-1-.5-1.8-1.3-2.300-2.300l.7-1-1-2z" fill="currentColor"/></svg>',
    'mail': '<svg viewBox="0 0 24 24" width="20" height="20"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m3.500 7 8.500 6 8.500-6" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>',
    'pin': '<svg viewBox="0 0 24 24" width="20" height="20"><path d="M12 21s7-6.200 7-11.500A7 7 0 0 0 5 9.500C5 14.800 12 21 12 21z" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="9.500" r="2.500" fill="currentColor"/></svg>',
}


def ctile(ico, label, value, href, ext=False):
    t = ' target="_blank" rel="noopener"' if ext else ''
    return (f'<a class="ctile" href="{href}"{t} data-reveal-item><span class="ctile__ico">{IC[ico]}</span>'
            f'<span class="ctile__t"><small>{label}</small><b>{value}</b></span><span class="ctile__go">{ARROW_UR}</span></a>')


def contact_top():
    tiles = (ctile('phone', 'Call us', '+91 XXXXX XXXXX', 'tel:+910000000000')
             + ctile('wa', 'WhatsApp', 'Chat with a coach', 'https://wa.me/910000000000', True)
             + ctile('mail', 'Email', 'hello@gymname.com', 'mailto:hello@gymname.com')
             + ctile('pin', 'Visit', '21 Performance Avenue, Sector 18', 'https://www.google.com/maps/search/?api=1&query=gym', True))
    return f"""
<section class="cform" id="join">
  <div class="wrap cform__grid">
    <aside class="cinfo">
      <div class="cstatus" data-open><i></i><span>Checking hours…</span></div>
      <div class="ctiles" data-reveal-group>{tiles}</div>
      <div class="chours" data-reveal>
        <h3>Opening hours</h3>
        <table><tr><td>Monday – Saturday</td><td>5:00 AM – 11:00 PM</td></tr><tr><td>Sunday</td><td>6:00 AM – 10:00 PM</td></tr></table>
        <p>Group classes follow the weekly timetable. Free trial slots are available every day.</p>
      </div>
    </aside>
    {form_card()}
  </div>
</section>"""


def map_section():
    return f"""
<section class="mapsec section" id="map">
  <div class="wrap">
    <div class="mapsec__box" data-img-reveal>
      <iframe title="Forge Fitness location map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Connaught%20Place%20New%20Delhi&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=&amp;output=embed"></iframe>
      <div class="mapsec__card">
        <p class="eyebrow"><i></i>Find us</p>
        <h3>Forge Fitness</h3>
        <p>21 Performance Avenue, Sector 18,<br>Your City – 110001</p>
        <div class="mapsec__btns">
          <a class="btn btn--dark btn--sm" href="https://www.google.com/maps/search/?api=1&query=gym" target="_blank" rel="noopener"><span class="btn__fill"></span><span class="btn__label">Get directions</span><span class="btn__icon">{ARROW_UR}</span></a>
          <a class="btn btn--ghost-dark btn--sm" href="tel:+910000000000"><span class="btn__fill"></span><span class="btn__label">Call now</span><span class="btn__icon">{ARROW}</span></a>
        </div>
      </div>
    </div>
  </div>
</section>"""


# =================================================================== page shell
TAIL = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="js/components.js?v=32" defer></script><script src="js/scroll.js?v=32" defer></script><script src="js/animations.js?v=32" defer></script>
<script src="js/interactions.js?v=32" defer></script><script src="js/main.js?v=32" defer></script>
</body></html>"""

SITE = 'https://www.example.com/'


def head(title, desc, fname, preload=False, schema=False):
    body_cls = ' class="has-hero"' if fname == 'index.html' else ''
    pre = ''
    if preload:
        pre = (f'<link rel="preload" as="image" media="(max-width: 767px)" imagesrcset="{srcset("pullup", 4 / 5.6, (480, 720, 960, 1200), "&crop=focalpoint&fp-x=0.5&fp-y=0.4")}" imagesizes="100vw" fetchpriority="high">\n'
               f'<link rel="preload" as="image" media="(min-width: 768px)" imagesrcset="{srcset("man", 16 / 9, (1200, 1800, 2400), "&crop=focalpoint&fp-x=0.5&fp-y=0.3")}" imagesizes="100vw" fetchpriority="high">\n')
    sc = f'<script type="application/ld+json">{SCHEMA}</script>\n' if schema else ''
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light"><meta name="theme-color" content="#F5F5F2">
<link rel="canonical" href="{SITE}{'' if fname == 'index.html' else fname}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{url('man', 1200, 630)}"><meta property="og:url" content="{SITE}{'' if fname == 'index.html' else fname}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='4' fill='%23111'/%3E%3Cpath d='M5 12v8M9 9v14M23 9v14M27 12v8M9 16h14' stroke='%23C8F031' stroke-width='2.6' fill='none'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com" crossorigin>
{pre}<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800;900&family=Manrope:wght@400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css?v=32"><link rel="stylesheet" href="css/animations.css?v=32"><link rel="stylesheet" href="css/responsive.css?v=32">
<script>try{{history.scrollRestoration='manual'}}catch(e){{}}document.documentElement.classList.add('js');setTimeout(function(){{if(!window.gsap){{document.documentElement.classList.remove('js')}}}},5000);</script>
{sc}</head>
<body{body_cls}>"""


PAGES_OUT = {}


def build_page(fname, title, desc, body, active, preload=False, schema=False):
    html = head(title, desc, fname, preload, schema) + nav(active) + '<main id="main">' + body + '</main>' + footer() + TAIL
    if 'id="join"' not in body:
        html = html.replace('href="#join"', 'href="contact.html"')   # land at the top of the contact page
    (ROOT / fname).write_text(html, encoding='utf-8')
    PAGES_OUT[fname] = len(html) // 1024


build_page('index.html', 'Forge Fitness — Premium Gym, Strength Training &amp; Personal Coaching',
           'Forge Fitness is a premium gym with professional equipment, expert trainers, group classes and personal coaching. Book a free trial today.',
           hero() + intro() + stats() + about() + facilities(('All facilities & equipment', 'facilities.html')) + textband() + programs(('Explore all programs', 'programs.html'))
           + trainers(('Meet the full team', 'trainers.html')) + textband(('TRAIN', 'PERFORM', 'EVOLVE')) + gallery(('Open the gallery', 'gallery.html')) + membership(('Compare all plans', 'membership.html'))
           + testimonials() + cta(), 'index.html', preload=True, schema=True)

build_page('about.html', 'About Forge Fitness — Our Story, Values &amp; Community',
           'Learn the story behind Forge Fitness: fifteen years of serious training, expert coaching and a community that shows up.',
           page_hero('About', 'BUILT BY <span class="hl">LIFTERS.</span>', 'A premium gym with one metric that matters: how much better you get. Meet the people and principles behind Forge.', 'bright', 'The Forge Fitness main training floor', '0.5')
           + about() + stats() + textband(('FORGED', 'IN', 'DISCIPLINE')) + story() + values() + why() + testimonials() + cta(), 'about.html')

build_page('facilities.html', 'Facilities &amp; Equipment — Forge Fitness',
           'Strength area, cardio zone, functional turf and recovery space — explore the premium facilities and equipment at Forge Fitness.',
           page_hero('Facilities', 'BUILT <span class="hl">TO TRAIN.</span>', 'Four purpose-built zones and commercial-grade equipment, designed so nothing gets between you and your next personal best.', 'squat', 'Squat racks on the Forge strength floor', '0.5')
           + facilities() + equipment() + textband(('PREMIUM', 'EQUIPMENT', 'CLEAN', 'SPACE')) + why() + cta(), 'facilities.html')

build_page('programs.html', 'Training Programs &amp; Class Timetable — Forge Fitness',
           'Strength, muscle building, fat loss, personal and functional training. See every program and the weekly class timetable.',
           page_hero('Training', 'TRAIN WITH <span class="hl">PURPOSE.</span>', 'Six programs, one method: assess, plan, train, evolve. Pick the path that matches your goal and your coach does the rest.', 'ropes2', 'Athlete training with battle ropes', '0.5')
           + programs() + textband(('LIFT', 'MOVE', 'RECOVER')) + process() + timetable() + cta(), 'programs.html')

build_page('gallery.html', 'Photo Gallery — Inside Forge Fitness',
           'Photos of the training floor, equipment, coaches and members at Forge Fitness. See real transformations too.',
           page_hero('Gallery', 'LIFE ON <span class="hl">THE FLOOR.</span>', 'Light, space and serious equipment — a look at where the work happens, and the people who do it.')
           + gallery_full() + results() + cta(), 'gallery.html')

build_page('trainers.html', 'Our Trainers — Certified Coaches at Forge Fitness',
           'Meet the certified strength, performance and mobility coaches at Forge Fitness.',
           page_hero('Trainers', 'MEET YOUR <span class="hl">COACHES.</span>', 'Certified, experienced and obsessed with technique. Our coaches build programmes around you — not a template.', 'rows', 'Coach spotting a member', '0.5')
           + trainers() + process('OUR <span class="hl">METHOD.</span>') + testimonials() + cta(), 'trainers.html')

build_page('membership.html', 'Membership Plans &amp; Pricing — Forge Fitness',
           'Basic, Pro and Elite memberships with flexible durations. Compare plans, read the FAQ and join today.',
           page_hero('Membership', 'CHOOSE YOUR <span class="hl">PLAN.</span>', 'Three plans, flexible durations, no hidden fees. Start with a free trial and upgrade whenever you are ready.')
           + membership(None, 'Pricing', 'SIMPLE, <span class="hl">FAIR</span> PRICING.') + compare() + faq() + join_form(), 'membership.html')

build_page('contact.html', 'Contact &amp; Free Trial — Forge Fitness',
           'Visit Forge Fitness, call us or send a message. Book your free trial class and a coach will contact you within 24 hours.',
           page_hero('Contact', 'COME <span class="hl">TRAIN</span> WITH US.', 'Fill in the form and a coach will call you within 24 hours to plan your free first session. Prefer to talk now? Call or WhatsApp us.')
           + contact_top() + map_section() + faq(), 'contact.html', schema=True)

build_page('404.html', 'Page not found — Forge Fitness', 'This page could not be found.',
           '<section class="phero" style="min-height:70svh;display:grid;align-items:center"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><b>404</b></nav>'
           '<h1 class="phero__title">REP <span class="hl">MISSED.</span></h1><p class="phero__lead" style="margin-top:18px">That page does not exist. Let us get you back to training.</p>'
           + btn('Back to home', 'index.html') + '</div></section>', None)

(ROOT / 'robots.txt').write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
urls = "".join(f'<url><loc>{SITE}{"" if f == "index.html" else f}</loc><changefreq>monthly</changefreq><priority>{"1.0" if f == "index.html" else "0.8"}</priority></url>' for f in PAGES_OUT if f != '404.html')
(ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
print("pages:", PAGES_OUT)
