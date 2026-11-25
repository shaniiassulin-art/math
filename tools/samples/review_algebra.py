# -*- coding: utf-8 -*-
# מבחני חזרה - אלגברה לינארית 96004: מועד א (5785), מועד ב, מבחן דוגמה.
# כל שאלה: מבחן, מספר, נקודות, נושאים, רמה (1 קלה, 2 בינונית, 3 קשה), השאלה, פתרון מלא ותשובה.
# שאלה שכתוב בה "אין קשר בין שני חלקים" מפוצלת לשני פריטים (א / ב), כדי שאפשר יהיה לסנן לפי נושא.
# כל החישובים נבדקו מחדש (sympy).

EXAMS = [('A', 'מועד א'), ('B', 'מועד ב'), ('S', 'מבחן דוגמה')]

TOPICS = [
    ('complex', 'מספרים מרוכבים'),
    ('matrices', 'מטריצות, הופכית ושחלוף'),
    ('det', 'דטרמיננטות'),
    ('systems', 'מערכות לינאריות ודרגה'),
    ('spaces', 'מרחבים וקטוריים: תת-מרחב, Span, בסיס ומימד'),
    ('linmap', 'העתקות לינאריות: גרעין ותמונה'),
    ('diag', 'ערכים עצמיים ולכסון'),
    ('inner', 'מכפלה פנימית וגרם-שמידט'),
]


def opts(*xs):
    """4 options of a multiple-choice question; tools/review.py lays them out after the question text"""
    return '§§OPTS§§' + '|||'.join(xs)


Q = [
# ============================================================== מועד א
dict(id='A1', exam='A', num='שאלה 1', pts=15, topics=['linmap'], level=2,
  q=r'תהי $T:\mathbb{R}^4\to M_2(\mathbb{R})$ העתקה לינארית: $T\begin{pmatrix}x\\y\\z\\t\end{pmatrix}=\begin{bmatrix}x+2y+z+2t&x+3y-2z+4t\\-y+3z-2t&2x+3y+5z+2t\end{bmatrix}$. '
    r'(i) מצאו את המטריצה הסטנדרטית שמייצגת את $T$. (ii) מצאו בסיס ל-$\operatorname{Im}(T)$. (iii) תנו דוגמה למטריצה סימטרית $A\in\operatorname{Im}(T)$ עם $\operatorname{Tr}(A)=14$.',
  steps=[
    (r'(i) המטריצה המייצגת', [
      r'בבסיס הסטנדרטי של $M_2$ ($E_{11},E_{12},E_{21},E_{22}$) כל איבר של התמונה הוא שורה, ובה המקדמים של $x,y,z,t$:',
      r'$$[T]=\begin{bmatrix}1&2&1&2\\1&3&-2&4\\0&-1&3&-2\\2&3&5&2\end{bmatrix}$$']),
    (r'(ii) התמונה נפרשת על ידי העמודות - מדרגים', [
      r'↓ $L_2\to L_2-L_1,\ \ L_4\to L_4-2L_1$ | $[0,1,-3,2]$, $\ [0,-1,3,-2]$',
      r'↓ $L_3\to L_3+L_2,\ \ L_4\to L_4+L_2$ | שתי שורות אפסים',
      r'האיברים המובילים בעמודות 1 ו-2, ולכן $\dim\operatorname{Im}(T)=2$, והעמודות 1, 2 של המטריצה המקורית הן בסיס:',
      r'$$\operatorname{Im}(T)=\operatorname{Span}\left\{\begin{bmatrix}1&1\\0&2\end{bmatrix},\begin{bmatrix}2&3\\-1&3\end{bmatrix}\right\}$$']),
    (r'(iii) מטריצה כללית בתמונה', [
      r'$$A=a\begin{bmatrix}1&1\\0&2\end{bmatrix}+b\begin{bmatrix}2&3\\-1&3\end{bmatrix}=\begin{bmatrix}a+2b&a+3b\\-b&2a+3b\end{bmatrix}$$']),
    (r'שני תנאים', [
      r'= סימטרית | $a+3b=-b\Rightarrow a=-4b$',
      r'= עקבה | $3a+5b=14\Rightarrow -7b=14\Rightarrow b=-2,\ a=8$']),
  ],
  ans=r'(ii) בסיס: $\begin{bmatrix}1&1\\0&2\end{bmatrix},\begin{bmatrix}2&3\\-1&3\end{bmatrix}$; (iii) $A=\begin{bmatrix}4&2\\2&10\end{bmatrix}$'),

dict(id='A2', exam='A', num='שאלה 2', pts=15, topics=['spaces'], level=2,
  q=r'במרחב $\mathbb{R}_2[X]$ נתונים $P_1=1+2X+X^2$, $P_2=3+2X+X^2$, $P_3=1-6X-3X^2$, $P_4=5-4X+2kX^2$, ו-$V=\operatorname{Span}\{P_1,P_2,P_3,P_4\}$. '
    r'(i) מצאו את $\dim(V)$ לפי ערכי $k$. (ii) כאשר $k=-1$ מצאו פולינום $P\in V$ כך ש-$P(1)=10$ ו-$P(0)=-5$.',
  steps=[
    (r'(i) וקטורי הקואורדינטות כשורות, ומדרגים', [
      r'$$\begin{bmatrix}1&2&1\\3&2&1\\1&-6&-3\\5&-4&2k\end{bmatrix}$$',
      r'↓ $L_2\to L_2-3L_1,\ L_3\to L_3-L_1,\ L_4\to L_4-5L_1$ | $[0,-4,-2]$, $[0,-8,-4]$, $[0,-14,2k-5]$',
      r'↓ $L_3\to L_3-2L_2,\ \ L_4\to L_4-\frac72L_2$ | $[0,0,0]$, $\ [0,0,2k+2]$']),
    (r'המימד = מספר השורות שאינן אפסים', [
      r'= $k\neq-1$ | $\dim V=3$ (כלומר $V=\mathbb{R}_2[X]$)',
      r'= $k=-1$ | $\dim V=2$']),
    (r'(ii) בסיס נוח כש-$k=-1$', [
      r'$P_2-P_1=2$, ולכן $1\in V$ וגם $P_1-1=2X+X^2\in V$:',
      r'= | $V=\operatorname{Span}\{1,\ 2X+X^2\}$',
      r'(בדיקה: $P_3=1-3(2X+X^2)$, $\ P_4=5-2(2X+X^2)$.)']),
    (r'מציבים את התנאים', [
      r'↓ $P=a+b(2X+X^2)$',
      r'↓ $P(0)=a=-5$',
      r'↓ $P(1)=a+3b=10\Rightarrow b=5$']),
  ],
  ans=r'(i) $\dim V=3$ אם $k\neq-1$, $\ \dim V=2$ אם $k=-1$; (ii) $P(X)=-5+10X+5X^2$'),

dict(id='A3', exam='A', num='שאלה 3', pts=15, topics=['complex'], level=1,
  q=r'יהי $z$ מספר מרוכב שמקיים $\operatorname{Re}(z)=\operatorname{Im}(z)$. הוכיחו: (i) $|z-1|=|z-i|$. (ii) $\frac{iz}{1-i}$ הוא מספר ממשי. (iii) $z^4+|z^4|=0$.',
  steps=[
    (r'כותבים את $z$', [
      r'= | $z=a+ai=a(1+i)$, $\ a\in\mathbb{R}$']),
    (r'(i)', [
      r'= | $|z-1|^2=(a-1)^2+a^2$',
      r'= | $|z-i|^2=a^2+(a-1)^2$',
      r'שני הביטויים שווים, ולכן $|z-1|=|z-i|$.']),
    (r'(ii)', [
      r'↓ $iz=ia(1+i)=a(i-1)=-a(1-i)$',
      r'↓ $\frac{iz}{1-i}=-a\in\mathbb{R}$']),
    (r'(iii) בהצגה קוטבית', [
      r'↓ $z=a\sqrt2\,e^{i\frac\pi4}$',
      r'↓ $z^4=4a^4e^{i\pi}=-4a^4$',
      r'↓ $|z^4|=4a^4\Rightarrow z^4+|z^4|=0$']),
  ],
  ans=r'שלוש הטענות נכונות (הוכחה בפתרון)'),

dict(id='A4', exam='A', num='שאלה 4', pts=15, topics=['matrices', 'det'], level=2,
  q=r'נתונה $A=\begin{bmatrix}k&0&1\\2&1&0\\0&1&k\end{bmatrix}$. (i) לאילו ערכים של $k$ המטריצה $A$ הפיכה? (ii) כאשר $A$ הפיכה מצאו את $A^{-1}$.',
  steps=[
    (r'(i) הדטרמיננטה (פיתוח לפי השורה הראשונה)', [
      r'$$\det A=k\begin{vmatrix}1&0\\1&k\end{vmatrix}-0+1\cdot\begin{vmatrix}2&1\\0&1\end{vmatrix}=k^2+2$$',
      r'$k^2+2>0$ לכל $k$ ממשי - ולכן $A$ הפיכה לכל $k$.']),
    (r'(ii) המינורים עם הסימנים, ואז שחלוף', [
      r'$$\operatorname{Adj}(A)=\begin{bmatrix}k&1&-1\\-2k&k^2&2\\2&-k&k\end{bmatrix}$$']),
    (r'מחלקים בדטרמיננטה', [
      r'$$A^{-1}=\frac{1}{k^2+2}\begin{bmatrix}k&1&-1\\-2k&k^2&2\\2&-k&k\end{bmatrix}$$',
      r'בדיקה: השורה הראשונה של $A$ כפול העמודה הראשונה: $k\cdot k+0+1\cdot2=k^2+2$ ✓']),
  ],
  ans=r'הפיכה לכל $k$; $\ A^{-1}=\frac{1}{k^2+2}\begin{bmatrix}k&1&-1\\-2k&k^2&2\\2&-k&k\end{bmatrix}$'),

dict(id='A5', exam='A', num='שאלה 5', pts=15, topics=['diag'], level=3,
  q=r'תהי $A=\begin{bmatrix}-1&1&-2\\1&-1&1\\1&-1&2\end{bmatrix}$. (i) קבעו אם $A$ ניתנת ללכסון; אם כן, מצאו $D$ אלכסונית ו-$P$ הפיכה כך ש-$D=P^{-1}AP$. (ii) מצאו את $\operatorname{Tr}(A^8)$.',
  steps=[
    (r'הפולינום האופייני', [
      r'$\operatorname{Tr}A=0$, $\ \det A=0$, וסכום המינורים הראשיים $2\times2$ הוא $0+0-1=-1$:',
      r'$$p_A(\lambda)=\lambda^3-\lambda=\lambda(\lambda-1)(\lambda+1)$$',
      r'שלושה ערכים עצמיים שונים: $-1,\ 0,\ 1$ - ולכן $A$ ניתנת ללכסון.']),
    (r'וקטורים עצמיים', [
      r'= $\lambda=-1$ | $(A+I)v=0\Rightarrow v=(-1,2,1)$',
      r'= $\lambda=0$ | $Av=0\Rightarrow v=(1,1,0)$',
      r'= $\lambda=1$ | $(A-I)v=0\Rightarrow v=(1,0,-1)$']),
    (r'$P$ ו-$D$', [
      r'$$P=\begin{bmatrix}-1&1&1\\2&1&0\\1&0&-1\end{bmatrix},\qquad D=\begin{bmatrix}-1&0&0\\0&0&0\\0&0&1\end{bmatrix}$$']),
    (r'(ii) העקבה של חזקה', [
      r'↓ $A^8=PD^8P^{-1}$',
      r'↓ $\operatorname{Tr}(A^8)=\operatorname{Tr}(D^8)$ | $\operatorname{Tr}(XY)=\operatorname{Tr}(YX)$',
      r'↓ $=(-1)^8+0^8+1^8=2$']),
  ],
  ans=r'ניתנת ללכסון, $D=\operatorname{diag}(-1,0,1)$; $\ \operatorname{Tr}(A^8)=2$'),

dict(id='A6a', exam='A', num='שאלה 6, חלק 1', pts=9, topics=['spaces'], level=2,
  q=r"יהי $V=\{P\in\mathbb{R}_3[X]\mid P''(1)+P'(1)+P(1)=0\}$. הוכיחו כי $V$ הוא תת-מרחב של $\mathbb{R}_3[X]$ ומצאו לו בסיס.",
  steps=[
    (r'תת-מרחב', [
      r"הביטוי $\varphi(P)=P''(1)+P'(1)+P(1)$ לינארי ב-$P$ (נגזרת והצבה לינאריות), ו-$V=\{P\mid\varphi(P)=0\}$:",
      r'= | $\varphi(0)=0$ - האפס ב-$V$',
      r'= | $\varphi(P+Q)=\varphi(P)+\varphi(Q)=0$ - סגור לחיבור',
      r'= | $\varphi(\lambda P)=\lambda\varphi(P)=0$ - סגור לכפל בסקלר']),
    (r'התנאי במקדמים', [
      r'↓ $P=a+bX+cX^2+dX^3$',
      r"↓ $P(1)=a+b+c+d,\ \ P'(1)=b+2c+3d,\ \ P''(1)=2c+6d$",
      r'↓ $a+2b+5c+10d=0\Rightarrow a=-2b-5c-10d$']),
    (r'בסיס (משתנים חופשיים $b,c,d$)', [
      r'$$P=b(X-2)+c(X^2-5)+d(X^3-10)$$',
      r'שלושת הפולינומים בלתי תלויים (מעלות שונות), ולכן $\dim V=3$.']),
  ],
  ans=r'בסיס: $\{X-2,\ X^2-5,\ X^3-10\}$, $\ \dim V=3$'),

dict(id='A6b', exam='A', num='שאלה 6, חלק 2', pts=6, topics=['matrices'], level=1,
  q=r'(i) תנו דוגמה לשתי מטריצות שונות, סימטריות והפיכות $A,B\in M_2(\mathbb{R})$ כך ש-$AB$ סימטרית. (ii) כנ"ל, כך ש-$AB$ לא סימטרית.',
  steps=[
    (r'(i) מטריצות אלכסוניות מתחלפות', [
      r'= | $A=\begin{bmatrix}1&0\\0&2\end{bmatrix},\ B=\begin{bmatrix}3&0\\0&4\end{bmatrix}$',
      r'= | $AB=\begin{bmatrix}3&0\\0&8\end{bmatrix}$ - סימטרית',
      r'(באופן כללי: $(AB)^t=B^tA^t=BA$, ולכן $AB$ סימטרית בדיוק כש-$AB=BA$.)']),
    (r'(ii) מטריצות שלא מתחלפות', [
      r'= | $A=\begin{bmatrix}1&1\\1&2\end{bmatrix}$ ($\det=1$), $\ B=\begin{bmatrix}1&0\\0&2\end{bmatrix}$',
      r'= | $AB=\begin{bmatrix}1&2\\1&4\end{bmatrix}$ - לא סימטרית']),
  ],
  ans=r'למשל (i) $\operatorname{diag}(1,2),\ \operatorname{diag}(3,4)$; (ii) $\begin{bmatrix}1&1\\1&2\end{bmatrix},\ \operatorname{diag}(1,2)$'),

dict(id='A7a', exam='A', num='שאלה 7, חלק 1', pts=10, topics=['inner', 'systems'], level=3,
  q=r'יהי $V=\left\{(x,y,z,t)\in\mathbb{R}^4\ \middle|\ x-2y-3z+8t=0,\ x-2y-2z+5t=0,\ 2x-4y-3z+7t=0\right\}$. מצאו בסיס אורתונורמלי ל-$V$.',
  steps=[
    (r'פותרים את המערכת ההומוגנית', [
      r'$$\begin{bmatrix}1&-2&-3&8\\1&-2&-2&5\\2&-4&-3&7\end{bmatrix}\longrightarrow\begin{bmatrix}1&-2&0&-1\\0&0&1&-3\\0&0&0&0\end{bmatrix}$$',
      r'$y=s,\ t=r$ חופשיים: $\ z=3r,\ \ x=2s+r$.']),
    (r'בסיס ל-$V$', [
      r'= | $u_1=(2,1,0,0),\ \ u_2=(1,0,3,1)$',
      r'$\langle u_1,u_2\rangle=2\neq0$ - לא אורתוגונליים, ולכן גרם-שמידט.']),
    (r'גרם-שמידט', [
      r'↓ $w_1=u_1=(2,1,0,0)$',
      r'↓ $w_2=u_2-\frac{\langle u_2,w_1\rangle}{\|w_1\|^2}w_1=(1,0,3,1)-\frac25(2,1,0,0)$',
      r'↓ $=\frac15(1,-2,15,5)$ | מכפילים ב-5: $(1,-2,15,5)$']),
    (r'מנרמלים', [
      r'= | $\|w_1\|=\sqrt5,\ \ \|(1,-2,15,5)\|=\sqrt{255}$']),
  ],
  ans=r'$\left\{\frac{1}{\sqrt5}(2,1,0,0),\ \frac{1}{\sqrt{255}}(1,-2,15,5)\right\}$'),

dict(id='A7b', exam='A', num='שאלה 7, חלק 2', pts=5, topics=['det'], level=2,
  q=r'נתון: $\det\begin{pmatrix}14x&21r&7u\\2y+4x&3s+6r&v+2u\\4z&6t&2w\end{pmatrix}=56$. חשבו את $\det\begin{pmatrix}x&y&z\\u&v&w\\r&s&t\end{pmatrix}$.',
  steps=[
    (r'מפשטים את השורות', [
      r'↓ שורה 1: מוציאים 7 | $(2x,\ 3r,\ u)$',
      r'↓ שורה 3: מוציאים 2 | $(2z,\ 3t,\ w)$',
      r'↓ $L_2\to L_2-2L_1$ | $(2y,\ 3s,\ v)$ - הדטרמיננטה לא משתנה',
      r'$$56=14\det\begin{pmatrix}2x&3r&u\\2y&3s&v\\2z&3t&w\end{pmatrix}$$']),
    (r'מוציאים מהעמודות ומשחלפים', [
      r'↓ עמודה 1: 2, עמודה 2: 3 | $56=84\det\begin{pmatrix}x&r&u\\y&s&v\\z&t&w\end{pmatrix}$',
      r'↓ שחלוף | $=84\det\begin{pmatrix}x&y&z\\r&s&t\\u&v&w\end{pmatrix}$',
      r'↓ החלפת שורות 2, 3 | $=-84\det\begin{pmatrix}x&y&z\\u&v&w\\r&s&t\end{pmatrix}$']),
    (r'התוצאה', [
      r'$$\det\begin{pmatrix}x&y&z\\u&v&w\\r&s&t\end{pmatrix}=-\frac{56}{84}=-\frac23$$']),
  ],
  ans=r'$-\frac23$'),

dict(id='Am1', exam='A', num='חלק ב, שאלה 1', pts=5, topics=['complex'], level=1, mc=True,
  q=r'נתון: $(4-3i)^3z=25e^{\frac{5\pi i}{7}}\,i(1+3i)^2$. איזו טענה נכונה? ' + opts(r'$|z|=2$', r'$|z|=1$', r'$|z|=5$', r'$|z|=4$'),
  steps=[
    (r'לוקחים ערך מוחלט לשני האגפים', [
      r'= | $|4-3i|^3=5^3=125$',
      r'= | $\left|25e^{\frac{5\pi i}7}\right|\cdot|i|\cdot|1+3i|^2=25\cdot1\cdot1\cdot10=250$',
      r'↓ $125|z|=250\Rightarrow|z|=2$']),
  ],
  ans=r'א. $|z|=2$'),

dict(id='Am2', exam='A', num='חלק ב, שאלה 2', pts=5, topics=['matrices', 'det'], level=3, mc=True,
  q=r'נתונות $A,B,C\in M_7(\mathbb{R})$ שמקיימות $ACA+AC=I_7$ וגם $AB+BA=0$. איזו טענה נכונה? '
    + opts(r'בהכרח $A$ הפיכה ו-$B$ לא הפיכה', r'בהכרח $A$ הפיכה ו-$B$ הפיכה', r'בהכרח $A$ לא הפיכה ו-$B$ לא הפיכה', r'בהכרח $A$ לא הפיכה ו-$B$ הפיכה'),
  steps=[
    (r'$A$ הפיכה', [
      r'$A(CA+C)=I_7$ - ולכן $A$ הפיכה.']),
    (r'$B$ לא הפיכה', [
      r'↓ $AB=-BA$',
      r'↓ $\det A\det B=(-1)^7\det B\det A=-\det A\det B$',
      r'↓ $\det A\det B=0$, ו-$\det A\neq0$ | $\det B=0$']),
  ],
  ans=r'א'),

dict(id='Am3', exam='A', num='חלק ב, שאלה 3', pts=5, topics=['linmap'], level=2, mc=True,
  q=r'$T:\mathbb{R}_3[X]\to M_2(\mathbb{R})$ לינארית ו-$T(1+X^2)=T(X+X^3)=0$. איזו טענה נכונה? '
    + opts(r'בהכרח $\dim\operatorname{Ker}T\geq\dim\operatorname{Im}T$', r'בהכרח $\dim\operatorname{Ker}T\leq\dim\operatorname{Im}T$', r'בהכרח $\dim\operatorname{Ker}T=\dim\operatorname{Im}T$', r'בהכרח $\dim\operatorname{Ker}T\neq\dim\operatorname{Im}T$'),
  steps=[
    (r'הגרעין לפחות 2', [
      r'$1+X^2$ ו-$X+X^3$ בלתי תלויים ושניהם בגרעין: $\dim\operatorname{Ker}T\geq2$.']),
    (r'משפט המימדים', [
      r'↓ $\dim\operatorname{Ker}T+\dim\operatorname{Im}T=\dim\mathbb{R}_3[X]=4$',
      r'↓ $\dim\operatorname{Im}T\leq2\leq\dim\operatorname{Ker}T$',
      r'(ג ו-ד לא בהכרח: אם הגרעין בדיוק 2 - יש שוויון, ואם 3 - אין.)']),
  ],
  ans=r'א'),

dict(id='Am4', exam='A', num='חלק ב, שאלה 4', pts=5, topics=['det'], level=2, mc=True,
  q=r'תהי $A\in M_3(\mathbb{R})$ עם $\det(A)=\frac12$. איזו טענה נכונה? '
    + opts(r'$\det(\operatorname{Adj}(2A))=16$', r'$\det(\operatorname{Adj}(2A))=32$', r'$\det(\operatorname{Adj}(2A))=8$', r'$\det(\operatorname{Adj}(2A))=4$'),
  steps=[
    (r'שתי נוסחאות', [
      r'= | $\det(\operatorname{Adj}B)=(\det B)^{n-1}$',
      r'= | $\det(2A)=2^3\det A=4$']),
    (r'מציבים', [
      r'$$\det(\operatorname{Adj}(2A))=4^{3-1}=16$$']),
  ],
  ans=r'א'),

dict(id='Am5', exam='A', num='חלק ב, שאלה 5', pts=5, topics=['spaces'], level=2, mc=True,
  q=r'$\vec u,\vec v\in\mathbb{R}^3$ בלתי תלויים, $\vec z=3\vec u+3\vec v$ ו-$\vec w=12\vec u+\vec v-4\vec z$. איזו טענה <b>לא</b> נכונה? '
    + opts(r'$\operatorname{span}\{\vec u,\vec w\}=\operatorname{span}\{\vec v,\vec w\}$', r'$\operatorname{span}\{\vec u,\vec v,\vec z\}=\operatorname{span}\{\vec u,\vec v\}$',
           r'$\operatorname{span}\{\vec u,\vec v,\vec w\}=\operatorname{span}\{\vec u,\vec z\}$', r'$\operatorname{span}\{\vec u,\vec z\}=\operatorname{span}\{\vec u,\vec w\}$'),
  steps=[
    (r'מפשטים את $\vec w$', [
      r'$$\vec w=12\vec u+\vec v-12\vec u-12\vec v=-11\vec v$$']),
    (r'בודקים כל טענה', [
      r'= א | $\operatorname{span}\{\vec u,\vec v\}$ מול $\operatorname{span}\{\vec v\}$ - שונים ✗',
      r'= ב | $\vec z\in\operatorname{span}\{\vec u,\vec v\}$ ✓',
      r'= ג | שני האגפים $=\operatorname{span}\{\vec u,\vec v\}$ ✓',
      r'= ד | שני האגפים $=\operatorname{span}\{\vec u,\vec v\}$ ✓']),
  ],
  ans=r'א'),

# ============================================================== מועד ב
dict(id='B1', exam='B', num='שאלה 1', pts=15, topics=['linmap'], level=2,
  q=r'תהי $T:\mathbb{R}_3[X]\to M_2(\mathbb{R})$: $T(a+bX+cX^2+dX^3)=\begin{bmatrix}2a-b+5d&b-c+d\\2a-c+6d&2a+b-2c+7d\end{bmatrix}$. '
    r"(i) מצאו את המטריצה הסטנדרטית. (ii) מצאו בסיס ל-$\operatorname{Ker}(T)$. (iii) מצאו את כל $P\in\operatorname{Ker}(T)$ שמקיימים $P(0)=10$ ו-$P'(0)=5$.",
  steps=[
    (r'(i)', [
      r'$$[T]=\begin{bmatrix}2&-1&0&5\\0&1&-1&1\\2&0&-1&6\\2&1&-2&7\end{bmatrix}$$']),
    (r'(ii) מדרגים', [
      r'↓ $L_3\to L_3-L_1,\ \ L_4\to L_4-L_1$ | $[0,1,-1,1]$, $\ [0,2,-2,2]$',
      r'↓ $L_3\to L_3-L_2,\ \ L_4\to L_4-2L_2$ | שתי שורות אפסים',
      r'נשאר: $2a-b+5d=0$, $\ b-c+d=0$ ⇒ $b=c-d$, $\ a=\frac c2-3d$.']),
    (r'בסיס לגרעין', [
      r'= $c=2,\ d=0$ | $1+2X+2X^2$',
      r'= $c=0,\ d=1$ | $-3-X+X^3$']),
    (r'(iii)', [
      r'↓ $P=\alpha(1+2X+2X^2)+\beta(-3-X+X^3)$',
      r"↓ $P(0)=\alpha-3\beta=10,\ \ P'(0)=2\alpha-\beta=5$",
      r'↓ $\alpha=1,\ \beta=-3$']),
  ],
  ans=r'בסיס: $\{1+2X+2X^2,\ -3-X+X^3\}$; $\ P=10+5X+2X^2-3X^3$ (הפולינום היחיד)'),

dict(id='B2', exam='B', num='שאלה 2', pts=15, topics=['spaces'], level=2,
  q=r'במרחב $M_2(\mathbb{R})$: $M_1=\begin{bmatrix}1&2\\1&2\end{bmatrix},M_2=\begin{bmatrix}2&1\\5&1\end{bmatrix},M_3=\begin{bmatrix}3&5\\4&5\end{bmatrix},M_4=\begin{bmatrix}1&0\\3&0\end{bmatrix}$, $V=\operatorname{Span}\{M_1,M_2,M_3,M_4\}$. '
    r'(i) מצאו בסיס $\Gamma$ ל-$V$ ואת $\dim V$. (ii) לאילו $k$: $\begin{bmatrix}4&k\\7&k\end{bmatrix}\in V$? (iii) מצאו $A\in V$ כך ש-$A\begin{bmatrix}1\\1\end{bmatrix}=\begin{bmatrix}0\\1\end{bmatrix}$.',
  steps=[
    (r'(i) וקטורי קואורדינטות כעמודות, ומדרגים', [
      r'$$\begin{bmatrix}1&2&3&1\\2&1&5&0\\1&5&4&3\\2&1&5&0\end{bmatrix}\longrightarrow\begin{bmatrix}1&0&\frac73&-\frac13\\0&1&\frac13&\frac23\\0&0&0&0\\0&0&0&0\end{bmatrix}$$',
      r'= | $M_3=\frac13(7M_1+M_2)$, $\ M_4=\frac13(2M_2-M_1)$',
      r'בסיס $\Gamma=\{M_1,M_2\}$, $\ \dim V=2$.']),
    (r'(ii)', [
      r'$$aM_1+bM_2=\begin{bmatrix}a+2b&2a+b\\a+5b&2a+b\end{bmatrix}=\begin{bmatrix}4&k\\7&k\end{bmatrix}$$',
      r'↓ $a+2b=4,\ a+5b=7\Rightarrow b=1,\ a=2$',
      r'↓ $k=2a+b=5$']),
    (r'(iii)', [
      r'↓ $A\begin{bmatrix}1\\1\end{bmatrix}=\begin{bmatrix}3a+3b\\3a+6b\end{bmatrix}=\begin{bmatrix}0\\1\end{bmatrix}$',
      r'↓ $a=-b,\ \ 3b=1\Rightarrow b=\frac13,\ a=-\frac13$']),
  ],
  ans=r'(i) $\Gamma=\{M_1,M_2\}$, $\dim V=2$; (ii) $k=5$; (iii) $A=\begin{bmatrix}\frac13&-\frac13\\\frac43&-\frac13\end{bmatrix}$'),

dict(id='B3a', exam='B', num='שאלה 3, חלק 1', pts=9, topics=['complex'], level=2,
  q=r'מצאו את כל הפתרונות המרוכבים של המשוואה $z^4+8iz=0$.',
  steps=[
    (r'מוציאים גורם משותף', [
      r'↓ $z(z^3+8i)=0$',
      r'↓ $z=0$ או $z^3=-8i=8e^{-i\frac\pi2}$']),
    (r'שורשים שלישיים', [
      r'$$z_k=2e^{i\left(-\frac\pi6+\frac{2\pi k}3\right)},\quad k=0,1,2$$',
      r'= $k=0$ | $2e^{-i\frac\pi6}=\sqrt3-i$',
      r'= $k=1$ | $2e^{i\frac\pi2}=2i$',
      r'= $k=2$ | $2e^{i\frac{7\pi}6}=-\sqrt3-i$']),
  ],
  ans=r'$z\in\{0,\ 2i,\ \sqrt3-i,\ -\sqrt3-i\}$'),

dict(id='B3b', exam='B', num='שאלה 3, חלק 2', pts=6, topics=['matrices'], level=2,
  q=r'נתונות $A,B\in M_5(\mathbb{R})$ שמקיימות $A^2+AB+2A+3I=0$. (i) הוכיחו ש-$A$ רגולרית ומצאו את $A^{-1}$. (ii) הוכיחו ש-$AB=BA$.',
  steps=[
    (r'(i) $A$ כגורם משותף משמאל', [
      r'↓ $A(A+B+2I)=-3I$',
      r'↓ $A\cdot\left(-\frac13(A+B+2I)\right)=I$',
      r'$A$ הפיכה, ו-$A^{-1}=-\frac13(A+B+2I)$.']),
    (r'(ii) גם בסדר ההפוך', [
      r'↓ $A^{-1}A=I\Rightarrow-\frac13(A+B+2I)A=I$',
      r'↓ $A^2+BA+2A=-3I$',
      r'↓ משווים ל-$A^2+AB+2A=-3I$ | $AB=BA$']),
  ],
  ans=r'$A^{-1}=-\frac13(A+B+2I)$, ומכאן $AB=BA$'),

dict(id='B4', exam='B', num='שאלה 4', pts=15, topics=['systems', 'det'], level=2,
  q=r'נתונה $A=\begin{bmatrix}2&k&0\\1&-1&k\\3&k&1\end{bmatrix}$, $k\in\mathbb{R}$. (i) מצאו את $\operatorname{rank}(A)$ לפי $k$. (ii) לאילו $k$ למערכת $A\vec x=\begin{bmatrix}2\\3\\4\end{bmatrix}$ יש אינסוף פתרונות? רשמו את הפתרונות.',
  steps=[
    (r'(i) הדטרמיננטה', [
      r'$$\det A=2(-1-k^2)-k(1-3k)=k^2-k-2=(k-2)(k+1)$$',
      r'= $k\neq2,-1$ | $\operatorname{rank}A=3$',
      r'= $k=2$ או $k=-1$ | $\operatorname{rank}A=2$ (יש שתי שורות בלתי תלויות)']),
    (r'(ii) $k=-1$', [
      r'המטריצה המורחבת מדורגת ל: $\left[\begin{array}{ccc|c}1&0&1&0\\0&1&2&0\\0&0&0&1\end{array}\right]$ - סתירה, אין פתרון.']),
    (r'$k=2$', [
      r'$$\left[\begin{array}{ccc|c}2&2&0&2\\1&-1&2&3\\3&2&1&4\end{array}\right]\longrightarrow\left[\begin{array}{ccc|c}1&0&1&2\\0&1&-1&-1\\0&0&0&0\end{array}\right]$$',
      r'$z=t$ חופשי: $\ x=2-t,\ \ y=t-1$.']),
  ],
  ans=r'(i) דרגה 3 אם $k\neq2,-1$, אחרת 2; (ii) $k=2$: $\{(2-t,\ t-1,\ t)\}_{t\in\mathbb{R}}$'),

dict(id='B5', exam='B', num='שאלה 5', pts=15, topics=['diag'], level=3,
  q=r'תהי $A=\begin{bmatrix}0&-1&1\\0&2&0\\-2&-1&3\end{bmatrix}$. (i) קבעו אם $A$ ניתנת ללכסון; אם כן, מצאו $D$ ו-$P$ עם $D=P^{-1}AP$. (ii) נגדיר $B=A^3-2A+I$. מצאו את הערכים העצמיים של $B$. האם $B$ ניתנת ללכסון?',
  steps=[
    (r'הפולינום האופייני (פיתוח לפי השורה השנייה)', [
      r'$$\det(A-\lambda I)=(2-\lambda)\begin{vmatrix}-\lambda&1\\-2&3-\lambda\end{vmatrix}=(2-\lambda)(\lambda-1)(\lambda-2)$$',
      r'= | $\lambda=1$ (פעם אחת), $\ \lambda=2$ (פעמיים)']),
    (r'וקטורים עצמיים', [
      r'= $\lambda=2$ | $-2x-y+z=0$: $\ (1,0,2),\ (0,1,1)$ - מימד 2',
      r'= $\lambda=1$ | $y=0,\ z=x$: $\ (1,0,1)$',
      r'לכל ערך עצמי הריבוי הגיאומטרי שווה לאלגברי - ניתנת ללכסון.']),
    (r'$P$ ו-$D$', [
      r'$$P=\begin{bmatrix}1&1&0\\0&0&1\\1&2&1\end{bmatrix},\qquad D=\begin{bmatrix}1&0&0\\0&2&0\\0&0&2\end{bmatrix}$$']),
    (r'(ii) $B=p(A)$ עם $p(\lambda)=\lambda^3-2\lambda+1$', [
      r'↓ $B=P\,p(D)\,P^{-1}$',
      r'↓ $p(1)=0,\ \ p(2)=5$',
      r'הערכים העצמיים של $B$: $0$ ו-$5$ (פעמיים), ו-$B$ ניתנת ללכסון (על ידי אותה $P$).']),
  ],
  ans=r'(i) כן, $D=\operatorname{diag}(1,2,2)$; (ii) $0,5$, ו-$B$ ניתנת ללכסון'),

dict(id='B6a', exam='B', num='שאלה 6, חלק 1', pts=9, topics=['spaces'], level=2,
  q=r'יהי $V=\left\{M\in M_2(\mathbb{R})\ \middle|\ M\begin{bmatrix}3&1\\1&1\end{bmatrix}=\begin{bmatrix}3&1\\1&1\end{bmatrix}M^t\right\}$. הוכיחו כי $V$ תת-מרחב של $M_2(\mathbb{R})$ ומצאו לו בסיס.',
  steps=[
    (r'תת-מרחב', [
      r'נסמן $S=\begin{bmatrix}3&1\\1&1\end{bmatrix}$. $V$ הוא הגרעין של ההעתקה הלינארית $M\mapsto MS-SM^t$, ולכן תת-מרחב:',
      r'= | $0\in V$',
      r'= | $(M+N)S-S(M+N)^t=(MS-SM^t)+(NS-SN^t)=0$',
      r'= | $(\lambda M)S-S(\lambda M)^t=\lambda(MS-SM^t)=0$']),
    (r'התנאי במקדמים', [
      r'$M=\begin{bmatrix}m_1&m_2\\m_3&m_4\end{bmatrix}$:',
      r'= | $MS=\begin{bmatrix}3m_1+m_2&m_1+m_2\\3m_3+m_4&m_3+m_4\end{bmatrix}$',
      r'= | $SM^t=\begin{bmatrix}3m_1+m_2&3m_3+m_4\\m_1+m_2&m_3+m_4\end{bmatrix}$',
      r'נשאר תנאי אחד: $m_1+m_2=3m_3+m_4$.']),
    (r'בסיס', [
      r'$m_1=-m_2+3m_3+m_4$, ו-$m_2,m_3,m_4$ חופשיים:',
      r'$$\left\{\begin{bmatrix}-1&1\\0&0\end{bmatrix},\begin{bmatrix}3&0\\1&0\end{bmatrix},\begin{bmatrix}1&0\\0&1\end{bmatrix}\right\}$$']),
  ],
  ans=r'בסיס: $\begin{bmatrix}-1&1\\0&0\end{bmatrix},\begin{bmatrix}3&0\\1&0\end{bmatrix},\begin{bmatrix}1&0\\0&1\end{bmatrix}$, $\ \dim V=3$'),

dict(id='B6b', exam='B', num='שאלה 6, חלק 2', pts=6, topics=['diag', 'matrices'], level=1,
  q=r'(i) תנו דוגמה לשתי מטריצות שונות $A,B\in M_2(\mathbb{R})$ שקולות שורה כך ש-$\operatorname{Spec}(A)=\operatorname{Spec}(B)$. (ii) כנ"ל, כך ש-$\operatorname{Spec}(A)\neq\operatorname{Spec}(B)$.',
  steps=[
    (r'רעיון', [
      r'כל שתי מטריצות הפיכות $2\times2$ שקולות שורה (שתיהן שקולות ל-$I$).']),
    (r'(i)', [
      r'= | $A=\begin{bmatrix}1&0\\0&2\end{bmatrix},\ B=\begin{bmatrix}2&0\\0&1\end{bmatrix}$',
      r'= | $\operatorname{Spec}(A)=\operatorname{Spec}(B)=\{1,2\}$']),
    (r'(ii)', [
      r'= | $A=I,\ B=2I$',
      r'= | $\operatorname{Spec}(A)=\{1\}\neq\{2\}=\operatorname{Spec}(B)$']),
  ],
  ans=r'למשל (i) $\operatorname{diag}(1,2),\ \operatorname{diag}(2,1)$; (ii) $I,\ 2I$'),

dict(id='B7a', exam='B', num='שאלה 7, חלק 1', pts=10, topics=['inner', 'linmap'], level=3,
  q=r'$T:\mathbb{R}^3\to\mathbb{R}^4$, $\ T(x,y,z)=(x+2z,\ x+2y,\ 2x+y+3z,\ y-z)$. מצאו בסיס אורתונורמלי ל-$\operatorname{Im}(T)$.',
  steps=[
    (r'התמונה נפרשת על ידי העמודות', [
      r'= | $c_1=(1,1,2,0),\ c_2=(0,2,1,1),\ c_3=(2,0,3,-1)$',
      r'= | $c_3=2c_1-c_2$ - ולכן בסיס $\{c_1,c_2\}$, $\ \dim\operatorname{Im}T=2$']),
    (r'גרם-שמידט', [
      r'↓ $w_1=c_1=(1,1,2,0)$',
      r'↓ $w_2=c_2-\frac{\langle c_2,w_1\rangle}{\|w_1\|^2}w_1=(0,2,1,1)-\frac46(1,1,2,0)$',
      r'↓ $=\frac13(-2,4,-1,3)$']),
    (r'מנרמלים', [
      r'= | $\|(1,1,2,0)\|=\sqrt6,\ \ \|(-2,4,-1,3)\|=\sqrt{30}$']),
  ],
  ans=r'$\left\{\frac1{\sqrt6}(1,1,2,0),\ \frac1{\sqrt{30}}(-2,4,-1,3)\right\}$'),

dict(id='B7b', exam='B', num='שאלה 7, חלק 2', pts=5, topics=['linmap'], level=1,
  q=r'תנו דוגמה להעתקה לינארית $T:\mathbb{R}^2\to\mathbb{R}^2$ כך ש-$\operatorname{Ker}(T)=\operatorname{Im}(T)$.',
  steps=[
    (r'מימדים', [
      r'$\dim\operatorname{Ker}+\dim\operatorname{Im}=2$ ושניהם שווים - כל אחד 1.']),
    (r'דוגמה', [
      r'= | $T(x,y)=(0,x)$',
      r'= | $\operatorname{Ker}T=\{(0,y)\}=\operatorname{Span}\{(0,1)\}$',
      r'= | $\operatorname{Im}T=\{(0,x)\}=\operatorname{Span}\{(0,1)\}$']),
  ],
  ans=r'למשל $T(x,y)=(0,x)$'),

dict(id='Bm1', exam='B', num='חלק ב, שאלה 1', pts=5, topics=['complex'], level=1, mc=True,
  q=r'$z$ מרוכב שמקיים $(z-\bar z)(z+\bar z)=0$. איזו טענה נכונה? '
    + opts(r'$z^3\bar z$ בהכרח ממשי', r'$z^3\bar z$ בהכרח מדומה טהור', r'$z^2\bar z$ בהכרח ממשי', r'$z^2\bar z$ בהכרח מדומה טהור'),
  steps=[
    (r'מה הנתון אומר', [
      r'$z-\bar z=2i\operatorname{Im}z$, $\ z+\bar z=2\operatorname{Re}z$ - ולכן $z$ ממשי או מדומה טהור.']),
    (r'בודקים', [
      r'= | $z^3\bar z=z^2|z|^2$, ו-$z^2$ ממשי בשני המקרים ⇒ ממשי ✓',
      r'= | $z^2\bar z=z|z|^2$ - ממשי או מדומה, תלוי ב-$z$']),
  ],
  ans=r'א'),

dict(id='Bm2', exam='B', num='חלק ב, שאלה 2', pts=5, topics=['linmap'], level=1, mc=True,
  q=r'נתונה העתקה לינארית $T:M_{4,2}(\mathbb{R})\to\mathbb{R}_8[X]$. איזו טענה נכונה? '
    + opts(r'$T$ בהכרח לא על', r'$T$ בהכרח על', r'$T$ בהכרח חד-חד ערכית', r'$T$ בהכרח לא חד-חד ערכית'),
  steps=[
    (r'מימדים', [
      r'= | $\dim M_{4,2}=8$, $\ \dim\mathbb{R}_8[X]=9$',
      r'= | $\dim\operatorname{Im}T\leq8<9$ ⇒ לא על',
      r'(חד-חד ערכיות - תלויה ב-$T$: גם העתקת האפס אפשרית.)']),
  ],
  ans=r'א'),

dict(id='Bm3', exam='B', num='חלק ב, שאלה 3', pts=5, topics=['det', 'matrices'], level=2, mc=True,
  q=r'$A\in M_3(\mathbb{R})$ ו-$A^{-1}=\begin{bmatrix}2&0&3\\1&2&1\\2&-2&1\end{bmatrix}$. איזו טענה נכונה? '
    + opts(r'$\operatorname{Tr}(\operatorname{Adj}A)=-\frac12$', r'$\operatorname{Tr}(\operatorname{Adj}A)=\frac12$', r'$\operatorname{Tr}(\operatorname{Adj}A)=2$', r'$\operatorname{Tr}(\operatorname{Adj}A)=-2$'),
  steps=[
    (r'$\operatorname{Adj}A=\det(A)\,A^{-1}$', [
      r'= | $\det(A^{-1})=2(2+2)+3(-2-4)=-10\Rightarrow\det A=-\frac1{10}$',
      r'= | $\operatorname{Tr}(A^{-1})=2+2+1=5$']),
    (r'מצרפים', [
      r'$$\operatorname{Tr}(\operatorname{Adj}A)=-\frac1{10}\cdot5=-\frac12$$',
      r'(בשאלה המקורית כתוב $M_2$ - זו טעות הקלדה, ההופכית היא $3\times3$.)']),
  ],
  ans=r'א'),

dict(id='Bm4', exam='B', num='חלק ב, שאלה 4', pts=5, topics=['spaces'], level=2, mc=True,
  q=r'$\{\vec u,\vec v,\vec w\}$ קבוצה פורשת של $\mathbb{R}^3$. איזו טענה <b>לא</b> נכונה? '
    + opts(r'$\{2\vec u+\vec v,\ \vec v+2\vec w,\ \vec u+\vec v+\vec w\}$ בהכרח פורשת', r'$\{\vec u,\ \vec u+2\vec v+\vec w,\ \vec u+\vec v+3\vec w\}$ בהכרח בת"ל',
           r'$\{2\vec u+\vec v,\ \vec v+2\vec w,\ 3\vec u+3\vec w\}$ בהכרח בת"ל', r'$\{\vec u+\vec v+\vec w,\ \vec u,\ \vec w\}$ בהכרח פורשת'),
  steps=[
    (r'$\{\vec u,\vec v,\vec w\}$ בסיס - בודקים דטרמיננטת המקדמים', [
      r'= א | $\begin{vmatrix}2&1&0\\0&1&2\\1&1&1\end{vmatrix}=0$ ⇒ תלויה, לא פורשת ✗',
      r'= ב | $\begin{vmatrix}1&0&0\\1&2&1\\1&1&3\end{vmatrix}=5\neq0$ ✓',
      r'= ג | $\begin{vmatrix}2&1&0\\0&1&2\\3&0&3\end{vmatrix}=12\neq0$ ✓',
      r'= ד | $\begin{vmatrix}1&1&1\\1&0&0\\0&0&1\end{vmatrix}=-1\neq0$ ✓']),
  ],
  ans=r'א'),

dict(id='Bm5', exam='B', num='חלק ב, שאלה 5', pts=5, topics=['det'], level=2, mc=True,
  q=r'$A\in M_3(\mathbb{R})$ הפיכה ו-$\det(3AA^t)+5\det(\operatorname{Adj}A)=\det(2A)$. איזו טענה נכונה? '
    + opts(r'$\det A=\frac14$', r'$\det A=4$', r'$\det A=\frac19$', r'$\det A=9$'),
  steps=[
    (r'מסמנים $d=\det A$', [
      r'= | $\det(3AA^t)=27d^2$',
      r'= | $\det(\operatorname{Adj}A)=d^{2}$',
      r'= | $\det(2A)=8d$']),
    (r'פותרים', [
      r'↓ $27d^2+5d^2=8d$',
      r'↓ $32d^2=8d$, $\ d\neq0$ | $d=\frac14$']),
  ],
  ans=r'א'),

# ============================================================== מבחן דוגמה
dict(id='S1', exam='S', num='שאלה 1', pts=15, topics=['linmap'], level=2,
  q=r'$T:M_2(\mathbb{R})\to\mathbb{R}_2[X]$, $\ T\begin{bmatrix}a&b\\c&d\end{bmatrix}=(a-2d)+(a+2b+4c)X+(b+2c+d)X^2$. '
    r'(i) מצאו את המטריצה הסטנדרטית. (ii) מצאו בסיס ל-$\operatorname{Ker}(T)$. (iii) תנו דוגמה למטריצה $A\in\operatorname{Ker}(T)$ סימטרית והפיכה.',
  steps=[
    (r'(i)', [
      r'$$[T]=\begin{bmatrix}1&0&0&-2\\1&2&4&0\\0&1&2&1\end{bmatrix}$$']),
    (r'(ii) מדרגים', [
      r'$$\begin{bmatrix}1&0&0&-2\\1&2&4&0\\0&1&2&1\end{bmatrix}\longrightarrow\begin{bmatrix}1&0&0&-2\\0&1&2&1\\0&0&0&0\end{bmatrix}$$',
      r'$a=2d$, $\ b=-2c-d$; $\ c,d$ חופשיים:',
      r'= $c=1,\ d=0$ | $\begin{bmatrix}0&-2\\1&0\end{bmatrix}$',
      r'= $c=0,\ d=1$ | $\begin{bmatrix}2&-1\\0&1\end{bmatrix}$']),
    (r'(iii)', [
      r'↓ $A=\alpha\begin{bmatrix}0&-2\\1&0\end{bmatrix}+\beta\begin{bmatrix}2&-1\\0&1\end{bmatrix}=\begin{bmatrix}2\beta&-2\alpha-\beta\\\alpha&\beta\end{bmatrix}$',
      r'↓ סימטרית: $-2\alpha-\beta=\alpha$ | $\beta=-3\alpha$',
      r'↓ $\alpha=1$ | $A=\begin{bmatrix}-6&1\\1&-3\end{bmatrix}$, $\ \det A=17\neq0$']),
  ],
  ans=r'בסיס: $\begin{bmatrix}0&-2\\1&0\end{bmatrix},\begin{bmatrix}2&-1\\0&1\end{bmatrix}$; $\ A=\begin{bmatrix}-6&1\\1&-3\end{bmatrix}$'),

dict(id='S2', exam='S', num='שאלה 2', pts=15, topics=['spaces'], level=3,
  q=r'במרחב $\mathbb{R}_2[X]$: $P_1=1+X+X^2$, $P_2=5-X+X^2$, $P_3=3+X^2$, $P_4=5+2X+3X^2$, $P_5=2-X$, ו-$V=\operatorname{Span}\{P_1,\dots,P_5\}$. '
    r'(i) מצאו בסיס $\Gamma$ ל-$V$ ואת $\dim V$. (ii) לאילו $k$: $Q=k+2kX+X^2\in V$? (iii) מצאו $P\in V$ עם $P(1)=1$, $P(-1)=2$, ואת $[P]_\Gamma$.',
  steps=[
    (r'(i) קואורדינטות כעמודות ומדרגים', [
      r'$$\begin{bmatrix}1&5&3&5&2\\1&-1&0&2&-1\\1&1&1&3&0\end{bmatrix}\longrightarrow\begin{bmatrix}1&0&\frac12&\frac52&-\frac12\\0&1&\frac12&\frac12&\frac12\\0&0&0&0&0\end{bmatrix}$$',
      r'בסיס $\Gamma=\{P_1,P_2\}$, $\ \dim V=2$ (למשל $P_3=\frac12(P_1+P_2)$).']),
    (r'(ii)', [
      r'↓ $aP_1+bP_2=(a+5b)+(a-b)X+(a+b)X^2$',
      r'↓ $a+b=1,\ \ a+5b=k,\ \ a-b=2k$',
      r'↓ $a=\frac{11}{10},\ b=-\frac1{10},\ k=\frac35$']),
    (r'(iii)', [
      r'↓ $P(1)=3a+5b=1,\ \ P(-1)=a+7b=2$',
      r'↓ $b=\frac5{16},\ \ a=-\frac3{16}$',
      r'↓ $P=-\frac3{16}P_1+\frac5{16}P_2=\frac{11}8-\frac12X+\frac18X^2$']),
  ],
  ans=r'(i) $\Gamma=\{P_1,P_2\}$, $\dim V=2$; (ii) $k=\frac35$; (iii) $P=\frac{11}8-\frac12X+\frac18X^2$, $\ [P]_\Gamma=\left(-\frac3{16},\frac5{16}\right)$'),

dict(id='S3a', exam='S', num='שאלה 3, חלק 1', pts=7, topics=['complex'], level=1,
  q=r'יהי $z$ מרוכב שמקיים $|z+1|=|z-1|$. הוכיחו ש-$iz$ הוא מספר ממשי.',
  steps=[
    (r'מציבים $z=a+bi$', [
      r'↓ $(a+1)^2+b^2=(a-1)^2+b^2$',
      r'↓ $4a=0\Rightarrow a=0$']),
    (r'מסקנה', [
      r'$z=bi$, ולכן $iz=i\cdot bi=-b\in\mathbb{R}$.']),
  ],
  ans=r'$z$ מדומה טהור, ולכן $iz=-b$ ממשי'),

dict(id='S3b', exam='S', num='שאלה 3, חלק 2', pts=8, topics=['matrices'], level=3,
  q=r'תהי $A\in M_5(\mathbb{R})$ שמקיימת $A^2=AA^t+2I_5$. (i) הוכיחו ש-$A$ רגולרית ובטאו את $A^{-1}$ באמצעות $A$. (ii) האם $A$ סימטרית, אנטי-סימטרית או לא זה ולא זה?',
  steps=[
    (r'(i)', [
      r'↓ $A^2-AA^t=2I$',
      r'↓ $A(A-A^t)=2I$',
      r'$A$ הפיכה ו-$A^{-1}=\frac12(A-A^t)$.']),
    (r'(ii) $A^{-1}$ אנטי-סימטרית', [
      r'= | $(A^{-1})^t=\frac12(A^t-A)=-A^{-1}$',
      r'↓ $(A^t)^{-1}=-A^{-1}$',
      r'↓ $A^t=-A$ | מהפכים את שני האגפים',
      r'התשובה שהמבחן מצפה לה: $A$ אנטי-סימטרית.']),
    (r'הערה חשובה', [
      r'מטריצה אנטי-סימטרית מסדר אי-זוגי אינה הפיכה: $\det A=\det A^t=\det(-A)=(-1)^5\det A$ ⇒ $\det A=0$. לכן בגודל 5 אין בכלל מטריצה שמקיימת את הנתון - השאלה עובדת רק בסדר זוגי. כדאי לדעת את הנימוק, ואם זה מופיע במבחן - לציין את זה.']),
  ],
  ans=r'$A^{-1}=\frac12(A-A^t)$; $A$ אנטי-סימטרית (ובסדר 5 אין מטריצה כזו בכלל - ראו הערה)'),

dict(id='S4', exam='S', num='שאלה 4', pts=15, topics=['systems', 'det'], level=2,
  q=r'נתונה $A=\begin{bmatrix}2&k&0\\1&2&1\\1&0&k\end{bmatrix}$. (i) לאילו $k$ המטריצה $A$ שקולת שורה ל-$B=\begin{bmatrix}2&1&0\\0&2&1\\0&0&1\end{bmatrix}$? (ii) לאילו $k$ למערכת $A\vec x=\begin{bmatrix}0\\2\\0\end{bmatrix}$ פתרון יחיד? מצאו אותו בכלל קרמר.',
  steps=[
    (r'(i) $B$ הפיכה ($\det B=4$)', [
      r'$A$ שקולת שורה ל-$B$ בדיוק כש-$A$ הפיכה (שתיהן שקולות ל-$I$):',
      r'$$\det A=2(2k-0)-k(k-1)=-k^2+5k=-k(k-5)$$',
      r'= | $k\neq0,\ k\neq5$']),
    (r'(ii) פתרון יחיד $\iff\det A\neq0$', [
      r'= $\Delta_1$ | $\begin{vmatrix}0&k&0\\2&2&1\\0&0&k\end{vmatrix}=-2k^2$',
      r'= $\Delta_2$ | $\begin{vmatrix}2&0&0\\1&2&1\\1&0&k\end{vmatrix}=4k$',
      r'= $\Delta_3$ | $\begin{vmatrix}2&k&0\\1&2&2\\1&0&0\end{vmatrix}=2k$']),
    (r'מחלקים ב-$\det A=-k(k-5)$', [
      r'= | $x=\frac{2k}{k-5},\ \ y=\frac{-4}{k-5},\ \ z=\frac{-2}{k-5}$',
      r'בדיקה בשורה השנייה: $\frac{2k-8-2}{k-5}=2$ ✓']),
  ],
  ans=r'$k\neq0,5$; $\ \left(\frac{2k}{k-5},\ -\frac4{k-5},\ -\frac2{k-5}\right)$'),

dict(id='S5', exam='S', num='שאלה 5', pts=15, topics=['diag'], level=3,
  q=r'תהי $A=\begin{bmatrix}1&0&0\\4&-7&12\\2&-4&7\end{bmatrix}$. (i) קבעו אם $A$ ניתנת ללכסון; אם כן, מצאו $D$ ו-$P$ עם $D=P^{-1}AP$. (ii) מצאו את $A^{5784}$.',
  steps=[
    (r'הפולינום האופייני (פיתוח לפי השורה הראשונה)', [
      r'$$\det(A-\lambda I)=(1-\lambda)\left[(-7-\lambda)(7-\lambda)+48\right]=(1-\lambda)(\lambda^2-1)$$',
      r'= | $\lambda=1$ (פעמיים), $\ \lambda=-1$']),
    (r'וקטורים עצמיים', [
      r'= $\lambda=1$ | $x-2y+3z=0$: $\ (2,1,0),\ (-3,0,1)$ - מימד 2',
      r'= $\lambda=-1$ | $x=0,\ y=2z$: $\ (0,2,1)$',
      r'ריבוי גיאומטרי = אלגברי לכל ערך עצמי ⇒ ניתנת ללכסון.']),
    (r'$P$ ו-$D$', [
      r'$$P=\begin{bmatrix}2&-3&0\\1&0&2\\0&1&1\end{bmatrix},\qquad D=\begin{bmatrix}1&0&0\\0&1&0\\0&0&-1\end{bmatrix}$$']),
    (r'(ii)', [
      r'↓ $D^2=I\Rightarrow A^2=PD^2P^{-1}=I$',
      r'↓ $A^{5784}=(A^2)^{2892}=I$ | 5784 זוגי']),
  ],
  ans=r'(i) כן, $D=\operatorname{diag}(1,1,-1)$; (ii) $A^{5784}=I$'),

dict(id='S6a', exam='S', num='שאלה 6, חלק 1', pts=9, topics=['spaces'], level=2,
  q=r'יהי $V=\left\{M\in M_2(\mathbb{R})\ \middle|\ \operatorname{tr}\left(\begin{bmatrix}1&2\\3&-1\end{bmatrix}M\right)=0\right\}$. הוכיחו כי $V$ תת-מרחב של $M_2(\mathbb{R})$ ומצאו לו בסיס.',
  steps=[
    (r'תת-מרחב', [
      r'$M\mapsto\operatorname{tr}(NM)$ לינארית (כפל משמאל ועקבה לינאריים), ו-$V$ הוא הגרעין שלה - לכן תת-מרחב.']),
    (r'התנאי', [
      r'$M=\begin{bmatrix}m_1&m_2\\m_3&m_4\end{bmatrix}$:',
      r'$$\operatorname{tr}(NM)=(m_1+2m_3)+(3m_2-m_4)=0\Rightarrow m_4=m_1+3m_2+2m_3$$']),
    (r'בסיס', [
      r'$$\left\{\begin{bmatrix}1&0\\0&1\end{bmatrix},\begin{bmatrix}0&1\\0&3\end{bmatrix},\begin{bmatrix}0&0\\1&2\end{bmatrix}\right\}$$',
      r'$\dim V=3$.']),
  ],
  ans=r'בסיס: $\begin{bmatrix}1&0\\0&1\end{bmatrix},\begin{bmatrix}0&1\\0&3\end{bmatrix},\begin{bmatrix}0&0\\1&2\end{bmatrix}$'),

dict(id='S6b', exam='S', num='שאלה 6, חלק 2', pts=6, topics=['matrices'], level=1,
  q=r'(i) תנו דוגמה לשתי מטריצות שונות והפיכות $A,B\in M_2(\mathbb{R})$ כך ש-$A+B$ מדורגת קנונית. (ii) כנ"ל, כך ש-$AB$ מדורגת קנונית.',
  steps=[
    (r'(i)', [
      r'= | $A=2I,\ B=-I$',
      r'= | $A+B=I$ - מדורגת קנונית']),
    (r'(ii)', [
      r'= | $A=2I,\ B=\frac12I$',
      r'= | $AB=I$ - מדורגת קנונית']),
  ],
  ans=r'למשל (i) $2I,\ -I$; (ii) $2I,\ \frac12I$'),

dict(id='S7a', exam='S', num='שאלה 7, חלק 1', pts=10, topics=['inner', 'linmap'], level=2,
  q=r'$T:\mathbb{R}^4\to\mathbb{R}^3$, $\ T(x,y,z,t)=(x+2y+3z-t,\ -x+y-2t,\ 2x-3y-z+5t)$. מצאו בסיס אורתוגונלי ל-$\operatorname{Im}(T)$.',
  steps=[
    (r'עמודות ומדרגים', [
      r'$$\begin{bmatrix}1&2&3&-1\\-1&1&0&-2\\2&-3&-1&5\end{bmatrix}\longrightarrow\begin{bmatrix}1&0&1&1\\0&1&1&-1\\0&0&0&0\end{bmatrix}$$',
      r'בסיס לתמונה: העמודות 1, 2: $\ c_1=(1,-1,2),\ c_2=(2,1,-3)$.']),
    (r'גרם-שמידט', [
      r'↓ $\langle c_2,c_1\rangle=2-1-6=-5,\ \ \|c_1\|^2=6$',
      r'↓ $w_2=c_2+\frac56c_1=\frac16(17,1,-8)$',
      r'בדיקה: $17-1-16=0$ ✓']),
  ],
  ans=r'$\{(1,-1,2),\ (17,1,-8)\}$'),

dict(id='S7b', exam='S', num='שאלה 7, חלק 2', pts=5, topics=['det'], level=2,
  q=r'נתונות $A,B\in M_5(\mathbb{R})$ שמקיימות $ABA=-B$. הוכיחו ש-$B$ אינה הפיכה.',
  steps=[
    (r'דטרמיננטה לשני האגפים', [
      r'↓ $\det(A)^2\det B=(-1)^5\det B=-\det B$',
      r'↓ $\det B\left(\det(A)^2+1\right)=0$']),
    (r'מסקנה', [
      r'$\det(A)^2+1\geq1>0$ (מספר ממשי), ולכן $\det B=0$ - $B$ לא הפיכה.']),
  ],
  ans=r'$\det B=0$'),

dict(id='Sm1', exam='S', num='חלק ב, שאלה 1', pts=5, topics=['complex'], level=1, mc=True,
  q=r'נתון: $(2-i)^4z=5i(1+3i)^2$. איזו טענה נכונה? ' + opts(r'$z\bar z=4$', r'$z\bar z=5$', r'$z\bar z=3$', r'$z\bar z=6$'),
  steps=[
    (r'ערך מוחלט', [
      r'↓ $|2-i|^4|z|=5\cdot|1+3i|^2$',
      r'↓ $25|z|=50\Rightarrow|z|=2$',
      r'↓ $z\bar z=|z|^2=4$']),
  ],
  ans=r'א'),

dict(id='Sm2', exam='S', num='חלק ב, שאלה 2', pts=5, topics=['matrices'], level=1, mc=True,
  q=r'נתונה $A=\begin{pmatrix}0&0&1\\0&1&0\\1&0&1\end{pmatrix}$. איזו טענה נכונה? '
    + opts(r'$\operatorname{Tr}(A^{-1})=0$', r'$\operatorname{Tr}(A^{-1})=1$', r'$\operatorname{Tr}(A^{-1})=2$', r'$\operatorname{Tr}(A^{-1})=\frac12$'),
  steps=[
    (r'מחשבים את ההופכית', [
      r'$$A^{-1}=\begin{pmatrix}-1&0&1\\0&1&0\\1&0&0\end{pmatrix}$$',
      r'בדיקה: $AA^{-1}=I$ ✓. $\ \operatorname{Tr}(A^{-1})=-1+1+0=0$.']),
  ],
  ans=r'א'),

dict(id='Sm3', exam='S', num='חלק ב, שאלה 3', pts=5, topics=['spaces'], level=2, mc=True,
  q=r'$\vec u,\vec v,\vec w\in\mathbb{R}^3$. איזו טענה נכונה? '
    + opts(r'אם $\{\vec u,\vec v,\vec w\}$ בת"ל אז $\operatorname{span}\{\vec u,\vec v,\vec w\}=\operatorname{span}\{\vec u+\vec v,\vec u+\vec w,\vec v+\vec w\}$',
           r'אם $\{\vec u,\vec v\},\{\vec u,\vec w\},\{\vec v,\vec w\}$ בת"ל אז $\{\vec u,\vec v,\vec w\}$ בת"ל',
           r'אם $\dim\operatorname{span}\{\vec u,\vec v,\vec w\}=2$ אז $\vec w\in\operatorname{span}\{\vec u,\vec v\}$',
           r'אם $\{\vec u,\vec v,\vec w\}$ ת"ל אז $\operatorname{span}\{\vec u,\vec v\}=\operatorname{span}\{\vec u+\vec w,\vec v+\vec w\}$'),
  steps=[
    (r'א נכונה', [
      r'$\begin{vmatrix}1&1&0\\1&0&1\\0&1&1\end{vmatrix}=-2\neq0$ - שלושת הסכומים בת"ל, ופורשים את אותו מרחב.']),
    (r'דוגמאות נגדיות לשאר', [
      r'= ב | $\vec u=e_1,\ \vec v=e_2,\ \vec w=e_1+e_2$',
      r'= ג | $\vec u=\vec v=e_1,\ \vec w=e_2$',
      r'= ד | $\vec u=\vec v=e_1,\ \vec w=e_2$: $\ \operatorname{span}\{e_1\}\neq\operatorname{span}\{e_1+e_2\}$']),
  ],
  ans=r'א'),

dict(id='Sm4', exam='S', num='חלק ב, שאלה 4', pts=5, topics=['systems'], level=1, mc=True,
  q=r'איזו טענה <b>לא</b> נכונה? '
    + opts(r'קיימת מערכת לינארית של 4 משוואות ו-5 נעלמים שיש לה פתרון יחיד', r'קיימת מערכת לינארית של 5 משוואות ו-4 נעלמים שיש לה פתרון יחיד',
           r'קיימת מערכת לינארית של 4 משוואות ו-5 נעלמים שיש לה אינסוף פתרונות', r'קיימת מערכת לינארית של 5 משוואות ו-4 נעלמים שיש לה אינסוף פתרונות'),
  steps=[
    (r'משתנים חופשיים', [
      r'ב-4 משוואות יש לכל היותר 4 איברים מובילים, ועם 5 נעלמים נשאר לפחות משתנה חופשי אחד: אם יש פתרון - יש אינסוף. לכן פתרון יחיד בלתי אפשרי.',
      r'ב, ג, ד אפשריות (למשל ב: 4 משוואות $x_i=0$ ועוד משוואה חוזרת).']),
  ],
  ans=r'א'),

dict(id='Sm5', exam='S', num='חלק ב, שאלה 5', pts=5, topics=['det'], level=3, mc=True,
  q=r'$A\in M_4(\mathbb{R})$ הפיכה ומקיימת $A^2+2\operatorname{Adj}(A^t)=0$. איזו טענה נכונה? '
    + opts(r'$\det A=\frac1{16}$', r'$\det A=16$', r'$\det A=\frac14$', r'$\det A=4$'),
  steps=[
    (r'מבטאים את $\operatorname{Adj}(A^t)$', [
      r'= | $\operatorname{Adj}(A^t)=\det(A^t)(A^t)^{-1}=d\,(A^{-1})^t$, $\ d=\det A$',
      r'↓ $A^2=-2d\,(A^{-1})^t$']),
    (r'דטרמיננטה לשני האגפים ($n=4$)', [
      r'↓ $d^2=(-2d)^4\cdot\frac1d=16d^3$',
      r'↓ $d\neq0$ | $d=\frac1{16}$']),
  ],
  ans=r'א'),
]


# ---------- סילבוס: באיזו יחידה נלמד כל נושא (לסינון "רק מה שכבר למדנו") ----------
SYLLABUS_PDF = 'syllabus.pdf'
STAGE_LABEL = 'נושא'
SYLLABUS = [
    (1, 'חלוקת פולינומים ופירוק לגורמים'),
    (2, 'מספרים מרוכבים, הצגה קוטבית, דה-מואבר'),
    (3, 'מטריצות: פעולות, משוחלפת, סימטרית, משולשת, אלכסונית'),
    (4, 'מערכות משוואות לינאריות, דירוג, שיטת גאוס'),
    (5, 'מטריצות הפיכות ומציאת ההופכית'),
    (6, 'דטרמיננטות, adj, כלל קרמר'),
    (7, 'מרחבים וקטוריים ותת-מרחבים'),
    (8, 'צירופים לינאריים, פרישה, אי-תלות, בסיס ומימד'),
    (9, 'מרחב השורות והעמודות, דרגה של מטריצה'),
    (10, 'ערכים ווקטורים עצמיים, לכסון'),
    (11, 'העתקות לינאריות, גרעין ותמונה'),
    (12, 'ערכים עצמיים של אופרטור לינארי'),
    (13, 'מכפלה פנימית, קושי-שוורץ, גרם-שמידט'),
]
STAGE = 6          # עד כאן נלמד לפי המצגות שהועלו (דטרמיננטות)
TOPIC_UNIT = {'complex': 2, 'matrices': 5, 'systems': 4, 'det': 6, 'spaces': 8, 'linmap': 11, 'diag': 10, 'inner': 13}
UNIT = {'B4': 9}   # דרגה של מטריצה
