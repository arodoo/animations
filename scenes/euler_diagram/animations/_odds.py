# File: scenes/euler_diagram/animations/_odds.py
# Odd numbers 1..89 on the nautilus spiral.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ._helpers import text_reveal
from ._spiral import pos, ODDS_START, sz_at

_NUMS = list(range(1, 90, 2))   # 45 odds
_BASE_SZ = 0.40
_STAGGER = 10
_BOUNCE = 1.5


def build_odds(appear_frame: int) -> List[Dict]:
    """45 golden odds, stagger 10f, high bounce."""
    cmds: List[Dict] = []
    for i, num in enumerate(_NUMS):
        x, y = pos(ODDS_START + i)
        sz = sz_at(ODDS_START + i, _BASE_SZ)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Odd{i}', str(num),
            x, y, 'MatOdds', f,
            sz=sz, bounce=_BOUNCE,
        )
    return cmds
