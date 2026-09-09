# -*- coding: utf-8 -*-
"""
server.py  --  Lesson 20 TRY / EXCEPT QUIZ.  One server, two pages.

Standard library only (no flask, nothing to install).

    python server.py                 -> http://localhost:8000
    ngrok http 8000                  -> give the https://....ngrok-free.app link
                                        to the class; that one link is all they need

Pages
    GET  /            the STUDENT page   - type a name, answer 20 questions,
                                           watch the class leaderboard fill up
    GET  /teacher     the TEACHER panel  - every player, the question they are on
                                           right now, the full answer key, and the
                                           buttons to fix a question or a player

Endpoints
    GET  /api/state       everybody's progress (both pages poll this)
    GET  /api/answers     teacher only - the key: right letter, why, and the
                          extra typed answers that have been blessed
    POST /api/join        {"name":..., "pet":...}
    POST /api/open        {"name":..., "q":n}        starts that student's 80s
    POST /api/answer      {"name":..., "q":n, "chosen":"b" | null}
    POST /api/override    {"name":..., "q":n}        teacher: count it as right
    POST /api/accept      {"q":n, "text":...}         (typed questions only - this
                          quiz has none, so it always answers 'use FIX instead')
    POST /api/restart     {"name":...}               one player starts over
    POST /api/reset       wipe the board

WHY THE ANSWERS ARE NOT IN THE PAGE
    /api/join hands out the questions with the 'correct' letter REMOVED. Every
    answer is judged here, on the server. Opening devtools shows a student
    nothing they could not already see on their screen.
"""

import ast
import json
import os
import re
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from questions import QUESTIONS

HERE = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(HERE, 'scores.json')
PORT = int(os.environ.get('PORT', 8000))

TOTAL = len(QUESTIONS)

# how long a student gets on each question. One number, change it here.
SECONDS = int(os.environ.get('SECONDS', 80))

# a small grace window, because the answer has to travel over the network
GRACE = 2.5

STUDENTS = {}          # name -> that student's dict
ACCEPTED = {}          # question number (as str) -> extra typed answers the teacher blessed
LOCK = threading.Lock()

PETS = ['fox', 'panda', 'owl', 'octopus', 'unicorn', 'turtle', 'lion', 'bee',
        'trex', 'whale', 'butterfly', 'penguin', 'koala', 'dolphin', 'horse',
        'parrot', 'frog', 'crab', 'shark', 'tiger']


def now():
    return datetime.now().strftime('%H:%M:%S')


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
        print('[server] loaded %d players from scores.json' % len(STUDENTS), flush=True)
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
        'pet': PETS[abs(hash(name)) % len(PETS)],
        'score': 0,
        'q': 1,                # the question they are looking at right now
        'answers': {},         # '1' -> what they picked / typed
        'right': {},           # '1' -> True / False
        'seconds': {},         # '1' -> how long that one took
        'opened': {},          # '1' -> unix time they first saw it
        'done': False,
        'started': now(),
        'last': now(),
    }


def student_for(name):
    """Called with LOCK held."""
    student = STUDENTS.get(name)
    if student is None:
        student = blank_student(name)
        STUDENTS[name] = student
    return student


def clean_name(data):
    name = (data.get('name') or 'anonymous').strip()[:20]
    return name or 'anonymous'


def clean_q(data):
    try:
        q = int(data.get('q'))
    except Exception:
        q = 1
    return q if q in QUESTIONS else 1


# ------------------------------------------------------------- the judging --
def read_value(text):
    """Turn what a student typed into a real python value.

    Accepts every honest spelling of the same answer:
        (7,)   7,   ( 7 , )   tuple([7])
    Returns (value, True) when it could be read, (None, False) when it could not.
    """
    text = (text or '').strip()
    if not text:
        return None, False
    try:
        return ast.literal_eval(text), True
    except Exception:
        pass
    squashed = text.replace(' ', '')
    if squashed.startswith('tuple(') and squashed.endswith(')'):
        try:
            return tuple(ast.literal_eval(text[text.index('(') + 1:text.rindex(')')])), True
        except Exception:
            return None, False
    return None, False


TYPE_NAME = {'tuple': tuple, 'list': list, 'set': set, 'dict': dict, 'str': str}


def judge_typed(q, text):
    """Did they type the right VALUE? Returns (right, one line for them)."""
    item = QUESTIONS[q]

    # anything the teacher has blessed for this question counts, as typed
    for blessed in ACCEPTED.get(str(q), []):
        if ''.join(str(text).split()) == ''.join(str(blessed).split()):
            return True, 'the teacher accepted this one too'

    value, ok = read_value(text)
    if not ok:
        return False, 'that is not something python can read as a value'
    wanted = TYPE_NAME.get(item.get('want_type'))
    if wanted is not None and not isinstance(value, wanted):
        got = type(value).__name__
        article = 'an' if got[0] in 'aeiou' else 'a'
        return False, 'you typed %s %s, not a %s' % (article, got, item['want_type'])
    if value != item['answer']:
        return False, 'python reads that as %r' % (value,)
    return True, 'python reads that as %r' % (value,)


def judge(q, chosen):
    """One answer in, (right, message) out. The only place this is decided."""
    item = QUESTIONS[q]
    if item.get('kind') == 'type':
        return judge_typed(q, chosen)
    return (chosen == item['correct']), ''


def right_answer_text(q):
    """What the student is shown afterwards, right or wrong."""
    item = QUESTIONS[q]
    if item.get('kind') == 'type':
        return item['expect']
    return '%s)  %s' % (item['correct'], item['options'][item['correct']])


# ------------------------------------------------------------------- logic --
def public_question(q):
    """What a student is allowed to see. The right letter stays home."""
    item = QUESTIONS[q]
    out = {
        'q': q,
        'kind': item.get('kind', 'choice'),
        'text': item['q'],
    }
    if item.get('kind') == 'type':
        out['placeholder'] = 'type python, e.g.  (1, 2, 3)'
    else:
        out['options'] = dict(item['options'])
    return out


def do_join(data):
    name = clean_name(data)
    pet = (data.get('pet') or '').strip()
    with LOCK:
        student = student_for(name)
        if pet in PETS:
            student['pet'] = pet
        student['last'] = now()
        save()
        snapshot = dict(student)
    print('[join  ] %s' % name, flush=True)
    return {'ok': True, 'student': snapshot, 'total': TOTAL, 'seconds': SECONDS,
            'questions': [public_question(n) for n in sorted(QUESTIONS)]}


def do_open(data):
    """Their 80 seconds on this question start the first time they see it."""
    name, q = clean_name(data), clean_q(data)
    with LOCK:
        student = student_for(name)
        student['q'] = q
        student['last'] = now()
        if str(q) not in student['opened']:
            student['opened'][str(q)] = time.time()
        left = SECONDS - (time.time() - student['opened'][str(q)])
        answered = str(q) in student['right']
        save()
    return {'ok': True, 'q': q, 'left': max(0, round(left, 1)),
            'answered': answered}


def do_answer(data):
    """One answer. chosen = a letter, the typed text, or null when time ran out."""
    name, q = clean_name(data), clean_q(data)
    chosen = data.get('chosen')
    with LOCK:
        student = student_for(name)
        if str(q) in student['right']:                 # already answered, ignore
            return {'ok': True, 'already': True,
                    'right': student['right'][str(q)],
                    'answer': right_answer_text(q), 'why': QUESTIONS[q]['why']}

        opened = student['opened'].get(str(q))
        if opened is None:
            opened = time.time()
            student['opened'][str(q)] = opened
        spent = time.time() - opened
        late = spent > SECONDS + GRACE

        if chosen is None or late:
            right, message = False, ''
            if late:
                message = 'the %d seconds were up' % SECONDS
        else:
            right, message = judge(q, chosen)

        student['answers'][str(q)] = '' if chosen is None else str(chosen)[:120]
        student['right'][str(q)] = bool(right)
        student['seconds'][str(q)] = round(min(spent, SECONDS), 1)
        student['last'] = now()
        if right:
            student['score'] = student['score'] + 1
        if len(student['right']) >= TOTAL:
            student['done'] = True
        score, done = student['score'], student['done']
        save()

    print('[answer] %-14s q%-3d %-3s %r' % (name, q, 'OK' if right else 'X', chosen),
          flush=True)
    return {'ok': True, 'right': bool(right), 'message': message,
            'answer': right_answer_text(q), 'why': QUESTIONS[q]['why'],
            'score': score, 'done': done, 'timeout': chosen is None or late}


# ------------------------------------------------------------ teacher side --
def do_override(data):
    """Teacher: 'that one was fine, give it to them.' One player, one question."""
    name, q = clean_name(data), clean_q(data)
    with LOCK:
        student = STUDENTS.get(name)
        if student is None:
            return {'ok': False, 'error': 'no such player'}
        was = student['right'].get(str(q))
        if was is True:
            return {'ok': True, 'already': True, 'score': student['score']}
        student['right'][str(q)] = True
        student['score'] = student['score'] + 1
        student['last'] = now()
        if len(student['right']) >= TOTAL:
            student['done'] = True
        score = student['score']
        save()
    print('[fix   ] %s given q%d  -> %d/%d' % (name, q, score, TOTAL), flush=True)
    return {'ok': True, 'score': score}


def do_accept(data):
    """Teacher: 'this typed answer is fine too.' Valid for everybody, right now."""
    q = clean_q(data)
    text = (data.get('text') or '').strip()
    if not text:
        return {'ok': False, 'error': 'type the answer you want to accept'}
    if QUESTIONS[q].get('kind') != 'type':
        return {'ok': False, 'error': 'question %d is multiple choice - use FIX '
                                      'on the player instead' % q}
    with LOCK:
        ACCEPTED.setdefault(str(q), [])
        squashed = [''.join(a.split()) for a in ACCEPTED[str(q)]]
        if ''.join(text.split()) not in squashed:
            ACCEPTED[str(q)].append(text)
        blessed = list(ACCEPTED[str(q)])
        save()
    print('[accept] q%d also accepts %r' % (q, text), flush=True)
    return {'ok': True, 'q': q, 'accepted': blessed}


def do_restart(data):
    """One player starts their own game over. Nobody else is touched."""
    name = clean_name(data)
    with LOCK:
        old = STUDENTS.get(name) or {}
        fresh = blank_student(name)
        if old.get('pet'):
            fresh['pet'] = old['pet']
        STUDENTS[name] = fresh
        save()
        snapshot = dict(fresh)
    print('[restrt] %s started over' % name, flush=True)
    return {'ok': True, 'student': snapshot, 'total': TOTAL, 'seconds': SECONDS,
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
        return {'total': TOTAL, 'seconds': SECONDS,
                'students': json.loads(json.dumps(STUDENTS)),
                'accepted': json.loads(json.dumps(ACCEPTED))}


def do_answers():
    """Teacher only - every question with its right answer and its why."""
    with LOCK:
        blessed = json.loads(json.dumps(ACCEPTED))
    out = []
    for n in sorted(QUESTIONS):
        item = QUESTIONS[n]
        row = {'q': n, 'kind': item.get('kind', 'choice'), 'text': item['q'],
               'why': item['why'], 'accepted': blessed.get(str(n), [])}
        if item.get('kind') == 'type':
            row['expect'] = item['expect']
            row['answer'] = repr(item['answer'])
        else:
            row['options'] = dict(item['options'])
            row['correct'] = item['correct']
        out.append(row)
    return {'ok': True, 'total': TOTAL, 'seconds': SECONDS, 'questions': out}


ROUTES = {                                    # path -> function. A dict, of course.
    '/api/join': do_join,
    '/api/open': do_open,
    '/api/answer': do_answer,
    '/api/override': do_override,
    '/api/accept': do_accept,
    '/api/restart': do_restart,
    '/api/reset': do_reset,
}


# ------------------------------------------------------------------ server --
class Handler(BaseHTTPRequestHandler):
    server_version = 'TryExceptQuiz/1.0'

    def log_message(self, *args):                 # keep the console readable
        pass

    # -- helpers ----------------------------------------------------------
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

    # -- verbs ------------------------------------------------------------
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
            return self.send_json({'ok': True, 'players': len(STUDENTS)})
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
    print('  TRY / EXCEPT QUIZ  --  lesson 20  --  %d questions, %d seconds each'
          % (TOTAL, SECONDS), flush=True)
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
