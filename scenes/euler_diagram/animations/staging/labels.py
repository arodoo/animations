# Set name labels inside each set arc, brighter than numbers.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.reveal import text_reveal
from ..domain.timing import Timing
from ..domain.spiral import pos_slot, display_sz_r

# (name, label_text, mid_slot, label_material, delay_frames_after_set_start)
_LABEL_DEFS = [
    ('LblOdds', 'IMPARES',    70,  'MatLblOdds',  160),
    ('LblNat',  'NATURALES',  210, 'MatLblNat',   240),
    ('LblInt',  'ENTEROS',   333,  'MatLblInt',   240),
    ('LblRat',  'RACIONALES', 490, 'MatLblRat',   240),
    ('LblReal', 'REALES',    600,  'MatLblReal',  180),
]


def _inner_pos(slot: int):
    """Position at 85% of slot radius — inside the set's ring."""
    x, y, _ = pos_slot(slot)
    r = math.hypot(x, y)
    a = math.atan2(y, x)
    r2 = r * 0.85
    return r2 * math.cos(a), r2 * math.sin(a), r2


def build_labels(
    t: Timing,
    label_sz: float = 1.0,
) -> List[Dict]:
    """One label per set inside its arc + '0' at origin."""
    starts = [
        t.odds_start, t.nat_start,
        t.int_start, t.rat_start,
        t.real_start,
    ]
    cmds: List[Dict] = []
    for (name, text, slot, mat, delay), s in zip(_LABEL_DEFS, starts):
        x, y, r2 = _inner_pos(slot)
        sz = display_sz_r(r2) * label_sz * 4.0
        cmds += text_reveal(
            name, text, x, y, mat,
            s + delay, sz=sz, extrude=sz * 0.12,
        )
    cmds += text_reveal(
        'Zero', '0', 0.0, 0.0, 'MatLblOdds',
        t.odds_start, sz=0.22, extrude=0.04,
    )
    return cmds
