# -*- coding: utf-8 -*-
"""
server.py  --  the teacher's scoreboard server for the Lesson 16 dict quiz.

Standard library only (no flask, nothing to install).

    python server.py                 -> http://localhost:8000
    ngrok http 8000                  -> give the https://....ngrok-free.app link
                                        to the students, they paste it into quiz.py

Pages / endpoints
    GET  /              the teacher console (a name + a progress bar per student)
    GET  /api/scores    JSON of everybody
    POST /api/start     {"name": ...}                          student signed in
    POST /api/answer    {"name":..., "question":n, "correct":true/false, ...}
    POST /api/finish    {"name": ...}                          student done
    POST /api/reset     wipe the board (teacher only)

Everything is kept in ONE dict - the same type the lesson is about:
    STUDENTS = { 'Yarden': {'score': 4, 'answered': 6, ...}, ... }
"""

import json
import os
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(HERE, 'scores.json')
PORT = int(os.environ.get('PORT', 8000))

try:
    from questions import QUESTIONS
    TOTAL = len(QUESTIONS)
except Exception:                                  # server can run on its own
    TOTAL = 20

# name -> that student's dict
STUDENTS = {}
LOCK = threading.Lock()


# ----------------------------------------------------------------- storage --
def load():
    """Read the board back from disk so a restart does not lose the class."""
    global STUDENTS
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, encoding='utf-8') as f:
                STUDENTS = json.load(f)
            print('[server] loaded %d students from scores.json' % len(STUDENTS), flush=True)
        except Exception as e:
            print('[server] could not read scores.json:', e, flush=True)


def save():
    """Called with LOCK already held."""
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(STUDENTS, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print('[server] could not write scores.json:', e, flush=True)


def blank_student(name):
    return {
        'name': name,
        'score': 0,
        'answered': 0,
        'total': TOTAL,
        'wrong': {},                 # question number -> what they picked
        'done': False,
        'started': now(),
        'last': now(),
    }


def now():
    return datetime.now().strftime('%H:%M:%S')


# ------------------------------------------------------------------- logic --
def do_start(data):
    name = (data.get('name') or 'anonymous').strip()[:24] or 'anonymous'
    with LOCK:
        STUDENTS[name] = blank_student(name)     # upsert - a re-run starts over
        save()
    print('[start ] %s signed in' % name, flush=True)
    return {'ok': True, 'name': name, 'total': TOTAL}


def do_answer(data):
    name = (data.get('name') or 'anonymous').strip()[:24] or 'anonymous'
    correct = bool(data.get('correct'))
    qnum = data.get('question')
    chosen = data.get('chosen')
    with LOCK:
        student = STUDENTS.get(name)              # .get - may not exist yet
        if student is None:
            student = blank_student(name)
            STUDENTS[name] = student
        student['answered'] = student['answered'] + 1
        student['last'] = now()
        if correct:
            student['score'] = student['score'] + 1
        else:
            student['wrong'][str(qnum)] = chosen  # upsert into a nested dict
        save()
        snapshot = dict(student)
    print('[answer] %-14s q%-3s %s   score %d/%d'
          % (name, qnum, 'OK ' if correct else 'X  ', snapshot['score'], TOTAL),
          flush=True)
    return {'ok': True, 'score': snapshot['score'],
            'answered': snapshot['answered'], 'total': TOTAL}


def do_finish(data):
    name = (data.get('name') or 'anonymous').strip()[:24] or 'anonymous'
    with LOCK:
        student = STUDENTS.get(name)
        if student is not None:
            student['done'] = True
            student['last'] = now()
            save()
            score = student['score']
        else:
            score = 0
    print('[finish] %s finished with %d/%d' % (name, score, TOTAL), flush=True)
    return {'ok': True, 'score': score, 'total': TOTAL}


def do_reset(_data):
    with LOCK:
        STUDENTS.clear()
        save()
    print('[reset ] board cleared', flush=True)
    return {'ok': True}


def do_scores():
    with LOCK:
        return {'total': TOTAL, 'students': json.loads(json.dumps(STUDENTS))}


ROUTES = {                                        # path -> function. A dict!
    '/api/start': do_start,
    '/api/answer': do_answer,
    '/api/finish': do_finish,
    '/api/reset': do_reset,
}


# ------------------------------------------------------------------ server --
class Handler(BaseHTTPRequestHandler):
    server_version = 'DictQuiz/1.0'

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
        if path in ('/', '/teacher', '/index.html'):
            return self.page('teacher.html')
        if path == '/api/scores':
            return self.send_json(do_scores())
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
    print('=' * 58, flush=True)
    print('  DICT QUIZ SERVER  --  lesson 16', flush=True)
    print('  teacher console :  http://localhost:%d/' % PORT, flush=True)
    print('  students point quiz.py at this address', flush=True)
    print('  ngrok           :  ngrok http %d' % PORT, flush=True)
    print('  Ctrl+C to stop', flush=True)
    print('=' * 58, flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n[server] bye', flush=True)
        httpd.server_close()


if __name__ == '__main__':
    main()
