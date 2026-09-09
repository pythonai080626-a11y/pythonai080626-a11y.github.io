# -*- coding: utf-8 -*-
"""
draft_easy_questions.py  --  REVIEW ONLY, not wired into the game yet.

A big first pass at EASY-level questions for Exam Rehearsal, covering the
topics not in the game yet: if/elif/else, for loops (break, continue), and
especially the data-type operations - list (append, pop, insert, remove,
sort, sorted, reverse, count, index), tuple (unpack, count, index), dict
(get, keys, values, set, pop), set (union, intersection, difference, add),
and string (join, split, replace).

NOTE - no 'while' anywhere: the shared judge (RUNNER_PY, the same one
func_01 uses) hard-bans the word "while" in submitted code everywhere, on
purpose - a runaway while loop would freeze the browser tab. So every loop
question here uses for (with break/continue where that is the point), even
count_until_zero, which would more naturally be a while - discovered this
the hard way once this batch was wired into the real game.

Same shape as exam_prep/questions.py - every question is a function, same
LANGUAGE rule (Hebrew task, English code) - but there is no 'hint' or
'solution'-button field here, because this file is not judged or played;
make_easy_review.py runs every 'solution' for real and captures its actual
printed output, then lays task + expected output + code out on one static
page (easy.html) so it can be read over quickly, before any of this is
turned into real game questions with tests/require/forbid and a judge.

Each entry: {id, title, topic, task (Hebrew), solution (English, full
runnable code ending in one or more print(...) calls)}.
"""

QUESTIONS = [

    # ------------------------------------------------------------- if / elif / else
    {
        'id': 'classify_number',
        'title': 'Positive, Negative, or Zero',
        'topic': 'if / elif / else',
        'task': "כתבו פונקציה בשם classify_number\n"
                "פרמטר אחד, בשם n\n"
                "אם n גדול מ-0 היא מחזירה 'positive'\n"
                "אם n קטן מ-0 היא מחזירה 'negative'\n"
                "אחרת היא מחזירה 'zero'",
        'solution': "def classify_number(n):\n"
                    "    if n > 0:\n"
                    "        return 'positive'\n"
                    "    elif n < 0:\n"
                    "        return 'negative'\n"
                    "    else:\n"
                    "        return 'zero'\n"
                    "\n"
                    "\n"
                    "print(classify_number(5))\n"
                    "print(classify_number(-3))\n"
                    "print(classify_number(0))\n",
    },
    {
        'id': 'is_even',
        'title': 'Even Or Odd',
        'topic': 'if / else · % operator',
        'task': "כתבו פונקציה בשם is_even\n"
                "פרמטר אחד, בשם n\n"
                "היא מחזירה True אם n זוגי, ו-False אם הוא אי-זוגי",
        'solution': "def is_even(n):\n"
                    "    if n % 2 == 0:\n"
                    "        return True\n"
                    "    else:\n"
                    "        return False\n"
                    "\n"
                    "\n"
                    "print(is_even(4))\n"
                    "print(is_even(7))\n",
    },
    {
        'id': 'letter_grade',
        'title': 'Letter Grade',
        'topic': 'if / elif / else · chained ranges',
        'task': "כתבו פונקציה בשם letter_grade\n"
                "פרמטר אחד, בשם score\n"
                "ציון 90 ומעלה מחזיר 'A'\n"
                "ציון 80 עד 89 מחזיר 'B'\n"
                "ציון 70 עד 79 מחזיר 'C'\n"
                "כל ציון נמוך יותר מחזיר 'F'",
        'solution': "def letter_grade(score):\n"
                    "    if score >= 90:\n"
                    "        return 'A'\n"
                    "    elif score >= 80:\n"
                    "        return 'B'\n"
                    "    elif score >= 70:\n"
                    "        return 'C'\n"
                    "    else:\n"
                    "        return 'F'\n"
                    "\n"
                    "\n"
                    "print(letter_grade(95))\n"
                    "print(letter_grade(82))\n"
                    "print(letter_grade(55))\n",
    },
    {
        'id': 'bigger_of_two',
        'title': 'The Bigger One',
        'topic': 'if / else · comparison',
        'task': "כתבו פונקציה בשם bigger_of_two\n"
                "שני פרמטרים: a ו-b\n"
                "היא מחזירה את הגדול מביניהם",
        'solution': "def bigger_of_two(a, b):\n"
                    "    if a > b:\n"
                    "        return a\n"
                    "    else:\n"
                    "        return b\n"
                    "\n"
                    "\n"
                    "print(bigger_of_two(3, 9))\n"
                    "print(bigger_of_two(10, 2))\n",
    },

    # ------------------------------------------------------------------------ loops
    {
        'id': 'sum_up_to',
        'title': 'Sum 1 To N',
        'topic': 'for loop · range',
        'task': "כתבו פונקציה בשם sum_up_to\n"
                "פרמטר אחד, בשם n\n"
                "היא מחזירה את הסכום של כל המספרים מ-1 עד n, כולל\n"
                "השתמשו בלולאת for ובפונקציית range",
        'solution': "def sum_up_to(n):\n"
                    "    total = 0\n"
                    "    for i in range(1, n + 1):\n"
                    "        total += i\n"
                    "    return total\n"
                    "\n"
                    "\n"
                    "print(sum_up_to(5))\n",
    },
    {
        'id': 'count_vowels',
        'title': 'Count The Vowels',
        'topic': 'for loop · if · strings',
        'task': "כתבו פונקציה בשם count_vowels\n"
                "פרמטר אחד, בשם word\n"
                "היא מחזירה כמה מהאותיות במילה הן תנועות: a, e, i, o, u\n"
                "(לא רגישה לרישיות)\n"
                "עברו על אותיות המילה עם לולאת for",
        'solution': "def count_vowels(word):\n"
                    "    vowels = 'aeiou'\n"
                    "    count = 0\n"
                    "    for ch in word.lower():\n"
                    "        if ch in vowels:\n"
                    "            count += 1\n"
                    "    return count\n"
                    "\n"
                    "\n"
                    "print(count_vowels('Hello World'))\n",
    },
    {
        'id': 'first_divisible_by',
        'title': 'First One That Divides',
        'topic': 'for loop · break',
        'task': "כתבו פונקציה בשם first_divisible_by\n"
                "שני פרמטרים: numbers (רשימה) ו-k\n"
                "היא מחזירה את המספר הראשון ברשימה שמתחלק ב-k בלי שארית\n"
                "עברו על הרשימה עם לולאת for, ועצרו אותה עם break ברגע שמוצאים\n"
                "את המספר - אין טעם להמשיך הלאה",
        'solution': "def first_divisible_by(numbers, k):\n"
                    "    result = None\n"
                    "    for n in numbers:\n"
                    "        if n % k == 0:\n"
                    "            result = n\n"
                    "            break\n"
                    "    return result\n"
                    "\n"
                    "\n"
                    "print(first_divisible_by([7, 9, 12, 15], 3))\n",
    },
    {
        'id': 'sum_skip_negatives',
        'title': 'Sum, Skipping The Negatives',
        'topic': 'for loop · continue',
        'task': "כתבו פונקציה בשם sum_skip_negatives\n"
                "פרמטר אחד, בשם numbers - רשימה של מספרים\n"
                "היא מחזירה את סכום כל המספרים החיוביים ברשימה\n"
                "עברו על הרשימה עם לולאת for, ודלגו על מספרים שליליים עם\n"
                "continue - במקום לבדוק אותם עם if נוסף",
        'solution': "def sum_skip_negatives(numbers):\n"
                    "    total = 0\n"
                    "    for n in numbers:\n"
                    "        if n < 0:\n"
                    "            continue\n"
                    "        total += n\n"
                    "    return total\n"
                    "\n"
                    "\n"
                    "print(sum_skip_negatives([3, -2, 5, -8, 1]))\n",
    },
    {
        'id': 'count_until_zero',
        'title': 'Count Until The First Zero',
        'topic': 'for loop · break',
        'task': "כתבו פונקציה בשם count_until_zero\n"
                "פרמטר אחד, בשם numbers - רשימה של מספרים\n"
                "היא מחזירה כמה מספרים יש ברשימה עד המספר 0 הראשון, לא כולל אותו\n"
                "(אם אין בכלל 0 ברשימה, מחזירה את האורך של כל הרשימה)\n"
                "עברו על הרשימה עם לולאת for, ועצרו אותה עם break ברגע שמגיעים ל-0",
        'solution': "def count_until_zero(numbers):\n"
                    "    count = 0\n"
                    "    for n in numbers:\n"
                    "        if n == 0:\n"
                    "            break\n"
                    "        count += 1\n"
                    "    return count\n"
                    "\n"
                    "\n"
                    "print(count_until_zero([4, 8, 2, 0, 9, 1]))\n",
    },

    # -------------------------------------------------------------------- lists
    {
        'id': 'append_item',
        'title': 'Add To The End',
        'topic': 'list · append',
        'task': "כתבו פונקציה בשם append_item\n"
                "שני פרמטרים: items (רשימה) ו-value\n"
                "היא מוסיפה את value לסוף הרשימה, ומחזירה את הרשימה",
        'solution': "def append_item(items, value):\n"
                    "    items.append(value)\n"
                    "    return items\n"
                    "\n"
                    "\n"
                    "print(append_item([1, 2, 3], 4))\n",
    },
    {
        'id': 'pop_last',
        'title': 'Remove The Last One',
        'topic': 'list · pop',
        'task': "כתבו פונקציה בשם pop_last\n"
                "פרמטר אחד, בשם items - רשימה\n"
                "היא מסירה את האיבר האחרון מהרשימה, ומחזירה את הרשימה",
        'solution': "def pop_last(items):\n"
                    "    items.pop()\n"
                    "    return items\n"
                    "\n"
                    "\n"
                    "print(pop_last([1, 2, 3, 4]))\n",
    },
    {
        'id': 'pop_at',
        'title': 'Remove By Position',
        'topic': 'list · pop(index)',
        'task': "כתבו פונקציה בשם pop_at\n"
                "שני פרמטרים: items (רשימה) ו-index\n"
                "היא מסירה מהרשימה את האיבר במיקום index, ומחזירה את האיבר שהוסר\n"
                "(לא את הרשימה)",
        'solution': "def pop_at(items, index):\n"
                    "    return items.pop(index)\n"
                    "\n"
                    "\n"
                    "print(pop_at([10, 20, 30, 40], 1))\n",
    },
    {
        'id': 'insert_at',
        'title': 'Insert In The Middle',
        'topic': 'list · insert',
        'task': "כתבו פונקציה בשם insert_at\n"
                "שלושה פרמטרים: items (רשימה), index ו-value\n"
                "היא מכניסה את value לרשימה במיקום index, ומחזירה את הרשימה",
        'solution': "def insert_at(items, index, value):\n"
                    "    items.insert(index, value)\n"
                    "    return items\n"
                    "\n"
                    "\n"
                    "print(insert_at([1, 2, 4], 2, 3))\n",
    },
    {
        'id': 'remove_value',
        'title': 'Remove By Value',
        'topic': 'list · remove',
        'task': "כתבו פונקציה בשם remove_value\n"
                "שני פרמטרים: items (רשימה) ו-value\n"
                "היא מסירה מהרשימה את ההופעה הראשונה של value, ומחזירה את הרשימה",
        'solution': "def remove_value(items, value):\n"
                    "    items.remove(value)\n"
                    "    return items\n"
                    "\n"
                    "\n"
                    "print(remove_value([5, 3, 8, 3], 3))\n",
    },
    {
        'id': 'sort_ascending',
        'title': 'Sort It',
        'topic': 'list · sort',
        'task': "כתבו פונקציה בשם sort_ascending\n"
                "פרמטר אחד, בשם items - רשימה של מספרים\n"
                "היא ממיינת את הרשימה מהקטן לגדול, ומחזירה אותה",
        'solution': "def sort_ascending(items):\n"
                    "    items.sort()\n"
                    "    return items\n"
                    "\n"
                    "\n"
                    "print(sort_ascending([5, 1, 4, 2]))\n",
    },
    {
        'id': 'sorted_copy',
        'title': 'Sort It Without Changing The Original',
        'topic': 'list · sorted',
        'task': "כתבו פונקציה בשם sorted_copy\n"
                "פרמטר אחד, בשם items - רשימה של מספרים\n"
                "היא מחזירה זוג (tuple): רשימה חדשה וממוינת, והרשימה המקורית\n"
                "בלי שהיא השתנתה",
        'solution': "def sorted_copy(items):\n"
                    "    new_list = sorted(items)\n"
                    "    return (new_list, items)\n"
                    "\n"
                    "\n"
                    "print(sorted_copy([3, 1, 2]))\n",
    },
    {
        'id': 'reverse_list',
        'title': 'Flip It Around',
        'topic': 'list · reverse',
        'task': "כתבו פונקציה בשם reverse_list\n"
                "פרמטר אחד, בשם items - רשימה\n"
                "היא הופכת את סדר הרשימה, ומחזירה אותה",
        'solution': "def reverse_list(items):\n"
                    "    items.reverse()\n"
                    "    return items\n"
                    "\n"
                    "\n"
                    "print(reverse_list([1, 2, 3]))\n",
    },
    {
        'id': 'count_value',
        'title': 'How Many Times',
        'topic': 'list · count',
        'task': "כתבו פונקציה בשם count_value\n"
                "שני פרמטרים: items (רשימה) ו-value\n"
                "היא מחזירה כמה פעמים value מופיע ברשימה",
        'solution': "def count_value(items, value):\n"
                    "    return items.count(value)\n"
                    "\n"
                    "\n"
                    "print(count_value([1, 2, 2, 3, 2], 2))\n",
    },
    {
        'id': 'index_of',
        'title': 'Where Is It',
        'topic': 'list · index',
        'task': "כתבו פונקציה בשם index_of\n"
                "שני פרמטרים: items (רשימה) ו-value\n"
                "היא מחזירה את המיקום הראשון של value ברשימה",
        'solution': "def index_of(items, value):\n"
                    "    return items.index(value)\n"
                    "\n"
                    "\n"
                    "print(index_of([10, 20, 30], 20))\n",
    },

    # ------------------------------------------------------------------- tuples
    {
        'id': 'unpack_sum',
        'title': 'Unpack And Add',
        'topic': 'tuple · unpacking',
        'task': "כתבו פונקציה בשם unpack_sum\n"
                "פרמטר אחד, בשם point - tuple של שני מספרים\n"
                "פרקו אותו לשני משתנים בשורה אחת, והחזירו את הסכום שלהם",
        'solution': "def unpack_sum(point):\n"
                    "    x, y = point\n"
                    "    return x + y\n"
                    "\n"
                    "\n"
                    "print(unpack_sum((3, 4)))\n",
    },
    {
        'id': 'count_in_tuple',
        'title': 'Count In A Tuple',
        'topic': 'tuple · count',
        'task': "כתבו פונקציה בשם count_in_tuple\n"
                "שני פרמטרים: t (tuple) ו-value\n"
                "היא מחזירה כמה פעמים value מופיע ב-t",
        'solution': "def count_in_tuple(t, value):\n"
                    "    return t.count(value)\n"
                    "\n"
                    "\n"
                    "print(count_in_tuple((1, 2, 2, 3, 2), 2))\n",
    },
    {
        'id': 'index_in_tuple',
        'title': 'Find In A Tuple',
        'topic': 'tuple · index',
        'task': "כתבו פונקציה בשם index_in_tuple\n"
                "שני פרמטרים: t (tuple) ו-value\n"
                "היא מחזירה את המיקום הראשון של value ב-t",
        'solution': "def index_in_tuple(t, value):\n"
                    "    return t.index(value)\n"
                    "\n"
                    "\n"
                    "print(index_in_tuple((10, 20, 30), 30))\n",
    },

    # --------------------------------------------------------------- dictionaries
    {
        'id': 'get_with_default',
        'title': 'Get, Safely',
        'topic': 'dict · get',
        'task': "כתבו פונקציה בשם get_with_default\n"
                "שני פרמטרים: d (מילון) ו-key\n"
                "היא מחזירה את הערך של key במילון\n"
                "אם המפתח לא קיים, מחזירה את המחרוזת 'not found' - בלי לקרוס",
        'solution': "def get_with_default(d, key):\n"
                    "    return d.get(key, 'not found')\n"
                    "\n"
                    "\n"
                    "print(get_with_default({'a': 1, 'b': 2}, 'b'))\n"
                    "print(get_with_default({'a': 1, 'b': 2}, 'c'))\n",
    },
    {
        'id': 'sorted_keys',
        'title': 'All The Keys, Sorted',
        'topic': 'dict · keys',
        'task': "כתבו פונקציה בשם sorted_keys\n"
                "פרמטר אחד, בשם d - מילון\n"
                "היא מחזירה רשימה ממוינת של כל המפתחות במילון",
        'solution': "def sorted_keys(d):\n"
                    "    return sorted(d.keys())\n"
                    "\n"
                    "\n"
                    "print(sorted_keys({'b': 1, 'a': 2, 'c': 3}))\n",
    },
    {
        'id': 'sum_values',
        'title': 'Sum All The Values',
        'topic': 'dict · values',
        'task': "כתבו פונקציה בשם sum_values\n"
                "פרמטר אחד, בשם d - מילון שהערכים בו הם מספרים\n"
                "היא מחזירה את הסכום של כל הערכים במילון",
        'solution': "def sum_values(d):\n"
                    "    return sum(d.values())\n"
                    "\n"
                    "\n"
                    "print(sum_values({'a': 10, 'b': 20, 'c': 5}))\n",
    },
    {
        'id': 'set_key',
        'title': 'Add A Key',
        'topic': 'dict · assignment',
        'task': "כתבו פונקציה בשם set_key\n"
                "שלושה פרמטרים: d (מילון), key ו-value\n"
                "היא קובעת ש-d[key] שווה ל-value, ומחזירה את המילון",
        'solution': "def set_key(d, key, value):\n"
                    "    d[key] = value\n"
                    "    return d\n"
                    "\n"
                    "\n"
                    "print(set_key({'a': 1}, 'b', 2))\n",
    },
    {
        'id': 'pop_key',
        'title': 'Remove A Key',
        'topic': 'dict · pop',
        'task': "כתבו פונקציה בשם pop_key\n"
                "שני פרמטרים: d (מילון) ו-key\n"
                "היא מסירה מהמילון את המפתח key, ומחזירה את המילון",
        'solution': "def pop_key(d, key):\n"
                    "    d.pop(key)\n"
                    "    return d\n"
                    "\n"
                    "\n"
                    "print(pop_key({'a': 1, 'b': 2}, 'a'))\n",
    },

    # ---------------------------------------------------------------------- sets
    {
        'id': 'union_sorted',
        'title': 'Everything From Both',
        'topic': 'set · union',
        'task': "כתבו פונקציה בשם union_sorted\n"
                "שני פרמטרים: a ו-b - שני sets\n"
                "היא מחזירה רשימה ממוינת של האיחוד (union) של שני הקבוצות -\n"
                "כל איבר שנמצא באחת מהן, לפחות",
        'solution': "def union_sorted(a, b):\n"
                    "    return sorted(a | b)\n"
                    "\n"
                    "\n"
                    "print(union_sorted({1, 2, 3}, {3, 4, 5}))\n",
    },
    {
        'id': 'intersection_sorted',
        'title': 'Only What They Share',
        'topic': 'set · intersection',
        'task': "כתבו פונקציה בשם intersection_sorted\n"
                "שני פרמטרים: a ו-b - שני sets\n"
                "היא מחזירה רשימה ממוינת של החיתוך (intersection) של שתי הקבוצות -\n"
                "רק איברים שנמצאים בשתיהן",
        'solution': "def intersection_sorted(a, b):\n"
                    "    return sorted(a & b)\n"
                    "\n"
                    "\n"
                    "print(intersection_sorted({1, 2, 3, 4}, {3, 4, 5}))\n",
    },
    {
        'id': 'difference_sorted',
        'title': 'What Only The First One Has',
        'topic': 'set · difference',
        'task': "כתבו פונקציה בשם difference_sorted\n"
                "שני פרמטרים: a ו-b - שני sets\n"
                "היא מחזירה רשימה ממוינת של ההפרש (difference) - כל איבר שנמצא\n"
                "ב-a אבל לא ב-b",
        'solution': "def difference_sorted(a, b):\n"
                    "    return sorted(a - b)\n"
                    "\n"
                    "\n"
                    "print(difference_sorted({1, 2, 3, 4}, {3, 4}))\n",
    },
    {
        'id': 'add_to_set',
        'title': 'Add To A Set',
        'topic': 'set · add',
        'task': "כתבו פונקציה בשם add_to_set\n"
                "שני פרמטרים: s (set) ו-item\n"
                "היא מוסיפה את item לקבוצה, ומחזירה רשימה ממוינת של הקבוצה",
        'solution': "def add_to_set(s, item):\n"
                    "    s.add(item)\n"
                    "    return sorted(s)\n"
                    "\n"
                    "\n"
                    "print(add_to_set({1, 2, 3}, 4))\n",
    },

    # -------------------------------------------------------------------- strings
    {
        'id': 'join_with_space',
        'title': 'Join Into One Sentence',
        'topic': 'string · join',
        'task': "כתבו פונקציה בשם join_with_space\n"
                "פרמטר אחד, בשם words - רשימה של מילים\n"
                "היא מחזירה את כל המילים מחוברות למחרוזת אחת, עם רווח בין כל שתיים",
        'solution': "def join_with_space(words):\n"
                    "    return ' '.join(words)\n"
                    "\n"
                    "\n"
                    "print(join_with_space(['I', 'love', 'Python']))\n",
    },
    {
        'id': 'split_into_words',
        'title': 'Split Into Words',
        'topic': 'string · split',
        'task': "כתבו פונקציה בשם split_into_words\n"
                "פרמטר אחד, בשם sentence - מחרוזת\n"
                "היא מחזירה רשימה של כל המילים במשפט",
        'solution': "def split_into_words(sentence):\n"
                    "    return sentence.split()\n"
                    "\n"
                    "\n"
                    "print(split_into_words('hello there world'))\n",
    },
    {
        'id': 'replace_letter',
        'title': 'Swap A Letter',
        'topic': 'string · replace',
        'task': "כתבו פונקציה בשם replace_letter\n"
                "שלושה פרמטרים: word, old ו-new\n"
                "היא מחזירה את word אחרי שכל הופעה של old הוחלפה ב-new",
        'solution': "def replace_letter(word, old, new):\n"
                    "    return word.replace(old, new)\n"
                    "\n"
                    "\n"
                    "print(replace_letter('banana', 'a', 'o'))\n",
    },

    # ---------------------------------------------------------- fundamentals
    {
        'id': 'greet',
        'title': 'Say It Back',
        'topic': 'functions · strings · return',
        'task': "כתבו פונקציה בשם greet\n"
                "היא לא מקבלת אף פרמטר\n"
                "היא מחזירה בדיוק את הטקסט הזה: 'Hello World'",
        'solution': "def greet():\n"
                    "    return 'Hello World'\n"
                    "\n"
                    "\n"
                    "print(greet())\n",
    },
    {
        'id': 'shout_upper',
        'title': 'Shout It',
        'topic': 'functions · strings · methods',
        'task': "כתבו פונקציה בשם shout\n"
                "פרמטר אחד, בשם word\n"
                "היא מחזירה את המילה באותיות גדולות",
        'solution': "def shout(word):\n"
                    "    return word.upper()\n"
                    "\n"
                    "\n"
                    "print(shout('hello'))\n",
    },
    {
        'id': 'shout_lower',
        'title': 'Whisper It',
        'topic': 'functions · strings · methods',
        'task': "כתבו פונקציה בשם whisper\n"
                "פרמטר אחד, בשם word\n"
                "היא מחזירה את המילה באותיות קטנות",
        'solution': "def whisper(word):\n"
                    "    return word.lower()\n"
                    "\n"
                    "\n"
                    "print(whisper('HELLO'))\n",
    },
    {
        'id': 'shout_title',
        'title': 'Title It',
        'topic': 'functions · strings · methods',
        'task': "כתבו פונקציה בשם title_case\n"
                "פרמטר אחד, בשם words\n"
                "היא מחזירה את הטקסט כשכל מילה בו מתחילה באות גדולה",
        'solution': "def title_case(words):\n"
                    "    return words.title()\n"
                    "\n"
                    "\n"
                    "print(title_case('hello world'))\n",
    },
    {
        'id': 'full_name',
        'title': 'Put It Together',
        'topic': 'functions · strings · concatenation',
        'task': "כתבו פונקציה בשם full_name\n"
                "שני פרמטרים: first ו-last\n"
                "היא מחזירה אותם ביחד, כשם אחד, עם רווח אחד ביניהם",
        'solution': "def full_name(first, last):\n"
                    "    return first + ' ' + last\n"
                    "\n"
                    "\n"
                    "print(full_name('Ada', 'Lovelace'))\n",
    },
    {
        'id': 'string_length',
        'title': 'How Long Is It',
        'topic': 'string · len',
        'task': "כתבו פונקציה בשם string_length\n"
                "פרמטר אחד, בשם word\n"
                "היא מחזירה כמה אותיות יש במילה",
        'solution': "def string_length(word):\n"
                    "    return len(word)\n"
                    "\n"
                    "\n"
                    "print(string_length('hello'))\n",
    },
    {
        'id': 'first_letter',
        'title': 'The First Letter',
        'topic': 'string · indexing',
        'task': "כתבו פונקציה בשם first_letter\n"
                "פרמטר אחד, בשם word\n"
                "היא מחזירה את האות הראשונה במילה",
        'solution': "def first_letter(word):\n"
                    "    return word[0]\n"
                    "\n"
                    "\n"
                    "print(first_letter('banana'))\n",
    },
    {
        'id': 'last_three',
        'title': 'The Last Three Letters',
        'topic': 'string · slicing',
        'task': "כתבו פונקציה בשם last_three\n"
                "פרמטר אחד, בשם word\n"
                "היא מחזירה את שלוש האותיות האחרונות במילה",
        'solution': "def last_three(word):\n"
                    "    return word[-3:]\n"
                    "\n"
                    "\n"
                    "print(last_three('banana'))\n",
    },
    {
        'id': 'count_substring',
        'title': 'Count The Occurrences',
        'topic': 'string · count',
        'task': "כתבו פונקציה בשם count_substring\n"
                "שני פרמטרים: word ו-sub\n"
                "היא מחזירה כמה פעמים sub מופיע בתוך word",
        'solution': "def count_substring(word, sub):\n"
                    "    return word.count(sub)\n"
                    "\n"
                    "\n"
                    "print(count_substring('banana', 'a'))\n",
    },
    {
        'id': 'starts_with',
        'title': 'Does It Start With',
        'topic': 'string · startswith',
        'task': "כתבו פונקציה בשם starts_with\n"
                "שני פרמטרים: word ו-prefix\n"
                "היא מחזירה True אם word מתחיל ב-prefix, אחרת False",
        'solution': "def starts_with(word, prefix):\n"
                    "    return word.startswith(prefix)\n"
                    "\n"
                    "\n"
                    "print(starts_with('banana', 'ban'))\n",
    },
    {
        'id': 'list_length',
        'title': 'How Many Items',
        'topic': 'list · len',
        'task': "כתבו פונקציה בשם list_length\n"
                "פרמטר אחד, בשם items - רשימה\n"
                "היא מחזירה כמה איברים יש ברשימה",
        'solution': "def list_length(items):\n"
                    "    return len(items)\n"
                    "\n"
                    "\n"
                    "print(list_length([1, 2, 3, 4]))\n",
    },
    {
        'id': 'first_item',
        'title': 'The First Item',
        'topic': 'list · indexing',
        'task': "כתבו פונקציה בשם first_item\n"
                "פרמטר אחד, בשם items - רשימה\n"
                "היא מחזירה את האיבר הראשון ברשימה",
        'solution': "def first_item(items):\n"
                    "    return items[0]\n"
                    "\n"
                    "\n"
                    "print(first_item([10, 20, 30]))\n",
    },
    {
        'id': 'last_item',
        'title': 'The Last Item',
        'topic': 'list · indexing',
        'task': "כתבו פונקציה בשם last_item\n"
                "פרמטר אחד, בשם items - רשימה\n"
                "היא מחזירה את האיבר האחרון ברשימה",
        'solution': "def last_item(items):\n"
                    "    return items[-1]\n"
                    "\n"
                    "\n"
                    "print(last_item([10, 20, 30]))\n",
    },
    {
        'id': 'list_sum',
        'title': 'Add Them All Up',
        'topic': 'list · sum',
        'task': "כתבו פונקציה בשם list_sum\n"
                "פרמטר אחד, בשם items - רשימה של מספרים\n"
                "היא מחזירה את הסכום של כל המספרים ברשימה",
        'solution': "def list_sum(items):\n"
                    "    return sum(items)\n"
                    "\n"
                    "\n"
                    "print(list_sum([1, 2, 3, 4]))\n",
    },
    {
        'id': 'list_max',
        'title': 'The Biggest One',
        'topic': 'list · max',
        'task': "כתבו פונקציה בשם list_max\n"
                "פרמטר אחד, בשם items - רשימה של מספרים\n"
                "היא מחזירה את המספר הגדול ביותר ברשימה",
        'solution': "def list_max(items):\n"
                    "    return max(items)\n"
                    "\n"
                    "\n"
                    "print(list_max([3, 9, 1]))\n",
    },
    {
        'id': 'list_min',
        'title': 'The Smallest One',
        'topic': 'list · min',
        'task': "כתבו פונקציה בשם list_min\n"
                "פרמטר אחד, בשם items - רשימה של מספרים\n"
                "היא מחזירה את המספר הקטן ביותר ברשימה",
        'solution': "def list_min(items):\n"
                    "    return min(items)\n"
                    "\n"
                    "\n"
                    "print(list_min([3, 9, 1]))\n",
    },
    {
        'id': 'combine_lists',
        'title': 'Combine Two Lists',
        'topic': 'list · concatenation',
        'task': "כתבו פונקציה בשם combine_lists\n"
                "שני פרמטרים: a ו-b - שתי רשימות\n"
                "היא מחזירה רשימה אחת, עם כל האיברים של a ואז כל האיברים של b",
        'solution': "def combine_lists(a, b):\n"
                    "    return a + b\n"
                    "\n"
                    "\n"
                    "print(combine_lists([1, 2], [3, 4]))\n",
    },
    {
        'id': 'is_in_list',
        'title': 'Is It There',
        'topic': 'list · in',
        'task': "כתבו פונקציה בשם is_in_list\n"
                "שני פרמטרים: items (רשימה) ו-value\n"
                "היא מחזירה True אם value נמצא ברשימה, אחרת False",
        'solution': "def is_in_list(items, value):\n"
                    "    return value in items\n"
                    "\n"
                    "\n"
                    "print(is_in_list([1, 2, 3], 2))\n",
    },
    {
        'id': 'absolute_value',
        'title': 'Always Positive',
        'topic': 'numbers · abs',
        'task': "כתבו פונקציה בשם absolute_value\n"
                "פרמטר אחד, בשם n\n"
                "היא מחזירה את הערך המוחלט של n - תמיד חיובי או אפס",
        'solution': "def absolute_value(n):\n"
                    "    return abs(n)\n"
                    "\n"
                    "\n"
                    "print(absolute_value(-7))\n",
    },
    {
        'id': 'round_number',
        'title': 'Round It',
        'topic': 'numbers · round',
        'task': "כתבו פונקציה בשם round_number\n"
                "שני פרמטרים: n ו-digits\n"
                "היא מחזירה את n מעוגל למספר הספרות digits אחרי הנקודה",
        'solution': "def round_number(n, digits):\n"
                    "    return round(n, digits)\n"
                    "\n"
                    "\n"
                    "print(round_number(3.14159, 2))\n",
    },
    {
        'id': 'in_range',
        'title': 'Inside The Range',
        'topic': 'if · and',
        'task': "כתבו פונקציה בשם in_range\n"
                "שלושה פרמטרים: n, low ו-high\n"
                "היא מחזירה True אם n נמצא בין low ל-high (כולל את שניהם), אחרת False\n"
                "השתמשו בתנאי אחד עם and, לא שני if נפרדים",
        'solution': "def in_range(n, low, high):\n"
                    "    return n >= low and n <= high\n"
                    "\n"
                    "\n"
                    "print(in_range(5, 1, 10))\n",
    },
    {
        'id': 'key_exists',
        'title': 'Is The Key There',
        'topic': 'dict · in',
        'task': "כתבו פונקציה בשם key_exists\n"
                "שני פרמטרים: d (מילון) ו-key\n"
                "היא מחזירה True אם key נמצא במילון, אחרת False",
        'solution': "def key_exists(d, key):\n"
                    "    return key in d\n"
                    "\n"
                    "\n"
                    "print(key_exists({'a': 1}, 'a'))\n",
    },
    {
        'id': 'item_in_set',
        'title': 'Is It In The Set',
        'topic': 'set · in',
        'task': "כתבו פונקציה בשם item_in_set\n"
                "שני פרמטרים: s (set) ו-item\n"
                "היא מחזירה True אם item נמצא בקבוצה, אחרת False",
        'solution': "def item_in_set(s, item):\n"
                    "    return item in s\n"
                    "\n"
                    "\n"
                    "print(item_in_set({1, 2, 3}, 2))\n",
    },
    {
        'id': 'make_point',
        'title': 'Make A Pair',
        'topic': 'tuple · creation',
        'task': "כתבו פונקציה בשם make_point\n"
                "שני פרמטרים: x ו-y\n"
                "היא מחזירה אותם כ-tuple אחד: (x, y)",
        'solution': "def make_point(x, y):\n"
                    "    return (x, y)\n"
                    "\n"
                    "\n"
                    "print(make_point(3, 4))\n",
    },
]
