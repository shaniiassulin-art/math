# -*- coding: utf-8 -*-
"""Adds explanation units (built from tools/units/<site>.py) to a site page, between markers.
   Run before tools/samples.py:  python3 tools/units.py"""
import html, importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import reminders as R

_d = importlib.util.spec_from_file_location('diagrams_u', os.path.join(HERE, 'samples', 'diagrams.py'))
DIA = importlib.util.module_from_spec(_d); _d.loader.exec_module(DIA)

_s = importlib.util.spec_from_file_location('samples_u', os.path.join(HERE, 'samples.py'))
S = importlib.util.module_from_spec(_s); _s.loader.exec_module(S)

SITES = {'calculus-1': ['calculus_12', 'calculus_34']}


def step_li(st):
    """a step: text, or dict(t=text, more=[explanation lines in the visual formats])"""
    if isinstance(st, str):
        return f'        <li>{mathify(st)}</li>\n'
    more = S.render_lines(st.get('more', []))
    more = more.replace('</div><!--/flow--><div class="flow">', '<div class="fl-arr">↓</div>')
    return f'        <li>{mathify(st["t"])}<div class="step-more">{more}</div></li>\n'


def thm_box(title, ls):
    return (f'      <div class="box box-thm"><div class="box-title">{mathify(title)}</div>'
            + S.render_lines(ls) + '</div>\n')


def mathify(s):
    return re.sub(r'\$(.+?)\$', lambda g: R.mwrap(g.group(1)), s)


def disp(latex):
    return '<div class="formula">' + R.mwrap(latex, True) + '</div>'


def lines(ls):
    out = ''
    for x in ls:
        x = x.strip()
        if x.startswith('$$') and x.endswith('$$'):
            out += disp(x[2:-2])
        else:
            out += f'<p>{mathify(x)}</p>'
    return out


def section(n, num, d):
    sid = f'ex{n}-{d["id"]}'
    h = f'\n      <h3 class="q" id="{sid}">{num}. {html.escape(d["title"])}</h3>\n'
    h += f'      <div class="src-tag">📍 {html.escape(d["src"])}</div>\n'
    h += f'      <div class="callout callout-id"><div class="callout-title"></div><p>{mathify(d["ident"])}</p></div>\n'
    h += '      <div class="callout callout-steps"><div class="callout-title"></div><ol class="steps">\n'
    h += ''.join(step_li(st) for st in d['steps'])
    h += '      </ol></div>\n'
    for title, ls in d.get('thm', []):
        h += thm_box(title, ls)
    for f in d.get('formula', []):
        for part in f.split('\\qquad'):
            if part.strip():
                h += '      ' + disp(part) + '\n'
    if d.get('table'):
        h += '      <table>\n        <tr><th scope="col">סוג</th><th scope="col">מתי</th></tr>\n'
        h += ''.join(f'        <tr><td><b>{a}</b></td><td>{mathify(b)}</td></tr>\n' for a, b in d['table'])
        h += '      </table>\n'
    if d.get('dia'):
        dg = DIA.diagram(d['dia'][4:] if d['dia'].startswith('svg:') else d['dia'])
        if d.get('dia_cap'):
            dg = dg.replace('</div><!--/dia-->', f'<div class="dia-cap">{mathify(d["dia_cap"])}</div></div><!--/dia-->', 1)
        h += '      ' + dg + '\n'
    if d.get('ex'):
        h += '      ' + lines(d['ex']) + '\n'
    h += f'      <div class="callout callout-warn">\n        <div class="callout-title">טעויות נפוצות</div>\n        <p>{mathify(d["warn"])}</p>\n      </div>\n'
    h += f'      <div class="callout callout-check"><div class="callout-title"></div><p>{mathify(d["check"])}</p></div>\n'
    return h


def unit(u):
    n = u['n']
    h = (f'\n    <section class="exercise" id="ex{n}">\n      <div class="ex-header">\n        <div class="ex-badge">{n}</div>\n'
         f'        <h2 class="ex-title">{html.escape(u["title"])}</h2>\n      </div>\n'
         f'      <p class="ex-intro">{html.escape(u["intro"])}</p>\n')
    toc = (f'<li class="toc-group"><details class="toc-details" id="details-{n}"><summary><a href="#ex{n}" class="top-link" data-ex="{n}">'
           f'<span class="num">{n}</span><span>{html.escape(u["short"])}</span></a></summary><ul class="sub-toc">\n')
    num = 0
    for pi, (ptitle, secs) in enumerate(u['parts'], 1):
        style = 'margin-top:0;font-size:1.4rem;' if pi == 1 else 'font-size:1.4rem;margin-top:56px;'
        h += f'\n      <h2 style="{style}" id="ex{n}-p{pi}">{html.escape(ptitle)}</h2>\n'
        toc += f'<li class="toc-part-li"><a href="#ex{n}-p{pi}" class="toc-part-link" data-ex="{n}">{html.escape(ptitle)}</a></li>\n'
        for d in secs:
            num += 1
            h += section(n, num, d)
            toc += f'<li><a href="#ex{n}-{d["id"]}" data-ex="{n}">{num}. {html.escape(d["title"])}</a></li>\n'
    h += f'\n      <div class="summary-sheet">\n        <div class="summary-sheet-title">✅ סיכום תרגיל {n} - דף נוסחאות מחשבתי</div>\n'
    h += ''.join(f'        <p><b>{a}:</b> {mathify(b)}</p>\n' for a, b in u['summary'])
    h += '      </div>\n'
    h += (f'\n      <div class="key-idea">\n        <h4>💡 הדבר שהכי חשוב להבין מכל תרגיל {n}</h4>\n        <p>{mathify(u["key"])}</p>\n      </div>\n'
          '      <div class="end-of-exercise"></div>\n    </section>\n')
    toc += '</ul></details></li>\n'
    return h, toc


def put(page, start, end, block, anchor):
    if start in page:
        a = page.index(start); b = page.index(end) + len(end)
        return page[:a] + start + block + end + page[b:]
    i = page.index(anchor)
    return page[:i] + start + block + end + '\n' + page[i:]


def _drop_old(page, n):
    """remove a unit that is written directly in the page (outside the markers) - it is rebuilt from the data"""
    a0 = page.find('<!-- units:start -->')
    m = re.search(rf'\n?\s*<section class="exercise" id="ex{n}">', page)
    if m and (a0 == -1 or m.start() < a0):
        end = page.index('</section>', m.start()) + len('</section>')
        # the section may contain nested <section>? (no) - but make sure we stop at its own end
        page = page[:m.start()] + page[end:]
    t0 = page.find('<!-- units-toc:start -->')
    m = re.search(rf'<li class="toc-group"><details class="toc-details" id="details-{n}">.*?</details></li>\n?', page, re.S)
    if m and (t0 == -1 or m.start() < t0):
        page = page[:m.start()] + page[m.end():]
    return page


def apply(site, page):
    units = []
    for name in SITES[site]:
        spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, 'units', name + '.py'))
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        units += mod.UNITS
    units.sort(key=lambda u: u['n'])
    for u in units:
        page = _drop_old(page, u['n'])
    body, toc = '', ''
    for u in units:
        h, t = unit(u)
        body += h; toc += t
    page = put(page, '<!-- units:start -->', '<!-- units:end -->', body + '\n    ', '<!-- files-section:start -->')
    page = put(page, '<!-- units-toc:start -->\n', '<!-- units-toc:end -->', toc, '    <!-- files-toc:start -->')
    return page


def main():
    for site in SITES:
        p = os.path.join(ROOT, site, 'index.html')
        page = open(p, encoding='utf-8').read()
        new = apply(site, page)
        if new != page:
            open(p, 'w', encoding='utf-8').write(new)
        print(site, 'units:', len(re.findall(r'<section class="exercise"', new)))


if __name__ == '__main__':
    main()
