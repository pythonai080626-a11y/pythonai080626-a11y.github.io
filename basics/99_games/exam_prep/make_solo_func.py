# -*- coding: utf-8 -*-
"""
make_solo_func.py  --  turn func_01/questions.py into a STANDALONE solo.html.

func_01 (Function Lab) is not a multiple-choice quiz - the student writes and
RUNS real Python, and the checker calls their function to see what comes back.
That needs a real Python interpreter, which the browser does not have on its
own. So this page loads Pyodide (CPython compiled to WebAssembly) from a CDN -
the same approach 99_games/simulator2 already uses for the Dict Race game -
and ports the exact judging logic from server.py + runner.py into Python that
runs inside the page.

    python make_solo_func.py

Re-run it whenever func_01/questions.py changes, or solo.html will drift.
"""

import importlib.util
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'func_01', 'questions.py')
OUT = os.path.join(HERE, 'func_01', 'solo.html')


def load_questions():
    spec = importlib.util.spec_from_file_location('func01_questions', SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.QUESTIONS


def build():
    Q = load_questions()
    payload = []
    for n in sorted(Q):
        item = Q[n]
        payload.append({
            'q': n,
            'title': item['title'],
            'kind': item.get('kind', 'write'),
            'setup': item.get('setup', ''),
            'task': item['task'],
            'starter': item.get('starter', ''),
            'expect': item.get('expect', ''),
            'tests': item.get('tests') or [],
            'prints': item.get('prints', ''),
            'require': item.get('require') or [],
            'forbid': item.get('forbid') or [],
            'hint': item['hint'],
            'solution': item['solution'],
            'trap': item['trap'],
        })

    page = TEMPLATE % {
        'total': len(payload),
        'questions': json.dumps(payload, ensure_ascii=False, indent=1),
        'runner_py': json.dumps(RUNNER_PY),
    }
    io.open(OUT, 'w', encoding='utf-8', newline='\r\n').write(page)
    print('func_01      -> %s  (%d challenges, %d bytes)'
          % (os.path.relpath(OUT, HERE), len(payload), len(page)))


# The RUNNER_PY string below is a near-verbatim port of func_01/runner.py's
# run_file() + interview(), and func_01/server.py's judge(). It runs INSIDE
# the page via Pyodide - the same file the student's attempt runs in.
RUNNER_PY = r"""
import ast, contextlib, io, json

MAX_CODE = 3000
BANNED = ('import', '__', 'open(', 'exec(', 'eval(', 'compile(',
          'input(', 'exit(', 'quit(', 'globals(', 'locals(',
          'while')   # a runaway while would freeze this tab - there is no
                      # subprocess timeout to save it here, unlike the server

def squash(text):
    return ''.join(str(text).split())

def atoms(text):
    import re
    found = re.findall(r'[A-Za-z_]\w*|-?\d+\.?\d*', str(text))
    return sorted(w.lower() for w in found)

def same(got, want):
    if isinstance(want, bool):
        return isinstance(got, bool) and got == want
    if isinstance(got, bool) != isinstance(want, bool):
        return False
    if isinstance(want, (int, float)) and isinstance(got, (int, float)):
        return abs(got - want) <= 1e-9 * max(1.0, abs(want))
    try:
        return got == want
    except Exception:
        return False

def short(text):
    text = str(text)
    return text if len(text) <= 300 else text[:300] + ' ...'

def run_file(source, out):
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        out['error'] = 'SyntaxError: %s   (line %s)' % (e.msg, e.lineno)
        return None
    body = list(tree.body)
    tail = None
    if body and isinstance(body[-1], ast.Expr):
        tail = body.pop()
    buf = io.StringIO()
    space = {'__name__': '__main__'}
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(ast.Module(body=body, type_ignores=[]), '<student>', 'exec'), space)
            if tail is not None:
                value = eval(compile(ast.Expression(tail.value), '<student>', 'eval'), space)
                if value is not None:
                    out['value'] = repr(value)
    except Exception as e:
        out['stdout'] = buf.getvalue()
        out['error'] = '%s: %s' % (type(e).__name__, e)
        return None
    out['stdout'] = buf.getvalue()
    return space

def interview(space, tests, out):
    for test in tests:
        call = test.get('call', '')
        wanted = test.get('is', '')
        row = {'call': call, 'want': wanted, 'got': '', 'ok': False, 'error': ''}
        try:
            want = eval(wanted, {'__builtins__': __builtins__}, {})
        except Exception as e:
            row['error'] = 'bad expected value: %s' % e
            out['tests'].append(row)
            continue
        noise = io.StringIO()
        try:
            with contextlib.redirect_stdout(noise):
                got = eval(call, space)
        except Exception as e:
            row['error'] = '%s: %s' % (type(e).__name__, e)
            row['got'] = row['error']
            out['tests'].append(row)
            continue
        row['got'] = short(repr(got))
        row['ok'] = same(got, want)
        out['tests'].append(row)

def shown(result):
    parts = []
    if (result.get('stdout') or '').strip():
        parts.append(result['stdout'].rstrip())
    if result.get('value'):
        parts.append(result['value'])
    return '\n'.join(parts)

def judge_challenge(question_json, code):
    q = json.loads(question_json)
    flat = squash(code).lower()

    if not code.strip():
        return json.dumps({'passed': False, 'output': '',
                           'reason': 'there is nothing in the editor yet', 'tests': []})
    if len(code) > MAX_CODE:
        return json.dumps({'passed': False, 'output': '',
                           'reason': 'keep it under %d characters' % MAX_CODE, 'tests': []})
    for bad in BANNED:
        if squash(bad).lower() in flat:
            return json.dumps({'passed': False, 'output': '',
                               'reason': '"%s" is switched off here - this one only needs '
                                        'def, a slot and return' % bad, 'tests': []})

    out = {'stdout': '', 'value': '', 'error': '', 'tests': []}
    space = run_file((q.get('setup') or '') + '\n' + (code or '') + '\n', out)
    result = out
    text_out = shown(result)

    if result.get('error'):
        return json.dumps({'passed': False, 'output': text_out,
                           'reason': result['error'], 'tests': []})

    if space is not None:
        interview(space, q.get('tests') or [], result)

    wanted_print = q.get('prints') or ''
    if wanted_print:
        if atoms(result.get('stdout', '')) != atoms(wanted_print):
            if not text_out.strip():
                reason = ('nothing came out - the function has to be CALLED, '
                          'and the answer printed')
            else:
                reason = 'that is not what should be on the screen yet'
            return json.dumps({'passed': False, 'output': text_out, 'reason': reason, 'tests': []})

    rows = result.get('tests') or []
    bad_rows = [r for r in rows if not r.get('ok')]
    if bad_rows:
        first = bad_rows[0]
        if first.get('error'):
            reason = 'we called  %s  and it did not survive:\n%s' % (first['call'], first['error'])
        elif first.get('got') == 'None':
            reason = ('we called  %s  and got None back.\n'
                      'Something printed it, or nobody returned it.' % first['call'])
        else:
            reason = 'we called  %s  and got  %s  back. It should be  %s' % (
                first['call'], first['got'], first['want'])
        return json.dumps({'passed': False, 'output': text_out, 'reason': reason, 'tests': rows})

    for needed in (q.get('require') or []):
        if isinstance(needed, list):
            if not any(squash(one).lower() in flat for one in needed):
                return json.dumps({'passed': False, 'output': text_out,
                    'reason': 'right answer, wrong road - this one needs  ' + '  or  '.join(needed),
                    'tests': rows})
        elif squash(needed).lower() not in flat:
            return json.dumps({'passed': False, 'output': text_out,
                'reason': 'right answer, wrong road - this one has to go through  ' + needed,
                'tests': rows})
    for banned in (q.get('forbid') or []):
        if squash(banned).lower() in flat:
            return json.dumps({'passed': False, 'output': text_out,
                'reason': 'no typing the answer by hand - "%s" has to be worked out, '
                         'not written down' % banned, 'tests': rows})

    return json.dumps({'passed': True, 'output': text_out, 'reason': '', 'tests': rows})
"""

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Function Lab</title>
<style>
:root{
  --bg:#05060f; --panel:#0d1020; --panel2:#12162b; --line:#232847;
  --ink:#e8ecff; --dim:#8b93bd;
  --cyan:#22e0ff; --pink:#ff3ea5; --lime:#b8ff3d; --amber:#ffcc3d; --violet:#a06bff;
  --mono:ui-monospace,"Cascadia Code","JetBrains Mono",Consolas,"Courier New",monospace;
}
*{box-sizing:border-box}
html,body{height:100%%}
body{margin:0; background:var(--bg); color:var(--ink);
  font-family:var(--mono); font-size:15px; overflow-x:hidden}

.aurora{position:fixed; inset:-20%%; z-index:0; filter:blur(90px); opacity:.5; pointer-events:none}
.blob{position:absolute; width:46vw; height:46vw; border-radius:50%%}
.b1{background:#7a3bff; top:-8%%; left:-6%%;  animation:drift1 19s ease-in-out infinite}
.b2{background:#ff2e8b; bottom:-12%%; right:-8%%; animation:drift2 23s ease-in-out infinite}
.b3{background:#00d9a3; top:35%%; left:45%%; animation:drift3 27s ease-in-out infinite}
@keyframes drift1{0%%,100%%{transform:translate(0,0) scale(1)}50%%{transform:translate(14vw,10vh) scale(1.2)}}
@keyframes drift2{0%%,100%%{transform:translate(0,0) scale(1.1)}50%%{transform:translate(-12vw,-8vh) scale(.9)}}
@keyframes drift3{0%%,100%%{transform:translate(0,0)}50%%{transform:translate(-16vw,12vh)}}

.wrap{position:relative; z-index:1; max-width:900px; margin:0 auto; padding:18px 20px 60px}
header{display:flex; align-items:center; gap:14px; flex-wrap:wrap; margin-bottom:16px}
.logo{font-size:24px; font-weight:800; letter-spacing:.14em;
  background:linear-gradient(92deg,var(--cyan),var(--violet) 55%%,var(--pink));
  -webkit-background-clip:text; background-clip:text; color:transparent}
.logo small{display:block; font-size:9.5px; letter-spacing:.32em; color:var(--dim);
  -webkit-text-fill-color:var(--dim); margin-top:3px}
.spacer{flex:1}
.badge{display:flex; align-items:center; gap:9px; background:rgba(18,22,43,.85);
  border:1px solid var(--line); border-radius:12px; padding:8px 14px}
.scoreBig{font-size:24px; font-weight:800; color:var(--lime); min-width:64px; text-align:right}
.scoreBig.bump{animation:bump .5s cubic-bezier(.2,1.7,.4,1)}
@keyframes bump{0%%{transform:scale(1)}40%%{transform:scale(1.45)}100%%{transform:scale(1)}}
.restart{font-size:12px; padding:9px 13px; border-color:#3a2140; color:var(--pink);
  background:rgba(255,62,165,.07)}
.restart:hover{border-color:var(--pink)}

.card{background:linear-gradient(180deg,rgba(13,16,32,.94),rgba(10,12,26,.94));
  border:1px solid var(--line); border-radius:18px; padding:18px;
  box-shadow:0 24px 60px rgba(0,0,0,.5)}
.card.shake{animation:shake .4s}
@keyframes shake{0%%,100%%{transform:translateX(0)}20%%{transform:translateX(-11px)}
  40%%{transform:translateX(9px)}60%%{transform:translateX(-6px)}80%%{transform:translateX(4px)}}

.strip{display:flex; gap:7px; margin-bottom:14px; flex-wrap:wrap; align-items:stretch}
.step{flex:1 1 42px; min-width:42px; border-radius:10px; border:1px solid var(--line);
  background:rgba(255,255,255,.03); color:var(--dim); padding:7px 4px; text-align:center;
  font-size:14px; font-weight:700; transition:.3s; overflow:hidden}
.step.won{border-color:var(--lime); background:rgba(184,255,61,.13); color:var(--lime)}
.step.gave{border-color:#4a4460; background:rgba(160,107,255,.1); color:#9d94bb}
.step.now{border-color:var(--cyan); background:rgba(34,224,255,.14); color:var(--cyan);
  flex:3 1 150px; box-shadow:0 0 0 1px var(--cyan) inset}
.step.locked{opacity:.4}

.lab{font-size:10px; letter-spacing:.26em; color:var(--dim); margin:0 0 7px; text-transform:uppercase}
.lab i{font-style:normal; color:var(--violet)}
.setup{background:#070a16; border:1px solid var(--line); border-radius:12px;
  padding:12px 14px; white-space:pre-wrap; word-break:break-word; line-height:1.55;
  font-size:14px; border-left:3px solid var(--violet)}
.task{font-size:16.5px; line-height:1.7; margin:0; color:#fff}
.mission{margin:14px 0}
.qname{font-size:13px; color:var(--dim); letter-spacing:.1em; margin:0 0 12px;
  display:flex; align-items:center; gap:10px; flex-wrap:wrap}
.qname b{color:var(--ink)}
.qname b.t{color:var(--cyan)}
.kind{font-size:10px; letter-spacing:.2em; font-weight:800; padding:4px 10px; border-radius:999px;
  border:1px solid var(--line)}
.kind.write{color:var(--lime); border-color:var(--lime); background:rgba(184,255,61,.1)}
.kind.call{color:var(--cyan); border-color:var(--cyan); background:rgba(34,224,255,.1)}
.kind.fix{color:var(--pink); border-color:var(--pink); background:rgba(255,62,165,.1)}

.edwrap{border:1px solid var(--line); border-radius:14px; overflow:hidden; background:#070a16;
  display:flex; transition:.2s}
.edwrap:focus-within{border-color:var(--cyan); box-shadow:0 0 0 1px var(--cyan)}
.gutter{padding:14px 10px 14px 14px; color:#3d466f; font-size:14px; line-height:1.6;
  text-align:right; user-select:none; background:#060812; min-width:44px; white-space:pre}
.codewrap{position:relative; flex:1; min-height:260px}
.hl,#code{margin:0; padding:14px; font-family:var(--mono); font-size:14px; line-height:1.6;
  white-space:pre-wrap; word-break:break-word; border:0; letter-spacing:0; tab-size:4}
.hl{position:absolute; inset:0; pointer-events:none; overflow:hidden; color:var(--ink)}
#code{position:relative; width:100%%; height:100%%; min-height:260px; resize:vertical;
  background:transparent; color:transparent; caret-color:var(--cyan); outline:none; display:block}
#code::selection{background:rgba(34,224,255,.28)}
.k{color:var(--pink)}   .s{color:var(--lime)}   .n{color:var(--amber)}
.c{color:#5a6494; font-style:italic}  .f{color:var(--cyan)}  .p{color:#c9d2ff}

.row{display:flex; gap:11px; margin-top:14px; flex-wrap:wrap; align-items:center}
button{font-family:var(--mono); cursor:pointer; border-radius:12px; font-size:14px;
  padding:12px 22px; border:1px solid var(--line); background:var(--panel2); color:var(--ink);
  transition:.16s; font-weight:600}
button:hover:not(:disabled){transform:translateY(-2px)}
button:disabled{opacity:.45; cursor:not-allowed}
.run{background:linear-gradient(92deg,var(--cyan),#3ba0ff); color:#04121c; border:0; font-weight:800}
.hint{border-color:var(--amber); color:var(--amber); background:rgba(255,204,61,.08)}
.reset{border-color:#3a4370; color:var(--dim); font-size:13px}
.giveup{border-color:#463a5e; color:#a89bc7; background:rgba(160,107,255,.07); font-size:13px}
.kbd{font-size:11px; color:var(--dim)}
.kbd b{color:var(--ink); background:#1a1f3a; border:1px solid var(--line); border-radius:5px; padding:2px 6px}

.res{margin-top:14px; border-radius:13px; padding:13px 15px; border:1px solid var(--line);
  background:#070a16; display:none}
.res.show{display:block}
.res.pass{border-color:var(--lime)}
.res.fail{border-color:var(--pink)}
.res h4{margin:0 0 8px; font-size:15px; letter-spacing:.05em}
.res.pass h4{color:var(--lime)} .res.fail h4{color:var(--pink)}
.res pre{margin:6px 0 0; white-space:pre-wrap; word-break:break-word; font-size:13.5px; color:var(--dim)}
.res .got{color:var(--ink)}
.gain{float:right; font-size:19px; font-weight:800; color:var(--lime)}
.nextup{margin-top:11px; color:var(--cyan); font-size:13px}

.tt{width:100%%; border-collapse:collapse; margin-top:10px; font-size:13px}
.tt th{text-align:left; font-size:9.5px; letter-spacing:.2em; color:var(--dim);
  font-weight:600; padding:0 8px 6px 0; text-transform:uppercase}
.tt td{padding:6px 8px 6px 0; border-top:1px solid #161b33; vertical-align:top;
  word-break:break-word; line-height:1.5}
.tt td.m{width:22px; font-weight:800}
.tt tr.y td.m{color:var(--lime)} .tt tr.n td.m{color:var(--pink)}
.tt .call{color:var(--cyan)} .tt .want{color:var(--lime)} .tt .gotv{color:var(--amber)}

.hintbox{margin-top:12px; border-radius:12px; padding:12px 14px; display:none;
  border:1px solid var(--amber); background:rgba(255,204,61,.08); color:var(--amber);
  line-height:1.7; white-space:pre-wrap}
.hintbox.show{display:block}

.answerbox{margin-top:14px; border-radius:13px; padding:15px 17px; display:none;
  border:1px solid var(--violet); background:rgba(160,107,255,.11)}
.answerbox.show{display:block}
.answerbox h4{margin:0 0 10px; font-size:15px; color:#cbb8ff; letter-spacing:.05em}
.answerbox pre{margin:0; padding:12px 14px; border-radius:10px; background:#070a16;
  border-left:3px solid var(--violet); color:var(--ink); font-size:14px; line-height:1.6;
  white-space:pre-wrap; word-break:break-word}
.answerbox .why{margin:12px 0 0; color:#c3b6e0; font-size:13px; line-height:1.7}
.answerbox .zero{float:right; font-size:15px; font-weight:800; color:#9d94bb}

.done{display:none; text-align:center; padding:40px 24px}
.done.show{display:block}
.done .big{font-size:60px; font-weight:800; color:var(--lime); line-height:1.1}
.done .of{color:var(--dim); font-size:15px; margin:6px 0 22px}
.done h2{margin:0 0 8px; font-size:24px; letter-spacing:.08em}
.done p{color:var(--dim); line-height:1.7; margin:0 auto 22px; max-width:460px}

.boot{text-align:center; padding:40px 24px}
.boot p{color:var(--dim); line-height:1.8; margin:0 0 18px}
.loadbar{height:8px; border-radius:8px; background:#0a0d1c; border:1px solid var(--line);
  overflow:hidden; max-width:340px; margin:0 auto 12px}
.loadfill{height:100%%; width:6%%; background:linear-gradient(90deg,var(--cyan),var(--violet));
  transition:width .4s ease}
.bootmsg{font-size:13px; color:var(--dim)}
#startBtn{display:none; margin-top:18px}
#startBtn.show{display:inline-block}

.toast{position:fixed; left:50%%; top:22px; transform:translateX(-50%%) translateY(-140%%); z-index:60;
  background:var(--panel2); border:1px solid var(--cyan); color:var(--ink);
  padding:12px 22px; border-radius:12px; transition:.4s cubic-bezier(.2,1.5,.4,1);
  box-shadow:0 14px 40px rgba(0,0,0,.6); font-size:14px}
.toast.on{transform:translateX(-50%%) translateY(0)}
.dot{position:fixed; width:9px; height:9px; z-index:70; pointer-events:none; border-radius:2px}
footer{text-align:center; color:var(--dim); font-size:.76rem; margin-top:26px}
footer a{color:var(--cyan)}
</style>
</head>
<body>
<div class="aurora"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div></div>

<div class="wrap">
  <header>
    <div class="logo">FUNCTION&nbsp;LAB<small>10 CHALLENGES &middot; PRACTISE ON YOUR OWN</small></div>
    <div class="spacer"></div>
    <div class="badge">POINTS <span class="scoreBig" id="score">0</span></div>
    <button class="restart" id="restartBtn" style="display:none">&#10226; start over</button>
  </header>

  <div class="card boot" id="boot">
    <p>Ten challenges on <b>functions with a door on each side</b> &mdash; values in
       through parameters, an answer out through <code>return</code>. Every one is
       real Python, checked by <b>calling your function</b>, not by reading it.</p>
    <div class="loadbar"><div class="loadfill" id="loadfill"></div></div>
    <div class="bootmsg" id="bootmsg">tap start to load Python&hellip;</div>
    <button class="run" id="startBtn">START &rarr;</button>
  </div>

  <div id="game" style="display:none">
    <div class="strip" id="strip"></div>

    <div class="card" id="stage">
      <div id="playing">
        <p class="qname">CHALLENGE <b id="qnum">1</b> OF <b id="qtot">%(total)d</b> &middot;
          <b class="t" id="qtitle">&mdash;</b>
          <span class="kind write" id="kind">WRITE IT</span></p>

        <div id="setupWrap" style="display:none">
          <p class="lab">Already in memory <i>&mdash; you do not type this</i></p>
          <div class="setup" id="setup">&mdash;</div>
        </div>

        <div class="mission">
          <p class="lab">Your mission</p>
          <p class="task" id="task" dir="auto">&mdash;</p>
        </div>

        <p class="lab" style="margin-top:16px">Your code</p>
        <div class="edwrap">
          <div class="gutter" id="gutter">1</div>
          <div class="codewrap">
            <pre class="hl" id="hl"></pre>
            <textarea id="code" spellcheck="false" autocomplete="off" autocapitalize="off"></textarea>
          </div>
        </div>

        <div class="row">
          <button class="run" id="runBtn">&#9654; RUN</button>
          <button class="hint" id="hintBtn">&#128161; HINT &mdash; costs half</button>
          <button class="reset" id="resetBtn">&#10226; back to the starting code</button>
          <button class="giveup" id="giveupBtn">&#129335; I don't know</button>
          <span class="kbd"><b>Ctrl</b> + <b>Enter</b> runs it</span>
        </div>

        <div class="hintbox" id="hintbox" dir="auto"></div>

        <div class="answerbox" id="answerbox">
          <h4><span class="zero">0 pts</span>THE ANSWER WAS</h4>
          <pre id="answerCode">&mdash;</pre>
          <p class="why" id="answerWhy" dir="auto">&mdash;</p>
          <button class="run" id="nextBtn" style="margin-top:14px">NEXT CHALLENGE &rarr;</button>
        </div>

        <div class="res" id="res"></div>
      </div>

      <div class="done" id="done">
        <h2>&#127942; ALL DONE</h2>
        <div class="big" id="finalScore">0</div>
        <div class="of">out of <span id="finalMax">1000</span></div>
        <p id="finalWord">&mdash;</p>
        <button class="run" id="againBtn">&#10226; play it again</button>
      </div>
    </div>
  </div>

  <footer>
    Practice version &mdash; runs Python in your browser, nothing is sent anywhere.
    <a href="../../index.html#simulators">back to the simulators</a>
  </footer>
</div>

<div class="toast" id="toast"></div>

<script src="https://cdn.jsdelivr.net/pyodide/v0.28.3/full/pyodide.js"></script>
<script>
const $ = id => document.getElementById(id);
const QUESTIONS = %(questions)s;
const TOTAL = QUESTIONS.length;
const FAST_SECONDS = 90;
const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v0.28.3/full/';

const RUNNER_PY = %(runner_py)s;

let pyodide = null, judgeChallenge = null;

function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function nl(s){return esc(s).split('\n').join('<br>');}

async function bootPython(){
  const bar = $('loadfill'), msg = $('bootmsg');
  let pct = 6; bar.style.width = pct + '%%';
  const creep = setInterval(() => { pct = Math.min(pct + 4, 88); bar.style.width = pct + '%%'; }, 700);
  try{
    msg.textContent = 'downloading Python (about 10 MB, once)…';
    pyodide = await loadPyodide({indexURL: PYODIDE_URL});
    msg.textContent = 'starting it up…';
    pyodide.runPython(RUNNER_PY);
    judgeChallenge = pyodide.globals.get('judge_challenge');
    clearInterval(creep);
    bar.style.width = '100%%';
    msg.innerHTML = 'Python is running in this tab. <b style="color:var(--lime)">Ready.</b>';
    $('startBtn').classList.add('show');
  }catch(e){
    clearInterval(creep); bar.style.width = '100%%';
    msg.innerHTML = '<b style="color:var(--pink)">Could not load Python.</b><br>' +
      'Check the internet connection and reload the page.<br>' +
      '<span style="opacity:.7">' + esc(String(e)).slice(0, 160) + '</span>';
  }
}

$('startBtn').onclick = () => {
  $('boot').style.display = 'none';
  $('game').style.display = '';
  $('restartBtn').style.display = '';
  begin();
};
bootPython();

/* ---------------- python syntax colours ---------------- */
const KW = /^(for|in|if|elif|else|while|print|return|def|not|and|or|is|True|False|None|break|continue|pass|del)$/;
const FN = /^(list|dict|set|tuple|sorted|max|min|sum|len|str|int|float|reversed|enumerate|zip|round|abs|type|help)$/;
function highlight(src){
  const re = /(#[^\n]*)|([furbFURB]{0,2}'(?:\\.|[^'\\\n])*'|[furbFURB]{0,2}"(?:\\.|[^"\\\n])*")|(\b\d+\.?\d*\b)|([A-Za-z_]\w*)/g;
  let out = '', last = 0, m;
  while((m = re.exec(src)) !== null){
    out += esc(src.slice(last, m.index));
    if(m[1])      out += '<span class="c">' + esc(m[1]) + '</span>';
    else if(m[2]) out += '<span class="s">' + esc(m[2]) + '</span>';
    else if(m[3]) out += '<span class="n">' + esc(m[3]) + '</span>';
    else {
      const w = m[4];
      out += '<span class="' + (KW.test(w) ? 'k' : (FN.test(w) ? 'f' : 'p')) + '">' + esc(w) + '</span>';
    }
    last = re.lastIndex;
  }
  return out + esc(src.slice(last)) + '\n';
}
function paintEditor(){
  const src = $('code').value;
  $('hl').innerHTML = highlight(src);
  let g = '';
  for(let i = 1; i <= Math.max(src.split('\n').length, 1); i++) g += i + '\n';
  $('gutter').textContent = g;
}
$('code').addEventListener('input', paintEditor);
$('code').addEventListener('scroll', () => { $('hl').scrollTop = $('code').scrollTop; });
$('code').addEventListener('keydown', e => {
  if(e.key === 'Enter' && (e.ctrlKey || e.metaKey)){ e.preventDefault(); return run(); }
  const el = e.target, s = el.selectionStart;
  if(e.key === 'Tab'){
    e.preventDefault();
    el.value = el.value.slice(0, s) + '    ' + el.value.slice(el.selectionEnd);
    el.selectionStart = el.selectionEnd = s + 4;
    paintEditor();
  }
});

/* ---------------- game state ---------------- */
let cur = 1, score = 0, finished = false;
let solved = {}, hinted = {}, gaveup = {};
const drafts = {};
const isDone = q => solved[q] !== undefined;
const qOf = n => QUESTIONS.find(x => x.q === n) || {};

function drawStrip(){
  $('strip').innerHTML = QUESTIONS.map(q => {
    let cls = 'step';
    if(gaveup[q.q]) cls += ' gave';
    else if(isDone(q.q)) cls += ' won';
    else if(q.q === cur && !finished) cls += ' now';
    else cls += ' locked';
    return '<div class="' + cls + '">' + q.q +
      (q.q === cur && !finished ? '<span class="sub">' + esc(q.title) + '</span>' : '') +
      '</div>';
  }).join('');
}

let toastT;
function toast(msg){
  $('toast').textContent = msg;
  $('toast').classList.add('on');
  clearTimeout(toastT);
  toastT = setTimeout(() => $('toast').classList.remove('on'), 2600);
}

function confetti(){
  const colors = ['#22e0ff','#ff3ea5','#b8ff3d','#ffcc3d','#a06bff'];
  for(let i = 0; i < 60; i++){
    const d = document.createElement('div');
    d.className = 'dot'; d.style.background = colors[i %% colors.length];
    d.style.left = (45 + Math.random() * 10) + 'vw'; d.style.top = '40vh';
    document.body.appendChild(d);
    const ang = Math.random() * Math.PI * 2, pow = 120 + Math.random() * 400;
    d.animate([
      {transform:'translate(0,0) rotate(0deg)', opacity:1},
      {transform:'translate(' + Math.cos(ang)*pow + 'px,' + (Math.sin(ang)*pow + 440) +
        'px) rotate(' + (Math.random()*900 - 450) + 'deg)', opacity:0}
    ], {duration: 1000 + Math.random()*900, easing:'cubic-bezier(.15,.7,.4,1)'})
     .onfinish = () => d.remove();
  }
}

const KIND_WORD = {write:'WRITE IT', call:'CALL IT', fix:'FIX IT'};
let openedAt = 0;

function openQ(n){
  cur = n; finished = false;
  $('playing').style.display = ''; $('done').classList.remove('show');
  const q = qOf(n);
  $('qnum').textContent = n; $('qtot').textContent = TOTAL;
  $('qtitle').textContent = q.title;
  $('kind').className = 'kind ' + (q.kind || 'write');
  $('kind').textContent = KIND_WORD[q.kind] || 'WRITE IT';

  $('setupWrap').style.display = q.setup ? '' : 'none';
  if(q.setup) $('setup').innerHTML = highlight(q.setup.replace(/\s+$/,''));
  $('task').innerHTML = nl(q.task);

  $('res').className = 'res';
  $('hintbox').className = 'hintbox';
  $('answerbox').className = 'answerbox';
  $('code').value = drafts[n] !== undefined ? drafts[n] : (q.starter || '');
  paintEditor();
  drawStrip();
  openedAt = Date.now();
  $('hintBtn').disabled = false; $('hintBtn').textContent = '💡 HINT — costs half';
  $('giveupBtn').disabled = false; $('runBtn').disabled = false;
}

function nextUnsolved(){
  for(const q of QUESTIONS) if(!isDone(q.q)) return q.q;
  return null;
}

function testTable(rows){
  if(!rows || !rows.length) return '';
  return '<table class="tt"><thead><tr><th></th><th>we called</th><th>wanted</th><th>got</th></tr></thead><tbody>' +
    rows.map(r => '<tr class="' + (r.ok ? 'y' : 'n') + '">' +
      '<td class="m">' + (r.ok ? '✔' : '✖') + '</td>' +
      '<td class="call">' + esc(r.call) + '</td>' +
      '<td class="want">' + esc(r.want) + '</td>' +
      '<td class="gotv">' + esc(r.error || r.got) + '</td></tr>').join('') +
    '</tbody></table>';
}

function pointsFor(elapsed, usedHint){
  const fast = elapsed <= FAST_SECONDS;
  return usedHint ? (fast ? 50 : 25) : (fast ? 100 : 50);
}

function run(){
  if(finished) return;
  const code = $('code').value;
  drafts[cur] = code;
  if(!code.trim()) return;
  $('runBtn').disabled = true; $('runBtn').textContent = '⏳ RUNNING…';

  let r;
  try{
    r = JSON.parse(judgeChallenge(JSON.stringify(qOf(cur)), code));
  }catch(e){
    r = {passed:false, output:'', reason:'could not run that: ' + e, tests:[]};
  }
  $('runBtn').textContent = '▶ RUN'; $('runBtn').disabled = false;

  const box = $('res');
  box.className = 'res show ' + (r.passed ? 'pass' : 'fail');

  if(r.passed){
    const elapsed = (Date.now() - openedAt) / 1000;
    const gained = pointsFor(elapsed, !!hinted[cur]);
    if(!isDone(cur)){
      solved[cur] = gained;
      score += gained;
    }
    $('score').textContent = score;
    $('score').classList.remove('bump'); void $('score').offsetWidth; $('score').classList.add('bump');
    confetti();
    drawStrip();
    const nxt = nextUnsolved();
    box.innerHTML = '<span class="gain">+' + gained + '</span>' +
      '<h4>✔ IT ANSWERS — in ' + elapsed.toFixed(1) + 's</h4>' +
      (r.output ? '<pre class="got">' + esc(r.output.trimEnd()) + '</pre>' : '') +
      testTable(r.tests) +
      '<div class="nextup">' + (nxt ? 'challenge ' + nxt + ' opening…' : 'that was the last one…') + '</div>';
    $('hintBtn').disabled = true; $('giveupBtn').disabled = true;
    setTimeout(() => nxt ? openQ(nxt) : finish(), 1900);
  } else {
    box.innerHTML = '<h4>✖ NOT YET</h4><pre>' + nl(r.reason || '') + '</pre>' +
      (r.output ? '<pre class="lab" style="letter-spacing:.2em;margin-top:12px">WHAT APPEARED ON THE SCREEN</pre>' +
                  '<pre class="got">' + esc(r.output.trimEnd()) + '</pre>' : '') +
      testTable(r.tests);
    $('stage').classList.add('shake');
    setTimeout(() => $('stage').classList.remove('shake'), 420);
  }
}

function useHint(){
  if(finished || isDone(cur)) return;
  hinted[cur] = true;
  $('hintbox').className = 'hintbox show';
  $('hintbox').textContent = '💡 ' + qOf(cur).hint;
  $('hintBtn').textContent = '💡 show the hint again';
}

function resetCode(){
  if(!confirm('Throw away your changes and go back to the starting code?')) return;
  drafts[cur] = qOf(cur).starter || '';
  $('code').value = drafts[cur];
  paintEditor();
}

function giveUp(){
  if(isDone(cur)) return;
  const q = qOf(cur);
  solved[cur] = 0; gaveup[cur] = true;
  drawStrip();
  $('res').className = 'res';
  $('answerbox').className = 'answerbox show';
  $('answerCode').innerHTML = highlight(q.solution.replace(/\s+$/,''));
  $('answerWhy').textContent = q.trap;
  $('hintBtn').disabled = true; $('giveupBtn').disabled = true; $('runBtn').disabled = true;
  toast('no shame in it — the answer is below');
}

function nextFromAnswer(){
  $('answerbox').className = 'answerbox';
  const nxt = nextUnsolved();
  if(nxt) openQ(nxt); else finish();
}

function finish(){
  finished = true;
  $('playing').style.display = 'none';
  $('done').classList.add('show');
  const max = TOTAL * 100;
  $('finalScore').textContent = score;
  $('finalMax').textContent = max;
  const pct = score / max;
  $('finalWord').textContent =
      pct >= 0.95 ? 'A perfect run. Ten functions written, called and repaired at full speed.'
    : pct >= 0.6  ? 'All ten done. The hints cost you a little, the functions did not.'
    : pct >= 0.3  ? 'You got through it — go back over the ones you gave up on.'
    :               'Worth another pass — open the lesson page and try again.';
  if(pct >= 0.95) confetti();
}

function begin(){
  cur = 1; score = 0; finished = false;
  solved = {}; hinted = {}; gaveup = {};
  for(const k in drafts) delete drafts[k];
  $('score').textContent = '0';
  openQ(1);
}

$('runBtn').onclick = run;
$('hintBtn').onclick = useHint;
$('resetBtn').onclick = resetCode;
$('giveupBtn').onclick = giveUp;
$('nextBtn').onclick = nextFromAnswer;
$('againBtn').onclick = begin;
$('restartBtn').onclick = () => { if(confirm('Start over from challenge 1? Your progress will be lost.')) begin(); };
</script>
</body>
</html>
"""


def main():
    build()


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
