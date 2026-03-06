# Act 1: Natural numbers emerge along spiral.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from app.components.text_spawner import (
    spawn_glow_text,
)
from app.components.number_drift import build_drift
from app.components.fractal_layout import spiral_pos

_NUMS = list(range(1, 16))
_STAGGER = 36
_SZ = 0.6
_MAT = 'MatNat'


def build_naturals(
    start: int,
    total: int,
) -> List[Dict]:
    """15 naturals along an Archimedean spiral."""
    cmds: List[Dict] = []
    pts = spiral_pos(
        len(_NUMS), r0=3.0, growth=0.4,
    )
    for i, num in enumerate(_NUMS):
        nm = f'Nat{i}'
        x, y = pts[i]
        f = start + i * _STAGGER
        cmds += spawn_glow_text(
            nm, str(num), x, y, 0.0,
            _MAT, f, sz=_SZ, ext=0.05,
        )
        cmds += build_drift(
            nm, x, y, 0.0,
            f + 60, total, amp=0.12,
        )
    return cmds
