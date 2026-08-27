# Dict Race — the first 20 minutes of lesson 17

Twenty dictionary challenges, one at a time. The student **writes real Python in the browser**, presses
`Ctrl + Enter`, and the code actually runs. Solve it and it disappears — the next one opens
by itself. The whole class watches each other's bars fill up.

Standard library only — **nothing to install**, no flask, no pip.

## The files

| file | what it is |
|---|---|
| `questions.py` | the 20 challenges. All of it is dicts — setup code, task, the values that must come out, the required command, the banned shortcuts, the hint, your answer key |
| `server.py` | judges the attempts, keeps the clock and the scores |
| `runner.py` | runs one attempt in a separate python, console-style — so a bare `prices.values()` still produces an answer |
| `index.html` | what the **students** open — editor, live leaderboard, confetti |
| `teacher.html` | your panel — every score, try an answer, accept an answer, the answer key |
| `scores.json` | written by the server so a restart does not lose the class |

## Running it in class

**1 — start the server**

```
cd 99_games\simulator1
python server.py
```

- your panel: <http://localhost:8000/teacher>
- the game: <http://localhost:8000/>

**2 — open it to the students**

```
ngrok http 8000
```

ngrok prints something like `https://a1b2-c3d4.ngrok-free.app`. **That link is the whole
game** — the students just open it in a browser and type their name. Nothing to download.
(The pages already send the `ngrok-skip-browser-warning` header, so the free-tier
interstitial will not get in the way.)

## The twenty challenges

They ramp: read a dict, look things up, change it, ask it questions, do sums over it,
reshape it, order it, reach inside a nested one — and then the punchline.

| # | name | it lands on | the trap you get to talk about |
|---|---|---|---|
| 1 | The Price List | `.values()` | `prices` alone gives the whole dict |
| 2 | The Name Tags | `.keys()` | the mirror image of challenge 1 |
| 3 | How Many | `len()` | counts the *pairs*, not the marks inside them |
| 4 | Look It Up | `d['key']` | `capitals['japan']` with a small j is a different key — KeyError |
| 5 | The Missing Colour | `.get()` | `pet['color']` raises KeyError and stops everything |
| 6 | New Arrival | `d['new'] = v` | there is no `.add()` — you assign to a key that does not exist yet |
| 7 | Price Change | `d['old'] = v` | a capital letter *adds* a second pair instead of changing the first |
| 8 | The Stock Room | `.items()` | `for k in stock:` only hands over the keys |
| 9 | Is Sushi On It? | `in` | `in` searches the keys — `40 in menu` is False though 40 is right there |
| 10 | Hidden In The Values | `in d.values()` | the other half of 9 — plain `in` never looks at the values |
| 11 | The Whole Bill | `sum(d.values())` | `sum(cart)` tries to add `'milk'` to `'bread'` and crashes |
| 12 | The Cheapest Number | `min(d.values())` | `min(tickets)` gives the smallest *name* — sets up 20 |
| 13 | The Cancelled Guest | `del` / `.pop()` | `pop` hands back what was *removed*, not what is left — `del` just removes, which is all we want |
| 14 | Last One Out | `.popitem()` | takes no key at all — the only way out when you don't know what's in there |
| 15 | Two Baskets | `.update()` / `\|` | `update()` returns `None` — it changes the dict where it stands |
| 16 | The Best Number | `max(d.values())` | gives the *number* — the NAME needs one more thing, and that is 20 |
| 17 | A To Z | `sorted(d)` | sorts the *names*, not the prices |
| 18 | Cheapest First | `sorted(d, key=d.get)` | `key=` is the entire difference — and it comes back in 20 |
| 19 | Deep Inside | `d['a']['b']` | one bracket gets you to the door, the second gets you through it |
| 20 | Who Won? | `max(d, key=d.get)` | `max(scores)` gives **Yarden** — no `key=`, so it compared the *names* |

13 and 15 each have two honest roads (`del` or `pop`, `update` or `|`) and both are accepted.
6, 7, 13 and 15 need two lines, and say so loudly on screen.

12 → 16 → 20 is the thread that matters: *smallest number*, *biggest number*, then the
**name** of the biggest. Only the last one needs `key=`, and by then they should feel why.

Challenge 20 is the one to slow down on. It is the exact moment
[`#topic-max`](https://pythonai080626-a11y.github.io/basics/lessons/17_lesson/17-lesson.html#topic-max)
in the lesson is built on — `key=` stops being syntax and becomes obvious.

## Scoring

|  | within 40 seconds | after 40 seconds |
|---|---|---|
| **on their own** | 100 | 50 |
| **used the hint** | 50 | 25 |

Twenty challenges, so **2000 points** is a perfect run.

The 40-second clock starts the first time that student *opens* that challenge, and it is
kept on the server — refreshing the page does not buy more time. A wrong answer costs
nothing but the clock, so they can keep trying. Solving something twice does not pay twice.

## One at a time

**Players cannot move between challenges.** They see the one they are on; the rest of the
strip is locked. Solve it and it turns green, the stage clears, and the next one opens by
itself after a beat. A latecomer starts at 1 and catches up at their own pace, and somebody
whose browser died comes back to exactly where they were.

There is a **⟲ start over** button on their own screen (and on the finish page). It wipes
that one player's score, hints and clocks and then **asks for a name again** — so the same
laptop can be handed straight to the next person, and whoever types their name next starts
clean at challenge 1. Nobody else on the board is touched. It asks before wiping.

## Saying how many lines it takes

A beginner does not guess that an answer is allowed to be more than one line, and they
really do not guess that the last line has to be the thing you want to look at. So every
challenge states its shape, right above the editor. One-liners say so quietly; the rest get
a purple warning:

> ⚠ **This one is not a one-liner.**
> TWO lines.
> Line 1 takes Omer out.
> Line 2 is just `party` on its own.
> Taking him out does not show you the dict by itself.

That is the `'shape'` field in `questions.py`, with `'lines'` saying how many.

**Every newline in `task`, `shape` and `hint` becomes a line break on screen.** So write one
idea per line and start a new line at each full stop or dash — a long unbroken sentence is
the easiest way to lose a beginner. All twenty are written that way. Challenges
6, 7, 13 and 15 are the ones that need it.

## I don't know

Next to RUN and HINT there is a 🤷 **I don't know** button. A beginner who is stuck on
challenge 4 should not spend the warm-up staring at challenge 4.

It asks first — *"Show the answer for challenge 4? You will get 0 points for this one, and
move on to the next."* Say yes and they get:

- the answer, laid out over as many lines as it takes
- **Worth knowing:** the near-miss for that challenge — the same note you have in your key
- **0 points** banked for it, and a **NEXT CHALLENGE →** button when they have read enough

Nothing auto-advances here. They read at their own pace and click on.

On the strip that challenge turns grey and says **shown** instead of green **+100**, and on
your panel its segment is grey rather than lit — so at a glance you can tell *solved* from
*given up*, and the per-player line counts them: `4 runs · 0 hints · 2 shown`.

## Your panel

- **the class, live** — every student, their score, which challenge they are on, how many
  runs, how many hints. Gold/silver/bronze on the top three. A segment per challenge, with
  the points they won there written inside it; the amber outline is where they are now.
- **try a student's answer** — *"I typed that and it said no!"* Paste it, run it, see exactly
  what it printed and why the checker refused. Nobody's score moves.
- **accept it anyway** — decided they were right? Paste their answer and it becomes a valid
  solution for that challenge, **for everybody, immediately**. No restart.
- **answer key** — all twenty solutions, the hint each one can buy, and the near-miss worth
  talking about once everyone is through.
- **reset the whole board** — clears every score and every accepted answer for the next group.
  (Different from a player's own *start over*, which only resets that one player.)

## Notes

- Coming back with the same name keeps that student's score — a browser crash costs nothing.
- The students' code runs **on your machine**, in a separate short-lived python. The guards
  above cover the accidents, not a determined attacker — this is built for a classroom, so
  do not point it at the open internet and walk away.
- A different port: `set PORT=9000` before `python server.py`.
- Adding a twenty-first challenge is one more entry in `questions.py` — both pages pick it up
  from the server, nothing else to change. Write `'answer'` as the values that have to come
  out, in any readable form; only the words and numbers in it are used.

## The serverless twin

[`../simulator2`](../simulator2/) is the same twenty challenges with no server at all —
Python runs in the player's browser via Pyodide, the order is shuffled every game, and it
is the one linked from the site under **Simulators**. Use this version when you want the
live class board; use that one for homework or a solo run.
