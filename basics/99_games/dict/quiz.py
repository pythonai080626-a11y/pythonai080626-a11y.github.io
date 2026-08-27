# -*- coding: utf-8 -*-
"""
quiz.py  --  Lesson 16 dictionary quiz  (the STUDENT side)

    1. you type your name
    2. 20 questions, 4 options each, exactly one is right
    3. every answer is sent to the teacher's server the moment you press Enter
    4. the teacher sees your name and your progress bar live

Run it:      python quiz.py
The teacher will give you the ngrok address to paste when it asks.
"""

import json
import sys
import time
import urllib.error
import urllib.request

from questions import QUESTIONS

# the teacher can hard-code the ngrok link here so nobody has to type it
SERVER = 'http://localhost:8000'

TOTAL = len(QUESTIONS)
online = True                       # turns False if the server cannot be reached


# --------------------------------------------------------------- colours ---
# a dict of colours, of course
C = {
    'reset': '\033[0m',   'bold': '\033[1m',   'dim': '\033[2m',
    'red': '\033[91m',    'green': '\033[92m', 'yellow': '\033[93m',
    'blue': '\033[94m',   'pink': '\033[95m',  'cyan': '\033[96m',
    'white': '\033[97m',  'grey': '\033[90m',
    'bg_green': '\033[42m\033[30m', 'bg_red': '\033[41m\033[97m',
    'bg_blue': '\033[44m\033[97m',  'bg_gold': '\033[43m\033[30m',
}

# one colour per option letter
LETTER_COLOR = {'a': C['cyan'], 'b': C['pink'], 'c': C['yellow'], 'd': C['green']}


def paint(text, *names):
    return ''.join(C[n] for n in names) + text + C['reset']


def setup_console():
    """Make Windows understand the colour codes and the emoji."""
    if sys.platform == 'win32':
        import os
        os.system('')                              # switches on ANSI on win10+
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


# ------------------------------------------------------------ animations ---
def type_out(text, delay=0.012, end='\n'):
    """Print letter by letter, like someone is typing it."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()


def spinner(text, seconds=0.8):
    frames = {0: '|', 1: '/', 2: '-', 3: '\\'}     # dict again
    steps = int(seconds / 0.08)
    for i in range(steps):
        sys.stdout.write('\r ' + C['cyan'] + frames[i % 4] + C['reset'] + ' ' + text)
        sys.stdout.flush()
        time.sleep(0.08)
    sys.stdout.write('\r' + ' ' * (len(text) + 6) + '\r')
    sys.stdout.flush()


def bar(score, answered):
    """A little progress bar right in the terminal."""
    width = 28
    filled = int(width * answered / TOTAL)
    good = int(width * score / TOTAL)
    line = paint('#' * good, 'green') + paint('#' * (filled - good), 'red') \
        + paint('.' * (width - filled), 'grey')
    return '[' + line + '] ' + paint('%d/%d' % (score, TOTAL), 'bold', 'white')


def banner():
    art = {
        1: "+--------------------------------------------------+",
        2: "|        D I C T I O N A R Y   Q U I Z              |",
        3: "|        lesson 16  *  key : value  *  20 Q         |",
        4: "+--------------------------------------------------+",
    }
    print()
    for n in sorted(art):
        print(paint(art[n], 'bold', 'cyan'))
        time.sleep(0.09)
    print()


def confetti():
    rows = {0: '  *   .    *      .   *    .     *   .  ',
            1: '    .    *    .      *    .    *     .  ',
            2: ' *    .     *    .      *     .   *     '}
    colors = {0: 'yellow', 1: 'pink', 2: 'cyan'}
    for r in range(6):
        print(paint(rows[r % 3], colors[r % 3]))
        time.sleep(0.09)


# --------------------------------------------------------------- network ---
def post(path, payload):
    """Send one dict to the server. Never crashes the quiz."""
    global online
    url = SERVER.rstrip('/') + path
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST', headers={
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'true',   # skip the free-ngrok warning page
    })
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            answer = json.loads(resp.read().decode('utf-8'))
        online = True
        return answer
    except Exception as e:
        if online:
            print(paint('  (the server did not answer: %s - your score is still '
                        'counted here)' % e, 'grey'))
        online = False
        return {'ok': False}


# ------------------------------------------------------------------ quiz ---
def ask_name():
    print(paint('  First things first.', 'dim'))
    name = ''
    while not name:
        name = input(paint('  What is your name? ', 'bold', 'yellow')).strip()
        if not name:
            print(paint('  A name, please - the teacher needs to find you on '
                        'the board.', 'red'))
    return name[:24]


def ask_server():
    global SERVER
    typed = input(paint('  Server address [', 'dim') + paint(SERVER, 'cyan')
                  + paint('] (Enter = keep): ', 'dim')).strip()
    if typed:
        if not typed.startswith('http'):
            typed = 'https://' + typed
        SERVER = typed


def show_question(number, item):
    print()
    print(paint(' Question %d of %d ' % (number, TOTAL), 'bg_blue', 'bold'))
    print()
    for line in item['q'].split('\n'):
        print('   ' + paint(line, 'white', 'bold'))
    print()
    for letter in sorted(item['options']):                 # a, b, c, d
        colour = LETTER_COLOR[letter]
        print('   ' + colour + C['bold'] + letter + ')' + C['reset']
              + ' ' + item['options'][letter])
        time.sleep(0.05)
    print()


def read_choice(item):
    while True:
        pick = input(paint('   your answer (a/b/c/d): ', 'bold', 'cyan')).strip().lower()
        if pick in item['options']:
            return pick
        print(paint('   Only a, b, c or d - try again.', 'red'))


def main():
    setup_console()
    banner()

    name = ask_name()
    ask_server()

    spinner('signing you in...', 0.9)
    post('/api/start', {'name': name})

    print()
    type_out(paint('  Hello %s! ' % name, 'bold', 'green')
             + paint('20 questions about dictionaries. Good luck.', 'white'), 0.012)
    print(paint('  Wrong answers are not the end of the world - you will be told why.',
                'dim'))
    time.sleep(0.6)

    score = 0
    answered = 0
    missed = {}                                   # question number -> your pick

    for number in sorted(QUESTIONS):              # 1, 2, 3 ... 20
        item = QUESTIONS[number]
        show_question(number, item)
        pick = read_choice(item)

        answered = answered + 1
        right = (pick == item['correct'])
        if right:
            score = score + 1
            print()
            print('   ' + paint('  CORRECT!  ', 'bg_green', 'bold') + ' '
                  + paint('+1 point', 'green', 'bold'))
        else:
            missed[number] = pick
            good = item['correct']
            print()
            print('   ' + paint('  NOT THIS TIME  ', 'bg_red', 'bold'))
            print('   ' + paint('you chose  ', 'grey') + paint(pick + ') '
                  + item['options'][pick], 'red'))
            print('   ' + paint('right one  ', 'grey') + paint(good + ') '
                  + item['options'][good], 'green', 'bold'))
            print('   ' + paint('why: ' + item['why'], 'yellow'))

        # ---- send this single answer to the teacher's server --------------
        post('/api/answer', {'name': name, 'question': number,
                             'chosen': pick, 'correct': right})

        print('   ' + bar(score, answered))
        time.sleep(0.35)

    # ------------------------------------------------------------- ending --
    post('/api/finish', {'name': name})

    print()
    spinner('adding up your points...', 1.0)
    print(paint('=' * 54, 'cyan'))
    type_out('  ' + paint(' FINAL SCORE ', 'bg_gold', 'bold') + '  '
             + paint('%s: %d out of %d' % (name, score, TOTAL), 'bold', 'white'), 0.015)
    print('  ' + bar(score, TOTAL))

    grade = round(score * 100 / TOTAL)
    verdicts = {                                   # a dict, one last time
        'gold': 'Dictionary master. Nothing left to teach you.',
        'good': 'Solid. A key or two slipped away, that is all.',
        'ok':   'You know the idea - go over .get() and the views again.',
        'redo': 'Open 16-lesson.html once more and run the examples yourself.',
    }
    if grade >= 90:
        band = 'gold'
    elif grade >= 70:
        band = 'good'
    elif grade >= 50:
        band = 'ok'
    else:
        band = 'redo'

    print('  ' + paint('%d%%' % grade, 'bold', 'green') + '  '
          + paint(verdicts[band], 'white'))

    if missed:
        print()
        print(paint('  questions to look at again:', 'yellow', 'bold'))
        for number in sorted(missed):
            print('   ' + paint('Q%-3d' % number, 'grey')
                  + paint('you said %s' % missed[number], 'red')
                  + paint('   right answer: %s' % QUESTIONS[number]['correct'], 'green'))
    else:
        confetti()
        print(paint('  A perfect 20/20 - not one key missing.', 'bold', 'green'))

    print(paint('=' * 54, 'cyan'))
    if not online:
        print(paint('  (the server was offline, so the teacher did not get '
                    'your last answers)', 'red'))
    print(paint('  Your name and score are on the teacher screen.', 'dim'))
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + paint('  quiz stopped. bye!', 'yellow'))
