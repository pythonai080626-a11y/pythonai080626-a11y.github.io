# -*- coding: utf-8 -*-
"""
questions.py  --  the 20 challenges of the Dict Race (lesson 17 warm-up).

Everything here is a dict, the same type the lesson is about:
    QUESTIONS      -> dict   number -> challenge-dict

Each challenge-dict holds:
    'title'     short arcade name shown on the progress strip
    'setup'     the code that ALREADY exists - the student never types it
    'task'      what they have to get out of the dict
    'answer'    the values that have to come out, written any readable way.
                We only take the words and numbers out of this, so
                "14, 31, 7"  and  "[14, 31, 7]"  mean exactly the same thing here.
    'shows'     how to describe that answer in one phrase, for the UI
    'lines'     how many lines the answer takes. Anything above 1 gets a loud
                warning on the student's screen - beginners do not guess that a
                two-line answer is allowed, let alone which line has to be last
    'shape'     that warning in words: how many lines, and what the LAST line is
    'require'   what their code MUST contain - the command they came to learn.
                A plain string must appear. A LIST means "any one of these", for
                the exercises that have two honest roads:
                    'require': ['.items()']              -> must have .items()
                    'require': [['pop(', 'del ']]        -> pop( OR del
    'forbid'    substrings their code must NOT contain - stops someone typing the
                answer out by hand instead of getting it from the dict
    'hint'      shown by the HINT button, and it costs half the points
    'solution'  the teacher's answer key. Also what the I DO NOT KNOW button
                shows, for 0 points
    'trap'      the near-miss. Shown to the teacher, and to a student who gave up

WRITING THE TEXT
    'task', 'shape' and 'hint' are shown to students with every newline turned
    into a line break. So KEEP THE LINES SHORT and start a new line at every
    full stop or dash - one idea per line. Long unbroken sentences are the
    single easiest way to lose a beginner.

WHAT COUNTS AS RIGHT
    The student does NOT have to print, and does NOT have to cast to a list.
    Getting the right values out with the right command is the whole exercise.
    All four of these pass challenge 1:
        prices.values()
        list(prices.values())
        print(prices.values())
        print(list(prices.values()))
    Order does not matter either - we compare WHICH values came out, not their
    order. For the two ordering exercises (17 and 18) the order therefore cannot
    be checked from the output, and 'require' carries the whole weight instead:
    18 insists on key=, which is the thing being taught.

THE RAMP
     1-4   reading a dict         .values()  .keys()  len()  d['key']
     5-7   missing keys, changing .get()  adding a pair  changing a value
     8-10  both halves, and asking .items()  in (keys)  in .values()
    11-12  arithmetic over a dict  sum()  min()
    13-15  changing the shape      pop/del  popitem  update/|
    16     the number, not the name  max() over the values
    17-18  order                   sorted()  sorted(key=)
    19     nested dicts            d['a']['b']
    20     the lesson's punchline  max(d, key=d.get)

    12 -> 16 -> 20 is the thread that matters:
    smallest number, biggest number, and then the NAME of the biggest.
    Only the last one needs key=, and by then they should feel why.
"""

QUESTIONS = {
    # ------------------------------------------------ 1-4  reading a dict --
    1: {
        'title': 'The Price List',
        'setup': "prices = {'mango': 14, 'apple': 31, 'kiwi': 7}",
        'task': "Get the PRICES out on their own.\n"
                "The values, without the names.",
        'answer': "14, 31, 7",
        'shows': "the three prices, without the fruit names",
        'lines': 1,
        'shape': "one line",
        'require': ['.values()'],
        'forbid': ['14,31,7'],
        'hint': "prices.values()\n"
                "That is the whole answer.\n"
                "No print needed, no list needed.",
        'solution': "prices.values()",
        'trap': "prices on its own gives you the whole thing, names and all. You only want half of it.",
    },
    2: {
        'title': 'The Name Tags',
        'setup': "pets = {'Rex': 'dog', 'Momo': 'cat', 'Kiwi': 'parrot'}",
        'task': "Now the other half.\n"
                "Get the NAMES out, without the animals.",
        'answer': "Rex, Momo, Kiwi",
        'shows': "the three names, without the animals",
        'lines': 1,
        'shape': "one line",
        'require': ['.keys()'],
        'forbid': ["'Rex'"],
        'hint': "pets.keys()\n"
                "The mirror image of .values().",
        'solution': "pets.keys()",
        'trap': "A dict hands you the keys by default, so list(pets) works too - but .keys() "
                "is the one that says out loud what you meant.",
    },
    3: {
        'title': 'How Many',
        'setup': "grades = {'Noa': 91, 'Omer': 78, 'Yarden': 84, 'Adi': 66}",
        'task': "How many students are in there?",
        'answer': "4",
        'shows': "one number - how many pairs",
        'lines': 1,
        'shape': "one line",
        'require': ['len('],
        'forbid': ['4'],
        'hint': "len(grades)\n"
                "It counts the PAIRS.",
        'solution': "len(grades)",
        'trap': "len counts the pairs, not the marks. It has no idea what is inside them.",
    },
    4: {
        'title': 'Look It Up',
        'setup': "capitals = {'France': 'Paris', 'Japan': 'Tokyo', 'Peru': 'Lima'}",
        'task': "Get the capital of Japan.",
        'answer': "Tokyo",
        'shows': "one city",
        'lines': 1,
        'shape': "one line",
        'require': ['Japan'],
        'forbid': ['Tokyo'],
        'hint': "capitals['Japan']\n"
                "Square brackets.\n"
                "The KEY goes inside them.",
        'solution': "capitals['Japan']",
        'trap': "capitals['japan'] with a small j is a different key entirely - KeyError. "
                "Keys are case sensitive.",
    },

    # ------------------------------- 5-7  missing keys, adding, changing --
    5: {
        'title': 'The Missing Colour',
        'setup': "pet = {'kind': 'parrot', 'age': 6}",
        'task': "There is no colour in there.\n"
                "Ask for it anyway.\n"
                "You should get the word unknown back, not a crash.",
        'answer': "unknown",
        'shows': "the word unknown, and no error",
        'lines': 1,
        'shape': "one line",
        'require': ['.get('],
        'forbid': [],
        'hint': "pet.get('color', 'unknown')\n"
                "The second thing you hand .get is what comes back\n"
                "when the key is not there.",
        'solution': "pet.get('color', 'unknown')",
        'trap': "pet['color'] raises KeyError and stops everything. .get never crashes - "
                "that is the entire reason it exists.",
    },
    6: {
        'title': 'New Arrival',
        'setup': "zoo = {'lion': 2, 'zebra': 4}",
        'task': "A penguin arrived.\n"
                "Put penguin in with a 1.\n"
                "Then show the whole zoo.",
        'answer': "lion 2, zebra 4, penguin 1",
        'shows': "the zoo with the penguin in it",
        'lines': 2,
        'shape': "TWO lines.\n"
                 "Line 1 puts the penguin in.\n"
                 "Line 2 is just  zoo  on its own.",
        'require': ['penguin'],
        'forbid': ["'lion':2", "'zebra':4"],
        'hint': "zoo['penguin'] = 1\n"
                "A key that is not there yet gets created.\n"
                "Then  zoo  on the next line.",
        'solution': "zoo['penguin'] = 1\nzoo",
        'trap': "There is no .add() on a dict. You just assign to a key that does not exist yet "
                "and it appears.",
    },
    7: {
        'title': 'Price Change',
        'setup': "menu = {'pizza': 40, 'pasta': 38}",
        'task': "Pizza went up to 45.\n"
                "Change it.\n"
                "Then show the menu.",
        'answer': "pizza 45, pasta 38",
        'shows': "the menu with the new pizza price",
        'lines': 2,
        'shape': "TWO lines.\n"
                 "Line 1 changes the price.\n"
                 "Line 2 is just  menu  on its own.",
        'require': ['pizza', '45'],
        'forbid': ["'pasta':38"],
        'hint': "menu['pizza'] = 45\n"
                "The same square brackets you used to read it.\n"
                "Then  menu  on the next line.",
        'solution': "menu['pizza'] = 45\nmenu",
        'trap': "menu['Pizza'] = 45 with a capital P does not change anything - it ADDS a "
                "second pair, and now you have two pizzas.",
    },

    # ------------------------------------ 8-10  both halves, and asking --
    8: {
        'title': 'The Stock Room',
        'setup': "stock = {'nails': 120, 'screws': 45, 'glue': 8}",
        'task': "Get the names AND the counts out together.\n"
                "Both halves of every pair.",
        'answer': "nails 120, screws 45, glue 8",
        'shows': "every name next to its count",
        'lines': 1,
        'shape': "one line",
        'require': ['.items()'],
        'forbid': ['nails:', 'screws:', 'glue:'],
        'hint': "stock.items()\n"
                "It hands you both halves of every pair at once.\n"
                "Printing them in a loop is fine too, but not required.",
        'solution': "stock.items()",
        'trap': "for name in stock: only gives you the keys - you would have to go back for stock[name].",
    },
    9: {
        'title': 'Is Sushi On It?',
        'setup': "menu = {'pizza': 40, 'pasta': 38, 'salad': 22}",
        'task': "Is sushi on the menu?\n"
                "Get a True or a False out.",
        'answer': "False",
        'shows': "one word - True or False",
        'lines': 1,
        'shape': "one line",
        'require': ['in', 'sushi'],
        'forbid': [],
        'hint': "'sushi' in menu\n"
                "in looks through the KEYS.\n"
                "It hands back True or False.",
        'solution': "'sushi' in menu",
        'trap': "in searches the keys, not the prices. 40 in menu is False, even though "
                "40 is sitting right there as a value.",
    },
    10: {
        'title': 'Hidden In The Values',
        'setup': "bag = {'a': 'apple', 'b': 'bread', 'c': 'cheese'}",
        'task': "Is bread in there as a VALUE?\n"
                "Get a True or a False out.",
        'answer': "True",
        'shows': "one word - True or False",
        'lines': 1,
        'shape': "one line",
        'require': ['.values()', 'bread'],
        'forbid': [],
        'hint': "'bread' in bag.values()\n"
                "Point in at the values and it looks there instead.",
        'solution': "'bread' in bag.values()",
        'trap': "'bread' in bag is False - plain in only ever searches the keys. This is the "
                "other half of challenge 9.",
    },

    # ---------------------------------- 11-12  arithmetic over a dict --
    11: {
        'title': 'The Whole Bill',
        'setup': "cart = {'milk': 6, 'bread': 9, 'eggs': 12}",
        'task': "What does the whole cart come to?",
        'answer': "27",
        'shows': "one number - everything added up",
        'lines': 1,
        'shape': "one line",
        'require': ['sum(', '.values()'],
        'forbid': ['27'],
        'hint': "sum(cart.values())\n"
                "sum needs numbers.\n"
                "So hand it the values.",
        'solution': "sum(cart.values())",
        'trap': "sum(cart) tries to add the NAMES together and crashes - you cannot add "
                "'milk' to 'bread'.",
    },
    12: {
        'title': 'The Cheapest Number',
        'setup': "tickets = {'balcony': 60, 'stalls': 120, 'standing': 35}",
        'task': "What is the smallest price?\n"
                "Just the number.",
        'answer': "35",
        'shows': "one number - the lowest price",
        'lines': 1,
        'shape': "one line",
        'require': ['min(', '.values()'],
        'forbid': ['35'],
        'hint': "min(tickets.values())\n"
                "The values are the prices.\n"
                "So that is what min has to look at.",
        'solution': "min(tickets.values())",
        'trap': "min(tickets) gives 'balcony' - the smallest NAME, alphabetically. Remember "
                "this one, it comes back at the end.",
    },

    # ------------------------------------- 13-15  changing the shape --
    13: {
        'title': 'The Cancelled Guest',
        'setup': "party = {'Noa': 'cake', 'Omer': 'chips', 'Yarden': 'juice'}",
        'task': "Omer cancelled.\n"
                "Remove him from the dict - del or pop, either is fine.\n"
                "Then show who is left.",
        'answer': "Noa cake, Yarden juice",
        'shows': "the party without Omer",
        'lines': 2,
        'shape': "TWO lines.\n"
                 "Line 1 takes Omer out.\n"
                 "Line 2 is just  party  on its own.\n"
                 "Taking him out does not show you the dict by itself.",
        'require': [['pop(', 'del ']],
        'forbid': ["'Noa':"],
        'hint': "del party['Omer']  takes him out.\n"
                "party.pop('Omer')  does the same job.\n"
                "Then put  party  on the last line.",
        'solution': "del party['Omer']\nparty",
        'trap': "Both roads are fine here. del just removes it. pop removes it AND hands you "
                "back 'chips' - what was taken out, not what is left. We only want to see who "
                "is left, so del says it more plainly. Either way, the dict is the thing you "
                "have to look at on the next line.",
    },
    14: {
        'title': 'Last One Out',
        'setup': "queue = {'first': 1, 'second': 2, 'third': 3}",
        'task': "Take out the LAST pair that went in.\n"
                "Do it without naming it.\n"
                "Then show what came out.",
        'answer': "third 3",
        'shows': "the pair that was removed",
        'lines': 1,
        'shape': "one line",
        'require': ['popitem('],
        'forbid': ['third'],
        'hint': "queue.popitem()\n"
                "It takes no key at all.\n"
                "It removes the last pair and hands that pair back.",
        'solution': "queue.popitem()",
        'trap': "pop needs a key, popitem refuses one. popitem is the only way to take "
                "something out when you do not know what is in there.",
    },
    15: {
        'title': 'Two Baskets',
        'setup': "basket = {'apple': 2}\nextra = {'pear': 5, 'plum': 9}",
        'task': "Put everything into one dict.\n"
                "Then show it.",
        'answer': "apple 2, pear 5, plum 9",
        'shows': "all three fruits together in one dict",
        'lines': 2,
        'shape': "ONE line if you use  |\n"
                 "TWO lines if you use .update()\n"
                 "Then  basket  on its own on line 2.",
        'require': [['.update(', '|']],
        'forbid': [],
        'hint': "basket | extra  does it in one go.\n"
                "Or  basket.update(extra)\n"
                "and then  basket  on the next line.",
        'solution': "basket | extra",
        'trap': "basket.update(extra) hands back None - it changes basket where it stands. "
                "Look at basket afterwards, not at what update gave you.",
    },

    # ------------------------- 16  the number, not the name (sets up 20) --
    16: {
        'title': 'The Best Number',
        'setup': "points = {'red': 45, 'blue': 88, 'green': 61}",
        'task': "What is the highest score?\n"
                "Just the number, not the name.",
        'answer': "88",
        'shows': "one number - the biggest score",
        'lines': 1,
        'shape': "one line",
        'require': ['max(', '.values()'],
        'forbid': ['88'],
        'hint': "max(points.values())\n"
                "The same idea as challenge 12, the other way up.",
        'solution': "max(points.values())",
        'trap': "max(points) gives 'red' - the last NAME alphabetically. And this one gives you "
                "the NUMBER. Getting the NAME of the best one needs one more thing - that is "
                "challenge 20, and it is the whole point of the lesson.",
    },

    # -------------------------------------------------- 17-18  order --
    17: {
        'title': 'A To Z',
        'setup': "fruit = {'pear': 3, 'apple': 9, 'mango': 5}",
        'task': "Get the names out in alphabetical order.",
        'answer': "apple, mango, pear",
        'shows': "the three names, sorted",
        'lines': 1,
        'shape': "one line",
        'require': ['sorted('],
        'forbid': ["'apple','mango'"],
        'hint': "sorted(fruit)\n"
                "Handing a dict to sorted sorts its KEYS.",
        'solution': "sorted(fruit)",
        'trap': "sorted(fruit) sorts the names, not the prices. Sorting by price needs "
                "one more thing - that is the next challenge.",
    },
    18: {
        'title': 'Cheapest First',
        'setup': "snacks = {'chips': 12, 'nuts': 30, 'gum': 4}",
        'task': "Get the names out ordered by PRICE.\n"
                "Cheapest first.",
        'answer': "gum, chips, nuts",
        'shows': "the names in price order",
        'lines': 1,
        'shape': "one line",
        'require': ['sorted(', 'key='],
        'forbid': [],
        'hint': "sorted(snacks, key=snacks.get)\n"
                "key= tells sorted what to compare each name BY.\n"
                "Here, its price.",
        'solution': "sorted(snacks, key=snacks.get)",
        'trap': "sorted(snacks) gives chips, gum, nuts - alphabetical. The key= is the entire "
                "difference, and it is the same key= you need in the last challenge.",
    },

    # --------------------------------------- 19  dicts inside dicts --
    19: {
        'title': 'Deep Inside',
        'setup': "school = {'noa': {'age': 14, 'grade': 92},\n"
                 "          'omer': {'age': 15, 'grade': 78}}",
        'task': "Get Omer's grade.",
        'answer': "78",
        'shows': "one number",
        'lines': 1,
        'shape': "one line",
        'require': ['omer', 'grade'],
        'forbid': ['78'],
        'hint': "school['omer']['grade']\n"
                "The first bracket gets you Omer's dict.\n"
                "The second reaches inside it.",
        'solution': "school['omer']['grade']",
        'trap': "school['omer'] hands you the whole inner dict. One set of brackets gets you "
                "to the door, the second gets you through it.",
    },

    # ------------------------------------------------ 20  the payoff --
    20: {
        'title': 'Who Won?',
        'setup': "scores = {'Yarden': 71, 'Omer': 93, 'Noa': 88}",
        'task': "Get the NAME of whoever scored the highest.",
        'answer': "Omer",
        'shows': "one name - the winner",
        'lines': 1,
        'shape': "one line",
        'require': ['max(', 'key='],
        'forbid': ['Omer', '93'],
        'hint': "max(scores, key=scores.get)\n"
                "key= tells max what to compare.\n"
                "So it weighs the scores instead of the names.",
        'solution': "max(scores, key=scores.get)",
        'trap': "max(scores) gives Yarden. With no key= it compared the NAMES alphabetically "
                "and Y wins. This is the whole point of the lesson.",
    },
}
