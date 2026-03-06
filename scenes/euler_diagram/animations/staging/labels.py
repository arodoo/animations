# Labels at set midpoints and zero at origin.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.reveal import text_reveal
from ..domain.timing import Timing
from ..domain.spiral import pos, sz_at_r

_LABEL_DEFS = [
    ('LblOdds', 'Impares',    30, 'MatOdds', 180),
    ('LblNat',  'Naturales', 135, 'MatNat',  250),
    ('LblInt',  'Enteros',   300, 'MatInt',  240),
    ('LblRat', 'Racionales', 495, 'MatRat',  250),
    ('LblReal', 'Reales',    660, 'MatReal', 120),
]


def _out_pos(idx: int):
    """Outward label position."""
    x, y = pos(idx)
    r = math.hypot(x, y)
    a = math.atan2(y, x)
    r2 = r * 1.50
    return r2 * math.cos(a), r2 * math.sin(a), r


def build_labels(
    t: Timing,
    label_sz: float = 1.10,
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
            sz=lbl_sz, extrude=0.015,
        )
    cmds += text_reveal(
        'Zero', '0', 0.0, 0.0, 'MatOdds',
        t.odds_start, sz=0.18,
        bounce=1.5, extrude=0.01,
    )
    return cmds
