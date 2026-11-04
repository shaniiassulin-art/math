# -*- coding: utf-8 -*-
# לכל שלב ב"שלבי הפתרון": המושגים שצריך להבין כדי לבצע אותו (ההסברים עצמם ב-concepts.py).
# STEP_CONCEPTS[סעיף][מספר השלב, מ-0] = [מושגים]. NEW_STEPS[סעיף] = [(טקסט השלב, [מושגים])] לסעיף שאין בו רשימת שלבים.

STEP_CONCEPTS = {'ex1-s1': {0: ['function', 'domainrules'], 1: ['ineq'], 2: ['intervals'], 3: ['intervals']}, 'ex1-s2': {0: ['ineq'], 1: ['factor'], 2: ['signtable'], 3: ['signtable'], 4: ['signtable', 'intervals']}, 'ex1-s3': {0: ['radians', 'trig', 'tancot'], 1: ['tancot'], 2: ['ineq']}, 'ex1-s4': {0: ['basegraphs', 'trig', 'radians'], 1: ['transform', 'factorarg'], 2: ['transform'], 3: ['basegraphs']}, 'ex1-s5': {0: ['transform', 'factorarg'], 1: ['factorarg'], 2: ['transform']}, 'ex1-s7': {0: ['function', 'parity', 'basegraphs'], 1: ['minusx'], 2: ['parity']}, 'ex1-s8': {0: ['compose', 'parity', 'minusx'], 1: ['trig', 'sincosparity'], 2: ['parity']}, 'ex1-s9': {0: ['parity'], 1: ['parity']}, 'ex1-s10': {0: ['compose'], 1: ['compose'], 2: ['expand', 'powers'], 3: ['compose']}, 'ex1-s11': {0: ['compose'], 2: ['compose', 'powers']}, 'ex1-s12': {0: ['compose', 'parity'], 1: ['parity'], 2: ['parity']}, 'ex1-s13': {1: ['compose'], 2: ['parity']}, 'ex1-s14': {0: ['model', 'compose'], 1: ['compose'], 2: ['powers']}, 'ex1-s15': {0: ['model'], 1: ['model'], 2: ['ratio']}, 'ex1-s16': {0: ['model', 'compose'], 1: ['ineq']}, 'ex1-s17': {0: ['trig', 'cosbound'], 1: ['cosbound', 'radians']}, 'ex1-s18': {0: ['factorarg', 'transform'], 2: ['trig', 'radians']}, 'ex1-s19': {0: ['domainrules', 'basegraphs', 'ineq', 'intervals'], 1: ['intervals'], 2: ['logrules'], 3: ['logrules']}, 'ex2-s1': {0: ['piecewise'], 1: ['piecewise'], 2: ['piecewise'], 3: ['dots'], 4: ['dots']}, 'ex2-s2': {0: ['abs', 'factor'], 1: ['signtable'], 2: ['abs'], 3: ['piecewise']}, 'ex2-s4': {0: ['basegraphs'], 1: ['transform', 'absgraph'], 2: ['absgraph', 'transform'], 3: ['range']}, 'ex2-s5': {0: ['floor'], 1: ['floor'], 2: ['dots']}, 'ex2-s6': {0: ['mono'], 1: ['mono'], 2: ['ineq'], 3: ['addineq']}, 'ex2-s7': {0: ['mono', 'compose'], 1: ['mono'], 2: ['mono']}, 'ex2-s8': {0: ['mono'], 1: ['mono'], 2: ['injective']}, 'ex2-s9': {0: ['trig', 'radians', 'period'], 1: ['injective', 'mono'], 2: ['range', 'onto'], 3: ['onto']}, 'ex2-s10': {0: ['counter'], 1: ['mono', 'sqineq', 'compose', 'injective'], 2: ['counter']}, 'ex2-s11': {0: ['injective', 'onto']}, 'ex2-s12': {0: ['piecewise'], 1: ['mono'], 2: ['injective'], 3: ['range', 'onto']}, 'ex2-s13': {0: ['floor'], 1: ['range'], 2: ['mono'], 3: ['floor', 'ineq']}, 'ex2-s14': {0: ['mono', 'floor', 'compose'], 2: ['injective'], 3: ['onto']}}

NEW_STEPS = {}   # all sections now have their own steps (tools/units)

# --------------------------------------------------------------- תרגילים 3-4: גבולות, רציפות, e
STEP_CONCEPTS.update({
 'ex3-s1': {0: ['limit', 'directsub'], 1: ['indet'], 2: ['indet']},
 'ex3-s2': {0: ['indet'], 1: ['cubes', 'factor'], 2: ['limit'], 3: ['directsub']},
 'ex3-s3': {0: ['conjmul'], 1: ['conjmul', 'expand'], 2: ['factor'], 3: ['directsub']},
 'ex3-s4': {0: ['onesided', 'abs'], 1: ['onesided'], 2: ['onesided']},
 'ex3-s5': {0: ['onesided', 'piecewise', 'conjmul'], 1: ['onesided'], 2: ['onesided'], 3: ['abs']},
 'ex3-s6': {0: ['kzero'], 1: ['kzero', 'abs'], 2: ['kzero']},
 'ex3-s7': {0: ['abs', 'onesided'], 1: ['abs'], 2: ['factor'], 3: ['onesided']},
 'ex3-s8': {0: ['floor', 'floorside'], 1: ['floorside'], 2: ['onesided'], 3: ['onesided']},
 'ex3-s9': {0: ['highpow'], 1: ['highpow'], 2: ['highpow'], 3: ['directsub']},
 'ex3-s10': {0: ['indet', 'conjmul'], 1: ['expand'], 2: ['highpow'], 3: ['highpow']},
 'ex3-s11': {0: ['highpow'], 1: ['sqrtabs'], 2: ['highpow']},
 'ex3-s12': {0: ['powers', 'expdom'], 1: ['expdom'], 2: ['highpow'], 3: ['expdom']},
 'ex3-s13': {0: ['indet', 'limlaws'], 1: ['counter'], 2: ['counter'], 3: ['counter']},
 'ex3-s14': {0: ['asym', 'highpow'], 1: ['asym'], 2: ['asym']},
 'ex3-s15': {0: ['indet'], 1: ['limlaws'], 2: ['indet'], 3: ['conjmul', 'highpow']},
 'ex4-s1': {0: ['tancot'], 1: ['sinlim'], 2: ['sinlim'], 3: ['directsub']},
 'ex4-s2': {0: ['tancot'], 1: ['onecos', 'pyth'], 2: ['sinlim'], 3: ['directsub']},
 'ex4-s3': {0: ['factor'], 1: ['limit'], 2: ['sinlim'], 3: ['directsub']},
 'ex4-s4': {0: ['varsub'], 1: ['varsub'], 2: ['varsub'], 3: ['sinlim']},
 'ex4-s5': {0: ['continuity', 'piecewise'], 1: ['continuity'], 2: ['onesided', 'cubes'], 3: ['continuity']},
 'ex4-s6': {0: ['contops'], 1: ['contops'], 2: ['counter'], 3: ['contops']},
 'ex4-s7': {0: ['limin', 'highpow'], 1: ['limin'], 2: ['limin']},
 'ex4-s8': {0: ['elim'], 1: ['elim'], 2: ['onepowinf'], 3: ['onepowinf']},
 'ex4-s9': {0: ['highpow'], 1: ['powinf'], 2: ['powinf']},
 'ex4-s10': {0: ['elim'], 1: ['onepowinf'], 2: ['elim'], 3: ['sinlim']},
 'ex4-s11': {0: ['continuity'], 1: ['onesided'], 2: ['disctypes'], 3: ['removable']},
 'ex4-s12': {0: ['onesided', 'conjmul'], 1: ['continuity'], 2: ['disctypes']},
 'ex4-s13': {0: ['avgcost'], 1: ['conjmul'], 2: ['disctypes'], 3: ['removable'], 4: ['avgcost']},
 'ex4-s14': {0: ['indet'], 1: ['onepowinf'], 2: ['elim'], 3: ['asym']},
 'ex4-s15': {0: ['composecont'], 1: ['composecont'], 2: ['counter'], 3: ['continuity']},
})

# --------------------------------------------------------------- יחידות 1-2 במבנה החדש (שלב = הסבר + דוגמה + תרשים)
STEP_CONCEPTS.update({
 'ex1-s1': {0: ['function', 'domainrules'], 1: ['domainrules'], 2: ['ineq'], 3: ['intervals'], 4: ['intervals', 'abs', 'factor']},
 'ex1-s2': {0: ['ineq'], 1: ['factor'], 2: ['signtable'], 3: ['signtable'], 4: ['intervals']},
 'ex1-s3': {0: ['radians', 'trig', 'tancot'], 1: ['tancot'], 2: ['tancot'], 3: ['ineq'], 4: ['intervals']},
 'ex1-s4': {0: ['basegraphs', 'trig'], 1: ['transform'], 2: ['transform'], 3: ['basegraphs']},
 'ex1-s5': {0: ['factorarg'], 1: ['factorarg', 'transform'], 2: ['transform']},
 'ex1-s6': {0: ['period', 'radians'], 1: ['range', 'ineq', 'cosbound'], 2: ['basegraphs', 'domainrules']},
 'ex1-s7': {0: ['function', 'parity'], 1: ['minusx'], 2: ['parity']},
 'ex1-s8': {0: ['parity'], 1: ['sincosparity'], 2: ['compose', 'parity']},
 'ex1-s9': {0: ['parity'], 1: ['parity'], 2: ['parity'], 3: ['parity']},
 'ex1-s10': {0: ['compose'], 1: ['compose'], 2: ['compose'], 3: ['expand', 'powers'], 4: ['compose']},
 'ex1-s11': {0: ['compose'], 1: ['compose'], 2: ['compose'], 3: ['compose']},
 'ex1-s12': {0: ['compose', 'parity'], 1: ['parity'], 2: ['parity'], 3: ['parity']},
 'ex1-s13': {1: ['compose'], 2: ['parity']},
 'ex1-s14': {0: ['model', 'compose'], 1: ['compose'], 2: ['powers'], 3: ['model']},
 'ex1-s15': {0: ['model'], 1: ['model'], 2: ['ratio'], 3: ['model']},
 'ex1-s16': {0: ['model', 'compose'], 1: ['ineq'], 3: ['compose']},
 'ex1-s17': {0: ['trig', 'cosbound'], 1: ['cosbound', 'radians'], 2: ['cosbound']},
 'ex1-s18': {0: ['factorarg', 'transform'], 1: ['transform'], 2: ['trig', 'radians']},
 'ex1-s19': {0: ['domainrules', 'basegraphs', 'ineq', 'intervals'], 1: ['logrules'], 2: ['logrules'], 3: ['intervals']},
 'ex2-s1': {0: ['piecewise'], 1: ['piecewise'], 2: ['piecewise'], 3: ['dots'], 4: ['dots']},
 'ex2-s2': {0: ['abs', 'factor'], 1: ['signtable'], 2: ['abs'], 3: ['piecewise']},
 'ex2-s3': {0: ['abs'], 1: ['absgraph', 'basegraphs'], 2: ['absgraph'], 3: ['transform']},
 'ex2-s4': {0: ['basegraphs'], 1: ['transform', 'absgraph'], 2: ['absgraph'], 3: ['range']},
 'ex2-s5': {0: ['floor'], 1: ['floor'], 2: ['floor'], 3: ['dots']},
 'ex2-s6': {0: ['mono'], 1: ['mono'], 2: ['ineq'], 3: ['addineq']},
 'ex2-s7': {0: ['mono'], 1: ['mono', 'compose'], 2: ['mono'], 3: ['mono']},
 'ex2-s8': {0: ['mono'], 1: ['mono'], 2: ['injective'], 3: ['counter', 'piecewise']},
 'ex2-s9': {0: ['trig', 'radians', 'period'], 1: ['injective', 'mono'], 2: ['range', 'onto'], 3: ['onto']},
 'ex2-s10': {0: ['counter'], 1: ['mono', 'sqineq', 'compose', 'injective'], 2: ['counter']},
 'ex2-s11': {0: ['injective', 'onto'], 1: ['injective', 'onto']},
 'ex2-s12': {0: ['piecewise'], 1: ['mono'], 2: ['injective'], 3: ['range', 'onto']},
 'ex2-s13': {0: ['floor'], 1: ['range'], 2: ['mono'], 3: ['floor', 'ineq']},
 'ex2-s14': {0: ['mono', 'floor', 'compose'], 2: ['injective'], 3: ['onto']},
})
