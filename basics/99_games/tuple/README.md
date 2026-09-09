# Tuple Quiz — lesson 19

A 20-question quiz on **tuples**, played in the browser, with **80 seconds on the clock
for every question**. Built like `99_games/func_01`: one server, two links — the students
open one and play, the teacher opens the other and watches the whole class live.

Standard library only — **nothing to install**, no flask, no pip.

## The two links

| who | link | what they get |
|---|---|---|
| **students** | `http://localhost:8000/` | type a name, answer 20 questions, watch the class leaderboard |
| **teacher** | `http://localhost:8000/teacher` | every player, the question they are on, the full answer key, and the fix buttons |

Over ngrok it is the same two paths on the public address: `https://….ngrok-free.app/`
for the class, `https://….ngrok-free.app/teacher` for you.

## The files

| file | what it is |
|---|---|
| `questions.py` | the 20 questions — 19 with four options, 1 the student types |
| `server.py` | the server, the clock and **the judging** — both pages come from here |
| `index.html` | the student page: name gate, question, countdown, leaderboard |
| `teacher.html` | the teacher panel: the class, the key, and the fixes |
| `scores.json` | written by the server so a restart does not lose the class |

## Running it in class

```
cd basics\99_games\tuple
python server.py
```

It prints both links. Then, to open it up to the class:

```
ngrok http 8000
```

Read out the `https://….ngrok-free.app` line — that is the students' link. (Both pages
send the `ngrok-skip-browser-warning` header, so the free-tier warning page does not get
in the way.)

Other port: `set PORT=9000`. Other clock: `set SECONDS=120`.

## What the student sees

- a name gate, then straight into question 1 — no install, no download
- a **countdown bar** that goes violet → amber → pink as the 80 seconds drain
- 19 questions where they click an option; the last one they **type**
- the moment they answer: the right option lights green, theirs goes pink, and the
  *why* line explains it
- **⏰ Time is up** if the clock beats them — the question is scored wrong but the answer
  and the why are still shown
- the class leaderboard down the side, updating every 3 seconds, their own row highlighted
- a final score, a verdict, and confetti for a perfect 20
- closing the tab loses nothing: typing the same name again picks up where they left off

## What the teacher sees

**The class tab** — one row per player, best first, medals for the top three:

- a **square for every one of the 20 questions**: green right, pink wrong, amber the one
  they are on *right now*. Hovering a square shows what they answered and how long it took.
- **click any pink square to give that player the point** — for when the wording tripped
  them up and you want it back. This is the "fix" button.
- **start over** per player, wiping just that one player
- how many answered, their average seconds, and how many times they ran the clock out
- across the top: players, finished, class average, top score, class pace
- the panel refreshes itself every **15 seconds**, and the header shows the time it
  last updated. **refresh** pulls it in right now &mdash; use that after a fix.

**The questions tab** — all 20 with the right answer marked in green, the *why* line, and
**how the class did on each one** (`14 answered · 43% got it right`), so you can see at a
glance which question to go back over.

On question 20 — the typed one — there is an **accept** box. Paste another spelling and
it counts for everybody from that moment on.

## The last question is typed, not picked

Question 20 has no options. The student writes python, and the server **evaluates the
value** rather than matching the text, so every honest spelling of the same answer counts:

```
(7,)      7,      ( 7 , )      tuple([7])
```

`(7)` does not, and the feedback says exactly why — *you typed an int, not a tuple*. That
is the whole point of the question.

## Where the questions come from

Straight off the topic page `basics/23_tuples/index.html`:

| # | topic | # | topic |
|---|---|---|---|
| 1 | `t[0] = 99` → TypeError | 11 | `.count(x)` |
| 2 | `(42)` is an int, not a tuple | 12 | `.index(x)` |
| 3 | packing without brackets | 13 | `+` builds a new tuple |
| 4 | unpacking into variables | 14 | `*` repeats the contents |
| 5 | the one-line swap | 15 | `sorted()` returns a **list** |
| 6 | star unpacking → a list | 16 | `.append()` → AttributeError |
| 7 | slicing `t[1:4]` | 17 | which value can be a dict key |
| 8 | reversing `t[::-1]` | 18 | the list → edit → tuple workaround |
| 9 | `len` · `min` · `max` · `sum` | 19 | a mutable list **inside** a tuple |
| 10 | `t[-1]` and `not in` | 20 | **typed:** write a one-item tuple |

No `namedtuple` — it is not in this lesson.

## Notes

- **The answers are not in the student page.** `/api/join` hands out the questions with
  the right letter stripped, and every answer is judged on the server. Opening devtools
  shows a student nothing they cannot already see.
- **The clock is the server's, not the browser's.** Refreshing the page does not buy more
  time, and an answer that arrives after 80 seconds (plus a couple of seconds for the
  network) is marked wrong even if the letter was right.
- Answering the same question twice does nothing — the first answer stands.
- `reset board` clears everything, including the accepted answers, for the next group.
