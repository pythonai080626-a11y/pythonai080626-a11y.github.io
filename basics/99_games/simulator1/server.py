# -*- coding: utf-8 -*-
"""
server.py  --  the Dict Race arcade server (lesson 17 warm-up, first 20 minutes).

Standard library only - no flask, nothing to install.

    python server.py                 -> http://localhost:8000
    ngrok http 8000                  -> hand the https://....ngrok-free.app link
                                        to the students, they open it in a browser

Pages
    GET  /                the STUDENT arcade
    GET  /teacher         the TEACHER panel

Endpoints
    GET  /api/state                        the whole board (both pages poll this)
    POST /api/join       {name}            sign in / come back
    POST /api/open       {name, q}         student opened a challenge - clock starts
    POST /api/hint       {name, q}         spend the hint, halve the points
    POST /api/giveup     {name, q}         'I do not know' - show the answer, 0 points
    POST /api/restart    {name}            that one player wipes their own game
    POST /api/run        {name, q, code}   run it, judge it, score it
    POST /api/spotlight  {q}               teacher moves the class to a challenge
    POST /api/accept     {q, code}         teacher blesses an extra valid answer
    POST /api/test       {q, code}         teacher tries code without scoring anybody
    POST /api/reset                        wipe the board for the next group

The scoring:
                      within 40s      after 40s
    no hint              100              50
    used the hint         50              25

The clock is kept HERE, not in the browser, so a refresh cannot buy more time.
"""

import json
import os
import re
import subprocess
import sys
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(HERE, 'scores.json')
RUNNER = os.path.join(HERE, 'runner.py')
PORT = int(os.environ.get('PORT', 8000))

FAST_SECONDS = 40          # the 100-point window
RUN_TIMEOUT = 5            # a student loop that never ends dies after this
MAX_CODE = 2000            # characters

try:
    from questions import QUESTIONS
except Exception as e:
    print('[server] cannot read questions.py:', e, flush=True)
    QUESTIONS = {}

TOTAL = len(QUESTIONS)

# name -> that student's dict.  ONE dict holds the whole class.
STUDENTS = {}
# question number (as str) -> list of extra answers the teacher accepted mid-game
ACCEPTED = {}
# which challenge the teacher wants everybody looking at
SPOTLIGHT = 1
LOCK = threading.Lock()

# things that have no business in a 3-line dict exercise
BANNED = ('import', '__', 'open(', 'exec(', 'eval(', 'compile(',
          'input(', 'exit(', 'quit(', 'globals(', 'locals(')

EMOJI = ['fox', 'panda', 'owl', 'octopus', 'unicorn', 'turtle', 'lion', 'bee',
         'trex', 'whale', 'butterfly', 'penguin', 'koala', 'dolphin', 'horse',
         'parrot', 'frog', 'crab', 'shark', 'tiger']


def now():
    return datetime.now().strftime('%H:%M:%S')


def squash(text):
    """Drop every space/tab/newline so ' [14 , 31] ' and '[14,31]' look the same."""
    return ''.join(str(text).split())


# the wrappers python puts around a view - they are not part of the answer
NOISE = re.compile(r'\b(dict_values|dict_keys|dict_items|odict_\w+|'
                   r'KeysView|ValuesView|ItemsView)\b')


def atoms(text):
    """The words and numbers that came out, ignoring how they were dressed up.

    This is what lets us stop caring about print() and list() and quotes:

        dict_values([14, 31, 7])   ->  ['14', '31', '7']
        [14, 31, 7]                ->  ['14', '31', '7']
        14, 31, 7                  ->  ['14', '31', '7']

    Sorted at the end, so the order the values come out in never costs a point.
    """
    clean = NOISE.sub(' ', str(text))
    return sorted(w.lower() for w in re.findall(r'[A-Za-z_]\w*|\d+\.?\d*', clean))


# ----------------------------------------------------------------- storage --
def load():
    global STUDENTS, ACCEPTED, SPOTLIGHT
    if not os.path.exists(SAVE_FILE):
        return
    try:
        with open(SAVE_FILE, encoding='utf-8') as f:
            saved = json.load(f)
        STUDENTS = saved.get('students', {})
        ACCEPTED = saved.get('accepted', {})
        SPOTLIGHT = saved.get('spotlight', 1)
        print('[server] loaded %d students from scores.json' % len(STUDENTS), flush=True)
    except Exception as e:
        print('[server] could not read scores.json:', e, flush=True)


def save():
    """Called with LOCK already held."""
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump({'students': STUDENTS, 'accepted': ACCEPTED,
                       'spotlight': SPOTLIGHT}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print('[server] could not write scores.json:', e, flush=True)


def blank_student(name):
    return {
        'name': name,
        'score': 0,
        'solved': {},        # '1' -> points won there
        'hinted': {},        # '1' -> True
        'gaveup': {},        # '1' -> True, they asked to be shown the answer
        'opened': {},        # '1' -> unix time they first saw it
        'tries': 0,
        'q': 1,              # what they are looking at right now
        'joined': now(),
        'last': now(),
        'pet': EMOJI[len(STUDENTS) % len(EMOJI)],
    }


def student_for(name):
    """LOCK must be held. Upsert - the .get / if-None pattern from the lesson."""
    student = STUDENTS.get(name)
    if student is None:
        student = blank_student(name)
        STUDENTS[name] = student
    return student


def clean_name(data):
    return (data.get('name') or 'anonymous').strip()[:20] or 'anonymous'


def clean_q(data):
    try:
        q = int(data.get('q'))
    except Exception:
        q = 1
    return q if q in QUESTIONS else 1


# -------------------------------------------------------------- running it --
def run_python(setup, code):
    """Run it in a fresh python. Returns (stdout, last-value-repr, error).

    runner.py evaluates a trailing expression the way the console does, so a
    student who writes  prices.values()  with no print still produces an answer.
    """
    payload = json.dumps({'setup': setup, 'code': code})
    try:
        proc = subprocess.run(
            [sys.executable, '-I', RUNNER],
            input=payload, capture_output=True, text=True,
            encoding='utf-8', errors='replace',
            timeout=RUN_TIMEOUT, cwd=HERE,
        )
    except subprocess.TimeoutExpired:
        return '', '', 'still running after %d seconds - is there a loop that never ends?' % RUN_TIMEOUT
    except Exception as e:
        return '', '', 'could not run python: %s' % e
    try:
        out = json.loads(proc.stdout or '{}')
    except Exception:
        err = [ln for ln in (proc.stderr or '').strip().split('\n') if ln.strip()]
        return '', '', err[-1] if err else 'your code crashed'
    return out.get('stdout', ''), out.get('value', ''), out.get('error', '')


def shown(stdout, value):
    """What the student actually produced, for the 'you got' panel."""
    parts = []
    if stdout.strip():
        parts.append(stdout.rstrip())
    if value:
        parts.append(value)
    return '\n'.join(parts)


def judge(q, code):
    """Return (passed, output, reason). Does not touch anybody's score.

    The rule: the right VALUES have to come out, using the command this exercise
    is about. Whether they printed it, wrapped it in list(), or just left the
    expression sitting there is none of our business.
    """
    question = QUESTIONS[q]
    flat = squash(code).lower()

    if not code.strip():
        return False, '', 'there is nothing in the editor yet'
    if len(code) > MAX_CODE:
        return False, '', 'keep it under %d characters - this one is a one-liner' % MAX_CODE
    for bad in BANNED:
        if squash(bad).lower() in flat:
            return False, '', '"%s" is switched off here - this is solvable with the dict alone' % bad

    stdout, value, error = run_python(question['setup'], code)
    got = shown(stdout, value)
    if error:
        return False, got, error

    want = atoms(question['answer'])
    if atoms(stdout) != want and atoms(value) != want:
        if not got.strip():
            return False, got, ('nothing came out - leave the answer on the last line, '
                                'or put a print() around it')
        return False, got, 'those are not the right values yet'

    # Right values. Now: did they USE the dict, or type the answer out by hand?
    blessed = [squash(a) for a in ACCEPTED.get(str(q), [])]
    if squash(code) in blessed:
        return True, got, 'accepted by the teacher'

    for needed in question.get('require', []):
        if isinstance(needed, (list, tuple)):          # two honest roads, either will do
            if not any(squash(one).lower() in flat for one in needed):
                return False, got, ('right answer, wrong road - this one needs  %s'
                                    % '  or  '.join(needed))
        elif squash(needed).lower() not in flat:
            return False, got, 'right answer, wrong road - this one has to go through  %s' % needed
    for banned in question.get('forbid', []):
        if squash(banned).lower() in flat:
            return False, got, 'no typing the answer by hand - "%s" has to come out of the dict' % banned
    return True, got, ''


def points_for(elapsed, used_hint):
    fast = elapsed <= FAST_SECONDS
    if used_hint:
        return 50 if fast else 25
    return 100 if fast else 50


# ------------------------------------------------------------------- logic --
def public_question(q):
    """What a student is allowed to see. The hint and the answer stay home."""
    question = QUESTIONS[q]
    return {
        'q': q,
        'title': question['title'],
        'setup': question['setup'],
        'task': question['task'],
        'answer': question['answer'],
        'shows': question['shows'],
        'lines': question.get('lines', 1),
        'shape': question.get('shape', 'one line'),
    }


def do_join(data):
    name = clean_name(data)
    with LOCK:
        student = student_for(name)
        student['last'] = now()
        save()
        snapshot = dict(student)
        spot = SPOTLIGHT
    print('[join  ] %s' % name, flush=True)
    return {'ok': True, 'student': snapshot, 'spotlight': spot,
            'total': TOTAL, 'fast': FAST_SECONDS,
            'questions': [public_question(n) for n in sorted(QUESTIONS)]}


def do_open(data):
    """Their clock for this challenge starts the first time they see it."""
    name, q = clean_name(data), clean_q(data)
    with LOCK:
        student = student_for(name)
        student['q'] = q
        student['last'] = now()
        if str(q) not in student['opened']:
            student['opened'][str(q)] = time.time()
        left = FAST_SECONDS - (time.time() - student['opened'][str(q)])
        solved = str(q) in student['solved']
        hinted = bool(student['hinted'].get(str(q)))
        save()
    return {'ok': True, 'q': q, 'fast_left': max(0, round(left, 1)),
            'solved': solved, 'hinted': hinted}


def do_hint(data):
    name, q = clean_name(data), clean_q(data)
    with LOCK:
        student = student_for(name)
        student['hinted'][str(q)] = True
        student['last'] = now()
        save()
    print('[hint  ] %-14s q%d' % (name, q), flush=True)
    return {'ok': True, 'hint': QUESTIONS[q]['hint']}


def do_run(data):
    name, q = clean_name(data), clean_q(data)
    code = data.get('code') or ''
    passed, output, reason = judge(q, code)

    with LOCK:
        student = student_for(name)
        student['tries'] = student['tries'] + 1
        student['last'] = now()
        opened = student['opened'].setdefault(str(q), time.time())
        elapsed = time.time() - opened
        used_hint = bool(student['hinted'].get(str(q)))
        gained = 0
        already = str(q) in student['solved']
        if passed and not already:
            gained = points_for(elapsed, used_hint)
            student['solved'][str(q)] = gained
            student['score'] = student['score'] + gained
        save()
        snapshot = dict(student)

    print('[run   ] %-14s q%d %s  %s  score %d'
          % (name, q, 'PASS' if passed else 'fail',
             ('+%d' % gained) if gained else '   ', snapshot['score']), flush=True)

    return {'ok': True, 'passed': passed, 'output': output, 'reason': reason,
            'answer': QUESTIONS[q]['answer'], 'gained': gained,
            'already': already, 'seconds': round(elapsed, 1),
            'used_hint': used_hint, 'score': snapshot['score'],
            'solved': sorted(int(n) for n in snapshot['solved'])}


def do_giveup(data):
    """I DO NOT KNOW. Show them the answer, bank a zero, let them move on.

    The question counts as done - 'solved' gets a 0 - so the next one opens and
    nobody gets stuck on a wall for the rest of the warm-up.
    """
    name, q = clean_name(data), clean_q(data)
    with LOCK:
        student = student_for(name)
        student['last'] = now()
        student.setdefault('gaveup', {})
        already = str(q) in student['solved']
        if not already:
            student['solved'][str(q)] = 0
            student['gaveup'][str(q)] = True
        save()
        snapshot = dict(student)
    print('[giveup] %-14s q%d  answer shown, 0 points' % (name, q), flush=True)
    return {'ok': True, 'q': q, 'already': already,
            'solution': QUESTIONS[q]['solution'],
            'trap': QUESTIONS[q]['trap'],
            'score': snapshot['score'],
            'solved': sorted(int(n) for n in snapshot['solved'])}


def do_spotlight(data):
    global SPOTLIGHT
    q = clean_q(data)
    with LOCK:
        SPOTLIGHT = q
        save()
    print('[spot  ] class moved to q%d' % q, flush=True)
    return {'ok': True, 'spotlight': q}


def do_accept(data):
    """Teacher: 'that answer was fine too.' Adds it as a valid solution, live."""
    q = clean_q(data)
    code = (data.get('code') or '').strip()
    if not code:
        return {'ok': False, 'error': 'paste the answer you want to accept'}
    with LOCK:
        ACCEPTED.setdefault(str(q), [])
        if squash(code) not in [squash(a) for a in ACCEPTED[str(q)]]:
            ACCEPTED[str(q)].append(code)
        save()
        blessed = list(ACCEPTED[str(q)])
    print('[accept] q%d also accepts: %s' % (q, code.replace('\n', ' ; ')), flush=True)
    return {'ok': True, 'q': q, 'accepted': blessed}


def do_test(data):
    """Teacher tries a student's claim. Nobody's score moves."""
    q = clean_q(data)
    passed, output, reason = judge(q, data.get('code') or '')
    return {'ok': True, 'passed': passed, 'output': output, 'reason': reason,
            'answer': QUESTIONS[q]['answer'], 'solution': QUESTIONS[q]['solution']}


def do_restart(data):
    """One player starts their own game over. Nobody else is touched."""
    name = clean_name(data)
    with LOCK:
        old = STUDENTS.get(name) or {}
        fresh = blank_student(name)
        if old.get('pet'):
            fresh['pet'] = old['pet']          # keep the animal they know themselves by
        STUDENTS[name] = fresh
        save()
        snapshot = dict(fresh)
    print('[restrt] %s started over' % name, flush=True)
    return {'ok': True, 'student': snapshot, 'total': TOTAL, 'fast': FAST_SECONDS,
            'questions': [public_question(n) for n in sorted(QUESTIONS)]}


def do_reset(_data):
    global SPOTLIGHT
    with LOCK:
        STUDENTS.clear()
        ACCEPTED.clear()
        SPOTLIGHT = 1
        save()
    print('[reset ] board cleared', flush=True)
    return {'ok': True}


def do_state():
    with LOCK:
        return {'total': TOTAL, 'fast': FAST_SECONDS, 'spotlight': SPOTLIGHT,
                'students': json.loads(json.dumps(STUDENTS)),
                'accepted': json.loads(json.dumps(ACCEPTED))}


def do_answers():
    """Teacher only - the answer key, the hints and the traps to talk about."""
    return {'ok': True, 'fast': FAST_SECONDS, 'questions': [{
        'q': n, 'title': QUESTIONS[n]['title'], 'setup': QUESTIONS[n]['setup'],
        'task': QUESTIONS[n]['task'], 'answer': QUESTIONS[n]['answer'],
        'hint': QUESTIONS[n]['hint'], 'solution': QUESTIONS[n]['solution'],
        'trap': QUESTIONS[n]['trap'],
    } for n in sorted(QUESTIONS)]}


ROUTES = {                                    # path -> function. A dict, of course.
    '/api/join': do_join,
    '/api/open': do_open,
    '/api/hint': do_hint,
    '/api/run': do_run,
    '/api/giveup': do_giveup,
    '/api/restart': do_restart,
    '/api/spotlight': do_spotlight,
    '/api/accept': do_accept,
    '/api/test': do_test,
    '/api/reset': do_reset,
}


# ------------------------------------------------------------------ server --
class Handler(BaseHTTPRequestHandler):
    server_version = 'DictRace/1.0'

    def log_message(self, *args):
        pass

    def send(self, code, body, ctype='application/json; charset=utf-8'):
        if not isinstance(body, bytes):
            body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, obj, code=200):
        self.send(code, json.dumps(obj, ensure_ascii=False))

    def page(self, filename):
        path = os.path.join(HERE, filename)
        if not os.path.exists(path):
            return self.send(404, 'missing file: ' + filename, 'text/plain')
        with open(path, 'rb') as f:
            self.send(200, f.read(), 'text/html; charset=utf-8')

    def do_OPTIONS(self):
        self.send(204, b'')

    def do_GET(self):
        path = self.path.split('?')[0]
        if path in ('/', '/index.html', '/play'):
            return self.page('index.html')
        if path in ('/teacher', '/teacher.html'):
            return self.page('teacher.html')
        if path == '/api/state':
            return self.send_json(do_state())
        if path == '/api/answers':
            return self.send_json(do_answers())
        if path == '/health':
            return self.send_json({'ok': True, 'students': len(STUDENTS)})
        self.send(404, json.dumps({'ok': False, 'error': 'not found'}))

    def do_POST(self):
        path = self.path.split('?')[0]
        handler = ROUTES.get(path)                # .get, not [ ] - no crash
        if handler is None:
            return self.send_json({'ok': False, 'error': 'no such endpoint'}, 404)
        try:
            length = int(self.headers.get('Content-Length') or 0)
            raw = self.rfile.read(length) if length else b'{}'
            data = json.loads(raw.decode('utf-8') or '{}')
            if not isinstance(data, dict):
                raise ValueError('body must be a JSON object')
        except Exception as e:
            return self.send_json({'ok': False, 'error': 'bad json: %s' % e}, 400)
        try:
            self.send_json(handler(data))
        except Exception as e:
            self.send_json({'ok': False, 'error': str(e)}, 500)


def main():
    load()
    httpd = ThreadingHTTPServer(('0.0.0.0', PORT), Handler)
    print('=' * 60, flush=True)
    print('  DICT RACE  --  lesson 17 warm-up  (%d challenges)' % TOTAL, flush=True)
    print('  students        :  http://localhost:%d/' % PORT, flush=True)
    print('  your panel      :  http://localhost:%d/teacher' % PORT, flush=True)
    print('  open the class  :  ngrok http %d' % PORT, flush=True)
    print('  Ctrl+C to stop', flush=True)
    print('=' * 60, flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n[server] bye', flush=True)
        httpd.server_close()


if __name__ == '__main__':
    main()
