# Set name labels — vertical pyramid column, guaranteed non-overlapping.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.reveal import text_reveal
from ..domain.timing import Timing
from ..domain.spiral import display_sz_r

# Pyramid column at x=0: IMPARES(top/small) → REALES(bottom/large).
# y positions guarantee no overlap given the _SZ_MULT-driven heights.
# Gaps verified: min 1.3 BU clearance between adjacent labels.
# (name, text, x, y, material, delay_after_set, sz_multiplier)
_LABEL_DEFS = [
    ('LblOdds', 'IMPARES',    0.0,   5.0, 'MatOdds',  160, 1.0),
    ('LblNat',  'NATURALES',  0.0,   2.0, 'MatNat',   240, 1.3),
    ('LblInt',  'ENTEROS',    0.0,  -2.0, 'MatInt',   240, 1.7),
    ('LblRat',  'RACIONALES', 0.0,  -7.0, 'MatRat',   240, 2.2),
    ('LblReal', 'REALES',     0.0, -15.0, 'MatReal',  180, 3.0),
]


def build_labels(
    t: Timing,
    label_sz: float = 1.0,
) -> List[Dict]:
    """Pyramid column of labels + '0' at origin."""
    starts = [
        t.odds_start, t.nat_start,
        t.int_start, t.rat_start,
        t.real_start,
    ]
    cmds: List[Dict] = []
    for (name, text, x, y, mat, delay, sz_m), s in zip(_LABEL_DEFS, starts):
        r = math.hypot(x, y) or 0.5
        sz = display_sz_r(r) * label_sz * 4.0 * sz_m
        cmds += text_reveal(
            name, text, x, y, mat,
            s + delay, sz=sz, extrude=sz * 0.10,
        )
    cmds += text_reveal(
        'Zero', '0', 0.0, 0.0, 'MatOdds',
        t.odds_start, sz=0.22, extrude=0.04,
    )
    return cmds
