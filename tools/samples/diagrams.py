# -*- coding: utf-8 -*-
# שרטוטים קטנים (SVG) עם מערכת צירים - להמחשה בתוך ההסברים ובפתרונות לדוגמה.
# בשימוש: שורה 'svg:<שם>' בתוך הסבר או בשלב של פתרון.
import math
import re

INK = '#23262B'
GRID = '#E3E6EE'
BLUE = '#2C4A8C'
PURPLE = '#6B3FA0'
GREEN = '#2A6F63'
ORANGE = '#B7790A'
RED = '#A23F35'
GREY = '#8A8F9C'


class Plot:
    _n = 0

    def __init__(self, xmin, xmax, ymin, ymax, w=300, pad=24, title='', ys=1.0):
        self.x0, self.x1, self.y0, self.y1 = xmin, xmax, ymin, ymax
        self.w = w
        self.s = (w - 2 * pad) / (xmax - xmin)
        self.sy = self.s * ys
        self.h = (ymax - ymin) * self.sy + 2 * pad
        Plot._n += 1
        self.cid = f'clp{Plot._n}'
        self.pad = pad
        self.el = []
        self.title = title

    def X(self, x):
        return self.pad + (x - self.x0) * self.s

    def Y(self, y):
        return self.pad + (self.y1 - y) * self.sy

    def add(self, s):
        self.el.append(s)

    def grid(self, step=1):
        x = math.ceil(self.x0 / step) * step
        while x <= self.x1 + 1e-9:
            self.add(f'<line x1="{self.X(x):.1f}" y1="{self.Y(self.y0):.1f}" x2="{self.X(x):.1f}" y2="{self.Y(self.y1):.1f}" stroke="{GRID}" stroke-width="1"/>')
            x += step
        y = math.ceil(self.y0 / step) * step
        while y <= self.y1 + 1e-9:
            self.add(f'<line x1="{self.X(self.x0):.1f}" y1="{self.Y(y):.1f}" x2="{self.X(self.x1):.1f}" y2="{self.Y(y):.1f}" stroke="{GRID}" stroke-width="1"/>')
            y += step

    def axes(self, xl='x', yl='y', ticks=None, yticks=None):
        m = '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>' % INK
        self.add(f'<defs>{m}</defs>')
        self.add(f'<line x1="{self.X(self.x0):.1f}" y1="{self.Y(0):.1f}" x2="{self.X(self.x1):.1f}" y2="{self.Y(0):.1f}" stroke="{INK}" stroke-width="1.4" marker-end="url(#ah)"/>')
        self.add(f'<line x1="{self.X(0):.1f}" y1="{self.Y(self.y0):.1f}" x2="{self.X(0):.1f}" y2="{self.Y(self.y1):.1f}" stroke="{INK}" stroke-width="1.4" marker-end="url(#ah)"/>')
        self.txt(self.x1, 0, xl, dx=-4, dy=16, anchor='end', it=True, size=13)
        self.txt(0, self.y1, yl, dx=8, dy=10, anchor='start', it=True, size=13)
        for t, lab in (ticks or []):
            self.add(f'<line x1="{self.X(t):.1f}" y1="{self.Y(0) - 4:.1f}" x2="{self.X(t):.1f}" y2="{self.Y(0) + 4:.1f}" stroke="{INK}"/>')
            self.txt(t, 0, lab, dy=17, size=12, color=GREY)
        for t, lab in (yticks or []):
            self.add(f'<line x1="{self.X(0) - 4:.1f}" y1="{self.Y(t):.1f}" x2="{self.X(0) + 4:.1f}" y2="{self.Y(t):.1f}" stroke="{INK}"/>')
            self.txt(0, t, lab, dx=-7, dy=4, anchor='end', size=12, color=GREY)

    def txt(self, x, y, s, dx=0, dy=0, anchor='middle', size=13, color=INK, it=False, bold=False, heb=False):
        st = ' font-style="italic"' if it else ''
        bw = ' font-weight="700"' if bold else ''
        fam = "'Assistant',sans-serif" if heb else "'Times New Roman',serif"
        d = ' direction="rtl" unicode-bidi="embed"' if heb else ' direction="ltr" unicode-bidi="embed"'
        self.add(f'<text x="{self.X(x) + dx:.1f}" y="{self.Y(y) + dy:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{color}"{st}{bw}{d} font-family="{fam}">{s}</text>')

    def seg(self, a, b, color=INK, w=2, dash=False, arrow=False):
        da = ' stroke-dasharray="5 4"' if dash else ''
        ar = ''
        if arrow:
            mid = 'a' + color[1:]
            self.add(f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker></defs>')
            ar = f' marker-end="url(#{mid})"'
        self.add(f'<line x1="{self.X(a[0]):.1f}" y1="{self.Y(a[1]):.1f}" x2="{self.X(b[0]):.1f}" y2="{self.Y(b[1]):.1f}" stroke="{color}" stroke-width="{w}"{da}{ar}/>')

    def dot(self, x, y, color=PURPLE, r=4.5, hollow=False):
        f = '#fff' if hollow else color
        self.add(f'<circle cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="{r}" fill="{f}" stroke="{color}" stroke-width="2"/>')

    def circle(self, r, color=GREY, dash=True, cx=0, cy=0):
        da = ' stroke-dasharray="4 4"' if dash else ''
        self.add(f'<circle cx="{self.X(cx):.1f}" cy="{self.Y(cy):.1f}" r="{r * self.s:.1f}" fill="none" stroke="{color}" stroke-width="1.5"{da}/>')

    def arc(self, r, t0, t1, color=ORANGE, w=2, arrow=True):
        """arc of radius r (plot units) from angle t0 to t1 (radians, counter-clockwise if t1>t0)"""
        n = 40
        pts = [(r * math.cos(t0 + (t1 - t0) * k / n), r * math.sin(t0 + (t1 - t0) * k / n)) for k in range(n + 1)]
        d = 'M' + ' L'.join(f'{self.X(x):.1f},{self.Y(y):.1f}' for x, y in pts)
        ar = ''
        if arrow:
            mid = 'arc' + color[1:]
            self.add(f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker></defs>')
            ar = f' marker-end="url(#{mid})"'
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"{ar}/>')

    def curve(self, f, a, b, color=BLUE, w=2.2, n=240, dash=False, jump=None):
        pts, path = [], []
        for k in range(n + 1):
            x = a + (b - a) * k / n
            try:
                y = f(x)
            except (ValueError, ZeroDivisionError):
                y = None
            if y is None or y != y or y < self.y0 - 2 or y > self.y1 + 2 or (jump and pts and abs(y - pts[-1][1]) > jump):
                if len(pts) > 1:
                    path.append(pts)
                pts = [] if y is None or y != y or y < self.y0 - 2 or y > self.y1 + 2 else [(x, y)]
                continue
            pts.append((x, y))
        if len(pts) > 1:
            path.append(pts)
        da = ' stroke-dasharray="6 4"' if dash else ''
        for p in path:
            d = 'M' + ' L'.join(f'{self.X(x):.1f},{self.Y(max(self.y0 - 1, min(self.y1 + 1, y))):.1f}' for x, y in p)
            self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"{da} clip-path="url(#{self.cid})"/>')

    def svg(self, label):
        clip = (f'<defs><clipPath id="{self.cid}"><rect x="{self.X(self.x0):.1f}" y="{self.Y(self.y1):.1f}" '
                f'width="{self.X(self.x1) - self.X(self.x0):.1f}" height="{self.Y(self.y0) - self.Y(self.y1):.1f}"/></clipPath></defs>')
        self.el.insert(0, clip)
        return (f'<svg viewBox="0 0 {self.w} {self.h:.0f}" role="img" aria-label="{label}" direction="ltr" xmlns="http://www.w3.org/2000/svg">'
                + ''.join(self.el) + '</svg>')


def L(t):
    return f'<bdi dir="ltr">{t}</bdi>'


def legend(items):
    """a small legend under the drawing: [(color, text)]"""
    return '<div class="dia-legend">' + ''.join(
        f'<span><i style="background:{c}"></i>{t}</span>' for c, t in items) + '</div>'


def box(svg, cap='', leg=None):
    return ('<div class="dia">' + svg + (legend(leg) if leg else '')
            + (f'<div class="dia-cap">{cap}</div>' if cap else '') + '</div><!--/dia-->')


# ---------------------------------------------------------------- מספרים מרוכבים
def d_plane():
    p = Plot(-3.5, 4.5, -3, 5, w=280)
    p.grid(); p.axes('Re', 'Im', ticks=[(3, '3')], yticks=[(4, '4'), (-2, '-2')])
    p.seg((3, 0), (3, 4), GREY, 1.5, dash=True); p.seg((0, 4), (3, 4), GREY, 1.5, dash=True)
    p.dot(3, 4); p.txt(3, 4, '3+4i', dx=6, dy=-8, anchor='start', it=True, color=PURPLE, bold=True)
    p.dot(0, -2, GREEN); p.txt(0, -2, '−2i', dx=8, dy=5, anchor='start', it=True, color=GREEN, bold=True)
    return box(p.svg('המישור המרוכב'), 'כל מספר '+L('<i>a+bi</i>')+' הוא נקודה: '+L('<i>a</i>')+' ימינה, '+L('<i>b</i>')+' למעלה')


def d_polar(a=1.0, b=math.sqrt(3), za='1+i√3', ra='r = 2', ta='θ = π/3', aa='a = 1', ba='b = √3'):
    R = math.hypot(a, b)
    m = max(abs(a), abs(b), R) + 0.8
    p = Plot(-0.6 if a >= 0 else -m, m if a >= 0 else 1.2, -0.6 if b >= 0 else -m, m if b >= 0 else 1.2, w=280)
    p.grid(); p.axes('Re', 'Im')
    p.seg((a, 0), (a, b), GREEN, 2, dash=True); p.seg((0, 0), (a, 0), BLUE, 3)
    p.seg((0, 0), (a, b), PURPLE, 2.6)
    t = math.atan2(b, a)
    p.arc(min(0.55, R * 0.35), 0, t)
    p.dot(a, b)
    p.txt(a, b, za, dx=8 if a >= 0 else -8, dy=-8, anchor='start' if a >= 0 else 'end', it=True, color=PURPLE, bold=True)
    p.txt(a / 2, b / 2, ra, dx=-8 if a >= 0 else 8, dy=-6, anchor='end' if a >= 0 else 'start', it=True, color=PURPLE)
    p.txt(0.75 * math.cos(t / 2), 0.75 * math.sin(t / 2), ta, dx=6, dy=2 if b >= 0 else 14, anchor='start' if a >= 0 else 'end', it=True, color=ORANGE)
    p.txt(a / 2, 0, aa, dy=17 if b >= 0 else -8, it=True, color=BLUE)
    p.txt(a, b / 2, ba, dx=7 if a >= 0 else -7, anchor='start' if a >= 0 else 'end', it=True, color=GREEN)
    return box(p.svg('הצגה קוטבית'), leg=[(PURPLE, L('r')+' - המרחק מהראשית'), (ORANGE, L('θ')+' - הזווית'),
                                          (BLUE, L('a = r·cosθ')), (GREEN, L('b = r·sinθ'))])


def d_polar_m5():
    return d_polar(-5 / 2.5, 5 / 2.5, '−5+5i', 'r = 5√2', 'θ = 3π/4', 'a = −5', 'b = 5')


def d_modulus():
    p = Plot(-0.8, 4.6, -0.8, 5, w=250)
    p.grid(); p.axes('Re', 'Im', ticks=[(3, '3')], yticks=[(4, '4')])
    p.seg((0, 0), (3, 0), BLUE, 3); p.seg((3, 0), (3, 4), GREEN, 3); p.seg((0, 0), (3, 4), PURPLE, 2.6)
    p.dot(3, 4); p.txt(3, 4, '3+4i', dx=8, dy=-6, anchor='start', it=True, color=PURPLE, bold=True)
    p.txt(1.2, 2.2, '|z| = 5', anchor='end', it=True, color=PURPLE, bold=True)
    return box(p.svg('ערך מוחלט'), 'המרחק מהראשית - היתר במשולש: '+L('√(3² + 4²) = 5'))


def d_conj():
    p = Plot(-1, 4.5, -4, 4.5, w=230)
    p.grid(); p.axes('Re', 'Im')
    p.seg((3, 2), (3, -2), GREY, 1.5, dash=True)
    p.dot(3, 2); p.txt(3, 2, 'z = 3+2i', dx=-8, dy=-8, anchor='end', it=True, color=PURPLE, bold=True)
    p.dot(3, -2, GREEN); p.txt(3, -2, 'z̄ = 3−2i', dx=-8, dy=16, anchor='end', it=True, color=GREEN, bold=True)
    return box(p.svg('צמוד'), 'הצמוד = שיקוף בציר האופקי (הממשי)')


def d_quadrants():
    p = Plot(-3, 3, -3, 3, w=240)
    p.axes('Re', 'Im')
    for (x, y, n, s, c) in [(1.5, 1.5, 'רביע 1', 'a>0, b>0', BLUE), (-1.5, 1.5, 'רביע 2', 'a<0, b>0', PURPLE),
                            (-1.5, -1.5, 'רביע 3', 'a<0, b<0', ORANGE), (1.5, -1.5, 'רביע 4', 'a>0, b<0', GREEN)]:
        p.txt(x, y, n, dy=-4, size=14, color=c, bold=True, heb=True)
        p.txt(x, y, s, dy=14, size=12, color=c, it=True)
    return box(p.svg('רביעים'), 'ממספרים נגד כיוון השעון, החל מימין-למעלה')


def d_argument():
    p = Plot(-3.4, 3.4, -3, 3.4, w=260)
    p.grid(); p.axes('Re', 'Im')
    p.seg((0, 0), (-2.2, 2.2), PURPLE, 2.6); p.dot(-2.2, 2.2)
    p.txt(-2.2, 2.2, '−5+5i', dx=-4, dy=-10, anchor='middle', it=True, color=PURPLE, bold=True)
    p.seg((0, 0), (2.2, -2.2), RED, 1.6, dash=True)
    p.txt(2.2, -2.2, '−π/4 ✗', dx=4, dy=16, anchor='middle', it=True, color=RED)
    p.arc(0.8, 0, 3 * math.pi / 4)
    p.txt(0.2, 1.05, '3π/4 ✓', anchor='start', it=True, color=ORANGE, bold=True)
    return box(p.svg('מציאת הזווית'), 'ל-'+L('tan')+' יש אותו ערך בשני כיוונים הפוכים - בוחרים את הכיוון שבו הנקודה באמת נמצאת')


def d_unit():
    t = math.pi / 3
    p = Plot(-1.4, 1.5, -1.4, 1.5, w=260)
    p.grid(0.5); p.axes('x', 'y', ticks=[(1, '1'), (-1, '−1')], yticks=[(1, '1'), (-1, '−1')])
    p.circle(1, GREY, dash=False)
    c, s = math.cos(t), math.sin(t)
    p.seg((0, 0), (c, 0), BLUE, 3); p.seg((c, 0), (c, s), GREEN, 3); p.seg((0, 0), (c, s), PURPLE, 2)
    p.arc(0.3, 0, t)
    p.dot(c, s)
    p.txt(c, s, '(cosθ, sinθ)', dx=6, dy=-8, anchor='start', it=True, color=PURPLE, bold=True)
    p.txt(c / 2, 0, 'cosθ', dy=17, it=True, color=BLUE)
    p.txt(c, s / 2, 'sinθ', dx=6, anchor='start', it=True, color=GREEN)
    p.txt(0.36, 0.16, 'θ', anchor='start', it=True, color=ORANGE)
    return box(p.svg('מעגל היחידה'), L('cosθ')+' - כמה ימינה, '+L('sinθ')+' - כמה למעלה')


def d_euler():
    p = Plot(-1.6, 1.6, -1.45, 1.6, w=260)
    p.grid(0.5); p.axes('Re', 'Im')
    p.circle(1, GREY, dash=False)
    for (x, y, lab, dx, dy, an) in [(1, 0, 'e^{i0} = 1', 6, -8, 'start'), (0, 1, 'e^{iπ/2} = i', 8, -6, 'start'),
                                     (-1, 0, 'e^{iπ} = −1', -6, -8, 'end'), (0, -1, 'e^{−iπ/2} = −i', 8, 14, 'start')]:
        p.dot(x, y)
        lab = lab.replace('e^{i0}', 'e<tspan baseline-shift="super" font-size="10">i0</tspan>')
        lab = lab.replace('e^{iπ/2}', 'e<tspan baseline-shift="super" font-size="10">iπ/2</tspan>')
        lab = lab.replace('e^{iπ}', 'e<tspan baseline-shift="super" font-size="10">iπ</tspan>')
        lab = lab.replace('e^{−iπ/2}', 'e<tspan baseline-shift="super" font-size="10">−iπ/2</tspan>')
        p.txt(x, y, lab, dx=dx, dy=dy, anchor=an, it=True, color=PURPLE, bold=True)
    p.arc(0.45, 0, math.pi / 2)
    return box(p.svg('ערכים של e בחזקת iθ'), L('e<sup>iθ</sup>')+' היא הנקודה על מעגל היחידה בזווית '+L('θ'))


def d_polarmult():
    p = Plot(-1.7, 2.6, -0.6, 2.8, w=270)
    p.grid(0.5); p.axes('Re', 'Im')
    a1, a2 = math.pi / 9, math.pi / 4
    r1, r2 = 1.2, 1.5
    z1 = (r1 * math.cos(a1), r1 * math.sin(a1)); z2 = (r2 * math.cos(a2), r2 * math.sin(a2))
    rr = 1.9; z3 = (rr * math.cos(a1 + a2 + 0.0), rr * math.sin(a1 + a2))
    p.seg((0, 0), z1, BLUE, 2.4); p.seg((0, 0), z2, GREEN, 2.4); p.seg((0, 0), z3, PURPLE, 2.8)
    p.dot(*z1, BLUE); p.dot(*z2, GREEN); p.dot(*z3, PURPLE)
    p.txt(*z1, 'z₁', dx=8, dy=4, anchor='start', it=True, color=BLUE, bold=True)
    p.txt(*z2, 'z₂', dx=8, dy=0, anchor='start', it=True, color=GREEN, bold=True)
    p.txt(*z3, 'z₁·z₂', dx=-6, dy=-6, anchor='end', it=True, color=PURPLE, bold=True)
    p.arc(0.4, 0, a1, BLUE, 1.8, arrow=False); p.arc(0.62, 0, a2, GREEN, 1.8, arrow=False); p.arc(0.85, 0, a1 + a2, ORANGE, 2)
    return box(p.svg('כפל בהצגה קוטבית'), 'בכפל: הזווית של התוצאה היא סכום הזוויות, והמרחק הוא מכפלת המרחקים')


def _roots(n, R, phi, labels, cap):
    m = R * 1.75
    p = Plot(-m, m, -R * 1.4, R * 1.45, w=290)
    if R < 1.5:
        p.grid(0.5); p.axes('Re', 'Im')
    else:
        p.grid(); p.axes('Re', 'Im')
    p.circle(R)
    pts = []
    for k in range(n):
        t = phi / n + 2 * math.pi * k / n
        pts.append((R * math.cos(t), R * math.sin(t)))
    for i in range(n):
        p.seg(pts[i], pts[(i + 1) % n], GREY, 1.2, dash=True)
    for (x, y), lab in zip(pts, labels):
        p.seg((0, 0), (x, y), PURPLE, 1.6)
        p.dot(x, y)
        p.txt(x, y, lab, dx=10 if x >= -0.01 else -10, dy=-8 if y >= 0 else 16, anchor='start' if x >= -0.01 else 'end', it=True, color=PURPLE, bold=True)
    return box(p.svg('פתרונות על מעגל'), cap)


def d_roots8():
    return _roots(3, 2, 0, ['z₀', 'z₁', 'z₂'],
                  'שלושת הפתרונות של '+L('z³ = 8')+' - על מעגל ברדיוס 2, בהפרשים של '+L('2π/3')+' (משולש שווה צלעות)')


def d_roots64i():
    return _roots(3, 4, math.pi / 2, ['z₀', 'z₁', 'z₂'],
                  'שלושת הפתרונות של '+L('z³ = 64i')+' - על מעגל ברדיוס 4, בהפרשים של '+L('2π/3'))


def d_fullturn():
    p = Plot(-1.6, 1.7, -1.5, 1.6, w=240)
    p.axes('Re', 'Im')
    p.circle(1, GREY, dash=False)
    t = math.pi / 3
    p.arc(0.55, 0, t, ORANGE, 2)
    p.arc(0.8, t, t + 2 * math.pi - 0.15, GREEN, 1.8)
    p.dot(math.cos(t), math.sin(t))
    p.txt(math.cos(t), math.sin(t), 'θ  ,  θ+2π', dx=8, dy=-6, anchor='start', it=True, color=PURPLE, bold=True)
    return box(p.svg('סיבוב שלם'), 'סיבוב שלם ('+L('2π')+') מחזיר לאותה נקודה')


def d_radians():
    p = Plot(-1.5, 1.5, -1.4, 1.5, w=250)
    p.axes('', '')
    p.circle(1, GREY, dash=False)
    for t, lab in [(0, '0'), (math.pi / 6, 'π/6 = 30°'), (math.pi / 4, 'π/4 = 45°'), (math.pi / 3, 'π/3 = 60°'), (math.pi / 2, 'π/2 = 90°'),
                   (math.pi, 'π = 180°'), (3 * math.pi / 2, '3π/2 = 270°')]:
        x, y = math.cos(t), math.sin(t)
        p.seg((0, 0), (x, y), GREY, 1, dash=True)
        p.dot(x, y, PURPLE, 3.5)
        right = x > 0.05
        p.txt(x, y, lab, dx=7 if right else (-7 if x < -0.05 else 6), dy=-4 if y > 0.05 else 14, anchor='start' if right or abs(x) <= 0.05 else 'end', size=11, it=True, color=PURPLE)
    return box(p.svg('זוויות ברדיאנים'), 'מודדים מהכיוון החיובי של הציר האופקי, נגד כיוון השעון')


# ---------------------------------------------------------------- חדו"א
def _pi_ticks(lo, hi):
    out = []
    for k in range(-4, 5):
        v = k * math.pi / 2
        if lo < v < hi and k:
            lab = {1: 'π/2', -1: '−π/2', 2: 'π', -2: '−π', 3: '3π/2', -3: '−3π/2', 4: '2π', -4: '−2π'}[k]
            out.append((v, lab))
    return out


def d_sincos():
    p = Plot(-3.6, 7, -1.5, 1.6, w=320, ys=1.7)
    p.axes('x', 'y', ticks=_pi_ticks(-3.6, 7), yticks=[(1, '1'), (-1, '−1')])
    p.curve(math.sin, -3.6, 6.9, BLUE); p.curve(math.cos, -3.6, 6.9, ORANGE)
    return box(p.svg('sin ו-cos'), leg=[(BLUE, L('sin x')), (ORANGE, L('cos x'))])


def d_logexp():
    p = Plot(-2.5, 5, -2.5, 5, w=270)
    p.grid(); p.axes('x', 'y', ticks=[(1, '1'), (2, '2')], yticks=[(1, '1')])
    p.curve(lambda x: math.log2(x) if x > 0 else None, 0.02, 5, BLUE)
    p.curve(lambda x: 2 ** x, -2.5, 2.4, ORANGE)
    p.dot(1, 0, BLUE, 3.5); p.dot(0, 1, ORANGE, 3.5)
    return box(p.svg('לוגריתם ומעריכית'), leg=[(BLUE, L('log₂x')+' עובר ב-'+L('(1,0)')+', אסימפטוטה '+L('x = 0')), (ORANGE, L('2ˣ')+' עובר ב-'+L('(0,1)')+', אסימפטוטה '+L('y = 0'))])


def d_transform():
    p = Plot(-3, 5, -1.5, 7, w=280)
    p.grid(); p.axes('x', 'y', ticks=[(-2, '−2'), (1, '1')], yticks=[(4, '4')])
    p.curve(lambda x: math.log2(x) if x > 0 else None, 0.02, 5, GREY, dash=True)
    p.curve(lambda x: math.log2(x + 2) + 4 if x > -2 else None, -1.995, 5, BLUE)
    p.seg((-2, -1.5), (-2, 7), RED, 1.4, dash=True)
    p.seg((1, 0), (-1, 4), ORANGE, 1.8, arrow=True)
    return box(p.svg('הזזה'), leg=[(GREY, L('log₂x')), (BLUE, L('log₂(x+2)+4')+' - 2 שמאלה ו-4 למעלה'), (RED, 'האסימפטוטה: '+L('x = −2'))])


def d_parity():
    p = Plot(-2.2, 2.2, -2.2, 3, w=270)
    p.grid(); p.axes('x', 'y')
    p.curve(lambda x: x * x, -1.75, 1.75, BLUE); p.curve(lambda x: x ** 3, -1.3, 1.3, ORANGE)
    p.dot(1, 1, BLUE, 3.5); p.dot(-1, 1, BLUE, 3.5); p.seg((-1, 1), (1, 1), BLUE, 1, dash=True)
    p.dot(1, 1, ORANGE, 3); p.dot(-1, -1, ORANGE, 3.5); p.seg((-1, -1), (1, 1), ORANGE, 1, dash=True)
    return box(p.svg('זוגית ואי-זוגית'), leg=[(BLUE, L('x²')+' זוגית - מראה בציר '+L('y')), (ORANGE, L('x³')+' אי-זוגית - סימטרית לראשית')])


def d_absgraph():
    p = Plot(-6.6, 6.6, -1.4, 1.6, w=320, ys=2.2)
    p.axes('x', 'y', ticks=_pi_ticks(-6.6, 6.6)[1:-1], yticks=[(1, '1')])
    p.curve(math.sin, -6.5, 6.5, GREY, 1.4, dash=True)
    p.curve(lambda x: abs(math.sin(x)), -6.5, 6.5, BLUE)
    p.curve(lambda x: math.sin(abs(x)), -6.5, 6.5, ORANGE, 1.8)
    return box(p.svg('ערך מוחלט'), leg=[(GREY, L('sin x')), (BLUE, L('|sin x|')+' - הכול למעלה'), (ORANGE, L('sin|x|')+' - השמאל מראה של הימין')])


def d_period():
    p = Plot(-0.5, 7, -1.5, 1.6, w=320, ys=1.6)
    p.axes('x', 'y', ticks=_pi_ticks(-0.5, 7), yticks=[(1, '1')])
    p.curve(math.sin, -0.4, 6.9, GREY, 1.6, dash=True); p.curve(lambda x: math.sin(2 * x), -0.4, 6.9, BLUE)
    return box(p.svg('מחזור'), leg=[(GREY, L('sin x')+' - מחזור '+L('2π')), (BLUE, L('sin 2x')+' - מחזור '+L('π'))])


def d_floor():
    p = Plot(-2.5, 3.6, -2.6, 3.4, w=260)
    p.grid(); p.axes('x', 'y', ticks=[(1, '1'), (2, '2')], yticks=[(1, '1'), (2, '2')])
    for n in range(-2, 3):
        p.seg((n, n), (n + 1, n), BLUE, 2.6)
        p.dot(n, n, BLUE, 3.5); p.dot(n + 1, n, BLUE, 3.5, hollow=True)
    return box(p.svg('ערך שלם'), 'מדרגות: נקודה מלאה בתחילת כל מדרגה, ריקה בסוף')


def d_injective():
    p = Plot(-2.2, 2.2, -1.4, 3.2, w=260)
    p.grid(); p.axes('x', 'y')
    p.curve(lambda x: x * x, -1.75, 1.75, BLUE); p.curve(lambda x: x ** 3, -1.4, 1.45, ORANGE)
    p.seg((-2.2, 1), (2.2, 1), RED, 1.4, dash=True)
    p.dot(-1, 1, RED, 3.5); p.dot(1, 1, RED, 3.5)
    return box(p.svg('חד-חד-ערכית'), leg=[(BLUE, L('x²')+' - הקו האופקי חותך פעמיים: לא חח"ע'), (ORANGE, L('x³')+' - כל קו אופקי חותך פעם אחת')])


def d_numline_interval():
    p = Plot(-1, 7, -0.8, 0.8, w=300)
    p.add(f'<line x1="{p.X(-1)}" y1="{p.Y(0)}" x2="{p.X(7)}" y2="{p.Y(0)}" stroke="{INK}" stroke-width="1.4"/>')
    p.seg((2, 0), (5, 0), BLUE, 5)
    p.dot(2, 0, BLUE, 5, hollow=True); p.dot(5, 0, BLUE, 5)
    p.txt(2, 0, '2', dy=22); p.txt(5, 0, '5', dy=22)
    p.txt(2, 0, 'לא כלול', dy=-12, size=12, color=BLUE, heb=True); p.txt(5, 0, 'כלול', dy=-12, size=12, color=BLUE, heb=True)
    return box(p.svg('קטע'), 'הקטע '+L('(2,5]')+' - עיגול ריק: לא כלול, מלא: כלול')


def d_signtable():
    p = Plot(-0.5, 6, -0.9, 0.9, w=310)
    p.add(f'<line x1="{p.X(-0.5)}" y1="{p.Y(0)}" x2="{p.X(6)}" y2="{p.Y(0)}" stroke="{INK}" stroke-width="1.4"/>')
    for x, lab, hol in [(1, '1', False), (2, '2', True), (4, '4', False)]:
        p.dot(x, 0, PURPLE, 4.5, hollow=hol); p.txt(x, 0, lab, dy=22)
    for x, s, c in [(0.25, '−', RED), (1.5, '+', GREEN), (3, '−', RED), (5, '+', GREEN)]:
        p.txt(x, 0, s, dy=-10, size=20, color=c, bold=True)
    return box(p.svg('טבלת סימנים'), 'הסימן של '+L('(x−1)(x−4)/(x−2)')+' בכל קטע. 2 - עיגול ריק (מתאפס במכנה)')


def d_dots():
    p = Plot(-2.5, 3, -1, 4.5, w=250)
    p.grid(); p.axes('x', 'y')
    p.curve(lambda x: x * x, -2, 0, BLUE); p.curve(lambda x: 2 + 0.5 * x, 0, 3, BLUE)
    p.dot(0, 0, BLUE, 4.5); p.dot(0, 2, BLUE, 4.5, hollow=True)
    return box(p.svg('נקודה מלאה וריקה'), 'ב-'+L('x = 0')+' הנקודה המלאה שייכת לגרף, הריקה לא')


DIAGRAMS = {
    'plane': d_plane, 'polar': d_polar, 'polar_m5': d_polar_m5, 'modulus': d_modulus, 'conj': d_conj,
    'quadrants': d_quadrants, 'argument': d_argument, 'unit': d_unit, 'euler': d_euler, 'polarmult': d_polarmult,
    'roots8': d_roots8, 'roots64i': d_roots64i, 'fullturn': d_fullturn, 'radians': d_radians,
    'sincos': d_sincos, 'logexp': d_logexp, 'transform': d_transform, 'parity': d_parity, 'absgraph': d_absgraph,
    'period': d_period, 'floor': d_floor, 'injective': d_injective, 'interval': d_numline_interval,
    'signtable': d_signtable, 'dots': d_dots,
}


def _num(t):
    return float(eval(t, {'math': math, 'pi': math.pi, 'sqrt': math.sqrt}))


def roots_generic(n, R, phi, cap=''):
    """the n solutions of z^n = R^n e^{i phi} (phi in radians)"""
    n = int(n)
    labels = [f'z{chr(0x2080 + k)}' for k in range(n)]
    return _roots(n, R, phi, labels, cap or ('הפתרונות על מעגל ברדיוס ' + L(f'{R:g}') + ', בהפרשים שווים של ' + L(f'2π/{n}')))


def points(*args):
    """'svg:points:a1:b1:label1:a2:b2:label2...' - points in the complex plane"""
    pts = [(_num(args[i]), _num(args[i + 1]), args[i + 2]) for i in range(0, len(args) - 2, 3)]
    m = max(max(abs(x), abs(y)) for x, y, _ in pts) * 1.6 + 0.6
    p = Plot(-m, m, -m, m, w=270)
    p.grid(1 if m < 7 else 2); p.axes('Re', 'Im')
    cols = [PURPLE, GREEN, BLUE, ORANGE]
    for k, (x, y, lab) in enumerate(pts):
        c = cols[k % 4]
        p.seg((0, 0), (x, y), c, 1.6, dash=True)
        p.dot(x, y, c)
        p.txt(x, y, lab, dx=8 if x >= 0 else -8, dy=-8 if y >= 0 else 16, anchor='start' if x >= 0 else 'end', it=True, color=c, bold=True)
    return box(p.svg('נקודות במישור'))


def d_fn(xmin, xmax, ymin, ymax, spec):
    """graphs of functions: spec = 'expr|legend;expr|legend' (python, variable x; floor, sqrt, log, sin, cos, ...)"""
    env = {k: getattr(math, k) for k in ('sin', 'cos', 'tan', 'sqrt', 'log', 'log2', 'floor', 'pi', 'e', 'exp')}
    env['ln'] = math.log
    env['log05'] = lambda v: math.log(v) / math.log(0.5)
    ys = 1.0
    ratio = (ymax - ymin) / (xmax - xmin)
    if ratio < 0.55:
        ys = 0.55 / ratio
    elif ratio > 1.05:
        ys = 1.05 / ratio
    p = Plot(xmin, xmax, ymin, ymax, w=300, ys=ys)
    span = max(xmax - xmin, ymax - ymin)
    step = 1 if span <= 12 else (2 if span <= 24 else 5)
    if ys == 1.0:
        p.grid(step)
    ticks = [(t, f'{t:g}'.replace('-', '−')) for t in range(int(math.ceil(xmin)), int(xmax) + 1) if t and (t % step == 0)] if xmax - xmin <= 24 else []
    yt = [(t, f'{t:g}'.replace('-', '−')) for t in range(int(math.ceil(ymin)), int(ymax) + 1) if t and (t % step == 0)] if ymax - ymin <= 24 else []
    if 'pi' in spec and xmax - xmin < 16:
        ticks = _pi_ticks(xmin, xmax)
    p.axes('x', 'y', ticks=ticks, yticks=yt)
    cols = [BLUE, ORANGE, PURPLE, GREEN]
    leg = []
    for k, part in enumerate(spec.split(';')):
        ex, _, lab = part.partition('|')
        dash = ex.startswith('~')
        ex = ex.lstrip('~')
        code = compile(ex, 'fn', 'eval')

        def f(x, code=code):
            try:
                v = eval(code, dict(env), {'x': x})
                return None if isinstance(v, complex) else v
            except (ValueError, ZeroDivisionError, OverflowError):
                return None
        col = GREY if dash else cols[k % 4]
        p.curve(f, xmin, xmax, col, 1.6 if dash else 2.4, n=600, dash=dash, jump=0.5 if 'floor' in ex else (ymax - ymin) / 3)
        if lab:
            leg.append((col, lab if re.search('[\u0590-\u05FF]', lab) else L(lab)))
    return box(p.svg('גרף'), leg=leg or None)


def diagram(name):
    """'name' or 'name:arg:arg...' (numbers may use pi and sqrt, e.g. 'roots:3:4:pi/2')"""
    if ':' in name:
        fn, *args = name.split(':')
        if fn == 'roots':
            return roots_generic(int(args[0]), _num(args[1]), _num(args[2]), *(args[3:4]))
        if fn == 'polar':
            a, b = _num(args[0]), _num(args[1])
            return d_polar(a, b, *args[2:])
        if fn == 'points':
            return points(*args)
        if fn == 'fn':
            return d_fn(_num(args[0]), _num(args[1]), _num(args[2]), _num(args[3]), ':'.join(args[4:]))
        raise KeyError(name)
    return DIAGRAMS[name]()
