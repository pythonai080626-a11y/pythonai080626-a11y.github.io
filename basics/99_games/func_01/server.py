# -*- coding: utf-8 -*-
"""
server.py  --  the FUNCTION LAB server (lesson 18, 10 challenges).

Standard library only - no flask, nothing to install.

    python server.py                 -> http://localhost:8000
    ngrok http 8000                  -> hand the https://....ngrok-free.app link
                                        to the students, they open it in a browser

Pages
    GET  /                the STUDENT lab
    GET  /teacher         the TEACHER panel

Endpoints
    GET  /api/state                        the whole board (both pages poll this)
    GET  /api/answers                      the answer key - teacher page only
    POST /api/join       {name}            sign in / come back
    POST /api/open       {name, q}         student opened a challenge - clock starts
    POST /api/hint       {name, q}         spend the hint, halve the points
    POST /api/giveup     {name, q}         'I do not know' - show the answer, 0 points
    POST /api/restart    {name}            that one player wipes their own game
    POST /api/run        {name, q, code}   run it, judge it, score it
    POST /api/accept     {q, code}         teacher blesses an extra valid answer
    POST /api/test       {q, code}         teacher tries code without scoring anybody
    POST /api/reset                        wipe the board for the next group

HOW A CHALLENGE IS JUDGED
    Their file has to RUN, and then their function has to answer correctly when
    WE call it - see runner.py. The body is none of our business: any shape that
    hands back the right values from the right slots passes.
    'require' only ever asks for the thing being taught (def, return, a name= at
    the call), and 'forbid' only stops the answer being typed out by hand.

    When the checker is wrong anyway, the teacher panel has ACCEPT IT ANYWAY.
    An accepted answer skips every check, for everybody, from that second on.

THE SCORING
                      within 90s      after 90s
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

FAST_SECONDS = 90          # the 100-point window. Writing a function takes longer
                           # than a one-liner, so it is wider than the dict game's
RUN_TIMEOUT = 6            # a loop that never ends dies after this
MAX_CODE = 3000            # characters

try:
    from questions import QUESTIONS
except Exception as e:
    print('[server] cannot read questions.py:', e, flush=True)
    QUESTIONS = {}

TOTAL = len(QUESTIONS)

# name -> that student's dict.  ONE dict holds the whole class.
STUDENTS = {}
# question number (as str) -> answers the teacher accepted mid-game
ACCEPTED = {}
LOCK = threading.Lock()

# things that have no business in a lesson-18 exercise
BANNED = ('import', '__', 'open(', 'exec(', 'eval(', 'compile(',
          'input(', 'exit(', 'quit(', 'globals(', 'locals(')

EMOJI = ['fox', 'panda', 'owl', 'octopus', 'unicorn', 'turtle', 'lion', 'bee',
         'trex', 'whale', 'butterfly', 'penguin', 'koala', 'dolphin', 'horse',
         'parrot', 'frog', 'crab', 'shark', 'tiger']


def now():
    return datetime.now().strftime('%H:%M:%S')


def squash(text):
    """Drop every space/tab/newline, so spacing never decides anything."""
    return ''.join(str(text).split())


def atoms(text):
    """The words and numbers that came out, ignoring how they were dressed up.

    Used only for the 'call' challenges, where what matters is that the right
    numbers reached the screen - not whether they used one print or two.
    """
    return sorted(w.lower() for w in
                  re.findall(r'[A-Za-z_]\w*|-?\d+\.?\d*', str(text)))


# ----------------------------------------------------------------- storage --
def load():
    global STUDENTS, ACCEPTED
    if not os.path.exists(SAVE_FILE):
        return
    try:
        with open(SAVE_FILE, encoding='utf-8') as f:
            saved = json.load(f)
        STUDENTS = saved.get('students', {})
        ACCEPTED = saved.get('accepted', {})
        print('[server] loaded %d students from scores.json' % len(STUDENTS), flush=True)
    except Exception as e:
        print('[server] could not read scores.json:', e, flush=True)


def save():
    """Called with LOCK already held."""
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump({'students': STUDENTS, 'accepted': ACCEPTED},
                      f, ensure_ascii=False, indent=2)
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
    """LOCK must be held. Upsert - the .get / if-None pattern from lesson 16."""
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
def run_python(setup, code, tests):
    """Run their file in a fresh python, then interview the function.

    Returns the dict runner.py printed:
        {'stdout':..., 'value':..., 'error':..., 'tests':[{call,want,got,ok,error}]}
    """
    payload = json.dumps({'setup': setup, 'code': code, 'tests': tests})
    try:
        proc = subprocess.run(
            [sys.executable, '-I', RUNNER],
            input=payload, capture_output=True, text=True,
            encoding='utf-8', errors='replace',
            timeout=RUN_TIMEOUT, cwd=HERE,
        )
    except subprocess.TimeoutExpired:
        return {'stdout': '', 'value': '', 'tests': [],
                'error': 'still running after %d seconds - is there a loop that never ends?'
                         % RUN_TIMEOUT}
    except Exception as e:
        return {'stdout': '', 'value': '', 'tests': [],
                'error': 'could not run python: %s' % e}
    try:
        return json.loads(proc.stdout or '{}')
    except Exception:
        err = [ln for ln in (proc.stderr or '').strip().split('\n') if ln.strip()]
        return {'stdout': '', 'value': '', 'tests': [],
                'error': err[-1] if err else 'your code crashed'}


def shown(result):
    """What appeared when their file ran, for the 'what came out' panel."""
    parts = []
    if (result.get('stdout') or '').strip():
        parts.append(result['stdout'].rstrip())
    if result.get('value'):
        parts.append(result['value'])
    return '\n'.join(parts)


def judge(q, code):
    """Return (passed, output, reason, tests). Does not touch anybody's score.

    The rule: the file has to run, and then the function has to answer us
    correctly. HOW the body is written is not checked and never will be.
    """
    question = QUESTIONS[q]
    flat = squash(code).lower()

    if not code.strip():
        return False, '', 'there is nothing in the editor yet', []
    if len(code) > MAX_CODE:
        return False, '', 'that is a lot of code for this one - keep it under %d characters' % MAX_CODE, []
    for bad in BANNED:
        if squash(bad).lower() in flat:
            return False, '', '"%s" is switched off here - this one only needs def, a slot and return' % bad, []

    # the teacher said this answer was fine. It skips everything else.
    blessed = [squash(a) for a in ACCEPTED.get(str(q), [])]
    if squash(code) in blessed:
        return True, '', 'accepted by the teacher', []

    result = run_python(question['setup'], code, question.get('tests') or [])
    out = shown(result)

    if result.get('error'):
        return False, out, result['error'], []

    # ---- the 'call' challenges: did the right values reach the screen? ----
    wanted_print = question.get('prints') or ''
    if wanted_print:
        if atoms(result.get('stdout', '')) != atoms(wanted_print):
            if not out.strip():
                return False, out, ('nothing came out - the function has to be CALLED, '
                                    'and the answer printed'), []
            return False, out, 'that is not what should be on the screen yet', []

    # ---- the write / fix challenges: we call the function ourselves ----
    rows = result.get('tests') or []
    bad = [r for r in rows if not r.get('ok')]
    if bad:
        first = bad[0]
        if first.get('error'):
            reason = 'we called  %s  and it did not survive:\n%s' % (first['call'], first['error'])
        elif first.get('got') == 'None':
            reason = ('we called  %s  and got None back.\n'
                      'Something printed it, or nobody returned it.' % first['call'])
        else:
            reason = 'we called  %s  and got  %s  back. It should be  %s' % (
                first['call'], first['got'], first['want'])
        return False, out, reason, rows

    # ---- right answers. Now: did they go through the thing being taught? ----
    for needed in question.get('require', []):
        if isinstance(needed, (list, tuple)):          # two honest roads
            if not any(squash(one).lower() in flat for one in needed):
                return False, out, ('right answer, wrong road - this one needs  %s'
                                    % '  or  '.join(needed)), rows
        elif squash(needed).lower() not in flat:
            return False, out, 'right answer, wrong road - this one has to go through  %s' % needed, rows
    for banned in question.get('forbid', []):
        if squash(banned).lower() in flat:
            return False, out, ('no typing the answer by hand - "%s" has to be worked out, '
                                'not written down' % banned), rows
    return True, out, '', rows


def points_for(elapsed, used_hint):
    fast = elapsed <= FAST_SECONDS
    if used_hint:
        return 50 if fast else 25
    return 100 if fast else 50


# ------------------------------------------------------------------- logic --
def public_question(q):
    """What a student is allowed to see. The hint, the answer and the test calls
    with their expected values stay home until they run something."""
    question = QUESTIONS[q]
    return {
        'q': q,
        'title': question['title'],
        'kind': question.get('kind', 'write'),
        'setup': question.get('setup', ''),
        'task': question['task'],
        'starter': question.get('starter', ''),
        'expect': question.get('expect', ''),
        'checks': [t['call'] for t in (question.get('tests') or [])],
        'prints': question.get('prints', ''),
    }


def do_join(data):
    name = clean_name(data)
    with LOCK:
        student = student_for(name)
        student['last'] = now()
        save()
        snapshot = dict(student)
    print('[join  ] %s' % name, flush=True)
    return {'ok': True, 'student': snapshot,
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
    passed, output, reason, rows = judge(q, code)

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

    print('[run   ] %-14s q%-3d %s  %s  score %d'
          % (name, q, 'PASS' if passed else 'fail',
             ('+%d' % gained) if gained else '   ', snapshot['score']), flush=True)

    return {'ok': True, 'passed': passed, 'output': output, 'reason': reason,
            'tests': rows, 'expect': QUESTIONS[q].get('expect', ''),
            'gained': gained, 'already': already, 'seconds': round(elapsed, 1),
            'used_hint': used_hint, 'score': snapshot['score'],
            'solved': sorted(int(n) for n in snapshot['solved'])}


def do_giveup(data):
    """I DO NOT KNOW. Show them the answer, bank a zero, let them move on."""
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


def do_accept(data):
    """Teacher: 'that answer was fine too.' Valid for everybody, right now."""
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
    print('[accept] q%d also accepts an answer of %d lines'
          % (q, len(code.split('\n'))), flush=True)
    return {'ok': True, 'q': q, 'accepted': blessed}


def do_test(data):
    """Teacher tries a student's claim. Nobody's score moves."""
    q = clean_q(data)
    passed, output, reason, rows = judge(q, data.get('code') or '')
    return {'ok': True, 'passed': passed, 'output': output, 'reason': reason,
            'tests': rows, 'expect': QUESTIONS[q].get('expect', ''),
            'solution': QUESTIONS[q]['solution']}


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
    with LOCK:
        STUDENTS.clear()
        ACCEPTED.clear()
        save()
    print('[reset ] board cleared', flush=True)
    return {'ok': True}


def do_state():
    with LOCK:
        return {'total': TOTAL, 'fast': FAST_SECONDS,
                'students': json.loads(json.dumps(STUDENTS)),
                'accepted': json.loads(json.dumps(ACCEPTED))}


def do_answers():
    """Teacher only - the key, the hints, the traps and what each one teaches."""
    return {'ok': True, 'fast': FAST_SECONDS, 'questions': [{
        'q': n,
        'title': QUESTIONS[n]['title'],
        'kind': QUESTIONS[n].get('kind', 'write'),
        'teaches': QUESTIONS[n].get('teaches', ''),
        'setup': QUESTIONS[n].get('setup', ''),
        'task': QUESTIONS[n]['task'],
        'expect': QUESTIONS[n].get('expect', ''),
        'checks': ['%s  ->  %s' % (t['call'], t['is'])
                   for t in (QUESTIONS[n].get('tests') or [])],
        'prints': QUESTIONS[n].get('prints', ''),
        'hint': QUESTIONS[n]['hint'],
        'solution': QUESTIONS[n]['solution'],
        'trap': QUESTIONS[n]['trap'],
    } for n in sorted(QUESTIONS)]}


ROUTES = {                                    # path -> function. A dict, of course.
    '/api/join': do_join,
    '/api/open': do_open,
    '/api/hint': do_hint,
    '/api/run': do_run,
    '/api/giveup': do_giveup,
    '/api/restart': do_restart,
    '/api/accept': do_accept,
    '/api/test': do_test,
    '/api/reset': do_reset,
}


# ------------------------------------------------------------------ server --
class Handler(BaseHTTPRequestHandler):
    server_version = 'FunctionLab/1.0'

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
    print('  FUNCTION LAB  --  lesson 18  (%d challenges)' % TOTAL, flush=True)
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
