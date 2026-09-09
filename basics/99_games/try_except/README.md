# Try / Except Quiz — lesson 20

A 15-question multiple-choice quiz on **errors** — `try`, `except`, `else`, `finally` and
`raise` — played in the browser, with **80 seconds on the clock for every question**.

Same engine as `99_games/tuple`: one server, two links — the students open one and play,
the teacher opens the other and watches the whole class live.

Standard library only — **nothing to install**, no flask, no pip.

## The two links

| who | link | what they get |
|---|---|---|
| **students** | `http://localhost:8000/` | type a name, answer 15 questions, watch the class leaderboard |
| **teacher** | `http://localhost:8000/teacher` | every player, the question they are on, the full answer key, and the fix button |

Over ngrok it is the same two paths on the public address: `https://….ngrok-free.app/`
for the class, `https://….ngrok-free.app/teacher` for you.

## Running it in class

```
cd basics\99_games\try_except
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

> Running this **and** the tuple quiz at the same time? Give one of them a different
> port: `set PORT=8001` before starting the second one.

## The files

| file | what it is |
|---|---|
| `questions.py` | the 15 questions, all multiple choice |
| `server.py` | the server, the clock and **the judging** — both pages come from here |
| `index.html` | the student page: name gate, question, countdown, leaderboard |
| `teacher.html` | the teacher panel: the class, the key, and the fix button |
| `answers.html` | a standalone answer key - open it on its own, no server |
| `scores.json` | written by the server so a restart does not lose the class |

## What the student sees

- a name gate, then straight into question 1 — no install, no download
- a **countdown bar** that goes red → amber → pink as the 80 seconds drain
- click an option; the moment they answer, the right one lights green, theirs goes pink,
  and the *why* line explains it
- **⏰ Time is up** if the clock beats them — scored wrong, but the answer and the why are
  still shown
- the class leaderboard down the side, updating every 3 seconds, their own row highlighted
- a final score, a verdict, and confetti for a perfect score
- closing the tab loses nothing: typing the same name again picks up where they left off

## What the teacher sees

**The class tab** — one row per player, best first, medals for the top three:

- a **square for every one of the 15 questions**: green right, pink wrong, amber the one
  they are on *right now*. Hovering a square shows what they answered and how long it took.
- **click any pink square to give that player the point** — for when the wording tripped
  them up and you want it back.
- **start over** per player, wiping just that one player
- how many answered, their average seconds, and how many times they ran the clock out
- across the top: players, finished, class average, top score, class pace
- the panel refreshes itself every **15 seconds**, and the header shows the time it last
  updated. **refresh** pulls it in right now — use that after a fix.

**The questions tab** — all 15 with the right answer marked in green, the *why* line, and
**how the class did on each one** (`14 answered · 43% got it right`), so you can see at a
glance which question to go back over.

## The questions are in Hebrew

This is a beginners' class, so **the question and the *why* line are in Hebrew**. The
python code and the four options stay in English.

Every question is built the same way, and `questions.py` says so at the top:

```
the code, on its own lines
                              <- a blank line
the question, in hebrew, on its own line
```

Never a sentence and a line of code on the same line. Both pages render the question
**one line at a time** with `dir="auto"`, so the code lines sit left-to-right and the
Hebrew lines go right-to-left, in their own font and colour.

## What the 15 questions cover

From lesson 20 and from the topic page `basics/24_try_except/index.html`:

| # | topic | # | topic |
|---|---|---|---|
| 1 | `int(input(...))` on a good number | 9 | `except Exception` first swallows the rest |
| 2 | `10 / 0` → ZeroDivisionError | 10 | `except (ValueError, TypeError) as e` |
| 3 | a missing dict key → KeyError | 11 | when `else` runs |
| 4 | `list.remove` → ValueError | 12 | order with an error: try → except → finally |
| 5 | **`raise`** — you throw it yourself | 13 | order without one: try → else → finally |
| 6 | `'5' + 3` → TypeError | 14 | `try/finally` with no `except` |
| 7 | the program survives, `Goodbye` prints | 15 | catching too deep → a TypeError later |
| 8 | no error → the except block is skipped | | |

Correct answers are spread **a4 · b3 · c4 · d4**, so nobody can pattern-match their way
through it.

## The answer key page

`answers.html` is a standalone page with all 15 questions, all four options each, the
right one marked, and the *why* line. No server needed — just open it. It has a **hide
the answers** toggle so it doubles as a worksheet for the projector, and a **print**
button with a proper print stylesheet. It is generated from `questions.py`, so it can
never disagree with the game.

## Notes

- **The answers are not in the student page.** `/api/join` hands out the questions with
  the right letter stripped, and every answer is judged on the server. Opening devtools
  shows a student nothing they cannot already see.
- **The clock is the server's, not the browser's.** Refreshing the page does not buy more
  time, and an answer that arrives after 80 seconds (plus a couple of seconds for the
  network) is marked wrong even if the letter was right.
- Answering the same question twice does nothing — the first answer stands.
- `reset board` clears everything for the next group.
- Every answer in `questions.py` was produced by **actually running the snippet**, error
  messages included.
