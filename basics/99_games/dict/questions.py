# -*- coding: utf-8 -*-
"""
questions.py  --  Lesson 16 (Dictionaries) quiz bank.

EVERYTHING here is a dict. No lists are used to hold the quiz:
    QUESTIONS       -> dict   number  ->  question-dict
    every question  -> dict   'q' / 'options' / 'correct' / 'why'
    every 'options' -> dict   'a' / 'b' / 'c' / 'd'  ->  text
Only ONE option is correct, and 'correct' holds its letter.
"""

QUESTIONS = {
    1: {
        'q': "empty = {}\nWhat does print(type(empty)) show?",
        'options': {
            'a': "<class 'set'>",
            'b': "<class 'dict'>",
            'c': "<class 'list'>",
            'd': "<class 'tuple'>",
        },
        'correct': 'b',
        'why': "The dict got the braces first. An empty SET must be written set().",
    },
    2: {
        'q': "prices = {'mango': 14, 'mango': 31}\nprint(prices)",
        'options': {
            'a': "{'mango': 14}",
            'b': "{'mango': 14, 'mango': 31}",
            'c': "{'mango': 31}",
            'd': "SyntaxError: duplicate key",
        },
        'correct': 'c',
        'why': "Keys are unique - the LAST one quietly wins. No error, no warning.",
    },
    3: {
        'q': "Which one of these is allowed to be a dict KEY?",
        'options': {
            'a': "['owl', 'fox']",
            'b': "{'owl', 'fox'}",
            'c': "{'owl': 1}",
            'd': "('owl', 'fox')",
        },
        'correct': 'd',
        'why': "A key must be hashable = immutable. str/int/tuple/frozenset yes; list/set/dict no.",
    },
    4: {
        'q': "box = {[2, 4]: 'oops'}\nWhat happens?",
        'options': {
            'a': "TypeError: unhashable type: 'list'",
            'b': "It works, the key is the list [2, 4]",
            'c': "KeyError: [2, 4]",
            'd': "The list is turned into a tuple automatically",
        },
        'correct': 'a',
        'why': "A list can change, so its hash would go stale. Python refuses it as a key.",
    },
    5: {
        'q': "pet = {'kind': 'parrot', 'age': 6}\nprint(pet['color'])",
        'options': {
            'a': "It prints None",
            'b': "KeyError: 'color'",
            'c': "It prints an empty line",
            'd': "IndexError: out of range",
        },
        'correct': 'b',
        'why': "Square brackets CRASH on a missing key. Use .get() when the key may be absent.",
    },
    6: {
        'q': "pet = {'kind': 'parrot', 'age': 6}\nprint(pet.get('color', 'unpainted'))",
        'options': {
            'a': "None",
            'b': "KeyError: 'color'",
            'c': "unpainted",
            'd': "color",
        },
        'correct': 'c',
        'why': "The 2nd argument of .get() is YOUR default, handed back when the key is missing.",
    },
    7: {
        'q': "pet = {'kind': 'parrot'}\nprint(pet.get('age'))      # no default given",
        'options': {
            'a': "None",
            'b': "0",
            'c': "'' (an empty string)",
            'd': "KeyError: 'age'",
        },
        'correct': 'a',
        'why': ".get() never crashes. With no second argument it hands back None.",
    },
    8: {
        'q': "shelf = {'lychee': 8, 'papaya': 2}\nfor thing in shelf:\n    print(thing)",
        'options': {
            'a': "8 then 2",
            'b': "lychee then papaya",
            'c': "('lychee', 8) then ('papaya', 2)",
            'd': "lychee 8 then papaya 2",
        },
        'correct': 'b',
        'why': "Looping a dict walks the KEYS only - not the values, not the pairs.",
    },
    9: {
        'q': "Which loop hands you the key AND the value on every turn?",
        'options': {
            'a': "for k, v in shelf:",
            'b': "for k, v in shelf.keys():",
            'c': "for k, v in shelf.items():",
            'd': "for k, v in shelf.values():",
        },
        'correct': 'c',
        'why': ".items() gives you both halves of the pair at once.",
    },
    10: {
        'q': "shelf = {'lychee': 8, 'papaya': 2}\nprint(8 in shelf)",
        'options': {
            'a': "True - 8 is sitting right there",
            'b': "False - 'in' looks at KEYS only",
            'c': "TypeError",
            'd': "None",
        },
        'correct': 'b',
        'why': "'in' asks about keys. For values you must write:  8 in shelf.values()",
    },
    11: {
        'q': "card = {'holder': 'Yarden'}\ncard['city'] = 'Ashdod'\nWhat did that second line do?",
        'options': {
            'a': "Crashed - 'city' does not exist yet",
            'b': "Replaced the value of 'holder'",
            'c': "Added a new pair 'city': 'Ashdod'",
            'd': "Nothing - you need .append() to add",
        },
        'correct': 'c',
        'why': "upsert = update + insert. One line adds a missing key or overwrites an existing one.",
    },
    12: {
        'q': "card = {'holder': 'Yarden', 'city': 'Ashdod'}\ncard['holder'] = 'Roni'\nprint(card)",
        'options': {
            'a': "{'city': 'Ashdod', 'holder': 'Roni'}",
            'b': "{'holder': 'Yarden', 'city': 'Ashdod', 'holder': 'Roni'}",
            'c': "{'holder': 'Roni', 'city': 'Ashdod'}",
            'd': "{'holder': 'Roni'}",
        },
        'correct': 'c',
        'why': "Overwriting a value does NOT move the key - a dict keeps insertion order.",
    },
    13: {
        'q': "card = {'holder': 'Roni', 'zone': 4}\ncard.update({'zone': 9, 'level': 2})\nprint(card)",
        'options': {
            'a': "{'holder': 'Roni', 'zone': 9, 'level': 2}",
            'b': "{'holder': 'Roni', 'zone': 4, 'level': 2}",
            'c': "{'zone': 9, 'level': 2}",
            'd': "{'holder': 'Roni', 'zone': 4, 'zone': 9, 'level': 2}",
        },
        'correct': 'a',
        'why': ".update() is upsert on every pair: 'zone' was overwritten, 'level' was added at the end.",
    },
    14: {
        'q': "names = ['teal', 'amber', 'plum', 'olive', 'coral']\ncodes = ['#008080', '#ffbf00', '#8e4585']\nprint(len(dict(zip(names, codes))))",
        'options': {
            'a': "5",
            'b': "3",
            'c': "8",
            'd': "TypeError - the lists are not the same length",
        },
        'correct': 'b',
        'why': "zip stops at the SHORTER side. 'olive' and 'coral' are dropped without a word.",
    },
    15: {
        'q': "blank = dict.fromkeys(['owl', 'camel', 'newt'], 0)\nprint(blank)",
        'options': {
            'a': "{'owl': None, 'camel': None, 'newt': None}",
            'b': "{0: 'owl', 0: 'camel', 0: 'newt'}",
            'c': "{'owl': 0, 'camel': 0, 'newt': 0}",
            'd': "{'owl', 'camel', 'newt'}",
        },
        'correct': 'c',
        'why': "fromkeys builds a blank form - every key starts with the SAME value you passed.",
    },
    16: {
        'q': "tools = ['drill', 'saw', 'plier']\nsizes = {t: len(t) for t in tools}\nprint(sizes)",
        'options': {
            'a': "{'drill', 'saw', 'plier'}",
            'b': "{'drill': 5, 'saw': 3, 'plier': 5}",
            'c': "{5: 'drill', 3: 'saw', 5: 'plier'}",
            'd': "{'drill': 'drill', 'saw': 'saw', 'plier': 'plier'}",
        },
        'correct': 'b',
        'why': "The colon is the whole difference: {t for ...} builds a set, {t: len(t) for ...} builds a dict.",
    },
    17: {
        'q': "pupil = {'who': 'Shira',\n         'home': {'town': 'Modiin', 'floor': 3},\n         'clubs': ['chess', 'choir', 'judo']}\nprint(pupil['home']['floor'], pupil['clubs'][-1])",
        'options': {
            'a': "3 judo",
            'b': "3 chess",
            'c': "floor judo",
            'd': "TypeError: you cannot chain brackets",
        },
        'correct': 'a',
        'why': "One bracket per step down: ['home'] gives back a dict, ['clubs'] gives back a list.",
    },
    18: {
        'q': "pupil = {'who': 'Shira', 'home': {'town': 'Modiin', 'floor': 3}}\nprint(len(pupil))",
        'options': {
            'a': "2",
            'b': "3",
            'c': "4",
            'd': "1",
        },
        'correct': 'a',
        'why': "len() counts the pairs on the top level - the nested dict is one single value.",
    },
    19: {
        'q': "Which line builds {'town': 'Eilat', 'zone': 9} correctly?",
        'options': {
            'a': "dict('town'='Eilat', 'zone'=9)",
            'b': "dict(town='Eilat', zone=9)",
            'c': "dict[town='Eilat', zone=9]",
            'd': "dict{'town': 'Eilat', 'zone': 9}",
        },
        'correct': 'b',
        'why': "With dict() the keys are written like variable names - no quotes - and Python makes them strings.",
    },
    20: {
        'q': "stock = {'bolt': 40, 'nut': 25}\nprint(stock.keys())",
        'options': {
            'a': "['bolt', 'nut']",
            'b': "{'bolt', 'nut'}",
            'c': "dict_keys(['bolt', 'nut'])",
            'd': "('bolt', 'nut')",
        },
        'correct': 'c',
        'why': ".keys() is a live VIEW, not a list. Wrap it in list(...) when you need to index or sort it.",
    },
}
