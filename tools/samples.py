#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
samples.py - "🎯 שאלה לדוגמה" בסוף כל סעיף בכל האתרים, עם פתרון שנפתח בלחיצה (שלבים בירוק),
ומקרא אחיד לכל האתרים.

התוכן נמצא ב-tools/samples/<site>.py. הכלי:
  * מכניס את השאלה לדוגמה בסוף כל סעיף (בין סמנים, אפשר להריץ שוב ושוב);
  * באתר החומר התיאורטי: מוחק את השאלות הישנות (box-q) ואת הדוגמאות הפתורות שהפכו לשאלה לדוגמה,
    ושאר הדוגמאות הקצרות מוצגות כ"למשל" בתוך ההסבר;
  * באתר האלגברה: מוחק את "דוגמה מהתרגיל" (היא עכשיו השאלה לדוגמה);
  * עוטף רשימות "שלב אחר שלב" שלא בתיבה בתיבת "שלבי הפתרון" הירוקה;
  * מחליף את המקרא באותו מקרא בכל האתרים.
שימוש: python3 tools/samples.py      (דורש latex2mathml)
"""
import html, importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import reminders as R

_cs = importlib.util.spec_from_file_location('concepts', os.path.join(HERE, 'samples', 'concepts.py'))
_cm = importlib.util.module_from_spec(_cs); _cs.loader.exec_module(_cm)
CONCEPTS = _cm.C

SITES = {'algebra-solutions': 'algebra_solutions', 'algebra-theory': 'algebra_theory', 'calculus-1': 'calculus_1'}


def mathify(s):
    s = re.sub(r'\$\$(.+?)\$\$', lambda g: '\x00' + R.mwrap(g.group(1), True) + '\x01', s)
    return re.sub(r'\$(.+?)\$', lambda g: R.mwrap(g.group(1)), s)


def line(s):
    s = s.strip()
    if s.startswith('$$') and s.endswith('$$') and s.count('$$') == 2:
        # separate formulas written side by side (\qquad) go on separate lines; a single formula is never broken
        return ''.join('<div class="formula sol-formula">' + R.mwrap(f, True) + '</div>'
                       for f in s[2:-2].split('\\qquad') if f.strip())
    out = mathify(s)
    out = out.replace('\x00', '<span class="sol-disp">').replace('\x01', '</span>')
    return '<div class="sol-line">' + out + '</div>'


def tip_line(x):
    """a text line in an explanation: a long formula inside the sentence gets its own line (never broken)"""
    x = x.strip()
    if x.startswith('$$'):
        return line(x).replace('formula sol-formula', 'formula tip-f')
    parts = re.split(r'(\$[^$]+\$)', x)
    out, buf = [], ''
    for p in parts:
        if p.startswith('$') and R._visible(p[1:-1]) > 16:
            if buf.strip(' :,.-'):
                out.append('<div class="tip-t">' + mathify(buf) + '</div>')
            buf = ''
            out.append('<div class="formula tip-f">' + R.m(p[1:-1], True) + '</div>')
        else:
            buf += p
    if buf.strip(' :,.-') or not out:
        out.append('<div class="tip-t">' + mathify(buf) + '</div>')
    return ''.join(out)


def tip_html(pid, label, lines):
    body = ''.join(f'<div class="tip-h">{mathify(x[1:])}</div>' if x.startswith('§') else tip_line(x) for x in lines)
    if isinstance(label, tuple):          # (title, [concept names])
        title, names = label
        inner = (f'<span class="tb-title">{mathify(title)}</span><span class="tb-list">'
                 + ''.join(f'<span class="tb-item">{mathify(n)}</span>' for n in names) + '</span>')
    else:
        inner = mathify(label)
    btn = f'<button type="button" class="tip-btn" aria-expanded="false" aria-controls="{pid}">{inner}</button>'
    panel = f'<div class="tip-panel" id="{pid}" hidden>{body}</div>'
    return btn, panel


def tips_block(items):
    if not items:
        return ''
    btns, panels = zip(*items)
    return '<div class="tip-row">' + ''.join(btns) + '</div>' + ''.join(panels)


def render(sid, d, tips=()):
    where = {}
    for k, (si, li, label, lines) in enumerate(tips):
        where.setdefault((si, li), []).append(tip_html(f'{sid}-tip{k + 1}', label, lines))
    used = set()
    steps = ''
    for n, (title, lines) in enumerate(d['steps'], 1):
        title = re.sub(r'^שלב \d+( במצגת)?\s*[:\-]\s*', '', title)   # the step number is already on the green chip
        body = f'<div class="sol-title">{mathify(title)}</div>' + tips_block(where.get((n - 1, -1)))
        used.add((n - 1, -1))
        for j, x in enumerate(lines):
            body += line(x) + tips_block(where.get((n - 1, j)))
            used.add((n - 1, j))
        steps += f'<div class="sol-step"><div class="sol-n">שלב {n}</div><div class="sol-body">{body}</div></div>'
    lost = set(where) - used
    if lost:
        raise ValueError(f'{sid}: tips point to missing lines {sorted(lost)}')
    return (f'\n      <!-- sample:start --><div class="box box-q sample" id="{sid}-sample">'
            f'<div class="box-title"><span class="sample-src">📍 {mathify(d["src"])}</span></div>'
            f'<p class="sample-q">{mathify(d["q"])}</p>'
            f'<button type="button" class="sample-btn" aria-expanded="false" aria-controls="{sid}-sol">'
            f'<span class="sb-show">הצגת הפתרון</span><span class="sb-hide">הסתרת הפתרון</span></button>'
            f'<span class="sample-hint">כדאי לנסות לבד קודם</span>'
            f'<div class="sample-sol" id="{sid}-sol" hidden>{steps}'
            f'<div class="sol-ans"><span class="sol-ans-lbl">✅ התשובה</span> {mathify(d["ans"])}</div></div>'
            f'</div><!-- sample:end -->')


# ------------------------------------------------------------------ html helpers
def div_end(page, start):
    """index just after the </div> that closes the <div ...> starting at `start`"""
    depth, i = 0, start
    tag = re.compile(r'<(/?)div\b[^>]*>')
    for mm in tag.finditer(page, start):
        depth += -1 if mm.group(1) else 1
        if depth == 0:
            return mm.end()
    raise ValueError('unbalanced div at %d' % start)


def remove_divs(seg, opener, which=None):
    """remove <div class=...> blocks that start with `opener`; `which` = ordinals to remove (None = all)"""
    out, pos, k = [], 0, 0
    while True:
        a = seg.find(opener, pos)
        if a == -1:
            break
        b = div_end(seg, a)
        if which is None or k in which:
            a2 = a
            while a2 > 0 and seg[a2 - 1] in ' \t':
                a2 -= 1
            if a2 > 0 and seg[a2 - 1] == '\n':
                a2 -= 1
            out.append(seg[pos:a2])
        else:
            out.append(seg[pos:b])
        pos, k = b, k + 1
    out.append(seg[pos:])
    return ''.join(out)


def section_end(page, stop):
    """move back over whitespace and html comments so the sample goes right after the last content"""
    i = stop
    while True:
        j = i
        while j > 0 and page[j - 1].isspace():
            j -= 1
        if page[max(0, j - 3):j] == '-->':
            c = page.rfind('<!--', 0, j)
            if 'sample:end' in page[c:j] or 'rem:end' in page[c:j]:
                return j
            i = c
            continue
        return j


# ------------------------------------------------------------------ per-site cleanup
THEORY_DROP_EX = {'ex1-s1': [0], 'ex1-s2': [0, 1, 2], 'ex1-s6': [1], 'ex1-s7': [0], 'ex1-s8': [0],
                  'ex1-s9': [1], 'ex1-s11': [0], 'ex2-s1': [0], 'ex2-s3': [0], 'ex2-s4': [0],
                  'ex2-s5': [0], 'ex2-s7': [1]}


def per_section(page, fn):
    secs = R.sections(page)
    out, last = [], 0
    for hid, a, b, stop in secs:
        out.append(page[last:b])
        out.append(fn(hid, page[b:stop]))
        last = stop
    out.append(page[last:])
    return ''.join(out)


def eg(seg):
    """remaining short worked examples -> 'למשל' inside the explanation"""
    def conv(mm):
        t = mm.group(1).strip()
        t = re.sub(r'^דוגמאות\s*', '', t)
        return '<div class="eg"><div class="eg-title">למשל' + (': ' + t if t else '') + '</div>'
    return re.sub(r'<div class="box box-ex">\s*<div class="box-title">(.*?)</div>', conv, seg, flags=re.S)


def clean_theory(page):
    def fn(hid, seg):
        seg = remove_divs(seg, '<div class="box box-q">')
        if hid in THEORY_DROP_EX:
            seg = remove_divs(seg, '<div class="box box-ex">', set(THEORY_DROP_EX[hid]))
        return eg(seg)
    return per_section(page, fn)


def clean_algebra(page):
    def fn(hid, seg):
        mm = re.search(r'\n?[ \t]*<h4 class="sub"[^>]*>\s*דוגמה[^<]*</h4>', seg)
        if not mm:
            return seg
        a, b = mm.start(), mm.end()
        while True:
            p = re.match(r'\s*<p>.*?</p>', seg[b:], re.S)
            if not p:
                break
            b += p.end()
        return seg[:a] + seg[b:]
    return per_section(page, fn)


def clean_calculus(page):
    # תיקון באג תצוגה: בדוגמה של סעיף 11 הופיע 3 בחזקת x במקום 3x
    return page.replace('<msup><mn>3</mn><mi>x</mi></msup><mo>&#x0002B;</mo><mn>1</mn>',
                        '<mn>3</mn><mi>x</mi><mo>&#x0002B;</mo><mn>1</mn>')


def wrap_steps(page):
    def conv(mm):
        before = page[max(0, mm.start() - 120):mm.start()]
        if 'callout-steps' in before:
            return mm.group(0)
        return '<div class="callout callout-steps"><div class="callout-title"></div>' + mm.group(0) + '</div>'
    return re.sub(r'<ol class="steps">.*?</ol>', conv, page, flags=re.S)


# ------------------------------------------------------------------ legend (identical everywhere)
LEGEND = '''<details class="legend">
        <summary class="legend-title">מקרא: מה כל סוג תיבה מראה</summary>
        <div class="legend-grid">
          <div class="callout callout-id"><div class="callout-title"></div><p>איך יודעים שזה סוג השאלה הזה</p></div>
          <div class="box box-def"><div class="box-title"></div><p>מה המושג אומר בדיוק</p></div>
          <div class="box box-thm"><div class="box-title"></div><p>הנוסחה או הכלל שצריך לזכור</p></div>
          <div class="callout callout-sym"><div class="callout-title"></div><p>מה כל סימן ואות אומרים</p></div>
          <div class="callout callout-steps"><div class="callout-title"></div><p>מה עושים, שלב אחרי שלב</p></div>
          <div class="box box-q sample"><div class="box-title"></div><p>שאלה מהחומר. לחיצה על "הצגת הפתרון" פותחת פתרון מלא, שלב אחרי שלב</p></div>
          <div class="callout callout-star"><div class="callout-title"></div><p>כלל או טיפ שכדאי לזכור</p></div>
          <div class="callout callout-warn"><div class="callout-title"></div><p>טעות נפוצה שכדאי להיזהר ממנה</p></div>
          <div class="callout callout-check"><div class="callout-title"></div><p>איך מוודאים שהתשובה נכונה</p></div>
          <div class="callout callout-info"><div class="callout-title"></div><p>הבהרה או הרחבה קטנה</p></div>
          <div class="callout callout-proof"><div class="callout-title"></div><p>למה הנוסחה נכונה (נפתחת בלחיצה)</p></div>
          <div class="tip-legend"><span class="tip-btn">מה צריך לדעת לשלב הזה</span><p>כפתור בכל שלב ב"שלבי הפתרון": לחיצה מסבירה מההתחלה כל מה שצריך לדעת כדי לבצע את השלב, עם דוגמאות</p></div>
        </div>
      </details>'''


def set_legend(page):
    a = page.find('<details class="legend">')
    if a == -1:
        return page
    depth = 0
    for mm in re.finditer(r'<(/?)details\b[^>]*>', page[a:]):
        depth += -1 if mm.group(1) else 1
        if depth == 0:
            return page[:a] + LEGEND + page[a + mm.end():]
    raise ValueError('unbalanced legend')


ASSETS = '''<!-- samples-assets:start -->
<style>
  /* תוויות אחידות לכל סוגי התיבות - זהות בכל האתרים */
  .callout-id{ --c:#2C4A8C; --tint:#F3F6FC; --lbl:"🔎 איך מזהים את סוג השאלה"; }
  .callout-steps{ --c:#2A6F63; --tint:#EEF7F3; --lbl:"🪜 שלבי הפתרון"; }
  .callout-sym{ --c:#4A5578; --tint:#F1F3F8; --lbl:"🔤 מקרא סימנים"; }
  .callout-star{ --c:#B7790A; --tint:#FFF7E3; --lbl:"⭐ כלל או טיפ"; }
  .callout-warn{ --c:#A23F35; --tint:#FDF0EE; --lbl:"⚠️ שימי לב"; }
  .callout-check{ --c:#1B7A99; --tint:#EAF6FA; --lbl:"✅ בדיקה"; }
  .callout-info{ --c:#6A6E78; --tint:#F6F6F4; --lbl:"📌 הערה"; }
  .callout-proof{ --c:#6A6E78; --tint:#FAFAF7; --lbl:"🔍 הוכחה"; border-style:dashed; }
  .callout-steps .steps{ margin-top:4px; }

  /* 🎯 שאלה לדוגמה - סגול */
  .box-q{ --c:#6B3FA0; --tint:#FFFFFF; --lbl:"🎯 שאלה לדוגמה"; }
  .sample{ border:2.5px solid var(--c) !important; box-shadow:0 3px 0 rgba(107,63,160,.16); background:#FBF9FE; margin-top:28px; }
  .sample > .box-title::after{ content:none !important; }
  .sample-src{ font-weight:600; font-size:.86rem; opacity:.95; }
  .sample-q{ font-size:1.06rem; font-weight:600; color:#2E1F4A; line-height:1.9; margin:4px 0 12px; overflow-x:auto; }
  .sample-btn{ min-height:44px; padding:0 20px; border-radius:100px; border:2px solid #6B3FA0; background:#6B3FA0; color:#fff;
    font:inherit; font-weight:700; font-size:.97rem; cursor:pointer; display:inline-flex; align-items:center; gap:8px; }
  .sample-btn::before{ content:"▾"; }
  .sample-btn[aria-expanded="true"]{ background:#fff; color:#6B3FA0; }
  .sample-btn[aria-expanded="true"]::before{ content:"▴"; }
  .sample-btn .sb-hide{ display:none; }
  .sample-btn[aria-expanded="true"] .sb-show{ display:none; }
  .sample-btn[aria-expanded="true"] .sb-hide{ display:inline; }
  .sample-btn:focus-visible{ outline:3px solid #A8791E; outline-offset:3px; }
  .sample-hint{ margin-inline-start:12px; font-size:.86rem; color:#6B5A86; }
  .sample-sol{ margin:16px 0 8px; display:flex; flex-direction:column; gap:10px; }
  .sample-sol[hidden]{ display:none; }

  /* שלבי הפתרון - ירוק, כמו "שלבי הפתרון" */
  .sol-step{ display:flex; gap:12px; align-items:flex-start; background:#EEF7F3; border:1.5px solid #2A6F63;
    border-inline-start-width:5px; border-radius:10px; padding:10px 14px; }
  .sol-n{ flex:0 0 auto; background:#2A6F63; color:#fff; font-weight:700; font-size:.82rem; border-radius:100px; padding:3px 10px; margin-top:3px; white-space:nowrap; }
  .sol-body{ flex:1 1 auto; min-width:0; max-width:100%; }
  .sol-title{ font-weight:700; color:#1E5A4F; margin-bottom:4px; line-height:1.7; }
  .sol-line{ line-height:1.9; margin:3px 0; overflow-x:auto; }
  .sol-formula{ margin:6px 0 !important; padding:8px 10px !important; background:rgba(255,255,255,.75) !important;
    border:none !important; border-radius:8px; overflow-x:auto; text-align:center; }
  .sample math, .rem-panel math, .tip-panel math{ max-width:none !important; }
  /* נוסחה לא נשברת לשורות: בטלפון היא קטנה מעט, ואם עדיין רחבה - גוללים אותה הצידה */
  .sol-formula, .tip-f, .sol-line, .tip-t, .sol-ans, .sample-q{ -webkit-overflow-scrolling:touch; }
  .sol-formula math, .tip-f math{ white-space:nowrap; }
  .sol-formula, .tip-f{ direction:ltr; }   /* גלילה הצידה מתחילה מתחילת הנוסחה (משמאל) */
  @media (max-width:560px){ .sol-formula, .tip-f{ font-size:.9em; } }
  .sol-disp{ display:block; text-align:center; margin:6px 0; }
  .sol-ans{ background:#fff; border:2px solid #2A6F63; border-radius:10px; padding:10px 14px; line-height:1.9; overflow-x:auto; }
  .sol-ans-lbl{ font-weight:800; color:#1E5A4F; margin-inline-end:6px; }
  @media (max-width:560px){ .sol-step{ flex-direction:column; align-items:stretch; gap:6px; padding:10px 12px; } .sol-n{ align-self:flex-start; } .sample-hint{ display:block; margin:8px 0 0; } }


  /* 💡 תזכורת בתוך שלב בפתרון */
  .tip-row{ display:flex; flex-wrap:wrap; gap:6px; margin:6px 0 4px; }
  .steps .tip-panel{ font-weight:400; }
  .tip-btn{ min-height:38px; padding:4px 12px; border-radius:100px; border:1.5px solid #8A9BC4; background:#fff; color:#2C3A5E;
    font:inherit; font-size:.88rem; font-weight:600; line-height:1.5; cursor:pointer; display:inline-flex; align-items:center; gap:6px; text-align:start; }
  .tip-btn::before{ content:"💡"; }
  .tip-btn[aria-expanded="true"]{ background:#5D6F9E; border-color:#5D6F9E; color:#fff; }
  .tip-btn:focus-visible{ outline:3px solid #A8791E; outline-offset:2px; }
  .tip-panel{ margin:2px 0 10px; padding:10px 14px; background:#fff; border:1.5px solid #8A9BC4; border-inline-start-width:5px; border-radius:10px; }
  .tip-panel[hidden]{ display:none; }
  .tip-h{ font-weight:800; color:#2C3A5E; margin:14px 0 4px; padding-top:10px; border-top:1px solid #DCE2EF; font-size:1rem; }
  .tip-panel > .tip-h:first-child{ margin-top:0; padding-top:0; border-top:none; }
  .tip-ref{ color:#6A6E78; font-size:.88rem; }
  @media (max-width:560px){ .steps li .tip-panel{ margin-inline-start:-30px; } }
  .tip-btn{ text-align:start; }

  .tip-t{ line-height:1.9; margin:4px 0; overflow-x:auto; }
  .tip-f{ margin:6px 0 !important; padding:6px 8px !important; background:#F3F5FA !important; border:none !important; border-radius:8px; text-align:center; overflow-x:auto; }
  .tip-panel math{ max-width:none !important; }
  .tip-legend{ border:1.5px dashed #8A9BC4; border-radius:12px; padding:12px 14px; background:#fff; }
  .tip-legend p{ margin:8px 0 0; }
  .tip-legend .tip-btn{ cursor:default; }
  .mwrap{ unicode-bidi:isolate; }
  .mfrag{ display:inline-block; margin:1px .12em; vertical-align:middle; }
  .mfrag.mgap{ margin-inline-start:1.2em; }

  /* כפתור "מה צריך לדעת" וההסבר - באותה מסגרת */
  .tip-wrap{ margin:10px auto 6px; max-width:100%; border:1.5px solid #8A9BC4; border-radius:14px; background:#fff; overflow:hidden; }
  .tip-wrap > .tip-btn{ width:100%; border:0; border-radius:0; align-items:center; justify-content:center; text-align:center; min-height:48px; }
  .tip-wrap > .tip-btn .tb-list{ justify-content:center; }
  .tip-wrap > .tip-btn[aria-expanded="true"]{ border-bottom:1px solid #DCE2EF; }
  .tip-wrap > .tip-panel{ margin:0 !important; border:0; border-radius:0; padding:12px 16px 14px; }
  @media (max-width:560px){ .steps li .tip-wrap{ margin-inline-start:-30px; } .steps li .tip-panel{ margin-inline-start:0 !important; } }
  .mcont{ color:#A8791E; font-weight:700; }
  .mpar{ white-space:nowrap; }
  .tline{ display:block; white-space:nowrap; overflow-x:auto; overflow-y:hidden; scrollbar-width:thin; }
  .mparline{ display:block; white-space:nowrap; }
  /* כל נוסחה שהיא ביטוי - בשורה משלה, משמאל לימין; העברית מימין לשמאל */
  .mline{ display:block; direction:ltr; text-align:center; margin:6px 0; padding:2px 0; overflow-x:auto; overflow-y:hidden; }
  .mline math{ max-width:none !important; white-space:nowrap; }
  .mjoin{ display:block; text-align:center; color:#5B5F6B; font-size:.92rem; }
  .steps li .mline{ text-align:center; }
  .tip-btn{ flex-direction:column; align-items:flex-start; gap:6px; padding:8px 14px; border-radius:14px; }
  .tip-btn::before{ display:none; }
  .tb-title{ font-weight:800; }
  .tb-title::before{ content:"💡 "; }
  .tb-list{ display:flex; flex-wrap:wrap; gap:6px; }
  .tb-item{ display:inline-block; unicode-bidi:isolate; background:#EEF1F8; color:#2C3A5E; border-radius:100px; padding:1px 10px; font-weight:600; font-size:.85rem; }
  .tip-btn[aria-expanded="true"] .tb-item{ background:rgba(255,255,255,.2); color:#fff; }
  .tip-t, .sol-line, .steps li{ line-height:1.9; }
  /* "למשל" - דוגמה קצרה בתוך ההסבר */
  .eg{ margin:12px 0 18px; padding:6px 14px; border-inline-start:3px solid #CFC6B2; max-width:80ch; overflow-x:auto; }
  .eg > p{ margin:4px 0; }
  .eg-title{ font-weight:700; color:#5B5F6B; font-size:.93rem; margin-bottom:2px; }
  .eg .formula{ background:transparent; border:none; padding:2px 0; margin:4px 0; }

  /* מקרא */
  .legend-grid .sample{ margin:0 !important; }
  .legend-grid .sample > p{ font-size:.92rem !important; font-weight:400 !important; }
  .legend-grid .rem-legend{ margin:0; }
  .legend-grid .rem-legend p{ padding:8px 14px 10px; }
  @media print{ .tip-panel[hidden]{ display:block !important; } .sample-sol[hidden]{ display:flex !important; } .sample-btn, .sample-hint{ display:none; } }
</style>
<script>
(function(){
  try {
    document.querySelectorAll('.sample-btn').forEach(function(b){
      var sol = document.getElementById(b.getAttribute('aria-controls'));
      if(!sol) return;
      b.addEventListener('click', function(){
        var open = b.getAttribute('aria-expanded') === 'true';
        b.setAttribute('aria-expanded', String(!open)); sol.hidden = open;
        if(!open){ var r = b.getBoundingClientRect(); if(r.top < 60) b.scrollIntoView({block:'center'}); }
      });
    });

    document.querySelectorAll('.tip-btn[aria-controls]').forEach(function(b){
      var p = document.getElementById(b.getAttribute('aria-controls'));
      if(!p) return;
      b.addEventListener('click', function(){
        var open = b.getAttribute('aria-expanded') === 'true';
        b.setAttribute('aria-expanded', String(!open)); p.hidden = open;
      });
    });
  } catch(err){}
})();
</script>
<!-- samples-assets:end -->
'''


TIP_RE = re.compile(r'<!-- tip:start -->.*?<!-- tip:end -->', re.S)
NEWSTEPS_RE = re.compile(r'\n?\s*<!-- newsteps:start -->.*?<!-- newsteps:end -->', re.S)


def concept_tip(keys, seen, stepno):
    """every concept the step needs, explained in full - only the first time it appears in this solution"""
    C = CONCEPTS
    new = [k for k in keys if k not in seen]
    lines = []
    for k in new:
        lines.append('§' + C[k]['name'])
        lines += C[k]['full']
        seen[k] = stepno
    return ('מה צריך לדעת לשלב הזה', [C[k]['name'] for k in new]), lines, new


def step_tips_html(prefix, keys, seen, stepno):
    if not keys:
        return ''
    label, lines, new = concept_tip(keys, seen, stepno)
    if not new:
        return ''
    btn, panel = tip_html(prefix, label, lines)
    return '<!-- tip:start --><div class="tip-wrap">' + btn + panel + '</div><!-- tip:end -->'


def apply_steps(page, stm):
    page = TIP_RE.sub('', page)
    page = NEWSTEPS_RE.sub('', page)
    secs = R.sections(page)
    out, last = [], 0
    for hid, a, b, stop in secs:
        seg = page[b:stop]
        seen = {}
        tips = getattr(stm, 'STEP_CONCEPTS', {}).get(hid, {})
        mm = re.search(r'<ol class="steps">(.*?)</ol>', seg, re.S)
        if tips:
            if not mm:
                raise ValueError(f'{hid}: no steps list')
            lis = list(re.finditer(r'<li>(.*?)</li>', mm.group(1), re.S))
            bad = [i for i in tips if i >= len(lis)]
            if bad:
                raise ValueError(f'{hid}: concepts for missing steps {bad}')
            htmls = {i: step_tips_html(f'{hid}-st{i + 1}', tips[i], seen, i + 1) for i in sorted(tips)}
            body = mm.group(1)
            for i in sorted(tips, reverse=True):
                e = lis[i].end() - len('</li>')
                body = body[:e] + htmls[i] + body[e:]
            seg = seg[:mm.start(1)] + body + seg[mm.end(1):]
        new = getattr(stm, 'NEW_STEPS', {}).get(hid)
        if new:
            if mm:
                raise ValueError(f'{hid}: already has steps')
            lis = ''.join(f'<li>{mathify(t)}{step_tips_html(f"{hid}-st{i + 1}", keys, seen, i + 1)}</li>'
                          for i, (t, keys) in enumerate(new))
            block = ('\n      <!-- newsteps:start --><div class="callout callout-steps"><div class="callout-title"></div>'
                     f'<ol class="steps">{lis}</ol></div><!-- newsteps:end -->')
            j = section_end(seg, len(seg))
            seg = seg[:j] + block + seg[j:]
        out.append(page[last:b]); out.append(seg); last = stop
    out.append(page[last:])
    return ''.join(out)


REL_CHARS = set('=<>≤≥⇒⇔≠≈∈')
OP_CHARS = set('+−-·×/√±')


def _mtext(mhtml):
    t = re.sub(r'<annotation[^>]*>.*?</annotation>', '', mhtml, flags=re.S)
    t = html.unescape(re.sub(r'<[^>]+>', '', t))
    return re.sub(r'\s+', '', t)



def _paren_lines(frag, fn):
    """find '( ... )' in text (skipping over formulas) without regex backtracking"""
    out, i, n = [], 0, len(frag)
    while i < n:
        j = frag.find('(', i)
        if j == -1:
            out.append(frag[i:]); break
        # is '(' inside a tag or a formula? then skip
        if frag.rfind('<math', 0, j) > frag.rfind('</math>', 0, j) or frag.rfind('<', 0, j) > frag.rfind('>', 0, j):
            out.append(frag[i:j + 1]); i = j + 1; continue
        k, ok = j + 1, False
        while k < n and k - j < 2000:
            ch = frag[k]
            if frag.startswith('<math', k):
                e = frag.find('</math>', k)
                if e == -1: break
                k = e + 7; continue
            if frag.startswith('<b>', k) or frag.startswith('</b>', k):
                k += 3 if frag[k + 1] == 'b' else 4; continue
            if ch in '(<':
                break
            if ch == ')':
                ok = True; break
            k += 1
        if ok:
            e = k + 1 + (1 if frag[k + 1:k + 2] == '.' else 0)
            out.append(frag[i:j]); out.append(fn_match(frag[j:e], fn)); i = e
        else:
            out.append(frag[i:j + 1]); i = j + 1
    return ''.join(out)


class _M:
    def __init__(self, t): self.t = t
    def group(self, k=0): return self.t


def fn_match(t, fn):
    return fn(_M(t))


def _glue_parens(frag):
    """short parentheses that belong to the sentence - never split from what is inside them"""
    def g(m):
        inner = m.group(0)
        vis = re.sub(r'<math\b.*?</math>', lambda q: _mtext(q.group(0)), inner, flags=re.S)
        vis = re.sub(r'<[^>]+>', '', vis)
        return '<span class="mpar">' + inner + '</span>' if len(vis) <= 18 else inner
    return _paren_lines(frag, g)


BOUND = re.compile(r'(\x02\d+\x03|\x07\d+\x08|<!--.*?-->|</?(?:li|ol|ul|div|p|br|button|h\d)\b[^>]*>)', re.S)
LINE_MAX = 32      # about one line on a phone
SCROLL_MAX = 46    # a clause up to this length scrolls sideways instead of being split


def _vis_len(t):
    t = re.sub(r'<math\b.*?</math>', lambda q: _mtext(q.group(0)), t, flags=re.S)
    return len(html.unescape(re.sub(r'<[^>]+>', '', t)).strip())


def _split_points(t):
    """positions after '. ' ', ' '; ' outside tags, formulas, glued parentheses and bold"""
    pts, i, depth, n = [], 0, 0, len(t)
    while i < n:
        if t.startswith('<span class="mpar">', i):
            e = t.find('</math>', i)
            j = t.find('</span>', e if e != -1 else i)
            i = j + 7 if j != -1 else n; continue
        if t.startswith('<math', i):
            i = t.find('</math>', i) + 7; continue
        if t.startswith('<b>', i): depth += 1; i += 3; continue
        if t.startswith('</b>', i): depth -= 1; i += 4; continue
        if t[i] == '<':
            i = t.find('>', i) + 1; continue
        if depth == 0 and t[i] in '.,;' and t[i + 1:i + 2] == ' ':
            pts.append(i + 1)
        i += 1
    return pts


def _space_points(t):
    pts, i, depth, n = [], 0, 0, len(t)
    while i < n:
        if t.startswith('<span class="mpar">', i):
            e = t.find('</math>', i); j = t.find('</span>', e if e != -1 else i)
            i = j + 7 if j != -1 else n; continue
        if t.startswith('<math', i):
            i = t.find('</math>', i) + 7; continue
        if t.startswith('<b>', i): depth += 1; i += 3; continue
        if t.startswith('</b>', i): depth -= 1; i += 4; continue
        if t[i] == '<':
            i = t.find('>', i) + 1; continue
        if depth == 0 and t[i] == ' ':
            pts.append(i + 1)
        i += 1
    return pts


def _text_lines(frag):
    parts = BOUND.split(frag)
    out = []
    for k, p in enumerate(parts):
        if k % 2 == 1 or not p.strip() or not (HEB.search(p) or '<math' in p):
            out.append(p); continue
        lead = p[:len(p) - len(p.lstrip())]; trail = p[len(p.rstrip()):]
        body = p.strip()
        pieces = [body]
        if _vis_len(body) > LINE_MAX:
            pieces, start, last = [], 0, 0
            for q in _split_points(body) + [len(body)]:
                if _vis_len(body[start:q]) > LINE_MAX and last > start:
                    pieces.append(body[start:last]); start = last
                last = q
            pieces.append(body[start:])
            # a clause that is still very long: split at a space near its middle (outside formulas)
            fine = []
            for x in pieces:
                while _vis_len(x) > SCROLL_MAX:
                    sp = [i for i in _space_points(x) if 0.35 < _vis_len(x[:i]) / _vis_len(x) < 0.65]
                    if not sp:
                        break
                    i = min(sp, key=lambda i: abs(_vis_len(x[:i]) - _vis_len(x) / 2))
                    fine.append(x[:i]); x = x[i:]
                fine.append(x)
            pieces = fine
        out.append(lead + ''.join(f'<span class="tline">{x.strip()}</span><!--/t-->' for x in pieces if x.strip()) + trail)
    return ''.join(out)


HEB = re.compile(r'[֐-׿]')


def separate_math(frag):
    """Hebrew right-to-left, formulas left-to-right: an expression goes to a line of its own (never broken).
    The Hebrew line before it ends with ':' and a sentence that continues after it starts with '←',
    so it is clear that the lines belong together."""
    keep = {}
    def protect(mm):
        keep[len(keep)] = mm.group(0)
        return f'\x02{len(keep) - 1}\x03'
    frag = re.sub(r'<button\b.*?</button>|<div class="tip-h">.*?</div>|<div class="formula[^"]*">.*?</div>|'
                  r'<span class="tline">.*?</span><!--/t-->|<span class="(?:mline|mjoin)">.*?</span>|<span class="mparline">.*?</math>[^<]*\)\.?</span>', protect, frag, flags=re.S)
    moved = []
    def conv(mm):
        t = _mtext(mm.group(0))
        lead = re.sub(r'<[^>]+>', '', mm.string[max(0, mm.start() - 40):mm.start()]).rstrip()
        is_example = lead.endswith(('דוגמה:', 'דוגמה', 'למשל:', 'למשל', 'דוגמאות:'))
        has_op = bool(OP_CHARS & set(t)) or '<mfrac' in mm.group(0) or '<msqrt' in mm.group(0) or '<mroot' in mm.group(0)
        if (len(t) > 6 or (len(t) >= 4 and REL_CHARS & set(t)) or (len(t) >= 3 and has_op)
                or (is_example and len(t) >= 2)):
            moved.append(mm.group(0))
            return f'\x04{len(moved) - 1}\x05'
        return mm.group(0)
    frag = re.sub(r'<math\b[^>]*display="inline"[^>]*>.*?</math>', conv, frag, flags=re.S)
    # a moved formula that was inside parentheses takes them along
    frag = re.sub(r'\(\s*(\x04\d+\x05)\s*\)', lambda m: '\x06' + m.group(1), frag)
    # connectors between two formulas
    frag = re.sub(r'(\x05)\s*(?:,\s*)?(?:ו-?|וגם)\s*(\x06?\x04)', r'\1<span class="mjoin">וגם</span>\2', frag)
    frag = re.sub(r'(\x05)\s*(?:,\s*)?או\s*(\x06?\x04)', r'\1<span class="mjoin">או</span>\2', frag)
    frag = re.sub(r'(\x05)\s*[,;]?\s*(\x06?\x04)', r'\1\2', frag)
    # Hebrew sentence before a formula: ends with an arrow; the formula is on the next line
    def before(m):
        core = m.group(1).rstrip()
        if not HEB.search(core) and not core.endswith(('</b>', ')')):
            return m.group(0)
        core = core.rstrip(':,;').rstrip()
        return core + ' ←' + m.group(2)
    frag = re.sub(r'((?:[^<>\x04\x05]|</b>|<b>|<math\b[^>]*>[^\x04]*?</math>)*?(?:[^\s<>\x04\x05\x06]|</math>)(?:</b>)?)\s*(\x06?\x04)', before, frag)
    formula_keys = {k for k, v in keep.items() if v.startswith('<div class="formula')}
    def colon_arrow(m):
        return (m.group(1) + ' ←' + m.group(2)) if int(m.group(3)) in formula_keys else m.group(0)
    frag = re.sub(r'([\u0590-\u05FF)"\w])\s*:\s*((?:</div>|</p>|</span>)?\s*(?:<div class="(?:tip-t|sol-line)">)?\s*\x02(\d+)\x03)', colon_arrow, frag)
    # text right after a formula: drop the punctuation that belonged to it
    def after(m):
        rest = m.group(2).lstrip('.,;:').lstrip()
        if rest.startswith('-'):
            rest = rest[1:].lstrip()
        return m.group(1) + rest
    frag = re.sub(r'(\x05)\s*([^<\x02\x04]+)', after, frag)
    def put(m):
        f = moved[int(m.group(2))]
        return '<span class="mline">' + ('(' + f + ')' if m.group(1) else f) + '</span>'
    frag = re.sub(r'(\x06)?\x04(\d+)\x05', put, frag)
    # a longer parenthetical remark with a formula: a line of its own; a short one stays in the sentence
    def paren_line(m):
        vis = re.sub(r'<math\b.*?</math>', lambda q: _mtext(q.group(0)), m.group(0), flags=re.S)
        vis = re.sub(r'<[^>]+>', '', vis)
        if '<math' in m.group(0) and len(vis) > 18:
            return '<span class="mparline">' + m.group(0) + '</span>'
        return m.group(0)
    frag = _paren_lines(frag, paren_line)
    # hide finished lines, glue short parentheses, then make every Hebrew run a line that does not wrap
    hold = {}
    def hide(mm):
        hold[len(hold)] = mm.group(0)
        return f'\x07{len(hold) - 1}\x08'
    frag = re.sub(r'<span class="(?:mline|mjoin|mparline)">.*?</span>', hide, frag, flags=re.S)
    frag = _glue_parens(frag)
    frag = _text_lines(frag)
    for k in sorted(hold, reverse=True):
        frag = frag.replace(f'\x07{k}\x08', hold[k])
    for k in sorted(keep, reverse=True):
        frag = frag.replace(f'\x02{k}\x03', keep[k])
    return frag


FENCE = re.compile(r'<mo(?![^>]*lspace)([^>]*)>(&#x00028;|&#x00029;|&#x0005B;|&#x0005D;|&#x0007C;|\(|\)|\[|\]|\|)</mo>')


def tight_fences(page):
    """no extra space inside parentheses and absolute-value bars"""
    return FENCE.sub(r'<mo lspace="0" rspace="0"\1>\2</mo>', page)


def separate_regions(page):
    out, pos = [], 0
    pat = re.compile(r'<div class="callout callout-steps">|<div class="box box-q sample"')
    while True:
        mm = pat.search(page, pos)
        if not mm:
            break
        e = div_end(page, mm.start())
        out.append(page[pos:mm.start()]); out.append(separate_math(page[mm.start():e])); pos = e
    out.append(page[pos:])
    return ''.join(out)

SAMPLE_RE = re.compile(r'\n?\s*<!-- sample:start -->.*?<!-- sample:end -->', re.S)


def apply(site, page):
    spec = importlib.util.spec_from_file_location(SITES[site], os.path.join(HERE, 'samples', SITES[site] + '.py'))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    data = mod.SAMPLES
    tips = {}
    sp = os.path.join(HERE, 'samples', 'steps_' + SITES[site] + '.py')
    spec = importlib.util.spec_from_file_location('steps_' + SITES[site], sp)
    stm = importlib.util.module_from_spec(spec); spec.loader.exec_module(stm)
    page = SAMPLE_RE.sub('', page)
    page = R.REM_RE.sub('', page)
    a = page.find('<!-- rem-assets:start -->')
    if a != -1:
        page = page[:a] + page[page.index('<!-- rem-assets:end -->') + len('<!-- rem-assets:end -->\n'):]
    if site == 'algebra-theory':
        page = clean_theory(page)
    elif site == 'algebra-solutions':
        page = clean_algebra(page)
    else:
        page = clean_calculus(page)
    page = wrap_steps(page)
    page = apply_steps(page, stm)
    page = set_legend(page)
    missing = []
    secs = R.sections(page)
    out, last = [], 0
    for hid, a, b, stop in secs:
        if hid not in data:
            missing.append(hid)
            continue
        ins = section_end(page, stop)
        out.append(page[last:ins]); out.append(render(hid, data[hid], tips.get(hid, ()))); last = ins
    out.append(page[last:])
    page = ''.join(out)
    page = separate_regions(page)
    page = tight_fences(page)
    a = page.find('<!-- samples-assets:start -->')
    if a != -1:
        page = page[:a] + page[page.index('<!-- samples-assets:end -->') + len('<!-- samples-assets:end -->\n'):]
    i = page.rindex('</body>')
    page = page[:i] + ASSETS + page[i:]
    return page, missing, len(secs) - len(missing)


def main():
    for site in SITES:
        p = os.path.join(ROOT, site, 'index.html')
        page, missing, n = apply(site, open(p, encoding='utf-8').read())
        open(p, 'w', encoding='utf-8').write(page)
        print(f'{site}: {n} sample questions' + (f'; missing: {missing}' if missing else ''))


if __name__ == '__main__':
    main()
