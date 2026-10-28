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

SITES = {'algebra-solutions': 'algebra_solutions', 'algebra-theory': 'algebra_theory', 'calculus-1': 'calculus_1'}


def mathify(s):
    s = re.sub(r'\$\$(.+?)\$\$', lambda g: '\x00' + R.mwrap(g.group(1), True) + '\x01', s)
    return re.sub(r'\$(.+?)\$', lambda g: R.mwrap(g.group(1)), s)


def line(s):
    s = s.strip()
    if s.startswith('$$') and s.endswith('$$') and s.count('$$') == 2:
        return '<div class="formula sol-formula">' + R.mwrap(s[2:-2], True) + '</div>'
    out = mathify(s)
    out = out.replace('\x00', '<span class="sol-disp">').replace('\x01', '</span>')
    return '<div class="sol-line">' + out + '</div>'


def tip_html(pid, label, lines):
    body = ''.join(line(x).replace('sol-line', 'tip-t').replace('formula sol-formula', 'formula tip-f') for x in lines)
    btn = (f'<button type="button" class="tip-btn" aria-expanded="false" aria-controls="{pid}">'
           f'{mathify(label)}</button>')
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
          <div class="tip-legend"><span class="tip-btn">תזכורת</span><p>כפתור בתוך "שלבי הפתרון", ליד מה שצריך להיזכר בו. לחיצה פותחת הסבר מפורט לדבר הזה, עם דוגמה</p></div>
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
  .sample math, .rem-panel math{ max-width:none !important; }
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
  .tip-t{ line-height:1.9; margin:4px 0; overflow-x:auto; }
  .tip-f{ margin:6px 0 !important; padding:6px 8px !important; background:#F3F5FA !important; border:none !important; border-radius:8px; text-align:center; overflow-x:auto; }
  .tip-panel math{ max-width:none !important; }
  .tip-legend{ border:1.5px dashed #8A9BC4; border-radius:12px; padding:12px 14px; background:#fff; }
  .tip-legend p{ margin:8px 0 0; }
  .tip-legend .tip-btn{ cursor:default; }
  .mwrap{ unicode-bidi:isolate; }
  .mfrag{ display:inline-block; margin:1px .12em; vertical-align:middle; }
  .mfrag.mgap{ margin-inline-start:1.2em; }

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


def step_tips_html(prefix, tips):
    items = [tip_html(f'{prefix}-{k + 1}', label, lines) for k, (label, lines) in enumerate(tips)]
    return '<!-- tip:start -->' + tips_block(items) + '<!-- tip:end -->' if items else ''


def apply_steps(page, stm):
    page = TIP_RE.sub('', page)
    page = NEWSTEPS_RE.sub('', page)
    secs = R.sections(page)
    out, last = [], 0
    for hid, a, b, stop in secs:
        seg = page[b:stop]
        tips = getattr(stm, 'STEP_TIPS', {}).get(hid, {})
        mm = re.search(r'<ol class="steps">(.*?)</ol>', seg, re.S)
        if tips:
            if not mm:
                raise ValueError(f'{hid}: no steps list for tips')
            lis = list(re.finditer(r'<li>(.*?)</li>', mm.group(1), re.S))
            bad = [i for i in tips if i >= len(lis)]
            if bad:
                raise ValueError(f'{hid}: tips for missing steps {bad}')
            body = mm.group(1)
            for i in sorted(tips, reverse=True):
                e = lis[i].end() - len('</li>')
                body = body[:e] + step_tips_html(f'{hid}-st{i + 1}', tips[i]) + body[e:]
            seg = seg[:mm.start(1)] + body + seg[mm.end(1):]
        new = getattr(stm, 'NEW_STEPS', {}).get(hid)
        if new:
            if mm:
                raise ValueError(f'{hid}: already has steps')
            lis = ''.join(f'<li>{mathify(t)}{step_tips_html(f"{hid}-st{i + 1}", tl)}</li>' for i, (t, tl) in enumerate(new))
            block = ('\n      <!-- newsteps:start --><div class="callout callout-steps"><div class="callout-title"></div>'
                     f'<ol class="steps">{lis}</ol></div><!-- newsteps:end -->')
            j = section_end(seg, len(seg))
            seg = seg[:j] + block + seg[j:]
        out.append(page[last:b]); out.append(seg); last = stop
    out.append(page[last:])
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
