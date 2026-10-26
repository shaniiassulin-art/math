#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_hub.py - בונה את דף הבית (index.html) של אתר המתמטיקה מתוך sites.json
ומתוך האתרים שבתיקיות (<slug>/index.html): שם, יחידות, מספר נושאים ותאריך עדכון.

בנוסף, מוודא שכל האתרים משתמשים באותו מפתח Google לחיפוש החכם (שם אחד בדפדפן),
כך שמכניסים את המפתח פעם אחת - בדף הבית או באחד האתרים - והוא עובד בכולם.

האתרים בתיקיות הם עותקים עצמאיים - עורכים אותם ישירות כאן, במאגר math.
Netlify מריץ את הסקריפט הזה בכל פרסום, כך שדף הבית תמיד מעודכן.
שימוש:  python3 build_hub.py
"""
import html, json, os, re, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
SHARED_KEY = 'mathGeminiKey_v1'

ICON_INNER = ('<rect width="64" height="64" rx="14" fill="#2C3A5E"/>'
              '<path d="M14 23.5C18 19 24 19.5 32 19.5S45 19 50.5 18" fill="none" stroke="#E3B95C" stroke-width="5" stroke-linecap="round"/>'
              '<path d="M26 20.5C26.5 31 25 40 19 47" fill="none" stroke="#E3B95C" stroke-width="5" stroke-linecap="round"/>'
              '<path d="M39.5 20C38.5 31 38.5 41 47 46" fill="none" stroke="#E3B95C" stroke-width="5" stroke-linecap="round"/>')
FAVICON = ('data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E'
           + ICON_INNER.replace('#2C3A5E', '#1F2A47').replace('"', '%22').replace('<', '%3C').replace('>', '%3E').replace('#', '%23')
           + '%3C/svg%3E')


def run(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def last_change(folder):
    try:
        return run('git', 'log', '-1', '--format=%cI', '--', folder, cwd=ROOT)
    except Exception:
        return ''


def share_key(page):
    """Every site stores the Google key under one shared name. Returns (page, old names found)."""
    old = re.findall(r"KEY_STORE\s*=\s*'(\w+)'", page)
    page = re.sub(r"(KEY_STORE\s*=\s*)'\w+'", r"\1'" + SHARED_KEY + "'", page)
    return page, [o for o in old if o != SHARED_KEY]


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
    sources = ''.join(f'<li>{e(x)}</li>' for x in s.get('sources', []))
    src_box = ''
    if s.get('sources_summary') or sources:
        src_box = (f'<span class="site-sources"><b>{e(s.get("sources_summary", "מבוסס על"))}:</b>'
                   + (f'<ul>{sources}</ul>' if sources else '') + '</span>')
    meta = []
    n = len(s['units'])
    if n:
        meta.append('יחידה אחת' if n == 1 else f'{n} יחידות')
    if s['topics']:
        meta.append('נושא אחד' if s['topics'] == 1 else f'{s["topics"]} נושאים')
    if s['date']:
        meta.append('עודכן ' + hebrew_date(s['date']))
    return f'''
      <a class="site-card {e(s.get('group', ''))}" href="{e(s['slug'])}/">
        <span class="site-kind">{e(s.get('kind', ''))}</span>
        <span class="site-name">{e(s['name'])}</span>
        <span class="site-desc">{e(s['description'])}</span>
        {src_box}
        <span class="site-meta">{' · '.join(meta)}</span>
        <span class="site-go">פתיחה <span aria-hidden="true">←</span></span>
      </a>'''


def hub(cfg, sites, old_keys):
    e = html.escape
    groups = ''
    for g in cfg['groups']:
        cards = ''.join(card(s) for s in sites if s.get('group') == g['id'])
        if not cards:
            continue
        groups += f'''
    <section class="group">
      <h2>{e(g['title'])}</h2>
      <div class="cards">{cards}
      </div>
    </section>
'''
    tpl = open(os.path.join(ROOT, 'hub_template.html'), encoding='utf-8').read()
    apple = open(os.path.join(ROOT, 'apple-touch-icon.png.b64'), encoding='utf-8').read().strip()
    return (tpl.replace('{{TITLE}}', e(cfg['hub_title']))
               .replace('{{SUBTITLE}}', e(cfg['hub_subtitle']))
               .replace('{{GROUPS}}', groups)
               .replace('{{ICON_INNER}}', ICON_INNER)
               .replace('{{FAVICON}}', FAVICON)
               .replace('{{APPLE_ICON}}', 'data:image/png;base64,' + apple)
               .replace('{{KEY_NAME}}', SHARED_KEY)
               .replace('{{OLD_KEYS}}', json.dumps(sorted(set(old_keys)))))


def main():
    cfg = json.load(open(os.path.join(ROOT, 'sites.json'), encoding='utf-8'))
    out, old_keys = [], list(cfg.get('old_key_names', []))
    for s in cfg['sites']:
        path = os.path.join(ROOT, s['slug'], 'index.html')
        page, old = share_key(open(path, encoding='utf-8').read())
        old_keys += old
        if write_if_changed(path, page):
            print(f"  מפתח משותף הוגדר באתר {s['slug']}")
        title, units, topics = info(page)
        out.append(dict(s, title=title, units=units, topics=topics, date=last_change(s['slug'])))
        print(f"✓ {s['slug']:20} {title}  ({len(units)} יחידות, {topics} נושאים)")
    changed = write_if_changed(os.path.join(ROOT, 'index.html'), hub(cfg, out, old_keys))
    print('דף הבית', 'עודכן' if changed else 'ללא שינוי')


if __name__ == '__main__':
    main()
