# Set name labels at midpoint of each set, same style as numbers.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.reveal import text_reveal
from ..domain.timing import Timing
from ..domain.spiral import (
    pos_slot, radius_slot, display_sz_r,
    ODDS_START, NAT_START, INT_START, RAT_START, REAL_START,
)

# (name, label_text, mid_slot, material, delay_frames_after_set_start)
# mid_slots recalibrated for TOTAL_SLOTS=700 size-aware packing.
_LABEL_DEFS = [
    ('LblOdds', 'IMPARES',    70,  'MatOdds',  160),
    ('LblNat',  'NATURALES',  210, 'MatNat',   240),
    ('LblInt',  'ENTEROS',   333,  'MatInt',   240),
    ('LblRat',  'RACIONALES', 490, 'MatRat',  240),
    ('LblReal', 'REALES',    600,  'MatReal',  180),
]


def _outer_pos(slot: int):
    """Position 60% further out than the slot, same angle."""
    x, y, _ = pos_slot(slot)
    r = math.hypot(x, y)
    a = math.atan2(y, x)
    r2 = r * 1.60
    return r2 * math.cos(a), r2 * math.sin(a), r


def build_labels(
    t: Timing,
    label_sz: float = 1.0,
) -> List[Dict]:
    """One label per set at midpoint + '0' at origin."""
    starts = [
        t.odds_start, t.nat_start,
        t.int_start, t.rat_start,
        t.real_start,
    ]
    cmds: List[Dict] = []
    for (name, text, slot, mat, delay), s in zip(_LABEL_DEFS, starts):
        x, y, r = _outer_pos(slot)
        sz = display_sz_r(r) * label_sz * 1.4
        cmds += text_reveal(
            name, text, x, y, mat,
            s + delay, sz=sz, extrude=sz * 0.15,
        )
    # '0' at origin appears with first odds number
    cmds += text_reveal(
        'Zero', '0', 0.0, 0.0, 'MatOdds',
        t.odds_start, sz=0.22, extrude=0.04,
    )
    return cmds
