#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync.py - בונה את אתר המתמטיקה המאגד.

לכל אתר שב-sites.json:
  1. מוריד את הגרסה העדכנית של index.html מהמאגר שלו בגיטהאב.
  2. מכניס לעותק שני שינויים קטנים בלבד:
     א. פס עליון "כל אתרי המתמטיקה" שמחזיר לדף הבית (לא צף, לא מסתיר טקסט).
     ב. שם נפרד לזיכרון מיקום הגלילה, כדי שהאתרים לא ידרסו זה את זה.
  3. שומר אותו ב-<slug>/index.html.
ואז בונה את דף הבית index.html מתוך sites.json.

המאגרים המקוריים לא משתנים. אפשר להריץ שוב ושוב - קובץ נכתב רק אם התוכן השתנה.
שימוש:  python3 sync.py            (מוריד מגיטהאב)
        python3 sync.py --src DIR  (לוקח מ-DIR/<שם המאגר>/ במקום להוריד, לבדיקות)
"""
import html, json, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))


def run(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def fetch(repo, src_dir, tmp):
    name = repo.split('/')[-1]
    if src_dir:
        d = os.path.join(src_dir, name)
    else:
        d = os.path.join(tmp, name)
        run('git', 'clone', '-q', '--depth', '1', f'https://github.com/{repo}.git', d)
    page = open(os.path.join(d, 'index.html'), encoding='utf-8').read()
    try:
        date = run('git', 'log', '-1', '--format=%cI', cwd=d)
    except Exception:
        date = ''
    return page, date


BACK_BAR = ('<div class="hub-back-bar" style="background:#1F2A47;padding:0 16px;font-family:\'Assistant\',system-ui,sans-serif;">'
            '<a href="../" style="display:inline-flex;align-items:center;gap:8px;min-height:44px;color:#F5F0E1;'
            'text-decoration:none;font-size:.95rem;font-weight:600;">'
            '<span aria-hidden="true" style="color:#E3B95C;">⌂</span> כל אתרי המתמטיקה</a></div>\n')


def patch(page, slug):
    # א. פס חזרה לדף הבית, מיד אחרי <body>
    m = re.search(r'<body[^>]*>', page)
    if not m:
        raise SystemExit('no <body> in page for ' + slug)
    page = page[:m.end()] + '\n' + BACK_BAR + page[m.end():]
    # ב. זיכרון גלילה נפרד לכל אתר (מפתחות שמסתיימים ב-ScrollY_vN)
    page = re.sub(r"'(\w*ScrollY_v\d+)'", lambda g: "'" + g.group(1) + '_' + slug + "'", page)
    return page


def info(page):
    title = re.search(r'<title>(.*?)</title>', page, re.S)
    units = [re.sub(r'<[^>]+>', '', u).strip() for u in re.findall(r'<h2 class="ex-title"[^>]*>(.*?)</h2>', page, re.S)]
    topics = len(re.findall(r'<h3 class="q"', page))
    return (html.unescape(title.group(1).strip()) if title else ''), units, topics


def write_if_changed(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and open(path, encoding='utf-8').read() == text:
        return False
    open(path, 'w', encoding='utf-8').write(text)
    return True


def hebrew_date(iso):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', iso or '')
    return f'{int(m.group(3))}.{int(m.group(2))}.{m.group(1)}' if m else ''


def card(s):
    e = html.escape
    units = s['units']
    shown = units[:5]
    more = len(units) - len(shown)
    unit_items = ''.join(f'<li>{e(u)}</li>' for u in shown)
    if more > 0:
        unit_items += f'<li class="more">ועוד {more}</li>'
    meta = []
    if units:
        meta.append('יחידה אחת' if len(units) == 1 else f'{len(units)} יחידות')
    if s['topics']:
        meta.append('נושא אחד' if s['topics'] == 1 else f'{s["topics"]} נושאים')
    if s['date']:
        meta.append('עודכן ' + hebrew_date(s['date']))
    return f'''
      <a class="site-card" href="{e(s['slug'])}/">
        <span class="site-name">{e(s['name'])}</span>
        <span class="site-desc">{e(s['description'])}</span>
        {'<ul class="site-units">' + unit_items + '</ul>' if unit_items else ''}
        <span class="site-meta">{' · '.join(meta)}</span>
        <span class="site-go">פתיחה <span aria-hidden="true">←</span></span>
      </a>'''


def hub(cfg, sites):
    e = html.escape
    courses = []
    for s in sites:
        if s['course'] not in courses:
            courses.append(s['course'])
    groups = ''
    for c in courses:
        cards = ''.join(card(s) for s in sites if s['course'] == c)
        groups += f'''
    <section class="course">
      <h2>{e(c)}</h2>
      <div class="cards">{cards}
      </div>
    </section>
'''
    tpl = open(os.path.join(ROOT, 'hub_template.html'), encoding='utf-8').read()
    return (tpl.replace('{{TITLE}}', e(cfg['hub_title']))
               .replace('{{SUBTITLE}}', e(cfg['hub_subtitle']))
               .replace('{{GROUPS}}', groups))


def main():
    src_dir = None
    if '--src' in sys.argv:
        src_dir = sys.argv[sys.argv.index('--src') + 1]
    cfg = json.load(open(os.path.join(ROOT, 'sites.json'), encoding='utf-8'))
    out = []
    changed = []
    with tempfile.TemporaryDirectory() as tmp:
        for s in cfg['sites']:
            page, date = fetch(s['repo'], src_dir, tmp)
            title, units, topics = info(page)
            if write_if_changed(os.path.join(ROOT, s['slug'], 'index.html'), patch(page, s['slug'])):
                changed.append(s['slug'])
            out.append(dict(s, title=title, units=units, topics=topics, date=date))
            print(f"✓ {s['slug']:20} {title}  ({len(units)} יחידות, {topics} נושאים)")
    if write_if_changed(os.path.join(ROOT, 'index.html'), hub(cfg, out)):
        changed.append('index.html')
    print('שונו:', ', '.join(changed) if changed else 'כלום')


if __name__ == '__main__':
    main()
