# -*- coding: utf-8 -*-
# לכל שלב ב"שלבי הפתרון": המושגים שצריך להבין כדי לבצע אותו (ההסברים עצמם ב-concepts.py).
# STEP_CONCEPTS[סעיף][מספר השלב, מ-0] = [מושגים]. השלבים עצמם - ב-tools/units/algebra_theory_u.py.

STEP_CONCEPTS = {
 'ex1-s1': {0: ['i', 'complex'], 1: ['plane'], 3: ['ipow']},
 'ex1-s2': {0: ['arith'], 1: ['expand'], 2: ['conj', 'division'], 3: ['zzbar']},
 'ex1-s3': {0: ['conj'], 1: ['conjrules'], 3: ['realimag'], 4: ['zzbar', 'modulus']},
 'ex1-s4': {0: ['modulus'], 1: ['pyth'], 2: ['modrules'], 3: ['zzbar'], 4: ['equal']},
 'ex1-s5': {0: ['radians', 'trig'], 2: ['pyth'], 3: ['quadrant']},
 'ex1-s6': {0: ['modulus'], 1: ['trig', 'argument'], 2: ['quadrant'], 3: ['polar', 'euler']},
 'ex1-s7': {0: ['polar'], 1: ['polarmult'], 3: ['trig']},
 'ex1-s8': {0: ['polar', 'euler'], 1: ['demoivre'], 2: ['fullturn'], 3: ['trig']},
 'ex1-s9': {0: ['polar'], 1: ['demoivre'], 2: ['polareq'], 3: ['roots', 'fullturn']},
 'ex1-s10': {0: ['quadform', 'delta'], 1: ['negdelta'], 2: ['conjroot'], 3: ['polyroot'], 4: ['longdiv']},
 'ex1-s11': {0: ['quadform'], 1: ['equal'], 2: ['modulus', 'modrules'], 3: ['system']},
 'ex2-s1': {0: ['matrix'], 1: ['aij'], 3: ['mateq']},
 'ex2-s2': {0: ['special']},
 'ex2-s3': {0: ['matadd']},
 'ex2-s4': {0: ['matmul']},
 'ex2-s5': {0: ['lincomb'], 1: ['matadd'], 2: ['mateq'], 3: ['system']},
 'ex2-s6': {0: ['transpose'], 1: ['symmetric']},
 'ex2-s7': {0: ['trace']},
}

NEW_STEPS = {}
