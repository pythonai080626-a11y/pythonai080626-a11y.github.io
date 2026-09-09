# -*- coding: utf-8 -*-
"""
make_solo.py  --  turn a quiz's questions.py into a STANDALONE solo.html.

The quizzes in here normally need `python server.py` running: the questions,
the clock and the judging all live on the server so a class can play together
and the teacher can watch. That is right for a lesson, and useless for a
student who just wants to practise from the main site.

So this builds a second front door for each one: a single HTML file with the
questions baked in, judged in the browser, no server and no install. Same
questions, same 'why' lines, same 80-second clock - minus the leaderboard and
the teacher panel, which is the part that needs a server.

    python make_solo.py                 rebuild all of them
    python make_solo.py tuple           rebuild one

Re-run it whenever a questions.py changes, or solo.html will drift.
"""

import ast
import html
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LETTERS = ['a', 'b', 'c', 'd']

# folder -> how the page introduces itself
GAMES = {
    'dict': {
        'title': 'Dictionary Quiz',
        'lesson': 'lesson 16',
        'blurb': 'Twenty questions on <b>dictionaries</b> &mdash; keys, values, '
                 '<code>.get()</code>, and the crashes in between.',
        'ink': '#eafff3', 'dim': '#8fc9a8',
        'bg1': '#071a12', 'bg2': '#0b2a1c', 'panel': '#0f2e20', 'panel2': '#143a29',
        'line': '#1e5c3c', 'accent': '#22c55e', 'deep': '#0b2418',
        'glow1': '#10502f', 'glow2': '#0d4d55', 'head': '#103d28,#0d3348',
    },
    'tuple': {
        'title': 'Tuple Quiz',
        'lesson': 'lesson 19',
        'blurb': 'Twenty questions on <b>tuples</b> &mdash; the comma that makes one, '
                 'slicing, and the lock that will not open.',
        'ink': '#f5edff', 'dim': '#b49bd4',
        'bg1': '#0b0614', 'bg2': '#160d26', 'panel': '#160d26', 'panel2': '#1d1233',
        'line': '#3a2260', 'accent': '#a855f7', 'deep': '#0a0512',
        'glow1': '#46208a', 'glow2': '#7c3f10', 'head': '#3b1d6e,#5b2f18',
    },
    'try_except': {
        'title': 'Try / Except Quiz',
        'lesson': 'lesson 20',
        'blurb': 'Fifteen questions on <b>errors</b> &mdash; <code>try</code>, '
                 '<code>except</code>, <code>else</code>, <code>finally</code> and '
                 '<code>raise</code>.',
        'ink': '#fff0ec', 'dim': '#e0a396',
        'bg1': '#120708', 'bg2': '#24100f', 'panel': '#24100f', 'panel2': '#2e1614',
        'line': '#6b2b28', 'accent': '#f87171', 'deep': '#170908',
        'glow1': '#7f1d1d', 'glow2': '#b45309', 'head': '#7f1d1d,#7c3f10',
    },
}


def load_questions(folder):
    path = os.path.join(HERE, folder, 'questions.py')
    spec = importlib.util.spec_from_file_location('q_' + folder, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.QUESTIONS


def accepted_spellings(item):
    """Every honest way of typing the answer to a 'type' question.

    The server evaluates what the student typed; a browser cannot, so we work
    the list out here instead - and CHECK each one really does evaluate to the
    expected value before letting it through.
    """
    want = item['answer']
    candidates = [repr(want)]
    if isinstance(want, tuple):
        inner = ', '.join(repr(v) for v in want)
        candidates += [
            '(%s,)' % inner if len(want) == 1 else '(%s)' % inner,
            '%s,' % inner,
            '( %s , )' % inner if len(want) == 1 else '( %s )' % inner,
            'tuple([%s])' % inner,
            'tuple((%s,))' % inner if len(want) == 1 else 'tuple((%s))' % inner,
        ]
    ok = []
    for text in candidates:
        try:
            value = ast.literal_eval(text)
        except Exception:
            squashed = text.replace(' ', '')
            if squashed.startswith('tuple(') and squashed.endswith(')'):
                try:
                    value = tuple(ast.literal_eval(text[text.index('(') + 1:text.rindex(')')]))
                except Exception:
                    continue
            else:
                continue
        if value == want and type(value) is type(want):
            flat = ''.join(text.split())
            if flat not in ok:
                ok.append(flat)
    return ok


def build(folder):
    cfg = GAMES[folder]
    Q = load_questions(folder)

    payload = []
    for n in sorted(Q):
        item = Q[n]
        row = {'q': n, 'kind': item.get('kind', 'choice'),
               'text': item['q'], 'why': item['why']}
        if row['kind'] == 'type':
            row['expect'] = item['expect']
            row['accept'] = accepted_spellings(item)
            if not row['accept']:
                raise SystemExit('q%d: could not work out an accepted spelling' % n)
        else:
            row['options'] = dict(item['options'])
            row['correct'] = item['correct']
        payload.append(row)

    page = TEMPLATE % {
        'title': html.escape(cfg['title']),
        'lesson': cfg['lesson'],
        'blurb': cfg['blurb'],
        'total': len(payload),
        'questions': json.dumps(payload, ensure_ascii=False, indent=1),
        'ink': cfg['ink'], 'dim': cfg['dim'],
        'bg1': cfg['bg1'], 'bg2': cfg['bg2'], 'panel': cfg['panel'],
        'panel2': cfg['panel2'], 'line': cfg['line'], 'accent': cfg['accent'],
        'deep': cfg['deep'], 'glow1': cfg['glow1'], 'glow2': cfg['glow2'],
        'head': cfg['head'],
    }
    out = os.path.join(HERE, folder, 'solo.html')
    io.open(out, 'w', encoding='utf-8', newline='\r\n').write(page)
    typed = sum(1 for r in payload if r['kind'] == 'type')
    print('%-12s -> %s  (%d questions, %d typed, %d bytes)'
          % (folder, os.path.relpath(out, HERE), len(payload), typed, len(page)))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<style>
:root{
  --bg1:%(bg1)s; --bg2:%(bg2)s; --panel:%(panel)s; --panel2:%(panel2)s;
  --line:%(line)s; --ink:%(ink)s; --dim:%(dim)s; --accent:%(accent)s; --deep:%(deep)s;
  --lime:#b8ff3d; --pink:#ff3ea5; --amber:#ffcc3d;
  --mono:ui-monospace,"Cascadia Code","JetBrains Mono",Consolas,"Courier New",monospace;
}
*{box-sizing:border-box}
body{
  margin:0; color:var(--ink); font-family:"Trebuchet MS","Segoe UI",sans-serif;
  background:
    radial-gradient(circle at 12%% 8%%, %(glow1)s 0%%, transparent 42%%),
    radial-gradient(circle at 88%% 10%%, %(glow2)s 0%%, transparent 40%%),
    linear-gradient(160deg,var(--bg1),var(--bg2));
  min-height:100vh; line-height:1.6;
}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes pop{0%%{transform:scale(.97)}55%%{transform:scale(1.03)}100%%{transform:scale(1)}}
@keyframes pulse{0%%,100%%{opacity:1}50%%{opacity:.3}}

.wrap{max-width:800px; margin:0 auto; padding:24px 18px 70px}
.card{
  background:var(--panel); border:1px solid var(--line); border-radius:18px;
  padding:24px 26px; animation:rise .45s ease both; margin-bottom:16px;
}
.top{
  background:linear-gradient(135deg,%(head)s 90%%);
  border:1px solid var(--line); border-radius:18px; padding:20px 24px; margin-bottom:18px;
  display:flex; flex-wrap:wrap; gap:12px; align-items:center; justify-content:space-between;
  box-shadow:0 16px 36px rgba(0,0,0,.4); animation:rise .5s ease both;
}
h1{margin:0; font-size:1.45rem}
h1 small{display:block; font-size:.68rem; font-weight:400; color:var(--dim);
  letter-spacing:.2em; text-transform:uppercase; margin-top:5px}
.score{text-align:right}
.score b{display:block; font-family:var(--mono); font-size:1.7rem; color:var(--lime); line-height:1}
.score span{font-size:.64rem; letter-spacing:.16em; color:var(--dim); text-transform:uppercase}

.btn{
  border:1px solid var(--line); background:var(--panel2); color:var(--ink); cursor:pointer;
  border-radius:12px; padding:13px 24px; font-weight:800; font-size:.92rem;
  font-family:inherit; transition:.18s;
}
.btn:hover:not(:disabled){transform:translateY(-2px); border-color:var(--accent)}
.btn:disabled{opacity:.45; cursor:default; transform:none}
.btn.go{background:var(--accent); border-color:var(--accent); color:#0b0b0b}
.btn.next{background:linear-gradient(135deg,#3f6212,#84cc16); border-color:var(--lime); color:#0b1400}

/* ---------- start ---------- */
.intro p{color:var(--dim); margin:0 0 18px}
.intro code{background:var(--panel2); padding:2px 7px; border-radius:6px; color:var(--accent)}
.optrow{display:flex; align-items:center; gap:10px; margin-bottom:20px; color:var(--dim); font-size:.9rem}
.optrow input{width:17px; height:17px; accent-color:var(--accent); cursor:pointer}
.optrow label{cursor:pointer}

/* ---------- progress + clock ---------- */
.strip{display:flex; flex-wrap:wrap; gap:6px; margin-bottom:16px}
.pip{
  width:28px; height:28px; border-radius:8px; display:flex; align-items:center;
  justify-content:center; font-size:.72rem; font-weight:800; font-family:var(--mono);
  background:var(--deep); border:1px solid var(--line); color:var(--dim);
}
.pip.now{border-color:var(--amber); color:var(--amber)}
.pip.ok{background:rgba(184,255,61,.15); border-color:var(--lime); color:var(--lime)}
.pip.no{background:rgba(255,62,165,.13); border-color:var(--pink); color:var(--pink)}
.timer{margin-bottom:18px}
.trow{display:flex; justify-content:space-between; font-size:.7rem; letter-spacing:.16em;
  text-transform:uppercase; color:var(--dim); margin-bottom:6px}
.tval{font-family:var(--mono); font-weight:800; color:var(--lime)}
.tval.mid{color:var(--amber)} .tval.low{color:var(--pink); animation:pulse 1s infinite}
.track{height:8px; border-radius:999px; background:var(--deep); border:1px solid var(--line); overflow:hidden}
.fill{height:100%%; width:100%%; background:linear-gradient(90deg,var(--accent),var(--lime));
  transition:width .3s linear}
.fill.mid{background:linear-gradient(90deg,#b45309,var(--amber))}
.fill.low{background:linear-gradient(90deg,#9f1239,var(--pink))}

/* ---------- the question ---------- */
.qhead{font-size:.74rem; color:var(--dim); letter-spacing:.12em; margin:0 0 12px}
.qhead b{color:var(--ink); font-size:.95rem}
.qtext{
  background:var(--deep); border:1px solid var(--line); border-left:3px solid var(--accent);
  border-radius:12px; padding:15px 17px; margin:0 0 18px; overflow-x:auto;
}
.ql{white-space:pre-wrap; word-break:break-word;
  font-family:var(--mono); font-size:14.5px; line-height:1.7; color:#fff}
.ql[dir="rtl"]{font-family:"Trebuchet MS","Segoe UI",sans-serif;
  font-size:16px; color:var(--amber); font-weight:700}

.opts{display:grid; gap:10px}
.opt{
  display:flex; align-items:center; gap:12px; text-align:left; width:100%%;
  background:var(--panel2); border:1px solid var(--line); border-radius:12px;
  padding:12px 15px; color:var(--ink); cursor:pointer; font-size:14.5px;
  font-family:var(--mono); transition:.15s;
}
.opt:hover:not(:disabled){transform:translateX(4px); border-color:var(--accent)}
.opt:disabled{cursor:default}
.opt .ltr{width:26px; height:26px; flex-shrink:0; border-radius:8px; display:flex;
  align-items:center; justify-content:center; font-weight:800; font-size:.8rem;
  background:var(--deep); border:1px solid var(--line)}
.opt .txt{white-space:pre-wrap; word-break:break-word}
.opt.right{border-color:var(--lime); background:rgba(184,255,61,.14); animation:pop .3s}
.opt.right .ltr{border-color:var(--lime); color:var(--lime)}
.opt.wrong{border-color:var(--pink); background:rgba(255,62,165,.14)}
.opt.dimmed{opacity:.42}

.typerow{display:flex; gap:10px; flex-wrap:wrap}
#typeIn{flex:1; min-width:200px; background:var(--deep); border:1px solid var(--line);
  border-radius:12px; padding:13px 16px; color:var(--lime); font-family:var(--mono);
  font-size:16px; outline:none}
#typeIn:focus{border-color:var(--amber)}

/* ---------- verdict ---------- */
.verdict{display:none; margin-top:18px; border-radius:14px; padding:15px 17px;
  border:1px solid var(--line); animation:rise .25s}
.verdict.show{display:block}
.verdict.ok{border-color:var(--lime); background:rgba(184,255,61,.09)}
.verdict.no{border-color:var(--pink); background:rgba(255,62,165,.09)}
.verdict.out{border-color:var(--amber); background:rgba(255,204,61,.09)}
.vtitle{font-size:1rem; font-weight:800; margin:0 0 7px}
.verdict.ok .vtitle{color:var(--lime)} .verdict.no .vtitle{color:var(--pink)}
.verdict.out .vtitle{color:var(--amber)}
.vline{font-size:.9rem; color:var(--dim); margin:4px 0}
.vline b{color:var(--ink); font-family:var(--mono)}
.vwhy{margin-top:9px; padding-top:9px; border-top:1px solid var(--line);
  font-size:.92rem; color:var(--amber)}

/* ---------- the end ---------- */
.done{text-align:center}
.done .big{font-size:3.6rem; font-weight:800; color:var(--lime); line-height:1; font-family:var(--mono)}
.done .of{color:var(--dim); margin:6px 0 14px}
.done .word{font-size:1.02rem; margin-bottom:22px}
.review{text-align:left; margin-top:20px}
.review h3{font-size:.72rem; letter-spacing:.22em; text-transform:uppercase;
  color:var(--dim); margin:0 0 10px}
.rv{background:var(--panel2); border:1px solid var(--line); border-radius:12px;
  padding:12px 15px; margin-bottom:9px}
.rv .n{font-family:var(--mono); font-size:.72rem; color:var(--dim); margin-bottom:6px}
.rv .good{color:var(--lime); font-family:var(--mono); font-size:.86rem}
.rv .w{color:var(--amber); font-size:.86rem; margin-top:5px}
footer{text-align:center; color:var(--dim); font-size:.76rem; margin-top:26px}
footer a{color:var(--accent)}
.dot{position:fixed; width:9px; height:9px; border-radius:2px; z-index:70; pointer-events:none}
</style>
</head>
<body>
<div class="wrap">

  <div class="top">
    <h1>%(title)s<small>%(lesson)s &middot; practise on your own</small></h1>
    <div class="score" id="scoreBox" style="display:none">
      <b id="scoreVal">0</b><span>points</span>
    </div>
  </div>

  <!-- ---------- start ---------- -->
  <div class="card intro" id="intro">
    <p>%(blurb)s</p>
    <p><b>%(total)d questions.</b> You get told straight away whether you were right,
       and <i>why</i>. Nothing is sent anywhere &mdash; this page runs entirely in your
       browser, so you can practise as many times as you like.</p>
    <div class="optrow">
      <input type="checkbox" id="useClock" checked>
      <label for="useClock">with the 80-second clock, like the real game</label>
    </div>
    <button class="btn go" id="startBtn">START &rarr;</button>
  </div>

  <!-- ---------- playing ---------- -->
  <div class="card" id="playing" style="display:none">
    <div class="strip" id="strip"></div>
    <div class="timer" id="timerBox">
      <div class="trow"><span>time left</span><span class="tval" id="tval">80s</span></div>
      <div class="track"><div class="fill" id="fill"></div></div>
    </div>
    <p class="qhead">QUESTION <b id="qnum">1</b> OF <b id="qtot">%(total)d</b></p>
    <div class="qtext" id="qtext"></div>
    <div class="opts" id="opts"></div>
    <div class="typerow" id="typerow" style="display:none">
      <input id="typeIn" spellcheck="false" autocomplete="off" placeholder="type python">
      <button class="btn go" id="sendBtn">ANSWER</button>
    </div>
    <div class="verdict" id="verdict">
      <p class="vtitle" id="vtitle"></p>
      <div id="vbody"></div>
      <div class="vwhy" id="vwhy" dir="auto"></div>
      <button class="btn next" id="nextBtn" style="margin-top:14px">NEXT &rarr;</button>
    </div>
  </div>

  <!-- ---------- finished ---------- -->
  <div class="card done" id="done" style="display:none">
    <div class="big"><span id="finalScore">0</span></div>
    <div class="of">out of %(total)d</div>
    <p class="word" id="finalWord"></p>
    <button class="btn go" id="againBtn">PLAY AGAIN</button>
    <div class="review" id="review"></div>
  </div>

  <footer>
    Practice version &mdash; no server, nothing saved.
    <a href="../../index.html#simulators">back to the simulators</a>
  </footer>
</div>

<script>
const QUESTIONS = %(questions)s;
const TOTAL = QUESTIONS.length;
const SECONDS = 80;

const $ = id => document.getElementById(id);
const esc = t => String(t == null ? '' : t)
  .replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

/* one line at a time, each choosing its own direction: python stays
   left-to-right, a hebrew question line goes right-to-left */
function qLines(text){
  return String(text == null ? '' : text).split('\n')
    .map(line => '<div class="ql" dir="auto">' + (esc(line) || '&nbsp;') + '</div>')
    .join('');
}
const squash = s => String(s == null ? '' : s).replace(/\s+/g, '');

let cur = 0, score = 0, locked = false, clockOn = true, tick = null, deadline = 0;
const given = {};      // index -> what they answered ('' = ran out of time)
const got   = {};      // index -> true / false

function drawStrip(){
  $('strip').innerHTML = QUESTIONS.map((q, i) => {
    let cls = 'pip';
    if(got[i] === true) cls += ' ok';
    else if(got[i] === false) cls += ' no';
    if(i === cur) cls += ' now';
    return '<div class="' + cls + '">' + (i + 1) + '</div>';
  }).join('');
}

function paintClock(){
  if(locked) return;
  const left = Math.max(0, (deadline - Date.now()) / 1000);
  const pct = Math.max(0, Math.min(100, left / SECONDS * 100));
  const tone = pct > 50 ? '' : (pct > 20 ? 'mid' : 'low');
  $('tval').textContent = Math.ceil(left) + 's';
  $('tval').className = 'tval ' + tone;
  $('fill').style.width = pct + '%%';
  $('fill').className = 'fill ' + tone;
  if(left <= 0){ clearInterval(tick); answer(null); }
}

function show(i){
  cur = i; locked = false;
  const q = QUESTIONS[i];
  $('qnum').textContent = i + 1;
  $('qtext').innerHTML = qLines(q.text);
  $('verdict').className = 'verdict';

  if(q.kind === 'type'){
    $('opts').innerHTML = '';
    $('typerow').style.display = 'flex';
    $('typeIn').value = ''; $('typeIn').disabled = false;
    $('sendBtn').disabled = false;
    setTimeout(() => $('typeIn').focus(), 50);
  } else {
    $('typerow').style.display = 'none';
    $('opts').innerHTML = ['a','b','c','d'].map(L =>
      '<button class="opt" data-pick="' + L + '">' +
        '<span class="ltr">' + L + '</span>' +
        '<span class="txt">' + esc(q.options[L]) + '</span>' +
      '</button>').join('');
    document.querySelectorAll('.opt').forEach(b => {
      b.onclick = () => answer(b.dataset.pick);
    });
  }

  drawStrip();
  clearInterval(tick);
  if(clockOn){
    deadline = Date.now() + SECONDS * 1000;
    tick = setInterval(paintClock, 200);
    paintClock();
  }
}

function answer(chosen){
  if(locked) return;
  locked = true;
  clearInterval(tick);
  const q = QUESTIONS[cur];
  const timedOut = (chosen === null);

  let right = false, note = '';
  if(!timedOut){
    if(q.kind === 'type'){
      right = q.accept.indexOf(squash(chosen)) !== -1;
      if(!right) note = 'that is not the same value';
    } else {
      right = (chosen === q.correct);
    }
  }
  given[cur] = timedOut ? '' : chosen;
  got[cur] = right;
  if(right){ score++; }
  $('scoreVal').textContent = score;

  document.querySelectorAll('.opt').forEach(b => {
    b.disabled = true;
    if(b.dataset.pick === q.correct) b.classList.add('right');
    else if(b.dataset.pick === chosen) b.classList.add('wrong');
    else b.classList.add('dimmed');
  });
  $('typeIn').disabled = true; $('sendBtn').disabled = true;

  const rightText = q.kind === 'type'
    ? q.expect
    : q.correct + ')  ' + q.options[q.correct];

  const v = $('verdict');
  let body = '';
  if(timedOut){
    v.className = 'verdict out show';
    $('vtitle').textContent = '⏰  Time is up';
    body += '<p class="vline">The 80 seconds ran out &mdash; no point for this one.</p>';
  } else if(right){
    v.className = 'verdict ok show';
    $('vtitle').textContent = '✅  Correct!  +1';
  } else {
    v.className = 'verdict no show';
    $('vtitle').textContent = '❌  Not this time';
    body += '<p class="vline">you said <b>' + esc(chosen) + '</b></p>';
    if(note) body += '<p class="vline">' + esc(note) + '</p>';
  }
  if(!right) body += '<p class="vline">right answer <b>' + esc(rightText) + '</b></p>';
  $('vbody').innerHTML = body;
  $('vwhy').textContent = q.why;
  $('nextBtn').textContent = (cur >= TOTAL - 1) ? 'SEE MY SCORE →' : 'NEXT →';
  drawStrip();
}

function next(){
  if(cur >= TOTAL - 1) return finish();
  show(cur + 1);
}

function finish(){
  clearInterval(tick);
  $('playing').style.display = 'none';
  $('done').style.display = '';
  $('finalScore').textContent = score;
  const pct = score / TOTAL;
  $('finalWord').textContent =
      pct === 1  ? 'A perfect run. Every single one.'
    : pct >= 0.8 ? 'Strong. Only a couple got away.'
    : pct >= 0.6 ? 'Solid, with a few worth another look.'
    : pct >= 0.4 ? 'Halfway there - read the why lines below.'
    :              'Worth going back over the lesson page, then try again.';

  const missed = QUESTIONS.map((q, i) => [q, i]).filter(p => got[p[1]] === false);
  $('review').innerHTML = missed.length
    ? '<h3>worth another look</h3>' + missed.map(function(p){
        const q = p[0], i = p[1];
        const rightText = q.kind === 'type' ? q.expect : q.correct + ')  ' + q.options[q.correct];
        return '<div class="rv">' +
          '<div class="n">QUESTION ' + (i + 1) +
            (given[i] ? '  &middot;  you said ' + esc(given[i]) : '  &middot;  no answer') + '</div>' +
          '<div class="good">' + esc(rightText) + '</div>' +
          '<div class="w" dir="auto">' + esc(q.why) + '</div>' +
        '</div>';
      }).join('')
    : '';
  if(pct === 1) confetti();
}

function confetti(){
  const colors = ['var(--accent)','#ff3ea5','#b8ff3d','#ffcc3d','#22e0ff'];
  for(let i = 0; i < 60; i++){
    const d = document.createElement('div');
    d.className = 'dot';
    d.style.background = colors[i %% colors.length];
    d.style.left = (45 + Math.random() * 10) + 'vw';
    d.style.top = '40vh';
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

function start(){
  clockOn = $('useClock').checked;
  $('timerBox').style.display = clockOn ? '' : 'none';
  score = 0;
  for(const k in given) delete given[k];
  for(const k in got) delete got[k];
  $('scoreVal').textContent = '0';
  $('scoreBox').style.display = '';
  $('intro').style.display = 'none';
  $('done').style.display = 'none';
  $('playing').style.display = '';
  show(0);
}

$('startBtn').onclick = start;
$('againBtn').onclick = () => { $('done').style.display = 'none'; $('intro').style.display = ''; $('scoreBox').style.display = 'none'; };
$('nextBtn').onclick = next;
$('sendBtn').onclick = () => { if(!locked) answer($('typeIn').value); };
$('typeIn').addEventListener('keydown', e => {
  if(e.key === 'Enter' && !locked) answer($('typeIn').value);
});
$('qtot').textContent = TOTAL;
</script>
</body>
</html>
"""


def main():
    wanted = sys.argv[1:] or sorted(GAMES)
    for folder in wanted:
        if folder not in GAMES:
            raise SystemExit('unknown game: %s (have: %s)' % (folder, ', '.join(sorted(GAMES))))
        build(folder)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
