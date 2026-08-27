# Dict Race — solo (serverless)

The same twenty dictionary challenges as [`../simulator1`](../simulator1/), but with
**nothing to run**. Two static files that work straight off GitHub Pages.

| file | what it is |
|---|---|
| `index.html` | the whole game — layout, judging, editor, scoring |
| `questions.js` | the 20 challenges, generated from `../simulator1/questions.py` |

Open it and play. There is no server, no ngrok, no `python server.py`.

## How Python runs with no server

The page loads **Pyodide** — CPython compiled to WebAssembly — from a CDN, and runs the
student's code inside their own browser tab. Same judging rules as the classroom version:
run `setup + code`, evaluate a trailing expression the way the console does, pull the words
and numbers out of whatever came back, compare as an unordered set, then check the command
the exercise is about actually appears.

First load pulls about 10 MB and takes a few seconds; after that the browser has it cached.
The start button stays greyed out until Python is genuinely ready, so nobody types into a
dead editor.

**The Pyodide version is pinned to `v0.28.3` on purpose.** 0.26.x and 0.27.x both fail to
boot in current Chromium with `ExitStatus: Program terminated with exit(1)`, and the older
0.25.1 has no `loadPyodide` at all. If you ever bump it, load the page and confirm the boot
screen reaches **Ready** before shipping it to a class.

## What is different from simulator1

|  | simulator1 (classroom) | simulator2 (solo) |
|---|---|---|
| needs a server | yes, `python server.py` + ngrok | **no** |
| runs the Python | on the teacher's machine | in the player's own tab |
| asks for a name | yes | **no** — press START and go |
| live class board | yes | **no** — there is nothing live to show |
| question order | 1 → 20, fixed | **shuffled every game** |
| teacher panel | yes | no |
| scores survive a refresh | yes, `scores.json` | no — a refresh is a new game |

Everything else is the same: 40 seconds for 100 points, 50 after that, halved if the hint is
used; **🤷 I don't know** shows the answer for 0 points and moves on; the shape note warns
when an answer needs more than one line.

## One extra rule here

`while` is refused, on top of the usual `import` / `open(` / `eval(` / dunder bans. Python
runs on this page's own thread, so an endless loop would freeze the tab with no way back and
lose the game. None of the twenty challenges needs one — `for` over a dict always ends.

## Changing the questions

`questions.py` in `../simulator1/` is the single source of truth. After editing it,
regenerate this copy:

```
cd basics/99_games/simulator1
python -c "import sys,json,io; sys.path.insert(0,'.'); from questions import QUESTIONS; \
out=[dict(QUESTIONS[n], q=n) for n in sorted(QUESTIONS)]; \
io.open('../simulator2/questions.js','w',encoding='utf-8').write('const QUESTIONS = '+json.dumps(out,ensure_ascii=False,indent=2)+';')"
```

`solution`, `hint` and `trap` all ship to the browser here — they have to, because there is
no server to hold them back. A determined student can read them in the page source. That is
the honest trade for having no server at all; it is a warm-up, not an exam.

## Where it is linked from

`basics/index.html` → the **Simulators** section, alongside the two Kahoot quizzes.
