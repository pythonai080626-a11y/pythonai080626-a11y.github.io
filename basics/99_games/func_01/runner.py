# -*- coding: utf-8 -*-
"""
runner.py  --  runs one student's file and then interviews their function.

The server hands us  {"setup":..., "code":..., "tests":[...]}  on stdin and
gets JSON back. It is started as a separate python (`python -I runner.py`) so
a student's endless loop dies with a timeout instead of taking the class down.

Two things happen here, in this order:

1. THE FILE RUNS.
   setup + their code, top to bottom, with stdout captured. If the last line is
   a bare expression it gets evaluated the way the console does, so a student
   who writes  triple(7)  with no print still produces something visible.

2. THE FUNCTION IS INTERVIEWED.
   Every test is a call we make ourselves, in the namespace their file left
   behind:
        {"call": "triple(7)", "is": "21"}
   The call runs in THEIR namespace, the expected value in an empty one, and
   the two are compared as values - not as text.

That second step is the whole idea of this game. We never look at the shape of
their body. One line or five, if/else or no else, their own variable names, a
comprehension instead of a loop: if the right values come back out of the right
slots, it is right.

What the comparison is fussy about, and why:
    True is not 1     -> lesson 18 asks for a real bool, so a bool is demanded
                         when a bool is expected
    18 is not '18'    -> == says so by itself
    250 == 250.0      -> fine, and numbers are compared with a tolerance so
                         price + price * percent / 100 is never punished for
                         float dust
    [1,2] is not (1,2) -> == says so by itself
"""

import ast
import contextlib
import io
import json
import sys

MAX_SHOW = 300              # a repr longer than this gets cut on their screen


def short(text):
    text = str(text)
    return text if len(text) <= MAX_SHOW else text[:MAX_SHOW] + ' ...'


def same(got, want):
    """Is this the answer, whatever road it came down?"""
    if isinstance(want, bool):                     # True is not 1 here
        return isinstance(got, bool) and got == want
    if isinstance(got, bool) != isinstance(want, bool):
        return False
    if isinstance(want, (int, float)) and isinstance(got, (int, float)):
        return abs(got - want) <= 1e-9 * max(1.0, abs(want))
    try:
        return got == want
    except Exception:
        return False


def run_file(source, out):
    """Run setup + their code. Returns the namespace it left behind, or None."""
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        out['error'] = 'SyntaxError: %s   (line %s)' % (e.msg, e.lineno)
        return None

    body = list(tree.body)
    tail = None
    if body and isinstance(body[-1], ast.Expr):    # a console-style last line
        tail = body.pop()

    buf = io.StringIO()
    space = {'__name__': '__main__'}
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(ast.Module(body=body, type_ignores=[]), '<student>', 'exec'), space)
            if tail is not None:
                value = eval(compile(ast.Expression(tail.value), '<student>', 'eval'), space)
                if value is not None:              # print(...) hands back None
                    out['value'] = repr(value)
    except Exception as e:
        out['stdout'] = buf.getvalue()
        out['error'] = '%s: %s' % (type(e).__name__, e)
        return None
    out['stdout'] = buf.getvalue()
    return space


def interview(space, tests, out):
    """Call their function ourselves, once per test, and write down what came back."""
    for test in tests:
        call = test.get('call', '')
        wanted = test.get('is', '')
        row = {'call': call, 'want': wanted, 'got': '', 'ok': False, 'error': ''}
        try:
            want = eval(wanted, {'__builtins__': __builtins__}, {})
        except Exception as e:                     # a broken answer key - say so
            row['error'] = 'bad expected value in questions.py: %s' % e
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


def main():
    try:
        # read as bytes: the file may hold hebrew, and the console codepage
        # on windows is not utf-8
        payload = json.loads(sys.stdin.buffer.read().decode('utf-8') or '{}')
    except Exception as e:
        print(json.dumps({'error': 'bad payload: %s' % e, 'tests': []}))
        return

    out = {'stdout': '', 'value': '', 'error': '', 'tests': []}
    source = (payload.get('setup') or '') + '\n' + (payload.get('code') or '') + '\n'

    space = run_file(source, out)
    if space is not None:
        interview(space, payload.get('tests') or [], out)

    print(json.dumps(out))


if __name__ == '__main__':
    main()
