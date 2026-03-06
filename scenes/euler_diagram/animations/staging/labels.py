# Set name labels — same material as numbers, adjacent to their arc.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.reveal import text_reveal
from ..domain.timing import Timing
from ..domain.spiral import pos_slot, display_sz_r

# mid_slots calibrated for TOTAL_SLOTS=1000, unclamped advances.
# Approximate slot midpoints: odds(0-85)=42, nat(85-231)=158,
# int(231-462)=347, rat(462-762)=612, real(762-962)=862.
_LABEL_DEFS = [
    ('LblOdds', 'IMPARES',    42,  'MatOdds',  160),
    ('LblNat',  'NATURALES',  158, 'MatNat',   240),
    ('LblInt',  'ENTEROS',   347,  'MatInt',   240),
    ('LblRat',  'RACIONALES', 612, 'MatRat',   240),
    ('LblReal', 'REALES',    862,  'MatReal',  180),
]


def _label_pos(slot: int):
    """Position at 90% of slot radius — adjacent to the arc, inside."""
    x, y, _ = pos_slot(slot)
    r = math.hypot(x, y)
    a = math.atan2(y, x)
    r2 = r * 0.90
    return r2 * math.cos(a), r2 * math.sin(a), r2


def build_labels(
    t: Timing,
    label_sz: float = 1.0,
) -> List[Dict]:
    """One label per set next to its arc + '0' at origin."""
    starts = [
        t.odds_start, t.nat_start,
        t.int_start, t.rat_start,
        t.real_start,
    ]
    cmds: List[Dict] = []
    for (name, text, slot, mat, delay), s in zip(_LABEL_DEFS, starts):
        x, y, r2 = _label_pos(slot)
        sz = display_sz_r(r2) * label_sz * 4.0
        cmds += text_reveal(
            name, text, x, y, mat,
            s + delay, sz=sz, extrude=sz * 0.12,
        )
    cmds += text_reveal(
        'Zero', '0', 0.0, 0.0, 'MatOdds',
        t.odds_start, sz=0.22, extrude=0.04,
    )
    return cmds
