# Act 2: Rationals flood the gaps.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from app.components.text_spawner import (
    spawn_glow_text,
)
from app.components.number_drift import build_drift
from app.components.fractal_layout import spiral_pos

_FRACS = [
    '1/2', '1/3', '2/3', '1/4', '3/4',
    '1/5', '2/5', '3/5', '4/5', '1/6',
    '5/6', '1/7', '2/7', '3/7', '1/8',
    '3/8', '5/8', '7/8', '1/9', '1/10',
]
_STAGGER = 24
_SZ = 0.4
_MAT = 'MatRat'


def build_rationals(
    start: int,
    total: int,
) -> List[Dict]:
    """20 fractions fill gaps between naturals."""
    cmds: List[Dict] = []
    pts = spiral_pos(
        len(_FRACS),
        r0=2.0, growth=0.3, step=0.35,
    )
    for i, frac in enumerate(_FRACS):
        nm = f'Rat{i}'
        x, y = pts[i]
        f = start + i * _STAGGER
        cmds += spawn_glow_text(
            nm, frac, x, y, 0.0,
            _MAT, f, sz=_SZ, ext=0.04,
        )
        cmds += build_drift(
            nm, x, y, 0.0,
            f + 48, total, amp=0.08,
        )
    return cmds
