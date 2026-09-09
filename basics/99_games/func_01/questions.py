# -*- coding: utf-8 -*-
"""
questions.py  --  the 10 challenges of FUNCTION LAB (lesson 18).

Lesson 18 is functions with a door on each side: values go IN through
parameters (with defaults, and with name= at the call), an answer comes OUT
through return, and a function with no return still hands back None.

So the game is not multiple choice. Every challenge is a real .py file the
student edits and runs, and there are three kinds of them:

    'write'   the editor holds a def line and a docstring - fill in the body
    'call'    the function is already written and in memory - call it properly
    'fix'     a broken file is in the editor - repair it, do not rewrite it

Each challenge-dict holds:
    'title'     short arcade name on the progress strip
    'kind'      write / call / fix   - drives the badge on the student's screen
    'teaches'   the one line the teacher can read out loud afterwards
    'setup'     code that ALREADY exists in memory. The student never types it.
                Only the 'call' challenges use it - it is shown, greyed out.
    'task'      what to do. Written one idea per line - every newline becomes a
                line break on their screen, so KEEP THE LINES SHORT.
    'starter'   what the editor is pre-filled with. For 'fix' this is the broken
                file; for 'write' it is the def line plus the docstring, so the
                habit from the lesson (:param / :return:) is already on screen.
    'expect'    one phrase: what has to come back
    'tests'     the checker. After their code runs we CALL their function and
                compare what came back:
                    {'call': 'triple(7)', 'is': '21'}
                Both sides are real python. The call runs in their namespace,
                the expected value in an empty one.
                This is what makes the checker judge the ANSWER and not the
                shape of it: any body that returns the right values passes -
                one line or five, if/else or no else, their own variable names.
    'prints'    for the 'call' challenges, what has to appear on screen. We
                compare the words and numbers only, so print() style is free.
    'require'   what the code MUST contain - the thing being taught, and only
                that. Almost always just def / return. The tests carry the rest.
    'forbid'    substrings that must NOT appear - stops the answer being typed
                out by hand instead of being worked out.
    'hint'      the HINT button. Costs half the points.
    'solution'  the answer key. Also what I DO NOT KNOW shows, for 0 points.
    'trap'      the near miss - what most of them will get wrong here.

THE RAMP
     1     one slot, one return                    triple(number)
     2     the function exists - CALL it           sticker_price(packs)
     3     two slots, filled left to right         triangle_area(base, height)
     4     name the slot at the call               split_bill(total=, people=)
     5     a default that fills itself             is_freezing(celsius=0)
     6     the order rule breaks the def line      SyntaxError, fix it
     7     one must, one may                       add_tax(price, percent=25)
     8     it printed, so nothing came back        print -> return
     9     it changed it, it did not give it back  scores = scores.sort()
    10     a whole dictionary back                 word_lengths(words)

    8 -> 9 is the pair that matters. Both files RUN. Both look like they work.
    Neither one hands anything back.
"""

QUESTIONS = {

    # ------------------------------------------- 1  one slot, one return --
    1: {
        'title': 'The Tripler',
        'kind': 'write',
        'teaches': 'a parameter is an empty slot; return hands the answer back',
        'setup': '',
        'task': "כתוב פונקציה שמקבלת מספר\n"
                "ומחזירה את המספר כפול 3",
        'starter': "def triple(number):\n"
                   "    '''return the number times 3'''\n"
                   "    # your line goes here\n"
                   "\n"
                   "\n"
                   "print(triple(7))\n",
        'expect': "המספר כפול 3, חוזר עם return",
        'tests': [
            {'call': "triple(7)", 'is': "21"},
            {'call': "triple(2.5)", 'is': "7.5"},
            {'call': "triple(0)", 'is': "0"},
        ],
        'prints': '',
        'require': ['def', 'return'],
        'forbid': [],
        'hint': "כל הגוף הוא שורה אחת:\n"
                "    return number * 3",
        'solution': "def triple(number):\n"
                    "    '''return the number times 3'''\n"
                    "    return number * 3\n"
                    "\n"
                    "\n"
                    "print(triple(7))\n",
        'trap': "עם print המספר רק מופיע על המסך ונעלם.\n"
                "רק return מחזיר את התוצאה החוצה, כך שאפשר להמשיך איתה.",
    },

    # ---------------------------------------- 2  the function exists: call --
    2: {
        'title': 'Wake It Up',
        'kind': 'call',
        'teaches': 'a def on its own does nothing - the call is what runs it',
        'setup': "def sticker_price(packs):\n"
                 "    '''\n"
                 "    price of a number of sticker packs\n"
                 "    :param packs: how many packs\n"
                 "    :return: the price, 7 a pack\n"
                 "    '''\n"
                 "    return packs * 7\n",
        'task': "קרא לפונקציה פעמיים\n"
                "פעם ראשונה שלח לפונקציה את המספר 6 והדפס את התשובה\n"
                "פעם שנייה שלח לפונקציה את המספר 10 והדפס את התוצאה",
        'starter': "# sticker_price is already in memory - just use it\n",
        'expect': "42 ואחריו 70, מודפסים",
        'tests': [],
        'prints': "42\n70",
        'require': ['sticker_price('],
        'forbid': ['42', '70'],
        'hint': "print(sticker_price(6))\n"
                "ואותה שורה שוב עם 10.\n"
                "המספר 6 נכנס לתוך המשבצת ששמה packs.",
        'solution': "print(sticker_price(6))\nprint(sticker_price(10))\n",
        'trap': "אם תכתוב print(6 * 7) יופיע אותו מספר על המסך, אבל לא השתמשת בפונקציה בכלל.\n"
                "כל הרעיון בפונקציה הוא שהמחיר 7 כתוב במקום אחד בלבד.",
    },

    # ------------------------------------ 3  two slots, left to right --
    3: {
        'title': 'Base And Height',
        'kind': 'write',
        'teaches': 'two parameters, filled in order; the names are part of the deal',
        'setup': '',
        'task': "כתוב פונקציה שמקבלת בסיס וגובה\n"
                "ומחזירה את שטח המשולש: בסיס כפול גובה חלקי 2\n"
                "\n"
                "אל תשנה את שמות המשבצות base ו-height.",
        'starter': "def triangle_area(base, height):\n"
                   "    '''return the area of the triangle'''\n"
                   "    # your line goes here\n"
                   "\n"
                   "\n"
                   "print(triangle_area(10, 6))\n",
        'expect': "השטח - base * height / 2",
        'tests': [
            {'call': "triangle_area(10, 6)", 'is': "30.0"},
            {'call': "triangle_area(3, 5)", 'is': "7.5"},
            {'call': "triangle_area(height=4, base=9)", 'is': "18.0"},
        ],
        'prints': '',
        'require': ['def', 'return'],
        'forbid': [],
        'hint': "    return base * height / 2\n"
                "הבדיקה האחרונה קוראת לפונקציה הפוך בכוונה - height=4, base=9.\n"
                "זה עובד רק אם המשבצות עדיין נקראות base ו-height.",
        'solution': "def triangle_area(base, height):\n"
                    "    '''return the area of the triangle'''\n"
                    "    return base * height / 2\n"
                    "\n"
                    "\n"
                    "print(triangle_area(10, 6))\n",
        'trap': "אם תשנה את שמות המשבצות ל-a ו-b, הכל עובד עד שמישהו קורא עם base=.\n"
                "שמות המשבצות הם לא עניין פרטי שלך - דרכם הקריאה מדברת איתך.",
    },

    # ------------------------------------------ 4  name the slot at the call --
    4: {
        'title': 'Backwards Bill',
        'kind': 'call',
        'teaches': 'name= at the call, so the order stops mattering',
        'setup': "def split_bill(total, people):\n"
                 "    '''\n"
                 "    what one person pays\n"
                 "    :param total: the whole bill\n"
                 "    :param people: how many are paying\n"
                 "    :return: one person's share\n"
                 "    '''\n"
                 "    return total / people\n",
        'task': "החשבון הוא 120 ויש 4 אנשים, אז כל אחד משלם 30\n"
                "\n"
                "הקריאה שלמטה הפוכה - היא מחלקת 4 בין 120 אנשים\n"
                "תקן אותה בלי להזיז את המספרים:\n"
                "בשורה שמפעילה את הפונקציה כתוב שם פרמטר שווה ליד כל פרמטר",
        'starter': "print(split_bill(4, 120))\n",
        'expect': "30.0 - וה-4 עדיין כתוב לפני ה-120",
        'tests': [],
        'prints': "30.0",
        'require': ['total=', 'people='],
        'forbid': ['split_bill(120,4)', 'split_bill(120.0,4)'],
        'hint': "split_bill(people=4, total=120)\n"
                "המספרים נשארים במקום. עכשיו כל אחד מהם אומר לאיזו משבצת הוא שייך,\n"
                "ולכן הסדר כבר לא משנה.",
        'trap': "גם החלפת מקום בין שני המספרים תדפיס 30.0, ולא תלמד כלום.\n"
                "בעוד חצי שנה split_bill(120, 4) לא יגיד לך כלום, "
                "אבל split_bill(total=120, people=4) כן.",
        'solution': "print(split_bill(people=4, total=120))\n",
    },

    # -------------------------------------- 5  a default that fills itself --
    5: {
        'title': 'Below Zero',
        'kind': 'write',
        'teaches': 'a default value, and returning a real True / False',
        'setup': '',
        'task': "כתוב פונקציה שמקבלת טמפרטורה\n"
                "ומחזירה True אם היא 0 או פחות, אחרת False\n"
                "\n"
                "ברירת המחדל של המשבצת היא 0,\n"
                "כך שגם קריאה בלי כלום בסוגריים חייבת לעבוד.",
        'starter': "def is_freezing(celsius=0):\n"
                   "    '''True if it is freezing, otherwise False'''\n"
                   "    # your lines go here\n"
                   "\n"
                   "\n"
                   "print(is_freezing())\n"
                   "print(is_freezing(15))\n",
        'expect': "True או False אמיתיים, ו-is_freezing() בלי ארגומנט לא קורסת",
        'tests': [
            {'call': "is_freezing()", 'is': "True"},
            {'call': "is_freezing(-8)", 'is': "True"},
            {'call': "is_freezing(15)", 'is': "False"},
            {'call': "is_freezing(celsius=0)", 'is': "True"},
        ],
        'prints': '',
        'require': ['def', 'return'],
        'forbid': ["'true'", '"true"', "'false'", '"false"'],
        'hint': "    if celsius <= 0:\n"
                "        return True\n"
                "    return False\n"
                "אין צורך ב-else - ה-return הראשון כבר יצא מהפונקציה.\n"
                "(גם return celsius <= 0 בשורה אחת זה בדיוק אותו דבר.)",
        'solution': "def is_freezing(celsius=0):\n"
                    "    '''True if it is freezing, otherwise False'''\n"
                    "    if celsius <= 0:\n"
                    "        return True\n"
                    "    return False\n"
                    "\n"
                    "\n"
                    "print(is_freezing())\n"
                    "print(is_freezing(15))\n",
        'trap': "return 'True' במרכאות מדפיס בדיוק אותו דבר ולא שווה כלום -\n"
                "אי אפשר לשאול עליו if. מילה במרכאות היא לא תשובה, היא תמונה של תשובה.",
    },

    # ------------------------------------- 6  the order rule, as a crash --
    6: {
        'title': 'It Will Not Even Start',
        'kind': 'fix',
        'teaches': 'slots without a default have to come first',
        'setup': '',
        'task': "הקובץ הזה לא רץ בכלל. פייתון נעצר כבר בשורת ה-def:\n"
                "SyntaxError: non-default argument follows default argument\n"
                "\n"
                "תקן את שורת ה-def כדי שהקובץ יתחיל לרוץ\n"
                "אל תיגע בגוף הפונקציה ואל תיגע בשתי הקריאות",
        'starter': "def name_tag(colour='blue', text):\n"
                   "    return text + ' (' + colour + ')'\n"
                   "\n"
                   "\n"
                   "print(name_tag('Dana'))\n"
                   "print(name_tag('Ori', 'red'))\n",
        'expect': "Dana (blue) ואחריו Ori (red)",
        'tests': [
            {'call': "name_tag('Dana')", 'is': "'Dana (blue)'"},
            {'call': "name_tag('Ori', 'red')", 'is': "'Ori (red)'"},
            {'call': "name_tag(text='Gil')", 'is': "'Gil (blue)'"},
        ],
        'prints': '',
        'require': ['def'],
        'forbid': [],
        'hint': "החלף בין שתי המשבצות:\n"
                "    def name_tag(text, colour='blue'):\n"
                "פייתון ממלא משבצות משמאל לימין, ולכן הוא לא יכול לדלג מעל text\n"
                "כדי להגיע ל-colour. מה שחייבים לתת - בא ראשון.",
        'solution': "def name_tag(text, colour='blue'):\n"
                    "    return text + ' (' + colour + ')'\n"
                    "\n"
                    "\n"
                    "print(name_tag('Dana'))\n"
                    "print(name_tag('Ori', 'red'))\n",
        'trap': "גם לתת ברירת מחדל גם ל-text - למשל text='' - יגרום לקובץ לרוץ,\n"
                "ואז name_tag() תבנה בשקט תווית ריקה במקום להגיד לך שחסר משהו.",
    },

    # ----------------------------------------- 7  one must, one may --
    7: {
        'title': 'Tax On Top',
        'kind': 'write',
        'teaches': 'one required slot and one with a default, in the right order',
        'setup': '',
        'task': "כתוב פונקציה שמקבלת מחיר ואחוז מס\n"
                "ומחזירה את המחיר אחרי שהוסיפו לו את המס\n"
                "\n"
                "את המחיר חייבים לתת, ואחוז המס הוא 25 כברירת מחדל\n"
                "200 עם 25% חוזר 250.0",
        'starter': "def add_tax(price, percent=25):\n"
                   "    '''return the price with the tax added'''\n"
                   "    # your line goes here\n"
                   "\n"
                   "\n"
                   "print(add_tax(200))\n"
                   "print(add_tax(80, 50))\n",
        'expect': "המחיר ועוד המס, חוזר עם return",
        'tests': [
            {'call': "add_tax(200)", 'is': "250.0"},
            {'call': "add_tax(80, 50)", 'is': "120.0"},
            {'call': "add_tax(price=40, percent=10)", 'is': "44.0"},
            {'call': "add_tax(60, percent=0)", 'is': "60"},
        ],
        'prints': '',
        'require': ['def', 'return'],
        'forbid': [],
        'hint': "    return price + price * percent / 100\n"
                "המס מתווסף מעל המחיר, לא יורד ממנו. 200 עולה ל-250.\n"
                "price * 1.25 עובד רק עבור 25 - האחוז חייב להיכנס לחישוב.",
        'solution': "def add_tax(price, percent=25):\n"
                    "    '''return the price with the tax added'''\n"
                    "    return price + price * percent / 100\n"
                    "\n"
                    "\n"
                    "print(add_tax(200))\n"
                    "print(add_tax(80, 50))\n",
        'trap': "price * 1.25 עובר את הבדיקה הראשונה ונופל בכל השאר.\n"
                "ברירת מחדל היא ערך שהקורא רשאי להחליף - לא מספר שאתה אופה בתוך הגוף.",
    },

    # ------------------------------------ 8  it printed, so nothing came back --
    8: {
        'title': 'Half The Job',
        'kind': 'fix',
        'teaches': 'no return means None comes back, however good the printout looks',
        'setup': '',
        'task': "יש בעיה בקוד התוכנית\n"
                "תקן את הפונקציה",
        'starter': "def stock_left(shelf, sold):\n"
                   "    print(shelf - sold)\n"
                   "\n"
                   "\n"
                   "left = stock_left(30, 12)\n"
                   "print(left * 2)\n",
        'expect': "הקובץ רץ עד הסוף והשורה האחרונה מדפיסה 36",
        'tests': [
            {'call': "stock_left(30, 12)", 'is': "18"},
            {'call': "stock_left(100, 100)", 'is': "0"},
            {'call': "stock_left(sold=5, shelf=9)", 'is': "4"},
        ],
        'prints': '',
        'require': ['return'],
        'forbid': [],
        'hint': "מילה אחת משתנה:\n"
                "    return shelf - sold\n"
                "print מראה לבן אדם. return נותן לתוכנית.\n"
                "רק אחד מהם מאפשר לשורה הבאה לעשות left * 2.",
        'solution': "def stock_left(shelf, sold):\n"
                    "    return shelf - sold\n"
                    "\n"
                    "\n"
                    "left = stock_left(30, 12)\n"
                    "print(left * 2)\n",
        'trap': "להשאיר את ה-print וגם להוסיף return זה עובד, ובדרך כלל זו טעות -\n"
                "עכשיו הפונקציה צועקת בכל פעם שמישהו משתמש בה.\n"
                "תבחר אחד: return בפנים, print בחוץ.",
    },

    # --------------------------- 9  it changed it, it did not give it back --
    9: {
        'title': 'The Vanishing List',
        'kind': 'fix',
        'teaches': '.sort() changes in place and returns None - the classic bug',
        'setup': '',
        'task': "הפונקציה מחזירה None\n"
                "תקן את הפונקציה",
        'starter': "def sorted_scores(scores):\n"
                   "    scores = scores.sort()\n"
                   "    return scores\n"
                   "\n"
                   "\n"
                   "print(sorted_scores([88, 41, 96, 60]))\n",
        'expect': "[41, 60, 88, 96] - רשימה, לא None",
        'tests': [
            {'call': "sorted_scores([88, 41, 96, 60])", 'is': "[41, 60, 88, 96]"},
            {'call': "sorted_scores([5])", 'is': "[5]"},
            {'call': "sorted_scores([])", 'is': "[]"},
        ],
        'prints': '',
        'require': ['return'],
        'forbid': ['=scores.sort()'],
        'hint': "דרך אחת - תן ל-sort לעשות את שלה, ואז תחזיר את הרשימה:\n"
                "    scores.sort()\n"
                "    return scores\n"
                "דרך שנייה - בקש רשימה חדשה ומסודרת:\n"
                "    return sorted(scores)",
        'solution': "def sorted_scores(scores):\n"
                    "    return sorted(scores)\n"
                    "\n"
                    "\n"
                    "print(sorted_scores([88, 41, 96, 60]))\n",
        'trap': "תשאל את זה על כל פעולה שאתה קורא לה: היא מחזירה משהו, או משנה במקום?\n"
                "sort, append ו-update משנות במקום. sorted ו-pop מחזירות.",
    },

    # ----------------------------------- 10  a whole dictionary back --
    10: {
        'title': 'How Long Is Each One',
        'kind': 'write',
        'teaches': 'a loop inside a function, and a whole dict handed back',
        'setup': '',
        'task': "כתוב פונקציה שמקבלת רשימת מילים\n"
                "ומחזירה מילון: כל מילה היא מפתח, ומספר האותיות שלה הוא הערך\n"
                "\n"
                "כלומר יש להתחיל ממילון ריק\n"
                "לרוץ על רשימת המילים\n"
                "ועבור כל מילה לשים במילון כמפתח את המילה\n"
                "ובערך את אורך המילה\n"
                "ובסוף מחזירה את המילון\n"
                "\n"
                "רשימה ריקה צריכה לחזור כמילון ריק.",
        'starter': "def word_lengths(words):\n"
                   "    sizes = {}\n"
                   "    # loop over words and fill sizes\n"
                   "    # then hand sizes back\n"
                   "\n"
                   "\n"
                   "print(word_lengths(['sun', 'moon', 'star']))\n",
        'expect': "מילון - המילה כמפתח, האורך שלה כערך",
        'tests': [
            {'call': "word_lengths(['sun', 'moon', 'star'])",
             'is': "{'sun': 3, 'moon': 4, 'star': 4}"},
            {'call': "word_lengths(['python'])", 'is': "{'python': 6}"},
            {'call': "word_lengths([])", 'is': "{}"},
        ],
        'prints': '',
        'require': ['def', 'return', 'for'],
        'forbid': [],
        'hint': "    for w in words:\n"
                "        sizes[w] = len(w)\n"
                "    return sizes\n"
                "ה-return בא אחרי הלולאה, לא בתוכה -\n"
                "בתוך הלולאה הוא היה יוצא כבר אחרי המילה הראשונה.\n"
                "(גם {w: len(w) for w in words} בשורה אחת נחשב.)",
        'solution': "def word_lengths(words):\n"
                    "    sizes = {}\n"
                    "    for w in words:\n"
                    "        sizes[w] = len(w)\n"
                    "    return sizes\n"
                    "\n"
                    "\n"
                    "print(word_lengths(['sun', 'moon', 'star']))\n",
        'trap': "return עם טאב אחד יותר מדי - בתוך הלולאה - מחזיר {'sun': 3} ונעצר.\n"
                "הפונקציה נראית נכונה ועונה אחרי מילה אחת.",
    },
}
