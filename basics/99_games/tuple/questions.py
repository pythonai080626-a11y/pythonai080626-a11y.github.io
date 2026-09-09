# -*- coding: utf-8 -*-
"""
questions.py  --  Lesson 19 (Tuples) quiz bank.

Twenty questions, taken straight off the topic page 23_tuples/index.html:
the comma that makes a tuple, packing and unpacking, star unpacking, indexing
and slicing, count / index, + and *, the built-ins, and immutability.

Two kinds of question live in here:

    'choice'  (19 of them)  four options, exactly one right
              -> 'options' is a dict 'a'/'b'/'c'/'d', 'correct' holds the letter

    'type'    (the last one) no options at all - the student TYPES python
              -> 'expect'  what has to come back, in words, for the feedback
              -> 'answer'  the value their line must evaluate to
              -> 'want_type' the type it must be, so (7) cannot pass for (7,)

              The checker evaluates what they typed and compares the VALUE.
              Any spelling of the right answer passes: (7,) / 7, / ( 7 , )
              / tuple([7]) are all the same tuple, so all four count.

Every question also carries 'why' - one line the student sees after answering,
right or wrong.
"""

QUESTIONS = {

    # ---------------------------------------------- immutability, up front --
    1: {
        'kind': 'choice',
        'q': "t = (1, 2, 3)\nt[0] = 99\nWhat happens?",
        'options': {
            'a': "t becomes (99, 2, 3)",
            'b': "Nothing - the line is ignored",
            'c': "t becomes (1, 2, 3, 99)",
            'd': "TypeError: 'tuple' object does not support item assignment",
        },
        'correct': 'd',
        'why': "A tuple cannot be changed. Not one item, not ever - that is the whole deal.",
    },
    2: {
        'kind': 'choice',
        'q': "x = (42)\nprint(type(x))",
        'options': {
            'a': "<class 'tuple'>",
            'b': "<class 'list'>",
            'c': "<class 'int'>",
            'd': "SyntaxError",
        },
        'correct': 'c',
        'why': "The COMMA makes a tuple, not the brackets. (42) is just 42 in brackets.",
    },
    3: {
        'kind': 'choice',
        'q': "point = 10, 20, 30      # no brackets at all\nprint(point)",
        'options': {
            'a': "10 20 30",
            'b': "(10, 20, 30)",
            'c': "[10, 20, 30]",
            'd': "SyntaxError: missing brackets",
        },
        'correct': 'b',
        'why': "Packing. The commas alone build the tuple - Python adds the brackets when it prints.",
    },

    # ------------------------------------------------ packing / unpacking --
    4: {
        'kind': 'choice',
        'q': "colours = ('red', 'green', 'blue')\nx, y, z = colours\nprint(y)",
        'options': {
            'a': "green",
            'b': "red",
            'c': "('green',)",
            'd': "ValueError: too many values to unpack",
        },
        'correct': 'a',
        'why': "Unpacking hands out the items left to right: x=red, y=green, z=blue.",
    },
    5: {
        'kind': 'choice',
        'q': "a, b = 1, 2\na, b = b, a\nprint(a, b)",
        'options': {
            'a': "1 2",
            'b': "1 1",
            'c': "2 2",
            'd': "2 1",
        },
        'correct': 'd',
        'why': "The right side is packed into (2, 1) FIRST, then unpacked - so no temp variable is needed.",
    },
    6: {
        'kind': 'choice',
        'q': "t = (1, 2, 3, 4, 5)\nfirst, *rest = t\nprint(rest)",
        'options': {
            'a': "(2, 3, 4, 5)",
            'b': "[2, 3, 4, 5]",
            'c': "2",
            'd': "(1, 2, 3, 4, 5)",
        },
        'correct': 'b',
        'why': "The * collects the rest into a LIST, with square brackets - never a tuple.",
    },

    # -------------------------------------------------- index and slicing --
    7: {
        'kind': 'choice',
        'q': "t = (0, 1, 2, 3, 4, 5)\nprint(t[1:4])",
        'options': {
            'a': "(1, 2, 3, 4)",
            'b': "(1, 2, 3)",
            'c': "[1, 2, 3]",
            'd': "(0, 1, 2, 3)",
        },
        'correct': 'b',
        'why': "A slice stops BEFORE the second number, and a slice of a tuple is a new tuple.",
    },
    8: {
        'kind': 'choice',
        'q': "t = (0, 1, 2, 3, 4, 5)\nprint(t[::-1])",
        'options': {
            'a': "(5, 4, 3, 2, 1, 0)",
            'b': "(0, 1, 2, 3, 4, 5)",
            'c': "[5, 4, 3, 2, 1, 0]",
            'd': "(0, 2, 4)",
        },
        'correct': 'a',
        'why': "Step -1 walks it backwards. The original t is untouched - this is a brand new tuple.",
    },
    9: {
        'kind': 'choice',
        'q': "t = (3, 1, 4, 1, 5, 9)\nprint(len(t), min(t), max(t), sum(t))",
        'options': {
            'a': "6 1 9 23",
            'b': "6 3 9 23",
            'c': "5 1 9 23",
            'd': "6 1 9 22",
        },
        'correct': 'a',
        'why': "Six items, smallest 1, biggest 9, and they add up to 23. All four work on a tuple.",
    },
    10: {
        'kind': 'choice',
        'q': "t = ('apple', 'banana', 'cherry')\nprint(t[-1], 'mango' not in t)",
        'options': {
            'a': "apple True",
            'b': "cherry False",
            'c': "cherry True",
            'd': "('cherry',) True",
        },
        'correct': 'c',
        'why': "-1 is the last item, and mango really is not in there, so 'not in' is True.",
    },

    # --------------------------------------------------- the two methods --
    11: {
        'kind': 'choice',
        'q': "t = (1, 2, 2, 3, 2, 4, 2)\nprint(t.count(2))",
        'options': {
            'a': "2",
            'b': "3",
            'c': "4",
            'd': "7",
        },
        'correct': 'c',
        'why': "count() answers HOW MANY, not where. The 2 shows up four times.",
    },
    12: {
        'kind': 'choice',
        'q': "t = ('cat', 'dog', 'bird', 'dog')\nprint(t.index('dog'))",
        'options': {
            'a': "1",
            'b': "3",
            'c': "2",
            'd': "(1, 3)",
        },
        'correct': 'a',
        'why': "index() gives the FIRST place it found it, and stops looking. The second dog is ignored.",
    },

    # ------------------------------------------------ building new tuples --
    13: {
        'kind': 'choice',
        'q': "a = (1, 2, 3)\nb = (4, 6, 1)\nprint(a + b)",
        'options': {
            'a': "(5, 8, 4)",
            'b': "TypeError: cannot add tuples",
            'c': "[1, 2, 3, 4, 6, 1]",
            'd': "(1, 2, 3, 4, 6, 1)",
        },
        'correct': 'd',
        'why': "+ glues them into a NEW tuple. a and b are both still exactly as they were.",
    },
    14: {
        'kind': 'choice',
        'q': "t = (1, 2)\nprint(t * 3)",
        'options': {
            'a': "(3, 6)",
            'b': "(1, 2, 3)",
            'c': "(1, 2, 1, 2, 1, 2)",
            'd': "((1, 2), (1, 2), (1, 2))",
        },
        'correct': 'c',
        'why': "* repeats the CONTENTS end to end - it does not multiply the numbers or nest anything.",
    },
    15: {
        'kind': 'choice',
        'q': "t = (3, 1, 4, 1, 5, 9)\nprint(sorted(t))",
        'options': {
            'a': "(1, 1, 3, 4, 5, 9)",
            'b': "[1, 1, 3, 4, 5, 9]",
            'c': "(9, 5, 4, 3, 1, 1)",
            'd': "AttributeError: 'tuple' object has no attribute 'sort'",
        },
        'correct': 'b',
        'why': "sorted() always hands back a LIST, whatever went in. Want a tuple? tuple(sorted(t)).",
    },
    16: {
        'kind': 'choice',
        'q': "t = (1, 2, 3)\nt.append(4)\nWhat happens?",
        'options': {
            'a': "AttributeError: 'tuple' object has no attribute 'append'",
            'b': "t becomes (1, 2, 3, 4)",
            'c': "It returns a new tuple (1, 2, 3, 4)",
            'd': "TypeError: append() takes no arguments",
        },
        'correct': 'a',
        'why': "append does not exist on a tuple. Nor do remove, sort, clear - everything that changes is gone.",
    },

    # --------------------------------------------- why the lock is useful --
    17: {
        'kind': 'choice',
        'q': "Which one of these lines RUNS without an error?",
        'options': {
            'a': "d = {[1, 2]: 'a'}",
            'b': "d = {{1, 2}: 'a'}",
            'c': "d = {(1, 2): 'a'}",
            'd': "d = {{'x': 1}: 'a'}",
        },
        'correct': 'c',
        'why': "A dict key must be unchangeable. A tuple qualifies; a list, a set and a dict do not.",
    },
    18: {
        'kind': 'choice',
        'q': "t = (1, 2, 3)\nlst = list(t)\nlst[0] = 99\nt = tuple(lst)\nprint(t)",
        'options': {
            'a': "TypeError - you still cannot change a tuple",
            'b': "(1, 2, 3)",
            'c': "[99, 2, 3]",
            'd': "(99, 2, 3)",
        },
        'correct': 'd',
        'why': "Nothing was changed - a list was built, edited, and locked again. t just points somewhere new.",
    },
    19: {
        'kind': 'choice',
        'q': "a = [1, 2]\ntup = (a, 12)\na.clear()\nprint(tup)",
        'options': {
            'a': "([1, 2], 12)",
            'b': "([], 12)",
            'c': "TypeError: tuple is immutable",
            'd': "(12,)",
        },
        'correct': 'b',
        'why': "The tuple still holds the same two items - but that list emptied itself, and the tuple has no say.",
    },

    # ------------------------------------------------- type it yourself --
    20: {
        'kind': 'type',
        'q': "Last one, and you TYPE this one - no options.\n"
             "\n"
             "Write a tuple that holds exactly ONE item: the number 7.",
        'expect': "a tuple of length 1 holding 7  ->  (7,)",
        'answer': (7,),
        'want_type': 'tuple',
        'why': "The trailing comma is the whole tuple. (7) is just the number 7 in brackets - "
               "(7,) is a tuple with one item in it.",
    },
}
