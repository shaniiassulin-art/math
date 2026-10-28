# -*- coding: utf-8 -*-
# שאלה לדוגמה לכל סעיף באתר "הכנה למבחן - אלגברה לינארית". השאלות מתוך תרגילי הקורס,
# והשלבים לפי "שלבי הפתרון" של אותו סעיף.

SAMPLES = {
'ex1-s1': dict(
    src='הנתונים של תרגיל כיתה 1, שאלה 3',
    q=r'נתונים $z_1=1-5i$ ו-$z_2=3+4i$. לכל אחד מהם מצאו את החלק הממשי, החלק המדומה, הצמוד והערך המוחלט.',
    steps=[
        (r'מזהים $a$ ו-$b$ בצורה $z=a+bi$', [
            r'$z_1=1+(-5)i$: $\ \operatorname{Re}(z_1)=1$, $\ \operatorname{Im}(z_1)=-5$ (בלי ה-$i$).',
            r'$z_2=3+4i$: $\ \operatorname{Re}(z_2)=3$, $\ \operatorname{Im}(z_2)=4$.']),
        (r'הצמוד: אותו $a$, סימן הפוך ל-$b$', [
            r'$$\overline{z_1}=1+5i\qquad \overline{z_2}=3-4i$$']),
        (r'הערך המוחלט: $|z|=\sqrt{a^2+b^2}$', [
            r'$$|z_1|=\sqrt{1^2+(-5)^2}=\sqrt{26}\qquad |z_2|=\sqrt{3^2+4^2}=5$$']),
        (r'בדיקה בעזרת $z\overline{z}=|z|^2$', [
            r'$$z_2\overline{z_2}=(3+4i)(3-4i)=9+16=25=5^2\ ✓$$']),
    ],
    ans=r'$z_1$: $1$, $-5$, $1+5i$, $\sqrt{26}$. $\quad z_2$: $3$, $4$, $3-4i$, $5$.'),

'ex1-s2': dict(
    src='תרגיל כיתה 1, שאלה 1ו',
    q=r'רשמו בהצגה קרטזית: $(1+2i)(4-6i)^2$.',
    steps=[
        (r'קודם החזקה - כפל מקוצר', [
            r'$$(4-6i)^2=16-48i+36i^2$$']),
        (r'מחליפים $i^2=-1$', [
            r'$$16-48i-36=-20-48i$$']),
        (r'עכשיו הכפל - פותחים סוגריים', [
            r'$$(1+2i)(-20-48i)=-20-48i-40i-96i^2$$']),
        (r'שוב $i^2=-1$, ואוספים איברים', [
            r'$$-20-88i+96=76-88i$$']),
    ],
    ans=r'$(1+2i)(4-6i)^2=76-88i$'),

'ex1-s3': dict(
    src='תרגיל כיתה 1, שאלה 1א',
    q=r'רשמו בהצגה קרטזית: $\frac{2+3i}{7-3i}$.',
    steps=[
        (r'המכנה לא חזקה - אפשר להתחיל', [
            r'הצמוד של המכנה $7-3i$ הוא $7+3i$.']),
        (r'מכפילים מונה ומכנה בצמוד של המכנה', [
            r'$$\frac{2+3i}{7-3i}=\frac{(2+3i)(7+3i)}{(7-3i)(7+3i)}=\frac{(2+3i)(7+3i)}{7^2+3^2}$$']),
        (r'פותחים את המונה ומחליפים $i^2=-1$', [
            r'$$(2+3i)(7+3i)=14+6i+21i+9i^2=5+27i$$']),
        (r'מפצלים לחלק ממשי ולחלק מדומה', [
            r'$$\frac{5+27i}{58}=\frac{5}{58}+\frac{27}{58}i$$']),
    ],
    ans=r'$\frac{2+3i}{7-3i}=\frac{5}{58}+\frac{27}{58}i$'),

'ex1-s4': dict(
    src='תרגיל כיתה 1, שאלה 2ג',
    q=r'רשמו בהצגה קרטזית: $(i+i^2+i^3+\dots+i^{101}+i^{102})^2$.',
    steps=[
        (r'מחלקים את הסכום לרביעיות', [
            r'כל ארבע חזקות רצופות נותנות $i+(-1)+(-i)+1=0$.',
            r'102 איברים = 25 רביעיות שלמות (100 איברים) ועוד 2 איברים: $i^{101}$ ו-$i^{102}$.']),
        (r'מחשבים את מה שנשאר לפי השארית בחלוקה ב-4', [
            r'$101=4\cdot25+1\Rightarrow i^{101}=i$. $\quad 102=4\cdot25+2\Rightarrow i^{102}=-1$.',
            r'$$i+i^2+\dots+i^{102}=0+i-1=-1+i$$']),
        (r'מעלים בריבוע', [
            r'$$(-1+i)^2=1-2i+i^2=-2i$$']),
    ],
    ans=r'$(i+i^2+\dots+i^{102})^2=-2i$'),

'ex1-s5': dict(
    src='תרגיל בית 1, שאלה 2',
    q=r'יהיו $a,b$ שני מספרים ממשיים, ונתון ש-$\frac{5-i}{a+bi}=1-i$. חשבו את $a^3+b^3$.',
    steps=[
        (r'נפטרים מהשבר - כופלים במכנה', [
            r'$$5-i=(1-i)(a+bi)$$']),
        (r'פותחים ומסדרים בצורה $(\dots)+(\dots)i$', [
            r'$$(1-i)(a+bi)=a+bi-ai-bi^2=(a+b)+(b-a)i$$']),
        (r'משווים חלקים', [
            r'$$\begin{cases}a+b=5\\b-a=-1\end{cases}\Rightarrow\begin{cases}a=3\\b=2\end{cases}$$']),
        (r'מחשבים את מה שמבקשים', [
            r'$$a^3+b^3=27+8=35$$']),
    ],
    ans=r'$a^3+b^3=35$'),

'ex1-s6': dict(
    src='תרגיל כיתה 1, שאלה 7 (שלב 1)',
    q=r'מצאו את המספר המרוכב $z$ המקיים $2z+\overline{z}=3+2i$.',
    steps=[
        (r'מציבים $z=a+bi$ ו-$\overline{z}=a-bi$', [
            r'$$2(a+bi)+(a-bi)=3+2i$$']),
        (r'מסדרים כל צד', [
            r'$$3a+bi=3+2i$$']),
        (r'משווים חלקים', [
            r'ממשי: $3a=3\Rightarrow a=1$. מדומה: $b=2$.']),
    ],
    ans=r'$z=1+2i$'),

'ex1-s7': dict(
    src='תרגיל בית 1, שאלה 4',
    q=r'נתון מספר מרוכב $z$ המקיים $\frac{z^2\,\overline{z}}{(2i+11)^2}=1+i$. מצאו את $|z|$.',
    steps=[
        (r'שמים ערך מוחלט על שני הצדדים', [
            r'$$\left|\frac{z^2\,\overline{z}}{(2i+11)^2}\right|=|1+i|$$']),
        (r'מפרקים לפי התכונות של כפל, חילוק וחזקה', [
            r'$$\frac{|z|^2\cdot|\overline{z}|}{|2i+11|^2}=\frac{|z|^3}{|11+2i|^2}$$',
            r'כי $|\overline{z}|=|z|$.']),
        (r'מחשבים כל גורם בנפרד', [
            r'$|11+2i|^2=121+4=125$, ו-$|1+i|=\sqrt2$.',
            r'$$\frac{|z|^3}{125}=\sqrt{2}$$']),
        (r'פותרים את המשוואה ב-$|z|$', [
            r'$$|z|^3=125\sqrt{2}\Rightarrow|z|=5\cdot\sqrt[6]{2}$$']),
    ],
    ans=r'$|z|=5\sqrt[6]{2}$'),

'ex1-s8': dict(
    src='תרגיל כיתה 1, שאלה 10',
    q=r'הוכיחו כי לכל מספר מרוכב $z\neq-2$ שמקיים $z\overline{z}+z+\overline{z}=0$, המספר $\omega=\frac{z}{z+2}$ הוא מדומה טהור.',
    steps=[
        (r'מדומה טהור - בודקים את $\omega+\overline{\omega}$', [
            r'$\omega$ מדומה טהור אם ורק אם $\omega+\overline{\omega}=0$.']),
        (r'מחשבים את הצמוד לפי התכונות', [
            r'$$\overline{\omega}=\frac{\overline{z}}{\overline{z}+2}$$']),
        (r'מכנה משותף ופתיחת המונה', [
            r'$$\omega+\overline{\omega}=\frac{z(\overline{z}+2)+\overline{z}(z+2)}{(z+2)(\overline{z}+2)}=\frac{2z\overline{z}+2z+2\overline{z}}{(z+2)(\overline{z}+2)}$$']),
        (r'מזהים את הנתון במונה', [
            r'$$2z\overline{z}+2z+2\overline{z}=2(z\overline{z}+z+\overline{z})=2\cdot0=0$$']),
    ],
    ans=r'$\omega+\overline{\omega}=0$, ולכן $\omega$ מדומה טהור. מ.ש.ל.'),

'ex1-s9': dict(
    src='תרגיל בית 1, שאלה 6ב',
    q=r'תהי $z$ מספר מרוכב שמקיים $|z+1|=|z-1|$. הוכיחו ש-$iz$ הוא מספר ממשי.',
    steps=[
        (r'מעלים בריבוע', [
            r'$$|z+1|^2=|z-1|^2$$']),
        (r'משתמשים ב-$|w|^2=w\overline{w}$', [
            r'$$(z+1)(\overline{z}+1)=(z-1)(\overline{z}-1)$$']),
        (r'פותחים ומבטלים איברים זהים', [
            r'$$z\overline{z}+z+\overline{z}+1=z\overline{z}-z-\overline{z}+1\Rightarrow2(z+\overline{z})=0$$']),
        (r'מזהים ומסיקים', [
            r'$z+\overline{z}=0$, כלומר $z$ מדומה טהור: $z=bi$.',
            r'ואז $iz=i\cdot bi=-b$ - מספר ממשי.']),
    ],
    ans=r'$z$ מדומה טהור, ולכן $iz$ ממשי. מ.ש.ל.'),

'ex1-s10': dict(
    src='תרגיל בית 1, שאלה 6א',
    q=r'תהי $z$ מספר מרוכב שמקיים $z^{11}=1$. הוכיחו ש-$z+\frac{1}{z}$ הוא מספר ממשי.',
    steps=[
        (r'מסיקים ש-$|z|=1$', [
            r'$|z^{11}|=|1|$, כלומר $|z|^{11}=1$, ולכן $|z|=1$.']),
        (r'מתרגמים לכלי עבודה', [
            r'$|z|=1$, ולכן אפשר לכתוב $z=e^{i\alpha}$ (וגם $\frac1z=\overline{z}$).']),
        (r'מחשבים', [
            r'$$z+\frac1z=e^{i\alpha}+e^{-i\alpha}=(\cos\alpha+i\sin\alpha)+(\cos\alpha-i\sin\alpha)=2\cos\alpha$$']),
    ],
    ans=r'$z+\frac1z=2\cos\alpha\in\mathbb{R}$. מ.ש.ל.'),

'ex1-s11': dict(
    src='תרגיל כיתה 1, שאלה 13ב',
    q=r'תהי $z$ מספר מרוכב שמקיים $\operatorname{Re}(z)=\operatorname{Im}(z)$. הוכיחו ש-$\frac{iz}{1-i}$ הוא מספר ממשי.',
    steps=[
        (r'כותבים את $z$ עם פרמטר אחד', [
            r'$\operatorname{Re}(z)=\operatorname{Im}(z)=a$, ולכן $z=a+ai=a(1+i)$, $\ a\in\mathbb{R}$.']),
        (r'מציבים', [
            r'$$\frac{iz}{1-i}=\frac{ia(1+i)}{1-i}=a\cdot\frac{-1+i}{1-i}$$']),
        (r'מצמצמים', [
            r'$-1+i=-(1-i)$, ולכן $\frac{-1+i}{1-i}=-1$:',
            r'$$\frac{iz}{1-i}=-a$$']),
    ],
    ans=r'$\frac{iz}{1-i}=-a\in\mathbb{R}$. מ.ש.ל.'),

'ex1-s12': dict(
    src='תרגיל כיתה 1, שאלה 14ד',
    q=r'רשמו הצגה קוטבית $re^{i\theta}$ למספר $-3-3i$.',
    steps=[
        (r'הרביע לפי הסימנים', [
            r'$a=-3<0$ ו-$b=-3<0$: רביע שלישי.']),
        (r'המרחק מהראשית', [
            r'$$r=\sqrt{(-3)^2+(-3)^2}=\sqrt{18}=3\sqrt{2}$$']),
        (r'זווית בסיס מהטנגנס', [
            r'$\tan\theta=\frac{-3}{-3}=1$, ולכן $\arctan1=\frac{\pi}{4}$.']),
        (r'תיקון לפי הרביע (שלישי: מחסירים $\pi$)', [
            r'$$\theta=\frac{\pi}{4}-\pi=-\frac{3\pi}{4}$$']),
        (r'כותבים את ההצגה', [
            r'$$-3-3i=3\sqrt{2}e^{-i\frac{3\pi}{4}}$$',
            r'כלומר $3\sqrt{2}\left(\cos\frac{3\pi}{4}-i\sin\frac{3\pi}{4}\right)$ - ובדיקה: $r\cos\theta=-3$, $\ r\sin\theta=-3$ ✓']),
    ],
    ans=r'$-3-3i=3\sqrt2e^{-i\frac{3\pi}{4}}$'),

'ex1-s13': dict(
    src='תרגיל בית 1, שאלה 10א',
    q=r'רשמו בהצגה קרטזית: $(\sqrt{3}+i)^7$.',
    steps=[
        (r'שלב 1: הבסיס בצורה קוטבית', [
            r'$r=\sqrt{3+1}=2$, רביע ראשון, $\tan\theta=\frac{1}{\sqrt3}$, ולכן $\theta=\frac{\pi}{6}$: $\ \sqrt3+i=2e^{i\frac{\pi}{6}}$.']),
        (r'שלב 2: דה-מואבר', [
            r'$$(\sqrt{3}+i)^7=2^7e^{i\frac{7\pi}{6}}=128e^{i\frac{7\pi}{6}}$$']),
        (r'חוזרים לקרטזי', [
            r'$\cos\frac{7\pi}{6}=-\frac{\sqrt3}{2}$, $\ \sin\frac{7\pi}{6}=-\frac12$:',
            r'$$128\left(-\frac{\sqrt3}{2}-\frac12i\right)=-64\sqrt{3}-64i$$']),
    ],
    ans=r'$(\sqrt3+i)^7=-64\sqrt3-64i$'),

'ex1-s14': dict(
    src='תרגיל כיתה 1, שאלה 16',
    q=r'בעזרת הצגה קוטבית הוכיחו שלכל $\alpha\in\mathbb{R}$: $\ \cos3\alpha=4\cos^3\alpha-3\cos\alpha$.',
    steps=[
        (r'כותבים את $e^{i3\alpha}$ בשתי דרכים', [
            r'$$\cos3\alpha+i\sin3\alpha=e^{i3\alpha}=(e^{i\alpha})^3=(\cos\alpha+i\sin\alpha)^3$$']),
        (r'פותחים בבינום, עם $i^2=-1$ ו-$i^3=-i$', [
            r'$$(\cos\alpha+i\sin\alpha)^3=\cos^3\alpha+3i\cos^2\alpha\sin\alpha-3\cos\alpha\sin^2\alpha-i\sin^3\alpha$$']),
        (r'משווים חלקים ממשיים', [
            r'$$\cos3\alpha=\cos^3\alpha-3\cos\alpha\sin^2\alpha$$']),
        (r'מחליפים $\sin^2\alpha=1-\cos^2\alpha$', [
            r'$$\cos3\alpha=\cos^3\alpha-3\cos\alpha(1-\cos^2\alpha)=4\cos^3\alpha-3\cos\alpha$$']),
    ],
    ans=r'$\cos3\alpha=4\cos^3\alpha-3\cos\alpha$. מ.ש.ל. (מהחלק המדומה מקבלים באותה דרך $\sin3\alpha=3\sin\alpha-4\sin^3\alpha$.)'),

'ex2-s1': dict(
    src='תרגיל בית 2, שאלה 2',
    q=r'מצאו את כל הפתרונות של המשוואה $z^4=16ie^{i\frac{\pi}{14}}$.',
    steps=[
        (r'שלב 1: צד ימין בצורה קוטבית', [
            r'$i=e^{i\frac{\pi}{2}}$, ולכן $16ie^{i\frac{\pi}{14}}=16e^{i\left(\frac{\pi}{2}+\frac{\pi}{14}\right)}=16e^{i\frac{4\pi}{7}}$.']),
        (r'שלב 2: מציבים $z=re^{i\theta}$', [
            r'$$r^4e^{i4\theta}=16e^{i\frac{4\pi}{7}}$$']),
        (r'משווים', [
            r'$$r^4=16\Rightarrow r=2\qquad 4\theta=\frac{4\pi}{7}+2\pi k\Rightarrow\theta=\frac{\pi}{7}+\frac{\pi k}{2}$$']),
        (r'כותבים את כל 4 הפתרונות ($k=0,1,2,3$)', [
            r'$$z_0=2e^{i\frac{\pi}{7}},\quad z_1=2e^{i\frac{9\pi}{14}},\quad z_2=2e^{i\frac{8\pi}{7}},\quad z_3=2e^{i\frac{23\pi}{14}}$$']),
    ],
    ans=r'4 פתרונות על מעגל ברדיוס 2, כל אחד מסובב ב-$\frac{\pi}{2}$ מהקודם.'),

'ex2-s2': dict(
    src='תרגיל בית 2, שאלה 1א',
    q=r'מצאו את כל הפתרונות של המשוואה $z^5-(\sqrt{3}-3i)z=0$.',
    steps=[
        (r'מוציאים $z$', [
            r'$$z\left(z^4-(\sqrt{3}-3i)\right)=0$$']),
        (r'מכפלה שווה 0', [
            r'$z=0$, או $z^4=\sqrt{3}-3i$.']),
        (r'צד ימין בצורה קוטבית', [
            r'$|\sqrt3-3i|=\sqrt{3+9}=2\sqrt3$; רביע רביעי, $\tan\theta=-\sqrt3$, ולכן $\theta=-\frac{\pi}{3}$:',
            r'$$\sqrt{3}-3i=2\sqrt{3}e^{-i\frac{\pi}{3}}$$']),
        (r'פותרים $z^4=2\sqrt3e^{-i\frac{\pi}{3}}$ לפי סעיף 1', [
            r'$r=\sqrt[4]{2\sqrt3}$, $\ \theta=-\frac{\pi}{12}+\frac{\pi k}{2}$, $\ k=0,1,2,3$:',
            r'$$z_k=\sqrt[4]{2\sqrt3}\,e^{i\left(-\frac{\pi}{12}+\frac{\pi k}{2}\right)}:\quad -\frac{\pi}{12},\ \frac{5\pi}{12},\ \frac{11\pi}{12},\ \frac{17\pi}{12}$$']),
        (r'מוסיפים את $z=0$', [
            r'לא מחלקים ב-$z$ - אחרת הפתרון הזה הולך לאיבוד.']),
    ],
    ans=r'5 פתרונות: $z=0$, ועוד ארבעת הפתרונות $z_k=\sqrt[4]{2\sqrt3}\,e^{i\left(-\frac{\pi}{12}+\frac{\pi k}{2}\right)}$.'),

'ex2-s3': dict(
    src='תרגיל בית 2, שאלה 1ב',
    q=r'מצאו את כל הפתרונות של המשוואה $z^6=\frac{1-i}{1+\sqrt{3}i}$.',
    steps=[
        (r'$z^6$ לבד בצד שמאל - אפשר להמשיך', [
            r'אין מקדם לפני $z^6$, לכן עוברים ישר לצד ימין.']),
        (r'כל גורם בצורה קוטבית בנפרד', [
            r'$1-i=\sqrt2e^{-i\frac{\pi}{4}}$ (רביע רביעי). $\quad 1+\sqrt3i=2e^{i\frac{\pi}{3}}$ (רביע ראשון).']),
        (r'חילוק: מחלקים מודולים ומחסירים זוויות', [
            r'$$\frac{\sqrt{2}e^{-i\frac{\pi}{4}}}{2e^{i\frac{\pi}{3}}}=\frac{\sqrt2}{2}e^{-i\frac{7\pi}{12}}=2^{-\frac12}e^{-i\frac{7\pi}{12}}$$']),
        (r'פותרים לפי סעיף 1', [
            r'$r^6=2^{-\frac12}\Rightarrow r=2^{-\frac{1}{12}}$; $\ 6\theta=-\frac{7\pi}{12}+2\pi k\Rightarrow\theta=-\frac{7\pi}{72}+\frac{\pi k}{3}$.',
            r'$$z_k=2^{-\frac{1}{12}}e^{i\left(-\frac{7\pi}{72}+\frac{\pi k}{3}\right)},\quad k=0,1,\dots,5$$']),
    ],
    ans=r'6 פתרונות: $z_k=2^{-\frac{1}{12}}e^{i\left(-\frac{7\pi}{72}+\frac{\pi k}{3}\right)}$, $\ k=0,\dots,5$.'),

'ex2-s4': dict(
    src='תרגיל בית 2, שאלה 3',
    q=r'מצאו את כל הפתרונות של המשוואה $\left(\frac{z+2i}{z-i}\right)^3=-1$.',
    steps=[
        (r'שלב 1 - הצבה', [
            r'מסמנים $\omega=\frac{z+2i}{z-i}$ ופותרים $\omega^3=-1=e^{i\pi}$:',
            r'$$\omega_k=e^{i\left(\frac{\pi}{3}+\frac{2\pi k}{3}\right)}:\quad \omega_0=e^{i\frac{\pi}{3}},\ \ \omega_1=e^{i\pi}=-1,\ \ \omega_2=e^{i\frac{5\pi}{3}}$$']),
        (r'שלב 2 - מחלצים את $z$', [
            r'$$\omega(z-i)=z+2i\Rightarrow z(\omega-1)=2i+i\omega\Rightarrow z=\frac{2i+i\omega}{\omega-1}$$',
            r'אף אחד מה-$\omega$-ות אינו 1, אז לכל אחד יש $z$ מתאים.']),
        (r'מציבים כל $\omega_k$', [
            r'$\omega_1=-1$: $\ z_1=\frac{2i-i}{-2}=-\frac{i}{2}$.',
            r'$\omega_0=\frac12+\frac{\sqrt3}{2}i$: אחרי כפל בצמוד של המכנה, $z_0=\frac{3\sqrt3}{2}-\frac{i}{2}$.',
            r'$\omega_2=\frac12-\frac{\sqrt3}{2}i$: באותה דרך, $z_2=-\frac{3\sqrt3}{2}-\frac{i}{2}$.']),
    ],
    ans=r'$z_0=\frac{3\sqrt3}{2}-\frac i2$, $\ z_1=-\frac i2$, $\ z_2=-\frac{3\sqrt3}{2}-\frac i2$'),

'ex2-s5': dict(
    src='תרגיל בית 2, שאלה 4 (א,ב)',
    q=r'נתון $z_0=\frac{\sqrt{2+\sqrt2}+i\sqrt{2-\sqrt2}}{2}$. א. חשבו את $z_0^2$ ורשמו אותו בהצגה קוטבית. ב. מצאו הצגה קוטבית ל-$z_0$.',
    steps=[
        (r'א. מעלים בריבוע (כפל מקוצר)', [
            r'לפי $(a+bi)^2=a^2-b^2+2abi$ עם $a=\sqrt{2+\sqrt2}$, $\ b=\sqrt{2-\sqrt2}$:',
            r'$$a^2-b^2=(2+\sqrt2)-(2-\sqrt2)=2\sqrt2$$',
            r'$$2ab=2\sqrt{(2+\sqrt2)(2-\sqrt2)}=2\sqrt{2}$$',
            r'$$z_0^2=\frac{2\sqrt2+2\sqrt2\,i}{4}=\frac{\sqrt2}{2}+\frac{\sqrt2}{2}i$$']),
        (r'צורה קוטבית של $z_0^2$', [
            r'$|z_0^2|=1$, רביע ראשון, $\tan\theta=1$, ולכן $z_0^2=e^{i\frac{\pi}{4}}$.']),
        (r'ב. שורש ריבועי: שתי אפשרויות', [
            r'$z_0=e^{i\frac{\pi}{8}}$ או $z_0=e^{i\left(\frac{\pi}{8}+\pi\right)}=-e^{i\frac{\pi}{8}}$.']),
        (r'בוחרים לפי הסימנים של $z_0$', [
            r'גם $\operatorname{Re}(z_0)$ וגם $\operatorname{Im}(z_0)$ חיוביים - רביע ראשון, ולכן $z_0=e^{i\frac{\pi}{8}}$.']),
    ],
    ans=r'$z_0^2=e^{i\frac{\pi}{4}}$, $\ z_0=e^{i\frac{\pi}{8}}$'),

'ex2-s6': dict(
    src='תרגיל בית 2, שאלה 6',
    q=r'פתרו את המשוואה $z^2+2z+2=0$ באמצעות הנוסחה לפתרון משוואה ריבועית.',
    steps=[
        (r'מחשבים $\Delta$', [
            r'$$\Delta=b^2-4ac=4-8=-4$$']),
        (r'$\Delta<0$: השורש הוא $i\sqrt{|\Delta|}$', [
            r'$$\sqrt{\Delta}=i\sqrt{4}=2i$$']),
        (r'מציבים בנוסחה', [
            r'$$z_{1,2}=\frac{-2\pm2i}{2}=-1\pm i$$']),
    ],
    ans=r'$z_1=-1+i$, $\ z_2=-1-i$ - שני פתרונות צמודים.'),

'ex2-s7': dict(
    src='תרגיל בית 2, שאלה 7',
    q=r'נתון הפולינום $P(z)=z^4-4z^3+3z^2+8z-10$. א. בדקו ש-$2+i$ שורש של $P(z)$. ב. מצאו את כל השורשים המרוכבים של $P(z)$.',
    steps=[
        (r'א. החזקות של $a=2+i$ בנפרד', [
            r'$$a^2=3+4i\qquad a^3=a^2\cdot a=2+11i\qquad a^4=(a^2)^2=-7+24i$$']),
        (r'מציבים ובודקים שיוצא 0', [
            r'$$P(2+i)=(-7+24i)-4(2+11i)+3(3+4i)+8(2+i)-10=0$$']),
        (r'ב. גם הצמוד שורש', [
            r'המקדמים של $P$ ממשיים, ולכן גם $2-i$ שורש.']),
        (r'בונים את הגורם הריבועי', [
            r'$$(z-(2+i))(z-(2-i))=z^2-2\operatorname{Re}(a)z+|a|^2=z^2-4z+5$$']),
        (r'חילוק ארוך ופתרון המנה', [
            r'$$P(z)=(z^2-4z+5)(z^2-2)$$',
            r'$z^2-2=0\Rightarrow z=\pm\sqrt2$.']),
    ],
    ans=r'השורשים: $2+i,\ 2-i,\ \sqrt2,\ -\sqrt2$'),

'ex2-s8': dict(
    src='תרגיל בית 2, שאלה 5',
    q=r'א. מצאו את כל הפתרונות של $iz^4-16e^{i\frac{\pi}{5}}=0$. ב. הוכיחו שאם $z$ אחד הפתרונות, אז $\omega=\frac{z-2}{z+2}$ הוא מדומה טהור.',
    steps=[
        (r'א. מבודדים ומעבירים לצורה קוטבית', [
            r'$$z^4=\frac{16e^{i\frac{\pi}{5}}}{i}=16e^{i\left(\frac{\pi}{5}-\frac{\pi}{2}\right)}=16e^{-i\frac{3\pi}{10}}$$',
            r'$$z_k=2e^{i\left(-\frac{3\pi}{40}+\frac{\pi k}{2}\right)},\quad k=0,1,2,3$$']),
        (r'ב. מה משותף לכל הפתרונות', [
            r'לכולם $|z|=2$, כלומר $z\overline{z}=4$.']),
        (r'מדומה טהור - בודקים $\omega+\overline{\omega}$', [
            r'$$\omega+\overline{\omega}=\frac{(z-2)(\overline{z}+2)+(\overline{z}-2)(z+2)}{(z+2)(\overline{z}+2)}=\frac{2z\overline{z}-8}{(z+2)(\overline{z}+2)}$$']),
        (r'מציבים $z\overline{z}=4$', [
            r'$$2\cdot4-8=0\Rightarrow\omega+\overline{\omega}=0$$']),
    ],
    ans=r'$\omega+\overline{\omega}=0$, ולכן $\omega$ מדומה טהור לכל אחד מהפתרונות. מ.ש.ל.'),
}
