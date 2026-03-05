# File: scenes/euler_diagram/animations/_labels.py
# Set labels and zero, placed along the spiral.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ._helpers import text_reveal
from ._timing import Timing
from ._spiral import pos, sz_at_r

# (name, text, spiral_idx, mat, delay_after_set_start)
# Indices = midpoints of each set: odds 0-44, nat 45-134,
# int 135-254, rat 255-404, real 405-479
_LABEL_DEFS = [
    ('LblOdds', 'Impares',    22, 'MatOdds', 160),
    ('LblNat',  'Naturales',  90, 'MatNat',  223),
    ('LblInt',  'Enteros',   195, 'MatInt',  215),
    ('LblRat', 'Racionales', 330, 'MatRat',  216),
    ('LblReal', 'Reales',    442, 'MatReal',  92),
]


def _out_pos(idx: int):
    """Outward label position; returns (x, y, r_spiral)."""
    x, y = pos(idx)
    r = math.hypot(x, y)
    a = math.atan2(y, x)
    r2 = r * 1.35
    return r2 * math.cos(a), r2 * math.sin(a), r


_DEFAULT_LABEL_SZ = 1.60


def build_labels(
    t: Timing,
    label_sz: float = _DEFAULT_LABEL_SZ,
) -> List[Dict]:
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
        lbl_sz = sz_at_r(r, label_sz)
        f = s + delay
        cmds += text_reveal(
            name, text, x, y, mat, f,
            sz=lbl_sz,
        )
    cmds += text_reveal(
        'Zero', '0', 0.0, 0.0, 'MatOdds',
        t.odds_start, sz=label_sz, bounce=1.5,
    )
    return cmds
