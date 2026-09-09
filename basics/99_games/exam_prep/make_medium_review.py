# -*- coding: utf-8 -*-
"""
make_medium_review.py  --  build medium.html from draft_medium_questions.py.

Same reviewer as easy (make_easy_review.py) - REVIEW ONLY, nothing here is
judged or wired into the game. See make_easy_review.py's docstring for how
this works: every solution runs for real, its actual printed output is
what "expected output" shows.

    python make_medium_review.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_easy_review import build  # noqa: E402

QSRC = os.path.join(HERE, 'draft_medium_questions.py')
OUT = os.path.join(HERE, 'medium.html')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build(QSRC, OUT, 'MEDIUM')
