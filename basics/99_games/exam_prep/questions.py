# -*- coding: utf-8 -*-
"""
questions.py  --  EXAM REHEARSAL.

Not a fixed quiz. A small, growing bank of coding questions, one bucket per
level:

    QUESTIONS = {
        'easy':   [ {id, title, topic, task, starter, ...}, ... ],
        'medium': [ ... ],
        'expert': [ ... ],
    }

Every question is a FUNCTION the student writes. It is judged the same way
Function Lab (99_games/func_01) judges - we CALL their function ourselves and
compare what came back. Never print(). A function is easy to check by its
output; a print statement is not, so every question here ends in return.

LANGUAGE - same rule as the Try/Except quiz (99_games/try_except)
    This is a beginners' class, so 'task' and 'hint' are in HEBREW.
    Everything else stays English: function names, string literals the
    function must return ('Hello World', not a Hebrew translation of it),
    the code in 'starter'/'solution', and the 'topic' tag.

PUNCTUATION IN 'task'
    No trailing period at the end of a line. A period stays only when it
    genuinely separates two sentences sitting on the SAME line (for example
    "...שגיאת ZeroDivisionError. תפסו אותה..." - one sentence ends and
    another starts, both on one line). A period that would just sit at the
    very end of a line is dropped.

QUESTIONS ARE FIXED, NOT RANDOM
    Each level's questions always show up in the same order (question 1,
    then 2, then 3...) so the student always knows which question they are
    on - there is a "Question X of Y" readout on screen. Nothing here is
    randomised on a normal SKIP / NEXT / level switch.

    Two questions that test two different things (upper vs. lower vs. title
    case, for example) are two SEPARATE questions, not "variants" of one -
    each with its own id/title, each always shown as itself.

'retry' - THE ONLY PLACE ANYTHING CHANGES
    TRY AGAIN (shown after the SOLUTION button was used) is the one moment
    where the text is allowed to change, so a second attempt does not feel
    like literally the same question. 'retry' is an OPTIONAL list of
    alternates - same shape as the question itself, one small thing swapped
    (a different literal to return, a different power, a different rounding).
    Only questions where that swap is genuinely a one-word change get a
    'retry' list. Everything else has none - TRY AGAIN then simply clears
    the solution box and resets the editor back to the original starter
    code, with the task left exactly as it was.

    Nothing is templated at runtime in the browser - every question and
    every retry entry is written out here, in full, in Python, and this
    file (via make_exam_prep.py) checks each one against its own answer
    before anything ships.

Shape of a question dict:
    'id'        stable identifier (used to track "solved" state)
    'title'     short English name shown above the task
    'topic'     small English tag, e.g. 'functions · strings · return'
    'task'      what to do, in Hebrew, one idea per line - a NUDGE, never
                spelling out the finished line of code
    'starter'   what the editor is pre-filled with (English)
    'expect'    one phrase: what has to come back (unused by the UI, kept
                for parity with func_01's shape)
    'tests'     [{'call': 'greet()', 'is': "'Hello World'"}, ...]
    'require'   substrings the code MUST contain (almost always def / return)
    'forbid'    substrings that must NOT appear
    'hint'      the HINT button (Hebrew) - names the tool to use (a
                function, a method, an operator) without handing over the
                finished line
    'solution'  the SOLUTION button (English code)
    'retry'     OPTIONAL - a list of alternate {task, starter, expect,
                tests, require, forbid, hint, solution} dicts, used only by
                TRY AGAIN
"""

QUESTIONS = {

    # ================================================================ EASY
    'easy': [
        {
            'id': 'classify_number',
            'title': 'Positive, Negative, or Zero',
            'topic': 'if / elif / else',
            'task': "כתבו פונקציה בשם classify_number\nפרמטר אחד, בשם n\nאם n גדול מ-0 היא מחזירה 'positive'\nאם n קטן מ-0 היא מחזירה 'negative'\nאחרת היא מחזירה 'zero'",
            'starter': "def classify_number(n):\n    '''return 'positive', 'negative', or 'zero' for n'''\n    # your line goes here\n\n\nprint(classify_number(5))\nprint(classify_number(-3))\nprint(classify_number(0))\n",
            'expect': "return 'positive', 'negative', or 'zero' for n",
            'tests': [
                {'call': 'classify_number(5)', 'is': "'positive'"},
                {'call': 'classify_number(-3)', 'is': "'negative'"},
                {'call': 'classify_number(0)', 'is': "'zero'"},
                {'call': 'classify_number(100)', 'is': "'positive'"},
            ],
            'require': ['def', 'return', 'if', 'elif'],
            'forbid': [],
            'hint': 'יש כאן שלוש אפשרויות - if, elif אחד, ו-else',
            'solution': "def classify_number(n):\n    if n > 0:\n        return 'positive'\n    elif n < 0:\n        return 'negative'\n    else:\n        return 'zero'\n\n\nprint(classify_number(5))\nprint(classify_number(-3))\nprint(classify_number(0))\n",
        },
        {
            'id': 'is_even',
            'title': 'Even Or Odd',
            'topic': 'if / else · % operator',
            'task': 'כתבו פונקציה בשם is_even\nפרמטר אחד, בשם n\nהיא מחזירה True אם n זוגי, ו-False אם הוא אי-זוגי',
            'starter': "def is_even(n):\n    '''return True if n is even, False otherwise'''\n    # your line goes here\n\n\nprint(is_even(4))\nprint(is_even(7))\n",
            'expect': 'return True if n is even, False otherwise',
            'tests': [
                {'call': 'is_even(4)', 'is': 'True'},
                {'call': 'is_even(7)', 'is': 'False'},
                {'call': 'is_even(0)', 'is': 'True'},
                {'call': 'is_even(-2)', 'is': 'True'},
            ],
            'require': ['def', 'return', 'if'],
            'forbid': [],
            'hint': 'האופרטור % נותן את השארית מחילוק - שארית 0 מחילוק ב-2 אומרת זוגי',
            'solution': 'def is_even(n):\n    if n % 2 == 0:\n        return True\n    else:\n        return False\n\n\nprint(is_even(4))\nprint(is_even(7))\n',
        },
        {
            'id': 'letter_grade',
            'title': 'Letter Grade',
            'topic': 'if / elif / else · chained ranges',
            'task': "כתבו פונקציה בשם letter_grade\nפרמטר אחד, בשם score\nציון 90 ומעלה מחזיר 'A'\nציון 80 עד 89 מחזיר 'B'\nציון 70 עד 79 מחזיר 'C'\nכל ציון נמוך יותר מחזיר 'F'",
            'starter': "def letter_grade(score):\n    '''return the letter grade for score'''\n    # your line goes here\n\n\nprint(letter_grade(95))\nprint(letter_grade(82))\nprint(letter_grade(55))\n",
            'expect': 'return the letter grade for score',
            'tests': [
                {'call': 'letter_grade(95)', 'is': "'A'"},
                {'call': 'letter_grade(82)', 'is': "'B'"},
                {'call': 'letter_grade(71)', 'is': "'C'"},
                {'call': 'letter_grade(55)', 'is': "'F'"},
            ],
            'require': ['def', 'return', 'if', 'elif'],
            'forbid': [],
            'hint': 'סדרו את התנאים מהגבוה לנמוך עם if ו-elif - הראשון שמתקיים קובע',
            'solution': "def letter_grade(score):\n    if score >= 90:\n        return 'A'\n    elif score >= 80:\n        return 'B'\n    elif score >= 70:\n        return 'C'\n    else:\n        return 'F'\n\n\nprint(letter_grade(95))\nprint(letter_grade(82))\nprint(letter_grade(55))\n",
        },
        {
            'id': 'bigger_of_two',
            'title': 'The Bigger One',
            'topic': 'if / else · comparison',
            'task': 'כתבו פונקציה בשם bigger_of_two\nשני פרמטרים: a ו-b\nהיא מחזירה את הגדול מביניהם',
            'starter': "def bigger_of_two(a, b):\n    '''return whichever of a, b is bigger'''\n    # your line goes here\n\n\nprint(bigger_of_two(3, 9))\nprint(bigger_of_two(10, 2))\n",
            'expect': 'return whichever of a, b is bigger',
            'tests': [
                {'call': 'bigger_of_two(3, 9)', 'is': '9'},
                {'call': 'bigger_of_two(10, 2)', 'is': '10'},
                {'call': 'bigger_of_two(-1, -5)', 'is': '-1'},
            ],
            'require': ['def', 'return', 'if'],
            'forbid': [],
            'hint': 'תנאי אחד עם if/else מספיק - איזה מהשניים גדול מהשני',
            'solution': 'def bigger_of_two(a, b):\n    if a > b:\n        return a\n    else:\n        return b\n\n\nprint(bigger_of_two(3, 9))\nprint(bigger_of_two(10, 2))\n',
        },
        {
            'id': 'sum_up_to',
            'title': 'Sum 1 To N',
            'topic': 'for loop · range',
            'task': 'כתבו פונקציה בשם sum_up_to\nפרמטר אחד, בשם n\nהיא מחזירה את הסכום של כל המספרים מ-1 עד n, כולל\nהשתמשו בלולאת for ובפונקציית range',
            'starter': "def sum_up_to(n):\n    '''return the sum of 1 through n'''\n    # your line goes here\n\n\nprint(sum_up_to(5))\n",
            'expect': 'return the sum of 1 through n',
            'tests': [
                {'call': 'sum_up_to(5)', 'is': '15'},
                {'call': 'sum_up_to(1)', 'is': '1'},
                {'call': 'sum_up_to(10)', 'is': '55'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': ['while'],
            'hint': 'range(1, n + 1) עובר על כל המספרים מ-1 עד n כולל',
            'solution': 'def sum_up_to(n):\n    total = 0\n    for i in range(1, n + 1):\n        total += i\n    return total\n\n\nprint(sum_up_to(5))\n',
        },
        {
            'id': 'count_vowels',
            'title': 'Count The Vowels',
            'topic': 'for loop · if · strings',
            'task': 'כתבו פונקציה בשם count_vowels\nפרמטר אחד, בשם word\nהיא מחזירה כמה מהאותיות במילה הן תנועות: a, e, i, o, u\n(לא רגישה לרישיות)\nעברו על אותיות המילה עם לולאת for',
            'starter': "def count_vowels(word):\n    '''return how many letters in word are vowels'''\n    # your lines go here\n\n\nprint(count_vowels('Hello World'))\n",
            'expect': 'return how many letters in word are vowels',
            'tests': [
                {'call': "count_vowels('Hello World')", 'is': '3'},
                {'call': "count_vowels('sky')", 'is': '0'},
                {'call': "count_vowels('AEIOU')", 'is': '5'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': ['while'],
            'hint': "עברו על כל אות במילה ובדקו אם היא נמצאת במחרוזת 'aeiou' עם in",
            'solution': "def count_vowels(word):\n    vowels = 'aeiou'\n    count = 0\n    for ch in word.lower():\n        if ch in vowels:\n            count += 1\n    return count\n\n\nprint(count_vowels('Hello World'))\n",
        },
        {
            'id': 'first_divisible_by',
            'title': 'First One That Divides',
            'topic': 'for loop · break',
            'task': 'כתבו פונקציה בשם first_divisible_by\nשני פרמטרים: numbers (רשימה) ו-k\nהיא מחזירה את המספר הראשון ברשימה שמתחלק ב-k בלי שארית\nעברו על הרשימה עם לולאת for, ועצרו אותה עם break ברגע שמוצאים\nאת המספר - אין טעם להמשיך הלאה',
            'starter': "def first_divisible_by(numbers, k):\n    '''return the first number in numbers divisible by k'''\n    # your lines go here\n\n\nprint(first_divisible_by([7, 9, 12, 15], 3))\n",
            'expect': 'return the first number in numbers divisible by k',
            'tests': [
                {'call': 'first_divisible_by([7, 9, 12, 15], 3)', 'is': '9'},
                {'call': 'first_divisible_by([2, 4, 6], 5)', 'is': 'None'},
                {'call': 'first_divisible_by([10, 15, 20], 5)', 'is': '10'},
            ],
            'require': ['def', 'return', 'for', 'break'],
            'forbid': ['while'],
            'hint': 'n % k == 0 בודק אם n מתחלק ב-k בלי שארית',
            'solution': 'def first_divisible_by(numbers, k):\n    result = None\n    for n in numbers:\n        if n % k == 0:\n            result = n\n            break\n    return result\n\n\nprint(first_divisible_by([7, 9, 12, 15], 3))\n',
        },
        {
            'id': 'sum_skip_negatives',
            'title': 'Sum, Skipping The Negatives',
            'topic': 'for loop · continue',
            'task': 'כתבו פונקציה בשם sum_skip_negatives\nפרמטר אחד, בשם numbers - רשימה של מספרים\nהיא מחזירה את סכום כל המספרים החיוביים ברשימה\nעברו על הרשימה עם לולאת for, ודלגו על מספרים שליליים עם\ncontinue - במקום לבדוק אותם עם if נוסף',
            'starter': "def sum_skip_negatives(numbers):\n    '''return the sum of the non-negative numbers in the list'''\n    # your lines go here\n\n\nprint(sum_skip_negatives([3, -2, 5, -8, 1]))\n",
            'expect': 'return the sum of the non-negative numbers in the list',
            'tests': [
                {'call': 'sum_skip_negatives([3, -2, 5, -8, 1])', 'is': '9'},
                {'call': 'sum_skip_negatives([-1, -2, -3])', 'is': '0'},
                {'call': 'sum_skip_negatives([1, 2, 3])', 'is': '6'},
            ],
            'require': ['def', 'return', 'for', 'continue'],
            'forbid': ['while'],
            'hint': 'continue מדלגת מיד לאיטרציה הבאה של הלולאה, בלי להריץ את שאר הגוף',
            'solution': 'def sum_skip_negatives(numbers):\n    total = 0\n    for n in numbers:\n        if n < 0:\n            continue\n        total += n\n    return total\n\n\nprint(sum_skip_negatives([3, -2, 5, -8, 1]))\n',
        },
        {
            'id': 'count_until_zero',
            'title': 'Count Until The First Zero',
            'topic': 'for loop · break',
            'task': 'כתבו פונקציה בשם count_until_zero\nפרמטר אחד, בשם numbers - רשימה של מספרים\nהיא מחזירה כמה מספרים יש ברשימה עד המספר 0 הראשון, לא כולל אותו\n(אם אין בכלל 0 ברשימה, מחזירה את האורך של כל הרשימה)\nעברו על הרשימה עם לולאת for, ועצרו אותה עם break ברגע שמגיעים ל-0',
            'starter': "def count_until_zero(numbers):\n    '''return how many numbers come before the first 0'''\n    # your lines go here\n\n\nprint(count_until_zero([4, 8, 2, 0, 9, 1]))\n",
            'expect': 'return how many numbers come before the first 0',
            'tests': [
                {'call': 'count_until_zero([4, 8, 2, 0, 9, 1])', 'is': '3'},
                {'call': 'count_until_zero([1, 2, 3])', 'is': '3'},
                {'call': 'count_until_zero([0, 5, 5])', 'is': '0'},
            ],
            'require': ['def', 'return', 'for', 'break'],
            'forbid': [],
            'hint': 'עברו על המספרים עם for, ועצרו את הלולאה עם break ברגע שמגיעים למספר 0',
            'solution': 'def count_until_zero(numbers):\n    count = 0\n    for n in numbers:\n        if n == 0:\n            break\n        count += 1\n    return count\n\n\nprint(count_until_zero([4, 8, 2, 0, 9, 1]))\n',
        },
        {
            'id': 'append_item',
            'title': 'Add To The End',
            'topic': 'list · append',
            'task': 'כתבו פונקציה בשם append_item\nשני פרמטרים: items (רשימה) ו-value\nהיא מוסיפה את value לסוף הרשימה, ומחזירה את הרשימה',
            'starter': "def append_item(items, value):\n    '''add value to the end of items, return items'''\n    # your line goes here\n\n\nprint(append_item([1, 2, 3], 4))\n",
            'expect': 'add value to the end of items, return items',
            'tests': [
                {'call': 'append_item([1, 2, 3], 4)', 'is': '[1, 2, 3, 4]'},
                {'call': 'append_item([], 1)', 'is': '[1]'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש לרשימה פעולה שמוסיפה איבר לסופה',
            'solution': 'def append_item(items, value):\n    items.append(value)\n    return items\n\n\nprint(append_item([1, 2, 3], 4))\n',
        },
        {
            'id': 'pop_last',
            'title': 'Remove The Last One',
            'topic': 'list · pop',
            'task': 'כתבו פונקציה בשם pop_last\nפרמטר אחד, בשם items - רשימה\nהיא מסירה את האיבר האחרון מהרשימה, ומחזירה את הרשימה',
            'starter': "def pop_last(items):\n    '''remove the last item from items, return items'''\n    # your line goes here\n\n\nprint(pop_last([1, 2, 3, 4]))\n",
            'expect': 'remove the last item from items, return items',
            'tests': [
                {'call': 'pop_last([1, 2, 3, 4])', 'is': '[1, 2, 3]'},
                {'call': 'pop_last([9])', 'is': '[]'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש לרשימה פעולה שמסירה ומחזירה את האיבר האחרון, בלי פרמטר',
            'solution': 'def pop_last(items):\n    items.pop()\n    return items\n\n\nprint(pop_last([1, 2, 3, 4]))\n',
        },
        {
            'id': 'pop_at',
            'title': 'Remove By Position',
            'topic': 'list · pop(index)',
            'task': 'כתבו פונקציה בשם pop_at\nשני פרמטרים: items (רשימה) ו-index\nהיא מסירה מהרשימה את האיבר במיקום index, ומחזירה את האיבר שהוסר\n(לא את הרשימה)',
            'starter': "def pop_at(items, index):\n    '''remove and return the item at index'''\n    # your line goes here\n\n\nprint(pop_at([10, 20, 30, 40], 1))\n",
            'expect': 'remove and return the item at index',
            'tests': [
                {'call': 'pop_at([10, 20, 30, 40], 1)', 'is': '20'},
                {'call': 'pop_at([5, 6, 7], 0)', 'is': '5'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'אותה פעולה כמו בשאלה הקודמת, אבל עם מיקום כפרמטר',
            'solution': 'def pop_at(items, index):\n    return items.pop(index)\n\n\nprint(pop_at([10, 20, 30, 40], 1))\n',
        },
        {
            'id': 'insert_at',
            'title': 'Insert In The Middle',
            'topic': 'list · insert',
            'task': 'כתבו פונקציה בשם insert_at\nשלושה פרמטרים: items (רשימה), index ו-value\nהיא מכניסה את value לרשימה במיקום index, ומחזירה את הרשימה',
            'starter': "def insert_at(items, index, value):\n    '''insert value at index, return items'''\n    # your line goes here\n\n\nprint(insert_at([1, 2, 4], 2, 3))\n",
            'expect': 'insert value at index, return items',
            'tests': [
                {'call': 'insert_at([1, 2, 4], 2, 3)', 'is': '[1, 2, 3, 4]'},
                {'call': 'insert_at([5, 6], 0, 1)', 'is': '[1, 5, 6]'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש לרשימה פעולה שמכניסה איבר במיקום מסוים, לא בסוף',
            'solution': 'def insert_at(items, index, value):\n    items.insert(index, value)\n    return items\n\n\nprint(insert_at([1, 2, 4], 2, 3))\n',
        },
        {
            'id': 'remove_value',
            'title': 'Remove By Value',
            'topic': 'list · remove',
            'task': 'כתבו פונקציה בשם remove_value\nשני פרמטרים: items (רשימה) ו-value\nהיא מסירה מהרשימה את ההופעה הראשונה של value, ומחזירה את הרשימה',
            'starter': "def remove_value(items, value):\n    '''remove the first occurrence of value, return items'''\n    # your line goes here\n\n\nprint(remove_value([5, 3, 8, 3], 3))\n",
            'expect': 'remove the first occurrence of value, return items',
            'tests': [
                {'call': 'remove_value([5, 3, 8, 3], 3)', 'is': '[5, 8, 3]'},
                {'call': 'remove_value([1, 2, 3], 2)', 'is': '[1, 3]'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש לרשימה פעולה שמסירה איבר לפי הערך שלו, לא לפי מיקום',
            'solution': 'def remove_value(items, value):\n    items.remove(value)\n    return items\n\n\nprint(remove_value([5, 3, 8, 3], 3))\n',
        },
        {
            'id': 'sort_ascending',
            'title': 'Sort It',
            'topic': 'list · sort',
            'task': 'כתבו פונקציה בשם sort_ascending\nפרמטר אחד, בשם items - רשימה של מספרים\nהיא ממיינת את הרשימה מהקטן לגדול, ומחזירה אותה',
            'starter': "def sort_ascending(items):\n    '''sort items in place, return items'''\n    # your line goes here\n\n\nprint(sort_ascending([5, 1, 4, 2]))\n",
            'expect': 'sort items in place, return items',
            'tests': [
                {'call': 'sort_ascending([5, 1, 4, 2])', 'is': '[1, 2, 4, 5]'},
                {'call': 'sort_ascending([3, 3, 1])', 'is': '[1, 3, 3]'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש לרשימה פעולה שממיינת אותה במקום - היא לא מחזירה רשימה חדשה',
            'solution': 'def sort_ascending(items):\n    items.sort()\n    return items\n\n\nprint(sort_ascending([5, 1, 4, 2]))\n',
        },
        {
            'id': 'sorted_copy',
            'title': 'Sort It Without Changing The Original',
            'topic': 'list · sorted',
            'task': 'כתבו פונקציה בשם sorted_copy\nפרמטר אחד, בשם items - רשימה של מספרים\nהיא מחזירה זוג (tuple): רשימה חדשה וממוינת, והרשימה המקורית\nבלי שהיא השתנתה',
            'starter': "def sorted_copy(items):\n    '''return (a new sorted list, the untouched original)'''\n    # your lines go here\n\n\nprint(sorted_copy([3, 1, 2]))\n",
            'expect': 'return (a new sorted list, the untouched original)',
            'tests': [
                {'call': 'sorted_copy([3, 1, 2])', 'is': '([1, 2, 3], [3, 1, 2])'},
                {'call': 'sorted_copy([9, 8])', 'is': '([8, 9], [9, 8])'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש פונקציה מובנית שמחזירה רשימה חדשה וממוינת, בלי לגעת במקורית',
            'solution': 'def sorted_copy(items):\n    new_list = sorted(items)\n    return (new_list, items)\n\n\nprint(sorted_copy([3, 1, 2]))\n',
        },
        {
            'id': 'reverse_list',
            'title': 'Flip It Around',
            'topic': 'list · reverse',
            'task': 'כתבו פונקציה בשם reverse_list\nפרמטר אחד, בשם items - רשימה\nהיא הופכת את סדר הרשימה, ומחזירה אותה',
            'starter': "def reverse_list(items):\n    '''reverse items in place, return items'''\n    # your line goes here\n\n\nprint(reverse_list([1, 2, 3]))\n",
            'expect': 'reverse items in place, return items',
            'tests': [
                {'call': 'reverse_list([1, 2, 3])', 'is': '[3, 2, 1]'},
                {'call': 'reverse_list([9, 8, 7, 6])', 'is': '[6, 7, 8, 9]'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש לרשימה פעולה שהופכת את הסדר שלה במקום',
            'solution': 'def reverse_list(items):\n    items.reverse()\n    return items\n\n\nprint(reverse_list([1, 2, 3]))\n',
        },
        {
            'id': 'count_value',
            'title': 'How Many Times',
            'topic': 'list · count',
            'task': 'כתבו פונקציה בשם count_value\nשני פרמטרים: items (רשימה) ו-value\nהיא מחזירה כמה פעמים value מופיע ברשימה',
            'starter': "def count_value(items, value):\n    '''return how many times value appears in items'''\n    # your line goes here\n\n\nprint(count_value([1, 2, 2, 3, 2], 2))\n",
            'expect': 'return how many times value appears in items',
            'tests': [
                {'call': 'count_value([1, 2, 2, 3, 2], 2)', 'is': '3'},
                {'call': 'count_value([1, 2, 3], 9)', 'is': '0'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש לרשימה פעולה שסופרת כמה פעמים ערך מסוים מופיע בה',
            'solution': 'def count_value(items, value):\n    return items.count(value)\n\n\nprint(count_value([1, 2, 2, 3, 2], 2))\n',
        },
        {
            'id': 'index_of',
            'title': 'Where Is It',
            'topic': 'list · index',
            'task': 'כתבו פונקציה בשם index_of\nשני פרמטרים: items (רשימה) ו-value\nהיא מחזירה את המיקום הראשון של value ברשימה',
            'starter': "def index_of(items, value):\n    '''return the first index of value in items'''\n    # your line goes here\n\n\nprint(index_of([10, 20, 30], 20))\n",
            'expect': 'return the first index of value in items',
            'tests': [
                {'call': 'index_of([10, 20, 30], 20)', 'is': '1'},
                {'call': 'index_of([5, 6, 7], 5)', 'is': '0'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש לרשימה פעולה שמחזירה את המיקום הראשון של ערך',
            'solution': 'def index_of(items, value):\n    return items.index(value)\n\n\nprint(index_of([10, 20, 30], 20))\n',
        },
        {
            'id': 'unpack_sum',
            'title': 'Unpack And Add',
            'topic': 'tuple · unpacking',
            'task': 'כתבו פונקציה בשם unpack_sum\nפרמטר אחד, בשם point - tuple של שני מספרים\nפרקו אותו לשני משתנים בשורה אחת, והחזירו את הסכום שלהם',
            'starter': "def unpack_sum(point):\n    '''unpack point into two variables, return their sum'''\n    # your line goes here\n\n\nprint(unpack_sum((3, 4)))\n",
            'expect': 'unpack point into two variables, return their sum',
            'tests': [
                {'call': 'unpack_sum((3, 4))', 'is': '7'},
                {'call': 'unpack_sum((10, -2))', 'is': '8'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'אפשר לפרק tuple לשני משתנים בשורה אחת: x, y = point',
            'solution': 'def unpack_sum(point):\n    x, y = point\n    return x + y\n\n\nprint(unpack_sum((3, 4)))\n',
        },
        {
            'id': 'count_in_tuple',
            'title': 'Count In A Tuple',
            'topic': 'tuple · count',
            'task': 'כתבו פונקציה בשם count_in_tuple\nשני פרמטרים: t (tuple) ו-value\nהיא מחזירה כמה פעמים value מופיע ב-t',
            'starter': "def count_in_tuple(t, value):\n    '''return how many times value appears in t'''\n    # your line goes here\n\n\nprint(count_in_tuple((1, 2, 2, 3, 2), 2))\n",
            'expect': 'return how many times value appears in t',
            'tests': [
                {'call': 'count_in_tuple((1, 2, 2, 3, 2), 2)', 'is': '3'},
                {'call': 'count_in_tuple((1, 2, 3), 9)', 'is': '0'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'ל-tuple יש את אותה פעולת ספירה כמו לרשימה',
            'solution': 'def count_in_tuple(t, value):\n    return t.count(value)\n\n\nprint(count_in_tuple((1, 2, 2, 3, 2), 2))\n',
        },
        {
            'id': 'index_in_tuple',
            'title': 'Find In A Tuple',
            'topic': 'tuple · index',
            'task': 'כתבו פונקציה בשם index_in_tuple\nשני פרמטרים: t (tuple) ו-value\nהיא מחזירה את המיקום הראשון של value ב-t',
            'starter': "def index_in_tuple(t, value):\n    '''return the first index of value in t'''\n    # your line goes here\n\n\nprint(index_in_tuple((10, 20, 30), 30))\n",
            'expect': 'return the first index of value in t',
            'tests': [
                {'call': 'index_in_tuple((10, 20, 30), 30)', 'is': '2'},
                {'call': 'index_in_tuple((5, 6, 7), 6)', 'is': '1'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'ל-tuple יש את אותה פעולת חיפוש מיקום כמו לרשימה',
            'solution': 'def index_in_tuple(t, value):\n    return t.index(value)\n\n\nprint(index_in_tuple((10, 20, 30), 30))\n',
        },
        {
            'id': 'get_with_default',
            'title': 'Get, Safely',
            'topic': 'dict · get',
            'task': "כתבו פונקציה בשם get_with_default\nשני פרמטרים: d (מילון) ו-key\nהיא מחזירה את הערך של key במילון\nאם המפתח לא קיים, מחזירה את המחרוזת 'not found' - בלי לקרוס",
            'starter': "def get_with_default(d, key):\n    '''return d[key], or 'not found' if key is missing'''\n    # your line goes here\n\n\nprint(get_with_default({'a': 1, 'b': 2}, 'b'))\nprint(get_with_default({'a': 1, 'b': 2}, 'c'))\n",
            'expect': "return d[key], or 'not found' if key is missing",
            'tests': [
                {'call': "get_with_default({'a': 1, 'b': 2}, 'b')", 'is': '2'},
                {'call': "get_with_default({'a': 1, 'b': 2}, 'c')", 'is': "'not found'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'get מקבלת ערך ברירת מחדל כפרמטר שני, למקרה שהמפתח לא קיים',
            'solution': "def get_with_default(d, key):\n    return d.get(key, 'not found')\n\n\nprint(get_with_default({'a': 1, 'b': 2}, 'b'))\nprint(get_with_default({'a': 1, 'b': 2}, 'c'))\n",
        },
        {
            'id': 'sorted_keys',
            'title': 'All The Keys, Sorted',
            'topic': 'dict · keys',
            'task': 'כתבו פונקציה בשם sorted_keys\nפרמטר אחד, בשם d - מילון\nהיא מחזירה רשימה ממוינת של כל המפתחות במילון',
            'starter': "def sorted_keys(d):\n    '''return a sorted list of d's keys'''\n    # your line goes here\n\n\nprint(sorted_keys({'b': 1, 'a': 2, 'c': 3}))\n",
            'expect': "return a sorted list of d's keys",
            'tests': [
                {'call': "sorted_keys({'b': 1, 'a': 2, 'c': 3})", 'is': "['a', 'b', 'c']"},
                {'call': "sorted_keys({'z': 1})", 'is': "['z']"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'd.keys() נותנת את כל המפתחות - מיינו אותם עם sorted',
            'solution': "def sorted_keys(d):\n    return sorted(d.keys())\n\n\nprint(sorted_keys({'b': 1, 'a': 2, 'c': 3}))\n",
        },
        {
            'id': 'sum_values',
            'title': 'Sum All The Values',
            'topic': 'dict · values',
            'task': 'כתבו פונקציה בשם sum_values\nפרמטר אחד, בשם d - מילון שהערכים בו הם מספרים\nהיא מחזירה את הסכום של כל הערכים במילון',
            'starter': "def sum_values(d):\n    '''return the sum of d's values'''\n    # your line goes here\n\n\nprint(sum_values({'a': 10, 'b': 20, 'c': 5}))\n",
            'expect': "return the sum of d's values",
            'tests': [
                {'call': "sum_values({'a': 10, 'b': 20, 'c': 5})", 'is': '35'},
                {'call': "sum_values({'x': 1})", 'is': '1'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'd.values() נותנת את כל הערכים - יש פונקציה שמחברת רשימה של מספרים',
            'solution': "def sum_values(d):\n    return sum(d.values())\n\n\nprint(sum_values({'a': 10, 'b': 20, 'c': 5}))\n",
        },
        {
            'id': 'set_key',
            'title': 'Add A Key',
            'topic': 'dict · assignment',
            'task': 'כתבו פונקציה בשם set_key\nשלושה פרמטרים: d (מילון), key ו-value\nהיא קובעת ש-d[key] שווה ל-value, ומחזירה את המילון',
            'starter': "def set_key(d, key, value):\n    '''set d[key] = value, return d'''\n    # your line goes here\n\n\nprint(set_key({'a': 1}, 'b', 2))\n",
            'expect': 'set d[key] = value, return d',
            'tests': [
                {'call': "set_key({'a': 1}, 'b', 2)", 'is': "{'a': 1, 'b': 2}"},
                {'call': "set_key({}, 'k', 9)", 'is': "{'k': 9}"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'אפשר לקבוע ערך למפתח במילון עם d[key] = value, גם אם הוא עוד לא קיים',
            'solution': "def set_key(d, key, value):\n    d[key] = value\n    return d\n\n\nprint(set_key({'a': 1}, 'b', 2))\n",
        },
        {
            'id': 'pop_key',
            'title': 'Remove A Key',
            'topic': 'dict · pop',
            'task': 'כתבו פונקציה בשם pop_key\nשני פרמטרים: d (מילון) ו-key\nהיא מסירה מהמילון את המפתח key, ומחזירה את המילון',
            'starter': "def pop_key(d, key):\n    '''remove key from d, return d'''\n    # your line goes here\n\n\nprint(pop_key({'a': 1, 'b': 2}, 'a'))\n",
            'expect': 'remove key from d, return d',
            'tests': [
                {'call': "pop_key({'a': 1, 'b': 2}, 'a')", 'is': "{'b': 2}"},
                {'call': "pop_key({'x': 1, 'y': 2}, 'y')", 'is': "{'x': 1}"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש למילון פעולת pop, בדיוק כמו לרשימה, אבל עם מפתח ולא מיקום',
            'solution': "def pop_key(d, key):\n    d.pop(key)\n    return d\n\n\nprint(pop_key({'a': 1, 'b': 2}, 'a'))\n",
        },
        {
            'id': 'union_sorted',
            'title': 'Everything From Both',
            'topic': 'set · union',
            'task': 'כתבו פונקציה בשם union_sorted\nשני פרמטרים: a ו-b - שני sets\nהיא מחזירה רשימה ממוינת של האיחוד (union) של שני הקבוצות -\nכל איבר שנמצא באחת מהן, לפחות',
            'starter': "def union_sorted(a, b):\n    '''return a sorted list of the union of a and b'''\n    # your line goes here\n\n\nprint(union_sorted({1, 2, 3}, {3, 4, 5}))\n",
            'expect': 'return a sorted list of the union of a and b',
            'tests': [
                {'call': 'union_sorted({1, 2, 3}, {3, 4, 5})', 'is': '[1, 2, 3, 4, 5]'},
                {'call': 'union_sorted({1}, {2})', 'is': '[1, 2]'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'האופרטור | על שני sets נותן את כל האיברים משניהם יחד',
            'solution': 'def union_sorted(a, b):\n    return sorted(a | b)\n\n\nprint(union_sorted({1, 2, 3}, {3, 4, 5}))\n',
        },
        {
            'id': 'intersection_sorted',
            'title': 'Only What They Share',
            'topic': 'set · intersection',
            'task': 'כתבו פונקציה בשם intersection_sorted\nשני פרמטרים: a ו-b - שני sets\nהיא מחזירה רשימה ממוינת של החיתוך (intersection) של שתי הקבוצות -\nרק איברים שנמצאים בשתיהן',
            'starter': "def intersection_sorted(a, b):\n    '''return a sorted list of the intersection of a and b'''\n    # your line goes here\n\n\nprint(intersection_sorted({1, 2, 3, 4}, {3, 4, 5}))\n",
            'expect': 'return a sorted list of the intersection of a and b',
            'tests': [
                {'call': 'intersection_sorted({1, 2, 3, 4}, {3, 4, 5})', 'is': '[3, 4]'},
                {'call': 'intersection_sorted({1, 2}, {3, 4})', 'is': '[]'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'האופרטור & על שני sets נותן רק את האיברים המשותפים',
            'solution': 'def intersection_sorted(a, b):\n    return sorted(a & b)\n\n\nprint(intersection_sorted({1, 2, 3, 4}, {3, 4, 5}))\n',
        },
        {
            'id': 'difference_sorted',
            'title': 'What Only The First One Has',
            'topic': 'set · difference',
            'task': 'כתבו פונקציה בשם difference_sorted\nשני פרמטרים: a ו-b - שני sets\nהיא מחזירה רשימה ממוינת של ההפרש (difference) - כל איבר שנמצא\nב-a אבל לא ב-b',
            'starter': "def difference_sorted(a, b):\n    '''return a sorted list of a's items that are not in b'''\n    # your line goes here\n\n\nprint(difference_sorted({1, 2, 3, 4}, {3, 4}))\n",
            'expect': "return a sorted list of a's items that are not in b",
            'tests': [
                {'call': 'difference_sorted({1, 2, 3, 4}, {3, 4})', 'is': '[1, 2]'},
                {'call': 'difference_sorted({1, 2}, {1, 2})', 'is': '[]'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'האופרטור - על שני sets נותן איברים שיש רק בראשון',
            'solution': 'def difference_sorted(a, b):\n    return sorted(a - b)\n\n\nprint(difference_sorted({1, 2, 3, 4}, {3, 4}))\n',
        },
        {
            'id': 'add_to_set',
            'title': 'Add To A Set',
            'topic': 'set · add',
            'task': 'כתבו פונקציה בשם add_to_set\nשני פרמטרים: s (set) ו-item\nהיא מוסיפה את item לקבוצה, ומחזירה רשימה ממוינת של הקבוצה',
            'starter': "def add_to_set(s, item):\n    '''add item to s, return a sorted list of s'''\n    # your line goes here\n\n\nprint(add_to_set({1, 2, 3}, 4))\n",
            'expect': 'add item to s, return a sorted list of s',
            'tests': [
                {'call': 'add_to_set({1, 2, 3}, 4)', 'is': '[1, 2, 3, 4]'},
                {'call': 'add_to_set({1, 2}, 2)', 'is': '[1, 2]'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש ל-set פעולה שמוסיפה איבר, בדיוק כמו append לרשימה',
            'solution': 'def add_to_set(s, item):\n    s.add(item)\n    return sorted(s)\n\n\nprint(add_to_set({1, 2, 3}, 4))\n',
        },
        {
            'id': 'join_with_space',
            'title': 'Join Into One Sentence',
            'topic': 'string · join',
            'task': 'כתבו פונקציה בשם join_with_space\nפרמטר אחד, בשם words - רשימה של מילים\nהיא מחזירה את כל המילים מחוברות למחרוזת אחת, עם רווח בין כל שתיים',
            'starter': "def join_with_space(words):\n    '''join words into one string, separated by spaces'''\n    # your line goes here\n\n\nprint(join_with_space(['I', 'love', 'Python']))\n",
            'expect': 'join words into one string, separated by spaces',
            'tests': [
                {'call': "join_with_space(['I', 'love', 'Python'])", 'is': "'I love Python'"},
                {'call': "join_with_space(['hi'])", 'is': "'hi'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': "' '.join(words) מחברת רשימת מילים למחרוזת אחת, עם רווח בין כל שתיים",
            'solution': "def join_with_space(words):\n    return ' '.join(words)\n\n\nprint(join_with_space(['I', 'love', 'Python']))\n",
        },
        {
            'id': 'split_into_words',
            'title': 'Split Into Words',
            'topic': 'string · split',
            'task': 'כתבו פונקציה בשם split_into_words\nפרמטר אחד, בשם sentence - מחרוזת\nהיא מחזירה רשימה של כל המילים במשפט',
            'starter': "def split_into_words(sentence):\n    '''split sentence into a list of words'''\n    # your line goes here\n\n\nprint(split_into_words('hello there world'))\n",
            'expect': 'split sentence into a list of words',
            'tests': [
                {'call': "split_into_words('hello there world')", 'is': "['hello', 'there', 'world']"},
                {'call': "split_into_words('one')", 'is': "['one']"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש למחרוזת פעולה שמפרקת אותה לרשימת מילים, לפי רווחים',
            'solution': "def split_into_words(sentence):\n    return sentence.split()\n\n\nprint(split_into_words('hello there world'))\n",
        },
        {
            'id': 'replace_letter',
            'title': 'Swap A Letter',
            'topic': 'string · replace',
            'task': 'כתבו פונקציה בשם replace_letter\nשלושה פרמטרים: word, old ו-new\nהיא מחזירה את word אחרי שכל הופעה של old הוחלפה ב-new',
            'starter': "def replace_letter(word, old, new):\n    '''return word with every old replaced by new'''\n    # your line goes here\n\n\nprint(replace_letter('banana', 'a', 'o'))\n",
            'expect': 'return word with every old replaced by new',
            'tests': [
                {'call': "replace_letter('banana', 'a', 'o')", 'is': "'bonono'"},
                {'call': "replace_letter('hello', 'l', 'L')", 'is': "'heLLo'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש למחרוזת פעולה שמחליפה כל הופעה של תת-מחרוזת אחת באחרת',
            'solution': "def replace_letter(word, old, new):\n    return word.replace(old, new)\n\n\nprint(replace_letter('banana', 'a', 'o'))\n",
        },
        {
            'id': 'greet',
            'title': 'Say It Back',
            'topic': 'functions · strings · return',
            'task': "כתבו פונקציה בשם greet\nהיא לא מקבלת אף פרמטר\nהיא מחזירה בדיוק את הטקסט הזה: 'Hello World'",
            'starter': "def greet():\n    '''return the greeting below, exactly'''\n    # your line goes here\n\n\nprint(greet())\n",
            'expect': 'return the greeting below, exactly',
            'tests': [
                {'call': 'greet()', 'is': "'Hello World'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'לא print - return\nprint רק מראה לכם על המסך; return מחזיר את הערך כדי שהתוכנית תוכל להשתמש בו',
            'solution': "def greet():\n    return 'Hello World'\n\n\nprint(greet())\n",
        },
        {
            'id': 'shout_upper',
            'title': 'Shout It',
            'topic': 'functions · strings · methods',
            'task': 'כתבו פונקציה בשם shout\nפרמטר אחד, בשם word\nהיא מחזירה את המילה באותיות גדולות',
            'starter': "def shout(word):\n    '''return word in UPPERCASE'''\n    # your line goes here\n\n\nprint(shout('hello'))\n",
            'expect': 'return word in UPPERCASE',
            'tests': [
                {'call': "shout('hello')", 'is': "'HELLO'"},
                {'call': "shout('Python')", 'is': "'PYTHON'"},
                {'call': "shout('abc')", 'is': "'ABC'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש למחרוזת פעולה שהופכת אותה לאותיות גדולות - חפשו אותה, היא נקראת בשם שמתאר בדיוק מה שהיא עושה',
            'solution': "def shout(word):\n    return word.upper()\n\n\nprint(shout('hello'))\n",
        },
        {
            'id': 'shout_lower',
            'title': 'Whisper It',
            'topic': 'functions · strings · methods',
            'task': 'כתבו פונקציה בשם whisper\nפרמטר אחד, בשם word\nהיא מחזירה את המילה באותיות קטנות',
            'starter': "def whisper(word):\n    '''return word in lowercase'''\n    # your line goes here\n\n\nprint(whisper('HELLO'))\n",
            'expect': 'return word in lowercase',
            'tests': [
                {'call': "whisper('HELLO')", 'is': "'hello'"},
                {'call': "whisper('Python')", 'is': "'python'"},
                {'call': "whisper('ABC')", 'is': "'abc'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש למחרוזת פעולה שהופכת אותה לאותיות קטנות - ההפך המדויק מהשאלה הקודמת',
            'solution': "def whisper(word):\n    return word.lower()\n\n\nprint(whisper('HELLO'))\n",
        },
        {
            'id': 'shout_title',
            'title': 'Title It',
            'topic': 'functions · strings · methods',
            'task': 'כתבו פונקציה בשם title_case\nפרמטר אחד, בשם words\nהיא מחזירה את הטקסט כשכל מילה בו מתחילה באות גדולה',
            'starter': "def title_case(words):\n    '''return words in Title Case'''\n    # your line goes here\n\n\nprint(title_case('hello world'))\n",
            'expect': 'return words in Title Case',
            'tests': [
                {'call': "title_case('hello world')", 'is': "'Hello World'"},
                {'call': "title_case('python code')", 'is': "'Python Code'"},
                {'call': "title_case('abc')", 'is': "'Abc'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש למחרוזת פעולה שמתאימה בול לתיאור הזה - חפשו משהו שקשור למילה title',
            'solution': "def title_case(words):\n    return words.title()\n\n\nprint(title_case('hello world'))\n",
        },
        {
            'id': 'full_name',
            'title': 'Put It Together',
            'topic': 'functions · strings · concatenation',
            'task': 'כתבו פונקציה בשם full_name\nשני פרמטרים: first ו-last\nהיא מחזירה אותם ביחד, כשם אחד, עם רווח אחד ביניהם',
            'starter': "def full_name(first, last):\n    '''return first and last joined by one space'''\n    # your line goes here\n\n\nprint(full_name('Ada', 'Lovelace'))\n",
            'expect': 'return first and last joined by one space',
            'tests': [
                {'call': "full_name('Ada', 'Lovelace')", 'is': "'Ada Lovelace'"},
                {'call': "full_name('Guido', 'Rossum')", 'is': "'Guido Rossum'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'אפשר לחבר מחרוזות עם + בדיוק כמו מספרים - אל תשכחו את הרווח בין השתיים',
            'solution': "def full_name(first, last):\n    return first + ' ' + last\n\n\nprint(full_name('Ada', 'Lovelace'))\n",
        },
        {
            'id': 'string_length',
            'title': 'How Long Is It',
            'topic': 'string · len',
            'task': 'כתבו פונקציה בשם string_length\nפרמטר אחד, בשם word\nהיא מחזירה כמה אותיות יש במילה',
            'starter': "def string_length(word):\n    '''return how many characters are in word'''\n    # your line goes here\n\n\nprint(string_length('hello'))\n",
            'expect': 'return how many characters are in word',
            'tests': [
                {'call': "string_length('hello')", 'is': '5'},
                {'call': "string_length('')", 'is': '0'},
                {'call': "string_length('python')", 'is': '6'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש פונקציה מובנית שמחזירה כמה איברים יש במחרוזת - היא לא שיטה על המחרוזת אלא פונקציה שמקבלת אותה כפרמטר',
            'solution': "def string_length(word):\n    return len(word)\n\n\nprint(string_length('hello'))\n",
        },
        {
            'id': 'first_letter',
            'title': 'The First Letter',
            'topic': 'string · indexing',
            'task': 'כתבו פונקציה בשם first_letter\nפרמטר אחד, בשם word\nהיא מחזירה את האות הראשונה במילה',
            'starter': "def first_letter(word):\n    '''return the first character of word'''\n    # your line goes here\n\n\nprint(first_letter('banana'))\n",
            'expect': 'return the first character of word',
            'tests': [
                {'call': "first_letter('banana')", 'is': "'b'"},
                {'call': "first_letter('zoo')", 'is': "'z'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'אפשר לגשת לתו בודד במחרוזת עם סוגריים מרובעים ומיקום - המיקום הראשון הוא 0',
            'solution': "def first_letter(word):\n    return word[0]\n\n\nprint(first_letter('banana'))\n",
        },
        {
            'id': 'last_three',
            'title': 'The Last Three Letters',
            'topic': 'string · slicing',
            'task': 'כתבו פונקציה בשם last_three\nפרמטר אחד, בשם word\nהיא מחזירה את שלוש האותיות האחרונות במילה',
            'starter': "def last_three(word):\n    '''return the last three characters of word'''\n    # your line goes here\n\n\nprint(last_three('banana'))\n",
            'expect': 'return the last three characters of word',
            'tests': [
                {'call': "last_three('banana')", 'is': "'ana'"},
                {'call': "last_three('hi there')", 'is': "'ere'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'חיתוך (slicing) עם מספר שלילי סופר מהסוף - word[-3:] לוקח מ-3 מהסוף עד הסוף',
            'solution': "def last_three(word):\n    return word[-3:]\n\n\nprint(last_three('banana'))\n",
        },
        {
            'id': 'count_substring',
            'title': 'Count The Occurrences',
            'topic': 'string · count',
            'task': 'כתבו פונקציה בשם count_substring\nשני פרמטרים: word ו-sub\nהיא מחזירה כמה פעמים sub מופיע בתוך word',
            'starter': "def count_substring(word, sub):\n    '''return how many times sub appears in word'''\n    # your line goes here\n\n\nprint(count_substring('banana', 'a'))\n",
            'expect': 'return how many times sub appears in word',
            'tests': [
                {'call': "count_substring('banana', 'a')", 'is': '3'},
                {'call': "count_substring('banana', 'na')", 'is': '2'},
                {'call': "count_substring('hello', 'z')", 'is': '0'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש למחרוזת פעולה שסופרת כמה פעמים תת-מחרוזת מופיעה בה',
            'solution': "def count_substring(word, sub):\n    return word.count(sub)\n\n\nprint(count_substring('banana', 'a'))\n",
        },
        {
            'id': 'starts_with',
            'title': 'Does It Start With',
            'topic': 'string · startswith',
            'task': 'כתבו פונקציה בשם starts_with\nשני פרמטרים: word ו-prefix\nהיא מחזירה True אם word מתחיל ב-prefix, אחרת False',
            'starter': "def starts_with(word, prefix):\n    '''return True if word starts with prefix'''\n    # your line goes here\n\n\nprint(starts_with('banana', 'ban'))\n",
            'expect': 'return True if word starts with prefix',
            'tests': [
                {'call': "starts_with('banana', 'ban')", 'is': 'True'},
                {'call': "starts_with('banana', 'app')", 'is': 'False'},
                {'call': "starts_with('python', 'py')", 'is': 'True'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש למחרוזת פעולה שבודקת אם היא מתחילה ברצף תווים מסוים',
            'solution': "def starts_with(word, prefix):\n    return word.startswith(prefix)\n\n\nprint(starts_with('banana', 'ban'))\n",
        },
        {
            'id': 'list_length',
            'title': 'How Many Items',
            'topic': 'list · len',
            'task': 'כתבו פונקציה בשם list_length\nפרמטר אחד, בשם items - רשימה\nהיא מחזירה כמה איברים יש ברשימה',
            'starter': "def list_length(items):\n    '''return how many items are in items'''\n    # your line goes here\n\n\nprint(list_length([1, 2, 3, 4]))\n",
            'expect': 'return how many items are in items',
            'tests': [
                {'call': 'list_length([1, 2, 3, 4])', 'is': '4'},
                {'call': 'list_length([])', 'is': '0'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'אותה פונקציה מובנית שסופרת אורך של מחרוזת עובדת גם על רשימה',
            'solution': 'def list_length(items):\n    return len(items)\n\n\nprint(list_length([1, 2, 3, 4]))\n',
        },
        {
            'id': 'first_item',
            'title': 'The First Item',
            'topic': 'list · indexing',
            'task': 'כתבו פונקציה בשם first_item\nפרמטר אחד, בשם items - רשימה\nהיא מחזירה את האיבר הראשון ברשימה',
            'starter': "def first_item(items):\n    '''return the first item in items'''\n    # your line goes here\n\n\nprint(first_item([10, 20, 30]))\n",
            'expect': 'return the first item in items',
            'tests': [
                {'call': 'first_item([10, 20, 30])', 'is': '10'},
                {'call': "first_item(['a', 'b'])", 'is': "'a'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'המיקום הראשון ברשימה הוא 0, בדיוק כמו במחרוזת',
            'solution': 'def first_item(items):\n    return items[0]\n\n\nprint(first_item([10, 20, 30]))\n',
        },
        {
            'id': 'last_item',
            'title': 'The Last Item',
            'topic': 'list · indexing',
            'task': 'כתבו פונקציה בשם last_item\nפרמטר אחד, בשם items - רשימה\nהיא מחזירה את האיבר האחרון ברשימה',
            'starter': "def last_item(items):\n    '''return the last item in items'''\n    # your line goes here\n\n\nprint(last_item([10, 20, 30]))\n",
            'expect': 'return the last item in items',
            'tests': [
                {'call': 'last_item([10, 20, 30])', 'is': '30'},
                {'call': "last_item(['a', 'b'])", 'is': "'b'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'מיקום -1 הוא תמיד האיבר האחרון, בלי לדעת כמה איברים יש',
            'solution': 'def last_item(items):\n    return items[-1]\n\n\nprint(last_item([10, 20, 30]))\n',
        },
        {
            'id': 'list_sum',
            'title': 'Add Them All Up',
            'topic': 'list · sum',
            'task': 'כתבו פונקציה בשם list_sum\nפרמטר אחד, בשם items - רשימה של מספרים\nהיא מחזירה את הסכום של כל המספרים ברשימה',
            'starter': "def list_sum(items):\n    '''return the sum of all the numbers in items'''\n    # your line goes here\n\n\nprint(list_sum([1, 2, 3, 4]))\n",
            'expect': 'return the sum of all the numbers in items',
            'tests': [
                {'call': 'list_sum([1, 2, 3, 4])', 'is': '10'},
                {'call': 'list_sum([10])', 'is': '10'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש פונקציה מובנית שמקבלת רשימה של מספרים ומחזירה את סכום כולם',
            'solution': 'def list_sum(items):\n    return sum(items)\n\n\nprint(list_sum([1, 2, 3, 4]))\n',
        },
        {
            'id': 'list_max',
            'title': 'The Biggest One',
            'topic': 'list · max',
            'task': 'כתבו פונקציה בשם list_max\nפרמטר אחד, בשם items - רשימה של מספרים\nהיא מחזירה את המספר הגדול ביותר ברשימה',
            'starter': "def list_max(items):\n    '''return the biggest number in items'''\n    # your line goes here\n\n\nprint(list_max([3, 9, 1]))\n",
            'expect': 'return the biggest number in items',
            'tests': [
                {'call': 'list_max([3, 9, 1])', 'is': '9'},
                {'call': 'list_max([-5, -2, -9])', 'is': '-2'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש פונקציה מובנית שמחזירה את הערך הגדול ביותר ברשימה',
            'solution': 'def list_max(items):\n    return max(items)\n\n\nprint(list_max([3, 9, 1]))\n',
        },
        {
            'id': 'list_min',
            'title': 'The Smallest One',
            'topic': 'list · min',
            'task': 'כתבו פונקציה בשם list_min\nפרמטר אחד, בשם items - רשימה של מספרים\nהיא מחזירה את המספר הקטן ביותר ברשימה',
            'starter': "def list_min(items):\n    '''return the smallest number in items'''\n    # your line goes here\n\n\nprint(list_min([3, 9, 1]))\n",
            'expect': 'return the smallest number in items',
            'tests': [
                {'call': 'list_min([3, 9, 1])', 'is': '1'},
                {'call': 'list_min([-5, -2, -9])', 'is': '-9'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש פונקציה מובנית שמחזירה את הערך הקטן ביותר ברשימה',
            'solution': 'def list_min(items):\n    return min(items)\n\n\nprint(list_min([3, 9, 1]))\n',
        },
        {
            'id': 'combine_lists',
            'title': 'Combine Two Lists',
            'topic': 'list · concatenation',
            'task': 'כתבו פונקציה בשם combine_lists\nשני פרמטרים: a ו-b - שתי רשימות\nהיא מחזירה רשימה אחת, עם כל האיברים של a ואז כל האיברים של b',
            'starter': "def combine_lists(a, b):\n    '''return a and b joined into one list'''\n    # your line goes here\n\n\nprint(combine_lists([1, 2], [3, 4]))\n",
            'expect': 'return a and b joined into one list',
            'tests': [
                {'call': 'combine_lists([1, 2], [3, 4])', 'is': '[1, 2, 3, 4]'},
                {'call': 'combine_lists([], [1])', 'is': '[1]'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'אפשר לחבר שתי רשימות עם + בדיוק כמו מחרוזות',
            'solution': 'def combine_lists(a, b):\n    return a + b\n\n\nprint(combine_lists([1, 2], [3, 4]))\n',
        },
        {
            'id': 'is_in_list',
            'title': 'Is It There',
            'topic': 'list · in',
            'task': 'כתבו פונקציה בשם is_in_list\nשני פרמטרים: items (רשימה) ו-value\nהיא מחזירה True אם value נמצא ברשימה, אחרת False',
            'starter': "def is_in_list(items, value):\n    '''return True if value is in items'''\n    # your line goes here\n\n\nprint(is_in_list([1, 2, 3], 2))\n",
            'expect': 'return True if value is in items',
            'tests': [
                {'call': 'is_in_list([1, 2, 3], 2)', 'is': 'True'},
                {'call': 'is_in_list([1, 2, 3], 9)', 'is': 'False'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'המילה השמורה in בודקת אם ערך נמצא בתוך רשימה, ומחזירה True או False',
            'solution': 'def is_in_list(items, value):\n    return value in items\n\n\nprint(is_in_list([1, 2, 3], 2))\n',
        },
        {
            'id': 'absolute_value',
            'title': 'Always Positive',
            'topic': 'numbers · abs',
            'task': 'כתבו פונקציה בשם absolute_value\nפרמטר אחד, בשם n\nהיא מחזירה את הערך המוחלט של n - תמיד חיובי או אפס',
            'starter': "def absolute_value(n):\n    '''return the absolute value of n'''\n    # your line goes here\n\n\nprint(absolute_value(-7))\n",
            'expect': 'return the absolute value of n',
            'tests': [
                {'call': 'absolute_value(-7)', 'is': '7'},
                {'call': 'absolute_value(7)', 'is': '7'},
                {'call': 'absolute_value(0)', 'is': '0'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש פונקציה מובנית שמחזירה את הערך המוחלט של מספר - היא לא שיטה, היא מקבלת את המספר כפרמטר',
            'solution': 'def absolute_value(n):\n    return abs(n)\n\n\nprint(absolute_value(-7))\n',
        },
        {
            'id': 'round_number',
            'title': 'Round It',
            'topic': 'numbers · round',
            'task': 'כתבו פונקציה בשם round_number\nשני פרמטרים: n ו-digits\nהיא מחזירה את n מעוגל למספר הספרות digits אחרי הנקודה',
            'starter': "def round_number(n, digits):\n    '''return n rounded to digits decimal places'''\n    # your line goes here\n\n\nprint(round_number(3.14159, 2))\n",
            'expect': 'return n rounded to digits decimal places',
            'tests': [
                {'call': 'round_number(3.14159, 2)', 'is': '3.14'},
                {'call': 'round_number(2.5, 0)', 'is': '2.0'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'יש פונקציה מובנית לעיגול שמקבלת את המספר ואת כמות הספרות כשני פרמטרים',
            'solution': 'def round_number(n, digits):\n    return round(n, digits)\n\n\nprint(round_number(3.14159, 2))\n',
        },
        {
            'id': 'in_range',
            'title': 'Inside The Range',
            'topic': 'if · and',
            'task': 'כתבו פונקציה בשם in_range\nשלושה פרמטרים: n, low ו-high\nהיא מחזירה True אם n נמצא בין low ל-high (כולל את שניהם), אחרת False\nהשתמשו בתנאי אחד עם and, לא שני if נפרדים',
            'starter': "def in_range(n, low, high):\n    '''return True if n is between low and high, inclusive'''\n    # your line goes here\n\n\nprint(in_range(5, 1, 10))\n",
            'expect': 'return True if n is between low and high, inclusive',
            'tests': [
                {'call': 'in_range(5, 1, 10)', 'is': 'True'},
                {'call': 'in_range(15, 1, 10)', 'is': 'False'},
                {'call': 'in_range(1, 1, 10)', 'is': 'True'},
            ],
            'require': ['def', 'return', 'and'],
            'forbid': [],
            'hint': 'אפשר לשרשר שתי השוואות עם and לתנאי אחד: low <= n and n <= high, או אפילו low <= n <= high',
            'solution': 'def in_range(n, low, high):\n    return n >= low and n <= high\n\n\nprint(in_range(5, 1, 10))\n',
        },
        {
            'id': 'key_exists',
            'title': 'Is The Key There',
            'topic': 'dict · in',
            'task': 'כתבו פונקציה בשם key_exists\nשני פרמטרים: d (מילון) ו-key\nהיא מחזירה True אם key נמצא במילון, אחרת False',
            'starter': "def key_exists(d, key):\n    '''return True if key is in d'''\n    # your line goes here\n\n\nprint(key_exists({'a': 1}, 'a'))\n",
            'expect': 'return True if key is in d',
            'tests': [
                {'call': "key_exists({'a': 1}, 'a')", 'is': 'True'},
                {'call': "key_exists({'a': 1}, 'b')", 'is': 'False'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'המילה השמורה in בודקת גם אם מפתח נמצא במילון',
            'solution': "def key_exists(d, key):\n    return key in d\n\n\nprint(key_exists({'a': 1}, 'a'))\n",
        },
        {
            'id': 'item_in_set',
            'title': 'Is It In The Set',
            'topic': 'set · in',
            'task': 'כתבו פונקציה בשם item_in_set\nשני פרמטרים: s (set) ו-item\nהיא מחזירה True אם item נמצא בקבוצה, אחרת False',
            'starter': "def item_in_set(s, item):\n    '''return True if item is in s'''\n    # your line goes here\n\n\nprint(item_in_set({1, 2, 3}, 2))\n",
            'expect': 'return True if item is in s',
            'tests': [
                {'call': 'item_in_set({1, 2, 3}, 2)', 'is': 'True'},
                {'call': 'item_in_set({1, 2, 3}, 9)', 'is': 'False'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'המילה השמורה in עובדת גם על set, בדיוק כמו על רשימה',
            'solution': 'def item_in_set(s, item):\n    return item in s\n\n\nprint(item_in_set({1, 2, 3}, 2))\n',
        },
        {
            'id': 'make_point',
            'title': 'Make A Pair',
            'topic': 'tuple · creation',
            'task': 'כתבו פונקציה בשם make_point\nשני פרמטרים: x ו-y\nהיא מחזירה אותם כ-tuple אחד: (x, y)',
            'starter': "def make_point(x, y):\n    '''return x and y as one tuple: (x, y)'''\n    # your line goes here\n\n\nprint(make_point(3, 4))\n",
            'expect': 'return x and y as one tuple: (x, y)',
            'tests': [
                {'call': 'make_point(3, 4)', 'is': '(3, 4)'},
                {'call': 'make_point(0, 0)', 'is': '(0, 0)'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'כדי להחזיר tuple, פשוט שימו את שני הערכים בסוגריים עגולים, מופרדים בפסיק',
            'solution': 'def make_point(x, y):\n    return (x, y)\n\n\nprint(make_point(3, 4))\n',
        },
    ],

    # ============================================================== MEDIUM
    'medium': [
        {
            'id': 'nested_loop_sum',
            'title': 'Sum Every Number, Everywhere',
            'topic': 'nested for loops',
            'task': 'כתבו פונקציה בשם nested_loop_sum\nפרמטר אחד, בשם rows - רשימה של רשימות של מספרים\nהיא מחזירה את הסכום של כל המספרים, בכל השורות יחד\nעברו על השורות עם לולאת for, ובתוך כל שורה עוד לולאת for',
            'starter': "def nested_loop_sum(rows):\n    '''return the sum of every number in every row'''\n    # your lines go here\n\n\nprint(nested_loop_sum([[1, 2, 3], [4, 5], [6]]))\n",
            'expect': 'return the sum of every number in every row',
            'tests': [
                {'call': 'nested_loop_sum([[1, 2, 3], [4, 5], [6]])', 'is': '21'},
                {'call': 'nested_loop_sum([[1], [2], [3]])', 'is': '6'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'hint': 'לולאת for חיצונית עוברת על השורות, ולולאת for פנימית עוברת על המספרים בכל שורה',
            'solution': 'def nested_loop_sum(rows):\n    total = 0\n    for row in rows:\n        for n in row:\n            total += n\n    return total\n\n\nprint(nested_loop_sum([[1, 2, 3], [4, 5], [6]]))\n',
        },
        {
            'id': 'squares_list',
            'title': 'Square Every Number',
            'topic': 'list comprehension',
            'task': 'כתבו פונקציה בשם squares_list\nפרמטר אחד, בשם numbers - רשימה של מספרים\nהיא מחזירה רשימה חדשה, עם הריבוע של כל מספר\nכתבו את זה כ-list comprehension, בשורה אחת',
            'starter': "def squares_list(numbers):\n    '''return a new list with each number squared'''\n    # your line goes here\n\n\nprint(squares_list([1, 2, 3, 4]))\n",
            'expect': 'return a new list with each number squared',
            'tests': [
                {'call': 'squares_list([1, 2, 3, 4])', 'is': '[1, 4, 9, 16]'},
                {'call': 'squares_list([0, 5])', 'is': '[0, 25]'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'hint': 'list comprehension: [ביטוי for משתנה in רשימה] - הביטוי כאן הוא n ** 2',
            'solution': 'def squares_list(numbers):\n    return [n ** 2 for n in numbers]\n\n\nprint(squares_list([1, 2, 3, 4]))\n',
        },
        {
            'id': 'evens_only',
            'title': 'Just The Even Ones',
            'topic': 'list comprehension · if',
            'task': 'כתבו פונקציה בשם evens_only\nפרמטר אחד, בשם numbers - רשימה של מספרים\nהיא מחזירה רשימה חדשה עם רק המספרים הזוגיים\nכתבו את זה כ-list comprehension עם תנאי, בשורה אחת',
            'starter': "def evens_only(numbers):\n    '''return a new list with only the even numbers'''\n    # your line goes here\n\n\nprint(evens_only([1, 2, 3, 4, 5, 6]))\n",
            'expect': 'return a new list with only the even numbers',
            'tests': [
                {'call': 'evens_only([1, 2, 3, 4, 5, 6])', 'is': '[2, 4, 6]'},
                {'call': 'evens_only([1, 3, 5])', 'is': '[]'},
            ],
            'require': ['def', 'return', 'for', 'if'],
            'forbid': [],
            'hint': 'list comprehension עם תנאי: [ביטוי for משתנה in רשימה if תנאי]',
            'solution': 'def evens_only(numbers):\n    return [n for n in numbers if n % 2 == 0]\n\n\nprint(evens_only([1, 2, 3, 4, 5, 6]))\n',
        },
        {
            'id': 'greet_with_default',
            'title': 'Greet, With A Default',
            'topic': 'default parameters · f-strings',
            'task': "כתבו פונקציה בשם greet_with_default\nפרמטר אחד, בשם name, עם ערך ברירת מחדל 'Guest'\nהיא מחזירה 'Hello, ' ואז השם ואז '!' - למשל 'Hello, Dana!'\nהשתמשו ב-f-string",
            'starter': "def greet_with_default(name='Guest'):\n    '''return a greeting for name (default 'Guest')'''\n    # your line goes here\n\n\nprint(greet_with_default())\nprint(greet_with_default('Dana'))\n",
            'expect': "return a greeting for name (default 'Guest')",
            'tests': [
                {'call': 'greet_with_default()', 'is': "'Hello, Guest!'"},
                {'call': "greet_with_default('Dana')", 'is': "'Hello, Dana!'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': "כתבו def greet_with_default(name='Guest') - ערך ברירת המחדל נכתב ישר בהגדרת הפרמטר",
            'solution': "def greet_with_default(name='Guest'):\n    return f'Hello, {name}!'\n\n\nprint(greet_with_default())\nprint(greet_with_default('Dana'))\n",
        },
        {
            'id': 'sort_by_length',
            'title': 'Sort By Length',
            'topic': 'sorted · key parameter',
            'task': 'כתבו פונקציה בשם sort_by_length\nפרמטר אחד, בשם words - רשימה של מילים\nהיא מחזירה את הרשימה ממוינת לפי אורך המילה, מהקצרה לארוכה\nיש ל-sorted פרמטר key שמקבל פונקציה - איזו פונקציה מודדת אורך',
            'starter': "def sort_by_length(words):\n    '''return words sorted by length, shortest to longest'''\n    # your line goes here\n\n\nprint(sort_by_length(['banana', 'kiwi', 'fig']))\n",
            'expect': 'return words sorted by length, shortest to longest',
            'tests': [
                {'call': "sort_by_length(['banana', 'kiwi', 'fig'])", 'is': "['fig', 'kiwi', 'banana']"},
                {'call': "sort_by_length(['a', 'bb'])", 'is': "['a', 'bb']"},
            ],
            'require': ['def', 'return', 'sorted', 'key'],
            'forbid': [],
            'hint': 'sorted(words, key=len) - הפרמטר key מקבל פונקציה שמחליטה לפי מה למיין',
            'solution': "def sort_by_length(words):\n    return sorted(words, key=len)\n\n\nprint(sort_by_length(['banana', 'kiwi', 'fig']))\n",
        },
        {
            'id': 'format_price',
            'title': 'Format As A Price',
            'topic': 'f-strings · number formatting',
            'task': "כתבו פונקציה בשם format_price\nפרמטר אחד, בשם amount - מספר\nהיא מחזירה אותו כמחרוזת מחיר, עם סימן $ ושתי ספרות אחרי הנקודה\nלמשל 9 הופך ל-'$9.00' - השתמשו ב-f-string עם :.2f",
            'starter': "def format_price(amount):\n    '''return amount formatted as a price, e.g. '$9.00''''\n    # your line goes here\n\n\nprint(format_price(9))\nprint(format_price(3.5))\n",
            'expect': "return amount formatted as a price, e.g. '$9.00'",
            'tests': [
                {'call': 'format_price(9)', 'is': "'$9.00'"},
                {'call': 'format_price(3.5)', 'is': "'$3.50'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': "f'${amount:.2f}' - ה-:.2f בתוך ה-f-string מעגל לשתי ספרות",
            'solution': "def format_price(amount):\n    return f'${amount:.2f}'\n\n\nprint(format_price(9))\nprint(format_price(3.5))\n",
        },
        {
            'id': 'min_and_max',
            'title': 'The Smallest And The Biggest',
            'topic': 'returning more than one value',
            'task': 'כתבו פונקציה בשם min_and_max\nפרמטר אחד, בשם numbers - רשימה של מספרים\nהיא מחזירה tuple: (המספר הקטן ביותר, המספר הגדול ביותר)',
            'starter': "def min_and_max(numbers):\n    '''return (the smallest number, the biggest number)'''\n    # your line goes here\n\n\nprint(min_and_max([4, 1, 9, 2]))\n",
            'expect': 'return (the smallest number, the biggest number)',
            'tests': [
                {'call': 'min_and_max([4, 1, 9, 2])', 'is': '(1, 9)'},
                {'call': 'min_and_max([7])', 'is': '(7, 7)'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'return (min(numbers), max(numbers)) - שני ערכים בסוגריים הם tuple',
            'solution': 'def min_and_max(numbers):\n    return (min(numbers), max(numbers))\n\n\nprint(min_and_max([4, 1, 9, 2]))\n',
        },
        {
            'id': 'flatten',
            'title': 'Flatten The List',
            'topic': 'nested for loops · append',
            'task': 'כתבו פונקציה בשם flatten\nפרמטר אחד, בשם nested - רשימה של רשימות\nהיא מחזירה רשימה אחת שטוחה, עם כל האיברים מכל השורות, לפי הסדר',
            'starter': "def flatten(nested):\n    '''return one flat list with every item from every row'''\n    # your lines go here\n\n\nprint(flatten([[1, 2], [3], [4, 5, 6]]))\n",
            'expect': 'return one flat list with every item from every row',
            'tests': [
                {'call': 'flatten([[1, 2], [3], [4, 5, 6]])', 'is': '[1, 2, 3, 4, 5, 6]'},
                {'call': 'flatten([[], [1]])', 'is': '[1]'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'hint': 'לולאת for חיצונית עוברת על השורות, לולאת for פנימית מוסיפה כל איבר לרשימה החדשה',
            'solution': 'def flatten(nested):\n    result = []\n    for row in nested:\n        for item in row:\n            result.append(item)\n    return result\n\n\nprint(flatten([[1, 2], [3], [4, 5, 6]]))\n',
        },
        {
            'id': 'remove_duplicates',
            'title': 'Remove Duplicates, Keep The Order',
            'topic': 'for loop · in · building a list',
            'task': 'כתבו פונקציה בשם remove_duplicates\nפרמטר אחד, בשם items - רשימה\nהיא מחזירה רשימה חדשה בלי כפילויות, כשהסדר המקורי נשמר\nעברו על הרשימה, והוסיפו איבר לרשימה החדשה רק אם הוא לא כבר בה',
            'starter': "def remove_duplicates(items):\n    '''return items with duplicates removed, order kept'''\n    # your lines go here\n\n\nprint(remove_duplicates([1, 2, 2, 3, 1, 4]))\n",
            'expect': 'return items with duplicates removed, order kept',
            'tests': [
                {'call': 'remove_duplicates([1, 2, 2, 3, 1, 4])', 'is': '[1, 2, 3, 4]'},
                {'call': 'remove_duplicates([1, 1, 1])', 'is': '[1]'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'hint': 'עברו על items, והוסיפו לרשימה החדשה רק איברים שעוד לא נמצאים בה',
            'solution': 'def remove_duplicates(items):\n    seen = []\n    for item in items:\n        if item not in seen:\n            seen.append(item)\n    return seen\n\n\nprint(remove_duplicates([1, 2, 2, 3, 1, 4]))\n',
        },
        {
            'id': 'is_palindrome',
            'title': 'Is It A Palindrome',
            'topic': 'string slicing · [::-1]',
            'task': 'כתבו פונקציה בשם is_palindrome\nפרמטר אחד, בשם word\nהיא מחזירה True אם המילה נקראת אותו דבר גם הפוך, אחרת False\n(לא רגישה לרישיות) - השתמשו בחיתוך word[::-1] כדי להפוך אותה',
            'starter': "def is_palindrome(word):\n    '''return True if word reads the same backwards'''\n    # your lines go here\n\n\nprint(is_palindrome('level'))\nprint(is_palindrome('hello'))\nprint(is_palindrome('Racecar'))\n",
            'expect': 'return True if word reads the same backwards',
            'tests': [
                {'call': "is_palindrome('level')", 'is': 'True'},
                {'call': "is_palindrome('hello')", 'is': 'False'},
                {'call': "is_palindrome('Racecar')", 'is': 'True'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'word[::-1] הופך את המחרוזת - השוו אותה למקור',
            'solution': "def is_palindrome(word):\n    clean = word.lower()\n    return clean == clean[::-1]\n\n\nprint(is_palindrome('level'))\nprint(is_palindrome('hello'))\nprint(is_palindrome('Racecar'))\n",
        },
        {
            'id': 'is_anagram',
            'title': 'Is It An Anagram',
            'topic': 'sorted · string comparison',
            'task': 'כתבו פונקציה בשם is_anagram\nשני פרמטרים: word1 ו-word2\nהיא מחזירה True אם שתי המילים מורכבות מאותן אותיות בדיוק,\nבכל סדר, אחרת False - (לא רגישה לרישיות)\nמיינו את האותיות של כל מילה והשוו',
            'starter': "def is_anagram(word1, word2):\n    '''return True if word1 and word2 use the same letters'''\n    # your line goes here\n\n\nprint(is_anagram('listen', 'silent'))\nprint(is_anagram('hello', 'world'))\n",
            'expect': 'return True if word1 and word2 use the same letters',
            'tests': [
                {'call': "is_anagram('listen', 'silent')", 'is': 'True'},
                {'call': "is_anagram('hello', 'world')", 'is': 'False'},
            ],
            'require': ['def', 'return', 'sorted'],
            'forbid': [],
            'hint': 'sorted() על מחרוזת מחזיר רשימה ממוינת של האותיות שלה - השוו בין שתי הרשימות',
            'solution': "def is_anagram(word1, word2):\n    return sorted(word1.lower()) == sorted(word2.lower())\n\n\nprint(is_anagram('listen', 'silent'))\nprint(is_anagram('hello', 'world'))\n",
        },
        {
            'id': 'word_frequency',
            'title': 'Word Frequency',
            'topic': 'for loop · dict',
            'task': 'כתבו פונקציה בשם word_frequency\nפרמטר אחד, בשם words - רשימה של מילים\nהיא מחזירה מילון: כל מילה היא מפתח, וכמה פעמים היא\nהופיעה ברשימה היא הערך\nאפשר גם עם dict רגיל, ואפשר גם עם defaultdict שניתן למעלה',
            'starter': "def word_frequency(words):\n    '''return a dict of word -> how many times it appears'''\n    # your lines go here\n\n\nprint(word_frequency(['a', 'b', 'a', 'c', 'b', 'a']))\n",
            'expect': 'return a dict of word -> how many times it appears',
            'tests': [
                {'call': "word_frequency(['a', 'b', 'a', 'c', 'b', 'a'])", 'is': "{'a': 3, 'b': 2, 'c': 1}"},
                {'call': "word_frequency(['x'])", 'is': "{'x': 1}"},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'setup': 'from collections import defaultdict\n',
            'hint': 'בדיוק כמו char_count אבל על מילים במקום אותיות - counts.get(w, 0) + 1',
            'solution': "def word_frequency(words):\n    counts = {}\n    for w in words:\n        counts[w] = counts.get(w, 0) + 1\n    return counts\n\n\nprint(word_frequency(['a', 'b', 'a', 'c', 'b', 'a']))\n",
        },
        {
            'id': 'average_rounded',
            'title': 'The Average, Rounded',
            'topic': 'sum / len · round',
            'task': 'כתבו פונקציה בשם average_rounded\nפרמטר אחד, בשם numbers - רשימה של מספרים\nהיא מחזירה את הממוצע שלהם, מעוגל לשתי ספרות אחרי הנקודה',
            'starter': "def average_rounded(numbers):\n    '''return the average of numbers, rounded to 2 decimal places'''\n    # your line goes here\n\n\nprint(average_rounded([1, 2, 4]))\n",
            'expect': 'return the average of numbers, rounded to 2 decimal places',
            'tests': [
                {'call': 'average_rounded([1, 2, 4])', 'is': '2.33'},
                {'call': 'average_rounded([10])', 'is': '10.0'},
                {'call': 'average_rounded([1, 2, 3])', 'is': '2.0'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'round(sum(numbers) / len(numbers), 2) - round מקבל את המספר ואת כמות הספרות',
            'solution': 'def average_rounded(numbers):\n    return round(sum(numbers) / len(numbers), 2)\n\n\nprint(average_rounded([1, 2, 4]))\n',
        },
        {
            'id': 'count_positive',
            'title': 'Count The Positives',
            'topic': 'for loop · if · counter',
            'task': 'כתבו פונקציה בשם count_positive\nפרמטר אחד, בשם numbers - רשימה של מספרים\nהיא מחזירה כמה מספרים ברשימה גדולים מ-0\nהפעם בלי list comprehension - התחילו ממונה על 0, עברו על\nהרשימה עם for, והוסיפו 1 למונה כל פעם שהמספר גדול מ-0',
            'starter': "def count_positive(numbers):\n    '''return how many numbers in the list are greater than 0'''\n    # your lines go here\n\n\nprint(count_positive([-5, 8, -2, 10, 0, 3]))\n",
            'expect': 'return how many numbers in the list are greater than 0',
            'tests': [
                {'call': 'count_positive([-5, 8, -2, 10, 0, 3])', 'is': '3'},
                {'call': 'count_positive([-1, -2])', 'is': '0'},
                {'call': 'count_positive([1, 2, 3])', 'is': '3'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'hint': 'התחילו ממונה על 0, עברו על הרשימה עם for, והוסיפו 1 כל פעם שהמספר גדול מ-0',
            'solution': 'def count_positive(numbers):\n    count = 0\n    for n in numbers:\n        if n > 0:\n            count += 1\n    return count\n\n\nprint(count_positive([-5, 8, -2, 10, 0, 3]))\n',
        },
        {
            'id': 'is_valid_password',
            'title': 'Is The Password Valid',
            'topic': 'strings · loop · combined conditions',
            'task': 'כתבו פונקציה בשם is_valid_password\nפרמטר אחד, בשם password\nהיא מחזירה True רק אם הסיסמה באורך 8 תווים לפחות, וגם יש בה\nלפחות ספרה אחת - אחרת False\nלבדיקה שתו הוא ספרה יש למחרוזת פעולה מוכנה',
            'starter': "def is_valid_password(password):\n    '''return True if password is 8+ chars and has a digit'''\n    # your lines go here\n\n\nprint(is_valid_password('abc12345'))\nprint(is_valid_password('ab1'))\nprint(is_valid_password('abcdefgh'))\n",
            'expect': 'return True if password is 8+ chars and has a digit',
            'tests': [
                {'call': "is_valid_password('abc12345')", 'is': 'True'},
                {'call': "is_valid_password('ab1')", 'is': 'False'},
                {'call': "is_valid_password('abcdefgh')", 'is': 'False'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'hint': 'בדקו קודם את len(password), ואז עברו על התווים עם for ובדקו ch.isdigit()',
            'solution': "def is_valid_password(password):\n    if len(password) < 8:\n        return False\n    for ch in password:\n        if ch.isdigit():\n            return True\n    return False\n\n\nprint(is_valid_password('abc12345'))\nprint(is_valid_password('ab1'))\nprint(is_valid_password('abcdefgh'))\n",
        },
        {
            'id': 'split_full_name',
            'title': 'Split The Full Name',
            'topic': 'string · split · tuple',
            'task': "כתבו פונקציה בשם split_full_name\nפרמטר אחד, בשם full - מחרוזת בצורת 'First Last'\nהיא מחזירה tuple: (First, Last) - שני החלקים בנפרד",
            'starter': "def split_full_name(full):\n    '''return full split into (first, last)'''\n    # your lines go here\n\n\nprint(split_full_name('Ada Lovelace'))\n",
            'expect': 'return full split into (first, last)',
            'tests': [
                {'call': "split_full_name('Ada Lovelace')", 'is': "('Ada', 'Lovelace')"},
                {'call': "split_full_name('Guido Rossum')", 'is': "('Guido', 'Rossum')"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'full.split() מפרקת לפי רווח - אפשר לפרוק ישר לשני משתנים: first, last = full.split()',
            'solution': "def split_full_name(full):\n    first, last = full.split()\n    return (first, last)\n\n\nprint(split_full_name('Ada Lovelace'))\n",
        },
        {
            'id': 'running_total',
            'title': 'The Running Total',
            'topic': 'for loop · building a list',
            'task': 'כתבו פונקציה בשם running_total\nפרמטר אחד, בשם numbers - רשימה של מספרים\nהיא מחזירה רשימה חדשה: כל איבר בה הוא הסכום המצטבר עד\nהמיקום הזה - למשל [1, 2, 3, 4] הופך ל-[1, 3, 6, 10]',
            'starter': "def running_total(numbers):\n    '''return the running (cumulative) total as a new list'''\n    # your lines go here\n\n\nprint(running_total([1, 2, 3, 4]))\n",
            'expect': 'return the running (cumulative) total as a new list',
            'tests': [
                {'call': 'running_total([1, 2, 3, 4])', 'is': '[1, 3, 6, 10]'},
                {'call': 'running_total([5])', 'is': '[5]'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'hint': 'שמרו משתנה total שמצטבר, והוסיפו אותו לרשימה החדשה בכל סיבוב של הלולאה',
            'solution': 'def running_total(numbers):\n    result = []\n    total = 0\n    for n in numbers:\n        total += n\n        result.append(total)\n    return result\n\n\nprint(running_total([1, 2, 3, 4]))\n',
        },
        {
            'id': 'common_elements',
            'title': 'What They Have In Common',
            'topic': 'list comprehension · in',
            'task': 'כתבו פונקציה בשם common_elements\nשני פרמטרים: a ו-b - שתי רשימות\nהיא מחזירה רשימה חדשה עם כל האיברים מ-a שנמצאים גם ב-b\n(שלא כמו intersection על sets, כאן זו רשימה רגילה - הסדר\nוהכפילויות של a נשמרים)',
            'starter': "def common_elements(a, b):\n    '''return a's items that are also in b, order and duplicates kept'''\n    # your line goes here\n\n\nprint(common_elements([1, 2, 3, 4], [2, 4, 6]))\n",
            'expect': "return a's items that are also in b, order and duplicates kept",
            'tests': [
                {'call': 'common_elements([1, 2, 3, 4], [2, 4, 6])', 'is': '[2, 4]'},
                {'call': 'common_elements([1, 1, 2], [1])', 'is': '[1, 1]'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'hint': 'list comprehension עם תנאי: [x for x in a if x in b]',
            'solution': 'def common_elements(a, b):\n    return [x for x in a if x in b]\n\n\nprint(common_elements([1, 2, 3, 4], [2, 4, 6]))\n',
        },
        {
            'id': 'repeat_word',
            'title': 'Repeat It',
            'topic': 'string · * operator',
            'task': 'כתבו פונקציה בשם repeat_word\nשני פרמטרים: word ו-n\nהיא מחזירה את word חוזר על עצמו n פעמים, ברצף, בלי רווחים\nאפשר להכפיל מחרוזת במספר עם *, בדיוק כמו מספרים',
            'starter': "def repeat_word(word, n):\n    '''return word repeated n times'''\n    # your line goes here\n\n\nprint(repeat_word('ab', 3))\n",
            'expect': 'return word repeated n times',
            'tests': [
                {'call': "repeat_word('ab', 3)", 'is': "'ababab'"},
                {'call': "repeat_word('x', 1)", 'is': "'x'"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': 'מחרוזת כפול מספר עם * חוזרת על עצמה - word * n',
            'solution': "def repeat_word(word, n):\n    return word * n\n\n\nprint(repeat_word('ab', 3))\n",
        },
        {
            'id': 'filter_by_score',
            'title': 'Who Passed',
            'topic': 'list of dicts · comprehension',
            'task': "כתבו פונקציה בשם filter_by_score\nשני פרמטרים: records (רשימה של מילונים, לכל אחד יש 'name' ו-'score') ו-threshold\nהיא מחזירה רשימה של השמות (name) בלבד, של כל הרשומות שבהן\nscore גדול או שווה ל-threshold",
            'starter': "def filter_by_score(records, threshold):\n    '''return the names of records whose score >= threshold'''\n    # your line goes here\n\n\nprint(filter_by_score([{'name': 'Ann', 'score': 70}, {'name': 'Bo', 'score': 50}, {'name': 'Cy', 'score': 90}], 60))\n",
            'expect': 'return the names of records whose score >= threshold',
            'tests': [
                {'call': "filter_by_score([{'name': 'Ann', 'score': 70}, {'name': 'Bo', 'score': 50}, {'name': 'Cy', 'score': 90}], 60)", 'is': "['Ann', 'Cy']"},
                {'call': "filter_by_score([{'name': 'A', 'score': 10}], 60)", 'is': '[]'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'hint': "list comprehension על records, עם r['name'] כביטוי ו-r['score'] >= threshold כתנאי",
            'solution': "def filter_by_score(records, threshold):\n    return [r['name'] for r in records if r['score'] >= threshold]\n\n\nprint(filter_by_score([{'name': 'Ann', 'score': 70}, {'name': 'Bo', 'score': 50}, {'name': 'Cy', 'score': 90}], 60))\n",
        },
    ],

    # =============================================================== EXPERT
    'expert': [
        {
            'id': 'safe_divide',
            'title': 'Divide, Safely',
            'topic': 'functions · try / except · return',
            'task': "כתבו פונקציה בשם safe_divide\n"
                    "שני פרמטרים: a ו-b\n"
                    "היא מחזירה a / b\n"
                    "\n"
                    "אבל אם b הוא 0, החלוקה מפילה את התוכנית עם שגיאת\n"
                    "ZeroDivisionError. תפסו אותה עם try/except, והחזירו\n"
                    "None במקום לקרוס",
            'starter': "def safe_divide(a, b):\n"
                       "    '''return a / b, or None if b is 0'''\n"
                       "    # your lines go here\n"
                       "\n"
                       "\n"
                       "print(safe_divide(10, 2))\n"
                       "print(safe_divide(10, 0))\n",
            'expect': "a / b - or None when b is 0, never a crash",
            'tests': [
                {'call': 'safe_divide(10, 2)', 'is': '5.0'},
                {'call': 'safe_divide(9, 3)', 'is': '3.0'},
                {'call': 'safe_divide(5, 0)', 'is': 'None'},
                {'call': 'safe_divide(0, 7)', 'is': '0.0'},
            ],
            'require': ['def', 'return', 'try', 'except'],
            'forbid': [],
            'hint': "return a / b בתוך try, ו-except שתופס ZeroDivisionError "
                    "- לא if שבודק b == 0 מראש",
            'solution': "def safe_divide(a, b):\n"
                        "    try:\n"
                        "        return a / b\n"
                        "    except ZeroDivisionError:\n"
                        "        return None\n"
                        "\n"
                        "\n"
                        "print(safe_divide(10, 2))\n"
                        "print(safe_divide(10, 0))\n",
            'retry': [
                {
                    'task': "כתבו פונקציה בשם safe_divide\n"
                            "שני פרמטרים: a ו-b\n"
                            "היא מחזירה a / b\n"
                            "\n"
                            "אבל אם b הוא 0, החלוקה מפילה את התוכנית עם שגיאת\n"
                            "ZeroDivisionError. תפסו אותה עם try/except, והחזירו\n"
                            "את המספר 0 במקום לקרוס",
                    'starter': "def safe_divide(a, b):\n"
                               "    '''return a / b, or 0 if b is 0'''\n"
                               "    # your lines go here\n"
                               "\n"
                               "\n"
                               "print(safe_divide(10, 2))\n"
                               "print(safe_divide(10, 0))\n",
                    'expect': "a / b - or 0 when b is 0, never a crash",
                    'tests': [
                        {'call': 'safe_divide(10, 2)', 'is': '5.0'},
                        {'call': 'safe_divide(9, 3)', 'is': '3.0'},
                        {'call': 'safe_divide(5, 0)', 'is': '0'},
                        {'call': 'safe_divide(0, 7)', 'is': '0.0'},
                    ],
                    'require': ['def', 'return', 'try', 'except'],
                    'forbid': [],
                    'hint': "return a / b בתוך try, ו-except שתופס "
                            "ZeroDivisionError - לא if שבודק b == 0 מראש",
                    'solution': "def safe_divide(a, b):\n"
                                "    try:\n"
                                "        return a / b\n"
                                "    except ZeroDivisionError:\n"
                                "        return 0\n"
                                "\n"
                                "\n"
                                "print(safe_divide(10, 2))\n"
                                "print(safe_divide(10, 0))\n",
                },
                {
                    'task': "כתבו פונקציה בשם safe_divide\n"
                            "שני פרמטרים: a ו-b\n"
                            "היא מחזירה a / b\n"
                            "\n"
                            "אבל אם b הוא 0, החלוקה מפילה את התוכנית עם שגיאת\n"
                            "ZeroDivisionError. תפסו אותה עם try/except, והחזירו\n"
                            "את המספר -1 במקום לקרוס",
                    'starter': "def safe_divide(a, b):\n"
                               "    '''return a / b, or -1 if b is 0'''\n"
                               "    # your lines go here\n"
                               "\n"
                               "\n"
                               "print(safe_divide(10, 2))\n"
                               "print(safe_divide(10, 0))\n",
                    'expect': "a / b - or -1 when b is 0, never a crash",
                    'tests': [
                        {'call': 'safe_divide(10, 2)', 'is': '5.0'},
                        {'call': 'safe_divide(9, 3)', 'is': '3.0'},
                        {'call': 'safe_divide(5, 0)', 'is': '-1'},
                        {'call': 'safe_divide(0, 7)', 'is': '0.0'},
                    ],
                    'require': ['def', 'return', 'try', 'except'],
                    'forbid': [],
                    'hint': "return a / b בתוך try, ו-except שתופס "
                            "ZeroDivisionError - לא if שבודק b == 0 מראש",
                    'solution': "def safe_divide(a, b):\n"
                                "    try:\n"
                                "        return a / b\n"
                                "    except ZeroDivisionError:\n"
                                "        return -1\n"
                                "\n"
                                "\n"
                                "print(safe_divide(10, 2))\n"
                                "print(safe_divide(10, 0))\n",
                },
            ],
        },
        {
            'id': 'char_count',
            'title': 'Count The Letters',
            'topic': 'functions · loops · dictionaries',
            'task': "כתבו פונקציה בשם char_count\n"
                    "פרמטר אחד, בשם word\n"
                    "היא מחזירה מילון: כל אות במילה היא מפתח, וכמה\n"
                    "פעמים היא הופיעה היא הערך\n"
                    "(רגישות לרישיות - 'A' ו-'a' נספרות בנפרד)",
            'starter': "def char_count(word):\n"
                       "    '''return a dict of letter -> how many times it appears'''\n"
                       "    # your lines go here\n"
                       "\n"
                       "\n"
                       "print(char_count('banana'))\n",
            'expect': "a dict - each letter as the key, its count as the value",
            'tests': [
                {'call': "char_count('banana')", 'is': "{'b': 1, 'a': 3, 'n': 2}"},
                {'call': "char_count('aa')", 'is': "{'a': 2}"},
                {'call': "char_count('')", 'is': '{}'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'setup': "from collections import defaultdict\n",
            'hint': "התחילו ממילון ריק, עברו על המילה עם for, ולכל אות\n"
                    "עדכנו את הספירה שלה במילון - יש למילון פעולה שמחזירה ערך\n"
                    "ברירת מחדל כשמפתח עוד לא קיים בו, נוחה בדיוק בשביל זה",
            'solution': "def char_count(word):\n"
                        "    counts = {}\n"
                        "    for ch in word:\n"
                        "        counts[ch] = counts.get(ch, 0) + 1\n"
                        "    return counts\n"
                        "\n"
                        "\n"
                        "print(char_count('banana'))\n",
        },
        {
            'id': 'unique_letters',
            'title': 'The Unique Ones',
            'topic': 'functions · sets · sorting',
            'task': "כתבו פונקציה בשם unique_letters\n"
                    "פרמטר אחד, בשם word\n"
                    "היא מחזירה רשימה ממוינת של כל האותיות השונות במילה,\n"
                    "כל אות פעם אחת בלבד",
            'starter': "def unique_letters(word):\n"
                       "    '''return a sorted list of the distinct letters in word'''\n"
                       "    # your line goes here\n"
                       "\n"
                       "\n"
                       "print(unique_letters('banana'))\n",
            'expect': "a sorted list of the distinct letters, handed back with return",
            'tests': [
                {'call': "unique_letters('banana')", 'is': "['a', 'b', 'n']"},
                {'call': "unique_letters('aa')", 'is': "['a']"},
                {'call': "unique_letters('')", 'is': '[]'},
                {'call': "unique_letters('dcba')", 'is': "['a', 'b', 'c', 'd']"},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': "יש טיפוס נתונים שמשאיר רק ערכים ייחודיים - הפכו אותו\n"
                    "לרשימה ממוינת עם הפונקציה שממיינת",
            'solution': "def unique_letters(word):\n"
                        "    return sorted(set(word))\n"
                        "\n"
                        "\n"
                        "print(unique_letters('banana'))\n",
        },
        {
            'id': 'indexed_pairs',
            'title': 'Number Every Item',
            'topic': 'enumerate',
            'task': 'כתבו פונקציה בשם indexed_pairs\nפרמטר אחד, בשם items - רשימה\nהיא מחזירה רשימה של זוגות (מיקום, איבר) לכל איבר ברשימה\nהשתמשו ב-enumerate במקום לספור מיקום בעצמכם',
            'starter': "def indexed_pairs(items):\n    '''return a list of (index, item) pairs'''\n    # your line goes here\n\n\nprint(indexed_pairs(['a', 'b', 'c']))\n",
            'expect': 'return a list of (index, item) pairs',
            'tests': [
                {'call': "indexed_pairs(['a', 'b', 'c'])", 'is': "[(0, 'a'), (1, 'b'), (2, 'c')]"},
                {'call': 'indexed_pairs([9])', 'is': '[(0, 9)]'},
            ],
            'require': ['def', 'return', 'enumerate'],
            'forbid': [],
            'hint': 'list(enumerate(items)) - enumerate מצרף מיקום לכל איבר',
            'solution': "def indexed_pairs(items):\n    return list(enumerate(items))\n\n\nprint(indexed_pairs(['a', 'b', 'c']))\n",
        },
        {
            'id': 'pair_up',
            'title': 'Pair Two Lists Together',
            'topic': 'zip',
            'task': 'כתבו פונקציה בשם pair_up\nשני פרמטרים: names ו-scores - שתי רשימות באותו אורך\nהיא מחזירה רשימה של זוגות, כל שם עם הציון שלו באותו מיקום\nהשתמשו ב-zip',
            'starter': "def pair_up(names, scores):\n    '''return a list pairing names with scores'''\n    # your line goes here\n\n\nprint(pair_up(['Ann', 'Bo'], [90, 80]))\n",
            'expect': 'return a list pairing names with scores',
            'tests': [
                {'call': "pair_up(['Ann', 'Bo'], [90, 80])", 'is': "[('Ann', 90), ('Bo', 80)]"},
                {'call': "pair_up(['X'], [1])", 'is': "[('X', 1)]"},
            ],
            'require': ['def', 'return', 'zip'],
            'forbid': [],
            'hint': 'list(zip(names, scores)) - zip מצמיד איברים משתי רשימות לפי מיקום',
            'solution': "def pair_up(names, scores):\n    return list(zip(names, scores))\n\n\nprint(pair_up(['Ann', 'Bo'], [90, 80]))\n",
        },
        {
            'id': 'fibonacci_list',
            'title': 'The Fibonacci Sequence',
            'topic': 'for loop · building a list',
            'task': "כתבו פונקציה בשם fibonacci_list\nפרמטר אחד, בשם n\nהיא מחזירה רשימה עם n המספרים הראשונים בסדרת פיבונאצ'י\n(כל מספר הוא סכום שני המספרים שלפניו: 0, 1, 1, 2, 3, 5, ...)",
            'starter': "def fibonacci_list(n):\n    '''return the first n Fibonacci numbers'''\n    # your lines go here\n\n\nprint(fibonacci_list(6))\n",
            'expect': 'return the first n Fibonacci numbers',
            'tests': [
                {'call': 'fibonacci_list(6)', 'is': '[0, 1, 1, 2, 3, 5]'},
                {'call': 'fibonacci_list(1)', 'is': '[0]'},
                {'call': 'fibonacci_list(0)', 'is': '[]'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'hint': 'שמרו שני משתנים a ו-b, בכל סיבוב הוסיפו את a לרשימה ואז a, b = b, a + b',
            'solution': 'def fibonacci_list(n):\n    result = []\n    a, b = 0, 1\n    for _ in range(n):\n        result.append(a)\n        a, b = b, a + b\n    return result\n\n\nprint(fibonacci_list(6))\n',
        },
        {
            'id': 'matrix_row_sums',
            'title': 'Sum Each Row',
            'topic': 'list comprehension · sum',
            'task': 'כתבו פונקציה בשם matrix_row_sums\nפרמטר אחד, בשם matrix - רשימה של רשימות של מספרים\nהיא מחזירה רשימה עם הסכום של כל שורה בנפרד\nכתבו את זה כ-list comprehension, עם sum על כל שורה',
            'starter': "def matrix_row_sums(matrix):\n    '''return a list with the sum of each row'''\n    # your line goes here\n\n\nprint(matrix_row_sums([[1, 2, 3], [4, 5], [6]]))\n",
            'expect': 'return a list with the sum of each row',
            'tests': [
                {'call': 'matrix_row_sums([[1, 2, 3], [4, 5], [6]])', 'is': '[6, 9, 6]'},
                {'call': 'matrix_row_sums([[9]])', 'is': '[9]'},
            ],
            'require': ['def', 'return'],
            'forbid': [],
            'hint': '[sum(row) for row in matrix] - sum על כל שורה בתוך list comprehension',
            'solution': 'def matrix_row_sums(matrix):\n    return [sum(row) for row in matrix]\n\n\nprint(matrix_row_sums([[1, 2, 3], [4, 5], [6]]))\n',
        },
        {
            'id': 'second_largest',
            'title': 'The Second Largest',
            'topic': 'for loop · tracking two values',
            'task': 'כתבו פונקציה בשם second_largest\nפרמטר אחד, בשם numbers - רשימה של מספרים שונים זה מזה\nהיא מחזירה את המספר השני בגודלו ברשימה, בלי למיין אותה\nעברו על הרשימה פעם אחת, ושמרו את הגדול והשני בגודלו תוך כדי',
            'starter': "def second_largest(numbers):\n    '''return the second-biggest number in the list'''\n    # your lines go here\n\n\nprint(second_largest([4, 1, 9, 2]))\n",
            'expect': 'return the second-biggest number in the list',
            'tests': [
                {'call': 'second_largest([4, 1, 9, 2])', 'is': '4'},
                {'call': 'second_largest([10, 20])', 'is': '10'},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'hint': 'שמרו את הגדול ואת השני בגודלו תוך כדי מעבר יחיד - עדכנו את שניהם כשמוצאים חדש גדול יותר',
            'solution': 'def second_largest(numbers):\n    first = second = None\n    for n in numbers:\n        if first is None or n > first:\n            second = first\n            first = n\n        elif n != first and (second is None or n > second):\n            second = n\n    return second\n\n\nprint(second_largest([4, 1, 9, 2]))\n',
        },
        {
            'id': 'group_by_length',
            'title': 'Group By Word Length',
            'topic': 'for loop · dict of lists',
            'task': 'כתבו פונקציה בשם group_by_length\nפרמטר אחד, בשם words - רשימה של מילים\nהיא מחזירה מילון: כל אורך מילה הוא מפתח, והערך הוא רשימה\nשל כל המילים באורך הזה\nעבור כל מילה - אם האורך שלה עוד לא מפתח במילון, התחילו בשבילו\nרשימה ריקה, ואז הוסיפו אליה את המילה\nאפשר גם עם dict רגיל, ואפשר גם עם defaultdict שניתן למעלה',
            'starter': "def group_by_length(words):\n    '''return a dict of word length -> list of words that length'''\n    # your lines go here\n\n\nprint(group_by_length(['a', 'bb', 'cc', 'ddd', 'e']))\n",
            'expect': 'return a dict of word length -> list of words that length',
            'tests': [
                {'call': "group_by_length(['a', 'bb', 'cc', 'ddd', 'e'])", 'is': "{1: ['a', 'e'], 2: ['bb', 'cc'], 3: ['ddd']}"},
                {'call': "group_by_length(['x'])", 'is': "{1: ['x']}"},
            ],
            'require': ['def', 'return', 'for'],
            'forbid': [],
            'setup': 'from collections import defaultdict\n',
            'hint': 'כמו char_count, רק שהמפתח הוא אורך המילה והערך הוא רשימה - אם אורך עוד לא במילון, התחילו רשימה ריקה',
            'solution': "def group_by_length(words):\n    groups = {}\n    for w in words:\n        n = len(w)\n        if n not in groups:\n            groups[n] = []\n        groups[n].append(w)\n    return groups\n\n\nprint(group_by_length(['a', 'bb', 'cc', 'ddd', 'e']))\n",
        },
        {
            'id': 'nested_get',
            'title': 'Safe Nested Lookup',
            'topic': 'dict of dicts · get',
            'task': 'כתבו פונקציה בשם nested_get\nשלושה פרמטרים: d (מילון של מילונים), outer_key ו-inner_key\nהיא מחזירה את d[outer_key][inner_key]\nאבל אם outer_key לא קיים ב-d, או ש-inner_key לא קיים\nבמילון הפנימי - מחזירה None במקום לקרוס\nהשתמשו ב-get במקום בסוגריים מרובעים',
            'starter': "def nested_get(d, outer_key, inner_key):\n    '''return d[outer_key][inner_key], or None if either key is missing'''\n    # your lines go here\n\n\nprint(nested_get({'a': {'x': 1}}, 'a', 'x'))\nprint(nested_get({'a': {'x': 1}}, 'z', 'x'))\n",
            'expect': 'return d[outer_key][inner_key], or None if either key is missing',
            'tests': [
                {'call': "nested_get({'a': {'x': 1}}, 'a', 'x')", 'is': '1'},
                {'call': "nested_get({'a': {'x': 1}}, 'z', 'x')", 'is': 'None'},
                {'call': "nested_get({'a': {'x': 1}}, 'a', 'y')", 'is': 'None'},
            ],
            'require': ['def', 'return', 'get'],
            'forbid': [],
            'hint': 'd.get(outer_key) מחזיר None אם המפתח לא קיים, בלי לקרוס - בדקו את זה לפני שממשיכים למפתח הפנימי',
            'solution': "def nested_get(d, outer_key, inner_key):\n    inner = d.get(outer_key)\n    if inner is None:\n        return None\n    return inner.get(inner_key)\n\n\nprint(nested_get({'a': {'x': 1}}, 'a', 'x'))\nprint(nested_get({'a': {'x': 1}}, 'z', 'x'))\n",
        },
        {
            'id': 'extract_numbers',
            'title': 'Extract The Numbers',
            'topic': 'regex · re.findall',
            'task': 'כתבו פונקציה בשם extract_numbers\nפרמטר אחד, בשם text\nיש לכם למעלה pattern מוכן בשם NUMBER_PATTERN, שכבר יודע\nלזהות רצף של ספרות בתוך טקסט - לא צריך לכתוב regex בעצמכם\nהשתמשו ב-re.findall עם ה-pattern הזה כדי למצוא את כל\nרצפי הספרות בטקסט, והחזירו אותם כרשימה של מספרים שלמים\n(לא כמחרוזות - צריך להמיר כל אחד עם int)',
            'starter': "def extract_numbers(text):\n    '''return every run of digits in text, as a list of ints'''\n    # your lines go here\n\n\nprint(extract_numbers('I have 3 cats and 12 dogs, and 007 fish'))\n",
            'expect': 'return every run of digits in text, as a list of ints',
            'tests': [
                {'call': "extract_numbers('I have 3 cats and 12 dogs, and 007 fish')", 'is': '[3, 12, 7]'},
                {'call': "extract_numbers('no digits')", 'is': '[]'},
            ],
            'require': ['def', 'return', 're.findall'],
            'forbid': [],
            'setup': "import re\n\n# a ready-made pattern - matches one or more digits in a row\nNUMBER_PATTERN = r'\\d+'\n",
            'hint': 're.findall(NUMBER_PATTERN, text) מחזיר רשימה של כל ההתאמות - int() כדי להפוך כל אחת למספר',
            'solution': "def extract_numbers(text):\n    matches = re.findall(NUMBER_PATTERN, text)\n    return [int(m) for m in matches]\n\n\nprint(extract_numbers('I have 3 cats and 12 dogs, and 007 fish'))\n",
        },
        {
            'id': 'sort_by_score',
            'title': 'Sort By Score',
            'topic': 'sorted · key · lambda',
            'task': 'כתבו פונקציה בשם sort_by_score\nפרמטר אחד, בשם records - רשימה של tuples בצורת (name, score)\nהיא מחזירה את הרשימה ממוינת לפי score, מהגבוה לנמוך\nהשתמשו ב-sorted עם key שהוא lambda, ו-reverse=True',
            'starter': "def sort_by_score(records):\n    '''return records sorted by score, highest first'''\n    # your line goes here\n\n\nprint(sort_by_score([('Ann', 70), ('Bo', 95), ('Cy', 82)]))\n",
            'expect': 'return records sorted by score, highest first',
            'tests': [
                {'call': "sort_by_score([('Ann', 70), ('Bo', 95), ('Cy', 82)])", 'is': "[('Bo', 95), ('Cy', 82), ('Ann', 70)]"},
                {'call': "sort_by_score([('A', 1)])", 'is': "[('A', 1)]"},
            ],
            'require': ['def', 'return', 'sorted', 'lambda'],
            'forbid': [],
            'hint': "sorted(records, key=lambda r: r[1], reverse=True) - lambda r: r[1] אומר 'מיינו לפי האיבר השני'",
            'solution': "def sort_by_score(records):\n    return sorted(records, key=lambda r: r[1], reverse=True)\n\n\nprint(sort_by_score([('Ann', 70), ('Bo', 95), ('Cy', 82)]))\n",
        },
        {
            'id': 'safe_int',
            'title': 'Convert, Safely',
            'topic': 'try / except · ValueError',
            'task': 'כתבו פונקציה בשם safe_int\nפרמטר אחד, בשם text\nהיא מנסה להפוך את text למספר שלם ולהחזיר אותו\nאבל אם text לא מייצג מספר, int(text) מפילה את התוכנית עם\nשגיאת ValueError. תפסו אותה עם try/except, והחזירו None\nבמקום לקרוס',
            'starter': "def safe_int(text):\n    '''return int(text), or None if text is not a number'''\n    # your lines go here\n\n\nprint(safe_int('42'))\nprint(safe_int('abc'))\n",
            'expect': 'return int(text), or None if text is not a number',
            'tests': [
                {'call': "safe_int('42')", 'is': '42'},
                {'call': "safe_int('abc')", 'is': 'None'},
            ],
            'require': ['def', 'return', 'try', 'except'],
            'forbid': [],
            'hint': 'int(text) בתוך try, ו-except שתופס ValueError',
            'solution': "def safe_int(text):\n    try:\n        return int(text)\n    except ValueError:\n        return None\n\n\nprint(safe_int('42'))\nprint(safe_int('abc'))\n",
        },
        {
            'id': 'merge_dicts',
            'title': 'Merge Two Dicts',
            'topic': 'dict · ** unpacking',
            'task': 'כתבו פונקציה בשם merge_dicts\nשני פרמטרים: a ו-b - שני מילונים\nהיא מחזירה מילון חדש שמשלב את שניהם - אם אותו מפתח קיים\nבשניהם, הערך מ-b הוא זה שנשאר\nהשתמשו בפריסה (unpacking) עם **, לא בלולאה',
            'starter': "def merge_dicts(a, b):\n    '''return a and b merged into one dict (b wins on conflicts)'''\n    # your line goes here\n\n\nprint(merge_dicts({'a': 1, 'b': 2}, {'b': 9, 'c': 3}))\n",
            'expect': 'return a and b merged into one dict (b wins on conflicts)',
            'tests': [
                {'call': "merge_dicts({'a': 1, 'b': 2}, {'b': 9, 'c': 3})", 'is': "{'a': 1, 'b': 9, 'c': 3}"},
                {'call': "merge_dicts({}, {'x': 1})", 'is': "{'x': 1}"},
            ],
            'require': ['def', 'return', '**'],
            'forbid': [],
            'hint': '{**a, **b} פורס את שני המילונים לתוך מילון חדש - b נכתב שני, אז הוא זה שמנצח בהתנגשות',
            'solution': "def merge_dicts(a, b):\n    return {**a, **b}\n\n\nprint(merge_dicts({'a': 1, 'b': 2}, {'b': 9, 'c': 3}))\n",
        },
        {
            'id': 'top_n',
            'title': 'The Top N',
            'topic': 'sorted · slicing',
            'task': 'כתבו פונקציה בשם top_n\nשני פרמטרים: numbers (רשימה של מספרים) ו-n\nהיא מחזירה את n המספרים הגדולים ביותר ברשימה, ממוינים\nמהגבוה לנמוך\nמיינו את כל הרשימה מהגבוה לנמוך, ואז קחו את n הראשונים עם חיתוך',
            'starter': "def top_n(numbers, n):\n    '''return the n biggest numbers, sorted highest first'''\n    # your line goes here\n\n\nprint(top_n([4, 1, 9, 2, 7], 3))\n",
            'expect': 'return the n biggest numbers, sorted highest first',
            'tests': [
                {'call': 'top_n([4, 1, 9, 2, 7], 3)', 'is': '[9, 7, 4]'},
                {'call': 'top_n([5, 5, 5], 2)', 'is': '[5, 5]'},
            ],
            'require': ['def', 'return', 'sorted'],
            'forbid': [],
            'hint': 'sorted(numbers, reverse=True) ממיין מהגבוה לנמוך - [:n] לוקח את n הראשונים',
            'solution': 'def top_n(numbers, n):\n    return sorted(numbers, reverse=True)[:n]\n\n\nprint(top_n([4, 1, 9, 2, 7], 3))\n',
        },
    ],
}

LEVELS = ['easy', 'medium', 'expert']
