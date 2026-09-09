# -*- coding: utf-8 -*-
"""
draft_expert_questions.py  --  REVIEW ONLY, not wired into the game yet.

Same idea as draft_easy_questions.py / draft_medium_questions.py, top tier:
EXPERT-level questions for Exam Rehearsal. Includes the 3 questions already
live in the game's expert level (safe_divide, char_count, unique_letters -
reproduced here so this page is a complete picture of the tier, not just
the new additions), plus:

  - enumerate and zip (indexed_pairs, pair_up), the Fibonacci sequence
    (fibonacci_list), matrix_row_sums, and second_largest - all moved here
    from the medium draft on request: this is a basics course, some
    students still struggle with plain functions, so these belong at the
    top tier, not medium
  - one regex question (extract_numbers) - the FIRST time regex shows up
    anywhere in this game. Per instruction: the student is not expected to
    write a regex from scratch - the pattern is handed to them, ready to
    use, and the challenge is calling re.findall with it correctly and
    doing something with the result. This is also the first question in
    the whole game that needs a 're' import - see the note below.
  - two more genuinely-advanced combinations: group_by_length (loop + dict
    of lists) and nested_get (safe two-level dict lookup)

NOTE - 'while' and 'import' are both banned in submitted code (see the
easy/medium drafts' notes) - EXCEPT that extract_numbers needs 're'.
Once this is wired into the real game, that one question's payload will
need a 'setup' field (a mechanism the judge already supports - see
make_solo_func.py's run_file(), which prepends q['setup'] to the student's
code before executing both in the same call) containing 'import re' and
the ready-made pattern; make_exam_prep.py does not have a UI for showing
that provided code to the student yet, so this still needs that piece of
work before extract_numbers can actually ship. Written and verified here
as plain Python so the question itself is ready when that lands.

Same shape as draft_easy_questions.py: {id, title, topic, task (Hebrew),
solution (English)}.
"""

QUESTIONS = [

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
        'solution': "def safe_divide(a, b):\n"
                    "    try:\n"
                    "        return a / b\n"
                    "    except ZeroDivisionError:\n"
                    "        return None\n"
                    "\n"
                    "\n"
                    "print(safe_divide(10, 2))\n"
                    "print(safe_divide(10, 0))\n",
    },
    {
        'id': 'char_count',
        'title': 'Count The Letters',
        'topic': 'functions · loops · dictionaries',
        'task': "כתבו פונקציה בשם char_count\n"
                "פרמטר אחד, בשם word\n"
                "היא מחזירה מילון: כל אות במילה היא מפתח, וכמה\n"
                "פעמים היא הופיעה היא הערך\n"
                "(רגישות לרישיות - 'A' ו-'a' נספרות בנפרד)\n"
                "אפשר גם עם dict רגיל, ואפשר גם עם defaultdict שניתן למעלה",
        'setup': "from collections import defaultdict\n",
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
        'task': "כתבו פונקציה בשם indexed_pairs\n"
                "פרמטר אחד, בשם items - רשימה\n"
                "היא מחזירה רשימה של זוגות (מיקום, איבר) לכל איבר ברשימה\n"
                "השתמשו ב-enumerate במקום לספור מיקום בעצמכם",
        'solution': "def indexed_pairs(items):\n"
                    "    return list(enumerate(items))\n"
                    "\n"
                    "\n"
                    "print(indexed_pairs(['a', 'b', 'c']))\n",
    },
    {
        'id': 'pair_up',
        'title': 'Pair Two Lists Together',
        'topic': 'zip',
        'task': "כתבו פונקציה בשם pair_up\n"
                "שני פרמטרים: names ו-scores - שתי רשימות באותו אורך\n"
                "היא מחזירה רשימה של זוגות, כל שם עם הציון שלו באותו מיקום\n"
                "השתמשו ב-zip",
        'solution': "def pair_up(names, scores):\n"
                    "    return list(zip(names, scores))\n"
                    "\n"
                    "\n"
                    "print(pair_up(['Ann', 'Bo'], [90, 80]))\n",
    },
    {
        'id': 'fibonacci_list',
        'title': 'The Fibonacci Sequence',
        'topic': 'for loop · building a list',
        'task': "כתבו פונקציה בשם fibonacci_list\n"
                "פרמטר אחד, בשם n\n"
                "היא מחזירה רשימה עם n המספרים הראשונים בסדרת פיבונאצ'י\n"
                "(כל מספר הוא סכום שני המספרים שלפניו: 0, 1, 1, 2, 3, 5, ...)",
        'solution': "def fibonacci_list(n):\n"
                    "    result = []\n"
                    "    a, b = 0, 1\n"
                    "    for _ in range(n):\n"
                    "        result.append(a)\n"
                    "        a, b = b, a + b\n"
                    "    return result\n"
                    "\n"
                    "\n"
                    "print(fibonacci_list(6))\n",
    },
    {
        'id': 'matrix_row_sums',
        'title': 'Sum Each Row',
        'topic': 'list comprehension · sum',
        'task': "כתבו פונקציה בשם matrix_row_sums\n"
                "פרמטר אחד, בשם matrix - רשימה של רשימות של מספרים\n"
                "היא מחזירה רשימה עם הסכום של כל שורה בנפרד\n"
                "כתבו את זה כ-list comprehension, עם sum על כל שורה",
        'solution': "def matrix_row_sums(matrix):\n"
                    "    return [sum(row) for row in matrix]\n"
                    "\n"
                    "\n"
                    "print(matrix_row_sums([[1, 2, 3], [4, 5], [6]]))\n",
    },
    {
        'id': 'second_largest',
        'title': 'The Second Largest',
        'topic': 'for loop · tracking two values',
        'task': "כתבו פונקציה בשם second_largest\n"
                "פרמטר אחד, בשם numbers - רשימה של מספרים שונים זה מזה\n"
                "היא מחזירה את המספר השני בגודלו ברשימה, בלי למיין אותה\n"
                "עברו על הרשימה פעם אחת, ושמרו את הגדול והשני בגודלו תוך כדי",
        'solution': "def second_largest(numbers):\n"
                    "    first = second = None\n"
                    "    for n in numbers:\n"
                    "        if first is None or n > first:\n"
                    "            second = first\n"
                    "            first = n\n"
                    "        elif n != first and (second is None or n > second):\n"
                    "            second = n\n"
                    "    return second\n"
                    "\n"
                    "\n"
                    "print(second_largest([4, 1, 9, 2]))\n",
    },
    {
        'id': 'group_by_length',
        'title': 'Group By Word Length',
        'topic': 'for loop · dict of lists',
        'task': "כתבו פונקציה בשם group_by_length\n"
                "פרמטר אחד, בשם words - רשימה של מילים\n"
                "היא מחזירה מילון: כל אורך מילה הוא מפתח, והערך הוא רשימה\n"
                "של כל המילים באורך הזה\n"
                "עבור כל מילה - אם האורך שלה עוד לא מפתח במילון, התחילו בשבילו\n"
                "רשימה ריקה, ואז הוסיפו אליה את המילה\n"
                "אפשר גם עם dict רגיל, ואפשר גם עם defaultdict שניתן למעלה",
        'setup': "from collections import defaultdict\n",
        'solution': "def group_by_length(words):\n"
                    "    groups = {}\n"
                    "    for w in words:\n"
                    "        n = len(w)\n"
                    "        if n not in groups:\n"
                    "            groups[n] = []\n"
                    "        groups[n].append(w)\n"
                    "    return groups\n"
                    "\n"
                    "\n"
                    "print(group_by_length(['a', 'bb', 'cc', 'ddd', 'e']))\n",
    },
    {
        'id': 'nested_get',
        'title': 'Safe Nested Lookup',
        'topic': 'dict of dicts · get',
        'task': "כתבו פונקציה בשם nested_get\n"
                "שלושה פרמטרים: d (מילון של מילונים), outer_key ו-inner_key\n"
                "היא מחזירה את d[outer_key][inner_key]\n"
                "אבל אם outer_key לא קיים ב-d, או ש-inner_key לא קיים\n"
                "במילון הפנימי - מחזירה None במקום לקרוס\n"
                "השתמשו ב-get במקום בסוגריים מרובעים",
        'solution': "def nested_get(d, outer_key, inner_key):\n"
                    "    inner = d.get(outer_key)\n"
                    "    if inner is None:\n"
                    "        return None\n"
                    "    return inner.get(inner_key)\n"
                    "\n"
                    "\n"
                    "print(nested_get({'a': {'x': 1}}, 'a', 'x'))\n"
                    "print(nested_get({'a': {'x': 1}}, 'z', 'x'))\n",
    },
    {
        'id': 'extract_numbers',
        'title': 'Extract The Numbers',
        'topic': 'regex · re.findall',
        'task': "כתבו פונקציה בשם extract_numbers\n"
                "פרמטר אחד, בשם text\n"
                "יש לכם למעלה pattern מוכן בשם NUMBER_PATTERN, שכבר יודע\n"
                "לזהות רצף של ספרות בתוך טקסט - לא צריך לכתוב regex בעצמכם\n"
                "השתמשו ב-re.findall עם ה-pattern הזה כדי למצוא את כל\n"
                "רצפי הספרות בטקסט, והחזירו אותם כרשימה של מספרים שלמים\n"
                "(לא כמחרוזות - צריך להמיר כל אחד עם int)",
        'setup': "import re\n"
                 "\n"
                 "# a ready-made pattern - matches one or more digits in a row\n"
                 "NUMBER_PATTERN = r'\\d+'\n",
        'solution': "def extract_numbers(text):\n"
                    "    matches = re.findall(NUMBER_PATTERN, text)\n"
                    "    return [int(m) for m in matches]\n"
                    "\n"
                    "\n"
                    "print(extract_numbers('I have 3 cats and 12 dogs, and 007 fish'))\n",
    },
    {
        'id': 'sort_by_score',
        'title': 'Sort By Score',
        'topic': 'sorted · key · lambda',
        'task': "כתבו פונקציה בשם sort_by_score\n"
                "פרמטר אחד, בשם records - רשימה של tuples בצורת (name, score)\n"
                "היא מחזירה את הרשימה ממוינת לפי score, מהגבוה לנמוך\n"
                "השתמשו ב-sorted עם key שהוא lambda, ו-reverse=True",
        'solution': "def sort_by_score(records):\n"
                    "    return sorted(records, key=lambda r: r[1], reverse=True)\n"
                    "\n"
                    "\n"
                    "print(sort_by_score([('Ann', 70), ('Bo', 95), ('Cy', 82)]))\n",
    },
    {
        'id': 'safe_int',
        'title': 'Convert, Safely',
        'topic': 'try / except · ValueError',
        'task': "כתבו פונקציה בשם safe_int\n"
                "פרמטר אחד, בשם text\n"
                "היא מנסה להפוך את text למספר שלם ולהחזיר אותו\n"
                "אבל אם text לא מייצג מספר, int(text) מפילה את התוכנית עם\n"
                "שגיאת ValueError. תפסו אותה עם try/except, והחזירו None\n"
                "במקום לקרוס",
        'solution': "def safe_int(text):\n"
                    "    try:\n"
                    "        return int(text)\n"
                    "    except ValueError:\n"
                    "        return None\n"
                    "\n"
                    "\n"
                    "print(safe_int('42'))\n"
                    "print(safe_int('abc'))\n",
    },
    {
        'id': 'merge_dicts',
        'title': 'Merge Two Dicts',
        'topic': 'dict · ** unpacking',
        'task': "כתבו פונקציה בשם merge_dicts\n"
                "שני פרמטרים: a ו-b - שני מילונים\n"
                "היא מחזירה מילון חדש שמשלב את שניהם - אם אותו מפתח קיים\n"
                "בשניהם, הערך מ-b הוא זה שנשאר\n"
                "השתמשו בפריסה (unpacking) עם **, לא בלולאה",
        'solution': "def merge_dicts(a, b):\n"
                    "    return {**a, **b}\n"
                    "\n"
                    "\n"
                    "print(merge_dicts({'a': 1, 'b': 2}, {'b': 9, 'c': 3}))\n",
    },
    {
        'id': 'top_n',
        'title': 'The Top N',
        'topic': 'sorted · slicing',
        'task': "כתבו פונקציה בשם top_n\n"
                "שני פרמטרים: numbers (רשימה של מספרים) ו-n\n"
                "היא מחזירה את n המספרים הגדולים ביותר ברשימה, ממוינים\n"
                "מהגבוה לנמוך\n"
                "מיינו את כל הרשימה מהגבוה לנמוך, ואז קחו את n הראשונים עם חיתוך",
        'solution': "def top_n(numbers, n):\n"
                    "    return sorted(numbers, reverse=True)[:n]\n"
                    "\n"
                    "\n"
                    "print(top_n([4, 1, 9, 2, 7], 3))\n",
    },
]
