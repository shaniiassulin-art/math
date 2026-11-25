# -*- coding: utf-8 -*-
# מבחני חזרה - חשבון דיפרנציאלי ואינטגרלי 1 (96002): 9 מבחנים, תשפ"א-תשפ"ה.
# שאלה שהופיעה בכמה מבחנים מופיעה פעם אחת, ו-also מפרט את שאר המבחנים שבהם הופיעה.
# שאלה שכתוב בה "אין קשר בין הסעיפים" מפוצלת לפריטים נפרדים, כדי שאפשר יהיה לסנן לפי נושא.
# כל החישובים נבדקו (sympy).

SUBJECT = 'חדו״א 1'

EXAMS = [('21A', 'מועד א תשפ״א'), ('22A', 'מועד א תשפ״ב'), ('22B', 'מועד ב תשפ״ב'), ('23A', 'מועד א תשפ״ג'),
         ('23B', 'מועד ב תשפ״ג'), ('24A', 'מועד א תשפ״ד'), ('24S', 'מבחן דוגמה תשפ״ד'), ('25A', 'מועד א תשפ״ה'),
         ('25S', 'מבחן דוגמה תשפ״ה')]

TOPICS = [
    ('limits', 'גבולות'),
    ('cont', 'רציפות ומשפט ערך הביניים'),
    ('deriv', 'נגזרות, גזירות וישר משיק'),
    ('mvt', 'משפטי רול ולגראנז׳ ואי-שוויונות'),
    ('analysis', 'חקירת פונקציה: עלייה, קיצון, קמירות, אסימפטוטות'),
    ('indef', 'אינטגרל לא מסוים: הצבה, חלקים, שברים חלקיים'),
    ('definite', 'אינטגרל מסוים, שטח ופונקציה צוברת'),
    ('improper', 'אינטגרל מוכלל'),
]


def opts(*xs):
    return '§§OPTS§§' + '|||'.join(xs)


Q = [
# ============================================================== מועד א תשפ"א
dict(id='21A-m1', exam='21A', num='שאלה 1 (אמריקאית)', pts=8, topics=['analysis'], level=2, mc=True,
  q=r'נתונה $f(x)=x^2a^x$, $\ a>1$ פרמטר. מי מהטענות נכונה? '
    + opts(r'אם $a=e$ אז לכל $x<0$ מתקיים $f(x)\leq\frac4{e^2}$', r'לכל $a>1$, $f$ חד-חד ערכית בקטע $(-\infty,0)$',
           r'$g(x)=\frac1{f(x)}$ יורדת בקטע $\left(\frac{-2}{\ln a},0\right)$', r'$f$ עולה בקטע $\left[\frac{-2}{\ln a},0\right]$', r'$f$ לא גזירה ב-$x=0$'),
  steps=[
    (r'הנגזרת', [
      r'$$f^{\prime}(x)=2xa^x+x^2a^x\ln a=xa^x(2+x\ln a)$$',
      r'= | $f^{\prime}=0$ ב-$x=0$ וב-$x=-\frac2{\ln a}$',
      r'= עולה | $\left(-\infty,-\frac2{\ln a}\right)$ ו-$(0,\infty)$',
      r'= יורדת | $\left(-\frac2{\ln a},0\right)$']),
    (r'בודקים את א ($a=e$)', [
      r'בתחום $x<0$ המקסימום הוא ב-$x=-2$: $f(-2)=4e^{-2}$, וכש-$x\to-\infty$ $f\to0$. לכן $f(x)\leq\frac4{e^2}$ ✓']),
    (r'שאר הטענות', [
      r'= ב | עולה ואז יורדת ב-$(-\infty,0)$ - לא חח"ע ✗',
      r'= ג | $f$ יורדת שם ⇒ $\frac1f$ עולה ✗',
      r'= ד | שם $f$ יורדת ✗',
      r'= ה | $f$ גזירה בכל מקום ✗']),
  ],
  ans=r'א'),

dict(id='21A-m2', exam='21A', num='שאלה 2 (אמריקאית)', pts=8, topics=['limits'], level=2, mc=True,
  q=r'$a,b>0$. מהו $\lim_{x\to a}\left(\frac xa\right)^{\frac b{x-a}}$? '
    + opts(r'$e^{b/a}$ לכל $a,b>0$', r'$e^{-b/a}$ לכל $a,b>0$', r'הגבול קיים רק אם $a\neq1$', r'$\infty$ לכל $a,b>0$', r'$0$ לכל $a,b>0$'),
  steps=[
    (r'גבול מסוג $1^\infty$ - דרך $e^{\ln}$', [
      r'↓ $\left(\frac xa\right)^{\frac b{x-a}}=e^{\frac{b\ln(x/a)}{x-a}}$',
      r'↓ $\lim_{x\to a}\frac{\ln x-\ln a}{x-a}=(\ln x)^{\prime}\big|_{x=a}=\frac1a$ | הגדרת הנגזרת',
      r'↓ הגבול $=e^{b/a}$']),
  ],
  ans=r'א'),

dict(id='21A-m3', exam='21A', num='שאלה 3 (אמריקאית)', pts=8, topics=['definite', 'deriv'], level=2, mc=True,
  q=r'$f(x)=(\cos\pi x)\cdot\int_1^{x^3}\frac{\cos\left(\frac\pi4t\right)}{t^2+1}\,dt$. הערך של $f^{\prime}(1)$ הוא: '
    + opts(r'$-\frac34\sqrt2$', r'$0$', r'$f$ לא גזירה ב-1', r'$-\frac12$', r'$\frac12$'),
  steps=[
    (r'כלל המכפלה והמשפט היסודי', [
      r'$$f^{\prime}(x)=-\pi\sin(\pi x)\int_1^{x^3}\dots\,dt+\cos(\pi x)\cdot\frac{\cos\left(\frac\pi4x^3\right)}{x^6+1}\cdot3x^2$$']),
    (r'מציבים $x=1$', [
      r'האינטגרל מ-1 עד 1 הוא 0, ו-$\cos\pi=-1$:',
      r'$$f^{\prime}(1)=-1\cdot\frac{\cos\frac\pi4}{2}\cdot3=-\frac{3\sqrt2}{4}$$']),
  ],
  ans=r'א'),

dict(id='21A-m4', exam='21A', num='שאלה 4 (אמריקאית)', pts=8, topics=['analysis'], level=2, mc=True,
  q=r'$f(x)=\frac{e^x}{\ln^2x+e^{2x}}$. מי מהטענות נכונה? '
    + opts(r'$y=0$ אסימפטוטה אופקית של $f$', r'$f$ מוגדרת לכל $x$', r'$x=0$ אסימפטוטה אנכית', r'$x=1$ אסימפטוטה אנכית', r'$y=3$ אסימפטוטה אופקית'),
  steps=[
    (r'תחום', [
      r'$\ln x$ מוגדר רק ל-$x>0$, והמכנה חיובי שם - תחום $x>0$.']),
    (r'קצוות התחום', [
      r'= $x\to0^+$ | $\ln^2x\to\infty$ ⇒ $f\to0$: אין אסימפטוטה אנכית',
      r'= $x\to\infty$ | $f\approx\frac{e^x}{e^{2x}}=e^{-x}\to0$ ⇒ $y=0$ אופקית ✓']),
  ],
  ans=r'א'),

dict(id='21A-m5', exam='21A', num='שאלה 5 (אמריקאית)', pts=8, topics=['improper'], level=1, mc=True,
  q=r'$\int_4^\infty\frac{ax^2+bx}{x^3+2}\,dx$, $\ a,b\geq0$. מי מהטענות נכונה? '
    + opts(r'אם $a=0,b=5$ האינטגרל מתכנס', r'אם $a=5,b=1$ מתכנס', r'אם $a=5,b=0$ מתכנס', r'אם $a=0,b=1$ מתבדר', r'אם $a=0,b=0$ מתבדר'),
  steps=[
    (r'השוואה גבולית', [
      r'= $a>0$ | $\frac{ax^2+bx}{x^3+2}\sim\frac ax$ ⇒ מתבדר',
      r'= $a=0,\ b>0$ | $\sim\frac b{x^2}$ ⇒ מתכנס',
      r'= $a=b=0$ | האינטגרנד 0 ⇒ מתכנס (ל-0)']),
  ],
  ans=r'א'),

dict(id='21A-m6', exam='21A', num='שאלה 6 (אמריקאית)', pts=8, topics=['cont', 'limits'], level=2, mc=True,
  q=r'$f(x)=\frac{\arcsin(bx)}x$ ל-$0<x\leq\frac1b$, $\ f(0)=a$, $\ f(x)=\frac{e^{-x}-e^x}{\ln(1-x)}$ ל-$x<0$; $a,b>0$. מי מהטענות נכונה? '
    + opts(r'לא יתכן ש-$x=0$ נקודת אי-רציפות מסוג שני', r'אם $a=2,b=2$ אז $x=0$ אי-רציפות סליקה', r'אם $a=2,b=1$ אז $f$ רציפה ב-0',
           r'אם $a=1,b=2$ אז $x=0$ אי-רציפות מסוג ראשון', r'אם $a=2,b=2$ אז $x=0$ אי-רציפות מסוג ראשון'),
  steps=[
    (r'הגבולות החד-צדדיים', [
      r'= $x\to0^+$ | $\frac{\arcsin bx}x\to b$',
      r'= $x\to0^-$ | $\frac{e^{-x}-e^x}{\ln(1-x)}\approx\frac{-2x}{-x}=2$']),
    (r'מסקנות', [
      r'שני הגבולות תמיד סופיים ⇒ אף פעם לא מסוג שני ✓ (א).',
      r'= $a=b=2$ | רציפה (ב, ה ✗)',
      r'= $a=2,b=1$ | קפיצה (ג ✗)',
      r'= $a=1,b=2$ | הגבולות שווים ל-2 ≠ 1: סליקה (ד ✗)']),
  ],
  ans=r'א'),

dict(id='21A-8', exam='21A', num='שאלה 8', pts=18, topics=['analysis'], level=2,
  q=r'נתונה $f(x)=\left(\sqrt[3]{x^2}-4\right)^2$. (8.1) מצאו תחומי עלייה, ירידה ונקודות קיצון מקומיות. (8.2) מצאו את כל ערכי $m$ שעבורם למשוואה $f(x)=m$ יש בדיוק 2 פתרונות.',
  steps=[
    (r'הנגזרת', [
      r'$$f^{\prime}(x)=2\left(x^{\frac23}-4\right)\cdot\frac23x^{-\frac13}=\frac{4\left(x^{\frac23}-4\right)}{3\sqrt[3]x}$$',
      r'= | $f^{\prime}=0$ ב-$x^{\frac23}=4$, כלומר $x=\pm8$',
      r'= | $f^{\prime}$ לא מוגדרת ב-$x=0$ (אבל $f$ רציפה שם)']),
    (r'טבלת סימנים', [
      r'= $x<-8$ | $f^{\prime}<0$ - יורדת',
      r'= $-8<x<0$ | $f^{\prime}>0$ - עולה',
      r'= $0<x<8$ | $f^{\prime}<0$ - יורדת',
      r'= $x>8$ | $f^{\prime}>0$ - עולה']),
    (r'קיצון', [
      r'= מינימום | $(\pm8,\ 0)$',
      r'= מקסימום מקומי | $(0,\ 16)$ - נקודה שבה $f$ לא גזירה']),
    (r'(8.2) לפי הגרף ($f$ זוגית, $f\to\infty$ באינסוף)', [
      r'= $m<0$ | אין פתרון',
      r'= $m=0$ | 2 פתרונות ($\pm8$) ✓',
      r'= $0<m<16$ | 4 פתרונות',
      r'= $m=16$ | 3 פתרונות',
      r'= $m>16$ | 2 פתרונות ✓']),
  ],
  ans=r'עולה ב-$(-8,0)\cup(8,\infty)$, יורדת ב-$(-\infty,-8)\cup(0,8)$; מינימום $(\pm8,0)$, מקסימום $(0,16)$; $\ m=0$ או $m>16$'),

dict(id='21A-9', exam='21A', num='שאלה 9', pts=18, topics=['cont'], level=1,
  q=r'תהי $f$ רציפה ב-$\mathbb{R}$. הוכיחו כי למשוואה $x+2\sin f(x)=1$ יש פתרון בקטע $[-2,3]$.',
  steps=[
    (r'פונקציית עזר', [
      r'$g(x)=x+2\sin f(x)-1$ - רציפה (הרכבה וסכום של רציפות).']),
    (r'סימנים בקצוות', [
      r'= | $g(-2)=-3+2\sin f(-2)\leq-1<0$',
      r'= | $g(3)=2+2\sin f(3)\geq0$']),
    (r'משפט ערך הביניים', [
      r'אם $g(3)=0$ - סיימנו. אחרת $g(3)>0>g(-2)$, ולפי משפט ערך הביניים יש $c\in(-2,3)$ עם $g(c)=0$.']),
  ],
  ans=r'יש $c\in[-2,3]$ עם $c+2\sin f(c)=1$'),

dict(id='21A-10', exam='21A', num='שאלה 10', pts=18, topics=['improper', 'indef'], level=2,
  q=r'הוכיחו שהאינטגרל המוכלל $\int_e^\infty\frac{\ln x}{x^2}\,dx$ מתכנס וחשבו את ערכו.',
  steps=[
    (r'אינטגרציה בחלקים', [
      r'$u=\ln x,\ v^{\prime}=x^{-2}$:',
      r'$$\int\frac{\ln x}{x^2}dx=-\frac{\ln x}x+\int\frac1{x^2}dx=-\frac{\ln x+1}x+C$$']),
    (r'הגבול', [
      r'↓ $\int_e^R\frac{\ln x}{x^2}dx=-\frac{\ln R+1}R+\frac2e$',
      r'↓ $R\to\infty$: $\frac{\ln R}R\to0$ | לופיטל',
      r'↓ האינטגרל מתכנס ל-$\frac2e$']),
  ],
  ans=r'$\frac2e$'),

dict(id='21A-11', exam='21A', num='שאלה 11', pts=18, topics=['definite', 'indef'], level=2,
  q=r'חשבו את $\int_1^3\frac{x}{x^2-6x+13}\,dx$.',
  steps=[
    (r'השלמה לריבוע ופירוק המונה', [
      r'↓ $x^2-6x+13=(x-3)^2+4$',
      r'↓ $x=(x-3)+3$']),
    (r'שני אינטגרלים', [
      r'= | $\int\frac{x-3}{(x-3)^2+4}dx=\frac12\ln\left((x-3)^2+4\right)$',
      r'= | $\int\frac3{(x-3)^2+4}dx=\frac32\arctan\frac{x-3}2$']),
    (r'מציבים גבולות', [
      r'↓ $\frac12(\ln4-\ln8)+\frac32\left(0-\arctan(-1)\right)$',
      r'↓ $=-\frac12\ln2+\frac{3\pi}8$']),
  ],
  ans=r'$\frac{3\pi}8-\frac12\ln2$'),

# ============================================================== מועד א תשפ"ב
dict(id='22A-m1', exam='22A', num='שאלה 1 (אמריקאית)', pts=8, topics=['cont', 'definite'], level=3, mc=True,
  q=r'$f(x)=\frac{\int_0^{x^2}4\sin(t^3)dt}{x^8}$ ל-$x>0$, $\ f(0)=a$, $\ f(x)=\frac{\ln(1+2x)}x+b$ ל-$x<0$. '
    r'(A) אם $a\neq1,b=-1$ אז $x=0$ סליקה. (B) אין $a,b$ שעבורם $f$ רציפה ב-0. (C) אם $b\neq-1$ אז $x=0$ קפיצה. מי נכונה? '
    + opts(r'נכונות: A, C; שגויה: B', r'נכונה: A; שגויות: B, C', r'נכונות: A, B; שגויה: C', r'כולן שגויות', r'כולן נכונות'),
  steps=[
    (r'הגבול מימין - לופיטל והמשפט היסודי', [
      r'$$\lim_{x\to0^+}\frac{4\sin(x^6)\cdot2x}{8x^7}=\lim\frac{\sin(x^6)}{x^6}=1$$']),
    (r'הגבול משמאל', [
      r'$\frac{\ln(1+2x)}x\to2$, ולכן הגבול $2+b$.']),
    (r'בודקים', [
      r'= A | $b=-1$: שני הגבולות 1, $f(0)=a\neq1$ ⇒ סליקה ✓',
      r'= B | $a=1,b=-1$ - רציפה ✗',
      r'= C | $b\neq-1$: גבולות סופיים ושונים ⇒ קפיצה ✓']),
  ],
  ans=r'א'),

dict(id='22A-m2', exam='22A', num='שאלה 2 (אמריקאית)', pts=8, topics=['deriv'], level=1, mc=True, also=['24S', '25S'],
  q=r'$f$ גזירה, $f(3)=3$, $f^{\prime}(3)=2$, ו-$g(x)=\sqrt{xf(x)-5}$. אז $g^{\prime}(3)$ שווה ל: '
    + opts(r'$\frac94$', r'$\frac32$', r'$0$', r'$\frac49$', r'$\frac23$'),
  steps=[
    (r'כלל השרשרת והמכפלה', [
      r'$$g^{\prime}(x)=\frac{f(x)+xf^{\prime}(x)}{2\sqrt{xf(x)-5}}$$',
      r'↓ $g^{\prime}(3)=\frac{3+3\cdot2}{2\sqrt{9-5}}=\frac94$']),
  ],
  ans=r'א'),

dict(id='22A-m3', exam='22A', num='שאלה 3 (אמריקאית)', pts=8, topics=['deriv'], level=1, mc=True, also=['24S'],
  q=r'הישר $y=x-3$ משיק לגרף $f(x)=x^4-ax^3+b$ ב-$x=1$. הערך של $a+b$: ' + opts(r'$-1$', r'$0$', r'$1$', r'$2$', r'$-2$'),
  steps=[
    (r'שני תנאים', [
      r'= שיפוע | $f^{\prime}(1)=4-3a=1\Rightarrow a=1$',
      r'= נקודה | $f(1)=1-a+b=-2\Rightarrow b=-2$',
      r'$a+b=-1$.']),
  ],
  ans=r'א'),

dict(id='22A-m4', exam='22A', num='שאלה 4 (אמריקאית)', pts=8, topics=['limits'], level=2, mc=True, also=['24S'],
  q=r'$f$ גזירה, $\lim_{x\to\infty}f(x)=\infty$, $\lim_{x\to\infty}f^{\prime}(x)=7$. אז $\lim_{x\to\infty}\left(1+\frac1{f(x)}\right)^x$ שווה ל: '
    + opts(r'$e^{1/7}$', r'$1$', r'$0$', r'$\infty$', r'$e^7$'),
  steps=[
    (r'גבול מסוג $1^\infty$', [
      r'↓ $\left(1+\frac1f\right)^x=\left[\left(1+\frac1f\right)^f\right]^{x/f}$',
      r'↓ $\lim\frac x{f(x)}=\lim\frac1{f^{\prime}(x)}=\frac17$ | לופיטל ($\frac\infty\infty$)',
      r'↓ הגבול $=e^{1/7}$']),
  ],
  ans=r'א'),

dict(id='22A-m5', exam='22A', num='שאלה 5 (אמריקאית)', pts=8, topics=['analysis'], level=2, mc=True,
  q=r'$f(x)=x+x\arctan x$. (A) $y=\left(1+\frac\pi2\right)x-1$ אסימפטוטה משופעת באינסוף. (B) $f$ קמורה (מחייכת) ב-$(0,\infty)$ וקעורה (עצובה) ב-$(-\infty,0)$. (C) $f$ קעורה ב-$(0,\infty)$ וקמורה ב-$(-\infty,0)$. מי נכונה? '
    + opts(r'נכונה: A; שגויות: B, C', r'נכונות: A, B; שגויה: C', r'נכונות: A, C; שגויה: B', r'כולן שגויות', r'נכונה: B; שגויות: A, C'),
  steps=[
    (r'(A)', [
      r'↓ $\frac{f(x)}x=1+\arctan x\to1+\frac\pi2$',
      r'↓ $f(x)-\left(1+\frac\pi2\right)x=x\left(\arctan x-\frac\pi2\right)=\frac{\arctan x-\frac\pi2}{1/x}\to-1$ | לופיטל',
      r'A נכונה.']),
    (r'(B), (C)', [
      r'$$f^{\prime\prime}(x)=\frac{2}{(1+x^2)^2}>0$$',
      r'$f$ קמורה (מחייכת) בכל הישר - B ו-C שגויות.']),
  ],
  ans=r'א'),

dict(id='22A-m6', exam='22A', num='שאלה 6 (אמריקאית)', pts=8, topics=['definite'], level=1, mc=True,
  q=r'מחשבים את $\int_1^8x\sqrt{3x+1}\,dx$ בהצבה $u=\sqrt{3x+1}$. מתקבל: '
    + opts(r'$\frac29\int_2^5(u^2-1)u^2\,du$', r'$\frac13\int_2^5(u^2-1)u\,du$', r'$\frac29\int_1^8(u^2-1)u\,du$', r'$\frac13\int_1^8(u^2-1)u^2\,du$', r'אף תשובה לא נכונה'),
  steps=[
    (r'ההצבה', [
      r'= | $x=\frac{u^2-1}3,\ \ dx=\frac{2u}3du$',
      r'= גבולות | $x=1\to u=2$, $\ x=8\to u=5$',
      r'↓ $x\sqrt{3x+1}\,dx=\frac{u^2-1}3\cdot u\cdot\frac{2u}3du=\frac29(u^2-1)u^2du$']),
  ],
  ans=r'א'),

dict(id='22A-7', exam='22A', num='שאלה 7', pts=18, topics=['cont', 'analysis'], level=2,
  q=r'$f(x)=x^{\frac1x}$ ל-$x>0$, $\ f(0)=0$. (א) הוכיחו ש-$f$ רציפה מימין ב-0. (ב) מצאו תחומי עלייה וירידה. (ג) האם יש ל-$f$ אסימפטוטה אופקית? אם כן, מהי?',
  steps=[
    (r'(א)', [
      r'↓ $x^{1/x}=e^{\frac{\ln x}x}$',
      r'↓ $x\to0^+$: $\frac{\ln x}x\to-\infty$ | $\ln x\to-\infty$, $\frac1x\to\infty$',
      r'↓ $f(x)\to0=f(0)$ ✓']),
    (r'(ב)', [
      r'$$f^{\prime}(x)=x^{\frac1x}\cdot\frac{1-\ln x}{x^2}$$',
      r'= עולה | $(0,e)$',
      r'= יורדת | $(e,\infty)$, מקסימום $e^{1/e}$ ב-$x=e$']),
    (r'(ג)', [
      r'$\frac{\ln x}x\to0$ כש-$x\to\infty$, ולכן $f\to e^0=1$: אסימפטוטה אופקית $y=1$ (ב-$+\infty$; התחום $x\geq0$).']),
  ],
  ans=r'עולה ב-$(0,e)$, יורדת ב-$(e,\infty)$; $\ y=1$'),

dict(id='22A-8', exam='22A', num='שאלה 8', pts=18, topics=['mvt'], level=2,
  q=r'$f$ גזירה ב-$\mathbb{R}$, $-2<f^{\prime}(x)<2$ לכל $x$, ו-$f(1)=3$. מצאו $\alpha,\beta$ כך ש-$\alpha<f(5)<\beta$.',
  steps=[
    (r'לגראנז׳ בקטע $[1,5]$', [
      r'יש $c\in(1,5)$ עם $f(5)-f(1)=4f^{\prime}(c)$.']),
    (r'חוסמים', [
      r'↓ $-8<4f^{\prime}(c)<8$',
      r'↓ $-8<f(5)-3<8\Rightarrow-5<f(5)<11$']),
  ],
  ans=r'$\alpha=-5,\ \beta=11$'),

dict(id='22A-9', exam='22A', num='שאלה 9', pts=18, topics=['indef', 'improper'], level=2,
  q=r'(א) חשבו $\int\frac{x-4}{(x+1)(x^2+4)}dx$. (ב) קבעו אם $\int_5^\infty\frac{x-4}{(x+1)(x^2+4)}dx$ מתכנס או מתבדר.',
  steps=[
    (r'(א) שברים חלקיים', [
      r'$$\frac{x-4}{(x+1)(x^2+4)}=\frac A{x+1}+\frac{Bx+C}{x^2+4}$$',
      r'= $x=-1$ | $-5=5A\Rightarrow A=-1$',
      r'= מקדם $x^2$ | $0=A+B\Rightarrow B=1$',
      r'= מקדם חופשי | $-4=4A+C\Rightarrow C=0$']),
    (r'האינטגרל', [
      r'$$-\ln|x+1|+\frac12\ln(x^2+4)+C=\ln\frac{\sqrt{x^2+4}}{|x+1|}+C$$']),
    (r'(ב)', [
      r'↓ $\ln\frac{\sqrt{x^2+4}}{x+1}\to\ln1=0$ כש-$x\to\infty$',
      r'↓ $\int_5^\infty=0-\ln\frac{\sqrt{29}}6=\ln\frac6{\sqrt{29}}$',
      r'מתכנס (גם בהשוואה: האינטגרנד $\sim\frac1{x^2}$).']),
  ],
  ans=r'(א) $-\ln|x+1|+\frac12\ln(x^2+4)+C$; (ב) מתכנס, $\ln\frac6{\sqrt{29}}$'),

dict(id='22A-10', exam='22A', num='שאלה 10', pts=18, topics=['indef'], level=2,
  q=r'חשבו $\int\sin^4(2x)\,dx$.',
  steps=[
    (r'הורדת חזקה', [
      r'↓ $\sin^2u=\frac{1-\cos2u}2$',
      r'↓ $\sin^4u=\frac{1-2\cos2u+\cos^22u}4=\frac{3-4\cos2u+\cos4u}8$',
      r'↓ $u=2x$ | $\sin^4(2x)=\frac{3-4\cos4x+\cos8x}8$']),
    (r'מבצעים אינטגרל', [
      r'$$\frac{3x}8-\frac{\sin4x}8+\frac{\sin8x}{64}+C$$']),
  ],
  ans=r'$\frac{3x}8-\frac{\sin4x}8+\frac{\sin8x}{64}+C$'),

# ============================================================== מועד ב תשפ"ב
dict(id='22B-m1', exam='22B', num='שאלה 1 (אמריקאית)', pts=8, topics=['cont', 'limits'], level=2, mc=True, also=['25S'],
  q=r'$f(x)=\frac{(x+5)\sin(x^2)}{1-\cos x}$ ל-$0<x<\frac\pi2$, $\ f(0)=a$, $\ f(x)=-\frac{\ln(1-10x)}x$ ל-$x<0$. (A) אם $a=10$, $f$ רציפה ב-0. (B) אם $a=8$, $x=0$ סליקה. (C) $x=0$ קפיצה. מי נכונה? '
    + opts(r'נכונות: A, B; שגויה: C', r'נכונה: A; שגויות: B, C', r'נכונה: B; שגויות: A, C', r'כולן שגויות', r'נכונה: C; שגויות: A, B'),
  steps=[
    (r'הגבולות', [
      r'= $x\to0^+$ | $1-\cos x\approx\frac{x^2}2$ ⇒ $\frac{5x^2}{x^2/2}=10$',
      r'= $x\to0^-$ | $-\frac{-10x}x=10$']),
    (r'מסקנה', [
      r'הגבול 10 משני הצדדים: $a=10$ רציפה (A ✓), $a\neq10$ סליקה (B ✓), אף פעם לא קפיצה (C ✗).']),
  ],
  ans=r'א'),

dict(id='22B-m2', exam='22B', num='שאלה 2 (אמריקאית)', pts=8, topics=['mvt', 'cont'], level=2, mc=True, also=['25S'],
  q=r'$f$ רציפה ב-$[0,\pi]$, גזירה ב-$(0,\pi)$, $f(0)=f(\pi)=0$, $g(x)=\sin x+f(x)$. (A) יש $c\in(0,\pi)$ עם $g^{\prime}(c)=0$ (רול). (B) יש $c\in(0,\pi)$ עם $g(c)=0$ (ערך הביניים). (C) $g(x)>f(x)$ לכל $x\in(0,\pi)$. מי נכונה? '
    + opts(r'נכונות: A, C; שגויה: B', r'נכונה: A; שגויות: B, C', r'נכונה: B; שגויות: A, C', r'כולן נכונות', r'נכונה: C; שגויות: A, B'),
  steps=[
    (r'בודקים', [
      r'= A | $g(0)=g(\pi)=0$, רציפה וגזירה ⇒ רול ✓',
      r'= B | דוגמה נגדית: $f\equiv0$, אז $g=\sin x>0$ ב-$(0,\pi)$ ✗',
      r'= C | $g-f=\sin x>0$ ✓']),
  ],
  ans=r'א'),

dict(id='22B-m3', exam='22B', num='שאלה 3 (אמריקאית)', pts=8, topics=['deriv'], level=2, mc=True,
  q=r'$f(x)=x^2\sin\frac1x$ ל-$x\neq0$, $f(0)=0$. הערך של $f^{\prime}(0)+f^{\prime}\left(\frac1\pi\right)$: '
    + opts(r'$1$', r'$0$', r'לא קיים, $f$ לא גזירה ב-0', r'$\pi$', r'$\frac1\pi$'),
  steps=[
    (r'$f^{\prime}(0)$ לפי ההגדרה', [
      r'$$f^{\prime}(0)=\lim_{h\to0}\frac{h^2\sin\frac1h}h=\lim h\sin\frac1h=0$$']),
    (r'$f^{\prime}\left(\frac1\pi\right)$', [
      r'↓ $f^{\prime}(x)=2x\sin\frac1x-\cos\frac1x$',
      r'↓ $f^{\prime}\left(\frac1\pi\right)=\frac2\pi\sin\pi-\cos\pi=1$']),
  ],
  ans=r'א'),

dict(id='22B-m4', exam='22B', num='שאלה 4 (אמריקאית)', pts=8, topics=['deriv'], level=2, mc=True, also=['25S'],
  q=r'$f(x)=(2+\cos x)^{x^2+x}$, ו-$y=ax+b$ משיק לגרף בנקודה $(0,1)$. $y(2)$ שווה ל: '
    + opts(r'$1+2\ln3$', r'$2+3\ln3$', r'$2+4\ln3$', r'$\ln3$', r'$4\ln3$'),
  steps=[
    (r'גזירה לוגריתמית', [
      r'$$\frac{f^{\prime}}f=(2x+1)\ln(2+\cos x)-\frac{(x^2+x)\sin x}{2+\cos x}$$',
      r'↓ $f^{\prime}(0)=1\cdot\ln3=\ln3$',
      r'↓ $y=x\ln3+1\Rightarrow y(2)=1+2\ln3$']),
  ],
  ans=r'א'),

dict(id='22B-m5', exam='22B', num='שאלה 5 (אמריקאית)', pts=8, topics=['definite', 'analysis'], level=2, mc=True, also=['25S'],
  q=r'$f(x)=\int_0^{x^2-3x}e^{t^2}dt$. מי נכונה? '
    + opts(r'$\lim_{x\to0}\frac{f(x)}x=-3$', r'$x=\frac32$ מקסימום מקומי', r'$x=\frac32$ נקודת פיתול', r'$f$ מתאפסת רק ב-$x=0$', r'ציר $y$ אסימפטוטה אנכית'),
  steps=[
    (r'הנגזרת', [
      r'$$f^{\prime}(x)=e^{(x^2-3x)^2}(2x-3)$$']),
    (r'בודקים', [
      r'= א | $\lim\frac{f(x)}x=f^{\prime}(0)=-3$ ✓ (כי $f(0)=0$)',
      r'= ב | $f^{\prime}$ עוברת מ-$-$ ל-$+$ ב-$\frac32$: מינימום ✗',
      r'= ד | $f=0$ גם ב-$x=3$ ✗']),
  ],
  ans=r'א'),

dict(id='22B-m6', exam='22B', num='שאלה 6 (אמריקאית)', pts=8, topics=['improper'], level=1, mc=True, also=['25S'],
  q=r'$\int_0^\infty\frac{x}{(3x^2+1)^4}dx$: ' + opts(r'מתכנס ל-$\frac1{18}$', r'מתכנס ל-0', r'מתכנס ל-$-\frac13$', r'מתכנס ל-1', r'מתבדר'),
  steps=[
    (r'פונקציה קדומה', [
      r'$$\int\frac x{(3x^2+1)^4}dx=-\frac1{18(3x^2+1)^3}+C$$',
      r'↓ $\int_0^R=\frac1{18}-\frac1{18(3R^2+1)^3}\to\frac1{18}$']),
  ],
  ans=r'א'),

dict(id='22B-7', exam='22B', num='שאלה 7', pts=18, topics=['analysis'], level=2, also=['25S'],
  q=r'$f(x)=\frac{\ln x}x$. (א) מצאו תחומי עלייה/ירידה ונקודות קיצון. (ב) מצאו תחומי קמירות/קעירות ונקודות פיתול.',
  steps=[
    (r'(א)', [
      r'$$f^{\prime}(x)=\frac{1-\ln x}{x^2}$$',
      r'= עולה | $(0,e)$',
      r'= יורדת | $(e,\infty)$',
      r'= מקסימום | $\left(e,\frac1e\right)$']),
    (r'(ב)', [
      r'$$f^{\prime\prime}(x)=\frac{2\ln x-3}{x^3}$$',
      r'= קעורה | $\left(0,e^{3/2}\right)$',
      r'= קמורה | $\left(e^{3/2},\infty\right)$',
      r'= פיתול | $\left(e^{3/2},\ \frac3{2e^{3/2}}\right)$']),
  ],
  ans=r'מקסימום $\left(e,\frac1e\right)$; פיתול ב-$x=e^{3/2}$'),

dict(id='22B-8', exam='22B', num='שאלה 8', pts=18, topics=['cont'], level=1, also=['25S'],
  q=r'$f:[0,1]\to[0,2]$ רציפה. הוכיחו שיש $a\in[0,1]$ עם $f(a)=2a^2$. (הדרכה: $g(x)=f(x)-2x^2$.)',
  steps=[
    (r'הקצוות', [
      r'= | $g(0)=f(0)\geq0$',
      r'= | $g(1)=f(1)-2\leq0$ (כי $f(1)\leq2$)']),
    (r'ערך הביניים', [
      r'$g$ רציפה. אם אחד הקצוות 0 - סיימנו; אחרת $g(0)>0>g(1)$ ויש $a$ עם $g(a)=0$, כלומר $f(a)=2a^2$.']),
  ],
  ans=r'קיימת (משפט ערך הביניים על $g$)'),

dict(id='22B-9', exam='22B', num='שאלה 9', pts=18, topics=['limits'], level=2, also=['25S'],
  q=r'חשבו $\lim_{x\to\infty}\left(\frac{x^2+x+3}{x^2+9}\right)^{2x}$.',
  steps=[
    (r'כותבים כ-$1+$משהו', [
      r'↓ $\frac{x^2+x+3}{x^2+9}=1+\frac{x-6}{x^2+9}$',
      r'↓ $\lim2x\cdot\frac{x-6}{x^2+9}=2$',
      r'↓ הגבול $=e^2$']),
  ],
  ans=r'$e^2$'),

dict(id='22B-10', exam='22B', num='שאלה 10', pts=18, topics=['definite'], level=2, also=['25S'],
  q=r'חשבו $\int_{\ln\frac\pi2}^{\ln\pi}e^{2x}\sin(e^x)\,dx$.',
  steps=[
    (r'הצבה $t=e^x$', [
      r'= | $dt=e^xdx$, $\ e^{2x}dx=t\,dt$',
      r'= גבולות | $\frac\pi2\to\pi$',
      r'$$\int_{\pi/2}^\pi t\sin t\,dt$$']),
    (r'בחלקים', [
      r'↓ $\left[-t\cos t+\sin t\right]_{\pi/2}^{\pi}$',
      r'↓ $=(\pi+0)-(0+1)=\pi-1$']),
  ],
  ans=r'$\pi-1$'),

# ============================================================== מועד א תשפ"ג
dict(id='23A-m1', exam='23A', num='שאלה 1 (אמריקאית)', pts=8, topics=['cont', 'limits'], level=2, mc=True,
  q=r'$f(x)=x^2\arctan\frac1x+\frac{a^2\sin2x}x$ ל-$x>0$, $\ f(x)=\frac{|ax|\ln(x^2+1)}{ax}+2$ ל-$x<0$. מי נכונה? '
    + opts(r'לא קיים $a$ שעבורו $x=0$ אי-רציפות ממין 2', r'לכל $a$ יש ב-0 אי-רציפות ממין ראשון', r'אם $a=0.5$, $f$ רציפה ב-0', r'אם $a=-0.5$, $x=0$ סליקה'),
  steps=[
    (r'הגבולות', [
      r'= $x\to0^+$ | $0+2a^2$',
      r'= $x\to0^-$ | $\pm\ln(x^2+1)+2\to2$']),
    (r'מסקנה', [
      r'שני הגבולות תמיד סופיים - אף פעם לא ממין 2 ✓. ($f$ לא מוגדרת ב-0, ולכן ג ✗; עם $a=\pm1$ הגבולות שווים - ב ✗; $a=-0.5$: $0.5\neq2$ - ד ✗.)']),
  ],
  ans=r'א'),

dict(id='23A-m2', exam='23A', num='שאלה 2 (אמריקאית)', pts=8, topics=['definite', 'deriv'], level=1, mc=True,
  q=r'$f(x)=\int_1^{x^3}\frac1{1+\ln t}dt$ בתחום $[1,\infty)$. ' + opts(r'$f^{\prime}(2)=\frac{12}{1+\ln8}$', r'$f^{\prime}(2)=\frac1{1+\ln8}$', r'$f^{\prime}(2)=\frac1{1+\ln2}$', r'$f^{\prime}(2)=\frac{12}{1+\ln2}$'),
  steps=[
    (r'המשפט היסודי וכלל השרשרת', [
      r'↓ $f^{\prime}(x)=\frac{3x^2}{1+\ln x^3}$',
      r'↓ $f^{\prime}(2)=\frac{12}{1+\ln8}$']),
  ],
  ans=r'א'),

dict(id='23A-m3', exam='23A', num='שאלה 3 (אמריקאית)', pts=8, topics=['deriv'], level=2, mc=True,
  q=r'משוואת המשיק ל-$f(x)=x^{x\ln x}$ בנקודה $x=1$ היא: ' + opts(r'$y=1$', r'$y=x+1$', r'$y=x-1$', r'$y=0$'),
  steps=[
    (r'גזירה לוגריתמית', [
      r'↓ $\ln f=x\ln^2x$',
      r'↓ $\frac{f^{\prime}}f=\ln^2x+2\ln x$',
      r'↓ $f(1)=1,\ \ f^{\prime}(1)=1\cdot0=0$ | המשיק $y=1$']),
  ],
  ans=r'א'),

dict(id='23A-m4', exam='23A', num='שאלה 4 (אמריקאית)', pts=8, topics=['limits'], level=2, mc=True,
  q=r'נתון $\lim_{x\to0}\left(\frac{2-x}{a+x}\right)^{\frac3x}=e^b$. אז בהכרח: ' + opts(r'$a=2,\ b=-3$', r'$a=0,\ b=3$', r'$a=2,\ b=3$', r'$a=0,\ b=0$'),
  steps=[
    (r'הבסיס חייב לשאוף ל-1', [
      r'אחרת הגבול 0 או $\infty$ - לכן $a=2$.']),
    (r'גבול $1^\infty$', [
      r'↓ $\frac{2-x}{2+x}=1-\frac{2x}{2+x}$',
      r'↓ $\frac3x\cdot\left(-\frac{2x}{2+x}\right)\to-3$ | $b=-3$']),
  ],
  ans=r'א'),

dict(id='23A-m5', exam='23A', num='שאלה 5 (אמריקאית)', pts=8, topics=['deriv'], level=3, mc=True,
  q=r'$g(x)=\frac{f^2(\sqrt x)}{\sqrt{f(x^2)+1}}$, $\ f(1)=3$, $f^{\prime}(1)=3$. $g^{\prime}(1)$ הוא: ' + opts(r'$\frac98$', r'$6$', r'$-\frac98$', r'$\frac{16}5$'),
  steps=[
    (r'כלל המנה', [
      r'= מונה בנקודה | $f^2(1)=9$, נגזרתו $2f(1)f^{\prime}(1)\cdot\frac1{2\sqrt1}=9$',
      r'= מכנה בנקודה | $\sqrt{4}=2$, נגזרתו $\frac{f^{\prime}(1)\cdot2}{2\cdot2}=\frac32$']),
    (r'מציבים', [
      r'$$g^{\prime}(1)=\frac{9\cdot2-9\cdot\frac32}{4}=\frac{4.5}4=\frac98$$']),
  ],
  ans=r'א'),

dict(id='23A-m6', exam='23A', num='שאלה 6 (אמריקאית)', pts=8, topics=['definite'], level=2, mc=True,
  q=r'מחשבים $\int_{-6}^1\frac x{\sqrt[3]{2-x}}dx$ בהצבה $u=\sqrt[3]{2-x}$ ומקבלים $\int_a^bg(u)du$. $g(u)$ הוא: '
    + opts(r'$-3u(2-u^3)$', r'$6u(2-u^3)$', r'$3u\sqrt[3]{2-u}$', r'$-6u\sqrt[3]{2-u}$'),
  steps=[
    (r'ההצבה', [
      r'= | $x=2-u^3$, $\ dx=-3u^2du$',
      r'↓ $\frac x{u}\cdot(-3u^2)=-3u(2-u^3)$']),
  ],
  ans=r'א'),

dict(id='23A-7a', exam='23A', num='שאלה 7א', pts=9, topics=['analysis'], level=1,
  q=r'האם ל-$f(x)=\frac{\ln x}x$ יש מינימום ומקסימום מוחלטים בקטע $[1,e^2]$? אם כן, מצאו אותם.',
  steps=[
    (r'ויירשטראס', [
      r'$f$ רציפה בקטע סגור - יש מינימום ומקסימום.']),
    (r'נקודות חשודות', [
      r'$f^{\prime}=\frac{1-\ln x}{x^2}=0\Rightarrow x=e$:',
      r'= | $f(1)=0$',
      r'= | $f(e)=\frac1e$',
      r'= | $f(e^2)=\frac2{e^2}<\frac1e$']),
  ],
  ans=r'מינימום 0 ב-$x=1$, מקסימום $\frac1e$ ב-$x=e$'),

dict(id='23A-7b', exam='23A', num='שאלה 7ב', pts=9, topics=['analysis', 'limits'], level=2,
  q=r'האם ל-$f(x)=x\ln\left(e+\frac1x\right)$ יש אסימפטוטה משופעת/אופקית באינסוף? אם כן מצאו אותה.',
  steps=[
    (r'שיפוע', [
      r'$$m=\lim\frac{f(x)}x=\lim\ln\left(e+\frac1x\right)=1$$']),
    (r'חיתוך', [
      r'↓ $b=\lim x\left(\ln\left(e+\frac1x\right)-1\right)=\lim\frac{\ln(e+t)-1}{t}$ | $t=\frac1x\to0$',
      r'↓ $=\frac1e$ | הנגזרת של $\ln$ ב-$e$']),
  ],
  ans=r'$y=x+\frac1e$'),

dict(id='23A-8', exam='23A', num='שאלה 8', pts=18, topics=['cont', 'mvt'], level=2,
  q=r'הוכיחו כי למשוואה $e^x-x-3=0$ יש בדיוק שני פתרונות ממשיים.',
  steps=[
    (r'לפחות שניים - ערך הביניים', [
      r'$f(x)=e^x-x-3$ רציפה:',
      r'= | $f(-10)=e^{-10}+7>0$',
      r'= | $f(0)=-2<0$',
      r'= | $f(10)=e^{10}-13>0$',
      r'יש שורש ב-$(-10,0)$ ושורש ב-$(0,10)$.']),
    (r'לכל היותר שניים - רול', [
      r'אם היו 3 שורשים, לפי רול ל-$f^{\prime}$ היו 2 אפסים. אבל $f^{\prime}=e^x-1=0$ רק ב-$x=0$.']),
  ],
  ans=r'בדיוק שני פתרונות'),

dict(id='23A-9a', exam='23A', num='שאלה 9א', pts=9, topics=['mvt'], level=1,
  q=r'הוכיחו שלכל $0<a<b<\frac\pi2$: $\ \arctan b-\arctan a\leq b-a$.',
  steps=[
    (r'לגראנז׳ על $\arctan$ ב-$[a,b]$', [
      r'↓ $\frac{\arctan b-\arctan a}{b-a}=\frac1{1+c^2}$ | $c\in(a,b)$',
      r'↓ $\frac1{1+c^2}\leq1$',
      r'↓ כופלים ב-$b-a>0$']),
  ],
  ans=r'$\arctan b-\arctan a\leq b-a$'),

dict(id='23A-9b', exam='23A', num='שאלה 9ב', pts=9, topics=['improper'], level=2,
  q=r'הוכיחו ש-$\int_0^\infty\frac1{(1+\sqrt x)^{2.4}}dx$ מתכנס.',
  steps=[
    (r'מפצלים', [
      r'ב-$[0,1]$ הפונקציה רציפה וחסומה - אינטגרל רגיל.']),
    (r'ב-$[1,\infty)$ - השוואה', [
      r'↓ $0<\frac1{(1+\sqrt x)^{2.4}}<\frac1{(\sqrt x)^{2.4}}=\frac1{x^{1.2}}$',
      r'↓ $\int_1^\infty\frac{dx}{x^{1.2}}$ מתכנס | $p=1.2>1$']),
  ],
  ans=r'מתכנס'),

dict(id='23A-10', exam='23A', num='שאלה 10', pts=18, topics=['indef'], level=2,
  q=r'חשבו $\int\frac{2x^2+x+5}{(x-3)(x^2+4)}dx$.',
  steps=[
    (r'שברים חלקיים', [
      r'$$\frac{2x^2+x+5}{(x-3)(x^2+4)}=\frac A{x-3}+\frac{Bx+C}{x^2+4}$$',
      r'= $x=3$ | $26=13A\Rightarrow A=2$',
      r'= $x=0$ | $5=8-3C\Rightarrow C=1$',
      r'= $x=1$ | $8=10-2(B+1)\Rightarrow B=0$']),
    (r'האינטגרל', [
      r'$$2\ln|x-3|+\frac12\arctan\frac x2+C$$']),
  ],
  ans=r'$2\ln|x-3|+\frac12\arctan\frac x2+C$'),

# ============================================================== מועד ב תשפ"ג
dict(id='23B-m1', exam='23B', num='שאלה 1 (אמריקאית)', pts=8, topics=['definite', 'limits'], level=2, mc=True,
  q=r'חשבו $\lim_{x\to1}\frac{2\int_1^{x^4}\frac{\ln t}tdt}{(x-1)^2}$. ' + opts(r'$16$', r'$9$', r'$4$', r'$25$'),
  steps=[
    (r'מחשבים את האינטגרל', [
      r'↓ $\int_1^{x^4}\frac{\ln t}tdt=\frac{\ln^2(x^4)}2=8\ln^2x$',
      r'↓ $\frac{16\ln^2x}{(x-1)^2}=16\left(\frac{\ln x}{x-1}\right)^2\to16$']),
  ],
  ans=r'א'),

dict(id='23B-m2', exam='23B', num='שאלה 2 (אמריקאית)', pts=8, topics=['limits'], level=1, mc=True,
  q=r'חשבו $\lim_{x\to\infty}\left(e^{3x}+x^2\right)^{\frac1x}$. ' + opts(r'$e^3$', r'$\infty$', r'$e$', r'$1$'),
  steps=[
    (r'$e^{\ln}$', [
      r'↓ $\frac{\ln(e^{3x}+x^2)}x=\frac{3x+\ln(1+x^2e^{-3x})}x\to3$',
      r'↓ הגבול $e^3$']),
  ],
  ans=r'א'),

dict(id='23B-m3', exam='23B', num='שאלה 3 (אמריקאית)', pts=8, topics=['analysis'], level=1, mc=True,
  q=r'$f(x)=x^3+3x^2$. כמה פתרונות יש למשוואה $f(x)=4$? ' + opts(r'2', r'1', r'0', r'3'),
  steps=[
    (r'פירוק', [
      r'$$x^3+3x^2-4=(x-1)(x+2)^2$$',
      r'שני פתרונות שונים: $x=1$, $x=-2$.']),
  ],
  ans=r'א'),

dict(id='23B-m4', exam='23B', num='שאלה 4 (אמריקאית)', pts=8, topics=['definite'], level=1, mc=True,
  q=r'השטח בין $y=\frac94x^8$ ל-$y=\frac94x^2$: ' + opts(r'1', r'2', r'3', r'4'),
  steps=[
    (r'נקודות חיתוך', [
      r'$x^8=x^2\Rightarrow x=0,\pm1$; ב-$[-1,1]$: $x^2\geq x^8$.']),
    (r'האינטגרל (סימטריה)', [
      r'$$2\int_0^1\frac94(x^2-x^8)dx=\frac92\left(\frac13-\frac19\right)=1$$']),
  ],
  ans=r'א'),

dict(id='23B-m5', exam='23B', num='שאלה 5 (אמריקאית)', pts=8, topics=['definite'], level=1, mc=True,
  q=r'$\int_0^{\pi/2}3\sin^3x\,dx=$ ' + opts(r'2', r'1', r'3', r'4'),
  steps=[
    (r'הצבה $u=\cos x$', [
      r'↓ $\sin^3x=(1-\cos^2x)\sin x$',
      r'↓ $3\int_0^1(1-u^2)du=3\cdot\frac23=2$']),
  ],
  ans=r'א'),

dict(id='23B-m6', exam='23B', num='שאלה 6 (אמריקאית)', pts=8, topics=['improper'], level=2, mc=True,
  q=r'$\int_1^\infty\frac{\ln x}{x^4}dx$: ' + opts(r'מתכנס ל-$\frac19$', r'מתכנס ל-$\frac14$', r'מתכנס ל-1', r'מתכנס ל-$\frac1{16}$'),
  steps=[
    (r'בחלקים', [
      r'$$\int\frac{\ln x}{x^4}=-\frac{\ln x}{3x^3}+\int\frac1{3x^4}=-\frac{\ln x}{3x^3}-\frac1{9x^3}+C$$',
      r'↓ מ-1 עד $\infty$: $0-\left(-\frac19\right)=\frac19$']),
  ],
  ans=r'א'),

dict(id='23B-7', exam='23B', num='שאלה 7', pts=18, topics=['analysis', 'limits'], level=2,
  q=r'$f(x)=x\arctan x+\frac{\arctan x}x$. (א) הראו ש-$f$ זוגית. (ב) מהו סוג אי-הרציפות ב-$x_0=0$? האם יש אסימפטוטה אנכית שם? (ג) מצאו את האסימפטוטה של $f$ במינוס אינסוף.',
  steps=[
    (r'(א)', [
      r'$\arctan$ אי-זוגית, ולכן $x\arctan x$ ו-$\frac{\arctan x}x$ זוגיות - וגם סכומן.']),
    (r'(ב)', [
      r'↓ $\lim_{x\to0}f=0+1=1$',
      r'$f$ לא מוגדרת ב-0 והגבול סופי: אי-רציפות סליקה, אין אסימפטוטה אנכית.']),
    (r'(ג) ב-$+\infty$, ואז זוגיות', [
      r'↓ $\frac{f}x\to\frac\pi2$',
      r'↓ $f-\frac\pi2x=x\left(\arctan x-\frac\pi2\right)+\frac{\arctan x}x\to-1$',
      r'↓ ב-$+\infty$: $y=\frac\pi2x-1$; ובגלל הזוגיות ב-$-\infty$: $y=-\frac\pi2x-1$']),
  ],
  ans=r'סליקה, אין אסימפטוטה אנכית; ב-$-\infty$: $y=-\frac\pi2x-1$'),

dict(id='23B-8a', exam='23B', num='שאלה 8א', pts=9, topics=['cont'], level=2,
  q=r'$g$ רציפה בקטע $[0,1]$ ו-$g\left(\frac49\right)<g\left(\frac13\right)<g\left(\frac29\right)$. הוכיחו שיש $c$ בקטע כך ש-$g(c)=\frac{g\left(\frac49\right)+g\left(\frac13\right)+g\left(\frac29\right)}3$.',
  steps=[
    (r'הממוצע בין הקטן לגדול', [
      r'נסמן $m$ - הממוצע. ממוצע של 3 מספרים נמצא בין הקטן לגדול:',
      r'$$g\left(\tfrac49\right)<m<g\left(\tfrac29\right)$$']),
    (r'ערך הביניים בקטע $\left[\frac29,\frac49\right]$', [
      r'$g$ רציפה שם ומקבלת את שני הערכים, ולכן יש $c\in\left(\frac29,\frac49\right)$ עם $g(c)=m$.']),
  ],
  ans=r'קיים $c$ (משפט ערך הביניים)'),

dict(id='23B-8b', exam='23B', num='שאלה 8ב', pts=9, topics=['indef'], level=2,
  q=r'חשבו $\int\frac{4x-1}{4x^2-12x+25}dx$.',
  steps=[
    (r'מפרקים לפי נגזרת המכנה ($8x-12$)', [
      r'↓ $4x-1=\frac12(8x-12)+5$',
      r'↓ $4x^2-12x+25=(2x-3)^2+16$']),
    (r'שני אינטגרלים', [
      r'= | $\frac12\int\frac{8x-12}{4x^2-12x+25}=\frac12\ln(4x^2-12x+25)$',
      r'= | $5\int\frac{dx}{(2x-3)^2+16}=\frac58\arctan\frac{2x-3}4$']),
  ],
  ans=r'$\frac12\ln(4x^2-12x+25)+\frac58\arctan\frac{2x-3}4+C$'),

dict(id='23B-9', exam='23B', num='שאלה 9', pts=18, topics=['deriv', 'definite'], level=2,
  q=r'$f(x)=\frac{\sin x}x$ ל-$x\neq0$, $f(0)=1$. (א) מצאו $f^{\prime}(x)$ ל-$x\neq0$. (ב) מצאו $f^{\prime}(0)$. (ג) נתון ש-$f$ יורדת ב-$\left[0,\frac\pi6\right]$. הראו ש-$\frac12\leq\int_0^{\pi/6}f(x)dx\leq\frac\pi6$.',
  steps=[
    (r'(א)', [
      r'$$f^{\prime}(x)=\frac{x\cos x-\sin x}{x^2}$$']),
    (r'(ב) לפי ההגדרה', [
      r'$$f^{\prime}(0)=\lim\frac{\frac{\sin h}h-1}h=\lim\frac{\sin h-h}{h^2}=\lim\frac{\cos h-1}{2h}=0$$']),
    (r'(ג) מונוטוניות', [
      r'= | $f\left(\frac\pi6\right)=\frac{1/2}{\pi/6}=\frac3\pi\leq f(x)\leq f(0)=1$',
      r'↓ $\frac\pi6\cdot\frac3\pi\leq\int_0^{\pi/6}f\leq\frac\pi6\cdot1$ | אורך הקטע $\frac\pi6$',
      r'↓ $\frac12\leq\int\leq\frac\pi6$']),
  ],
  ans=r'$f^{\prime}(0)=0$; האי-שוויון מתקיים'),

dict(id='23B-10', exam='23B', num='שאלה 10', pts=18, topics=['cont', 'limits'], level=2,
  q=r'$f(x)=\frac{a+\ln(1+3x^2)}{1-\cos2x}$ ל-$x<0$, $\ f(0)=b$, $\ f(x)=(1-2x)^{\frac1x}$ ל-$x>0$. (א) חשבו $\lim_{x\to0^+}f$. (ב) חשבו $\lim_{x\to0^-}f$. (ג) לאילו $a,b$ יש אי-רציפות סליקה ב-0? (ד) לאילו - אי-רציפות מסוג שני?',
  steps=[
    (r'(א)', [
      r'$$(1-2x)^{\frac1x}\to e^{-2}$$']),
    (r'(ב)', [
      r'המכנה $1-\cos2x\approx2x^2\to0^+$:',
      r'= $a>0$ | $+\infty$',
      r'= $a<0$ | $-\infty$',
      r'= $a=0$ | $\frac{3x^2}{2x^2}=\frac32$']),
    (r'(ג), (ד)', [
      r'סליקה דורשת גבולות שווים: אבל גם כש-$a=0$, $\frac32\neq e^{-2}$ - אין ערכים.',
      r'מסוג שני: $a\neq0$ (גבול אינסופי משמאל), לכל $b$.']),
  ],
  ans=r'$e^{-2}$; $\frac32$ אם $a=0$ ו-$\pm\infty$ אחרת; סליקה - אף פעם; מסוג שני - $a\neq0$'),

# ============================================================== מועד א תשפ"ד
dict(id='24A-1', exam='24A', num='שאלה 1', pts=20, topics=['cont', 'limits'], level=2,
  q=r'$f(x)=\frac{\sin bx}{x+\sin2x}$ ל-$x<0$, $\ f(0)=2a-7$, $\ f(x)=x\ln x$ ל-$x>0$. מצאו (אם קיימים) $a,b$ כך ש-$x=0$: (i) נקודת רציפות; (ii) אי-רציפות סליקה; (iii) אי-רציפות מסוג ראשון; (iv) אי-רציפות מסוג שני.',
  steps=[
    (r'הגבולות', [
      r'= $x\to0^-$ | $\frac{\frac{\sin bx}x}{1+\frac{\sin2x}x}\to\frac b3$',
      r'= $x\to0^+$ | $x\ln x=\frac{\ln x}{1/x}\to0$ (לופיטל)']),
    (r'ארבעת המקרים', [
      r'= (i) רציפה | $b=0$, $\ 2a-7=0\Rightarrow a=\frac72$',
      r'= (ii) סליקה | $b=0$, $\ a\neq\frac72$',
      r'= (iii) קפיצה | $b\neq0$, $a$ כלשהו',
      r'= (iv) סוג שני | אין - שני הגבולות תמיד סופיים']),
  ],
  ans=r'(i) $a=\frac72,b=0$; (ii) $b=0,a\neq\frac72$; (iii) $b\neq0$; (iv) אין'),

dict(id='24A-2a', exam='24A', num='שאלה 2א', pts=10, topics=['cont', 'analysis'], level=1,
  q=r'הוכיחו כי למשוואה $x^5+5\arctan x-8=0$ יש פתרון ממשי אחד בלבד.',
  steps=[
    (r'קיום', [
      r'$f(x)=x^5+5\arctan x-8$ רציפה; $f(0)=-8<0$, $f(2)=24+5\arctan2>0$ ⇒ שורש ב-$(0,2)$.']),
    (r'יחידות', [
      r'$f^{\prime}(x)=5x^4+\frac5{1+x^2}>0$ - עולה ממש, ולכן חותכת את ציר $x$ פעם אחת לכל היותר.']),
  ],
  ans=r'פתרון יחיד'),

dict(id='24A-2b', exam='24A', num='שאלה 2ב', pts=10, topics=['indef'], level=1,
  q=r'חשבו $\int\frac{dx}{x^3-x^2-2x}$.',
  steps=[
    (r'פירוק', [
      r'$$\frac1{x(x+1)(x-2)}=\frac Ax+\frac B{x+1}+\frac C{x-2}$$',
      r'= $x=0$ | $1=-2A\Rightarrow A=-\frac12$',
      r'= $x=-1$ | $1=3B\Rightarrow B=\frac13$',
      r'= $x=2$ | $1=6C\Rightarrow C=\frac16$']),
  ],
  ans=r'$-\frac12\ln|x|+\frac13\ln|x+1|+\frac16\ln|x-2|+C$'),

dict(id='24A-3a', exam='24A', num='שאלה 3א', pts=10, topics=['analysis'], level=1,
  q=r'הוכיחו כי $0\leq x-\sin^2x$ לכל $x\in[0,\infty)$.',
  steps=[
    (r'פונקציית עזר', [
      r'= | $f(x)=x-\sin^2x$, $\ f(0)=0$',
      r'= | $f^{\prime}(x)=1-2\sin x\cos x=1-\sin2x\geq0$',
      r'$f$ עולה ב-$[0,\infty)$, ולכן $f(x)\geq f(0)=0$.']),
  ],
  ans=r'מתקיים'),

dict(id='24A-3b', exam='24A', num='שאלה 3ב', pts=10, topics=['definite'], level=2,
  q=r'חשבו $\int_0^{\ln2}\frac{e^{2x}}{e^x+1}dx$.',
  steps=[
    (r'הצבה $t=e^x$', [
      r'= | $dt=e^xdx$, גבולות $1\to2$',
      r'$$\int_1^2\frac t{t+1}dt=\int_1^2\left(1-\frac1{t+1}\right)dt$$']),
    (r'מחשבים', [
      r'$$\left[t-\ln(t+1)\right]_1^2=1-\ln3+\ln2=1+\ln\frac23$$']),
  ],
  ans=r'$1+\ln\frac23$'),

dict(id='24A-4a', exam='24A', num='שאלה 4א', pts=10, topics=['indef'], level=1,
  q=r'חשבו $\int(x^2+1)\sin x\,dx$.',
  steps=[
    (r'בחלקים פעמיים', [
      r'↓ $\int(x^2+1)\sin x=-(x^2+1)\cos x+\int2x\cos x$',
      r'↓ $\int2x\cos x=2x\sin x-\int2\sin x=2x\sin x+2\cos x$']),
  ],
  ans=r'$(1-x^2)\cos x+2x\sin x+C$'),

dict(id='24A-4b', exam='24A', num='שאלה 4ב', pts=10, topics=['deriv'], level=2,
  q=r'$f(x)=x^3\sin\frac1x+\sin x$ ל-$x\neq0$, $f(0)=0$. האם $f$ גזירה ב-0? אם כן מצאו $f^{\prime}(0)$.',
  steps=[
    (r'הגדרת הנגזרת', [
      r'$$f^{\prime}(0)=\lim_{h\to0}\left(h^2\sin\frac1h+\frac{\sin h}h\right)=0+1=1$$',
      r'($h^2\sin\frac1h\to0$: חסומה כפול שואפת ל-0.)']),
  ],
  ans=r'גזירה, $f^{\prime}(0)=1$'),

dict(id='24A-m1', exam='24A', num='שאלה 1 (אמריקאית)', pts=8, topics=['deriv'], level=1, mc=True,
  q=r'$f(x)=e^{ax}+x+b$, והישר $y=2$ משיק לגרף ב-$x_0=0$. אז: ' + opts(r'$a=-1,\ b=1$', r'$a=-1,\ b=-1$', r'$a=1,\ b=-1$', r'$a=1,\ b=1$', r'אף אחת'),
  steps=[
    (r'תנאים', [
      r'= | $f(0)=1+b=2\Rightarrow b=1$',
      r'= | $f^{\prime}(0)=a+1=0\Rightarrow a=-1$']),
  ],
  ans=r'א'),

dict(id='24A-m3', exam='24A', num='שאלה 3 (אמריקאית)', pts=8, topics=['deriv'], level=2, mc=True,
  q=r'$g(x)=e^{\sqrt{x^2+b}}$, $f(x)=\sqrt{x+a}$, $h(x)=g(f(x))$. נתון $h^{\prime}(a)=e^{\sqrt{2a+b}}$. אז $2a+b=$ ' + opts(r'$\frac12$', r'$\frac14$', r'1', r'חסרים נתונים', r'אף אחת'),
  steps=[
    (r'ההרכבה', [
      r'↓ $h(x)=e^{\sqrt{(\sqrt{x+a})^2+b}}=e^{\sqrt{x+a+b}}$',
      r'↓ $h^{\prime}(x)=e^{\sqrt{x+a+b}}\cdot\frac1{2\sqrt{x+a+b}}$']),
    (r'מציבים $x=a$', [
      r'↓ $h^{\prime}(a)=e^{\sqrt{2a+b}}\cdot\frac1{2\sqrt{2a+b}}=e^{\sqrt{2a+b}}$',
      r'↓ $2\sqrt{2a+b}=1\Rightarrow2a+b=\frac14$']),
  ],
  ans=r'ב. $\frac14$'),

dict(id='24A-m4', exam='24A', num='שאלה 4 (אמריקאית)', pts=8, topics=['limits'], level=2, mc=True,
  q=r'$f$ גזירה, $\lim_{x\to2}f(x)=0$, $\lim_{x\to2}f^{\prime}(x)=7$. אז $\lim_{x\to2}(1+f(x))^{\frac1{x-2}}=$ ' + opts(r'$e^7$', r'1', r'$e^{1/7}$', r'0', r'אף אחת'),
  steps=[
    (r'$e^{\ln}$ ולופיטל', [
      r'$$\lim\frac{\ln(1+f(x))}{x-2}=\lim\frac{f^{\prime}(x)}{1+f(x)}=7$$',
      r'הגבול $e^7$.']),
  ],
  ans=r'א'),

dict(id='24A-m5', exam='24A', num='שאלה 5 (אמריקאית)', pts=8, topics=['deriv', 'cont'], level=1, mc=True,
  q=r'בחרו את הטענה הנכונה: ' + opts(r'אם $f$ גזירה ב-$a$, אז היא רציפה ב-$a$', r'אם $f$ רציפה ב-$a$, אז היא גזירה ב-$a$', r'אם $f$ לא גזירה ב-$a$, אז היא לא רציפה ב-$a$',
                                       r'אם $f,g$ לא גזירות ב-$a$, אז $f+g$ לא גזירה ב-$a$', r'יש יותר מטענה אחת נכונה'),
  steps=[
    (r'משפט ודוגמאות נגדיות', [
      r'= א | משפט: גזירה ⇒ רציפה ✓',
      r'= ב, ג | $|x|$ ב-0: רציפה ולא גזירה ✗',
      r'= ד | $|x|+(-|x|)=0$ גזירה ✗']),
  ],
  ans=r'א'),

dict(id='24A-bonus', exam='24A', num='שאלת בונוס', pts=10, topics=['cont'], level=1,
  q=r'$f,g,h$ רציפות ב-$[1,2]$, $f(2)=5,\ g(2)=4,\ h(2)=12,\ f(1)=1,\ g(1)=2,\ h(1)=6$. הוכיחו שיש $1<c<2$ עם $f(c)g(c)=h(c)$.',
  steps=[
    (r'פונקציית עזר', [
      r'= | $M(x)=f(x)g(x)-h(x)$ רציפה',
      r'= | $M(1)=2-6=-4<0$',
      r'= | $M(2)=20-12=8>0$',
      r'לפי ערך הביניים יש $c\in(1,2)$ עם $M(c)=0$.']),
  ],
  ans=r'קיים $c$'),

# ============================================================== מבחן דוגמה תשפ"ד
dict(id='24S-1', exam='24S', num='שאלה 1', pts=20, topics=['limits', 'deriv'], level=2,
  q=r'$f,g$ גזירות 3 פעמים, $f^{\prime}(3)=4$, $g^{\prime}(3)=5$, $f(3)=g(3)=0$. חשבו $\lim_{x\to3}\frac{f(x)g(x)}{(x-3)^2}$.',
  steps=[
    (r'מפרקים לשני גבולות', [
      r'= | $\frac{f(x)}{x-3}=\frac{f(x)-f(3)}{x-3}\to f^{\prime}(3)=4$',
      r'= | $\frac{g(x)}{x-3}\to g^{\prime}(3)=5$',
      r'הגבול $4\cdot5=20$.']),
  ],
  ans=r'20'),

dict(id='24S-2', exam='24S', num='שאלה 2', pts=20, topics=['analysis', 'mvt'], level=1,
  q=r'הוכיחו כי לכל $x\in\left(0,\frac\pi2\right]$: $\ 1-x<\cos x$.',
  steps=[
    (r'פונקציית עזר', [
      r'= | $h(x)=\cos x-1+x$, $\ h(0)=0$',
      r'= | $h^{\prime}(x)=1-\sin x>0$ ב-$\left(0,\frac\pi2\right)$',
      r'$h$ עולה ממש ב-$\left[0,\frac\pi2\right]$, ולכן $h(x)>h(0)=0$ ל-$x>0$.']),
  ],
  ans=r'מתקיים'),

dict(id='24S-3a', exam='24S', num='שאלה 3א', pts=10, topics=['indef'], level=2, also=['25S'],
  q=r'חשבו $\int\frac{x+7}{(x+2)(x^2+2x+5)}dx$.',
  steps=[
    (r'שברים חלקיים', [
      r'= $x=-2$ | $5=5A\Rightarrow A=1$',
      r'= מקדם $x^2$ | $0=1+B\Rightarrow B=-1$',
      r'= מקדם חופשי | $7=5+2C\Rightarrow C=1$',
      r'$$\frac1{x+2}+\frac{1-x}{x^2+2x+5}$$']),
    (r'החלק השני', [
      r'↓ $1-x=-(x+1)+2$',
      r'↓ $\int\frac{-(x+1)}{(x+1)^2+4}=-\frac12\ln(x^2+2x+5)$',
      r'↓ $\int\frac2{(x+1)^2+4}=\arctan\frac{x+1}2$']),
  ],
  ans=r'$\ln|x+2|-\frac12\ln(x^2+2x+5)+\arctan\frac{x+1}2+C$'),

dict(id='24S-3b', exam='24S', num='שאלה 3ב', pts=10, topics=['analysis', 'limits'], level=1,
  q=r'מצאו את האסימפטוטות של $f(x)=\arctan\frac x{x-2}$.',
  steps=[
    (r'אופקית', [
      r'$\frac x{x-2}\to1$ ב-$\pm\infty$ ⇒ $f\to\frac\pi4$: אסימפטוטה $y=\frac\pi4$.']),
    (r'אנכית?', [
      r'ב-$x=2$: $f\to\pm\frac\pi2$ - גבולות סופיים, אין אסימפטוטה אנכית.']),
  ],
  ans=r'$y=\frac\pi4$ בלבד'),

dict(id='24S-4a', exam='24S', num='שאלה 4א', pts=10, topics=['indef'], level=2,
  q=r'חשבו $\int\cos(\ln x)\,dx$.',
  steps=[
    (r'בחלקים פעמיים', [
      r'↓ $I=x\cos\ln x+\int\sin\ln x\,dx$ | $u=\cos\ln x,\ v^{\prime}=1$',
      r'↓ $\int\sin\ln x=x\sin\ln x-I$',
      r'↓ $2I=x(\cos\ln x+\sin\ln x)$']),
  ],
  ans=r'$\frac x2\left(\cos\ln x+\sin\ln x\right)+C$'),

dict(id='24S-4b', exam='24S', num='שאלה 4ב', pts=10, topics=['limits'], level=1,
  q=r'חשבו $\lim_{x\to\infty}\frac{3x-\cos2x}{4x+\sin x}$.',
  steps=[
    (r'מחלקים ב-$x$', [
      r'$$\frac{3-\frac{\cos2x}x}{4+\frac{\sin x}x}\to\frac34$$',
      r'(חסומה חלקי $x$ שואפת ל-0. לופיטל לא מתאים כאן - הגבול של מנת הנגזרות לא קיים.)']),
  ],
  ans=r'$\frac34$'),

dict(id='24S-m1', exam='24S', num='שאלה 1 (אמריקאית)', pts=8, topics=['cont'], level=1, mc=True,
  q=r'$f(x)=\frac{\sin2x}{ax}$ ל-$x>0$, $f(0)=2$, $f(x)=\frac{\cos2x}{2+x}$ ל-$x<0$. אם $x_0=0$ אי-רציפות סליקה אז: ' + opts(r'$a=0$', r'$a=1$', r'$a=2$', r'$a=4$'),
  steps=[
    (r'הגבולות', [
      r'= $x\to0^-$ | $\frac12$',
      r'= $x\to0^+$ | $\frac2a$',
      r'סליקה: שווים זה לזה (ושונים מ-$f(0)=2$): $\frac2a=\frac12\Rightarrow a=4$.']),
  ],
  ans=r'ד. $a=4$'),

dict(id='24S-m5', exam='24S', num='שאלה 5 (אמריקאית)', pts=8, topics=['cont', 'analysis'], level=1, mc=True,
  q=r'למשוואה $x^3+e^x+100=0$: ' + opts(r'יש פתרון יחיד', r'יש שני פתרונות', r'יש שלושה פתרונות', r'אין פתרון ממשי'),
  steps=[
    (r'קיום ויחידות', [
      r'= | $f^{\prime}(x)=3x^2+e^x>0$ - עולה ממש',
      r'= | $f(-10)=-900+e^{-10}<0$, $\ f(0)=101>0$',
      r'בדיוק פתרון אחד.']),
  ],
  ans=r'א'),

dict(id='24S-bonus', exam='24S', num='שאלת בונוס', pts=10, topics=['deriv', 'analysis'], level=2,
  q=r'$y=(ax^2+bx+1)e^{-x}$ משיקה לציר $x$ בנקודה $x=-1$. מצאו את $a,b$ ואת נקודות הקיצון.',
  steps=[
    (r'שני תנאים', [
      r'= $y(-1)=0$ | $a-b+1=0$',
      r'= $y^{\prime}(-1)=0$ | $y^{\prime}=e^{-x}\left(-ax^2+(2a-b)x+b-1\right)$ ⇒ $-3a+2b-1=0$',
      r'↓ $a=1,\ b=2$ | $y=(x+1)^2e^{-x}$']),
    (r'קיצון', [
      r'$y^{\prime}=e^{-x}(1-x^2)$:',
      r'= מינימום | $(-1,\ 0)$',
      r'= מקסימום | $\left(1,\ \frac4e\right)$']),
  ],
  ans=r'$a=1,b=2$; מינימום $(-1,0)$, מקסימום $\left(1,\frac4e\right)$'),

# ============================================================== מועד א תשפ"ה
dict(id='25A-1a', exam='25A', num='שאלה 1א', pts=15, topics=['cont', 'limits'], level=2,
  q=r'$f(x)=\frac{\sqrt{1-ax}-\cos x}x$ ל-$x<0$, $\ f(0)=-1$, $\ f(x)=-1+b\sin\frac1x$ ל-$x>0$; $a>0$. (i) חשבו את הגבולות החד-צדדיים, ואם יש $a,b$ שעבורם $f$ רציפה. (ii) האם יש ערכים שעבורם 0 קפיצה? אי-רציפות עיקרית (סוג שני)?',
  steps=[
    (r'משמאל', [
      r'↓ $\frac{\sqrt{1-ax}-1}x+\frac{1-\cos x}x$',
      r'↓ $\to-\frac a2+0$ | $\sqrt{1-ax}\approx1-\frac{ax}2$']),
    (r'מימין', [
      r'$b\sin\frac1x$ - קיים גבול רק אם $b=0$, ואז הגבול $-1$.']),
    (r'מקרים', [
      r'= רציפה | $b=0$ ו-$-\frac a2=-1$: $\ a=2$',
      r'= קפיצה | $b=0$, $\ a\neq2$',
      r'= סוג שני | $b\neq0$ (אין גבול מימין), כל $a>0$']),
  ],
  ans=r'רציפה: $a=2,b=0$; קפיצה: $b=0,a\neq2$; סוג שני: $b\neq0$'),

dict(id='25A-1b', exam='25A', num='שאלה 1ב', pts=15, topics=['indef'], level=2,
  q=r'חשבו $\int\frac{x^3-1}{x(x^2+1)}dx$.',
  steps=[
    (r'חילוק', [
      r'$$\frac{x^3-1}{x^3+x}=1-\frac{x+1}{x(x^2+1)}$$']),
    (r'שברים חלקיים', [
      r'$$\frac{x+1}{x(x^2+1)}=\frac1x+\frac{1-x}{x^2+1}$$']),
    (r'מצרפים', [
      r'$$x-\ln|x|-\arctan x+\frac12\ln(x^2+1)+C$$']),
  ],
  ans=r'$x-\ln|x|-\arctan x+\frac12\ln(x^2+1)+C$'),

dict(id='25A-2a', exam='25A', num='שאלה 2א', pts=15, topics=['cont'], level=2,
  q=r'(i) הוכיחו שלמשוואה $x^3-2\arctan x=0$ יש פתרון בקטע $[1,2]$. (ii) הוכיחו שיש לה לפחות 3 פתרונות ממשיים. (מותר: $3<\pi<4$, $\arctan1=\frac\pi4$.)',
  steps=[
    (r'(i) ערך הביניים', [
      r'= | $g(1)=1-\frac\pi2<0$ (כי $\pi>3$)',
      r'= | $g(2)=8-2\arctan2>8-\pi>0$']),
    (r'(ii)', [
      r'$g$ אי-זוגית: $g(0)=0$, ואם $g(c)=0$ ל-$c\in(1,2)$ אז גם $g(-c)=0$. שלושה פתרונות: $0,\ c,\ -c$.']),
  ],
  ans=r'הוכחה בפתרון'),

dict(id='25A-2b', exam='25A', num='שאלה 2ב', pts=15, topics=['definite'], level=2,
  q=r'חשבו $\int_0^9e^{\sqrt{4x}}dx$.',
  steps=[
    (r'הצבה $t=2\sqrt x$', [
      r'= | $x=\frac{t^2}4,\ dx=\frac t2dt$, גבולות $0\to6$',
      r'$$\frac12\int_0^6te^tdt$$']),
    (r'בחלקים', [
      r'↓ $\frac12\left[(t-1)e^t\right]_0^6$',
      r'↓ $=\frac12(5e^6+1)$']),
  ],
  ans=r'$\frac{5e^6+1}2$'),

dict(id='25A-3a', exam='25A', num='שאלה 3א', pts=15, topics=['deriv', 'limits'], level=3,
  q=r'$f(x)=\frac{\sin x-x+\frac{x^3}6}{x^4}$ ל-$x\neq0$, $f(0)=0$. הוכיחו בעזרת הגדרת הנגזרת ש-$f$ גזירה ב-0 וחשבו $f^{\prime}(0)$.',
  steps=[
    (r'הגדרה', [
      r'$$f^{\prime}(0)=\lim_{x\to0}\frac{\sin x-x+\frac{x^3}6}{x^5}$$']),
    (r'לופיטל חמש פעמים (כל פעם $\frac00$)', [
      r'↓ $\frac{\cos x-1+\frac{x^2}2}{5x^4}$',
      r'↓ $\frac{-\sin x+x}{20x^3}$',
      r'↓ $\frac{-\cos x+1}{60x^2}$',
      r'↓ $\frac{\sin x}{120x}\to\frac1{120}$']),
  ],
  ans=r'$f^{\prime}(0)=\frac1{120}$'),

dict(id='25A-3b', exam='25A', num='שאלה 3ב', pts=15, topics=['improper'], level=2,
  q=r'בדקו את התכנסות $\int_1^\infty\frac{x+\cos^2x}{\sqrt{7x^6+x^2+5}}dx$.',
  steps=[
    (r'אינטגרנד חיובי - השוואה גבולית עם $\frac1{x^2}$', [
      r'$$\frac{\frac{x+\cos^2x}{\sqrt{7x^6+x^2+5}}}{\frac1{x^2}}=\frac{x^3+x^2\cos^2x}{\sqrt{7x^6+x^2+5}}\to\frac1{\sqrt7}$$',
      r'הגבול חיובי וסופי, ו-$\int_1^\infty\frac{dx}{x^2}$ מתכנס - לכן גם האינטגרל מתכנס.']),
  ],
  ans=r'מתכנס'),

dict(id='25A-m1', exam='25A', num='שאלה 1 (אמריקאית)', pts=7, topics=['analysis'], level=2, mc=True,
  q=r'גרף הנגזרת $f^{\prime}$: שלילית עד סביב 0, חיובית עד 2 (מקסימום ב-1), שלילית בין 2 ל-4 (מינימום ב-3), חיובית אחרי 4. (A) $x_0=3$ נקודת פיתול של $f$. (B) $f$ קמורה (מחייכת) ב-$[0,1]$. (C) $f$ עולה ב-$[3,4]$. מי נכונה? '
    + opts(r'נכונות: A, B; שגויה: C', r'נכונה: A; שגויות: B, C', r'נכונה: B; שגויות: A, C', r'כולן שגויות', r'נכונה: C; שגויות: A, B'),
  steps=[
    (r'מקריאים מהגרף של $f^{\prime}$', [
      r'= A | $f^{\prime}$ מחליפה כיוון (מינימום) ב-3 ⇒ $f^{\prime\prime}$ מחליפה סימן ⇒ פיתול ✓',
      r'= B | $f^{\prime}$ עולה ב-$[0,1]$ ⇒ $f^{\prime\prime}>0$ ⇒ קמורה ✓',
      r'= C | $f^{\prime}<0$ ב-$(2,4)$ ⇒ $f$ יורדת ✗']),
  ],
  ans=r'א'),

dict(id='25A-m2', exam='25A', num='שאלה 2 (אמריקאית)', pts=7, topics=['deriv'], level=1, mc=True,
  q=r'$f(g(x))=4x^2$, $g(2)=1$, $g^{\prime}(2)=\frac12$. מהו $f^{\prime}(1)$? ' + opts(r'32', r'8', r'16', r'4', r'2'),
  steps=[
    (r'גוזרים את שני האגפים', [
      r'↓ $f^{\prime}(g(x))g^{\prime}(x)=8x$',
      r'↓ $x=2$: $f^{\prime}(1)\cdot\frac12=16$ | $f^{\prime}(1)=32$']),
  ],
  ans=r'א'),

dict(id='25A-m3', exam='25A', num='שאלה 3 (אמריקאית)', pts=7, topics=['analysis'], level=2, mc=True,
  q=r'$f(x)=\sqrt[x]{2x}=(2x)^{\frac1x}$, $x>0$. מי נכונה? '
    + opts(r'נקודת קיצון אחת בלבד: $x=\frac e2$, מקסימום', r'נקודת קיצון אחת בלבד: $x=\frac e2$, מינימום', r'שתי נקודות קיצון',
           r'נקודת קיצון אחת: $x=\frac{\sqrt e}2$, מקסימום', r'נקודת קיצון אחת: $x=\frac{\sqrt e}2$, מינימום'),
  steps=[
    (r'גזירה לוגריתמית', [
      r'↓ $\ln f=\frac{\ln2x}x$',
      r'↓ $\frac{f^{\prime}}f=\frac{1-\ln2x}{x^2}$',
      r'↓ $f^{\prime}=0\iff2x=e$ | $x=\frac e2$',
      r'לפני: $f^{\prime}>0$, אחרי: $f^{\prime}<0$ - מקסימום.']),
  ],
  ans=r'א'),

dict(id='25A-m4', exam='25A', num='שאלה 4 (אמריקאית)', pts=7, topics=['definite', 'limits'], level=2, mc=True,
  q=r'חשבו $\lim_{x\to1}\frac{\int_1^{x^2}t\ln t\,dt}{(x-1)^2}$. ' + opts(r'2', r'1', r'3', r'4', r'$\infty$'),
  steps=[
    (r'לופיטל והמשפט היסודי', [
      r'↓ $\frac{x^2\ln(x^2)\cdot2x}{2(x-1)}=\frac{2x^3\ln x}{x-1}$',
      r'↓ $\frac{\ln x}{x-1}\to1$ | הגבול $2$']),
  ],
  ans=r'א'),

dict(id='25A-m5', exam='25A', num='שאלה 5 (אמריקאית)', pts=7, topics=['definite'], level=1, mc=True,
  q=r'חשבו $\int_1^4\frac{(1+\sqrt x)^3}{\sqrt x}dx$. ' + opts(r'$\frac{65}2$', r'$\frac{27}2$', r'$\frac{27}4$', r'46', r'$\frac{65}4$'),
  steps=[
    (r'הצבה $u=1+\sqrt x$', [
      r'= | $du=\frac{dx}{2\sqrt x}$, גבולות $2\to3$',
      r'$$2\int_2^3u^3du=\frac{u^4}2\Big|_2^3=\frac{81-16}2=\frac{65}2$$']),
  ],
  ans=r'א'),

dict(id='25A-m6', exam='25A', num='שאלה 6 (אמריקאית)', pts=7, topics=['analysis', 'limits'], level=2, mc=True,
  q=r'$f(x)=x\arctan\frac1x$, $f(0)=0$. מי נכונה? '
    + opts(r'$y=1$ אופקית ב-$\infty$ וב-$-\infty$; אין אנכית', r'$y=1$ אופקית בשני הכיוונים; $x=0$ אנכית', r'$y=\frac\pi2x$ ב-$\infty$, $y=-\frac\pi2x$ ב-$-\infty$; אין אנכית',
           r'כמו ג, ועם אנכית $x=0$', r'$y=\frac\pi2x+1$ משופעת בשני הכיוונים; אין אנכית'),
  steps=[
    (r'באינסוף', [
      r'$t=\frac1x\to0$: $\ f=\frac{\arctan t}t\to1$ (משני הכיוונים).']),
    (r'ליד 0', [
      r'$|f(x)|\leq\frac\pi2|x|\to0$ - אין אסימפטוטה אנכית.']),
  ],
  ans=r'א'),

dict(id='25A-x', exam='25A', num='שאלה פתוחה נוספת (מילואים)', pts=30, topics=['analysis', 'definite'], level=2,
  q=r'$f(x)=x\ln x$ ל-$x>0$, $f(0)=0$. (א) הוכיחו ש-$f$ רציפה מימין ב-0. (ב) מצאו תחומי עלייה/ירידה וקמירות/קעירות. (ג) מצאו ערכי קיצון גלובליים ב-$[0,e]$. (ד) מצאו את השטח בין הגרף לציר $x$ ב-$1\leq x\leq e$.',
  steps=[
    (r'(א)', [
      r'$x\ln x=\frac{\ln x}{1/x}\to\lim\frac{1/x}{-1/x^2}=\lim(-x)=0$ ✓']),
    (r'(ב)', [
      r'= | $f^{\prime}=\ln x+1$: יורדת ב-$\left(0,\frac1e\right)$, עולה ב-$\left(\frac1e,\infty\right)$',
      r'= | $f^{\prime\prime}=\frac1x>0$: קמורה בכל התחום']),
    (r'(ג)', [
      r'= | $f(0)=0,\ f\left(\frac1e\right)=-\frac1e,\ f(e)=e$',
      r'מינימום $-\frac1e$ ב-$\frac1e$, מקסימום $e$ ב-$e$.']),
    (r'(ד)', [
      r'$$\int_1^ex\ln x\,dx=\left[\frac{x^2\ln x}2-\frac{x^2}4\right]_1^e=\frac{e^2+1}4$$']),
  ],
  ans=r'מינימום $-\frac1e$, מקסימום $e$; שטח $\frac{e^2+1}4$'),

dict(id='25A-m7', exam='25A', num='שאלה אמריקאית נוספת (מילואים)', pts=6, topics=['limits'], level=1, mc=True,
  q=r'חשבו $\lim_{x\to\infty}\left(\sqrt{x^2+4x+1}-\sqrt{x^2-x}\right)$. ' + opts(r'$\frac14$', r'3', r'$\frac52$', r'0', r'$\infty$'),
  steps=[
    (r'כפל בצמוד', [
      r'$$\frac{5x+1}{\sqrt{x^2+4x+1}+\sqrt{x^2-x}}\to\frac52$$']),
  ],
  ans=r'ג. $\frac52$'),

# ============================================================== מבחן דוגמה תשפ"ה
dict(id='25S-m3', exam='25S', num='שאלה 3 (אמריקאית)', pts=7, topics=['definite'], level=1, mc=True,
  q=r'מהו $\int_0^{\pi/2}\sin^4x\cos^3x\,dx$? ' + opts(r'$\frac2{35}$', r'1', r'$\infty$', r'$\pi$', r'$\frac27$'),
  steps=[
    (r'הצבה $u=\sin x$', [
      r'↓ $\cos^3x=(1-\sin^2x)\cos x$',
      r'↓ $\int_0^1u^4(1-u^2)du=\frac15-\frac17=\frac2{35}$']),
  ],
  ans=r'א'),
]


# ---------- סילבוס: באיזה שבוע נלמד כל נושא (לסינון "רק מה שכבר למדנו") ----------
SYLLABUS_PDF = 'syllabus.pdf'
STAGE_LABEL = 'שבוע'
SYLLABUS = [
    (1, 'פונקציות: תחום, טווח, זוגיות, הזזות, הרכבה'),
    (2, 'תכונות פונקציות; מושג הגבול, גבולות חד-צדדיים ובאינסוף'),
    (3, 'מצבי אי-ודאות, סנדוויץ׳, הגבול sin x/x; הגדרת רציפות'),
    (4, 'המספר e והגבולות שלו, ln; מיון אי-רציפות; ערך הביניים, ויירשטראס'),
    (5, 'הגדרת הנגזרת, ישר משיק, כלל השרשרת'),
    (6, 'נגזרת של פונקציה הפוכה; פרמה, רול'),
    (7, 'לגראנז׳, מבחני הנגזרת הראשונה והשנייה, לופיטל'),
    (8, 'קמירות וקעירות, אסימפטוטות, חקירת פונקציה'),
    (9, 'אינטגרל לא מסוים: מיידיים, הצבה, חלקים'),
    (10, 'אינטגרציה של פונקציות רציונליות וטריגונומטריות'),
    (11, 'אינטגרל מסוים, ערך ממוצע, המשפט היסודי'),
    (12, 'גבולות משתנים, אינטגרלים מוכללים ומבחני השוואה'),
    (13, 'יישומי האינטגרל, סיכום וחזרה'),
]
STAGE = 4          # עד כאן נלמד לפי הקבצים שהועלו (תרגיל בית 4)
TOPIC_UNIT = {'limits': 4, 'cont': 4, 'deriv': 6, 'mvt': 7, 'analysis': 8, 'indef': 10, 'definite': 12, 'improper': 12}
UNIT = {'21A-m2': 5,      # גבול דרך הגדרת הנגזרת
        '22A-m4': 7, '24A-m4': 7, '24A-1': 7}   # לופיטל
