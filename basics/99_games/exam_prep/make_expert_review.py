# -*- coding: utf-8 -*-
"""
make_expert_review.py  --  build expert.html from draft_expert_questions.py.

Same reviewer as easy/medium (make_easy_review.py) - REVIEW ONLY, nothing
here is judged or wired into the game.

    python make_expert_review.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_easy_review import build  # noqa: E402

QSRC = os.path.join(HERE, 'draft_expert_questions.py')
OUT = os.path.join(HERE, 'expert.html')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build(QSRC, OUT, 'EXPERT')
