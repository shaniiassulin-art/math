#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
files_section.py - מוסיף לאתר חלק "קבצי הקורס": הקבצים המקוריים (עמודי PDF כתמונות מדויקות),
כל קובץ תחת הכותרת שכתובה בו, ולפני כל שאלה - פס עם קישורים לסעיפים המתאימים במדריך.

שימוש:  python3 tools/files_section.py algebra-solutions
קורא:   <site>/files/files.json  (רשימת הקבצים, כותרות, ומיפוי שאלה -> סעיפים במדריך)
        <site>/files/<id>.pdf, <site>/files/<id>-p<N>.webp  (עמודים, מוכנים מראש)
המיקום של כל שאלה בעמוד מחושב מה-PDF (pdftotext) ונשמר ב-files.json, כך שאפשר להריץ שוב גם בלי pdftotext.
אפשר להריץ שוב ושוב: החלק מוחלף בין סימונים, בלי כפילויות.
"""
import html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_MARKS = re.compile(r'[‎‏‪-‮]')


def locate(pdf, n_questions):
    """Find where each question starts: [(page, y_pt)], page size, and where content ends on the last page."""
    out = subprocess.run(['pdftotext', '-bbox', pdf, '-'], check=True, capture_output=True, text=True).stdout
    pages = re.findall(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', out, re.S)
    W, H = float(pages[0][0]), float(pages[0][1])
    cands = []  # (page, y, text) of number-like tokens at the right margin, merged per line
    last_y = 0
    for pi, (_, _, body) in enumerate(pages, 1):
        rows = {}
        for x0, y0, x1, y1, t in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', body):
            t = DIR_MARKS.sub('', html.unescape(t)).strip()
            if pi == len(pages):
                last_y = max(last_y, float(y1))
            if float(x1) >= W * 0.925 and re.fullmatch(r'[.\d\s]+', t) and re.search(r'\d', t):
                key = round(float(y0))
                rows.setdefault(key, []).append((float(x0), t))
        for y, toks in sorted(rows.items()):
            digits = re.sub(r'\D', '', ''.join(t for _, t in sorted(toks)))
            if digits:
                cands.append((pi, y, int(digits)))
    starts, want = [], 1
    for p, y, num in cands:
        if num == want:
            starts.append([p, y]); want += 1
    if len(starts) != n_questions:
        raise SystemExit(f'{pdf}: found {len(starts)} questions, expected {n_questions}')
    return {'w': W, 'h': H, 'pages': len(pages), 'starts': starts, 'end': [len(pages), min(H, last_y + 28)]}


def crop_x(site_dir, f, W):
    """Horizontal content bounds (in PDF points) over all pages, from the page images, to drop empty side margins."""
    from PIL import Image, ImageOps
    x0, x1 = None, None
    for p in range(1, f['layout']['pages'] + 1):
        im = Image.open(os.path.join(site_dir, 'files', f'{f["id"]}-p{p}.webp')).convert('L')
        bb = ImageOps.invert(im).point(lambda v: 255 if v > 12 else 0).getbbox()
        if bb:
            k = W / im.width
            x0 = bb[0] * k if x0 is None else min(x0, bb[0] * k)
            x1 = bb[2] * k if x1 is None else max(x1, bb[2] * k)
    return [max(0.0, round(x0 - 10, 1)), min(W, round(x1 + 10, 1))]


def slices(lay):
    """Cut the document into vertical slices: header, then one run per question (split at page breaks)."""
    W, H = lay['w'], lay['h']
    pts = [[1, 0.0]] + [[p, max(0.0, y - 12)] for p, y in lay['starts']] + [lay['end']]
    runs = []  # list of (question_no or 0, [(page, y0, y1), ...])
    for qi in range(len(pts) - 1):
        (p0, y0), (p1, y1) = pts[qi], pts[qi + 1]
        segs = []
        p, y = p0, y0
        while (p, y) < (p1, y1):
            end = y1 if p == p1 else H
            if end - y > 1:
                segs.append((p, y, end))
            p, y = p + 1, 0.0
        runs.append((qi, segs))
    return runs


def build(site, cfg, guide):
    e = html.escape
    titles = {}
    for hid, txt in re.findall(r'<h3 class="q" id="([^"]+)"[^>]*>(.*?)</h3>', guide, re.S):
        titles[hid] = re.sub(r'<[^>]+>', '', txt).strip()
    docs, toc = '', ''
    for f in cfg['files']:
        lay, qmap = f['layout'], cfg['maps'][f['map']]
        W = lay['w']
        cx0, cx1 = lay.get('crop', [0, W])
        cw = cx1 - cx0
        jump = ' '.join(f'<a href="#file-{f["id"]}-q{n}">{n}</a>' for n in range(1, f['questions'] + 1))
        body, seen_pages = '', set()
        for q, segs in slices(lay):
            if q:
                links = ''.join(f'<a href="#{s}">{e(titles.get(s, s))}</a>' for s in qmap.get(str(q), []) if s in titles)
                body += (f'\n        <div class="q-bar" id="file-{f["id"]}-q{q}"><span class="q-num">שאלה {q}</span>'
                         f'<span class="q-lbl">במדריך:</span>{links}</div>')
            for p, y0, y1 in segs:
                first = p not in seen_pages
                seen_pages.add(p)
                alt = f'{e(f["title"])} - עמוד {p}' if first else ''
                cls = 'file-slice page-start' if first and p > 1 else 'file-slice'
                body += (f'\n        <div class="{cls}" style="aspect-ratio:{cw:.1f} / {y1 - y0:.1f}">'
                         f'<img src="files/{f["id"]}-p{p}.webp" alt="{alt}" loading="lazy" decoding="async" '
                         f'style="width:{W / cw * 100:.3f}%;margin-left:-{cx0 / cw * 100:.3f}%;margin-top:-{y0 / cw * 100:.3f}%"></div>')
        docs += f'''
      <div class="file-doc">
        <h3 class="file-title" id="file-{f["id"]}">{e(f["title"])}</h3>
        <div class="file-actions">
          <a class="file-open" href="files/{e(f["pdf"])}" target="_blank" rel="noopener">פתיחת ה-PDF המקורי</a>
          <span class="file-jump"><span>קפיצה לשאלה:</span> {jump}</span>
        </div>
        <div class="file-hint">↔ אפשר לגלול את הקובץ הצידה, או להגדיל בשתי אצבעות.</div>
        <div class="file-scroll"><div class="file-pages">{body}
        </div></div>
      </div>'''
        toc += f'\n            <li><a href="#file-{f["id"]}" data-ex="files">{e(f["title"])}</a></li>'
    section = f'''<!-- files-section:start -->
    <section class="files-section" id="files">
      <div class="ex-header">
        <div class="ex-badge" aria-hidden="true">📄</div>
        <h2 class="files-title">{e(cfg["section_title"])}</h2>
      </div>
      <p class="ex-intro">{e(cfg["section_intro"])}</p>{docs}
    </section>
    <!-- files-section:end -->
'''
    toc_group = f'''<!-- files-toc:start -->
      <li class="toc-group">
        <details class="toc-details" id="details-files">
          <summary><a href="#files" class="top-link" data-ex="files"><span class="num">📄</span><span>{e(cfg["section_title"])}</span></a></summary>
          <ul class="sub-toc">{toc}
          </ul>
        </details>
      </li>
      <!-- files-toc:end -->
'''
    return section, toc_group


CSS = '''<!-- files-css:start -->
<style>
  /* ===== קבצי הקורס ===== */
  .files-section{ margin-top:70px; padding-top:30px; border-top:1px solid var(--line); scroll-margin-top:60px; }
  .files-title{ font-size:1.85rem; margin:0; }
  .file-doc{ margin:30px 0 44px; }
  .file-title{ font-size:1.3rem; margin:0 0 8px; scroll-margin-top:70px; }
  .file-actions{ display:flex; flex-wrap:wrap; align-items:center; gap:8px 16px; margin-bottom:12px; font-size:.92rem; }
  .file-open{ display:inline-flex; align-items:center; min-height:44px; padding:0 16px; border-radius:100px;
    background:var(--indigo-2); color:#fff !important; text-decoration:none; font-weight:700; }
  .file-jump{ display:flex; flex-wrap:wrap; align-items:center; gap:6px; color:var(--ink-soft); }
  .file-jump a{ display:inline-flex; align-items:center; justify-content:center; min-width:36px; min-height:36px;
    border:1px solid var(--line); border-radius:8px; background:var(--paper); text-decoration:none; color:var(--indigo-2); font-weight:600; }
  .file-pages{ background:#fff; border:1px solid var(--line); border-radius:10px; overflow:hidden; max-width:820px; }
  .file-slice{ overflow:hidden; line-height:0; direction:ltr; }
  .file-slice img{ display:block; height:auto; max-width:none; }
  /* בטלפון: הקובץ ברוחב קריא, וגוללים הצידה בתוך הקובץ בלבד */
  .file-scroll{ overflow-x:auto; -webkit-overflow-scrolling:touch; border-radius:10px; }
  @media (max-width:700px){ .file-pages{ width:640px; } .file-hint{ display:block; } }
  .file-hint{ display:none; font-size:.85rem; color:var(--ink-soft); margin:-4px 0 8px; }
  .file-slice.page-start{ border-top:10px solid var(--bg); box-shadow:inset 0 1px 0 var(--line); }
  .q-bar{ display:flex; flex-wrap:wrap; align-items:center; gap:6px 8px; padding:8px 12px; line-height:1.4;
    background:var(--indigo-soft); border-top:1px solid #D5DBEA; border-bottom:1px solid #D5DBEA; font-size:.9rem; scroll-margin-top:70px; }
  .q-bar .q-num{ font-weight:800; color:var(--indigo-2); }
  .q-bar .q-lbl{ color:var(--ink-soft); }
  .q-bar a{ display:inline-flex; align-items:center; min-height:40px; padding:4px 12px; border-radius:100px;
    background:#fff; border:1px solid #C9D1E6; color:var(--indigo-2); text-decoration:none; font-weight:600; }
  .q-bar a:hover{ border-color:var(--gold); }
  @media print{ .file-actions, .q-bar{ display:none; } }
</style>
<!-- files-css:end -->
'''


def replace_between(s, start, end, new, anchor_before):
    if start in s:
        a = s.index(start); b = s.index(end) + len(end)
        while b < len(s) and s[b] == '\n':
            b += 1
        return s[:a] + new + s[b:]
    i = s.index(anchor_before)
    return s[:i] + new + s[i:]


def main(site):
    d = os.path.join(ROOT, site)
    cfg_path = os.path.join(d, 'files', 'files.json')
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    for f in cfg['files']:
        if 'layout' not in f or '--relocate' in sys.argv:
            f['layout'] = locate(os.path.join(d, 'files', f['pdf']), f['questions'])
        if 'crop' not in f['layout'] or '--relocate' in sys.argv:
            f['layout']['crop'] = crop_x(d, f, f['layout']['w'])
    json.dump(cfg, open(cfg_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    path = os.path.join(d, 'index.html')
    page = open(path, encoding='utf-8').read()
    section, toc_group = build(site, cfg, page)
    page = replace_between(page, '<!-- files-css:start -->', '<!-- files-css:end -->', CSS, '</head>')
    page = replace_between(page, '<!-- files-section:start -->', '<!-- files-section:end -->', section, '<footer class="site-footer"')
    page = replace_between(page, '<!-- files-toc:start -->', '<!-- files-toc:end -->', toc_group, '</ul>\n    <div class="toc-note">')
    open(path, 'w', encoding='utf-8').write(page)
    print('files section updated:', site, [(f['id'], len(f['layout']['starts'])) for f in cfg['files']])


if __name__ == '__main__':
    main(sys.argv[1])
