# -*- coding: utf-8 -*-
# לכל שלב ב"שלבי הפתרון": המושגים שצריך להבין כדי לבצע אותו (ההסברים עצמם ב-concepts.py).
# STEP_CONCEPTS[סעיף][מספר השלב, מ-0] = [מושגים]. השלבים עצמם ב-tools/units/algebra_solutions_u.py.

STEP_CONCEPTS = {
'ex1-s1': {0: ['i', 'complex', 'plane'], 1: ['conj'], 2: ['modulus'], 3: ['zzbar', 'expand'], 4: ['equal']},
'ex1-s2': {0: ['expand', 'i'], 1: ['i'], 2: ['expand'], 3: ['complex']},
'ex1-s3': {0: ['expand', 'i'], 1: ['conj', 'division'], 2: ['zzbar'], 3: ['expand', 'complex'], 4: ['division', 'conjrules']},
'ex1-s4': {0: ['i', 'ipow'], 1: ['ipow', 'powers'], 2: ['division'], 3: ['ipow']},
'ex1-s5': {0: ['division'], 1: ['expand', 'i'], 2: ['equal'], 3: ['system']},
'ex1-s6': {0: ['complex', 'conj'], 1: ['expand'], 2: ['equal', 'system'], 3: ['equal']},
'ex1-s7': {0: ['modulus'], 1: ['modrules'], 2: ['modulus'], 4: ['modrules']},
'ex1-s8': {0: ['realimag'], 1: ['conjrules'], 2: ['expand'], 3: ['zzbar'], 4: ['realimag']},
'ex1-s9': {0: ['modulus', 'plane'], 2: ['zzbar'], 3: ['expand'], 4: ['realimag']},
'ex1-s10': {0: ['modrules'], 1: ['zzbar', 'euler'], 2: ['euler', 'trig'], 3: ['realimag', 'conjrules']},
'ex1-s11': {0: ['complex', 'plane'], 1: ['modulus'], 2: ['powers', 'i']},
'ex1-s12': {0: ['quadrant'], 1: ['modulus'], 2: ['radians', 'trig'], 3: ['argument'], 4: ['polar', 'euler']},
'ex1-s13': {0: ['polar'], 1: ['demoivre'], 2: ['fullturn'], 3: ['trig']},
'ex1-s14': {0: ['euler', 'demoivre'], 1: ['binom3', 'ipow'], 2: ['equal'], 3: ['pyth']},
'ex2-s1': {0: ['polar', 'argument'], 1: ['demoivre'], 2: ['polareq', 'fullturn'], 3: ['roots'], 4: ['roots']},
'ex2-s2': {1: ['zeroprod'], 2: ['division', 'polar'], 3: ['roots']},
'ex2-s3': {0: ['division'], 1: ['polar', 'euler'], 2: ['polarmult'], 3: ['roots']},
'ex2-s4': {0: ['substitution'], 1: ['roots'], 3: ['division']},
'ex2-s5': {0: ['polar', 'demoivre'], 1: ['conj', 'polarmult'], 2: ['polarmult'], 3: ['roots']},
'ex2-s6': {0: ['quadform'], 1: ['negdelta', 'i'], 2: ['conj']},
'ex2-s7': {0: ['polyroot', 'powers'], 1: ['polyroot'], 2: ['conjroot'], 3: ['conjroot', 'modulus'], 4: ['longdiv', 'quadform']},
'ex2-s8': {0: ['roots', 'zzbar'], 1: ['realimag', 'conjrules'], 2: ['expand'], 3: ['zzbar']},
}

NEW_STEPS = {}
