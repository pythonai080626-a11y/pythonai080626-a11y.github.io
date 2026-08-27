# Dictionary Quiz — lesson 16

A 20-question quiz on **dictionaries**, played in the Python console.
Every answer is sent to a small server the moment the student presses Enter, and the
teacher watches the whole class fill up their progress bars live.

Standard library only — **nothing to install**, no flask, no pip.

## The files

| file | what it is |
|---|---|
| `questions.py` | the 20 questions. All of it is dicts: `QUESTIONS[n]['options']['a']`, one `'correct'` letter per question |
| `quiz.py` | the **student** program — asks the name, then the 20 questions, sends each answer |
| `server.py` | the **server** — collects the answers, serves the teacher console |
| `teacher.html` | the teacher console: every student's name + an animated progress bar |
| `scores.json` | written by the server so a restart does not lose the class |

## Running it in class

**1 — the teacher starts the server**

```
cd 99_games\dict
python server.py
```

Open <http://localhost:8000> — that is the console.

**2 — open it to the students with ngrok**

```
ngrok http 8000
```

ngrok prints a line like `https://a1b2-c3d4.ngrok-free.app`. That is the address the
students need. (The quiz already sends the `ngrok-skip-browser-warning` header, so the
free-tier warning page will not get in the way.)

**3 — the students run the quiz**

```
python quiz.py
```

It asks two things:

```
  What is your name? Yarden
  Server address [http://localhost:8000] (Enter = keep): a1b2-c3d4.ngrok-free.app
```

Press Enter to keep the default when everyone is on the same machine, otherwise paste
the ngrok address. To save the typing, the teacher can put the link straight into
`quiz.py`:

```python
SERVER = 'https://a1b2-c3d4.ngrok-free.app'
```

## What the student sees

- a typed-out banner and coloured options — `a)` cyan, `b)` pink, `c)` yellow, `d)` green
- **CORRECT!** in green, or **NOT THIS TIME** in red, which also shows the right answer
  and one line explaining *why*
- a progress bar after every question — green blocks are points, red blocks are misses
- a final score, a percentage, a verdict, and confetti for a perfect 20/20

## What the teacher sees

- one row per student, sorted best first, gold/silver/bronze for the top three
- an animated bar per student: the bright part is the score, the pale part is how far
  they have got, so you can tell "slow" from "struggling" at a glance
- the bar turns red under 40% and amber under 70%
- `question 9/20` while they are working, a gold `finished 🏆` badge when they are done
- class size, how many finished, class average and top score across the top
- the page refreshes itself every 2 seconds. **reset board** clears everything for the
  next group

## Notes

- Running `quiz.py` twice with the same name starts that student over from zero.
- If the server is down the quiz keeps working offline — it says so once, and the
  student still gets their score at the end.
- A different port: `set PORT=9000` before `python server.py`.
