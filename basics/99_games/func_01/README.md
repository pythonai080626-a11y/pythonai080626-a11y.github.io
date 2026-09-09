# Function Lab — lesson 18

Ten challenges on **functions with a door on each side**: values in through
parameters, an answer out through `return`. Played in the browser, on the
teacher's machine, over ngrok.

This is not multiple choice. Every challenge is a real `.py` file the student
edits and runs, and the checker **calls their function** to see whether it
answers correctly.

Standard library only — **nothing to install**, no flask, no pip.

## The files

| file | what it is |
|---|---|
| `questions.py` | the 10 challenges. Everything is a dict, the way lesson 16 taught it |
| `runner.py` | runs one student's file in a separate python, then interviews their function |
| `server.py` | the judge, the clock, the scoreboard. Serves both pages |
| `index.html` | the **student** lab — task, editor, RUN, hint, the live class list |
| `teacher.html` | the **teacher** panel — the board, the answer key, and the override |
| `scores.json` | written by the server so a restart does not lose the class |

## Running it in class

**1 — start the server**

```
cd 99_games\func_01
python server.py
```

- students: <http://localhost:8000>
- your panel: <http://localhost:8000/teacher>

**2 — open it to the room**

```
ngrok http 8000
```

Give the students the `https://....ngrok-free.app` link. Nothing to configure —
the page talks to whatever address it was opened from.

A different port: `set PORT=9000` before `python server.py`.

## The three kinds of challenge

| badge | what they do | example |
|---|---|---|
| **WRITE IT** | the `def` line and the docstring are already in the editor — fill in the body | `triple(number)` |
| **CALL IT** | the function is already in memory. Write the call | `sticker_price(6)` |
| **FIX IT** | a broken file is in the editor. Repair it, do not rewrite it | `scores = scores.sort()` |

The ten, in order:

| # | title | kind | what it teaches |
|---|---|---|---|
| 1 | The Tripler | write | one slot, one `return` |
| 2 | Wake It Up | call | a `def` on its own never runs — the call is what runs it |
| 3 | Base And Height | write | two slots, and the names are part of the deal |
| 4 | Backwards Bill | call | `name=` at the call, so the order stops mattering |
| 5 | Below Zero | write | a default that fills itself, and a real `True` / `False` |
| 6 | It Will Not Even Start | fix | slots without a default have to come first — `SyntaxError` |
| 7 | Tax On Top | write | one required slot, one with a default |
| 8 | Half The Job | fix | it printed, so `None` came back |
| 9 | The Vanishing List | fix | `.sort()` changes in place and returns `None` |
| 10 | How Long Is Each One | write | a loop inside a function, and a whole dict handed back |

**8 → 9 is the pair worth stopping on.** Both files run. Both look like they
work. Neither one hands anything back.

## How an answer is judged

Two steps, and neither one reads their body:

1. **The file has to run.** `setup` + their code, top to bottom.
2. **We call their function ourselves.** Every challenge carries a handful of
   calls with the values they must produce:

   ```python
   'tests': [
       {'call': "is_freezing()",   'is': "True"},
       {'call': "is_freezing(15)", 'is': "False"},
   ]
   ```

   The call runs in *their* namespace; the expected value in an empty one. The
   two are compared as values, not as text.

So **any shape of a right answer passes** — their own variable names, one line
or five, `if/else` or no `else`, a loop or a comprehension. The student sees the
list of calls before they start, and gets a ✔/✖ table of what came back after
every run.

What the comparison *is* fussy about, and why:

| | |
|---|---|
| `True` is not `1` | lesson 18 asks for a real bool, so a bool is demanded where a bool is expected |
| `18` is not `'18'` | `==` says so by itself |
| `250 == 250.0` | fine — and numbers get a tolerance, so `price + price * percent / 100` is never punished for float dust |

`require` only ever asks for the thing being taught — `def`, `return`, a
`total=` at the call. `forbid` only stops the answer being typed out by hand
(printing `42` instead of calling the function). `import`, `eval`, `open` and
friends are switched off, and a loop that never ends is killed after 6 seconds.

## The scoring

|  | within 90s | after 90s |
|---|---|---|
| no hint | 100 | 50 |
| used the hint | 50 | 25 |

1000 points for a perfect run. The clock lives on the **server**, so refreshing
the page does not buy more time. It starts the first time that student opens
that challenge.

**I don't know** shows the answer and the near-miss, banks a 0, and opens the
next one — so nobody sits on a wall for the rest of the hour.

## What the teacher sees

- one row per student: score, which challenge they are on, how many runs, how
  many hints, how many answers they asked for
- a segment per challenge — bright for points, grey for an answer they were
  shown, amber outline for the one they are sitting on right now
- **where they are stuck**: a bar chart of how many students are on each
  challenge. If a bar spikes, stop the room and talk about that one
- the **answer key**: the task, what each one teaches, the calls the checker
  makes, the solution, the hint they can buy, and the near miss
- **try a student's answer** — paste it, run it, nobody is scored
- **accept it anyway** — their answer was fine and the checker disagreed? Paste
  it and it becomes valid for that challenge, for everybody, from that second
  on. It skips every check, so paste exactly what they typed.
- **reset the whole board** — between groups, not during one

The page refreshes itself every 2 seconds.

## Notes

- Nobody can jump around. Each student is locked to their own current challenge
  and the next opens only when they solve it. A latecomer starts at 1.
- **start over** on a student's own screen wipes only that player.
- The editor keeps a draft per challenge, and **back to the starting code** puts
  the original file back without touching the clock or the points.
- Coming back with the same name picks up exactly where they left off.
