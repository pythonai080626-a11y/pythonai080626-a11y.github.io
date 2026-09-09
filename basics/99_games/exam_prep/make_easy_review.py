# -*- coding: utf-8 -*-
"""
make_easy_review.py  --  build easy.html from draft_easy_questions.py.

REVIEW ONLY. This is not the game - there is no judge, no Pyodide, nothing
interactive. Every 'solution' is executed for real, in plain CPython, and
its actual printed output is captured - so "expected output" on the page is
never guessed, only ever what the code really does. That is the one thing
this script checks: does every draft question's code even run without
crashing. Nothing here is graded against tests/require/forbid the way the
real game questions are - this step comes before any of that.

    python make_easy_review.py
"""

import importlib.util
import io
import contextlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
QSRC = os.path.join(HERE, 'draft_easy_questions.py')
OUT = os.path.join(HERE, 'easy.html')


def load_questions(qsrc):
    spec = importlib.util.spec_from_file_location('draft_questions_' + os.path.basename(qsrc), qsrc)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.QUESTIONS


def run_for_real(items):
    """Execute every solution (with its 'setup' code, if any - given/
    provided code the student would not have to write themselves, e.g. a
    ready-made 'import re' + pattern - run first, in the same namespace,
    the same way the real judge's run_file() prepends q['setup']) and
    capture exactly what it prints. Refuses to build if any of them crash."""
    problems = []
    for q in items:
        full_source = (q.get('setup', '') or '') + q['solution']
        buf = io.StringIO()
        ns = {}
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(full_source, '<%s>' % q['id'], 'exec'), ns)
        except Exception as e:
            problems.append('%s: crashed - %s: %s' % (q['id'], type(e).__name__, e))
            continue
        output = buf.getvalue()
        if not output.strip():
            problems.append('%s: prints nothing' % q['id'])
        q['expected_output'] = output.rstrip('\n')
        q['full_source'] = full_source
    return problems


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def build(qsrc=QSRC, out=OUT, level_label='EASY'):
    items = load_questions(qsrc)
    problems = run_for_real(items)
    if problems:
        print('REFUSING TO BUILD - fix these first:')
        for p in problems:
            print('  -', p)
        raise SystemExit(1)

    cards = []
    for i, q in enumerate(items, start=1):
        cards.append(CARD % {
            'n': i,
            'title': esc(q['title']),
            'topic': esc(q['topic']),
            'task': esc(q['task']),
            'code': esc(q['full_source'].rstrip()),
            'out': esc(q['expected_output']),
        })

    page = TEMPLATE % {
        'level': level_label,
        'count': len(items),
        'cards': '\n'.join(cards),
    }
    io.open(out, 'w', encoding='utf-8', newline='\r\n').write(page)
    print('%s review -> %s  (%d questions, %d bytes)'
          % (level_label.lower(), os.path.relpath(out, HERE), len(items), len(page)))


CARD = """
    <section class="card">
      <div class="head">
        <span class="n">#%(n)s</span>
        <h2>%(title)s</h2>
        <span class="topic">%(topic)s</span>
      </div>
      <p class="task" dir="auto">%(task)s</p>
      <div class="cols">
        <div class="col">
          <div class="lab">python program</div>
          <pre class="code">%(code)s</pre>
        </div>
        <div class="col">
          <div class="lab">expected output</div>
          <pre class="out">%(out)s</pre>
        </div>
      </div>
    </section>
"""

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(level)s Review</title>
<style>
:root{
  --bg:#05060f; --panel:#0d1020; --panel2:#12162b; --line:#232847;
  --ink:#e8ecff; --dim:#8b93bd; --lime:#b8ff3d; --cyan:#22e0ff;
  --mono:ui-monospace,"Cascadia Code","JetBrains Mono",Consolas,"Courier New",monospace;
}
*{box-sizing:border-box}
body{margin:0; background:var(--bg); color:var(--ink); font-family:var(--mono);
  font-size:14px; padding:24px 20px 60px}
.wrap{max-width:980px; margin:0 auto}
header{margin-bottom:22px}
h1{font-size:22px; margin:0 0 6px; letter-spacing:.04em}
header p{color:var(--dim); margin:0; font-size:13px}
.card{background:var(--panel); border:1px solid var(--line); border-radius:14px;
  padding:16px 18px; margin-bottom:16px}
.head{display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:10px}
.n{color:var(--dim); font-size:12px; font-weight:800}
.head h2{margin:0; font-size:16px; color:var(--ink)}
.topic{margin-inline-start:auto; font-size:11px; color:var(--cyan);
  background:rgba(34,224,255,.1); border:1px solid #164a55; border-radius:8px; padding:3px 9px}
.task{white-space:pre-wrap; font-size:14.5px; line-height:1.7; color:#fff;
  background:#0a0d1c; border-inline-start:3px solid var(--lime); border-radius:6px;
  padding:10px 12px; margin:0 0 12px}
.cols{display:grid; grid-template-columns:1fr 1fr; gap:12px}
@media (max-width:720px){ .cols{grid-template-columns:1fr} }
.lab{font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:var(--dim); margin:0 0 5px}
.code,.out{margin:0; background:#070a16; border:1px solid var(--line); border-radius:8px;
  padding:10px 12px; font-size:13px; line-height:1.55; white-space:pre-wrap; word-break:break-word}
.code{color:var(--ink)}
.out{color:var(--lime)}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Exam Rehearsal - %(level)s, draft review (%(count)s questions)</h1>
    <p>Not wired into the game yet - just a fast read-through: Hebrew task, the Python program, and its real output.</p>
  </header>
%(cards)s
</div>
</body>
</html>
"""


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build(QSRC, OUT, 'EASY')
