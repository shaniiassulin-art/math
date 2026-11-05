# -*- coding: utf-8 -*-
# לכל שלב ב"שלבי הפתרון": המושגים שצריך להבין כדי לבצע אותו (ההסברים עצמם ב-concepts.py).
# STEP_CONCEPTS[סעיף][מספר השלב, מ-0] = [מושגים].  המפתח -1: מושגים שהסעיף עצמו מגדיר בתיבת ההגדרה 📘.
# בפעם הראשונה באתר - ההסבר משולב בשלב; אחר כך - כפתור "מה צריך לדעת" עם קישור לסעיף שבו הוסבר.

STEP_CONCEPTS = {
 'ex1-s1': {-1: ['i', 'complex', 'plane'], 3: ['ipow']},
 'ex1-s2': {-1: ['arith', 'division'], 1: ['expand'], 2: ['conj']},
 'ex1-s3': {-1: ['conj', 'conjrules', 'realimag'], 4: ['zzbar']},
 'ex1-s4': {-1: ['modulus', 'modrules', 'zzbar'], 1: ['pyth'], 4: ['equal']},
 'ex1-s5': {-1: ['trig', 'pyth'], 0: ['radians'], 3: ['quadrant']},
 'ex1-s6': {-1: ['polar', 'euler', 'argument', 'polareq'], 0: ['modulus'], 1: ['trig'], 2: ['quadrant']},
 'ex1-s7': {-1: ['polarmult'], 0: ['polar'], 3: ['trig']},
 'ex1-s8': {-1: ['demoivre'], 0: ['polar'], 2: ['fullturn'], 3: ['trig']},
 'ex1-s9': {-1: ['roots'], 0: ['polar'], 1: ['demoivre'], 2: ['polareq'], 3: ['fullturn']},
 'ex1-s10': {-1: ['negdelta', 'conjroot'], 0: ['quadform'], 3: ['polyroot'], 4: ['longdiv']},
 'ex1-s11': {-1: ['delta'], 0: ['quadform'], 1: ['equal'], 2: ['modrules'], 3: ['system']},
 'ex2-s1': {-1: ['matrix', 'aij', 'mateq']},
 'ex2-s2': {-1: ['special']},
 'ex2-s3': {-1: ['matadd']},
 'ex2-s4': {-1: ['matmul']},
 'ex2-s5': {-1: ['lincomb'], 1: ['matadd'], 2: ['mateq'], 3: ['system']},
 'ex2-s6': {-1: ['transpose', 'symmetric']},
 'ex2-s7': {-1: ['trace'], 2: ['transpose']},
}

NEW_STEPS = {}
