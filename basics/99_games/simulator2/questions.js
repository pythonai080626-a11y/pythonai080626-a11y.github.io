const QUESTIONS = [
  {
    "title": "The Price List",
    "setup": "prices = {'mango': 14, 'apple': 31, 'kiwi': 7}",
    "task": "Get the PRICES out on their own.\nThe values, without the names.",
    "answer": "14, 31, 7",
    "shows": "the three prices, without the fruit names",
    "lines": 1,
    "shape": "one line",
    "require": [
      ".values()"
    ],
    "forbid": [
      "14,31,7"
    ],
    "hint": "prices.values()\nThat is the whole answer.\nNo print needed, no list needed.",
    "solution": "prices.values()",
    "trap": "prices on its own gives you the whole thing, names and all. You only want half of it.",
    "q": 1
  },
  {
    "title": "The Name Tags",
    "setup": "pets = {'Rex': 'dog', 'Momo': 'cat', 'Kiwi': 'parrot'}",
    "task": "Now the other half.\nGet the NAMES out, without the animals.",
    "answer": "Rex, Momo, Kiwi",
    "shows": "the three names, without the animals",
    "lines": 1,
    "shape": "one line",
    "require": [
      ".keys()"
    ],
    "forbid": [
      "'Rex'"
    ],
    "hint": "pets.keys()\nThe mirror image of .values().",
    "solution": "pets.keys()",
    "trap": "A dict hands you the keys by default, so list(pets) works too - but .keys() is the one that says out loud what you meant.",
    "q": 2
  },
  {
    "title": "How Many",
    "setup": "grades = {'Noa': 91, 'Omer': 78, 'Yarden': 84, 'Adi': 66}",
    "task": "How many students are in there?",
    "answer": "4",
    "shows": "one number - how many pairs",
    "lines": 1,
    "shape": "one line",
    "require": [
      "len("
    ],
    "forbid": [
      "4"
    ],
    "hint": "len(grades)\nIt counts the PAIRS.",
    "solution": "len(grades)",
    "trap": "len counts the pairs, not the marks. It has no idea what is inside them.",
    "q": 3
  },
  {
    "title": "Look It Up",
    "setup": "capitals = {'France': 'Paris', 'Japan': 'Tokyo', 'Peru': 'Lima'}",
    "task": "Get the capital of Japan.",
    "answer": "Tokyo",
    "shows": "one city",
    "lines": 1,
    "shape": "one line",
    "require": [
      "Japan"
    ],
    "forbid": [
      "Tokyo"
    ],
    "hint": "capitals['Japan']\nSquare brackets.\nThe KEY goes inside them.",
    "solution": "capitals['Japan']",
    "trap": "capitals['japan'] with a small j is a different key entirely - KeyError. Keys are case sensitive.",
    "q": 4
  },
  {
    "title": "The Missing Colour",
    "setup": "pet = {'kind': 'parrot', 'age': 6}",
    "task": "There is no colour in there.\nAsk for it anyway.\nYou should get the word unknown back, not a crash.",
    "answer": "unknown",
    "shows": "the word unknown, and no error",
    "lines": 1,
    "shape": "one line",
    "require": [
      ".get("
    ],
    "forbid": [],
    "hint": "pet.get('color', 'unknown')\nThe second thing you hand .get is what comes back\nwhen the key is not there.",
    "solution": "pet.get('color', 'unknown')",
    "trap": "pet['color'] raises KeyError and stops everything. .get never crashes - that is the entire reason it exists.",
    "q": 5
  },
  {
    "title": "New Arrival",
    "setup": "zoo = {'lion': 2, 'zebra': 4}",
    "task": "A penguin arrived.\nPut penguin in with a 1.\nThen show the whole zoo.",
    "answer": "lion 2, zebra 4, penguin 1",
    "shows": "the zoo with the penguin in it",
    "lines": 2,
    "shape": "TWO lines.\nLine 1 puts the penguin in.\nLine 2 is just  zoo  on its own.",
    "require": [
      "penguin"
    ],
    "forbid": [
      "'lion':2",
      "'zebra':4"
    ],
    "hint": "zoo['penguin'] = 1\nA key that is not there yet gets created.\nThen  zoo  on the next line.",
    "solution": "zoo['penguin'] = 1\nzoo",
    "trap": "There is no .add() on a dict. You just assign to a key that does not exist yet and it appears.",
    "q": 6
  },
  {
    "title": "Price Change",
    "setup": "menu = {'pizza': 40, 'pasta': 38}",
    "task": "Pizza went up to 45.\nChange it.\nThen show the menu.",
    "answer": "pizza 45, pasta 38",
    "shows": "the menu with the new pizza price",
    "lines": 2,
    "shape": "TWO lines.\nLine 1 changes the price.\nLine 2 is just  menu  on its own.",
    "require": [
      "pizza",
      "45"
    ],
    "forbid": [
      "'pasta':38"
    ],
    "hint": "menu['pizza'] = 45\nThe same square brackets you used to read it.\nThen  menu  on the next line.",
    "solution": "menu['pizza'] = 45\nmenu",
    "trap": "menu['Pizza'] = 45 with a capital P does not change anything - it ADDS a second pair, and now you have two pizzas.",
    "q": 7
  },
  {
    "title": "The Stock Room",
    "setup": "stock = {'nails': 120, 'screws': 45, 'glue': 8}",
    "task": "Get the names AND the counts out together.\nBoth halves of every pair.",
    "answer": "nails 120, screws 45, glue 8",
    "shows": "every name next to its count",
    "lines": 1,
    "shape": "one line",
    "require": [
      ".items()"
    ],
    "forbid": [
      "nails:",
      "screws:",
      "glue:"
    ],
    "hint": "stock.items()\nIt hands you both halves of every pair at once.\nPrinting them in a loop is fine too, but not required.",
    "solution": "stock.items()",
    "trap": "for name in stock: only gives you the keys - you would have to go back for stock[name].",
    "q": 8
  },
  {
    "title": "Is Sushi On It?",
    "setup": "menu = {'pizza': 40, 'pasta': 38, 'salad': 22}",
    "task": "Is sushi on the menu?\nGet a True or a False out.",
    "answer": "False",
    "shows": "one word - True or False",
    "lines": 1,
    "shape": "one line",
    "require": [
      "in",
      "sushi"
    ],
    "forbid": [],
    "hint": "'sushi' in menu\nin looks through the KEYS.\nIt hands back True or False.",
    "solution": "'sushi' in menu",
    "trap": "in searches the keys, not the prices. 40 in menu is False, even though 40 is sitting right there as a value.",
    "q": 9
  },
  {
    "title": "Hidden In The Values",
    "setup": "bag = {'a': 'apple', 'b': 'bread', 'c': 'cheese'}",
    "task": "Is bread in there as a VALUE?\nGet a True or a False out.",
    "answer": "True",
    "shows": "one word - True or False",
    "lines": 1,
    "shape": "one line",
    "require": [
      ".values()",
      "bread"
    ],
    "forbid": [],
    "hint": "'bread' in bag.values()\nPoint in at the values and it looks there instead.",
    "solution": "'bread' in bag.values()",
    "trap": "'bread' in bag is False - plain in only ever searches the keys. This is the other half of challenge 9.",
    "q": 10
  },
  {
    "title": "The Whole Bill",
    "setup": "cart = {'milk': 6, 'bread': 9, 'eggs': 12}",
    "task": "What does the whole cart come to?",
    "answer": "27",
    "shows": "one number - everything added up",
    "lines": 1,
    "shape": "one line",
    "require": [
      "sum(",
      ".values()"
    ],
    "forbid": [
      "27"
    ],
    "hint": "sum(cart.values())\nsum needs numbers.\nSo hand it the values.",
    "solution": "sum(cart.values())",
    "trap": "sum(cart) tries to add the NAMES together and crashes - you cannot add 'milk' to 'bread'.",
    "q": 11
  },
  {
    "title": "The Cheapest Number",
    "setup": "tickets = {'balcony': 60, 'stalls': 120, 'standing': 35}",
    "task": "What is the smallest price?\nJust the number.",
    "answer": "35",
    "shows": "one number - the lowest price",
    "lines": 1,
    "shape": "one line",
    "require": [
      "min(",
      ".values()"
    ],
    "forbid": [
      "35"
    ],
    "hint": "min(tickets.values())\nThe values are the prices.\nSo that is what min has to look at.",
    "solution": "min(tickets.values())",
    "trap": "min(tickets) gives 'balcony' - the smallest NAME, alphabetically. Remember this one, it comes back at the end.",
    "q": 12
  },
  {
    "title": "The Cancelled Guest",
    "setup": "party = {'Noa': 'cake', 'Omer': 'chips', 'Yarden': 'juice'}",
    "task": "Omer cancelled.\nRemove him from the dict - del or pop, either is fine.\nThen show who is left.",
    "answer": "Noa cake, Yarden juice",
    "shows": "the party without Omer",
    "lines": 2,
    "shape": "TWO lines.\nLine 1 takes Omer out.\nLine 2 is just  party  on its own.\nTaking him out does not show you the dict by itself.",
    "require": [
      [
        "pop(",
        "del "
      ]
    ],
    "forbid": [
      "'Noa':"
    ],
    "hint": "del party['Omer']  takes him out.\nparty.pop('Omer')  does the same job.\nThen put  party  on the last line.",
    "solution": "del party['Omer']\nparty",
    "trap": "Both roads are fine here. del just removes it. pop removes it AND hands you back 'chips' - what was taken out, not what is left. We only want to see who is left, so del says it more plainly. Either way, the dict is the thing you have to look at on the next line.",
    "q": 13
  },
  {
    "title": "Last One Out",
    "setup": "queue = {'first': 1, 'second': 2, 'third': 3}",
    "task": "Take out the LAST pair that went in.\nDo it without naming it.\nThen show what came out.",
    "answer": "third 3",
    "shows": "the pair that was removed",
    "lines": 1,
    "shape": "one line",
    "require": [
      "popitem("
    ],
    "forbid": [
      "third"
    ],
    "hint": "queue.popitem()\nIt takes no key at all.\nIt removes the last pair and hands that pair back.",
    "solution": "queue.popitem()",
    "trap": "pop needs a key, popitem refuses one. popitem is the only way to take something out when you do not know what is in there.",
    "q": 14
  },
  {
    "title": "Two Baskets",
    "setup": "basket = {'apple': 2}\nextra = {'pear': 5, 'plum': 9}",
    "task": "Put everything into one dict.\nThen show it.",
    "answer": "apple 2, pear 5, plum 9",
    "shows": "all three fruits together in one dict",
    "lines": 2,
    "shape": "ONE line if you use  |\nTWO lines if you use .update()\nThen  basket  on its own on line 2.",
    "require": [
      [
        ".update(",
        "|"
      ]
    ],
    "forbid": [],
    "hint": "basket | extra  does it in one go.\nOr  basket.update(extra)\nand then  basket  on the next line.",
    "solution": "basket | extra",
    "trap": "basket.update(extra) hands back None - it changes basket where it stands. Look at basket afterwards, not at what update gave you.",
    "q": 15
  },
  {
    "title": "The Best Number",
    "setup": "points = {'red': 45, 'blue': 88, 'green': 61}",
    "task": "What is the highest score?\nJust the number, not the name.",
    "answer": "88",
    "shows": "one number - the biggest score",
    "lines": 1,
    "shape": "one line",
    "require": [
      "max(",
      ".values()"
    ],
    "forbid": [
      "88"
    ],
    "hint": "max(points.values())\nThe same idea as challenge 12, the other way up.",
    "solution": "max(points.values())",
    "trap": "max(points) gives 'red' - the last NAME alphabetically. And this one gives you the NUMBER. Getting the NAME of the best one needs one more thing - that is challenge 20, and it is the whole point of the lesson.",
    "q": 16
  },
  {
    "title": "A To Z",
    "setup": "fruit = {'pear': 3, 'apple': 9, 'mango': 5}",
    "task": "Get the names out in alphabetical order.",
    "answer": "apple, mango, pear",
    "shows": "the three names, sorted",
    "lines": 1,
    "shape": "one line",
    "require": [
      "sorted("
    ],
    "forbid": [
      "'apple','mango'"
    ],
    "hint": "sorted(fruit)\nHanding a dict to sorted sorts its KEYS.",
    "solution": "sorted(fruit)",
    "trap": "sorted(fruit) sorts the names, not the prices. Sorting by price needs one more thing - that is the next challenge.",
    "q": 17
  },
  {
    "title": "Cheapest First",
    "setup": "snacks = {'chips': 12, 'nuts': 30, 'gum': 4}",
    "task": "Get the names out ordered by PRICE.\nCheapest first.",
    "answer": "gum, chips, nuts",
    "shows": "the names in price order",
    "lines": 1,
    "shape": "one line",
    "require": [
      "sorted(",
      "key="
    ],
    "forbid": [],
    "hint": "sorted(snacks, key=snacks.get)\nkey= tells sorted what to compare each name BY.\nHere, its price.",
    "solution": "sorted(snacks, key=snacks.get)",
    "trap": "sorted(snacks) gives chips, gum, nuts - alphabetical. The key= is the entire difference, and it is the same key= you need in the last challenge.",
    "q": 18
  },
  {
    "title": "Deep Inside",
    "setup": "school = {'noa': {'age': 14, 'grade': 92},\n          'omer': {'age': 15, 'grade': 78}}",
    "task": "Get Omer's grade.",
    "answer": "78",
    "shows": "one number",
    "lines": 1,
    "shape": "one line",
    "require": [
      "omer",
      "grade"
    ],
    "forbid": [
      "78"
    ],
    "hint": "school['omer']['grade']\nThe first bracket gets you Omer's dict.\nThe second reaches inside it.",
    "solution": "school['omer']['grade']",
    "trap": "school['omer'] hands you the whole inner dict. One set of brackets gets you to the door, the second gets you through it.",
    "q": 19
  },
  {
    "title": "Who Won?",
    "setup": "scores = {'Yarden': 71, 'Omer': 93, 'Noa': 88}",
    "task": "Get the NAME of whoever scored the highest.",
    "answer": "Omer",
    "shows": "one name - the winner",
    "lines": 1,
    "shape": "one line",
    "require": [
      "max(",
      "key="
    ],
    "forbid": [
      "Omer",
      "93"
    ],
    "hint": "max(scores, key=scores.get)\nkey= tells max what to compare.\nSo it weighs the scores instead of the names.",
    "solution": "max(scores, key=scores.get)",
    "trap": "max(scores) gives Yarden. With no key= it compared the NAMES alphabetically and Y wins. This is the whole point of the lesson.",
    "q": 20
  }
];