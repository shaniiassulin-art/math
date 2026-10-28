#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reminders.py - מוסיף לכל סעיף פתרון בכל האתרים תיבת "תזכורות": המושגים מסעיפים אחרים שהסעיף משתמש בהם
(למשל e בחזקת i·θ, הצמוד, ערך מוחלט, תחום הגדרה), כל אחד נפתח בלחיצה, עם קישור למקום שבו הוא מוסבר במלואו.

המושגים נמצאים ב-LIBRARY למטה. כל מושג: כותרת, הסבר קצר (LaTeX בין $...$), המקום שבו הוא מוסבר בכל אתר,
וביטויים שמזהים שהסעיף משתמש בו. בסעיף שבו המושג עצמו מוסבר - לא מציגים לו תזכורת.

שימוש:  python3 tools/reminders.py            (מעדכן את כל האתרים)
        python3 tools/reminders.py --report   (רק מדפיס איזו תזכורת תיכנס לאיזה סעיף, בלי לכתוב)
דורש: pip install latex2mathml
"""
import html, os, re, sys
from latex2mathml.converter import convert

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES = ['algebra-solutions', 'algebra-theory', 'calculus-1']
MAX_PER_SECTION = 6

# ---------------------------------------------------------------- the reminders
E_POW_I = r'<msup><mi>e</mi>\s*<mrow>(?:(?!</msup>).)*?<mi>i</mi>'
CONJ = r'<mover>\s*(?:<mrow>)?\s*<mi>[zwω]</mi>|<mover><mrow><msub><mi>z</mi>|\bצמוד'
BAR = r'&#x0007C;|<mo[^>]*>\|</mo>'
TRIG = r'<mi>(?:sin|cos)</mi>'

LIBRARY = [
    # ------------------------------------------------ complex numbers
    dict(id='euler', sites={'algebra-solutions': 'ex1-s12', 'algebra-theory': 'ex1-s6'},
         title=r'מה זה $e^{i\theta}$?',
         body=r'$e^{i\theta}=\cos\theta+i\sin\theta$ (נוסחת אוילר). זה מספר על מעגל היחידה: $|e^{i\theta}|=1$, בזווית $\theta$ מהציר הממשי. '
              r'לכן $re^{i\theta}$ הוא המספר במרחק $r$ מהראשית בזווית $\theta$.<br>'
              r'<b>כללי חישוב:</b> $e^{i\alpha}\cdot e^{i\beta}=e^{i(\alpha+\beta)}$, $\ \frac{e^{i\alpha}}{e^{i\beta}}=e^{i(\alpha-\beta)}$, $\ \overline{e^{i\theta}}=e^{-i\theta}$, $\ e^{i(\theta+2\pi k)}=e^{i\theta}$.<br>'
              r'<b>ערכים שכדאי לזכור:</b> $e^{i\pi}=-1$, $\ e^{i\frac{\pi}{2}}=i$, $\ e^{-i\frac{\pi}{2}}=-i$, $\ e^{0}=1$.',
         triggers=[E_POW_I]),
    dict(id='polar', sites={'algebra-solutions': 'ex1-s12', 'algebra-theory': 'ex1-s6'},
         title=r'הצגה קוטבית $re^{i\theta}$',
         body=r'$z=a+bi=r(\cos\theta+i\sin\theta)=re^{i\theta}$, כאשר $r=|z|=\sqrt{a^2+b^2}$ ו-$\tan\theta=\frac{b}{a}$.<br>'
              r'<b>תיקון לפי הרביע:</b> ברביע הראשון והרביעי $\theta=\arctan\frac{b}{a}$; ברביע השני מוסיפים $\pi$; ברביע השלישי מחסירים $\pi$. '
              r'על הצירים: $\theta=\frac{\pi}{2}$ (מדומה חיובי), $-\frac{\pi}{2}$ (מדומה שלילי), $\pi$ (ממשי שלילי).',
         triggers=[r'קוטבי', r'<mi>arctan</mi>', r'<mo>arg</mo>']),
    dict(id='conj', sites={'algebra-solutions': 'ex1-s1', 'algebra-theory': 'ex1-s3'},
         title=r'הצמוד $\overline{z}$',
         body=r'$\overline{a+bi}=a-bi$ - שיקוף ביחס לציר הממשי.<br>'
              r'$z\overline{z}=|z|^2$, $\ z+\overline{z}=2\operatorname{Re}(z)$, $\ z-\overline{z}=2i\operatorname{Im}(z)$.<br>'
              r'הצמוד "עובר" על כל פעולה: $\overline{z_1\pm z_2}=\overline{z_1}\pm\overline{z_2}$, $\ \overline{z_1z_2}=\overline{z_1}\,\overline{z_2}$, '
              r'$\ \overline{\left(\frac{z_1}{z_2}\right)}=\frac{\overline{z_1}}{\overline{z_2}}$, $\ \overline{i}=-i$.',
         triggers=[CONJ]),
    dict(id='modulus', sites={'algebra-solutions': 'ex1-s1', 'algebra-theory': 'ex1-s4'},
         title=r'ערך מוחלט (מודול) $|z|$',
         body=r'$|a+bi|=\sqrt{a^2+b^2}$ - המרחק של $z$ מהראשית.<br>'
              r'$|z_1z_2|=|z_1||z_2|$, $\ \left|\frac{z_1}{z_2}\right|=\frac{|z_1|}{|z_2|}$, $\ |z^n|=|z|^n$, $\ |\overline{z}|=|z|$, $\ |z|^2=z\overline{z}$.<br>'
              r'שימי לב: באופן כללי $|z_1+z_2|\neq|z_1|+|z_2|$.',
         triggers=[r'ערך מוחלט|ערכים מוחלטים|מודול', BAR]),
    dict(id='divide', sites={'algebra-solutions': 'ex1-s3', 'algebra-theory': 'ex1-s2'},
         title=r'חילוק מספרים מרוכבים',
         body=r'כופלים מונה ומכנה בצמוד של המכנה, והמכנה נהיה ממשי: '
              r'$\frac{a+bi}{c+di}=\frac{(a+bi)(c-di)}{(c+di)(c-di)}=\frac{(a+bi)(c-di)}{c^2+d^2}$. מקרה מיוחד: $\frac{1}{i}=-i$.',
         triggers=[r'<mfrac>(?:(?!</mfrac>).)*?<mrow>(?:(?!</mrow>).)*?</mrow>\s*<mrow>(?:(?!</mrow>).)*?<mi>i</mi>(?:(?!</mrow>).)*?</mrow>\s*</mfrac>', r'בצמוד של המכנה|בצמוד המכנה']),
    dict(id='ipow', sites={'algebra-solutions': 'ex1-s4', 'algebra-theory': 'ex1-s1'},
         title=r'חזקות של $i$',
         body=r'$i^2=-1$, $\ i^3=-i$, $\ i^4=1$, ומשם זה חוזר במחזור של 4: $i^n$ תלוי רק בשארית של $n$ בחלוקה ב-4.',
         triggers=[r'<msup><mi>i</mi><mn>(?:[3-9]|\d{2,})</mn>', r'<msup><mi>i</mi><mrow><mo>&#x02212;</mo>']),
    dict(id='equal', sites={'algebra-solutions': 'ex1-s5', 'algebra-theory': 'ex1-s1'},
         title=r'שוויון מספרים מרוכבים',
         body=r'$a+bi=c+di$ אם ורק אם $a=c$ וגם $b=d$. משווים חלק ממשי לחלק ממשי וחלק מדומה לחלק מדומה - '
              r'ומכל שוויון מרוכב מקבלים שתי משוואות ממשיות.',
         triggers=[r'(?:משוו|השוו|השוואת)[^.<]{0,40}(?:ממשי|מדומה)', r'השוואת חלקים|השוו חלקים|השוואת החלק']),
    dict(id='realtest', sites={'algebra-solutions': 'ex1-s8', 'algebra-theory': 'ex1-s3'},
         title=r'מתי מספר הוא ממשי או מדומה טהור',
         body=r'$w$ <b>ממשי</b> אם ורק אם $w=\overline{w}$, כלומר $w-\overline{w}=0$.<br>'
              r'$w$ <b>מדומה טהור</b> אם ורק אם $\overline{w}=-w$, כלומר $w+\overline{w}=0$.',
         triggers=[r'מדומה טהור', r'הוא (?:מספר )?ממשי']),
    dict(id='demoivre', sites={'algebra-solutions': 'ex1-s13', 'algebra-theory': 'ex1-s8'},
         title=r'נוסחת דה-מואבר',
         body=r'$\left(re^{i\theta}\right)^n=r^ne^{in\theta}$, כלומר $(\cos\theta+i\sin\theta)^n=\cos n\theta+i\sin n\theta$. '
              r'מעלים את $r$ בחזקה וכופלים את הזווית ב-$n$.',
         triggers=[r'מואבר']),
    dict(id='roots', sites={'algebra-solutions': 'ex2-s1', 'algebra-theory': 'ex1-s9'},
         title=r'הפתרונות של $z^n=w$',
         body=r'אם $w=Re^{i\varphi}$ אז $z_k=\sqrt[n]{R}\,e^{i\frac{\varphi+2\pi k}{n}}$, $\ k=0,1,\dots,n-1$. '
              r'יש בדיוק $n$ פתרונות, על מעגל ברדיוס $\sqrt[n]{R}$, במרווחים שווים של $\frac{2\pi}{n}$.',
         triggers=[r'<mn>2</mn>\s*<mi>&#x003C0;</mi>\s*<mi>k</mi>', r'נוסחת השורש|שורש מסדר']),
    dict(id='quad', sites={'algebra-solutions': 'ex2-s6', 'algebra-theory': 'ex1-s10'},
         title=r'משוואה ריבועית עם $\Delta<0$',
         body=r'$az^2+bz+c=0$, $\ \Delta=b^2-4ac$. אם $\Delta<0$: $\ z_{1,2}=\frac{-b\pm i\sqrt{|\Delta|}}{2a}$ - שני פתרונות צמודים.',
         triggers=[r'<mi>&#x00394;</mi>', r'דיסקרימיננט']),
    dict(id='conjroots', sites={'algebra-solutions': 'ex2-s7', 'algebra-theory': 'ex1-s10'},
         title=r'שורשים צמודים בפולינום עם מקדמים ממשיים',
         body=r'אם כל המקדמים של $P$ ממשיים ו-$a$ שורש, אז גם $\overline{a}$ שורש. '
              r'לכן $P$ מתחלק ב-$(z-a)(z-\overline{a})=z^2-2\operatorname{Re}(a)z+|a|^2$.',
         triggers=[r'מקדמים ממשיים']),
    dict(id='trig', sites={'algebra-solutions': None, 'algebra-theory': 'ex1-s5'},
         link_other={'algebra-solutions': ('algebra-theory', 'ex1-s5')},
         title=r'ערכי $\sin$ ו-$\cos$ בזוויות מיוחדות',
         body=r'$\cos\frac{\pi}{6}=\frac{\sqrt3}{2},\ \sin\frac{\pi}{6}=\frac12$; $\quad\cos\frac{\pi}{4}=\sin\frac{\pi}{4}=\frac{\sqrt2}{2}$; '
              r'$\quad\cos\frac{\pi}{3}=\frac12,\ \sin\frac{\pi}{3}=\frac{\sqrt3}{2}$; $\quad\cos\frac{\pi}{2}=0,\ \sin\frac{\pi}{2}=1$; $\quad\cos\pi=-1,\ \sin\pi=0$.<br>'
              r'וגם: $\cos(-\theta)=\cos\theta$, $\ \sin(-\theta)=-\sin\theta$, $\ \sin^2\theta+\cos^2\theta=1$.',
         triggers=[TRIG]),
    dict(id='longdiv', sites={'algebra-solutions': None, 'algebra-theory': None},
         title=r'חילוק פולינומים (חילוק ארוך)',
         body=r'מחלקים את האיבר המוביל במוביל של המחלק, כופלים את המחלק בתוצאה, מחסירים, וחוזרים - '
              r'עד שדרגת השארית קטנה מדרגת המחלק. בסוף $A=B\cdot Q+R$.',
         triggers=[r'חילוק ארוך|חלוקה ארוכה|חילוק פולינום']),
    # ------------------------------------------------ matrices
    dict(id='mat_entry', sites={'algebra-theory': 'ex2-s1'},
         title=r'סימון איברי מטריצה',
         body=r'$A=[a_{ij}]$ מסדר $n\times m$: $n$ שורות ו-$m$ עמודות. $a_{ij}$ הוא האיבר בשורה $i$ ובעמודה $j$.',
         triggers=[r'<msub><mi>a</mi><mrow><mi>i</mi>', r'<msub><mi>[ab]</mi><mrow><mi>i</mi><mo>[^<]*</mo><mi>j</mi>']),
    dict(id='mat_special', sites={'algebra-theory': 'ex2-s2'},
         title=r'מטריצות מיוחדות',
         body=r'<b>ריבועית</b> $n\times n$; <b>היחידה</b> $I_n$ - 1 באלכסון הראשי ו-0 בשאר, ו-$AI=IA=A$; '
              r'<b>אלכסונית</b> - אפסים מחוץ לאלכסון; <b>משולשת</b> עליונה או תחתונה; <b>מטריצת האפס</b>.',
         triggers=[r'<msub><mi>I</mi>', r'מטריצת היחידה|אלכסונית|משולשת']),
    dict(id='mat_mult', sites={'algebra-theory': 'ex2-s4'},
         title=r'כפל מטריצות',
         body=r'אם $A$ מסדר $n\times m$ ו-$B$ מסדר $m\times p$, אז $AB$ מסדר $n\times p$ ו-$(AB)_{ij}=\sum_{k=1}^{m}a_{ik}b_{kj}$ '
              r'(שורה $i$ של $A$ כפול עמודה $j$ של $B$). באופן כללי $AB\neq BA$.',
         triggers=[r'<mi>A</mi>\s*<mi>B</mi>', r'כפל מטריצות']),
    dict(id='mat_t', sites={'algebra-theory': 'ex2-s6'},
         title=r'המטריצה המשוחלפת $A^t$',
         body=r'$(A^t)_{ij}=a_{ji}$ - השורות הופכות לעמודות. $(A^t)^t=A$, $\ (A+B)^t=A^t+B^t$, $\ (\lambda A)^t=\lambda A^t$, $\ (AB)^t=B^tA^t$.',
         triggers=[r'<msup><mi>[A-Z]</mi><mi>t</mi>', r'משוחלפ']),
    dict(id='mat_tr', sites={'algebra-theory': 'ex2-s7'},
         title=r'עקבה $\operatorname{tr}(A)$',
         body=r'$\operatorname{tr}(A)=a_{11}+a_{22}+\dots+a_{nn}$ - סכום האלכסון הראשי (רק למטריצה ריבועית). $\operatorname{tr}(AB)=\operatorname{tr}(BA)$.',
         triggers=[r'<mo>tr</mo>', r'עקבה']),
    # ------------------------------------------------ calculus
    dict(id='domain', sites={'calculus-1': 'ex1-s1'},
         title=r'תחום הגדרה',
         body=r'שלושה תנאים: <b>מכנה</b> $\neq0$; ביטוי בתוך <b>שורש זוגי</b> $\geq0$; הארגומנט של <b>$\log$ או $\ln$</b> $>0$. '
              r'התחום הוא החיתוך של כל התנאים.',
         triggers=[r'תחום הגדרה|תחום ההגדרה', r'<msub><mi>D</mi>']),
    dict(id='signs', sites={'calculus-1': 'ex1-s2'},
         title=r'טבלת סימנים',
         body=r'כדי לפתור $\frac{p(x)}{q(x)}\geq0$: מוצאים את האפסים של המונה ושל המכנה, מסמנים אותם על ציר, '
              r'ובודקים את הסימן בכל קטע. אפסי המכנה תמיד מוחרגים מהתשובה.',
         triggers=[r'טבלת סימנים|טבלת הסימנים']),
    dict(id='transform', sites={'calculus-1': 'ex1-s4'},
         title=r'הזזות, מתיחות ושיקופים',
         body=r'$f(x)+c$ - הזזה למעלה ב-$c$; $\ f(x-c)$ - הזזה <b>ימינה</b> ב-$c$; $\ a\,f(x)$ - מתיחה אנכית פי $a$; '
              r'$\ f(bx)$ - כיווץ אופקי פי $b$; $\ -f(x)$ - שיקוף ביחס לציר $x$; $\ f(-x)$ - שיקוף ביחס לציר $y$.<br>'
              r'שינוי <b>בתוך</b> הסוגריים פועל על $x$ - ולכן בכיוון ההפוך מהאינטואיציה.',
         triggers=[r'הזזה|הזזות|מתיחה|מתיחות|שיקוף|טרנספורמ']),
    dict(id='period', sites={'calculus-1': 'ex1-s6'},
         title=r'$\sin$, $\cos$, $\tan$: מחזור ותמונה',
         body=r'$\sin$ ו-$\cos$: מחזור $2\pi$, תמונה $[-1,1]$ (לכן $-1\leq\cos x\leq1$). '
              r'$\tan$: מחזור $\pi$, לא מוגדר ב-$x=\frac{\pi}{2}+k\pi$. אחרי $f(bx)$ המחזור מתחלק ב-$|b|$.',
         triggers=[r'<mi>(?:sin|cos|tan|cot)</mi>']),
    dict(id='parity', sites={'calculus-1': 'ex1-s7'},
         title=r'זוגית ואי-זוגית',
         body=r'<b>זוגית:</b> $f(-x)=f(x)$ לכל $x$ בתחום - סימטרית לציר $y$. <b>אי-זוגית:</b> $f(-x)=-f(x)$ - סימטרית לראשית.<br>'
              r'תנאי מקדים: התחום סימטרי ($x\in D\Rightarrow -x\in D$).',
         triggers=[r'זוגיות|(?:אי-)?זוגית|f\(-x\)']),
    dict(id='compose', sites={'calculus-1': 'ex1-s10'},
         title=r'הרכבת פונקציות $f\circ g$',
         body=r'$(f\circ g)(x)=f(g(x))$ - קודם $g$, ואז $f$ על התוצאה. התחום: $x$ בתחום של $g$, וגם $g(x)$ בתחום של $f$. '
              r'באופן כללי $f\circ g\neq g\circ f$.',
         triggers=[r'&#x02218;|∘', r'הרכבה|הרכבת']),
    dict(id='logs', sites={'calculus-1': 'ex1-s19'},
         title=r'חוקי לוגריתמים',
         body=r'$\log_a(xy)=\log_a x+\log_a y$, $\ \log_a\frac{x}{y}=\log_a x-\log_a y$, $\ \log_a x^k=k\log_a x$ - '
              r'נכונים רק כש-$x,y>0$. $\log_a x$ מוגדר רק ל-$x>0$, ו-$\ln x=\log_e x$.',
         triggers=[r'<mi>(?:log|ln)</mi>']),
    dict(id='piecewise', sites={'calculus-1': 'ex2-s1'},
         title=r'פונקציה מוגדרת למקוטעין',
         body=r'בכל קטע של $x$ יש נוסחה אחרת. משרטטים כל נוסחה רק בקטע שלה, ובודקים מה קורה בנקודות המעבר (נקודה מלאה או ריקה).',
         triggers=[r'מקוטעין']),
    dict(id='abs', sites={'calculus-1': 'ex2-s2'},
         title=r'ערך מוחלט $|x|$',
         body=r'$|x|=x$ אם $x\geq0$, ו-$|x|=-x$ אם $x<0$. כדי "לפתוח" ערך מוחלט מפרקים למקרים לפי הנקודה שבה הביטוי שבפנים מתאפס.',
         triggers=[r'ערך מוחלט|ערכים מוחלטים', BAR]),
    dict(id='floor', sites={'calculus-1': 'ex2-s5'},
         title=r'ערך שלם $[x]$',
         body=r'$[x]$ - המספר השלם הגדול ביותר שקטן או שווה ל-$x$. למשל $[2.7]=2$, $\ [-2.3]=-3$. הגרף נראה כמו מדרגות.',
         triggers=[r'ערך שלם|ערך השלם']),
    dict(id='mono', sites={'calculus-1': 'ex2-s6'},
         title=r'מונוטוניות',
         body=r'<b>עולה ממש:</b> $x_1<x_2\Rightarrow f(x_1)<f(x_2)$. <b>עולה (חלש):</b> $x_1<x_2\Rightarrow f(x_1)\leq f(x_2)$. '
              r'<b>יורדת ממש:</b> $x_1<x_2\Rightarrow f(x_1)>f(x_2)$.',
         triggers=[r'מונוטונ|עולה ממש|יורדת ממש|עולה חלש']),
    dict(id='injective', sites={'calculus-1': 'ex2-s9'},
         title=r'חד-חד-ערכית ו"על"',
         body=r'<b>חד-חד-ערכית:</b> $f(x_1)=f(x_2)\Rightarrow x_1=x_2$ - כל קו אופקי חותך את הגרף לכל היותר פעם אחת.<br>'
              r'<b>"על" $B$:</b> לכל $y\in B$ קיים $x$ עם $f(x)=y$ - התמונה היא כל $B$.',
         triggers=[r'חד-חד-ערכי|חח&quot;ע|חח"ע|"על"|&quot;על&quot;|״על״']),
]

# ---------------------------------------------------------------- helpers
def m(latex):
    x = convert(html.unescape(latex))
    x = x.replace('<mi>&#x000B1;</mi>', '<mo>&#x000B1;</mo>')
    return x.replace('<math ', '<math dir="ltr" ', 1)


def mathify(s):
    return re.sub(r'\$(.+?)\$', lambda g: m(g.group(1)), s)


def section_titles(page):
    out = {}
    for hid, attrs, txt in re.findall(r'<h3 class="q" id="([^"]+)"([^>]*)>(.*?)</h3>', page, re.S):
        plain = re.search(r'data-plain="([^"]*)"', attrs)
        if plain:
            out[hid] = html.unescape(plain.group(1)).strip()
        else:
            t = re.sub(r'<annotation[^>]*>.*?</annotation>', '', txt, flags=re.S)
            out[hid] = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', t))).strip()
    return out


REM_RE = re.compile(r'\n?\s*<!-- rem:start -->.*?<!-- rem:end -->', re.S)


def sections(page):
    """[(id, start_of_h3, end_of_h3_tag, end_of_section_content)]"""
    hs = [(mm.group(1), mm.start(), mm.end()) for mm in re.finditer(r'<h3 class="q" id="([^"]+)"[^>]*>.*?</h3>', page, re.S)]
    out = []
    for k, (hid, a, b) in enumerate(hs):
        nxt = hs[k + 1][1] if k + 1 < len(hs) else len(page)
        stop = min([x for x in (page.find('<div class="summary-sheet', b), page.find('</section>', b)) if x != -1] + [nxt])
        out.append((hid, a, b, stop))
    return out


def used_concepts(site, hid, seg):
    seg = REM_RE.sub('', seg)
    seg = re.sub(r'<div class="src-tag[^"]*">.*?</div>', '', seg, flags=re.S)
    seg = re.sub(r'<annotation[^>]*>.*?</annotation>', '', seg, flags=re.S)
    found = []
    for c in LIBRARY:
        if site not in c['sites']:
            continue
        if c['sites'][site] == hid:
            continue                           # the section that explains this concept
        if any(re.search(t, seg, re.S) for t in c['triggers']):
            found.append(c)
    return found[:MAX_PER_SECTION]


def box(site, items, titles_by_site):
    rows = ''
    for c in items:
        home = c['sites'].get(site)
        link = ''
        if home and home in titles_by_site[site]:
            link = f'<a class="rem-link" href="#{home}">↩ ההסבר המלא: {html.escape(titles_by_site[site][home])}</a>'
        elif c.get('link_other', {}).get(site):
            osite, oid = c['link_other'][site]
            t = titles_by_site.get(osite, {}).get(oid, '')
            link = f'<a class="rem-link" href="../{osite}/#{oid}">↩ ההסבר המלא באתר החומר התיאורטי: {html.escape(t)}</a>'
        rows += (f'<div class="rem-item"><button type="button" class="rem-toggle" aria-expanded="true">'
                 f'<span>{mathify(c["title"])}</span></button>'
                 f'<div class="rem-body">{mathify(c["body"])}{("<br>" + link) if link else ""}</div></div>')
    return ('\n      <!-- rem:start --><div class="rem-box" role="note" aria-label="תזכורות לסעיף הזה">'
            '<div class="rem-head">🔁 תזכורות לסעיף הזה <span>לחצי על מושג כדי לפתוח אותו</span></div>'
            + rows + '</div><!-- rem:end -->')


ASSETS = '''<!-- rem-assets:start -->
<style>
  /* תזכורות: מושגים מסעיפים אחרים שהסעיף משתמש בהם */
  .rem-box{ margin:8px 0 20px; max-width:80ch; border:1.5px solid #8A9BC4; border-radius:12px; background:#F5F7FC; overflow:hidden; }
  .rem-head{ display:flex; flex-wrap:wrap; align-items:baseline; gap:4px 10px; padding:8px 14px; background:#5D6F9E; color:#fff; font-weight:700; font-size:.95rem; }
  .rem-head span{ font-weight:400; font-size:.82rem; opacity:.9; }
  .rem-item + .rem-item{ border-top:1px solid #DCE2EF; }
  .rem-toggle{ width:100%; display:flex; align-items:center; justify-content:space-between; gap:10px; min-height:44px; padding:6px 14px;
    background:none; border:0; font:inherit; font-weight:600; font-size:.97rem; color:#1F2A47; cursor:pointer; text-align:right; }
  .rem-toggle::after{ content:"▾"; color:#A8791E; font-size:.85rem; flex:0 0 auto; }
  .rem-toggle[aria-expanded="false"]::after{ content:"◂"; }
  .rem-toggle:focus-visible{ outline:3px solid #A8791E; outline-offset:-3px; border-radius:8px; }
  .rem-body{ padding:2px 16px 12px; font-size:.95rem; line-height:1.75; overflow-x:auto; }
  .rem-body[hidden]{ display:none; }
  .rem-link{ display:inline-block; margin-top:6px; font-size:.88rem; font-weight:600; color:#2C3A5E; }
  @media print{ .rem-body[hidden]{ display:block; } .rem-toggle::after{ content:""; } }
</style>
<script>
(function(){
  try {
    document.querySelectorAll('.rem-box .rem-toggle').forEach(function(b){
      var body = b.nextElementSibling;
      b.setAttribute('aria-expanded', 'false'); body.hidden = true;
      b.addEventListener('click', function(){
        var open = b.getAttribute('aria-expanded') === 'true';
        b.setAttribute('aria-expanded', String(!open)); body.hidden = open;
      });
    });
  } catch(err){}
})();
</script>
<!-- rem-assets:end -->
'''


def apply(site, page, titles_by_site, report=None):
    page = REM_RE.sub('', page)
    secs = sections(page)
    out, last = [], 0
    for hid, a, b, stop in secs:
        items = used_concepts(site, hid, page[b:stop])
        if report is not None:
            report.append((site, hid, [c['id'] for c in items]))
        if not items:
            continue
        ins = b
        mm = re.match(r'\s*<div class="src-tag[^"]*">.*?</div>', page[b:stop], re.S)
        if mm:
            ins = b + mm.end()
        out.append(page[last:ins]); out.append(box(site, items, titles_by_site)); last = ins
    out.append(page[last:])
    page = ''.join(out)
    # keep the smart-search catalog clean: skip reminder boxes when building section summaries
    page = page.replace("if(!el.classList.contains('box-q') && snippet.length<260)",
                        "if(!el.classList.contains('box-q') && !el.classList.contains('rem-box') && snippet.length<260)")
    a = page.find('<!-- rem-assets:start -->')
    if a != -1:
        b = page.index('<!-- rem-assets:end -->') + len('<!-- rem-assets:end -->\n')
        page = page[:a] + page[b:]
    i = page.rindex('</body>')
    return page[:i] + ASSETS + page[i:]


def main():
    pages = {s: open(os.path.join(ROOT, s, 'index.html'), encoding='utf-8').read() for s in SITES}
    titles = {s: section_titles(p) for s, p in pages.items()}
    report = []
    for s in SITES:
        new = apply(s, pages[s], titles, report)
        if '--report' not in sys.argv:
            open(os.path.join(ROOT, s, 'index.html'), 'w', encoding='utf-8').write(new)
    for site, hid, ids in report:
        print(f'{site:18} {hid:8} {titles[site].get(hid, "")[:46]:48} -> {", ".join(ids) or "-"}')
    if '--report' not in sys.argv:
        print('written:', ', '.join(SITES))


if __name__ == '__main__':
    main()
