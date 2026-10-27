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


def _lines(pdf):
    out = subprocess.run(['pdftotext', '-bbox-layout', pdf, '-'], check=True, capture_output=True, text=True).stdout
    pages = []
    for pm in re.finditer(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', out, re.S):
        L = []
        for lm in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', pm.group(3), re.S):
            words = [(float(a), float(b), float(c), float(d), DIR_MARKS.sub('', html.unescape(t)).strip())
                     for a, b, c, d, t in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', lm.group(5))]
            words = [w for w in words if w[4]]
            if words:
                L.append((float(lm.group(2)), float(lm.group(4)), words))
        pages.append((float(pm.group(1)), float(pm.group(2)), L))
    return pages


def locate(pdf, expected=None):
    """Where each question starts, per part ('main', and 'extra' after a 'תרגול נוסף' heading if there is one).
    Question numbers are the number at the right end of a line (RTL), merged when split into digits."""
    pages = _lines(pdf)
    W, H = pages[0][0], pages[0][1]
    split, cands, last_y = None, [], 0.0
    for pi, (w, h, L) in enumerate(pages, 1):
        right = max(max(q[2] for q in ws) for _, _, ws in L) if L else w
        for y0, y1, words in L:
            if pi == len(pages):
                last_y = max(last_y, y1)
            flat = ''.join(q[4] for q in words)  # pdftotext gives Hebrew words visually reversed
            if split is None and 'ףסונ' in flat and 'לוגר' in flat and len(flat) < 40 and 'ללוכ' not in flat:
                split = (pi, y0)
            edge = [q for q in words if q[2] >= right - 30]
            ds = [q for q in edge if re.fullmatch(r'[.\d]+', q[4])]
            if ds and max(q[2] for q in ds) >= right - 30:
                digits = ''.join(re.sub(r'\D', '', q[4]) for q in sorted(ds, key=lambda q: q[0]))
                if digits and len(digits) <= 2:
                    cands.append((pi, y0, int(digits)))
            else:
                rw = max(words, key=lambda q: q[2])
                m = re.match(r'^\.?(\d{1,2})\.?(?![\d,])', rw[4])
                if m and rw[2] >= right - 30:
                    cands.append((pi, y0, int(m.group(1))))
    parts = {}
    for name in ('main', 'extra'):
        if name == 'extra' and split is None:
            continue
        want, starts = 1, []
        for p, y, n in cands:
            inside = (split is None or (p, y) < split) if name == 'main' else (p, y) > split
            if inside and n == want:
                starts.append([p, round(y)]); want += 1
        parts[name] = starts
    if expected and len(parts.get('main', [])) != expected:
        raise SystemExit(f'{pdf}: found {len(parts.get("main", []))} questions, expected {expected}')
    return {'w': W, 'h': H, 'pages': len(pages), 'parts': parts,
            'split': [split[0], round(split[1])] if split else None, 'end': [len(pages), min(H, last_y + 28)]}


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


def cut_points(site_dir, f):
    """Where to cut above each question: normally 12pt above its number, but if a grey heading band
    (the topic title of the question) sits right above it, cut above that band so it stays with its question."""
    from PIL import Image
    lay = f['layout']
    W = lay['w']
    cx0, cx1 = lay.get('crop', [0, W])
    imgs = {}

    def img(p):
        if p not in imgs:
            imgs[p] = Image.open(os.path.join(site_dir, 'files', f'{f["id"]}-p{p}.webp')).convert('RGB')
        return imgs[p]

    others = [(p, y) for st in parts_of(lay).values() for p, y in st]

    def cut(p, y):
        im = img(p)
        k = im.width / W
        xa, xb = int(cx0 * k), int(cx1 * k)
        default = max(0.0, y - 12)
        zones = [(oy - 4, oy + 14) for op, oy in others if op == p and oy < y - 1]   # other questions' number lines
        band_top = None
        r = int((y - 2) * k)
        stop = max(0, int((y - 60) * k))
        while r > stop:
            ypt = r / k
            if any(z0 <= ypt <= z1 for z0, z1 in zones):
                break                                  # never cross into the previous question
            row = im.crop((xa, r, xb, r + 1)).tobytes()
            trip = [row[i:i + 3] for i in range(0, len(row), 3)]
            n = len(trip)
            # neutral grey only (a heading band or question box) - coloured highlights (yellow, cyan) are not bands
            grey = sum(1 for R, G, B in trip if 175 <= R <= 248 and abs(R - G) < 8 and abs(G - B) < 8) / n
            dark = sum(1 for R, G, B in trip if R + G + B < 420) / n
            if grey > 0.45:
                band_top = r                           # grey heading band (topic title)
            elif dark > 0.002 and band_top is not None:
                break                                  # content above the band belongs to the previous question
            r -= 1
        if band_top is None:
            return default
        return max(0.0, min(default, band_top / k - 4))

    cuts = {part: [[p, round(cut(p, y), 1)] for p, y in starts] for part, starts in parts_of(lay).items()}
    split = [lay['split'][0], round(cut(*lay['split']), 1)] if lay.get('split') else None
    return cuts, split


def heading_bands(site_dir, f, after):
    """Grey heading bands (topic titles) from (page, y) on, as [(page, top_pt)]."""
    from PIL import Image
    lay = f['layout']
    W = lay['w']
    cx0, cx1 = lay.get('crop', [0, W])
    out = []
    for p in range(after[0], lay['pages'] + 1):
        im = Image.open(os.path.join(site_dir, 'files', f'{f["id"]}-p{p}.webp')).convert('L')
        k = im.width / W
        xa, xb = int(cx0 * k), int(cx1 * k)
        run = None
        for r in range(im.height + 1):
            g = 0.0
            if r < im.height and not (p == after[0] and r / k < after[1] - 2):
                row = im.crop((xa, r, xb, r + 1)).tobytes()
                g = sum(1 for v in row if 200 <= v <= 248) / len(row)
            if g > 0.45:
                run = r if run is None else run
            else:
                if run is not None and (r - run) / k > 6:
                    out.append([p, round(run / k, 1)])
                run = None
    return out


def extra_by_bands(site_dir, f, cfg):
    """A solution file whose extra-practice part is arranged by topic headings instead of question numbers:
    if the number of grey heading bands after the split equals the number of extra questions in the
    questions file, each band starts the next question."""
    lay = f['layout']
    if not f['id'].endswith('-solution') or not lay.get('split'):
        return False
    ref = next((g for g in cfg['files'] if g['id'] == f['id'][:-len('-solution')]), None)
    if not ref:
        return False
    want = len(parts_of(ref['layout']).get('extra', []))
    have = len(parts_of(lay).get('extra', []))
    if not want or have == want:
        return False
    bands = heading_bands(site_dir, f, lay['split'])
    if len(bands) != want:
        return False
    lay['parts']['extra'] = [[p, round(y + 12)] for p, y in bands]
    lay['cuts']['extra'] = [[p, max(0.0, round(y - 2, 1))] for p, y in bands]
    if lay.get('split_cut'):
        lay['cuts']['extra'][0] = list(lay['split_cut'])
    lay['extra_by_bands'] = True
    return True


def grey_boxes(site_dir, f, min_h=14):
    """Tops of the grey question boxes (neutral grey fill, not coloured highlights) over the whole file: [(page, top_pt)]."""
    from PIL import Image
    lay = f['layout']
    W = lay['w']
    cx0, cx1 = lay.get('crop', [0, W])
    out = []
    for p in range(1, lay['pages'] + 1):
        im = Image.open(os.path.join(site_dir, 'files', f'{f["id"]}-p{p}.webp')).convert('RGB')
        k = im.width / W
        xa, xb = int(cx0 * k), int(cx1 * k)
        run = None
        for r in range(im.height + 1):
            frac = 0.0
            if r < im.height:
                px = im.crop((xa, r, xb, r + 1)).tobytes()
                trip = [px[i:i + 3] for i in range(0, len(px), 3)]
                frac = sum(1 for R, G, B in trip if 175 <= R <= 248 and abs(R - G) < 8 and abs(G - B) < 8) / len(trip)
            if frac > 0.6:
                run = r if run is None else run
            else:
                if run is not None and (r - run) / k >= min_h:
                    top, bottom = round(run / k, 1), round(r / k, 1)
                    if out and out[-1][0] == p and top - out[-1][2] < 22:
                        out[-1][2] = bottom          # same box, interrupted by a dark line of content
                    else:
                        out.append([p, top, bottom])
                run = None
    return [[p, t] for p, t, _ in out]


def check_with_boxes(site_dir, f):
    """Solution files put every question inside a grey box. If there is exactly one box per question and the
    numbers found in the text disagree with the boxes, trust the boxes."""
    lay = f['layout']
    main = parts_of(lay).get('main', [])
    if lay.get('split') or not f['id'].endswith('-solution') or not main:
        return False
    boxes = grey_boxes(site_dir, f)
    if len(boxes) != len(main):
        return False
    off = [b for b, q in zip(boxes, main) if b[0] != q[0] or abs(b[1] + 12 - q[1]) > 25]
    if not off:
        return False
    lay['parts'] = {'main': [[p, round(y + 12)] for p, y in boxes]}
    lay['cuts'] = {'main': [[p, max(0.0, round(y - 3, 1))] for p, y in boxes]}
    lay['by_boxes'] = True
    return True


def parts_of(lay):
    """{'main': [[p,y],...], 'extra': [...]} - also reads the older one-part layout ('starts')."""
    return lay.get('parts') or {'main': lay.get('starts', [])}


def slices(lay):
    """Cut the document into vertical runs: header, then one run per question (and one at the 'תרגול נוסף'
    heading), each run split at page breaks. Returns [(label, [(page, y0, y1), ...])], label = (part, n) or None."""
    H = lay['h']
    marks = [(1, 0.0, None)]
    cuts = lay.get('cuts')
    for part, starts in parts_of(lay).items():
        if cuts:
            marks += [(p, y, (part, i)) for i, (p, y) in enumerate(cuts[part], 1)]
        else:
            marks += [(p, max(0.0, y - 12), (part, i)) for i, (p, y) in enumerate(starts, 1)]
    if lay.get('split'):
        sp = lay.get('split_cut') or [lay['split'][0], max(0.0, lay['split'][1] - 12)]
        marks.append((sp[0], sp[1], None))
    marks.sort(key=lambda m: (m[0], m[1]))
    marks.append((lay['end'][0], lay['end'][1], None))
    runs = []
    for (p0, y0, label), (p1, y1, _) in zip(marks, marks[1:]):
        segs, p, y = [], p0, y0
        while (p, y) < (p1, y1):
            end = y1 if p == p1 else H
            if end - y > 1:
                segs.append((p, y, end))
            p, y = p + 1, 0.0
        runs.append((label, segs))
    return runs


PART_NAMES = {'main': 'שאלה', 'extra': 'תרגול נוסף · שאלה'}
PART_JUMP = {'main': 'קפיצה לשאלה:', 'extra': 'תרגול נוסף:'}


def linked_parts(f, cfg):
    """Parts of this file that get a link bar per question: the file has a map, and (for a solution file)
    its numbering matches the questions file of the same map."""
    if not f.get('map') or f['map'] not in cfg['maps']:
        return set()
    mine = parts_of(f['layout'])
    ref = next((g for g in cfg['files'] if g.get('map') == f['map'] and g is not f and not g['id'].endswith('-solution')), None)
    out = set()
    for part, starts in mine.items():
        if part not in cfg['maps'][f['map']]:
            continue
        if ref is None or f is ref or len(parts_of(ref['layout']).get(part, [])) == len(starts):
            out.add(part)
    return out


TYPE_LABELS = {'q': 'שאלות', 's': 'פתרונות', 'p': 'מצגות'}


def file_type(f):
    if f.get('kind') == 'slides':
        return 'p'
    return 's' if f['id'].endswith('-solution') else 'q'


def short_label(f):
    if f.get('short'):
        return f['short']
    m = re.search(r'(פתרון )?תרגיל (כיתה|בית) \d+', f['title'])
    if m:
        return m.group(0)
    return f['title'].split(' - ')[0].strip()


def render_doc(f):
    """The whole file, open: every page as an exact image (A4 pages cropped to the content width), no links."""
    e = html.escape
    if f.get('kind') == 'slides':
        body = ''.join(f'\n          <div class="slide"><img src="files/{f["id"]}-p{p}.webp" alt="{e(f["title"])} - שקף {p}" '
                       f'loading="lazy" decoding="async" width="1000" height="750"></div>' for p in range(1, f['pages'] + 1))
        pages = f'<div class="file-pages slides">{body}\n        </div>'
        hint = ''
    else:
        lay = f['layout']
        W, H = lay['w'], lay['h']
        cx0, cx1 = lay.get('crop', [0, W])
        cw = cx1 - cx0
        body = ''
        for p in range(1, lay['pages'] + 1):
            y1 = lay['end'][1] if p == lay['pages'] else H
            cls = 'file-slice page-start' if p > 1 else 'file-slice'
            body += (f'\n          <div class="{cls}" style="aspect-ratio:{cw:.1f} / {y1:.1f}">'
                     f'<img src="files/{f["id"]}-p{p}.webp" alt="{e(f["title"])} - עמוד {p}" loading="lazy" decoding="async" '
                     f'style="width:{W / cw * 100:.3f}%;margin-left:-{cx0 / cw * 100:.3f}%"></div>')
        pages = f'<div class="file-scroll"><div class="file-pages">{body}\n        </div></div>'
        hint = '\n        <div class="file-hint">↔ אפשר לגלול את הקובץ הצידה, או להגדיל בשתי אצבעות.</div>'
    return f'''
      <div class="file-doc" id="file-{f["id"]}" data-type="{file_type(f)}">
        <h3 class="file-title">{e(f["title"])}</h3>
        <div class="file-actions">
          <a class="file-open" href="files/{e(f["pdf"])}" target="_blank" rel="noopener">פתיחת ה-PDF המקורי</a>
        </div>{hint}
        {pages}
      </div>'''


def build(site, cfg, guide):
    """Files section: choose the type (questions / solutions / presentations), then the file; one file is shown at a time."""
    e = html.escape
    types = []
    for f in cfg['files']:
        t = file_type(f)
        if t not in types:
            types.append(t)
    type_btns = ''.join(f'<button type="button" class="ff-type" data-type="{t}" aria-pressed="false">{TYPE_LABELS[t]}</button>'
                        for t in types)
    groups = ''
    for t in types:
        chips = ''.join(f'<button type="button" class="ff-file" data-file="{e(f["id"])}" aria-pressed="false">{e(short_label(f))}</button>'
                        for f in cfg['files'] if file_type(f) == t)
        groups += f'\n          <div class="ff-group" data-type="{t}">{chips}</div>'
    docs = ''.join(render_doc(f) for f in cfg['files'])
    section = f'''<!-- files-section:start -->
    <section class="files-section" id="files">
      <div class="ex-header">
        <div class="ex-badge" aria-hidden="true">📄</div>
        <h2 class="files-title">{e(cfg["section_title"])}</h2>
      </div>
      <p class="ex-intro">{e(cfg["section_intro"])}</p>
      <div class="files-filter" id="filesFilter" hidden>
        <div class="ff-types{' single' if len(types) == 1 else ''}" role="group" aria-label="סוג הקובץ">{type_btns}</div>
        <div class="ff-files" role="group" aria-label="בחירת קובץ">{groups}
        </div>
      </div>{docs}
      <script>
      (function(){{
        try {{
          var box = document.getElementById('filesFilter'); if(!box) return;
          var KEY = 'filesView_' + location.pathname;
          var docs = [].slice.call(document.querySelectorAll('.files-section .file-doc'));
          var types = [].slice.call(box.querySelectorAll('.ff-type'));
          var state = {{}};
          try {{ state = JSON.parse(localStorage.getItem(KEY) || '{{}}') || {{}}; }} catch(e){{ state = {{}}; }}
          function firstOf(t){{ var d = docs.filter(function(x){{ return x.dataset.type === t; }})[0]; return d ? d.id.slice(5) : null; }}
          function show(t, id){{
            if(!t) t = types[0].dataset.type;
            if(!id || !document.getElementById('file-' + id) || document.getElementById('file-' + id).dataset.type !== t) id = (state.files || {{}})[t] || firstOf(t);
            if(!document.getElementById('file-' + id)) id = firstOf(t);
            state.type = t; state.files = state.files || {{}}; state.files[t] = id;
            types.forEach(function(b){{ b.setAttribute('aria-pressed', String(b.dataset.type === t)); }});
            [].forEach.call(box.querySelectorAll('.ff-group'), function(g){{ g.hidden = g.dataset.type !== t; }});
            [].forEach.call(box.querySelectorAll('.ff-file'), function(b){{ b.setAttribute('aria-pressed', String(b.dataset.file === id)); }});
            docs.forEach(function(d){{ d.hidden = d.id !== 'file-' + id; }});
            try {{ localStorage.setItem(KEY, JSON.stringify(state)); }} catch(e){{}}
          }}
          types.forEach(function(b){{ b.addEventListener('click', function(){{ show(b.dataset.type); }}); }});
          [].forEach.call(box.querySelectorAll('.ff-file'), function(b){{
            b.addEventListener('click', function(){{ show(b.closest('.ff-group').dataset.type, b.dataset.file); }});
          }});
          box.hidden = false;
          show(state.type, state.type && state.files ? state.files[state.type] : null);
        }} catch(err){{}}
      }})();
      </script>
    </section>
    <!-- files-section:end -->
'''
    toc_group = f'''<!-- files-toc:start -->
      <li><a href="#files"><span class="num">📄</span><span>{e(cfg["section_title"])}</span></a></li>
      <!-- files-toc:end -->
'''
    return section, toc_group


CSS = '''<!-- files-css:start -->
<style>
  /* ===== קבצי הקורס ===== */
  .files-section{ margin-top:70px; padding-top:30px; border-top:1px solid var(--line); scroll-margin-top:60px; }
  .files-title{ font-size:1.85rem; margin:0; }
  .file-doc{ margin:22px 0 44px; }
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
  .file-hint{ display:none; font-size:.85rem; color:var(--ink-soft); margin:-4px 0 8px; }
  @media (max-width:700px){ .file-pages{ width:640px; } .file-hint{ display:block; } }
  .file-note{ font-size:.92rem; color:var(--ink-soft); background:var(--gold-soft); border-radius:8px; padding:8px 12px; max-width:72ch; }
  .file-slice.page-start{ border-top:10px solid var(--bg); box-shadow:inset 0 1px 0 var(--line); }
  .q-bar{ display:flex; flex-wrap:wrap; align-items:center; gap:6px 8px; padding:8px 12px; line-height:1.4;
    background:var(--indigo-soft); border-top:1px solid #D5DBEA; border-bottom:1px solid #D5DBEA; font-size:.9rem; scroll-margin-top:70px; }
  .q-bar .q-num{ font-weight:800; color:var(--indigo-2); }
  .q-bar .q-lbl{ color:var(--ink-soft); }
  .q-bar a{ display:inline-flex; align-items:center; min-height:40px; padding:4px 12px; border-radius:100px;
    background:#fff; border:1px solid #C9D1E6; color:var(--indigo-2); text-decoration:none; font-weight:600; }
  .q-bar a:hover{ border-color:var(--gold); }
  .file-pages.slides{ background:var(--bg); border:none; }
  .slide{ margin:0 0 10px; border:1px solid var(--line); border-radius:8px; overflow:hidden; background:#fff; line-height:0; }
  .slide img{ display:block; width:100%; height:auto; }
  .file-pages.slides .q-bar{ border:1px solid #D5DBEA; border-radius:10px; margin:22px 0 10px; }
  .file-jump.topics a{ min-width:0; padding:4px 10px; }
  @media (max-width:700px){ .file-pages.slides{ width:auto; } }
  /* בחירת קובץ: סוג ואז קובץ */
  .files-filter{ margin:18px 0 6px; display:grid; gap:10px; }
  .ff-types{ display:flex; flex-wrap:wrap; gap:8px; }
  .ff-types.single{ display:none; }
  .ff-type{ min-height:44px; padding:0 22px; border-radius:100px; border:1.5px solid var(--indigo-2); background:var(--paper);
    color:var(--indigo-2); font-family:'Assistant',sans-serif; font-weight:700; font-size:1rem; cursor:pointer; }
  .ff-type[aria-pressed="true"]{ background:var(--indigo-2); color:#fff; }
  .ff-group{ display:flex; flex-wrap:wrap; gap:8px; }
  .ff-file{ min-height:44px; padding:0 16px; border-radius:10px; border:1px solid var(--line); background:var(--paper);
    color:var(--ink); font-family:'Assistant',sans-serif; font-size:.95rem; font-weight:600; cursor:pointer; }
  .ff-file[aria-pressed="true"]{ border-color:var(--gold); background:var(--gold-soft); color:var(--gold-text); box-shadow:inset 0 0 0 1px var(--gold); }
  .file-doc[hidden], .ff-group[hidden]{ display:none !important; }
  @media print{ .file-actions, .files-filter{ display:none; } }
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
        if f.get('kind') == 'slides':
            continue
        if 'layout' not in f or '--relocate' in sys.argv:
            f['layout'] = locate(os.path.join(d, 'files', f['pdf']), f.get('questions'))
        if 'crop' not in f['layout'] or '--relocate' in sys.argv:
            f['layout']['crop'] = crop_x(d, f, f['layout']['w'])
        if 'cuts' not in f['layout'] or '--relocate' in sys.argv:
            f['layout']['cuts'], f['layout']['split_cut'] = cut_points(d, f)
    for f in cfg['files']:
        if f.get('kind') == 'slides':
            continue
        if not f['layout'].get('extra_by_bands') or '--relocate' in sys.argv:
            extra_by_bands(d, f, cfg)
        if not f['layout'].get('by_boxes') and not f['layout'].get('boxes_checked') or '--relocate' in sys.argv:
            if check_with_boxes(d, f):
                print(f"  {f['id']}: question positions taken from the grey boxes")
            f['layout']['boxes_checked'] = True
    json.dump(cfg, open(cfg_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    path = os.path.join(d, 'index.html')
    page = open(path, encoding='utf-8').read()
    section, toc_group = build(site, cfg, page)
    page = replace_between(page, '<!-- files-css:start -->', '<!-- files-css:end -->', CSS, '</head>')
    page = replace_between(page, '<!-- files-section:start -->', '<!-- files-section:end -->', section, '<footer class="site-footer"')
    page = replace_between(page, '<!-- files-toc:start -->', '<!-- files-toc:end -->', toc_group, '</ul>\n    <div class="toc-note">')
    open(path, 'w', encoding='utf-8').write(page)
    print('files section updated:', site)
    for f in cfg['files']:
        if f.get('kind') == 'slides':
            print(f"  {f['id']:20} slides={f['pages']}, topics={len(f['topics'])}")
            continue
        print(f"  {f['id']:20} " + ', '.join(f"{k}={len(v)}" for k, v in parts_of(f['layout']).items()) + f"  links: {sorted(linked_parts(f, cfg)) or '-'}")


if __name__ == '__main__':
    main(sys.argv[1])
