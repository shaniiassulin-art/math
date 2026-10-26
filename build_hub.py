#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_hub.py - בונה את דף הבית (index.html) של אתר המתמטיקה מתוך sites.json
ומתוך האתרים שבתיקיות (<slug>/index.html): שם, יחידות, מספר נושאים ותאריך עדכון.

האתרים בתיקיות הם עותקים עצמאיים - עורכים אותם ישירות כאן, במאגר math.
Netlify מריץ את הסקריפט הזה בכל פרסום, כך שדף הבית תמיד מעודכן.
שימוש:  python3 build_hub.py
"""
import html, json, os, re, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))


def run(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def last_change(folder):
    try:
        return run('git', 'log', '-1', '--format=%cI', '--', folder, cwd=ROOT)
    except Exception:
        return ''


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
    cfg = json.load(open(os.path.join(ROOT, 'sites.json'), encoding='utf-8'))
    out = []
    for s in cfg['sites']:
        page = open(os.path.join(ROOT, s['slug'], 'index.html'), encoding='utf-8').read()
        title, units, topics = info(page)
        out.append(dict(s, title=title, units=units, topics=topics, date=last_change(s['slug'])))
        print(f"✓ {s['slug']:20} {title}  ({len(units)} יחידות, {topics} נושאים)")
    changed = write_if_changed(os.path.join(ROOT, 'index.html'), hub(cfg, out))
    print('דף הבית', 'עודכן' if changed else 'ללא שינוי')


if __name__ == '__main__':
    main()
