# -*- coding: utf-8 -*-
"""
questions.py  --  Lesson 20 (try / except / else / finally) quiz bank.

Fifteen multiple-choice questions, from lesson 20 and from the topic page
24_try_except/index.html.

THE SHAPE OF A QUESTION - please keep to it:

    the python code comes FIRST, on its own lines,
    then a BLANK LINE,
    then the question itself, in HEBREW, on its own line.

    Never a sentence and a line of code on the same line - it is unreadable.
    The code stays English. The four options stay English. Only the question
    and the 'why' are in Hebrew, because this is a beginners' class.

Every question is the same shape:
    'kind'     always 'choice' - four options, exactly one right
    'q'        code, blank line, then the question in Hebrew
    'options'  a dict 'a'/'b'/'c'/'d' -> the text, in English
    'correct'  the letter that is right
    'why'      one line in Hebrew, shown afterwards whether they got it or not

Every answer in here was produced by actually running the snippet.
"""

QUESTIONS = {

    # ------------------------------------------------ input and int --
    1: {
        'kind': 'choice',
        'q': "x = int(input('Enter a number? '))\n"
             "print(x)\n"
             "\n"
             "המשתמש הקליד 10\n"
             "מה יקרה?",
        'options': {
            'a': "x is the string '10'",
            'b': "ValueError - input() always gives text",
            'c': "x is None until you print it",
            'd': "x is the number 10, and the program carries on",
        },
        'correct': 'd',
        'why': "input מחזיר תמיד מחרוזת, "
               "ו-int() הופך אותה למספר. "
               "'10' זה טקסט, 10 זה מספר.",
    },

    # ------------------------------------------- which error is which --
    2: {
        'kind': 'choice',
        'q': "print(10 / 0)\n"
             "\n"
             "איזו שגיאה תיזרק?",
        'options': {
            'a': "ValueError",
            'b': "TypeError",
            'c': "ZeroDivisionError",
            'd': "ArithmeticError: cannot divide",
        },
        'correct': 'c',
        'why': "חלוקה באפס. יש לה סוג "
               "שגיאה משלה, וזה השם "
               "שבו תופסים אותה.",
    },
    3: {
        'kind': 'choice',
        'q': "prices = {'apple': 12}\n"
             "print(prices['mango'])\n"
             "\n"
             "מה קורה?",
        'options': {
            'a': "It prints None",
            'b': "IndexError: out of range",
            'c': "It prints nothing",
            'd': "KeyError: 'mango'",
        },
        'correct': 'd',
        'why': "סוגריים מרובעים "
               "קורסים על מפתח שלא "
               "קיים. בדיוק מזה .get() מגן.",
    },
    4: {
        'kind': 'choice',
        'q': "fruits = ['apple', 'banana']\n"
             "fruits.remove('orange')\n"
             "\n"
             "מה קורה?",
        'options': {
            'a': "ValueError: list.remove(x): x not in list",
            'b': "KeyError: 'orange'",
            'c': "Nothing - the list is left alone",
            'd': "IndexError: list index out of range",
        },
        'correct': 'a',
        'why': "אי אפשר למחוק משהו "
               "שלא היה שם. בדקו עם "
               "'orange' in fruits, או תפסו את ה-ValueError.",
    },
    5: {
        'kind': 'choice',
        'q': "def my_div(a, b):\n"
             "    if b == 0:\n"
             "        raise ZeroDivisionError('b is zero')\n"
             "    return a / b\n"
             "\n"
             "מי זרק את השגיאה?",
        'options': {
            'a': "Python did, because b was zero",
            'b': "Nobody - raise only prints a warning",
            'c': "You did - raise throws an error on purpose",
            'd': "SyntaxError - you cannot raise a built-in error",
        },
        'correct': 'c',
        'why': "שתי דרכים שבהן שגיאה "
               "מתחילה: פייתון מחליט, "
               "או שאתם מחליטים עם raise. "
               "המחרוזת בסוגריים "
               "היא ההודעה.",
    },
    6: {
        'kind': 'choice',
        'q': "print('5' + 3)\n"
             "\n"
             "מה יקרה?",
        'options': {
            'a': "53",
            'b': "8",
            'c': "TypeError: can only concatenate str (not \"int\") to str",
            'd': "ValueError: cannot add",
        },
        'correct': 'c',
        'why': "טיפוס לא נכון לגמרי, "
               "ולכן TypeError. ValueError היא הטיפוס "
               "הנכון עם ערך שאי אפשר "
               "להשתמש בו.",
    },

    # ----------------------------------------------- try / except --
    7: {
        'kind': 'choice',
        'q': "try:\n"
             "    number = int(input('Enter: '))\n"
             "except ValueError:\n"
             "    print('not a number')\n"
             "\n"
             "print('Goodbye')\n"
             "\n"
             "המשתמש הקליד abc\n"
             "מה יופיע על המסך?",
        'options': {
            'a': "not a number   (and nothing else)",
            'b': "a red traceback, and Goodbye never prints",
            'c': "not a number\nGoodbye",
            'd': "Goodbye   (and nothing else)",
        },
        'correct': 'c',
        'why': "זו כל הנקודה: "
               "התוכנית לא מתה, "
               "ולכן היא המשיכה "
               "לשורה הבאה.",
    },
    8: {
        'kind': 'choice',
        'q': "try:\n"
             "    number = int('12')\n"
             "    print('got it')\n"
             "except ValueError:\n"
             "    print('not a number')\n"
             "\n"
             "מה יודפס?",
        'options': {
            'a': "got it",
            'b': "got it\nnot a number",
            'c': "not a number",
            'd': "nothing at all",
        },
        'correct': 'a',
        'why': "שום דבר לא נשבר, "
               "ולכן בלוק ה-except לא רץ "
               "בכלל. הוא רשת, לא שלב.",
    },

    # ------------------------------------------ several except blocks --
    9: {
        'kind': 'choice',
        'q': "try:\n"
             "    1 / 0\n"
             "except Exception:\n"
             "    print('something broke')\n"
             "except ZeroDivisionError:\n"
             "    print('divided by zero')\n"
             "\n"
             "מה יודפס?",
        'options': {
            'a': "divided by zero",
            'b': "something broke",
            'c': "both lines print",
            'd': "SyntaxError - Exception must come last",
        },
        'correct': 'b',
        'why': "פייתון לוקח את "
               "הבלוק הראשון "
               "שמתאים. Exception מתאים "
               "להכל, ולכן השורה "
               "מתחתיו לא תרוץ "
               "לעולם.",
    },
    10: {
        'kind': 'choice',
        'q': "except ValueError:\n"
             "    print('bad input')\n"
             "except TypeError:\n"
             "    print('bad input')\n"
             "\n"
             "שתי השגיאות "
             "מקבלות אותה "
             "תגובה בדיוק\n"
             "איזו שורה תופסת "
             "את שתיהן בבלוק "
             "אחד?",
        'options': {
            'a': "except ValueError, TypeError as e:",
            'b': "except (ValueError, TypeError) as e:",
            'c': "except ValueError and TypeError as e:",
            'd': "except [ValueError, TypeError] as e:",
        },
        'correct': 'b',
        'why': "זה tuple, ולכן צריך "
               "סוגריים. בלעדיהם "
               "זו SyntaxError בפייתון "
               "מודרני.",
    },

    # --------------------------------------------- else and finally --
    11: {
        'kind': 'choice',
        'q': "try:\n"
             "    x = 10 / 2\n"
             "except ZeroDivisionError:\n"
             "    print('broke')\n"
             "else:\n"
             "    print('fine')\n"
             "\n"
             "מתי רץ הבלוק else?",
        'options': {
            'a': "Only when the try block finished with NO error",
            'b': "Only when an error was caught",
            'c': "Always, error or not",
            'd': "Only when no except block matched",
        },
        'correct': 'a',
        'why': "else הוא ההפך מ-except. "
               "הוא מאפשר להשאיר "
               "בתוך ה-try רק את "
               "השורות שעלולות "
               "להישבר.",
    },
    12: {
        'kind': 'choice',
        'q': "try:\n"
             "    print('A')\n"
             "    1 / 0\n"
             "except ZeroDivisionError:\n"
             "    print('B')\n"
             "else:\n"
             "    print('C')\n"
             "finally:\n"
             "    print('D')\n"
             "\n"
             "מה יודפס, ובאיזה "
             "סדר?",
        'options': {
            'a': "A B C D",
            'b': "A C D",
            'c': "A B",
            'd': "A B D",
        },
        'correct': 'd',
        'why': "השגיאה קרתה, "
               "ולכן except רץ ו-else לא. "
               "finally רץ בכל מקרה.",
    },
    13: {
        'kind': 'choice',
        'q': "try:\n"
             "    print('A')\n"
             "except ZeroDivisionError:\n"
             "    print('B')\n"
             "else:\n"
             "    print('C')\n"
             "finally:\n"
             "    print('D')\n"
             "\n"
             "הפעם אין שגיאה\n"
             "מה יודפס?",
        'options': {
            'a': "A B D",
            'b': "A C D",
            'c': "A C",
            'd': "A D",
        },
        'correct': 'b',
        'why': "אין שגיאה, ולכן else "
               "רץ ו-except מדולג. finally עדיין "
               "רץ - הוא תמיד רץ.",
    },
    14: {
        'kind': 'choice',
        'q': "try:\n"
             "    1 / 0\n"
             "finally:\n"
             "    print('cleaning up')\n"
             "\n"
             "אין except בכלל\n"
             "מה קורה?",
        'options': {
            'a': "'cleaning up' prints, then the program crashes with ZeroDivisionError",
            'b': "The program crashes and 'cleaning up' never prints",
            'c': "'cleaning up' prints and the error is quietly swallowed",
            'd': "SyntaxError - a try must have an except",
        },
        'correct': 'a',
        'why': "finally לא נועד לטפל "
               "בשגיאה. הוא נועד "
               "לוודא שהניקיון "
               "קורה בדרך החוצה.",
    },

    # ------------------------------------------------ where to catch --
    15: {
        'kind': 'choice',
        'q': "def my_div(a, b):\n"
             "    try:\n"
             "        return a / b\n"
             "    except ZeroDivisionError:\n"
             "        return 'no answer'\n"
             "\n"
             "x = my_div(10, 0)\n"
             "print(x ** 3)\n"
             "\n"
             "מה קורה?",
        'options': {
            'a': "It prints 'no answer'",
            'b': "It prints 0",
            'c': "ZeroDivisionError: division by zero",
            'd': "TypeError - x is the string 'no answer', and you cannot cube a string",
        },
        'correct': 'd',
        'why': "הפונקציה תפסה את "
               "השגיאה עמוק מדי "
               "והחזירה מחרוזת. "
               "הבעיה האמיתית "
               "צפה שוב מאוחר "
               "יותר, בתחפושת.",
    },
}
