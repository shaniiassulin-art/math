# -*- coding: utf-8 -*-
# שאלה לדוגמה לכל סעיף באתר החומר התיאורטי - כולן מתוך המצגות, והפתרון בדרך של המצגת.
# פורמט: src, q (השאלה), steps = [(כותרת, [שורות])], ans. מתמטיקה בין $...$, ושורה שכולה $$...$$ מוצגת כנוסחה בשורה נפרדת.

SAMPLES = {
'ex1-s1': dict(
    src='מצגת מספרים מרוכבים, פרק 1 (הגדרה)',
    q=r'לכל אחד מהמספרים $3-i\sqrt{2}$, $\ -\pi-7i$, $\ 5+4i$, $\ 6i$, $\ 3$: מצאו את $\operatorname{Re}(z)$ ואת $\operatorname{Im}(z)$, וקבעו אם המספר ממשי, מדומה טהור, או אף אחד מהם.',
    steps=[
        (r'כותבים כל מספר בצורה $z=a+ib$', [
            r'$$3-i\sqrt{2}=3+i(-\sqrt{2})\qquad -\pi-7i=-\pi+i(-7)\qquad 5+4i$$',
            r'$$6i=0+6i\qquad 3=3+0i$$']),
        (r'קוראים את שני החלקים', [
            r'$a$ הוא החלק הממשי, ו-$b$ הוא החלק המדומה - <b>בלי</b> ה-$i$:',
            r'$$\operatorname{Re}(3-i\sqrt{2})=3,\quad \operatorname{Im}(3-i\sqrt{2})=-\sqrt{2}$$',
            r'$$\operatorname{Re}(-\pi-7i)=-\pi,\quad \operatorname{Im}(-\pi-7i)=-7$$',
            r'$$\operatorname{Re}(5+4i)=5,\quad \operatorname{Im}(5+4i)=4$$',
            r'$$\operatorname{Re}(6i)=0,\quad \operatorname{Im}(6i)=6\qquad \operatorname{Re}(3)=3,\quad \operatorname{Im}(3)=0$$']),
        (r'מסווגים לפי ההערה במצגת', [
            r'כאשר $b=0$ - $z$ מספר ממשי. כאשר $a=0$ - $z$ מדומה טהור.']),
    ],
    ans=r'$3$ ממשי; $6i$ מדומה טהור; $3-i\sqrt{2}$, $-\pi-7i$, $5+4i$ - לא ממשיים ולא מדומים טהורים.'),

'ex1-s2': dict(
    src='מצגת מספרים מרוכבים, פרק 2 (פעולות - הדוגמאות של חיבור, כפל וחילוק)',
    q=r'נתונים $z_1=2+3i$, $z_2=-7+6i$. חשבו את $z_1+z_2$ ואת $z_1z_2$. בנוסף, עבור $w_1=2-3i$, $w_2=1+4i$ רשמו את $\frac{w_1}{w_2}$ בצורה קרטזית.',
    steps=[
        (r'חיבור: ממשי עם ממשי, מדומה עם מדומה', [
            r'$$z_1+z_2=(a_1+a_2)+i(b_1+b_2)=(2-7)+i(3+6)=-5+9i$$']),
        (r'כפל לפי הנוסחה מהמצגת', [
            r'$$z_1z_2=(a_1a_2-b_1b_2)+i(a_1b_2+a_2b_1)$$',
            r'$$=((2)(-7)-(3)(6))+i((2)(6)+(3)(-7))=-32-9i$$']),
        (r'חילוק: מכפילים מונה ומכנה בצמוד של המכנה', [
            r'הצמוד של $w_2=1+4i$ הוא $\overline{w_2}=1-4i$:',
            r'$$\frac{2-3i}{1+4i}=\frac{(2-3i)(1-4i)}{(1+4i)(1-4i)}$$']),
        (r'מחשבים מכנה ומונה', [
            r'במכנה: $(1+4i)(1-4i)=1^2+4^2=17$ - מספר ממשי.',
            r'במונה: $(2-3i)(1-4i)=2-8i-3i+12i^2=-10-11i$.']),
        (r'מפצלים לחלק ממשי ולחלק מדומה', [
            r'$$\frac{w_1}{w_2}=\frac{-10-11i}{17}=-\frac{10}{17}-i\frac{11}{17}$$']),
    ],
    ans=r'$z_1+z_2=-5+9i$, $\ z_1z_2=-32-9i$, $\ \frac{w_1}{w_2}=-\frac{10}{17}-\frac{11}{17}i$'),

'ex1-s3': dict(
    src='מצגת מספרים מרוכבים - התרגיל בסוף המצגת',
    q=r'הוכיחו כי לכל מספר מרוכב $z$ ($z\neq-i$) שמקיים $|z|=1$, המספר $\omega=\frac{1+iz}{z+i}$ הוא מספר <b>ממשי</b>.',
    steps=[
        (r'בוחרים את התכונה שמתאימה', [
            r'לפי תכונות הצמוד: $\omega$ ממשי אם ורק אם $\omega-\overline{\omega}=0$. לכן מחשבים את $\omega-\overline{\omega}$.']),
        (r'מחשבים את הצמוד לפי התכונות', [
            r'הצמוד עובר על חיבור, כפל וחילוק, ו-$\overline{i}=-i$:',
            r'$$\overline{\omega}=\frac{\overline{1+iz}}{\overline{z+i}}=\frac{1-i\overline{z}}{\overline{z}-i}$$']),
        (r'מכנה משותף', [
            r'$$\omega-\overline{\omega}=\frac{(1+iz)(\overline{z}-i)-(1-i\overline{z})(z+i)}{(z+i)(\overline{z}-i)}$$']),
        (r'פותחים את המונה', [
            r'$(1+iz)(\overline{z}-i)=\overline{z}-i+iz\overline{z}+z$',
            r'$(1-i\overline{z})(z+i)=z+i-iz\overline{z}+\overline{z}$',
            r'בהפרש $z$ ו-$\overline{z}$ מתבטלים, ונשאר: $\ -2i+2iz\overline{z}=2i(z\overline{z}-1)$.']),
        (r'מציבים את הנתון', [
            r'$z\overline{z}=|z|^2=1$, ולכן המונה הוא $2i(|z|^2-1)=0$.',
            r'$$\omega-\overline{\omega}=0$$']),
    ],
    ans=r'$\omega-\overline{\omega}=0$, ולכן $\omega$ ממשי. מ.ש.ל.'),

'ex1-s4': dict(
    src='מצגת מספרים מרוכבים, פרק 2 - התרגיל על המודול',
    q=r'נתון מספר מרוכב $z=a+bi$, כאשר $a,b$ הם המספרים הממשיים המקיימים $\frac{4i-a}{1+2i}=1+ib$. מצאו את $\left|\frac{2z}{1+i}\right|$.',
    steps=[
        (r'שלב 1 במצגת: מוצאים את $z$ - כופלים במכנה', [
            r'$$4i-a=(1+ib)(1+2i)=1+2i+ib+2i^2b=(1-2b)+i(b+2)$$']),
        (r'משווים חלק ממשי וחלק מדומה', [
            r'$$\begin{cases}-a=1-2b\\4=b+2\end{cases}\Rightarrow\begin{cases}a=3\\b=2\end{cases}\Rightarrow z=3+2i$$']),
        (r'שלב 2: מחשבים את הערך המוחלט לפי תכונות המודול', [
            r'מודול של מכפלה ומנה הוא מכפלה ומנה של המודולים - לא צריך לחשב את השבר:',
            r'$$\left|\frac{2z}{1+i}\right|=\frac{2|3+2i|}{|1+i|}=\frac{2\sqrt{3^2+2^2}}{\sqrt{1^2+1^2}}=\frac{2\sqrt{13}}{\sqrt{2}}$$']),
        (r'מפשטים', [
            r'$$\frac{2\sqrt{13}}{\sqrt{2}}=\sqrt{2}\cdot\sqrt{13}=\sqrt{26}$$']),
    ],
    ans=r'$\left|\frac{2z}{1+i}\right|=\sqrt{26}$'),

'ex1-s5': dict(
    src='מצגת מספרים מרוכבים - תזכורת: הפונקציות הטריגונומטריות',
    q=r'בעזרת מעגל היחידה מצאו את $\cos\alpha$, $\sin\alpha$ ו-$\tan\alpha$ עבור $\alpha=\frac{\pi}{3}$.',
    steps=[
        (r'מסמנים את הזווית על מעגל היחידה', [
            r'הנקודה על המעגל בזווית $\alpha$ היא $(\cos\alpha,\sin\alpha)$: הקואורדינטה האופקית היא $\cos\alpha$, והאנכית היא $\sin\alpha$.']),
        (r'קוראים את ההיטל האופקי', [
            r'בזווית $\frac{\pi}{3}$ ההיטל על הציר האופקי הוא $\frac12$ (כמו בשקף), ולכן $\cos\frac{\pi}{3}=\frac12$.']),
        (r'מוצאים את הגובה לפי פיתגורס', [
            r'הרדיוס הוא 1, ולכן $\cos^2\alpha+\sin^2\alpha=1$:',
            r'$$\sin\frac{\pi}{3}=\sqrt{1-\frac14}=\frac{\sqrt{3}}{2}$$']),
        (r'מחשבים טנגנס', [
            r'$$\tan\frac{\pi}{3}=\frac{\sin\frac{\pi}{3}}{\cos\frac{\pi}{3}}=\frac{\sqrt{3}/2}{1/2}=\sqrt{3}$$']),
    ],
    ans=r'$\cos\frac{\pi}{3}=\frac12$, $\ \sin\frac{\pi}{3}=\frac{\sqrt3}{2}$, $\ \tan\frac{\pi}{3}=\sqrt3$ - בדיוק העמודה של $\frac{\pi}{3}$ בטבלה.'),

'ex1-s6': dict(
    src='מצגת מספרים מרוכבים, פרק 3 - דוגמה: הצגה קוטבית של $-5+5i$',
    q=r'רשמו את $z=-5+5i$ בהצגה קוטבית $z=re^{i\theta}$.',
    steps=[
        (r'מודול של $z$', [
            r'$$r=|z|=\sqrt{a^2+b^2}=\sqrt{25+25}=5\sqrt{2}$$']),
        (r'ארגומנט של $z$ - מהטנגנס', [
            r'$$\tan\theta=\frac{b}{a}=\frac{5}{-5}=-1$$',
            r'מהטבלה $\tan\frac{\pi}{4}=1$, ולכן יש שתי אפשרויות: $\theta=-\frac{\pi}{4}$ או $\theta=-\frac{\pi}{4}+\pi=\frac{3\pi}{4}$.']),
        (r'"איך לדעת?" - בוחרים לפי הסימנים', [
            r'$\operatorname{Re}(z)=-5<0$ ו-$\operatorname{Im}(z)=5>0$: הנקודה ברביע השני, ולכן $\theta=\frac{3\pi}{4}$.']),
        (r'כותבים את ההצגה', [
            r'$$z=5\sqrt{2}e^{i\frac{3\pi}{4}}=5\sqrt{2}\left(\cos\frac{3\pi}{4}+i\sin\frac{3\pi}{4}\right)$$']),
    ],
    ans=r'$-5+5i=5\sqrt{2}e^{i\frac{3\pi}{4}}$'),

'ex1-s7': dict(
    src='מצגת מספרים מרוכבים, פרק 3 - דוגמה: כפל וחילוק בהצגה קוטבית',
    q=r'נתונים $z_1=1+i\sqrt{3}$ ו-$z_2=-5+5i$. חשבו את $z_1z_2$ ואת $\frac{z_1}{z_2}$ בהצגה קוטבית.',
    steps=[
        (r'מעבירים כל מספר להצגה קוטבית', [
            r'$|z_1|=\sqrt{1+3}=2$, $\tan\theta_1=\sqrt3$ ברביע הראשון: $z_1=2e^{i\frac{\pi}{3}}$.',
            r'$|z_2|=5\sqrt2$, ברביע השני: $z_2=5\sqrt{2}e^{i\frac{3\pi}{4}}$.']),
        (r'כפל: מכפילים מודולים ומחברים זוויות', [
            r'$$z_1z_2=2\cdot5\sqrt{2}\,e^{i\left(\frac{\pi}{3}+\frac{3\pi}{4}\right)}=10\sqrt{2}e^{i\frac{13\pi}{12}}$$']),
        (r'חילוק: מחלקים מודולים ומחסירים זוויות', [
            r'$$\frac{z_1}{z_2}=\frac{2}{5\sqrt{2}}e^{i\left(\frac{\pi}{3}-\frac{3\pi}{4}\right)}=\frac{\sqrt{2}}{5}e^{-i\frac{5\pi}{12}}$$']),
    ],
    ans=r'$z_1z_2=10\sqrt{2}e^{i\frac{13\pi}{12}}$, $\ \frac{z_1}{z_2}=\frac{\sqrt2}{5}e^{-i\frac{5\pi}{12}}$'),

'ex1-s8': dict(
    src='מצגת מספרים מרוכבים, פרק 4 - דוגמה לנוסחת דה מואבר',
    q=r'רשמו את $(1+i\sqrt{3})^7$ בצורה קרטזית.',
    steps=[
        (r'מעבירים את הבסיס להצגה קוטבית', [
            r'$|1+i\sqrt3|=2$, וברביע הראשון $\tan\theta=\sqrt3$, ולכן $1+i\sqrt{3}=2e^{i\frac{\pi}{3}}$.']),
        (r'מפעילים דה מואבר: $(re^{i\theta})^n=r^ne^{in\theta}$', [
            r'$$(1+i\sqrt{3})^7=\left(2e^{i\frac{\pi}{3}}\right)^7=2^7e^{i\frac{7\pi}{3}}$$']),
        (r'מורידים סיבוב שלם', [
            r'$\frac{7\pi}{3}=\frac{\pi}{3}+2\pi$, ולכן $128e^{i\frac{7\pi}{3}}=128e^{i\frac{\pi}{3}}$.']),
        (r'חוזרים לצורה קרטזית', [
            r'$$128\left(\cos\frac{\pi}{3}+i\sin\frac{\pi}{3}\right)=128\left(\frac12+i\frac{\sqrt3}{2}\right)=64+64\sqrt{3}\,i$$']),
    ],
    ans=r'$(1+i\sqrt3)^7=64+64\sqrt3\,i$'),

'ex1-s9': dict(
    src='מצגת מספרים מרוכבים, פרק 5 - דוגמה 2: $z^3=64i$',
    q=r'מצאו את כל הפתרונות של המשוואה $z^3=64i$ ותארו אותם במישור.',
    steps=[
        (r'נחפש $z$ בצורה קוטבית', [
            r'$z=re^{i\theta}$, ולכן $z^3=r^3e^{i3\theta}$.']),
        (r'כותבים את צד ימין בצורה קוטבית', [
            r'$64i$ על הציר המדומה החיובי: $64i=64e^{i\frac{\pi}{2}}$. המשוואה: $r^3e^{i3\theta}=64e^{i\frac{\pi}{2}}$.']),
        (r'משווים מודולים וזוויות (עם $2k\pi$)', [
            r'$$r^3=64\Rightarrow r=4\qquad 3\theta=\frac{\pi}{2}+2k\pi\Rightarrow\theta=\frac{\pi}{6}+\frac{2k\pi}{3}$$']),
        (r'מציבים $k=0,1,2$', [
            r'$$z_0=4e^{i\frac{\pi}{6}},\qquad z_1=4e^{i\frac{5\pi}{6}},\qquad z_2=4e^{i\frac{3\pi}{2}}=-4i$$']),
        (r'במישור', [
            r'שלושת הפתרונות על מעגל ברדיוס 4, במרווחים של $\frac{2\pi}{3}$ - קודקודים של משולש שווה צלעות.']),
    ],
    ans=r'$z_0=4e^{i\frac{\pi}{6}}$, $\ z_1=4e^{i\frac{5\pi}{6}}$, $\ z_2=-4i$'),

'ex1-s10': dict(
    src='מצגת מספרים מרוכבים, פרק 6 - התרגיל על פולינום עם מקדמים ממשיים',
    q=r'נתון הפולינום $P(z)=z^4-4z^3+4z^2-4$. א. בדקו ש-$1+i$ הוא שורש של $P(z)$. ב. מצאו את כל השורשים המרוכבים של $P(z)$.',
    steps=[
        (r'א. מחשבים את החזקות של $1+i$ בנפרד', [
            r'$$(1+i)^2=1+2i+i^2=2i\qquad (1+i)^3=2i(1+i)=2i-2\qquad (1+i)^4=(2i)^2=-4$$']),
        (r'מציבים בפולינום', [
            r'$$P(1+i)=-4-4(2i-2)+4(2i)-4=-4-8i+8+8i-4=0$$',
            r'לכן $1+i$ שורש.']),
        (r'ב. משפט השורשים הצמודים', [
            r'המקדמים של $P$ ממשיים ו-$1+i$ שורש, ולכן גם $1-i$ שורש.']),
        (r'מחלקים בגורם הריבועי', [
            r'$$(z-(1+i))(z-(1-i))=z^2-2z+2$$',
            r'חילוק ארוך של $P(z)$ ב-$z^2-2z+2$ נותן מנה $z^2-2z-2$ ושארית 0:',
            r'$$P(z)=(z^2-2z+2)(z^2-2z-2)$$']),
        (r'פותרים את המנה', [
            r'$$z^2-2z-2=0\Rightarrow z=\frac{2\pm\sqrt{4+8}}{2}=1\pm\sqrt{3}$$']),
    ],
    ans=r'לפולינום 4 שורשים: $1+i,\ 1-i,\ 1+\sqrt3,\ 1-\sqrt3$'),

'ex1-s11': dict(
    src='מצגת מספרים מרוכבים, פרק 6 מקרה 2 - הדוגמה $Z^2-2iZ+2-4i=0$',
    q=r'פתרו את המשוואה $z^2-2iz+2-4i=0$.',
    steps=[
        (r'שלב 1: מחשבים את $\Delta$', [
            r'$a=1$, $b=-2i$, $c=2-4i$:',
            r'$$\Delta=b^2-4ac=(-2i)^2-4(2-4i)=-4-8+16i=-12+16i$$']),
        (r'שלב 2: מחפשים $\delta=\alpha+i\beta$ עם $\delta^2=\Delta$', [
            r'$\delta^2=\alpha^2-\beta^2+2i\alpha\beta$, ולכן $\alpha^2-\beta^2=-12$ ו-$2\alpha\beta=16>0$.',
            r'ומהמודול: $|\delta|^2=|\Delta|$, כלומר $\alpha^2+\beta^2=\sqrt{(-12)^2+16^2}=20$.']),
        (r'פותרים את המערכת', [
            r'$$\begin{cases}\alpha^2-\beta^2=-12\\\alpha^2+\beta^2=20\end{cases}\Rightarrow\alpha^2=4,\ \beta^2=16$$',
            r'$2\alpha\beta>0$, כלומר $\alpha$ ו-$\beta$ באותו סימן: $\delta=2+4i$ או $\delta=-2-4i$. בוחרים $\delta=2+4i$.']),
        (r'שלב 3: שני הפתרונות', [
            r'$$z_1=\frac{-b-\delta}{2a}=\frac{2i-2-4i}{2}=-1-i\qquad z_2=\frac{-b+\delta}{2a}=\frac{2i+2+4i}{2}=1+3i$$']),
    ],
    ans=r'$z_1=-1-i$, $\ z_2=1+3i$'),

'ex2-s1': dict(
    src='מצגת מטריצות, פרק 1 (הגדרות) - דוגמה למטריצה מסדר 2 על 3 ולשוויון',
    q=r'נתונה $A=\begin{bmatrix}2&3&4\\6&7&8\end{bmatrix}$. מאיזה סדר $A$, ומהו $a_{1,2}$? ובנוסף: האם $\begin{bmatrix}1&3&-5\\7&8&3\\0&0&0\end{bmatrix}=\begin{bmatrix}1&3&-5\\7&8&3\end{bmatrix}$?',
    steps=[
        (r'סופרים שורות ועמודות', [
            r'ב-$A$ יש $n=2$ שורות ו-$m=3$ עמודות, ולכן $A\in M_{2,3}(\mathbb{R})$.']),
        (r'מוצאים את האיבר לפי האינדקסים', [
            r'$a_{1,2}$: שורה $i=1$, עמודה $j=2$, ולכן $a_{1,2}=3$.']),
        (r'שוויון מטריצות: אותו סדר, ושוויון איבר-איבר', [
            r'המטריצה הראשונה מסדר $3\times3$ והשנייה מסדר $2\times3$. לא אותו סדר - ולכן הן <b>לא</b> שוות (גם אם האיברים שמופיעים בשתיהן זהים).']),
    ],
    ans=r'$A\in M_{2,3}(\mathbb{R})$, $\ a_{1,2}=3$; המטריצות לא שוות.'),

'ex2-s2': dict(
    src='מצגת מטריצות, פרק 1 - מקרים מיוחדים',
    q=r'לאיזה סוג שייכת כל מטריצה? $A=\begin{bmatrix}1&3&-5\\7&8&3\\0&1&3\end{bmatrix}$, $B=\begin{bmatrix}3&1&-1&7\end{bmatrix}$, $C=\begin{bmatrix}0\\9\\-3\end{bmatrix}$, $D=\begin{bmatrix}1&0&0\\0&-9&0\\0&0&3\end{bmatrix}$, $E=\begin{bmatrix}1&0&0\\5&-9&0\\6&7&3\end{bmatrix}$, $F=\begin{bmatrix}1&5&6\\0&-9&7\\0&0&3\end{bmatrix}$',
    steps=[
        (r'קודם הסדר', [
            r'$A$ מסדר $3\times3$ - <b>ריבועית</b>. $B$ מסדר $1\times4$ - <b>וקטור שורה</b> ($\mathbb{R}_4$). $C$ מסדר $3\times1$ - <b>וקטור עמודה</b> ($\mathbb{R}^3$).']),
        (r'במטריצות הריבועיות - בודקים איפה האפסים', [
            r'$D$: $a_{i,j}=0$ לכל $i\neq j$ - <b>אלכסונית</b>.',
            r'$E$: $a_{i,j}=0$ כש-$i<j$ (כל מה שמעל האלכסון) - <b>משולשת תחתונה</b>.',
            r'$F$: $a_{i,j}=0$ כש-$i>j$ (כל מה שמתחת לאלכסון) - <b>משולשת עליונה</b>.']),
        (r'ומה עם $A$?', [
            r'ב-$A$ יש איברים שונים מאפס גם מעל וגם מתחת לאלכסון, ולכן היא ריבועית בלבד.']),
    ],
    ans=r'$A$ ריבועית; $B$ וקטור שורה; $C$ וקטור עמודה; $D$ אלכסונית; $E$ משולשת תחתונה; $F$ משולשת עליונה.'),

'ex2-s3': dict(
    src='מצגת מטריצות, פרק 2 - הדוגמאות של כפל בסקלר וחיבור',
    q=r'חשבו את $5\begin{bmatrix}2&3&0\\3&1&5\end{bmatrix}$ ואת $\begin{bmatrix}2&3&4\\3&4&5\end{bmatrix}+\begin{bmatrix}1&-3&0\\9&-1&7\end{bmatrix}$.',
    steps=[
        (r'כפל בסקלר: $\lambda A=[\lambda a_{i,j}]$', [
            r'כופלים כל איבר ב-5:',
            r'$$5\begin{bmatrix}2&3&0\\3&1&5\end{bmatrix}=\begin{bmatrix}10&15&0\\15&5&25\end{bmatrix}$$']),
        (r'חיבור: בודקים שהסדרים שווים', [
            r'שתי המטריצות ב-$M_{2,3}(\mathbb{R})$ - אפשר לחבר.']),
        (r'מחברים איבר-איבר: $A+B=[a_{i,j}+b_{i,j}]$', [
            r'$$\begin{bmatrix}2&3&4\\3&4&5\end{bmatrix}+\begin{bmatrix}1&-3&0\\9&-1&7\end{bmatrix}=\begin{bmatrix}3&0&4\\12&3&12\end{bmatrix}$$']),
    ],
    ans=r'$\begin{bmatrix}10&15&0\\15&5&25\end{bmatrix}$ ו-$\begin{bmatrix}3&0&4\\12&3&12\end{bmatrix}$'),

'ex2-s4': dict(
    src='מצגת מטריצות, פרק 2 - הדוגמה של כפל מטריצות',
    q=r'האם המכפלה $\begin{bmatrix}2&3\\1&-2\end{bmatrix}\begin{bmatrix}2&3&4\\3&4&5\end{bmatrix}$ קיימת? אם כן, מאיזה סדר היא? חשבו אותה.',
    steps=[
        (r'האם קיימת? - המספרים הפנימיים', [
            r'הראשונה $2\times2$ והשנייה $2\times3$: מספר העמודות של הראשונה (2) שווה למספר השורות של השנייה (2) - <b>כן</b>, קיימת.']),
        (r'הסדר של התוצאה - המספרים החיצוניים', [
            r'$2\times\underline{2}\cdot\underline{2}\times3$, ולכן התוצאה ב-$M_{2,3}(\mathbb{R})$.']),
        (r'שורה 1 כפול כל עמודה: $c_{i,j}=\sum_k a_{i,k}b_{k,j}$', [
            r'$$c_{1,1}=2\cdot2+3\cdot3=13\qquad c_{1,2}=2\cdot3+3\cdot4=18\qquad c_{1,3}=2\cdot4+3\cdot5=23$$']),
        (r'שורה 2 כפול כל עמודה', [
            r'$$c_{2,1}=1\cdot2+(-2)\cdot3=-4\qquad c_{2,2}=1\cdot3+(-2)\cdot4=-5\qquad c_{2,3}=1\cdot4+(-2)\cdot5=-6$$']),
    ],
    ans=r'$\begin{bmatrix}2&3\\1&-2\end{bmatrix}\begin{bmatrix}2&3&4\\3&4&5\end{bmatrix}=\begin{bmatrix}13&18&23\\-4&-5&-6\end{bmatrix}\in M_{2,3}(\mathbb{R})$'),

'ex2-s5': dict(
    src='מצגת מטריצות, פרק 2 - צירוף לינארי, דוגמה 1',
    q=r'האם $\begin{bmatrix}-7&6\\3&4\end{bmatrix}$ היא צירוף לינארי של $M_1=\begin{bmatrix}1&2\\1&3\end{bmatrix}$ ו-$M_2=\begin{bmatrix}2&0\\0&1\end{bmatrix}$?',
    steps=[
        (r'מחפשים מקדמים $\alpha,\beta$', [
            r'$$\begin{bmatrix}-7&6\\3&4\end{bmatrix}=\alpha\begin{bmatrix}1&2\\1&3\end{bmatrix}+\beta\begin{bmatrix}2&0\\0&1\end{bmatrix}=\begin{bmatrix}\alpha+2\beta&2\alpha\\\alpha&3\alpha+\beta\end{bmatrix}$$']),
        (r'שוויון איבר-איבר נותן מערכת', [
            r'$$\begin{cases}\alpha+2\beta=-7\\2\alpha=6\\\alpha=3\\3\alpha+\beta=4\end{cases}$$']),
        (r'פותרים ובודקים שכל המשוואות מתקיימות', [
            r'$\alpha=3$, ומהראשונה $\beta=-5$. בדיקה ברביעית: $3\cdot3-5=4$ ✓.']),
    ],
    ans=r'כן: $\begin{bmatrix}-7&6\\3&4\end{bmatrix}=3M_1-5M_2$'),

'ex2-s6': dict(
    src='מצגת מטריצות, פרק 3 - התרגיל על $M=ADA^t$',
    q=r'נתונות מטריצות $A,D\in M_n(\mathbb{R})$, ונתון ש-$D$ מטריצה אלכסונית. הוכיחו שהמטריצה $M=ADA^t$ סימטרית.',
    steps=[
        (r'מה צריך להוכיח?', [
            r'מטריצה סימטרית מקיימת $M^t=M$. לכן מחשבים את $M^t$.']),
        (r'משחלפים מכפלה - הסדר מתהפך', [
            r'לפי $(ABC)^t=C^tB^tA^t$:',
            r'$$M^t=(ADA^t)^t=(A^t)^tD^tA^t$$']),
        (r'משתמשים בשתי עובדות', [
            r'$(A^t)^t=A$, ו-$D^t=D$ כי $D$ אלכסונית.']),
        (r'מסכמים', [
            r'$$M^t=ADA^t=M$$']),
    ],
    ans=r'$M^t=M$, ולכן $M=ADA^t$ סימטרית. מ.ש.ל.'),

'ex2-s7': dict(
    src='מצגת מטריצות, פרק 3 (עקבה) - הדוגמה ל-$tr(AB)=tr(BA)$',
    q=r'נתונות $A=\begin{bmatrix}1&2&0\\4&-1&5\end{bmatrix}$ ו-$B=\begin{bmatrix}3&0\\1&5\\-4&1\end{bmatrix}$. חשבו את $\operatorname{tr}(AB)$ ואת $\operatorname{tr}(BA)$.',
    steps=[
        (r'מחשבים את $AB$ (מסדר $2\times2$)', [
            r'$$AB=\begin{bmatrix}5&10\\-9&0\end{bmatrix}\Rightarrow\operatorname{tr}(AB)=5+0=5$$']),
        (r'מחשבים את $BA$ (מסדר $3\times3$)', [
            r'$$BA=\begin{bmatrix}3&6&0\\21&-3&25\\0&-9&5\end{bmatrix}\Rightarrow\operatorname{tr}(BA)=3-3+5=5$$']),
        (r'משווים', [
            r'$AB$ ו-$BA$ שונות לגמרי (אפילו לא מאותו סדר), ובכל זאת העקבות שוות - בדיוק כמו התכונה $\operatorname{tr}(AB)=\operatorname{tr}(BA)$.']),
    ],
    ans=r'$\operatorname{tr}(AB)=\operatorname{tr}(BA)=5$'),
}
