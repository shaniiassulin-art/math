# -*- coding: utf-8 -*-
# לכל שלב ב"שלבי הפתרון": המושגים שצריך להבין כדי לבצע אותו (ההסברים עצמם ב-concepts.py).
# STEP_CONCEPTS[סעיף][מספר השלב, מ-0] = [מושגים]. NEW_STEPS[סעיף] = [(טקסט השלב, [מושגים])] לסעיף שאין בו רשימת שלבים.

STEP_CONCEPTS = {'ex1-s1': {0: ['function', 'domainrules'], 1: ['ineq'], 2: ['intervals'], 3: ['intervals']}, 'ex1-s2': {0: ['ineq'], 1: ['factor'], 2: ['signtable'], 3: ['signtable'], 4: ['signtable', 'intervals']}, 'ex1-s3': {0: ['radians', 'trig', 'tancot'], 1: ['tancot'], 2: ['ineq']}, 'ex1-s4': {0: ['basegraphs', 'trig', 'radians'], 1: ['transform', 'factorarg'], 2: ['transform'], 3: ['basegraphs']}, 'ex1-s5': {0: ['transform', 'factorarg'], 1: ['factorarg'], 2: ['transform']}, 'ex1-s7': {0: ['function', 'parity', 'basegraphs'], 1: ['minusx'], 2: ['parity']}, 'ex1-s8': {0: ['compose', 'parity', 'minusx'], 1: ['trig', 'sincosparity'], 2: ['parity']}, 'ex1-s9': {0: ['parity'], 1: ['parity']}, 'ex1-s10': {0: ['compose'], 1: ['compose'], 2: ['expand', 'powers'], 3: ['compose']}, 'ex1-s11': {0: ['compose'], 2: ['compose', 'powers']}, 'ex1-s12': {0: ['compose', 'parity'], 1: ['parity'], 2: ['parity']}, 'ex1-s13': {1: ['compose'], 2: ['parity']}, 'ex1-s14': {0: ['model', 'compose'], 1: ['compose'], 2: ['powers']}, 'ex1-s15': {0: ['model'], 1: ['model'], 2: ['ratio']}, 'ex1-s16': {0: ['model', 'compose'], 1: ['ineq']}, 'ex1-s17': {0: ['trig', 'cosbound'], 1: ['cosbound', 'radians']}, 'ex1-s18': {0: ['factorarg', 'transform'], 2: ['trig', 'radians']}, 'ex1-s19': {0: ['domainrules', 'basegraphs', 'ineq', 'intervals'], 1: ['intervals'], 2: ['logrules'], 3: ['logrules']}, 'ex2-s1': {0: ['piecewise'], 1: ['piecewise'], 2: ['piecewise'], 3: ['dots'], 4: ['dots']}, 'ex2-s2': {0: ['abs', 'factor'], 1: ['signtable'], 2: ['abs'], 3: ['piecewise']}, 'ex2-s4': {0: ['basegraphs'], 1: ['transform', 'absgraph'], 2: ['absgraph', 'transform'], 3: ['range']}, 'ex2-s5': {0: ['floor'], 1: ['floor'], 2: ['dots']}, 'ex2-s6': {0: ['mono'], 1: ['mono'], 2: ['ineq'], 3: ['addineq']}, 'ex2-s7': {0: ['mono', 'compose'], 1: ['mono'], 2: ['mono']}, 'ex2-s8': {0: ['mono'], 1: ['mono'], 2: ['injective']}, 'ex2-s9': {0: ['trig', 'radians', 'period'], 1: ['injective', 'mono'], 2: ['range', 'onto'], 3: ['onto']}, 'ex2-s10': {0: ['counter'], 1: ['mono', 'sqineq', 'compose', 'injective'], 2: ['counter']}, 'ex2-s11': {0: ['injective', 'onto']}, 'ex2-s12': {0: ['piecewise'], 1: ['mono'], 2: ['injective'], 3: ['range', 'onto']}, 'ex2-s13': {0: ['floor'], 1: ['range'], 2: ['mono'], 3: ['floor', 'ineq']}, 'ex2-s14': {0: ['mono', 'floor', 'compose'], 2: ['injective'], 3: ['onto']}}

NEW_STEPS = {
'ex1-s6': [
    ('<b>מחזור:</b> אם לבסיס מחזור $T$, אז ל-$f(bx)$ המחזור $\\frac{T}{|b|}$. הזזות ומתיחות אנכיות לא משנות אותו.', ['radians', 'trig', 'period']),
    ('<b>תמונה של $\\sin$/$\\cos$:</b> מתחילים מ-$-1\\leq\\cos(\\dots)\\leq1$ ומפעילים את מה שמחוץ לסוגריים - כפל, מינוס, הוספה.', ['range', 'ineq']),
    ('<b>לוגריתם:</b> מוצאים את האסימפטוטה מ"מה שבפנים $=0$", ואת התחום מ"מה שבפנים $>0$".', ['basegraphs', 'domainrules']),
],
'ex2-s3': [
    ('<b>מזהים איפה הערך המוחלט:</b> סביב כל הפונקציה - $|f(x)|$, או רק סביב $x$ - $f(|x|)$.', ['abs']),
    ('<b>$|f(x)|$:</b> משרטטים את $f$, ומשקפים למעלה כל חלק שמתחת לציר $x$.', ['absgraph']),
    ('<b>$f(|x|)$:</b> משאירים את הצד הימני ($x\\geq0$), מוחקים את השמאלי, ובמקומו משקפים את הימני בציר $y$.', ['absgraph']),
],
}
