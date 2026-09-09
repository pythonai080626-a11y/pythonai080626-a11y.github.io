# -*- coding: utf-8 -*-
"""
make_exam_prep.py  --  build exam_prep/index.html from exam_prep/questions.py.

Exam Rehearsal: pick a level, get a real coding question, write a real
function, press RUN. Judged the same way as Function Lab (99_games/func_01) -
we call the student's function ourselves and compare what came back, using
Pyodide (CPython compiled to WebAssembly) so no server is needed at all.

Grows with the question bank: add more entries to exam_prep/questions.py and
re-run this script - nothing else changes.

    python make_exam_prep.py

Every variant is checked against its own solution (and its own starter code)
before the page is built - see self_check() below. That is also where
'expected_output' gets computed: exactly what the SOLUTION prints, so the
"expected output" panel is never guessed at, only ever the real thing.
"""

import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
QSRC = os.path.join(HERE, 'exam_prep', 'questions.py')
OUT = os.path.join(HERE, 'exam_prep', 'index.html')

sys.path.insert(0, HERE)
from make_solo_func import RUNNER_PY  # noqa: E402  (the verified func_01 judge, ported)


def load_questions():
    spec = importlib.util.spec_from_file_location('exam_prep_questions', QSRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.QUESTIONS, mod.LEVELS


def _check_one(judge_challenge, level, qid, label, v, problems):
    """Check one {task, starter, expect, tests, require, forbid, solution}
    shape against the real judge, and attach 'expected_output' to it (what
    the SOLUTION prints)."""
    payload = json.dumps({
        'setup': v.get('setup', ''), 'task': v['task'], 'starter': v['starter'],
        'expect': v['expect'], 'tests': v['tests'], 'prints': '',
        'require': v['require'], 'forbid': v['forbid'],
    })
    sol = json.loads(judge_challenge(payload, v['solution']))
    if not sol['passed']:
        problems.append('%s/%s %s: SOLUTION does not pass - %s'
                        % (level, qid, label, sol['reason']))
    elif not (sol.get('output') or '').strip():
        problems.append('%s/%s %s: SOLUTION prints nothing - the '
                        'starter/solution needs a print(...) call at the end '
                        'for the expected-output panel to show anything'
                        % (level, qid, label))
    else:
        v['expected_output'] = sol['output']
    start = json.loads(judge_challenge(payload, v['starter']))
    if start['passed']:
        problems.append('%s/%s %s: STARTER already passes - '
                        'the challenge gives nothing away, but this one does'
                        % (level, qid, label))


def self_check(Q, LEVELS):
    """Run every solution and every starter through the real judge, in plain
    CPython (not Pyodide - same interpreter family, much faster to run here).
    Refuses to build the page if anything is wrong.

    Along the way this attaches 'expected_output' to every question and
    every retry entry: exactly what the SOLUTION prints, captured from the
    same judge run."""
    ns = {}
    exec(compile(RUNNER_PY, '<runner_py>', 'exec'), ns)
    judge_challenge = ns['judge_challenge']

    problems = []
    for level in LEVELS:
        for item in Q.get(level, []):
            _check_one(judge_challenge, level, item['id'], 'primary', item, problems)
            for ri, r in enumerate(item.get('retry', [])):
                _check_one(judge_challenge, level, item['id'], 'retry %d' % ri, r, problems)
    return problems


def build():
    Q, LEVELS = load_questions()

    problems = self_check(Q, LEVELS)
    if problems:
        print('REFUSING TO BUILD - fix these first:')
        for p in problems:
            print('  -', p)
        raise SystemExit(1)

    bank = {}
    counts = {}
    for level in LEVELS:
        items = []
        for item in Q.get(level, []):
            items.append({
                'id': item['id'],
                'title': item['title'],
                'topic': item['topic'],
                'task': item['task'],
                'starter': item['starter'],
                'expect': item['expect'],
                'tests': item['tests'],
                'require': item['require'],
                'forbid': item['forbid'],
                'hint': item['hint'],
                'solution': item['solution'],
                'expected_output': item['expected_output'],
                'setup': item.get('setup', ''),
                'retry': item.get('retry', []),
            })
        bank[level] = items
        counts[level] = len(items)

    page = TEMPLATE % {
        'levels': json.dumps(LEVELS),
        'bank': json.dumps(bank, ensure_ascii=False, indent=1),
        'runner_py': json.dumps(RUNNER_PY),
    }
    io.open(OUT, 'w', encoding='utf-8', newline='\r\n').write(page)
    total_q = sum(len(Q.get(lv, [])) for lv in LEVELS)
    print('exam_prep    -> %s  (%d questions across %d levels, %s per level, %d bytes)'
          % (os.path.relpath(OUT, HERE), total_q, len(LEVELS),
             '/'.join(str(counts[lv]) for lv in LEVELS), len(page)))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Exam Rehearsal</title>
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
.logo{font-size:24px; font-weight:800; letter-spacing:.12em;
  background:linear-gradient(92deg,var(--cyan),var(--violet) 55%%,var(--pink));
  -webkit-background-clip:text; background-clip:text; color:transparent}
.logo small{display:block; font-size:9.5px; letter-spacing:.3em; color:var(--dim);
  -webkit-text-fill-color:var(--dim); margin-top:3px}
.spacer{flex:1}
.badge{display:flex; align-items:center; gap:9px; background:rgba(18,22,43,.85);
  border:1px solid var(--line); border-radius:12px; padding:8px 14px; font-size:13px}
.scoreBig{font-size:22px; font-weight:800; color:var(--lime)}
.scoreBig.bump{animation:bump .5s cubic-bezier(.2,1.7,.4,1)}
@keyframes bump{0%%{transform:scale(1)}40%%{transform:scale(1.4)}100%%{transform:scale(1)}}

/* ---------- level tabs ---------- */
.levels{display:flex; gap:9px; margin-bottom:16px; flex-wrap:wrap}
.lvl{
  flex:1; min-width:120px; border-radius:13px; border:1px solid var(--line);
  background:var(--panel2); color:var(--dim); padding:11px 14px; text-align:center;
  cursor:pointer; font-weight:800; font-size:13px; letter-spacing:.08em;
  text-transform:uppercase; transition:.16s;
}
.lvl:hover{border-color:var(--cyan)}
.lvl.on.easy{border-color:var(--lime); color:var(--lime); background:rgba(184,255,61,.1)}
.lvl.on.medium{border-color:var(--amber); color:var(--amber); background:rgba(255,204,61,.1)}
.lvl.on.expert{border-color:var(--pink); color:var(--pink); background:rgba(255,62,165,.1)}
.lvl .n{display:block; font-size:10px; font-weight:600; opacity:.7; margin-top:2px;
  text-transform:none; letter-spacing:0}

.card{background:linear-gradient(180deg,rgba(13,16,32,.94),rgba(10,12,26,.94));
  border:1px solid var(--line); border-radius:18px; padding:18px;
  box-shadow:0 24px 60px rgba(0,0,0,.5)}
.card.shake{animation:shake .4s}
@keyframes shake{0%%,100%%{transform:translateX(0)}20%%{transform:translateX(-11px)}
  40%%{transform:translateX(9px)}60%%{transform:translateX(-6px)}80%%{transform:translateX(4px)}}

.qname{font-size:13px; color:var(--dim); letter-spacing:.06em; margin:0 0 12px;
  display:flex; align-items:center; gap:10px; flex-wrap:wrap}
.qname b{color:var(--ink)}
.topic{font-size:11.5px; color:var(--dim); letter-spacing:.02em}

.task{font-size:16.5px; line-height:1.7; margin:0 0 16px; color:#fff; white-space:pre-wrap}

/* code the student did NOT have to write themselves - a ready-made import,
   a given pattern/constant - shown read-only, above the editor, so they
   know it is already there for them to use. */
.setupWrap{margin:0 0 16px}
.setupWrap .lab{margin:0 0 6px; font-size:11.5px; color:var(--dim)}
.setupCode{background:#070a16; border:1px solid var(--line); border-inline-start:3px solid var(--violet);
  border-radius:10px; padding:11px 14px; margin:0; white-space:pre-wrap; word-break:break-word;
  line-height:1.55; font-size:13.5px; color:var(--ink)}

/* level + progress, right above the expected-output panel - a single,
   unmissable "which level, which question" readout (e.g. "E · 3 / 5"). */
.levelTag{display:inline-flex; align-items:center; gap:5px; font-size:12.5px;
  font-weight:800; letter-spacing:.06em; margin:0 0 8px; padding:5px 11px;
  border-radius:9px; border:1px solid var(--line); background:var(--panel2); color:var(--dim)}
.levelTag.easy{border-color:var(--lime); color:var(--lime); background:rgba(184,255,61,.1)}
.levelTag.medium{border-color:var(--amber); color:var(--amber); background:rgba(255,204,61,.1)}
.levelTag.expert{border-color:var(--pink); color:var(--pink); background:rgba(255,62,165,.1)}

.outbox{
  position:relative; background:#070a16; border:2px solid var(--line);
  border-radius:12px; padding:10px 14px; margin:0 0 16px;
}
/* the border colour tracks the current level, same hue as .levelTag/.pill -
   light green on EASY, amber on MEDIUM, red-pink on EXPERT. No animation -
   just a static colour, set once when the question opens. */
.outbox.easy{border-color:var(--lime)}
.outbox.medium{border-color:var(--amber)}
.outbox.expert{border-color:var(--pink)}
.outbox .lab{margin:0 0 6px; position:relative}
.outtext{margin:0; font-family:var(--mono); font-size:14px; line-height:1.6;
  color:var(--lime); white-space:pre-wrap; word-break:break-word}
.outbox.medium .outtext{color:var(--amber)}
.outbox.expert .outtext{color:var(--pink)}

.edwrap{border:1px solid var(--line); border-radius:14px; overflow:hidden; background:#070a16;
  display:flex; transition:.2s}
.edwrap:focus-within{border-color:var(--cyan); box-shadow:0 0 0 1px var(--cyan)}
.gutter{padding:14px 10px 14px 14px; color:#3d466f; font-size:14px; line-height:1.6;
  text-align:right; user-select:none; background:#060812; min-width:44px; white-space:pre}
.codewrap{position:relative; flex:1; min-height:220px}
.hl,#code{margin:0; padding:14px; font-family:var(--mono); font-size:14px; line-height:1.6;
  white-space:pre-wrap; word-break:break-word; border:0; letter-spacing:0; tab-size:4}
.hl{position:absolute; inset:0; pointer-events:none; overflow:hidden; color:var(--ink)}
#code{position:relative; width:100%%; height:100%%; min-height:220px; resize:vertical;
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
.solve{border-color:var(--violet); color:#cbb8ff; background:rgba(160,107,255,.08)}
.skip{border-color:#3a4370; color:var(--dim); font-size:13px}
.btnkbd{font-size:9.5px; opacity:.6; margin-inline-start:6px; font-weight:700; letter-spacing:.02em}
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

.solvebox{margin-top:12px; border-radius:12px; padding:14px 16px; display:none;
  border:1px solid var(--violet); background:rgba(160,107,255,.1)}
.solvebox.show{display:block}
.solvebox pre{margin:8px 0 0; padding:12px 14px; border-radius:10px; background:#070a16;
  border-left:3px solid var(--violet); color:var(--ink); font-size:14px; line-height:1.6;
  white-space:pre-wrap; word-break:break-word}
.solvehead{display:flex; align-items:center; justify-content:space-between; gap:10px}
.copyBtn{
  display:flex; align-items:center; gap:6px; padding:5px 11px; font-size:11px;
  border-radius:8px; border:1px solid var(--violet); color:#cbb8ff;
  background:rgba(160,107,255,.12); cursor:pointer; font-family:var(--mono);
  font-weight:700; letter-spacing:.04em; transition:.15s;
}
.copyBtn:hover{background:rgba(160,107,255,.24); transform:translateY(-1px)}
.copyBtn.done{border-color:var(--lime); color:var(--lime); background:rgba(184,255,61,.14)}

.boot{text-align:center; padding:40px 24px}
.boot p{color:var(--dim); line-height:1.8; margin:0 0 18px}
.loadbar{height:8px; border-radius:8px; background:#0a0d1c; border:1px solid var(--line);
  overflow:hidden; max-width:340px; margin:0 auto 12px}
.loadfill{height:100%%; width:6%%; background:linear-gradient(90deg,var(--cyan),var(--violet));
  transition:width .4s ease}
.bootmsg{font-size:13px; color:var(--dim)}
#startBtn{display:none; margin-top:18px}
#startBtn.show{display:inline-block}

footer{text-align:center; color:var(--dim); font-size:.76rem; margin-top:26px}
footer a{color:var(--cyan)}

/* ---------- level-complete modal ---------- */
.levelModal{position:fixed; inset:0; z-index:80; display:none; align-items:center;
  justify-content:center; background:rgba(3,4,12,.82); backdrop-filter:blur(6px); padding:20px}
.levelModal.show{display:flex; animation:lmFade .18s ease}
@keyframes lmFade{from{opacity:0}to{opacity:1}}
.levelModalCard{position:relative; width:min(420px,100%%); text-align:center; padding:32px 26px 26px;
  border-radius:20px; border:1px solid var(--lime);
  background:linear-gradient(180deg,#141833,#0b0e1e);
  box-shadow:0 30px 90px rgba(0,0,0,.7), 0 0 60px rgba(184,255,61,.2);
  animation:lmPop .28s cubic-bezier(.2,1.5,.42,1)}
@keyframes lmPop{from{opacity:0; transform:scale(.9) translateY(14px)}to{opacity:1; transform:none}}
.lmIcon{font-size:44px; margin-bottom:10px; line-height:1}
.levelModalCard h3{margin:0 0 8px; font-size:19px; color:var(--ink)}
.levelModalCard p{margin:0 0 24px; color:var(--dim); font-size:13.5px; line-height:1.75}
.lmRow{display:flex; gap:10px; justify-content:center; flex-wrap:wrap}
.lmBtn{padding:12px 18px; font-size:12.5px; border-radius:12px; border:1px solid var(--line);
  cursor:pointer; font-family:var(--mono); font-weight:700; transition:.15s}
.lmRestart{background:var(--panel2); color:var(--dim)}
.lmRestart:hover{border-color:var(--ink); color:var(--ink); transform:translateY(-1px)}
.lmNext{background:linear-gradient(92deg,var(--lime),#84cc16); color:#0b1400; border:0; font-weight:800}
.lmNext:hover{transform:translateY(-1px)}
.lmClose{position:absolute; top:10px; right:12px; background:none; border:0; color:var(--dim);
  font-size:22px; cursor:pointer; line-height:1; padding:4px 8px}
.lmClose:hover{color:var(--ink)}

/* ---------- solved-one modal - the keyboard-first "keep going" popup ---------- */
.solvedModal{position:fixed; inset:0; z-index:85; display:none; align-items:center;
  justify-content:center; background:rgba(3,4,12,.8); backdrop-filter:blur(5px); padding:20px}
.solvedModal.show{display:flex; animation:lmFade .15s ease}
.solvedModalCard{width:min(340px,100%%); text-align:center; padding:28px 24px 22px;
  border-radius:18px; border:1px solid var(--cyan);
  background:linear-gradient(180deg,#141833,#0b0e1e);
  box-shadow:0 26px 70px rgba(0,0,0,.65), 0 0 46px rgba(34,224,255,.22);
  animation:lmPop .22s cubic-bezier(.2,1.5,.42,1)}
.svIcon{font-size:38px; margin-bottom:8px; line-height:1}
.solvedModalCard h3{margin:0 0 8px; font-size:18px; color:var(--ink)}
.solvedModalCard p{margin:0 0 20px; color:var(--dim); font-size:13px}
.svBtn{width:100%%; padding:13px 18px; font-size:13px; border-radius:12px; border:0;
  cursor:pointer; font-family:var(--mono); font-weight:800; letter-spacing:.02em;
  background:linear-gradient(92deg,var(--cyan),#3ba0ff); color:#04121c; transition:.15s}
.svBtn:hover{transform:translateY(-1px)}
.svBtn:focus{outline:2px solid var(--cyan); outline-offset:3px}
.svHint{margin-top:11px; font-size:11px; color:var(--dim)}
.svHint b{color:var(--cyan); background:#1a1f3a; border:1px solid var(--line);
  border-radius:5px; padding:1px 6px}

/* ---------- final-stats modal - shown once the last level is finished ---------- */
.statsModal{position:fixed; inset:0; z-index:80; display:none; align-items:center;
  justify-content:center; background:rgba(3,4,12,.85); backdrop-filter:blur(6px); padding:20px}
.statsModal.show{display:flex; animation:lmFade .18s ease}
.statsModalCard{position:relative; width:min(440px,100%%); text-align:center; padding:32px 26px 26px;
  border-radius:20px; border:1px solid var(--pink);
  background:linear-gradient(180deg,#141833,#0b0e1e);
  box-shadow:0 30px 90px rgba(0,0,0,.7), 0 0 60px rgba(255,62,165,.22);
  animation:lmPop .28s cubic-bezier(.2,1.5,.42,1)}
.statsModalCard h3{margin:10px 0 8px; font-size:19px; color:var(--ink)}
.statsModalCard p{margin:0 0 20px; color:var(--dim); font-size:13.5px; line-height:1.75}
.statsGrid{display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:22px}
.statCell{background:#0d1020; border:1px solid var(--line); border-radius:12px; padding:14px 10px}
.statCell .num{font-size:23px; font-weight:800; color:var(--pink)}
.statCell .lab{font-size:10px; color:var(--dim); letter-spacing:.05em; text-transform:uppercase; margin-top:4px}
.statsRestart{width:100%%; padding:13px 18px; font-size:13px; border-radius:12px; border:0;
  cursor:pointer; font-family:var(--mono); font-weight:800; letter-spacing:.02em;
  background:linear-gradient(92deg,var(--pink),#c2185b); color:#2a0313; transition:.15s}
.statsRestart:hover{transform:translateY(-1px)}
.statsRestart:focus{outline:2px solid var(--pink); outline-offset:3px}
</style>
</head>
<body>
<div class="aurora"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div></div>

<div class="wrap">
  <header>
    <div class="logo">EXAM&nbsp;REHEARSAL<small>WRITE IT &middot; RUN IT &middot; SEE IF IT WORKS</small></div>
    <div class="spacer"></div>
    <div class="badge">SOLVED <span class="scoreBig" id="score">0</span></div>
  </header>

  <div class="card boot" id="boot">
    <p>Pick a level, get a real question, and write a real function. Press <b>RUN</b>
       and your code actually runs &mdash; the checker <b>calls your function</b> and
       compares what came back, exactly like Function Lab.</p>
    <div class="loadbar"><div class="loadfill" id="loadfill"></div></div>
    <div class="bootmsg" id="bootmsg">tap start to load Python&hellip;</div>
    <button class="run" id="startBtn">START &rarr;</button>
  </div>

  <div id="game" style="display:none">
    <div class="levels" id="levels"></div>

    <div class="card" id="stage">
      <p class="qname">
        <span class="pill" id="pill">EASY</span>
        <b id="qtitle">&mdash;</b>
        <span class="topic" id="qtopic"></span>
      </p>

      <p class="task" id="task" dir="auto">&mdash;</p>

      <div class="setupWrap" id="setupWrap" style="display:none">
        <p class="lab" dir="auto">כבר כתוב בשבילכם - לא צריך להעתיק</p>
        <pre class="setupCode" id="setupCode">&mdash;</pre>
      </div>

      <div class="levelTag" id="levelTag">E &middot; 1 / 1</div>
      <div class="outbox" id="outbox">
        <p class="lab" dir="auto">פלט צפוי</p>
        <pre class="outtext" id="outtext">&mdash;</pre>
      </div>

      <div class="edwrap">
        <div class="gutter" id="gutter">1</div>
        <div class="codewrap">
          <pre class="hl" id="hl"></pre>
          <textarea id="code" spellcheck="false" autocomplete="off" autocapitalize="off"></textarea>
        </div>
      </div>

      <div class="row">
        <button class="run" id="runBtn">&#9654; RUN</button>
        <button class="hint" id="hintBtn">&#128161; HINT</button>
        <button class="solve" id="solveBtn">&#128273; SOLUTION</button>
        <button class="skip" id="skipBtn">&#8594; SKIP <span class="btnkbd">Ctrl+Shift+S</span></button>
        <button class="run" id="nextBtn" style="display:none">&#10004; NEXT &rarr; <span class="btnkbd">Ctrl+Shift+S</span></button>
        <button class="run" id="tryagainBtn" style="display:none">&#10226; TRY AGAIN <span class="btnkbd">Ctrl+Shift+S</span></button>
        <span class="kbd"><b>Ctrl</b> + <b>Enter</b> runs it &middot; <b>Ctrl</b> + <b>Shift</b> + <b>S</b> skips</span>
      </div>

      <div class="hintbox" id="hintbox" dir="auto"></div>
      <div class="solvebox" id="solvebox">
        <div class="solvehead">
          <b style="color:#cbb8ff; letter-spacing:.05em">SOLUTION</b>
          <button class="copyBtn" id="copyBtn" title="copy the solution" type="button">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <rect x="9" y="9" width="12" height="12" rx="2"/>
              <path d="M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1"/>
            </svg>
            <span id="copyLabel">copy</span>
          </button>
        </div>
        <pre id="solveCode">&mdash;</pre>
      </div>

      <div class="res" id="res"></div>
    </div>
  </div>

  <footer>
    Practice version &mdash; runs Python in your browser, nothing is sent anywhere.
    <a href="../../index.html#simulators">back to the simulators</a>
  </footer>
</div>

<div class="levelModal" id="levelModal">
  <div class="levelModalCard">
    <button class="lmClose" id="lmCloseBtn" aria-label="close" type="button">&times;</button>
    <div class="lmIcon" id="lmIcon">&#127942;</div>
    <h3 id="lmTitle">Level complete!</h3>
    <p id="lmText">You solved every question in this level.</p>
    <div class="lmRow">
      <button class="lmBtn lmRestart" id="lmRestartBtn" type="button">&#8635; Restart This Level</button>
      <button class="lmBtn lmNext" id="lmNextBtn" type="button">Next Level &rarr;</button>
    </div>
  </div>
</div>

<div class="solvedModal" id="solvedModal">
  <div class="solvedModalCard">
    <div class="svIcon">&#9989;</div>
    <h3>Correct!</h3>
    <p id="svText">0/0 solved in EASY</p>
    <button class="svBtn" id="svContinueBtn" type="button">Continue &rarr;</button>
    <div class="svHint">press <b>Enter</b> to continue</div>
  </div>
</div>

<div class="statsModal" id="statsModal">
  <div class="statsModalCard">
    <div class="lmIcon">&#127937;</div>
    <h3>That's every level</h3>
    <p>Here's how the run went.</p>
    <div class="statsGrid" id="statsGrid"></div>
    <button class="statsRestart" id="statsRestartBtn" type="button">&#8635; Play Again</button>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/pyodide/v0.28.3/full/pyodide.js"></script>
<script>
const $ = id => document.getElementById(id);
const LEVELS = %(levels)s;
const BANK = %(bank)s;                    // level -> [ {id,title,topic,task,starter,...,retry[]}, ... ]
const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v0.28.3/full/';
const RUNNER_PY = %(runner_py)s;

let pyodide = null, judgeChallenge = null;

function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}

/* reveal text one character at a time, left to right - the expected-output
   panel is easy to miss otherwise. Multi-line safe (a plain interval, not a
   CSS steps() trick, so newlines like safe_divide's two print() lines work). */
let _typeTimer = null;
function typeOut(el, text){
  clearInterval(_typeTimer);
  el.textContent = '';
  const chars = Array.from(String(text));
  if(!chars.length) return;
  const per = Math.max(10, Math.min(35, 700 / chars.length));
  let i = 0;
  _typeTimer = setInterval(() => {
    el.textContent += chars[i];
    i++;
    if(i >= chars.length) clearInterval(_typeTimer);
  }, per);
}

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
  pickLevel(LEVELS[0]);
};
bootPython();

/* ---------------- python syntax colours ---------------- */
const KW = /^(for|in|if|elif|else|while|print|return|def|not|and|or|is|True|False|None|break|continue|pass|del|try|except|raise)$/;
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

/* ---------------- level + question picking ---------------- */
/* Questions are FIXED, not random: each level always presents its
   questions in the same order (curIndex walks the pool 0, 1, 2, ...).
   'retry' is the only exception - it only ever fires from tryAgain(). */
let curLevel = LEVELS[0], curIndex = 0, curItem = null, curVariant = null,
    lastRetryText = '', solved = false;
let score = 0;
let skippedCount = 0;        // SKIP clicked on an unsolved question
let wrongAttempts = 0;       // RUN judged as failing (ran, but did not solve it)
let solvedIds = {};          // level -> Set of question ids solved at least once this session

function drawLevels(){
  $('levels').innerHTML = LEVELS.map(lv => {
    const pool = BANK[lv] || [];
    const done = solvedIds[lv] || new Set();
    const doneCount = pool.filter(it => done.has(it.id)).length;
    const progress = pool.length ? (' &middot; ' + doneCount + '/' + pool.length + ' solved') : '';
    return '<div class="lvl' + (lv === curLevel ? ' on ' + lv : '') + '" data-lvl="' + lv + '">' +
      lv + '<span class="n">' + pool.length + ' question' +
      (pool.length === 1 ? '' : 's') + progress + '</span>' +
    '</div>';
  }).join('');
  document.querySelectorAll('.lvl').forEach(el => {
    el.onclick = () => pickLevel(el.dataset.lvl);
  });
}

function pickLevel(lv){
  curLevel = lv;
  curIndex = 0;
  drawLevels();
  openItemAtIndex();
}

/* the plain {task, starter, ...} shape of a question as it is written in
   questions.py - what is shown by default, and again on every SKIP/NEXT. */
function baseShape(item){
  return {
    task: item.task, starter: item.starter, expect: item.expect,
    tests: item.tests, require: item.require, forbid: item.forbid,
    hint: item.hint, solution: item.solution,
    expected_output: item.expected_output, setup: item.setup || '',
  };
}

/* open curIndex's question in curLevel's pool, always its base shape -
   never a retry variant. Used on level switch, SKIP and NEXT. */
function openItemAtIndex(){
  const pool = BANK[curLevel] || [];
  if(!pool.length) return;
  curItem = pool[curIndex];
  curVariant = baseShape(curItem);
  lastRetryText = '';
  openQuestion();
}

function nextItem(){
  const pool = BANK[curLevel] || [];
  if(!pool.length) return;
  curIndex = (curIndex + 1) %% pool.length;
  openItemAtIndex();
}

/* the ONLY place a question's text is allowed to change: TRY AGAIN, after
   SOLUTION was already revealed. If the question has a 'retry' list, pick
   one of its alternates (avoiding an immediate repeat); otherwise there is
   nothing to swap, so just reset back to the original starter/task. */
function pickRetry(){
  const pool = curItem.retry || [];
  if(!pool.length){
    curVariant = baseShape(curItem);
    lastRetryText = '';
    return;
  }
  let tries = 0, v;
  do {
    v = pool[Math.floor(Math.random() * pool.length)];
    tries++;
  } while (pool.length > 1 && v.task === lastRetryText && tries < 8);
  curVariant = v;
  lastRetryText = v.task;
}

const LEVEL_LETTER = {easy: 'E', medium: 'M', expert: 'X'};

function openQuestion(){
  const pool = BANK[curLevel] || [];
  $('pill').className = 'pill ' + curLevel;
  $('pill').textContent = curLevel;
  $('qtitle').textContent = curItem.title;
  $('qtopic').textContent = curItem.topic;
  $('levelTag').className = 'levelTag ' + curLevel;
  $('levelTag').textContent = (LEVEL_LETTER[curLevel] || '?') + ' · ' + (curIndex + 1) + ' / ' + pool.length;
  $('outbox').className = 'outbox ' + curLevel;
  $('task').textContent = curVariant.task;
  if(curVariant.setup && curVariant.setup.trim()){
    $('setupWrap').style.display = '';
    $('setupCode').innerHTML = highlight(curVariant.setup.replace(/\s+$/, ''));
  } else {
    $('setupWrap').style.display = 'none';
  }
  typeOut($('outtext'), curVariant.expected_output || '—');
  $('code').value = curVariant.starter;
  paintEditor();
  $('res').className = 'res';
  $('hintbox').className = 'hintbox';
  $('solvebox').className = 'solvebox';
  solved = false;
  $('runBtn').disabled = false;
  $('runBtn').textContent = '▶ RUN';
  $('hintBtn').disabled = false;
  $('code').disabled = false;
  showSkipMode();
  focusEditorAtEnd();
}

/* start every question with the cursor already in the editor, right after
   the last character of the starter code - so the student can just start
   typing, no click needed. setTimeout(0) because a just-shown/just-focused
   modal button may still hold focus in the same tick otherwise. */
function focusEditorAtEnd(){
  setTimeout(() => {
    const el = $('code');
    el.focus();
    const end = el.value.length;
    if(el.setSelectionRange) el.setSelectionRange(end, end);
  }, 0);
}

/* ---------------- skip / next / try again button state ---------------- */
/* Three states, exactly one visible at a time:
     SKIP       - the default: has not been solved, has not seen the answer.
                  "I don't want to solve this one" - move on.
     NEXT       - shown only after a CORRECT run. RUN is disabled from that
                  point on (running it again cannot change the score), and
                  NEXT is the deliberate "on to the next one" action.
     TRY AGAIN  - shown after the SOLUTION was revealed - have another go,
                  on a fresh variant, now that the answer is known. */
function showSkipMode(){
  $('skipBtn').style.display = '';
  $('nextBtn').style.display = 'none';
  $('tryagainBtn').style.display = 'none';
}
function showNextMode(){
  $('skipBtn').style.display = 'none';
  $('nextBtn').style.display = '';
  $('tryagainBtn').style.display = 'none';
}
function showTryAgainMode(){
  $('skipBtn').style.display = 'none';
  $('nextBtn').style.display = 'none';
  $('tryagainBtn').style.display = '';
}

/* true once curIndex is sitting on the last question of the current level -
   moving past it (by any route: SKIP, NEXT, or a correct run) means the
   level is over, so the caller shows the end-of-level choice instead of
   silently wrapping back around to question 1. */
function atLastQuestion(){
  const pool = BANK[curLevel] || [];
  return pool.length > 0 && curIndex === pool.length - 1;
}

function skip(){
  skippedCount++;
  if(atLastQuestion()) endOfLevelReached();
  else nextItem();
}

/* the "move on" action after a CORRECT run - used by the inline NEXT
   button and by the solved-popup's Continue button. Never counts as a
   skip: the question was solved, not skipped. */
function advanceAfterSolve(){
  if(atLastQuestion()) endOfLevelReached();
  else nextItem();
}

function tryAgain(){
  pickRetry();
  openQuestion();
}

/* ---------------- judging ---------------- */
function testTable(rows){
  if(!rows || !rows.length) return '';
  return '<table class="tt"><thead><tr><th></th><th>we called</th><th>expected</th><th>got</th></tr></thead><tbody>' +
    rows.map(r => '<tr class="' + (r.ok ? 'y' : 'n') + '">' +
      '<td class="m">' + (r.ok ? '✔' : '✖') + '</td>' +
      '<td class="call">' + esc(r.call) + '</td>' +
      '<td class="want">' + esc(r.want) + '</td>' +
      '<td class="gotv">' + esc(r.error || r.got) + '</td></tr>').join('') +
    '</tbody></table>';
}

function run(){
  if(solved) return;                    // already scored - RUN is disabled, but be safe
  const code = $('code').value;
  if(!code.trim()) return;
  $('runBtn').disabled = true; $('runBtn').textContent = '⏳ RUNNING…';

  const payload = JSON.stringify({
    setup: curVariant.setup || '', task: curVariant.task, starter: curVariant.starter,
    expect: curVariant.expect, tests: curVariant.tests, prints: '',
    require: curVariant.require, forbid: curVariant.forbid,
  });
  let r;
  try{ r = JSON.parse(judgeChallenge(payload, code)); }
  catch(e){ r = {passed:false, output:'', reason:'could not run that: ' + e, tests:[]}; }
  $('runBtn').textContent = '▶ RUN';

  const box = $('res');
  box.className = 'res show ' + (r.passed ? 'pass' : 'fail');
  if(r.passed){
    solved = true;
    score++;
    $('score').textContent = score;
    $('score').classList.remove('bump'); void $('score').offsetWidth; $('score').classList.add('bump');
    solvedIds[curLevel] = solvedIds[curLevel] || new Set();
    solvedIds[curLevel].add(curItem.id);
    drawLevels();
    box.innerHTML = '<h4>✔ IT ANSWERS</h4>' + testTable(r.tests);
    $('runBtn').disabled = true;         // scored once - re-running cannot change that
    showNextMode();                      // the inline NEXT button stays as a mouse fallback
    announceSolved();                    // the keyboard-first popup - this is the main path
  } else {
    wrongAttempts++;
    $('runBtn').disabled = false;
    box.innerHTML = '<h4>✖ NOT YET</h4><pre>' + esc(r.reason || '') + '</pre>' + testTable(r.tests);
    $('stage').classList.add('shake');
    setTimeout(() => $('stage').classList.remove('shake'), 420);
  }
}

function useHint(){
  $('hintbox').className = 'hintbox show';
  $('hintbox').textContent = '💡 ' + curVariant.hint;
}

/* seeing the solution ends the attempt: RUN, HINT and the editor itself
   are locked, and TRY AGAIN (a fresh go, per pickRetry()) is the only
   thing left to click - openQuestion() unlocks all three again next time
   a question opens. */
function showSolution(){
  $('solvebox').className = 'solvebox show';
  $('solveCode').innerHTML = highlight(curVariant.solution.replace(/\s+$/,''));
  $('copyBtn').classList.remove('done');
  $('copyLabel').textContent = 'copy';
  showTryAgainMode();
  $('runBtn').disabled = true;
  $('hintBtn').disabled = true;
  $('code').disabled = true;
}

function copySolution(){
  const text = curVariant.solution.replace(/\s+$/, '') + '\n';
  const done = () => {
    $('copyBtn').classList.add('done');
    $('copyLabel').textContent = 'copied!';
    clearTimeout(copySolution._t);
    copySolution._t = setTimeout(() => {
      $('copyBtn').classList.remove('done');
      $('copyLabel').textContent = 'copy';
    }, 1600);
  };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
  } else {
    fallbackCopy(text, done);
  }
}
function fallbackCopy(text, done){
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.select();
  try{ document.execCommand('copy'); done(); }catch(e){}
  document.body.removeChild(ta);
}

/* ---------------- level-complete / stats modals ---------------- */
let levelModalOpen = false;
let solvedModalOpen = false;
let statsModalOpen = false;

/* Decide which popup to show right after a correct run: the small
   "correct - keep going" one, unless this WAS the last question of the
   level, in which case there is no "keep going" - go straight to the
   end-of-level choice (or the final stats, on the last level). Either way
   the main button gets keyboard focus, so pressing Enter again - no mouse -
   moves on. That is the whole point: Ctrl+Enter to run, Enter to continue. */
function announceSolved(){
  if(atLastQuestion()) endOfLevelReached();
  else showSolvedModal();
}

function showSolvedModal(){
  solvedModalOpen = true;
  const pool = BANK[curLevel] || [];
  const done = solvedIds[curLevel] || new Set();
  const doneCount = pool.filter(it => done.has(it.id)).length;
  $('svText').textContent = doneCount + '/' + pool.length + ' solved in ' + curLevel.toUpperCase();
  $('solvedModal').className = 'solvedModal show';
  setTimeout(() => $('svContinueBtn').focus(), 0);
}

function closeSolvedModal(){
  solvedModalOpen = false;
  $('solvedModal').className = 'solvedModal';
}

function continueAfterSolve(){
  closeSolvedModal();
  advanceAfterSolve();
}

/* Reached the last question of the current level - by SKIP or by solving
   it. A level with more levels after it offers Next Level / Restart This
   Level; the last level (EXPERT) instead ends the run and shows the final
   stats screen. */
function endOfLevelReached(){
  const idx = LEVELS.indexOf(curLevel);
  const hasNext = idx >= 0 && idx < LEVELS.length - 1;
  if(hasNext) showLevelModal();
  else showStatsModal();
}

function showLevelModal(){
  levelModalOpen = true;
  const pool = BANK[curLevel] || [];
  const done = solvedIds[curLevel] || new Set();
  const doneCount = pool.filter(it => done.has(it.id)).length;
  $('lmIcon').textContent = '🏆';
  $('lmTitle').textContent = 'End of ' + curLevel.toUpperCase();
  $('lmText').textContent = 'You made it through ' + curLevel.toUpperCase() +
    ' (' + doneCount + '/' + pool.length + ' solved). Ready for more?';
  $('lmNextBtn').style.display = '';
  $('levelModal').className = 'levelModal show';
  setTimeout(() => $('lmNextBtn').focus(), 0);
}

function closeLevelModal(){
  levelModalOpen = false;
  $('levelModal').className = 'levelModal';
}

function goNextLevel(){
  closeLevelModal();
  const idx = LEVELS.indexOf(curLevel);
  if(idx >= 0 && idx < LEVELS.length - 1) pickLevel(LEVELS[idx + 1]);
}

function restartLevel(){
  closeLevelModal();
  solvedIds[curLevel] = new Set();
  curIndex = 0;
  drawLevels();
  openItemAtIndex();
}

/* the final report: every level is done (skipped through, or solved) -
   how many questions were skipped, how many were solved, how many RUNs
   came back wrong, and the average number of tries it took per solved
   question (score + wrongAttempts, over score). */
function showStatsModal(){
  statsModalOpen = true;
  const avg = score ? ((score + wrongAttempts) / score).toFixed(1) : '—';
  const cells = [
    [skippedCount, 'skipped'],
    [score, 'solved'],
    [wrongAttempts, 'wrong tries'],
    [avg, 'avg tries / solved'],
  ];
  $('statsGrid').innerHTML = cells.map(c =>
    '<div class="statCell"><div class="num">' + esc(c[0]) + '</div><div class="lab">' + c[1] + '</div></div>'
  ).join('');
  $('statsModal').className = 'statsModal show';
  setTimeout(() => $('statsRestartBtn').focus(), 0);
}

function closeStatsModal(){
  statsModalOpen = false;
  $('statsModal').className = 'statsModal';
}

function restartEverything(){
  closeStatsModal();
  solvedIds = {};
  score = 0;
  skippedCount = 0;
  wrongAttempts = 0;
  $('score').textContent = score;
  drawLevels();
  pickLevel(LEVELS[0]);
}

document.addEventListener('keydown', e => {
  if(e.key === 'Escape'){
    if(solvedModalOpen) closeSolvedModal();
    if(levelModalOpen) closeLevelModal();
    if(statsModalOpen) closeStatsModal();
    return;
  }
  if((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 's' || e.key === 'S')){
    e.preventDefault();   // plain Ctrl+S opens the browser's save dialog - Shift avoids that
    if($('game').style.display === 'none') return;         // game not started yet
    if(solvedModalOpen || levelModalOpen || statsModalOpen) return;   // a popup is already deciding what's next
    if($('tryagainBtn').style.display !== 'none') tryAgain();
    else if($('nextBtn').style.display !== 'none') advanceAfterSolve();
    else skip();
  }
});

$('runBtn').onclick = run;
$('hintBtn').onclick = useHint;
$('solveBtn').onclick = showSolution;
$('skipBtn').onclick = skip;
$('nextBtn').onclick = advanceAfterSolve;
$('tryagainBtn').onclick = tryAgain;
$('copyBtn').onclick = copySolution;
$('svContinueBtn').onclick = continueAfterSolve;
$('lmNextBtn').onclick = goNextLevel;
$('lmRestartBtn').onclick = restartLevel;
$('lmCloseBtn').onclick = closeLevelModal;
$('statsRestartBtn').onclick = restartEverything;
</script>
</body>
</html>
"""


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build()
