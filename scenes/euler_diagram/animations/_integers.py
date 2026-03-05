# File: scenes/euler_diagram/animations/_integers.py
# Negative integers -1..-120 on the nautilus spiral.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ._helpers import text_reveal
from ._spiral import pos, INT_START, sz_at

_NUMS = list(range(-1, -121, -1))   # 120 negatives
_BASE_SZ = 0.35
_STAGGER = 5
_BOUNCE = 1.3


def build_integers(appear_frame: int) -> List[Dict]:
    """120 negatives, stagger 5f, violet."""
    cmds: List[Dict] = []
    for i, num in enumerate(_NUMS):
        x, y = pos(INT_START + i)
        sz = sz_at(INT_START + i, _BASE_SZ)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Int{i}', str(num),
            x, y, 'MatInt', f,
            sz=sz, bounce=_BOUNCE,
        )
    return cmds
