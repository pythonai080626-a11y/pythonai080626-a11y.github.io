# -*- coding: utf-8 -*-
"""
runner.py  --  runs one student's attempt and reports what came out of it.

The server hands us {"setup": ..., "code": ...} on stdin and gets JSON back.

The point of this file is that a student should NOT have to wrap their answer in
print(...) to be right. We run their code the way the python console does: the
last line, if it is just an expression, gets evaluated and its value is reported
too. So all of these count as an answer:

    prices.values()                  -> value  dict_values([14, 31, 7])
    list(prices.values())            -> value  [14, 31, 7]
    print(prices.values())           -> stdout dict_values([14, 31, 7])
    print(list(prices.values()))     -> stdout [14, 31, 7]

The judging itself happens back in server.py - here we only run it.
"""

import ast
import contextlib
import io
import json
import sys


def main():
    try:
        payload = json.loads(sys.stdin.read() or '{}')
    except Exception as e:
        print(json.dumps({'error': 'bad payload: %s' % e}))
        return

    source = (payload.get('setup') or '') + '\n' + (payload.get('code') or '') + '\n'
    out = {'stdout': '', 'value': '', 'has_value': False, 'error': ''}

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        out['error'] = 'SyntaxError: %s (line %s)' % (e.msg, e.lineno)
        print(json.dumps(out))
        return

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
                if value is not None:                # print(...) hands back None
                    out['value'] = repr(value)
                    out['has_value'] = True
    except Exception as e:
        out['error'] = '%s: %s' % (type(e).__name__, e)

    out['stdout'] = buf.getvalue()
    print(json.dumps(out))


if __name__ == '__main__':
    main()
