# -*- coding: utf-8 -*-
"""
draft_medium_questions.py  --  REVIEW ONLY, not wired into the game yet.

Same idea as draft_easy_questions.py, one tier up: MEDIUM-level questions
for Exam Rehearsal, trying to touch as many different topics as possible
rather than going deep on any one - nested loops, list comprehensions
(plain and filtered), default parameters, sorting with a key function,
f-string formatting, returning more than one value at once (as a tuple),
flattening nested lists, de-duplicating while keeping order, palindrome/
anagram checks, word-frequency counting, and per-row work on a list of
lists.

NOT here, on purpose:
  - recursion - not covered in this course, dropped entirely (was
    'factorial'), not just moved
  - enumerate, zip, and the Fibonacci sequence - moved up to EXPERT
    (draft_expert_questions.py) - this is a basics course and some
    students still struggle with plain functions, so these don't belong
    at the "medium" tier
  - matrix_row_sums and second_largest also moved to EXPERT for the same
    reason

NOTE - same 'while' ban as easy: the shared judge hard-bans the word
"while" anywhere in submitted code (a runaway while would freeze the
browser tab), and also bans "import" (so no collections.Counter, no
random, no math - everything here is written with plain built-ins and
loops instead).

Same shape as draft_easy_questions.py: {id, title, topic, task (Hebrew),
solution (English)}. make_easy_review.py's build() is reused (it takes the
questions module + output path as arguments) to turn this into medium.html.
"""

QUESTIONS = [

    {
        'id': 'nested_loop_sum',
        'title': 'Sum Every Number, Everywhere',
        'topic': 'nested for loops',
        'task': "כתבו פונקציה בשם nested_loop_sum\n"
                "פרמטר אחד, בשם rows - רשימה של רשימות של מספרים\n"
                "היא מחזירה את הסכום של כל המספרים, בכל השורות יחד\n"
                "עברו על השורות עם לולאת for, ובתוך כל שורה עוד לולאת for",
        'solution': "def nested_loop_sum(rows):\n"
                    "    total = 0\n"
                    "    for row in rows:\n"
                    "        for n in row:\n"
                    "            total += n\n"
                    "    return total\n"
                    "\n"
                    "\n"
                    "print(nested_loop_sum([[1, 2, 3], [4, 5], [6]]))\n",
    },
    {
        'id': 'squares_list',
        'title': 'Square Every Number',
        'topic': 'list comprehension',
        'task': "כתבו פונקציה בשם squares_list\n"
                "פרמטר אחד, בשם numbers - רשימה של מספרים\n"
                "היא מחזירה רשימה חדשה, עם הריבוע של כל מספר\n"
                "כתבו את זה כ-list comprehension, בשורה אחת",
        'solution': "def squares_list(numbers):\n"
                    "    return [n ** 2 for n in numbers]\n"
                    "\n"
                    "\n"
                    "print(squares_list([1, 2, 3, 4]))\n",
    },
    {
        'id': 'evens_only',
        'title': 'Just The Even Ones',
        'topic': 'list comprehension · if',
        'task': "כתבו פונקציה בשם evens_only\n"
                "פרמטר אחד, בשם numbers - רשימה של מספרים\n"
                "היא מחזירה רשימה חדשה עם רק המספרים הזוגיים\n"
                "כתבו את זה כ-list comprehension עם תנאי, בשורה אחת",
        'solution': "def evens_only(numbers):\n"
                    "    return [n for n in numbers if n % 2 == 0]\n"
                    "\n"
                    "\n"
                    "print(evens_only([1, 2, 3, 4, 5, 6]))\n",
    },
    {
        'id': 'greet_with_default',
        'title': 'Greet, With A Default',
        'topic': 'default parameters · f-strings',
        'task': "כתבו פונקציה בשם greet_with_default\n"
                "פרמטר אחד, בשם name, עם ערך ברירת מחדל 'Guest'\n"
                "היא מחזירה 'Hello, ' ואז השם ואז '!' - למשל 'Hello, Dana!'\n"
                "השתמשו ב-f-string",
        'solution': "def greet_with_default(name='Guest'):\n"
                    "    return f'Hello, {name}!'\n"
                    "\n"
                    "\n"
                    "print(greet_with_default())\n"
                    "print(greet_with_default('Dana'))\n",
    },
    {
        'id': 'sort_by_length',
        'title': 'Sort By Length',
        'topic': 'sorted · key parameter',
        'task': "כתבו פונקציה בשם sort_by_length\n"
                "פרמטר אחד, בשם words - רשימה של מילים\n"
                "היא מחזירה את הרשימה ממוינת לפי אורך המילה, מהקצרה לארוכה\n"
                "יש ל-sorted פרמטר key שמקבל פונקציה - איזו פונקציה מודדת אורך",
        'solution': "def sort_by_length(words):\n"
                    "    return sorted(words, key=len)\n"
                    "\n"
                    "\n"
                    "print(sort_by_length(['banana', 'kiwi', 'fig']))\n",
    },
    {
        'id': 'format_price',
        'title': 'Format As A Price',
        'topic': 'f-strings · number formatting',
        'task': "כתבו פונקציה בשם format_price\n"
                "פרמטר אחד, בשם amount - מספר\n"
                "היא מחזירה אותו כמחרוזת מחיר, עם סימן $ ושתי ספרות אחרי הנקודה\n"
                "למשל 9 הופך ל-'$9.00' - השתמשו ב-f-string עם :.2f",
        'solution': "def format_price(amount):\n"
                    "    return f'${amount:.2f}'\n"
                    "\n"
                    "\n"
                    "print(format_price(9))\n"
                    "print(format_price(3.5))\n",
    },
    {
        'id': 'min_and_max',
        'title': 'The Smallest And The Biggest',
        'topic': 'returning more than one value',
        'task': "כתבו פונקציה בשם min_and_max\n"
                "פרמטר אחד, בשם numbers - רשימה של מספרים\n"
                "היא מחזירה tuple: (המספר הקטן ביותר, המספר הגדול ביותר)",
        'solution': "def min_and_max(numbers):\n"
                    "    return (min(numbers), max(numbers))\n"
                    "\n"
                    "\n"
                    "print(min_and_max([4, 1, 9, 2]))\n",
    },
    {
        'id': 'flatten',
        'title': 'Flatten The List',
        'topic': 'nested for loops · append',
        'task': "כתבו פונקציה בשם flatten\n"
                "פרמטר אחד, בשם nested - רשימה של רשימות\n"
                "היא מחזירה רשימה אחת שטוחה, עם כל האיברים מכל השורות, לפי הסדר",
        'solution': "def flatten(nested):\n"
                    "    result = []\n"
                    "    for row in nested:\n"
                    "        for item in row:\n"
                    "            result.append(item)\n"
                    "    return result\n"
                    "\n"
                    "\n"
                    "print(flatten([[1, 2], [3], [4, 5, 6]]))\n",
    },
    {
        'id': 'remove_duplicates',
        'title': 'Remove Duplicates, Keep The Order',
        'topic': 'for loop · in · building a list',
        'task': "כתבו פונקציה בשם remove_duplicates\n"
                "פרמטר אחד, בשם items - רשימה\n"
                "היא מחזירה רשימה חדשה בלי כפילויות, כשהסדר המקורי נשמר\n"
                "עברו על הרשימה, והוסיפו איבר לרשימה החדשה רק אם הוא לא כבר בה",
        'solution': "def remove_duplicates(items):\n"
                    "    seen = []\n"
                    "    for item in items:\n"
                    "        if item not in seen:\n"
                    "            seen.append(item)\n"
                    "    return seen\n"
                    "\n"
                    "\n"
                    "print(remove_duplicates([1, 2, 2, 3, 1, 4]))\n",
    },
    {
        'id': 'is_palindrome',
        'title': 'Is It A Palindrome',
        'topic': 'string slicing · [::-1]',
        'task': "כתבו פונקציה בשם is_palindrome\n"
                "פרמטר אחד, בשם word\n"
                "היא מחזירה True אם המילה נקראת אותו דבר גם הפוך, אחרת False\n"
                "(לא רגישה לרישיות) - השתמשו בחיתוך word[::-1] כדי להפוך אותה",
        'solution': "def is_palindrome(word):\n"
                    "    clean = word.lower()\n"
                    "    return clean == clean[::-1]\n"
                    "\n"
                    "\n"
                    "print(is_palindrome('level'))\n"
                    "print(is_palindrome('hello'))\n"
                    "print(is_palindrome('Racecar'))\n",
    },
    {
        'id': 'is_anagram',
        'title': 'Is It An Anagram',
        'topic': 'sorted · string comparison',
        'task': "כתבו פונקציה בשם is_anagram\n"
                "שני פרמטרים: word1 ו-word2\n"
                "היא מחזירה True אם שתי המילים מורכבות מאותן אותיות בדיוק,\n"
                "בכל סדר, אחרת False - (לא רגישה לרישיות)\n"
                "מיינו את האותיות של כל מילה והשוו",
        'solution': "def is_anagram(word1, word2):\n"
                    "    return sorted(word1.lower()) == sorted(word2.lower())\n"
                    "\n"
                    "\n"
                    "print(is_anagram('listen', 'silent'))\n"
                    "print(is_anagram('hello', 'world'))\n",
    },
    {
        'id': 'word_frequency',
        'title': 'Word Frequency',
        'topic': 'for loop · dict',
        'task': "כתבו פונקציה בשם word_frequency\n"
                "פרמטר אחד, בשם words - רשימה של מילים\n"
                "היא מחזירה מילון: כל מילה היא מפתח, וכמה פעמים היא\n"
                "הופיעה ברשימה היא הערך\n"
                "אפשר גם עם dict רגיל, ואפשר גם עם defaultdict שניתן למעלה",
        'setup': "from collections import defaultdict\n",
        'solution': "def word_frequency(words):\n"
                    "    counts = {}\n"
                    "    for w in words:\n"
                    "        counts[w] = counts.get(w, 0) + 1\n"
                    "    return counts\n"
                    "\n"
                    "\n"
                    "print(word_frequency(['a', 'b', 'a', 'c', 'b', 'a']))\n",
    },
    {
        'id': 'average_rounded',
        'title': 'The Average, Rounded',
        'topic': 'sum / len · round',
        'task': "כתבו פונקציה בשם average_rounded\n"
                "פרמטר אחד, בשם numbers - רשימה של מספרים\n"
                "היא מחזירה את הממוצע שלהם, מעוגל לשתי ספרות אחרי הנקודה",
        'solution': "def average_rounded(numbers):\n"
                    "    return round(sum(numbers) / len(numbers), 2)\n"
                    "\n"
                    "\n"
                    "print(average_rounded([1, 2, 4]))\n",
    },
    {
        'id': 'count_positive',
        'title': 'Count The Positives',
        'topic': 'for loop · if · counter',
        'task': "כתבו פונקציה בשם count_positive\n"
                "פרמטר אחד, בשם numbers - רשימה של מספרים\n"
                "היא מחזירה כמה מספרים ברשימה גדולים מ-0\n"
                "הפעם בלי list comprehension - התחילו ממונה על 0, עברו על\n"
                "הרשימה עם for, והוסיפו 1 למונה כל פעם שהמספר גדול מ-0",
        'solution': "def count_positive(numbers):\n"
                    "    count = 0\n"
                    "    for n in numbers:\n"
                    "        if n > 0:\n"
                    "            count += 1\n"
                    "    return count\n"
                    "\n"
                    "\n"
                    "print(count_positive([-5, 8, -2, 10, 0, 3]))\n",
    },
    {
        'id': 'is_valid_password',
        'title': 'Is The Password Valid',
        'topic': 'strings · loop · combined conditions',
        'task': "כתבו פונקציה בשם is_valid_password\n"
                "פרמטר אחד, בשם password\n"
                "היא מחזירה True רק אם הסיסמה באורך 8 תווים לפחות, וגם יש בה\n"
                "לפחות ספרה אחת - אחרת False\n"
                "לבדיקה שתו הוא ספרה יש למחרוזת פעולה מוכנה",
        'solution': "def is_valid_password(password):\n"
                    "    if len(password) < 8:\n"
                    "        return False\n"
                    "    for ch in password:\n"
                    "        if ch.isdigit():\n"
                    "            return True\n"
                    "    return False\n"
                    "\n"
                    "\n"
                    "print(is_valid_password('abc12345'))\n"
                    "print(is_valid_password('ab1'))\n"
                    "print(is_valid_password('abcdefgh'))\n",
    },
    {
        'id': 'split_full_name',
        'title': 'Split The Full Name',
        'topic': 'string · split · tuple',
        'task': "כתבו פונקציה בשם split_full_name\n"
                "פרמטר אחד, בשם full - מחרוזת בצורת 'First Last'\n"
                "היא מחזירה tuple: (First, Last) - שני החלקים בנפרד",
        'solution': "def split_full_name(full):\n"
                    "    first, last = full.split()\n"
                    "    return (first, last)\n"
                    "\n"
                    "\n"
                    "print(split_full_name('Ada Lovelace'))\n",
    },
    {
        'id': 'running_total',
        'title': 'The Running Total',
        'topic': 'for loop · building a list',
        'task': "כתבו פונקציה בשם running_total\n"
                "פרמטר אחד, בשם numbers - רשימה של מספרים\n"
                "היא מחזירה רשימה חדשה: כל איבר בה הוא הסכום המצטבר עד\n"
                "המיקום הזה - למשל [1, 2, 3, 4] הופך ל-[1, 3, 6, 10]",
        'solution': "def running_total(numbers):\n"
                    "    result = []\n"
                    "    total = 0\n"
                    "    for n in numbers:\n"
                    "        total += n\n"
                    "        result.append(total)\n"
                    "    return result\n"
                    "\n"
                    "\n"
                    "print(running_total([1, 2, 3, 4]))\n",
    },
    {
        'id': 'common_elements',
        'title': 'What They Have In Common',
        'topic': 'list comprehension · in',
        'task': "כתבו פונקציה בשם common_elements\n"
                "שני פרמטרים: a ו-b - שתי רשימות\n"
                "היא מחזירה רשימה חדשה עם כל האיברים מ-a שנמצאים גם ב-b\n"
                "(שלא כמו intersection על sets, כאן זו רשימה רגילה - הסדר\n"
                "והכפילויות של a נשמרים)",
        'solution': "def common_elements(a, b):\n"
                    "    return [x for x in a if x in b]\n"
                    "\n"
                    "\n"
                    "print(common_elements([1, 2, 3, 4], [2, 4, 6]))\n",
    },
    {
        'id': 'repeat_word',
        'title': 'Repeat It',
        'topic': 'string · * operator',
        'task': "כתבו פונקציה בשם repeat_word\n"
                "שני פרמטרים: word ו-n\n"
                "היא מחזירה את word חוזר על עצמו n פעמים, ברצף, בלי רווחים\n"
                "אפשר להכפיל מחרוזת במספר עם *, בדיוק כמו מספרים",
        'solution': "def repeat_word(word, n):\n"
                    "    return word * n\n"
                    "\n"
                    "\n"
                    "print(repeat_word('ab', 3))\n",
    },
    {
        'id': 'filter_by_score',
        'title': 'Who Passed',
        'topic': 'list of dicts · comprehension',
        'task': "כתבו פונקציה בשם filter_by_score\n"
                "שני פרמטרים: records (רשימה של מילונים, לכל אחד יש 'name' "
                "ו-'score') ו-threshold\n"
                "היא מחזירה רשימה של השמות (name) בלבד, של כל הרשומות שבהן\n"
                "score גדול או שווה ל-threshold",
        'solution': "def filter_by_score(records, threshold):\n"
                    "    return [r['name'] for r in records if r['score'] >= threshold]\n"
                    "\n"
                    "\n"
                    "print(filter_by_score([{'name': 'Ann', 'score': 70}, "
                    "{'name': 'Bo', 'score': 50}, {'name': 'Cy', 'score': 90}], 60))\n",
    },
]
