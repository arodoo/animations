# File: scenes/euler_diagram/animations/_labels.py
# Set labels and zero, placed along the spiral.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ._helpers import text_reveal
from ._timing import Timing
from ._spiral import pos, sz_at_r

# (name, text, spiral_idx, mat, delay_after_set_start)
_LABEL_DEFS = [
    ('LblOdds', 'Impares',     7, 'MatOdds', 160),
    ('LblNat',  'Naturales',  30, 'MatNat',  223),
    ('LblInt',  'Enteros',    65, 'MatInt',  215),
    ('LblRat', 'Racionales', 110, 'MatRat',  216),
    ('LblReal', 'Reales',    147, 'MatReal',  92),
]


def _out_pos(idx: int):
    """Outward label position; returns (x, y, r_spiral)."""
    x, y = pos(idx)
    r = math.hypot(x, y)
    a = math.atan2(y, x)
    r2 = r * 1.75
    return r2 * math.cos(a), r2 * math.sin(a), r


def build_labels(t: Timing) -> List[Dict]:
    """Labels at set midpoints + '0' at center."""
    starts = [
        t.odds_start, t.nat_start,
        t.int_start, t.rat_start,
        t.real_start,
    ]
    cmds: List[Dict] = []
    for entry, s in zip(_LABEL_DEFS, starts):
        name, text, idx, mat, delay = entry
        x, y, r = _out_pos(idx)
        lbl_sz = sz_at_r(r, 0.7)
        f = s + delay
        cmds += text_reveal(
            name, text, x, y, mat, f,
            sz=lbl_sz,
        )
    cmds += text_reveal(
        'Zero', '0', 0.0, 0.0, 'MatOdds',
        t.odds_start, sz=0.7, bounce=1.5,
    )
    return cmds
